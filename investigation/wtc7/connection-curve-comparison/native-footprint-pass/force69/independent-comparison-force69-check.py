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
BOXES = {'F6-Im2': [205, 0, 365, 88], 'F7-Im1': [220, 50, 335, 88],
         'F7-Im2': [330, 0, 475, 88], 'F8-Im1': [195, 10, 370, 88],
         'F9-Im0': [220, 55, 325, 88], 'F9-Im1': [245, 0, 375, 88]}
CONTEXTS = {'F6-Im2': [203, 0, 367, 88], 'F7-Im1': [218, 48, 337, 88],
            'F7-Im2': [328, 0, 477, 88], 'F8-Im1': [193, 8, 372, 88],
            'F9-Im0': [218, 53, 327, 88], 'F9-Im1': [243, 0, 377, 88]}
SOURCES = {'F6-Im2': 'Im2.jpg', 'F7-Im1': 'Im1.jpg', 'F7-Im2': 'Im2.jpg',
           'F8-Im1': 'Im1.jpg', 'F9-Im0': 'Im0.jpg', 'F9-Im1': 'Im1.jpg'}
PAIRS = {'F6-Im2': 'F6', 'F7-Im1': 'F7', 'F7-Im2': 'F7',
         'F8-Im1': 'F8', 'F9-Im0': 'F9', 'F9-Im1': 'F9'}
