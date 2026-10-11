"""Independent E4/E5 audit: no imports or execution of reader/comparator code.

This is computational verification of preserved annotations, not an independent
visual reading, historical authentication, model validation, or human acceptance.
"""
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
BOXES = {'E4': [440, 72, 690, 92], 'E5': [395, 18, 690, 47]}
CONTEXTS = {'E4': [438, 70, 692, 92], 'E5': [393, 16, 692, 49]}
FROZEN = {
    'reader-E4-root.py': '5a3becf0ced4dcbd733370c3bf7590b325c2a815a13489c0591aa817caa05376',
    'reader-E4-root.json': 'b1ad179b8cbd256e0cb01c9d79ac54778dccc6312698e38008399db6a93c9326',
    'reader-E4-root-repeat.json': 'b1ad179b8cbd256e0cb01c9d79ac54778dccc6312698e38008399db6a93c9326',
    'reader-E4-independent.py': '075f83589d5fa12f84eda89b5c6ff2b8ae08e66f3be7cf8e576e43f27c6e5c92',
    'reader-E4-independent.json': 'f7545fea9317bc7c24ec7b5f6e5d63bc5158e1a11b31b361fa29099d39976a01',
    'reader-E4-independent-repeat.json': 'f7545fea9317bc7c24ec7b5f6e5d63bc5158e1a11b31b361fa29099d39976a01',
    'reader-E5-root.py': 'f679bc92da880a0fe80e5eed1ea66e091259393615030e02e28e2f416966d7e8',
    'reader-E5-root.json': '68190d7db15e73a24b04c854c7c3bf5966cd92877550b49ce22ed2730723f536',
    'reader-E5-root-repeat.json': '68190d7db15e73a24b04c854c7c3bf5966cd92877550b49ce22ed2730723f536',
    'reader-E5-independent.py': 'd9f3d393d13cbd9458a0cae93e15af00fed3e1f152cdcb60c8e179447500bb13',
    'reader-E5-independent.json': '81f9d9d19a7fa827702ca118e8bc3f5d1d4cd8db95380fb765b7407f98a39f38',
    'reader-E5-independent-repeat.json': '81f9d9d19a7fa827702ca118e8bc3f5d1d4cd8db95380fb765b7407f98a39f38',
    'comparison-E4-01.json': '1304d3e863b6ff2f716ce29da4f491c1e2fd3e440729a0ee93b0f02fa3e61663',
    'comparison-E4-02.json': '1304d3e863b6ff2f716ce29da4f491c1e2fd3e440729a0ee93b0f02fa3e61663',
    'comparison-E5-01.json': '3488a350f3da9c0be15d265b56ca2e40b3c561e4db7d79a66fb156d72c11876b',
    'comparison-E5-02.json': '3488a350f3da9c0be15d265b56ca2e40b3c561e4db7d79a66fb156d72c11876b',
    'compare_e45.py': 'e9f5f1d99a1c041a06cb6f4f86b25bd2d3245f14e8e1e58c8382b3ab3c6974b2',
    'test_compare_e45.py': '0ebedbb46fb0cb6bd014a5abd84592d307722e667c89bc9f3e0a8fc694735f02',
    'context-independent-check.json': 'd06d8bce8e58c0016582cd5e0dd52b13ad9daadd86ca21f71f26484305e9373b',
}
OPS = ('intersection', 'union', 'root_only', 'peer_only', 'symmetric_difference')
STATUSES = ('identified_local_fragment', 'fringe_only', 'no_attributable_cells',
            'identity_conflict', 'boundary_truncated')


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


def membership(a, b):
    """Enumerated boolean membership; no producer-style set operations."""
    out = {key: [] for key in OPS}
    values = list(a) + list(b)
    if values:
        for y in range(min(values), max(values) + 1):
            left, right = y in a, y in b
            decisions = (left and right, left or right, left and not right,
                         right and not left, left != right)
            for key, keep in zip(OPS, decisions):
                if keep:
                    out[key].append(y)
    return out


