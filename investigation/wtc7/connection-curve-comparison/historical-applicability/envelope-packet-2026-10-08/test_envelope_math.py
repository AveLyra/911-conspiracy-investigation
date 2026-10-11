"""Synthetic exact controls only; not source mapping or historical acceptance."""
from fractions import Fraction as Q
import unittest

from envelope_math import (Interval as I, Cell, Scenario, AxisBox,
                           difference_page, compare_envelopes,
                           reader_robust_sign, require_same_domain)


def cell(x=(0, 1), spring=(10, 12), shell=(4, 5)):
    return Cell(I(*x), I(*spring), I(*shell))


def scenario(*cells, panel="force", pair="toy", frame="toy-page"):
    return Scenario(pair, panel, frame, cells)


def axis(left=(0, 0), right=(Q(8, 5), Q(8, 5)), top=(0, 0),
         bottom=(1_000_000, 1_000_000), frame="toy-page"):
    return AxisBox(frame, I(*left), I(*right), I(*top), I(*bottom))


class ExactArithmetic(unittest.TestCase):
    def test_exact_positive_case_and_rendered_y_orientation(self):
        c = cell(x=(0, 2))  # width 2, shell minus spring is [5,8]
        self.assertEqual(difference_page(c), I(5, 8))
        r = compare_envelopes(scenario(c), axis())
        self.assertEqual(r["integrals"], {"signed": I(10, 16), "absolute": I(10, 16),
                                           "squared": I(50, 128)})
        self.assertEqual(r["means"], {"signed": I(5, 8), "absolute": I(5, 8),
                                       "squared": I(25, 64)})
        self.assertEqual(r["domain_length"], I(2, 2))
        self.assertFalse(r["human_accepted"])

    def test_reversed_models_reverse_signed_only(self):
        c = cell()
        positive = compare_envelopes(scenario(c), axis())
        negative = compare_envelopes(scenario(Cell(c.x, c.shell_y, c.spring_y)), axis())
        self.assertEqual(negative["integrals"]["signed"], I(-8, -5))
        for kind in ("absolute", "squared"):
            self.assertEqual(positive["integrals"][kind], negative["integrals"][kind])

    def test_zero_straddling_and_touch(self):
        for spring, shell, signed, absolute, squared in (
            ((2, 4), (1, 3), (-1, 3), (0, 3), (0, 9)),
            ((2, 4), (0, 2), (0, 4), (0, 4), (0, 16)),
            ((0, 2), (2, 4), (-4, 0), (0, 4), (0, 16)),
            ((2, 2), (2, 2), (0, 0), (0, 0), (0, 0)),
        ):
            s = scenario(cell(spring=spring, shell=shell))
            r = compare_envelopes(s, axis())
            self.assertEqual(r["integrals"], {"signed": I(*signed),
                                               "absolute": I(*absolute), "squared": I(*squared)})
            self.assertIsNone(reader_robust_sign({"one": s}, Q(1, 2))["sign"])

    def test_signed_cancellation_preserves_absolute_and_squared(self):
        s = scenario(cell((0, 1), (3, 3), (1, 1)),
                     cell((2, 3), (1, 1), (3, 3)))
        r = compare_envelopes(s, axis(bottom=(500_000, 1_000_000)))
        self.assertEqual(r["integrals"]["signed"], I(0, 0))
        self.assertEqual(r["integrals"]["absolute"], I(4, 8))
        self.assertEqual(r["integrals"]["squared"], I(8, 32))
        self.assertEqual(r["means"]["absolute"], I(2, 4))
        self.assertEqual(r["means"]["squared"], I(4, 16))

    def test_shared_axis_vertices_and_negative_sum(self):
        # kx in [2/15, 1/5], ky in [1/4, 1/2]. Complete-box extrema.
        a = axis((0, 2), (10, 12), (0, 1_000_000), (3_000_000, 4_000_000))
        s = scenario(cell((0, 3), (1, 2), (4, 5)))  # page integral [-12,-6]
        r = compare_envelopes(s, a)
        self.assertEqual(r["axis_vertices_evaluated"], 16)
        self.assertEqual(r["domain_length"], I(Q(2, 5), Q(3, 5)))
        self.assertEqual(r["integrals"], {"signed": I(Q(-6, 5), Q(-1, 5)),
                                           "absolute": I(Q(1, 5), Q(6, 5)),
                                           "squared": I(Q(1, 10), Q(12, 5))})
        self.assertEqual(r["means"], {"signed": I(-2, Q(-1, 2)),
                                       "absolute": I(Q(1, 2), 2), "squared": I(Q(1, 4), 4)})

    def test_means_cancel_horizontal_axis_factor(self):
        s = scenario(cell())
        narrow = compare_envelopes(s, axis(right=(10, 20)))
        wide = compare_envelopes(s, axis(left=(-100, -20), right=(50, 80)))
        self.assertEqual(narrow["means"], wide["means"])
        self.assertNotEqual(narrow["integrals"], wide["integrals"])

    def test_shared_offsets_cancel_before_hulls(self):
        s = scenario(cell())
        shifted = scenario(cell((100, 101), (1010, 1012), (1004, 1005)))
        base = compare_envelopes(s, axis())
        translated = compare_envelopes(shifted, axis((100, 100), (Q(508, 5), Q(508, 5)),
                                                      (1000, 1000), (1_001_000, 1_001_000)))
        self.assertEqual(base["integrals"], translated["integrals"])
        self.assertEqual(base["means"], translated["means"])
        # Even an uncertain B (hence physical offset ky*B) does not add a
        # separate offset uncertainty to the difference: only ky appears.
        r = compare_envelopes(s, axis(bottom=(1_000_000, 2_000_000)))
        self.assertEqual(r["means"]["signed"], I(Q(5, 2), 8))

    def test_disjoint_gaps_not_integrated_and_missing_tails_not_extrapolated(self):
        cells = (cell((Q(1, 10), Q(1, 5)), (1, 1), (0, 0)),
                 cell((Q(4, 5), Q(9, 10)), (1, 1), (0, 0)))
        r = compare_envelopes(scenario(*cells), axis())
        self.assertEqual(r["domain_page"], tuple(c.x for c in cells))
        self.assertEqual(r["page_length"], Q(1, 5))
        self.assertEqual(r["integrals"]["signed"], I(Q(1, 5), Q(1, 5)))
        self.assertEqual(r["means"]["signed"], I(1, 1))

    def test_force_and_energy_have_fixed_scales_and_distinct_units(self):
        force = compare_envelopes(scenario(cell()), axis())
        energy = compare_envelopes(scenario(cell(), panel="energy"), axis())
        self.assertEqual(force["means"]["signed"], I(5, 8))
        self.assertEqual(energy["means"]["signed"], I(4, Q(32, 5)))
        self.assertEqual(force["units"]["integrals"]["signed"], "N-m")
        self.assertEqual(energy["units"]["integrals"]["signed"], "N-m^2")
        self.assertEqual(energy["units"]["integrals"]["squared"], "N^2-m^3")
        self.assertEqual(energy["units"]["means"]["squared"], "N^2-m^2")

    def test_empty_is_unavailable_not_zero_agreement(self):
        r = compare_envelopes(scenario(), axis())
        self.assertEqual(r["status"], "unavailable-empty-domain")
        self.assertIsNone(r["integrals"])
        self.assertIsNone(r["means"])
        self.assertEqual(r["domain_length"], I(0, 0))


