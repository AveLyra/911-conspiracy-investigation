"""Exact joint feasibility of frozen printed positions and centered velocities."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'multipoint-table-reproduction'
TRACKS = ('ne', 'ec', 'wc', 'nw')
SPANS = {'30': F(2, 5), '30000/1001': F(1001, 2500), '2997/100': F(400, 999)}
EPS = F(1, 200)
PINS = {
    OLD / 'transcription-root/table47.json': 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
    OLD / 'transcription-independent/table47.json': 'fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8',
    HERE.parent / 'luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf': 'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394',
}


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def validate_rows(rows):
    if not rows:
        raise ValueError('Empty table')
    ids = [r['row'] for r in rows]
    times = [F(r['time_s']) for r in rows]
    if len(set(ids)) != len(ids) or ids != sorted(ids):
        raise ValueError('Duplicate or unsorted source rows')
    if any(b-a != F(1, 5) for a, b in zip(times, times[1:])):
        raise ValueError('Nonuniform or duplicate nominal time grid')
    for r in rows:
        for track in TRACKS:
            for suffix in ('y', 'v'):
                value = r[track + '_' + suffix]
                if value is not None:
                    if not isinstance(value, str):
                        raise ValueError('Input tokens must remain strings or null')
                    F(value)


def build(rows, track, span):
    """Edge u->v,b denotes x[v]-x[u] <= b; anchor vertex is zero."""
    validate_rows(rows)
    present = [r for r in rows if r[track+'_y'] is not None]
    vertex = {r['row']: i+1 for i, r in enumerate(present)}
    indexed = {F(r['time_s']): r for r in rows}
    edges, supported, unsupported = [], [], []

    def edge(u, v, bound, label):
        edges.append({'u': u, 'v': v, 'bound': str(bound), 'label': label})

    for r in present:
        y, v = F(r[track+'_y']), vertex[r['row']]
        edge(0, v, y+EPS, f"position:{r['row']}:upper")
        edge(v, 0, -(y-EPS), f"position:{r['row']}:lower")
    for r in rows:
        if r[track+'_v'] is None:
            continue
        t = F(r['time_s'])
        previous, following = indexed.get(t-F(1, 5)), indexed.get(t+F(1, 5))
        if previous is None or following is None or any(
                p[track+'_y'] is None for p in (previous, following)):
            unsupported.append(r['row'])
            continue
        u, v = vertex[previous['row']], vertex[following['row']]
        velocity = F(r[track+'_v'])
        edge(u, v, span*(velocity+EPS), f"velocity:{r['row']}:upper")
        edge(v, u, -span*(velocity-EPS), f"velocity:{r['row']}:lower")
        supported.append({'row': r['row'], 'previous_row': previous['row'],
                          'following_row': following['row'], 'printed': r[track+'_v']})
    return {'vertex_rows': [None]+[r['row'] for r in present], 'edges': edges,
            'supported': supported, 'unsupported': unsupported}


def solve(n, edges):
    """Bellman-Ford with an implicit zero-weight supersource, exact rationals."""
    d, pred = [F(0) for _ in range(n)], [None]*n
    for _ in range(n):
        changed = None
        for index, e in enumerate(edges):
            candidate = d[e['u']] + F(e['bound'])
            if d[e['v']] > candidate:
                d[e['v']], pred[e['v']], changed = candidate, index, e['v']
        if changed is None:
            return {'feasible': True, 'vertices': [str(x-d[0]) for x in d]}
    x = changed
    for _ in range(n):
        x = edges[pred[x]]['u']
    cycle, current = [], x
    while True:
        index = pred[current]
        cycle.append(index)
        current = edges[index]['u']
        if current == x:
            break
        if len(cycle) > n:
            raise AssertionError('Invalid predecessor cycle')
    cycle.reverse()
    return {'feasible': False, 'cycle_edge_indices': cycle,
            'cycle_bound_sum': str(sum((F(edges[i]['bound']) for i in cycle), F(0)))}


def check_certificate(n, edges, result):
    """Check a witness/cycle without running the feasibility algorithm."""
    if result['feasible']:
        values = list(map(F, result['vertices']))
        assert len(values) == n and values[0] == 0
        slacks = [F(e['bound'])-(values[e['v']]-values[e['u']]) for e in edges]
        assert all(x >= 0 for x in slacks)
        return {'checked_edges': len(edges), 'witness_tight_edges': slacks.count(F(0))}
    cycle = result['cycle_edge_indices']
    assert cycle and all(isinstance(i, int) and 0 <= i < len(edges) for i in cycle)
    assert all(edges[a]['v'] == edges[b]['u'] for a, b in zip(cycle, cycle[1:]+cycle[:1]))
    total = sum((F(edges[i]['bound']) for i in cycle), F(0))
    assert total == F(result['cycle_bound_sum']) and total < 0
    return {'checked_cycle_edges': len(cycle), 'contradiction': f'0 <= {total} is false'}


def historical():
    before = {str(p): identity(p) for p in PINS}
    for p, pin in PINS.items():
        assert before[str(p)]['sha256'] == pin, p.name
    table = json.loads((OLD/'transcription-root/table47.json').read_text())
    other = json.loads((OLD/'transcription-independent/table47.json').read_text())
    mapping = {'time_s': 'time_s', 'ref_x': 'ref_building_x', 'ref_y': 'ref_building_y'}
    for short, long in zip(TRACKS, ('ne_corner', 'ec_roofline', 'wc_roofline', 'nw_corner')):
        for suffix in ('y', 'v'):
            mapping[short+'_'+suffix] = long+'_'+suffix
    assert len(table['rows']) == len(other['rows']) == 70
    for a, b in zip(table['rows'], other['rows']):
        assert a['row'] == b['source_row']
        assert all(a[k] == b[v] for k, v in mapping.items())
    cases = []
    for track in TRACKS:
        for clock, span in SPANS.items():
            graph = build(table['rows'], track, span)
            result = solve(len(graph['vertex_rows']), graph['edges'])
            verified = check_certificate(len(graph['vertex_rows']), graph['edges'], result)
            cases.append({'track': track, 'clock': clock, 'span': str(span),
                          **graph, **result, 'certificate_check': verified})
    assert all(identity(p) == before[str(p)] for p in PINS)
    pins = {**before, str(Path(__file__)): identity(Path(__file__)),
            str(HERE/'PROTOCOL.md'): identity(HERE/'PROTOCOL.md')}
    return {'schema': 'joint-table-consistency-v1', 'cases': cases, 'pins': pins,
            'rounding': 'closed +/-1/200; not a historical tie policy',
            'input_reconciliation': '70 rows, all 11 selected columns agree exactly'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Refusing existing output')
    result = historical()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'saved': args.output.name, 'cases': len(result['cases'])}))
