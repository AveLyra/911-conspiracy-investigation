#!/usr/bin/env python3
"""Exact, exploratory feasibility of one constant image-y separation.

No source retrieval, floating-point arithmetic, coordinate mutation, or
interpolation. Constructed witnesses are mathematical, not historical data.
"""

import hashlib
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path


BASE = Path(__file__).resolve().parent
FRAMES = [258] + list(range(288, 349, 3))
PINS = {
    "root-observations.json": "20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a",
    "independent-observations.json": "529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f",
}
INPUTS = ["joint_feasibility.py", "JOINT-ENVELOPE-ADDENDUM.md", "PROTOCOL.md", *PINS]
LABEL = "mathematical_nonhistorical_witness_not_new_observations"


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def pins():
    return {name: pin(BASE / name) for name in INPUTS}


def interval(lo, hi):
    return [str(F(lo)), str(F(hi))]


def box(row, feature):
    feature = row[feature]
    lo, hi = F(feature["ymin"]), F(feature["ymax"])
    if lo > hi:
        raise ValueError("invalid_source_interval")
    return lo, hi


def solve(observers, selected):
    """Join exact source boxes, reject conflicting observers, then intersect c."""
    maps = {name: {r["frame"]: r for r in rows} for name, rows in observers.items()}
    result = {
        "observers": list(observers), "selected_frames": selected,
        "included_frames": [], "omitted_frames": [], "joined_inputs": [],
        "observer_intersection_conflicts": [], "constant_interval": None,
        "constant": None, "witness_label": LABEL, "witness": [],
    }
    for frame in selected:
        reasons = [
            {"observer": name, "feature": feature, "status": rows[frame][feature]["status"]}
            for name, rows in maps.items() for feature in ("A", "B")
            if rows[frame][feature]["status"] != "localized"
        ]
        if reasons:
            result["omitted_frames"].append({"frame": frame, "reasons": reasons})
            continue
        joined = {"frame": frame, "source_boxes": {}}
        for name, rows in maps.items():
            joined["source_boxes"][name] = {s: interval(*box(rows[frame], s)) for s in ("A", "B")}
        for feature in ("A", "B"):
            boxes = [box(rows[frame], feature) for rows in maps.values()]
            lo, hi = max(v[0] for v in boxes), min(v[1] for v in boxes)
            joined[feature] = interval(lo, hi)
            if lo > hi:
                result["observer_intersection_conflicts"].append(
                    {"frame": frame, "feature": feature, "empty_intersection": interval(lo, hi)})
        a, b = [F(v) for v in joined["A"]], [F(v) for v in joined["B"]]
        joined["constant_interval"] = interval(a[0] - b[1], a[1] - b[0]) if a[0] <= a[1] and b[0] <= b[1] else None
        result["joined_inputs"].append(joined)
        result["included_frames"].append(frame)
    if result["observer_intersection_conflicts"]:
        result["status"] = "rejected_empty_observer_intersection"
        return result
    if not result["joined_inputs"]:
        result["status"] = "insufficient_no_localized_pairs"
        return result
    lower = max(F(row["constant_interval"][0]) for row in result["joined_inputs"])
    upper = min(F(row["constant_interval"][1]) for row in result["joined_inputs"])
    result["constant_interval"] = interval(lower, upper)
    if lower > upper:
        result["status"] = "infeasible_constant_separation_within_supplied_boxes"
        return result
    c = (lower + upper) / 2
    result["status"] = "feasible_on_included_samples_only"
    result["constant"] = str(c)
    for row in result["joined_inputs"]:
        a, b = [F(v) for v in row["A"]], [F(v) for v in row["B"]]
        lo, hi = max(a[0], c + b[0]), min(a[1], c + b[1])
        if lo > hi:
            raise AssertionError("empty_witness_A_intersection")
        ay = (lo + hi) / 2
        by = ay - c
        for boxes in row["source_boxes"].values():
            if not (F(boxes["A"][0]) <= ay <= F(boxes["A"][1]) and F(boxes["B"][0]) <= by <= F(boxes["B"][1])):
                raise AssertionError("witness_outside_original_box")
        result["witness"].append({"frame": row["frame"], "A_y": str(ay), "B_y": str(by), "A_minus_B": str(ay - by), "A_witness_interval": interval(lo, hi)})
    return result


def fixture(frame, a, b):
    return {"frame": frame, **{s: {"status": "localized", "y": str((F(v[0]) + F(v[1])) / 2), "ymin": str(F(v[0])), "ymax": str(F(v[1]))} for s, v in (("A", a), ("B", b))}}


