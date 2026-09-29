"""Producer's independently authored exact toy controls; no root oracle import."""
from fractions import Fraction as Q
import unittest

from curve_uncertainty import (SUPPORT_TAG, SharedAxis, SupportedBranch,
                               compare_uncertain, local_envelope)


def curve(points, name='toy'):
    return (SupportedBranch(name, SUPPORT_TAG, points),)


def line(slope=1, offset=0, low=-10, high=10):
    return curve([(low, slope*low+offset), (high, slope*high+offset)])


class LocalControls(unittest.TestCase):
    def test_flat_and_sloping_envelopes_with_y_expansion(self):
        flat = local_envelope(line(0, -3), (-2, 4), y_radius=Q(1, 3))
        self.assertEqual(flat['bounds'], (Q(-10, 3), Q(-8, 3)))
        self.assertEqual(flat['status'], 'resolved')
        self.assertEqual(flat['support'], ((Q(-10), Q(10)),))
        self.assertEqual(local_envelope(line(-2, -1), (-3, 2), y_radius=1)['bounds'], (-6, 6))

    def test_narrow_interior_peak_not_endpoint_only(self):
        c = curve([(0, 0), (Q(499, 1000), 0), (Q(1, 2), 10), (Q(501, 1000), 0), (1, 0)])
        r = local_envelope(c, (Q(1, 4), Q(3, 4)))
        self.assertEqual(r['bounds'], (0, 10))
        self.assertEqual(r['evaluated_x'], (Q(1, 4), Q(499, 1000), Q(1, 2), Q(501, 1000), Q(3, 4)))

    def test_point_query_and_exact_interpolation(self):
        c = curve([(-1, -2), (2, 7)])
        r = local_envelope(c, (Q(1, 3), Q(1, 3)), y_radius=Q(1, 7))
        self.assertEqual(r['bounds'], (Q(13, 7), Q(15, 7)))
        self.assertEqual(r['evaluated_x'], (Q(1, 3),))

    def test_support_edges_and_gaps(self):
        c = (SupportedBranch('left', SUPPORT_TAG, [(0, 0), (1, 1)]),
             SupportedBranch('right', SUPPORT_TAG, [(2, 4), (3, 9)]))
        for query, bounds in [((0, 1), (0, 1)), ((1, 1), (1, 1)), ((2, 3), (4, 9))]:
            self.assertEqual(local_envelope(c, query)['bounds'], bounds)
        for query in [(1, 2), (Q(1, 2), Q(5, 2)), (-1, 0), (3, 4), (Q(3, 2), Q(3, 2))]:
            r = local_envelope(c, query)
            self.assertEqual(r['status'], 'unresolved'); self.assertIsNone(r['bounds'])
            self.assertEqual(r['reason'], 'query-not-fully-supported')
            self.assertEqual(r['support'], ((0, 1), (2, 3)))

    def test_unknown_identity_not_zero(self):
        r = local_envelope(None, (0, 1))
        self.assertEqual(r['status'], 'unresolved')
        self.assertEqual(r['reason'], 'unknown-identity-or-support')
        self.assertIsNone(r['bounds']); self.assertIsNone(r['support'])