class AlternativeControls(unittest.TestCase):
    def test_same_position_strict_positive_and_negative(self):
        for spring, shell, sign in [((3, 4), (0, 1), "positive"),
                                    ((0, 1), (3, 4), "negative")]:
            a = scenario(cell((0, 2), spring, shell))
            b = scenario(cell((Q(1, 2), 3), spring, shell))
            r = reader_robust_sign({"primary": a, "peer": b}, 1)
            self.assertEqual(r["sign"], sign)
            # Local common-position eligibility does not make aggregates comparable.
            with self.assertRaisesRegex(ValueError, "changed comparison domain"):
                require_same_domain({"primary": a, "peer": b})

    def test_missing_alternative_or_changed_coverage_never_agrees(self):
        primary = scenario(cell())
        for other, state in [(None, "alternative-unavailable"),
                             (scenario(), "outside-coverage"),
                             (scenario(cell((2, 3))), "outside-coverage")]:
            alternatives = {"primary": primary, "peer": other}
            r = reader_robust_sign(alternatives, Q(1, 2))
            self.assertIsNone(r["sign"])
            self.assertEqual(r["alternatives"]["peer"]["status"], state)
            with self.assertRaises(ValueError):
                require_same_domain(alternatives)

    def test_unresolved_boundaries_including_adjacent_open_cells(self):
        s = scenario(cell(), cell((1, 2)))
        for x in (0, 1, 2):
            r = reader_robust_sign({"a": s}, x)
            self.assertIsNone(r["sign"])
            self.assertEqual(r["alternatives"]["a"]["status"], "boundary-unresolved")
        with self.assertRaises(ValueError):
            require_same_domain({"a": s, "b": scenario(cell((0, 2)))})

    def test_disagreement_and_identical_domain(self):
        a = scenario(cell())
        b = scenario(cell(spring=(4, 5), shell=(10, 12)))
        self.assertEqual(require_same_domain({"a": a, "b": b}), (I(0, 1),))
        self.assertIsNone(reader_robust_sign({"a": a, "b": b}, Q(1, 2))["sign"])


