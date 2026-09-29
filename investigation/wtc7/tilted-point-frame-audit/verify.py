#!/usr/bin/env python3
"""Independent representation oracle; never imports the panel producer.

Historical execution requires root clearance after synthetic controls. Importing
this module does not read historical inputs or decode/render historical media.
"""
from __future__ import annotations

from fractions import Fraction
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "tilted-camera-source-join"
PINS = {
    "project01.json": "4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8",
    "probe01/probe.json": "778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de",
    "probe01/selection.json": "afd9abc4bd64a0422a749715a8dbb727f7e23447f1c6bf45e9c93d32030f7f6b",
    "views01/frames.json": "2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15",
    "views02/frames.json": "2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15",
    "source/TiltedCameraWTC7Clip.mp4": "393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f",
    "source/receipt.json": "a100331b8e5e66ebb41959811e3ff650750e8284fdba0e4c8dcebdd736ed8ea9",
    "probe01/execution.json": "548965fa3f7de60fd71fb42b2d211e63143502e041743db32d3df6a9b5ac25fd",
    "views01/receipt.json": "4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29",
    "views01/execution.json": "afc698e4f6215018fa821108270ba13012ae82459cc9893b747445a96003db59",
    "prepare_media.py": "b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5",
}
AUTHORITY_PINS = {
    HERE / "PROTOCOL.md": "50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d",
    HERE / "method-review.md": "cfe0b94704f419f18a8efb7992d03c38841242f3a369d21d877fba39f0e43fc6",
    Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md"):
        "54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd",
    Path("/opt/homebrew/bin/ffmpeg"): "7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569",
    Path("/opt/homebrew/bin/ffprobe"): "fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad",
}
IDS = ("pointmass05", "pointmass08")
FRAME_INDICES = tuple(range(150, 445, 6))
NUMERIC_TEXT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
HEX256 = re.compile(r"[0-9a-f]{64}")
PANEL_SIZE = (1128, 648)
BACKGROUND = (24, 24, 24)
PADDING = (255, 0, 255)
CYAN = (0, 255, 255)
NATIVE_RECT = (12, 72, 732, 552)
SLOTS = {
    "pointmass05": ((744, 140, 924, 320), (936, 140, 1116, 320)),
    "pointmass08": ((744, 420, 924, 600), (936, 420, 1116, 600)),
}
EXPECTED_LAYOUT = {
    "panel_size": [1128, 648], "native_rect": list(NATIVE_RECT),
    "slots": {name: {"plain_rect": list(rects[0]), "marked_rect": list(rects[1]),
                     "label_top": 56 if name == IDS[0] else 336}
              for name, rects in SLOTS.items()},
    "crop_size": [60, 60], "scale": 3, "padding_rgb": list(PADDING),
    "mask_mode": "L", "mask_size": [60, 60], "mask_valid": 255, "mask_padding": 0,
    "background_rgb": list(BACKGROUND), "marker_rgb": list(CYAN),
    "marker_center": [91, 91], "marker_arm_offsets_inclusive": [[-15, -6], [6, 15]],
    "marker_thickness": 1, "marker_gap_offsets_inclusive": [-5, 5],
    "rounding": "mathematical floor(exact saved binary value + 1/2)",
    "continuous_domain": "[0,720) x [0,480)",
    "rectangles": "half-open integer pixel bounds",
    "labels": "outside native/plain/marked rectangles; missing slots are background only",
}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def identity(path):
    return {"bytes": Path(path).stat().st_size, "sha256": digest(path)}


def read_json(path):
    def reject_constant(value):
        raise ValueError("nonfinite JSON constant")

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(), parse_constant=reject_constant,
                      object_pairs_hook=unique_pairs)


def read_pinned(path, sha):
    require(digest(path) == sha, "source pin mismatch")
    return read_json(path)


def finite(value):
    require(type(value) in (int, float) and math.isfinite(value), "finite real, not boolean")
    return value


def rounded(value):
    """Exact nearest-half-up for the supplied finite integer/binary float."""
    finite(value)
    return (Fraction(value) + Fraction(1, 2)).__floor__()


