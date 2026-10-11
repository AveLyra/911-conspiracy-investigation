"""Synthetic controls only; no new historical annotation or producer import."""
import copy
from fractions import Fraction as Q
import unittest

import independent_check as check


def row(x, values=None, identity='s', fringe=None):
    core, edge = ([] if values is None else values), ([] if fringe is None else fringe)
    selected = core+edge
    flags = []
    if selected:
        flags = [name for name, condition in [('target_left', x == 220), ('target_right', x == 329),
            ('target_top', 0 in selected), ('target_bottom', 87 in selected)] if condition]
    return {'x': x, 'core': core, 'fringe': edge, 'fragment_id': identity if selected else None,
        'fragment_membership': [{'fragment_id': identity, 'core': core.copy(), 'fringe': edge.copy()}] if selected else [],
        'status': 'identified_local_fragment' if core else ('fringe_only' if edge else 'no_attributable_cells'),
        'reason': 'Invented synthetic fixture, no historical attribution.', 'boundary_flags': flags,
        'unassigned_band_refs': []}


def source(role='primary'):
    return {'reader': role, 'pair': 'F7', 'region_id': 'F7-Im2-early', 'source': 'Im2.jpg',
        'target_box': [220, 0, 330, 88], 'context_box': [218, 0, 332, 88],
        'human_accepted': False, 'physical_support': None,
        'coverage': {'full_context_inspected': True, 'uncompleted_context': [], 'raw_context_cells': 10032,
            'rows': [0, 87], 'prior_knowledge': 'Synthetic fixture only.',
            'raw_blocks': [{'columns': [218, 331], 'receipt': 'synthetic-not-historical'}],
            'actual_views': [{'path': '../../native-strips01/Im2.jpg', 'receipt': 'synthetic-view'},
                             {'path': '../../render01/page-076.png', 'receipt': 'synthetic-view'}]},
        'routes': {'solid': [row(x, [20]) for x in range(220, 330)],
                   'dash': [row(x, [30], 'd') for x in range(220, 330)]}, 'unassigned_bands': []}


def cell(identity, route, lo, hi, source_name='Im1', native=None, fragment='body'):
    return {'id': identity, 'route': route, 'render_x': [lo, hi], 'source': source_name,
            'native_rectangle': native or [0, 1 if route == 'solid' else 3, 1, 2 if route == 'solid' else 4],
            'body': [identity.split(':')[0], source_name, fragment]}


class IndependentControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = check.helper('bookkeeping')
        cls.geo = check.helper('geometry')
        cls.raw = check.helper('rows')

    def assert_bad_source(self, mutate):
        data = source()
        mutate(data)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            check.annotation(data, 'primary', self.book)

    def expected_rows(self, data):
        invocation = {'native_dimensions': [741, 88], 'ctm': [Q('355.5269928'), 0, 0,
                       Q('42.2400055'), Q('128.3399963'), Q('593.2799988')]}
        return self.raw.expected_rows(self.geo.copy_source(data),
            {'pair': 'F7', 'source': 'Im2', 'target_box': check.TARGET}, 'F', invocation)

    def test_valid_original_no_alias_mutation(self):
        data = source()
        before = check.encoded(data)
        check.annotation(data, 'primary', self.book)
        self.expected_rows(data)
        self.assertEqual(before, check.encoded(data))
        self.assertEqual(data['region_id'], 'F7-Im2-early')

    def test_identity_and_role_guard(self):
        for key, value in [('region_id', 'F7-Im2'), ('reader', 'peer'), ('source', 'Im3.jpg'), ('pair', 'F6')]:
            with self.subTest(key=key):
                self.assert_bad_source(lambda d: d.__setitem__(key, value))

    def test_target_boolean_and_old_box_rejected(self):
        self.assert_bad_source(lambda d: d.__setitem__('target_box', [220, False, 330, 88]))
        self.assert_bad_source(lambda d: d.__setitem__('target_box', [330, 0, 475, 88]))

    def test_no_human_or_physical_acceptance(self):
        self.assert_bad_source(lambda d: d.__setitem__('human_accepted', True))
        self.assert_bad_source(lambda d: d.__setitem__('physical_support', []))

    def test_context_attestation_controls(self):
        for field, value in [('raw_context_cells', 10031), ('rows', [0, 86]),
                             ('full_context_inspected', False), ('uncompleted_context', [220]),
                             ('prior_knowledge', {}), ('counterpart_new_annotations_read', True)]:
            with self.subTest(field=field):
                self.assert_bad_source(lambda d: d['coverage'].__setitem__(field, value))

    def test_truncated_or_missing_context_block(self):
        self.assert_bad_source(lambda d: d['coverage']['raw_blocks'][0].__setitem__('truncated', True))
        self.assert_bad_source(lambda d: d['coverage']['raw_blocks'][0].__setitem__('columns', [219, 331]))
        self.assert_bad_source(lambda d: d['coverage']['raw_blocks'].append(copy.deepcopy(d['coverage']['raw_blocks'][0])))

    def test_view_source_path_required(self):
        self.assert_bad_source(lambda d: d['coverage'].__setitem__('actual_views', [{'path': '../../native-strips01/Im1.jpg'}]))
        self.assert_bad_source(lambda d: d['coverage'].__setitem__('actual_views', ['Im2.jpg', 'page-076.png']))

    def test_view_receipt_required(self):
        self.assert_bad_source(lambda d: d['coverage']['actual_views'][0].pop('receipt'))

    def test_source_columns_missing_or_duplicate(self):
        self.assert_bad_source(lambda d: d['routes']['solid'].pop())
        self.assert_bad_source(lambda d: d['routes']['solid'].__setitem__(1, copy.deepcopy(d['routes']['solid'][0])))

    def test_membership_class_union_and_overlap(self):
        self.assert_bad_source(lambda d: d['routes']['solid'][10]['fragment_membership'][0].__setitem__('core', [21]))
        self.assert_bad_source(lambda d: d['routes']['solid'][10]['fringe'].append(20))
        self.assert_bad_source(lambda d: d['routes']['solid'][10]['fragment_membership'].append(
            {'fragment_id': 'second', 'core': [20], 'fringe': []}))

    def test_cross_route_shared_ink_rejected_in_new_original(self):
        self.assert_bad_source(lambda d: d['routes']['dash'].__setitem__(10, row(230, [20], 'd')))

    def test_real_reciprocal_multiband_preserved(self):
        data = source()
        first = row(230, [40], 'u1') | {'band_id': 'u1', 'candidate_routes': ['solid']}
        second = row(230, [50], 'u2') | {'band_id': 'u2', 'candidate_routes': ['dash']}
        first['status'] = second['status'] = 'identity_conflict'
        data['unassigned_bands'] = [first, second]
        data['routes']['solid'][10]['unassigned_band_refs'] = ['u1']
        data['routes']['dash'][10]['unassigned_band_refs'] = ['u2']
        self.assertEqual(len(check.annotation(data, 'primary', self.book)[230]), 2)
        data['routes']['dash'][10]['unassigned_band_refs'] = ['u1']
        with self.assertRaises(ValueError):
            check.annotation(data, 'primary', self.book)

    def test_missing_and_nonreciprocal_band_refs(self):
        self.assert_bad_source(lambda d: d['routes']['solid'][10]['unassigned_band_refs'].append('missing'))
        data = source()
        band = row(230, [40], 'u') | {'band_id': 'u', 'candidate_routes': ['solid']}
        data['unassigned_bands'] = [band]
        with self.assertRaises(ValueError):
            check.annotation(data, 'primary', self.book)

    def test_finite_neighbor_guard_no_recursive_erosion(self):
        data = source()
        data['routes']['dash'][10] = row(230)
        rows = {r['column']: r for r in self.expected_rows(data) if r['route'] == 'dash'}
        self.assertTrue(rows[228]['conditional_window'])
        self.assertFalse(rows[229]['conditional_window'])
        self.assertFalse(rows[230]['conditional_window'])
        self.assertFalse(rows[231]['conditional_window'])
        self.assertTrue(rows[232]['conditional_window'])

    def test_fragment_change_neighbor_exclusion(self):
        data = source()
        data['routes']['dash'][20] = row(240, [30], 'd-other')
        rows = {r['column']: r for r in self.expected_rows(data) if r['route'] == 'dash'}
        self.assertTrue(rows[238]['conditional_window'])
        self.assertEqual([rows[x]['conditional_window'] for x in (239, 240, 241)], [False]*3)
        self.assertTrue(rows[242]['conditional_window'])

    def test_440_invented_decisions_and_target_edge_rules(self):
        all_rows = self.expected_rows(source()) + self.expected_rows(source('peer'))
        self.assertEqual(len(all_rows), 440)
        self.assertEqual(sum(r['conditional_window'] for r in all_rows), 424)
        self.assertTrue(all(r['curve_support_established'] is False for r in all_rows))

    def test_disconnected_and_band_referenced_eligibility(self):
        data = source()
        data['routes']['solid'][10] = row(230, [20, 22])
        data['routes']['solid'][30]['unassigned_band_refs'] = ['synthetic-ref']
        rows = {r['column']: r for r in self.expected_rows(data) if r['route'] == 'solid'}
        self.assertIn('disconnected_outer', rows[230]['reasons'])
        self.assertIsNone(rows[230]['native_rectangle'])
        self.assertIn('unassigned_band_reference', rows[250]['reasons'])
        self.assertIsNotNone(rows[250]['native_rectangle'])
        self.assertFalse(rows[250]['conditional_window'])

    def test_prior_manual_ctm_axis_mask_oracles(self):
        self.assertEqual(len(self.raw.manual_checks()), 12)

    def test_truth_table_set_operations(self):
        self.assertEqual(self.book.operations([0, 2], [2, 87]), {'intersection': [2],
            'union': [0, 2, 87], 'primary_only': [0], 'peer_only': [87], 'symmetric_difference': [0, 87]})

    def test_comparison_counts_and_class_change(self):
        readers = {'primary': source(), 'peer': source('peer')}
        readers['peer']['routes']['solid'][10] = row(230, [], 's', [20])
        result, summary = check.comparisons(readers, self.book)
        self.assertEqual(len(result['route_records']), 220)
        self.assertEqual(len(result['all_ink_columns']), 110)
        self.assertEqual(summary['routes'], {'entries': 220, 'outer_different': 0, 'class_different': 1})
        self.assertEqual(summary['all_ink']['class_different'], 1)
        self.assertEqual(summary['status_different'], 1)

    def test_cross_strip_pairing_no_seam_join(self):
        cells = [cell('s:1', 'solid', 0, 1, 'Im1'), cell('d:1', 'dash', 0, 1, 'Im2')]
        result = self.geo.midpoint_partition(cells)
        self.assertEqual(result['paired_segment_count'], 1)
        self.assertEqual(result['segments'][0]['status'], 'paired_local_candidate')

    def test_shared_native_cell_and_duplicate_coverage(self):
        solid = cell('s:1', 'solid', 0, 1, native=[0, 1, 1, 2])
        dash = cell('d:1', 'dash', 0, 1, native=[0, 1, 1, 2])
        self.assertEqual(self.geo.midpoint_partition([solid, dash])['segments'][0]['status'], 'shared_ink_ownership_conflict')
        duplicate = cell('s2:1', 'solid', 0, 1)
        self.assertEqual(self.geo.midpoint_partition([solid, duplicate, dash])['segments'][0]['status'], 'overlapping_candidate_coverage')

    def test_native_gap_not_marginal_axis_hull_overlap(self):
        result = self.geo.midpoint_partition([cell('s:1', 'solid', 0, 1), cell('d:1', 'dash', 2, 3)])
        self.assertEqual(result['paired_segment_count'], 0)
        self.assertEqual([p['status'] for p in result['segments']], ['solid_only', 'gap', 'dash_only'])

    def test_same_fragment_id_not_cross_reader_body(self):
        cells = [cell('s1:1', 'solid', 0, 1), cell('s2:1', 'solid', 1, 2),
                 cell('d:1', 'dash', 0, 2)]
        result = self.geo.midpoint_partition(cells)
        self.assertEqual(len(result['paired_runs']), 2)

    def test_shared_axis_length_corner_oracle(self):
        self.assertEqual(self.geo.bounds_by_vertices(2, {'L': [0, 1], 'R': [9, 10]}), [Q(8, 25), Q(2, 5)])
        with self.assertRaises(ValueError):
            self.geo.bounds_by_vertices(1, {'L': [0, 10], 'R': [9, 10]})

    def test_required_pins_omission_and_boolean_bytes(self):
        pin = {'sha256': '0'*64, 'bytes': 1}
        required = {'a': pin, 'b': pin}
        check.require_map(required, required)
        for key in required:
            omitted = dict(required)
            del omitted[key]
            with self.assertRaises(ValueError):
                check.require_map(omitted, required)
        with self.assertRaises(ValueError):
            check.pin_shape({'sha256': '0'*64, 'bytes': True})


if __name__ == '__main__':
    unittest.main()
