"""Synthetic-only tests for the three prospectively declared clock candidates."""

from fractions import Fraction as F
import unittest

import clock_oracle as oracle


class ClockSyntheticTests(unittest.TestCase):
    def test_fixed_spans(self):
        self.assertEqual([F(12)/rate for _, rate in oracle.CANDIDATES],
                         [F(2, 5), F(1001, 2500), F(400, 999)])

    def test_linear_positions_recover_true_velocity_each_span(self):
        for _, rate in oracle.CANDIDATES:
            span = F(12)/rate
            for velocity in (F(-31), F(-1, 3), F(0), F(17, 2)):
                previous_time = F(27, 5)
                following_time = previous_time+span
                previous_y = F(93)+velocity*previous_time
                following_y = F(93)+velocity*following_time
                result = oracle.derivative_trial(previous_y, following_y, velocity, span)
                self.assertEqual(result["calculated_velocity"], velocity)
                self.assertEqual(result["printed_minus_calculated_velocity"], 0)
                self.assertTrue(result["rounding_compatible"])

    def test_rounding_extrema_and_beyond_bound_each_span(self):
        for _, rate in oracle.CANDIDATES:
            span = F(12)/rate
            velocity = F(-27)
            previous_y = F(100)
            following_y = previous_y+velocity*span
            bound = F(1, 100)/span+F(1, 200)
            for direction in (F(-1), F(1)):
                at_bound = oracle.derivative_trial(previous_y+direction*F(1, 200),
                                                   following_y-direction*F(1, 200),
                                                   velocity+direction*F(1, 200), span)
                self.assertEqual(at_bound["printed_minus_calculated_velocity"], direction*bound)
                self.assertTrue(at_bound["rounding_compatible"])
                outside = oracle.derivative_trial(previous_y+direction*F(1, 200),
                                                  following_y-direction*F(1, 200),
                                                  velocity+direction*(F(1, 200)+F(1, 1000000)), span)
                self.assertFalse(outside["rounding_compatible"])

    def test_translation_invariance(self):
        for _, rate in oracle.CANDIDATES:
            span = F(12)/rate
            original = oracle.derivative_trial(F(100), F(91), F(-20), span)
            translated = oracle.derivative_trial(F(100)+F(23456789, 3),
                                                 F(91)+F(23456789, 3), F(-20), span)
            self.assertEqual(original, translated)

    def test_supported_and_unsupported_membership_each_candidate(self):
        rows = []
        for index in range(3):
            time = F(index, 5)
            row = {"source_row": index+1, "time_s": time}
            for track in oracle.TRACKS:
                row[track+"_y"] = 100-5*time
                row[track+"_v"] = F(-5)
            rows.append(row)
        result = oracle.evaluate_candidates(rows)
        self.assertEqual(result["total_row_candidate_count"], 12)
        self.assertEqual(len(result["unsupported"]), 8)
        for candidate in result["candidate_results"]:
            self.assertEqual(candidate["tested_count"], 4)
            self.assertTrue(all(row["source_row"] == 2 and row["support_source_rows"] == [1, 2, 3]
                                for row in candidate["rows"]))
        with self.assertRaises(ValueError):
            oracle.evaluate_candidates(rows+[rows[0]])

    def test_malformed_inputs_fail(self):
        for span in (F(0), F(-1), 0.4, "0.4", None):
            with self.assertRaises(ValueError):
                oracle.derivative_trial(F(100), F(90), F(-25), span)
        with self.assertRaises(ValueError):
            oracle.derivative_trial(100.0, F(90), F(-25), F(2, 5))


if __name__ == "__main__":
    unittest.main(verbosity=2)