def point_geometry(x, y, width=720, height=480):
    finite(x); finite(y)
    require(type(width) is int and type(height) is int and min(width, height) > 0,
            "positive integer native dimensions")
    r, s = rounded(x), rounded(y)
    return {
        "rounded": [r, s],
        "rounding_difference": [r - x, s - y],
        "crop": [r - 30, s - 30, r + 30, s + 30],
        "point_in_native": 0 <= x < width and 0 <= y < height,
        "rounded_cell_in_native": 0 <= r < width and 0 <= s < height,
    }


def scalar_coordinate(row, axis):
    require(row.get("status") == "saved_object" and row.get("finite_complete") is True,
            "finite saved row required")
    objects = row["objects"]
    require(len(objects) == 1 and objects[0].get("finite_complete") is True,
            "single finite coordinate object")
    field = objects[0]["coordinates"][axis]
    require(field.get("status") == "present" and len(field["occurrences"]) == 1,
            "single coordinate occurrence")
    cell = field["occurrences"][0]
    literal, value = cell["saved_text"], cell["value"]
    require(isinstance(literal, str) and NUMERIC_TEXT.fullmatch(literal), "numeric saved text")
    require(cell.get("status") == "valid_finite" and finite(value) == float(literal),
            "saved text/value agreement")
    return value


def project_rows(project):
    """Reconstruct the full fixed 83-row contract from the pinned export."""
    tracks = project["pointmass_tracks"]
    chosen = {name: [t for t in tracks if t["track_id"] == name] for name in IDS}
    require(all(len(items) == 1 for items in chosen.values()), "unique selected track IDs")
    result = []
    for name in IDS:
        track = chosen[name][0]
        expected = list(range(150, 403, 6) if name == IDS[0] else range(210, 445, 6))
        keys = list(range(360, 403, 6)) if name == IDS[0] else expected
        require(track["saved_indices"] == expected, "complete saved-index domain")
        require(len(track["framedata"]) == 1 and len(track["keyFrames"]) == 1,
                "single frame/key arrays")
        require(track["keyFrames"][0]["values"] == keys, "complete key membership")
        rows = track["framedata"][0]["rows"]
        require([r["index"] for r in rows] == expected, "complete ordered source rows")
        for row in rows:
            frame = row["index"]
            require(type(frame) is int, "integer source frame")
            member = row["saved_keyFrame_member"]
            require(type(member) is bool and member == (frame in keys), "saved key flag agreement")
            result.append({"track_id": name, "frame": frame, "x": scalar_coordinate(row, "x"),
                           "y": scalar_coordinate(row, "y"), "key": member})
    result.sort(key=lambda r: (r["frame"], r["track_id"]))
    require(len(result) == 83 and tuple(sorted({r["frame"] for r in result})) == FRAME_INDICES,
            "exact 83 rows and 50 frame union")
    return result


def source_clock(probe, selection, frames):
    """Check every preserved 476-frame PTS/hash join, without nominal retiming."""
    streams = probe["streams"]
    require(len(streams) == 1, "one selected video stream")
    s = streams[0]
    require((s["index"], s["width"], s["height"], s["pix_fmt"], s["time_base"],
             s["sample_aspect_ratio"], s["display_aspect_ratio"], s["nb_frames"]) ==
            (0, 720, 480, "yuv420p", "1/60000", "131:144", "131:96", "476"),
            "literal source stream geometry and clock")
    require(len(probe["frames"]) == len(frames) == len(selection["frames"]) == 476,
            "all 476 records")
    require(selection["geometry"] == [720, 480] and selection["time_base"] == "1/60000"
            and selection["n"] == 476, "saved selection geometry and clock")
    previous = None
    for n, (p, f, q) in enumerate(zip(probe["frames"], frames, selection["frames"])):
        require((p["stream_index"], p["width"], p["height"], p["pix_fmt"]) ==
                (0, 720, 480, "yuv420p"), "per-frame native geometry")
        pts = p["pts"]
        require(type(pts) is int and type(p["best_effort_timestamp"]) is int
                and all(type(v) is int for v in (f["pts"], q["pts"], f["index"], q["index"]))
                and p["best_effort_timestamp"] == pts
                and f["pts"] == q["pts"] == pts and f["index"] == q["index"] == n,
                "exact frame/PTS joins")
        time = Fraction(pts, 60000)
        require(Fraction(f["time_seconds_exact"]) == Fraction(q["time_seconds_exact"]) == time,
                "exact rational PTS seconds")
        require(previous is None or time > previous, "strict PTS order")
        previous = time
        require(HEX256.fullmatch(f["decoded_sha256"]) and HEX256.fullmatch(f["luma_sha256"]),
                "complete decoded/luma hashes")
    return frames


