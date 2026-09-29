#!/usr/bin/env python3
"""Independent exact interval-chain feasibility; no producer imports or media."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
BASE = UNIT.parent
OLD = BASE / 'multipoint-table-reproduction'
EPS = F(1, 200)
SPANS = {'nominal_30': F(12, 30),
         'nominal_30000_1001': F(12, F(30000, 1001)),
         'average_2997_100': F(12, F(2997, 100))}
POINTS = {'NE': 'ne_corner', 'EC': 'ec_roofline',
          'WC': 'wc_roofline', 'NW': 'nw_corner'}
PINS = {
    UNIT/'PROTOCOL.md': '4ed21c2fae4d36869588130321767134d72539fb618f47168e6c6170026300c0',
    OLD/'PROTOCOL.md': '85c1570d523fa8514e9596ecc36e85bc1299586f0a70b0211c38f3725eb59aac',
    OLD/'CLOCK-ADDENDUM.md': '198d31a14ca49368bfc00c64ed3d4827d8fea9d7045a4f2a090e75a5ec6a866f',
    OLD/'transcription-independent/table47.json': 'fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8',
    OLD/'transcription-root/table47.json': 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
    BASE/'luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf': 'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394',
}


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def decimal(token, nullable=False):
    if token is None and nullable:
        return None
    if not isinstance(token, str) or not re.fullmatch(r'-?\d+\.\d+', token):
        raise ValueError('Expected a preserved decimal token or permitted null')
    return F(token)


def validate_rows(rows):
    """Reject reordering/gaps in the nominal grid; never sort or fill data."""
    if not rows:
        raise ValueError('Empty table')
    first = decimal(rows[0]['time_s'])
    for i, row in enumerate(rows):
        if row['source_row'] != i + 1 or type(row['source_row']) is not int:
            raise ValueError('Duplicate, unsorted or nonconsecutive source rows')
        if decimal(row['time_s']) != first + F(i, 5):
            raise ValueError('Unsorted or non-grid time')
        for prefix in POINTS.values():
            decimal(row[prefix+'_y'], True)
            decimal(row[prefix+'_v'], True)


def reconcile(root, independent):
    a, b = root['rows'], independent['rows']
    aliases = {'time_s': 'time_s', 'ref_x': 'ref_building_x', 'ref_y': 'ref_building_y'}
    for short, long in zip(('ne', 'ec', 'wc', 'nw'), POINTS.values()):
        for suffix in ('y', 'v'):
            aliases[short+'_'+suffix] = long+'_'+suffix
    if set(aliases) != set(root['columns']) or len(a) != len(b) or len(a) != 70:
        raise ValueError('Transcription schema/coverage mismatch')
    count = 0
    for ar, br in zip(a, b):
        if ar['row'] != br['source_row']:
            raise ValueError('Transcription row mismatch')
        for old, new in aliases.items():
            if ar[old] != br[new]:
                raise ValueError('Transcription token mismatch')
            count += ar[old] is not None
    validate_rows(b)
    if decimal(b[0]['time_s']) != -1 or decimal(b[-1]['time_s']) != F(64, 5):
        raise ValueError('Wrong fixed table extent')
    return {'rows': 70, 'columns': 11, 'numeric_tokens': count, 'nulls': 770-count}


def problem(rows, prefix, span):
    if span <= 0:
        raise ValueError('Nonpositive span')
    bounds, links, unsupported = {}, [], []
    for i, row in enumerate(rows):
        y = decimal(row[prefix+'_y'], True)
        if y is not None:
            bounds[i] = (y-EPS, y+EPS)
    for i, row in enumerate(rows):
        v = decimal(row[prefix+'_v'], True)
        if v is None:
            continue
        if i-1 not in bounds or i+1 not in bounds:
            unsupported.append({'source_row': row['source_row'], 'time_s': row['time_s'],
                                'velocity_token': row[prefix+'_v'],
                                'reason': 'missing preceding or following position'})
        else:
            links.append({'left': i-1, 'right': i+1, 'center': i,
                          'lo': span*(v-EPS), 'hi': span*(v+EPS)})
    return bounds, links, unsupported


def primitive_inequalities(bounds, links):
    """Each atom is sum(coeff*x) <= rhs, reconstructed from original inputs."""
    atoms = {}
    for i, (lo, hi) in bounds.items():
        if lo > hi:
            raise ValueError('Reversed position bounds')
        atoms[f'p:{i}:lower'] = ({i: -1}, -lo)
        atoms[f'p:{i}:upper'] = ({i: 1}, hi)
    for link in links:
        a, b, c = link['left'], link['right'], link['center']
        if b != a+2 or c != a+1 or a not in bounds or b not in bounds:
            raise ValueError('Not a valid disjoint sample-chain edge')
        if link['lo'] > link['hi'] or f'd:{c}:lower' in atoms:
            raise ValueError('Reversed or duplicate difference constraint')
        atoms[f'd:{c}:lower'] = ({a: 1, b: -1}, -link['lo'])
        atoms[f'd:{c}:upper'] = ({a: -1, b: 1}, link['hi'])
    return atoms


def validate_certificate(bounds, links, certificate):
    atoms = primitive_inequalities(bounds, links)
    total, rhs = {}, F(0)
    if not certificate['atoms']:
        raise ValueError('Empty certificate')
    for key in certificate['atoms']:
        if key not in atoms:
            raise ValueError('Certificate names a nonexistent input inequality')
        coeffs, value = atoms[key]
        rhs += value
        for i, coefficient in coeffs.items():
            total[i] = total.get(i, 0) + coefficient
    if any(total.values()) or rhs >= 0 or rhs != F(certificate['sum_rhs']):
        raise ValueError('Certificate does not prove zero <= negative')
    return True


def validate_witness(bounds, links, witness):
    values = {int(k): F(v) for k, v in witness.items()}
    if set(values) != set(bounds) or len(values) != len(witness):
        raise ValueError('Incomplete or duplicate witness variables')
    for i, (lo, hi) in bounds.items():
        if not lo <= values[i] <= hi:
            raise ValueError('Witness violates original position bound')
    for link in links:
        delta = values[link['right']]-values[link['left']]
        if not link['lo'] <= delta <= link['hi']:
            raise ValueError('Witness violates original derivative bound')
    return True


def forward(bounds, links, strict=False):
    """Exact reachability on each disjoint path, including isolated positions.

    All constraints are open when strict=True. Minkowski addition and
    intersection of open intervals stay open, so equality is then empty.
    Closed mode retains equality. No epsilon/tolerance search is used.
    """
    primitive_inequalities(bounds, links)
    incoming = {e['right']: e for e in links}
    outgoing = {e['left']: e for e in links}
    if len(incoming) != len(links) or len(outgoing) != len(links):
        raise ValueError('Branching sample chain')
    chains, witness, visited = [], {}, set()
    for start in sorted(set(bounds)-set(incoming)):
        nodes, edges = [start], []
        while nodes[-1] in outgoing:
            edge = outgoing[nodes[-1]]
            edges.append(edge)
            nodes.append(edge['right'])
        visited.update(nodes)
        lo, hi = bounds[start]
        lows, highs = [f'p:{start}:lower'], [f'p:{start}:upper']
        reach = [(lo, hi)]
        failure = None
        if lo > hi or (strict and lo == hi):
            failure = {'at_node': start, 'lower': lo, 'upper': hi}
        for edge in edges:
            if failure is not None:
                break
            node, center = edge['right'], edge['center']
            candidate_lo, candidate_hi = lo+edge['lo'], hi+edge['hi']
            orig_lo, orig_hi = bounds[node]
            if orig_lo >= candidate_lo:
                lo, lows = orig_lo, [f'p:{node}:lower']
            else:
                lo, lows = candidate_lo, lows+[f'd:{center}:lower']
            if orig_hi <= candidate_hi:
                hi, highs = orig_hi, [f'p:{node}:upper']
            else:
                hi, highs = candidate_hi, highs+[f'd:{center}:upper']
            reach.append((lo, hi))
            if lo > hi or (strict and lo == hi):
                failure = {'at_node': node, 'lower': lo, 'upper': hi}
                if not strict:
                    failure['certificate'] = {'atoms': lows+highs, 'sum_rhs': hi-lo}
                    validate_certificate(bounds, links, failure['certificate'])
        result = {'nodes': nodes, 'source_rows': [i+1 for i in nodes],
                  'velocity_source_rows': [e['center']+1 for e in edges],
                  'reachable_prefix': reach, 'feasible': failure is None}
        if failure:
            result['contradiction'] = failure
        elif not strict:
            # Reconstruct backwards, intersecting each reachable prefix with
            # the exact preimage of the already chosen following position.
            value = (reach[-1][0]+reach[-1][1])/2
            witness[nodes[-1]] = value
            for j in range(len(edges)-1, -1, -1):
                edge = edges[j]
                left_lo = max(reach[j][0], value-edge['hi'])
                left_hi = min(reach[j][1], value-edge['lo'])
                if left_lo > left_hi:
                    raise AssertionError('Backwards witness has empty preimage')
                value = (left_lo+left_hi)/2
                witness[nodes[j]] = value
        chains.append(result)
    if visited != set(bounds):
        raise ValueError('Unvisited variables/cycle in chain graph')
    feasible = all(c['feasible'] for c in chains)
    if feasible and not strict:
        validate_witness(bounds, links, witness)
    return {'feasible': feasible, 'chains': chains,
            'witness': witness if feasible and not strict else None}


def solve(bounds, links):
    result = forward(bounds, links)
    if result['feasible']:
        strict = forward(bounds, links, True)
        result['all_constraints_strictly_feasible'] = strict['feasible']
        result['boundary_only'] = not strict['feasible']
    else:
        result['all_constraints_strictly_feasible'] = False
        result['boundary_only'] = None
    return result


def save(path, data):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, sort_keys=True, default=str, allow_nan=False)
        handle.write('\n')


def create_output(path):
    path.mkdir()


def run(name):
    out = HERE/name
    if out.exists():
        raise FileExistsError('Refusing existing oracle output')
    from test_chain_oracle import run_controls
    controls = run_controls()  # Must pass before historical inputs are loaded.
    snapshots = {}
    for path, pin in PINS.items():
        data = path.read_bytes()
        if identity(data)['sha256'] != pin:
            raise ValueError('Pinned input changed: '+path.name)
        snapshots[path] = data
    for path in (HERE/'chain_oracle.py', HERE/'test_chain_oracle.py', Path(sys.executable)):
        snapshots[path] = path.read_bytes()
    before = {str(p): identity(b) for p, b in snapshots.items()}
    a = json.loads(snapshots[OLD/'transcription-root/table47.json'])
    b = json.loads(snapshots[OLD/'transcription-independent/table47.json'])
    reconciliation = reconcile(a, b)
    if b['source_sha256'] != PINS[BASE/'luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf']:
        raise ValueError('Transcription source identity mismatch')
    create_output(out)
    save(out/'start.json', {'pins_before': before, 'argv': sys.argv,
                           'controls': controls, 'python': sys.version})
    cases = []
    for point, prefix in POINTS.items():
        for clock, span in SPANS.items():
            bounds, links, unsupported = problem(b['rows'], prefix, span)
            result = solve(bounds, links)
            rowwise = [e['center']+1 for e in links
                       if max(bounds[e['right']][0]-bounds[e['left']][1], e['lo'])
                       > min(bounds[e['right']][1]-bounds[e['left']][0], e['hi'])]
            cases.append({'point': point, 'clock': clock, 'span': span,
                          'position_count': len(bounds), 'velocity_constraints': len(links),
                          'unsupported_velocities': unsupported,
                          'position_bounds': bounds, 'difference_constraints': links,
                          'rowwise_incompatible_source_rows': rowwise, **result})
    for clock in SPANS:
        group = [c for c in cases if c['clock'] == clock]
        if sum(c['velocity_constraints'] for c in group) != 161:
            raise ValueError('Supported-row count differs from fixed prior study')
        unsupported = [(c['point'], u['source_row']) for c in group for u in c['unsupported_velocities']]
        if unsupported != [('NW', 1)]:
            raise ValueError('Unsupported-row membership changed')
    save(out/'results.json', {'method': 'exact disjoint interval-chain reachability',
                            'reconciliation': reconciliation, 'rounding_half_width': EPS,
                            'cases': cases, 'controls': controls,
                            'scope': 'printed-table consistency; not historical measurement'})
    after = {str(p): identity(p.read_bytes()) for p in snapshots}
    if before != after:
        raise ValueError('An input/code/runtime changed during calculation')
    save(out/'receipt.json', {'status': 'complete', 'pins_before': before, 'pins_after': after,
                             'products': {p.name: identity(p.read_bytes()) for p in sorted(out.iterdir())},
                             'cases': len(cases), 'controls': controls})
    # Deliberately no finding details before the independent-results exchange.
    print(json.dumps({'status': 'frozen', 'run': name, 'cases': len(cases),
                      'controls': len(controls), 'results': identity((out/'results.json').read_bytes())}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', choices=['run01', 'run02'])
    run(parser.parse_args().run)
