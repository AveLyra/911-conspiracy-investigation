"""Independent literal annotation and comparison audit; no producer execution.

The only code loaded from producer scripts is inert AST data: explicit manual
tables, metadata expressions and literal note strings. Expansion, validation,
RGB checking and comparison arithmetic are separately implemented here.
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
BOXES = {'F4-Im4': [330, 0, 425, 88], 'F5-Im4': [375, 0, 475, 88], 'F5-Im2': [225, 50, 350, 88]}
CONTEXTS = {'F4-Im4': [328, 0, 427, 88], 'F5-Im4': [373, 0, 477, 88], 'F5-Im2': [223, 48, 352, 88]}
SOURCES = {'F4-Im4': 'Im4.jpg', 'F5-Im4': 'Im4.jpg', 'F5-Im2': 'Im2.jpg'}
PAIRS = {'F4-Im4': 'F4', 'F5-Im4': 'F5', 'F5-Im2': 'F5'}
ROUTES = ('solid', 'dash')
CLASSES = ('core', 'fringe', 'outer')
OPS = ('intersection', 'union', 'primary_only', 'peer_only', 'symmetric_difference')
STATUSES = ('identified_local_fragment', 'fringe_only', 'no_attributable_cells', 'identity_conflict', 'boundary_truncated')
FROZEN = {
    'reader-F4-Im4-primary.py': '9678fa929a5b56921b77feb7a539572a647dac145f38edee0625d1c5b92c5bec',
    'reader-F4-Im4-primary.json': 'efe923d01d0a91154cde9114bd6b4fac972735d49e42c10bd8f7cced3e36bc0b',
    'reader-F4-Im4-peer.py': '919186992631e9f6176c2db6513521fdb6035aae6a30ec02e521cb69a15e1e0d',
    'reader-F4-Im4-peer.json': '63dec672d9c97ee5e29b88aed6bebc6ae8d86f0d39a08ab8cadc68ad5c40b1f7',
    'reader-F5-Im4-primary.py': '8414eb5254959964cbb8bb8092e5bdb437b95791ec3e2628eac0649a4d999ddd',
    'reader-F5-Im4-primary.json': '2074d58d5d581ed32ea0458c4b47473b2612b42fd0c045235f635e69c7ede84c',
    'reader-F5-Im4-peer.py': 'ef726c398a64a866ad645a54528929a3dc46458244cb51f131db80bb0e9db141',
    'reader-F5-Im4-peer.json': '482f8b218c7e1b66e5fca5392720bcd5dcbd4662fd82a900406b55888121e733',
    'reader-F5-Im2-primary.py': '86a6661ca5b2ac76de8985917efaba9fdbfd6756bcf0818222dcdcf28dd3015d',
    'reader-F5-Im2-primary.json': '5757e0a203ec10a23e1b8739ace7feffc030a98436320a77498dc1d431e46cfb',
    'reader-F5-Im2-peer.py': '97a9d422aefa1b60db554f5f24b456bd25b8d0eaabe971e81cb4529584084242',
    'reader-F5-Im2-peer.json': '0ec257d1f95910ddcaf47a7e6512644a04f595688aaff9ea2eb84a2e16cfed36',
    'comparison-F4-Im4-01.json': '758bfd0a872e4a88acbf9ce3493db9d1972a03426eacecf6512867adad655121',
    'comparison-F4-Im4-02.json': '758bfd0a872e4a88acbf9ce3493db9d1972a03426eacecf6512867adad655121',
    'comparison-F5-Im4-01.json': '04b33d34611bf6559ce7307055dfcaa1a0cc94ae9fe65106a62e46ef79838aea',
    'comparison-F5-Im4-02.json': '04b33d34611bf6559ce7307055dfcaa1a0cc94ae9fe65106a62e46ef79838aea',
    'comparison-F5-Im2-01.json': '740b718ea2c226b0da6cf9c8a43c34e9e50148181d88c043f28c1fef43136596',
    'comparison-F5-Im2-02.json': '740b718ea2c226b0da6cf9c8a43c34e9e50148181d88c043f28c1fef43136596',
    'compare_force45.py': '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
    'test_compare_force45.py': '7fdd3792f0c31e07bd23a7e48fdf8d535d2803153e0a7c8423ae9183679c1254',
    'context-independent-check.py': 'd9c5f52907a9d75e244bc8f4df3eeb3b5121f279f02d46ff3c1e477c57bf6767',
    'context-independent-check.json': '55f244a2dbb0fc62312afe5761b418864ba3ba779a117d657339ee095b03d8c8',
    'context-independent-check-repeat.json': '55f244a2dbb0fc62312afe5761b418864ba3ba779a117d657339ee095b03d8c8',
}


def require(ok, label):
    if not ok:
        raise AssertionError(label)


def equal(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(equal(actual[k], v) for k, v in expected.items())
    if type(expected) in (list, tuple):
        return len(actual) == len(expected) and all(equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read(name):
    return json.loads((HERE / name).read_text())


def literal(node, env):
    """Whitelisted data expressions, never eval/exec or arbitrary calls."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        require(node.id in env, 'declared literal name: ' + node.id)
        return env[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [literal(value, env) for value in node.elts]
    if isinstance(node, ast.Dict):
        require(all(key is not None for key in node.keys), 'no mapping unpack')
        keys = [literal(key, env) for key in node.keys]
        require(len(keys) == len(set(keys)), 'unique literal dictionary keys')
        return {key: literal(value, env) for key, value in zip(keys, node.values)}
    if isinstance(node, ast.Subscript):
        collection, key = literal(node.value, env), literal(node.slice, env)
        require(type(collection) in (dict, list, tuple), 'literal collection subscript')
        require(type(key) in (str, int), 'literal key type')
        return collection[key]
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
        left, right = literal(node.left, env), literal(node.right, env)
        require(type(left) is int and type(right) is int, 'integer metadata arithmetic only')
        return left + right if isinstance(node.op, ast.Add) else left - right
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        left, right = literal(node.left, env), literal(node.right, env)
        require(type(left) is int and type(right) is int, 'integer metadata product only')
        return left * right
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'len':
        require(len(node.args) == 1 and not node.keywords, 'literal length signature')
        value = literal(node.args[0], env)
        require(type(value) in (dict, list, tuple, str), 'literal length operand')
        return len(value)
    raise AssertionError('nonliteral data expression: ' + ast.dump(node))


def declarations(tree):
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = literal(node.value, values)
            except (AssertionError, KeyError, IndexError):
                pass
    return values


def fn(tree, name):
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    require(len(found) == 1, 'unique declared function: ' + name)
    return found[0]


def return_fields(tree, name='build'):
    nodes = [node.value for node in fn(tree, name).body if isinstance(node, ast.Return)]
    require(len(nodes) == 1 and isinstance(nodes[0], ast.Dict), 'one literal return dictionary')
    require(all(key is not None for key in nodes[0].keys), 'no return dictionary unpack')
    return {ast.literal_eval(key): value for key, value in zip(nodes[0].keys, nodes[0].values)}


def text_literal(tree, start):
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) is str and node.value.startswith(start) and node.value not in found:
            found.append(node.value)
    require(len(found) == 1, 'unique literal text: ' + start)
    return found[0]


