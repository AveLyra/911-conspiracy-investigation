#!/usr/bin/env python3
"""Independent frozen-annotation comparison; never imports the matcher.

Reads completed run01/run02 products and existing PNG byte hashes only. Does not
decode media or change annotations, configuration, plans or run products.
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
FROZEN = {
    "independent-annotations.json": "c323d66d504c264df6792e7e5681b2d828dc6ab85db842bde0711a0e94b98b70",
    "independent-annotations.md": "bd001a83628b0a7725292a9fd957651b7268c88f2b051fcb13fb446fb0fd882e",
    "independent-comparison.md": "fc47df3a43e955674a57a87273a6e1dc7c60c9c9cbe921276cff21a54ff800f3",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def load(path):
    return json.loads(path.read_text())


def frozen_checks():
    pins = {name: pin(ROOT / name) for name in FROZEN}
    for name, expected in FROZEN.items():
        require(pins[name]["sha256"] == expected, f"Frozen file changed: {name}")
    return pins


def key(row):
    return row["camera"], row["index"], row["reference"], 2 * row["half"] + 1


def index_rows(rows):
    indexed = {}
    for row in rows:
        k = key(row)
        require(k not in indexed, f"Duplicate automatic key: {k}")
        indexed[k] = row
    return indexed


def compare_point(point, auto, size):
    result = {"comparison": None, "auto_minus_manual_xy": None,
              "automatic_acceptance_without_manual_identity_support": False}
    valid = False
    if auto is not None:
        xy = auto.get("candidate_xy")
        valid = (isinstance(xy, list) and len(xy) == 2
                 and all(type(x) is int for x in xy)
                 and 0 <= xy[0] < size[0] and 0 <= xy[1] < size[1])
    result["automatic_coordinate_valid_native_integer"] = valid
    result["automatic_record_status"] = "missing_auto_record" if auto is None else auto["status"]
    if point["status"] != "localized":
        result["comparison"] = {"ambiguous": "manual_identity_ambiguous",
                                "unavailable": "manual_feature_unavailable"}[point["status"]]
        result["automatic_acceptance_without_manual_identity_support"] = bool(
            auto is not None and auto["status"] == "candidate")
    elif not valid:
        result["comparison"] = "no_coordinate_comparison"
    else:
        delta = [auto["candidate_xy"][i] - point["xy"][i] for i in (0, 1)]
        result["auto_minus_manual_xy"] = delta
        inside = all(abs(delta[i]) <= point["envelope_halfwidth_xy"][i] for i in (0, 1))
        result["comparison"] = "inside_manual_envelope" if inside else "outside_manual_envelope"
    return result


def self_test():
    point = {"status": "localized", "xy": [10, 10], "envelope_halfwidth_xy": [3, 4]}
    auto = {"status": "candidate", "candidate_xy": [13, 6]}
    require(compare_point(point, auto, [30, 30])["comparison"] == "inside_manual_envelope", "Inclusive boundary")
    auto["candidate_xy"] = [14, 6]
    require(compare_point(point, auto, [30, 30])["comparison"] == "outside_manual_envelope", "Outside boundary")
    auto.update(status="rejected", candidate_xy=[10, 10])
    require(compare_point(point, auto, [30, 30])["comparison"] == "inside_manual_envelope", "Rejected finite winner retained")
    for invalid in [None, [float("nan"), 10], [True, 10], [10.0, 10], [-1, 10], [30, 10]]:
        auto["candidate_xy"] = invalid
        require(compare_point(point, auto, [30, 30])["comparison"] == "no_coordinate_comparison", "Invalid coordinate")
    require(compare_point(point, None, [30, 30])["automatic_record_status"] == "missing_auto_record", "Missing explicit")
    for status in ["ambiguous", "unavailable"]:
        p = {"status": status, "xy": None, "envelope_halfwidth_xy": None}
        r = compare_point(p, {"status": "candidate", "candidate_xy": [10, 10]}, [30, 30])
        require(r["auto_minus_manual_xy"] is None and r["automatic_acceptance_without_manual_identity_support"], "No guessed identity")
    row = {"camera": "camera2", "index": 1, "reference": "C2-R1", "half": 9}
    try:
        index_rows([row, row])
    except ValueError:
        pass
    else:
        raise ValueError("Duplicate not rejected")
    require(Fraction("665404/2997") == 665404 * Fraction("1/2997"), "Exact rational PTS")
    return "passed: inclusive/outside envelopes, rejected winner, malformed/no winner, missing record, ambiguous/unavailable, duplicate key, rational PTS"


def read_run(name):
    path = ROOT / name
    receipt = load(path / "receipt.json")
    require(receipt["status"] == "complete_diagnostic_not_camera_calibration", f"Incomplete run {name}")
    names = ["matches.json", "features.json", "PROTOCOL.md", "input-pins.json", "initial.json", "measure.py", "test_measure.py"]
    pins = {n: pin(path / n) for n in names}
    for n in names:
        require(pins[n] == receipt["products"][n], f"Receipt product mismatch {name}/{n}")
    rows = load(path / "matches.json")
    require(len(rows) == receipt["match_rows"], "Receipt match count")
    initial = load(path / "initial.json")
    for n in ["features.json", "PROTOCOL.md", "measure.py", "test_measure.py"]:
        require(pins[n] == initial["pins"][str(ROOT / n)], f"Snapshot lineage mismatch {name}/{n}")
    return {"name": name, "path": path, "receipt": receipt, "pins": pins,
            "receipt_pin": pin(path / "receipt.json"), "initial": initial,
            "input_pins": load(path / "input-pins.json"), "features": load(path / "features.json"),
            "rows": index_rows(rows)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    tests = self_test()
    if args.self_test and not args.output:
        print(tests)
        return
    require(args.output is not None, "Specify --output (exclusive creation)")
    before = frozen_checks()
    annotations = load(ROOT / "independent-annotations.json")
    runs = [read_run("run01"), read_run("run02")]
    records, image_checks, overlays = [], {}, []
    for camera, details in annotations["cameras"].items():
        features = {f["id"]: f for f in details["features"]}
        for run in runs:
            require(run["features"]["half_widths"] == [9, 13], "Template sizes changed")
            require({f["id"]: f["xy"] for f in run["features"][camera]} ==
                    {k: f["baseline_xy"] for k, f in features.items()}, "Baseline configuration changed")
        baseline = (ROOT / details["baseline_png"]).resolve()
        frame_images = [(details["baseline_frame"], baseline, details["baseline_png_sha256"])]
        for frame in details["annotations"]:
            frame_images.append((frame["frame"], baseline.with_name(f"f{frame['frame']:06d}.png"), frame["png_sha256"]))
            for point in frame["points"]:
                for template_size in annotations["template_sizes"]:
                    k = camera, frame["frame"], point["id"], template_size
                    auto = runs[0]["rows"].get(k)
                    repeat = runs[1]["rows"].get(k)
                    require(auto == repeat, f"Compared row differs between runs: {k}")
                    if auto is not None:
                        require(Fraction(auto["seconds_exact"]) == Fraction(frame["source_time_seconds_exact"]), f"PTS mismatch {k}")
                        require(int(auto["pts"]) * Fraction(auto["time_base"]) == Fraction(frame["source_time_seconds_exact"]), f"Raw PTS mismatch {k}")
                        require(auto["baseline_xy"] == features[point["id"]]["baseline_xy"], f"Baseline row mismatch {k}")
                        require(auto["status"] in ("candidate", "rejected"), f"Unknown auto status {k}")
                    record = {"camera": camera, "source_id_from_frozen_annotations": details["source_id"],
                              "frame": frame["frame"], "reference": point["id"], "template_size": template_size,
                              "source_time_seconds_exact": frame["source_time_seconds_exact"],
                              "png_sha256": frame["png_sha256"], "manual": point,
                              "baseline_feature": features[point["id"]], "automatic": auto,
                              "run02_compared_row_identical": True,
                              "post_output_annotation_identity_caution": point["id"] == "C2-R3"}
                    record.update(compare_point(point, auto, details["stored_size"]))
                    records.append(record)
        for index, path, expected_sha in frame_images:
            actual = pin(path)
            require(actual["sha256"] == expected_sha, f"Manual PNG hash mismatch {camera}/{index}")
            data = path.read_bytes()
            require(data[:8] == b"\x89PNG\r\n\x1a\n" and list(struct.unpack(">II", data[16:24])) == details["stored_size"], "PNG stored dimensions")
            for run in runs:
                require(run["input_pins"][str(path)] == actual, f"Run input pin mismatch {camera}/{index}")
            image_checks[str(path)] = actual
            for half in [9, 13]:
                name = f"overlay-{camera}-{index}-{half}.png"
                actual_overlay = pin(runs[0]["path"] / name)
                require(actual_overlay == runs[0]["receipt"]["products"][name], f"Overlay pin mismatch {name}")
                overlays.append({"path": f"run01/{name}", **actual_overlay,
                                 "visual_review": "post-output computational AI inspection completed; no frozen annotation edits"})
    require(len(records) == 120, "Expected 120 comparison rows")
    require(len({(r["camera"], r["frame"], r["reference"], r["template_size"]) for r in records}) == 120, "Expected keys unique")
    summaries = []
    for camera in annotations["cameras"]:
        for size in annotations["template_sizes"]:
            group = [r for r in records if r["camera"] == camera and r["template_size"] == size]
            summaries.append({"camera": camera, "template_size": size, "rows": len(group),
                              "manual_status": dict(Counter(r["manual"]["status"] for r in group)),
                              "automatic_status": dict(Counter(r["automatic_record_status"] for r in group)),
                              "comparison": dict(Counter(r["comparison"] for r in group)),
                              "comparison_by_automatic_status": dict(Counter(r["comparison"] + "/" + r["automatic_record_status"] for r in group)),
                              "automatic_acceptance_without_manual_identity_support": sum(r["automatic_acceptance_without_manual_identity_support"] for r in group),
                              "post_output_identity_caution_rows": sum(r["post_output_annotation_identity_caution"] for r in group)})
    after = frozen_checks()
    require(before == after, "Frozen files changed during comparison")
    output = {"schema_version": 1, "status": "completed_bounded_comparison_not_calibration",
              "plan_sha256": FROZEN["independent-comparison.md"], "frozen_before": before, "frozen_after": after,
              "comparison_script": pin(Path(__file__)), "python": sys.version, "self_tests": tests,
              "run_provenance": [{"path": str(r["path"]), "receipt": r["receipt_pin"], "consumed_products": r["pins"],
                                  "initial": r["initial"], "status": r["receipt"]["status"], "automatic_total_rows": len(r["rows"])} for r in runs],
              "source_id_limit": "Automatic rows name cameras; source IDs are inherited from frozen annotations, linked by exact native PNG hashes and exact PTS, not independently authenticated.",
              "image_checks": image_checks, "summaries": summaries, "records": records,
              "repeat_check": "All 120 compared run02 rows equal run01; no claim here to verify every other run product.",
              "post_output_review": {"overlay_count": len(overlays), "overlays": overlays,
                  "additional_review": ["native Camera 2 f6593 PNG", "independent-grids/camera2-baseline-grid.png"],
                  "annotation_error": "C2-R3 (288,400) is on a dark low-feature region rather than the described bright cap, which is visibly farther right/lower. Baseline description-coordinate misassociation is a reviewer error. Original annotations, status labels and all planned rows are preserved; the five R3 manual evaluation rows (ten size-specific comparisons) do not validate the claimed cap identity. No replacement point or corrected run is introduced.",
                  "disclosure": "Parent flagged the R3 hypothesis after viewing outputs; this reviewer confirmed against the native baseline and grid. This is post-output review, not blind discovery.",
                  "other_findings": "No other gross reference swaps identified in these sampled overlays. Late Camera 4 candidates are rejected and land on unrelated or insecurely identified regions after reframing. Right-edge C4-R3 text is clipped in some late overlays; raw JSON retains full IDs. Marker/label pixels obscure their immediate underlying image. Banner motion, overlap-point identity and different-depth references remain uncertain."},
              "limitations": "Computational AI subjective envelopes, not human ground truth or a pristine holdout. Numerical envelope agreement does not establish feature identity, stationarity, zero/subpixel camera motion, transfer to target, physical calibration, synchronization, acceleration or cause."}
    with args.output.open("x") as stream:
        json.dump(output, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "pin": pin(args.output), "summaries": summaries}, indent=2))


if __name__ == "__main__":
    main()
