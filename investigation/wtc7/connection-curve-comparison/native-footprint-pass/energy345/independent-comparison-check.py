"""Independent E3 comparison audit; never imports or executes reader/comparator code."""
import argparse
import ast
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
import sys
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'reader-E3-root.json': 'b5a8133dc71a0b516d69a3283bc068d75ef083d91ad4727124f8c70a49fc217f',
    'reader-E3-independent.json': '245b5ffe99b0481ab86e57c3bb7d1fccd7d1539a6ce004de967ec118d2e6c243',
    'reader-E3-root.py': 'ed9f65d6187a00fb0555202f1312f7c4c591cc1dfc9c8534b9e91295d65bf71b',
    'reader-E3-independent.py': '9f9165018c5eed713dbd339d48343c54086e3d391b2b4fd5d09d6854728a70f8',
    'compare_e3.py': 'ec94734c4c3f6f5066db934693fec31c18ed26a2303dde8bf5d97d0673526b37',
    'test_compare_e3.py': 'e2c3a1744e7e72298b5e1513b4ab8f56423d64766b7fb2f78ff390f2c148a3b6',
    'comparison01.json': '5604430b3b161b5b7aac362fccddd391f162d579918e0a49988a6a17ce0a9d03',
    'comparison02.json': '5604430b3b161b5b7aac362fccddd391f162d579918e0a49988a6a17ce0a9d03',
    'context-independent-check.json': 'd06d8bce8e58c0016582cd5e0dd52b13ad9daadd86ca21f71f26484305e9373b',
    'correct-E3-independent.py': '6b0deabb34d3cdd8baef4823886bf9ad5ab9ca08710a98b53ae40a1365b55514',
    'reader-E3-independent-corrected.json': 'd1bc331329ecf5eae6a9ac55708efde3d69653c5b3a6c2f9210301f1a3fc1d53',
    'reader-E3-independent-corrected-repeat.json': 'd1bc331329ecf5eae6a9ac55708efde3d69653c5b3a6c2f9210301f1a3fc1d53',
}
OPS = ('intersection', 'union', 'root_only', 'peer_only', 'symmetric_difference')
STATUSES = ('identified_local_fragment', 'fringe_only', 'no_attributable_cells',
            'identity_conflict', 'boundary_truncated')

def require(condition, label):
    if not condition:
        raise AssertionError(label)