def flags(box, x, rows):
    x0, y0, x1, y1 = box
    if not rows:
        return []
    return [name for name, ok in (('target_left', x == x0), ('target_right', x == x1 - 1),
                                   ('target_top', y0 in rows), ('target_bottom', y1 - 1 in rows)) if ok]


def valid_rows(rows, low, high):
    require(type(rows) is list and all(type(y) is int and low <= y < high for y in rows), 'bounded integer rows')
    require(all(a < b for a, b in zip(rows, rows[1:])), 'strictly increasing rows')


def expand_tables(runs, box, prefix=''):
    """Build per-column memberships, preserving literal member order and holes."""
    x0, y0, x1, y1 = box
    output = {}
    for run in runs:
        require(type(run) is list and len(run) == 5, 'five-field literal run')
        first, last, core, fringe, fragment = run
        require(type(first) is int and type(last) is int and x0 <= first <= last < x1, 'literal run x bounds')
        valid_rows(core, y0, y1)
        valid_rows(fringe, y0, y1)
        require(not any(y in fringe for y in core), 'literal class disjointness')
        require(type(fragment) is str and fragment and bool(core or fringe), 'nonempty identified literal member')
        for x in range(first, last + 1):
            previous = output.setdefault(x, [])
            identity = prefix + fragment
            require(all(member['fragment_id'] != identity for member in previous), 'one local member ID per column')
            require(not any(y in p['core'] + p['fringe'] for p in previous for y in core + fringe), 'members do not share cells')
            previous.append({'fragment_id': identity, 'core': list(core), 'fringe': list(fringe)})
    return output


