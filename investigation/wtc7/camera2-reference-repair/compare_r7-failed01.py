#!/usr/bin/env python3
"""Compare frozen R7 annotations to saved candidates; no matcher imports.

The helper verifies artifact identities and repeats arithmetic, not visual review.
It reads existing PNG bytes for hashes/header checks, never raw video or pixels.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parent
CRITERIA_SHA = "40a98f6bb2ca25c1cc2ea0e5a724bdfacf2da6720b060914553c379c816463fb"
FROZEN = {
    "evaluation-annotations.json": "4ef189587f0039a01b7968e83784779196008d541fa357aeec97dba159af67d6",
    "evaluation-annotations.md": "920c5b56d7d16cba9f944a0365876fa9f0bdfff46a168d352cdb5443217c245b",
    "candidate-seeds.json": "b093c5041ca34b5e1e27b617cc681f46cbd0327c6c525bec89faf43f7991078e",
    "preflight01/selection.json": "1615cf412019ea9e15d116e20007966890238c3beb68e54abfa5a08666db8fae",
    "preflight01/receipt.json": "8fea3c45f64ecf96aefa2c329d0f322a20d03ec42daea80bef9fad49706318b6",
}
FRAMES = [6654, 6751, 6931, 7013, 7104]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def load(path):
    return json.loads(path.read_text())


def frozen_checks():
    result = {name: pin(ROOT / name) for name in FROZEN}
    for name, expected in FROZEN.items():
        require(result[name]["sha256"] == expected, f"Changed frozen input: {name}")
    # The report's results are additive; its original criteria prefix is fixed.
    criteria = (ROOT / "comparison-report.md").read_bytes().split(b"\n## Results\n", 1)[0]
    require(sha(criteria) == CRITERIA_SHA, "Changed declared comparison criteria")
    result["comparison_report_criteria_prefix"] = {"bytes": len(criteria), "sha256": sha(criteria)}
    return result


def match_key(row):
    return row["camera"], row["index"], row["reference"], 2 * row["half"] + 1


def index_matches(rows):
    result = {}
    for row in rows:
        k = match_key(row)
        require(k not in result, f"Duplicate match key: {k}")
        result[k] = row
    return result


def compare(annotation, automatic, geometry):
    status = "missing_auto_record" if automatic is None else automatic["status"]
    xy = None if automatic is None else automatic.get("candidate_xy")
    valid = (isinstance(xy, list) and len(xy) == 2
             and all(type(x) is int for x in xy)
             and 0 <= xy[0] < geometry[0] and 0 <= xy[1] < geometry[1])
    result = {"automatic_status": status, "valid_native_integer_candidate": valid,
              "auto_minus_manual_xy": None,
              "automatic_acceptance_without_manual_identity_support": False}
    if annotation["status"] != "localized":
        result["outcome"] = {"ambiguous": "manual_identity_ambiguous",
                             "unavailable": "manual_feature_unavailable"}[annotation["status"]]
        result["automatic_acceptance_without_manual_identity_support"] = status == "candidate"
    elif not valid:
        result["outcome"] = "no_coordinate_comparison"
    else:
        delta = [xy[i] - annotation["xy"][i] for i in (0, 1)]
        result["auto_minus_manual_xy"] = delta
        inside = all(abs(delta[i]) <= annotation["envelope_halfwidth_xy"][i] for i in (0, 1))
        result["outcome"] = "inside_manual_envelope" if inside else "outside_manual_envelope"
    return result


def self_test():
    manual = {"status": "localized", "xy": [10, 10], "envelope_halfwidth_xy": [3, 4]}
    row = {"status": "candidate", "candidate_xy": [13, 6]}
    require(compare(manual, row, [40, 40])["outcome"] == "inside_manual_envelope", "Inclusive rectangle")
    row["candidate_xy"] = [14, 6]
    require(compare(manual, row, [40, 40])["outcome"] == "outside_manual_envelope", "Outside rectangle")
    row.update(status="rejected", candidate_xy=[10, 10])
    r = compare(manual, row, [40, 40])
    require(r["outcome"] == "inside_manual_envelope" and r["automatic_status"] == "rejected", "Rejected winner kept rejected")
    for bad in [None, [float("nan"), 10], [10.0, 10], [True, 10], [-1, 10], [40, 10]]:
        row["candidate_xy"] = bad
        require(compare(manual, row, [40, 40])["outcome"] == "no_coordinate_comparison", "Invalid coordinate")
    require(compare(manual, None, [40, 40])["automatic_status"] == "missing_auto_record", "Missing explicit")
    for status in ["ambiguous", "unavailable"]:
        r = compare({"status": status}, {"status": "candidate", "candidate_xy": [10, 10]}, [40, 40])
        require(r["auto_minus_manual_xy"] is None and r["automatic_acceptance_without_manual_identity_support"], "Unresolved identity retained")
    record = {"camera": "camera2", "index": 1, "reference": "C2-R7", "half": 9}
    try:
        index_matches([record, record])
    except ValueError:
        pass
    else:
        raise ValueError("Duplicate was not rejected")
    require(693102 * Fraction("1/2997") == Fraction("231034/999"), "Exact rational PTS")
    return "passed: inclusive/outside rectangle, rejected finite winner, invalid/missing coordinate, unresolved identity, duplicate-key rejection, rational PTS"


def read_run(name):
    directory = ROOT / name
    receipt = load(directory / "receipt.json")
    require(receipt["stage"] == "run" and receipt["status"] == "complete", f"Incomplete run: {name}")
    snapshots = {
        "snapshot-0-repair.py": ROOT / "repair.py",
        "snapshot-1-PROTOCOL.md": ROOT / "PROTOCOL.md",
        "snapshot-2-candidate-seeds.json": ROOT / "candidate-seeds.json",
        "snapshot-3-test_repair.py": ROOT / "test_repair.py",
        "snapshot-4-measure.py": ROOT.parent / "reference-motion/measure.py",
        "snapshot-5-visual-review.json": ROOT / "visual-review.json",
    }
    names = ["matches.json", "initial.json", "input-pins.json", "preflight-selection.json", "preflight-receipt.json", *snapshots]
    products = {n: pin(directory / n) for n in names}
    for n, identity in products.items():
        require(identity == receipt["products"][n], f"Receipt product mismatch: {name}/{n}")
    initial = load(directory / "initial.json")
    require(initial["pins"] == receipt["pins"], f"Before/after pin mismatch: {name}")
    for filename, original in snapshots.items():
        require(products[filename] == receipt["pins"][str(original)], f"Snapshot lineage mismatch: {name}/{filename}")
    require(products["preflight-selection.json"]["sha256"] == FROZEN["preflight01/selection.json"], "Changed selected configuration")
    require(products["preflight-receipt.json"]["sha256"] == FROZEN["preflight01/receipt.json"], "Changed preflight receipt")
    matches = index_matches(load(directory / "matches.json"))
    require(len(matches) == 852, f"Unexpected historical match count: {name}")
    return {"directory": directory, "receipt": receipt, "products": products,
            "initial_runtime": {k: v for k, v in initial.items() if k != "pins"}, "matches": matches}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    tests = self_test()
    if args.self_test and args.output is None:
        print(tests)
        return
    require(args.output is not None, "Specify --output; file must not already exist")
    frozen_before = frozen_checks()
    annotation = load(ROOT / "evaluation-annotations.json")
    require(annotation["reference"] == "C2-R7" and annotation["camera"] == "camera2", "Unexpected annotation identity")
    require([r["frame"] for r in annotation["annotations"]] == FRAMES, "Changed evaluation frame set")
    runs = [read_run("run01"), read_run("run02")]
    records, images, overlays = [], {}, []
    baseline = ROOT.parent / "multiview-onset-review/refine01/camera2/f006593.png"
    expected_images = [(6593, baseline, annotation["frozen_selection"]["baseline_png_sha256"])]
    for manual in annotation["annotations"]:
        expected_images.append((manual["frame"], (ROOT / manual["png"]).resolve(), manual["png_sha256"]))
        require(int(manual["source_pts"]) * Fraction(manual["source_time_base"]) == Fraction(manual["source_time_seconds_exact"]), "Manual PTS mismatch")
        for size in [19, 27]:
            k = "camera2", manual["frame"], "C2-R7", size
            auto = runs[0]["matches"].get(k)
            repeated = runs[1]["matches"].get(k)
            require(auto == repeated, f"Run02 differs at compared key: {k}")
            if auto is not None:
                require(auto["status"] in ["candidate", "rejected"], f"Unknown status: {k}")
                require(auto["baseline_xy"] == annotation["frozen_selection"]["baseline_xy"], f"Baseline mismatch: {k}")
                require(Fraction(auto["seconds_exact"]) == Fraction(manual["source_time_seconds_exact"]), f"Exact seconds mismatch: {k}")
                require(int(auto["pts"]) * Fraction(auto["time_base"]) == Fraction(manual["source_time_seconds_exact"]), f"Raw PTS mismatch: {k}")
            record = {"camera": "camera2", "source_id_from_frozen_annotations": annotation["source_id"],
                      "frame": manual["frame"], "reference": "C2-R7", "template_size": size,
                      "manual": manual, "automatic": auto, "run02_compared_row_identical": True}
            record.update(compare(manual, auto, annotation["stored_size"]))
            records.append(record)
    for frame, path, expected_sha in expected_images:
        identity = pin(path)
        require(identity["sha256"] == expected_sha, f"Native image hash mismatch: {frame}")
        data = path.read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == (640, 480), "PNG signature/geometry mismatch")
        require(data[24:26] == bytes([8, 0]), "Expected 8-bit grayscale PNG")
        for run in runs:
            require(run["receipt"]["pins"][str(path)] == identity, f"Native image run pin mismatch: {frame}")
        images[str(path)] = identity
        for half in [9, 13]:
            name = f"overlay-{frame}-{half}.png"
            identity = pin(runs[0]["directory"] / name)
            require(identity == runs[0]["receipt"]["products"][name], f"Overlay receipt mismatch: {name}")
            overlays.append({"path": f"run01/{name}", **identity})
    require(len(records) == 10, "Expected ten comparisons")
    summaries = []
    for size in [19, 27]:
        rows = [r for r in records if r["template_size"] == size]
        summaries.append({"template_size": size, "rows": len(rows),
                          "automatic_status_counts": dict(Counter(r["automatic_status"] for r in rows)),
                          "manual_status_counts": dict(Counter(r["manual"]["status"] for r in rows)),
                          "outcome_counts": dict(Counter(r["outcome"] for r in rows)),
                          "accepted_without_manual_identity_support": sum(r["automatic_acceptance_without_manual_identity_support"] for r in rows)})
    frozen_after = frozen_checks()
    require(frozen_before == frozen_after, "Frozen inputs changed during comparison")
    output = {"schema_version": 1, "status": "complete_bounded_comparison_not_calibration",
              "python": sys.version, "executable": sys.executable, "executable_identity": pin(Path(sys.executable)),
              "script_identity": pin(Path(__file__)), "self_tests": tests,
              "frozen_before": frozen_before, "frozen_after": frozen_after,
              "runs": [{"path": str(r["directory"]), "receipt_identity": pin(r["directory"] / "receipt.json"),
                        "consumed_products": r["products"], "initial_runtime": r["initial_runtime"],
                        "status": r["receipt"]["status"], "stage": r["receipt"]["stage"]} for r in runs],
              "native_image_checks": images, "summaries": summaries, "records": records,
              "overlay_artifact_inventory": overlays,
              "visual_scope_note": "This inventory pins twelve requested overlays. The helper does not perform or attest to visual inspection; see the separate report's actual post-output coverage.",
              "context_not_manually_reannotated": [runs[0]["matches"][("camera2", frame, "C2-R6", size)] for frame in [6654, 6751] for size in [19, 27]],
              "repeat_scope": "Only the ten R7 comparison records are tested for exact run01/run02 equality here, not every historical grid or transform.",
              "interpretation_limits": "Subjective encoded-pixel envelope agreement is not calibrated accuracy, independently authenticated source identity, correct material correspondence, physical stationarity, zero/subpixel camera motion, target calibration, acceleration or cause."}
    with args.output.open("x") as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "identity": pin(args.output), "python": output["python"], "summaries": summaries}, indent=2))


if __name__ == "__main__":
    main()