class SharedPairControls(unittest.TestCase):
    def setUp(self):
        self.axis = SharedAxis('producer-identity')

    def check_bounds(self, r, expected, sign):
        self.assertEqual(r['status'], 'resolved')
        self.assertEqual(r['bounds'], expected)
        self.assertEqual(r['sign'], sign)
        self.assertEqual(r['failures'], ())
        for witness in r['centerline_extremizers'].values():
            self.assertLessEqual(r['reachable_t'][0], witness['t'])
            self.assertLessEqual(witness['t'], r['reachable_t'][1])
            self.assertLessEqual(abs(witness['u']-witness['t']), r['reference_x_radius'])
            self.assertLessEqual(abs(witness['v']-witness['t']), r['candidate_x_radius'])

    def test_flat_positive_negative_and_exact_zero(self):
        for difference, sign in [(2, 'positive'), (-2, 'negative'), (0, 'unresolved')]:
            r = compare_uncertain(line(0, 1), line(0, 1+difference), (-2, 4), axis=self.axis)
            self.check_bounds(r, (difference, difference), sign)

    def test_positive_and_negative_zero_touch_are_not_strict_signs(self):
        for center, expected in [(1, (0, 2)), (-1, (-2, 0))]:
            r = compare_uncertain(line(0, 0), line(0, center), (0, 0), axis=self.axis, candidate_y_radius=1)
            self.check_bounds(r, expected, 'unresolved')

    def test_unequal_y_radii_before_positive_shared_scale(self):
        axis = SharedAxis('different-y-radii', y_scale=(2, 3))
        r = compare_uncertain(line(0, 1), line(0, 3), (0, 1), axis=axis,
                              reference_y_radius=Q(1, 4), candidate_y_radius=Q(1, 2))
        self.assertEqual(r['ordinate_expanded_bounds'], (Q(5, 4), Q(11, 4)))
        self.check_bounds(r, (Q(5, 2), Q(33, 4)), 'positive')

    def test_common_vertical_offset_cancels_and_is_retained(self):
        axis = SharedAxis('shared-offset', y_offset=(-1_000_000, 1_000_000))
        r = compare_uncertain(line(2, 1), line(2, 4), (-1, 1), axis=axis)
        self.check_bounds(r, (3, 3), 'positive')
        self.assertEqual(r['axis']['y_offset'], (-1_000_000, 1_000_000))
        self.assertEqual(r['axis']['calibration_id'], 'shared-offset')
        self.assertTrue(r['shared_y_offset_cancels'])

    def test_identical_slopes_common_horizontal_offset_cancels(self):
        axis = SharedAxis('shared-x', x_offset=(-2, 3))
        r = compare_uncertain(line(), line(offset=2), (0, 0), axis=axis)
        self.assertEqual(r['reachable_t'], (-2, 3))
        self.check_bounds(r, (2, 2), 'positive')

    def test_different_slopes_common_horizontal_offset_does_not_cancel(self):
        r = compare_uncertain(line(), line(2), (0, 0), axis=SharedAxis('slope-difference', x_offset=(-2, 3)))
        self.check_bounds(r, (-2, 3), 'unresolved')

    def test_identical_centerlines_independent_local_radii_do_not_cancel(self):
        c = line()
        r = compare_uncertain(c, c, (-1, 2), axis=self.axis,
                              reference_x_radius=1, candidate_x_radius=2)
        self.check_bounds(r, (-3, 3), 'unresolved')
        self.assertEqual(r['reference_demand'], (-2, 3))
        self.assertEqual(r['candidate_demand'], (-3, 4))

    def test_unequal_x_y_radii_and_signed_scale(self):
        r = compare_uncertain(line(), line(2), (-1, 2),
                              axis=SharedAxis('rational-radii', y_scale=(Q(1, 2), 2)),
                              reference_x_radius=Q(1, 2), candidate_x_radius=Q(1, 4),
                              reference_y_radius=Q(1, 3), candidate_y_radius=Q(1, 6))
        self.assertEqual(r['centerline_bounds'], (-2, 3))
        self.assertEqual(r['ordinate_expanded_bounds'], (Q(-5, 2), Q(7, 2)))
        self.check_bounds(r, (-5, 7), 'unresolved')

    def test_positive_scale_interval_with_negative_difference(self):
        r = compare_uncertain(line(0, 3), line(0, 0), (0, 0),
                              axis=SharedAxis('negative-difference', y_scale=(2, 4)), candidate_y_radius=1)
        self.check_bounds(r, (-16, -4), 'negative')

    def test_negative_query_horizontal_product_extrema(self):
        r = compare_uncertain(line(0, 0), line(), (-2, -1),
                              axis=SharedAxis('negative-x', x_scale=(1, 2), x_offset=(-1, 1)))
        self.assertEqual(r['reachable_t'], (-5, 0))
        self.check_bounds(r, (-5, 0), 'unresolved')

    def test_rational_point_query_and_all_calibration_terms(self):
        r = compare_uncertain(line(0, 0), line(), (Q(1, 3), Q(1, 3)),
                              axis=SharedAxis('exact-rational', x_scale=(Q(1, 2), Q(3, 2)),
                                              x_offset=(Q(1, 7), Q(1, 7)), y_scale=(Q(2, 3), Q(2, 3))))
        self.assertEqual(r['reachable_t'], (Q(13, 42), Q(9, 14)))
        self.check_bounds(r, (Q(13, 63), Q(3, 7)), 'positive')

    def test_narrow_peak_and_zero_radii_diagonal_degeneracy(self):
        peak = curve([(0, 0), (Q(499, 1000), 0), (Q(1, 2), 10), (Q(501, 1000), 0), (1, 0)])
        r = compare_uncertain(line(0, 0), peak, (0, 1), axis=self.axis)
        self.check_bounds(r, (0, 10), 'unresolved')
        self.assertEqual(r['centerline_extremizers']['maximum']['v'], Q(1, 2))

    def test_point_domain_and_single_variable_line_degeneracy(self):
        peak = curve([(-1, 0), (0, 2), (1, 0)])
        point = compare_uncertain(line(0, 1), peak, (0, 0), axis=self.axis)
        self.check_bounds(point, (1, 1), 'positive')
        spread = compare_uncertain(line(0, 1), peak, (0, 0), axis=self.axis, candidate_x_radius=1)
        self.check_bounds(spread, (-1, 1), 'unresolved')

    def test_shared_t_constraint_excludes_independent_marginal_extremes(self):
        absolute = curve([(-3, 3), (0, 0), (3, 3)])
        r = compare_uncertain(absolute, absolute, (-1, 1), axis=self.axis,
                              reference_x_radius=Q(1, 2), candidate_x_radius=Q(1, 2))
        # Independent marginal subtraction gives a valid but non-tight enclosure
        # [-3/2,3/2]; the shared-t model's exact extrema are [-1,1].
        self.check_bounds(r, (-1, 1), 'unresolved')

    def test_full_demand_required_and_failing_curve_named(self):
        reference = curve([(0, 0), (1, 1)])
        candidate = line()
        r = compare_uncertain(reference, candidate, (0, 1), axis=self.axis, reference_x_radius=Q(1, 10))
        self.assertEqual(r['status'], 'unresolved'); self.assertIsNone(r['bounds']); self.assertIsNone(r['sign'])
        self.assertEqual(r['failures'], ({'curve': 'reference', 'query': (Q(-1, 10), Q(11, 10)),
                                         'reason': 'query-not-fully-supported'},))
        gap = (SupportedBranch('left', SUPPORT_TAG, [(0, 0), (1, 1)]),
               SupportedBranch('right', SUPPORT_TAG, [(2, 2), (3, 3)]))
        r = compare_uncertain(candidate, gap, (1, 2), axis=self.axis)
        self.assertEqual(r['failures'][0]['curve'], 'candidate'); self.assertIsNone(r['bounds'])
        self.check_bounds(compare_uncertain(reference, candidate, (1, 1), axis=self.axis), (0, 0), 'unresolved')

    def test_unknown_curve_never_yields_numeric_pair(self):
        for ref, cand in [(None, line()), (line(), None), (None, None)]:
            r = compare_uncertain(ref, cand, (0, 1), axis=self.axis)
            self.assertEqual(r['status'], 'unresolved'); self.assertIsNone(r['bounds']); self.assertIsNone(r['sign'])
            self.assertTrue(all(f['reason'] == 'unknown-identity-or-support' for f in r['failures']))


