"""Synthetic-only checks; this module never opens the historical tables."""

from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest

import exact_oracle as oracle


def camera_rows():
    rows = []
    for index in range(70):
        time = F(-1) + F(index, 5)
        row = {"source_row": index+1, "time_s": time}
        for point in oracle.POINTS:
            row[point+"_y"] = F(200) + 3*time - F(5)*time*time
            row[point+"_v"] = 3 - 10*time
        rows.append(row)
    return rows


def western_rows():
    result = []
    for index, time in enumerate(map(F, ("8.00", "8.20", "8.40")), 1):
        row = {"source_row": index, "time_s": time, "reference_point_y": F(10)}
        for point, offset in (("nw_corner", F(0)), ("center", F(4)), ("sw_corner", F(8))):
            row[point+"_y"] = 100-time-offset
            row[point+"_relative_y"] = row[point+"_y"] - row["reference_point_y"]
            if point != "nw_corner":
                row[point+"_adjusted_y"] = row[point+"_relative_y"] + offset
        result.append(row)
    return result


def raw_table(page):
    fields = oracle.FIELDS47 if page == 47 else oracle.FIELDS50
    rows = []
    for index in range(70 if page == 47 else 25):
        time = -1 + index/5 if page == 47 else 8 + index/30
        rows.append({"source_row": index+1, "time_s": f"{time:.2f}",
                     "row_top_pdf_points": index, **{field: "12.00" for field in fields}})
    return {"pdf_page_1based": page, "source_sha256": oracle.SOURCE_SHA256,
            "headers": [{"key": field} for field in fields], "rows": rows}


class ExactFitTests(unittest.TestCase):
    def test_constant_velocity(self):
        times = [F(index, 5) for index in range(10)]
        fit = oracle.exact_fit(times, [F(7)]*10, 1)
        self.assertEqual(fit["coefficients_centered"], [F(7), F(0)])
        self.assertEqual(fit["downward_acceleration"], 0)
        self.assertEqual(fit["sse"], 0)
        self.assertIsNone(fit["r_squared_descriptive"])

    def test_constant_and_linear_positions(self):
        times = [F(index, 5) for index in range(9)]
        for values in ([F(9)]*9, [F(9)-3*time for time in times]):
            fit = oracle.exact_fit(times, values, 2)
            self.assertEqual(fit["downward_acceleration"], 0)
            self.assertEqual(fit["sse"], 0)

    def test_known_line_and_quadratic_even_and_odd(self):
        for count in (3, 4, 7, 10, 13, 24):
            times = [F(31, 7) + F(index, 5) for index in range(count)]
            for degree in (1, 2):
                values = [F(12)-F(49, 5)*time if degree == 1 else
                          F(12) + F(17, 3)*time - F(49, 10)*time*time for time in times]
                fit = oracle.exact_fit(times, values, degree)
                self.assertEqual(fit["downward_acceleration"], F(49, 5))
                self.assertEqual(fit["residuals_observed_minus_fit"], [F(0)]*count)
                expected = [F(12), -F(49, 5)] if degree == 1 else [F(12), F(17, 3), -F(49, 10)]
                self.assertEqual(fit["coefficients_uncentered"], expected)

    def test_hand_derived_small_design_weights(self):
        linear = oracle.exact_fit([F(0), F(1)], [F(2), F(8)], 1)
        self.assertEqual(linear["acceleration_input_weights"], [F(1), F(-1)])
        quadratic = oracle.exact_fit([F(0), F(1), F(2)], [F(2), F(8), F(19)], 2)
        self.assertEqual(quadratic["acceleration_input_weights"], [F(-1), F(2), F(-1)])
        self.assertEqual(quadratic["downward_acceleration"], F(-5))

    def test_rational_noisy_residual_orthogonality(self):
        times = [F(5)+F(index, 5) for index in range(8)]
        values = [F(17-index*index, 7) + F((-1)**index, 13) for index in range(8)]
        for degree in (1, 2):
            fit = oracle.exact_fit(times, values, degree)
            for power in range(degree+1):
                self.assertEqual(sum(residual*(time-fit["time_center"])**power for time, residual in
                                     zip(times, fit["residuals_observed_minus_fit"])), 0)

    def test_time_and_value_translation_invariance(self):
        times = [F(index, 5) for index in range(11)]
        values = [F((index*7)%13, 3) for index in range(11)]
        for degree in (1, 2):
            original = oracle.exact_fit(times, values, degree)
            shifted = oracle.exact_fit([time+F(987654321, 7) for time in times],
                                       [value+F(7654321, 3) for value in values], degree)
            for key in ("downward_acceleration", "acceleration_input_weights",
                        "residuals_observed_minus_fit", "display_rounding_half_width"):
                self.assertEqual(original[key], shifted[key])

    def test_extremal_rounding_witnesses_all_window_sizes(self):
        for count in range(4, 25):
            times = [F(8)+F(index, 5) for index in range(count)]
            values = [F(100)-time*time for time in times]
            for degree in (1, 2):
                nominal = oracle.exact_fit(times, values, degree)
                signs = [F(1) if weight > 0 else F(-1) if weight < 0 else F(0)
                         for weight in nominal["acceleration_input_weights"]]
                for direction in (F(-1), F(1)):
                    perturbed = oracle.exact_fit(times, [value+direction*oracle.HALF_DISPLAY*sign
                                                        for value, sign in zip(values, signs)], degree)
                    self.assertEqual(perturbed["downward_acceleration"]-nominal["downward_acceleration"],
                                     direction*nominal["display_rounding_half_width"])

    def test_basis_response_weights(self):
        times = [F(index, 5) for index in range(7)]
        for degree in (1, 2):
            nominal = oracle.exact_fit(times, [F(0)]*7, degree)
            for index, expected in enumerate(nominal["acceleration_input_weights"]):
                basis = [F(int(row == index)) for row in range(7)]
                self.assertEqual(oracle.exact_fit(times, basis, degree)["downward_acceleration"], expected)

    def test_bad_fit_inputs_fail(self):
        cases = (([F(0), F(1)], [F(1)], 1), ([F(0)], [F(1)], 2),
                 ([F(0), F(0)], [F(1), F(1)], 1), ([F(1), F(0)], [F(1), F(1)], 1),
                 ([0.0, 1.0], [F(1), F(2)], 1), ([F(0), F(1)], [F(1), None], 1),
                 ([F(0), F(1)], [F(1), F(2)], 3))
        for args in cases:
            with self.assertRaises(ValueError):
                oracle.exact_fit(*args)
        with self.assertRaises(ValueError):
            oracle.solve_square([[1, 1], [1, 1]], [2, 2])