def native_pixels(path, expected_luma):
    """Read pixel arrays for byte validation only; no display or interpretation."""
    with Image.open(path) as im:
        require(im.format == "PNG" and im.mode == "L" and im.size == (720, 480),
                "native PNG geometry and mode")
        pixels = np.asarray(im).copy()
    require(hashlib.sha256(pixels.tobytes()).hexdigest() == expected_luma, "native luma identity")
    return pixels


def independent_crop(native, x, y, padding):
    """Direct integer gather, not PIL crop/resize or producer code."""
    require(native.dtype == np.uint8 and (native.ndim == 2 or
            (native.ndim == 3 and native.shape[2] == 3)), "uint8 luma/RGB control input")
    height, width = native.shape[:2]
    box = point_geometry(x, y, width, height)["crop"]
    xs = np.arange(60, dtype=np.int64) + box[0]
    ys = np.arange(60, dtype=np.int64) + box[1]
    valid = ((ys[:, None] >= 0) & (ys[:, None] < height)
             & (xs[None, :] >= 0) & (xs[None, :] < width))
    base = np.zeros((60, 60, 3), dtype=np.uint8)
    base[:] = padding
    iy, ix = np.nonzero(valid)
    values = native[ys[iy], xs[ix]]
    base[iy, ix] = values[:, None] if native.ndim == 2 else values
    # Repeat by explicit index gather, independently of producer resizing.
    axis = np.arange(180) // 3
    return base[axis[:, None], axis[None, :]], valid[axis[:, None], axis[None, :]]


def independent_marked(plain):
    require(plain.shape == (180, 180, 3) and plain.dtype == np.uint8, "RGB crop geometry")
    yy, xx = np.indices((180, 180))
    arm_x = (np.abs(xx - 91) >= 6) & (np.abs(xx - 91) <= 15)
    arm_y = (np.abs(yy - 91) >= 6) & (np.abs(yy - 91) <= 15)
    mask = ((yy == 91) & arm_x) | ((xx == 91) & arm_y)
    require(np.count_nonzero(mask) == 40 and not mask[91, 91], "40-pixel gapped crosshair")
    result = plain.copy()
    result[mask] = CYAN
    return result, mask


def equal_pixels(actual, expected, label):
    require(actual.dtype == expected.dtype and actual.shape == expected.shape
            and np.array_equal(actual, expected), label)
    return int(expected.size)


def region(array, rect):
    left, top, right, bottom = rect
    return array[top:bottom, left:right]


def check_panel_regions(panel, native, rows):
    """Check every historical source/crop sample and missing slot, no OCR."""
    require(panel.dtype == np.uint8 and panel.shape == (648, 1128, 3), "complete panel geometry")
    require(native.dtype == np.uint8 and native.shape in ((480, 720), (480, 720, 3)), "native/control geometry")
    by_id = {row["track_id"]: row for row in rows}
    require(len(by_id) == len(rows) and set(by_id) <= set(IDS), "unique known panel tracks")
    expected_native = np.stack([native] * 3, axis=2) if native.ndim == 2 else native
    count = equal_pixels(region(panel, NATIVE_RECT), expected_native, "unmarked full native pixels")
    for name, (plain_rect, marked_rect) in SLOTS.items():
        if name in by_id:
            row = by_id[name]
            plain, _ = independent_crop(native, row["x"], row["y"], PADDING)
            marked, _ = independent_marked(plain)
        else:
            plain = np.empty((180, 180, 3), dtype=np.uint8)
            plain[:] = BACKGROUND
            marked = plain
        count += equal_pixels(region(panel, plain_rect), plain, "unmarked crop or missing slot")
        count += equal_pixels(region(panel, marked_rect), marked, "marked crop or missing slot")
    return count


def manifest_geometry(x, y):
    g = point_geometry(x, y)
    r, s = g["rounded"]
    left, top, _, _ = g["crop"]
    valid_x = sum(0 <= left + k < 720 for k in range(60))
    valid_y = sum(0 <= top + k < 480 for k in range(60))
    valid = valid_x * valid_y
    return {"rounded": [r, s], "source_rect": g["crop"],
            "rounding_difference": g["rounding_difference"],
            "rounding_difference_exact": [str(Fraction(r) - Fraction(x)), str(Fraction(s) - Fraction(y))],
            "original_coordinate_inside": g["point_in_native"],
            "rounded_cell_inside": g["rounded_cell_in_native"],
            "valid_source_pixels": valid, "padding_pixels": 3600 - valid,
            "fully_in_source_crop": valid == 3600}


