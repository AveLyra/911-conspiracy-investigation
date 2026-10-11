"""Fixed F6–F9 reader reconciliation using the pinned F4/F5 set machinery."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER = HERE / '../force45/compare_force45.py'
HELPER_SHA = '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be'
TARGETS = {'F6-Im2': [205,0,365,88], 'F7-Im1': [220,50,335,88],
           'F7-Im2': [330,0,475,88], 'F8-Im1': [195,10,370,88],
           'F9-Im0': [220,55,325,88], 'F9-Im1': [245,0,375,88]}
CONTEXTS = {'F6-Im2': [203,0,367,88], 'F7-Im1': [218,48,337,88],
            'F7-Im2': [328,0,477,88], 'F8-Im1': [193,8,372,88],
            'F9-Im0': [218,53,327,88], 'F9-Im1': [243,0,377,88]}
ROLES = ('primary', 'peer')


def pin_bytes(raw):
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def pin(path):
    return pin_bytes(path.read_bytes())


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def helper():
    require(pin(HELPER)['sha256'] == HELPER_SHA, 'pinned comparison helper')
    spec = importlib.util.spec_from_file_location('fixed_force45_set_helper', HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Only this imported instance is adapted; the preserved source is unchanged.
    module.TARGETS = TARGETS
    module.CONTEXTS = CONTEXTS
    return module


def validate(data, region, role, h):
    bands = h.validate(data, region, role)
    referenced = set()
    for route, rows in data['routes'].items():
        for row in rows:
            refs = row.get('band_refs', row.get('unassigned_band_refs', []))
            keys = []
            for ref in refs:
                if type(ref) is str:
                    key = (row['x'], ref)
                else:
                    require(type(ref) is dict and set(ref) == {'x','band_id'}, 'reference schema')
                    key = (ref['x'], ref['band_id'])
                require(key not in keys, 'duplicate reference')
                keys.append(key)
                band = bands[row['x']]
                require(route in band.get('candidate_routes', []), 'explicit route-specific uncertainty')
                referenced.add((row['x'],route))
            if row['status'] == 'identity_conflict':
                require(bool(keys), 'route conflict needs referenced material')
            if keys and not(row['core'] or row['fringe']):
                require(row['status'] == 'identity_conflict', 'unassigned route identity stays unresolved')
    for band in bands.values():
        require('candidate_routes' in band, 'explicit candidate route field')
        candidates = band['candidate_routes']
        require(type(candidates) is list and all(v in ('solid','dash') for v in candidates)
                and len(candidates) == len(set(candidates)), 'candidate route labels')
        require(bool(band['core'] or band['fringe']) or not candidates, 'empty band candidates')
        require(band['status'] != 'identity_conflict' or bool(band['core'] or band['fringe']), 'band conflict needs material')
        require(all((band['x'],route) in referenced for route in candidates), 'each candidate route retains its reference')
    return bands


def totals(records):
    return {'entries': len(records),
            'outer_different': sum(bool(r['sets']['outer']['symmetric_difference']) for r in records),
            'class_different': sum(bool(r['sets']['core']['symmetric_difference'] or
                                         r['sets']['fringe']['symmetric_difference']) for r in records)}


def run(region, reading_pins):
    require(region in TARGETS and set(reading_pins) == set(ROLES), 'region and named roles')
    h = helper()
    inputs, readings, dependencies = {}, {}, {}
    for role in ROLES:
        name = f'reader-{region}-{role}.json'
        raw = (HERE / name).read_bytes()
        inputs[name] = pin_bytes(raw)
        require(inputs[name]['sha256'] == reading_pins[role], 'frozen reading changed')
        require(raw == (HERE / f'reader-{region}-{role}-repeat.json').read_bytes(), 'reader repeat')
        data = json.loads(raw)
        readings[role] = data
        source = '../../native-strips01/' + region.split('-')[1] + '.jpg'
        require({'PROTOCOL.md','context01.json','context02.json',source} <= set(data['inputs']), 'required dependency roster')
        for path, expected in data['inputs'].items():
            actual = pin(HERE / path)
            require(actual == expected, 'reader dependency: ' + path)
            dependencies[path] = actual
        script = f'reader-{region}-{role}.py'
        require(pin(HERE / script) == data['script_pin'], 'reader literal script')
        dependencies[script] = data['script_pin']
        if role == 'peer':
            require(pin(HERE/'peer_export.py') == data['expander_pin'], 'peer expansion helper')
            dependencies['peer_export.py'] = data['expander_pin']
        else:
            require('primary_helper.py' in data['inputs'], 'primary expansion helper in dependency roster')
    bands = {role: validate(readings[role], region, role, h) for role in ROLES}
    routes = []
    for route in ('solid','dash'):
        for a, b in zip(readings['primary']['routes'][route], readings['peer']['routes'][route]):
            routes.append({'route': route, 'x': a['x'], 'primary_original': a,
                           'peer_original': b, 'sets': h.comparison(a,b)})
    box = TARGETS[region]
    ink = h.visible_geometry(readings, bands, box[0], box[2])
    context_raw = (HERE / 'context01.json').read_bytes()
    require(context_raw == (HERE / 'context02.json').read_bytes(), 'context repeat')
    context = json.loads(context_raw)
    require(context['target_boxes'][region] == box and context['context_boxes'][region] == CONTEXTS[region], 'context geometry')
    require(context['sources'][region] == region.split('-')[1]+'.jpg' and context['pairs'][region] == region.split('-')[0], 'context identity')
    records = context['cells'][region]
    pixels = {(r['x'],r['y']):r['rgb'] for r in records}
    x0,y0,x1,y1 = CONTEXTS[region]
    require(len(records) == len(pixels) == (x1-x0)*(y1-y0), 'context record count')
    require(set(pixels) == {(x,y) for x in range(x0,x1) for y in range(y0,y1)}, 'context coverage')
    whites = {}
    for role, data in readings.items():
        whites[role] = [{'scope': scope, 'class': label, 'x': row['x'], 'y': y}
                        for scope, rows in list(data['routes'].items()) + [('unassigned',data['unassigned_bands'])]
                        for row in rows for label in ('core','fringe') for y in row[label]
                        if pixels[row['x'],y] == [255,255,255]]
    require(inputs == {name:pin(HERE/name) for name in inputs}, 'readings preserved')
    require(dependencies == {name:pin(HERE/name) for name in dependencies}, 'dependencies preserved')
    return {'status':'native_reader_comparison_not_physical_measurement', 'region_id':region,
            'pair':region.split('-')[0], 'source_image':region.split('-')[1]+'.jpg',
            'input_pins':inputs, 'dependencies':dependencies, 'script_pin':pin(Path(__file__)),
            'helper_pin':pin(HELPER), 'test_pin':pin(HERE/'test_compare_force69.py'),
            'literal_readings':readings, 'route_comparisons':routes, 'visible_ink_comparisons':ink,
            'summary':{'routes':totals(routes), 'visible_ink':totals(ink),
                       'route_status_different':sum(r['primary_original']['status'] != r['peer_original']['status'] for r in routes),
                       'selected_exact_white_cells':whites},
            'limits':['Reader differences are not physical-model errors.',
                      'Common source and methods can correlate reader errors; no independent historical evidence.',
                      'Fragment IDs are local; no seam join, curve containment, physical support or cause finding.'],
            'human_accepted':False, 'physical_support':None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', choices=list(TARGETS), required=True)
    parser.add_argument('--primary-sha', required=True)
    parser.add_argument('--peer-sha', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    require(args.output in [f'comparison-{args.region}-01.json',f'comparison-{args.region}-02.json'], 'fixed output name')
    value = run(args.region, {'primary':args.primary_sha,'peer':args.peer_sha})
    with (HERE/args.output).open('x') as out:
        json.dump(value,out,indent=2,sort_keys=True,allow_nan=False)
        out.write('\n')
    print(json.dumps({'output':pin(HERE/args.output),'summary':value['summary']}))
