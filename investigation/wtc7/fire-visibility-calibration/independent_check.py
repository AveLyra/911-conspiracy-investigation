#!/usr/bin/env python3
"""Independent protocol arithmetic; no producer imports or image classification."""

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path


BASE = Path(__file__).resolve().parent
SOURCES = Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation")
PROTOCOL_HASH = "ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5"
GEOMETRY_HASH = "d7c593a6d7ccad9f1f403bf0ee8a2bfe5afd6d0c6e5dd446c3602e6a5e590a13"
LABEL_HASHES = {
    "main.json": "a770538e31081ab46e40dc9c26e78bf660128bc419c1491d3357839190f9c3ba",
    "reviewer.json": "ea8547d0eed74751074637dcb4f3b8d9c7108723b4f3230ff98e787eefa3dc2b",
}
IMAGE_HASHES = {
    "A-e43e4088a4a2": "6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469",
    "A-ad43dfe2413b": "8a314243feac6b213548048597e20f5e981156a77a291938b93e3b76490958b3",
}
SAMPLE = {
    "A-e43e4088a4a2": ("U02", "U04", "U05", "U06"),
    "A-ad43dfe2413b": ("R01C03", "R01C06", "R01C08", "R01C10", "R01C11",
                        "R01C12", "R02C05", "R02C10", "U02"),
}
KEYS = {(aid, uid) for aid, ids in SAMPLE.items() for uid in ids}
THRESHOLDS = (0.25, 0.5, 0.75)
STATES = ("eligible", "unknown", "excluded")
APPEARANCES = ("flame_structure", "ambiguous_glow", "smoke_only_source_unknown",
               "no_flame_discernible", "non_evaluable")
AXES = ("candidate_identity", "opportunity", "cautions", "decisive_exclusions",
        "appearance", "reason")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON object key")
        result[key] = value
    return result


def finite_json(value):
    if isinstance(value, dict):
        for child in value.values():
            finite_json(child)
    elif isinstance(value, list):
        for child in value:
            finite_json(child)
    elif type(value) is float:
        require(math.isfinite(value), "Non-finite JSON value")


def read_json(path, snapshots):
    data = path.read_bytes()
    snapshots[path.resolve()] = digest(data)
    value = json.loads(data, object_pairs_hook=unique_object)
    finite_json(value)
    return value


def interval(value, *, opportunity=False):
    if value is None:
        return
    require(type(value) is list and len(value) == 2, "Bad interval")
    require(all(type(x) in (int, float) and math.isfinite(x) for x in value),
            "Non-numeric interval endpoint")
    require(0 <= value[0] <= value[1] <= 1, "Unordered interval")
    if opportunity:
        require(value in ([0, .25], [.25, .5], [.5, .75], [.75, 1]),
                "Opportunity must be a declared coarse bin")


def identify(row):
    return row["asset_id"], row["unit_id"]


def classify(row, unit, threshold):
    """Derive gate independently from protocol clauses, collecting both axes."""
    interval(row["opportunity"], opportunity=True)
    in_frame = unit["in_frame_fraction"]
    interval(in_frame)
    xs, ys = zip(*unit["polygon"])
    span_failure = min(max(xs) - min(xs), max(ys) - min(ys)) < 8
    identity = row["candidate_identity"]
    op = row["opportunity"]
    failure = (identity in ("not_single", "clipped") or span_failure or
               (in_frame is not None and in_frame[1] == 0) or
               bool(row["decisive_exclusions"]) or
               (op is not None and op[1] < threshold))
    uncertainty = (identity == "unresolved" or op is None or in_frame is None or
                   (op is not None and op[0] < threshold <= op[1]))
    preliminary = "excluded" if failure else "unknown" if uncertainty else "eligible"
    conflict = preliminary == "eligible" and row["appearance"] == "non_evaluable"
    return {"status": "unknown" if conflict else preliminary,
            "preliminary_status": preliminary, "semantic_conflict": conflict}


