#!/usr/bin/env python3
"""Offline, deterministic comparison of independent batch-2 observation axes."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from PIL import Image


PROTOCOL_SHA256 = "8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff"
PROVENANCE_KEY_SHA256 = "c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3"
SOURCE_DIR = Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation")
KEY_PATH = "assets/run-01/reviewed-provenance-key.json"
SAMPLE = (
    "A-873f87e7149b", "A-e1b0c06ad11d", "A-9e7b4935c8aa", "A-0b722775db93",
    "A-fa6f410444bb", "A-ffe3726a0312", "A-0e60b82a1a4c", "A-6902e91e39ee",
    "A-671f312eade8", "A-69d899e75343", "A-8bc36f05fe38", "A-7b61385d1373",
    "A-f1e2fa01e344",
)
TOP_FIELDS = {"reviewer", "independence", "protocol_sha256", "provenance_key_sha256", "assets"}
ASSET_FIELDS = {
    "asset_id", "image_sha256", "dimensions", "complete_native_image_inspected",
    "target_rect", "target_evaluability", "target_reason", "luminous_features",
    "smoke", "nondetection_regions", "visibility_limits", "overlay_regions",
}
LUMINOUS_FIELDS = {"rect", "appearance", "target_relation", "reason", "alternatives"}
TARGET_STATUSES = {"partial_detail", "limited_detail", "unresolved_target"}
LUMINOUS_APPEARANCES = {"flame_like", "ambiguous_glow"}
TARGET_RELATIONS = {"on_candidate_facade", "uncertain"}
SMOKE_STATUSES = {"visible", "uncertain", "not_identified"}


class ValidationError(ValueError):
    """Frozen schema or source verification failed."""


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
        value = json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        raise ValidationError(f"invalid JSON: {exc}") from exc
    finite_tree(value)
    return value


def read_json(path):
    data = Path(path).read_bytes()
    return decode_json(data), sha256_bytes(data)


def nonblank(value, context):
    require(isinstance(value, str) and bool(value.strip()), f"{context} must be a nonblank string")


def enum(value, choices, context):
    require(isinstance(value, str) and value in choices, f"invalid {context}")


def exact_fields(value, fields, context):
    require(isinstance(value, dict) and set(value) == fields,
            f"{context} must have exactly the protocol fields")


def string_list(value, context, *, nonempty=False):
    require(isinstance(value, list), f"{context} must be a list")
    if nonempty:
        require(bool(value), f"{context} must not be empty")
    for item in value:
        nonblank(item, context)


def dimensions(value, context):
    require(isinstance(value, list) and len(value) == 2
            and all(type(item) is int and item > 0 for item in value),
            f"{context} must contain two positive integer dimensions, not booleans")


def rectangle(value, size, context):
    require(isinstance(value, list) and len(value) == 4, f"{context} must have four coordinates")
    for coordinate in value:
        require(type(coordinate) is int
                or (type(coordinate) is float and math.isfinite(coordinate)),
                f"{context} coordinates must be finite numbers, not booleans")
    x0, y0, x1, y1 = value
    require(0 <= x0 < x1 <= size[0] and 0 <= y0 < y1 <= size[1],
            f"{context} must be in bounds and nondegenerate")


def rectangle_list(value, size, context):
    require(isinstance(value, list), f"{context} must be a list")
    for rect in value:
        rectangle(rect, size, context)


def extract_pins(key):
    """Use only byte/dimension metadata; no captions or earlier labels."""
    require(isinstance(key, dict) and isinstance(key.get("assets"), list),
            "provenance key must contain assets")
    require(len(key["assets"]) == 28, "provenance key must retain 28 extraction assets")
    by_id = {}
    for entry in key["assets"]:
        require(isinstance(entry, dict), "provenance asset must be an object")
        asset_id = entry.get("asset_id")
        nonblank(asset_id, "provenance asset_id")
        require(asset_id not in by_id, "duplicate provenance asset_id")
        by_id[asset_id] = entry
    pins = {}
    for asset_id in SAMPLE:
        require(asset_id in by_id, "declared sample asset absent from provenance key")
        entry = by_id[asset_id]
        view = entry.get("extracted_view")
        require(isinstance(view, dict), "provenance extracted_view missing")
        expected_path = f"assets/run-01/images/{asset_id}.jpg"
        require(view.get("path") == expected_path, "unexpected source image path")
        digest = view.get("sha256")
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
                "invalid source image SHA-256")
        dimensions(view.get("dimensions"), "source image")
        dimensions(entry.get("native_pdf_dimensions"), "native PDF image")
        require(view["dimensions"] == entry["native_pdf_dimensions"], "source/native dimension mismatch")
        require(view.get("format") == "JPEG", "source metadata must specify JPEG")
        require(type(view.get("bytes")) is int and view["bytes"] > 0, "invalid image byte size")
        pins[asset_id] = {"asset_id": asset_id, "path": expected_path,
                          "sha256": digest, "dimensions": view["dimensions"],
                          "bytes": view["bytes"]}
    return pins


def verify_sources(source_dir, protocol_path):
    protocol_hash = sha256_bytes(Path(protocol_path).read_bytes())
    require(protocol_hash == PROTOCOL_SHA256, "protocol SHA-256 mismatch")
    key, key_hash = read_json(Path(source_dir) / KEY_PATH)
    require(key_hash == PROVENANCE_KEY_SHA256, "provenance key SHA-256 mismatch")
    pins = extract_pins(key)
    for asset_id, pin in pins.items():
        path = Path(source_dir) / pin["path"]
        encoded = path.read_bytes()
        require(len(encoded) == pin["bytes"], f"image byte-size mismatch: {asset_id}")
        require(sha256_bytes(encoded) == pin["sha256"], f"image SHA-256 mismatch: {asset_id}")
        # Header inspection only: no pixel decoding, rendering, processing or save.
        with Image.open(path) as image:
            require(image.format == "JPEG", f"source format mismatch: {asset_id}")
            require(list(image.size) == pin["dimensions"], f"full-source dimensions mismatch: {asset_id}")
    return pins, {"protocol_sha256": protocol_hash, "provenance_key_sha256": key_hash,
                  "images": [pins[asset_id] for asset_id in SAMPLE]}


def validate_labels(data, pins):
    require(isinstance(data, dict), "observation record must be an object")
    finite_tree(data)
    require(TOP_FIELDS <= set(data), "observation record missing required top-level fields")
    nonblank(data["reviewer"], "reviewer")
    independence = data["independence"]
    require((isinstance(independence, str) and bool(independence.strip()))
            or (isinstance(independence, dict) and bool(independence)),
            "independence must be a nonblank string or nonempty object")
    require(data["protocol_sha256"] == PROTOCOL_SHA256, "record protocol SHA-256 mismatch")
    require(data["provenance_key_sha256"] == PROVENANCE_KEY_SHA256, "record provenance SHA-256 mismatch")
    require(isinstance(data["assets"], list), "record assets must be a list")
    seen = set()
    for asset in data["assets"]:
        exact_fields(asset, ASSET_FIELDS, "asset")
        asset_id = asset["asset_id"]
        nonblank(asset_id, "asset_id")
        require(asset_id in SAMPLE, "unknown or out-of-sample asset_id")
        require(asset_id not in seen, "duplicate asset_id")
        seen.add(asset_id)
        pin = pins[asset_id]
        require(asset["image_sha256"] == pin["sha256"], "record image SHA-256 mismatch")
        dimensions(asset["dimensions"], "record image")
        require(asset["dimensions"] == pin["dimensions"], "record image dimensions mismatch")
        require(asset["complete_native_image_inspected"] is True,
                "complete_native_image_inspected must be true")
        enum(asset["target_evaluability"], TARGET_STATUSES, "target_evaluability")
        nonblank(asset["target_reason"], "target_reason")
        size = asset["dimensions"]
        if asset["target_evaluability"] == "unresolved_target":
            require(asset["target_rect"] is None, "unresolved target requires null target_rect")
        else:
            rectangle(asset["target_rect"], size, "target_rect")
        require(isinstance(asset["luminous_features"], list), "luminous_features must be a list")
        for feature in asset["luminous_features"]:
            exact_fields(feature, LUMINOUS_FIELDS, "luminous feature")
            rectangle(feature["rect"], size, "luminous feature rect")
            enum(feature["appearance"], LUMINOUS_APPEARANCES, "luminous appearance")
            enum(feature["target_relation"], TARGET_RELATIONS, "luminous target_relation")
            nonblank(feature["reason"], "luminous reason")
            string_list(feature["alternatives"], "luminous alternatives", nonempty=True)
        smoke = asset["smoke"]
        exact_fields(smoke, {"status", "regions", "reason"}, "smoke")
        enum(smoke["status"], SMOKE_STATUSES, "smoke status")
        rectangle_list(smoke["regions"], size, "smoke regions")
        nonblank(smoke["reason"], "smoke reason")
        if smoke["status"] == "visible":
            require(bool(smoke["regions"]), "visible smoke requires at least one locator")
        if smoke["status"] == "not_identified":
            require(not smoke["regions"], "not_identified smoke requires empty regions")
        require(isinstance(asset["nondetection_regions"], list), "nondetection_regions must be a list")
        for region in asset["nondetection_regions"]:
            exact_fields(region, {"rect", "reason"}, "nondetection region")
            rectangle(region["rect"], size, "nondetection rect")
            nonblank(region["reason"], "nondetection reason")
        string_list(asset["visibility_limits"], "visibility_limits", nonempty=True)
        rectangle_list(asset["overlay_regions"], size, "overlay_regions")
    require(seen == set(SAMPLE) and len(data["assets"]) == 13, "missing sample assets")
    return data


def axis_values(asset):
    """Descriptive presence axes, with no exclusive-class or severity inference."""
    return {
        "target_evaluability": asset["target_evaluability"],
        "flame_like_identified": any(f["appearance"] == "flame_like" for f in asset["luminous_features"]),
        "ambiguous_glow_identified": any(f["appearance"] == "ambiguous_glow" for f in asset["luminous_features"]),
        "smoke_status": asset["smoke"]["status"],
        "nondetection_region_identified": bool(asset["nondetection_regions"]),
    }


def paired_value(left, right):
    return {"left": left, "right": right, "identical_json": left == right}


def compare_records(records):
    comparisons = []
    for index, left in enumerate(records):
        for right in records[index + 1:]:
            left_assets = {asset["asset_id"]: asset for asset in left["assets"]}
            right_assets = {asset["asset_id"]: asset for asset in right["assets"]}
            compared_assets = []
            for asset_id in SAMPLE:
                lhs, rhs = left_assets[asset_id], right_assets[asset_id]
                left_axes, right_axes = axis_values(lhs), axis_values(rhs)
                axes = {axis: {"left": left_axes[axis], "right": right_axes[axis],
                               "comparison": "same" if left_axes[axis] == right_axes[axis] else "different"}
                        for axis in left_axes}
                regions = {field: paired_value(lhs[field], rhs[field]) for field in
                           ("target_rect", "luminous_features", "nondetection_regions", "overlay_regions")}
                regions["smoke_regions"] = paired_value(lhs["smoke"]["regions"], rhs["smoke"]["regions"])
                descriptions = {field: paired_value(lhs[field], rhs[field])
                                for field in ("target_reason", "visibility_limits")}
                descriptions["smoke_reason"] = paired_value(lhs["smoke"]["reason"], rhs["smoke"]["reason"])
                compared_assets.append({"asset_id": asset_id, "axes": axes,
                                        "regions_without_forced_matching": regions,
                                        "descriptions": descriptions})
            comparisons.append({"left_reviewer": left["reviewer"], "right_reviewer": right["reviewer"],
                                "assets": compared_assets})
    return comparisons


def verify_snapshot(report, label_paths, source_dir, protocol_path):
    sources = report["source_hashes"]
    checks = [
        (Path(protocol_path), sources["protocol_sha256"], "protocol"),
        (Path(source_dir) / KEY_PATH, sources["provenance_key_sha256"], "provenance key"),
        (Path(__file__), sources["code_sha256"], "code"),
    ]
    checks.extend((Path(source_dir) / pin["path"], pin["sha256"], pin["asset_id"])
                  for pin in sources["images"])
    checks.extend((Path(path), source["sha256"], "observation record")
                  for path, source in zip(label_paths, sources["labels"]))
    for path, expected, name in checks:
        require(sha256_bytes(path.read_bytes()) == expected, f"input changed during comparison: {name}")


def build_report(label_paths, source_dir=SOURCE_DIR, protocol_path=None):
    if protocol_path is None:
        protocol_path = Path(__file__).with_name("PROTOCOL.md")
    require(len(label_paths) >= 2, "at least two observation records required for comparison")
    pins, sources = verify_sources(source_dir, protocol_path)
    records, label_sources, reviewers = [], [], set()
    for path in label_paths:
        data, digest = read_json(path)
        validate_labels(data, pins)
        require(data["reviewer"] not in reviewers, "duplicate reviewer identity")
        reviewers.add(data["reviewer"])
        records.append(data)
        label_sources.append({"reviewer": data["reviewer"], "sha256": digest})
    sources["labels"] = label_sources
    sources["code_sha256"] = sha256_bytes(Path(__file__).read_bytes())
    report = {
        "schema_version": 2,
        "scope": "research-only descriptive comparison of the declared 13-image coverage batch",
        "limitations": [
            "Independent luminous, smoke and nondetection axes may coexist; no exclusive primary class is imposed.",
            "Rectangles are approximate locators; different box counts do not count physical fires or windows.",
            "Identical JSON or matching presence descriptions do not certify spatial agreement, detection accuracy or expert validation.",
            "No area totals, percentages, calibrated detection limits, interior-fire absence, temperatures or causes are calculated.",
            "Figure filenames do not establish independent exposures, corroboration, source clocks or fire events.",
            "The separate 28-asset inventory and prior-record preservation checks remain required before claiming extraction coverage.",
            "Reason strings are checked for presence, not automatically certified for substantive observational adequacy.",
        ],
        "sample_asset_ids": list(SAMPLE),
        "source_hashes": sources,
        "raw_records": records,
        "comparisons": compare_records(records),
    }
    verify_snapshot(report, label_paths, source_dir, protocol_path)
    return report


def write_report(report, out):
    encoded = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    with Path(out).open("x", encoding="utf-8") as stream:
        stream.write(encoded)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", type=Path, nargs="+", required=True)
    parser.add_argument("--out", type=Path, required=True, help="fresh JSON file, never overwritten")
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
    print("Saved validated descriptive comparisons to a fresh JSON file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
