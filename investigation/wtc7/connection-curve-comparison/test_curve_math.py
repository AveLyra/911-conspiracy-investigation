"""Synthetic, exact hand-expected controls; no historical inputs or graphics."""

from fractions import Fraction as Q
import unittest

from curve_math import (
    ORDER_TAG, PURE_DISSIPATION_IDENTITY, SUPPORT_TAG, SupportedBranch,
    compare_curves, conditional_pure_dissipation_residual, mn_m_to_nm, ordered_area,
)


def branch(name, points):
    return SupportedBranch(name, SUPPORT_TAG, points)


def compare(ref, cand, *, x_axis=(0, 1), y_axis=(0, 2)):
    return compare_curves((branch("reference", ref),), (branch("candidate", cand),),
                          x_axis=x_axis, y_axis=y_axis)


class ExactDifferenceTests(unittest.TestCase):
    def test_different_sampling_same_linear_function(self):
        result = compare([(0, 0), (1, 1)], [(0, 0), (Q(1, 7), Q(1, 7)), (1, 1)])
        for field in ("signed_difference_area", "absolute_difference_area",
                      "squared_difference_integral", "normalized_mean_absolute"):
            self.assertEqual(result[field], 0)
        self.assertEqual(result["reference_area"], Q(1, 2))
        self.assertEqual(result["candidate_area"], Q(1, 2))
        self.assertEqual(result["reference_peak_common"], {"value": Q(1), "locations": ((Q(1), Q(1)),)})

    def test_sign_cancellation_has_nonzero_absolute_and_squared_error(self):
        result = compare([(0, 1), (1, 1)], [(0, 0), (1, 2)])
        self.assertEqual(result["reference_area"], 1)
        self.assertEqual(result["candidate_area"], 1)
        self.assertEqual(result["signed_difference_area"], 0)
        self.assertEqual(result["absolute_difference_area"], Q(1, 2))
        self.assertEqual(result["squared_difference_integral"], Q(1, 3))
        self.assertEqual(result["normalized_mean_absolute"], Q(1, 4))
        self.assertEqual(result["normalized_mean_squared"], Q(1, 12))
        self.assertEqual(result["interior_zero_crossings"], (Q(1, 2),))
        self.assertEqual(len(result["pieces"]), 2)
        self.assertEqual(result["maximum_absolute_difference"],
                         {"value": Q(1), "locations": ((Q(0), Q(0)), (Q(1), Q(1)))})
        self.assertEqual(result["reference_peak_common"]["locations"], ((Q(0), Q(1)),))

    def test_zero_reference_is_finite_without_epsilon(self):
        eps = Q(1, 10**20)
        result = compare([(0, 0), (1, 0)], [(0, eps), (1, eps)], y_axis=(0, 1))
        self.assertEqual(result["signed_mean"], eps)
        self.assertEqual(result["normalized_mean_absolute"], eps)
        self.assertEqual(result["normalized_mean_squared"], eps * eps)
        self.assertEqual(result["maximum_absolute_difference"]["locations"], ((Q(0), Q(1)),))

    def test_narrow_spike_not_missed_by_sampling(self):
        lo, mid, hi = Q(499, 1000), Q(1, 2), Q(501, 1000)
        result = compare([(0, 0), (1, 0)], [(0, 0), (lo, 0), (mid, 2), (hi, 0), (1, 0)])
        self.assertEqual(result["absolute_difference_area"], Q(1, 500))
        self.assertEqual(result["squared_difference_integral"], Q(1, 375))
        self.assertEqual(result["candidate_peak_common"], {"value": Q(2), "locations": ((mid, mid),)})

    def test_negative_signed_difference_retained(self):
        result = compare([(0, 2), (1, 2)], [(0, 0), (1, 0)])
        self.assertEqual(result["signed_difference_area"], -2)
        self.assertEqual(result["absolute_difference_area"], 2)
        self.assertEqual(result["normalized_signed_mean"], -1)
        self.assertEqual(result["normalized_mean_squared"], 1)

    def test_signed_axes_are_supported(self):
        result = compare([(-1, -1), (1, 1)], [(-1, 1), (1, -1)], x_axis=(-1, 1), y_axis=(-1, 1))
        self.assertEqual(result["signed_difference_area"], 0)
        self.assertEqual(result["absolute_difference_area"], 2)
        self.assertEqual(result["squared_difference_integral"], Q(8, 3))
        self.assertEqual(result["interior_zero_crossings"], (Q(0),))

    def test_changed_axis_changes_normalization_not_arithmetic(self):
        args = ([(0, 1), (1, 1)], [(0, 0), (1, 2)])
        small = compare(*args)
        large = compare(*args, x_axis=(0, 2), y_axis=(0, 4))
        self.assertEqual(large["absolute_difference_area"], small["absolute_difference_area"])
        self.assertEqual(large["normalized_mean_absolute"], small["normalized_mean_absolute"] / 2)
        self.assertEqual(large["normalized_mean_squared"], small["normalized_mean_squared"] / 4)
        self.assertEqual(large["coverage_nominal"], 1)
        self.assertEqual(large["coverage_axis"], Q(1, 2))

    def test_zero_at_existing_knot_does_not_add_false_crossing(self):
        result = compare([(0, 1), (Q(1, 2), 1), (1, 1)], [(0, 0), (Q(1, 2), 1), (1, 2)])
        self.assertEqual(result["absolute_difference_area"], Q(1, 2))
        self.assertEqual(result["squared_difference_integral"], Q(1, 3))
        self.assertEqual(result["interior_zero_crossings"], ())
        self.assertEqual(len(result["pieces"]), 2)


