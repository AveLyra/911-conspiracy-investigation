"""Adversarial synthetic controls for the separate admission checker."""
import copy
from fractions import Fraction as Q
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_admission_under_test', HERE/'independent_check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def cell(key, route, lo, hi, y=1, source='Im3', body=None):
    return {'id': key, 'route': route, 'render_x': [lo, hi],
            'native_rectangle': [10, y, 11, y+1], 'source': source,
            'body': body or ['reader', source, route+'-fragment']}


def axes():
    return {'L': [0, 1], 'R': [9, 10]}


class GeometryControls(unittest.TestCase):
    def test_empty_preserves_empty_candidate_only(self):
        result = check.midpoint_partition([])
        self.assertEqual(result['segments'], [])
        self.assertEqual(result['paired_runs'], [])
        self.assertEqual(result['render_lengths']['paired_local_candidate'], 0)

    def test_exact_rational_pair(self):
        result = check.midpoint_partition([cell('s', 'solid', '1/3', '4/3'),
                                           cell('d', 'dash', '2/3', '5/3', y=5)])
        self.assertEqual([r['status'] for r in result['segments']], ['solid_only', 'paired_local_candidate', 'dash_only'])
        self.assertEqual(result['render_lengths']['paired_local_candidate'], Q(2, 3))
        self.assertEqual(result['paired_runs'][0]['render_x'], [Q(2, 3), Q(4, 3)])

    def test_endpoint_touch_is_zero(self):
        result = check.midpoint_partition([cell('s', 'solid', 0, 1), cell('d', 'dash', 1, 2, y=5)])
        self.assertEqual(result['paired_segment_count'], 0)
        self.assertEqual(result['any_paired_render_length'], 0)

    def test_gap_never_bridged(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1), cell('d1', 'dash', 0, 1, y=5),
                                           cell('s2', 'solid', 2, 3), cell('d2', 'dash', 2, 3, y=5)])
        self.assertEqual([r['status'] for r in result['segments']], ['paired_local_candidate', 'gap', 'paired_local_candidate'])
        self.assertEqual(len(result['paired_runs']), 2)
        self.assertEqual(result['render_lengths']['gap'], 1)

    def test_duplicate_coverage_withholds_unique_pair(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1), cell('s2', 'solid', 0, 1),
                                           cell('d', 'dash', 0, 1, y=5)])
        self.assertEqual(result['segments'][0]['status'], 'overlapping_candidate_coverage')
        self.assertEqual(result['segments'][0]['solid_refs'], ['s1', 's2'])
        self.assertEqual(result['segments'][0]['overlapping_routes'], ['solid'])
        self.assertEqual(result['own_candidate_render_lengths']['solid'], 1)

    def test_one_style_multiple_rows_has_overlap_flag(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1), cell('s2', 'solid', 0, 1, y=3)])
        self.assertEqual(result['segments'][0]['status'], 'solid_only')
        self.assertEqual(result['segments'][0]['overlapping_routes'], ['solid'])

    def test_same_native_cell_shared_ink(self):
        result = check.midpoint_partition([cell('s', 'solid', 0, 1), cell('d', 'dash', 0, 1)])
        self.assertEqual(result['segments'][0]['status'], 'shared_ink_ownership_conflict')
        self.assertEqual(result['segments'][0]['shared_ink_conflicts'], [['s', 'd']])
        self.assertEqual(result['render_lengths']['paired_local_candidate'], 0)

    def test_touching_native_rectangles_do_not_share_cell(self):
        self.assertFalse(check.native_intersection(cell('s', 'solid', 0, 1), cell('d', 'dash', 0, 1, y=2)))

    def test_cross_strip_same_native_indices_not_shared(self):
        result = check.midpoint_partition([cell('s', 'solid', 0, 1, source='Im2'),
                                           cell('d', 'dash', 0, 1, source='Im3')])
        self.assertEqual(result['segments'][0]['status'], 'paired_local_candidate')
        self.assertEqual(result['paired_runs'][0]['body_pair'][0][1], 'Im2')

    def test_internal_boundary_retained_but_same_body_grouped(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1), cell('s2', 'solid', 1, 2),
                                           cell('d', 'dash', 0, 2, y=5)])
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['paired_runs'][0]['segment_indices'], [0, 1])

    def test_fragment_change_not_grouped(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1),
                                           cell('s2', 'solid', 1, 2, body=['reader', 'Im3', 'new']),
                                           cell('d', 'dash', 0, 2, y=5)])
        self.assertEqual(len(result['paired_runs']), 2)

    def test_source_region_change_not_grouped(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1),
                                           cell('s2', 'solid', 1, 2, body=['other-region-reader', 'Im3', 'solid-fragment']),
                                           cell('d', 'dash', 0, 2, y=5)])
        self.assertEqual(len(result['paired_runs']), 2)

    def test_reused_label_after_gap_not_continuity(self):
        result = check.midpoint_partition([cell('s1', 'solid', 0, 1), cell('s2', 'solid', 2, 3),
                                           cell('d', 'dash', 0, 3, y=5)])
        self.assertEqual(len(result['paired_runs']), 2)
        self.assertEqual(result['render_lengths']['dash_only'], 1)

    def test_partition_rejects_bad_ids_and_rectangles(self):
        good = cell('s', 'solid', 0, 1)
        with self.assertRaises(ValueError):
            check.midpoint_partition([good, good])
        for field, value in [('render_x', [0, 0]), ('render_x', [1, 0]), ('render_x', [False, 1]),
                             ('render_x', [0.0, 1]), ('native_rectangle', [0, 1, 0, 2]),
                             ('native_rectangle', [0, 1, 1, True]), ('body', ['', 'Im3', 'f'])]:
            with self.subTest(field=field, value=value):
                bad = dict(good, **{field: value})
                with self.assertRaises(ValueError):
                    check.midpoint_partition([bad])

    def test_shared_axis_vertex_bounds(self):
        self.assertEqual(check.bounds_by_vertices(2, axes()), [Q(8, 25), Q(2, 5)])
        self.assertEqual(check.bounds_by_vertices(0, axes()), [0, 0])

    def test_axis_rejects_invalid_intervals_and_boolean(self):
        for box in ({'L': [0, 1], 'R': [1, 10]}, {'L': [1, 0], 'R': [9, 10]},
                    {'L': [0, 1], 'R': [10, 9]}, {'L': [False, 1], 'R': [9, 10]}):
            with self.subTest(box=box), self.assertRaises(ValueError):
                check.bounds_by_vertices(1, box)
        with self.assertRaises(ValueError):
            check.bounds_by_vertices(-1, axes())

    def test_marginal_hull_overlap_does_not_create_source_overlap(self):
        # Common translation t in [-2,2] produces overlapping marginal hulls
        # [-2,3] and [0,5]; at every single t, the source gap is still one unit.
        self.assertLessEqual(max(-2, 0), min(3, 5))
        result = check.midpoint_partition([cell('s', 'solid', 0, 1), cell('d', 'dash', 2, 3, y=5)])
        self.assertEqual(result['render_lengths']['paired_local_candidate'], 0)

    def test_scenario_check_rejects_mutated_geometry_or_acceptance(self):
        candidates = [cell('s', 'solid', 0, 1), cell('d', 'dash', 0, 1, y=5)]
        result = check.midpoint_partition(candidates)
        result.update(solid_reader='primary', dash_reader='peer',
                      conditional_candidate_length_m={'F-root': check.bounds_by_vertices(1, axes())},
                      actual_D=None, candidate_set='C_H', human_accepted=False)
        result = check.normalize(result)
        check.scenario_check(result, candidates, 'F3', 'primary', 'peer', {'F-root': axes()})
        for mutation in ('accepted', 'refs', 'length', 'body', 'conflict'):
            bad = copy.deepcopy(result)
            if mutation == 'accepted': bad['human_accepted'] = True
            if mutation == 'refs': bad['segments'][0]['solid_refs'] = []
            if mutation == 'length': bad['render_lengths']['paired_local_candidate'] = '2'
            if mutation == 'body': bad['paired_runs'][0]['body_pair'][0][2] = 'invented'
            if mutation == 'conflict': bad['segments'][0]['shared_ink_conflicts'] = [['s', 'd']]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                check.scenario_check(bad, candidates, 'F3', 'primary', 'peer', {'F-root': axes()})