def pin(path):
    value = path.read_bytes()
    return {'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}

def read(name):
    return json.loads((HERE / name).read_text())

def normalize(value):
    return json.loads(json.dumps(value, allow_nan=False))

def membership_operations(a, b):
    # Deliberately distinct from producer set algebra: enumerate membership
    # independently for every possible integer between the observed endpoints.
    values = list(a) + list(b)
    out = {key: [] for key in OPS}
    if not values:
        return out
    for y in range(min(values), max(values) + 1):
        left = y in a
        right = y in b
        decisions = (left and right, left or right, left and not right,
                     right and not left, left != right)
        for key, keep in zip(OPS, decisions):
            if keep:
                out[key].append(y)
    return out

def classes(record):
    core, fringe = record['core'], record['fringe']
    return {'core': core, 'fringe': fringe,
            'outer': sorted(core + fringe)}

def flags(x, selected):
    expected = []
    if selected:
        if x == 365:
            expected.append('target_left')
        if x == 689:
            expected.append('target_right')
        if 30 in selected:
            expected.append('target_top')
        if 59 in selected:
            expected.append('target_bottom')
    return expected

def validate_rows(record):
    require(type(record['x']) is int and 365 <= record['x'] <= 689, 'column bounds')
    for label in ('core', 'fringe'):
        rows = record[label]
        require(type(rows) is list, 'row list')
        require(all(type(y) is int and 30 <= y <= 59 for y in rows), 'row type/bounds')
        require(all(a < b for a, b in zip(rows, rows[1:])), 'strict row order')
    require(not any(y in record['fringe'] for y in record['core']), 'disjoint classes')
    require(record['boundary_flags'] == flags(record['x'], record['core'] + record['fringe']),
            'selected-cell flags')

def controls():
    results = {}
    expected = {'intersection': [42], 'union': [40, 42, 44], 'root_only': [40],
                'peer_only': [44], 'symmetric_difference': [40, 44]}
    results['five_operations_explicit_fixture'] = membership_operations([40, 42], [42, 44]) == expected
    results['empty_fixture'] = membership_operations([], []) == {k: [] for k in OPS}
    results['one_empty_and_hole'] = membership_operations([], [40, 42]) == {
        'intersection': [], 'union': [40, 42], 'root_only': [], 'peer_only': [40, 42],
        'symmetric_difference': [40, 42]}
    results['same_outer_different_classes'] = (
        membership_operations([40, 42], [40, 42])['symmetric_difference'] == []
        and membership_operations([40], [42])['symmetric_difference'] == [40, 42])
    results['empty_boundary_has_no_flags'] = flags(365, []) == []
    results['all_selected_edges'] = flags(689, [30, 59]) == ['target_right', 'target_top', 'target_bottom']
    base = {'x': 367, 'core': [43], 'fringe': [42, 44], 'boundary_flags': []}
    for label, changes in [
        ('reject_boolean', {'core': [True]}),
        ('reject_unsorted', {'fringe': [44, 42]}),
        ('reject_class_overlap', {'fringe': [43]}),
        ('reject_outside_row', {'fringe': [60]}),
        ('reject_phantom_boundary', {'boundary_flags': ['target_left']}),
        ('reject_duplicate_row', {'core': [43, 43]}),
    ]:
        try:
            validate_rows(dict(base, **changes))
        except AssertionError:
            results[label] = True
        else:
            results[label] = False
    require(all(results.values()), 'independent synthetic controls')
    return results

def constants(tree):
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return out

def literal(node, env):
    """Only containers, constants, names, and dict construction; no eval/exec."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        require(node.id in env, 'known literal name ' + node.id)
        return env[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal(item, env) for item in node.elts]
    if isinstance(node, ast.Dict):
        require(all(k is not None for k in node.keys), 'no dictionary unpack')
        return {literal(k, env): literal(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict':
        require(not node.args and all(k.arg for k in node.keywords), 'literal dict keywords')
        return {k.arg: literal(k.value, env) for k in node.keywords}
    raise AssertionError('Nonliteral metadata expression: ' + ast.dump(node))

def return_items(tree):
    build = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'build']
    require(len(build) == 1, 'one build function')
    returned = [node.value for node in build[0].body if isinstance(node, ast.Return)]
    require(len(returned) == 1, 'one top-level build return')
    node = returned[0]
    if isinstance(node, ast.Dict):
        return {ast.literal_eval(k): v for k, v in zip(node.keys, node.values)}
    require(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict',
            'metadata return shape')
    return {k.arg: k.value for k in node.keywords}

def note(tree, prefix):
    choices = sorted({node.value for node in ast.walk(tree)
                      if isinstance(node, ast.Constant) and isinstance(node.value, str)
                      and node.value.startswith(prefix)})
    require(len(choices) == 1, 'unique literal note: ' + prefix)
    return choices[0]

def record(x, core, fringe, status, fragment, text, refs, peer=False):
    return {'x': x, 'core': list(core), 'fringe': list(fringe), 'status': status,
            'fragment_id': fragment, 'boundary_flags': flags(x, core + fringe),
            'note': text, 'unassigned_band_refs' if peer else 'band_refs': refs}

def expand_root(tree, env):
    returned = return_items(tree)
    ins = literal(returned['literal_instructions'], env)
    groups = {}
    for i, (a, b) in enumerate(env['DASH_RUNS'], 1):
        for x in range(a, b + 1):
            require(x not in groups, 'root runs nonoverlap')
            groups[x] = i
    routes = {'solid': [], 'dash': []}
    bands = []
    for x in range(365, 690):
        if x in env['EARLY_FRINGE']:
            core, fringe, local = ins['early_core'], env['EARLY_FRINGE'][x], 'u-merged01'
        elif 375 <= x <= 485:
            core, fringe, local = ins['merged_later']['core'], ins['merged_later']['fringe'], 'u-merged01'
        elif x in groups or x in env['EMPTY_INTERBODY']:
            core, fringe, local = [], [], None
        else:
            core, fringe, local = [], [43], 'u-pale-' + str(x)
        bands.append(record(x, core, fringe, 'identity_conflict' if core or fringe else 'no_attributable_cells',
                            local, note(tree, 'Visible merged ink'), []))
        refs = [local] if local else []
        routes['solid'].append(record(x, [], [], 'identity_conflict', None,
                                      note(tree, 'No independently separable solid assignment'), refs))
        if x in groups:
            routes['dash'].append(record(x, ins['dash_core'], ins['dash_fringe'],
                                        'boundary_truncated' if x == 689 else 'identified_local_fragment',
                                        'd' + str(groups[x]).zfill(2),
                                        note(tree, 'Local repeated dash body supported'), []))
        else:
            routes['dash'].append(record(x, [], [], 'identity_conflict' if refs else 'no_attributable_cells',
                                        None, note(tree, 'No unique dash-body cells assigned'), refs))
    result = {}
    for key, value in returned.items():
        if key == 'inputs':
            result[key] = {name: pin(HERE / name) for name in env['EXPECTED']}
        elif key == 'script_pin':
            result[key] = pin(HERE / 'reader-E3-root.py')
        elif key == 'routes':
            result[key] = routes
        elif key == 'unassigned_bands':
            result[key] = bands
        else:
            result[key] = literal(value, env)
    return normalize(result)

def expand_peer(tree, env):
    bands = []
    for a, b, core, fringe in env['BAND']:
        for x in range(a, b + 1):
            bands.append({'band_id': 'E3-independent-shared-band', 'x': x,
                          'core': list(core), 'fringe': list(fringe),
                          'boundary_flags': flags(x, core + fringe),
                          'competing_identities': ['spring ink', 'shell ink', 'overprinted spring and shell ink'],
                          'note': note(tree, 'Visible black band;')})
    band_x = [row['x'] for row in bands]
    require(band_x == list(range(365, 481)), 'peer band coverage from literal runs')
    groups = {}
    for i, (a, b) in enumerate(env['DASH_BODIES'], 1):
        for x in range(a, b + 1):
            require(x not in groups, 'peer dash runs nonoverlap')
            groups[x] = i
    endpoints = dict(env['ENDPOINTS'])
    require(len(endpoints) == len(env['ENDPOINTS']), 'unique peer endpoints')
    require(not any(x in groups for x in endpoints), 'endpoint not dash core')
    routes = {'solid': [], 'dash': []}
    for x in range(365, 690):
        refs = [{'band_id': 'E3-independent-shared-band', 'x': x}] if x in band_x else []
        routes['solid'].append(record(x, [], [], 'identity_conflict', None,
                                      note(tree, 'No separately resolved spring footprint:' if refs else
                                           'Dashed ink is visible locally;'), refs, True))
        if x in groups:
            dash = record(x, [43], [42, 44], 'boundary_truncated' if x == 689 else 'identified_local_fragment',
                          'E3-independent-dash-' + str(groups[x]).zfill(2),
                          note(tree, 'Locally distinguishable black dash body'), [], True)
        elif x in endpoints:
            dash = record(x, [], [43], 'fringe_only',
                          'E3-independent-dash-' + str(endpoints[x]).zfill(2),
                          note(tree, 'Pale material adjacent to this visually distinguished'), [], True)
        else:
            dash = record(x, [], [], 'identity_conflict' if refs else 'no_attributable_cells', None,
                          note(tree, 'Shell contribution not partitionable' if refs else
                               'No shell cells attributed in this inspected column;'), refs, True)
        routes['dash'].append(dash)
    result = {}
    for key, value in return_items(tree).items():
        if key == 'frozen_utc':
            continue
        if key == 'annotation_script_sha256':
            result[key] = pin(HERE / 'reader-E3-independent.py')['sha256']
        elif key == 'routes':
            result[key] = routes
        elif key == 'unassigned_bands':
            result[key] = bands
        else:
            result[key] = literal(value, env)
    return normalize(result)

def validate_reader(data):
    require(data['pair'] == 'E3', 'pair')
    boxes = [value for value in (data.get('target_box'), data.get('coverage', {}).get('target_box'))
             if value is not None]
    require(boxes and all(value == [365, 30, 690, 60] for value in boxes), 'all target declarations')
    require(set(data['routes']) == {'solid', 'dash'}, 'exact routes')
    band_map = {}
    last = 364
    for band in data['unassigned_bands']:
        validate_rows(band)
        require(band['x'] > last, 'unique ordered bands')
        last = band['x']
        band_map[band['x']] = band
        require('note' in band and isinstance(band['note'], str), 'band note')
        bid = band.get('band_id', band.get('fragment_id'))
        require(not band['core'] + band['fringe'] or isinstance(bid, str) and bool(bid), 'visible band ID')
    for route in ('solid', 'dash'):
        entries = data['routes'][route]
        require([r['x'] for r in entries] == list(range(365, 690)), 'complete ordered routes')
        for r in entries:
            validate_rows(r)
            require(r['status'] in STATUSES and isinstance(r['note'], str), 'status/note')
            selected = r['core'] + r['fringe']
            if r['status'] == 'no_attributable_cells':
                require(not selected and r['fragment_id'] is None, 'empty no-attribution')
            if r['status'] == 'fringe_only':
                require(not r['core'] and bool(r['fringe']), 'fringe-only')
            if r['status'] == 'identified_local_fragment':
                require(bool(r['core']) and isinstance(r['fragment_id'], str), 'identified local fragment')
            if r['status'] == 'boundary_truncated':
                require(bool(selected) and bool(r['boundary_flags']), 'selected boundary')
            require(not ('band_refs' in r and 'unassigned_band_refs' in r), 'one reference schema')
            refs = r.get('band_refs', r.get('unassigned_band_refs', []))
            require(type(refs) is list, 'reference list')
            for ref in refs:
                x = r['x'] if isinstance(ref, str) else ref['x']
                bid = ref if isinstance(ref, str) else ref['band_id']
                require(x == r['x'] and x in band_map, 'same-column reference')
                actual = band_map[x].get('band_id', band_map[x].get('fragment_id'))
                require(actual == bid and bool(bid), 'exact band ID reference')
            other = band_map.get(r['x'])
            require(not other or not any(y in other['core'] + other['fringe'] for y in selected),
                    'no model/unassigned duplicate')
    for i in range(325):
        solid = data['routes']['solid'][i]
        dash = data['routes']['dash'][i]
        require(not any(y in dash['core'] + dash['fringe'] for y in solid['core'] + solid['fringe']),
                'no cross-model duplicate')
    return band_map

def verify_sets(saved, left, right):
    require(set(saved) == {'core', 'fringe', 'outer'}, 'three set classes')
    a, b = classes(left), classes(right)
    for key in ('core', 'fringe', 'outer'):
        require(saved[key] == membership_operations(a[key], b[key]), 'independent operation ' + key)
    return 15

def totals(rows):
    return {'entries': len(rows),
            'outer_different': sum(bool(r['sets']['outer']['symmetric_difference']) for r in rows),
            'class_different': sum(bool(r['sets']['core']['symmetric_difference'] or
                                      r['sets']['fringe']['symmetric_difference']) for r in rows)}

def visible(data, band_map, x):
    members = [data['routes'][route][x - 365] for route in ('solid', 'dash')]
    if x in band_map:
        members.append(band_map[x])
    out = {}
    for label in ('core', 'fringe'):
        out[label] = [y for y in range(30, 60) if any(y in r[label] for r in members)]
    require(not any(y in out['fringe'] for y in out['core']), 'visible classes disjoint')
    return out

def check_correction(root, peer, root_bands, pixels):
    first = (HERE / 'reader-E3-independent-corrected.json').read_bytes()
    second = (HERE / 'reader-E3-independent-corrected-repeat.json').read_bytes()
    require(first == second, 'corrected repeated bytes')
    corrected = json.loads(first)
    expected = normalize(peer)
    removed = [(372, 46), (373, 46), (381, 45)]
    for x, y in removed:
        matches = [row for row in expected['unassigned_bands'] if row['x'] == x]
        require(len(matches) == 1, 'one correction target band')
        row = matches[0]
        require(row['fringe'].count(y) == 1 and y not in row['core'], 'remove fringe only')
        require(pixels[x, y] == (255, 255, 255), 'correction exact-white source')
        row['fringe'] = [v for v in row['fringe'] if v != y]
    timestamp = expected.pop('frozen_utc')
    script_tree = ast.parse((HERE / 'correct-E3-independent.py').read_text())
    values = constants(script_tree)
    require(values['ORIGINAL'] == EXPECTED['reader-E3-independent.json'], 'correction literal parent pin')
    require(values['CONTEXT'] == pin(HERE / 'context01.json')['sha256'], 'correction literal context pin')
    require(values['CHANGES'] == removed, 'correction literal exact changes')
    expected['source_history'] = {
        'original_frozen_utc': timestamp,
        'retained_metadata_status': note(script_tree, 'All other original metadata and coverage retained verbatim'),
    }
    expected['correction'] = {
        'status': note(script_tree, 'post-exchange erratum;'),
        'parent_file': 'reader-E3-independent.json',
        'parent_sha256': EXPECTED['reader-E3-independent.json'],
        'context_file': 'context01.json',
        'context_sha256': pin(HERE / 'context01.json')['sha256'],
        'correction_script_sha256': EXPECTED['correct-E3-independent.py'],
        'changes': [{'band_id': 'E3-independent-shared-band', 'x': x, 'y': y,
                     'operation': 'remove fringe membership', 'rgb': [255, 255, 255]}
                    for x, y in removed],
        'reason': note(script_tree, 'Overbroad literal manual run transcription'),
        'corrected_freeze_utc': None,
        'freeze_note': note(script_tree, 'Deterministic artifact;'),
        'verification': {'removed_cells': 3, 'all_routes_unchanged': True,
                         'all_other_original_fields_unchanged_except_relocated_freeze': True,
                         'new_source_decisions': 0},
    }
    require(corrected == expected, 'entire corrected object exact authorized transform')
    require(corrected['routes'] == peer['routes'], 'corrected routes unchanged')
    corrected_bands = validate_reader(corrected)
    selected_white = []
    for scope, entries in list(corrected['routes'].items()) + [('unassigned', corrected['unassigned_bands'])]:
        for row in entries:
            for label in ('core', 'fringe'):
                for y in row[label]:
                    if pixels[row['x'], y] == (255, 255, 255):
                        selected_white.append({'scope': scope, 'class': label, 'x': row['x'], 'y': y})
    require(not selected_white, 'no corrected selected exact-white cells')
    geometry = []
    for x in range(365, 690):
        a = classes(visible(root, root_bands, x))
        b = classes(visible(corrected, corrected_bands, x))
        geometry.append({'x': x, 'sets': {key: membership_operations(a[key], b[key])
                                        for key in ('core', 'fringe', 'outer')}})
    return {
        'status': 'exact_three_cell_post_exchange_derivative_verified',
        'parent_file_pin': pin(HERE / 'reader-E3-independent.json'),
        'correction_script_pin': pin(HERE / 'correct-E3-independent.py'),
        'corrected_file_pin': pin(HERE / 'reader-E3-independent-corrected.json'),
        'repeat_file_pin': pin(HERE / 'reader-E3-independent-corrected-repeat.json'),
        'repeat_bytes_equal': True,
        'only_annotation_changes': [{'x': x, 'y': y, 'operation': 'remove unassigned fringe membership'}
                                    for x, y in removed],
        'all_650_routes_unchanged': True,
        'all_other_original_fields_unchanged_except_relocated_freeze': True,
        'freeze_relocation_and_all_added_provenance_checked': True,
        'whole_corrected_object_semantically_matched': True,
        'selected_exact_white_cells': selected_white,
        'corrected_visible_ink_comparison_to_root': totals(geometry),
        'corrected_visible_set_operations_computed': 4875,
        'corrected_visible_difference_columns': [
            {'x': row['x'], **{key + '_symmetric_difference': row['sets'][key]['symmetric_difference']
                              for key in ('core', 'fringe', 'outer')}}
            for row in geometry if row['sets']['core']['symmetric_difference']
            or row['sets']['fringe']['symmetric_difference']],
        'limit': 'These corrected visible-ink sets are newly computed by this independent checker, not results asserted to be in the unchanged original comparison01/02 files. This is an erratum, not another blind/source reading.',
    }

def run():
    synthetic = controls()
    for name in EXPECTED:
        require((HERE / name).is_file(), 'missing required frozen output: ' + name)
    before = {name: pin(HERE / name) for name in EXPECTED}
    for name, sha in EXPECTED.items():
        require(before[name]['sha256'] == sha, 'frozen pin ' + name)
    root, peer = read('reader-E3-root.json'), read('reader-E3-independent.json')
    dependencies = {}
    for who, data in (('root', root), ('independent', peer)):
        for name, declared in data.get('inputs', data.get('pins')).items():
            current = pin(HERE / name)
            require(current == declared if isinstance(declared, dict) else current['sha256'] == declared,
                    'declared dependency ' + who + ' ' + name)
            dependencies[name] = current
        script = 'reader-E3-' + who + '.py'
        dependencies[script] = before[script]
        if who == 'root':
            require(data['script_pin'] == before[script], 'root script pin')
        else:
            require(data['annotation_script_sha256'] == before[script]['sha256'], 'peer script pin')
    before.update(dependencies)
    before['independent-comparison-check.py'] = pin(Path(__file__))
    raw1 = (HERE / 'comparison01.json').read_bytes()
    raw2 = (HERE / 'comparison02.json').read_bytes()
    require(raw1 == raw2, 'comparison01/02 exact bytes')
    out = json.loads(raw1)
    require(out == json.loads(raw2), 'comparison structures')
    trees = {who: ast.parse((HERE / ('reader-E3-' + who + '.py')).read_text())
             for who in ('root', 'independent')}
    envs = {who: constants(tree) for who, tree in trees.items()}
    require(root == expand_root(trees['root'], envs['root']), 'all root semantics/literal expansion')
    peer_replay = expand_peer(trees['independent'], envs['independent'])
    require({k: v for k, v in peer.items() if k != 'frozen_utc'} == peer_replay,
            'all peer semantics except frozen_utc')
    require(datetime.fromisoformat(peer['frozen_utc']).utcoffset().total_seconds() == 0,
            'peer timestamp parse UTC; excluded from semantic replay only')
    for name, sha in envs['root']['EXPECTED'].items():
        require(pin(HERE / name)['sha256'] == sha, 'root script constant pin')
    for name, sha in envs['independent']['PINS'].items():
        require(pin(HERE / name)['sha256'] == sha, 'peer script constant pin')
    bands = {'root': validate_reader(root), 'independent': validate_reader(peer)}
    require(out['literal_readings'] == {'root': root, 'independent': peer}, 'all literal originals retained')
    require(out['input_pins'] == {name: before[name] for name in
                                 ('reader-E3-root.json', 'reader-E3-independent.json')}, 'input pins retained')
    require(out['dependencies'] == dependencies, 'exact declared dependency union')
    require(out['script_pin'] == before['compare_e3.py'], 'comparator pin')
    require(out['human_accepted'] is False, 'unaccepted comparison')
    require(out['status'] == 'comparison_preserves_disagreement_not_physical_measurement', 'comparison status')
    rows = out['route_comparisons']
    require(len(rows) == 650, '650 paired route rows')
    operations = 0
    for n, row in enumerate(rows):
        route = 'solid' if n < 325 else 'dash'
        i = n % 325
        require(row['route'] == route and row['x'] == i + 365, 'route comparison ordering')
        a, b = root['routes'][route][i], peer['routes'][route][i]
        require(row['root_original'] == a and row['peer_original'] == b, 'route original retention')
        operations += verify_sets(row['sets'], a, b)
    geometry = out['visible_ink_comparisons']
    require(len(geometry) == 325, '325 visible columns')
    for x, row in enumerate(geometry, 365):
        require(row['x'] == x, 'visible ordering')
        require(row['root_unassigned_original'] == bands['root'].get(x), 'root unassigned original retention')
        require(row['peer_unassigned_original'] == bands['independent'].get(x), 'peer missing vs empty retention')
        operations += verify_sets(row['sets'], visible(root, bands['root'], x),
                                   visible(peer, bands['independent'], x))
    require(operations == 14625, 'total independent set operations')
    context_receipt = read('context-independent-check.json')
    require(context_receipt['status'] == 'passed' and context_receipt['total_checked_cells'] == 26641,
            'pinned all-context receipt scope')
    require(context_receipt['inputs'] == context_receipt['inputs_after'], 'prior context before/after')
    context = read('context01.json')
    pixels = {(r['x'], r['y']): tuple(r['rgb']) for r in context['cells']['E3']}
    with Image.open(HERE / '../../native-strips01/Im10.jpg') as image:
        require(image.mode == 'RGB' and image.size == (745, 92), 'source representation')
        image.load()
        raw_rgb = image.tobytes()
    white = {'root': [], 'independent': []}
    selected = 0
    for who, data in (('root', root), ('independent', peer)):
        for scope, records in list(data['routes'].items()) + [('unassigned', data['unassigned_bands'])]:
            for row in records:
                for label in ('core', 'fringe'):
                    for y in row[label]:
                        x = row['x']
                        offset = (y * 745 + x) * 3
                        value = tuple(raw_rgb[offset:offset + 3])
                        require(value == pixels[x, y], 'selected cell source/context equality')
                        selected += 1
                        if value == (255, 255, 255):
                            white[who].append({'scope': scope, 'class': label, 'x': x, 'y': y})
    known = [{'scope': 'unassigned', 'class': 'fringe', 'x': x, 'y': y}
             for x, y in [(372, 46), (373, 46), (381, 45)]]
    require(white == {'root': [], 'independent': known}, 'exact three preserved white selections')
    summary = {'routes': totals(rows), 'visible_ink': totals(geometry),
               'route_status_different': sum(row['root_original']['status'] != row['peer_original']['status']
                                             for row in rows),
               'selected_exact_white_cells': white}
    require(out['summary'] == summary, 'all summary counts and flags')
    correction_result = check_correction(root, peer, bands['root'], pixels)
    after = {name: pin(HERE / name) for name in before}
    require(before == after, 'all before/after pins unchanged')
    return {
        'status': 'passed_original_comparison_with_preserved_white_selection_flags',
        'independent_synthetic_controls': synthetic,
        'synthetic_control_count': len(synthetic),
        'inputs': before, 'inputs_after': after,
        'literal_expansion': {
            'method': 'AST literal extraction and separately authored manual-run expansion; no reader import, exec, eval, or reader execution.',
            'root_all_semantics_match': True,
            'peer_all_semantics_except_frozen_utc_match': True,
            'semantic_replay_exclusions': ['reader-E3-independent.json:frozen_utc'],
            'peer_frozen_utc_retained_in_pinned_original': peer['frozen_utc'],
            'route_records': 1300, 'root_unassigned_records': 325, 'peer_unassigned_records': 116,
            'total_supplied_unassigned_records': 441,
            'whole_byte_reader_expansion_determinism_claimed': False,
        },
        'comparison': {'paired_route_rows': 650, 'visible_ink_rows': 325,
                       'set_operations_checked': operations, 'repeat_bytes_equal': True,
                       'repeat_structures_equal': True, 'all_raw_originals_retained': True,
                       'summary': summary,
                       'per_route': {route: totals([r for r in rows if r['route'] == route])
                                     for route in ('solid', 'dash')},
                       'route_status_counts': {who: {route: dict(Counter(r['status'] for r in data['routes'][route]))
                                                    for route in ('solid', 'dash')}
                                               for who, data in (('root', root), ('independent', peer))}},
        'selected_cells_rechecked_against_fresh_RGB': selected,
        'separate_corrected_derivative': correction_result,
        'previous_context_check_reused': {'path': 'context-independent-check.json',
                                         'pin': before['context-independent-check.json'],
                                         'scope': '26,641 context cells previously checked; not all repeated in this task.'},
        'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
        'command': [sys.executable, '-B', str(Path(__file__).resolve())],
        'scope_review': {
            'decision': 'original frozen E3 comparison verified; annotations remain unaccepted',
            'generic_schema_limit': 'Producer boundary_truncated requires nonempty core, stricter than the parent possible fringe-only boundary case. No frozen E3 route exercises that case; no rule was weakened.',
            'three_white_selections': 'Original peer fringe selections are retained and correctly flagged, not endorsed as visible ink or repaired in place.',
        },
        'limits': [
            'Same-source nonblind AI computational verification, not an independent historical source or human acceptance.',
            'No new image views or ink classification; metadata attestations are retained and replayed, not independently witnessed perception.',
            'Set arithmetic and faithful expansion do not establish source accuracy, model identity, pre-raster containment, physical support, ordinates or cause.',
            'The root explicitly supplies 325 unassigned records; peer supplies 116. Missing peer records stay null, not fabricated empty annotations.',
            'Fresh selected-cell checks use Pillow 12.3.0; saved producer context used Pillow 12.0.0. Shared decoder-family limitation remains.',
            'Original comparison01/02 retain the original three flagged white selections. The separate corrected derivative is checked independently and never substituted into those frozen results.',
        ],
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    result = {'status': 'passed', 'controls': controls()} if args.controls else run()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
