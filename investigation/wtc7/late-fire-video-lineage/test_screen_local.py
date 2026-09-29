#!/usr/bin/env python3
"""Synthetic controls only; no historical-media reads. Retain all test artifacts."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from unittest import mock
from fractions import Fraction
from pathlib import Path

from PIL import Image

import screen_local as screen

ARTIFACTS = None
PROTOCOL = Path(__file__).with_name("PROTOCOL.md")


def lines(pts, width=64, height=48):
    return [f"pts={value}|width={width}|height={height}\n" for value in pts]


def planned(pts, step=2):
    return screen.frame_plan(lines(pts), Fraction(1, 1000), step, (64, 48))


class UnitControls(unittest.TestCase):
    def test_exact_boundaries_and_first_frame(self):
        rows, coverage = planned([0, 1999, 2000, 2001, 3999, 4000])
        self.assertEqual([row["source_pts"] for row in rows], [0, 2000, 4000])
        self.assertEqual([row["source_frame_index"] for row in rows], [0, 2, 5])
        self.assertEqual([row["bin"] for row in rows], [0, 1, 2])
        self.assertEqual([row["frames"] for row in coverage["frame_count_per_occupied_bin"]], [2, 3, 1])

    def test_negative_nonzero_start_gaps(self):
        rows, coverage = planned([-1, 0, 5999, 6000])
        self.assertEqual([row["bin"] for row in rows], [-1, 0, 2, 3])
        self.assertEqual(coverage["empty_bins_within_observed_range"], [1])
        rows, coverage = planned([3000, 3750, 6000, 6750])
        self.assertEqual([row["bin"] for row in rows], [1, 3])
        self.assertEqual(coverage["observed_bin_range"], [1, 3])
        self.assertEqual(coverage["empty_bins_within_observed_range"], [2])

    def test_rational_time_base_not_decimal_rounding(self):
        rows, coverage = screen.frame_plan(lines([59, 60, 119, 120]), Fraction(1001, 30000), 2, (64, 48))
        self.assertEqual([row["source_pts"] for row in rows], [59, 60, 120])
        self.assertEqual([row["source_seconds_exact"] for row in rows], ["59059/30000", "1001/500", "1001/250"])

    def test_duplicate_and_out_of_order_pts_rejected(self):
        for pts in ([0, 0], [1000, 500]):
            with self.subTest(pts=pts), self.assertRaisesRegex(screen.CheckError, "source_pts_duplicate_or_out_of_order"):
                planned(pts)

    def test_bad_inventory_rejected(self):
        for value in ("pts=N/A|width=64|height=48", "pts=1.5|width=64|height=48", "pts=1|width=64", "pts=1|pts=2|width=64|height=48", "pts=1|width=64|height=48|tag=private", "bad"):
            with self.subTest(value=value), self.assertRaises(screen.CheckError):
                screen.frame_plan([value], Fraction(1, 1000), 2, (64, 48))

    def test_geometry_change_and_empty_rejected(self):
        with self.assertRaisesRegex(screen.CheckError, "source_geometry_change"):
            screen.frame_plan(lines([0]) + lines([1], width=63), Fraction(1, 1000), 2, (64, 48))
        with self.assertRaisesRegex(screen.CheckError, "source_no_frames"):
            planned([])

    def test_timebase_rejected(self):
        for value in ("0/1", "-1/2", "1/0", "N/A", None):
            with self.subTest(value=value), self.assertRaises(screen.CheckError):
                screen.parse_positive_fraction(value)

    def test_selected_pts_timebase_dimensions_and_count(self):
        rows, coverage = planned([0, 2000])
        base = "[Parsed_showinfo_1 @ x] config in time_base: 1/1000, frame_rate: 4/1\n"
        frames = "[Parsed_showinfo_1 @ x] [info] n: 0 pts: 0 pts_time:0 fmt:yuv420p s:64x48\n[Parsed_showinfo_1 @ x] [info] n: 1 pts: 2000 pts_time:2 fmt:yuv420p s:64x48\n"
        screen.reconcile_showinfo(base + frames, rows, Fraction(1, 1000), (64, 48))
        for malformed in (base.replace("1/1000", "1/900") + frames, base + frames.replace("pts: 2000", "pts: 0"), base + frames.replace("n: 1", "n: 0"), base + frames.replace("64x48", "63x48"), base + frames.replace("pts_time:2", "pts_time:3"), base):
            with self.subTest(), self.assertRaises(screen.CheckError):
                screen.reconcile_showinfo(malformed, rows, Fraction(1, 1000), (64, 48))

    def test_printed_timestamp_rounding(self):
        screen.validate_display_time("1.96667", Fraction(59, 30))
        screen.validate_display_time("1.23457e+06", Fraction(1234567))
        for value in ("nan", "N/A", "1.96660"):
            with self.subTest(value=value), self.assertRaises(screen.CheckError):
                screen.validate_display_time(value, Fraction(59, 30))

    def test_native_dimensions_and_mode(self):
        root = ARTIFACTS / "native-contract"
        root.mkdir()
        good = root / "good.png"
        Image.new("RGB", (64, 48), (5, 8, 11)).save(good)
        screen.validate_png(good, (64, 48))
        with self.assertRaisesRegex(screen.CheckError, "native_png_contract"):
            screen.validate_png(good, (63, 48))
        wrong = root / "gray.png"
        Image.new("L", (64, 48), 5).save(wrong)
        with self.assertRaisesRegex(screen.CheckError, "native_png_contract"):
            screen.validate_png(wrong, (64, 48))

    def test_only_exact_reviewed_warning_is_accepted(self):
        known = "[swscaler @ 0x123] [swscaler @ 0x456] [warning] No accelerated colorspace conversion found from yuv420p to rgb24."
        self.assertEqual(screen.classify_decode_diagnostics(known)["reviewed_software_colorspace_fallback_notices"], 1)
        for line in ("[decoder @ 0x1] [warning] damaged frame", known.replace("yuv420p", "yuv422p"), known.replace("[warning]", "[error]")):
            with self.subTest(line=line), self.assertRaisesRegex(screen.CheckError, "decode_diagnostic_review"):
                screen.classify_decode_diagnostics(line)


class RealDecoderSyntheticControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ARTIFACTS / "tiny-fixture"
        cls.root.mkdir()
        cls.source = cls.root / "nonzero-gap.mkv"
        argv = [str(screen.FFMPEG), "-nostdin", "-hide_banner", "-loglevel", "warning", "-n",
                "-f", "lavfi", "-i", "testsrc2=size=64x48:rate=4:duration=5",
                "-vf", "select='lt(n,4)+gte(n,12)',setpts=PTS+3/TB,setsar=2/1",
                "-an", "-c:v", "ffv1", "-fps_mode", "passthrough", str(cls.source)]
        with (cls.root / "generation.stdout").open("xb") as stdout, (cls.root / "generation.stderr").open("xb") as stderr:
            result = subprocess.run(argv, stdout=stdout, stderr=stderr, check=False)
        screen.save(cls.root / "generation.json", {"argv": argv, "returncode": result.returncode})
        if result.returncode:
            raise RuntimeError("Synthetic fixture generation failed; see local diagnostics")
        cls.pin = screen.identity(cls.source)
        cls.selection = cls.root / "selection.json"
        screen.save(cls.selection, {"protocol_sha256": screen.PROTOCOL_SHA256, "sources": [{"id": "SYNTHETIC-ONLY", "path": str(cls.source), **cls.pin, "step_seconds": 2}]})

    def invoke(self, selection, output, ids=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return screen.run(selection, PROTOCOL, output, ids)

    def test_01_full_decode_gap_sar_native_reproduction(self):
        first = self.root / "run01"
        second = self.root / "run02"
        self.invoke(self.selection, first)
        self.invoke(self.selection, second, ["SYNTHETIC-ONLY"])
        receipt = json.loads((first / "SYNTHETIC-ONLY" / "receipt.json").read_text())
        rows = json.loads((first / "SYNTHETIC-ONLY" / "frames.json").read_text())
        self.assertEqual(receipt["coverage"]["decoded_frame_count"], 12)
        self.assertEqual(receipt["coverage"]["empty_bins_within_observed_range"], [2])
        self.assertEqual([row["source_pts"] for row in rows], [3000, 6000])
        self.assertEqual([row["source_frame_index"] for row in rows], [0, 4])
        self.assertEqual(receipt["allowlisted_probe"]["streams"][0]["sample_aspect_ratio"], "2:1")
        for row in rows:
            self.assertEqual((row["width"], row["height"]), (64, 48))
            self.assertEqual(screen.identity(first / "SYNTHETIC-ONLY" / row["png"]), screen.identity(second / "SYNTHETIC-ONLY" / row["png"]))
        for sheet in receipt["overview_sheets"]:
            with Image.open(first / "SYNTHETIC-ONLY" / sheet["path"]) as image:
                self.assertEqual(image.size, (960, 1120))
            self.assertEqual(screen.identity(first / "SYNTHETIC-ONLY" / sheet["path"]), screen.identity(second / "SYNTHETIC-ONLY" / sheet["path"]))
        for command in receipt["commands"]:
            self.assertNotIn("-ss", command["argv"])
        self.assertEqual(screen.identity(self.source), self.pin)
        self.assertEqual(receipt["source_before"], receipt["source_after"])
        for path, pin in receipt["products"].items():
            self.assertEqual(screen.identity(first / "SYNTHETIC-ONLY" / path), pin)

    def test_02_overwrite_refusal(self):
        output = self.root / "existing"
        output.mkdir()
        sentinel = output / "sentinel.json"
        screen.save(sentinel, {"keep": True})
        original = screen.identity(sentinel)
        with self.assertRaises(FileExistsError):
            self.invoke(self.selection, output)
        self.assertEqual(screen.identity(sentinel), original)
        self.assertEqual(len(list(output.iterdir())), 1)

    def test_03_bad_hash_preserved_failure_before_decode(self):
        selection = self.root / "wrong-hash.json"
        value = json.loads(self.selection.read_text())
        value["sources"][0]["sha256"] = "0" * 64
        screen.save(selection, value)
        output = self.root / "failed-hash"
        with self.assertRaisesRegex(screen.CheckError, "source_pin_mismatch"):
            self.invoke(selection, output)
        failure = json.loads((output / "failure.json").read_text())
        self.assertEqual(failure["category"], "source_pin_mismatch")
        self.assertFalse((output / "SYNTHETIC-ONLY").exists())
        self.assertTrue((output / "screen_local.snapshot.py").exists())
        self.assertEqual(failure["source_pins_after_failure"]["SYNTHETIC-ONLY"], self.pin)

    def test_04_subset_and_protocol_pin_rejected(self):
        with self.assertRaisesRegex(screen.CheckError, "source_subset_invalid"):
            self.invoke(self.selection, self.root / "bad-subset", ["missing"])
        value = json.loads(self.selection.read_text())
        value["protocol_sha256"] = "0" * 64
        selection = self.root / "wrong-protocol.json"
        screen.save(selection, value)
        with self.assertRaisesRegex(screen.CheckError, "selection_protocol_pin_mismatch"):
            self.invoke(selection, self.root / "bad-protocol")

    def test_05_changed_input_identity_after_decode_rejected(self):
        original = screen.identity
        count = 0

        def changing_identity(path):
            nonlocal count
            result = original(path)
            if Path(path) == self.source:
                count += 1
                if count >= 3:
                    result["sha256"] = "0" * 64
            return result

        output = self.root / "failed-change-simulation"
        with mock.patch.object(screen, "identity", side_effect=changing_identity):
            with self.assertRaisesRegex(screen.CheckError, "source_changed"):
                self.invoke(self.selection, output)
        failure = json.loads((output / "SYNTHETIC-ONLY" / "failure.json").read_text())
        self.assertEqual(failure["phase"], "source_hash_after")
        self.assertFalse(failure["source_after_matches_pin"])
        self.assertTrue((output / "SYNTHETIC-ONLY" / "frames.json").exists())
        self.assertEqual(original(self.source), self.pin)


def main():
    global ARTIFACTS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    if args.artifacts:
        ARTIFACTS = args.artifacts
        ARTIFACTS.mkdir(exist_ok=False)
    else:
        ARTIFACTS = Path(tempfile.mkdtemp(prefix="late-fire-screen-tests-"))
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    with (ARTIFACTS / "unittest-local.txt").open("x") as output:
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    receipt = {"status": "passed" if result.wasSuccessful() else "failed", "tests_run": result.testsRun,
               "failures": len(result.failures), "errors": len(result.errors),
               "script": screen.identity(Path(screen.__file__)), "test_script": screen.identity(Path(__file__)),
               "protocol": screen.identity(PROTOCOL), "artifacts": str(ARTIFACTS),
               "scope": "Synthetic PTS and tiny generated pixels only; no historical-media visual validity or figure correspondence tested."}
    screen.save(ARTIFACTS / "test-receipt.json", receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
