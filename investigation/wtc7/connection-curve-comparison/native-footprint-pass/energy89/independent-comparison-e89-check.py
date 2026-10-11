"""Separate E8/E9 computation audit; never imports or executes producer code."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import sys
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
BOXES = {'E8': [535, 54, 690, 86], 'E9': [530, 30, 690, 56]}
CONTEXTS = {'E8': [533, 52, 692, 88], 'E9': [528, 28, 692, 58]}
FROZEN = {
    'reader-E8-root.py': '4c133cead7a17d0e30d80d8366940d1fa58d2a9da780a3f898b02209d8974cb3',
    'reader-E8-root.json': 'd207e809439d24e7ab88e2d61872f36a91cac027ed3b3af3aa86d97e7effcc16',
    'reader-E8-independent.py': '7952536247d8e6b3f3b12196ee458757926a9090a16fd4ee66074ee26fb9ffef',
    'reader-E8-independent.json': '65d92369ea0d766f8260ac52f9b7c775cb09e732e76a6977b4ab406f498861c5',
    'reader-E9-root.py': '8639493c8788d4f32906776a85931869d5a9947437929a3b83d583cd8dd76c8f',
    'reader-E9-root.json': '5c3a935c553215d364b1bb394ffe93e2d394bd329b63ba543157c8fc1ee44958',
    'reader-E9-independent.py': '5c8f6171832029f4c45fb937a31a80bbe734f56f0143487765f615299715444a',
    'reader-E9-independent.json': '0f1df29307604fa6a3aa04b6b1bc2c5422e284a7542b67415aad4e5565d71dc7',
    'context-independent-check.py': '8d6037c87381860982b79a8e75952a5106d2dd222a4af4e1ebbc87262b38f5a7',
    'context-independent-check.json': 'b1030a355f46c167433c236dff6082f5495420b08de80c068b12bd176a3714f5',
    'context-independent-check-repeat.json': 'b1030a355f46c167433c236dff6082f5495420b08de80c068b12bd176a3714f5',
    '../energy345/independent-comparison-e45-check01.json': '9c0136651ce958fb794ed1c333e0e5ba8a2c5bd1921c2ea4e5d84e0e17f9bd1b',
    '../energy345/independent-comparison-e45-check02.json': '9c0136651ce958fb794ed1c333e0e5ba8a2c5bd1921c2ea4e5d84e0e17f9bd1b',
    'compare_e89.py': '55010eeb6fa8d726523d3ca63455d54ff0c90744a7b1f613b610a4afb4e5de36',
    'test_compare_e89.py': 'ab9bc25f5afd3d41da2cafde3cf3c5242a610b76f0cebe2f45c31df35c44f1dc',
    'comparison-E8-01.json': '38ae2b48756b580947f473afd9dc64924f1451f4c318c662372fe10ebb4e8674',
    'comparison-E8-02.json': '38ae2b48756b580947f473afd9dc64924f1451f4c318c662372fe10ebb4e8674',
    'comparison-E9-01.json': '8b5e7ed6f72f43dbec70354f39f1bfb8545925ec8c0fb853f292b2e6b11c28b7',
    'comparison-E9-02.json': '8b5e7ed6f72f43dbec70354f39f1bfb8545925ec8c0fb853f292b2e6b11c28b7',
}
OPS = ('intersection', 'union', 'root_only', 'peer_only', 'symmetric_difference')
STATUSES = ('identified_local_fragment', 'fringe_only', 'no_attributable_cells', 'identity_conflict', 'boundary_truncated')


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read(name):
    return json.loads((HERE / name).read_text())


def normalize(value):
    return json.loads(json.dumps(value, allow_nan=False))


def constants(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result


def literal(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        require(node.id in env, 'known literal metadata name ' + node.id)
        return env[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal(v, env) for v in node.elts]
    if isinstance(node, ast.Dict):
        require(all(k is not None for k in node.keys), 'no dictionary unpack')
        return {literal(k, env): literal(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict':
        require(not node.args and all(k.arg for k in node.keywords), 'literal dict keywords only')
        return {k.arg: literal(k.value, env) for k in node.keywords}
    raise AssertionError('nonliteral expression ' + ast.dump(node))


def function(tree, name):
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    require(len(matches) == 1, 'unique function ' + name)
    return matches[0]


def fields(tree):
    found = [n.value for n in function(tree, 'build').body if isinstance(n, ast.Return)]
    require(len(found) == 1, 'one top-level build return')
    node = found[0]
    if isinstance(node, ast.Dict):
        return {ast.literal_eval(k): v for k, v in zip(node.keys, node.values)}
    require(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict', 'return literal dict')
    return {k.arg: k.value for k in node.keywords}


def assigned(tree, fname, target, env):
    found = [n.value for n in ast.walk(function(tree, fname)) if isinstance(n, ast.Assign)
             and any(ast.unparse(t) == target for t in n.targets)]
    require(len(found) == 1, 'unique literal assignment ' + target)
    return literal(found[0], env)


def note(tree, prefix):
    values = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) is str and node.value.startswith(prefix) and node.value not in values:
            values.append(node.value)
    require(len(values) == 1, 'one literal note ' + prefix)
    return values[0]


def flags(pair, x, selected):
    x0, y0, x1, y1 = BOXES[pair]
    if not selected:
        return []
    return [name for name, present in [('target_left', x == x0), ('target_right', x == x1 - 1),
                                       ('target_top', y0 in selected), ('target_bottom', y1 - 1 in selected)] if present]


def row(pair, who, x, core, fringe, fid, status, text, refs):
    return {'x': x, 'core': list(core), 'fringe': list(fringe), 'fragment_id': fid, 'status': status,
            'note': text, 'boundary_flags': flags(pair, x, core + fringe),
            'band_refs' if who == 'root' else 'unassigned_band_refs': refs}


def expand_runs(pair, runs, default_id=None):
    """Literal source order is preserved separately; output is indexed by x.

    Source tables need not be sorted. Bounds and overlaps are checked, and no
    table run is interpolated or merged with a different local fragment.
    """
    x0, _, x1, _ = BOXES[pair]
    indexed = {}
    for run in runs:
        require(type(run) in (list, tuple) and len(run) in (4, 5), 'manual run shape')
        start, end, core, fringe = run[:4]
        require(type(start) is int and type(end) is int and x0 <= start <= end < x1, 'manual run bounds')
        fid = run[4] if len(run) == 5 else default_id
        require(type(fid) is str and bool(fid), 'manual fragment identity')
        for x in range(start, end + 1):
            require(x not in indexed, 'manual runs do not overlap')
            indexed[x] = (list(core), list(fringe), fid)
    return indexed


def expand_root(pair, tree, env):
    maps = {route: expand_runs(pair, env[key]) for route, key in
            [('solid', 'SOLID'), ('dash', 'DASH'), ('band', 'UNASSIGNED')]}
    routes, bands = {'solid': [], 'dash': []}, []
    x0, _, x1, _ = BOXES[pair]
    for x in range(x0, x1):
        uc, uf, bid = maps['band'].get(x, ([], [], None))
        bands.append(row(pair, 'root', x, uc, uf, bid, 'identity_conflict' if bid else 'no_attributable_cells',
                         note(tree, 'Close traces or pale interbody' if pair == 'E8' else 'Pale interbody material retained'), []))
        for route in ('solid', 'dash'):
            core, fringe, fid = maps[route].get(x, ([], [], None))
            status = ('boundary_truncated' if flags(pair, x, core + fringe) else
                      'identified_local_fragment' if core else 'fringe_only') if fid else 'identity_conflict'
            routes[route].append(row(pair, 'root', x, core, fringe, fid, status,
                note(tree, 'Manual visible-ink/style reading.' if pair == 'E8' else 'Full-strip continuous/broken style,'),
                [bid] if not fid and bid else []))
    return routes, bands


def expand_peer_e8(tree, env):
    maps = {'solid': expand_runs('E8', env['SOLID'], 'E8-independent-solid'), 'dash': {}}
    for i, pieces in enumerate(env['DASH'], 1):
        local = expand_runs('E8', pieces, 'E8-independent-dash-' + str(i).zfill(2))
        require(not any(x in maps['dash'] for x in local), 'separate dash bodies disjoint')
        maps['dash'].update(local)
    routes = {'solid': [], 'dash': []}
    bands = assigned(tree, 'build', 'bands', env)
    for route in ('solid', 'dash'):
        for x in range(535, 690):
            core, fringe, fid = maps[route].get(x, ([], [], None))
            status = 'boundary_truncated' if flags('E8', x, core + fringe) else 'identified_local_fragment' if core else 'no_attributable_cells'
            text = note(tree, 'Locally identifiable cyan stroke:' if core else 'Inspected pale interbody material')
            # Literal pre-export contact decision, not a correction inferred from RGB.
            if x == 535:
                fringe = assigned(tree, 'build', "routes['" + route + "'][0]['fringe']", env)
                refs = assigned(tree, 'build', "routes[k][0]['unassigned_band_refs']", env)
            else:
                refs = []
            routes[route].append(row('E8', 'independent', x, core, fringe, fid, status, text, refs))
    return routes, bands


def expand_peer_e9(tree, env):
    maps = {'solid': expand_runs('E9', env['SOLID_RUNS'], 'E9i-solid01'),
            'dash': expand_runs('E9', env['DASH_RUNS']), 'band': expand_runs('E9', env['UNASSIGNED_RUNS'])}
    routes, bands = {'solid': [], 'dash': []}, []
    for x in range(530, 690):
        uc, uf, local = maps['band'].get(x, ([], [], None))
        bid = 'E9i-' + local if local else None
        bands.append({'x': x, 'core': uc, 'fringe': uf,
            'status': 'identity_conflict' if uc or uf else 'no_attributable_cells', 'fragment_id': bid,
            'model': None, 'boundary_flags': flags('E9', x, uc + uf),
            'note': note(tree, 'Pale interstitial purple material' if bid else 'No separate unassigned cells'),
            'competing_identities': ['solid-edge material', 'dash-edge material', 'mixed or compression/background material'] if bid else []})
        refs = [{'band_id': bid, 'x': x}] if bid else []
        for route in ('solid', 'dash'):
            core, fringe, fid = maps[route].get(x, ([], [], None))
            if route == 'dash' and fid:
                fid = 'E9i-' + fid
            selected = core + fringe
            if selected:
                status = 'boundary_truncated' if flags('E9', x, selected) else 'identified_local_fragment' if core else 'fringe_only'
                text = note(tree, 'Purple local continuous stroke' if route == 'solid' else 'Purple local broken-body')
                if flags('E9', x, selected):
                    text += note(tree, ' Selected cells touch the target boundary;')
            else:
                status = 'identity_conflict' if refs else 'no_attributable_cells'
                text = note(tree, 'No model-specific cells selected' if refs else 'No cells attributed to this route')
            routes[route].append(row('E9', 'independent', x, core, fringe, fid, status, text, refs))
    return routes, bands


def expand(pair, who, tree):
    env = constants(tree)
    if who == 'root':
        routes, bands = expand_root(pair, tree, env)
    else:
        routes, bands = expand_peer_e8(tree, env) if pair == 'E8' else expand_peer_e9(tree, env)
    env['selected_count'] = sum(len(r['core']) + len(r['fringe']) for rows in list(routes.values()) + [bands] for r in rows)
    env['exact_white'] = []  # Independently verified from source in the full check.
    result = {}
    for key, value in fields(tree).items():
        if key in ('inputs', 'inputs_after'):
            result[key] = {name: pin(HERE / name) for name in env['EXPECTED' if who == 'root' else 'PINS']}
        elif key == 'script_pin':
            result[key] = pin(HERE / ('reader-' + pair + '-' + who + '.py'))
        elif key == 'annotation_script_sha256':
            result[key] = pin(HERE / 'reader-E8-independent.py')['sha256']
        elif key == 'routes':
            result[key] = routes
        elif key == 'unassigned_bands':
            result[key] = bands
        else:
            result[key] = literal(value, env)
    if pair == 'E8' and who == 'independent':
        result['verification'] = assigned(tree, 'verify', "a['verification']", dict(env, white=[]))
    return normalize(result)


def validate_row(pair, r):
    x0, y0, x1, y1 = BOXES[pair]
    require(type(r['x']) is int and x0 <= r['x'] < x1, 'integer column bounds')
    for label in ('core', 'fringe'):
        values = r[label]
        require(type(values) is list and all(type(y) is int and y0 <= y < y1 for y in values), 'integer row bounds')
        require(all(a < b for a, b in zip(values, values[1:])), 'strict row ordering')
    require(not any(y in r['fringe'] for y in r['core']), 'disjoint core/fringe')
    require(r['boundary_flags'] == flags(pair, r['x'], r['core'] + r['fringe']), 'selected-cell boundary flags')


def validate(pair, data):
    require(data['pair'] == pair and sorted(data['routes']) == ['dash', 'solid'], 'pair and routes')
    for key, expected in [('target_box', BOXES[pair]), ('context_box', CONTEXTS[pair])]:
        values = [v for v in [data.get(key), data.get('coverage', {}).get(key)] if v is not None]
        require(values and all(v == expected for v in values), 'all declared boxes')
    x0, _, x1, _ = BOXES[pair]
    bands, last = {}, x0 - 1
    for r in data['unassigned_bands']:
        validate_row(pair, r)
        require(r['x'] > last, 'ordered unique unassigned records')
        last = r['x']
        fid = r.get('band_id', r.get('fragment_id'))
        require(not r['core'] + r['fringe'] or type(fid) is str and bool(fid), 'visible band identity')
        require(type(r['note']) is str, 'band note')
        bands[r['x']] = r
    for route in ('solid', 'dash'):
        require([r['x'] for r in data['routes'][route]] == list(range(x0, x1)), 'complete ordered route')
        for r in data['routes'][route]:
            validate_row(pair, r)
            selected = r['core'] + r['fringe']
            status, fid = r['status'], r['fragment_id']
            require(status in STATUSES and type(r['note']) is str, 'route status/note')
            require(not selected or type(fid) is str and bool(fid), 'selected local fragment')
            if status == 'no_attributable_cells':
                require(not selected and fid is None, 'empty no-attribution')
            if status == 'fringe_only':
                require(not r['core'] and bool(r['fringe']), 'fringe-only classes')
            if status == 'identified_local_fragment':
                require(bool(r['core']), 'identified core')
            if status == 'boundary_truncated':
                require(bool(selected) and bool(r['boundary_flags']), 'selected boundary with local ID')
            require(not ('band_refs' in r and 'unassigned_band_refs' in r), 'one ref schema')
            refs = r.get('band_refs', r.get('unassigned_band_refs', []))
            require(type(refs) is list, 'ref list')
            seen = []
            for ref in refs:
                require(type(ref) in (str, dict), 'ref shape')
                rx, bid = (r['x'], ref) if type(ref) is str else (ref['x'], ref['band_id'])
                require(type(rx) is int and rx == r['x'] and rx in bands, 'same-column real band')
                actual = bands[rx].get('band_id', bands[rx].get('fragment_id'))
                require(type(bid) is str and bool(bid) and bid == actual, 'exact band ID')
                require((rx, bid) not in seen, 'unique band reference')
                seen.append((rx, bid))
            if r['x'] in bands:
                b = bands[r['x']]
                require(not any(y in b['core'] + b['fringe'] for y in selected), 'no model/unassigned duplicate')
    for a, b in zip(data['routes']['solid'], data['routes']['dash']):
        require(not any(y in b['core'] + b['fringe'] for y in a['core'] + a['fringe']), 'no duplicate models')
    return bands


def coverage(pair, data):
    c = data['coverage']
    blocks = c.get('context_blocks_inclusive', c.get('blocks', c.get('raw_blocks')))
    require(type(blocks) is list, 'recorded reading blocks')
    columns = []
    for block in blocks:
        a, b = (block['first'], block['last']) if type(block) is dict else block
        require(type(a) is int and type(b) is int and a <= b, 'integer reading block')
        columns.extend(range(a, b + 1))
    x0, y0, x1, y1 = CONTEXTS[pair]
    require(columns == list(range(x0, x1)), 'complete declared raw-reading coverage')
    declared_rows = c.get('context_rows_inclusive', c.get('rows_inclusive', c.get('raw_rows_inclusive')))
    require(declared_rows == [y0, y1 - 1], 'declared reading rows')
    require(c.get('context_cells', c.get('raw_context_cells')) == (x1 - x0) * (y1 - y0), 'declared raw cell count')
    require(c['model_route_records'] == (BOXES[pair][2] - BOXES[pair][0]) * 2, 'declared route count')
    if 'unassigned_band_records' in c:
        require(c['unassigned_band_records'] == len(data['unassigned_bands']), 'declared band count')


def operations(a, b):
    result = {key: [] for key in OPS}
    combined = list(a) + list(b)
    if combined:
        for y in range(min(combined), max(combined) + 1):
            left, right = y in a, y in b
            choices = (left and right, left or right, left and not right, right and not left, left != right)
            for key, include in zip(OPS, choices):
                if include:
                    result[key].append(y)
    return result


def classes(r):
    return {'core': r['core'], 'fringe': r['fringe'], 'outer': sorted(r['core'] + r['fringe'])}


def verify_sets(saved, left, right):
    require(sorted(saved) == ['core', 'fringe', 'outer'], 'all three comparison classes')
    a, b = classes(left), classes(right)
    for label in ('core', 'fringe', 'outer'):
        require(saved[label] == operations(a[label], b[label]), 'all five independent operations ' + label)
    return 15


def visible(pair, data, bands, x):
    x0, y0, _, y1 = BOXES[pair]
    members = [data['routes'][route][x - x0] for route in ('solid', 'dash')]
    if x in bands:
        members.append(bands[x])
    result = {label: [y for y in range(y0, y1) if any(y in r[label] for r in members)] for label in ('core', 'fringe')}
    require(not any(y in result['fringe'] for y in result['core']), 'visible class disjointness')
    return result


def totals(records):
    return {'entries': len(records),
            'outer_different': sum(bool(r['sets']['outer']['symmetric_difference']) for r in records),
            'class_different': sum(bool(r['sets']['core']['symmetric_difference'] or r['sets']['fringe']['symmetric_difference']) for r in records)}


def controls():
    result = {
        'explicit_five_operations': operations([60, 62], [62, 64]) == {'intersection': [62], 'union': [60, 62, 64], 'root_only': [60], 'peer_only': [64], 'symmetric_difference': [60, 64]},
        'empty': operations([], []) == {key: [] for key in OPS},
        'one_empty_holes': operations([], [60, 62]) == {'intersection': [], 'union': [60, 62], 'root_only': [], 'peer_only': [60, 62], 'symmetric_difference': [60, 62]},
        'empty_boundary': flags('E8', 535, []) == [],
        'all_selected_edges': flags('E8', 689, [54, 85]) == ['target_right', 'target_top', 'target_bottom'],
    }
    base = {'x': 540, 'core': [62], 'fringe': [61, 63], 'boundary_flags': []}
    for label, changes in [('boolean_x', {'x': True}), ('boolean_y', {'core': [True]}),
                            ('outside_x', {'x': 690}), ('outside_y', {'core': [86]}),
                            ('duplicate_y', {'core': [62, 62]}), ('row_order', {'fringe': [63, 61]}),
                            ('class_overlap', {'fringe': [62]}), ('phantom_boundary', {'boundary_flags': ['target_left']})]:
        try:
            validate_row('E8', dict(base, **changes))
        except AssertionError:
            result['reject_' + label] = True
        else:
            result['reject_' + label] = False
    require(all(result.values()), 'all scalar controls')
    return result


def context_pixels(context):
    require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(), 'context repeat bytes')
    with Image.open(HERE / '../../native-strips01/Im7.jpg') as source:
        require(source.mode == 'RGB' and source.size == (745, 92), 'RGB source representation')
        source.load()
        raw = source.tobytes()
    pixels = {}
    for pair in ('E8', 'E9'):
        require(context['target_boxes'][pair] == BOXES[pair] and context['context_boxes'][pair] == CONTEXTS[pair], 'context identity')
        require(context['sources'][pair] == 'Im7.jpg', 'context source')
        x0, y0, x1, y1 = CONTEXTS[pair]
        rows = context['cells'][pair]
        require(len(rows) == (x1 - x0) * (y1 - y0), 'all context records')
        pixels[pair] = {}
        for i, record in enumerate(rows):
            x, y = x0 + i % (x1 - x0), y0 + i // (x1 - x0)
            require(sorted(record) == ['rgb', 'x', 'y'], 'context cell keys')
            require(type(record['x']) is int and type(record['y']) is int and record['x'] == x and record['y'] == y, 'ordered unique context')
            require(type(record['rgb']) is list and len(record['rgb']) == 3 and all(type(v) is int and 0 <= v <= 255 for v in record['rgb']), 'integer RGB')
            offset = 3 * (y * 745 + x)
            require(record['rgb'] == list(raw[offset:offset + 3]), 'fresh source/context RGB equality')
            pixels[pair][x, y] = record['rgb']
    return pixels


def selected_cells(data, pixels):
    white, count = [], 0
    for scope, records in list(data['routes'].items()) + [('unassigned', data['unassigned_bands'])]:
        for r in records:
            for label in ('core', 'fringe'):
                for y in r[label]:
                    count += 1
                    if pixels[r['x'], y] == [255, 255, 255]:
                        white.append({'scope': scope, 'class': label, 'x': r['x'], 'y': y})
    return white, count


def check_comparison(pair, data, bands, saved, white, dependencies, pins):
    require(saved['pair'] == pair and saved['human_accepted'] is False, 'unaccepted pair')
    require(saved['status'] == 'comparison_preserves_disagreement_not_physical_measurement', 'comparison status')
    require(saved['literal_readings'] == data, 'every original reader field retained')
    names = ['reader-' + pair + '-' + who + '.json' for who in ('root', 'independent')]
    require(saved['input_pins'] == {name: pins[name] for name in names}, 'reader pins retained')
    require(saved['dependencies'] == dependencies, 'exact comparison dependencies')
    require(saved['script_pin'] == pins['compare_e89.py'] and saved['test_pin'] == pins['test_compare_e89.py'], 'comparator code/test pins')
    require(saved['reviewer_independence'] == 'Comparator author also authored peer E8 annotation; not independent verification', 'comparator role')
    x0, _, x1, _ = BOXES[pair]
    width = x1 - x0
    rows, geometry = saved['route_comparisons'], saved['visible_ink_comparisons']
    require(len(rows) == width * 2 and len(geometry) == width, 'complete comparison')
    nops = 0
    for i, r in enumerate(rows):
        route, column = ('solid' if i < width else 'dash'), i % width
        require(r['route'] == route and type(r['x']) is int and r['x'] == x0 + column, 'route order')
        a, b = data['root']['routes'][route][column], data['independent']['routes'][route][column]
        require(r['root_original'] == a and r['peer_original'] == b, 'route originals')
        nops += verify_sets(r['sets'], a, b)
    for x, r in enumerate(geometry, x0):
        require(type(r['x']) is int and r['x'] == x, 'visible order')
        require(r['root_unassigned_original'] == bands['root'].get(x), 'root band original')
        require(r['peer_unassigned_original'] == bands['independent'].get(x), 'peer absent versus empty band original')
        nops += verify_sets(r['sets'], visible(pair, data['root'], bands['root'], x), visible(pair, data['independent'], bands['independent'], x))
    summary = {'routes': totals(rows), 'visible_ink': totals(geometry),
               'route_status_different': sum(r['root_original']['status'] != r['peer_original']['status'] for r in rows),
               'selected_exact_white_cells': white}
    require(saved['summary'] == summary, 'every summary value')
    require(nops == width * 45, 'operation count')
    return {'paired_route_rows': len(rows), 'visible_ink_rows': len(geometry), 'set_operations_checked': nops,
            'summary': summary, 'per_route': {route: totals([r for r in rows if r['route'] == route]) for route in ('solid', 'dash')},
            'expanded_route_records': width * 4,
            'expanded_unassigned_records': {who: len(d['unassigned_bands']) for who, d in data.items()},
            'route_status_counts': {who: {route: dict(Counter(r['status'] for r in d['routes'][route])) for route in ('solid', 'dash')} for who, d in data.items()},
            'all_original_metadata_and_records_retained': True, 'literal_replay_exclusions': [],
            'reader_repeat_bytes_equal': True, 'comparison_repeat_bytes_equal': True}


def run():
    scalar = controls()
    before = {name: pin(HERE / name) for name in FROZEN}
    for name, expected in FROZEN.items():
        require(before[name]['sha256'] == expected, 'frozen pin ' + name)
    for name in ('independent-comparison-e89-check.py', 'test_independent_comparison_e89.py'):
        before[name] = pin(HERE / name)
    prior = read('../energy345/independent-comparison-e45-check01.json')
    require(prior['inputs'] == prior['inputs_after'], 'prior E345 preservation receipt')
    prior_files = {}
    for name, expected in prior['inputs'].items():
        resolved_name = str((HERE / '../energy345' / name).resolve())
        current = pin(Path(resolved_name))
        require(current == expected, 'prior E345 file unchanged ' + name)
        before[resolved_name] = prior_files[resolved_name] = current
    context_check = read('context-independent-check.json')
    require(context_check['status'] == 'passed' and context_check['total_checked_cells'] == 10644, 'context check scope')
    require(context_check['inputs'] == context_check['inputs_after'], 'context check preservation')
    for name, expected in context_check['inputs'].items():
        require(pin(HERE / name) == expected, 'context check input ' + name)
        before[name] = expected
    context = read('context01.json')
    for name, expected in context['inputs'].items():
        require(pin(HERE / name) == expected, 'saved context pin ' + name)
        before[name] = expected
    pixels = context_pixels(context)
    results, counts = {}, {}
    for pair in ('E8', 'E9'):
        readers, bands, white, dependencies = {}, {}, {}, {}
        counts[pair] = {}
        for who in ('root', 'independent'):
            filename = 'reader-' + pair + '-' + who + '.json'
            repeat = 'reader-' + pair + '-' + who + '-repeat.json'
            require((HERE / filename).read_bytes() == (HERE / repeat).read_bytes(), 'reader exact repeats ' + pair + who)
            before[repeat] = pin(HERE / repeat)
            data = read(filename)
            script = 'reader-' + pair + '-' + who + '.py'
            tree = ast.parse((HERE / script).read_text())
            env = constants(tree)
            expected = env['EXPECTED' if who == 'root' else 'PINS']
            declared = data.get('inputs', data.get('pins'))
            require(sorted(expected) == sorted(declared), 'exact annotation dependency names')
            for name, sha in expected.items():
                actual = pin(HERE / name)
                require(actual['sha256'] == sha, 'literal dependency pin ' + name)
                require(declared[name] == (actual if type(declared[name]) is dict else sha), 'reader dependency pin ' + name)
                before[name] = dependencies[name] = actual
            dependencies[script] = before[script]
            script_pin = data.get('script_pin', data.get('annotation_script_sha256'))
            require(script_pin == (before[script] if type(script_pin) is dict else before[script]['sha256']), 'reader code pin')
            require(data == expand(pair, who, tree), 'all independent literal metadata/records ' + pair + who)
            readers[who] = data
            bands[who] = validate(pair, data)
            coverage(pair, data)
            white[who], counts[pair][who] = selected_cells(data, pixels[pair])
        first, second = 'comparison-' + pair + '-01.json', 'comparison-' + pair + '-02.json'
        require((HERE / first).read_bytes() == (HERE / second).read_bytes(), 'comparison exact repeats ' + pair)
        results[pair] = check_comparison(pair, readers, bands, read(first), white, dependencies, before)
        require(white == {'root': [], 'independent': []}, 'no selected exact-white ' + pair)
    after = {name: pin(HERE / name) for name in before}
    require(before == after, 'all originals and dependency files preserved')
    return {'status': 'passed_independent_E8_E9_computational_check', 'inputs': before, 'inputs_after': after,
            'independent_scalar_controls': scalar, 'independent_scalar_control_count': len(scalar),
            'comparison_results': results, 'all_set_operations_checked': sum(r['set_operations_checked'] for r in results.values()),
            'source_context_cells_rechecked': {pair: len(p) for pair, p in pixels.items()}, 'selected_cells_rechecked': counts,
            'prior_E345_receipt_inputs_preserved': len(prior_files),
            'literal_expansion': 'AST literal extraction and separately authored expansion; no reader/comparator imports, exec, eval or execution. All metadata and records compared; no exclusions.',
            'literal_table_order_note': 'Root E8 DASH has x595 before x587-593. The nonoverlapping literal table is preserved verbatim; independent expansion checks bounds/overlaps and ordered complete output without sorting or rewriting source decisions.',
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'limits': [
                'Same-source nonblind AI computational check, not another visual/source reading, historical authentication, human acceptance or expert validation.',
                'Source-reading coverage and perception metadata are faithfully replayed and internally checked, not independently witnessed.',
                'Fresh RGB checks and production share the Pillow decoder family; no independent codec validation.',
                'Nonwhite selection does not certify curve ink or model identity; exact-white screening diagnoses one transcription error class.',
                'Faithful literal expansion and set arithmetic establish no physical ordinate, calibrated containment, support, model discrepancy, cause or intent.',
                'E8 peer supplies one unassigned record; its missing records remain null instead of fabricated empties. Root E8 and both E9 readers supply explicit per-column bands.',
                'Existing E345 receipt inputs were checked unchanged; their scientific interpretations were not reopened.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', choices=['independent-comparison-e89-check01.json', 'independent-comparison-e89-check02.json'])
    args = parser.parse_args()
    result = {'status': 'passed', 'controls': controls()} if args.controls else run()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        out = HERE / args.output
        with out.open('x') as stream:
            stream.write(payload)
        print(json.dumps({'output': out.name, 'pin': pin(out), 'status': result['status']}))
    else:
        print(payload, end='')
