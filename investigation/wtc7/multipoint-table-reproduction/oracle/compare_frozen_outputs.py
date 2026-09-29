#!/usr/bin/env python3
"""Compare two already-frozen independent outputs, without importing producers."""

import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path


ORACLE_HASH = "a703e5a5c2ffb5b572b8bb3339a02194b69f7c1da53a383b7be5a8fa9db3c091"
PRODUCER_HASH = "c78146f9bb596a5c0c8241ae918d43f700c35596131e62af53912f75fd5a5dfd"
TRACK = {"ne_corner": "ne", "ec_roofline": "ec", "wc_roofline": "wc", "nw_corner": "nw",
         "center": "center", "sw_corner": "sw"}
COLUMNS = {"nw_corner_relative_y": "nw", "center_adjusted_y": "center", "sw_corner_adjusted_y": "sw"}
TOLERANCE = 1e-8


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact(value):
    return F(value["exact"]) if isinstance(value, dict) else F(str(value))


def compare(producer, oracle):
    maxima, count = {}, {"numeric": 0, "exact": 0}

    def same(actual, expected, label):
        count["exact"] += 1
        if actual != expected:
            raise AssertionError(f"{label}: unequal {actual!r} versus {expected!r}")

    def close(actual, expected, label):
        if isinstance(actual, list):
            same(len(actual), len(expected), label+" length")
            for a, b in zip(actual, expected):
                close(a, b, label)
            return
        value = float(exact(expected)) if isinstance(expected, dict) else float(expected)
        if not math.isfinite(actual) or not math.isfinite(value):
            raise AssertionError(label+": nonfinite comparison")
        delta = abs(actual-value)
        maxima[label] = max(maxima.get(label, 0.0), delta)
        count["numeric"] += 1
        if delta > TOLERANCE:
            raise AssertionError(f"{label}: delta {delta} exceeds {TOLERANCE}")

    def producer_key(item):
        return item["track"], item["category"], item["family"], F(item["start_s"]), F(item["end_s"])

    def oracle_key(item):
        return (TRACK[item["point"]], "grid" if item["kind"] == "fixed_grid" else "extended",
                "velocity" if item["family"] == "velocity_linear" else "position",
                exact(item["start"]), exact(item["end"]))

    pfit = {producer_key(item): item for item in producer["fits"]}
    ofit = {oracle_key(item): item for item in oracle["fit_windows"]}
    same(len(producer["fits"]), 98, "producer fit count")
    same(len(oracle["fit_windows"]), 98, "oracle fit count")
    same(len(pfit), 98, "unique producer fit keys")
    same(len(ofit), 98, "unique oracle fit keys")
    same(set(pfit), set(ofit), "fit key membership")
    for key in pfit:
        p, o = pfit[key], ofit[key]
        for field in ("n", "source_rows", "primary", "display_intervals_overlap"):
            same(p[field], o[field], "fit "+field)
        same([F(str(value)) for value in p["times_s"]], [exact(value) for value in o["times"]], "fit times")
        same([F(str(value)) for value in p["values"]], [exact(value) for value in o["values"]], "fit input values")
        for pfield, ofield in (
            ("center_s", "time_center"), ("coefficients_centered", "coefficients_centered"),
            ("residuals", "residuals_observed_minus_fit"),
            ("downward_acceleration", "downward_acceleration"),
            ("acceleration_input_weights", "acceleration_input_weights"),
            ("display_rounding_half_width", "display_rounding_half_width"),
            ("display_rounding_interval", "display_rounding_interval"),
            ("reported_target", "reported_target"), ("target_difference", "difference_from_reported_target"),
            ("rmse", "rmse_display"),
        ):
            close(p[pfield], o[ofield], pfield)
        close([value-residual for value, residual in zip(p["values"], p["residuals"])],
              o["predicted"], "predictions_recovered_from_residuals")

    pderivative = {(item["track"], item["row"]): item for item in producer["centered_differences"]["rows"]}
    oderivative = {(TRACK[item["point"]], item["source_row"]): item
                   for item in oracle["centered_derivative_checks"] if item["tested"]}
    same(len(pderivative), 161, "producer derivative count")
    same(set(pderivative), set(oderivative), "derivative membership")
    for key in pderivative:
        p, o = pderivative[key], oderivative[key]
        same(F(p["time_s"]), exact(o["time"]), "derivative time")
        same(F(p["residual_fraction"]), exact(o["residual_printed_minus_derivative"]), "derivative exact residual")
        same(p["rounding_compatible"], o["within_rounding_bound"], "derivative classification")
        close(p["calculated_v"], o["centered_derivative"], "centered derivative")
        close(p["residual"], o["residual_printed_minus_derivative"], "derivative residual display")
    unsupported_p = {(item["track"], item["row"], F(item["time_s"]))
                     for item in producer["centered_differences"]["unsupported"]}
    unsupported_o = {(TRACK[item["point"]], item["source_row"], exact(item["time"]))
                     for item in oracle["centered_derivative_checks"] if not item["tested"]}
    same(unsupported_p, unsupported_o, "unsupported derivative membership")

    pwest, owest = producer["western"], oracle["western_checks"]
    psub = {(item["track"], item["row"]): item for item in pwest["subtractions"]}
    osub = {(TRACK[item["point"]], item["source_row"]): item for item in owest["subtraction_checks"]}
    same(len(psub), 75, "western subtraction count")
    same(set(psub), set(osub), "western subtraction membership")
    for key in psub:
        p, o = psub[key], osub[key]
        same(F(p["time_s"]), exact(o["time"]), "western subtraction time")
        same(F(p["residual_fraction"]), exact(o["residual_relative_minus_raw_difference"]), "western exact subtraction")
        same(p["rounding_compatible"], o["within_rounding_bound"], "western subtraction classification")
        close(p["residual"], o["residual_relative_minus_raw_difference"], "western subtraction display")
    for item in owest["constant_offset_checks"]:
        p = pwest["offsets"][TRACK[item["point"]]]
        same([F(value) for value in p["differences_fraction"]],
             [exact(value) for value in item["per_row_differences"]], "offset per-row differences")
        same([F(value) for value in p["intersection_fraction"]],
             [exact(item["intersection_lower"]), exact(item["intersection_upper"])], "offset exact intersection")
        same(p["compatible_common_offset"], item["nonempty_intersection"], "offset classification")
    pdisp = {F(item["time_s"]): item for item in pwest["displacements_from_8_20"]}
    same(len(pdisp), 25, "western displacement row count")
    for item in owest["displacements"]:
        p = pdisp[exact(item["time"])]
        for column, value in item["displacements"].items():
            same(F(str(p["displacements"][COLUMNS[column]])), exact(value), "western exact displacement")
    same(len(owest["pairwise_displacement_differences"]), 75, "western pairwise comparison count")
    for item in owest["pairwise_displacement_differences"]:
        pair = COLUMNS[item["first"]]+"-"+COLUMNS[item["second"]]
        same(F(pdisp[exact(item["time"])]["pair_differences_fraction"][pair]),
             exact(item["first_minus_second"]), "western exact pairwise difference")
    maximum = max(abs(F(value)) for item in pdisp.values() for value in item["pair_differences_fraction"].values())
    same(maximum, exact(owest["maximum_absolute_pairwise_difference"]), "western maximum difference")
    for p, o in zip(producer["scale_clock_factors"], oracle["analytic_sensitivity"]):
        same(F(p["change"]), exact(o["relative_change"]), "analytic scenario membership")
        close(p["clock_only_acceleration_factor"], o["clock_only_acceleration_factor"], "clock factors")
        close(p["scale_only_acceleration_factor"], o["spatial_only_acceleration_factor"], "scale factors")
    return {"status": "pass", "tolerance": TOLERANCE, "comparison_counts": count,
            "maximum_absolute_numeric_differences": maxima, "fit_count": 98,
            "derivative_count": 161, "western_subtraction_count": 75,
            "western_pairwise_count": 75}


