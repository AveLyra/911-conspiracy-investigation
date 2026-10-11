"""Validate and preserve literal native annotations; never infer curve support."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
FROZEN = {'PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
          'REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
          '../native-strips01/Im8.jpg': '0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83'}
TARGETS = {'E6': [515, 57, 690, 85], 'E7': [580, 14, 690, 30]}
STATUSES = {'identified_local_fragment', 'fringe_only', 'no_attributable_cells',
            'identity_conflict', 'boundary_truncated'}


def pin(path):
    data = Path(path).read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def rows(value, low, high):
    if (not isinstance(value, list) or any(type(y) is not int or not low <= y < high for y in value)
            or value != sorted(set(value))):
        raise ValueError('Invalid row set')
    return set(value)


def validate(record, pair):
    if pair not in TARGETS or record.get('pair') != pair:
        raise ValueError('Pair mismatch')
    aliases = [record[k] for k in ['target_box', 'target_rectangle_half_open'] if k in record]
    if 'target_box' in record.get('coverage', {}): aliases.append(record['coverage']['target_box'])
    if not aliases or any(v != TARGETS[pair] or not isinstance(v, list) or any(type(x) is not int for x in v) for v in aliases):
        raise ValueError('Target mismatch')
    target = aliases[0]
    if not isinstance(record.get('reader'), str) or not record['reader'].strip():
        raise ValueError('Missing reader')
    if not isinstance(record.get('routes'), dict) or set(record['routes']) != {'solid', 'dash'}:
        raise ValueError('Route coverage')
    x0, y0, x1, y1 = target
    for entries in record['routes'].values():
        if not isinstance(entries, list) or len(entries) != x1-x0:
            raise ValueError('Column coverage')
        for x, e in zip(range(x0, x1), entries):
            if not isinstance(e, dict) or type(e.get('x')) is not int or e['x'] != x:
                raise ValueError('Column identity/order')
            c, f = rows(e.get('core'), y0, y1), rows(e.get('fringe'), y0, y1)
            if c & f: raise ValueError('Class overlap')
            if e.get('status') not in STATUSES or not isinstance(e.get('note'), str) or not e['note'].strip():
                raise ValueError('Status/note')
            flags = []
            if c | f:
                if x == x0: flags.append('target_left')
                if x == x1-1: flags.append('target_right')
                if y0 in c | f: flags.append('target_top')
                if y1-1 in c | f: flags.append('target_bottom')
            actual = e.get('boundary_flags')
            if not isinstance(actual, list) or len(actual) != len(set(actual)) or set(actual) != set(flags):
                raise ValueError('Boundary flags')
            if e['status'] == 'no_attributable_cells' and c | f: raise ValueError('Nonempty absence status')
            if e['status'] == 'fringe_only' and (c or not f): raise ValueError('Invalid fringe-only status')
            if e['status'] == 'identified_local_fragment' and not c: raise ValueError('Identified without core')
            if e['status'] == 'boundary_truncated' and not flags: raise ValueError('Boundary status without boundary')
            ident = e.get('fragment_id')
            if ident is not None and (not isinstance(ident, str) or not ident.strip()):
                raise ValueError('Fragment ID')
            membership = e.get('fragment_membership')
            if membership is not None:
                if not isinstance(membership, dict): raise ValueError('Membership map')
                cc, ff = set(), set()
                for name, item in membership.items():
                    if not isinstance(name, str) or not name.strip() or not isinstance(item, dict):
                        raise ValueError('Membership item')
                    pc, pf = rows(item.get('core'), y0, y1), rows(item.get('fringe'), y0, y1)
                    if pc & pf: raise ValueError('Membership overlap')
                    cc |= pc; ff |= pf
                if cc != c or ff != f: raise ValueError('Membership union')
                if ident is not None and set(membership) != {ident}: raise ValueError('Inconsistent ID')
            elif c | f:
                unresolved_fringe = not c and bool(f) and e['status'] in ('fringe_only', 'boundary_truncated')
                if ident is None and e['status'] != 'identity_conflict' and not unresolved_fringe:
                    raise ValueError('Missing attribution or explicit conflict')
    return record['routes']


def family(a, b):
    return dict(intersection=sorted(a & b), union=sorted(a | b),
                root_only=sorted(a-b), peer_only=sorted(b-a), symmetric_difference=sorted(a ^ b))


def identity(e):
    m = e.get('fragment_membership')
    return {'explicit_single_id': e.get('fragment_id') is not None,
            'membership_count': len(m) if m is not None else None,
            'explicit_conflict': e['status'] == 'identity_conflict',
            'unknown_attribution': e.get('fragment_id') is None and not m}


def compare(root, peer, pair):
    a, b = validate(root, pair), validate(peer, pair)
    result = []
    for route in ['solid', 'dash']:
        for left, right in zip(a[route], b[route]):
            c, f = set(left['core']), set(left['fringe'])
            d, g = set(right['core']), set(right['fringe'])
            result.append({'route': route, 'x': left['x'], 'root': copy.deepcopy(left),
                           'peer': copy.deepcopy(right), 'core': family(c, d),
                           'fringe': family(f, g), 'outer': family(c | f, d | g),
                           'status_equal': left['status'] == right['status'],
                           'root_identity': identity(left), 'peer_identity': identity(right)})
    return result


def save(path, result):
    with Path(path).open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def declared_paths(record):
    found = {}
    def add(path, value):
        if not isinstance(value, dict) or not isinstance(value.get('sha256'), str) or len(value['sha256']) != 64 or any(c not in '0123456789abcdef' for c in value['sha256']):
            raise ValueError('Malformed pin')
        if 'bytes' in value and (type(value['bytes']) is not int or value['bytes'] < 0): raise ValueError('Malformed byte count')
        if path in found and found[path]['sha256'] != value['sha256']: raise ValueError('Contradictory pins')
        found[path] = value
    for name, value in record.get('inputs', {}).items():
        add((HERE/name).resolve(), value)
    # Explicit adapter for the frozen E6 peer schema, not filename inference.
    adapter = {'source_sha256': '../native-strips01/Im8.jpg', 'protocol_sha256': 'PROTOCOL.md',
               'roster_sha256': 'REGIONS.json', 'raw_context_sha256': 'context01.json',
               'literal_script_sha256': 'reader-E6-independent.py'}
    for key, value in record.get('pins', {}).items():
        if isinstance(value, str):
            if record.get('pair') != 'E6' or key not in adapter: raise ValueError('Unknown pin schema')
            add((HERE/adapter[key]).resolve(), {'sha256': value})
        elif isinstance(value, dict) and isinstance(value.get('path'), str):
            add(Path(value['path']).resolve(), value)
        else: raise ValueError('Malformed pin schema')
    if 'script_pin' in record:
        if record.get('pair') not in TARGETS: raise ValueError('Unknown root script pair')
        add((HERE/f"reader-{record['pair']}-root.py").resolve(), record['script_pin'])
    return found


def run(root_path, peer_path, pair, output):
    if Path(output).exists(): raise FileExistsError('Preserve existing output')
    reader_before = {str(Path(p).resolve()): pin(p) for p in [root_path, peer_path]}
    for name, expected in FROZEN.items():
        if pin(HERE/name)['sha256'] != expected: raise ValueError('Frozen input changed')
    root, peer = [json.loads(Path(p).read_text()) for p in [root_path, peer_path]]
    declarations = [declared_paths(r) for r in [root, peer]]
    mandatory = {(HERE/n).resolve() for n in ['PROTOCOL.md', 'REGIONS.json', '../native-strips01/Im8.jpg']}
    for declared in declarations:
        if not mandatory <= set(declared): raise ValueError('Missing mandatory pins')
        for path, expected in declared.items():
            actual = pin(path)
            if actual['sha256'] != expected['sha256'] or ('bytes' in expected and actual['bytes'] != expected['bytes']):
                raise ValueError('Declared pin mismatch')
    page = (HERE/'../render01/page-076.png').resolve()
    paths = set().union(*[set(d) for d in declarations]) | {Path(root_path).resolve(), Path(peer_path).resolve(), Path(__file__).resolve(), page}
    before = {str(p): pin(p) for p in sorted(paths)}
    if any(before[p] != value for p, value in reader_before.items()):
        raise ValueError('Reader changed during load')
    result = compare(root, peer, pair)
    after = {str(p): pin(p) for p in sorted(paths)}
    if before != after: raise ValueError('Inputs changed')
    save(output, {'pair': pair, 'rows': result, 'inputs': before, 'inputs_after': after,
                  'additional_verifier_pins': {'composed_page': str(page), 'reason': 'Verifier pins page independently; not a claim every reader originally declared it.'},
                  'python': platform.python_version(), 'limits': 'Annotation sets only. Local IDs are not equated across readers; no support or human acceptance.'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--peer', required=True, type=Path)
    parser.add_argument('--pair', required=True, choices=TARGETS)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    run(args.root, args.peer, args.pair, args.output)