class InvalidInputControls(unittest.TestCase):
    def test_axis_must_be_explicit(self):
        for axis in [None, {}, 'shared', True]:
            with self.assertRaises(ValueError): compare_uncertain(None, None, (0, 1), axis=axis)
        with self.assertRaises(TypeError): compare_uncertain(line(), line(), (0, 1))

    def test_closed_intervals_exact_types_and_scale_positivity(self):
        for bad in [True, False, 1.0, float('nan'), float('inf'), '1/2', None]:
            with self.assertRaises(ValueError): local_envelope(None, (0, bad))
            with self.assertRaises(ValueError): local_envelope(None, (0, 1), y_radius=bad)
            for field in ['x_scale', 'x_offset', 'y_scale', 'y_offset']:
                with self.assertRaises(ValueError): SharedAxis('invalid', **{field:(bad, bad)})
        for bad in [(), (0,), (0, 1, 2), '0,1', (1, 0)]:
            with self.assertRaises(ValueError): local_envelope(None, bad)
            with self.assertRaises(ValueError): SharedAxis('invalid', x_offset=bad)
        for bad in [(0, 1), (-1, 1), (-2, -1)]:
            with self.assertRaises(ValueError): SharedAxis('invalid', x_scale=bad)
            with self.assertRaises(ValueError): SharedAxis('invalid', y_scale=bad)
        for name in ['', ' ', None, True]:
            with self.assertRaises(ValueError): SharedAxis(name)

    def test_negative_radii_and_invalid_values_even_when_other_curve_unknown(self):
        fields = ['reference_x_radius', 'candidate_x_radius', 'reference_y_radius', 'candidate_y_radius']
        for field in fields:
            for bad in [-1, True, 0.0, float('nan'), None]:
                with self.assertRaises(ValueError): compare_uncertain(None, line(), (0, 1), axis=SharedAxis('test'), **{field:bad})
        with self.assertRaises(ValueError): local_envelope(None, (0, 1), y_radius=-1)

    def test_malformed_curves_not_short_circuited_by_unknown_partner(self):
        for bad in [[], (), 'curve', True, ((0, 0), (1, 1)), [object()]]:
            with self.assertRaises(ValueError): compare_uncertain(None, bad, (0, 1), axis=SharedAxis('test'))
            with self.assertRaises(ValueError): compare_uncertain(bad, None, (0, 1), axis=SharedAxis('test'))
            with self.assertRaises(ValueError): local_envelope(bad, (0, 1))
        first=SupportedBranch('first',SUPPORT_TAG,[(0,0),(1,1)])
        for second in [SupportedBranch('second',SUPPORT_TAG,[(1,1),(2,2)]),
                       SupportedBranch('second',SUPPORT_TAG,[(Q(1,2),0),(2,2)]),
                       SupportedBranch('first',SUPPORT_TAG,[(2,2),(3,3)])]:
            with self.assertRaises(ValueError): compare_uncertain(None,(first,second),(0,1),axis=SharedAxis('test'))

    def test_invalid_function_branch_is_rejected_by_reused_core(self):
        for points in [[(0,0)],[(0,0),(0,1)],[(1,1),(0,0)],[(0,0),(1,1),(Q(1,2),0)]]:
            with self.assertRaises(ValueError): curve(points)
        for tag in [None,'unknown','bridged-gap',True]:
            with self.assertRaises(ValueError): SupportedBranch('unknown',tag,[(0,0),(1,1)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
