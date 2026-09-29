#!/usr/bin/env python3
"""Strict, offline bookkeeping for the frozen v2 visibility pilot.

This program classifies proposed-region appearance opportunity, never fire
prevalence. Source images and geometry are read only. Output must be a new file.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from PIL import Image


PROTOCOL_SHA256 = "ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5"
GEOMETRY_SHA256 = "d7c593a6d7ccad9f1f403bf0ee8a2bfe5afd6d0c6e5dd446c3602e6a5e590a13"
SOURCE_DIR = Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation")
GEOMETRY_NAME = "geometry-main-v1.json"
SAMPLE = {
    "A-e43e4088a4a2": ("U02", "U04", "U05", "U06"),
    "A-ad43dfe2413b": (
        "R01C03", "R01C06", "R01C08", "R01C10", "R01C11",
        "R01C12", "R02C05", "R02C10", "U02",
    ),
}
PINS = {
    "A-e43e4088a4a2": {
        "path": "assets/run-01/images/A-e43e4088a4a2.jpg",
        "sha256": "6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469",
        "width": 720, "height": 478,
    },
    "A-ad43dfe2413b": {
        "path": "assets/run-01/images/A-ad43dfe2413b.jpg",
        "sha256": "8a314243feac6b213548048597e20f5e981156a77a291938b93e3b76490958b3",
        "width": 705, "height": 480,
    },
}
THRESHOLDS = (0.25, 0.5, 0.75)
IDENTITIES = {"single_candidate", "unresolved", "not_single", "clipped"}
APPEARANCES = {
    "flame_structure", "ambiguous_glow", "smoke_only_source_unknown",
    "no_flame_discernible", "non_evaluable",
}
OPPORTUNITIES = {(0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1)}
ROW_FIELDS = {
    "asset_id", "unit_id", "candidate_identity", "opportunity", "cautions",
    "decisive_exclusions", "appearance", "reason",
}
TOP_FIELDS = {
    "reviewer", "independence", "protocol_sha256", "geometry_sha256", "annotations",
}
DIFFERENCE_AXES = (
    "candidate_identity", "opportunity", "cautions", "decisive_exclusions",
    "appearance", "reason",
)


class ValidationError(ValueError):
    """An input fails the frozen protocol or source verification."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def reject_constant(value):
    raise ValidationError(f"non-finite JSON constant: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def finite_tree(value):
    """Catch overflowed JSON exponents, including inside extra metadata."""
    if isinstance(value, float):
        require(math.isfinite(value), "non-finite JSON number")
    elif isinstance(value, dict):
        for item in value.values():
            finite_tree(item)
    elif isinstance(value, list):
        for item in value:
            finite_tree(item)


def decode_json(data):
    try:
        value = json.loads(data, object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        raise ValidationError(f"invalid JSON: {exc}") from exc
    finite_tree(value)
    return value


def read_json(path):
    data = Path(path).read_bytes()
    return decode_json(data), sha256_bytes(data)


def nonblank(value, context):
    require(isinstance(value, str) and bool(value.strip()),
            f"{context} must be a nonblank string")


def number(value, context):
    require(type(value) is int or (type(value) is float and math.isfinite(value)),
            f"{context} must be a finite number, not boolean")


def interval(value, context, *, coarse=False):
    if value is None:
        return
    require(isinstance(value, list) and len(value) == 2,
            f"{context} must be null or a two-number interval")
    for bound in value:
        number(bound, context)
    require(0 <= value[0] <= value[1] <= 1,
            f"{context} must lie in [0, 1] in ascending order")
    if coarse:
        require(tuple(value) in OPPORTUNITIES,
                f"{context} is not one of the four frozen coarse intervals")


def polygon(value, width, height, context):
    require(isinstance(value, list) and len(value) >= 3,
            f"{context} must have at least three vertices")
    for point in value:
        require(isinstance(point, list) and len(point) == 2,
                f"{context} vertices must be coordinate pairs")
        number(point[0], context)
        number(point[1], context)
        require(0 <= point[0] <= width and 0 <= point[1] <= height,
                f"{context} vertex is outside the full source image")
    # Image-edge coordinates at width/height are valid boundary coordinates.


def validate_geometry(data):
    require(isinstance(data, dict) and isinstance(data.get("assets"), list),
            "geometry must contain an assets list")
    require(len(data["assets"]) == len(PINS), "geometry asset count mismatch")
    assets, units = {}, {}
    for asset in data["assets"]:
        require(isinstance(asset, dict), "geometry asset must be an object")
        asset_id = asset.get("asset_id")
        nonblank(asset_id, "geometry asset_id")
        require(asset_id in PINS and asset_id not in assets,
                "unknown or duplicate geometry asset_id")
        pin = PINS[asset_id]
        for key in ("path", "sha256", "width", "height"):
            require(asset.get(key) == pin[key], f"geometry {asset_id} {key} mismatch")
        require(type(asset["width"]) is int and type(asset["height"]) is int,
                "geometry dimensions must be integers, not booleans")
        width, height = asset["width"], asset["height"]
        polygon(asset.get("target_polygon"), width, height, "target_polygon")
        require(isinstance(asset.get("overlay_rectangles"), list),
                "overlay_rectangles must be a list")
        for rectangle in asset["overlay_rectangles"]:
            require(isinstance(rectangle, list) and len(rectangle) == 4,
                    "overlay rectangle requires four coordinates")
            for coordinate in rectangle:
                number(coordinate, "overlay rectangle")
            x0, y0, x1, y1 = rectangle
            require(0 <= x0 <= x1 <= width and 0 <= y0 <= y1 <= height,
                    "overlay rectangle outside source image")
        require(isinstance(asset.get("units"), list), "geometry units must be a list")
        for unit in asset["units"]:
            require(isinstance(unit, dict), "geometry unit must be an object")
            unit_id = unit.get("unit_id")
            nonblank(unit_id, "geometry unit_id")
            key = (asset_id, unit_id)
            require(key not in units, "duplicate geometry unit ID")
            polygon(unit.get("polygon"), width, height, f"{asset_id}/{unit_id} polygon")
            require("in_frame_fraction" in unit, "missing in_frame_fraction")
            interval(unit["in_frame_fraction"], "in_frame_fraction")
            units[key] = unit
        assets[asset_id] = asset
    for asset_id, sample_ids in SAMPLE.items():
        for unit_id in sample_ids:
            require((asset_id, unit_id) in units, "sample ID missing from geometry")
    return units


def verify_sources(source_dir, protocol_path):
    protocol_hash = sha256_bytes(Path(protocol_path).read_bytes())
    require(protocol_hash == PROTOCOL_SHA256, "protocol SHA-256 mismatch")
    geometry, geometry_hash = read_json(Path(source_dir) / GEOMETRY_NAME)
    require(geometry_hash == GEOMETRY_SHA256, "geometry SHA-256 mismatch")
    units = validate_geometry(geometry)
    image_sources = []
    for asset_id, pin in PINS.items():
        path = Path(source_dir) / pin["path"]
        image_hash = sha256_bytes(path.read_bytes())
        require(image_hash == pin["sha256"], f"image SHA-256 mismatch: {asset_id}")
        with Image.open(path) as image:
            require(image.format == "JPEG", f"source is not JPEG: {asset_id}")
            require(image.size == (pin["width"], pin["height"]),
                    f"full-source dimensions mismatch: {asset_id}")
            image.verify()
        image_sources.append({"asset_id": asset_id, **pin})
    return units, {
        "protocol_sha256": protocol_hash,
        "geometry_sha256": geometry_hash,
        "images": image_sources,
    }


def validate_labels(data):
    require(isinstance(data, dict), "labels must be an object")
    finite_tree(data)
    require(TOP_FIELDS <= set(data), "labels missing required top-level fields")
    nonblank(data["reviewer"], "reviewer")
    independence = data["independence"]
    require((isinstance(independence, str) and bool(independence.strip()))
            or (isinstance(independence, dict) and bool(independence)),
            "independence must be a nonblank string or a nonempty metadata object")
    require(data["protocol_sha256"] == PROTOCOL_SHA256, "label protocol SHA-256 mismatch")
    require(data["geometry_sha256"] == GEOMETRY_SHA256, "label geometry SHA-256 mismatch")
    annotations = data["annotations"]
    require(isinstance(annotations, list), "annotations must be a list")
    expected = {(asset_id, unit_id) for asset_id, ids in SAMPLE.items() for unit_id in ids}
    observed = set()
    for row in annotations:
        require(isinstance(row, dict) and set(row) == ROW_FIELDS,
                "each annotation must have exactly the protocol row fields")
        nonblank(row["asset_id"], "asset_id")
        nonblank(row["unit_id"], "unit_id")
        key = (row["asset_id"], row["unit_id"])
        require(key in expected, "unknown or out-of-sample annotation ID")
        require(key not in observed, "duplicate annotation ID")
        observed.add(key)
        require(isinstance(row["candidate_identity"], str)
                and row["candidate_identity"] in IDENTITIES, "invalid candidate_identity")
        require(isinstance(row["appearance"], str)
                and row["appearance"] in APPEARANCES, "invalid appearance")
        interval(row["opportunity"], "opportunity", coarse=True)
        require(isinstance(row["cautions"], list), "cautions must be a list")
        for caution in row["cautions"]:
            nonblank(caution, "caution")
        require(isinstance(row["decisive_exclusions"], list),
                "decisive_exclusions must be a list")
        for exclusion in row["decisive_exclusions"]:
            require(isinstance(exclusion, dict) and set(exclusion) == {"code", "reason"},
                    "decisive exclusion requires exactly code and reason")
            nonblank(exclusion["code"], "decisive exclusion code")
            nonblank(exclusion["reason"], "decisive exclusion reason")
        nonblank(row["reason"], "annotation reason")
    require(observed == expected and len(annotations) == 13, "missing sample annotations")
    return data


def classify(row, geometry, threshold):
    """Apply all gates before precedence; retain unresolved reasons on exclusions."""
    require(type(threshold) in (int, float) and threshold in THRESHOLDS,
            "threshold must be one of .25, .5, .75")
    excluded, unresolved, eligible = [], [], []
    identity = row["candidate_identity"]
    if identity in {"not_single", "clipped"}:
        excluded.append({"code": f"identity_{identity}", "detail": row["reason"]})
    elif identity == "unresolved":
        unresolved.append({"code": "identity_unresolved", "detail": row["reason"]})
    xs, ys = zip(*geometry["polygon"])
    spans = {"x": max(xs) - min(xs), "y": max(ys) - min(ys)}
    if min(spans.values()) < 8:
        excluded.append({"code": "native_axis_span_below_8", "detail": spans})
    in_frame = geometry["in_frame_fraction"]
    if in_frame is None:
        unresolved.append({"code": "in_frame_unknown", "detail": None})
    elif in_frame[1] == 0:
        excluded.append({"code": "in_frame_upper_zero", "detail": in_frame})
    for limitation in row["decisive_exclusions"]:
        excluded.append({"code": "decisive_exclusion", "detail": limitation})
    opportunity = row["opportunity"]
    if opportunity is None:
        unresolved.append({"code": "opportunity_unknown", "detail": None})
    elif opportunity[0] >= threshold:
        eligible.append({"code": "opportunity_lower_at_least_threshold",
                         "detail": {"opportunity": opportunity, "threshold": threshold}})
    elif opportunity[1] < threshold:
        excluded.append({"code": "opportunity_upper_below_threshold",
                         "detail": {"opportunity": opportunity, "threshold": threshold}})
    else:
        unresolved.append({"code": "opportunity_crosses_or_ends_at_threshold",
                           "detail": {"opportunity": opportunity, "threshold": threshold}})
    preliminary = "excluded" if excluded else "unknown" if unresolved else "eligible"
    conflict = preliminary == "eligible" and row["appearance"] == "non_evaluable"
    conflict_reasons = ([{"code": "semantic_conflict",
                         "detail": "Preliminary eligible opportunity paired with non_evaluable appearance; pending review."}]
                        if conflict else [])
    return {
        "asset_id": row["asset_id"], "unit_id": row["unit_id"],
        "threshold": threshold, "native_axis_span_px": spans,
        "in_frame_fraction": in_frame,
        "preliminary_status": preliminary,
        "status": "unknown" if conflict else preliminary,
        "semantic_conflict": conflict,
        "reasons": {"exclusion": excluded, "unresolved": unresolved,
                    "opportunity_satisfied": eligible, "semantic_conflict": conflict_reasons},
        "annotation": row,
    }


def reviewer_summary(labels, geometry):
    rows = {(row["asset_id"], row["unit_id"]): row for row in labels["annotations"]}
    images = []
    for asset_id, unit_ids in SAMPLE.items():
        thresholds = []
        for threshold in THRESHOLDS:
            groups = {status: [] for status in ("eligible", "unknown", "excluded")}
            preliminary = {status: 0 for status in groups}
            for unit_id in unit_ids:
                key = (asset_id, unit_id)
                result = classify(rows[key], geometry[key], threshold)
                groups[result["status"]].append(result)
                preliminary[result["preliminary_status"]] += 1
            counts = {status: len(values) for status, values in groups.items()}
            require(sum(counts.values()) == len(unit_ids), "internal count partition failure")
            thresholds.append({"threshold": threshold, "counts": counts,
                               "preliminary_counts": preliminary, "subsets": groups})
        images.append({"asset_id": asset_id, "sample_count": len(unit_ids),
                       "thresholds": thresholds})
    return {"reviewer": labels["reviewer"], "images": images}


def differences(label_sets):
    """Report every axis independently; no averaging or agreement percentage."""
    results = []
    for left_index, left in enumerate(label_sets):
        for right in label_sets[left_index + 1:]:
            left_rows = {(r["asset_id"], r["unit_id"]): r for r in left["annotations"]}
            right_rows = {(r["asset_id"], r["unit_id"]): r for r in right["annotations"]}
            axes = {axis: [] for axis in DIFFERENCE_AXES}
            for asset_id, unit_ids in SAMPLE.items():
                for unit_id in unit_ids:
                    key = (asset_id, unit_id)
                    for axis in DIFFERENCE_AXES:
                        if left_rows[key][axis] != right_rows[key][axis]:
                            axes[axis].append({"asset_id": asset_id, "unit_id": unit_id,
                                               "left": left_rows[key][axis],
                                               "right": right_rows[key][axis]})
            results.append({"left_reviewer": left["reviewer"],
                            "right_reviewer": right["reviewer"],
                            "axes": axes,
                            "counts": {axis: len(values) for axis, values in axes.items()}})
    return results


def build_report(label_paths, source_dir=SOURCE_DIR, protocol_path=None):
    if protocol_path is None:
        protocol_path = Path(__file__).with_name("PROTOCOL.md")
    geometry, sources = verify_sources(source_dir, protocol_path)
    label_sets, label_sources = [], []
    seen_reviewers = set()
    require(len(label_paths) >= 1, "at least one label file required")
    for path in label_paths:
        data, digest = read_json(path)
        validate_labels(data)
        require(data["reviewer"] not in seen_reviewers, "duplicate reviewer identity")
        seen_reviewers.add(data["reviewer"])
        label_sets.append(data)
        label_sources.append({"reviewer": data["reviewer"], "sha256": digest})
    sources["code_sha256"] = sha256_bytes(Path(__file__).read_bytes())
    sources["labels"] = label_sources
    report = {
        "schema_version": 2,
        "scope": "selected candidate-appearance opportunity subset; research-only calibration",
        "limitations": [
            "Deliberately selected 13-unit pilot; no percentages or population inference.",
            "Opportunity intervals are coarse judgments, not pixel measurements or confidence intervals.",
            "Appearance categories describe the visible portion, not verified emission or absence of interior fire.",
            "AI rule-comprehension and agreement do not establish visual accuracy or expert validation.",
            "No temperature, chronology, model-input bias, structural consequence, or cause ranking is calculated.",
        ],
        "source_hashes": sources,
        "sample": {key: list(value) for key, value in SAMPLE.items()},
        "raw_label_sets": label_sets,
        "reviewers": [reviewer_summary(labels, geometry) for labels in label_sets],
        "pairwise_differences": differences(label_sets),
    }
    verify_snapshot(report, label_paths, source_dir, protocol_path)
    return report


def verify_snapshot(report, label_paths, source_dir, protocol_path):
    """Recheck the files used in this result; no source is rewritten."""
    sources = report["source_hashes"]
    checks = [
        (Path(protocol_path), sources["protocol_sha256"], "protocol"),
        (Path(source_dir) / GEOMETRY_NAME, sources["geometry_sha256"], "geometry"),
        (Path(__file__), sources["code_sha256"], "code"),
    ]
    checks.extend((Path(source_dir) / image["path"], image["sha256"], image["asset_id"])
                  for image in sources["images"])
    checks.extend((Path(path), metadata["sha256"], "labels")
                  for path, metadata in zip(label_paths, sources["labels"]))
    for path, expected, name in checks:
        require(sha256_bytes(path.read_bytes()) == expected,
                f"input changed during summary: {name}")


def write_report(report, out):
    # Exclusive creation also rejects symlinks and protects every earlier attempt.
    encoded = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with Path(out).open("x", encoding="utf-8") as stream:
        stream.write(encoded)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True, help="fresh JSON file; never overwritten")
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    parser.add_argument("--protocol", type=Path, default=Path(__file__).with_name("PROTOCOL.md"))
    args = parser.parse_args(argv)
    try:
        require(not args.out.exists() and not args.out.is_symlink(), "output already exists")
        report = build_report(args.labels, args.source_dir, args.protocol)
        write_report(report, args.out)
    except (ValidationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print("Saved validated 13-unit calibration bookkeeping to a fresh JSON file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