def classes(row):
    return {'core': row['core'], 'fringe': row['fringe'],
            'outer': sorted(row['core'] + row['fringe'])}


def flags(pair, x, selected):
    x0, y0, x1, y1 = BOXES[pair]
    out = []
    if selected:
        for edge, present in [('target_left', x == x0), ('target_right', x == x1 - 1),
                              ('target_top', y0 in selected), ('target_bottom', y1 - 1 in selected)]:
            if present:
                out.append(edge)
    return out


def validate_row(pair, row):
    x0, y0, x1, y1 = BOXES[pair]
    require(type(row['x']) is int and x0 <= row['x'] < x1, 'integer column bounds')
    for label in ('core', 'fringe'):
        values = row[label]
        require(type(values) is list, 'row list')
        require(all(type(y) is int and y0 <= y < y1 for y in values), 'integer row bounds')
        require(all(a < b for a, b in zip(values, values[1:])), 'strict row order')
    require(not any(y in row['fringe'] for y in row['core']), 'classes disjoint')
    require(row['boundary_flags'] == flags(pair, row['x'], row['core'] + row['fringe']),
            'selected-cell boundary flags')


def validate_reader(pair, data):
    require(data['pair'] == pair, 'pair identity')
    for field, expected in [('target_box', BOXES[pair]), ('context_box', CONTEXTS[pair])]:
        declarations = [v for v in (data.get(field), data.get('coverage', {}).get(field)) if v is not None]
        require(declarations and all(v == expected for v in declarations), 'all declared ' + field)
    require(sorted(data['routes']) == ['dash', 'solid'], 'exact two routes')
    x0, _, x1, _ = BOXES[pair]
    bands = {}
    last = x0 - 1
    for row in data['unassigned_bands']:
        validate_row(pair, row)
        require(row['x'] > last, 'unique ordered bands')
        last = row['x']
        bid = row.get('band_id', row.get('fragment_id'))
        require(not row['core'] + row['fringe'] or type(bid) is str and bool(bid), 'selected band identity')
        require(type(row['note']) is str, 'band note')
        bands[row['x']] = row
    for route in ('solid', 'dash'):
        rows = data['routes'][route]
        require([r['x'] for r in rows] == list(range(x0, x1)), 'complete ordered route')
        for row in rows:
            validate_row(pair, row)
            selected = row['core'] + row['fringe']
            status = row['status']
            require(status in STATUSES and type(row['note']) is str, 'status and note')
            if status == 'no_attributable_cells':
                require(not selected and row['fragment_id'] is None, 'empty no attribution')
            if status == 'fringe_only':
                require(not row['core'] and bool(row['fringe']), 'fringe-only classes')
            if status == 'identified_local_fragment':
                require(bool(row['core']) and type(row['fragment_id']) is str and bool(row['fragment_id']),
                        'identified core fragment')
            if status == 'boundary_truncated':
                require(bool(selected) and bool(row['boundary_flags']), 'selected boundary truncation')
                require(type(row['fragment_id']) is str and bool(row['fragment_id']), 'boundary fragment')
            require(not ('band_refs' in row and 'unassigned_band_refs' in row), 'one reference schema')
            refs = row.get('band_refs', row.get('unassigned_band_refs', []))
            require(type(refs) is list, 'reference list')
            seen = []
            for ref in refs:
                require(type(ref) in (str, dict), 'reference shape')
                rx = row['x'] if type(ref) is str else ref['x']
                bid = ref if type(ref) is str else ref['band_id']
                require(type(rx) is int and rx == row['x'] and rx in bands, 'same-column band reference')
                actual = bands[rx].get('band_id', bands[rx].get('fragment_id'))
                require(type(bid) is str and bool(bid) and bid == actual, 'exact band identity')
                require((rx, bid) not in seen, 'unique reference')
                seen.append((rx, bid))
            if row['x'] in bands:
                other = bands[row['x']]
                require(not any(y in other['core'] + other['fringe'] for y in selected),
                        'no duplicate model and unassigned ink')
    for left, right in zip(data['routes']['solid'], data['routes']['dash']):
        require(not any(y in right['core'] + right['fringe'] for y in left['core'] + left['fringe']),
                'no duplicate models')
    return bands


