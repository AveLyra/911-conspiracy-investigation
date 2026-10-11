"""Finite verification of the declared synthetic challenge, not historical tests."""
import base64
from fractions import Fraction as F
from io import BytesIO
from pathlib import Path
import unittest

from PIL import Image
import raster_challenge as r


class ChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helper = r.load_renderer()
        cls.all_scenes = {s.name: s for s in r.scenes()}

    def test_declared_suite_is_fixed(self):
        self.assertEqual(len(r.scenes()), 16)
        self.assertEqual(len(set(s.name for s in r.scenes())), 16)
        self.assertEqual(r.CODECS, ("png", "jpg50s2"))
        self.assertEqual(r.COLUMNS, tuple(range(64, 96)))

    def test_ordinary_render_matches_unchanged_helper(self):
        # Independent existing renderer has integer sample-coordinate algebra.
        for slope, m2 in (("0", 0), ("1/2", 1)):
            for phase, p2 in (("0", 0), ("1/2", 1)):
                s = r.Scene("ordinary", (0, 0, 0), slope, phase)
                old_scene = {"description": "control", "color": [0, 0, 0],
                             "segments": [self.helper.segment("A", m2, p2, 1)], "white_masks": []}
                self.assertEqual(r.render(s, self.helper).tobytes(), self.helper.render_scene(old_scene).tobytes())

    def test_straight_truth_uses_full_column_end_limits(self):
        s = r.Scene("steep", (0, 0, 0), "2", "1/2")
        self.assertEqual(r.truth(s, 80)["ordinate_infimum_supremum"], ["97/2", "101/2"])
        self.assertEqual(r.truth(s, 80)["support_length"], "1")

    def test_quartic_has_exact_peak_and_zero_at_samples(self):
        s = self.all_scenes["quartic_excursion"]
        self.assertEqual([r.center(s, F(80) + v) for v in r.OFFSETS], [F(48)] * 4)
        self.assertEqual(r.center(s, F(161, 2)), 52)
        self.assertEqual(r.truth(s, 80)["ordinate_infimum_supremum"], ["48", "52"])
        self.assertEqual(r.truth(s, 79)["ordinate_infimum_supremum"], ["48", "48"])

    def test_exact_subpixel_support_gap(self):
        s = self.all_scenes["subpixel_gap"]
        self.assertEqual(r.truth(s, 80)["support_length"], "7/8")
        self.assertFalse(r.truth(s, 80)["full_column_support"])
        self.assertTrue(all(r.supported(s, F(80) + v) for v in r.OFFSETS))
        self.assertFalse(r.supported(s, F(161, 2)))

    def test_fractional_cap_support(self):
        s = self.all_scenes["fractional_cap"]
        self.assertEqual(r.truth(s, 80)["support_length"], "1/2")
        self.assertEqual(r.truth(s, 81)["support_length"], "0")
        self.assertIsNone(r.truth(s, 81)["ordinate_infimum_supremum"])

    def test_curvature_alias_does_not_enclose_truth(self):
        ordinary = r.render(self.all_scenes["black-m0-p0"], self.helper)
        s = self.all_scenes["quartic_excursion"]
        curved = r.render(s, self.helper)
        self.assertEqual(ordinary.tobytes(), curved.tobytes())
        result = r.column_result(s, curved, 80)
        self.assertEqual(result["observed"]["envelope"], [47, 49])
        self.assertEqual(result["outcome"], "enclosure_failure")
        self.assertTrue(result["three_column_single_run_diagnostic"])
        self.assertEqual(r.column_result(self.all_scenes["black-m0-p0"], ordinary, 80)["outcome"], "contained")

    def test_gap_alias_does_not_establish_full_support(self):
        ordinary = r.render(self.all_scenes["black-m0-p0"], self.helper)
        s = self.all_scenes["subpixel_gap"]
        gapped = r.render(s, self.helper)
        self.assertEqual(ordinary.tobytes(), gapped.tobytes())
        result = r.column_result(s, gapped, 80)
        self.assertEqual(result["outcome"], "unsupported_full_column_proposal")
        self.assertTrue(result["three_column_single_run_diagnostic"])

    def test_fractional_cap_observation_is_not_full_support(self):
        s = self.all_scenes["fractional_cap"]
        image = r.render(s, self.helper)
        result = r.column_result(s, image, 80)
        self.assertIsNotNone(result["observed"]["envelope"])
        self.assertEqual(result["outcome"], "unsupported_full_column_proposal")
        self.assertFalse(result["three_column_single_run_diagnostic"])

    def test_pale_phase_quantization_and_nonvacuous_control(self):
        blank = r.render(self.all_scenes["blank"], self.helper)
        pale0 = r.render(self.all_scenes["pale254-m0-p0"], self.helper)
        pale_half = r.render(self.all_scenes["pale254-m0-p1/2"], self.helper)
        self.assertEqual(blank.tobytes(), pale0.tobytes())
        self.assertNotEqual(blank.tobytes(), pale_half.tobytes())
        self.assertEqual(r.diagnostic(pale_half, 80)["envelope"], [48, 49])

    def test_codecs_preserve_equal_input_counterexample(self):
        a = r.render(self.all_scenes["black-m0-p0"], self.helper)
        b = r.render(self.all_scenes["quartic_excursion"], self.helper)
        for codec in r.CODECS:
            ea, da, wa = self.helper.encode_decode(a, codec)
            eb, db, wb = self.helper.encode_decode(b, codec)
            self.assertEqual(ea, eb)
            self.assertEqual(da.tobytes(), db.tobytes())
            self.assertEqual(wa, wb)

    def test_complete_encoded_case_is_retained(self):
        s = self.all_scenes["black-m0-p0"]
        result = r.raster_record(s, "png", r.render(s, self.helper), self.helper)
        encoded = base64.b64decode(result["encoded_base64"], validate=True)
        self.assertEqual(r.digest(encoded), result["encoded_sha256"])
        with Image.open(BytesIO(encoded)) as image:
            image.load()
            self.assertEqual(r.digest(image.tobytes()), result["decoded_rgb_sha256"])
        self.assertEqual(len(result["columns"]), 32)

    def test_disconnected_geometry_is_not_hulled(self):
        image = Image.new("RGB", (r.WIDTH, r.HEIGHT), "white")
        image.putpixel((80, 40), (0, 0, 0))
        image.putpixel((80, 42), (0, 0, 0))
        result = r.diagnostic(image, 80)
        self.assertEqual(result["runs"], [[40, 41], [42, 43]])
        self.assertIsNone(result["envelope"])

    def test_invalid_scene_column_and_image_are_errors(self):
        for bad in ((True, 0, 0), (256, 0, 0), (255, 255, 255)):
            with self.assertRaises(ValueError):
                r.Scene("bad", bad)
        with self.assertRaises(ValueError):
            r.Scene("bad", (0, 0, 0), feature="quartic_excursion", slope="2")
        for x in (True, -1, 160, 1.0):
            with self.assertRaises(ValueError):
                r.truth(self.all_scenes["black-m0-p0"], x)
        with self.assertRaises(ValueError):
            r.diagnostic(Image.new("L", (r.WIDTH, r.HEIGHT)), 80)

    def test_fixed_output_route_and_existing_file_refusal(self):
        with self.assertRaises(ValueError):
            r.save(Path("/private/tmp/not-a-declared-result.json"))
        # Check exclusive-open semantics without writing any file.
        from unittest.mock import patch
        with patch.object(Path, "exists", return_value=True):
            with self.assertRaises(FileExistsError):
                r.save(r.HERE / "raster-challenge01.json")


if __name__ == "__main__":
    unittest.main()