def validate_rows(rows):
    require(type(rows) is list, "Labels must be a list")
    indexed = {}
    for row in rows:
        key = identify(row)
        require(key in KEYS and key not in indexed, "Unknown or duplicate sample ID")
        require(row["candidate_identity"] in
                ("single_candidate", "unresolved", "not_single", "clipped"),
                "Unknown identity")
        require(row["appearance"] in APPEARANCES, "Unknown appearance")
        interval(row["opportunity"], opportunity=True)
        require(isinstance(row["reason"], str) and row["reason"].strip(), "Missing reason")
        require(type(row["cautions"]) is list and
                all(isinstance(x, str) and x.strip() for x in row["cautions"]),
                "Bad cautions")
        require(type(row["decisive_exclusions"]) is list, "Bad exclusion list")
        for item in row["decisive_exclusions"]:
            require(type(item) is dict and all(isinstance(item.get(k), str) and
                    item[k].strip() for k in ("code", "reason")), "Missing exclusion reason")
        indexed[key] = row
    require(set(indexed) == KEYS, "Incomplete declared sample")
    return indexed


def selftest():
    unit = {"polygon": [[0, 0], [20, 0], [20, 20], [0, 20]],
            "in_frame_fraction": [1, 1]}
    row = {"candidate_identity": "single_candidate", "opportunity": [.5, .75],
           "decisive_exclusions": [], "appearance": "flame_structure", "cautions": []}
    checks = 0

    def expect(r, threshold, status, preliminary=None, conflict=False, geometry=None):
        nonlocal checks
        want = {"status": status, "preliminary_status": preliminary or status,
                "semantic_conflict": conflict}
        require(classify(r, geometry or unit, threshold) == want, "Synthetic arithmetic failed")
        checks += 1

    for category in APPEARANCES[:-1]:
        expect(dict(row, appearance=category, cautions=["glass_unknown", "minor_frame"]),
               .5, "eligible")
    expect(dict(row, opportunity=[.25, .5]), .5, "unknown")
    expect(dict(row, opportunity=[.5, .75]), .75, "unknown")
    expect(dict(row, candidate_identity="unresolved", opportunity=[0, .25]), .5, "excluded")
    expect(dict(row, candidate_identity="unresolved"), .5, "unknown")
    expect(dict(row, appearance="non_evaluable"), .5, "unknown", "eligible", True)
    expect(dict(row, candidate_identity="clipped"), .5, "excluded")
    expect(dict(row, decisive_exclusions=[{"code": "overlay", "reason": "Dominant overlay"}]),
           .5, "excluded")
    expect(dict(row, opportunity=None), .5, "unknown")
    expect(row, .5, "excluded", geometry=dict(unit, in_frame_fraction=[0, 0]))
    expect(row, .5, "unknown", geometry=dict(unit, in_frame_fraction=None))
    expect(row, .5, "eligible", geometry=dict(unit, polygon=[[0,0],[8,0],[8,8],[0,8]]))
    expect(row, .5, "excluded", geometry=dict(unit, polygon=[[0,0],[7,0],[7,8],[0,8]]))
    return checks