def literal_constants(tree):
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return out


def literal(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        require(node.id in env, 'known literal name')
        return env[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal(v, env) for v in node.elts]
    if isinstance(node, ast.Dict):
        require(all(k is not None for k in node.keys), 'no dictionary unpack')
        return {literal(k, env): literal(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict':
        require(not node.args and all(k.arg for k in node.keywords), 'only literal dict keywords')
        return {k.arg: literal(k.value, env) for k in node.keywords}
    raise AssertionError('nonliteral expression: ' + ast.dump(node))


def returned_fields(tree):
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build']
    require(len(functions) == 1, 'one build function')
    returns = [n.value for n in functions[0].body if isinstance(n, ast.Return)]
    require(len(returns) == 1, 'one top-level return')
    node = returns[0]
    if isinstance(node, ast.Dict):
        return {ast.literal_eval(k): v for k, v in zip(node.keys, node.values)}
    require(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict',
            'literal return dict')
    return {v.arg: v.value for v in node.keywords}


def note(tree, prefix):
    values = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) is str and node.value.startswith(prefix):
            if node.value not in values:
                values.append(node.value)
    require(len(values) == 1, 'unique literal note ' + prefix)
    return values[0]


def record(pair, who, x, core, fringe, status, fragment, text, refs):
    return {'x': x, 'core': list(core), 'fringe': list(fringe), 'status': status,
            'fragment_id': fragment, 'boundary_flags': flags(pair, x, core + fringe), 'note': text,
            'band_refs' if who == 'root' else 'unassigned_band_refs': refs}


def run_membership(runs, pair):
    x0, _, x1, _ = BOXES[pair]
    mapped = {}
    last = x0 - 1
    for i, endpoints in enumerate(runs, 1):
        require(type(endpoints) in (list, tuple) and len(endpoints) == 2, 'literal run shape')
        a, b = endpoints
        require(type(a) is int and type(b) is int and x0 <= a <= b < x1 and a > last,
                'literal runs bounded ordered nonoverlapping')
        last = b
        for x in range(a, b + 1):
            mapped[x] = i
    return mapped


def expand_e4(who, tree, env):
    routes = {'solid': [], 'dash': []}
    bands = []
    groups = run_membership(env['DASH_RUNS' if who == 'root' else 'BODIES'], 'E4')
    for x in range(440, 690):
        if who == 'root':
            if x <= 479:
                core, fringe, bid = [86, 87], [85, 88], 'u-merged01'
            elif x <= 485:
                core, fringe, bid = [86], [85, 87, 88], 'u-merged01'
            elif x in groups:
                core, fringe, bid = [], [], None
            else:
                core, fringe, bid = [], [86, 87], 'u-pale-' + str(x)
            bands.append(record('E4', who, x, core, fringe,
                                'identity_conflict' if core or fringe else 'no_attributable_cells',
                                bid, note(tree, 'Merged ink or tentative interbody'), []))
            refs = [bid] if bid else []
            solid_note = note(tree, 'No independently separable solid trace assigned.')
            dash_empty_note = note(tree, 'No uniquely identified dashed cells;')
            dash_body_note = note(tree, 'Locally repeated body supported')
            fid = 'd' + str(groups[x]).zfill(2) if x in groups else None
        else:
            refs = []
            if x <= 480:
                bid = 'E4-independent-shared-gold'
                bands.append({'band_id': bid, 'x': x, 'core': [86, 87], 'fringe': [85, 88],
                              'boundary_flags': flags('E4', x, [85, 86, 87, 88]),
                              'competing_identities': ['spring contribution', 'shell contribution', 'overprinted contributions'],
                              'note': note(tree, 'One visible gold band;')})
                refs = [{'band_id': bid, 'x': x}]
            solid_note = note(tree, 'No separately identified continuous spring footprint.')
            dash_empty_note = note(tree, 'Shared gold contributions' if refs else 'Pale yellow/compression')
            dash_body_note = note(tree, 'Visible repeated gold dash body;')
            fid = 'E4-independent-dash-' + str(groups[x]).zfill(2) if x in groups else None
        routes['solid'].append(record('E4', who, x, [], [], 'identity_conflict', None, solid_note, refs))
        if x in groups:
            dash = record('E4', who, x, [86], [85, 87, 88],
                          'boundary_truncated' if x == 689 else 'identified_local_fragment',
                          fid, dash_body_note, [])
        else:
            dash = record('E4', who, x, [], [],
                          'identity_conflict' if refs or who == 'root' else 'no_attributable_cells',
                          None, dash_empty_note, refs)
        routes['dash'].append(dash)
    result = {}
    for key, value in returned_fields(tree).items():
        if key == 'inputs':
            result[key] = {name: pin(HERE / name) for name in env['EXPECTED']}
        elif key == 'script_pin':
            result[key] = pin(HERE / 'reader-E4-root.py')
        elif key == 'annotation_script_sha256':
            result[key] = pin(HERE / 'reader-E4-independent.py')['sha256']
        elif key == 'routes':
            result[key] = routes
        elif key == 'unassigned_bands':
            result[key] = bands
        else:
            result[key] = literal(value, env)
    if who == 'independent':
        result['verification'] = {'records': 500, 'context_cells': 5588, 'selected_exact_white': [],
                                  'bounds_membership_disjointness_and_references': 'passed; no selections redrawn',
                                  'pre_freeze_failures': []}
    return normalize(result)


def explicit_runs(runs, default_id=None):
    """Independent literal expansion into per-column tuples, without RGB."""
    by_column = {}
    last = 394
    for run in runs:
        require(len(run) in (4, 5), 'four/five-field manual run')
        first, final, core, fringe = run[:4]
        require(type(first) is int and type(final) is int and 395 <= first <= final < 690,
                'E5 manual run bounds')
        require(first > last, 'E5 ordered nonoverlapping manual runs')
        last = final
        local = run[4] if len(run) == 5 else default_id
        require(type(local) is str and bool(local), 'E5 manual local fragment')
        for x in range(first, final + 1):
            by_column[x] = (list(core), list(fringe), local)
    return by_column


def expand_e5(who, tree, env):
    mappings = {
        'solid': explicit_runs(env['SOLID_RUNS'], 'E5i-solid-approach01' if who == 'independent' else None),
        'dash': explicit_runs(env['DASH_RUNS']),
        'band': explicit_runs(env['BAND_RUNS' if who == 'root' else 'UNASSIGNED_RUNS']),
    }
    routes, bands = {'solid': [], 'dash': []}, []
    for x in range(395, 690):
        uc, uf, local = mappings['band'].get(x, ([], [], None))
        bid = ('E5i-' + local if local else None) if who == 'independent' else local
        if who == 'root':
            bands.append(record('E5', who, x, uc, uf, 'identity_conflict' if bid else 'no_attributable_cells',
                bid, note(tree, 'Visible contact/merged ink assigned once.'), []))
            refs = [bid] if bid else []
        else:
            band_note = note(tree, 'Single visible blue band;' if local == 'u-merged01' else
                             'Blue material between or adjacent' if local else 'No separate unassigned cells')
            bands.append({'x': x, 'core': uc, 'fringe': uf,
                          'status': 'identity_conflict' if uc or uf else 'no_attributable_cells',
                          'fragment_id': bid, 'model': None, 'boundary_flags': flags('E5', x, uc + uf),
                          'note': band_note,
                          'competing_identities': ['spring-associated ink', 'shell-associated ink', 'overprinted contributions'] if uc or uf else [],
                          'fringe_alternative': note(tree, 'Compression/background material remains possible')})
            refs = [{'band_id': bid, 'x': x}] if bid else []
        for route in ('solid', 'dash'):
            core, fringe, fid = mappings[route].get(x, ([], [], None))
            if who == 'independent' and route == 'dash' and fid:
                fid = 'E5i-' + fid
            selected = core + fringe
            edges = flags('E5', x, selected)
            if selected:
                status = 'boundary_truncated' if edges else 'identified_local_fragment' if core else 'fringe_only'
            else:
                status = 'identity_conflict' if bid else 'no_attributable_cells'
            if who == 'root':
                text = note(tree, 'Approach identity uses connected solid')
            elif selected:
                text = note(tree, 'Local blue continuous approach' if route == 'solid' else 'Local blue broken-body/endpoint')
                if edges:
                    text += note(tree, ' Selected cells touch the target boundary;')
            else:
                text = note(tree, 'No model-specific cells assigned' if refs else 'No cells attributed to this route')
            routes[route].append(record('E5', who, x, core, fringe, status, fid, text, refs))
    result = {}
    literal_env = dict(env)
    literal_env['selected_count'] = sum(len(r['core']) + len(r['fringe'])
                                      for rows in list(routes.values()) + [bands] for r in rows)
    # Verified from source/context separately; this constant does not choose ink.
    literal_env['exact_white'] = []
    for key, value in returned_fields(tree).items():
        if key in ('inputs', 'inputs_after'):
            result[key] = {name: pin(HERE / name) for name in env['EXPECTED' if who == 'root' else 'PINS']}
        elif key == 'script_pin':
            result[key] = pin(HERE / ('reader-E5-' + who + '.py'))
        elif key == 'routes':
            result[key] = routes
        elif key == 'unassigned_bands':
            result[key] = bands
        else:
            result[key] = literal(value, literal_env)
    return normalize(result)


def visible(pair, data, bands, x):
    x0, y0, _, y1 = BOXES[pair]
    members = [data['routes'][route][x - x0] for route in ('solid', 'dash')]
    if x in bands:
        members.append(bands[x])
    result = {label: [y for y in range(y0, y1) if any(y in row[label] for row in members)]
              for label in ('core', 'fringe')}
    require(not any(y in result['fringe'] for y in result['core']), 'visible classes disjoint')
    return result


def verify_sets(saved, left, right):
    require(sorted(saved) == ['core', 'fringe', 'outer'], 'three comparison classes')
    a, b = classes(left), classes(right)
    for label in ('core', 'fringe', 'outer'):
        require(saved[label] == membership(a[label], b[label]), 'all five operations ' + label)
    return 15


def totals(rows):
    return {'entries': len(rows),
            'outer_different': sum(bool(r['sets']['outer']['symmetric_difference']) for r in rows),
            'class_different': sum(bool(r['sets']['core']['symmetric_difference'] or
                                       r['sets']['fringe']['symmetric_difference']) for r in rows)}


def controls():
    outcomes = {}
    outcomes['five_explicit_operations'] = membership([74, 76], [76, 78]) == {
        'intersection': [76], 'union': [74, 76, 78], 'root_only': [74],
        'peer_only': [78], 'symmetric_difference': [74, 78]}
    outcomes['empty'] = membership([], []) == {key: [] for key in OPS}
    outcomes['one_empty_preserves_hole'] = membership([], [74, 76]) == {
        'intersection': [], 'union': [74, 76], 'root_only': [],
        'peer_only': [74, 76], 'symmetric_difference': [74, 76]}
    outcomes['same_outer_distinct_classes'] = membership([74], [76])['symmetric_difference'] == [74, 76]
    outcomes['empty_boundary'] = flags('E4', 440, []) == []
    outcomes['all_selected_edges'] = flags('E4', 689, [72, 91]) == ['target_right', 'target_top', 'target_bottom']
    base = {'x': 442, 'core': [76], 'fringe': [75, 77], 'boundary_flags': []}
    for label, changes in [
        ('boolean_column', {'x': True}), ('boolean_row', {'core': [True]}),
        ('outside_column', {'x': 690}), ('outside_row', {'core': [92]}),
        ('row_duplicate', {'core': [76, 76]}), ('unsorted_row', {'fringe': [77, 75]}),
        ('class_overlap', {'fringe': [76]}), ('phantom_boundary', {'boundary_flags': ['target_left']})]:
        try:
            validate_row('E4', dict(base, **changes))
        except AssertionError:
            outcomes['reject_' + label] = True
        else:
            outcomes['reject_' + label] = False
    try:
        literal(ast.parse('dangerous()').body[0].value, {})
    except AssertionError:
        outcomes['reject_nonliteral_call'] = True
    else:
        outcomes['reject_nonliteral_call'] = False
    require(all(outcomes.values()), 'all independent fixture controls')
    return outcomes


def source_context(context):
    require((HERE / 'context01.json').read_bytes() == (HERE / 'context02.json').read_bytes(),
            'context repeat bytes')
    with Image.open(HERE / '../../native-strips01/Im9.jpg') as source:
        require(source.mode == 'RGB' and source.size == (745, 92), 'source RGB size')
        source.load()
        raw = source.tobytes()
    pixels, counts = {}, {}
    for pair in ('E4', 'E5'):
        require(context['target_boxes'][pair] == BOXES[pair], 'context target identity')
        require(context['context_boxes'][pair] == CONTEXTS[pair], 'context rectangle identity')
        require(context['sources'][pair] == 'Im9.jpg', 'context source identity')
        x0, y0, x1, y1 = CONTEXTS[pair]
        rows = context['cells'][pair]
        require(len(rows) == (x1 - x0) * (y1 - y0), 'complete context cell count')
        pixels[pair] = {}
        for i, row in enumerate(rows):
            x, y = x0 + i % (x1 - x0), y0 + i // (x1 - x0)
            require(sorted(row) == ['rgb', 'x', 'y'], 'exact context cell keys')
            require(type(row['x']) is int and type(row['y']) is int and row['x'] == x and row['y'] == y,
                    'unique ordered context coordinates')
            value = row['rgb']
            require(type(value) is list and len(value) == 3 and all(type(v) is int and 0 <= v <= 255 for v in value),
                    'integer RGB channels')
            offset = (y * 745 + x) * 3
            require(value == list(raw[offset:offset + 3]), 'context matches fresh source RGB')
            pixels[pair][x, y] = value
        counts[pair] = len(rows)
    return pixels, counts


def whites(pair, data, pixels):
    result, count = [], 0
    for scope, rows in list(data['routes'].items()) + [('unassigned', data['unassigned_bands'])]:
        for row in rows:
            for label in ('core', 'fringe'):
                for y in row[label]:
                    count += 1
                    if pixels[row['x'], y] == [255, 255, 255]:
                        result.append({'scope': scope, 'class': label, 'x': row['x'], 'y': y})
    return result, count


def compare_pair(pair, data, bands, saved, selected_white, dependencies, pins):
    root, peer = data['root'], data['independent']
    require(saved['pair'] == pair and saved['human_accepted'] is False, 'unaccepted pair')
    require(saved['status'] == 'comparison_preserves_disagreement_not_physical_measurement', 'comparison status')
    require(saved['literal_readings'] == data, 'every original reader field retained')
    names = ['reader-' + pair + '-' + who + '.json' for who in ('root', 'independent')]
    require(saved['input_pins'] == {name: pins[name] for name in names}, 'comparison original pins')
    require(saved['dependencies'] == dependencies, 'exact comparison dependencies')
    require(saved['script_pin'] == pins['compare_e45.py'], 'comparison code pin')
    require(saved['test_pin'] == pins['test_compare_e45.py'], 'comparison test pin')
    require(saved['reviewer_independence'] == 'Comparator author also authored peer E4 annotation; not independent verification',
            'comparator independence disclosure preserved')
    x0, _, x1, _ = BOXES[pair]
    width = x1 - x0
    rows = saved['route_comparisons']
    geometry = saved['visible_ink_comparisons']
    require(len(rows) == width * 2 and len(geometry) == width, 'complete comparison coverage')
    operations = 0
    for n, row in enumerate(rows):
        route, i = ('solid' if n < width else 'dash'), n % width
        require(row['route'] == route and type(row['x']) is int and row['x'] == x0 + i, 'route comparison order')
        a, b = root['routes'][route][i], peer['routes'][route][i]
        require(row['root_original'] == a and row['peer_original'] == b, 'complete route originals retained')
        operations += verify_sets(row['sets'], a, b)
    for x, row in enumerate(geometry, x0):
        require(type(row['x']) is int and row['x'] == x, 'visible comparison order')
        require(row['root_unassigned_original'] == bands['root'].get(x), 'root unassigned original retained')
        require(row['peer_unassigned_original'] == bands['independent'].get(x), 'peer missing versus empty retained')
        operations += verify_sets(row['sets'], visible(pair, root, bands['root'], x),
                                  visible(pair, peer, bands['independent'], x))
    summary = {'routes': totals(rows), 'visible_ink': totals(geometry),
               'route_status_different': sum(row['root_original']['status'] != row['peer_original']['status'] for row in rows),
               'selected_exact_white_cells': selected_white}
    require(saved['summary'] == summary, 'every saved summary value')
    require(operations == width * 45, 'all comparison operations counted')
    return {'paired_route_rows': len(rows), 'visible_ink_rows': len(geometry),
            'set_operations_checked': operations, 'summary': summary,
            'per_route': {route: totals([row for row in rows if row['route'] == route]) for route in ('solid', 'dash')},
            'route_status_counts': {who: {route: dict(Counter(row['status'] for row in reader['routes'][route]))
                                           for route in ('solid', 'dash')} for who, reader in data.items()},
            'all_original_metadata_and_records_retained': True, 'comparison_repeat_bytes_equal': True,
            'literal_replay_exclusions': [], 'reader_repeat_bytes_equal': True}


def run():
    synthetic = controls()
    before = {name: pin(HERE / name) for name in FROZEN}
    for name, expected in FROZEN.items():
        require(before[name]['sha256'] == expected, 'fixed artifact pin ' + name)
    # Existing E3 checker supplies already-frozen E3 pins, read as AST data only.
    old_checker = HERE / 'independent-comparison-check.py'
    old_pins = literal_constants(ast.parse(old_checker.read_text()))['EXPECTED']
    preserved_e3 = {}
    for name, expected in old_pins.items():
        current = pin(HERE / name)
        require(current['sha256'] == expected, 'preserved E3 original ' + name)
        preserved_e3[name] = current
    before.update(preserved_e3)
    for name in ['independent-comparison-check.py', 'independent-comparison-check.json',
                 'independent-comparison-e45-check.py', 'test_independent_comparison_e45.py']:
        before[name] = pin(HERE / name)
    context = read('context01.json')
    context_receipt = read('context-independent-check.json')
    require(context_receipt['status'] == 'passed' and context_receipt['total_checked_cells'] == 26641,
            'prior all-context check scope')
    require(context_receipt['inputs'] == context_receipt['inputs_after'], 'prior context preservation')
    for name, declared in context_receipt['inputs'].items():
        require(pin(HERE / name) == declared, 'prior context pin ' + name)
        before[name] = declared
    require(context['human_accepted'] is False and context['classification'] is None, 'unclassified context')
    for name, declared in context['inputs'].items():
        require(pin(HERE / name) == declared, 'saved context pin ' + name)
        before[name] = declared
    pixels, context_counts = source_context(context)
    results, selected_counts = {}, {}
    for pair in ('E4', 'E5'):
        readers, band_maps, selected_white, dependencies = {}, {}, {}, {}
        selected_counts[pair] = {}
        for who in ('root', 'independent'):
            name = 'reader-' + pair + '-' + who + '.json'
            repeated = 'reader-' + pair + '-' + who + '-repeat.json'
            require((HERE / name).read_bytes() == (HERE / repeated).read_bytes(), 'exact reader repeats ' + pair + who)
            data = read(name)
            script = 'reader-' + pair + '-' + who + '.py'
            tree = ast.parse((HERE / script).read_text())
            env = literal_constants(tree)
            expected = env['EXPECTED'] if 'EXPECTED' in env else env['PINS']
            declared = data['inputs'] if 'inputs' in data else data['pins']
            require(sorted(declared) == sorted(expected), 'all annotation dependencies declared')
            for dep, sha in expected.items():
                current = pin(HERE / dep)
                require(current['sha256'] == sha, 'literal annotation dependency ' + dep)
                require(declared[dep] == (current if type(declared[dep]) is dict else sha), 'record dependency pin ' + dep)
                before[dep] = dependencies[dep] = current
            dependencies[script] = before[script]
            script_declared = data.get('script_pin', data.get('annotation_script_sha256'))
            require(script_declared == (before[script] if type(script_declared) is dict else before[script]['sha256']),
                    'annotation code pin ' + script)
            expanded = expand_e4(who, tree, env) if pair == 'E4' else expand_e5(who, tree, env)
            require(data == expanded, 'complete independent AST/manual expansion ' + pair + who)
            readers[who] = data
            band_maps[who] = validate_reader(pair, data)
            selected_white[who], selected_counts[pair][who] = whites(pair, data, pixels[pair])
        first, second = 'comparison-' + pair + '-01.json', 'comparison-' + pair + '-02.json'
        require((HERE / first).read_bytes() == (HERE / second).read_bytes(), 'exact comparison repeats ' + pair)
        saved = read(first)
        results[pair] = compare_pair(pair, readers, band_maps, saved, selected_white, dependencies, before)
        require(selected_white == {'root': [], 'independent': []}, 'no exact-white selections ' + pair)
        results[pair]['expanded_route_records'] = (BOXES[pair][2] - BOXES[pair][0]) * 4
        results[pair]['expanded_unassigned_records'] = {who: len(reader['unassigned_bands']) for who, reader in readers.items()}
    after = {name: pin(HERE / name) for name in before}
    require(after == before, 'every protected original/input/code file unchanged')
    return {'status': 'passed_independent_E4_E5_computational_check',
            'inputs': before, 'inputs_after': after,
            'independent_scalar_controls': synthetic, 'independent_scalar_control_count': len(synthetic),
            'comparison_results': results, 'all_set_operations_checked': sum(r['set_operations_checked'] for r in results.values()),
            'source_context_cells_rechecked': context_counts,
            'selected_cells_rechecked': selected_counts,
            'preserved_E3_frozen_files': preserved_e3,
            'literal_expansion': 'AST literal extraction and separately authored manual expansion; no reader/comparator imports, exec, eval or executions. Every reader field checked; no timestamp exclusions.',
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'limits': [
                'Same-source nonblind AI computational verification; no independent visual reading, human acceptance or historical authentication.',
                'Coverage and perception attestations are preserved/replayed, not independently witnessed.',
                'Fresh RGB checks use the Pillow decoder family, as did source-context creation; no independent codec validation.',
                'Selected exact-white checks catch a transcription class; nonwhite does not certify ink, fringe, model identity or calibrated containment.',
                'Faithful annotation expansion and set arithmetic do not establish physical ordinates, support, model discrepancy, cause or intent.',
                'E4 peer missing unassigned entries remain null in the comparison; explicit empty root and E5 records retain their distinct original meaning.',
                'Frozen E3 comparison/correction artifacts are integrity-checked and preserved, not reinterpreted or substituted.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = {'status': 'passed', 'controls': controls()} if args.controls else run()
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        target = HERE / args.output
        require(target.parent.resolve() == HERE and target.name.startswith('independent-comparison-e45-'),
                'checker outputs only')
        with target.open('x') as output:
            output.write(raw)
        print(json.dumps({'output': target.name, 'pin': pin(target), 'status': result['status']}))
    else:
        print(raw, end='')