def union_rows(members, label):
    combined = [y for member in members for y in member[label]]
    require(len(combined) == len(set(combined)), 'unique membership row union')
    return sorted(combined)


def primary_expand(region, tree, env):
    box = BOXES[region]
    maps = {route: expand_tables(env[name], box) for route, name in
            (('solid', 'SOLID'), ('dash', 'DASH'), ('unassigned', 'UNASSIGNED'))}
    if region == 'F4-Im4':
        band_note = route_note = text_literal(tree, 'Manual local ink attribution only.')
    elif region == 'F5-Im4':
        band_note = text_literal(tree, 'Pale between-body material or blue/red')
        route_note = text_literal(tree, 'Manual local blue continuous/broken-style')
    else:
        band_note = text_literal(tree, 'Unresolved blue/red or blue/green overlap,')
        route_note = text_literal(tree, 'Manual continuous/broken blue-style attribution')

    def record(x, pieces, refs, band=False):
        core, fringe = union_rows(pieces, 'core'), union_rows(pieces, 'fringe')
        boundary = flags(box, x, core + fringe)
        if core or fringe:
            status = ('identity_conflict' if band else 'boundary_truncated' if boundary else
                      'identified_local_fragment' if core else 'fringe_only')
        else:
            status = 'identity_conflict' if refs and region != 'F4-Im4' else 'no_attributable_cells'
        return {'x': x, 'core': core, 'fringe': fringe, 'fragments': pieces,
                'fragment_id': pieces[0]['fragment_id'] if len(pieces) == 1 else None,
                'status': status, 'boundary_flags': boundary, 'band_refs': refs,
                'note': band_note if band else route_note}

    routes, bands = {route: [] for route in ROUTES}, []
    for x in range(box[0], box[2]):
        unresolved = maps['unassigned'].get(x, [])
        bands.append(record(x, unresolved, [], True))
        ids = [member['fragment_id'] for member in unresolved]
        if region == 'F5-Im2':
            refs = {'solid': [v for v in ids if v in ('u-red', 'u-green', 'u-green-fringe', 'u-cross')],
                    'dash': [v for v in ids if v in ('u-cross', 'u314', 'u337', 'u338')]}
        else:
            refs = {'solid': [], 'dash': ids}
        for route in ROUTES:
            routes[route].append(record(x, maps[route].get(x, []), refs[route]))
    return routes, bands


def peer_expand(region, helper_tree, cfg):
    box = BOXES[region]
    prefix = region + '-peer-'
    maps = {key: expand_tables(cfg[key], box, prefix) for key in (*ROUTES, 'unassigned')}
    routes, bands = {route: [] for route in ROUTES}, []
    for x in range(box[0], box[2]):
        pieces = maps['unassigned'].get(x, [])
        core, fringe = union_rows(pieces, 'core'), union_rows(pieces, 'fringe')
        bid = prefix + 'unassigned-' + str(x) if pieces else None
        band = {'x': x, 'core': core, 'fringe': fringe,
                'status': 'identity_conflict' if pieces else 'no_attributable_cells',
                'fragment_id': pieces[0]['fragment_id'] if len(pieces) == 1 else None,
                'band_id': bid, 'model': None, 'boundary_flags': flags(box, x, core + fringe),
                'note': text_literal(helper_tree, 'Selected unresolved ink retained once;' if pieces else 'Inspected column with no selected unassigned cells;'),
                'competing_identities': ['nearby stroke edge', 'compression or background material'] if pieces else []}
        if len(pieces) > 1:
            band['fragments'] = pieces
        bands.append(band)
        refs = [{'band_id': bid, 'x': x}] if pieces else []
        for route in ROUTES:
            members = maps[route].get(x, [])
            core, fringe = union_rows(members, 'core'), union_rows(members, 'fringe')
            boundary = flags(box, x, core + fringe)
            status = ('boundary_truncated' if boundary else 'identified_local_fragment' if core else 'fringe_only') if core or fringe else ('identity_conflict' if refs else 'no_attributable_cells')
            row = {'x': x, 'core': core, 'fringe': fringe, 'status': status,
                   'fragment_id': members[0]['fragment_id'] if len(members) == 1 else None,
                   'boundary_flags': boundary, 'unassigned_band_refs': refs,
                   'note': text_literal(helper_tree, 'Local visible style attribution;' if core or fringe else 'No attributable model cells selected after inspection;')}
            if len(members) > 1:
                row['fragments'] = members
            routes[route].append(row)
    return routes, bands