class PreservationControls(unittest.TestCase):
    def test_copy_only_membership_rename(self):
        row = {'x': 2, 'core': [3], 'fringe': [4], 'fragment_id': 'a',
               'fragment_membership': [{'fragment_id': 'a', 'core': [3], 'fringe': [4]}]}
        original = {'routes': {'solid': [row], 'dash': []}, 'unassigned_bands': [{'id': 'unassigned'}]}
        before = copy.deepcopy(original)
        changed = check.copy_source(original)
        self.assertEqual(original, before)
        self.assertEqual(changed['routes']['solid'][0]['fragments'], row['fragment_membership'])
        self.assertNotIn('fragment_membership', changed['routes']['solid'][0])
        self.assertEqual(changed['unassigned_bands'], original['unassigned_bands'])
        changed['routes']['solid'][0]['fragments'][0]['core'].append(5)
        self.assertEqual(original, before)

    def test_ambiguous_or_overlapping_membership_rejected(self):
        row = {'x': 2, 'core': [3], 'fringe': [], 'fragment_membership': []}
        for amendment in ({'fragments': []}, {'fragment_membership': {}},
                          {'fragment_membership': [{'core': [3], 'fringe': []}, {'core': [], 'fringe': [3]}]}):
            with self.subTest(amendment=amendment), self.assertRaises(ValueError):
                check.copy_source({'routes': {'solid': [dict(row, **amendment)], 'dash': []}})

    def test_pinned_independent_helper_identity_and_controls(self):
        helper = check.prior_helper()
        self.assertEqual(len(helper.manual_checks()), 12)

    def test_pin_shape_rejects_boolean_size_and_bad_sha(self):
        for value in ({'bytes': True, 'sha256': '0'*64}, {'bytes': -1, 'sha256': '0'*64},
                      {'bytes': 1, 'sha256': 'wrong'}, {'bytes': 1, 'sha256': '0'*64, 'extra': 1}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                check.require_pin_shape(value)

    def test_every_required_dependency_omission_rejected(self):
        required = {name: {'bytes': 0, 'sha256': '0'*64} for name in ('one', 'two', 'three')}
        check.check_required_pins(required, required)
        for name in required:
            missing = dict(required)
            del missing[name]
            with self.subTest(name=name), self.assertRaises(ValueError):
                check.check_required_pins(missing, required)

    def test_owner_relative_pins_are_normalized_and_changed_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'source.json'
            check.save_exclusive(path, {'observed': 1})
            expected = check.pin(path)
            got = {}
            check.include_map(got, {'source.json': expected}, Path(directory))
            self.assertEqual(got, {os.path.relpath(path.resolve(), check.BASE): expected})
            wrong = dict(expected, bytes=expected['bytes']+1)
            with self.assertRaises(ValueError):
                check.include_map({}, {'source.json': wrong}, Path(directory))

    def test_exclusive_receipt_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'receipt.json'
            check.save_exclusive(path, {'status': 'synthetic'})
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                check.save_exclusive(path, {'status': 'replacement'})
            self.assertEqual(path.read_bytes(), original)

    def test_downstream_acceptance_and_boolean_version_rejected(self):
        good = {'status': 'conditional_candidate_geometry_not_admitted_support', 'version': 1,
                'human_accepted': False, 'shared_axis_parameters': True,
                'assumptions': ['Hidentity', 'Hsupport', 'Hink0'],
                'actual_D': None, 'quantile_targets': None, 'model_discrepancies': None}
        check.acceptance_guards(good)
        for key, value in [('version', True), ('human_accepted', True), ('actual_D', []),
                           ('quantile_targets', [0]), ('shared_axis_parameters', False)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                check.acceptance_guards(dict(good, **{key: value}))


if __name__ == '__main__':
    unittest.main()
