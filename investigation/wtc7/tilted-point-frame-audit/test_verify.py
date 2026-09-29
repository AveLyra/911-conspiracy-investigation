#!/usr/bin/env python3
"""Synthetic tests of the independent verifier; no historical data reads."""
import argparse
import copy
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import unittest

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import verify as v

CONTROL = None


def synthetic_project():
    tracks = []
    for name, start, stop, key_start in (("pointmass05", 150, 403, 360),
                                        ("pointmass08", 210, 445, 210)):
        indices = list(range(start, stop, 6))
        keys = list(range(key_start, stop, 6))
        rows = []
        for n in indices:
            coords = {}
            for axis, value in (("x", 100.25), ("y", 120.75)):
                coords[axis] = {"status": "present", "occurrences": [
                    {"status": "valid_finite", "saved_text": str(value), "value": value,
                     "text_sha256": hashlib.sha256(str(value).encode()).hexdigest(),
                     "xml_path": f"/synthetic/{name}/{n}/{axis}"}]}
            rows.append({"index": n, "status": "saved_object", "finite_complete": True,
                         "entry_ordinal_one_based": indices.index(n) + 1,
                         "xml_path": f"/synthetic/{name}/{n}",
                         "saved_keyFrame_member": n in keys,
                         "objects": [{"finite_complete": True, "coordinates": coords}]})
        tracks.append({"track_id": name, "saved_indices": indices,
                       "xml_path": f"/synthetic/{name}",
                       "keyFrames": [{"values": keys}], "framedata": [{"rows": rows}]})
    return {"pointmass_tracks": tracks}


def synthetic_clock():
    stream = {"index": 0, "width": 720, "height": 480, "pix_fmt": "yuv420p",
              "time_base": "1/60000", "sample_aspect_ratio": "131:144",
              "display_aspect_ratio": "131:96", "nb_frames": "476"}
    probe, frames, selected = [], [], []
    for n in range(476):
        # Nonuniform synthetic increments and nonzero origin are intentional.
        pts = 3000 + 2002 * n + n // 3
        p = {"stream_index": 0, "width": 720, "height": 480, "pix_fmt": "yuv420p",
             "pts": pts, "best_effort_timestamp": pts}
        basic = {"index": n, "pts": pts, "time_seconds_exact": str(Fraction(pts, 60000))}
        frame = dict(basic, decoded_sha256=hashlib.sha256(f"raw-{n}".encode()).hexdigest(),
                     luma_sha256=hashlib.sha256(f"luma-{n}".encode()).hexdigest())
        probe.append(p); frames.append(frame); selected.append(basic)
    return ({"streams": [stream], "frames": probe},
            {"geometry": [720, 480], "time_base": "1/60000", "n": 476, "frames": selected}, frames)