def selected_white(data, pixels):
    count, white = 0, []
    for scope, records in list(data['routes'].items()) + [('unassigned', data['unassigned_bands'])]:
        for row in records:
            for label in ('core', 'fringe'):
                for y in row[label]:
                    count += 1
                    if pixels[row['x'], y] == [255, 255, 255]:
                        white.append({'scope': scope, 'class': label, 'x': row['x'], 'y': y})
    return count, white


def expand(region, role, tree, pixels, helper_tree=None):
    env = declarations(tree)
    script = 'reader-' + region + '-' + role + '.py'
    if role == 'primary':
        routes, bands = primary_expand(region, tree, env)
        nodes = return_fields(tree)
        computed = {'inputs': {name: pin(HERE / name) for name in env['EXPECTED']}, 'script_pin': pin(HERE / script),
                    'routes': routes, 'unassigned_bands': bands}
    else:
        helper_tree = helper_tree or tree
        helper_env = declarations(helper_tree)
        cfg = env['CONFIG']
        routes, bands = peer_expand(region, helper_tree, cfg)
        count, whites = selected_white({'routes': routes, 'unassigned_bands': bands}, pixels)
        deps = {name: pin(HERE / name) for name in helper_env['PINS']}
        if region != 'F4-Im4':
            expected_nodes = [node.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                              and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                              and node.targets[0].id == 'expected']
            require(len(expected_nodes) == 1, 'one shared expander pin declaration')
            declared = literal(expected_nodes[0], env)
            actual = pin(HERE / 'reader-F4-Im4-peer.py')
            require(actual['sha256'] == declared, 'literal shared peer-expander pin')
            deps['reader-F4-Im4-peer.py'] = actual
        computed = {'inputs': deps, 'inputs_after': deps, 'script_pin': pin(HERE / script),
                    'expander_pin': pin(HERE / 'reader-F4-Im4-peer.py'),
                    'literal_manual_transcription': {key + '_runs_inclusive': cfg[key] for key in (*ROUTES, 'unassigned')},
                    'pre_freeze_transcription_checks': {'selected_cells_checked_for_exact_white': count,
                                                       'selected_exact_white_cells': whites, 'post_export_corrections': []},
                    'routes': routes, 'unassigned_bands': bands}
        box, cb = BOXES[region], CONTEXTS[region]
        env.update(cfg=cfg, rid=region, box=box, cb=cb, x0=box[0], x1=box[2], px=pixels)
        nodes = return_fields(helper_tree)
    output = {key: computed[key] if key in computed else literal(value, env) for key, value in nodes.items()}
    return output


def validate_row(row, box):
    x0, y0, x1, y1 = box
    require(type(row['x']) is int and x0 <= row['x'] < x1, 'integer target column')
    for label in ('core', 'fringe'):
        valid_rows(row[label], y0, y1)
    require(not any(y in row['fringe'] for y in row['core']), 'core/fringe disjointness')
    require(equal(row['boundary_flags'], flags(box, row['x'], row['core'] + row['fringe'])), 'exact selected boundary flags')
    require(type(row['note']) is str and bool(row['note'].strip()) and row['status'] in STATUSES, 'record note and status')
    selected = row['core'] + row['fringe']
    if 'fragments' in row:
        fragments = row['fragments']
        require(type(fragments) is list, 'fragment list')
        identities, seen = [], []
        for member in fragments:
            require(set(member) == {'fragment_id', 'core', 'fringe'}, 'membership keys')
            identity = member['fragment_id']
            require(type(identity) is str and identity and identity not in identities, 'unique local member ID')
            identities.append(identity)
            for label in ('core', 'fringe'):
                valid_rows(member[label], y0, y1)
            cells = member['core'] + member['fringe']
            require(bool(cells) and len(cells) == len(set(cells)) and not any(y in seen for y in cells), 'member cells unique and nonempty')
            seen += cells
        for label in ('core', 'fringe'):
            require(equal(union_rows(fragments, label), row[label]), 'exact class membership union')
        require(row['fragment_id'] == (identities[0] if len(identities) == 1 else None), 'single versus multi-fragment identity')
    else:
        require((type(row['fragment_id']) is str and bool(row['fragment_id'])) if selected else row['fragment_id'] is None,
                'selected local identity or explicit empty')
    if row['status'] == 'no_attributable_cells':
        require(not selected and row['fragment_id'] is None, 'empty status is empty')
    elif row['status'] == 'fringe_only':
        require(not row['core'] and bool(row['fringe']), 'fringe-only semantics')
    elif row['status'] == 'identified_local_fragment':
        require(bool(row['core']), 'identified core semantics')
    elif row['status'] == 'boundary_truncated':
        require(bool(selected) and bool(row['boundary_flags']), 'selected boundary semantics')


