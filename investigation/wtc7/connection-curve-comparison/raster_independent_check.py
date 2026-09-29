#!/usr/bin/env python3
"""Independent, synthetic-only audit. Never imports producer functions.

This checker reads only the fixed synthetic-run01/02 directories next to this
file. It prints JSON to stdout and writes no files. Synthetic support coverage
is not historical uncertainty calibration or physical validation.
"""

from __future__ import annotations

import argparse
import hashlib
from functools import lru_cache
from fractions import Fraction
from io import BytesIO
from itertools import groupby
import json
from pathlib import Path
import platform
import sys

from PIL import Image, features


COLORS = {
    "black": (0, 0, 0), "gold": (204, 153, 0), "blue": (0, 0, 255),
    "red": (255, 0, 0), "green": (0, 128, 0), "cyan": (0, 180, 180),
    "purple": (128, 0, 128),
}
ALLOWANCES = (0, 1, 2, 4)
SIZE = (160, 96)
STAGE_SHA = "4adaa3b617a624de9353feda130c1778e0c60d00e133d88754f66baa3298b248"
CODECS = {
    "png": ("PNG", {"compress_level": 6}),
    "jpg95s0": ("JPEG", {"quality": 95, "subsampling": 0, "optimize": False, "progressive": False}),
    "jpg75s0": ("JPEG", {"quality": 75, "subsampling": 0, "optimize": False, "progressive": False}),
    "jpg75s2": ("JPEG", {"quality": 75, "subsampling": 2, "optimize": False, "progressive": False}),
    "jpg50s2": ("JPEG", {"quality": 50, "subsampling": 2, "optimize": False, "progressive": False}),
}


def rgb(value):
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("RGB must have three integer channels")
    if any(type(channel) is not int or not 0 <= channel <= 255 for channel in value):
        raise ValueError("RGB channels must be nonboolean integers from 0 to 255")
    return tuple(value)


def admitted(pixel, target):
    """Use exact rational projection/residuals, not producer integer code."""
    pixel, target = rgb(pixel), rgb(target)
    return _rational_admitted(pixel, target)


@lru_cache(maxsize=None)
def _rational_admitted(pixel, target):
    direction = tuple(255 - channel for channel in target)
    darkness = tuple(255 - channel for channel in pixel)
    norm = sum(component * component for component in direction)
    if not norm:
        raise ValueError("White target has no contrast direction")
    amount = Fraction(sum(a * b for a, b in zip(direction, darkness)), norm)
    return amount >= Fraction(1, 5) and all(
        abs(Fraction(z) - amount * q) <= 32
        for z, q in zip(darkness, direction)
    )


def row_runs(rows):
    rows = list(rows)
    if any(type(row) is not int or not 0 <= row < SIZE[1] for row in rows):
        raise ValueError("Invalid row")
    if rows != sorted(set(rows)):
        raise ValueError("Rows must be ordered and unique")
    result = []
    for _, values in groupby(enumerate(rows), key=lambda item: item[1] - item[0]):
        members = [item[1] for item in values]
        result.append([members[0], members[-1] + 1])
    return result