class SupportTests(unittest.TestCase):
    def test_disjoint_support_never_fills_gap(self):
        ref = (branch("left", [(0, 1), (Q(2, 5), 1)]),
               branch("right", [(Q(3, 5), 1), (1, 1)]))
        cand = (branch("whole", [(0, 2), (1, 2)]),)
        result = compare_curves(ref, cand, x_axis=(0, 1), y_axis=(0, 2))
        self.assertEqual(result["common_intervals"], ((Q(0), Q(2, 5)), (Q(3, 5), Q(1))))
        self.assertEqual(result["common_length"], Q(4, 5))
        self.assertEqual(result["coverage_nominal"], Q(4, 5))
        self.assertEqual(result["coverage_axis"], Q(4, 5))
        self.assertEqual(result["signed_difference_area"], Q(4, 5))
        self.assertEqual(result["reference_area"], Q(4, 5))
        self.assertEqual(result["candidate_area"], Q(8, 5))
        self.assertEqual(result["candidate_peak_common"]["locations"], result["common_intervals"])
        self.assertEqual(result["reference_support"], result["common_intervals"])
        self.assertEqual(result["candidate_support"], ((Q(0), Q(1)),))
        self.assertEqual(result["area_scope"], "joint-supported-domain-only")

    def test_common_peak_excludes_unshared_high_tail(self):
        result = compare([(0, 0), (1, 1)], [(Q(1, 4), 0), (Q(3, 4), 0)])
        self.assertEqual(result["common_intervals"], ((Q(1, 4), Q(3, 4)),))
        self.assertEqual(result["reference_peak_common"]["value"], Q(3, 4))
        self.assertEqual(result["reference_peak_own"]["value"], 1)
        self.assertEqual(result["reference_peak_own"]["locations"], ((Q(1), Q(1)),))
        self.assertEqual(result["reference_terminal_supported"], (Q(1), Q(1)))
        self.assertEqual(result["candidate_terminal_supported"], (Q(3, 4), Q(0)))
        self.assertEqual(result["common_terminal_supported"], (Q(3, 4), Q(3, 4), Q(0)))
        self.assertEqual(result["reference_area"], Q(1, 4))
        self.assertEqual(result["common_length"], Q(1, 2))
        self.assertEqual(result["coverage_nominal"], 1)
        self.assertEqual(result["coverage_axis"], Q(1, 2))

    def test_no_common_interval_rejected_including_endpoint_only(self):
        for second in ([(1, 0), (2, 0)], [(Q(3, 2), 0), (2, 0)]):
            with self.subTest(second=second), self.assertRaises(ValueError):
                compare([(0, 0), (1, 0)], second, x_axis=(0, 2))

    def test_crossed_disjoint_branches_have_exact_joint_coverage(self):
        ref = (branch("a", [(0, 1), (2, 1)]), branch("b", [(3, 1), (5, 1)]))
        cand = (branch("c", [(1, 0), (4, 0)]),)
        result = compare_curves(ref, cand, x_axis=(0, 5), y_axis=(0, 2))
        self.assertEqual(result["common_intervals"], ((Q(1), Q(2)), (Q(3), Q(4))))
        self.assertEqual(result["coverage_nominal"], Q(2, 3))
        self.assertEqual(result["coverage_axis"], Q(2, 5))
        self.assertEqual(result["signed_difference_area"], -2)

    def test_overlapping_touching_or_unsorted_branches_rejected(self):
        first = branch("a", [(0, 0), (1, 0)])
        for second in (branch("b", [(Q(1, 2), 0), (2, 0)]),
                       branch("b", [(1, 0), (2, 0)]),
                       branch("b", [(-2, 0), (-1, 0)])):
            with self.subTest(second=second), self.assertRaises(ValueError):
                compare_curves((first, second), (first,), x_axis=(-2, 2), y_axis=(0, 2))

    def test_repeated_branch_names_rejected(self):
        a, b = branch("same", [(0, 0), (1, 0)]), branch("same", [(2, 0), (3, 0)])
        with self.assertRaises(ValueError):
            compare_curves((a, b), (a,), x_axis=(0, 3), y_axis=(0, 2))