def validate(region, role, data):
    box = BOXES[region]
    for field, wanted in [('pair', PAIRS[region]), ('region_id', region), ('reader', role), ('source_image', SOURCES[region]),
                          ('target_box', box), ('context_box', CONTEXTS[region]), ('human_accepted', False), ('physical_support', None)]:
        require(equal(data[field], wanted), 'source-region identity or scope: ' + field)
    require(set(data['routes']) == set(ROUTES), 'both route keys only')
    bands, previous = {}, box[0] - 1
    for band in data['unassigned_bands']:
        validate_row(band, box)
        require(band['status'] in ('identity_conflict', 'no_attributable_cells'), 'unassigned band status')
        require(band['x'] > previous, 'ordered unique band columns')
        previous = band['x']
        bands[band['x']] = band
    for route in ROUTES:
        require(equal([row['x'] for row in data['routes'][route]], list(range(box[0], box[2]))), 'complete ordered route')
        for row in data['routes'][route]:
            validate_row(row, box)
            require(not ('band_refs' in row and 'unassigned_band_refs' in row), 'one band-reference schema')
            refs = row.get('band_refs', row.get('unassigned_band_refs', []))
            require(type(refs) is list, 'reference list')
            seen = []
            for ref in refs:
                if type(ref) is str:
                    column, identity = row['x'], ref
                else:
                    require(type(ref) is dict and set(ref) == {'band_id', 'x'}, 'reference object schema')
                    column, identity = ref['x'], ref['band_id']
                require(type(column) is int and column == row['x'] and column in bands, 'reference to real same-column band')
                band = bands[column]
                require(bool(band['core'] + band['fringe']), 'reference is to selected unresolved material')
                ids = ([band['band_id']] if band.get('band_id') is not None else
                       [p['fragment_id'] for p in band.get('fragments', [])] if 'fragments' in band else [band['fragment_id']])
                require(type(identity) is str and identity and identity in ids and (column, identity) not in seen,
                        'exact distinct band or band-member reference')
                seen.append((column, identity))
            if row['x'] in bands:
                band = bands[row['x']]
                require(not any(y in band['core'] + band['fringe'] for y in row['core'] + row['fringe']), 'model/band partition')
    for primary_route, other_route in zip(data['routes']['solid'], data['routes']['dash']):
        require(not any(y in other_route['core'] + other_route['fringe'] for y in primary_route['core'] + primary_route['fringe']), 'model/model partition')
    return bands


def coverage(region, data):
    details = data['coverage']
    box, context = BOXES[region], CONTEXTS[region]
    blocks = details.get('context_blocks_inclusive', details.get('raw_blocks'))
    actual_columns = []
    require(type(blocks) is list and bool(blocks), 'recorded reading blocks')
    for block in blocks:
        require(type(block) is list and len(block) in (2, 4), 'reading block record')
        first, last = block[:2]
        require(type(first) is int and type(last) is int and first <= last, 'reading block integer bounds')
        actual_columns.extend(range(first, last + 1))
    require(equal(actual_columns, list(range(context[0], context[2]))), 'complete declared reading columns')
    require(equal(details.get('context_rows_inclusive', details.get('raw_rows_inclusive')), [context[1], context[3] - 1]), 'complete declared reading rows')
    require(details.get('context_cells', details.get('raw_context_cells')) == (context[2] - context[0]) * (context[3] - context[1]), 'declared context count')
    require(details['model_route_records'] == 2 * (box[2] - box[0]), 'declared route count')
    require(details['unassigned_band_records'] == len(data['unassigned_bands']), 'declared band count')


