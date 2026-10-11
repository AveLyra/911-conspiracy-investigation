"""Synthetic controls for F6 Im3 schema, reconciliation and cross-pair audit."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import compare as c


def fixture(role='primary'):
    data = {'region_id': 'F6-Im3', 'pair': 'F6', 'source': 'Im3.jpg', 'reader': role,
            'target_box': [145, 0, 440, 88], 'context_box': [143, 0, 442, 88],
            'coverage': {'full_context_inspected': True, 'raw_context_cells': 26312,
                         'raw_blocks': [{'columns': [143, 441], 'receipt': 'synthetic'}],
                         'actual_views': ['synthetic, not historical'], 'prior_knowledge': 'synthetic',
                         'rows': [0, 87],
                         'uncompleted_context': []}, 'human_accepted': False, 'physical_support': None,
            'routes': {}, 'unassigned_bands': []}
    for route in ('solid', 'dash'):
        data['routes'][route] = [{'x': x, 'core': [], 'fringe': [], 'fragment_id': None,
                                 'fragment_membership': [], 'status': 'no_attributable_cells',
                                 'reason': 'Synthetic empty', 'boundary_flags': [],
                                 'unassigned_band_refs': []} for x in range(145, 440)]
    return data


def select(row, core, fringe):
    row.update(core=core, fringe=fringe, fragment_id='synthetic',
               fragment_membership=[{'fragment_id': 'synthetic', 'core': core, 'fringe': fringe}],
               status='identified_local_fragment' if core else 'fringe_only')


class Contracts(unittest.TestCase):
    def setUp(self):
        self.helpers = c.helpers()
        self.data = fixture()

    def check(self, data=None, role='primary'):
        return c.validate(self.data if data is None else data, role, self.helpers)

    def test_empty_complete_and_preserved(self):
        original = copy.deepcopy(self.data)
        self.check()
        self.check(fixture('peer'), 'peer')
        self.assertEqual(original, self.data)

    def test_legacy_alias_rejected(self):
        self.data['reader'] = 'force56_peer'
        with self.assertRaises(ValueError):
            self.check(role='peer')

    def test_source_mismatch(self):
        self.data['source'] = 'Im2.jpg'
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_column(self):
        self.data['routes']['solid'].pop()
        with self.assertRaises(ValueError):
            self.check()

    def test_target_bounds(self):
        for bad in (-1, 88, True):
            data = fixture()
            select(data['routes']['solid'][1], [bad], [])
            with self.assertRaises(ValueError):
                self.check(data)

    def test_boundary_flags(self):
        row = self.data['routes']['solid'][0]
        select(row, [0], [87])
        row.update(status='boundary_truncated', boundary_flags=['target_left', 'target_top', 'target_bottom'])
        self.check()
        row['boundary_flags'].pop()
        with self.assertRaises(ValueError):
            self.check()

    def test_membership_loss(self):
        row = self.data['routes']['solid'][1]
        select(row, [40], [])
        row['fragment_membership'] = []
        with self.assertRaises(ValueError):
            self.check()

    def test_duplicate_route_ink(self):
        for route in ('solid', 'dash'):
            select(self.data['routes'][route][1], [40], [])
        with self.assertRaises(ValueError):
            self.check()

    def test_bad_raw_coverage(self):
        self.data['coverage']['raw_blocks'][0]['columns'][1] = 440
        with self.assertRaises(ValueError):
            self.check()

    def test_uninspected_rejected(self):
        self.data['coverage']['full_context_inspected'] = False
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_view_record(self):
        self.data['coverage']['actual_views'] = []
        with self.assertRaises(ValueError):
            self.check()

    def test_unfinished_context(self):
        self.data['coverage']['uncompleted_context'] = [441]
        with self.assertRaises(ValueError):
            self.check()

    def test_consistent_row_aliases(self):
        self.data['coverage']['rows_covered'] = [0, 87]
        old = copy.deepcopy(self.data)
        self.check()
        self.assertEqual(old, self.data)
        for bad in ([0, 86], [False, 87], []):
            self.data['coverage']['rows_covered'] = bad
            with self.assertRaises(ValueError):
                self.check()

    def test_primary_band_without_outgoing_reference_field(self):
        self.add_band('solid', 40)
        self.data['unassigned_bands'][0].pop('unassigned_band_refs')
        old = copy.deepcopy(self.data)
        self.check()
        self.assertEqual(old, self.data)
        self.data['unassigned_bands'][0]['unassigned_band_refs'] = ['invented']
        with self.assertRaises(ValueError):
            self.check()
        self.data['unassigned_bands'][0]['unassigned_band_refs'] = []
        self.data['unassigned_bands'][0]['unknown'] = True
        with self.assertRaises(ValueError):
            self.check()

    def add_band(self, route, y):
        row = self.data['routes'][route][1]
        band = copy.deepcopy(row)
        select(band, [y], [])
        band.update(band_id=route, candidate_routes=[route])
        self.data['unassigned_bands'].append(band)
        row.update(status='identity_conflict', unassigned_band_refs=[route])

    def test_multiple_bands_reciprocal_and_preserved(self):
        self.add_band('solid', 40)
        self.add_band('dash', 50)
        old = copy.deepcopy(self.data)
        self.assertEqual(len(self.check()[146]), 2)
        self.assertEqual(old, self.data)
        self.data['routes']['dash'][1]['unassigned_band_refs'] = ['solid']
        with self.assertRaises(ValueError):
            self.check()

    def test_missing_reciprocal(self):
        self.add_band('solid', 40)
        self.data['routes']['solid'][1].update(status='no_attributable_cells', unassigned_band_refs=[])
        with self.assertRaises(ValueError):
            self.check()

    def test_orphan_reference(self):
        self.data['routes']['solid'][1]['unassigned_band_refs'] = ['missing']
        with self.assertRaises(ValueError):
            self.check()

    def test_class_operations(self):
        h = self.helpers[1]
        actual = h.comparison({'core': [1, 2], 'fringe': [3]}, {'core': [2, 3], 'fringe': [4]})
        self.assertEqual(actual['outer'], {'intersection': [2, 3], 'union': [1, 2, 3, 4],
                                         'primary_only': [1], 'peer_only': [4], 'symmetric_difference': [1, 4]})
        self.assertEqual(actual['core']['symmetric_difference'], [1, 3])

    def test_cross_all_four_pairings_and_class_direction(self):
        new = {role: fixture(role) for role in c.ROLES}
        old = {role: fixture(role) for role in c.ROLES}
        select(new['primary']['routes']['solid'][1], [40], [41])
        select(old['peer']['routes']['dash'][1], [41], [40])
        out = c.cross_pair(new, old)
        self.assertEqual([(r['f6_reader'], r['f5_reader']) for r in out],
                         [('primary', 'primary'), ('primary', 'peer'), ('peer', 'primary'), ('peer', 'peer')])
        self.assertTrue(all(len(r['intersections']) == 9 for r in out))
        hit = out[1]['intersections'][1]['cells']
        self.assertEqual(hit, {'core_core': [], 'core_fringe': [[146, 40]], 'fringe_core': [[146, 41]],
                               'fringe_fringe': [], 'outer': [[146, 40], [146, 41]]})
        self.assertTrue(all(not e['cells']['outer'] for r in (out[0], out[2], out[3]) for e in r['intersections']))

    def test_cross_includes_unassigned_and_no_false_column_match(self):
        new = {role: fixture(role) for role in c.ROLES}
        old = {role: fixture(role) for role in c.ROLES}
        row = copy.deepcopy(new['primary']['routes']['solid'][1])
        select(row, [40], [])
        new['primary']['unassigned_bands'] = [row]
        select(old['primary']['routes']['solid'][1], [40], [])
        select(old['peer']['routes']['solid'][2], [40], [])
        out = c.cross_pair(new, old)
        self.assertEqual(out[0]['intersections'][6]['cells']['outer'], [[146, 40]])
        self.assertEqual(out[1]['intersections'][6]['cells']['outer'], [])

    def test_recursive_pin_mutation_rejected(self):
        with tempfile.TemporaryDirectory(prefix='f6-im3-pins-') as tmp:
            leaf = Path(tmp)/'leaf.txt'
            leaf.write_text('synthetic')
            root = Path(tmp)/'root.json'
            root.write_text(json.dumps({'inputs': {'leaf.txt': c.pin(leaf)}}))
            deps = {}
            c.collect(root, c.pin(root), deps)
            self.assertEqual(len(deps), 2)
            leaf.write_text('changed')
            with self.assertRaises(ValueError):
                c.collect(root, c.pin(root), {})
            with self.assertRaises(ValueError):
                c.collect(leaf, c.pin(leaf), deps)


if __name__ == '__main__':
    unittest.main()
