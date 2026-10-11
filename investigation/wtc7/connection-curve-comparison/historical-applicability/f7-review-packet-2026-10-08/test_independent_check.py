"""Synthetic-only composition, boundary, metadata and provenance controls."""
import ast
from collections import Counter
import contextlib
import copy
from fractions import Fraction as Q
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

import independent_check as c


def segment(a=10, b=11, state='paired_local_candidate'):
    return {'render_x': [a, b], 'status': state}


def scenarios(segments):
    return [{'solid_reader': solid, 'dash_reader': dash,
             'segments': copy.deepcopy(segments), 'actual_D': None, 'human_accepted': False,
             'own_candidate_render_lengths': {'solid': '1', 'dash': '1'}}
            for solid in c.ROLES for dash in c.ROLES]


def cell(pair, role, route, x):
    y = 20 if route == 'solid' else 30
    return {'id': '-'.join((pair, role, route, str(x))), 'pair': pair, 'role': role,
            'route': route, 'reader_path': 'synthetic-reader-' + role, 'source': 'Im0',
            'fragment_id': 'toy-' + route, 'native_rectangle': [x, y, x+1, y+2],
            'render_rectangle': [x, y, x+1, y+2], 'render_x': [x, x+1]}


def fixtures():
    admission = {'human_accepted': False, 'actual_D': None, 'model_discrepancies': None,
        'pairs': [{'pair': p, 'scenarios': scenarios([] if p == 'F7' else [segment()]),
                   'retained_pair_field': p} for p in c.PAIRS],
        'candidate_cells': [cell(p, r, style, 10) for p in c.PAIRS if p != 'F7'
                            for r in c.ROLES for style in ('solid', 'dash')],
        'axis_boxes': {panel+'-'+reader: {'L': [0, 0], 'R': [100, 100]}
                      for panel in ('F', 'E') for reader in ('root', 'independent')},
        'other_preserved_field': {'synthetic': True}}
    f7 = {'human_accepted': False, 'actual_D': None, 'model_discrepancies': None,
        'status': 'conditional_F7_coverage_followup_not_admitted_support',
        'region_id': 'F7-Im2-early', 'axis_boxes': copy.deepcopy(admission['axis_boxes']),
        'new_candidate_cells': [cell('F7', r, style, 30) for r in c.ROLES for style in ('solid', 'dash')],
        'preserved_old_F7_candidate_cells': [],
        'before_scenarios': copy.deepcopy(next(p for p in admission['pairs'] if p['pair'] == 'F7')['scenarios']),
        'after_scenarios': scenarios([segment(30, 31)])}
    invocations = {'Im0': {'ctm': [36, 0, 0, 36, 0, 756], 'native_dimensions': [100, 100]}}
    return admission, f7, invocations


def packet_fixture():
    admission, f7, invocations = fixtures()
    previous_slots, previous_inventory = c.old.reconstruct(admission, invocations)
    composed = c.compose(admission, f7, (52, 4, 0))
    slots, raw_inventory = c.old.reconstruct(composed, invocations)
    inventory = c.normalize_inventory(raw_inventory)
    metadata = c.compose_metadata(admission, f7, previous_slots, slots)
    previous = {'version': 1, 'status': 'conditional_mapping_packet_pending_human',
        'slots': previous_slots, 'inventory': previous_inventory, 'assets': {},
        'summary': dict(Counter(s['selection_status'] for s in previous_slots)),
        'human_accepted': False, 'actual_D': None, 'model_discrepancies': None,
        'original_actual_D_sampling_fulfilled': False,
        'domain_kind': 'C_H_primary_primary_not_actual_D', 'parent_result': c.ADMISSION_REF,
        'assumptions': ['Hidentity', 'Hsupport', 'Hink0'], 'limits': 'keep this exact',
        'inputs': {}, 'inputs_after': {}, 'source_pdf': {'synthetic': True}}
    actual = copy.deepcopy(previous)
    actual.update(version=2, packet_id=c.PACKET_ID, parent_packet=c.OLD_PACKET_REF,
                  f7_result=c.F7_REF, composition=metadata, slots=copy.deepcopy(slots),
                  inventory=copy.deepcopy(inventory), summary=dict(Counter(s['selection_status'] for s in slots)))
    return admission, f7, previous, actual, slots, inventory, metadata