def operations(left, right):
    """Truth-table arithmetic over the entire integer range, not producer sets."""
    output = {key: [] for key in OPS}
    combined = left + right
    if combined:
        for y in range(min(combined), max(combined) + 1):
            a, b = y in left, y in right
            for key, keep in zip(OPS, (a and b, a or b, a and not b, b and not a, a != b)):
                if keep:
                    output[key].append(y)
    return output


def classes(row):
    return {'core': row['core'], 'fringe': row['fringe'], 'outer': sorted(row['core'] + row['fringe'])}


def verify_sets(saved, left, right):
    require(set(saved) == set(CLASSES), 'all three class operations')
    a, b = classes(left), classes(right)
    for label in CLASSES:
        require(equal(saved[label], operations(a[label], b[label])), 'five exact operations for ' + label)
    return 15


def all_ink(region, data, bands, x):
    box = BOXES[region]
    members = [data['routes'][route][x - box[0]] for route in ROUTES]
    if x in bands:
        members.append(bands[x])
    result = {label: [y for y in range(box[1], box[3]) if any(y in member[label] for member in members)] for label in ('core', 'fringe')}
    require(not any(y in result['fringe'] for y in result['core']), 'all-ink class disjointness')
    return result


def totals(records):
    return {'entries': len(records),
            'outer_different': sum(bool(row['sets']['outer']['symmetric_difference']) for row in records),
            'class_different': sum(bool(row['sets']['core']['symmetric_difference'] or row['sets']['fringe']['symmetric_difference']) for row in records)}


def source_contexts(context):
    require(equal(context['target_boxes'], BOXES) and equal(context['context_boxes'], CONTEXTS), 'fixed source contexts')
    require(equal(context['sources'], SOURCES) and equal(context['pairs'], PAIRS), 'separate region source/pair maps')
    require(equal(context['source_dimensions'], {'Im4.jpg': [741, 88], 'Im2.jpg': [741, 88]}), 'two native source dimensions')
    require(context['human_accepted'] is False and context['classification'] is None, 'raw context not classified/accepted')
    decoded = {}
    for source_name in ('Im4.jpg', 'Im2.jpg'):
        with Image.open(HERE / '../../native-strips01' / source_name) as source:
            require(source.mode == 'RGB' and source.size == (741, 88), 'original source representation')
            source.load()
            decoded[source_name] = source.tobytes()
    result = {}
    for region, box in CONTEXTS.items():
        x0, y0, x1, y1 = box
        rows = context['cells'][region]
        require(len(rows) == (x1 - x0) * (y1 - y0), 'all raw context records')
        values = {}
        for i, record in enumerate(rows):
            x, y = x0 + i % (x1 - x0), y0 + i // (x1 - x0)
            require(type(record) is dict and set(record) == {'x', 'y', 'rgb'}, 'raw record keys')
            require(equal(record['x'], x) and equal(record['y'], y), 'unique row-major coordinates')
            rgb = record['rgb']
            require(type(rgb) is list and len(rgb) == 3 and all(type(channel) is int and 0 <= channel <= 255 for channel in rgb), 'integer RGB triplet')
            index = 3 * (y * 741 + x)
            require(equal(rgb, list(decoded[SOURCES[region]][index:index + 3])), 'fresh source RGB equality')
            values[x, y] = rgb
        result[region] = values
    require(sum(map(len, result.values())) == 23024, 'complete three-region RGB audit')
    return result