def source_point_records(project):
    core = project_rows(project)
    tracks = {t["track_id"]: t for t in project["pointmass_tracks"] if t["track_id"] in IDS}
    result = []
    for simple in core:
        track = tracks[simple["track_id"]]
        saved = next(r for r in track["framedata"][0]["rows"] if r["index"] == simple["frame"])
        ordinal = track["saved_indices"].index(simple["frame"]) + 1
        require(saved["entry_ordinal_one_based"] == ordinal, "source ordinal")
        record = {"track_id": simple["track_id"], "frame_index": simple["frame"],
                  "key": simple["key"], "entry_ordinal_one_based": ordinal,
                  "source_row_xml_path": saved["xml_path"], "source_track_xml_path": track["xml_path"]}
        for axis in ("x", "y"):
            cell = saved["objects"][0]["coordinates"][axis]["occurrences"][0]
            literal, value = cell["saved_text"], simple[axis]
            sha = hashlib.sha256(literal.encode()).hexdigest()
            require(sha == cell["text_sha256"], "saved literal hash")
            record.update({axis: value, axis + "_saved_text": literal,
                           axis + "_saved_text_sha256": sha, axis + "_float_hex": float(value).hex(),
                           axis + "_xml_path": cell["xml_path"]})
        record.update(manifest_geometry(simple["x"], simple["y"]))
        result.append(record)
    return result


def label_specs(frame, points, synthetic=False, synthetic_rgb=False):
    """Literal frozen labeling contract, independent of producer execution."""
    prefix = "SYNTHETIC CONTROL | " if synthetic else "SOURCE-GUIDED H0 | "
    labels = [
        (12, 8, 1104, prefix + f"frame {frame['index']} | PTS {frame['pts']} * {frame['time_base']} = {frame['time_seconds_exact']} s"),
        (12, 28, 1104, "H0 conditional: native 720x480, x right/y down; no SAR correction, rotation, time shift or fitted transform."),
        (12, 56, 720, "Complete synthetic RGB coordinate-pattern image, unmarked."
         if synthetic and synthetic_rgb else "Complete native image, unmarked (Y plane repeated as RGB for this panel)."),
    ]
    by_id = {r["track_id"]: r for r in points}
    require(len(by_id) == len(points) and set(by_id) <= set(IDS), "label row coverage")
    for name, top in ((IDS[0], 56), (IDS[1], 336)):
        if name not in by_id:
            labels.extend([(744, top, 372, name.upper() + ": NO SAVED ROW"),
                           (744, top + 16, 372, "No counterpart invented; blank slots are not data.")])
            continue
        row = by_id[name]
        g = manifest_geometry(row["x"], row["y"])
        labels.extend([
            (744, top, 372, f"{name.upper()} key={str(row['key']).lower()} | saved image-space"),
            (744, top + 16, 372, "x=" + row["x_saved_text"]),
            (744, top + 32, 372, "y=" + row["y_saved_text"]),
            (744, top + 48, 372, f"cell={g['rounded']} inside: xy={g['original_coordinate_inside']} cell={g['rounded_cell_inside']}"),
            (744, top + 64, 180, "Unmarked / 3x nearest"),
            (936, top + 64, 180, "Marked / gap at (91,91)"),
        ])
    labels.extend([
        (12, 568, 720, "Cyan arms mark a rounded cell; center/gap untouched. Unmarked crop remains alongside."),
        (12, 586, 720, "Magenta is outside-source padding, not evidence; separate 60x60 validity masks retained."),
        (12, 604, 720, "Saved key status does not establish manual marking. H0 does not establish material-point identity."),
        (12, 622, 720, "Encoded PTS are not authenticated exposure times or the assigned analysis clock."),
    ])
    return labels