def controls():
    groups = []
    base = [fixture(1, (10, 12), (3, 5)), fixture(2, (15, 17), (8, 10))]
    cases = [
        ("feasible", {"one": base}, "feasible_on_included_samples_only", ["5", "9"]),
        ("infeasible", {"one": [base[0], fixture(2, (20, 21), (1, 2))]}, "infeasible_constant_separation_within_supplied_boxes", ["18", "9"]),
        ("touching_bound", {"one": [fixture(1, (5, 7), (1, 2)), fixture(2, (8, 9), (1, 2))]}, "feasible_on_included_samples_only", ["6", "6"]),
    ]
    for name, inputs, expected_status, expected_interval in cases:
        result = solve(inputs, [1, 2])
        passed = result["status"] == expected_status and result["constant_interval"] == expected_interval
        groups.append({"name": name, "inputs": inputs, "selected_frames": [1, 2], "expected": {"status": expected_status, "constant_interval": expected_interval}, "result": result, "pass": passed})
    shifted = [fixture(1, (13, 15), (6, 8)), fixture(2, (8, 10), (1, 3))]
    original, translated = solve({"one": base}, [1, 2]), solve({"one": shifted}, [1, 2])
    shifts = [F(3), F(-7)]
    passed = original["constant_interval"] == translated["constant_interval"] and original["constant"] == translated["constant"]
    passed = passed and all(F(v[f]) - F(u[f]) == d for u, v, d in zip(original["witness"], translated["witness"], shifts) for f in ("A_y", "B_y"))
    groups.append({"name": "common_translation", "inputs": {"original": {"one": base}, "translated": {"one": shifted}}, "selected_frames": [1, 2], "translations": [str(x) for x in shifts], "expected": "same_constant_interval_and_constant; each_witness_coordinate_shifts_by_declared_translation", "results": {"original": original, "translated": translated}, "pass": passed})
    empty_cases = []
    for feature, other in [("A", fixture(1, (12, 13), (3, 5))), ("B", fixture(1, (10, 11), (6, 7)))]:
        inputs = {"one": [fixture(1, (10, 11), (3, 5))], "two": [other]}
        result = solve(inputs, [1])
        passed = result["status"] == "rejected_empty_observer_intersection" and result["constant_interval"] is None and result["witness"] == [] and [x["feature"] for x in result["observer_intersection_conflicts"]] == [feature]
        empty_cases.append({"inputs": inputs, "selected_frames": [1], "expected_empty_feature": feature, "result": result, "pass": passed})
    groups.append({"name": "empty_observer_intersection", "cases": empty_cases, "pass": all(x["pass"] for x in empty_cases)})
    return {"label": "fully_retained_synthetic_interval_fixtures_not_historical_inputs", "groups": groups, "pass": all(g["pass"] for g in groups)}


def read_observer(name):
    raw = json.loads((BASE / (name + "-observations.json")).read_text())
    if [r["frame"] for r in raw["rows"]] != FRAMES:
        raise ValueError("frozen_frame_coverage")
    rows = []
    for row in raw["rows"]:
        normalized = {"frame": row["frame"]}
        for feature in ("A", "B"):
            source = row[feature]
            if source["status"] == "localized":
                if any(type(source[k]) is not int for k in ("y", "ymin", "ymax")) or not source["ymin"] <= source["y"] <= source["ymax"]:
                    raise ValueError("invalid_frozen_localized_y")
            elif source["status"] != "unlocalizable" or any(source[k] is not None for k in ("y", "ymin", "ymax")):
                raise ValueError("invalid_frozen_missing_y")
            normalized[feature] = {k: str(F(v)) if type(v) is int else v for k, v in source.items()}
        rows.append(normalized)
    return rows


def save(out, name, value):
    with (out / name).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, ensure_ascii=False)
        stream.write("\n")


def main():
    out = BASE / "joint01"
    try:
        out.mkdir()
    except FileExistsError:
        print("refused_existing_output")
        return 2
    before = pins()
    stage = "controls"
    try:
        control_result = controls()
        save(out, "controls.json", control_result)
        if not control_result["pass"]:
            raise AssertionError("control_failure")
        stage = "frozen_input_validation"
        if any(before[n]["sha256"] != expected for n, expected in PINS.items()):
            raise ValueError("frozen_input_pin_mismatch")
        observers = {name: read_observer(name) for name in ("root", "independent")}
        stage = "historical_envelope_feasibility"
        scenarios = []
        for selection in ("root", "independent", "combined"):
            selected_observers = observers if selection == "combined" else {selection: observers[selection]}
            for coverage, frames in (("selected22", FRAMES), ("late21", FRAMES[1:])):
                result = solve(selected_observers, frames)
                scenarios.append({"name": selection + "_" + coverage, **result})
        result = {"label": "exact_interval_countermodel_feasibility_not_historical_reconstruction", "arithmetic": "fractions.Fraction; all coordinate quantities stored as exact rational strings", "original_observers": observers, "scenarios": scenarios, "limitations": "conditional subjective y envelopes; omitted frames impose no measured constraint and receive no witness; B fixed-column silhouette; no probability, physical rigidity, calibration, force or cause inference"}
        save(out, "result.json", result)
        after = pins()
        if before != after:
            raise ValueError("inputs_changed_during_execution")
        receipt = {"status": "pass_exact_conditional_image_envelope_diagnostic", "python": platform.python_version(), "command": "PYTHONDONTWRITEBYTECODE=1 python3 research/sherlock-wtc7-investigation/camera3-late-reannotation/joint_feasibility.py", "inputs_before": before, "inputs_after": after, "control_groups": len(control_result["groups"]), "control_pass": control_result["pass"], "scenarios": len(scenarios), "products": {n: pin(out / n) for n in ("controls.json", "result.json")}, "independent_reproduction": "pending; producer witness membership checks are not an independent solver"}
        save(out, "receipt.json", receipt)
        print(json.dumps({"status": receipt["status"], "control_groups": len(control_result["groups"]), "scenarios": [{"name": s["name"], "status": s["status"], "constant_interval": s["constant_interval"], "constant": s["constant"], "included": len(s["included_frames"]), "omitted": [r["frame"] for r in s["omitted_frames"]]} for s in scenarios]}))
        return 0
    except (ValueError, AssertionError, KeyError, TypeError, OSError) as exc:
        receipt = {"status": "failed", "stage": stage, "exception_type": type(exc).__name__, "inputs_before": before, "products": {p.name: pin(p) for p in out.iterdir() if p.is_file()}, "python": platform.python_version()}
        save(out, "receipt.json", receipt)
        print(json.dumps({"status": "failed", "stage": stage, "exception_type": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