def check_comparison(region, readers, bands, saved, whites, dependencies, inputs, comparator_tree):
    box = BOXES[region]
    route_rows, ink_rows = [], []
    for route in ROUTES:
        for i, x in enumerate(range(box[0], box[2])):
            a, b = readers['primary']['routes'][route][i], readers['peer']['routes'][route][i]
            ca, cb = classes(a), classes(b)
            route_rows.append({'route': route, 'x': x, 'primary_original': a, 'peer_original': b,
                               'sets': {key: operations(ca[key], cb[key]) for key in CLASSES}})
    for x in range(box[0], box[2]):
        ca = classes(all_ink(region, readers['primary'], bands['primary'], x))
        cb = classes(all_ink(region, readers['peer'], bands['peer'], x))
        ink_rows.append({'x': x, 'primary_unassigned_original': bands['primary'].get(x),
                         'peer_unassigned_original': bands['peer'].get(x),
                         'sets': {key: operations(ca[key], cb[key]) for key in CLASSES}})
    summary = {'routes': totals(route_rows), 'visible_ink': totals(ink_rows),
               'route_status_different': sum(row['primary_original']['status'] != row['peer_original']['status'] for row in route_rows),
               'selected_exact_white_cells': whites}
    names = ['reader-' + region + '-' + role + '.json' for role in ('primary', 'peer')]
    computed = {'input_pins': {name: inputs[name] for name in names}, 'dependencies': dependencies,
                'script_pin': inputs['compare_force45.py'], 'test_pin': inputs['test_compare_force45.py'],
                'literal_readings': readers, 'route_comparisons': route_rows,
                'visible_ink_comparisons': ink_rows, 'summary': summary}
    env = {'data': readers, 'region': region}
    expected = {key: computed[key] if key in computed else literal(value, env)
                for key, value in return_fields(comparator_tree, 'run').items()}
    require(equal(saved, expected), 'entire independently reconstructed comparison, including metadata and every operation: ' + region)
    nops = 15 * (len(route_rows) + len(ink_rows))
    require(nops == 45 * (box[2] - box[0]), 'complete arithmetic operation count')
    return {'paired_route_rows': len(route_rows), 'all_ink_columns': len(ink_rows), 'set_operations_checked': nops,
            'summary': summary, 'per_route': {route: totals([row for row in route_rows if row['route'] == route]) for route in ROUTES},
            'reader_route_records': sum(len(rows) for data in readers.values() for rows in data['routes'].values()),
            'reader_unassigned_records': {role: len(data['unassigned_bands']) for role, data in readers.items()},
            'route_status_counts': {role: {route: dict(Counter(row['status'] for row in data['routes'][route])) for route in ROUTES}
                                    for role, data in readers.items()},
            'literal_replay_exclusions': [], 'all_original_metadata_and_records_retained': True}