def check_complete_panel(panel, native, points, frame, synthetic=False):
    count = check_panel_regions(panel, native, points)
    expected = np.empty_like(panel); expected[:] = BACKGROUND
    expected[72:552, 12:732] = np.stack([native] * 3, axis=2) if native.ndim == 2 else native
    protected = np.zeros(panel.shape[:2], dtype=bool)
    for rect in [NATIVE_RECT] + [r for pair in SLOTS.values() for r in pair]:
        region(protected, rect)[:] = True
    for row in points:
        plain, _ = independent_crop(native, row["x"], row["y"], PADDING)
        marked, _ = independent_marked(plain)
        a, b = SLOTS[row["track_id"]]
        region(expected, a)[:] = plain
        region(expected, b)[:] = marked
    canvas = Image.fromarray(expected)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=12)
    label_count = 0
    for x, y, width, text in label_specs(frame, points, synthetic, native.ndim == 3):
        box = draw.textbbox((x, y), text, font=font)
        # The fixed default font's leading 'x' has a -1 pixel left bearing.
        # This one-pixel glyph allowance stays outside all protected regions;
        # it is not permission to widen source rectangles or clip a label.
        require(draw.textlength(text, font=font) <= width
                and box[0] >= x - 1 and box[1] >= y
                and box[2] <= x + width + 1 and box[3] <= y + 16,
                "label remains within declared exterior band")
        require(not np.any(region(protected, box)), "label intersects a protected image region")
        draw.text((x, y), text, font=font, fill=(240, 240, 240))
        label_count += 1
    equal_pixels(panel, np.asarray(canvas), "complete panel including labels/background")
    return {"protected_channel_samples": count, "all_panel_channel_samples": int(panel.size),
            "exterior_labels_checked": label_count}


