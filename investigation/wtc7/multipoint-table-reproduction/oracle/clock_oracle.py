#!/usr/bin/env python3
"""Post-result, independently coded exact derivative-clock diagnostic.

The original nominal-grid fit/derivative outputs remain unchanged. This
module does not read or import the producer's clock diagnostic or results.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


TABLE_SHA256 = "fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8"
SOURCE_SHA256 = "cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394"
ADDENDUM_SHA256 = "198d31a14ca49368bfc00c64ed3d4827d8fea9d7045a4f2a090e75a5ec6a866f"
TRACKS = ("ne_corner", "ec_roofline", "wc_roofline", "nw_corner")
CANDIDATES = (
    ("nominal_30", F(30)),
    ("r_frame_rate_30000_1001", F(30000, 1001)),
    ("avg_frame_rate_2997_100", F(2997, 100)),
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def derivative_trial(previous_y, following_y, printed_v, span):
    if any(not isinstance(value, F) for value in (previous_y, following_y, printed_v, span)):
        raise ValueError("exact rational inputs required")
    if span <= 0:
        raise ValueError("positive time span required")
    derivative = (following_y-previous_y) / span
    residual = printed_v-derivative
    bound = F(1, 100)/span + F(1, 200)
    return {"calculated_velocity": derivative,
            "printed_minus_calculated_velocity": residual,
            "rounding_bound": bound, "rounding_compatible": abs(residual) <= bound}


def evaluate_candidates(rows):
    by_time = {row["time_s"]: row for row in rows}
    if len(by_time) != len(rows):
        raise ValueError("duplicate nominal time")
    supported, unsupported = [], []
    for track in TRACKS:
        for row in rows:
            if row[track+"_v"] is None:
                continue
            time = row["time_s"]
            if (time-F(1, 5) not in by_time or time+F(1, 5) not in by_time or
                    row[track+"_y"] is None):
                unsupported.append({"track": track, "source_row": row["source_row"], "time": time})
                continue
            previous, following = by_time[time-F(1, 5)], by_time[time+F(1, 5)]
            if previous[track+"_y"] is None or following[track+"_y"] is None:
                unsupported.append({"track": track, "source_row": row["source_row"], "time": time})
                continue
            supported.append({"track": track, "source_row": row["source_row"], "time": time,
                              "support_source_rows": [previous["source_row"], row["source_row"], following["source_row"]],
                              "previous_y": previous[track+"_y"], "following_y": following[track+"_y"],
                              "printed_v": row[track+"_v"]})
    output = []
    for label, frame_rate in CANDIDATES:
        span = F(12)/frame_rate
        trials = []
        for item in supported:
            trial = derivative_trial(item["previous_y"], item["following_y"], item["printed_v"], span)
            trials.append({**item, **trial})
        failures = [item for item in trials if not item["rounding_compatible"]]
        output.append({"candidate": label, "hypothesized_frame_rate": frame_rate,
                       "centered_span": span, "rounding_bound": F(1, 100)/span+F(1, 200),
                       "tested_count": len(trials), "failure_count": len(failures),
                       "rows": trials, "failures": failures,
                       "largest_absolute_residual": max((abs(item["printed_minus_calculated_velocity"]) for item in trials), default=None)})
    return {"candidate_results": output, "unsupported": unsupported,
            "total_row_candidate_count": sum(item["tested_count"] for item in output)}


def serialize(value):
    if isinstance(value, F):
        return {"exact": str(value), "display": float(value)}
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def historical_result():
    unit = Path(__file__).resolve().parent.parent
    table = unit / "transcription-independent" / "table47.json"
    addendum = unit / "CLOCK-ADDENDUM.md"
    if sha256(table) != TABLE_SHA256 or sha256(addendum) != ADDENDUM_SHA256:
        raise ValueError("frozen input/addendum hash mismatch")
    raw = json.loads(table.read_text())
    if raw["source_sha256"] != SOURCE_SHA256 or sha256(raw["source_path"]) != SOURCE_SHA256:
        raise ValueError("source mismatch")
    rows = []
    for expected_index, item in enumerate(raw["rows"], 1):
        if item["source_row"] != expected_index:
            raise ValueError("source row locator mismatch")
        time = F(item["time_s"])
        if time != F(-1)+F(expected_index-1, 5):
            raise ValueError("nominal printed grid mismatch")
        row = {"source_row": expected_index, "time_s": time}
        for track in TRACKS:
            for suffix in ("_y", "_v"):
                token = item[track+suffix]
                if token is not None and not isinstance(token, str):
                    raise ValueError("printed decimal string or null required")
                row[track+suffix] = None if token is None else F(token)
        rows.append(row)
    if len(rows) != 70:
        raise ValueError("expected all 70 source rows")
    result = evaluate_candidates(rows)
    if result["total_row_candidate_count"] != 483 or len(result["unsupported"]) != 1:
        raise ValueError("diagnostic membership differs from declared support")
    result.update({"schema": "independent-post-result-clock-diagnostic-v1",
                   "scope": "Three separately declared spans; no fitting or historical timebase identification.",
                   "python": sys.version, "table_sha256": TABLE_SHA256, "source_sha256": SOURCE_SHA256,
                   "addendum_sha256": ADDENDUM_SHA256, "code_sha256": sha256(__file__),
                   "tests_sha256": sha256(Path(__file__).with_name("clock_test_oracle.py"))})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    target = Path(args.output)
    if target.parent.resolve() != Path(__file__).resolve().parent or not target.name.startswith("clock-"):
        raise ValueError("new clock output must be under oracle/ with a clock- prefix")
    result = historical_result()
    with target.open("x") as handle:
        json.dump(serialize(result), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(target), "sha256": sha256(target),
                      "row_candidate_count": result["total_row_candidate_count"]}))