ROUTES = ('solid', 'dash')
CLASSES = ('core', 'fringe', 'outer')
OPS = ('intersection', 'union', 'primary_only', 'peer_only', 'symmetric_difference')
STATUSES = ('identified_local_fragment', 'fringe_only', 'no_attributable_cells', 'identity_conflict', 'boundary_truncated')
FROZEN = {
    'reader-F9-Im0-primary.py': '4ad69e414aa6cd6b83744eab224ed5c33795cd8f60402c251cb9dcf931a20d72',
    'reader-F9-Im0-primary.json': 'f4a569da1e398e3d2e2a90728d07d97098d975d669f444f30c6df8139849b109',
    'comparison-F9-Im0-01.json': 'ab291e04dc519a4a4f77d67ebb4e412ee490e6e82463f143918bf386284b891a',
    'comparison-F9-Im0-02.json': 'ab291e04dc519a4a4f77d67ebb4e412ee490e6e82463f143918bf386284b891a',
    'primary_helper.py': 'e045e142fe8dfa9fe2d112a8ffb5198e99ef02ffc23c7d61ac6e7cf9538ec132',
    'reader-F9-Im0-peer.py': 'a6ce13f6a425fac0753307992a82807dda435ef7cae8655db4f53e530ee8540f',
    'reader-F9-Im0-peer.json': '81913ce599fc26ac2ba82b845fcdd80d95eb40d28a13ac5f628893e891adfc77',
    'peer_export.py': '767ed301d916c7056659282d6e30f8f6124fe5d27a879183a0d7a355758319e6',
    'compare_force69.py': 'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
    'test_compare_force69.py': 'ce57d610316955c7bcaeacd733310e6e786bf96227eeeef6bec6399b458786c2',
    '../force45/compare_force45.py': '932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
    'context-independent-check.py': 'daaa3525317030d01a0e026fe6ea4efba20934c5868e8988c984c29f0f4e00aa',
    'context-independent-check.json': '9ddd692d51443ebfba6a4d39a42519a54bbf8cbc1567b428e7c7aa907148424e',
    'context-independent-check-repeat.json': '9ddd692d51443ebfba6a4d39a42519a54bbf8cbc1567b428e7c7aa907148424e',
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



def owners(values):
    require(type(values) is list and all(type(value) is str and value in ROUTES for value in values),
            'explicit route candidate list')
    require(len(values) == len(set(values)), 'unique route candidates')
    return values


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


def expand_primary(region, spec, helper_tree):
    box = BOXES[region]
    require(spec['region'] == region, 'primary literal source-region identity')
    runs, ownership = spec['literal'], spec.get('ownership', {})
    require(type(runs) is dict and set(runs) == {'solid', 'dash', 'unassigned'}, 'primary literal route keys')
    require(type(ownership) is dict, 'primary ownership map')
    maps = {route: expand_tables(runs[route], box) for route in (*ROUTES, 'unassigned')}
    used_ids = {member['fragment_id'] for group in maps['unassigned'].values() for member in group}
    require(set(ownership) == used_ids, 'exact unresolved fragment ownership roster')
    for value in ownership.values():
        owners(value)
    band_note = text_literal(helper_tree, 'Manually retained unresolved material;')
    route_note = text_literal(helper_tree, 'Manual source-native local-style attribution.')

    def record(x, members, refs, is_band=False, possible=None):
        core, fringe = union_rows(members, 'core'), union_rows(members, 'fringe')
        boundary = flags(box, x, core + fringe)
        if is_band:
            status = 'identity_conflict' if core or fringe else 'no_attributable_cells'
        elif core or fringe:
            status = 'boundary_truncated' if boundary else 'identified_local_fragment' if core else 'fringe_only'
        else:
            status = 'identity_conflict' if refs else 'no_attributable_cells'
        value = {'x': x, 'core': core, 'fringe': fringe,
                 'fragment_id': members[0]['fragment_id'] if len(members) == 1 else None,
                 'fragments': members, 'status': status, 'boundary_flags': boundary,
                 'band_refs': refs, 'note': band_note if is_band else route_note}
        if is_band:
            value.update(band_id='unassigned-' + str(x) if core or fringe else None,
                         possible_routes_by_fragment=possible,
                         candidate_routes=[route for route in ROUTES if any(route in value for value in possible.values())])
        return value

    routes, bands = {route: [] for route in ROUTES}, []
    for x in range(box[0], box[2]):
        members = maps['unassigned'].get(x, [])
        possible = {member['fragment_id']: ownership[member['fragment_id']] for member in members}
        band = record(x, members, [], True, possible)
        bands.append(band)
        for route in ROUTES:
            refs = [band['band_id']] if any(route in value for value in possible.values()) else []
            routes[route].append(record(x, maps[route].get(x, []), refs))
    return routes, bands


def expand_peer(region, cfg, helper_tree):
    box = BOXES[region]
    for key, wanted in [('pair', PAIRS[region]), ('region_id', region), ('source_image', SOURCES[region]),
                        ('target', box), ('context', CONTEXTS[region])]:
        require(equal(cfg[key], wanted), 'peer literal identity: ' + key)
    prefix = region + '-peer-'
    maps = {route: expand_tables(cfg[route], box, prefix) for route in (*ROUTES, 'unassigned')}
    require(type(cfg['unassigned_candidates']) is dict and
            set(cfg['unassigned_candidates']) == set(maps['unassigned']), 'explicit ownership per material column')
    require(type(cfg['unassigned_reasons']) is dict, 'literal unassigned reasons')
    for values in cfg['unassigned_candidates'].values():
        owners(values)
        require(values == sorted(values), 'peer candidate order')
    routes, bands = {route: [] for route in ROUTES}, []
    for x in range(box[0], box[2]):
        pieces = maps['unassigned'].get(x, [])
        core, fringe = union_rows(pieces, 'core'), union_rows(pieces, 'fringe')
        possible = cfg['unassigned_candidates'].get(x, [])
        bid = prefix + 'unassigned-' + str(x) if pieces else None
        band = {'x': x, 'core': core, 'fringe': fringe,
                'status': 'identity_conflict' if pieces else 'no_attributable_cells',
                'fragment_id': pieces[0]['fragment_id'] if len(pieces) == 1 else None,
                'band_id': bid, 'model': None, 'candidate_routes': possible,
                'boundary_flags': flags(box, x, core + fringe),
                'note': cfg['unassigned_reasons'].get(x, text_literal(helper_tree, 'Inspected column;')),
                'competing_identities': ['listed route edge or body', 'compression/background or another fragment'] if pieces else []}
        if len(pieces) > 1:
            band['fragments'] = pieces
        bands.append(band)
        for route in ROUTES:
            members = maps[route].get(x, [])
            core, fringe = union_rows(members, 'core'), union_rows(members, 'fringe')
            boundary = flags(box, x, core + fringe)
            refs = [{'band_id': bid, 'x': x}] if route in possible else []
            status = ('boundary_truncated' if boundary else 'identified_local_fragment' if core else 'fringe_only') if core or fringe else ('identity_conflict' if refs else 'no_attributable_cells')
            value = {'x': x, 'core': core, 'fringe': fringe, 'status': status,
                     'fragment_id': members[0]['fragment_id'] if len(members) == 1 else None,
                     'boundary_flags': boundary, 'unassigned_band_refs': refs,
                     'note': text_literal(helper_tree, 'Local visible style attribution;' if core or fringe else 'No model cells selected after actual inspection;')}
            if len(members) > 1:
                value['fragments'] = members
            routes[route].append(value)
    return routes, bands


def expand(region, role, tree, pixels, helper_tree, context):
    env, helper_env = declarations(tree), declarations(helper_tree)
    script = 'reader-' + region + '-' + role + '.py'
    box, cb = BOXES[region], CONTEXTS[region]
    if role == 'primary':
        spec = env['SPEC']
        routes, bands = expand_primary(region, spec, helper_tree)
        deps = {name: pin(HERE / name) for name in helper_env['EXPECTED']}
        deps['primary_helper.py'] = pin(HERE / 'primary_helper.py')
        computed = {'pair': PAIRS[region], 'inputs': deps, 'script_pin': pin(HERE / script),
                    'routes': routes, 'unassigned_bands': bands}
        helper_env.update(spec=spec, rid=region, box=box, raw=context, runs=spec['literal'],
                          ownership=spec.get('ownership', {}))
    else:
        cfg = env['CONFIG']
        routes, bands = expand_peer(region, cfg, helper_tree)
        count, whites = selected_white({'routes': routes, 'unassigned_bands': bands}, pixels)
        deps = {name: pin(HERE / name) for name in helper_env['PINS']}
        computed = {'inputs': deps, 'inputs_after': deps, 'script_pin': pin(HERE / script),
                    'expander_pin': pin(HERE / 'peer_export.py'),
                    'literal_manual_transcription': {key + '_runs_inclusive': cfg[key] for key in (*ROUTES, 'unassigned')},
                    'pre_freeze_transcription_checks': {
                        'selected_cells_checked_for_exact_white': count,
                        'selected_exact_white_cells': [[w['scope'], w['class'], w['x'], w['y']] for w in whites],
                        'post_export_corrections': []},
                    'routes': routes, 'unassigned_bands': bands}
        helper_env.update(cfg=cfg, rid=region, box=box, cb=cb, x0=box[0], x1=box[2], px=pixels)
    nodes = return_fields(helper_tree)
    return {key: computed[key] if key in computed else literal(value, helper_env) for key, value in nodes.items()}

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
    bands, previous, referenced = {}, box[0] - 1, set()
    for band in data['unassigned_bands']:
        validate_row(band, box)
        require(band['status'] in ('identity_conflict', 'no_attributable_cells'), 'unassigned band status')
        require(band['x'] > previous, 'ordered unique band columns')
        require('candidate_routes' in band, 'explicit candidate route field')
        candidates = owners(band['candidate_routes'])
        material = bool(band['core'] or band['fringe'])
        require(material or not candidates, 'empty band has no candidates')
        require(band['status'] != 'identity_conflict' or material, 'band conflict requires material')
        if 'possible_routes_by_fragment' in band:
            local = band['possible_routes_by_fragment']
            ids = [part['fragment_id'] for part in band.get('fragments', [])]
            require(type(local) is dict and set(local) == set(ids), 'exact fragment ownership keys')
            for value in local.values():
                owners(value)
            require(set(candidates) == {route for value in local.values() for route in value},
                    'aggregate candidates equal fragment ownership')
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
                require(route in band['candidate_routes'], 'reference belongs to candidate route')
                referenced.add((column, route))
                seen.append((column, identity))
            if row['status'] == 'identity_conflict':
                require(bool(seen), 'route conflict requires real material reference')
            if seen and not (row['core'] or row['fringe']):
                require(row['status'] == 'identity_conflict', 'unassigned-only route stays unresolved')
            if row['x'] in bands:
                band = bands[row['x']]
                require(not any(y in band['core'] + band['fringe'] for y in row['core'] + row['fringe']), 'model/band partition')
    for band in bands.values():
        require(all((band['x'], route) in referenced for route in band['candidate_routes']),
                'every candidate route has its material reference')
    for primary_route, other_route in zip(data['routes']['solid'], data['routes']['dash']):
        require(not any(y in other_route['core'] + other_route['fringe'] for y in primary_route['core'] + primary_route['fringe']), 'model/model partition')
    return bands



def coverage(region, data, context):
    details = data['coverage']
    box, target = BOXES[region], CONTEXTS[region]
    if data['reader'] == 'primary':
        blocks = details['context_blocks_inclusive']
        require(type(blocks) is list and bool(blocks), 'primary reading blocks')
        columns = []
        for block in blocks:
            require(type(block) is list and len(block) == 2 and all(type(v) is int for v in block),
                    'primary inclusive column block')
            first, last = block
            require(first <= last, 'nonempty primary block')
            columns.extend(range(first, last + 1))
        require(equal(columns, list(range(target[0], target[2]))), 'all declared primary context columns')
        require(equal(details['context_rows_inclusive'], [target[1], target[3] - 1]), 'all primary context rows')
        require(equal(details['context_cells'], (target[2] - target[0]) * (target[3] - target[1])), 'primary context count')
        require(details['all_target_columns_read'] is True and details['native_strip_viewed'] is True
                and details['complete_composed_page_viewed'] is True, 'explicit primary viewed/read claims')
    else:
        blocks = details['raw_blocks']
        require(type(blocks) is list and bool(blocks), 'peer reading blocks')
        wanted = {(x, y) for x in range(target[0], target[2]) for y in range(target[1], target[3])}
        seen = set()
        target_cells = {(row['x'], row['y']): row['rgb'] for row in context['cells'][region]}
        for block in blocks:
            require(type(block) is dict and {'display_region', 'box', 'untruncated', 'receipt'} <= set(block),
                    'peer source block metadata')
            other, rect = block['display_region'], block['box']
            require(other in SOURCES and SOURCES[other] == SOURCES[region], 'same-source reading reuse only')
            require(type(rect) is list and len(rect) == 4 and all(type(v) is int for v in rect), 'integer reading block')
            x0, y0, x1, y1 = rect
            ox0, oy0, ox1, oy1 = CONTEXTS[other]
            require(ox0 <= x0 < x1 <= ox1 and oy0 <= y0 < y1 <= oy1, 'block inside referenced context')
            require(block['untruncated'] is True and type(block['receipt']) is str and bool(block['receipt'].strip()),
                    'explicit untruncated reading receipt')
            other_cells = {(row['x'], row['y']): row['rgb'] for row in context['cells'][other]}
            for xy in wanted:
                if x0 <= xy[0] < x1 and y0 <= xy[1] < y1:
                    require(equal(target_cells[xy], other_cells[xy]), 'reused exact source-cell equality')
                    seen.add(xy)
        require(seen == wanted, 'complete declared peer context coverage')
        require(equal(details['raw_context_cells'], len(wanted)), 'peer context count')
        require(details['full_native_strip_viewed'] is True and details['full_composed_page_viewed'] is True
                and details['all_blocks_untruncated'] is True, 'explicit peer viewed/read claims')
        require(equal(details['target_columns'], box[2] - box[0]), 'peer target column count')
    require(equal(details['model_route_records'], 2 * (box[2] - box[0])), 'declared route count')
    require(equal(details['unassigned_band_records'], len(data['unassigned_bands'])), 'declared band count')

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
    require(equal(context['source_dimensions'], {'Im0.jpg': [741, 88], 'Im1.jpg': [741, 88], 'Im2.jpg': [741, 88]}), 'three native source dimensions')
    require(context['human_accepted'] is False and context['classification'] is None, 'raw context not classified/accepted')
    decoded = {}
    for source_name in ('Im0.jpg', 'Im1.jpg', 'Im2.jpg'):
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
    require(sum(map(len, result.values())) == 62231, 'complete six-region RGB audit')
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
                'script_pin': inputs['compare_force69.py'], 'test_pin': inputs['test_compare_force69.py'],
                'helper_pin': inputs['../force45/compare_force45.py'], 'pair': PAIRS[region], 'source_image': SOURCES[region],
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


def run(regions=None):
    regions = list(BOXES) if regions is None else regions
    require(type(regions) is list and bool(regions) and len(regions) == len(set(regions))
            and all(region in BOXES for region in regions), 'explicit unique declared region scope')
    required = {f'reader-{region}-{role}.{ext}' for region in regions for role in ('primary', 'peer') for ext in ('py', 'json')}
    required |= {f'comparison-{region}-{repeat}.json' for region in regions for repeat in ('01', '02')}
    require(required <= set(FROZEN), 'all reader and comparator outputs must be frozen before replay')
    before = {name: pin(HERE / name) for name in FROZEN}
    for name, sha in FROZEN.items():
        require(before[name]['sha256'] == sha, 'frozen artifact pin: ' + name)
    for name in ('independent-comparison-force69-check.py', 'test_independent_comparison_force69.py'):
        before[name] = pin(HERE / name)
    context_check = read('context-independent-check.json')
    require(context_check['status'] == 'passed' and context_check['total_records_checked'] == 62231, 'prior context checker scope')
    require(equal(context_check['inputs_before'], context_check['inputs_after']), 'context checker input preservation')
    for name, value in context_check['inputs_before'].items():
        require(equal(pin(HERE / name), value), 'context receipt dependency: ' + name)
        before[name] = value
    old_root = HERE / '../force45'
    old = context_check['prior_force45_artifact_pins_before']
    require(equal(old, context_check['prior_force45_artifact_pins_after']), 'old artifact preservation receipt')
    old_before = {name: pin(old_root / name) for name in old}
    require(equal(old_before, old), 'all older force45 artifacts unchanged')
    context_bytes = (HERE / 'context01.json').read_bytes()
    require(context_bytes == (HERE / 'context02.json').read_bytes(), 'context byte-identical repeat')
    context = json.loads(context_bytes)
    for name, value in context['inputs'].items():
        require(equal(pin(HERE / name), value), 'raw context dependency pin')
        before[name] = value
    pixels = source_contexts(context)
    helper_trees = {role: ast.parse((HERE / name).read_text()) for role, name in
                    [('primary', 'primary_helper.py'), ('peer', 'peer_export.py')]}
    comparator_tree = ast.parse((HERE / 'compare_force69.py').read_text())
    results, selected_counts, white_results = {}, {}, {}
    for region in regions:
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
            helper_env = declarations(helper_trees[role])
            expected_pins = dict(helper_env['EXPECTED' if role == 'primary' else 'PINS'])
            if role == 'primary':
                expected_pins['primary_helper.py'] = FROZEN['primary_helper.py']
            require(set(data['inputs']) == set(expected_pins), 'exact annotation dependency roster')
            for name, sha in expected_pins.items():
                value = pin(HERE / name)
                require(value['sha256'] == sha and equal(data['inputs'][name], value), 'literal annotation dependency: ' + name)
                before[name] = dependencies[name] = value
            dependencies[script] = before[script]
            if role == 'peer':
                require(equal(data['expander_pin'], before['peer_export.py']), 'peer exporter pin')
                dependencies['peer_export.py'] = before['peer_export.py']
            independently_expanded = expand(region, role, tree, pixels[region], helper_trees[role], context)
            require(equal(data, independently_expanded), 'all literal annotation metadata and records: ' + stem)
            readers[role] = data
            bands[role] = validate(region, role, data)
            coverage(region, data, context)
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
    return {'status': 'passed_independent_force69_computational_check', 'inputs_before': before, 'inputs_after': after,
            'annotation_region_scope': regions, 'full_fixed_batch_annotation_audit': set(regions) == set(BOXES),
            'regions': results, 'source_context_records_rechecked': {region: len(values) for region, values in pixels.items()},
            'selected_cells_rechecked': selected_counts, 'selected_exact_white': white_results,
            'all_set_operations_checked': sum(result['set_operations_checked'] for result in results.values()),
            'all_reader_route_records_checked': sum(result['reader_route_records'] for result in results.values()),
            'all_unassigned_records_checked': sum(sum(result['reader_unassigned_records'].values()) for result in results.values()),
            'older_force45_pins_before': old_before, 'older_force45_pins_after': old_after,
            'older_force45_pin_count': len(old_before), 'reader_repeat_bytes_equal': True, 'comparison_repeat_bytes_equal': True,
            'synthetic_controls': 'Separate synthetic-only unittest suite; historical replay is not counted as a synthetic test.',
            'literal_replay': 'Inert AST data and separately authored expansion; no producer imports, exec, eval, or subprocess execution; no excluded metadata or records.',
            'runtime': {'python': platform.python_version(), 'pillow': pillow_version},
            'command': [sys.executable, '-B', str(Path(__file__).resolve())],
            'limits': [
                'Same-source nonblind computational check, not a new visual reading, human acceptance, or expert validation.',
                'Recorded reading coverage and perception are internally checked and replayed, not independently witnessed.',
                'Shared Pillow decoder family; fresh source RGB is not independent codec validation or historical authentication.',
                'Exact-white screening diagnoses one transcription-error class; nonwhite cells need not be curve ink.',
                'Region identities, including separate F7 and F9 sources, are retained; no seam join or cross-source coordinate union.',
                'Complete literal replay and set arithmetic establish no original-curve bounds, physical support, model discrepancy, cause, or intent.',
            ], 'human_accepted': False, 'physical_support': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', choices=list(BOXES), action='append')
    parser.add_argument('--output')
    args = parser.parse_args()
    regions = list(BOXES) if args.region is None else args.region
    stem = 'independent-comparison-force69' if set(regions) == set(BOXES) else 'independent-comparison-force69-' + '-'.join(regions)
    if args.output:
        require(args.output in [stem + '-check01.json', stem + '-check02.json'], 'fixed scoped audit output')
    value = run(regions)
    payload = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.output:
        out = HERE / args.output
        with out.open('x') as destination:
            destination.write(payload)
        print(json.dumps({'output': out.name, 'pin': pin(out), 'status': value['status']}))
    else:
        print(payload, end='')
