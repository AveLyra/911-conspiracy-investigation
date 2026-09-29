#!/usr/bin/env python3
"""Exact comparison of frozen clock outputs and the unchanged original baseline."""

import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


EXPECTED = {
    "producer": "a625dde21e5767adc60147421afb94084d96842fc9ec7e733706555e80297c87",
    "oracle": "2079a1e96f593b2e3520163df687e59e9f6e1c5e4af8edf2f9b672bc869f21ec",
    "baseline": "a703e5a5c2ffb5b572b8bb3339a02194b69f7c1da53a383b7be5a8fa9db3c091",
}
TRACK = {"ne_corner": "ne", "ec_roofline": "ec", "wc_roofline": "wc", "nw_corner": "nw"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact(value):
    return F(value["exact"])


def compare(producer, oracle, baseline):
    count = 0

    def same(actual, expected, label):
        nonlocal count
        count += 1
        if actual != expected:
            raise AssertionError(f"{label}: {actual!r} != {expected!r}")

    same(len(producer["rows"]), 483, "producer total count")
    same(oracle["total_row_candidate_count"], 483, "oracle total count")
    pmap = {(F(row["rate_hypothesis"]), row["track"], row["row"]): row for row in producer["rows"]}
    omap = {}
    summary = {}
    for candidate in oracle["candidate_results"]:
        rate = exact(candidate["hypothesized_frame_rate"])
        for row in candidate["rows"]:
            omap[rate, TRACK[row["track"]], row["source_row"]] = (row, candidate)
        psummary = producer["summary"][str(rate)]
        same(psummary["checked"], candidate["tested_count"], "candidate test count")
        same(psummary["failures"], candidate["failure_count"], "candidate failure count")
        maximum = max(abs(F(row["residual_fraction"])) for key, row in pmap.items() if key[0] == rate)
        same(maximum, exact(candidate["largest_absolute_residual"]), "maximum absolute residual")
        summary[str(rate)] = {"rows": candidate["tested_count"], "failures": candidate["failure_count"],
                              "bound": candidate["rounding_bound"]["exact"], "maximum_absolute_residual": str(maximum)}
    same(len(pmap), 483, "unique producer rows")
    same(len(omap), 483, "unique oracle rows")
    same(set(pmap), set(omap), "all row-candidate memberships")
    for key, p in pmap.items():
        o, candidate = omap[key]
        same(F(p["time_s"]), exact(o["time"]), "time")
        same(F(p["centered_span_fraction"]), exact(candidate["centered_span"]), "span")
        same(F(p["calculated_fraction"]), exact(o["calculated_velocity"]), "calculated velocity")
        same(F(p["residual_fraction"]), exact(o["printed_minus_calculated_velocity"]), "residual")
        same(F(p["bound_fraction"]), exact(o["rounding_bound"]), "rounding bound")
        same(p["compatible"], o["rounding_compatible"], "classification")
    p_unsupported = {(row["track"], row["row"], F(row["time_s"])) for row in producer["unsupported"]}
    o_unsupported = {(TRACK[row["track"]], row["source_row"], exact(row["time"])) for row in oracle["unsupported"]}
    same(p_unsupported, o_unsupported, "unsupported membership")
    baseline_rows = [row for row in baseline["centered_derivative_checks"] if row["tested"]]
    same(len(baseline_rows), 161, "baseline row count")
    for row in baseline_rows:
        clock_row, candidate = omap[F(30), TRACK[row["point"]], row["source_row"]]
        same(exact(row["time"]), exact(clock_row["time"]), "baseline time")
        same(exact(row["centered_derivative"]), exact(clock_row["calculated_velocity"]), "baseline velocity")
        same(exact(row["residual_printed_minus_derivative"]), exact(clock_row["printed_minus_calculated_velocity"]), "baseline residual")
        same(exact(row["rounding_bound"]), exact(clock_row["rounding_bound"]), "baseline bound")
        same(row["within_rounding_bound"], clock_row["rounding_compatible"], "baseline classification")
    return {"status": "pass", "exact_comparison_count": count, "row_candidate_count": 483,
            "original_baseline_rows_matched": 161, "summary": summary}


def negative_checks(producer, oracle, baseline):
    output = []
    for field in ("calculated_fraction", "residual_fraction", "bound_fraction", "centered_span_fraction", "row", "compatible"):
        corrupted = deepcopy(producer)
        if field == "row":
            corrupted["rows"][0][field] += 1
        elif field == "compatible":
            corrupted["rows"][0][field] = not corrupted["rows"][0][field]
        else:
            corrupted["rows"][0][field] = str(F(corrupted["rows"][0][field])+F(1, 1000000))
        try:
            compare(corrupted, oracle, baseline)
        except AssertionError as error:
            output.append({"field_corrupted": field, "rejected": True, "reason": str(error)})
        else:
            raise AssertionError("comparison failed to reject corrupted "+field)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (*EXPECTED, "output"):
        parser.add_argument("--"+name, required=True)
    args = parser.parse_args()
    loaded = {}
    for name, expected_hash in EXPECTED.items():
        path = getattr(args, name)
        if sha256(path) != expected_hash:
            raise ValueError(name+" frozen hash mismatch")
        loaded[name] = json.loads(Path(path).read_text())
    try:
        output = compare(**loaded)
        output["negative_checks"] = negative_checks(**loaded)
    except AssertionError as error:
        output = {"status": "fail", "reason": str(error)}
    output.update({"input_sha256": EXPECTED, "comparison_code_sha256": sha256(__file__)})
    with Path(args.output).open("x") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(output, indent=2, sort_keys=True))
    raise SystemExit(0 if output["status"] == "pass" else 1)