class OrderedAreaAndEnergyTests(unittest.TestCase):
    def test_backtracking_is_not_sorted(self):
        self.assertEqual(ordered_area([(0, 0), (1, 1), (0, 0)], order_tag=ORDER_TAG), 0)
        self.assertEqual(ordered_area([(0, 0), (1, 2), (0, 1)], order_tag=ORDER_TAG), Q(-1, 2))

    def test_vertical_drop_is_not_averaged_to_ramp(self):
        self.assertEqual(ordered_area([(0, 0), (1, 1), (1, 0), (2, 0)], order_tag=ORDER_TAG), Q(1, 2))
        self.assertEqual(ordered_area([(1, 0), (1, 2)], order_tag=ORDER_TAG), 0)

    def test_repeated_ordered_vertex_contributes_zero_without_deletion(self):
        self.assertEqual(ordered_area([(0, 0), (1, 1), (1, 1), (2, 0)],
                                     order_tag=ORDER_TAG), 1)

    def test_unknown_path_order_rejected(self):
        for tag in ("unknown", "", None, True):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                ordered_area([(0, 0), (1, 1)], order_tag=tag)

    def test_unit_conversion_is_exact(self):
        self.assertEqual(mn_m_to_nm(1), 1_000_000)
        self.assertEqual(mn_m_to_nm(Q(1, 3)), Q(1_000_000, 3))
        self.assertEqual(mn_m_to_nm(-1), -1_000_000)

    def test_elastic_work_does_not_establish_dissipation(self):
        work = ordered_area([(0, 0), (1, 1)], order_tag=ORDER_TAG)
        self.assertEqual(work, Q(1, 2))
        with self.assertRaises(ValueError):
            conditional_pure_dissipation_residual(work, 0, identity="linear-elastic-stored-energy")
        # A caller could deliberately stipulate a false physical identity.
        # The returned conditional residual is arithmetic, not validation.
        self.assertEqual(conditional_pure_dissipation_residual(work, 0,
                         identity=PURE_DISSIPATION_IDENTITY), Q(-1, 2))

    def test_pure_dissipation_is_only_a_stipulated_toy_identity(self):
        work = ordered_area([(0, 2), (1, 2)], order_tag=ORDER_TAG)
        self.assertEqual(conditional_pure_dissipation_residual(work, 2,
                         identity=PURE_DISSIPATION_IDENTITY), 0)
        for identity in (None, "unknown", "D=W", True):
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                conditional_pure_dissipation_residual(work, 2, identity=identity)


