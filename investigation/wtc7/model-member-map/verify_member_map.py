#!/usr/bin/env python3
"""Independent, bounded, numeric-only released-deck verification.

No solver or embedded pathname is executed.  The independently written core
precedes the schema adapter marker; its hash is frozen before producer reads.
"""
from __future__ import annotations

import argparse
from array import array
from collections import Counter, defaultdict
import gc
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import resource
import sys
import time

import numpy as np

CAP = 512 * 1024 * 1024
LINE_CAP = 65536
TOL = 1e-8
RUN_PROGRESS = []
PROTOCOL_SHA = 'd2c2b77d9801236c0a7d940349412a3b3cc50cc977997b67114ac2aff9afac7c'
SOURCE_DIR = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
# Only these six preservation paths can be opened; source text never selects one.
PINS = {
    116: ('Damage_Global_ANSYS_CaseB_4.0hr.k.gz', 5331, '982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da', 17314, '876066eb62e4c849c6bb9fb1598cc0be8b700843483a6ddd3cf6aa9847ad2455'),
    117: ('G6A_CaseA_El_Delete_List.k.gz', 103872, 'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273', 325983, 'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25'),
    118: ('WTC7_CaseB_400pm.int.gz', 2702040, '51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447', 34808082, 'fa721837357cf7b7fd43e49d2a9d171973663e12399c503163ef56c3464b060d'),
    119: ('discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7', 508372, '8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
    120: ('elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59', 232959541, '7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
    121: ('wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d', 333947423, '8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}
NAME_IDS = {p[0][:-3]: k for k, p in PINS.items()}
NUM = re.compile(r'^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[EeDd][+-]?[0-9]+)?$')
INTEGER = re.compile(r'^[+-]?[0-9]+$')
KNOWN = {
    'NODE', 'ELEMENT_SHELL_THICKNESS', 'ELEMENT_BEAM', 'ELEMENT_DISCRETE',
    'ELEMENT_SOLID', 'PART', 'LOAD_THERMAL_VARIABLE_NODE', 'INCLUDE',
    'INCLUDE_TRANSFORM', 'SET_SHELL_LIST', 'SET_BEAM', 'SET_BEAM_LIST',
    'SET_PART_LIST', 'DATABASE_CROSS_SECTION_PLANE_ID', 'CONTROL_TERMINATION',
    'DEFINE_CURVE', 'DELETE_SHELL_SET', 'DELETE_BEAM_SET',
    'MAT_PIECEWISE_LINEAR_PLASTICITY', 'MAT_PLASTICITY_COMPRESSION_TENSION',
    'MAT_RIGID', 'MAT_ELASTIC', 'MAT_ELASTIC_VISCOPLASTIC_THERMAL',
    'MAT_SPRING_NONLINEAR_ELASTIC', 'SECTION_BEAM', 'SECTION_SHELL',
    'SECTION_SOLID', 'SECTION_DISCRETE', 'HOURGLASS',
}


class CheckError(Exception):
    def __init__(self, code, src=0, line=0):
        self.code, self.src, self.line = code, int(src), int(line)
        super().__init__(code)


def require(ok, code, src=0, line=0):
    if not ok:
        raise CheckError(code, src, line)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def check_pins():
    out = {}
    for src, (name, size, digest, _, _) in PINS.items():
        p = SOURCE_DIR / name
        got = sha(p)
        require(p.stat().st_size == size and got == digest, 'compressed_pin', src)
        out[str(src)] = {'bytes': size, 'sha256': got}
    return out


def number(token, integer=False):
    token = token.strip()
    if not token:
        return 0 if integer else 0.0
    require(bool((INTEGER if integer else NUM).fullmatch(token)), 'nonnumeric_field')
    v = int(token) if integer else float(token.replace('D', 'E').replace('d', 'e'))
    require(integer or math.isfinite(v), 'nonfinite_field')
    return v


def card(line, widths, integer_positions=(), required=0, preserve_blanks=False):
    """Fixed card, comma-delimited card, or unambiguously spaced free card.

    Blanks are defaults only in declared numeric fields, never arbitrary text.
    A free-format row cannot silently overflow the specified card.
    """
    line = line.split('$', 1)[0].rstrip('\r\n')
    if ',' in line:
        fields = line.split(',')
        require(len(fields) <= len(widths), 'extra_numeric_fields')
    else:
        require(not line[sum(widths):].strip(), 'fixed_card_overflow')
        starts = [0]
        for width in widths:
            starts.append(starts[-1] + width)
        fixed = [line[starts[i]:starts[i + 1]] for i in range(len(widths))]
        valid_fixed = all(not x.strip() or (INTEGER if i in integer_positions else NUM).fullmatch(x.strip()) for i, x in enumerate(fixed))
        if valid_fixed:
            fields = fixed
        else:
            spaced = line.split()
            require(all(NUM.fullmatch(x) for x in spaced) and required <= len(spaced) <= len(widths), 'nonnumeric_field')
            fields = spaced
    require(len(fields) >= required and all(x.strip() for x in fields[:required]), 'missing_required_field')
    fields += [''] * (len(widths) - len(fields))
    ints = set(integer_positions)
    return tuple(None if preserve_blanks and not x.strip() else number(x, i in ints) for i, x in enumerate(fields))


def card_used_fields(line, width=8):
    """Discriminate documented old/new SOLID layouts without guessing."""
    s = line.split('$', 1)[0].rstrip()
    if ',' in s:
        return len(s.split(','))
    t = s.split()
    if all(INTEGER.fullmatch(x) for x in t) and len(t) > 1:
        return len(t)
    return (len(s) + width - 1) // width


class Deck:
    """Typed stream parser.  Numeric events contain no headings/comments."""
    def __init__(self, src, binary):
        self.src, self.binary = src, binary
        self.stats = {'bytes': 0, 'lines': 0, 'eof': False, 'keywords': {}, 'data_lines': {}}
        if src in PINS:
            RUN_PROGRESS.append({'src': src, 'stream': self.stats})

    def events(self):
        keyword = None
        keyword_line = 0
        index = 0
        pending = None
        heading_column = None
        digest = hashlib.sha256()
        counts, data = Counter(), Counter()
        while True:
            raw = self.binary.readline(LINE_CAP + 1)
            if not raw:
                require(pending is None, 'missing_element_continuation', self.src, self.stats['lines'])
                self.stats.update(eof=True, sha256=digest.hexdigest(), keywords=dict(counts), data_lines=dict(data))
                return
            self.stats['lines'] += 1
            n = self.stats['lines']
            self.stats['bytes'] += len(raw)
            require(len(raw) <= LINE_CAP, 'line_cap', self.src, n)
            require(self.stats['bytes'] <= CAP, 'uncompressed_cap', self.src, n)
            require(b'\x00' not in raw, 'nul_byte', self.src, n)
            digest.update(raw)
            try:
                line = raw.decode('ascii')
            except UnicodeDecodeError:
                raise CheckError('nonascii_data', self.src, n) from None
            s = line.strip()
            meaningful_blank = (keyword == 'PART' and index == 0) or (keyword == 'DATABASE_CROSS_SECTION_PLANE_ID' and index == 2)
            if (not s and not meaningful_blank) or s.startswith('$'):
                continue
            if s.startswith('*'):
                require(pending is None, 'missing_element_continuation', self.src, n)
                name = s[1:].split('$', 1)[0].strip().upper()
                # Unknown text is not retained.  Known keyword variants are not flattened.
                keyword = name if name in KNOWN else None
                if name.startswith(('ELEMENT_SHELL_THICKNESS_', 'ELEMENT_BEAM_', 'ELEMENT_SOLID_', 'PART_')):
                    raise CheckError('unsupported_card_variant', self.src, n)
                if name.startswith(('MAT_', 'SECTION_', 'ELEMENT_', 'INCLUDE', 'SET_PART')) and name not in KNOWN:
                    raise CheckError('unsupported_typed_keyword', self.src, n)
                if name.startswith('KEYWORD') and name != 'KEYWORD':
                    raise CheckError('unsupported_global_format', self.src, n)
                keyword_line, index, heading_column = n, 0, None
                if keyword:
                    counts[keyword] += 1
                continue
            if keyword is None:
                continue
            data[keyword] += 1
            i, index = index, index + 1
            try:
                if keyword == 'NODE':
                    v = card(line, [8, 16, 16, 16, 8, 8], [0], 4)
                    yield 'node', n, v
                elif keyword == 'ELEMENT_SHELL_THICKNESS':
                    if pending is None:
                        v = card(line, [8] * 10, range(10), 6)
                        require(not any(v[6:]), 'higher_order_shell_unsupported')
                        pending = (n, v)
                    else:
                        thick = card(line, [16] * 5, (), 4)
                        yield 'shell', pending[0], (pending[1], thick)
                        pending = None
                elif keyword == 'ELEMENT_BEAM':
                    yield 'beam', n, card(line, [8] * 10, range(10), 4)
                elif keyword == 'ELEMENT_DISCRETE':
                    yield 'discrete', n, card(line, [8] * 5 + [16, 8, 16], [0, 1, 2, 3, 4, 6], 4)
                elif keyword == 'ELEMENT_SOLID':
                    if pending is not None:
                        nodes = card(line, [8] * 10, range(10), 4)
                        require(not any(nodes[8:]), 'ten_node_solid_unsupported')
                        yield 'solid', pending[0], pending[1] + nodes[:8]
                        pending = None
                    else:
                        used = card_used_fields(line)
                        if used == 2:
                            pending = (n, card(line, [8, 8], [0, 1], 2))
                        elif used == 10:
                            yield 'solid', n, card(line, [8] * 10, range(10), 10)
                        else:
                            raise CheckError('ambiguous_solid_card')
                elif keyword == 'PART':
                    if i == 0:
                        continue
                    require(i == 1, 'extra_part_card')
                    yield 'part', n, card(line, [10] * 8, range(8), 3)
                elif keyword.startswith('MAT_') or keyword.startswith('SECTION_') or keyword == 'HOURGLASS':
                    if i == 0:
                        # Only the identifier field is used; all other material data are out of scope.
                        first = line.split(',')[0] if ',' in line else line[:10]
                        yield 'definition', n, (keyword, number(first, True))
                elif keyword in ('SET_SHELL_LIST', 'SET_BEAM', 'SET_BEAM_LIST', 'SET_PART_LIST'):
                    if i == 0:
                        v = card(line, [10] * 8, [0], 1)
                        sid = v[0]
                        yield 'set_header', n, (keyword, sid)
                    else:
                        yield 'set_ids', n, (keyword, sid, card(line, [10] * 8, range(8), 1))
                elif keyword == 'LOAD_THERMAL_VARIABLE_NODE':
                    # v971 order is NID, TS (scale), TB (base), LCID, not NID/LCID/TB/TS.
                    yield 'thermal', n, card(line, [10] * 4, [0, 3], 4)
                elif keyword in ('INCLUDE', 'INCLUDE_TRANSFORM'):
                    if i == 0:
                        require(s in NAME_IDS, 'unallowlisted_include')
                        yield 'include', n, (keyword, NAME_IDS[s])
                    else:
                        require(keyword == 'INCLUDE_TRANSFORM' and i <= 4, 'extra_include_card')
                        widths = [10] * (7 if i == 1 else 1 if i in (2, 4) else 5)
                        # FCTTEM is an edition-dependent character convention, not
                        # an integer ID or an arbitrary temperature multiplier.
                        # Preserve the known numeric row without integer coercion.
                        ints = range(len(widths)) if i != 3 else []
                        yield 'transform', n, (i, card(line, widths, ints, 1))
                elif keyword == 'DATABASE_CROSS_SECTION_PLANE_ID':
                    if i == 0:
                        first, heading = line.split(',', 1) if ',' in line else (line[:10], line[10:])
                        csid = number(first, True)
                        heading = heading.strip()
                        m = re.fullmatch(r'(?i)col(?:umn)?[ _-]*([0-9]+)', heading)
                        heading_column = int(m.group(1)) if m else None
                        yield 'plane_id', n, (csid, heading_column, hashlib.sha256(heading.encode('ascii')).hexdigest())
                    elif i in (1, 2):
                        ints = [0] if i == 1 else [5, 6]
                        values = card(line, [10] * 8, ints, 0, True)
                        require(i == 1 or values[7] is None, 'nonblank_unused_plane_field')
                        yield 'plane_card', n, (i, values)
                    else:
                        raise CheckError('extra_plane_card')
                elif keyword == 'CONTROL_TERMINATION' and i == 0:
                    yield 'termination', n, card(line, [10] * 8, (), 1)
                elif keyword in ('DELETE_SHELL_SET', 'DELETE_BEAM_SET'):
                    yield 'active_delete', n, (keyword, card(line, [10] * 8, (), 1))
            except CheckError as e:
                raise CheckError(e.code, self.src, n) from None


def read_deck(src):
    return gzip.open(SOURCE_DIR / PINS[src][0], 'rb')


def audit_stream(src, stats):
    require(stats['eof'], 'no_eof', src)
    require(stats['bytes'] == PINS[src][3], 'uncompressed_size', src)
    require(stats['sha256'] == PINS[src][4], 'uncompressed_hash', src)


class NodeTable:
    def __init__(self, ids, xyz):
        ni = np.frombuffer(ids, dtype=np.int64)
        co = np.frombuffer(xyz, dtype=np.float64).reshape(-1, 3)
        order = np.argsort(ni)
        self.ids, self.xyz = ni[order], co[order]
        require(np.all(self.ids > 0), 'nonpositive_node_id')
        require(not np.any(self.ids[1:] == self.ids[:-1]), 'duplicate_node_id')

    def lookup(self, ids):
        ids = np.asarray(ids, dtype=np.int64)
        ix = np.searchsorted(self.ids, ids)
        clipped = np.minimum(ix, len(self.ids) - 1)
        ok = (ix < len(self.ids)) & (self.ids[clipped] == ids)
        return ix, ok


def bounds(xyz):
    return None if not len(xyz) else [xyz.min(axis=0).tolist(), xyz.max(axis=0).tolist()]


def temperature_summary(values):
    values = np.asarray(values, dtype=np.float64)
    return {
        'count': int(values.size),
        'min': float(values.min()) if values.size else None,
        'max': float(values.max()) if values.size else None,
        'le_25_01': int(np.sum(values <= 25.01)),
        'gt_25_01': int(np.sum(values > 25.01)),
        'gt_100': int(np.sum(values > 100)),
        'gt_200': int(np.sum(values > 200)),
        'gt_300': int(np.sum(values > 300)),
    }


def deduplicate_assignments(ids, ts, tb, lc):
    """Retain per-node supplied-TS ranges; never select a historical scalar.

    Different same-node TB/LCID values cannot be represented by this bounded
    scalar-coefficient join and are separately rejected.  TS ranges are input
    ambiguity bounds, not confidence intervals or solver-behavior claims.
    """
    order = np.argsort(ids, kind='stable')
    si, ss, sb, sl = ids[order], ts[order], tb[order], lc[order]
    same = si[1:] == si[:-1]
    conflict = same & ((ss[1:] != ss[:-1]) | (sb[1:] != sb[:-1]) | (sl[1:] != sl[:-1]))
    starts = np.r_[True, ~same]
    start_ix = np.nonzero(starts)[0]
    group_sizes = np.diff(np.r_[start_ix, len(si)])
    low = np.minimum.reduceat(ss, start_ix)
    high = np.maximum.reduceat(ss, start_ix)
    ambiguous = low != high
    incompatible = ((np.minimum.reduceat(sb, start_ix) != np.maximum.reduceat(sb, start_ix)) |
                    (np.minimum.reduceat(sl, start_ix) != np.maximum.reduceat(sl, start_ix)))
    diagnostic = {'row_count': len(ids), 'unique_node_count': int(np.sum(starts)),
                  'repeated_rows': int(np.sum(same)), 'repeated_node_groups': int(np.sum(group_sizes > 1)),
                  'max_rows_per_node': int(group_sizes.max()) if len(group_sizes) else 0,
                  'conflicting_adjacent_assignments': int(np.sum(conflict)),
                  'ambiguous_ts_node_groups': int(np.sum(ambiguous)),
                  'rows_at_ambiguous_ts_nodes': int(np.sum(group_sizes[ambiguous])),
                  'incompatible_base_or_curve_groups': int(np.sum(incompatible)),
                  'row_temperature': temperature_summary(ts)}
    widest = np.lexsort((si[starts], -(high - low)))[:10]
    diagnostic['largest_ts_ranges'] = [{'node_id': int(si[start_ix[j]]), 'min': float(low[j]),
                                       'max': float(high[j]), 'span': float(high[j] - low[j]),
                                       'rows': int(group_sizes[j])}
                                      for j in widest if ambiguous[j]]
    require(not np.any(incompatible), 'conflicting_base_or_curve_assignments')
    return si[starts], low, high, sb[starts], sl[starts], diagnostic


def coefficient_envelope(low, high):
    low, high = np.asarray(low), np.asarray(high)
    require(low.shape == high.shape and bool(np.all(low <= high)), 'bad_coefficient_bounds')
    return {'node_count': len(low), 'unambiguous_count': int(np.sum(low == high)),
            'ambiguous_count': int(np.sum(low != high)),
            'min_supplied_ts': float(low.min()) if len(low) else None,
            'max_supplied_ts': float(high.max()) if len(high) else None,
            'definite_le_25_01': int(np.sum(high <= 25.01)),
            'possible_le_25_01': int(np.sum(low <= 25.01)),
            'thresholds': {str(q): {'definite_gt': int(np.sum(low > q)),
                                   'possible_gt': int(np.sum(high > q))}
                           for q in (25.01, 100, 200, 300)}}


def physical_nodes(kind, v):
    if kind == 'shell':
        return tuple(dict.fromkeys(x for x in v[2:6] if x > 0))
    if kind in ('beam', 'discrete'):
        return tuple(dict.fromkeys(x for x in v[2:4] if x > 0))
    if kind == 'solid':
        return tuple(dict.fromkeys(x for x in v[2:10] if x > 0))
    raise CheckError('unknown_element_kind')


def offset_part(src, v):
    offset = 1000 if src == 120 else 0
    return [x + offset if x != 0 else 0 for x in v[:3]]


def model_join():
    """Two bounded streaming passes; unique incidence is encoded in uint64."""
    node_ids, coordinates = array('q'), array('d')
    t_ids, t_ts, t_tb, t_lcid = array('q'), array('d'), array('d'), array('q')
    sets, set_lines = defaultdict(list), {}
    parts, definitions, source_counts = {}, {}, {}
    includes, transforms, planes, termination, active_delete = [], [], [], [], []
    for src in PINS:
        with read_deck(src) as f:
            d = Deck(src, f)
            for kind, line, v in d.events():
                if kind == 'node':
                    node_ids.append(v[0]); coordinates.extend(v[1:4])
                elif kind == 'thermal':
                    t_ids.append(v[0]); t_ts.append(v[1]); t_tb.append(v[2]); t_lcid.append(v[3])
                elif kind == 'part':
                    pid, sec, mat = offset_part(src, v)
                    require(pid not in parts, 'duplicate_effective_part', src, line)
                    parts[pid] = {'src': src, 'line': line, 'original': list(v[:3]), 'effective': [pid, sec, mat]}
                elif kind == 'definition':
                    kw, ident = v
                    off = 1000 if src == 120 else 0
                    require((kw, ident + off) not in definitions, 'duplicate_definition', src, line)
                    definitions[(kw, ident + off)] = [src, line, ident]
                elif kind == 'set_header':
                    key = (src, v[0], v[1])
                    require(key not in set_lines, 'duplicate_set_header', src, line)
                    set_lines[key] = line
                elif kind == 'set_ids':
                    key = (src, v[0], v[1])
                    require(key in set_lines, 'set_without_header', src, line)
                    sets[key].extend(x for x in v[2] if x != 0)
                elif kind == 'include':
                    includes.append([src, line, *v])
                elif kind == 'transform':
                    transforms.append([src, line, v[0], list(v[1])])
                elif kind == 'plane_id':
                    planes.append({'src': src, 'line': line, 'csid': v[0], 'column_label': v[1], 'heading_sha256': v[2], 'cards': []})
                elif kind == 'plane_card':
                    require(planes and planes[-1]['src'] == src, 'plane_without_id', src, line)
                    planes[-1]['cards'].append(list(v[1]))
                elif kind == 'termination':
                    termination.append([src, line, v[0]])
                elif kind == 'active_delete':
                    active_delete.append([src, line, v[0], list(v[1])])
            audit_stream(src, d.stats)
            source_counts[src] = d.stats
    # Observed transform must match the independently documented interpretation.
    require([x[3] for x in transforms] == [[0, 0, 1000, 1000, 0, 0, 0], [1000], [1., 1., 1., 1, 0.], [0]], 'unexpected_transform')
    require(sorted(x[3] for x in includes) == [118, 119, 120], 'active_include_set')
    require(not active_delete, 'unexpected_active_damage')
    mat_defs, sec_defs = defaultdict(list), defaultdict(list)
    for kw, ident in definitions:
        if kw.startswith('MAT_'):
            mat_defs[ident].append(kw)
        elif kw.startswith('SECTION_'):
            sec_defs[ident].append(kw)
    for part in parts.values():
        _, sec, mat = part['effective']
        # Geometry and numeric MID references remain testable without a supplied
        # constitutive definition.  Missing/ambiguous definitions are retained,
        # not invented and not mislabeled as complete material reconstruction.
        for name, matches in [('material', mat_defs[mat]), ('section', sec_defs[sec])]:
            part[name + '_definition_status'] = 'resolved' if len(matches) == 1 else 'missing' if not matches else 'ambiguous'
            part[name + '_definition_keywords'] = sorted(matches)
    for key, val in sets.items():
        require(len(val) == len(set(val)), 'duplicate_set_member', key[0], set_lines[key])
    nodes = NodeTable(node_ids, coordinates)
    del node_ids, coordinates
    gc.collect()
    tids = np.frombuffer(t_ids, dtype=np.int64)
    ts = np.frombuffer(t_ts, dtype=np.float64)
    tb = np.frombuffer(t_tb, dtype=np.float64)
    lc = np.frombuffer(t_lcid, dtype=np.int64)
    tids, ts_low, ts_high, tb, lc, thermal_duplicates = deduplicate_assignments(tids, ts, tb, lc)
    del ts
    del t_ids, t_ts, t_tb, t_lcid
    thermal_ix, tok = nodes.lookup(tids)
    assignment_at_node = np.full(len(nodes.ids), -1, dtype=np.int32)
    assignment_at_node[thermal_ix[tok]] = np.nonzero(tok)[0]
    pid_order = sorted(parts)
    pid_index = {p: i for i, p in enumerate(pid_order)}
    shell2 = set(sets[(116, 'SET_SHELL_LIST', 2)])
    beam_keys = [k for k in sets if k[0] == 116 and k[1] in ('SET_BEAM', 'SET_BEAM_LIST') and k[2] == 2]
    require(len(beam_keys) == 1, 'beam_set2_resolution')
    beam2 = set(sets[beam_keys[0]])
    shell1 = set(sets[(117, 'SET_SHELL_LIST', 1)])
    ids_by_kind = defaultdict(lambda: array('q'))
    source_mesh = defaultdict(Counter)
    part_mesh_counts = defaultdict(Counter)
    pair_chunks, chunk_nodes, chunk_parts = [], [], []
    targets, set1_members = {}, {}
    missing_node_links = Counter()
    orientation_missing = 0
    source_missing_parts = Counter()

    def flush():
        if not chunk_nodes:
            return
        idx, found = nodes.lookup(chunk_nodes)
        require(bool(np.all(found)), 'unexpected_mesh_missing_node')
        p = np.asarray(chunk_parts, dtype=np.uint64)
        encoded = p * np.uint64(len(nodes.ids)) + idx.astype(np.uint64)
        pair_chunks.append(np.unique(encoded))
        chunk_nodes.clear(); chunk_parts.clear()

    for src in (119, 120, 121):
        with read_deck(src) as f:
            d = Deck(src, f)
            for kind, line, raw in d.events():
                if kind not in ('shell', 'beam', 'solid', 'discrete'):
                    continue
                v = raw[0] if kind == 'shell' else raw
                eid, opid = v[:2]
                pid = opid + (1000 if src == 120 else 0)
                require(eid > 0, 'nonpositive_element_id', src, line)
                ids_by_kind[kind].append(eid)
                source_mesh[src][kind] += 1
                part_mesh_counts[pid][kind] += 1
                physical = physical_nodes(kind, v)
                if kind == 'shell':
                    require(len(physical) in (3, 4), 'degenerate_shell', src, line)
                    source_mesh[src]['triangle' if len(physical) == 3 else 'quad'] += 1
                if kind == 'beam':
                    require(len(physical) == 2, 'degenerate_beam', src, line)
                    if v[4] > 0:
                        _, ook = nodes.lookup([v[4]])
                        orientation_missing += int(not ook[0])
                if pid not in pid_index:
                    source_missing_parts[(src, pid)] += 1
                    continue
                if kind == 'discrete' and v[3] == 0:
                    source_mesh[src]['ground_discrete'] += 1
                # Nodes are collected in bounded chunks, not per-node Python sets.
                chunk_nodes.extend(physical)
                chunk_parts.extend([pid_index[pid]] * len(physical))
                if len(chunk_nodes) >= 65536:
                    flush()
                targeted = (kind == 'shell' and eid in shell2) or (kind in ('beam', 'discrete') and eid in beam2)
                if targeted:
                    key = (kind, eid)
                    require(key not in targets, 'duplicate_target_element', src, line)
                    ix, found = nodes.lookup(physical)
                    xyz = nodes.xyz[ix[found]]
                    targets[key] = {'src': src, 'line': line, 'kind': kind, 'eid': eid,
                                    'requested_set_kind': 'shell' if kind == 'shell' else 'beam',
                                    'original_pid': opid, 'effective_pid': pid,
                                    'part': parts[pid], 'node_ids': list(physical),
                                    'xyz': xyz.tolist(), 'missing_node_ids': [physical[i] for i in range(len(physical)) if not found[i]],
                                    'centroid': xyz.mean(axis=0).tolist() if len(xyz) == len(physical) else None,
                                    'bounds': bounds(xyz) if len(xyz) == len(physical) else None,
                                    'orientation_node': v[4] if kind == 'beam' else None}
                if kind == 'shell' and eid in shell1:
                    require(eid not in set1_members, 'duplicate_set1_element', src, line)
                    set1_members[eid] = pid
            audit_stream(src, d.stats)
            require(d.stats == source_counts[src], 'pass_hash_or_count_change', src)
    flush()
    require(not source_missing_parts, 'missing_element_part')
    duplicates = {}
    allids = []
    for kind, ids in ids_by_kind.items():
        x = np.frombuffer(ids, dtype=np.int64)
        duplicates[kind] = len(x) - len(np.unique(x))
        allids.append(x)
    require(not any(duplicates.values()), 'duplicate_element_within_kind')
    joined_ids = np.concatenate(allids)
    cross_kind_duplicates = len(joined_ids) - len(np.unique(joined_ids))
    del joined_ids, allids, ids_by_kind
    pairs = np.unique(np.concatenate(pair_chunks))
    del pair_chunks
    gc.collect()
    partition = np.searchsorted(pairs, np.arange(len(pid_order) + 1, dtype=np.uint64) * np.uint64(len(nodes.ids)))
    part_nodes = {}
    thermal_degree = np.zeros(len(tids), dtype=np.int32)

    def summarize(ix):
        a = assignment_at_node[ix]
        ai = a[a >= 0]
        assigned_ix = ix[a >= 0]
        unambiguous = ts_low[ai] == ts_high[ai]
        return {'unique_node_count': len(ix), 'bounds': bounds(nodes.xyz[ix]),
                'assigned_node_count': len(ai), 'unassigned_node_count': len(ix) - len(ai),
                'temperature_unambiguous': temperature_summary(ts_low[ai[unambiguous]]),
                'coefficient_envelope': coefficient_envelope(ts_low[ai], ts_high[ai]),
                'assigned_bounds': bounds(nodes.xyz[assigned_ix]),
                'threshold_bounds_definite': {str(q): bounds(nodes.xyz[assigned_ix[ts_low[ai] > q]]) for q in (25.01, 100, 200, 300)},
                'threshold_bounds_possible': {str(q): bounds(nodes.xyz[assigned_ix[ts_high[ai] > q]]) for q in (25.01, 100, 200, 300)}}

    part_results = {}
    for i, pid in enumerate(pid_order):
        ni = (pairs[partition[i]:partition[i + 1]] % np.uint64(len(nodes.ids))).astype(np.int64)
        part_nodes[pid] = ni
        ai = assignment_at_node[ni]
        np.add.at(thermal_degree, ai[ai >= 0], 1)
        part_results[pid] = {**parts[pid], 'element_counts': dict(part_mesh_counts[pid]), **summarize(ni)}
    union_ix = np.unique(pairs % np.uint64(len(nodes.ids))).astype(np.int64)
    thermal_global = {'temperature_unambiguous': temperature_summary(ts_low[ts_low == ts_high]),
                      'coefficient_envelope': coefficient_envelope(ts_low, ts_high),
                      'assignment_rows': thermal_duplicates,
                      'base_min': float(tb.min()), 'base_max': float(tb.max()),
                      'curve_ids': np.unique(lc).tolist(), 'missing_mesh_node_count': int(np.sum(~tok)),
                      'incident_zero_parts': int(np.sum(thermal_degree == 0)),
                      'incident_one_part': int(np.sum(thermal_degree == 1)),
                      'incident_multiple_parts': int(np.sum(thermal_degree > 1)),
                      'part_node_incidence_count': int(thermal_degree.sum()),
                      'incidence_histogram': {str(k): int(v) for k, v in zip(*np.unique(thermal_degree, return_counts=True))},
                      'bounds': bounds(nodes.xyz[thermal_ix[tok]])}
    plane_results = []
    for plane in planes:
        require(len(plane['cards']) == 2, 'plane_card_count', plane['src'], plane['line'])
        sid = plane['cards'][0][0] or 0
        key = (121, 'SET_PART_LIST', sid)
        selected = pid_order if sid == 0 else sets.get(key)
        require(selected is not None, 'plane_missing_part_set', plane['src'], plane['line'])
        missing = sorted(set(selected) - set(parts))
        chosen = [part_nodes[p] for p in selected if p in part_nodes]
        ni = np.unique(np.concatenate(chosen)) if chosen else np.asarray([], dtype=np.int64)
        plane_results.append({**plane, 'part_set_id': sid, 'part_ids': selected,
                              'missing_part_ids': missing, **summarize(ni)})
    case1 = {'requested': len(shell1), 'matched': len(set1_members),
             'unmatched': sorted(shell1 - set(set1_members)), 'overlap_set2_shell': len(shell1 & shell2),
             'matched_per_part': dict(Counter(set1_members.values()))}
    result = {'sources': source_counts, 'mesh': dict(source_mesh), 'node_count': len(nodes.ids),
              'node_bounds': bounds(nodes.xyz),
              'duplicate_elements_by_kind': duplicates, 'cross_kind_duplicate_count': cross_kind_duplicates,
              'orientation_missing_node_count': orientation_missing, 'parts': part_results,
              'definitions': definitions, 'sets': sets, 'set_lines': set_lines,
              'includes': includes, 'transforms': transforms, 'termination': termination,
              'active_delete': active_delete, 'targets': targets, 'case1': case1,
              'target_missing': {'shell': sorted(shell2 - {k[1] for k in targets if k[0] == 'shell'}),
                                 'beam': sorted(beam2 - {k[1] for k in targets if k[0] in ('beam', 'discrete')})},
              'thermal': thermal_global, 'all_incident_nodes': summarize(union_ix), 'planes': plane_results,
              'unique_incidence_count': len(pairs)}
    return result


def full_join_fixture():
    """Run the actual two-pass assembler against six finite synthetic decks."""
    fixtures = {
        116: '*SET_SHELL_LIST\n2\n11\n*SET_BEAM\n2\n12,13\n',
        117: '*SET_SHELL_LIST\n1\n11,99\n',
        118: '*LOAD_THERMAL_VARIABLE_NODE\n10,25,0,2\n11,100,0,2\n11,200,0,2\n12,300,0,2\n',
        119: '*KEYWORD\n*END\n',
        120: '*PART\n\n1,1,1\n*MAT_RIGID\n1,1,1\n*SECTION_SHELL\n1,2\n*ELEMENT_SHELL_THICKNESS\n11,1,10,11,12,12\n.1,.1,.1,.1\n',
        121: ('*NODE\n10,0,0,0\n11,2,0,0\n12,0,2,0\n13,20,10,0\n'
              '*PART\n\n2,2,2\n*MAT_ELASTIC\n2,1,1\n*SECTION_BEAM\n2,1\n'
              '*PART\n\n3,3,99\n*SECTION_DISCRETE\n3,1\n'
              '*ELEMENT_BEAM\n12,2,10,11,13\n*ELEMENT_DISCRETE\n13,3,10,0,99,1,1,0\n'
              '*SET_PART_LIST\n179\n1001,2\n*DATABASE_CROSS_SECTION_PLANE_ID\n79,Col79\n179,0,0,0,0,0,1\n,,,,,,,\n'
              '*INCLUDE_TRANSFORM\nelem_thick_to-renum.k\n0,0,1000,1000,0,0,0\n1000\n1.,1.,1.,1.,0.\n0\n'
              '*INCLUDE\ndiscrete_mass.k\n*INCLUDE\nWTC7_CaseB_400pm.int\n*CONTROL_TERMINATION\n4.5\n')}
    global read_deck, audit_stream
    old_reader, old_audit, old_progress = read_deck, audit_stream, len(RUN_PROGRESS)
    try:
        read_deck = lambda src: io.BytesIO(fixtures[src].encode('ascii'))
        audit_stream = lambda src, stats: require(stats['eof'], 'fixture_eof')
        got = model_join()
    finally:
        read_deck, audit_stream = old_reader, old_audit
        del RUN_PROGRESS[old_progress:]
    require(got['node_count'] == 4 and got['unique_incidence_count'] == 6, 'full_join_node_counts')
    require(got['parts'][1001]['unique_node_count'] == 3 and got['parts'][2]['unique_node_count'] == 2, 'full_join_part_counts')
    require(got['parts'][3]['material_definition_status'] == 'missing', 'full_join_missing_material')
    require(got['thermal']['assignment_rows']['row_count'] == 4 and got['thermal']['coefficient_envelope']['node_count'] == 3, 'full_join_thermal_rows')
    require(got['thermal']['incidence_histogram'] == {'1': 1, '2': 1, '3': 1}, 'full_join_incidence')
    require(got['parts'][1001]['coefficient_envelope']['thresholds']['100'] == {'definite_gt': 1, 'possible_gt': 2}, 'full_join_thresholds')
    require(got['targets'][('beam', 12)]['centroid'] == [1., 0., 0.], 'full_join_orientation')
    require(np.max(np.abs(np.asarray(got['targets'][('shell', 11)]['centroid']) - [2/3, 2/3, 0])) < TOL, 'full_join_triangle_geometry')
    require(got['targets'][('discrete', 13)]['node_ids'] == [10] and not got['target_missing']['beam'], 'full_join_discrete_id_match')
    require(got['case1']['matched'] == 1 and got['case1']['unmatched'] == [99] and got['case1']['overlap_set2_shell'] == 1, 'full_join_case1')
    require(got['planes'][0]['part_set_id'] == 179 and got['planes'][0]['unique_node_count'] == 3, 'full_join_plane_union')
    require(not got['active_delete'], 'full_join_no_active_deletion')


def selftests():
    tests = []
    def run(name, data, expected):
        d = Deck(0, io.BytesIO(data.encode('ascii')))
        ev = list(d.events())
        require(expected(ev), 'selftest_' + name)
        tests.append(name)
        return ev
    run('fixed_node', '*NODE\n' + f'{17:8d}{1.25:16.8e}{-2.5:16.8e}{3.:16.8e}\n',
        lambda e: e[0][2][:4] == (17, 1.25, -2.5, 3.))
    run('free_node', '*NODE\n17,1.25,-2.5,3,0,0\n', lambda e: e[0][2][:4] == (17, 1.25, -2.5, 3.))
    e = run('shell_continuation_triangle', '*ELEMENT_SHELL_THICKNESS\n1,2,10,11,12,12\n.1,.2,.3,.3\n',
            lambda e: len(e) == 1 and e[0][0] == 'shell' and physical_nodes('shell', e[0][2][0]) == (10, 11, 12))
    require(e[0][2][1] == (.1, .2, .3, .3, 0.), 'thickness_values')
    run('beam_orientation_excluded', '*ELEMENT_BEAM\n2,3,10,11,999\n',
        lambda e: physical_nodes('beam', e[0][2]) == (10, 11) and e[0][2][4] == 999)
    run('discrete_ground_vid_not_node', '*ELEMENT_DISCRETE\n3,4,10,0,987,1,1,0\n',
        lambda e: physical_nodes('discrete', e[0][2]) == (10,))
    a = run('old_solid', '*ELEMENT_SOLID\n4,5,1,2,3,4,5,6,7,8\n', lambda e: len(e) == 1)
    b = run('new_solid', '*ELEMENT_SOLID\n4,5\n1,2,3,4,5,6,7,8\n', lambda e: len(e) == 1)
    require(a[0][2] == b[0][2], 'solid_layout_equivalence')
    run('thermal_field_order', '*LOAD_THERMAL_VARIABLE_NODE\n10,300,25,2\n', lambda e: e[0][2] == (10, 300., 25., 2))
    run('blank_part_title', '*PART\n\n1,2,3\n', lambda e: e[0][0] == 'part' and e[0][2][:3] == (1, 2, 3))
    run('blank_plane_defaults', '*DATABASE_CROSS_SECTION_PLANE_ID\n' + f'{79:10d}' + 'Col79\n179,0,0,-64.9,0,0,90.4748\n\n',
        lambda e: len(e) == 3 and e[0][2][:2] == (79, 79) and e[2][2][1] == (None,) * 8)
    run('comma_plane_id_and_padding', '*DATABASE_CROSS_SECTION_PLANE_ID\n79,Col79\n179,0,0,-64.9,0,0,90.4748\n,,,,,,,\n',
        lambda e: len(e) == 3 and e[0][2][:2] == (79, 79) and e[2][2][1] == (None,) * 8)
    run('include_transform_cards', '*INCLUDE_TRANSFORM\nelem_thick_to-renum.k\n0,0,1000,1000,0,0,0\n1000\n1,1,1,1,0\n0\n',
        lambda e: len(e) == 5 and e[-1][2] == (4, (0,)))
    run('numeric_conversion_convention', '*INCLUDE_TRANSFORM\nelem_thick_to-renum.k\n0,0,1000,1000,0,0,0\n1000\n1.0,1.0,1.0,1.0,0.0\n0\n',
        lambda e: e[3][2] == (3, (1., 1., 1., 1., 0.)))
    require(offset_part(120, (7, 8, 9)) == [1007, 1008, 1009], 'offset_fixture')
    require(offset_part(120, (7, 0, 0)) == [1007, 0, 0], 'zero_offset_fixture')
    tests.append('part_material_section_offsets')
    n = NodeTable(array('q', [12, 10, 11]), array('d', [2, 0, 0, 0, 0, 0, 1, 0, 0]))
    ix, ok = n.lookup([10, 12, 13]); require(ix[:2].tolist() == [0, 2] and ok.tolist() == [True, True, False], 'lookup_fixture')
    tests.append('node_sort_missing_lookup')
    require(temperature_summary([25, 25.01, 100, 200, 300, 301]) == {'count': 6, 'min': 25., 'max': 301., 'le_25_01': 2, 'gt_25_01': 4, 'gt_100': 3, 'gt_200': 2, 'gt_300': 1}, 'threshold_fixture')
    tests.append('exact_threshold_boundaries')
    unique = deduplicate_assignments(np.array([2, 1, 2]), np.array([100., 25., 100.]), np.array([0., 0., 0.]), np.array([2, 2, 2]))
    require(unique[0].tolist() == [1, 2] and unique[1].tolist() == [25., 100.] and unique[5]['repeated_rows'] == 1, 'identical_thermal_fixture')
    tests.append('identical_thermal_duplicates')
    ambiguous = deduplicate_assignments(np.array([2, 2, 1]), np.array([100., 101., 25.]), np.array([0., 0., 0.]), np.array([2, 2, 2]))
    require(ambiguous[1].tolist() == [25., 100.] and ambiguous[2].tolist() == [25., 101.], 'thermal_range_fixture')
    env = coefficient_envelope(ambiguous[1], ambiguous[2])
    require(env['thresholds']['100'] == {'definite_gt': 0, 'possible_gt': 1} and env['ambiguous_count'] == 1, 'thermal_threshold_range_fixture')
    tests.append('conflicting_ts_ranges_and_thresholds')
    try:
        deduplicate_assignments(np.array([2, 2]), np.array([100., 101.]), np.array([0., 1.]), np.array([2, 2]))
    except CheckError as e:
        require(e.code == 'conflicting_base_or_curve_assignments', 'wrong_thermal_conflict')
    else:
        raise CheckError('missing_thermal_conflict')
    tests.append('conflicting_thermal_base_rejected')
    # Two parts share node1; repeated links within each part are not new samples.
    encoded = np.unique(np.asarray([0, 1, 1, 4, 4, 5], dtype=np.uint64))
    require(encoded.tolist() == [0, 1, 4, 5] and len(np.unique(encoded % 3)) == 3, 'shared_nodes_fixture')
    tests.append('shared_node_deduplication')
    run('inactive_damage', '$ *DELETE_SHELL_SET\n$ 2\n*SET_SHELL_LIST\n2\n1,2,3\n',
        lambda e: not any(x[0] == 'active_delete' for x in e))
    for name, data, code in [
        ('missing_thickness', '*ELEMENT_SHELL_THICKNESS\n1,2,10,11,12,12\n', 'missing_element_continuation'),
        ('ambiguous_solid', '*ELEMENT_SOLID\n1,2,3\n', 'ambiguous_solid_card'),
        ('variant_rejected', '*ELEMENT_SHELL_THICKNESS_OFFSET\n', 'unsupported_card_variant'),
        ('nonfinite_rejected', '*NODE\n1,NaN,0,0\n', 'nonnumeric_field'),
        ('nonnumeric_part_rejected', '*PART\nignored heading\n1,parameter,3\n', 'nonnumeric_field'),
    ]:
        try:
            list(Deck(0, io.BytesIO(data.encode('ascii'))).events())
        except CheckError as e:
            require(e.code == code, 'wrong_rejection_' + name)
        else:
            raise CheckError('missing_rejection_' + name)
        tests.append(name)
    try:
        NodeTable(array('q', [1, 1]), array('d', [0.] * 6))
    except CheckError as e:
        require(e.code == 'duplicate_node_id', 'wrong_duplicate_rejection')
    else:
        raise CheckError('duplicate_not_rejected')
    tests.append('duplicate_node_rejected')
    full_join_fixture()
    tests.append('full_two_pass_synthetic_assembly_and_joins')
    return tests


# INDEPENDENT_CORE_END -- freeze this prefix before producer code/output reads.


def normalized_plane_heading(heading):
    """Post-schema source normalization; keep raw headings out of derivatives."""
    clean = ' '.join(heading.strip().lower().split())
    match = re.fullmatch(r'col(?:umn)?[ _-]*([0-9]+)(?:[ _-]+x[ _-]*sect(?:ion)?)?', clean)
    all_columns = clean in {'total columns forces', 'total column forces', 'all columns', 'all column forces', 'all columns forces', 'all columns x-sect'}
    return (int(match.group(1)) if match else None), all_columns


def source_header_scan():
    """Independent lexical activity/heading audit, with no raw text output."""
    result = {'parts': {}, 'planes': {}, 'part_sets': {}, 'includes': [], 'active_delete': [], 'commented_delete': [], 'streams': []}
    for src in PINS:
        kw, kwline, index, title_hash, title_raw_hash = None, 0, 0, None, None
        stats = {'bytes': 0, 'lines': 0, 'eof': False}
        h = hashlib.sha256()
        with read_deck(src) as f:
            while True:
                raw = f.readline(LINE_CAP + 1)
                if not raw:
                    break
                stats['lines'] += 1; stats['bytes'] += len(raw); h.update(raw)
                n = stats['lines']
                require(len(raw) <= LINE_CAP and stats['bytes'] <= CAP and b'\0' not in raw, 'supplement_stream_cap', src, n)
                s = raw.decode('ascii').strip()
                commented = s.startswith('$')
                candidate = s.lstrip('$').strip() if commented else s
                if candidate.startswith('*DELETE_'):
                    token = candidate.split('$', 1)[0].strip().upper()
                    known = token in {'*DELETE_ELEMENT_BEAM', '*DELETE_ELEMENT_SHELL', '*DELETE_BEAM_SET', '*DELETE_SHELL_SET'}
                    result['commented_delete' if commented else 'active_delete'].append(
                        {'src': src, 'line': n, 'keyword': token if known else None, 'keyword_sha256': hashlib.sha256(token.encode()).hexdigest()})
                if commented:
                    continue
                if s.startswith('*'):
                    kw, kwline, index = s.split('$', 1)[0].strip().upper(), n, 0
                    continue
                if not s and not (kw == '*PART' and index == 0):
                    continue
                i, index = index, index + 1
                if kw == '*PART':
                    if i == 0:
                        title_hash = hashlib.sha256(s.encode()).hexdigest()
                        title_raw_hash = hashlib.sha256(raw.rstrip(b'\r\n')).hexdigest()
                    elif i == 1:
                        v = card(raw.decode(), [10] * 8, range(8), 3)
                        pid = offset_part(src, v)[0]
                        result['parts'][str(pid)] = {'src': src, 'line': n, 'keyword_line': kwline, 'heading_sha256': title_hash,
                                                    'heading_preserving_spaces_sha256': title_raw_hash}
                elif kw == '*DATABASE_CROSS_SECTION_PLANE_ID' and i == 0:
                    first, heading = s.split(',', 1) if ',' in s else (s[:10], s[10:])
                    csid = number(first, True)
                    col, allcol = normalized_plane_heading(heading)
                    result['planes'][str(csid)] = {'src': src, 'line': n, 'keyword_line': kwline,
                        'column_number': col, 'all_columns': allcol,
                        'heading_only_sha256': hashlib.sha256(heading.strip().encode()).hexdigest(),
                        'raw_id_heading_card_sha256': hashlib.sha256(raw.rstrip(b'\r\n')).hexdigest(),
                        'stripped_id_heading_card_sha256': hashlib.sha256(s.encode()).hexdigest()}
                elif kw == '*SET_PART_LIST' and i == 0:
                    sid = card(raw.decode(), [10] * 8, [0], 1)[0]
                    result['part_sets'][str(sid)] = {'src': src, 'line': n, 'keyword_line': kwline}
                elif kw in ('*INCLUDE', '*INCLUDE_TRANSFORM') and i == 0:
                    require(s in NAME_IDS, 'supplement_unknown_include', src, n)
                    result['includes'].append({'src': src, 'keyword_line': kwline, 'line': n, 'kind': kw, 'included_src': NAME_IDS[s]})
        stats.update(eof=True, sha256=h.hexdigest())
        audit_stream(src, stats)
        result['streams'].append({'src': src, **stats})
    return result


def supplemental_calculation():
    """Post-schema independent extrema, Case A geometry and bounded examples."""
    unit = Path(__file__).parent
    checkpoint_file = unit / 'independent-checkpoint01.json'
    require(sha(checkpoint_file) == '85e2649cdc2ccc2974f4959e5f19bb8d01f8533e16326bb2647c092252bcbd2e', 'checkpoint_pin')
    own = json.loads(checkpoint_file.read_text())['result']
    headers = source_header_scan()
    streams = []
    def events(src):
        with read_deck(src) as f:
            deck = Deck(src, f)
            yield from deck.events()
            audit_stream(src, deck.stats)
            streams.append({'src': src, **deck.stats})
    ids, scales, bases, curves = array('q'), array('d'), array('d'), array('q')
    for kind, line, v in events(118):
        if kind == 'thermal':
            ids.append(v[0]); scales.append(v[1]); bases.append(v[2]); curves.append(v[3])
    raw_ids = np.frombuffer(ids, dtype=np.int64)
    tids, lo, hi, _, _, duplicate = deduplicate_assignments(raw_ids, np.frombuffer(scales, dtype=np.float64), np.frombuffer(bases, dtype=np.float64), np.frombuffer(curves, dtype=np.int64))
    count_ids, row_counts = np.unique(raw_ids, return_counts=True)
    require(np.array_equal(count_ids, tids), 'supplement_thermal_order')
    del raw_ids, ids, scales, bases, curves, count_ids
    case_ids = set()
    for kind, line, v in events(117):
        if kind == 'set_ids' and v[0] == 'SET_SHELL_LIST' and v[1] == 1:
            case_ids.update(x for x in v[2] if x > 0)
    part_extrema = {str(p['effective'][0]): None for p in own['parts']}
    selected_parts = set(p for plane in own['planes'] for p in plane['part_ids'])
    high_by_part = defaultdict(set)
    case_by_part = defaultdict(set)
    case_element_counts = Counter()
    chunk_nodes, chunk_parts = [], []
    def flush():
        if not chunk_nodes:
            return
        ns = np.asarray(chunk_nodes, dtype=np.int64)
        ps = np.asarray(chunk_parts, dtype=np.int64)
        ix = np.searchsorted(tids, ns)
        valid = (ix < len(tids)) & (tids[np.minimum(ix, len(tids) - 1)] == ns)
        ix, ps = ix[valid], ps[valid]
        for pid in np.unique(ps):
            take = ix[ps == pid]
            row = [float(lo[take].min()), float(lo[take].max()), float(hi[take].min()), float(hi[take].max())]
            key = str(int(pid)); old = part_extrema[key]
            part_extrema[key] = row if old is None else [min(old[0], row[0]), max(old[1], row[1]), min(old[2], row[2]), max(old[3], row[3])]
            if int(pid) in selected_parts:
                high_by_part[int(pid)].update(int(x) for x in tids[take[hi[take] > 300]])
        chunk_nodes.clear(); chunk_parts.clear()
    for src in (119, 120, 121):
        for kind, line, raw in events(src):
            if kind not in ('shell', 'beam', 'discrete', 'solid'):
                continue
            v = raw[0] if kind == 'shell' else raw
            pid = v[1] + (1000 if src == 120 else 0)
            ns = physical_nodes(kind, v)
            chunk_nodes.extend(ns); chunk_parts.extend([pid] * len(ns))
            if len(chunk_nodes) >= 65536:
                flush()
            if kind == 'shell' and v[0] in case_ids:
                case_by_part[pid].update(ns); case_element_counts[pid] += 1
    flush()
    needed = set().union(*case_by_part.values(), *high_by_part.values())
    coordinates = {}
    for src in (119, 121):
        for kind, line, v in events(src):
            if kind == 'node' and v[0] in needed:
                require(v[0] not in coordinates, 'supplement_duplicate_coordinate', src, line)
                coordinates[v[0]] = v[1:4]
    require(set(coordinates) == needed, 'supplement_missing_coordinate')
    case_bounds = {str(pid): {'elements': case_element_counts[pid],
                            'bounds': bounds(np.asarray([coordinates[n] for n in sorted(ns)]))}
                   for pid, ns in case_by_part.items()}
    plane_extrema, examples = {}, {}
    for plane in own['planes']:
        csid, pids = str(plane['csid']), plane['part_ids']
        ext = [part_extrema[str(p)] for p in pids if part_extrema.get(str(p)) is not None]
        plane_extrema[csid] = [min(e[0] for e in ext), max(e[1] for e in ext), min(e[2] for e in ext), max(e[3] for e in ext)] if ext else None
        ns = set().union(*(high_by_part[p] for p in pids))
        ordered = sorted(ns, key=lambda n: (-hi[np.searchsorted(tids, n)], n))[:10]
        examples[csid] = []
        for nid in ordered:
            ix = int(np.searchsorted(tids, nid))
            examples[csid].append({'nid': nid, 'min': float(lo[ix]), 'max': float(hi[ix]),
                'rows': int(row_counts[ix]), 'coordinates': list(coordinates[nid]),
                'incident_part_ids_in_set': [p for p in pids if nid in high_by_part[p]]})
    return {'headers': headers, 'streams': streams, 'thermal_duplicates': duplicate,
            'global_endpoint_extrema': [float(lo.min()), float(lo.max()), float(hi.min()), float(hi.max())],
            'part_endpoint_extrema': part_extrema, 'plane_endpoint_extrema': plane_extrema,
            'casea_parts': case_bounds, 'high_TS_node_examples': examples,
            'targeted_coordinate_count_internal_only': len(coordinates),
            'scope': 'Post-schema independent source check; no full node dump, solver semantics, or physical temperature inference.'}


def supplement():
    dest = Path(__file__).with_name('independent-supplement01.json')
    require(not dest.exists(), 'supplement_exists')
    started = time.time()
    before = check_pins()
    tests = selftests()
    require(normalized_plane_heading('Column 79 x-sect') == (79, False), 'supplement_heading_control')
    result = supplemental_calculation()
    after = check_pins()
    require(before == after, 'supplement_source_changed')
    receipt = {'status': 'PASS', 'inputs_before': before, 'inputs_after': after,
        'verifier_sha256': sha(__file__), 'core_sha256': hashlib.sha256(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0]).hexdigest(),
        'schema_seen_before_supplement': 'run04/member-map.json and receipt.json; no producer code read',
        'schema_sha256': sha(Path(__file__).parent / 'run04/member-map.json'),
        'elapsed_seconds': time.time() - started, 'selftest_count': len(tests) + 1,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)}
    require(receipt['peak_rss_bytes'] <= 768 * 1024 * 1024, 'supplement_memory_cap')
    with dest.open('x') as f:
        json.dump({'receipt': receipt, 'result': result}, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')
    return {'status': 'PASS', 'supplement_sha256': sha(dest), 'elapsed_seconds': receipt['elapsed_seconds'],
            'peak_rss_bytes': receipt['peak_rss_bytes'], 'high_TS_examples': sum(map(len, result['high_TS_node_examples'].values())),
            'casea_parts': len(result['casea_parts']), 'active_delete_count': len(result['headers']['active_delete'])}


class Comparison:
    def __init__(self):
        self.counts = Counter()
        self.max_error = 0.0
        self.failures = []

    def same(self, actual, expected, path):
        if isinstance(actual, bool) or isinstance(expected, bool):
            self.counts['boolean'] += 1
            if type(actual) is not type(expected) or actual != expected:
                self.failures.append({'path': path, 'code': 'boolean'})
        elif isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            is_integer = isinstance(actual, int) and isinstance(expected, int)
            self.counts['integer' if is_integer else 'float'] += 1
            error = abs(actual - expected)
            if not math.isfinite(error) or error > (0 if is_integer else TOL):
                self.failures.append({'path': path, 'code': 'numeric', 'absolute_error': error if math.isfinite(error) else None})
            if math.isfinite(error):
                self.max_error = max(self.max_error, error)
        elif isinstance(actual, dict) and isinstance(expected, dict):
            self.same(sorted(actual), sorted(expected), path + '.keys')
            for key in sorted(set(actual) & set(expected)):
                self.same(actual[key], expected[key], path + '.' + str(key))
        elif isinstance(actual, list) and isinstance(expected, list):
            self.counts['list'] += 1
            if len(actual) != len(expected):
                self.failures.append({'path': path, 'code': 'list_length'})
            for i, (a, b) in enumerate(zip(actual, expected)):
                self.same(a, b, path + '.' + str(i))
        else:
            self.counts['null_or_string'] += 1
            if actual != expected:
                self.failures.append({'path': path, 'code': 'value_or_type'})


def expected_envelope(envelope, unambiguous, extrema):
    def endpoint(which):
        minimum = which == 'min'
        result = {'count': envelope['node_count'],
                  'min': extrema[0 if minimum else 2] if extrema else None,
                  'max': extrema[1 if minimum else 3] if extrema else None,
                  'le_25_01': envelope['possible_le_25_01' if minimum else 'definite_le_25_01']}
        for threshold in (100, 200, 300):
            result['gt_' + str(threshold)] = envelope['thresholds'][str(threshold)]['definite_gt' if minimum else 'possible_gt']
        return result
    return {'conflicting_nodes': envelope['ambiguous_count'],
            'min_assignment_per_node': endpoint('min'), 'max_assignment_per_node': endpoint('max'),
            'unambiguous_nodes_only': {k: v for k, v in unambiguous.items() if k != 'gt_25_01'}}


def final_comparison(output_name=None, producer_run='run06'):
    unit = Path(__file__).parent
    if output_name:
        require(bool(re.fullmatch(r'verification(?:-root)?[0-9]+\.json', output_name)), 'unsafe_verification_output_name')
        require(not (unit / output_name).exists(), 'verification_output_exists')
    files = {'checkpoint': unit / 'independent-checkpoint01.json',
             'supplement': unit / 'independent-supplement01.json',
             'producer_result': unit / producer_run / 'member-map.json', 'producer_receipt': unit / producer_run / 'receipt.json',
             'producer_code': unit / 'map_members.py', 'protocol': unit / 'PROTOCOL.md',
             'thermal_addendum': unit / 'THERMAL-DUPLICATE-ADDENDUM.md',
             'cross_family_addendum': unit / 'CROSS-FAMILY-ADDENDUM.md'}
    pins_before = {k: sha(p) for k, p in files.items()}
    require(pins_before['checkpoint'] == '85e2649cdc2ccc2974f4959e5f19bb8d01f8533e16326bb2647c092252bcbd2e', 'final_checkpoint_pin')
    require(pins_before['supplement'] == '7803e6b2d82b852d37c656e44bbf0c04b4d109f1a1ac03fb97a87ab8816a8fc8', 'final_supplement_pin')
    tests = selftests()
    sources_before = check_pins()
    checkpoint_doc = json.loads(files['checkpoint'].read_text())
    supplement_doc = json.loads(files['supplement'].read_text())
    own, sup = checkpoint_doc['result'], supplement_doc['result']
    # This fresh low-memory scan independently checks the producer's exact raw
    # hash recipe and the previously unresolved all-columns suffix.  Frozen
    # supplementary stripped hashes remain unchanged and are cross-checked.
    fresh_headers = source_header_scan()
    producer = json.loads(files['producer_result'].read_text())
    receipt = json.loads(files['producer_receipt'].read_text())
    c = Comparison()
    c.same(checkpoint_doc['receipt']['core_sha256'], hashlib.sha256(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0]).hexdigest(), 'independent_core_freeze')
    for key, receipt_key in [('producer_code', 'producer_sha256'), ('producer_result', 'result_sha256'),
                             ('protocol', 'protocol_sha256'), ('thermal_addendum', 'thermal_duplicate_addendum_sha256')]:
        c.same(pins_before[key], receipt[receipt_key], 'producer_pin.' + key)
    if 'cross_family_addendum_sha256' in receipt:
        c.same(pins_before['cross_family_addendum'], receipt['cross_family_addendum_sha256'], 'producer_pin.cross_family_addendum')
    c.same(pins_before['protocol'], PROTOCOL_SHA, 'protocol_freeze')
    for src, pin in PINS.items():
        row = receipt['sources'][pin[0]]
        expected = {'compressed_bytes': pin[1], 'compressed_sha256': pin[2], 'uncompressed_bytes': pin[3],
                    'uncompressed_sha256': pin[4], 'eof': True, 'pin_after': True, 'lines': own['sources'][str(src)]['lines']}
        c.same(row, expected, 'source.' + str(src))
    record_counts = {PINS[int(src)][0] + ':' + kind: n for src, counts in own['mesh'].items()
                     for kind, n in counts.items() if kind in ('shell', 'beam', 'solid', 'discrete')}
    c.same(producer['element_records'], record_counts, 'element_records')
    c.same(producer['unique_nodes'], own['node_count'], 'unique_nodes')
    node_rows = {PINS[int(src)][0]: row['data_lines']['NODE'] for src, row in own['sources'].items() if 'NODE' in row['data_lines']}
    c.same(producer['node_rows'], node_rows, 'node_rows')
    c.same(producer['diagnostics'], {'quad_shells': sum(r.get('quad', 0) for r in own['mesh'].values())}, 'quad_count')
    kinds_to_keywords = {'shell': 'ELEMENT_SHELL_THICKNESS', 'beam': 'ELEMENT_BEAM', 'discrete': 'ELEMENT_DISCRETE', 'solid': 'ELEMENT_SOLID'}
    expected_data = {PINS[int(src)][0]: {kind: own['sources'][str(src)]['data_lines'][kinds_to_keywords[kind]]
                      for kind in counts if kind in kinds_to_keywords} for src, counts in own['mesh'].items()}
    c.same(receipt['data_lines'], expected_data, 'element_data_lines')
    c.same(producer['part_definition_count'], len(own['parts']), 'part_definitions')
    c.same(producer['partset_count'], len(own['part_sets']), 'partset_count')
    c.same(producer['plane_count'], len(own['planes']), 'plane_count')
    parts = {p['effective'][0]: p for p in own['parts']}
    active = {pid for pid, p in parts.items() if p['element_counts']}
    c.same(sorted(p['pid'] for p in producer['parts']), sorted(active), 'active_part_coverage')

    def expected_definition(part):
        pid, sec, mat = part['effective']
        return {'pid': pid, 'section_id': sec, 'material_id': mat,
                'original_pid': part['original'][0], 'original_section_id': part['original'][1],
                'original_material_id': part['original'][2], 'line': part['line'],
                'source': PINS[part['src']][0], 'heading_sha256': fresh_headers['parts'][str(pid)]['heading_preserving_spaces_sha256']}

    for row in producer['parts']:
        pid = row['pid']; part = parts[pid]; path = 'part.' + str(pid)
        expected = {'pid': pid, 'definition': expected_definition(part), 'elements': part['element_counts'],
                    'geometry_bounds': part['bounds'], 'thermal_node_bounds': part['assigned_bounds'],
                    'assigned_TS_envelope': expected_envelope(part['coefficient_envelope'], part['temperature_unambiguous'], sup['part_endpoint_extrema'][str(pid)]),
                    'material_keyword': '*' + part['material_definition_keywords'][0] if part['material_definition_status'] == 'resolved' else None,
                    'section_defined': part['section_definition_status'] == 'resolved'}
        c.same(row, expected, path)

    targets = {(t['kind'], t['eid']): t for t in own['targets']}
    ordinary = producer['damage_set2']['elements']
    candidates = producer['set2_beam_id_discrete_candidates']['elements']
    c.same(sorted((r['kind'], r['eid']) for r in ordinary + candidates), sorted(targets), 'target_coverage')
    for row in ordinary + candidates:
        t = targets[(row['kind'], row['eid'])]
        expected = {'eid': t['eid'], 'kind': t['kind'], 'line': t['line'], 'source': PINS[t['src']][0],
                    'pid': t['effective_pid'], 'original_pid': t['original_pid'], 'definition': expected_definition(t['part']),
                    'node_ids': t['node_ids'], 'node_coordinates': t['xyz'], 'missing_nodes': t['missing_node_ids'],
                    'centroid': t['centroid'], 'bounds': t['bounds'], 'orientation_node': t['orientation_node']}
        if t['kind'] == 'discrete':
            expected['selection_status'] = 'numeric_set2_beam_id_cross_family_candidate'
        c.same(row, expected, 'target.' + t['kind'] + '.' + str(t['eid']))
    c.same(producer['damage_set2']['matched'], {'shell': sum(t['kind'] == 'shell' for t in own['targets']), 'beam': sum(t['kind'] == 'beam' for t in own['targets'])}, 'explicit_target_matches')
    c.same(producer['damage_set2']['unmatched'], {'shell': own['target_missing']['shell'], 'beam': sorted(t['eid'] for t in own['targets'] if t['kind'] == 'discrete')}, 'explicit_family_unmatched')
    c.same(producer['set2_beam_id_discrete_candidates']['count'], len(candidates), 'candidate_count')
    c.same(producer['casea_set1']['matched'], own['case1']['matched'], 'casea.matched')
    c.same(len(producer['casea_set1']['unmatched']), own['case1']['unmatched_count'], 'casea.unmatched')
    c.same(len(producer['casea_set1']['overlap_set2_shells']), own['case1']['overlap_set2_shell'], 'casea.overlap')
    c.same(producer['casea_set1']['parts'], sup['casea_parts'], 'casea.parts')
    c.same({k: v['elements'] for k, v in sup['casea_parts'].items()}, own['case1']['matched_per_part'], 'casea.independent_supplement_counts')

    planes = {p['csid']: p for p in own['planes']}
    c.same(sorted(p['plane_id'] for p in producer['column_diagnostics']), sorted(planes), 'plane_coverage')
    example_count = 0
    for row in producer['column_diagnostics']:
        pid = row['plane_id']; p = planes[pid]; key = str(pid); header = fresh_headers['planes'][key]
        c.same(header['heading_only_sha256'], p['heading_sha256'], 'plane.' + key + '.independent_heading_recipe')
        first = list(p['cards'][0])
        while first and first[-1] is None:
            first.pop()
        expected = {'plane_id': pid, 'psid': p['part_set_id'], 'source': PINS[p['src']][0],
                    'line': header['keyword_line'], 'column_number': header['column_number'], 'all_columns': header['all_columns'],
                    'heading_sha256': header['raw_id_heading_card_sha256'], 'plane_card': first, 'second_plane_card': p['cards'][1],
                    'partset': {'source': PINS[p['src']][0], 'line': sup['headers']['part_sets'][str(p['part_set_id'])]['keyword_line'], 'part_ids': p['part_ids']},
                    'missing_part_ids': p['missing_part_ids'], 'member_geometry_bounds': p['bounds'], 'thermal_node_bounds': p['assigned_bounds'],
                    'assigned_TS_envelope': expected_envelope(p['coefficient_envelope'], p['temperature_unambiguous'], sup['plane_endpoint_extrema'][key]),
                    'scope': 'entire_referenced_part_set_not_only_plane_intersection',
                    'high_TS_node_examples': [{k: example[k] for k in ('nid', 'min', 'max', 'rows')} for example in sup['high_TS_node_examples'][key]]}
        c.same(row, expected, 'plane.' + key)
        for example in sup['high_TS_node_examples'][key]:
            c.same(bool(example['incident_part_ids_in_set']), True, 'plane.' + key + '.example_membership.' + str(example['nid']))
            c.same(example['max'] > 300, True, 'plane.' + key + '.example_threshold.' + str(example['nid']))
            example_count += 1
    thermal = own['thermal']; tr = receipt['thermal']; d = thermal['assignment_rows']
    for rootkey, ownkey in [('rows', 'row_count'), ('repeated_rows_beyond_unique', 'repeated_rows'),
                             ('nodes_with_repeated_rows', 'repeated_node_groups'), ('conflicting_node_count', 'ambiguous_ts_node_groups'),
                             ('max_rows_per_node', 'max_rows_per_node')]:
        c.same(tr[rootkey], d[ownkey], 'thermal.' + rootkey)
    c.same(tr['row_assigned_TS'], {k: v for k, v in d['row_temperature'].items() if k != 'gt_25_01'}, 'thermal.raw_rows')
    c.same(tr['unique_node_assigned_TS_envelope'], expected_envelope(thermal['coefficient_envelope'], thermal['temperature_unambiguous'], sup['global_endpoint_extrema']), 'thermal.unique_envelope')
    c.same(tr['bases'], {str(thermal['base_min']): d['row_count']}, 'thermal.base')
    c.same(thermal['base_min'], thermal['base_max'], 'thermal.constant_base')
    c.same(tr['curves'], {str(thermal['curve_ids'][0]): d['row_count']}, 'thermal.curve')
    c.same(thermal['curve_ids'], [2], 'thermal.curve_ids')
    c.same(tr['largest_supplied_ranges'], [{'nid': r['node_id'], 'min': r['min'], 'max': r['max'], 'rows': r['rows']} for r in d['largest_ts_ranges']], 'thermal.largest_ranges')
    c.same(producer['thermal_join'], {'no_geometry': thermal['missing_mesh_node_count'], 'no_mesh_incidence': thermal['incident_zero_parts'],
               'multiple_part_incidence': thermal['incident_multiple_parts'], 'part_incidence_sum': thermal['part_node_incidence_count'],
               'max_part_incidence': max(int(k) for k in thermal['incidence_histogram']), 'missing_assignments_mean': 'unknown_not_ambient'}, 'thermal.join')
    c.same(producer['active_delete_cards'], sup['headers']['active_delete'], 'active_delete_independent_scan')
    expected_includes = [{'source': PINS[r['src']][0], 'line': r['keyword_line'], 'kind': r['kind'], 'included': PINS[r['included_src']][0]} for r in sup['headers']['includes']]
    c.same(producer['includes'], expected_includes, 'includes')
    transform = producer['transforms'][0]
    c.same(len(producer['transforms']), 1, 'transform.count')
    c.same(transform['source'], PINS[121][0], 'transform.source')
    c.same(transform['line'], next(r['keyword_line'] for r in sup['headers']['includes'] if r['kind'] == '*INCLUDE_TRANSFORM'), 'transform.line')
    c.same(transform['cards'], [r[3] + [None] * (8 - len(r[3])) for r in own['transforms']], 'transform.cards')
    c.same(transform['coordinate_transform'], 'identity', 'transform.coordinate_rule')
    c.same(transform['FCTTEM_caveat'], 'numeric_1_in_character_conversion_flag_field', 'transform.temperature_caveat')
    # Freshly reproduce small list streams, including source header locators.
    for src, field in [(116, 'damage_sets'), (117, 'casea_sets')]:
        values, headers = defaultdict(list), {}
        with read_deck(src) as f:
            deck = Deck(src, f)
            for kind, line, v in deck.events():
                if kind == 'set_header':
                    family = 'shell' if v[0] == 'SET_SHELL_LIST' else 'beam'
                    headers[family] = {'header_line': line, 'set_id': v[1]}
                elif kind == 'set_ids':
                    family = 'shell' if v[0] == 'SET_SHELL_LIST' else 'beam'
                    values[family].extend(x for x in v[2] if x != 0)
            audit_stream(src, deck.stats)
        if src == 116:
            expected_sets = {k: {**h, 'ids': values[k]} for k, h in headers.items()}
        else:
            expected_sets = {k: {**h, 'count': len(values[k])} for k, h in headers.items()}
        c.same(receipt[field], expected_sets, field)
    c.same(receipt['status'], 'complete', 'producer_status')
    c.same(receipt['controls']['errors'], 0, 'producer_recorded_controls.errors')
    c.same(receipt['controls']['failures'], 0, 'producer_recorded_controls.failures')
    c.same(receipt['controls']['run'] > 0, True, 'producer_recorded_controls.nonempty')
    c.same(fresh_headers['active_delete'], sup['headers']['active_delete'], 'repeated_active_delete_scan')
    for pid, row in sup['headers']['parts'].items():
        c.same(fresh_headers['parts'][pid]['heading_sha256'], row['heading_sha256'], 'stripped_part_heading_stability.' + pid)
    sources_after = check_pins()
    pins_after = {k: sha(p) for k, p in files.items()}
    c.same(sources_after, sources_before, 'source_pins_stable')
    c.same(pins_after, pins_before, 'derivative_pins_stable')
    result = {'status': 'PASS' if not c.failures else 'FAIL', 'absolute_float_tolerance': TOL,
              'integer_and_membership_comparison': 'exact', 'comparison_counts': dict(c.counts),
              'maximum_absolute_error': c.max_error, 'failures': c.failures,
              'input_hashes_before': pins_before, 'input_hashes_after': pins_after,
              'source_pins_before': sources_before, 'source_pins_after': sources_after,
              'verifier_sha256': sha(__file__), 'command': sys.argv, 'producer_run': producer_run,
              'fresh_header_scan': {'source_count': len(fresh_headers['streams']), 'part_headings': len(fresh_headers['parts']),
                 'plane_headings': len(fresh_headers['planes']), 'recognized_columns': sum(r['column_number'] is not None for r in fresh_headers['planes'].values()),
                 'recognized_all_columns': sum(r['all_columns'] for r in fresh_headers['planes'].values()),
                 'active_delete': fresh_headers['active_delete'], 'commented_delete': fresh_headers['commented_delete'], 'streams': fresh_headers['streams']},
              'coverage': {'part_definitions': len(parts), 'element_bearing_parts': len(active), 'planes': len(planes),
                           'part_sets': len(own['part_sets']), 'damage_shells': sum(t['kind'] == 'shell' for t in own['targets']),
                           'damage_explicit_beams': sum(t['kind'] == 'beam' for t in own['targets']),
                           'damage_discrete_numeric_candidates': len(candidates), 'casea_elements': own['case1']['matched'],
                           'casea_part_bounds': len(sup['casea_parts']), 'high_TS_example_occurrences': example_count,
                           'high_TS_unique_example_nodes': len({e['nid'] for examples in sup['high_TS_node_examples'].values() for e in examples}),
                           'independent_control_groups': len(tests)},
              'limitations': ['Numeric input joins are not solver execution or physical-cause identification.',
                 'Producer control count is checked as a receipt statement; final consumer comparison does not itself rerun producer unit tests.',
                 'Original checkpoint bare-column labels and delete-spelling guard were supplemented by independent source scans after schema access.',
                 'Producer heading hashes retain source whitespace excluding CR/LF; plane hashes include the ID card, not only the heading. Both recipes were independently source-checked.',
                 'Earlier producer code versions are not reconstructed here; the selected final producer code is directly hash checked.',
                 'Cross-family numeric matches do not establish deletion semantics; coefficient ranges are source-assignment envelopes.']}
    if output_name:
        require(bool(re.fullmatch(r'verification(?:-root)?[0-9]+\.json', output_name)), 'unsafe_verification_output_name')
        require(not c.failures, 'comparison_failed_no_final_receipt_written')
        with (unit / output_name).open('x') as f:
            json.dump(result, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')
    return result


def safe_checkpoint(result):
    """Never serialize node arrays, arbitrary text, or the Case A ID list."""
    result = dict(result)
    result['parts'] = [result['parts'][p] for p in sorted(result['parts'])]
    result['targets'] = [result['targets'][k] for k in sorted(result['targets'])]
    result['definitions'] = [{'keyword': k[0], 'effective_id': k[1], 'src': v[0], 'line': v[1], 'original_id': v[2]}
                             for k, v in sorted(result['definitions'].items())]
    result['part_sets'] = [{'src': k[0], 'sid': k[2], 'line': result['set_lines'][k], 'part_ids': v}
                           for k, v in sorted(result['sets'].items()) if k[1] == 'SET_PART_LIST']
    result.pop('sets')
    result.pop('set_lines')
    result['case1'] = dict(result['case1'])
    result['case1']['unmatched_count'] = len(result['case1'].pop('unmatched'))
    return result


def checkpoint():
    dest = Path(__file__).with_name('independent-checkpoint01.json')
    require(not dest.exists(), 'checkpoint_exists')
    require(sha(Path(__file__).with_name('PROTOCOL.md')) == PROTOCOL_SHA, 'protocol_pin')
    addendum_sha = '7433fb5d5b4e151eb70df22b1c40825939d3868842af0ee0ff816c830f236b94'
    require(sha(Path(__file__).with_name('THERMAL-DUPLICATE-ADDENDUM.md')) == addendum_sha, 'thermal_addendum_pin')
    started = time.time()
    tests = selftests()
    before = check_pins()
    try:
        result = safe_checkpoint(model_join())
    except Exception as problem:
        error = problem if isinstance(problem, CheckError) else CheckError('unexpected_runtime_exception')
        failures = sorted(Path(__file__).parent.glob('independent-failed[0-9][0-9].json'))
        failure_dest = Path(__file__).with_name(f'independent-failed{len(failures) + 1:02d}.json')
        code = Path(__file__).read_bytes()
        failure = {'status': 'FAIL', 'code': error.code, 'src': error.src, 'line': error.line,
                   'inputs_before': before, 'inputs_after': check_pins(), 'streams': RUN_PROGRESS,
                   'selftests': tests, 'verifier_sha256': hashlib.sha256(code).hexdigest(),
                   'core_sha256': hashlib.sha256(code.split(b'# INDEPENDENT_CORE_END')[0]).hexdigest(),
                   'elapsed_seconds': time.time() - started,
                   'partial_stream_hashes': 'Not retained; EOF streams have full uncompressed hashes.',
                   'checkpoint_created': False}
        with failure_dest.open('x') as f:
            json.dump(failure, f, indent=2, sort_keys=True, allow_nan=False)
            f.write('\n')
        raise error from None
    after = check_pins()
    require(before == after, 'input_changed')
    code = Path(__file__).read_bytes()
    receipt = {'status': 'PASS', 'selftests': tests, 'inputs_before': before, 'inputs_after': after,
               'protocol_sha256': PROTOCOL_SHA, 'verifier_sha256': hashlib.sha256(code).hexdigest(),
               'thermal_addendum_sha256': addendum_sha,
               'core_sha256': hashlib.sha256(code.split(b'# INDEPENDENT_CORE_END')[0]).hexdigest(),
               'elapsed_seconds': time.time() - started,
               'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024),
               'python': sys.version.split()[0], 'numpy': np.__version__, 'command': sys.argv,
               'interpretation': 'Independent numeric input joins only; no solver execution or physical accuracy inference.'}
    require(receipt['peak_rss_bytes'] <= 768 * 1024 * 1024, 'memory_cap_exceeded')
    with dest.open('x') as f:
        json.dump({'receipt': receipt, 'result': result}, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
    return {'status': 'PASS', 'checkpoint_sha256': sha(dest), 'selftest_count': len(tests),
            'mesh': result['mesh'], 'node_count': result['node_count'], 'part_count': len(result['parts']),
            'target_count': len(result['targets']), 'case1': result['case1'],
            'plane_count': len(result['planes']), 'part_set_count': len(result['part_sets']),
            'peak_rss_bytes': receipt['peak_rss_bytes'], 'elapsed_seconds': receipt['elapsed_seconds']}


if __name__ == '__main__':
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument('--selftest', action='store_true')
        ap.add_argument('--checkpoint', action='store_true')
        ap.add_argument('--supplement', action='store_true')
        ap.add_argument('--verify', action='store_true')
        ap.add_argument('--output')
        ap.add_argument('--run', choices=['run05', 'run06'], default='run06')
        args = ap.parse_args()
        require(sum([args.selftest, args.checkpoint, args.supplement, args.verify]) == 1, 'choose_one_mode')
        require(args.output is None or args.verify, 'output_only_for_verification')
        output = {'status': 'PASS', 'selftests': selftests()} if args.selftest else supplement() if args.supplement else final_comparison(args.output, args.run) if args.verify else checkpoint()
        print(json.dumps(output, sort_keys=True))
        if output.get('status') == 'FAIL':
            sys.exit(1)
    except CheckError as e:
        print(json.dumps({'status': 'FAIL', 'code': e.code, 'src': e.src, 'line': e.line}, sort_keys=True))
        sys.exit(1)