class ProtocolTests(unittest.TestCase):
    def test_windows_exact_counts_membership_and_repeated_contrast(self):
        rows = camera_rows()
        windows = oracle.window_definitions(rows)
        self.assertEqual(len(windows), 49)
        self.assertEqual(sum(item[1] == "fixed_grid" for item in windows), 45)
        self.assertEqual(sum(item[-1] for item in windows), 4)
        allfits = oracle.fit_windows(rows)
        self.assertEqual(len(allfits), 98)
        for position in range(0, len(allfits), 2):
            velocity, quadratic = allfits[position:position+2]
            self.assertEqual(velocity["times"], quadratic["times"])
            self.assertEqual(velocity["source_rows"], quadratic["source_rows"])
            self.assertEqual(velocity["n"], 1+int((velocity["end"]-velocity["start"])*5))
            self.assertEqual(velocity["downward_acceleration"], 10)
            self.assertEqual(quadratic["downward_acceleration"], 10)
        missing = deepcopy(rows)
        missing[46]["ne_corner_v"] = None
        with self.assertRaises(ValueError):
            oracle.select_window(missing, "ne_corner", F("8.0"), F("9.2"))
        with self.assertRaises(ValueError):
            oracle.select_window(rows, "ne_corner", F("8.1"), F("9.2"))

    def test_derivative_ground_truth_and_bound_edges(self):
        rows = camera_rows()
        checks = oracle.derivative_check(rows)
        self.assertEqual(sum(item["tested"] for item in checks), 68*4)
        self.assertTrue(all(item["residual_printed_minus_derivative"] == 0 for item in checks if item["tested"]))
        for shift, expected in ((F("0.030"), True), (F("0.030001"), False), (-F("0.030"), True)):
            trial = deepcopy(rows)
            trial[10]["ne_corner_v"] += shift
            chosen = next(item for item in oracle.derivative_check(trial)
                          if item["point"] == "ne_corner" and item["source_row"] == 11)
            self.assertEqual(chosen["within_rounding_bound"], expected)
        # Opposite endpoint rounding errors plus velocity rounding attain 0.030.
        trial = deepcopy(rows)
        trial[9]["ne_corner_y"] += F("0.005")
        trial[11]["ne_corner_y"] -= F("0.005")
        trial[10]["ne_corner_v"] += F("0.005")
        chosen = next(item for item in oracle.derivative_check(trial)
                      if item["point"] == "ne_corner" and item["source_row"] == 11)
        self.assertEqual(chosen["residual_printed_minus_derivative"], F("0.030"))

    def test_western_identity_offsets_translation_and_exact_edges(self):
        rows = western_rows()
        result = oracle.western_check(rows)
        self.assertEqual(result["maximum_absolute_pairwise_difference"], 0)
        self.assertTrue(all(item["within_rounding_bound"] for item in result["subtraction_checks"]))
        self.assertEqual(result["constant_offset_checks"][0]["intersection_lower"], F("3.99"))
        self.assertEqual(result["constant_offset_checks"][0]["intersection_upper"], F("4.01"))
        translated = deepcopy(rows)
        for row in translated:
            row["center_adjusted_y"] += F(30)
        shifted = oracle.western_check(translated)
        self.assertEqual(result["displacements"], shifted["displacements"])
        for discrepancy, expected in ((F("0.015"), True), (F("0.015001"), False)):
            trial = deepcopy(rows)
            trial[0]["nw_corner_relative_y"] += discrepancy
            self.assertEqual(oracle.western_check(trial)["subtraction_checks"][0]["within_rounding_bound"], expected)
        for discrepancy, expected in ((F("0.020"), True), (F("0.020001"), False)):
            trial = deepcopy(rows)
            trial[0]["center_adjusted_y"] += discrepancy
            self.assertEqual(oracle.western_check(trial)["constant_offset_checks"][0]["nonempty_intersection"], expected)
        with self.assertRaises(ValueError):
            oracle.western_check([rows[0], rows[2]])

    def test_western_pairwise_directions_and_maximum(self):
        rows = western_rows()
        rows[2]["center_adjusted_y"] -= F(3)
        result = oracle.western_check(rows)
        self.assertEqual(result["maximum_absolute_pairwise_difference"], 3)
        self.assertEqual(len(result["maximum_locations"]), 2)
        self.assertTrue(all(item["time"] == F("8.4") for item in result["maximum_locations"]))

    def test_decimal_tokens_and_schema_failures(self):
        for value in (1, 1.0, True, "NaN", "Infinity", "1e2", "1/2", "", "+1.0", None):
            with self.assertRaises(ValueError):
                oracle.decimal_token(value)
        self.assertIsNone(oracle.decimal_token(None, allow_null=True))
        for page in (47, 50):
            base = raw_table(page)
            self.assertEqual(len(oracle.validate_table(base, page)), len(base["rows"]))
            trials = []
            bad = deepcopy(base); bad["rows"].pop(); trials.append(bad)
            bad = deepcopy(base); bad["rows"][0]["source_row"] = 2; trials.append(bad)
            bad = deepcopy(base); bad["rows"][1]["time_s"] = bad["rows"][0]["time_s"]; trials.append(bad)
            bad = deepcopy(base); del bad["rows"][0][base["headers"][0]["key"]]; trials.append(bad)
            bad = deepcopy(base); bad["rows"][0][base["headers"][0]["key"]] = 12.0; trials.append(bad)
            bad = deepcopy(base); bad["headers"].reverse(); trials.append(bad)
            bad = deepcopy(base); bad["source_sha256"] = "wrong"; trials.append(bad)
            for trial in trials:
                with self.assertRaises(ValueError):
                    oracle.validate_table(trial, page)
        bad = raw_table(50); bad["rows"][0]["center_y"] = None
        with self.assertRaises(ValueError):
            oracle.validate_table(bad, 50)

    def test_exclusive_output_preserves_prior_file(self):
        with tempfile.TemporaryDirectory(prefix="wtc7-oracle-synthetic-", dir="/private/tmp") as directory:
            path = Path(directory)/"result.json"
            oracle.exclusive_json(path, {"value": F(1, 3)})
            original_hash = oracle.digest(path)
            with self.assertRaises(FileExistsError):
                oracle.exclusive_json(path, {"value": F(99)})
            self.assertEqual(oracle.digest(path), original_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)
