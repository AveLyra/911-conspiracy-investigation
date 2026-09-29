#!/usr/bin/env python3
"""Bounded, numeric-only released-input joins. Never invokes LS-DYNA.

This is a scoped card reader, not a general LS-DYNA parser. Unsupported
required card structure fails closed. No source text is emitted on error.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unittest
from collections import Counter
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PINS = {
    'Damage_Global_ANSYS_CaseB_4.0hr.k.gz': (5331, '982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da'),
    'G6A_CaseA_El_Delete_List.k.gz': (103872, 'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273'),
    'WTC7_CaseB_400pm.int.gz': (2702040, '51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447'),
    'discrete_mass.k.gz': (70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7'),
    'elem_thick_to-renum.k.gz': (23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59'),
    'wtc7_global_8a_no-conn-matl.k.gz': (47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d'),
}
MASTER = 'wtc7_global_8a_no-conn-matl.k.gz'
OUTSIDE = 'elem_thick_to-renum.k.gz'
MASS = 'discrete_mass.k.gz'
THERMAL = 'WTC7_CaseB_400pm.int.gz'
DAMAGE = 'Damage_Global_ANSYS_CaseB_4.0hr.k.gz'
CASEA = 'G6A_CaseA_El_Delete_List.k.gz'
BYTE_CAP = 512 * 1024 * 1024
LINE_CAP = 16384
ID_CAP = 6000001
LIMITS = (25.01, 100.0, 200.0, 300.0)
MATERIAL_KEYWORDS = {b'*MAT_PIECEWISE_LINEAR_PLASTICITY', b'*MAT_ELASTIC_VISCOPLASTIC_THERMAL',
                     b'*MAT_RIGID', b'*MAT_SPRING_NONLINEAR_ELASTIC', b'*MAT_ELASTIC',
                     b'*MAT_PLASTICITY_COMPRESSION_TENSION'}
DELETE_KEYWORDS = {b'*DELETE_ELEMENT_SHELL', b'*DELETE_ELEMENT_BEAM'}


class CardError(Exception):
    def __init__(self, code):
        self.code = code


def require(condition, code):
    if not condition:
        raise CardError(code)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def fields(line, widths):
    """Preserve empty CSV/fixed fields, including explicit all-blank cards."""
    if b',' in line:
        return [v.strip() for v in line.strip(b'\r\n').split(b',')]
    values, pos = [], 0
    for width in widths:
        values.append(line[pos:pos + width].strip())
        pos += width
    require(not line[pos:].strip(), 'fixed_card_trailing_data')
    return values


def number(value, default=None):
    if not value:
        return default
    try:
        result = float(value.replace(b'D', b'E').replace(b'd', b'e'))
    except (ValueError, OverflowError):
        raise CardError('non_numeric_field') from None
    require(math.isfinite(result), 'non_finite_field')
    return result


def integer(value, default=None):
    v = number(value, default)
    if v is None:
        return None
    require(int(v) == v, 'non_integral_id')
    return int(v)


def id_card(line, width, count):
    return [integer(v, 0) for v in fields(line, [width] * count)]


def values_card(line, width, count):
    return [number(v) for v in fields(line, [width] * count)]


def vertex_ids(kind, ids):
    # Beams' third node is an orientation node, not a physical endpoint.
    if kind in ('beam', 'discrete'):
        return ids[2:4]
    if kind == 'shell':
        return ids[2:6]
    return ids[2:10]


def summary(values):
    if not len(values):
        return {'count': 0, 'min': None, 'max': None, 'le_25_01': 0,
                'gt_100': 0, 'gt_200': 0, 'gt_300': 0}
    return {'count': int(len(values)), 'min': float(np.min(values)),
            'max': float(np.max(values)), 'le_25_01': int(np.sum(values <= LIMITS[0])),
            'gt_100': int(np.sum(values > LIMITS[1])),
            'gt_200': int(np.sum(values > LIMITS[2])),
            'gt_300': int(np.sum(values > LIMITS[3]))}


def bounds(coords):
    return None if not len(coords) else [coords.min(axis=0).tolist(), coords.max(axis=0).tolist()]


class Reader:
    def __init__(self):
        self.receipts = {}
        self.name, self.line = None, 0

    def lines(self, name):
        self.name, self.line = name, 0
        path = SOURCE / name
        require((path.stat().st_size, digest(path)) == PINS[name], 'source_pin_before')
        receipt = {'compressed_bytes': path.stat().st_size, 'compressed_sha256': PINS[name][1],
                   'eof': False, 'uncompressed_bytes': 0, 'lines': 0}
        self.receipts[name] = receipt
        h = hashlib.sha256()
        with gzip.open(path, 'rb') as stream:
            while True:
                raw = stream.readline(LINE_CAP + 1)
                if not raw:
                    break
                self.line += 1
                receipt['lines'] = self.line
                receipt['uncompressed_bytes'] += len(raw)
                require(len(raw) <= LINE_CAP, 'line_cap')
                require(receipt['uncompressed_bytes'] <= BYTE_CAP, 'byte_cap')
                h.update(raw)
                yield self.line, raw.rstrip(b'\r\n')
        require((path.stat().st_size, digest(path)) == PINS[name], 'source_pin_after')
        receipt.update(eof=True, uncompressed_sha256=h.hexdigest(), pin_after=True)


class MemberMap:
    def __init__(self, cap=ID_CAP):
        self.cap = cap
        self.xyz = np.full((cap, 3), np.nan)
        self.present = np.zeros(cap, dtype=bool)
        self.ts = np.full(cap, np.nan)
        self.ts_hi = np.full(cap, np.nan)
        self.thermal_counts = np.zeros(cap, dtype=np.uint16)
        self.seen = {k: np.zeros(cap, dtype=bool) for k in ('shell', 'beam', 'solid', 'discrete')}
        self.counts, self.node_counts = {}, {}
        self.parts, self.partsets, self.planes = {}, {}, []
        self.partnodes, self.partbbox, self.part_elements = {}, {}, {}
        self.batch, self.targets, self.casea_parts = [], [], {}
        self.discrete_candidates = []
        self.target_ids, self.casea_ids = {}, set()
        self.found = {'shell': set(), 'beam': set(), 'casea': set()}
        self.diagnostics = Counter()
        self.includes, self.transforms, self.active_delete = [], [], []
        self.materials, self.sections = {}, set()

    def check_id(self, value):
        require(0 < value < self.cap, 'id_outside_declared_cap')

    def node(self, name, line):
        row = fields(line, [8, 16, 16, 16, 8, 8])
        nid = integer(row[0]); self.check_id(nid)
        xyz = [number(v) for v in row[1:4]]
        require(all(v is not None for v in xyz), 'node_missing_coordinate')
        if self.present[nid]:
            self.diagnostics['duplicate_nodes'] += 1
            require(np.array_equal(self.xyz[nid], xyz), 'conflicting_duplicate_node')
        else:
            self.xyz[nid] = xyz
            self.present[nid] = True
        self.node_counts[name] = self.node_counts.get(name, 0) + 1

    def thermal(self, reader):
        rows, curves, bases, coefficients = 0, Counter(), Counter(), Counter()
        active, ended = False, False
        repeated = 0
        for _, raw in reader.lines(THERMAL):
            s = raw.strip()
            if s.startswith(b'$') or not s:
                continue
            require(not ended, 'noncomment_data_after_end')
            if s.startswith(b'*'):
                active = s == b'*LOAD_THERMAL_VARIABLE_NODE'
                ended = s == b'*END'
                continue
            if active:
                row = fields(raw, [10] * 4)
                require(len(row) == 4, 'thermal_field_count')
                nid = integer(row[0]); self.check_id(nid)
                vals = [number(v) for v in row[1:]]
                require(all(v is not None for v in vals), 'thermal_missing_field')
                require(vals[1] == 0 and vals[2] == 2, 'unsupported_thermal_curve_or_base')
                if np.isfinite(self.ts[nid]):
                    repeated += 1
                    self.ts[nid] = min(self.ts[nid], vals[0])
                    self.ts_hi[nid] = max(self.ts_hi[nid], vals[0])
                else:
                    self.ts[nid] = vals[0]
                    self.ts_hi[nid] = vals[0]
                require(self.thermal_counts[nid] < 65535, 'thermal_repeat_count_cap')
                self.thermal_counts[nid] += 1
                bases[vals[1]] += 1; curves[integer(row[3])] += 1
                coefficients[vals[0]] += 1
                rows += 1
        nodes = np.flatnonzero(np.isfinite(self.ts))
        conflict_ids = nodes[self.ts[nodes] != self.ts_hi[nodes]]
        sample = sorted(map(int, conflict_ids), key=lambda n: (-(self.ts_hi[n] - self.ts[n]), n))[:10]
        row_summary = {'count': rows, 'min': min(coefficients), 'max': max(coefficients),
            'le_25_01': sum(n for v, n in coefficients.items() if v <= 25.01),
            'gt_100': sum(n for v, n in coefficients.items() if v > 100),
            'gt_200': sum(n for v, n in coefficients.items() if v > 200),
            'gt_300': sum(n for v, n in coefficients.items() if v > 300)}
        return {'rows': rows, 'curves': dict(curves), 'bases': dict(bases),
                'repeated_rows_beyond_unique': repeated, 'conflicting_node_count': int(len(conflict_ids)),
                'nodes_with_repeated_rows': int(np.sum(self.thermal_counts > 1)),
                'max_rows_per_node': int(self.thermal_counts.max()),
                'row_assigned_TS': row_summary, 'unique_node_assigned_TS_envelope': self.thermal_summary(nodes),
                'largest_supplied_ranges': [{'nid': n, 'min': float(self.ts[n]), 'max': float(self.ts_hi[n]),
                    'rows': int(self.thermal_counts[n])} for n in sample],
                'duplicate_solver_semantics': 'unresolved_no_first_last_sum_or_average_selected'}

    def thermal_summary(self, nodes):
        lo, hi = self.ts[nodes], self.ts_hi[nodes]
        consistent = lo == hi
        return {'min_assignment_per_node': summary(lo), 'max_assignment_per_node': summary(hi),
                'unambiguous_nodes_only': summary(lo[consistent]),
                'conflicting_nodes': int(np.sum(~consistent))}

    def deletion(self, reader, name):
        sets, key, header, ended = {}, None, False, False
        for lineno, raw in reader.lines(name):
            s = raw.strip()
            if s.startswith(b'$') or not s:
                continue
            require(not ended, 'noncomment_data_after_end')
            if s.startswith(b'*'):
                ended = s == b'*END'
                key = {b'*SET_SHELL_LIST': 'shell', b'*SET_BEAM': 'beam',
                       b'*SET_BEAM_LIST': 'beam'}.get(s)
                header = True
                continue
            if key:
                row = id_card(raw, 10, 8)
                if header:
                    require(key not in sets, 'repeated_deletion_set_kind')
                    require(row[0] == (2 if name == DAMAGE else 1), 'unexpected_deletion_set_id')
                    sets[key] = {'set_id': row[0], 'header_line': lineno, 'ids': []}
                    header = False
                else:
                    sets[key]['ids'].extend(v for v in row if v)
        for kind, value in sets.items():
            require(len(value['ids']) == len(set(value['ids'])), 'duplicate_deletion_id')
            for eid in value['ids']:
                self.check_id(eid)
            if name == DAMAGE:
                self.target_ids[kind] = set(value['ids'])
            else:
                require(kind == 'shell', 'casea_unexpected_kind')
                self.casea_ids = set(value['ids'])
        return sets

    def element(self, name, lineno, kind, row, offset):
        require(len(row) == {'beam': 5, 'discrete': 4, 'shell': 6, 'solid': 10}[kind],
                'unsupported_element_card_arity')
        eid, pid = row[:2]
        self.check_id(eid)
        nodes = vertex_ids(kind, row)
        require(all(v > 0 for v in nodes), 'nonpositive_element_node')
        for nid in nodes:
            self.check_id(nid)
        if self.seen[kind][eid]:
            self.diagnostics['duplicate_' + kind + '_ids'] += 1
            raise CardError('duplicate_element_id')
        self.seen[kind][eid] = True
        key = name + ':' + kind
        self.counts[key] = self.counts.get(key, 0) + 1
        if kind == 'shell':
            self.diagnostics['triangle_shells' if nodes[2] == nodes[3] else 'quad_shells'] += 1
        effective = pid + offset
        if eid in self.target_ids.get(kind, set()):
            self.found[kind].add(eid)
            self.targets.append({'source': name, 'line': lineno, 'kind': kind, 'eid': eid,
                                 'original_pid': pid, 'pid': effective, 'node_ids': list(dict.fromkeys(nodes)),
                                 'orientation_node': row[4] if kind == 'beam' else None})
        elif kind == 'discrete' and eid in self.target_ids.get('beam', set()):
            self.discrete_candidates.append({'source': name, 'line': lineno, 'kind': kind, 'eid': eid,
                'original_pid': pid, 'pid': effective, 'node_ids': list(dict.fromkeys(nodes)),
                'orientation_node': None, 'selection_status': 'numeric_set2_beam_id_cross_family_candidate'})
        in_casea = kind == 'shell' and eid in self.casea_ids
        if in_casea:
            self.found['casea'].add(eid)
        self.batch.append((effective, kind, nodes, in_casea))
        if len(self.batch) >= 20000:
            self.flush()

    @staticmethod
    def merge_bbox(target, pid, bbox):
        if bbox is None:
            return
        a = np.asarray(bbox)
        if pid not in target:
            # Aggregate ownership must not alias a source part's cached bounds.
            target[pid] = a.copy()
        else:
            target[pid][0] = np.minimum(target[pid][0], a[0])
            target[pid][1] = np.maximum(target[pid][1], a[1])

    def flush(self):
        groups = {}
        for pid, kind, nodes, casea in self.batch:
            group = groups.setdefault(pid, {'nodes': [], 'casea': [], 'counts': Counter()})
            group['nodes'].extend(nodes)
            if casea:
                group['casea'].extend(nodes)
                self.casea_parts.setdefault(pid, {'elements': 0})['elements'] += 1
            group['counts'][kind] += 1
        for pid, group in groups.items():
            nodes = np.unique(group['nodes'])
            absent = nodes[~self.present[nodes]]
            require(not len(absent), 'element_node_not_defined_before_use')
            self.merge_bbox(self.partbbox, pid, bounds(self.xyz[nodes]))
            self.part_elements.setdefault(pid, Counter()).update(group['counts'])
            therm = nodes[np.isfinite(self.ts[nodes])]
            self.partnodes.setdefault(pid, set()).update(map(int, therm))
            if group['casea']:
                bbox = bounds(self.xyz[np.unique(group['casea'])])
                obj = self.casea_parts[pid]
                if 'bounds' not in obj:
                    obj['bounds'] = bbox
                else:
                    obj['bounds'] = [np.minimum(obj['bounds'][0], bbox[0]).tolist(),
                                     np.maximum(obj['bounds'][1], bbox[1]).tolist()]
        self.batch.clear()

    def metadata(self, name, keyword, start, cards, offset):
        if keyword == b'*PART':
            require(len(cards) >= 2, 'part_cards_missing')
            row = id_card(cards[1][1], 10, 8)
            pid = row[0] + offset
            require(pid not in self.parts, 'duplicate_part_id')
            self.parts[pid] = {'source': name, 'line': cards[1][0], 'original_pid': row[0],
                               'pid': pid, 'original_section_id': row[1], 'original_material_id': row[2],
                               'section_id': row[1] + offset if row[1] else 0,
                               'material_id': row[2] + offset if row[2] else 0,
                               'heading_sha256': hashlib.sha256(cards[0][1]).hexdigest()}
        elif keyword == b'*SET_PART_LIST':
            require(cards, 'set_header_missing')
            sid = integer(fields(cards[0][1], [10] * 8)[0])
            require(sid not in self.partsets, 'duplicate_partset_id')
            ids = []
            for _, raw in cards[1:]:
                ids.extend(v + offset for v in id_card(raw, 10, 8) if v)
            self.partsets[sid] = {'source': name, 'line': start, 'part_ids': ids}
        elif keyword == b'*DATABASE_CROSS_SECTION_PLANE_ID':
            require(len(cards) == 3, 'plane_card_count')
            title = cards[0][1]
            # Allowlist only a numeric column label; arbitrary source title is hashed.
            label_fields = fields(title, [10, 70])
            label = label_fields[1].strip() if len(label_fields) == 2 else b''
            match = re.fullmatch(rb'Col(?:umn)?\s*0*(\d+)\s+X-Sect', label, re.I)
            row = values_card(cards[1][1], 10, 8)
            self.planes.append({'source': name, 'line': start,
                'heading_sha256': hashlib.sha256(title).hexdigest(),
                'column_number': int(match[1]) if match else None,
                'all_columns': label.lower() == b'all columns x-sect',
                'plane_id': integer(label_fields[0]),
                'psid': integer(fields(cards[1][1], [10] * 8)[0], 0), 'plane_card': row,
                'second_plane_card': values_card(cards[2][1], 10, 8)})
        elif keyword in (b'*INCLUDE', b'*INCLUDE_TRANSFORM'):
            require(cards, 'include_missing')
            bare = cards[0][1].strip().decode('ascii') + '.gz'
            require(bare in PINS, 'include_not_allowlisted')
            self.includes.append({'source': name, 'line': start, 'included': bare,
                                  'kind': keyword.decode('ascii')})
            if keyword == b'*INCLUDE_TRANSFORM':
                require(len(cards) == 5, 'transform_card_count')
                rows = [values_card(c[1], 10, 8) for c in cards[1:]]
                require(rows[0][:7] == [0, 0, 1000, 1000, 0, 0, 0], 'unsupported_id_transform')
                require(rows[1][0] == 1000, 'unsupported_section_offset')
                require(rows[2][:3] == [1, 1, 1], 'unsupported_scale')
                require((rows[3][0] or 0) == 0, 'unsupported_geometry_transform')
                require(bare == OUTSIDE, 'unexpected_transformed_include')
                self.transforms.append({'source': name, 'line': start, 'cards': rows,
                                        'coordinate_transform': 'identity',
                                        'FCTTEM_caveat': 'numeric_1_in_character_conversion_flag_field'})
        elif keyword.startswith(b'*MAT_') and cards:
            require(keyword in MATERIAL_KEYWORDS, 'unsupported_material_keyword')
            mid = integer(fields(cards[0][1], [10] * 8)[0])
            if mid is not None:
                require(mid + offset not in self.materials, 'duplicate_material_id')
                self.materials[mid + offset] = keyword.decode('ascii')
        elif keyword.startswith(b'*SECTION_') and cards:
            sid = integer(fields(cards[0][1], [10] * 8)[0])
            if sid is not None:
                self.sections.add(sid + offset)

    def mesh(self, reader, name, offset=0):
        keyword, start, cards, pending = b'', 0, [], None
        data_lines = Counter()
        keep, ended = False, False
        for lineno, raw in reader.lines(name):
            s = raw.strip()
            if s.startswith(b'$'):
                continue
            require(not ended or not s, 'noncomment_data_after_end')
            if s.startswith(b'*'):
                require(pending is None, 'shell_missing_thickness_card')
                if keep:
                    self.metadata(name, keyword, start, cards, offset)
                keyword, start, cards = s.upper(), lineno, []
                if keyword.startswith(b'*ELEMENT_'):
                    require(keyword in (b'*ELEMENT_SHELL_THICKNESS', b'*ELEMENT_BEAM',
                            b'*ELEMENT_SOLID', b'*ELEMENT_DISCRETE'), 'unsupported_element_variant')
                if keyword.startswith(b'*NODE'):
                    require(keyword == b'*NODE', 'unsupported_node_variant')
                if keyword.startswith(b'*PART'):
                    require(keyword == b'*PART', 'unsupported_part_variant')
                if keyword.startswith(b'*SET_PART'):
                    require(keyword == b'*SET_PART_LIST', 'unsupported_partset_variant')
                if keyword.startswith(b'*KEYWORD'):
                    require(keyword == b'*KEYWORD', 'unsupported_global_format')
                ended = keyword == b'*END'
                keep = keyword in (b'*PART', b'*SET_PART_LIST', b'*DATABASE_CROSS_SECTION_PLANE_ID',
                                   b'*INCLUDE', b'*INCLUDE_TRANSFORM') or keyword.startswith((b'*MAT_', b'*SECTION_'))
                if keyword.startswith(b'*DELETE_ELEMENT'):
                    require(keyword in DELETE_KEYWORDS, 'unsupported_delete_keyword')
                    self.active_delete.append({'source': name, 'line': lineno,
                                               'keyword': keyword.decode('ascii')})
                continue
            if keep:
                cards.append((lineno, raw))
                require(len(cards) < 10000, 'metadata_card_cap')
            if not s:
                continue
            if keyword == b'*NODE':
                self.node(name, raw)
            elif keyword == b'*ELEMENT_SHELL_THICKNESS':
                data_lines['shell'] += 1
                if pending is None:
                    row = id_card(raw, 8, 10)
                    require(len(row) >= 6 and not any(row[6:]), 'unsupported_shell_extra_nodes')
                    pending = (lineno, row[:6])
                else:
                    row = values_card(raw, 16, 5)
                    require(len(row) >= 4 and all(v is not None and v >= 0 for v in row[:4]), 'shell_thickness_invalid')
                    self.element(name, pending[0], 'shell', pending[1], offset)
                    pending = None
            elif keyword in (b'*ELEMENT_BEAM', b'*ELEMENT_SOLID', b'*ELEMENT_DISCRETE'):
                kind = {b'*ELEMENT_BEAM': 'beam', b'*ELEMENT_SOLID': 'solid', b'*ELEMENT_DISCRETE': 'discrete'}[keyword]
                data_lines[kind] += 1
                row = fields(raw, [8] * 5 + [16, 8, 16] if kind == 'discrete' else [8] * 10)
                take = 10 if kind == 'solid' else (5 if kind == 'beam' else 4)
                ids = [integer(v, 0) for v in row[:take]]
                self.element(name, lineno, kind, ids, offset)
        require(pending is None, 'shell_missing_thickness_eof')
        if keep:
            self.metadata(name, keyword, start, cards, offset)
        self.flush()
        return dict(data_lines)

    def results(self):
        thermal_ids = np.flatnonzero(np.isfinite(self.ts))
        linkage = np.zeros(self.cap, dtype=np.uint16)
        part_reports = []
        for pid, elements in sorted(self.part_elements.items()):
            nodes = np.array(sorted(self.partnodes.get(pid, set())), dtype=np.int64)
            linkage[nodes] += 1
            part = self.parts.get(pid)
            part_reports.append({'pid': pid, 'definition': part, 'elements': dict(elements),
                'geometry_bounds': self.partbbox[pid].tolist(),
                'assigned_TS_envelope': self.thermal_summary(nodes), 'thermal_node_bounds': bounds(self.xyz[nodes]),
                'material_keyword': self.materials.get(part['material_id']) if part else None,
                'section_defined': part['section_id'] in self.sections if part else False})
        for target in self.targets + self.discrete_candidates:
            nodes = np.asarray(target['node_ids'])
            valid = self.present[nodes]
            target.update(definition=self.parts.get(target['pid']),
                missing_nodes=nodes[~valid].tolist(),
                node_coordinates=self.xyz[nodes[valid]].tolist(),
                centroid=self.xyz[nodes[valid]].mean(axis=0).tolist() if valid.all() else None,
                bounds=bounds(self.xyz[nodes[valid]]))
        planes = []
        for plane in self.planes:
            partset = self.partsets.get(plane['psid'])
            members = partset['part_ids'] if partset else (list(self.parts) if plane['psid'] == 0 else [])
            nodes = set()
            bbox = {}
            for pid in members:
                nodes.update(self.partnodes.get(pid, set()))
                self.merge_bbox(bbox, 0, self.partbbox.get(pid))
            a = np.array(sorted(nodes), dtype=np.int64)
            high = a[self.ts_hi[a] > 300][:10]
            planes.append({**plane, 'partset': partset, 'missing_part_ids': sorted(set(members) - set(self.parts)),
                'assigned_TS_envelope': self.thermal_summary(a), 'thermal_node_bounds': bounds(self.xyz[a]),
                'high_TS_node_examples': [{'nid': int(n), 'min': float(self.ts[n]), 'max': float(self.ts_hi[n]),
                                          'rows': int(self.thermal_counts[n])} for n in high],
                'member_geometry_bounds': bbox[0].tolist() if bbox else None,
                'scope': 'entire_referenced_part_set_not_only_plane_intersection'})
        return {'node_rows': self.node_counts, 'unique_nodes': int(self.present.sum()),
            'element_records': self.counts, 'diagnostics': dict(self.diagnostics),
            'part_definition_count': len(self.parts), 'partset_count': len(self.partsets),
            'plane_count': len(self.planes), 'includes': self.includes, 'transforms': self.transforms,
            'active_delete_cards': self.active_delete,
            'thermal_join': {'no_geometry': int((~self.present[thermal_ids]).sum()),
                'no_mesh_incidence': int((linkage[thermal_ids] == 0).sum()),
                'multiple_part_incidence': int((linkage[thermal_ids] > 1).sum()),
                'part_incidence_sum': int(linkage[thermal_ids].sum()),
                'max_part_incidence': int(linkage[thermal_ids].max()),
                'missing_assignments_mean': 'unknown_not_ambient'},
            'damage_set2': {'status': 'unused_candidate_list_not_active_deletion',
                'matched': {k: len(self.found[k]) for k in ('shell', 'beam')},
                'unmatched': {k: sorted(self.target_ids[k] - self.found[k]) for k in ('shell', 'beam')},
                'elements': sorted(self.targets, key=lambda t: (t['kind'], t['eid']))},
            'set2_beam_id_discrete_candidates': {'status': 'numeric_cross_family_matches_delete_semantics_unresolved',
                'count': len(self.discrete_candidates),
                'elements': sorted(self.discrete_candidates, key=lambda t: t['eid'])},
            'casea_set1': {'status': 'unreferenced_purpose_unestablished',
                'matched': len(self.found['casea']), 'unmatched': sorted(self.casea_ids - self.found['casea']),
                'overlap_set2_shells': sorted(self.casea_ids & self.target_ids['shell']),
                'parts': self.casea_parts}, 'parts': part_reports, 'column_diagnostics': planes}


class Controls(unittest.TestCase):
    class SyntheticReader:
        def __init__(self, lines):
            self.cards = lines

        def lines(self, name):
            yield from enumerate(self.cards, 1)

    def test_fixed_and_free_fields(self):
        fixed = b'%8d%16.8f%16.8f%16.8f%8d%8d' % (5, -80, -50, -95.4786, 7, 7)
        m = MemberMap(20); m.node('synthetic', fixed)
        m.node('synthetic', b'6,-80,-50,-95.4786,7,7')
        np.testing.assert_array_equal(m.xyz[5], m.xyz[6])

    def test_blanks(self):
        self.assertEqual(values_card(b',,,,,,,', 10, 8), [None] * 8)

    def test_shell_two_cards_triangle(self):
        conn = id_card(b'1,2,3,4,5,5', 8, 6)
        thick = values_card(b'0.1,0.1,0.1,0.1', 16, 4)
        self.assertEqual(len(set(vertex_ids('shell', conn))), 3)
        self.assertEqual(thick, [0.1] * 4)
        with self.assertRaises(CardError):
            id_card(b'0.1,0.1,0.1,0.1', 8, 6)

    def test_orientation_offset_shared(self):
        m = MemberMap(20)
        for nid in (1, 2, 3):
            m.node('synthetic', f'{nid},{nid},0,0'.encode())
        m.ts[1:3] = [25, 300]
        m.element('synthetic', 1, 'beam', [1, 2, 1, 2, 19], 1000)
        m.element('synthetic', 2, 'beam', [2, 3, 1, 2, 19], 1000)
        m.flush()
        self.assertEqual(m.partnodes[1002], {1, 2})
        self.assertEqual(m.partnodes[1003], {1, 2})
        self.assertEqual(m.partbbox[1002].tolist(), [[1, 0, 0], [2, 0, 0]])

    def test_duplicate_missing_inactive(self):
        m = MemberMap(20)
        m.element('synthetic', 1, 'beam', [1, 2, 1, 2, 19], 0)
        with self.assertRaises(CardError):
            m.element('synthetic', 2, 'beam', [1, 2, 1, 2, 19], 0)
        with self.assertRaises(CardError):
            m.flush()
        self.assertEqual(m.active_delete, [])

    def test_actual_card_state_and_inactive_list(self):
        m = MemberMap(20)
        cards = [b'*NODE', b'1,1,0,0', b'2,2,0,0', b'3,3,0,0',
                 b'*ELEMENT_SHELL_THICKNESS', b'1,2,1,2,3,3', b'0,0,0,0',
                 b'$*DELETE_ELEMENT_SHELL', b'$2', b'*END']
        result = m.mesh(self.SyntheticReader(cards), 'synthetic')
        self.assertEqual(result['shell'], 2)
        self.assertEqual(m.counts['synthetic:shell'], 1)
        self.assertEqual(m.diagnostics['triangle_shells'], 1)
        self.assertEqual(m.active_delete, [])

    def test_orphan_thickness_and_unsupported_variant(self):
        for cards in ([b'*ELEMENT_SHELL_THICKNESS', b'1,2,3,4,5,5', b'*END'],
                      [b'*ELEMENT_BEAM_OFFSET']):
            with self.assertRaises(CardError):
                MemberMap(20).mesh(self.SyntheticReader(cards), 'synthetic')

    def test_transform_and_plane_blanks(self):
        m = MemberMap(20)
        cards = [(1, b'elem_thick_to-renum.k'), (2, b'0,0,1000,1000,0,0,0'),
                 (3, b'1000'), (4, b'1,1,1,1,0'), (5, b'0')]
        m.metadata('synthetic', b'*INCLUDE_TRANSFORM', 1, cards, 0)
        self.assertEqual(m.transforms[0]['coordinate_transform'], 'identity')
        m.metadata('synthetic', b'*DATABASE_CROSS_SECTION_PLANE_ID', 6,
                   [(7, b'        79Col 79 X-Sect'), (8, b'179,0,0,-64.9,0,0,90.4748'),
                    (9, b',,,,,,,')], 0)
        self.assertEqual(m.planes[0]['column_number'], 79)
        self.assertEqual(m.planes[0]['psid'], 179)
        self.assertEqual(m.planes[0]['second_plane_card'], [None] * 8)

    def test_thermal_threshold_boundaries(self):
        self.assertEqual(summary(np.array([25.01, 100, 200, 300])),
                         {'count': 4, 'min': 25.01, 'max': 300.0, 'le_25_01': 1,
                          'gt_100': 2, 'gt_200': 1, 'gt_300': 0})

    def test_short_csv_elements_and_two_card_solid_rejected(self):
        for keyword, raw in ((b'*ELEMENT_SOLID', b'20,2'), (b'*ELEMENT_BEAM', b'1,2'),
                             (b'*ELEMENT_DISCRETE', b'1,2')):
            with self.assertRaises(CardError):
                MemberMap(30).mesh(self.SyntheticReader([keyword, raw]), 'synthetic')

    def test_no_unallowlisted_text_export(self):
        with self.assertRaises(CardError):
            MemberMap(30).metadata('synthetic', b'*MAT_SYNTHETIC_UNALLOWLISTED_TEXT',
                                   1, [(2, b'1')], 0)
        with self.assertRaises(CardError):
            MemberMap(30).mesh(self.SyntheticReader([b'*DELETE_ELEMENT_SYNTHETIC_UNALLOWLISTED_TEXT']), 'synthetic')

    def test_standard_material124_mid(self):
        m = MemberMap(30)
        m.metadata('synthetic', b'*MAT_PLASTICITY_COMPRESSION_TENSION', 1,
                   [(2, b'44,1,2,0.3,0,0,0,0')], 0)
        self.assertEqual(m.materials[44], '*MAT_PLASTICITY_COMPRESSION_TENSION')

    def test_cross_family_candidate_not_explicit_beam(self):
        m = MemberMap(30); m.target_ids['beam'] = {1}
        for n in [1, 2]:
            m.node('synthetic', f'{n},{n},0,0'.encode())
        m.element('synthetic', 3, 'discrete', [1, 2, 1, 2], 0); m.flush()
        self.assertEqual(m.found['beam'], set())
        self.assertEqual(m.targets, [])
        self.assertEqual(m.discrete_candidates[0]['kind'], 'discrete')
        self.assertEqual(m.discrete_candidates[0]['eid'], 1)

    def test_aggregate_bounds_do_not_mutate_source_part(self):
        first = np.array([[1., 2., 3.], [4., 5., 6.]])
        second = np.array([[-10., -20., -30.], [40., 50., 60.]])
        original = first.copy()
        union = {}
        MemberMap.merge_bbox(union, 0, first)
        MemberMap.merge_bbox(union, 0, second)
        np.testing.assert_array_equal(first, original)
        alone = {}; MemberMap.merge_bbox(alone, 0, first)
        np.testing.assert_array_equal(alone[0], original)
        self.assertFalse(np.shares_memory(union[0], first))

    def test_fractional_partset_rejected(self):
        with self.assertRaises(CardError):
            MemberMap(30).metadata('synthetic', b'*DATABASE_CROSS_SECTION_PLANE_ID', 1,
                [(2, b'79,Col 79 X-Sect'), (3, b'179.9,0,0,-1,0,0,1'), (4, b',,,,,,,')], 0)

    def test_repeated_set_and_post_end_rejected(self):
        cards = [b'*SET_SHELL_LIST', b'2', b'4', b'*SET_SHELL_LIST', b'2', b'5']
        with self.assertRaises(CardError):
            MemberMap(30).deletion(self.SyntheticReader(cards), DAMAGE)
        with self.assertRaises(CardError):
            MemberMap(30).thermal(self.SyntheticReader([b'*END', b'*LOAD_THERMAL_VARIABLE_NODE']))
        with self.assertRaises(CardError):
            MemberMap(30).deletion(self.SyntheticReader([b'*END', b'*SET_SHELL_LIST']), DAMAGE)

    def test_repeated_equal_and_conflicting_thermal(self):
        r = self.SyntheticReader([b'*LOAD_THERMAL_VARIABLE_NODE', b'1,25,0,2', b'1,25,0,2'])
        obj = MemberMap(30).thermal(r)
        self.assertEqual(obj['rows'], 2)
        self.assertEqual(obj['unique_node_assigned_TS_envelope']['min_assignment_per_node']['count'], 1)
        self.assertEqual(obj['repeated_rows_beyond_unique'], 1)
        conflict = MemberMap(30).thermal(self.SyntheticReader([b'*LOAD_THERMAL_VARIABLE_NODE', b'1,25,0,2', b'1,30,0,2']))
        self.assertEqual(conflict['conflicting_node_count'], 1)
        self.assertEqual(conflict['unique_node_assigned_TS_envelope']['min_assignment_per_node']['min'], 25)
        self.assertEqual(conflict['unique_node_assigned_TS_envelope']['max_assignment_per_node']['max'], 30)
        self.assertEqual(conflict['unique_node_assigned_TS_envelope']['unambiguous_nodes_only']['count'], 0)


def run(out):
    require(out.parent.resolve() == HERE and not out.exists(), 'output_must_be_new_child')
    out.mkdir()
    receipt = {'status': 'running', 'protocol_sha256': digest(HERE / 'PROTOCOL.md'),
               'thermal_duplicate_addendum_sha256': digest(HERE / 'THERMAL-DUPLICATE-ADDENDUM.md'),
               'cross_family_addendum_sha256': digest(HERE / 'CROSS-FAMILY-ADDENDUM.md'),
               'producer_sha256': digest(Path(__file__)), 'python': sys.version.split()[0],
               'numpy': np.__version__, 'byte_cap_per_file': BYTE_CAP, 'line_cap': LINE_CAP,
               'id_cap_exclusive': ID_CAP, 'scope': 'local_input_joins_no_solver_or_causal_finding'}
    reader = Reader()
    try:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        result = unittest.TestResult(); suite.run(result)
        receipt['controls'] = {'run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors)}
        require(result.wasSuccessful(), 'synthetic_controls_failed')
        m = MemberMap()
        receipt['damage_sets'] = m.deletion(reader, DAMAGE)
        # Do not dump the 45k Case A source IDs; retain counts and matched aggregate.
        ca = m.deletion(reader, CASEA)
        receipt['casea_sets'] = {k: {a: b for a, b in v.items() if a != 'ids'} | {'count': len(v['ids'])} for k, v in ca.items()}
        receipt['thermal'] = m.thermal(reader)
        print('thermal_and_candidate_lists_complete', flush=True)
        receipt['data_lines'] = {}
        for name, offset in ((MASTER, 0), (OUTSIDE, 1000), (MASS, 0)):
            receipt['data_lines'][name] = m.mesh(reader, name, offset)
            print('mesh_file_complete:' + name, flush=True)
        require(len(m.transforms) == 1, 'transform_not_verified')
        expected = {(MASTER, OUTSIDE, '*INCLUDE_TRANSFORM'), (MASTER, MASS, '*INCLUDE'),
                    (MASTER, THERMAL, '*INCLUDE')}
        actual = [(v['source'], v['included'], v['kind']) for v in m.includes]
        require(len(actual) == 3 and set(actual) == expected, 'active_include_graph_mismatch')
        require(not m.active_delete, 'active_delete_invalidates_unused_status')
        require(len({p['plane_id'] for p in m.planes}) == len(m.planes), 'duplicate_plane_id')
        payload = m.results()
        (out / 'member-map.json').write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + '\n')
        receipt.update(status='complete', result_sha256=digest(out / 'member-map.json'))
    except Exception as exc:
        receipt.update(status='failed', error={'code': exc.code if isinstance(exc, CardError) else 'unexpected_' + type(exc).__name__,
                                              'source': reader.name, 'line': reader.line})
    receipt['sources'] = reader.receipts
    # Even a parser rejection must retain a post-read source-integrity check.
    for name, source_receipt in reader.receipts.items():
        path = SOURCE / name
        try:
            source_receipt['pin_after'] = (path.stat().st_size, digest(path)) == PINS[name]
        except Exception:
            source_receipt['pin_after'] = False
        if not source_receipt['pin_after']:
            receipt.update(status='failed', error={'code': 'source_pin_final', 'source': name, 'line': None})
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps({'status': receipt['status'], 'error': receipt.get('error')}), flush=True)
    return 0 if receipt['status'] == 'complete' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.controls:
        unittest.main(argv=[sys.argv[0]], exit=True)
    elif args.output:
        try:
            sys.exit(run(args.output.resolve()))
        except CardError as exc:
            print(json.dumps({'status': 'rejected', 'code': exc.code})); sys.exit(2)
    else:
        parser.error('choose --controls or --output')