def same(actual, expected, label):
    require(type(actual) is type(expected), label + " type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), label + " keys")
        for key in expected:
            same(actual[key], expected[key], label + "/" + str(key))
    elif isinstance(expected, list):
        require(len(actual) == len(expected), label + " length")
        for i, (a, b) in enumerate(zip(actual, expected)):
            same(a, b, label + "/" + str(i))
    else:
        require(actual == expected, label + " value")


def historical_sources():
    pins = {}
    documents = {}
    for name, sha in PINS.items():
        path = SOURCE / name
        require(digest(path) == sha, "held input identity: " + name)
        pins[str(path)] = identity(path)
        if name.endswith(".json"):
            documents[name] = read_json(path)
    for path, sha in AUTHORITY_PINS.items():
        require(digest(path) == sha, "control/runtime pin: " + path.name)
        pins[str(path)] = identity(path)
    same(documents["views02/frames.json"], documents["views01/frames.json"], "held hash-map repeats")
    source_clock(documents["probe01/probe.json"], documents["probe01/selection.json"],
                 documents["views01/frames.json"])
    return documents, pins


def expected_manifest(documents):
    points = source_point_records(documents["project01.json"])
    hashes = documents["views01/frames.json"]
    frames, enriched, png_types = [], [], {}
    for n in FRAME_INDICES:
        baseline = hashes[n]
        frame = {k: baseline[k] for k in ("index", "pts", "time_seconds_exact", "decoded_sha256", "luma_sha256")}
        frame.update(time_base="1/60000", native_png=f"native/frame-{n:04d}.png",
                     panel_png=f"panels/frame-{n:04d}.png")
        png_types[frame["native_png"]] = ("L", (720, 480))
        png_types[frame["panel_png"]] = ("RGB", PANEL_SIZE)
        current = [r for r in points if r["frame_index"] == n]
        slots = {}
        for name in IDS:
            rows = [r for r in current if r["track_id"] == name]
            if not rows:
                slots[name] = {"status": "missing_saved_row"}
                continue
            row = rows[0]
            slots[name] = {"status": "saved_row", "row_key": [n, name],
                           **manifest_geometry(row["x"], row["y"])}
            out = {**row, "pts": baseline["pts"], "time_base": "1/60000",
                   "time_seconds_exact": baseline["time_seconds_exact"]}
            for kind in ("plain", "marked", "mask"):
                filename = f"crops/{name}-f{n:04d}-{kind}.png"
                out[kind + "_png"] = filename
                png_types[filename] = ("L", (60, 60)) if kind == "mask" else ("RGB", (180, 180))
            enriched.append(out)
        frame["slots"] = slots
        frames.append(frame)
    return {
        "schema_version": 1, "status": "representation_only_not_visual_acceptance",
        "hypothesis": "H0 direct saved image xy to native720x480; no transform",
        "sample_aspect_ratio_unapplied": "131:144", "selection_indices": list(FRAME_INDICES),
        "row_count": 83, "layout": EXPECTED_LAYOUT,
        "source_project_sha256": PINS["project01.json"],
        "source_media_sha256": PINS["source/TiltedCameraWTC7Clip.mp4"],
        "frames": frames, "points": enriched,
    }, png_types


def read_png(path, mode, size, metadata):
    with Image.open(path) as im:
        require(im.format == "PNG" and im.mode == mode and im.size == size, "PNG format/mode/size")
        pixels = np.asarray(im).copy()
    same(metadata, {**identity(path), "mode": mode, "size": list(size),
                    "pixel_sha256": hashlib.sha256(pixels.tobytes()).hexdigest()}, "PNG metadata")
    return pixels


def verify_run(run, documents, source_pins, producer_sha):
    require(run.parent == HERE and run.is_dir() and not run.is_symlink(), "direct owned run directory")
    require(not (run / "failure.json").exists(), "failed producer run not admitted")
    manifest = read_json(run / "manifest.json")
    expected, png_types = expected_manifest(documents)
    require(set(manifest) == set(expected) | {"products"}, "manifest field scope")
    same({k: manifest[k] for k in expected}, expected, "independent manifest")
    require(set(manifest["products"]) == set(png_types) and len(png_types) == 349, "all 349 PNG products")
    meta_files = {"probe.json", "probe.stdout.json", "frames.json", "manifest.json", "probe-execution.json",
                  "decode-execution.json", "probe.stderr", "decode.stderr"}
    substantive_names = set(png_types) | meta_files
    actual_files = {str(p.relative_to(run)) for p in run.rglob("*") if p.is_file()}
    require(actual_files == substantive_names | {"input-receipt.json", "receipt.json"}, "exact complete run inventory")
    require(not any(p.is_symlink() for p in run.rglob("*")), "no symlink products")
    same(read_json(run / "probe.json"), documents["probe01/probe.json"], "complete probe repeat")
    same(read_json(run / "frames.json"), documents["views01/frames.json"], "all 476 decoded/luma/PTS rows")
    receipt, initial = read_json(run / "receipt.json"), read_json(run / "input-receipt.json")
    require(receipt["status"] == "prepared_pending_independent_checks_and_review", "producer status")
    same(receipt["determinism_exceptions"], ["input-receipt.json", "receipt.json"], "only explicit path exceptions")
    for key in ("no_historical_view_performed", "no_new_coordinate_measurement", "all_476_hashes_and_pts_match"):
        require(receipt[key] is True, "producer scope flag")
    require(receipt["output_directory"] == initial["output_directory"] == str(run), "run path receipt")
    require(initial["reviewed_producer_sha256"] == producer_sha and initial["no_human_review_claim"] is True,
            "reviewed producer and no human approval claim")
    same(receipt["inputs_before"], receipt["inputs_after"], "producer pre/post pin equality")
    same(initial["inputs_before"], receipt["inputs_before"], "initial/final input pins")
    same(initial["argv"], receipt["argv"], "initial/final invocation")
    expected_pins = {p: pin for p, pin in source_pins.items() if p != str(SOURCE / "views02/frames.json")}
    for path in (HERE / "prepare.py", HERE / "test_prepare.py", Path(sys.executable),
                 Path(Image.__file__), Path(Image.core.__file__), Path(ImageDraw.__file__), Path(ImageFont.__file__)):
        expected_pins[str(path)] = identity(path)
    require(digest(HERE / "prepare.py") == producer_sha, "current reviewed producer bytes")
    same(receipt["inputs_before"], expected_pins, "exact permitted source/procedure/runtime pins")
    require(initial["python"] == "3.12.14" and initial["pillow"] == PILLOW_VERSION == "12.3.0",
            "declared producer runtime")
    require(set(receipt["products"]) == substantive_names, "receipt complete substantive products")
    for name in substantive_names:
        same(receipt["products"][name], identity(run / name), "product file pin")
    for stage in ("probe", "decode"):
        execution = read_json(run / (stage + "-execution.json"))
        same(execution, receipt[stage + "_execution"], "execution receipt join")
        require(execution["returncode"] == 0 and execution["stderr_bytes"] == 0
                and (run / (stage + ".stderr")).read_bytes() == b""
                and execution["stderr_sha256"] == hashlib.sha256(b"").hexdigest(), "empty successful diagnostics")
        if stage == "decode":
            old = documents["views01/receipt.json"]["execution"]
            same(execution["argv"], old["argv"], "unmodified decode command")
            require(execution["stdout_bytes"] == old["raw_bytes"]
                    and execution["stdout_sha256"] == old["raw_sha256"], "full decoded raw-stream identity")
        else:
            same(execution["argv"], documents["probe01/execution.json"]["argv"], "unmodified probe command")
            stdout = (run / "probe.stdout.json").read_bytes()
            require(len(stdout) == execution["stdout_bytes"]
                    and hashlib.sha256(stdout).hexdigest() == execution["stdout_sha256"], "exact retained probe stdout")
            same(read_json(run / "probe.stdout.json"), documents["probe01/probe.json"], "raw probe JSON content")
    totals = {"native_luma_samples": 0, "crop_channel_samples": 0, "mask_samples": 0,
              "protected_channel_samples": 0, "all_panel_channel_samples": 0, "exterior_labels_checked": 0}
    for frame in expected["frames"]:
        native = read_png(run / frame["native_png"], "L", (720, 480), manifest["products"][frame["native_png"]])
        require(hashlib.sha256(native.tobytes()).hexdigest() == frame["luma_sha256"], "native-to-prior luma identity")
        totals["native_luma_samples"] += native.size
        points = [r for r in expected["points"] if r["frame_index"] == frame["index"]]
        for point in points:
            plain, valid = independent_crop(native, point["x"], point["y"], PADDING)
            marked, _ = independent_marked(plain)
            mask = valid[::3, ::3].astype(np.uint8) * 255
            for kind, wanted in (("plain", plain), ("marked", marked), ("mask", mask)):
                name = point[kind + "_png"]
                mode, size = png_types[name]
                actual = read_png(run / name, mode, size, manifest["products"][name])
                n = equal_pixels(actual, wanted, "every independent " + kind + " pixel")
                totals["mask_samples" if kind == "mask" else "crop_channel_samples"] += n
        panel = read_png(run / frame["panel_png"], "RGB", PANEL_SIZE, manifest["products"][frame["panel_png"]])
        for key, value in check_complete_panel(panel, native, points, frame).items():
            totals[key] += value
    return {"run": str(run), "frames": 50, "rows": 83, "pngs": 349, "all_clock_rows": 476,
            "totals": totals, "substantive": receipt["products"]}


def exclusive_report(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, sort_keys=True); stream.write("\n")


def verify_synthetic_fixture_directory(directory, producer_sha):
    """Independently check saved producer fixtures; never imports its code."""
    receipt = read_json(directory / "receipt.json")
    require(receipt["successful"] is True and receipt["tests_run"] == 13
            and receipt["failures"] == receipt["errors"] == 0,
            "completed synthetic producer controls")
    require(receipt["historical_decode_or_view"] is False, "synthetic fixture scope")
    same(receipt["inputs_before"], receipt["inputs_after"], "synthetic producer stable pins")
    require(receipt["inputs_before"][str(HERE / "prepare.py")]["sha256"] == producer_sha,
            "synthetic fixtures bound to final producer")
    for relative, pin in receipt["products"].items():
        require(not Path(relative).is_absolute() and ".." not in Path(relative).parts, "local fixture path")
        same(identity(directory / relative), pin, "synthetic product pin")
    fixture = read_json(directory / "fixtures.json")
    require(fixture["status"] == "synthetic_only" and
            fixture["pattern"] == "RGB(x%256,y%256,x//256+4*(y//256))", "declared coordinate pattern")
    same(fixture["layout"], EXPECTED_LAYOUT, "synthetic layout")
    yy, xx = np.indices((480, 720))
    native = np.stack((xx % 256, yy % 256, xx // 256 + 4 * (yy // 256)), axis=2).astype(np.uint8)
    image = read_png(directory / "synthetic-native.png", "RGB", (720, 480), fixture["products"]["synthetic-native.png"])
    equal_pixels(image, native, "independent entire synthetic coordinate pattern")
    wanted = {
        "central": [(IDS[0], 360.5, 240.25, False), (IDS[1], 100.5, 200.5, True)],
        "boundaries": [(IDS[0], -0.4, 0, False), (IDS[1], 719.8, 479.8, True)],
        "missing": [(IDS[1], -100.5, -100.5, True)],
    }
    records = fixture["fixtures"]
    require([r["name"] for r in records] == list(wanted), "three fixed fixtures")
    sums = {"panels": 0, "crop_files": 0, "mask_files": 0, "all_panel_channel_samples": 0}
    for record in records:
        name = record["name"]
        frame = {"index": 0, "pts": 17, "time_base": "1/60000", "time_seconds_exact": "17/60000"}
        points = [{"track_id": track, "frame_index": 0, "x": x, "y": y, "key": key,
                   "x_saved_text": str(x), "y_saved_text": str(y)} for track, x, y, key in wanted[name]]
        same(record["frame"], frame, "synthetic clock")
        same(record["points"], points, "fixed synthetic fixture points")
        expected_slots = {track: {"status": "missing_saved_row"} for track in IDS}
        for row in points:
            track = row["track_id"]
            expected_slots[track] = {"status": "saved_row", "row_key": [0, track],
                                     **manifest_geometry(row["x"], row["y"])}
            plain, valid = independent_crop(native, row["x"], row["y"], PADDING)
            marked, _ = independent_marked(plain)
            for kind, pixels in (("plain", plain), ("marked", marked), ("mask", valid[::3, ::3].astype(np.uint8) * 255)):
                filename = f"{name}-{track}-{kind}.png"
                mode, size = ("L", (60, 60)) if kind == "mask" else ("RGB", (180, 180))
                actual = read_png(directory / filename, mode, size, fixture["products"][filename])
                equal_pixels(actual, pixels, "independent synthetic " + kind)
                sums["mask_files" if kind == "mask" else "crop_files"] += 1
        same(record["slots"], expected_slots, "synthetic slots and exact geometry")
        require(record["panel_png"] == name + "-panel.png", "fixed synthetic panel path")
        panel = read_png(directory / record["panel_png"], "RGB", PANEL_SIZE, fixture["products"][record["panel_png"]])
        outcome = check_complete_panel(panel, native, points, frame, synthetic=True)
        sums["all_panel_channel_samples"] += outcome["all_panel_channel_samples"]
        sums["panels"] += 1
    return {"status": "pass_synthetic_representation", "directory": str(directory),
            "producer_sha256": producer_sha, "fixture_sha256": digest(directory / "fixtures.json"), **sums}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", nargs=2, type=Path, required=True)
    parser.add_argument("--reviewed-producer-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    # This command is historical validation, never a default/import action.
    runs = [p.resolve() for p in args.runs]
    require(len(set(runs)) == 2 and all(p.parent == HERE for p in runs), "two distinct owned run paths")
    out = args.out.resolve()
    require(out.parent == HERE and re.fullmatch(r"verification[a-z0-9_-]*\.json", out.name)
            and not out.exists(), "new owned verification receipt required")
    require(HEX256.fullmatch(args.reviewed_producer_sha256), "explicit producer review hash")
    procedure = {str(p): identity(p) for p in (Path(__file__), HERE / "test_verify.py", Path(sys.executable))}
    result = {"status": "started", "argv": sys.argv, "procedure": procedure,
              "python": sys.version, "pillow": PILLOW_VERSION, "numpy": np.__version__,
              "producer_imported": False, "historical_images_displayed": False,
              "physical_or_human_acceptance": False}
    code = 1
    try:
        documents, pins = historical_sources()
        results = [verify_run(run, documents, pins, args.reviewed_producer_sha256) for run in runs]
        same(results[0]["substantive"], results[1]["substantive"], "two complete substantive repeats")
        for name in results[0]["substantive"]:
            require((runs[0] / name).read_bytes() == (runs[1] / name).read_bytes(), "actual repeat byte equality")
        require(all(identity(Path(path)) == pin for path, pin in {**pins, **procedure}.items()), "post-check source/procedure pins")
        result.update(status="pass_representation_only", source_pins=pins,
                      runs=[{k: v for k, v in r.items() if k != "substantive"} for r in results],
                      substantive_files_per_run=len(results[0]["substantive"]),
                      substantive_repeat_byte_identity=True,
                      remaining_limits=["shared Pillow/font decoder dependency", "H0 historical raster mapping unverified",
                                        "no visual interpretation, original-track validation or cause finding"])
        code = 0
    except Exception as error:
        result.update(status="failed_not_admitted", error_type=type(error).__name__, error=str(error))
    exclusive_report(out, result)
    print(json.dumps({"status": result["status"], "receipt": str(out), "sha256": digest(out)}, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