class ValidationControls(unittest.TestCase):
    def test_non_exact_types_including_bool_nonfinite_and_strings_rejected(self):
        for value in (True, False, 1.0, float("inf"), float("nan"), "1", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                I(value, 2)

    def test_reversed_zero_overlap_backtracking_and_unspecified_cells(self):
        for operation in (lambda: I(2, 1), lambda: cell((1, 1)),
                          lambda: scenario(cell(), cell((Q(1, 2), 2))),
                          lambda: scenario(cell((2, 3)), cell()),
                          lambda: scenario(cell(), cell()),
                          lambda: Scenario("toy", "force", "toy-page", [cell()]),
                          lambda: scenario(None), lambda: Cell((0, 1), I(0, 1), I(0, 1))):
            with self.assertRaises(ValueError):
                operation()

    def test_invalid_axis_states_and_units(self):
        for operation in (lambda: axis(left=(0, 2), right=(1, 3)),
                          lambda: axis(top=(0, 1), bottom=(1, 2)),
                          lambda: scenario(cell(), panel="MN"),
                          lambda: scenario(cell(), panel="unspecified-energy"),
                          lambda: scenario(cell(), pair=""),
                          lambda: axis(frame=""),
                          lambda: compare_envelopes(scenario(), axis(frame="other")),
                          lambda: compare_envelopes(None, axis()),
                          lambda: compare_envelopes(scenario(), None)):
            with self.assertRaises(ValueError):
                operation()

    def test_mismatched_alternative_identity_units_or_frame(self):
        a = scenario(cell())
        for b in (scenario(cell(), pair="other"), scenario(cell(), panel="energy"),
                  scenario(cell(), frame="other")):
            for fn in (require_same_domain, lambda alts: reader_robust_sign(alts, Q(1, 2))):
                with self.assertRaises(ValueError):
                    fn({"a": a, "b": b})

    def test_bad_input_not_hidden_by_missing_alternative(self):
        for alternatives in ({}, {"": None}, {"missing": None, "malformed": 7}):
            with self.assertRaises(ValueError):
                reader_robust_sign(alternatives, Q(1, 2))
        with self.assertRaises(ValueError):
            reader_robust_sign({"a": None}, 0.5)
        self.assertIsNone(reader_robust_sign({"a": None, "b": None}, 1)["sign"])


if __name__ == "__main__":
    unittest.main()
