"""F6 Im3 reading reconciliation and shared-source F5 attribution audit."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGION = 'F6-Im3'
TARGETS = {REGION: [145, 0, 440, 88]}
CONTEXTS = {REGION: [143, 0, 442, 88]}
HELPERS = {
    '../force56-remainder/compare.py': '81dc892b21e891a9c11d2bc7697d1b936a497a91950584659e04fc718776313a',
    '../force45/compare_force45.py': '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
    '../force69/compare_force69.py': 'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
    '../approach34/compare.py': 'cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac',
}
OLD_PINS = {
    'primary': '6ce861b44d73e09a88e3d79e754f7f2f41b9458a0baafb1630c22b2de3f2c2b3',
    'peer': 'dbed8ae98651c5fc21a4a11e2d97c6897ed609eac809e20b1638e376246de5f4',
}
ROLES = ('primary', 'peer')
SCOPES = ('solid', 'dash', 'unassigned')
MAIN_CHARTER = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md')


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem+'_'+path.parent.name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def helpers():
    for name, sha in HELPERS.items():
        require(pin(HERE/name)['sha256'] == sha, 'helper pin '+name)
    old = load(HERE/'../force56-remainder/compare.py')
    old.TARGETS = TARGETS
    old.CONTEXTS = CONTEXTS
    h, v, a = old.helpers()
    return old, h, v, a


def validate(data, role, helpers_used=None):
    old, h, _, a = helpers_used or helpers()
    require(role in ROLES and data['reader'] == role, 'exact reader role; no legacy alias')
    require(type(data['target_box']) is list and all(type(n) is int for n in data['target_box']), 'integer target geometry')
    require(type(data['context_box']) is list and all(type(n) is int for n in data['context_box']), 'integer context geometry')
    coverage = data['coverage']
    require({'full_context_inspected', 'raw_context_cells', 'raw_blocks', 'actual_views', 'prior_knowledge', 'uncompleted_context'} <= set(coverage), 'standard actual coverage fields')
    require(bool(coverage['actual_views']) and bool(coverage['prior_knowledge']), 'view and prior-knowledge record')
    row_fields = [key for key in ('rows', 'rows_covered', 'rows_inspected') if key in coverage]
    require(bool(row_fields) and all(type(coverage[key]) is list and
            all(type(n) is int for n in coverage[key]) and coverage[key] == [0, 87]
            for key in row_fields), 'explicit consistent inclusive row coverage')
    base_fields = {'x', 'core', 'fringe', 'fragment_id', 'fragment_membership', 'status', 'reason', 'boundary_flags', 'unassigned_band_refs'}
    for records in data['routes'].values():
        require(all(set(row) == base_fields for row in records), 'exact route fields')
    for band in data['unassigned_bands']:
        wanted = base_fields | {'band_id', 'candidate_routes'}
        require(set(band) == wanted or (role == 'primary' and set(band) == wanted-{'unassigned_band_refs'}), 'declared band fields only')
        require('unassigned_band_refs' not in band or band['unassigned_band_refs'] == [], 'no band-to-band reference')
    return old.validate(data, REGION, role, h, a)


def collect(path, expected, deps):
    path = path.resolve()
    name = os.path.relpath(path, HERE)
    require(pin(path) == expected, 'dependency '+name)
    if name in deps:
        require(deps[name] == expected, 'conflicting dependency '+name)
        return
    deps[name] = expected
    if path.suffix == '.json':
        obj = json.loads(path.read_text())
        if isinstance(obj, dict) and isinstance(obj.get('inputs'), dict):
            for child, value in obj['inputs'].items():
                collect(path.parent/child, value, deps)


def selected(data, scope, label):
    records = data['unassigned_bands'] if scope == 'unassigned' else data['routes'][scope]
    labels = ('core', 'fringe') if label == 'outer' else (label,)
    return {(r['x'], y) for r in records for cls in labels for y in r[cls]}


def cross_pair(new, prior):
    comparisons = []
    for role6 in ROLES:
        for role5 in ROLES:
            intersections = []
            for scope6 in SCOPES:
                for scope5 in SCOPES:
                    cells = {}
                    for label6, label5 in [('core', 'core'), ('core', 'fringe'), ('fringe', 'core'), ('fringe', 'fringe'), ('outer', 'outer')]:
                        key = 'outer' if label6 == 'outer' else label6+'_'+label5
                        cells[key] = [list(p) for p in sorted(selected(new[role6], scope6, label6) & selected(prior[role5], scope5, label5))]
                    intersections.append({'f6_scope': scope6, 'f5_scope': scope5, 'cells': cells})
            comparisons.append({'f6_reader': role6, 'f5_reader': role5, 'intersections': intersections})
    return comparisons


def run(reading_pins):
    require(set(reading_pins) == set(ROLES), 'both explicitly frozen readers')
    modules = helpers()
    _, h, v, _ = modules
    deps = {}
    for name in list(HELPERS) + ['PROTOCOL.md', 'READERS.md', 'CONSUMER-COMPATIBILITY.md', 'context01.json', 'context02.json', 'compare.py', 'test_compare.py', '../force56-remainder/context01.json']:
        collect(HERE/name, pin(HERE/name), deps)
    require((HERE/'../../../CHARTER.md').read_bytes() == MAIN_CHARTER.read_bytes(), 'worktree charter differs from controlling main')
    collect(MAIN_CHARTER, pin(MAIN_CHARTER), deps)
    readings, bands, input_pins, prior = {}, {}, {}, {}
    for role in ROLES:
        path = HERE/f'reader-{role}.json'
        input_pins[path.name] = pin(path)
        require(input_pins[path.name]['sha256'] == reading_pins[role], 'frozen reader hash')
        data = json.loads(path.read_text())
        readings[role] = data
        require({'PROTOCOL.md', 'READERS.md', 'context01.json', 'context02.json', '../../native-strips01/Im3.jpg'} <= set(data['inputs']), 'required reader dependencies')
        collect(path, input_pins[path.name], deps)
        script = HERE/f'reader-{role}.py'
        collect(script, data['script_pin'], deps)
        require(load(script).build() == data, 'literal expansion reproduction')
        bands[role] = validate(data, role, modules)
        old_path = HERE/f'../force56-remainder/reader-F5-{role}.json'
        require(pin(old_path)['sha256'] == OLD_PINS[role], 'frozen prior F5 hash')
        input_pins[f'../force56-remainder/reader-F5-{role}.json'] = pin(old_path)
        old_data = json.loads(old_path.read_text())
        require(old_data['region_id'] == 'F5-Im3' and old_data['source'] == 'Im3.jpg' and old_data['target_box'] == [310, 0, 425, 88], 'prior same-source geometry')
        collect(old_path, pin(old_path), deps)
        old_script = old_path.with_suffix('.py')
        collect(old_script, old_data['script_pin'], deps)
        require(load(old_script).build() == old_data, 'prior literal reproduction')
        prior[role] = old_data
    raw = (HERE/'context01.json').read_bytes()
    require(raw == (HERE/'context02.json').read_bytes(), 'context repeat')
    context = json.loads(raw)
    require(context['target_boxes'] == {'F6': TARGETS[REGION]} and context['context_boxes'] == {'F6': CONTEXTS[REGION]}, 'context geometry')
    require(context['sources'] == {'F6': 'Im3.jpg'} and context['source_size'] == [741, 88], 'context source')
    pixels = {(r['x'], r['y']): r['rgb'] for r in context['cells']['F6']}
    require(len(context['cells']['F6']) == len(pixels) == 26312, 'context count')
    require(set(pixels) == {(x, y) for x in range(143, 442) for y in range(88)}, 'context coordinates')
    old_context = json.loads((HERE/'../force56-remainder/context01.json').read_text())['cells']['F5']
    require(len(old_context) == 10472 and all(pixels[r['x'], r['y']] == r['rgb'] for r in old_context), 'exact old-context overlap')
    routes = []
    for route in ('solid', 'dash'):
        for r, s in zip(readings['primary']['routes'][route], readings['peer']['routes'][route]):
            routes.append({'route': route, 'x': r['x'], 'primary_original': r, 'peer_original': s, 'sets': h.comparison(r, s)})
    geometry = []
    for x in range(145, 440):
        selections = []
        for role in ROLES:
            records = [readings[role]['routes'][r][x-145] for r in ('solid', 'dash')] + bands[role].get(x, [])
            selections.append({label: sorted({y for r in records for y in r[label]}) for label in ('core', 'fringe')})
        geometry.append({'x': x, 'primary_unassigned_originals': bands['primary'].get(x, []), 'peer_unassigned_originals': bands['peer'].get(x, []), 'sets': h.comparison(*selections)})
    whites = {role: [{'scope': scope, 'class': label, 'x': r['x'], 'y': y}
                    for scope, rs in [(r, data['routes'][r]) for r in ('solid', 'dash')]+[('unassigned', data['unassigned_bands'])]
                    for r in rs for label in ('core', 'fringe') for y in r[label]
                    if pixels[r['x'], y] == [255, 255, 255]] for role, data in readings.items()}
    require(deps == {name: pin(HERE/name) for name in deps}, 'all dependencies unchanged')
    return {'status': 'native_ink_reconciliation_not_physical_measurement', 'pair': 'F6', 'region_id': REGION,
            'input_pins': input_pins, 'dependencies': deps, 'script_pin': pin(Path(__file__)), 'test_pin': pin(HERE/'test_compare.py'),
            'literal_readings': readings, 'prior_F5_readings': prior,
            'literal_reproductions': {role: True for role in ROLES},
            'route_comparisons': routes, 'visible_ink_comparisons': geometry,
            'cross_pair_comparisons': cross_pair(readings, prior), 'exact_old_context_overlap_cells': 10472,
            'summary': {'routes': v.totals(routes), 'visible_ink': v.totals(geometry),
                        'status_different': sum(r['primary_original']['status'] != r['peer_original']['status'] for r in routes),
                        'selected_exact_white_cells': whites},
            'human_accepted': False, 'physical_support': None,
            'limits': ['Same source pixels are not independent evidence.',
                       'Cross-pair cell intersections are attribution-conflict candidates, not physical-curve coincidence.',
                       'Original reader-local identities, bands, statuses and class differences are preserved; no voting or averaging.',
                       'No seam join, support union, physical envelope, human acceptance or cause finding.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--primary-sha', required=True)
    p.add_argument('--peer-sha', required=True)
    p.add_argument('--run', choices=['01', '02'], required=True)
    args = p.parse_args()
    value = run({'primary': args.primary_sha, 'peer': args.peer_sha})
    out = HERE/f'comparison{args.run}.json'
    with out.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
    print(json.dumps({'output': pin(out), 'summary': value['summary']}, sort_keys=True))