def adversarial_comparator_checks(producer, oracle):
    checks = []
    for name in ("coefficient", "residual", "weight", "membership", "overlap_flag", "derivative_fraction", "west_fraction"):
        bad = deepcopy(producer)
        if name == "coefficient":
            bad["fits"][0]["coefficients_centered"][0] += 1e-4
        elif name == "residual":
            bad["fits"][0]["residuals"][0] += 1e-4
        elif name == "weight":
            bad["fits"][0]["acceleration_input_weights"][0] += 1e-4
        elif name == "membership":
            bad["fits"][0]["source_rows"][0] += 1
        elif name == "overlap_flag":
            bad["fits"][0]["display_intervals_overlap"] = not bad["fits"][0]["display_intervals_overlap"]
        elif name == "derivative_fraction":
            bad["centered_differences"]["rows"][0]["residual_fraction"] = "1/1000000"
        else:
            bad["western"]["subtractions"][0]["residual_fraction"] = "9/100"
        try:
            compare(bad, oracle)
        except AssertionError as error:
            checks.append({"corruption": name, "correctly_rejected": True, "reason": str(error)})
        else:
            raise AssertionError("comparator failed to reject "+name)
    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--oracle", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if digest(args.producer) != PRODUCER_HASH or digest(args.oracle) != ORACLE_HASH:
        raise ValueError("frozen result hash mismatch")
    producer = json.loads(Path(args.producer).read_text())
    oracle = json.loads(Path(args.oracle).read_text())
    try:
        result = compare(producer, oracle)
        result["negative_comparator_checks"] = adversarial_comparator_checks(producer, oracle)
    except AssertionError as error:
        result = {"status": "fail", "error": str(error)}
    result.update({"producer_sha256": PRODUCER_HASH, "oracle_sha256": ORACLE_HASH,
                   "comparison_code_sha256": digest(__file__)})
    with Path(args.output).open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "pass" else 1)