def run():
    required = {f'reader-{region}-{role}.{ext}' for region in BOXES for role in ('primary', 'peer') for ext in ('py', 'json')}
    required |= {f'comparison-{region}-{repeat}.json' for region in BOXES for repeat in ('01', '02')}
    require(required <= set(FROZEN), 'all reader and comparator outputs must be frozen before replay')
    before = {name: pin(HERE / name) for name in FROZEN}
    for name, sha in FROZEN.items():
        require(before[name]['sha256'] == sha, 'frozen artifact pin: ' + name)
    for name in ('independent-comparison-force45-check.py', 'test_independent_comparison_force45.py'):
        before[name] = pin(HERE / name)
    context_check = read('context-independent-check.json')
    require(context_check['status'] == 'passed' and context_check['total_records_checked'] == 23024, 'prior context checker scope')
    require(equal(context_check['inputs_before'], context_check['inputs_after']), 'context checker input preservation')
    for name, value in context_check['inputs_before'].items():
        require(equal(pin(HERE / name), value), 'context receipt dependency: ' + name)
        before[name] = value
    old_root = HERE / '../energy89'
    old = context_check['prior_energy89_artifact_pins_before']
    require(equal(old, context_check['prior_energy89_artifact_pins_after']), 'old artifact preservation receipt')
    old_before = {name: pin(old_root / name) for name in old}
    require(equal(old_before, old), 'all older energy89 artifacts unchanged')
    context_bytes = (HERE / 'context01.json').read_bytes()
    require(context_bytes == (HERE / 'context02.json').read_bytes(), 'context byte-identical repeat')
    context = json.loads(context_bytes)
    for name, value in context['inputs'].items():
        require(equal(pin(HERE / name), value), 'raw context dependency pin')
        before[name] = value
    pixels = source_contexts(context)
    peer_helper = ast.parse((HERE / 'reader-F4-Im4-peer.py').read_text())
    peer_base_pins = declarations(peer_helper)['PINS']
    comparator_tree = ast.parse((HERE / 'compare_force45.py').read_text())
    results, selected_counts, white_results = {}, {}, {}
    for region in BOXES:
        readers, bands, dependencies, counts, whites = {}, {}, {}, {}, {}
        for role in ('primary', 'peer'):
            stem = 'reader-' + region + '-' + role
            original, repeat = stem + '.json', stem + '-repeat.json'
            raw = (HERE / original).read_bytes()
            require(raw == (HERE / repeat).read_bytes(), 'reader byte-identical repeat: ' + stem)
            before[repeat] = pin(HERE / repeat)
            data = json.loads(raw)
            script = stem + '.py'
            tree = ast.parse((HERE / script).read_text())
            env = declarations(tree)
            expected_pins = dict(env['EXPECTED'] if role == 'primary' else peer_base_pins)
            if role == 'peer' and region != 'F4-Im4':
                expected_pins['reader-F4-Im4-peer.py'] = FROZEN['reader-F4-Im4-peer.py']
            require(set(data['inputs']) == set(expected_pins), 'exact annotation dependency roster')
            for name, sha in expected_pins.items():
                value = pin(HERE / name)
                require(value['sha256'] == sha and equal(data['inputs'][name], value), 'literal annotation dependency: ' + name)
                before[name] = dependencies[name] = value
            dependencies[script] = before[script]
            if role == 'peer':
                dependencies['reader-F4-Im4-peer.py'] = before['reader-F4-Im4-peer.py']
            independently_expanded = expand(region, role, tree, pixels[region], peer_helper if role == 'peer' else None)
            require(equal(data, independently_expanded), 'all literal annotation metadata and records: ' + stem)
            readers[role] = data
            bands[role] = validate(region, role, data)
            coverage(region, data)
            counts[role], whites[role] = selected_white(data, pixels[region])
        first, second = 'comparison-' + region + '-01.json', 'comparison-' + region + '-02.json'
        raw = (HERE / first).read_bytes()
        require(raw == (HERE / second).read_bytes(), 'comparison byte-identical repeat: ' + region)
        results[region] = check_comparison(region, readers, bands, json.loads(raw), whites, dependencies, before, comparator_tree)
        require(equal(whites, {'primary': [], 'peer': []}), 'no selected exact-white transcription issue: ' + region)
        selected_counts[region], white_results[region] = counts, whites
    after = {name: pin(HERE / name) for name in before}
    old_after = {name: pin(old_root / name) for name in old_before}
    require(equal(before, after) and equal(old_before, old_after), 'every new and old dependency preserved during replay')
    return {'status': 'passed_independent_force45_computational_check', 'inputs_before': before, 'inputs_after': after,
            'regions': results, 'source_context_records_rechecked': {region: len(values) for region, values in pixels.items()},
            'selected_cells_rechecked': selected_counts, 'selected_exact_white': white_results,
            'all_set_operations_checked': sum(result['set_operations_checked'] for result in results.values()),
            'all_reader_route_records_checked': sum(result['reader_route_records'] for result in results.values()),
            'all_unassigned_records_checked': sum(sum(result['reader_unassigned_records'].values()) for result in results.values()),
            'older_energy89_pins_before': old_before, 'older_energy89_pins_after': old_after,
            'older_energy89_pin_count': len(old_before), 'reader_repeat_bytes_equal': True, 'comparison_repeat_bytes_equal': True,
            'synthetic_controls': 'Separate synthetic-only unittest suite; historical replay is not counted as a synthetic test.',
            'literal_replay': 'Inert AST data and separately authored expansion; no producer imports, exec, eval, or subprocess execution; no excluded metadata or records.',
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'limits': [
                'Same-source nonblind computational check, not a new visual reading, human acceptance, or expert validation.',
                'Recorded reading coverage and perception are internally checked and replayed, not independently witnessed.',
                'Shared Pillow decoder family; fresh source RGB is not independent codec validation or historical authentication.',
                'Exact-white screening diagnoses one transcription-error class; nonwhite cells need not be curve ink.',
                'Region identities, including two separate F5 sources, are retained; no seam join or cross-source coordinate union.',
                'Complete literal replay and set arithmetic establish no original-curve bounds, physical support, model discrepancy, cause, or intent.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', choices=['independent-comparison-force45-check01.json', 'independent-comparison-force45-check02.json'])
    args = parser.parse_args()
    value = run()
    payload = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        out = HERE / args.output
        with out.open('x') as destination:
            destination.write(payload)
        print(json.dumps({'output': out.name, 'pin': pin(out), 'status': value['status']}))
    else:
        print(payload, end='')
