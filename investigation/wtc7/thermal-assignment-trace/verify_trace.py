#!/usr/bin/env python3
"""Independent numeric-only row trace; no producer import or solver behavior."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import sys
import time

BASE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PINS = {
    118: ('WTC7_CaseB_400pm.int.gz', 2702040, '51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447', 34808082, 'fa721837357cf7b7fd43e49d2a9d171973663e12399c503163ef56c3464b060d'),
    119: ('discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7', 508372, '8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
    120: ('elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59', 232959541, '7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
    121: ('wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d', 333947423, '8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}
PROTOCOL_SHA = '94922827e48709fcac6b4c2dea5329c93e6ce71f75cfb484912545cf2dfa292f'
DEPENDENCY = BASE.parent / 'model-member-map' / 'independent-checkpoint01.json'
DEPENDENCY_SHA = '85e2649cdc2ccc2974f4959e5f19bb8d01f8533e16326bb2647c092252bcbd2e'
BYTE_CAP, LINE_CAP = 512 * 1024**2, 16384
NODE_CAP, RUN_CAP, ROW_CAP = 2000, 10000, 20000
MEM_CAP = 768 * 1024**2
INTEGER = re.compile(r'[+-]?[0-9]+\Z')
NUMERIC = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eEdD][+-]?[0-9]+)?\Z')
ALLOWED = {'NODE', 'ELEMENT_SHELL_THICKNESS', 'ELEMENT_BEAM', 'ELEMENT_DISCRETE', 'ELEMENT_SOLID', 'LOAD_THERMAL_VARIABLE_NODE'}
PROGRESS = []


class TraceError(Exception):
    def __init__(self, code, src=0, line=0):
        self.code, self.src, self.line = code, src, line
        super().__init__(code)


def check(value, code, src=0, line=0):
    if not value:
        raise TraceError(code, src, line)


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def scalar(token, integer=False):
    token = token.strip()
    if not token:
        return 0 if integer else '0'
    check(bool((INTEGER if integer else NUMERIC).fullmatch(token)), 'invalid_numeric_token')
    if integer:
        return int(token)
    try:
        v = Decimal(token.replace('D', 'E').replace('d', 'e'))
    except InvalidOperation:
        raise TraceError('invalid_decimal') from None
    check(v.is_finite(), 'nonfinite_decimal')
    check(abs(v.adjusted()) < 1000 or not v, 'decimal_exponent_cap')
    s = format(v, 'f')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return '0' if not v else s


def fields(text, widths, integers=(), required=0):
    text = text.split('$', 1)[0].rstrip('\r\n')
    ints = set(integers)
    if ',' in text:
        pieces = text.split(',')
        check(len(pieces) <= len(widths), 'extra_fields')
    else:
        check(not text[sum(widths):].strip(), 'fixed_width_overflow')
        pieces, pos = [], 0
        for width in widths:
            pieces.append(text[pos:pos + width]); pos += width
        valid = all(not p.strip() or (INTEGER if i in ints else NUMERIC).fullmatch(p.strip()) for i, p in enumerate(pieces))
        if not valid:
            pieces = text.split()
            check(required <= len(pieces) <= len(widths), 'free_field_count')
    pieces += [''] * (len(widths) - len(pieces))
    check(all(p.strip() for p in pieces[:required]), 'missing_required_field')
    return tuple(scalar(p, i in ints) for i, p in enumerate(pieces))


def node_identifier(text):
    if ',' in text:
        token = text.split(',', 1)[0]
    else:
        token = text[:8]
        if not INTEGER.fullmatch(token.strip()):
            token = text.split()[0] if text.split() else ''
    check(bool(token.strip()), 'missing_node_id')
    return scalar(token, True)


def typed_stream(src, fileobj, phase, selected=None):
    """All bytes hashed; only required typed cards parsed, never arbitrary text."""
    state = {'src': src, 'phase': phase, 'lines': 0, 'bytes': 0, 'eof': False}
    PROGRESS.append(state)
    h, keyword, pending = hashlib.sha256(), None, None
    counts = Counter()
    while True:
        raw = fileobj.readline(LINE_CAP + 1)
        if not raw:
            check(pending is None, 'missing_continuation', src, state['lines'])
            state.update(eof=True, sha256=h.hexdigest(), typed_records=dict(sorted(counts.items())))
            return
        state['lines'] += 1; state['bytes'] += len(raw)
        line = state['lines']
        check(len(raw) <= LINE_CAP, 'line_cap', src, line)
        check(state['bytes'] <= BYTE_CAP, 'byte_cap', src, line)
        check(b'\x00' not in raw, 'nul_byte', src, line)
        h.update(raw)
        try:
            text = raw.decode('ascii')
        except UnicodeDecodeError:
            raise TraceError('nonascii_input', src, line) from None
        s = text.strip()
        if not s or s.startswith('$'):
            continue
        if s.startswith('*'):
            check(pending is None, 'missing_continuation', src, line)
            name = s[1:].split('$', 1)[0].strip().upper()
            if name.startswith(('ELEMENT_', 'NODE', 'LOAD_THERMAL_VARIABLE_NODE')):
                check(name in ALLOWED, 'unsupported_required_keyword', src, line)
            if name.startswith('KEYWORD'):
                check(name == 'KEYWORD', 'unsupported_global_format', src, line)
            keyword = name if name in ALLOWED else None
            continue
        try:
            if keyword == 'ELEMENT_SHELL_THICKNESS' and phase != 'thermal':
                if pending is None:
                    v = fields(text, [8] * 10, range(10), 6)
                    check(v[0] > 0 and v[1] > 0 and all(n > 0 for n in v[2:6]), 'invalid_shell_id')
                    check(not any(v[6:]), 'higher_order_shell')
                    pending = (line, v)
                else:
                    fields(text, [16] * 5, (), 4)
                    origin, v = pending; pending = None
                    counts['shell'] += 1
                    yield 'shell', origin, v
            elif phase == 'select':
                continue
            elif keyword == 'NODE' and phase == 'join':
                nid = node_identifier(text)
                counts['node_rows'] += 1
                if nid in selected:
                    v = fields(text, [8, 16, 16, 16, 8, 8], [0], 4)
                    yield 'node', line, v
            elif keyword == 'ELEMENT_BEAM' and phase == 'join':
                v = fields(text, [8] * 10, range(10), 4)
                check(all(n > 0 for n in v[:4]), 'invalid_beam_id')
                counts['beam'] += 1
                yield 'beam', line, v
            elif keyword == 'ELEMENT_DISCRETE' and phase == 'join':
                v = fields(text, [8] * 5 + [16, 8, 16], [0, 1, 2, 3, 4, 6], 4)
                check(all(n > 0 for n in v[:3]) and v[3] >= 0, 'invalid_discrete_id')
                counts['discrete'] += 1
                yield 'discrete', line, v
            elif keyword == 'ELEMENT_SOLID' and phase == 'join':
                clean = text.split('$', 1)[0].rstrip()
                if pending is not None:
                    nodes = fields(text, [8] * 10, range(10), 4)
                    check(not any(nodes[8:]), 'unsupported_ten_node_solid')
                    origin, base = pending; pending = None
                    v = base + nodes[:8]
                else:
                    pieces = clean.split(',') if ',' in clean else clean.split()
                    used = len(pieces) if ',' in clean or all(INTEGER.fullmatch(p) for p in pieces) else (len(clean) + 7) // 8
                    if used == 2:
                        pending = (line, fields(text, [8] * 2, range(2), 2)); continue
                    check(used == 10, 'unsupported_solid_layout')
                    origin, v = line, fields(text, [8] * 10, range(10), 10)
                check(v[0] > 0 and v[1] > 0, 'invalid_solid_id')
                counts['solid'] += 1
                yield 'solid', origin, v
            elif keyword == 'LOAD_THERMAL_VARIABLE_NODE' and phase == 'thermal':
                v = fields(text, [10] * 4, [0, 3], 4)
                check(v[0] > 0, 'invalid_thermal_node')
                counts['thermal'] += 1
                yield 'thermal', line, v
        except TraceError as e:
            raise TraceError(e.code, src, line) from None


def physical_vertices(kind, v):
    end = 6 if kind == 'shell' else 4 if kind in ('beam', 'discrete') else 10
    return set(n for n in v[2:end] if n > 0)


def selected_vertices(iterator):
    nodes, shell_count = set(), 0
    for kind, _, v in iterator:
        if kind == 'shell' and v[1] == 179:
            nodes.update(physical_vertices(kind, v)); shell_count += 1
            check(len(nodes) <= NODE_CAP, 'selection_cap')
    check(shell_count > 0 and nodes, 'empty_pid179_selection')
    return nodes, shell_count


def ordering_trace(iterator, selected):
    runs, traces, previous, row = [], [], None, 0
    adjacent_equal = 0
    for kind, line, v in iterator:
        check(kind == 'thermal', 'unexpected_thermal_event')
        row += 1
        nid, ts, tb, lcid = v
        if previous is None or nid < previous:
            check(len(runs) < RUN_CAP, 'run_cap')
            runs.append({'run': len(runs) + 1, 'first_line': line, 'last_line': line,
                         'first_row': row, 'last_row': row, 'row_count': 0,
                         'first_nid': nid, 'last_nid': nid})
        if previous == nid:
            adjacent_equal += 1
        run = runs[-1]
        run.update(last_line=line, last_row=row, last_nid=nid)
        run['row_count'] += 1
        if nid in selected:
            check(len(traces) < ROW_CAP, 'selected_row_cap')
            traces.append({'src': 118, 'line': line, 'row': row, 'run': run['run'],
                           'nid': nid, 'ts': ts, 'tb': tb, 'lcid': lcid})
        previous = nid
    return {'assignment_rows': row, 'adjacent_equal_nid_pairs': adjacent_equal,
            'ordering_runs': runs, 'selected_rows': traces}


def assignment_summary(rows):
    values = [(r['ts'], r['tb'], r['lcid']) for r in rows]
    count, distinct = len(values), len(set(values))
    category = 'unassigned' if not count else 'single' if count == 1 else 'repeated_equal' if distinct == 1 else 'repeated_unequal'
    return {'rows': count, 'distinct_assignments': distinct,
            'rows_beyond_one': max(0, count - 1), 'equal_duplicate_rows': count - distinct,
            'adjacent_equal_assignments': sum(a == b for a, b in zip(values, values[1:])),
            'adjacent_unequal_assignments': sum(a != b for a, b in zip(values, values[1:])),
            'category': category}


def assemble(events):
    pid_nodes, shell_count = selected_vertices(events(121, 'select', None))
    chosen = pid_nodes | {842747, 842833}
    check(len(chosen) <= NODE_CAP, 'selection_cap')
    coordinates, incident = {}, defaultdict(Counter)
    for src in (119, 120, 121):
        for kind, line, v in events(src, 'join', chosen):
            if kind == 'node':
                check(v[0] not in coordinates, 'duplicate_selected_node', src, line)
                coordinates[v[0]] = {'src': src, 'line': line, 'xyz': list(v[1:4])}
            else:
                pid = v[1] + (1000 if src == 120 else 0)
                for nid in physical_vertices(kind, v) & chosen:
                    incident[nid][(pid, kind)] += 1
    trace = ordering_trace(events(118, 'thermal', chosen), chosen)
    rows_by_node = defaultdict(list)
    for row in trace['selected_rows']:
        rows_by_node[row['nid']].append(row)
    nodes, part_nodes = {}, defaultdict(set)
    for nid in sorted(chosen):
        incidence = defaultdict(dict)
        for (pid, kind), count in sorted(incident[nid].items()):
            incidence[pid][kind] = count; part_nodes[pid].add(nid)
        nodes[str(nid)] = {'nid': nid, 'pid179_vertex': nid in pid_nodes,
            'exception_target': nid in (842747, 842833),
            'coordinate': coordinates.get(nid),
            'incident_parts': [{'pid': pid, 'element_kind_counts': kinds} for pid, kinds in sorted(incidence.items())],
            'assignments': rows_by_node[nid], 'assignment_summary': assignment_summary(rows_by_node[nid])}
    per_part = []
    for pid, ids in sorted(part_nodes.items()):
        cats = Counter(nodes[str(n)]['assignment_summary']['category'] for n in ids)
        kind_counts = Counter()
        for n in ids:
            for (p, kind), count in incident[n].items():
                if p == pid:
                    kind_counts[kind] += count
        per_part.append({'pid': pid, 'selected_nodes': len(ids),
                         'assignment_categories': dict(sorted(cats.items())),
                         'node_element_incidence_kind_counts': dict(sorted(kind_counts.items()))})
    return {'selection': {'pid179_shells': shell_count, 'pid179_vertices': sorted(pid_nodes),
                          'selected_nodes': sorted(chosen)},
            'thermal': trace, 'nodes': nodes, 'per_incident_part': per_part,
            'unmatched': {'coordinates': sorted(chosen - coordinates.keys()),
                          'incidence': sorted(n for n in chosen if not incident[n]),
                          'thermal': sorted(n for n in chosen if not rows_by_node[n])},
            'assignment_categories': dict(sorted(Counter(n['assignment_summary']['category'] for n in nodes.values()).items()))}


def pinned_sources():
    result = {}
    for src, (name, size, sha, _, _) in PINS.items():
        path = SOURCE / name
        value = {'bytes': path.stat().st_size, 'sha256': digest(path)}
        check(value == {'bytes': size, 'sha256': sha}, 'source_pin', src)
        result[str(src)] = value
    return result


def historical_events(src, phase, selected):
    with gzip.open(SOURCE / PINS[src][0], 'rb') as f:
        yield from typed_stream(src, f, phase, selected)
    record = PROGRESS[-1]
    check(record['eof'] and record['bytes'] == PINS[src][3] and record['sha256'] == PINS[src][4], 'stream_pin', src)


def controls():
    names = []
    def ok(name, value):
        check(value, 'control_' + name); names.append(name)
    def reject(name, fn, code):
        try:
            fn()
        except TraceError as e:
            ok(name, e.code == code)
        else:
            raise TraceError('control_missing_rejection_' + name)
    def capped(name, value, fn):
        old = globals()[name]
        try:
            globals()[name] = value
            return fn()
        finally:
            globals()[name] = old
    def parse(text, phase='join', selected=None):
        return list(typed_stream(0, io.BytesIO(text.encode()), phase, selected or {1, 2, 3, 4}))
    ok('fixed_node', fields(f'{1:8d}{1.25:16.8f}{-2:16.8f}{0:16.8f}', [8,16,16,16,8,8], [0],4)[:4] == (1,'1.25','-2','0'))
    ok('comma_decimal', fields('1,2.500D+1,0,2', [10]*4,[0,3],4) == (1,'25','0',2))
    ok('space_free', fields('1 2.5 0 2', [10]*4,[0,3],4) == (1,'2.5','0',2))
    reject('nonfinite', lambda: scalar('NaN'), 'invalid_numeric_token')
    reject('missing_numeric', lambda: fields('1,,0,2',[10]*4,[0,3],4), 'missing_required_field')
    reject('oversize_line', lambda: parse('$' * (LINE_CAP+1)), 'line_cap')
    reject('oversize_stream', lambda: capped('BYTE_CAP',3,lambda: parse('$123\n')), 'byte_cap')
    reject('unsupported_keyword', lambda: parse('*ELEMENT_BEAM_ORIENTATION\n'), 'unsupported_required_keyword')
    reject('missing_thickness', lambda: parse('*ELEMENT_SHELL_THICKNESS\n1,179,1,2,3,4\n*END\n'), 'missing_continuation')
    shell = parse('*ELEMENT_SHELL_THICKNESS\n1,179,1,2,3,3\n1,1,1,1\n')
    ok('shell_pair_triangle', len(shell) == 1 and physical_vertices('shell', shell[0][2]) == {1,2,3})
    ok('beam_orientation', physical_vertices('beam',(1,1,1,2,999,0)) == {1,2})
    ok('grounded_discrete', physical_vertices('discrete',(1,1,1,0,999)) == {1})
    solid = parse('*ELEMENT_SOLID\n1,1\n1,2,3,4,1,2,3,4\n')
    ok('two_card_solid', physical_vertices('solid',solid[0][2]) == {1,2,3,4})
    sequence = [('thermal', n+10, (nid,'25','0',2)) for n,nid in enumerate((1,1,2,1,3,3,2))]
    out = ordering_trace(iter(sequence), {1,2})
    ok('nondecreasing_boundaries', [r['row_count'] for r in out['ordering_runs']] == [3,3,1] and out['adjacent_equal_nid_pairs'] == 2)
    ok('selected_row_locators', [(r['row'],r['line'],r['run']) for r in out['selected_rows']] == [(1,10,1),(2,11,1),(3,12,1),(4,13,2),(7,16,3)])
    reject('ordering_run_cap',lambda: capped('RUN_CAP',2,lambda: ordering_trace(iter(sequence),{1,2})), 'run_cap')
    reject('selected_row_cap',lambda: capped('ROW_CAP',2,lambda: ordering_trace(iter(sequence),{1,2})), 'selected_row_cap')
    ok('empty_ordering', ordering_trace(iter([]),set())['ordering_runs']==[])
    equal = assignment_summary([{'ts':'25','tb':'0','lcid':2}]*3)
    ok('equal_repeats', equal['category']=='repeated_equal' and equal['equal_duplicate_rows']==2)
    unequal = assignment_summary([{'ts':v,'tb':'0','lcid':2} for v in ('25','26','25')])
    ok('unequal_repeats', unequal['category']=='repeated_unequal' and unequal['distinct_assignments']==2 and unequal['adjacent_unequal_assignments']==2)
    fixtures = {
        121: '*NODE\n1,0,0,0\n2,1,0,0\n3,1,1,0\n4,0,1,0\n*ELEMENT_SHELL_THICKNESS\n1,179,1,2,3,4\n1,1,1,1\n*ELEMENT_BEAM\n2,9,1,2,842747\n*ELEMENT_DISCRETE\n3,8,2,0,842833\n',
        120: '*ELEMENT_SHELL_THICKNESS\n4,1,1,2,3,4\n1,1,1,1\n',
        119: '*NODE\n842747,2,0,0\n842833,3,0,0\n*ELEMENT_SOLID\n5,10,842747,842833,1,2,842747,842833,1,2\n',
        118: '*LOAD_THERMAL_VARIABLE_NODE\n1,25,0,2\n2,26,0,2\n2,26,0,2\n842747,300,0,2\n1,26,0,2\n842747,25,0,2\n'}
    def fixture_events(src, phase, selected):
        return typed_stream(src, io.BytesIO(fixtures[src].encode()), phase, selected)
    joined = assemble(fixture_events)
    ok('full_selection', joined['selection']['pid179_vertices']==[1,2,3,4] and len(joined['nodes'])==6)
    ok('full_part_offset', any(p['pid']==1001 for p in joined['nodes']['1']['incident_parts']))
    ok('full_orientation_excluded', joined['nodes']['842747']['incident_parts']==[{'pid':10,'element_kind_counts':{'solid':1}}])
    ok('full_grounded_incidence', any(p=={'pid':8,'element_kind_counts':{'discrete':1}} for p in joined['nodes']['2']['incident_parts']))
    ok('full_unassigned', joined['unmatched']['thermal']==[3,4,842833])
    ok('full_equal_unequal', joined['nodes']['1']['assignment_summary']['category']=='repeated_unequal' and joined['nodes']['2']['assignment_summary']['category']=='repeated_equal')
    reject('node_selection_cap',lambda: capped('NODE_CAP',3,lambda: assemble(fixture_events)), 'selection_cap')
    fixtures[119] += '*NODE\n1,0,0,0\n'
    reject('duplicate_selected_coordinate',lambda: assemble(fixture_events), 'duplicate_selected_node')
    PROGRESS.clear()
    return {'passed': len(names), 'groups': names}


# INDEPENDENT_CORE_END

INDEPENDENT_SHA = '25f62e23ab44efd260e1416e56bc3c6f4aa23f8a090d21af7ba6bcc4c23f5b77'
CORE_SHA = 'c5819e03ebd5eaab953e351e308d01dedb93dd661c3b1531a9152cba0f7ca228'
ROOT_SHA = '54f20f57b06948f95a1ad8d384fd5f8a1778c0a6c0d2d8966efa139addac13ae'
ROOT_CODE_SHA = 'dc88bbbecb668baebf54afae33af807fefeccef58d2399eb812e2697bd75f90c'
HELPER_SHA = 'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
SUPPLEMENT_SHA = '6d2a9d48a2e5ef3e6aba543ab41394bb1510293f2a68d5f3aeaa123e4b0c4e8d'


def load_independent():
    check(digest(BASE/'independent01.json')==INDEPENDENT_SHA, 'independent_pin')
    check(hashlib.sha256(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0]).hexdigest()==CORE_SHA, 'core_changed')
    return json.loads((BASE/'independent01.json').read_text())


def region_grouping(own):
    grouped = defaultdict(list)
    for key, node in own['nodes'].items():
        rows = node['assignments']
        if node['pid179_vertex'] and len({r['ts'] for r in rows}) > 1:
            group = (node['coordinate']['xyz'][2], tuple(r['ts'] for r in rows), tuple(r['run'] for r in rows))
            grouped[group].append(int(key))
    result = [{'z':z,'ts':list(ts),'runs':list(runs),'nodes':sorted(ids),'node_count':len(ids)}
              for (z,ts,runs),ids in sorted(grouped.items(),key=lambda kv:Decimal(kv[0][0]))]
    steps = [scalar(str(Decimal(b['z'])-Decimal(a['z']))) for a,b in zip(result,result[1:])]
    return {'groups':result,'adjacent_z_differences':steps,
            'all_repeated_region_single_part179': all(own['nodes'][str(n)]['incident_parts'][0]['pid']==179 and len(own['nodes'][str(n)]['incident_parts'])==1 for g in result for n in g['nodes'])}


class ThermalKeywordCounter:
    def __init__(self, fileobj):
        self.fileobj, self.counts = fileobj, Counter()
    def readline(self, size):
        line = self.fileobj.readline(size)
        if line.lstrip().startswith(b'*'):
            token = line.strip().split(b'$',1)[0].strip().upper()
            check(token in (b'*KEYWORD',b'*LOAD_THERMAL_VARIABLE_NODE',b'*END'), 'unsupported_thermal_block')
            self.counts[token.decode('ascii')] += 1
        return line


def supplement():
    """Post-schema source checks, not retroactive blind-checkpoint additions."""
    own = load_independent()['result']
    shells = [{'eid':v[0],'line':line} for kind,line,v in historical_events(121,'select',None) if kind=='shell' and v[1]==179]
    nodes, bases, curves = {}, Counter(), Counter()
    rows = 0
    with gzip.open(SOURCE/PINS[118][0],'rb') as f:
        wrapper = ThermalKeywordCounter(f)
        for kind,line,v in typed_stream(118,wrapper,'thermal',set()):
            nid,ts,tb,lcid = v; rows += 1
            bases[tb] += 1; curves[str(lcid)] += 1
            if nid in nodes:
                item=nodes[nid]; item[0]+=1; item[2]=item[2] or item[1]!=ts
            else:
                nodes[nid]=[1,ts,False]
    stream = PROGRESS[-1]
    check(stream['eof'] and stream['bytes']==PINS[118][3] and stream['sha256']==PINS[118][4], 'supplement_thermal_pin')
    multiplicity=Counter(v[0] for v in nodes.values())
    return {'post_schema':True,'region_shells':shells,
            'thermal':{'rows':rows,'unique_nodes':len(nodes),'nodes_repeated':sum(v[0]>1 for v in nodes.values()),
                       'nodes_unequal_TS':sum(v[2] for v in nodes.values()),
                       'multiplicity':{str(k):v for k,v in sorted(multiplicity.items())},
                       'bases':dict(bases),'curves':dict(curves),'keywords':dict(wrapper.counts)},
            'exploratory_region_grouping':region_grouping(own)}


class ExactComparison:
    def __init__(self):
        self.counts=Counter(); self.failures=[]; self.max_error=Decimal(0)
    def failure(self,path,code):
        self.failures.append({'path':path,'code':code})
    def same(self,got,want,path):
        if isinstance(got,bool) or isinstance(want,bool):
            self.counts['boolean']+=1
            if type(got) is not type(want) or got!=want:self.failure(path,'boolean')
        elif isinstance(got,int) and isinstance(want,int):
            self.counts['integer']+=1; self.max_error=max(self.max_error,abs(Decimal(got)-Decimal(want)))
            if got!=want:self.failure(path,'integer')
        elif isinstance(got,str) and isinstance(want,str) and NUMERIC.fullmatch(got) and NUMERIC.fullmatch(want):
            self.counts['exact_decimal']+=1; a,b=Decimal(got),Decimal(want)
            self.max_error=max(self.max_error,abs(a-b))
            if a!=b:self.failure(path,'decimal')
        elif isinstance(got,dict) and isinstance(want,dict):
            self.counts['dict']+=1
            if set(got)!=set(want):self.failure(path,'keys')
            for k in sorted(set(got)&set(want)):self.same(got[k],want[k],path+'.'+str(k))
        elif isinstance(got,list) and isinstance(want,list):
            self.counts['list']+=1
            if len(got)!=len(want):self.failure(path,'length')
            for i,(a,b) in enumerate(zip(got,want)):self.same(a,b,path+'.'+str(i))
        else:
            self.counts['other']+=1
            if type(got) is not type(want) or got!=want:self.failure(path,'value_or_type')


def compare():
    independent=load_independent(); own=independent['result']
    supfile=BASE/'independent-supplement01.json'
    check(digest(supfile)==SUPPLEMENT_SHA,'supplement_pin')
    supplemental=json.loads(supfile.read_text()); sup=supplemental['result']
    rootfile=BASE/'run01.json'; rootcode=BASE/'trace_assignments.py'
    check(digest(rootfile)==ROOT_SHA,'root_output_pin')
    check(digest(rootcode)==ROOT_CODE_SHA,'root_code_pin')
    check(digest(BASE.parent/'model-member-map'/'map_members.py')==HELPER_SHA,'root_helper_pin')
    rootdoc=json.loads(rootfile.read_text()); root=rootdoc['result']; c=ExactComparison()
    c.same(independent['receipt']['status'],'PASS','independent_status')
    c.same(supplemental['receipt']['status'],'PASS','supplement_status')
    c.same(rootdoc['status'],'PASS','root_status')
    c.same(rootdoc['protocol_sha256'],PROTOCOL_SHA,'root_protocol')
    c.same(rootdoc['code_sha256'],ROOT_CODE_SHA,'root_code')
    c.same(rootdoc['helper_sha256'],HELPER_SHA,'root_helper')
    c.same(root['region_pid'],179,'region_pid')
    c.same(root['region_nodes'],own['selection']['pid179_vertices'],'selected_region_ids')
    c.same(root['region_shells'],sup['region_shells'],'selected_shell_locators')
    c.same(len(root['region_shells']),own['selection']['pid179_shells'],'selected_shell_count')
    expected_nodes=[]
    grouped=Counter()
    for nid in own['selection']['selected_nodes']:
        n=own['nodes'][str(nid)]; coord=n['coordinate']; rows=n['assignments']
        incidence=[{'pid':p['pid'],'kind':kind,'elements':count} for p in n['incident_parts'] for kind,count in sorted(p['element_kind_counts'].items())]
        unequal=len({r['ts'] for r in rows})>1
        expected_nodes.append({'nid':nid,'region179':n['pid179_vertex'],
            'coordinates':None if coord is None else {'source':PINS[coord['src']][0],'line':coord['line'],'xyz':coord['xyz']},
            'assignments':[{'nid':r['nid'],'line':r['line'],'row':r['row'],'run':r['run'],'TS':r['ts'],'TB':r['tb'],'LCID':r['lcid']} for r in rows],
            'incidence':incidence,'unequal_TS':unequal})
        grouped[('region179' if n['pid179_vertex'] else 'exception',len(rows),unequal,len(n['incident_parts']))]+=1
    c.same(root['nodes'],expected_nodes,'selected_nodes')
    expected_groups=[{'selection':s,'assignment_count':a,'unequal_TS':u,'part_count':p,'nodes':n} for (s,a,u,p),n in sorted(grouped.items())]
    c.same(root['groups'],expected_groups,'groups')
    expected_thermal={**sup['thermal'],'ordering_runs':[{'run':r['run'],'first_line':r['first_line'],'last_line':r['last_line'],'first_nid':r['first_nid'],'last_nid':r['last_nid'],'rows':r['row_count']} for r in own['thermal']['ordering_runs']]}
    c.same(root['thermal'],expected_thermal,'thermal')
    c.same(root['thermal']['rows'],own['thermal']['assignment_rows'],'original_full_row_count')
    counts={PINS[r['src']][0]+':'+k:v for r in independent['receipt']['streams'] if r['phase']=='join' for k,v in r['typed_records'].items() if k in ('shell','beam','discrete','solid')}
    c.same(root['mesh_counts'],counts,'mesh_counts')
    actual_passes=[]
    for item in root['source_receipts']:
        c.same(len(item['sources']),1,'single_source_pass')
        for name,record in item['sources'].items():
            ids=[k for k,v in PINS.items() if v[0]==name]
            check(len(ids)==1,'unknown_receipt_source'); src=ids[0]
            phase='select' if item['pass']=='select_region' else 'thermal' if item['pass']=='thermal_order' else 'join'
            actual_passes.append((src,phase))
            ownstream=[r for r in independent['receipt']['streams'] if r['src']==src and r['phase']==phase]
            check(len(ownstream)==1,'ambiguous_receipt_stream')
            pin=PINS[src]
            expected={'compressed_bytes':pin[1],'compressed_sha256':pin[2],'uncompressed_bytes':pin[3],'uncompressed_sha256':pin[4],'eof':True,'pin_after':True,'lines':ownstream[0]['lines']}
            c.same(record,expected,'stream.'+str(src)+'.'+phase)
    c.same(sorted(actual_passes),sorted((r['src'],r['phase']) for r in independent['receipt']['streams']),'source_pass_coverage')
    for doc,label in ((independent,'independent'),(supplemental,'supplement')):
        c.same(doc['receipt']['sources_before'],doc['receipt']['sources_after'],label+'.stable_sources')
        c.same(doc['receipt']['sources_after'],pinned_sources(),label+'.current_source_pins')
    grouping=region_grouping(own)
    c.same(sup['exploratory_region_grouping'],grouping,'grouping_repeat')
    expected_table=[('-67.2846','50.57','46.97',177,178),('-63.3984','51.94','36.82',178,342),('-59.5122','36.96','25',342,343),('-55.626','25','46.69',343,507),('-51.7398','46.86','97.37',507,508),('-47.8536','97.67','62.24',508,672),('-43.9674','62.56','25',672,673)]
    c.same([{k:v for k,v in g.items() if k!='nodes'} for g in grouping['groups']],
           [{'z':z,'ts':[a,b],'runs':[r,s],'node_count':9} for z,a,b,r,s in expected_table],'displayed_group_table')
    c.same(grouping['adjacent_z_differences'],['3.8862']*6,'displayed_spacing')
    c.same(grouping['all_repeated_region_single_part179'],True,'displayed_single_part')
    example=own['nodes']['921518']
    c.same([(r['line'],r['ts'],r['tb'],r['lcid']) for r in example['assignments']],[(512465,'50.57','0',2),(512527,'46.97','0',2)],'example_rows')
    c.same(example['coordinate']['line'],925814,'example_coordinate_line')
    c.same(example['incident_parts'],[{'pid':179,'element_kind_counts':{'shell':4}}],'example_incidence')
    check(digest(rootfile)==ROOT_SHA and digest(rootcode)==ROOT_CODE_SHA and digest(supfile)==SUPPLEMENT_SHA and digest(BASE/'independent01.json')==INDEPENDENT_SHA,'changed_derivative_after')
    return {'status':'PASS' if not c.failures else 'FAIL','comparison_counts':dict(c.counts),
            'maximum_absolute_numeric_error':str(c.max_error),'exact_decimal_comparison':True,'failures':c.failures,
            'coverage':{'selected_nodes':len(expected_nodes),'selected_thermal_rows':len(own['thermal']['selected_rows']),
                        'ordering_runs':len(own['thermal']['ordering_runs']),'region_shell_locators':len(sup['region_shells']),
                        'coordinate_components':3*len(expected_nodes),'node_part_kind_incidence_rows':sum(len(n['incidence']) for n in expected_nodes),
                        'global_thermal_rows':sup['thermal']['rows'],'displayed_groups':len(grouping['groups'])},
            'pins':{'independent':INDEPENDENT_SHA,'supplement':digest(supfile),'root_result':ROOT_SHA,'root_code':ROOT_CODE_SHA,'root_helper':HELPER_SHA,
                    'report':digest(BASE/'report.md')},
            'exploratory_region_grouping':grouping,
            'not_replicated':['Root wall time, memory and eight producer controls are recorded execution claims, not independently repeated here.',
                              'This consumer uses frozen independent/supplemental source reconstructions; it does not rerun the complete source trace.',
                              'No historical solver duplicate rule, thermal transfer routine, effective temperature or physical cause is identified.']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--controls-only', action='store_true')
    p.add_argument('--supplement', action='store_true')
    p.add_argument('--compare', action='store_true')
    p.add_argument('--output', default='independent01.json')
    a = p.parse_args()
    check(bool(re.fullmatch(r'independent(?:[0-9]{2}|-(?:failed|controls|supplement|comparison)[0-9]{2})\.json', a.output)), 'output_name')
    check(sum((a.controls_only,a.supplement,a.compare))<=1,'exclusive_mode')
    out = BASE / a.output
    check(not out.exists(), 'output_exists')
    begin = time.monotonic()
    receipt = {'command': sys.argv, 'python': sys.version.split()[0], 'code_sha256': digest(__file__),
               'core_sha256': hashlib.sha256(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0]).hexdigest()}
    try:
        receipt['controls'] = controls()
        if not a.controls_only:
            check(digest(BASE/'PROTOCOL.md') == PROTOCOL_SHA, 'protocol_pin')
            check(digest(DEPENDENCY) == DEPENDENCY_SHA, 'transform_dependency_pin')
            receipt.update(protocol_sha256=PROTOCOL_SHA, transform_dependency_sha256=DEPENDENCY_SHA)
            receipt['sources_before'] = pinned_sources()
            result = compare() if a.compare else supplement() if a.supplement else assemble(historical_events)
            receipt['sources_after'] = pinned_sources()
            check(receipt['sources_before']==receipt['sources_after'], 'changed_sources')
            check(digest(DEPENDENCY)==DEPENDENCY_SHA and digest(BASE/'PROTOCOL.md')==PROTOCOL_SHA, 'changed_dependency')
        else:
            result = None
        receipt.update(status=result['status'] if a.compare else 'PASS', seconds=round(time.monotonic()-begin,6), peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, streams=PROGRESS)
        check(receipt['peak_rss_bytes'] <= MEM_CAP, 'memory_cap')
        payload = {'receipt':receipt, 'result':result}
    except (TraceError, OSError, UnicodeError, ValueError, MemoryError) as e:
        error = {'code':e.code,'src':e.src,'line':e.line} if isinstance(e,TraceError) else {'code':'runtime_'+type(e).__name__,'src':PROGRESS[-1]['src'] if PROGRESS else 0,'line':PROGRESS[-1]['lines'] if PROGRESS else 0}
        receipt.update(status='FAIL', error=error, seconds=round(time.monotonic()-begin,6), peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, streams=PROGRESS)
        if not a.controls_only:
            try:
                receipt['sources_after_failure'] = pinned_sources()
            except (TraceError, OSError) as pin_error:
                receipt['sources_after_failure_error'] = pin_error.code if isinstance(pin_error,TraceError) else 'runtime_'+type(pin_error).__name__
            if re.fullmatch(r'independent[0-9]{2}\.json', out.name):
                out = BASE / out.name.replace('independent','independent-failed',1)
        payload = {'receipt':receipt, 'result':None}
    with out.open('x') as f:
        json.dump(payload,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'status':receipt['status'], 'output':out.name, 'sha256':digest(out), 'controls':receipt.get('controls'), 'error':receipt.get('error'), 'seconds':receipt['seconds']}))
    return 0 if receipt['status']=='PASS' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except TraceError as e:
        print(json.dumps({'status':'FAIL','code':e.code,'src':e.src,'line':e.line})); raise SystemExit(1)
    except (OSError, UnicodeError, ValueError, MemoryError) as e:
        print(json.dumps({'status':'FAIL','code':'runtime_'+type(e).__name__})); raise SystemExit(1)