class CompositionControls(unittest.TestCase):
    def test_exact_additive_composition_without_mutation(self):
        a, f, _ = fixtures()
        before = c.encoded([a, f])
        result = c.compose(a, f, (52, 4, 0))
        self.assertEqual(c.encoded([a, f]), before)
        self.assertEqual(result['candidate_cells'][:52], a['candidate_cells'])
        self.assertEqual(result['candidate_cells'][52:], f['new_candidate_cells'])
        self.assertEqual(result['other_preserved_field'], a['other_preserved_field'])
        self.assertEqual([p for p in result['pairs'] if p['pair'] != 'F7'],
                         [p for p in a['pairs'] if p['pair'] != 'F7'])
        result['candidate_cells'][0]['id'] = 'mutated return only'
        self.assertNotEqual(result['candidate_cells'][0]['id'], a['candidate_cells'][0]['id'])

    def test_non_F7_missing_duplicate_and_collision_additions(self):
        for mode in ('foreign', 'missing', 'duplicate', 'collision', 'no_id'):
            a, f, _ = fixtures()
            if mode == 'foreign': f['new_candidate_cells'][0]['pair'] = 'F6'
            if mode == 'missing': f['new_candidate_cells'].pop()
            if mode == 'duplicate': f['new_candidate_cells'][1] = copy.deepcopy(f['new_candidate_cells'][0])
            if mode == 'collision': f['new_candidate_cells'][0]['id'] = a['candidate_cells'][0]['id']
            if mode == 'no_id': f['new_candidate_cells'][0]['id'] = ''
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                c.compose(a, f, (52, 4, 0))

    def test_old_F7_cell_change_rejected(self):
        a, f, _ = fixtures()
        prior = cell('F7', 'primary', 'solid', 5)
        a['candidate_cells'].append(prior)
        f['preserved_old_F7_candidate_cells'] = [copy.deepcopy(prior)]
        c.compose(a, f, (53, 4, 1))
        f['preserved_old_F7_candidate_cells'][0]['native_rectangle'][1] += 1
        with self.assertRaisesRegex(ValueError, 'old F7 cells'):
            c.compose(a, f, (53, 4, 1))

    def test_changed_old_scenarios_or_axes(self):
        for mutate in (
            lambda f: f['before_scenarios'][0].update(segments=[segment()]),
            lambda f: f['axis_boxes']['F-root'].update(L=[1, 1])):
            a, f, _ = fixtures()
            mutate(f)
            with self.assertRaises(ValueError):
                c.compose(a, f, (52, 4, 0))

    def test_changed_pair_roster_or_order(self):
        a, f, _ = fixtures()
        a['pairs'][0], a['pairs'][1] = a['pairs'][1], a['pairs'][0]
        with self.assertRaisesRegex(ValueError, 'roster/order'):
            c.compose(a, f, (52, 4, 0))

    def test_bad_or_reordered_scenarios(self):
        for mode in ('missing', 'swapped', 'overlap', 'accepted'):
            a, f, _ = fixtures()
            if mode == 'missing': f['after_scenarios'].pop()
            if mode == 'swapped': f['after_scenarios'][0], f['after_scenarios'][1] = f['after_scenarios'][1], f['after_scenarios'][0]
            if mode == 'overlap': f['after_scenarios'][0]['segments'] = [segment(0, 2), segment(1, 3)]
            if mode == 'accepted': f['after_scenarios'][0]['human_accepted'] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                c.compose(a, f, (52, 4, 0))

    def test_acceptance_and_identity_contamination(self):
        for target in ('admission', 'f7'):
            for key, value in [('human_accepted', True), ('actual_D', []), ('model_discrepancies', {})]:
                a, f, _ = fixtures()
                (a if target == 'admission' else f)[key] = value
                with self.subTest(target=target, key=key), self.assertRaises(ValueError):
                    c.compose(a, f, (52, 4, 0))
        a, f, _ = fixtures()
        f['region_id'] = 'F7-Im2'
        with self.assertRaises(ValueError):
            c.compose(a, f, (52, 4, 0))

    def test_all42_and39_unchanged_known_quantiles(self):
        a, f, previous, actual, slots, inventory, metadata = packet_fixture()
        self.assertEqual(len(slots), 42)
        self.assertEqual(sum(len(s['entries']) for s in slots), 84)
        self.assertEqual(metadata['changed_slot_ids'], ['CE-F7Q1', 'CE-F7Q2', 'CE-F7Q3'])
        self.assertEqual(len(metadata['unchanged_slot_ids']), 39)
        self.assertEqual([s['page_x'] for s in slots if s['pair'] == 'F7'],
                         [Q(121, 4), Q(61, 2), Q(123, 4)])
        for s in slots:
            self.assertFalse(s['human_accepted'])
            for e in s['entries']:
                self.assertIsNone(e['human_response'])
                self.assertEqual(e['human_status'], 'uninspected')
        c.check_packet(actual, previous, slots, inventory, {}, metadata)

    def test_non_F7_slot_mutation_rejected_even_with_same_counts(self):
        a, f, previous, _, slots, _, _ = packet_fixture()
        slots[0]['entries'][0]['reason'] = 'silently changed'
        with self.assertRaisesRegex(ValueError, 'non-F7 slot changed'):
            c.compose_metadata(a, f, previous['slots'], slots)

    def test_slot_reordering_or_missing_rejected(self):
        a, f, previous, _, slots, _, _ = packet_fixture()
        for changed in (slots[:-1], [slots[1], slots[0]] + slots[2:]):
            with self.assertRaises(ValueError):
                c.compose_metadata(a, f, previous['slots'], changed)

    def test_empty_new_F7_stays_unavailable(self):
        a, f, invocations = fixtures()
        f['after_scenarios'] = scenarios([])
        result = c.compose(a, f, (52, 4, 0))
        slots, _ = c.old.reconstruct(result, invocations)
        chosen = [s for s in slots if s['pair'] == 'F7']
        self.assertTrue(all(s['page_x'] is None and s['selection_status'] ==
                            'unavailable_empty_primary_domain' for s in chosen))

    def test_boundary_tie_not_nudged_or_filled(self):
        a, f, invocations = fixtures()
        f['after_scenarios'] = scenarios([segment(30, Q(121, 4)),
            segment(Q(121, 4), Q(123, 4), 'gap'), segment(Q(123, 4), 31)])
        slots, _ = c.old.reconstruct(c.compose(a, f, (52, 4, 0)), invocations)
        middle = next(s for s in slots if s['id'] == 'CE-F7Q2')
        self.assertEqual(middle['page_x'], Q(121, 4))
        self.assertTrue(middle['cumulative_tie'])
        self.assertEqual(middle['selection_status'], 'boundary_unresolved')

    def test_same_position_peer_gap_retained(self):
        a, f, invocations = fixtures()
        f['after_scenarios'][3]['segments'] = [segment(30, 31, 'gap')]
        slots, _ = c.old.reconstruct(c.compose(a, f, (52, 4, 0)), invocations)
        chosen = next(s for s in slots if s['id'] == 'CE-F7Q1')
        self.assertEqual(chosen['page_x'], Q(121, 4))
        self.assertEqual(chosen['scenario_states']['peer-peer']['status'], 'gap')

    def test_duplicate_flags_and_native_inverse(self):
        *_, slots, _, _ = packet_fixture()
        first = next(s for s in slots if s['id'] == 'CE-F7Q1')
        self.assertEqual(first['duplicate_paired_slots'], ['CE-F7Q2', 'CE-F7Q3'])
        mapping = first['entries'][0]['mappings']['primary'][0]
        self.assertEqual(mapping['native_x'], Q(121, 4))
        self.assertFalse(mapping['boundary_touch'])

    def test_inventory_normalization_explicit_and_no_mutation(self):
        a, f, invocations = fixtures()
        _, raw = c.old.reconstruct(c.compose(a, f, (52, 4, 0)), invocations)
        before = c.encoded(raw)
        result = c.normalize_inventory(raw)
        self.assertEqual(c.encoded(raw), before)
        self.assertEqual(sum(r['all_scenarios_preserved_in'] == c.F7_REF for r in result), 1)
        self.assertEqual(sum(r['all_scenarios_preserved_in'] == c.ADMISSION_REF for r in result), 13)
        raw[0]['all_scenarios_preserved_in'] = 'unknown'
        with self.assertRaises(ValueError):
            c.normalize_inventory(raw)

    def test_metadata_human_and_old_top_level_preservation(self):
        for key, value in [('packet_id', 'old'), ('version', True), ('version', 1),
                           ('parent_packet', 'wrong'), ('f7_result', 'wrong'),
                           ('limits', 'silently rewritten'), ('human_accepted', True),
                           ('actual_D', []), ('model_discrepancies', {}),
                           ('original_actual_D_sampling_fulfilled', True)]:
            _, _, prev, actual, slots, inv, metadata = packet_fixture()
            actual[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                c.check_packet(actual, prev, slots, inv, {}, metadata)

    def test_added_field_and_entered_response_rejected(self):
        for mutate in (lambda x: x.update(unreviewed_extra=True),
                       lambda x: x['slots'][0]['entries'][0].update(human_response='agree'),
                       lambda x: x['slots'][0]['entries'][0].update(human_status='inspected')):
            _, _, prev, actual, slots, inv, metadata = packet_fixture()
            mutate(actual)
            with self.assertRaises(ValueError):
                c.check_packet(actual, prev, slots, inv, {}, metadata)


class ProvenanceControls(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix='f7-packet-check-')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()

    def test_declared_map_resolves_against_its_owner(self):
        graph, f7 = self.root/'graph', self.root/'graph'/'nested'/'f7'
        f7.mkdir(parents=True)
        (graph/'data.txt').write_bytes(b'wrong owner')
        (f7/'data.txt').write_bytes(b'right owner')
        expected = c.pin(f7/'data.txt')
        record = {'inputs': {'data.txt': expected}, 'inputs_after': {'data.txt': expected}}
        required = {}
        c.include_declared(required, record, f7)
        self.assertEqual(required[os.path.relpath(f7/'data.txt', c.BASE)], expected)
        with self.assertRaises(ValueError):
            c.include_declared({}, record, graph)

    def test_relative_parent_path_from_receipt_owner(self):
        graph, f7 = self.root/'graph', self.root/'graph'/'nested'/'f7'
        f7.mkdir(parents=True)
        target = graph/'shared.txt'
        target.write_bytes(b'exact synthetic')
        expected = c.pin(target)
        record = {'inputs': {'../../shared.txt': expected}, 'inputs_after': {'../../shared.txt': expected}}
        required = {}
        c.include_declared(required, record, f7)
        self.assertEqual(required[os.path.relpath(target, c.BASE)], expected)
        with self.assertRaises(FileNotFoundError):
            c.include_declared({}, record, graph)

    def test_declared_before_after_and_changed_bytes(self):
        path = self.root/'data.txt'
        path.write_bytes(b'synthetic')
        expected = c.pin(path)
        record = {'inputs': {'data.txt': expected}, 'inputs_after': {}}
        with self.assertRaises(ValueError):
            c.include_declared({}, record, self.root)
        record['inputs_after'] = copy.deepcopy(record['inputs'])
        path.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            c.include_declared({}, record, self.root)

    def test_required_omission_wrong_digest_boolean_bytes(self):
        required = {n: {'sha256': 'a'*64, 'bytes': 1} for n in ('old', 'f7', 'protocol')}
        c.old.require_closure(required, required)
        for name in required:
            bad = copy.deepcopy(required)
            bad.pop(name)
            with self.assertRaises(ValueError):
                c.old.require_closure(bad, required)
        bad = copy.deepcopy(required)
        bad['old']['bytes'] = True
        with self.assertRaises(ValueError):
            c.old.require_closure(bad, required)

    def test_missing_frozen_producer_not_discovered(self):
        for value in (None, '', True, 'a'*63, 'Z'*64):
            with self.assertRaises(ValueError):
                c.digest(value)

    def test_bad_helper_hash_not_executed(self):
        path = self.root/'bad.py'
        path.write_text('raise RuntimeError("must not execute")')
        with self.assertRaisesRegex(ValueError, 'helper changed'):
            c.import_helper(path)

    def test_packet_identity_and_two_copies(self):
        a, b = self.root/'one.json', self.root/'two.json'
        a.write_bytes(b'{}\n'); b.write_bytes(b'{}\n')
        sha = c.pin(a)['sha256']
        self.assertEqual(c.matching_packets(a, b, sha), [a, b])
        for left, right, frozen in ((a, a, sha), (a, b, '0'*64)):
            with self.assertRaises(ValueError):
                c.matching_packets(left, right, frozen)
        b.write_bytes(b'{ }\n')
        with self.assertRaises(ValueError):
            c.matching_packets(a, b, sha)

    def test_symlink_and_hardlink_not_independent_packet_copies(self):
        a = self.root/'one.json'
        a.write_bytes(b'{}\n')
        link = self.root/'link.json'
        link.symlink_to(a)
        with self.assertRaises(ValueError):
            c.matching_packets(a, link, c.pin(a)['sha256'])
        hard = self.root/'hard.json'
        os.link(a, hard)
        with self.assertRaises(ValueError):
            c.matching_packets(a, hard, c.pin(a)['sha256'])

    def test_exclusive_receipt(self):
        value = {'synthetic': True}
        path = c.save_receipt(value, self.root)
        self.assertEqual(path.name, 'independent-check.json')
        self.assertEqual(path.read_bytes(), c.encoded(value))
        with self.assertRaises(FileExistsError):
            c.save_receipt({}, self.root)
        self.assertEqual(path.read_bytes(), c.encoded(value))

    def test_headers_valid_rgb_and_invalid_depth(self):
        path = self.root/'header.png'
        header = b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR'
        path.write_bytes(header + struct.pack('>IIBBBBB', 7, 11, 8, 2, 0, 0, 0))
        self.assertEqual(c.old.image_header(path), (7, 11))
        path.write_bytes(header + struct.pack('>IIBBBBB', 7, 11, 16, 2, 0, 0, 0))
        with self.assertRaises(ValueError):
            c.old.image_header(path)

    def test_cli_dispatch_without_historical_execution(self):
        receipt = {'status': 'synthetic-only'}
        with mock.patch.object(c, 'verify', return_value=receipt) as verify:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                c.main(['--expected-sha', 'a'*64])
            self.assertEqual(json.loads(out.getvalue()), receipt)
            verify.assert_called_once_with(c.HERE/'packet01.json', c.HERE/'packet02.json', 'a'*64)

    def test_no_producer_import_or_old_global_mutation(self):
        tree = ast.parse(Path(c.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(n.name in ('packet', 'assess', 'calculate') for n in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn(node.module, ('packet', 'assess', 'calculate'))
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                self.assertFalse(any(isinstance(t, ast.Attribute) and
                    isinstance(t.value, ast.Name) and t.value.id == 'old' for t in targets))


if __name__ == '__main__':
    unittest.main()

