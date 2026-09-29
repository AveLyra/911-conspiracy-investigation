#!/usr/bin/env python3
"""Bounded direct-incidence audit, not a solver or restraint-strength model."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest

HERE = Path(__file__).resolve().parent
HELPER = HERE.parent / 'model-member-map/map_members.py'
HELPER_SHA = 'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
PROTOCOL_SHA = 'b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA
spec = importlib.util.spec_from_file_location('pinned_member_reader', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

RECOGNIZED = {
    b'*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID',
    b'*CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_ID',
    b'*CONTACT_TIED_NODES_TO_SURFACE_ID',
    b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID',
    b'*CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID',
    b'*CONTACT_TIED_SHELL_EDGE_TO_SURFACE_BEAM_OFFSET_ID',
    b'*CONTACT_TIED_SHELL_EDGE_TO_SURFACE_CONSTRAINED_OFFSET_ID',
    b'*CONTACT_TIED_NODES_TO_SURFACE_OFFSET_ID',
    b'*CONSTRAINED_NODAL_RIGID_BODY', b'*CONSTRAINED_RIGID_BODIES',
    b'*CONSTRAINED_EXTRA_NODES_NODE', b'*CONSTRAINED_EXTRA_NODES_SET',
    b'*BOUNDARY_SPC_NODE', b'*BOUNDARY_SPC_SET', b'*SET_NODE_LIST',
}
FAMILIES = (b'*CONTACT', b'*CONSTRAINED', b'*BOUNDARY')
FILES = ((m.MASTER, 0), (m.OUTSIDE, 1000), (m.MASS, 0))


class InventoryReader(m.Reader):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.family_counts = Counter()

    def lines(self, name):
        block = None
        for line, raw in super().lines(name):
            stripped = raw.strip()
            if stripped.startswith(b'*'):
                key = stripped.upper()
                block = None
                family = next((k for k in FAMILIES if key.startswith(k)), None)
                if family or key == b'*SET_NODE_LIST':
                    label = family.decode() if family else '*SET_NODE_LIST'
                    self.family_counts[label] += 1
                    block = {'source': name, 'keyword_line': line, 'family': label,
                             'keyword': key.decode() if key in RECOGNIZED else None,
                             'keyword_sha256': hashlib.sha256(key).hexdigest(),
                             'cards': [], 'heading_expected': key.endswith(b'_ID')}
                    self.blocks.append(block)
            elif block is not None and not stripped.startswith(b'$'):
                cards = block['cards']
                m.require(len(cards) < 100000, 'restraint_metadata_card_cap')
                record = {'line': line}
                if block['heading_expected'] and not cards:
                    # The textual heading is not exported or interpreted.
                    try:
                        record['numeric_id'] = m.integer(raw[:10])
                    except m.CardError:
                        record['numeric_id'] = None
                    record['heading_sha256'] = hashlib.sha256(raw).hexdigest()
                else:
                    try:
                        record['numeric_fields'] = m.values_card(raw, 10, 8)
                    except m.CardError:
                        record['unparsed_sha256'] = hashlib.sha256(raw).hexdigest()
                        record['interpretation'] = 'unparsed_not_exported'
                cards.append(record)
            yield line, raw


def element_record(source, line, kind, row, offset):
    nodes = list(m.vertex_ids(kind, row))
    return {'source': source, 'line': line, 'kind': kind, 'eid': row[0],
            'original_pid': row[1], 'pid': row[1] + offset,
            'nodes': nodes, 'orientation_node': row[4] if kind == 'beam' else None}


def shared(record, seed_nodes, seed_parts):
    if record['pid'] in seed_parts:
        return []
    return sorted(set(record['nodes']) & seed_nodes)


def select_diagnostic(mapper):
    selected = [p for p in mapper.planes if p['column_number'] == 79]
    m.require(len(selected) == 1, 'column79_diagnostic_cardinality')
    plane = selected[0]
    partset = mapper.partsets.get(plane['psid'])
    m.require(partset is not None, 'column79_partset_missing')
    m.require(partset['part_ids'] == [179], 'prior_candidate_part_mismatch')
    m.require(179 in mapper.parts, 'column79_part_definition_missing')
    return plane, partset


class SeedMap(m.MemberMap):
    def __init__(self, cap=m.ID_CAP):
        super().__init__(cap)
        self.seed_records = []
        self.constraint_fields = {}

    def node(self, name, raw):
        super().node(name, raw)
        row = m.fields(raw, [8, 16, 16, 16, 8, 8])
        nid = m.integer(row[0])
        tc = m.integer(row[4], 0) if len(row) > 4 else 0
        rc = m.integer(row[5], 0) if len(row) > 5 else 0
        if tc or rc:
            self.constraint_fields[nid] = [tc, rc]

    def element(self, name, line, kind, row, offset):
        super().element(name, line, kind, row, offset)
        if row[1] + offset == 179:
            self.seed_records.append(element_record(name, line, kind, row, offset))


class NeighborMap(m.MemberMap):
    """Second lexical pass; first full map owns coordinate/ID validation."""
    def __init__(self, seed_nodes, seed_parts):
        self.seed_nodes, self.seed_parts = set(seed_nodes), set(seed_parts)
        self.neighbors, self.orientation_only = [], []
        self.active_delete = []
        self.counts = Counter()

    def node(self, name, raw):
        pass

    def metadata(self, name, keyword, start, cards, offset):
        pass

    def flush(self):
        pass

    def element(self, name, line, kind, row, offset):
        record = element_record(name, line, kind, row, offset)
        self.counts[name + ':' + kind] += 1
        matched = shared(record, self.seed_nodes, self.seed_parts)
        if matched:
            self.neighbors.append({**record, 'matched_seed_nodes': matched})
        elif kind == 'beam' and record['pid'] not in self.seed_parts and row[4] in self.seed_nodes:
            self.orientation_only.append(record)


def coordinates(mapper, ids):
    result = []
    for nid in sorted(ids):
        mapper.check_id(nid)
        m.require(mapper.present[nid], 'selected_coordinate_missing')
        result.append({'nid': nid, 'xyz': mapper.xyz[nid].tolist(),
                       'node_constraint_fields': mapper.constraint_fields.get(nid, [0, 0])})
    return result


class Controls(unittest.TestCase):
    def test_orientation_is_not_endpoint(self):
        r = element_record('x', 1, 'beam', [7, 3, 1, 2, 9], 0)
        self.assertEqual(shared(r, {9}, {179}), [])
        self.assertEqual(r['orientation_node'], 9)

    def test_order_repeats_and_unique_match(self):
        r = element_record('x', 1, 'shell', [7, 3, 2, 1, 2, 9], 0)
        self.assertEqual(r['nodes'], [2, 1, 2, 9])
        self.assertEqual(shared(r, {1, 2}, {179}), [1, 2])

    def test_offset_preserves_node_eid_namespace(self):
        r = element_record('x', 1, 'shell', [7, 179, 1, 2, 3, 4], 1000)
        self.assertEqual((r['eid'], r['pid'], r['nodes']), (7, 1179, [1, 2, 3, 4]))
        self.assertEqual(shared(r, {1}, {179}), [1])

    def test_seed_parts_excluded(self):
        r = element_record('x', 1, 'shell', [7, 179, 1, 2, 3, 4], 0)
        self.assertEqual(shared(r, {1}, {179}), [])

    def test_coincident_ids_not_joined(self):
        c = SeedMap(20)
        c.node('x', b'1,0,0,0'); c.node('x', b'2,0,0,0')
        r = element_record('x', 1, 'discrete', [7, 3, 2, 3], 0)
        self.assertEqual(shared(r, {1}, {179}), [])

    def test_missing_coordinate_rejected(self):
        with self.assertRaises(m.CardError):
            coordinates(SeedMap(20), {1})

    def test_constraint_fields_preserved(self):
        c = SeedMap(20); c.node('x', b'1,0,0,0,7,6')
        self.assertEqual(coordinates(c, {1})[0]['node_constraint_fields'], [7, 6])

    def test_wrong_or_missing_diagnostic_rejected(self):
        c = SeedMap(20)
        with self.assertRaises(m.CardError):
            select_diagnostic(c)
        c.planes = [{'column_number': 79, 'psid': 179}]
        c.partsets = {179: {'part_ids': [178]}}
        with self.assertRaises(m.CardError):
            select_diagnostic(c)

    def test_neighbor_parser_thickness_and_orientation(self):
        c = NeighborMap({9}, {179})
        c.mesh(m.Controls.SyntheticReader([
            b'*ELEMENT_SHELL_THICKNESS', b'1,3,9,2,3,4', b'.1,.1,.1,.1',
            b'*ELEMENT_BEAM', b'2,3,1,2,9', b'*END']), 'x')
        self.assertEqual(len(c.neighbors), 1)
        self.assertEqual(len(c.orientation_only), 1)
        self.assertEqual(c.counts, {'x:shell': 1, 'x:beam': 1})

    def test_no_neighbors_and_missing_thickness(self):
        c = NeighborMap({9}, {179})
        c.mesh(m.Controls.SyntheticReader([b'*ELEMENT_DISCRETE', b'1,3,1,2', b'*END']), 'x')
        self.assertEqual(c.neighbors, [])
        with self.assertRaises(m.CardError):
            c.mesh(m.Controls.SyntheticReader([b'*ELEMENT_SHELL_THICKNESS', b'1,3,9,2,3,4', b'*END']), 'x')


def run(output):
    m.require(output.parent.resolve() == HERE and not output.exists(), 'new_unit_output_required')
    m.require(m.digest(HERE / 'PROTOCOL.md') == PROTOCOL_SHA, 'protocol_pin')
    started = time.monotonic()
    receipt = {'status': 'running', 'protocol_sha256': PROTOCOL_SHA,
               'producer_sha256': m.digest(Path(__file__)), 'helper_sha256': HELPER_SHA,
               'python': sys.version.split()[0], 'numpy': m.np.__version__,
               'scope': 'direct_node_incidence_not_residual_capacity', 'sources': {}}
    readers = []
    try:
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromTestCase(m.Controls),
            unittest.defaultTestLoader.loadTestsFromTestCase(Controls)])
        tests = unittest.TestResult(); suite.run(tests)
        receipt['controls'] = {'run': tests.testsRun, 'failures': len(tests.failures), 'errors': len(tests.errors)}
        m.require(tests.wasSuccessful(), 'controls_failed')
        seed = SeedMap(); first = InventoryReader(); readers.append(first)
        for name, offset in FILES:
            seed.mesh(first, name, offset)
            print('seed_pass_file_complete:' + name, flush=True)
        plane, partset = select_diagnostic(seed)
        m.require(len(seed.transforms) == 1, 'transform_cardinality')
        expected = {(m.MASTER, m.OUTSIDE, '*INCLUDE_TRANSFORM'),
                    (m.MASTER, m.MASS, '*INCLUDE'), (m.MASTER, m.THERMAL, '*INCLUDE')}
        actual = [(v['source'], v['included'], v['kind']) for v in seed.includes]
        m.require(len(actual) == 3 and set(actual) == expected, 'include_graph')
        m.require(not seed.active_delete, 'unexpected_active_deletion')
        nodes = {n for r in seed.seed_records for n in r['nodes']}
        m.require(nodes, 'empty_seed')
        second = m.Reader(); readers.append(second)
        neighbors = NeighborMap(nodes, partset['part_ids'])
        for name, offset in FILES:
            neighbors.mesh(second, name, offset)
            print('neighbor_pass_file_complete:' + name, flush=True)
        m.require(dict(neighbors.counts) == seed.counts, 'pass_record_counts_disagree')
        selected = nodes | {n for r in neighbors.neighbors for n in r['nodes']}
        incident_parts = set(partset['part_ids']) | {r['pid'] for r in neighbors.neighbors}
        definitions = []
        for pid in sorted(incident_parts):
            p = seed.parts.get(pid)
            m.require(p is not None, 'incident_part_missing')
            definitions.append({**p, 'section_defined': p['section_id'] in seed.sections,
                                'material_keyword': seed.materials.get(p['material_id'])})
        result = {
            'diagnostic': plane, 'partset': partset,
            'seed_records': seed.seed_records, 'seed_node_ids': sorted(nodes),
            'neighbors': neighbors.neighbors, 'orientation_only_candidates': neighbors.orientation_only,
            'coordinates': coordinates(seed, selected), 'part_definitions': definitions,
            'seed_bounds': m.bounds(seed.xyz[sorted(nodes)]),
            'unique_model_nodes': int(seed.present.sum()), 'all_element_counts': seed.counts,
            'include_graph': seed.includes, 'transforms': seed.transforms,
            'restraint_family_counts': dict(first.family_counts), 'restraint_blocks': first.blocks,
            'all_nodes_with_nonzero_constraint_fields': len(seed.constraint_fields),
            'boundary': 'contact/constraint cards inventoried, not expanded; no physical units/story/direction inferred',
        }
        receipt.update(status='complete', result=result)
    except Exception as exc:
        receipt.update(status='failed', error=exc.code if isinstance(exc, m.CardError) else 'unexpected_' + type(exc).__name__)
    receipt['sources'] = {str(i + 1): r.receipts for i, r in enumerate(readers)}
    receipt['elapsed_seconds'] = time.monotonic() - started
    with output.open('x') as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True, allow_nan=False); stream.write('\n')
    print(json.dumps({'status': receipt['status'], 'error': receipt.get('error'),
                      'output_sha256': m.digest(output)}), flush=True)
    return 0 if receipt['status'] == 'complete' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if args.controls:
        unittest.main(argv=[sys.argv[0]], exit=True)
    elif args.output:
        try:
            sys.exit(run(args.output.resolve()))
        except m.CardError as exc:
            print(json.dumps({'status': 'rejected', 'error': exc.code})); sys.exit(2)
    else:
        parser.error('choose --controls or --output')
