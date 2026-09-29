#!/usr/bin/env python3
"""Numeric-only, create-only source trace; never runs a structural solver."""
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
HELPER = HERE.parent / 'model-member-map/map_members.py'
HELPER_SHA = 'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA
spec = importlib.util.spec_from_file_location('pinned_member_reader', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def decimal_text(value):
    try:
        d = Decimal(value.decode('ascii').replace('D', 'E').replace('d', 'e'))
    except (InvalidOperation, UnicodeError):
        raise m.CardError('decimal_syntax') from None
    m.require(d.is_finite(), 'decimal_nonfinite')
    return '0' if not d else format(d.normalize(), 'f')


def mesh_records(lines, coordinate_ids=frozenset()):
    """Yield typed elements and selected coordinates; skip arbitrary metadata."""
    keyword, pending, ended = b'', None, False
    for line, raw in lines:
        s = raw.strip()
        if not s or s.startswith(b'$'):
            continue
        m.require(not ended, 'data_after_end')
        if s.startswith(b'*'):
            m.require(pending is None, 'missing_thickness')
            keyword = s.upper()
            ended = keyword == b'*END'
            if keyword.startswith(b'*ELEMENT_'):
                m.require(keyword in (b'*ELEMENT_SHELL_THICKNESS', b'*ELEMENT_BEAM',
                                      b'*ELEMENT_DISCRETE', b'*ELEMENT_SOLID'), 'element_variant')
            if keyword.startswith(b'*NODE'):
                m.require(keyword == b'*NODE', 'node_variant')
            continue
        if keyword == b'*NODE':
            nid = m.integer(raw.split(b',')[0] if b',' in raw else raw[:8])
            if nid in coordinate_ids:
                row = m.fields(raw, [8, 16, 16, 16, 8, 8])
                yield ('node', line, nid, tuple(decimal_text(v) for v in row[1:4]))
        elif keyword == b'*ELEMENT_SHELL_THICKNESS':
            if pending is None:
                row = m.id_card(raw, 8, 10)
                m.require(len(row) >= 6 and not any(row[6:]), 'shell_arity')
                pending = ('shell', line, row[0], row[1], tuple(row[2:6]))
            else:
                row = m.values_card(raw, 16, 5)
                m.require(len(row) >= 4 and all(v is not None and v >= 0 for v in row[:4]),
                          'thickness_value')
                yield pending
                pending = None
        elif keyword in (b'*ELEMENT_BEAM', b'*ELEMENT_DISCRETE', b'*ELEMENT_SOLID'):
            kind = {b'*ELEMENT_BEAM': 'beam', b'*ELEMENT_DISCRETE': 'discrete',
                    b'*ELEMENT_SOLID': 'solid'}[keyword]
            widths = [8] * 5 + [16, 8, 16] if kind == 'discrete' else [8] * 10
            fields = m.fields(raw, widths)
            take = 10 if kind == 'solid' else 4
            m.require(len(fields) >= take, 'element_arity')
            row = [m.integer(v, 0) for v in fields[:take]]
            m.require(row[0] > 0 and row[1] > 0, 'element_id')
            m.require(all(n > 0 or (kind == 'discrete' and i == 1 and n == 0)
                          for i, n in enumerate(row[2:])), 'endpoint_id')
            yield (kind, line, row[0], row[1], tuple(n for n in row[2:] if n))
    m.require(pending is None, 'missing_thickness_eof')


def thermal_trace(lines, targets):
    selected = {n: [] for n in targets}
    all_nodes = {}
    runs, previous, rows, keyword, ended = [], None, 0, b'', False
    keyword_counts = Counter()
    bases, curves = Counter(), Counter()
    for line, raw in lines:
        s = raw.strip()
        if not s or s.startswith(b'$'):
            continue
        m.require(not ended, 'thermal_after_end')
        if s.startswith(b'*'):
            m.require(s in (b'*KEYWORD', b'*LOAD_THERMAL_VARIABLE_NODE', b'*END'),
                      'thermal_keyword')
            keyword = s
            keyword_counts[s.decode('ascii')] += 1
            ended = s == b'*END'
            continue
        m.require(keyword == b'*LOAD_THERMAL_VARIABLE_NODE', 'thermal_outside_load')
        fields = m.fields(raw, [10] * 4)
        m.require(len(fields) == 4, 'thermal_arity')
        nid, ts, tb, lcid = (m.integer(fields[0]), decimal_text(fields[1]),
                             decimal_text(fields[2]), m.integer(fields[3]))
        m.require(0 < nid < m.ID_CAP, 'thermal_nid')
        rows += 1
        if previous is None or nid < previous:
            runs.append({'run': len(runs) + 1, 'first_line': line, 'last_line': line,
                         'first_nid': nid, 'last_nid': nid, 'rows': 0})
            m.require(len(runs) <= 10000, 'run_cap')
        runs[-1].update(last_line=line, last_nid=nid, rows=runs[-1]['rows'] + 1)
        previous = nid
        bases[tb] += 1
        curves[lcid] += 1
        d = Decimal(ts)
        if nid in all_nodes:
            entry = all_nodes[nid]
            entry[0] += 1
            entry[1], entry[2] = min(entry[1], d), max(entry[2], d)
        else:
            all_nodes[nid] = [1, d, d]
        if nid in targets:
            selected[nid].append({'line': line, 'row': rows, 'run': len(runs),
                                  'nid': nid, 'TS': ts, 'TB': tb, 'LCID': lcid})
    m.require(sum(map(len, selected.values())) <= 20000, 'selected_row_cap')
    counts = Counter(e[0] for e in all_nodes.values())
    return {'rows': rows, 'unique_nodes': len(all_nodes),
            'nodes_repeated': sum(v for k, v in counts.items() if k > 1),
            'nodes_unequal_TS': sum(e[1] != e[2] for e in all_nodes.values()),
            'multiplicity': dict(sorted(counts.items())), 'bases': dict(bases),
            'curves': dict(curves), 'keywords': dict(keyword_counts),
            'ordering_runs': runs}, selected


def collect():
    receipts = []
    reader = m.Reader()
    region, region_elements = set(), []
    for kind, line, eid, pid, nodes in mesh_records(reader.lines(m.MASTER)):
        if kind == 'shell' and pid == 179:
            region.update(nodes)
            region_elements.append({'line': line, 'eid': eid})
    receipts.append({'pass': 'select_region', 'sources': reader.receipts})
    targets = region | {842747, 842833}
    m.require(len(targets) <= 2000, 'target_cap')
    reader = m.Reader()
    thermal, traces = thermal_trace(reader.lines(m.THERMAL), targets)
    receipts.append({'pass': 'thermal_order', 'sources': reader.receipts})
    coords, incidence, mesh_counts = {}, defaultdict(Counter), Counter()
    for name, offset in ((m.MASTER, 0), (m.OUTSIDE, 1000), (m.MASS, 0)):
        reader = m.Reader()
        for rec in mesh_records(reader.lines(name), targets):
            if rec[0] == 'node':
                _, line, nid, xyz = rec
                m.require(nid not in coords, 'duplicate_target_coordinates')
                coords[nid] = {'source': name, 'line': line, 'xyz': xyz}
            else:
                kind, line, eid, pid, nodes = rec
                mesh_counts[name + ':' + kind] += 1
                for nid in set(nodes) & targets:
                    incidence[nid][(pid + offset, kind)] += 1
        receipts.append({'pass': 'target_incidence', 'sources': reader.receipts})
    records = []
    groups = Counter()
    for nid in sorted(targets):
        unequal = len({r['TS'] for r in traces[nid]}) > 1
        part_count = len({p for p, k in incidence[nid]})
        groups[('region179' if nid in region else 'exception', len(traces[nid]), unequal,
                part_count)] += 1
        records.append({'nid': nid, 'region179': nid in region,
                        'coordinates': coords.get(nid), 'assignments': traces[nid],
                        'unequal_TS': unequal,
                        'incidence': [{'pid': p, 'kind': k, 'elements': n}
                                      for (p, k), n in sorted(incidence[nid].items())]})
    return {'scope': 'supplied_rows_not_solver_temperatures', 'region_pid': 179,
            'region_nodes': sorted(region), 'region_shells': region_elements,
            'mesh_counts': dict(mesh_counts), 'thermal': thermal, 'nodes': records,
            'groups': [{'selection': s, 'assignment_count': a, 'unequal_TS': u,
                        'part_count': p, 'nodes': n}
                       for (s, a, u, p), n in sorted(groups.items())],
            'source_receipts': receipts}


class Controls(unittest.TestCase):
    def test_decimal_fixed_free(self):
        self.assertEqual(decimal_text(b'2.500D+1'), '25')
        fixed = b'%10d%10.2f%10.2f%10d' % (1, 25, 0, 2)
        a = thermal_trace(enumerate([b'*LOAD_THERMAL_VARIABLE_NODE', fixed], 1), {1})
        b = thermal_trace(enumerate([b'*LOAD_THERMAL_VARIABLE_NODE', b'1,25,0,2'], 1), {1})
        self.assertEqual(a, b)

    def test_repeat_order_and_conflict(self):
        lines = [b'*LOAD_THERMAL_VARIABLE_NODE', b'1,25,0,2', b'1,25,0,2',
                 b'2,40,0,2', b'1,100,0,2', b'*END']
        a, b = thermal_trace(enumerate(lines, 1), {1})
        self.assertEqual([r['rows'] for r in a['ordering_runs']], [3, 1])
        self.assertEqual(a['nodes_unequal_TS'], 1)
        self.assertEqual([v['row'] for v in b[1]], [1, 2, 4])
        self.assertEqual([v['run'] for v in b[1]], [1, 1, 2])

    def test_shell_continuation_and_triangle(self):
        r = list(mesh_records(enumerate([b'*ELEMENT_SHELL_THICKNESS', b'1,179,1,2,3,3',
                                         b'.1,.1,.1,.1', b'*END'], 1)))
        self.assertEqual(r, [('shell', 2, 1, 179, (1, 2, 3, 3))])

    def test_beam_orientation_and_ground(self):
        r = list(mesh_records(enumerate([b'*ELEMENT_BEAM', b'1,2,3,4,999',
                                         b'*ELEMENT_DISCRETE', b'5,6,7,0,888,1,0,0'], 1)))
        self.assertEqual(r[0][-1], (3, 4))
        self.assertEqual(r[1][-1], (7,))

    def test_shared_incidence_offset(self):
        counts = Counter()
        for pid, offset, nodes in [(2, 1000, (1, 1, 3)), (5, 0, (1, 4))]:
            for n in set(nodes) & {1}:
                counts[(n, pid + offset)] += 1
        self.assertEqual(counts, {(1, 1002): 1, (1, 5): 1})

    def test_rejections(self):
        for body in ([b'*ELEMENT_SHELL_THICKNESS', b'1,2,3,4,5,6', b'*END'],
                     [b'*ELEMENT_SHELL_OFFSET'], [b'*NODE_EXTRA'],
                     [b'*END', b'1,2,3,4']):
            with self.assertRaises(m.CardError):
                list(mesh_records(enumerate(body, 1)))
        for val in (b'NaN', b'Infinity', b'private-unparsed-label'):
            with self.assertRaises(m.CardError):
                decimal_text(val)
        with self.assertRaises(m.CardError):
            thermal_trace(enumerate([b'*LOAD_OTHER', b'1,2,3,4'], 1), {1})

    def test_reader_caps(self):
        import gzip
        with tempfile.TemporaryDirectory(prefix='thermal-trace-control-') as td:
            p = Path(td) / 'synthetic.gz'
            p.write_bytes(gzip.compress(b'12345678\n12345678\n', mtime=0))
            with patch.object(m, 'SOURCE', Path(td)), patch.object(m, 'PINS',
                    {'synthetic.gz': (p.stat().st_size, m.digest(p))}):
                for key, value in [('LINE_CAP', 4), ('BYTE_CAP', 12)]:
                    with patch.object(m, key, value), self.assertRaises(m.CardError):
                        list(m.Reader().lines('synthetic.gz'))

    def test_ordering_run_cap(self):
        rows = [b'*LOAD_THERMAL_VARIABLE_NODE'] + [b'2,25,0,2', b'1,25,0,2'] * 10001
        with self.assertRaises(m.CardError):
            thermal_trace(enumerate(rows, 1), set())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output')
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    test = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    if not test.wasSuccessful():
        return 1
    if args.controls:
        return 0
    dest = HERE / args.output if args.output else None
    if dest is None or dest.parent != HERE or dest.exists():
        print(json.dumps({'status': 'REFUSED', 'code': 'create_only_output'}))
        return 2
    start = time.monotonic()
    receipt = {'code_sha256': m.digest(Path(__file__)), 'helper_sha256': HELPER_SHA,
               'protocol_sha256': m.digest(HERE / 'PROTOCOL.md'), 'python': sys.version,
               'command': sys.argv, 'controls': test.testsRun}
    try:
        result = collect()
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = peak if sys.platform == 'darwin' else peak * 1024
        m.require(peak_bytes <= 768 * 1024 ** 2, 'memory_cap')
        receipt.update(status='PASS', peak_memory_bytes=peak_bytes, result=result)
    except Exception as exc:
        receipt.update(status='FAIL', error=exc.code if isinstance(exc, m.CardError) else type(exc).__name__)
    receipt['elapsed_seconds'] = time.monotonic() - start
    with dest.open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'elapsed_seconds')}))
    return 0 if receipt['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