class Controls(unittest.TestCase):
    def test_half_up_exact_and_invalid(self):
        cases = {0: 0, 2: 2, 2.49: 2, 2.5: 3, -2.5: -2, -2.51: -3,
                 -0.5: 0, -0.4: 0, 0.5: 1, math.nextafter(0.5, 0): 0}
        for value, expected in cases.items():
            self.assertEqual(v.rounded(value), expected)
        for value in (True, False, float("nan"), float("inf"), "1", None):
            with self.assertRaises(ValueError): v.rounded(value)

    def test_continuous_domain_distinct_from_rounded_cell(self):
        left = v.point_geometry(-0.4, 0)
        self.assertEqual(left["rounded"], [0, 0])
        self.assertFalse(left["point_in_native"])
        self.assertTrue(left["rounded_cell_in_native"])
        right = v.point_geometry(719.8, 479.8)
        self.assertEqual(right["rounded"], [720, 480])
        self.assertTrue(right["point_in_native"])
        self.assertFalse(right["rounded_cell_in_native"])
        self.assertEqual(v.point_geometry(4.5, 7.5)["crop"], [-25, -22, 35, 38])

    def test_complete_source_rows_and_membership(self):
        rows = v.project_rows(synthetic_project())
        self.assertEqual(len(rows), 83)
        self.assertEqual(sorted({r["frame"] for r in rows}), list(range(150, 445, 6)))
        self.assertEqual(sum(r["key"] for r in rows), 48)
        self.assertEqual(sum(not r["key"] for r in rows), 35)
        self.assertEqual(rows[0], {"track_id": "pointmass05", "frame": 150,
                                  "x": 100.25, "y": 120.75, "key": False})

    def test_missing_duplicate_and_changed_key_rejected(self):
        mutations = []
        p = synthetic_project(); p["pointmass_tracks"][0]["framedata"][0]["rows"].pop(); mutations.append(p)
        p = synthetic_project(); p["pointmass_tracks"].append(copy.deepcopy(p["pointmass_tracks"][0])); mutations.append(p)
        p = synthetic_project(); p["pointmass_tracks"][0]["framedata"][0]["rows"][0]["saved_keyFrame_member"] = True; mutations.append(p)
        p = synthetic_project(); p["pointmass_tracks"][1]["keyFrames"][0]["values"].pop(); mutations.append(p)
        p = synthetic_project(); p["pointmass_tracks"][0]["framedata"][0]["rows"][0]["index"] = 151; mutations.append(p)
        for p in mutations:
            with self.assertRaises(ValueError): v.project_rows(p)

    def test_invalid_coordinate_presence_and_lexical_identity(self):
        for key, value in (("value", True), ("value", float("inf")),
                           ("saved_text", "NaN"), ("saved_text", "100.5")):
            p = synthetic_project()
            cell = p["pointmass_tracks"][0]["framedata"][0]["rows"][0]["objects"][0]["coordinates"]["x"]["occurrences"][0]
            cell[key] = value
            with self.assertRaises(ValueError): v.project_rows(p)

    def test_all_frame_clock_join_and_irregular_timestamps(self):
        probe, selection, frames = synthetic_clock()
        self.assertEqual(v.source_clock(probe, selection, frames), frames)
        self.assertEqual(Fraction(frames[0]["time_seconds_exact"]), Fraction(1, 20))
        self.assertNotEqual(frames[3]["pts"] - frames[2]["pts"], frames[2]["pts"] - frames[1]["pts"])

    def test_corrupt_pts_hash_geometry_index_and_count_rejected(self):
        for action in ("pts", "hash", "geometry", "index", "count", "boolean"):
            probe, selection, frames = synthetic_clock()
            if action == "pts": selection["frames"][200]["pts"] += 1
            if action == "hash": frames[200]["decoded_sha256"] = "x" * 64
            if action == "geometry": probe["frames"][200]["width"] = 640
            if action == "index": frames[200]["index"] = 199
            if action == "count": frames.pop()
            if action == "boolean": frames[0]["index"] = False
            with self.assertRaises(ValueError): v.source_clock(probe, selection, frames)

    def test_pins_and_duplicate_json_keys(self):
        p = CONTROL / "synthetic-json.json"
        p.write_text('{"synthetic_only": true}\n')
        pin = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(v.read_pinned(p, pin), {"synthetic_only": True})
        with self.assertRaises(ValueError): v.read_pinned(p, "0" * 64)
        p = CONTROL / "duplicate-json.json"
        p.write_text('{"n": 1, "n": 2}')
        with self.assertRaises(ValueError): v.read_json(p)

    def test_crop_all_cells_padding_and_repetition(self):
        yy, xx = np.indices((80, 90))
        native = ((xx + 7 * yy) % 256).astype(np.uint8)
        for x, y in ((40.25, 40.75), (-0.4, 0), (89.8, 79.8), (-500, 500)):
            actual, mask = v.independent_crop(native, x, y, v.PADDING)
            # Slow direct loop is the small-control oracle, independent of gather.
            expected = np.empty((180, 180, 3), dtype=np.uint8)
            expected_mask = np.zeros((180, 180), dtype=bool)
            r, s = math.floor(Fraction(x) + Fraction(1, 2)), math.floor(Fraction(y) + Fraction(1, 2))
            for dy in range(180):
                for dx in range(180):
                    sx, sy = r - 30 + dx // 3, s - 30 + dy // 3
                    valid = 0 <= sx < 90 and 0 <= sy < 80
                    expected[dy, dx] = ((sx + 7 * sy) % 256,) * 3 if valid else v.PADDING
                    expected_mask[dy, dx] = valid
            self.assertTrue(np.array_equal(actual, expected))
            self.assertTrue(np.array_equal(mask, expected_mask))

    def test_marker_exact_arms_and_open_center(self):
        plain = np.zeros((180, 180, 3), dtype=np.uint8)
        marked, mask = v.independent_marked(plain)
        expected = {(91 + d, 91) for d in list(range(-15, -5)) + list(range(6, 16))}
        expected |= {(91, 91 + d) for d in list(range(-15, -5)) + list(range(6, 16))}
        found = {(int(x), int(y)) for y, x in np.argwhere(mask)}
        self.assertEqual(found, expected)
        self.assertTrue(np.all(marked[mask] == np.array([0, 255, 255])))
        self.assertTrue(np.all(marked[86:97, 86:97] == 0))

    def test_native_png_pin_and_corruption(self):
        yy, xx = np.indices((480, 720))
        native = ((xx + 7 * yy) % 256).astype(np.uint8)
        p = CONTROL / "synthetic-native.png"
        Image.fromarray(native).save(p)
        sha = hashlib.sha256(native.tobytes()).hexdigest()
        self.assertTrue(np.array_equal(v.native_pixels(p, sha), native))
        with self.assertRaises(ValueError): v.native_pixels(p, "0" * 64)

    def test_full_panel_source_crop_marker_and_missing_slot_corruption(self):
        yy, xx = np.indices((480, 720))
        native = ((xx + 7 * yy) % 256).astype(np.uint8)
        row = {"track_id": "pointmass05", "x": 100, "y": 120}
        panel = np.empty((648, 1128, 3), dtype=np.uint8); panel[:] = v.BACKGROUND
        panel[72:552, 12:732] = np.stack([native] * 3, axis=2)
        # Fixture uses PIL crop/resize, not the verifier's gather.
        crop = Image.fromarray(native).crop((70, 90, 130, 150)).resize((180, 180), Image.Resampling.NEAREST).convert("RGB")
        panel[140:320, 744:924] = np.asarray(crop)
        marked = np.asarray(crop).copy()
        for offset in list(range(-15, -5)) + list(range(6, 16)):
            marked[91, 91 + offset] = v.CYAN
            marked[91 + offset, 91] = v.CYAN
        panel[140:320, 936:1116] = marked
        self.assertEqual(v.check_panel_regions(panel, native, [row]), 1425600)
        for x, y in ((12, 72), (744, 140), (1027, 231), (1012, 231), (744, 420)):
            bad = panel.copy(); bad[y, x, 0] ^= 1
            with self.assertRaises(ValueError): v.check_panel_regions(bad, native, [row])
        with self.assertRaises(ValueError): v.check_panel_regions(panel, native, [])

    def test_full_manifest_derivation_and_exact_geometry(self):
        probe, selection, frames = synthetic_clock()
        documents = {"project01.json": synthetic_project(), "views01/frames.json": frames}
        manifest, pngs = v.expected_manifest(documents)
        self.assertEqual((len(manifest["points"]), len(manifest["frames"]), len(pngs)), (83, 50, 349))
        first = manifest["points"][0]
        self.assertEqual(first["source_row_xml_path"], "/synthetic/pointmass05/150")
        self.assertEqual(first["rounded"], [100, 121])
        self.assertEqual(first["rounding_difference_exact"], ["-1/4", "1/4"])
        self.assertEqual(first["source_rect"], [70, 91, 130, 151])
        self.assertEqual(first["pts"], frames[150]["pts"])
        self.assertEqual(first["mask_png"], "crops/pointmass05-f0150-mask.png")
        self.assertEqual(manifest["frames"][0]["slots"]["pointmass08"], {"status": "missing_saved_row"})
        bad = copy.deepcopy(manifest); bad["points"].pop()
        with self.assertRaises(ValueError): v.same(bad, manifest, "manifest")
        with self.assertRaises(ValueError): v.same({"n": True}, {"n": 1}, "types")

    def test_complete_rgb_panel_labels_and_exterior_corruption(self):
        yy, xx = np.indices((480, 720))
        native = np.stack((xx % 256, yy % 256, xx // 256 + 4 * (yy // 256)), axis=2).astype(np.uint8)
        frame = {"index": 0, "pts": 17, "time_base": "1/60000", "time_seconds_exact": "17/60000"}
        point = {"track_id": "pointmass05", "x": 100.5, "y": 200.5, "key": False,
                 "x_saved_text": "100.5", "y_saved_text": "200.5"}
        canvas = Image.new("RGB", v.PANEL_SIZE, v.BACKGROUND)
        canvas.paste(Image.fromarray(native), (12, 72))
        crop = Image.fromarray(native).crop((71, 171, 131, 231)).resize((180, 180), Image.Resampling.NEAREST)
        canvas.paste(crop, (744, 140))
        marked = crop.copy(); pen = ImageDraw.Draw(marked)
        for lo, hi in ((-15, -6), (6, 15)):
            pen.line((91 + lo, 91, 91 + hi, 91), fill=v.CYAN)
            pen.line((91, 91 + lo, 91, 91 + hi), fill=v.CYAN)
        canvas.paste(marked, (936, 140))
        labels = v.label_specs(frame, [point], True, True)
        self.assertEqual(labels[2][3], "Complete synthetic RGB coordinate-pattern image, unmarked.")
        self.assertEqual(len(labels), 15)
        pen = ImageDraw.Draw(canvas); font = ImageFont.load_default(size=12)
        for x, y, width, text in labels:
            pen.text((x, y), text, fill=(240, 240, 240), font=font)
        panel = np.array(canvas)
        self.assertEqual(v.check_complete_panel(panel, native, [point], frame, True)["exterior_labels_checked"], 15)
        for x, y in ((0, 0), (12, 8), (900, 610)):
            bad = panel.copy(); bad[y, x, 0] ^= 1
            with self.assertRaises(ValueError): v.check_complete_panel(bad, native, [point], frame, True)

    def test_exclusive_receipt_preserves_existing_bytes(self):
        p = CONTROL / "exclusive-report.json"
        v.exclusive_report(p, {"synthetic": True})
        before = p.read_bytes()
        with self.assertRaises(FileExistsError): v.exclusive_report(p, {"overwrite": True})
        self.assertEqual(p.read_bytes(), before)


def main():
    global CONTROL
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    CONTROL = args.out.resolve()
    v.require(CONTROL.parent == v.HERE and CONTROL.name.startswith("verify-controls"), "owned control output")
    CONTROL.mkdir(exist_ok=False)
    before = {str(p): v.identity(p) for p in (Path(__file__), v.HERE / "verify.py")}
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    transcript = stream.getvalue()
    (CONTROL / "tests.txt").write_text(transcript)
    receipt = {"status": "pass" if result.wasSuccessful() else "fail", "tests": result.testsRun,
               "failures": len(result.failures), "errors": len(result.errors), "procedure": before,
               "python": sys.version, "historical_inputs_read": False, "producer_imported": False,
               "products": {p.name: v.identity(p) for p in CONTROL.iterdir() if p.is_file()}}
    v.require(all(v.identity(Path(p)) == pin for p, pin in before.items()), "code unchanged during controls")
    with (CONTROL / "receipt.json").open("x") as f:
        json.dump(receipt, f, indent=2, sort_keys=True); f.write("\n")
    print(transcript)
    print(json.dumps({k: receipt[k] for k in ("status", "tests", "failures", "errors")}, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
