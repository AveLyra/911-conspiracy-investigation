"""Append frozen F5/F6 readings; conditional coordinates, not support findings."""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
PRIOR = 'historical-applicability/approach34-extension-2026-10-08/'
CALC = 'historical-applicability/conditional-envelopes-2026-10-08/'
SOURCE = 'native-footprint-pass/force56-remainder/'
REGIONS = {'F5': ('Im3', [310, 0, 425, 88]), 'F6': ('Im1', [270, 55, 340, 88])}
AUTHORITY = {Path(p).resolve() for p in (
    '/Users/admin/docs/911/AGENTS.md', '/Users/admin/docs/911/START-HERE.md',
    '/Users/admin/docs/911/WORKFLOW.md',
    '/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md',
    '/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md',
    '/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md')}
FIXED = {
    PRIOR+'run-v2-01.json': '1c307f8b41d9fb0e1fbe928d4ea1cc177c6bb923ac897ec608fdfae07349a4be',
    PRIOR+'run-v2-02.json': '1c307f8b41d9fb0e1fbe928d4ea1cc177c6bb923ac897ec608fdfae07349a4be',
    PRIOR+'extend.py': '18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0',
    CALC+'calculate.py': '9d3f00efca8cb858b80a2b34c11f8253d2de59c66b46257df9dfc715d73ee89a',
    SOURCE+'compare.py': '81dc892b21e891a9c11d2bc7697d1b936a497a91950584659e04fc718776313a',
    SOURCE+'independent-check.json': '449bdc39b7eaea29cc67fa81a9fcaa0688928dc79f2743e4f33546f873729076',
    SOURCE+'reader-F5-primary.json': '6ce861b44d73e09a88e3d79e754f7f2f41b9458a0baafb1630c22b2de3f2c2b3',
    SOURCE+'reader-F5-peer.json': 'dbed8ae98651c5fc21a4a11e2d97c6897ed609eac809e20b1638e376246de5f4',
    SOURCE+'reader-F6-primary.json': '4e3dab2e3cf358854da349a987e897fbb1f5915f8ee5c2e67e246cfa06da96be',
    SOURCE+'reader-F6-peer.json': 'b1345970d11e24d552e1bb755279f84f2d251db1232e1d4cedc298b02135310e',
}
RESIDUAL = {
    'F5': {
        'remaining_inventory': 'Im3 descent [310,0,425,88] is now annotated separately from prior Im4/Im2 targets. Out-of-target Im3 rise/descent, broader Im4 rise, out-of-box Im2 material, Im5 origin/tail and joins remain pending or unresolved. Qualitative descriptions are not exact complementary masks.',
        'identity_and_topology_limits': 'Prior Im4 blue/red overlap x446-455 and Im2 allocations at x225/286/292 remain. New Im3 contacts, primary-only bands near x391/403 and primary-only bottom clipping at solid x375 retain reader alternatives. Neither shared color nor adjacent strips establish continuation; core/fringe disagreement is not a model discrepancy.',
        'next_evidence_action': 'Retain all three completed local targets separately. Recover or specifically disposition out-of-target Im3 and broader Im4/Im2 material, Im5 origin/tail and joins without repeating the completed Im3 descent or inferring support across contacts.'
    },
    'F6': {
        'remaining_inventory': 'Corrected lower-Im1 broken-crest target [270,55,340,88] is now annotated separately from the Im2 target. Out-of-target Im1 and seam, Im3 irregular shoulder/rise/descent, Im4 rise/descent, Im5 origin/tail, remaining Im2 material and joins remain pending or unresolved. Qualitative descriptions are not exact complementary masks.',
        'identity_and_topology_limits': 'Prior Im2 same-red meeting x260-267 and colored overlap near356 remain. Im1 red/green contact, fringe-only versus core-bearing readings at x288/320 and x325 band/allocation disagreement remain alternatives. No attributed solid inside this Im1 target is not zero force or a missing solid model; the Im2 solid crest is not an automatic seam join.',
        'next_evidence_action': 'Preserve the corrected Im1 attribution and separately completed Im2 pieces. Recover or specifically disposition out-of-target Im1/seam, Im3 shoulder and downstream candidates, Im4/Im5 and remaining Im2/joins; do not repeat the completed lower-Im1 target or infer through-contact support.'
    }
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    def rational(item):
        if isinstance(item, Fraction):
            return str(item)
        raise TypeError('Unexpected JSON value')
    return (json.dumps(value, default=rational, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()


def exact(a, b):
    return encode(a) == encode(b)


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def key(path, root=BASE, allowed=AUTHORITY):
    resolved = path.resolve()
    if resolved not in allowed:
        resolved.relative_to(root.resolve())
    return os.path.relpath(resolved, root.resolve())


def include(pins, path, expected=None, root=BASE, allowed=AUTHORITY):
    name = key(path, root, allowed)
    observed = pin(path)
    if isinstance(expected, str):
        require(observed['sha256'] == expected, 'Changed frozen SHA: '+name)
    elif expected is not None:
        require(type(expected) is dict and set(expected) == {'bytes', 'sha256'}, 'Pin schema')
        require(exact(observed, expected), 'Changed dependency: '+name)
    require(name not in pins or exact(pins[name], observed), 'Conflicting pin: '+name)
    pins[name] = observed
    return name


def closure(roots, pins, root=BASE, allowed=AUTHORITY):
    root = root.resolve()
    queue = [include(pins, p, root=root, allowed=allowed) for p in roots]
    visited = set()
    while queue:
        name = queue.pop(0)
        if name in visited or not name.endswith('.json'):
            continue
        visited.add(name)
        path = root/name
        require(exact(pin(path), pins[name]), 'Changed dependency-map owner')
        data = json.loads(path.read_text())
        require(type(data) is dict, 'Dependency JSON object required')
        if 'inputs_after' in data:
            require(exact(data['inputs'], data['inputs_after']), 'Before/after map differs')
        for field in ('inputs', 'inputs_after', 'input_pins', 'dependencies'):
            if field not in data:
                continue
            require(type(data[field]) is dict, 'Dependency map required')
            for child, expected in data[field].items():
                require(isinstance(child, str), 'Dependency path required')
                queue.append(include(pins, path.parent/child, expected, root, allowed))
        if 'script_pin' in data:
            require(path.name.startswith(('reader-', 'comparison-')), 'Unknown script-pin owner')
            script = path.with_suffix('.py') if path.name.startswith('reader-') else path.parent/'compare.py'
            include(pins, script, data['script_pin'], root, allowed)
        if 'test_pin' in data:
            require(path.name.startswith('comparison-'), 'Unknown test-pin owner')
            include(pins, path.parent/'test_compare.py', data['test_pin'], root, allowed)
    return sorted(visited)


def import_fixed(name):
    require(pin(BASE/name)['sha256'] == FIXED[name], 'Changed method before import')
    spec = importlib.util.spec_from_file_location('force56_extension_'+Path(name).stem, BASE/name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def adapt(original, pair, role, validator, adapter):
    saved = encode(original)
    source, box = REGIONS[pair]
    h, _, a = validator.helpers()
    validator.validate(original, pair+'-'+source, role, h, a)
    routes = {route: [adapter.row_adapter(row, height=88) for row in original['routes'][route]]
              for route in ('solid', 'dash')}
    require(encode(original) == saved, 'Original mutated')
    return routes


def inventory(previous, originals, adapter, pins):
    result = copy.deepcopy(previous)
    for item in result['pairs']:
        pair = item['pair']
        if pair not in REGIONS:
            continue
        source, box = REGIONS[pair]
        require(not any(r['source'] == source and r['target_box'] == box for r in item['completed_footprints']), 'Duplicate target')
        readers = []
        for role in ('primary', 'peer'):
            path = SOURCE+f'reader-{pair}-{role}.json'
            readers.append({'path': path, 'route_records': sum(map(len, originals[path]['routes'].values())),
                            'target_source_field': 'target_box', 'human_accepted_field': False, 'physical_support_field': None})
        item['completed_footprints'].append({'source': source, 'target_box': box.copy(), 'readers': readers})
        item.setdefault('additional_batches', []).append({'report': SOURCE+'report.md', 'verification': SOURCE+'independent-check.json'})
        item.update(RESIDUAL[pair])
    present, missing = [], []
    for item in result['pairs']:
        roles = [set(), set()]
        for region in item['completed_footprints']:
            require(len(region['readers']) == 2, 'Reader roster')
            for index, reader in enumerate(region['readers']):
                name = reader['path']
                require(name in pins and exact(pin(BASE/name), pins[name]), 'Unpinned inventory reader')
                data = originals[name] if name in originals else json.loads((BASE/name).read_text())
                for route, rows in adapter.get_routes(data).items():
                    if any(r['status'] == 'identified_local_fragment' and r.get('core', r.get('core_rows')) for r in rows):
                        roles[index].add(route)
        (present if all(r == {'solid', 'dash'} for r in roles) else missing).append(item['pair'])
    result['counts'] = adapter.count_inventory(result['pairs'])
    result['candidate_presence']['pairs_with_both_style_candidates'] = present
    result['candidate_presence']['pairs_without_both_style_candidates'] = missing
    result['claims'] = [
        {'claim': 'Twenty-one completed local regions preserve forty-two readings and 13,240 route records.',
         'type': 'derived artifact coverage', 'strength': 'A within checked file scope',
         'support': 'Prior inventory plus four frozen F5/F6 originals.',
         'falsifier': 'Missing, duplicated or changed region, reading or record.'},
        copy.deepcopy(previous['claims'][1]), copy.deepcopy(previous['claims'][2])]
    return result


def build():
    before = {}
    for name, sha in FIXED.items():
        include(before, BASE/name, sha)
    prior = json.loads((BASE/(PRIOR+'run-v2-01.json')).read_text())
    require((BASE/(PRIOR+'run-v2-01.json')).read_bytes() == (BASE/(PRIOR+'run-v2-02.json')).read_bytes(), 'Prior repeat differs')
    require(exact(prior['inputs'], prior['inputs_after']), 'Prior map differs')
    for name, expected in prior['inputs'].items():
        include(before, BASE/name, expected)
    require(len(prior['readings']) == 38 and prior['records'] == 12500, 'Prior scope')
    roots = [BASE/(SOURCE+'independent-check.json')]
    roots += [BASE/(SOURCE+f'reader-{pair}-{role}.json') for pair in REGIONS for role in ('primary', 'peer')]
    roots += [BASE/(SOURCE+f'comparison-{pair}-{run}.json') for pair in REGIONS for run in ('01', '02')]
    roots += [BASE/(SOURCE+name) for name in ('context01.json', 'context02.json')]
    nodes = closure(roots, before)
    for name in ('PROTOCOL.md', 'extend.py', 'test_extend.py'):
        include(before, HERE/name)
    # All declared inputs, including helper method hashes, have been checked before imports.
    adapter = import_fixed(PRIOR+'extend.py')
    calc = import_fixed(CALC+'calculate.py')
    validator = import_fixed(SOURCE+'compare.py')
    for path, sha in validator.HELPERS.items():
        name = key(BASE/SOURCE/path)
        require(name in before and before[name]['sha256'] == sha, 'Missing validator helper pin')
    rep = json.loads((BASE/'pypdf-representation01.json').read_text(), parse_float=Fraction)
    strips = {r['name']: calc.geometry.Strip(r['name'], *r['native_dimensions'], r['ctm']) for r in rep['image_invocations']}
    originals, added = {}, []
    for pair, (source, box) in REGIONS.items():
        require((strips[source].width, strips[source].height) == (741, 88), 'Source-specific dimensions')
        for role in ('primary', 'peer'):
            name = SOURCE+f'reader-{pair}-{role}.json'
            original = json.loads((BASE/name).read_text())
            originals[name] = original
            routes = adapt(original, pair, role, validator, adapter)
            rows = calc.process(routes, strips[source], box, 'F')
            added.append({'pair': pair, 'source': source, 'reader_path': name, 'rows': rows,
                          'summary': {'records': len(rows), 'conditional_windows': sum(r['conditional_window'] for r in rows),
                                      'reasons_nonexclusive': dict(Counter(k for r in rows for k in r['reasons']))}})
    inv = inventory(prior['inventory'], originals, adapter, before)
    require(inv['counts'] == {'completed_regions': 21, 'original_readings': 42, 'original_route_records': 13240, 'pairs': 14}, 'Extended coverage')
    for old, new in zip(prior['inventory']['pairs'], inv['pairs']):
        if old['pair'] not in REGIONS:
            require(exact(old, new), 'Unrelated inventory changed')
    readings = copy.deepcopy(prior['readings']) + added
    require(exact(readings[:38], prior['readings']), 'Older reading changed')
    require(sum(r['summary']['records'] for r in added) == 740, 'New record count')
    require(sum(len(r['unassigned_bands']) for r in originals.values()) == 50, 'New band count')
    after = {name: pin(BASE/name) for name in before}
    require(exact(before, after), 'Input changed during integration')
    return {'status': 'conditional_force56_extension_not_accepted_measurement', 'version': 1,
            'inputs': before, 'inputs_after': after, 'new_dependency_json_nodes': nodes,
            'prior_conditional_result': PRIOR+'run-v2-01.json', 'inventory': inv,
            'prior_source_originals': copy.deepcopy(prior['new_source_originals']), 'new_source_originals': originals,
            'readings': readings, 'records': 13240,
            'axis_boxes': copy.deepcopy(prior['axis_boxes']), 'assumptions': copy.deepcopy(prior['assumptions']),
            'conditional_window_counts': {'prior': sum(r['summary']['conditional_windows'] for r in prior['readings']),
                                          'new': sum(r['summary']['conditional_windows'] for r in added),
                                          'total': sum(r['summary']['conditional_windows'] for r in readings)},
            'human_accepted': False, 'common_support': None, 'quantile_targets': None, 'model_discrepancies': None,
            'shared_axis_parameters': True,
            'limits': 'Conditional local windows only; original role serialization, bands and prior results unchanged. No source rereading, seam join, continuous support, independent-error model, model discrepancy or historical cause.'}


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