class InvalidInputTests(unittest.TestCase):
    def test_nonexact_nonfinite_and_boolean_numbers_rejected_every_numeric_route(self):
        for bad in (True, False, float("nan"), float("inf"), -float("inf"), 0.5, "1/2", None):
            with self.subTest(bad=repr(bad)):
                with self.assertRaises(ValueError):
                    branch("bad", [(0, 0), (1, bad)])
                with self.assertRaises(ValueError):
                    branch("bad", [(0, 0), (bad, 1)])
                with self.assertRaises(ValueError):
                    compare([(0, 0), (1, 0)], [(0, 0), (1, 0)], y_axis=(0, bad))
                with self.assertRaises(ValueError):
                    ordered_area([(0, 0), (1, bad)], order_tag=ORDER_TAG)
                with self.assertRaises(ValueError):
                    mn_m_to_nm(bad)
                with self.assertRaises(ValueError):
                    conditional_pure_dissipation_residual(0, bad, identity=PURE_DISSIPATION_IDENTITY)

    def test_invalid_monotone_domain_rejected(self):
        for points in ([], [(0, 0)], [(0, 0), (0, 1)], [(1, 0), (0, 1)],
                       [(0, 0), (1, 1), (0, 0)], [(0, 0), (0, 0), (1, 1)]):
            with self.subTest(points=points), self.assertRaises(ValueError):
                branch("bad", points)

    def test_unknown_support_and_missing_identity_rejected(self):
        for tag in ("unknown", "inferred-through-gap", None, True):
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                SupportedBranch("bad", tag, [(0, 0), (1, 1)])
        for name in ("", "  ", None, True):
            with self.subTest(name=name), self.assertRaises(ValueError):
                branch(name, [(0, 0), (1, 1)])

    def test_zero_reversed_and_malformed_axes_rejected(self):
        for axis in ((0, 0), (1, 0), (), (0,), (0, 1, 2), "0,1"):
            with self.subTest(axis=axis):
                with self.assertRaises(ValueError):
                    compare([(0, 0), (1, 0)], [(0, 0), (1, 0)], x_axis=axis)
                with self.assertRaises(ValueError):
                    compare([(0, 0), (1, 0)], [(0, 0), (1, 0)], y_axis=axis)

    def test_outside_axis_support_rejected_not_clipped_silently(self):
        for x_axis, y_axis in (((0, Q(1, 2)), (0, 2)), ((0, 1), (0, Q(1, 2)))):
            with self.subTest(x_axis=x_axis, y_axis=y_axis), self.assertRaises(ValueError):
                compare([(0, 0), (1, 1)], [(0, 0), (1, 1)], x_axis=x_axis, y_axis=y_axis)

    def test_missing_or_malformed_curves_rejected(self):
        valid = (branch("valid", [(0, 0), (1, 1)]),)
        for invalid in ((), [], None, "curve", ((0, 0), (1, 1))):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                compare_curves(invalid, valid, x_axis=(0, 1), y_axis=(0, 2))
        for points in (None, "points", [(0,), (1, 1)], [(0, 0, 0), (1, 1)]):
            with self.subTest(points=points), self.assertRaises(ValueError):
                ordered_area(points, order_tag=ORDER_TAG)


if __name__ == "__main__":
    unittest.main()