def selected_base(target):
    """Independent 4x4-center sampling for w1, m1/2, p1/2, dashed.

    Coordinates use sixteenths: subpixel u has an odd numerator in eighths,
    v has numerator 4*subrow+2 in sixteenths. The centerline is
    48 + (u-80)/2 + 1/2. Each channel is mixed and rounded half-up.
    """
    target = rgb(target)
    result = bytearray()
    for y in range(SIZE[1]):
        for x in range(SIZE[0]):
            hits = 0
            if 16 <= x < 144 and ((x - 16) // 8) % 2 == 0:
                for subx in range(4):
                    u8 = 8 * x + 2 * subx + 1
                    center16 = 768 + (u8 - 640) + 8
                    for suby in range(4):
                        v16 = 16 * y + 4 * suby + 2
                        hits += -8 <= v16 - center16 < 8
            result.extend((hits * channel + (16 - hits) * 255 + 8) // 16 for channel in target)
    return bytes(result)


def columns(image, target):
    if image.mode != "RGB" or image.size != SIZE:
        raise ValueError("Expected the fixed 160x96 RGB synthetic raster")
    target = rgb(target)
    pixels = image.load()
    result = []
    for x in range(16, 144):
        visible = ((x - 16) // 8) % 2 == 0
        support_y2 = [x + 17, x + 18] if visible else None
        runs = row_runs(y for y in range(96) if admitted(pixels[x, y], target))
        status = "missing" if not runs else "single" if len(runs) == 1 else "ambiguous"
        envelope = runs[0] if len(runs) == 1 else None
        coverage = {
            str(allowance): (
                2 * (envelope[0] - allowance) <= support_y2[0]
                and 2 * (envelope[1] + allowance) >= support_y2[1]
            ) if visible and envelope is not None else None
            for allowance in ALLOWANCES
        }
        result.append({
            "x": x, "truth_support": visible, "truth_centerline_y2": support_y2,
            "runs_y": runs, "status": status, "envelope_y": envelope,
            "envelope_width": envelope[1] - envelope[0] if envelope else None,
            "coverage": coverage,
        })
    return result


def boundary_controls():
    records = []

    def check(name, observed, expected):
        if observed != expected:
            raise AssertionError(f"{name}: {observed!r} != {expected!r}")
        records.append({"name": name, "passed": True})

    check("white_background_rejected", admitted((255, 255, 255), COLORS["black"]), False)
    check("contrast_50_over_255_rejected", admitted((205, 205, 205), COLORS["black"]), False)
    check("contrast_exact_one_fifth_admitted", admitted((204, 204, 204), COLORS["black"]), True)
    check("residual_exact_32_admitted", admitted((155, 203, 203), COLORS["black"]), True)
    check("residual_over_32_rejected", admitted((154, 203, 203), COLORS["black"]), False)
    check("zero_target_component_residual_boundary", admitted((204, 204, 223), COLORS["blue"]), True)
    check("zero_target_component_residual_outside", admitted((204, 204, 222), COLORS["blue"]), False)
    check("empty_runs", row_runs([]), [])
    check("edge_cells_and_disconnected_runs", row_runs([0, 1, 3, 95]), [[0, 2], [3, 4], [95, 96]])
    check("half_up_black_half_coverage", (8 * 0 + 8 * 255 + 8) // 16, 128)
    check("cache_warm_integer_pixel", admitted((0, 0, 0), COLORS["black"]), True)
    for name, action in (
        ("white_target_rejected", lambda: admitted((0, 0, 0), (255, 255, 255))),
        ("bool_rgb_rejected", lambda: rgb((True, 0, 0))),
        ("noninteger_rgb_rejected", lambda: rgb((1.0, 0, 0))),
        ("nonfinite_rgb_rejected", lambda: rgb((float("nan"), 0, 0))),
        ("out_of_range_rgb_rejected", lambda: rgb((256, 0, 0))),
        ("malformed_rgb_rejected", lambda: rgb((0, 0))),
        ("unordered_rows_rejected", lambda: row_runs([1, 0])),
        ("duplicate_rows_rejected", lambda: row_runs([1, 1])),
        ("warmed_cache_bool_pixel_rejected", lambda: admitted((False, 0, 0), COLORS["black"])),
        ("warmed_cache_float_pixel_rejected", lambda: admitted((0.0, 0, 0), COLORS["black"])),
        ("warmed_cache_bool_target_rejected", lambda: admitted((0, 0, 0), (False, 0, 0))),
        ("warmed_cache_float_target_rejected", lambda: admitted((0, 0, 0), (0.0, 0, 0))),
    ):
        try:
            action()
        except ValueError:
            records.append({"name": name, "passed": True})
        else:
            raise AssertionError(f"{name}: did not reject")
    blank = Image.new("RGB", SIZE, "white")
    blank_result = columns(blank, COLORS["black"])
    check("blank_128_missing_columns", sum(item["status"] == "missing" for item in blank_result), 128)
    check("geometric_support_64_columns_independent_of_blank_mask", sum(item["truth_support"] for item in blank_result), 64)
    marked = blank.copy()
    marked.putpixel((16, 18), (0, 0, 0))
    marked.putpixel((17, 16), (0, 0, 0))
    marked.putpixel((17, 18), (0, 0, 0))
    marked.putpixel((24, 20), (0, 0, 0))
    recovered = {item["x"]: item for item in columns(marked, COLORS["black"])}
    check("full_cell_edges_preserved", recovered[16]["envelope_y"], [18, 19])
    check("all_four_allowances_without_selection", recovered[16]["coverage"], {"0": False, "1": False, "2": True, "4": True})
    check("disconnected_runs_remain_ambiguous", recovered[17]["status"], "ambiguous")
    check("ambiguous_no_numeric_envelope", recovered[17]["envelope_y"], None)
    check("gap_candidate_does_not_become_truth_support", recovered[24]["truth_support"], False)
    check("gap_candidate_has_no_coverage_claim", recovered[24]["coverage"], {str(a): None for a in ALLOWANCES})
    return records


def producer_shape(record):
    """Translate independently calculated fields to the frozen output schema."""
    result = {key: value for key, value in record.items() if key != "coverage"}
    result["run_widths"] = [last - first for first, last in record["runs_y"]]
    envelope = record["envelope_y"]
    result["allowances"] = {
        str(a): {
            "envelope_y": [envelope[0] - a, envelope[1] + a] if envelope else None,
            "width": envelope[1] - envelope[0] + 2 * a if envelope else None,
            "covered": record["coverage"][str(a)],
        } for a in ALLOWANCES
    }
    return result


def independently_summarize(records):
    true = [item for item in records if item["truth_support"]]
    gaps = [item for item in records if not item["truth_support"]]
    result = {"true_columns": len(true), "gap_columns": len(gaps)}
    for label, subset in (("true", true), ("gap", gaps)):
        result[f"{label}_status_columns"] = {
            status: [item["x"] for item in subset if item["status"] == status]
            for status in ("missing", "ambiguous", "single")
        }
    result["gap_candidate_columns"] = [item["x"] for item in gaps if item["runs_y"]]
    result["allowances"] = {
        str(a): {
            "covered_columns": [item["x"] for item in true if item["coverage"][str(a)] is True],
            "single_enclosure_failures": [item["x"] for item in true if item["coverage"][str(a)] is False],
            "unassessed_missing_or_ambiguous": [item["x"] for item in true if item["coverage"][str(a)] is None],
        } for a in ALLOWANCES
    }
    return result


def independent_scene(scene):
    """Render known synthetic descriptors with exact rational point tests.

    This is separate from both selected_base and the producer's integer scene
    renderer. Label metadata does not paint pixels. Same-color bands are a
    union, and white masks act after their union at every subpixel sample.
    """
    counts = [0] * (SIZE[0] * SIZE[1])
    target = rgb(scene["color"])
    vertical_samples = [(row, Fraction(8 * row + 2 * subrow + 1, 8))
                        for row in range(96) for subrow in range(4)]
    for x in range(160):
        for subx in range(4):
            u = Fraction(8 * x + 2 * subx + 1, 8)
            bands = []
            for segment in scene["segments"]:
                if not segment["start"] <= u < segment["end"]:
                    continue
                if segment["dashed"] and int((u - 16) // 8) % 2:
                    continue
                center = 48 + Fraction(segment["m2"], 2) * (u - 80) + Fraction(segment["p2"], 2)
                bands.append((center - Fraction(segment["w"], 2), center + Fraction(segment["w"], 2)))
            if not bands:
                continue
            masks = [(low, high) for left, low, right, high in scene["white_masks"] if left <= u < right]
            for y, v in vertical_samples:
                if any(low <= v < high for low, high in bands) and not any(low <= v < high for low, high in masks):
                    counts[y * 160 + x] += 1
    return bytes((count * channel + (16 - count) * 255 + 8) // 16
                 for count in counts for channel in target)


def expected_ambiguity_geometry(name):
    def segment(label, slope, phase, width, start=16, end=144, dashed=False):
        return {"label": label, "m2": slope, "p2": phase, "w": width,
                "start": start, "end": end, "dashed": dashed}

    def scene(color, segments, masks=None):
        return {"color": list(COLORS[color]), "segments": segments, "white_masks": masks or []}

    if name == "dash-mask":
        return (
            scene("red", [segment("A", 1, 1, 1, dashed=True)]),
            scene("red", [segment("A", 1, 1, 1)], [[x, 0, x + 8, 96] for x in range(24, 144, 16)]),
        )
    if name == "cross-identity":
        return (
            scene("blue", [segment("A", 1, 0, 3), segment("B", -1, 0, 3)]),
            scene("blue", [segment("A", 1, 0, 3, end=80), segment("B", -1, 0, 3, end=80),
                           segment("A", -1, 0, 3, start=80), segment("B", 1, 0, 3, start=80)]),
        )
    if name == "full-occlusion":
        return scene("purple", []), scene("purple", [segment("A", 1, 1, 3)], [[0, 0, 160, 96]])
    raise ValueError("Undeclared ambiguity")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fixed_file(base, relative):
    candidate = base / relative
    if not candidate.resolve().is_relative_to(base.resolve()):
        raise ValueError("Synthetic input outside its fixed directory")
    for path in (candidate, *candidate.parents):
        if path == base.parent:
            break
        if path.is_symlink():
            raise ValueError("Synthetic inputs must not be symlinks")
    return candidate


def audit(run_name):
    here = Path(__file__).resolve().parent
    run = here / run_name
    if run_name not in ("synthetic-run01", "synthetic-run02") or run.is_symlink():
        raise ValueError("Only fixed nonsymlink synthetic runs are accepted")
    stage = (here / "RASTER-UNCERTAINTY-STAGE.md").read_bytes()
    if digest(stage) != STAGE_SHA:
        raise ValueError("Frozen stage changed")
    manifest_bytes = fixed_file(run, "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest["status"] != "completed_not_scientifically_accepted":
        raise ValueError("Incomplete producer run")
    consumed = {"manifest.json": digest(manifest_bytes)}
    mismatches = []

    def same(label, actual, expected):
        if actual != expected:
            mismatches.append({"check": label, "actual": actual, "expected": expected})

    def read_product(relative):
        data = fixed_file(run, relative).read_bytes()
        pin = {"bytes": len(data), "sha256": digest(data)}
        same(f"manifest:{relative}", pin, manifest["products"][relative])
        consumed[relative] = pin["sha256"]
        return data

    same("producer_input_pins_before_after", manifest["input_pins_before"], manifest["input_pins_after"])
    current_pins = {}
    for name in ("RASTER-UNCERTAINTY-STAGE.md", "NUMERICAL-PROTOCOL.md", "HUMAN-REVIEW-GATE.md",
                 "REGISTRATION-STAGE.md", "raster_uncertainty.py", "test_raster_uncertainty.py"):
        data = fixed_file(here, name).read_bytes()
        current_pins[name] = {"bytes": len(data), "sha256": digest(data)}
        same(f"current_input:{name}", current_pins[name], manifest["input_pins_before"][name])
    cases = []
    for color, target in COLORS.items():
        case_id = f"{color}-w1-m1-p1-dashed"
        base_rgb = selected_base(target)
        for codec, (fmt, settings) in CODECS.items():
            prefix = f"cases/{case_id}/{codec}"
            encoded = read_product(prefix + (".png" if fmt == "PNG" else ".jpg"))
            with Image.open(BytesIO(encoded)) as image:
                image.load()
                same(f"{prefix}:image_geometry", [image.width, image.height, image.mode], [160, 96, "RGB"])
                decoded_rgb = image.tobytes()
                recovered = columns(image, target)
            report = json.loads(read_product(prefix + ".json"))
            same(f"{prefix}:id", report["id"], case_id)
            same(f"{prefix}:parameters", report["parameters"], {"color": color, "rgb": list(target), "w": 1, "m2": 1, "p2": 1, "style": "dashed"})
            same(f"{prefix}:codec", report["codec"], codec)
            same(f"{prefix}:settings", report["settings"], settings)
            same(f"{prefix}:base_rgb", report["base_rgb_sha256"], digest(base_rgb))
            same(f"{prefix}:decoded_rgb", report["decoded_rgb_sha256"], digest(decoded_rgb))
            same(f"{prefix}:encoded_pin", report["encoded"], {"path": prefix + (".png" if fmt == "PNG" else ".jpg"), "bytes": len(encoded), "sha256": digest(encoded)})
            if codec == "png":
                same(f"{prefix}:independent_base_pixels", digest(decoded_rgb), digest(base_rgb))
            same(f"{prefix}:column_count", len(report["columns"]), 128)
            for index, record in enumerate(recovered):
                if index < len(report["columns"]):
                    same(f"{prefix}:column:{record['x']}", report["columns"][index], producer_shape(record))
            summary = independently_summarize(recovered)
            same(f"{prefix}:summary", report["summary"], summary)
            cases.append({"id": case_id, "codec": codec, "columns_checked": len(recovered),
                          "independent_summary_counts": {
                              "true_columns": summary["true_columns"], "gap_columns": summary["gap_columns"],
                              "true_status": {key: len(value) for key, value in summary["true_status_columns"].items()},
                              "gap_status": {key: len(value) for key, value in summary["gap_status_columns"].items()},
                              "gap_candidate_columns": len(summary["gap_candidate_columns"]),
                              "allowances": {a: {key: len(value) for key, value in data.items()}
                                             for a, data in summary["allowances"].items()},
                          }, "producer_warnings": report["warnings"]})
    ambiguities = []
    for name in ("dash-mask", "cross-identity", "full-occlusion"):
        prefix = f"ambiguity/{name}"
        latent = json.loads(read_product(prefix + "/latent.json"))
        expected_geometry = expected_ambiguity_geometry(name)
        independently_rendered = []
        for side, expected in zip(("a", "b"), expected_geometry):
            actual = {key: value for key, value in latent[side].items() if key != "description"}
            same(f"{prefix}:{side}:geometry", actual, expected)
            independently_rendered.append(independent_scene(expected))
        a, b = independently_rendered
        published = json.loads(read_product(prefix + "/results.json"))
        same(f"{prefix}:latent_geometry_differs", expected_geometry[0] != expected_geometry[1], True)
        same(f"{prefix}:independent_base_equal", a == b, True)
        same(f"{prefix}:reported_base_a", published["base_a_sha256"], digest(a))
        same(f"{prefix}:reported_base_b", published["base_b_sha256"], digest(b))
        same(f"{prefix}:reported_latent_difference", published["latent_descriptors_differ"], True)
        same(f"{prefix}:reported_base_equality", published["base_equal"], True)
        codec_checks = []
        for codec, (fmt, settings) in CODECS.items():
            saved_encoded, saved_rgb = [], []
            for side, rgb_bytes in zip(("a", "b"), independently_rendered):
                encoded = read_product(f"{prefix}/{side}-{codec}.{'png' if fmt == 'PNG' else 'jpg'}")
                stream = BytesIO()
                Image.frombytes("RGB", SIZE, rgb_bytes).save(stream, format=fmt, **settings)
                same(f"{prefix}:{side}:{codec}:independent_reencode", digest(encoded), digest(stream.getvalue()))
                with Image.open(BytesIO(encoded)) as image:
                    image.load()
                    same(f"{prefix}:{side}:{codec}:decoded_geometry", [image.width, image.height, image.mode], [160, 96, "RGB"])
                    pixels = image.tobytes()
                saved_encoded.append(encoded)
                saved_rgb.append(pixels)
                same(f"{prefix}:{side}:{codec}:reported_encoded", published["codecs"][codec][f"{side}_encoded_sha256"], digest(encoded))
                same(f"{prefix}:{side}:{codec}:reported_decoded", published["codecs"][codec][f"{side}_rgb_sha256"], digest(pixels))
            same(f"{prefix}:{codec}:encoded_pair_equal", saved_encoded[0] == saved_encoded[1], True)
            same(f"{prefix}:{codec}:decoded_pair_equal", saved_rgb[0] == saved_rgb[1], True)
            same(f"{prefix}:{codec}:reported_encoded_equality", published["codecs"][codec]["encoded_equal"], True)
            same(f"{prefix}:{codec}:reported_decoded_equality", published["codecs"][codec]["decoded_equal"], True)
            codec_checks.append(codec)
        ambiguities.append({"id": name, "latent_geometry_differs": True, "independent_base_sha256": digest(a), "codecs_checked": codec_checks})
    after = {name: digest(fixed_file(run, name).read_bytes()) for name in consumed}
    same("consumed_inputs_stable", after, consumed)
    return {
        "synthetic_only": True, "run": run_name,
        "runtime": {"python": platform.python_version(), "pillow": Image.__version__,
                    "jpeg_codec": features.version_codec("jpg"), "libjpeg_turbo": features.version_feature("libjpeg_turbo")},
        "checker_sha256": digest(Path(__file__).read_bytes()), "stage_sha256": STAGE_SHA,
        "producer_current_pins": current_pins, "consumed_file_sha256": consumed,
        "boundary_controls": boundary_controls(), "selected_cases": cases,
        "case_count": len(cases), "column_count": sum(item["columns_checked"] for item in cases),
        "ambiguities": ambiguities, "mismatches": mismatches,
        "limits": ["Prior-informed separate implementation; not blind independent historical evidence.",
                   "No producer predicate, component, envelope or renderer imports.",
                   "Shared Pillow/JPEG runtime; no independent codec implementation.",
                   "Only the fixed 35-case sample is recomputed, not all 560 cases.",
                   "Boundary controls here test this independent checker, not extra producer executions.",
                   "Synthetic equality or coverage does not calibrate historical graph uncertainty."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--run", choices=("synthetic-run01", "synthetic-run02"))
    args = parser.parse_args()
    if args.self_test == bool(args.run):
        parser.error("Choose exactly one of --self-test or --run")
    result = audit(args.run) if args.run else {"synthetic_only": True, "boundary_controls": boundary_controls()}
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("mismatches"):
        sys.exit(1)


if __name__ == "__main__":
    main()