def compare(summary_path):
    snapshots = {}

    def pinned(path, expected):
        actual = digest(path.read_bytes())
        require(actual == expected, f"Pinned input mismatch: {path.name}")
        snapshots[path.resolve()] = actual

    pinned(BASE / "PROTOCOL.md", PROTOCOL_HASH)
    geometry_path = SOURCES / "geometry-main-v1.json"
    pinned(geometry_path, GEOMETRY_HASH)
    geometry = read_json(geometry_path, snapshots)
    geometries = {(asset["asset_id"], unit["unit_id"]): unit
                  for asset in geometry["assets"] for unit in asset["units"]}
    assets = {asset["asset_id"]: asset for asset in geometry["assets"]}
    for aid, expected in IMAGE_HASHES.items():
        pinned(SOURCES / "assets" / "run-01" / "images" / f"{aid}.jpg", expected)

    documents, rows, label_hashes = {}, {}, {}
    for filename, expected in LABEL_HASHES.items():
        path = BASE / filename
        pinned(path, expected)
        document = read_json(path, snapshots)
        role = document["reviewer"]
        require(type(role) is str and role.strip() and role not in documents,
                "Missing or duplicate reviewer name")
        require(document["protocol_sha256"] == PROTOCOL_HASH and
                document["geometry_sha256"] == GEOMETRY_HASH, "Label input pin mismatch")
        require(bool(document["independence"]), "Missing independence metadata")
        documents[role] = document
        rows[role] = validate_rows(document["annotations"])
        label_hashes[role] = expected

    summary = read_json(summary_path, snapshots)
    raw = summary["raw_label_sets"]
    require(type(raw) is list and len(raw) == len(documents), "Wrong raw label-set count")
    require({item["reviewer"]: item for item in raw} == documents,
            "Summary raw documents differ from frozen originals")
    pins = summary["source_hashes"]
    require(pins["protocol_sha256"] == PROTOCOL_HASH and
            pins["geometry_sha256"] == GEOMETRY_HASH, "Summary source pins differ")
    producer = BASE / "summarize.py"
    producer_hash = digest(producer.read_bytes())
    snapshots[producer.resolve()] = producer_hash
    require(pins["code_sha256"] == producer_hash, "Producer code hash mismatch")
    label_pins = pins["labels"]
    require(len(label_pins) == len(documents) and
            {item["reviewer"]: item["sha256"] for item in label_pins} == label_hashes,
            "Summary label pins differ")
    require(len(pins["images"]) == len(IMAGE_HASHES), "Wrong image pin count")
    seen_images = set()
    for image in pins["images"]:
        aid = image["asset_id"]
        require(aid in IMAGE_HASHES and aid not in seen_images, "Wrong image pin ID")
        seen_images.add(aid)
        path = Path(image["path"])
        if not path.is_absolute():
            path = SOURCES / path
        expected_path = SOURCES / "assets" / "run-01" / "images" / f"{aid}.jpg"
        require(path.resolve() == expected_path.resolve(), "Wrong source image path")
        require(image["sha256"] == IMAGE_HASHES[aid], "Wrong source image hash")
        require(all(type(image[axis]) is int and image[axis] == assets[aid][axis]
                    for axis in ("width", "height")), "Wrong source image dimensions")

    checked_rows = 0
    count_groups = 0
    derived_report = []
    seen_reviewers = set()
    require(len(summary["reviewers"]) == len(documents), "Wrong summary reviewer count")
    for reviewer in summary["reviewers"]:
        role = reviewer["reviewer"]
        require(role in documents and role not in seen_reviewers, "Unknown/duplicate reviewer")
        seen_reviewers.add(role)
        require(len(reviewer["images"]) == len(SAMPLE), "Wrong image group count")
        seen_assets = set()
        for image in reviewer["images"]:
            aid = image["asset_id"]
            require(aid in SAMPLE and aid not in seen_assets, "Unknown/duplicate image group")
            seen_assets.add(aid)
            expected_keys = {(aid, uid) for uid in SAMPLE[aid]}
            require(type(image["sample_count"]) is int and
                    image["sample_count"] == len(expected_keys), "Sample count differs")
            require(len(image["thresholds"]) == len(THRESHOLDS), "Wrong threshold group count")
            seen_thresholds = set()
            for scenario in image["thresholds"]:
                threshold = scenario["threshold"]
                require(type(threshold) in (float, int) and threshold in THRESHOLDS and
                        threshold not in seen_thresholds, "Unknown/duplicate threshold")
                seen_thresholds.add(threshold)
                expected = {key: classify(rows[role][key], geometries[key], threshold)
                            for key in expected_keys}
                for field, decision in (("counts", "status"),
                                        ("preliminary_counts", "preliminary_status")):
                    counts = dict.fromkeys(STATES, 0)
                    counts.update(Counter(value[decision] for value in expected.values()))
                    actual = scenario[field]
                    require(set(actual).issubset(STATES) and all(type(v) is int for v in actual.values()),
                            "Invalid status count")
                    require({state: actual.get(state, 0) for state in STATES} == counts,
                            f"Count disagreement: {role}, {aid}, {threshold}, {field}")
                require(set(scenario["subsets"]) == set(STATES), "Wrong subset names")
                seen_keys = set()
                for status, members in scenario["subsets"].items():
                    require(type(members) is list, "Subset is not a list")
                    for item in members:
                        key = identify(item)
                        require(key in expected_keys and key not in seen_keys,
                                "Unknown/duplicate classified member")
                        seen_keys.add(key)
                        require(item["annotation"] == rows[role][key], "Classified annotation changed")
                        require(type(item["threshold"]) in (float, int) and
                                item["threshold"] == threshold, "Classified threshold differs")
                        require(item["status"] == status, "Subset contradicts member status")
                        for field, value in expected[key].items():
                            require(type(item[field]) is type(value) and item[field] == value,
                                    f"Decision disagreement: {role}, {key}, {threshold}, {field}")
                        xs, ys = zip(*geometries[key]["polygon"])
                        require(item["native_axis_span_px"] ==
                                {"x": max(xs) - min(xs), "y": max(ys) - min(ys)},
                                "Native span differs")
                        require(item["in_frame_fraction"] == geometries[key]["in_frame_fraction"],
                                "In-frame input differs")
                        checked_rows += 1
                require(seen_keys == expected_keys, "Missing classified members")
                count_groups += 1
                derived_report.append({"reviewer": role, "asset_id": aid, "threshold": threshold,
                                       "counts": {state: sum(v["status"] == state for v in expected.values())
                                                  for state in STATES},
                                       "semantic_conflict_count": sum(v["semantic_conflict"]
                                                                      for v in expected.values())})

    expected_pairs = {frozenset(pair) for pair in itertools.combinations(documents, 2)}
    actual_pairs = summary["pairwise_differences"]
    require(len(actual_pairs) == len(expected_pairs), "Wrong pairwise comparison count")
    seen_pairs = set()
    difference_counts = []
    for pair in actual_pairs:
        left, right = pair["left_reviewer"], pair["right_reviewer"]
        key = frozenset((left, right))
        require(key in expected_pairs and key not in seen_pairs, "Wrong/duplicate reviewer pair")
        seen_pairs.add(key)
        require(set(pair["axes"]) == set(AXES) and set(pair["counts"]) == set(AXES),
                "Wrong comparison axes")
        totals = {}
        for axis in AXES:
            want = {unit_key: {"asset_id": unit_key[0], "unit_id": unit_key[1],
                               "left": rows[left][unit_key][axis], "right": rows[right][unit_key][axis]}
                    for unit_key in KEYS if rows[left][unit_key][axis] != rows[right][unit_key][axis]}
            actual = pair["axes"][axis]
            require(type(actual) is list and len(actual) == len(want) and
                    {identify(item): item for item in actual} == want,
                    f"Pairwise difference disagreement: {axis}")
            require(type(pair["counts"][axis]) is int and pair["counts"][axis] == len(want),
                    f"Difference count disagreement: {axis}")
            totals[axis] = len(want)
        difference_counts.append({"left_reviewer": left, "right_reviewer": right, "counts": totals})
    return {"status": "independently_reproduced", "classified_rows_checked": checked_rows,
            "reviewer_image_threshold_groups_checked": count_groups,
            "independent_counts": derived_report, "independent_difference_counts": difference_counts,
            "scope": "Frozen input hashes, complete raw-label equality, status/member/count arithmetic, "
                     "preliminary decisions, semantic conflicts and pairwise field differences. "
                     "No producer imports, image decoding, perception validation or causal inference."}, snapshots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    checks = selftest()
    if args.selftest:
        require(args.summary is None and args.out is None, "Selftest takes no historical inputs")
        print(json.dumps({"synthetic_checks_passed": checks}))
        return
    require(args.summary is not None and args.out is not None, "--summary and --out required")
    require(not args.out.exists(), "Receipt destination exists; never overwrite")
    receipt, snapshots = compare(args.summary.resolve())
    for path, old_hash in snapshots.items():
        require(digest(path.read_bytes()) == old_hash, "Input changed during independent check")
    receipt["synthetic_checks_passed"] = checks
    receipt["checker_sha256"] = digest(Path(__file__).read_bytes())
    receipt["verified_input_hashes"] = {str(path): value for path, value in snapshots.items()}
    with args.out.open("x") as handle:
        json.dump(receipt, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"status": receipt["status"], "receipt": str(args.out)}))


if __name__ == "__main__":
    main()
