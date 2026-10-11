"""Extend conditional graphical preparation; no supported-domain inference."""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
OLD = 'historical-applicability/conditional-envelopes-2026-10-08/'
RECON = 'historical-applicability/footprint-reconciliation-2026-10-08.json'
APP = 'native-footprint-pass/approach34/'
FIXED = {
    RECON: 'ed4a1ded5e53b7d102c9462f5f939883640359da5c0472220a92fbba1b7a354e',
    OLD+'run01.json': '940947030c60d1b5a4d0b1f9ac4f3191db7fb8b355337b47062b796f4ce73678',
    OLD+'run02.json': '940947030c60d1b5a4d0b1f9ac4f3191db7fb8b355337b47062b796f4ce73678',
    OLD+'calculate.py': '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    OLD+'independent-check.json': '18c8ad5d71add639838fa27c8ce8cd0c52470302410bc850da910a296e9c8f6f',
    'historical-applicability/screen.py': 'eab1bc47664a9e4a9176f0f1c79b20c0c3b223e03f64b983c982d74a67433b82',
    'registration_controls.py': '98873f48740f69499f509e1e1db5c425586d25811e83ae9c88c862db7e54bc54',
    APP+'compare.py': 'cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac',
    APP+'verification.json': '8008c29ffaede15900a650c01d43dc40ad3764f4b116433c84f66cc6f21f8829',
    APP+'independent-check.json': 'fd38b2f372166c124fe46e908e9eeef2bfd20f92e4e3e24fb7d1d375a6072c23',
}
RESIDUAL = {
    'E3': {
        'remaining_inventory': 'Im10 approach [195,35,365,92] and terminal [365,30,690,60] have completed annotations and remain separate. Crowded Im11 origin, Im10/Im11 boundary, and earlier or out-of-box Im10 portions retain pending recovery or disposition. Qualitative descriptions are not exact complementary masks.',
        'identity_and_topology_limits': 'Early mixed-color attribution and the later shared black edge remain disputed inside the completed approach. Adjacency at x365 does not establish continuity. Only the older terminal target lacks a separately attributed solid footprint; hidden continuation and termination remain unresolved alternatives.',
        'next_evidence_action': 'Retain the completed approach and terminal separately. Recover or specifically disposition the Im11 origin, earlier/out-of-box Im10 material and boundary; do not repeat completed annotation or infer a through-contact path.'
    },
    'E4': {
        'remaining_inventory': 'Im10 approach [195,0,440,92] and Im9 terminal [440,72,690,92] have completed annotations and remain separate. Im11 origin, earlier/out-of-box portions, Im9 bend/transition outside the terminal target, and Im10/Im11 and Im9/Im10 joins retain pending recovery or disposition. Qualitative descriptions are not exact complementary masks.',
        'identity_and_topology_limits': 'The Im10 approach has locally attributed solid and dash pieces, unresolved contacts and source-edge clipping. Top-edge selections and later empty records establish neither termination nor continuation. The older Im9 terminal still lacks a separately attributed solid footprint and retains its x481-485 dash-attribution disagreement.',
        'next_evidence_action': 'Retain completed Im10 and Im9 targets without a seam join. Recover or specifically disposition earlier/out-of-box material, the Im9 bend/transition and origins/joins; do not repeat completed annotation or treat clipping as an endpoint.'
    }
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def load(name):
    return json.loads((BASE/name).read_text())


def import_pinned(name, expected):
    require(pin(BASE/name)['sha256'] == expected, 'Changed method before import: '+name)
    spec = importlib.util.spec_from_file_location('extension_'+Path(name).stem, BASE/name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def row_adapter(raw, height=92):
    """Exact membership rename on a copy, never silently accept another schema."""
    require(not ({'column', 'core_rows', 'fringe_rows', 'fragments', 'band_refs'} & set(raw)),
            'Ambiguous membership/record aliases')
    require(type(raw['x']) is int and raw['x'] >= 0, 'Invalid column')
    members = raw['fragment_membership']
    require(type(members) is list, 'List membership required')
    occupied, unions, ids = set(), {'core': set(), 'fringe': set()}, set()
    for entry in [raw]+members:
        for label in ('core', 'fringe'):
            rows = entry[label]
            require(type(rows) is list and all(type(y) is int and 0 <= y < height for y in rows)
                    and rows == sorted(set(rows)), 'Invalid member rows')
        require(not set(entry['core']) & set(entry['fringe']), 'Overlapping classes')
    for member in members:
        key = member['fragment_id']
        require(isinstance(key, str) and key.strip() and key not in ids, 'Duplicate/invalid member ID')
        ids.add(key)
        selected = set(member['core']) | set(member['fringe'])
        require(not occupied & selected, 'Overlapping member cells')
        occupied |= selected
        for label in unions:
            unions[label].update(member[label])
    require(all(unions[label] == set(raw[label]) for label in unions), 'Lost fragment membership')
    copied = copy.deepcopy(raw)
    copied['fragments'] = copied.pop('fragment_membership')
    return copied


def adapt_original(original, validator):
    snapshot = copy.deepcopy(original)
    h, v = validator.helpers()
    validator.validate(original, original['pair']+'-Im10', original['reader'], h, v)
    routes = {route: [row_adapter(row) for row in original['routes'][route]]
              for route in ('solid', 'dash')}
    require(original == snapshot, 'Original mutated during validation/adaptation')
    return routes


def get_routes(data):
    if 'routes' in data:
        return data['routes']
    return {route: [r for r in data['observations'] if r['route'] == route]
            for route in ('solid', 'dash')}


def count_inventory(pairs):
    return {
        'completed_regions': sum(len(p['completed_footprints']) for p in pairs),
        'original_readings': sum(len(r['readers']) for p in pairs for r in p['completed_footprints']),
        'original_route_records': sum(q['route_records'] for p in pairs for r in p['completed_footprints'] for q in r['readers']),
        'pairs': len(pairs)
    }


def extend_inventory(previous, originals):
    pairs = copy.deepcopy(previous['pairs'])
    for pair in pairs:
        name = pair['pair']
        if name not in RESIDUAL:
            continue
        readers = []
        for role in ('primary', 'peer'):
            path = APP+f'reader-{name}-{role}.json'
            original = originals[path]
            readers.append({'path': path, 'route_records': sum(map(len, original['routes'].values())),
                            'target_source_field': 'target_box', 'human_accepted_field': False,
                            'physical_support_field': None})
        target = originals[readers[0]['path']]['target_box']
        require(not any(r['source']=='Im10' and r['target_box']==target for r in pair['completed_footprints']),
                'Duplicate approach region')
        pair['completed_footprints'].append({'source': 'Im10', 'target_box': target, 'readers': readers})
        pair['additional_batches'] = [{'report': APP+'report.md', 'verification': APP+'verification.json'}]
        pair.update(RESIDUAL[name])
    present, missing = [], []
    for pair in pairs:
        by_role = [set(), set()]
        for region in pair['completed_footprints']:
            require(len(region['readers']) == 2, 'Paired reader roster')
            for index, reader in enumerate(region['readers']):
                path = reader['path']
                data = originals[path] if path in originals else load(path)
                for route, records in get_routes(data).items():
                    if any(r['status']=='identified_local_fragment' and r.get('core', r.get('core_rows')) for r in records):
                        by_role[index].add(route)
        (present if all(s == {'solid', 'dash'} for s in by_role) else missing).append(pair['pair'])
    return {'pairs': pairs, 'counts': count_inventory(pairs),
            'candidate_presence': {
                'criterion': previous['annotation_candidate_presence']['criterion'],
                'pairs_with_both_style_candidates': present, 'pairs_without_both_style_candidates': missing,
                'limits': 'Presence only; neither common support nor accepted identity, continuity, enclosure or model accuracy. Older E3/E4 terminal limitations and F7 Im1 missing dash remain local.'},
            'preserved_corrections': copy.deepcopy(previous['preserved_corrections']),
            'acceptance': copy.deepcopy(previous['acceptance']),
            'claims': [
                {'claim': 'Nineteen completed local regions preserve thirty-eight original readings and 12,500 route records.',
                 'type': 'derived artifact coverage', 'strength': 'A within checked file scope',
                 'support': 'Pinned previous inventory plus four approach originals; complete target/route checks.',
                 'falsifier': 'Missing or duplicated region, reader or route record.'},
                {'claim': 'Both styles have local candidates in all fourteen pairs under the unchanged candidate-presence criterion.',
                 'type': 'derived annotation-label presence', 'strength': 'A for this narrow label count, not identity accuracy',
                 'support': 'All original files; complete presence scan. New E3/E4 approaches supply local solid candidates absent in old terminal targets.',
                 'falsifier': 'A role/style lacks an identified core-bearing record in all completed regions of a pair.'},
                {'claim': 'Full supported-domain disposition, common support and selected human curve review remain incomplete.',
                 'type': 'readiness finding', 'strength': 'B within the checked dependency record',
                 'support': 'Retained outside-target obligations, conditional assumptions and unchanged acceptance fields.',
                 'falsifier': 'A completed source-specific support record and the required attributable human sample responses.'}
            ]}


def build():
    before = {}

    def include(name, expected=None):
        value = pin(BASE/name)
        if isinstance(expected, str):
            require(value['sha256'] == expected, 'Changed input: '+name)
        elif expected is not None:
            require(value == expected, 'Changed input: '+name)
        if name in before:
            require(before[name] == value, 'Inconsistent input pin: '+name)
        before[name] = value

    for name, expected in FIXED.items():
        include(name, expected)
    prior = load(OLD+'run01.json')
    require((BASE/(OLD+'run01.json')).read_bytes() == (BASE/(OLD+'run02.json')).read_bytes(), 'Prior repeats differ')
    require(prior['inputs'] == prior['inputs_after'], 'Prior pin receipt differs')
    for name, expected in prior['inputs'].items():
        include(name, expected)
    rec = load(RECON)
    require(len(prior['readings']) == 34 and prior['records'] == 10840, 'Prior scope')
    manifest = load(APP+'verification.json')
    for field in ('source_sha256', 'artifact_sha256'):
        for name, sha in manifest[field].items():
            resolved = (BASE/APP/name).resolve().relative_to(BASE)
            include(str(resolved), sha)
    for name in ('PROTOCOL.md', 'extend.py', 'test_extend.py'):
        include(str((HERE/name).relative_to(BASE)))
    calc = import_pinned(OLD+'calculate.py', FIXED[OLD+'calculate.py'])
    validator = import_pinned(APP+'compare.py', FIXED[APP+'compare.py'])
    for name, sha in validator.HELPERS.items():
        include(str((BASE/APP/name).resolve().relative_to(BASE)), sha)
    representation = json.loads((BASE/'pypdf-representation01.json').read_text(), parse_float=Fraction)
    strips = {r['name']: calc.geometry.Strip(r['name'], *r['native_dimensions'], r['ctm'])
              for r in representation['image_invocations']}
    originals, new_readings = {}, []
    for pair in ('E3', 'E4'):
        for role in ('primary', 'peer'):
            path = APP+f'reader-{pair}-{role}.json'
            original = load(path)
            originals[path] = original
            routes = adapt_original(original, validator)
            rows = calc.process(routes, strips['Im10'], original['target_box'], 'E')
            new_readings.append({'pair': pair, 'source': 'Im10', 'reader_path': path, 'rows': rows,
                'summary': {'records': len(rows), 'conditional_windows': sum(r['conditional_window'] for r in rows),
                            'reasons_nonexclusive': dict(Counter(reason for r in rows for reason in r['reasons']))}})
    inventory = extend_inventory(rec, originals)
    require(inventory['counts'] == {'completed_regions': 19, 'original_readings': 38,
                                   'original_route_records': 12500, 'pairs': 14}, 'Extended scope')
    require(all(a == b for a,b in zip(rec['pairs'], inventory['pairs']) if a['pair'] not in RESIDUAL),
            'Unrelated pair modified')
    readings = copy.deepcopy(prior['readings']) + new_readings
    require(readings[:34] == prior['readings'], 'Prior reading changed')
    total = sum(r['summary']['records'] for r in readings)
    require(total == 12500 and len(new_readings) == 4, 'Extended records')
    after = {name: pin(BASE/name) for name in before}
    require(before == after, 'Input changed during extension')
    return {
        'status': 'conditional_preparation_extension_not_accepted_measurement',
        'inputs': before, 'inputs_after': after,
        'prior_inventory': RECON, 'prior_conditional_result': OLD+'run01.json',
        'inventory': inventory, 'new_source_originals': originals, 'readings': readings,
        'axis_boxes': copy.deepcopy(prior['axis_boxes']), 'records': total,
        'assumptions': copy.deepcopy(prior['assumptions']),
        'conditional_window_counts': {
            'prior': sum(r['summary']['conditional_windows'] for r in prior['readings']),
            'new': sum(r['summary']['conditional_windows'] for r in new_readings),
            'total': sum(r['summary']['conditional_windows'] for r in readings)},
        'human_accepted': False, 'common_support': None, 'quantile_targets': None,
        'model_discrepancies': None, 'shared_axis_parameters': True,
        'limits': 'Conditional marginal windows only. New source originals and all old decisions preserved. No image rereading, seam join, continuous support, independent-error model, model discrepancy or historical cause.'}


def encode(value):
    def rational(item):
        if isinstance(item, Fraction):
            return str(item)
        raise TypeError('Unexpected JSON value')
    return (json.dumps(value, default=rational, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def save(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=('run01', 'run02'))
    args = parser.parse_args()
    target = HERE/(args.run+'.json')
    if target.exists():
        raise FileExistsError('Existing output preserved')
    result = build()
    save(target, encode(result))
    print(json.dumps({'output': pin(target), 'counts': result['inventory']['counts'],
                      'windows': result['conditional_window_counts'], 'pins': len(result['inputs'])}))
