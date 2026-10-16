import copy
import json
from pathlib import Path
import unittest
from compare_records import compare, sub


class Comparisons(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent
        self.timing = json.loads((root / "timing-observations.json").read_text())
        self.swf = json.loads((root / "swf-structure-run01.json").read_text())

    def test_decimal_not_float(self):
        self.assertEqual(sub("6.3", "6.9"), "-0.6")

    def test_west_penthouse_signed_residuals(self):
        out = compare(self.timing, self.swf)
        row = out["timing_residuals"][-1]
        self.assertEqual(row["model_minus_observed_with_debris"], ["-2.4", "-2.0"])
        self.assertEqual(row["model_minus_observed_without_debris"], ["1.3", "1.6"])

    def test_proxy_and_reference_not_independent(self):
        out = compare(self.timing, self.swf)
        self.assertIn("proxy", out["timing_residuals"][0]["qualifier"])
        self.assertFalse(any(r["event"] == "Start of east-penthouse descent" for r in out["timing_residuals"]))
        self.assertEqual(out["faq_12_9_check"]["observed_interval_using_vibration_proxy"], "12.9")

    def test_conflicting_clocks_retained(self):
        out = compare(self.timing, self.swf)["clock_offsets_absolute_minus_relative"]
        self.assertEqual(out["figure_12_66_and_12_67_panel_pairs"], ["13.3"] * 5 + ["14.3"])
        self.assertEqual(out["figure_12_68_caption_endpoint_pairs"], ["16.0", "16.0"])
        self.assertEqual(out["figure_12_68_panel_pairs"], ["13.3"] * 3)

    def test_reject_unmatched_tag_sequence(self):
        changed = copy.deepcopy(self.swf)
        changed["files"][1]["tags"][0]["code"] = 999
        with self.assertRaises(ValueError):
            compare(self.timing, changed)

    def test_pair_differences(self):
        out = compare(self.timing, self.swf)["swf_date_pairs"]
        self.assertEqual([r["same_payloads"] for r in out], [59, 129])
        self.assertEqual([r["root_tags"] for r in out], [61, 130])


if __name__ == "__main__":
    unittest.main()
