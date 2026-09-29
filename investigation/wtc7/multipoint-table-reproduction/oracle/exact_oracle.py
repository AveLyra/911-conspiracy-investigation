#!/usr/bin/env python3
"""Independent, standard-library rational audit of the declared printed tables.

No producer code is imported. Historical execution requires an explicit
reconciliation receipt and produces a new, exclusive directory. Fractions are
the comparison authority; floating displays are conveniences only.
"""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import sys
from fractions import Fraction as F


SOURCE_SHA256 = "cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394"
INPUT_SHA256 = {
    47: "fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8",
    50: "9af054e9730915e35a429f2d846f3450120ea19b41a7c166b917b8f82e643c34",
}
POINTS = ("ne_corner", "ec_roofline", "wc_roofline", "nw_corner")
ONSET = dict(zip(POINTS, map(F, ("8.0", "8.2", "8.2", "8.2"))))
TARGET = dict(zip(POINTS, map(F, ("9.30", "9.79", "9.81", "9.92"))))
FIELDS47 = ("ref_building_x", "ref_building_y") + tuple(
    point + suffix for point in POINTS for suffix in ("_y", "_v")
)
FIELDS50 = (
    "reference_point_y", "nw_corner_y", "nw_corner_relative_y",
    "center_y", "center_relative_y", "center_adjusted_y",
    "sw_corner_y", "sw_corner_relative_y", "sw_corner_adjusted_y",
)
HALF_DISPLAY = F("0.005")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decimal_token(value, allow_null=False):
    if value is None and allow_null:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"-?\d+\.\d+", value):
        raise ValueError(f"not a finite printed decimal token: {value!r}")
    return F(value)


def validate_table(data, page):
    if page not in (47, 50):
        raise ValueError("unsupported source page")
    fields = FIELDS47 if page == 47 else FIELDS50
    if data.get("pdf_page_1based") != page:
        raise ValueError("source page mismatch")
    if data.get("source_sha256") != SOURCE_SHA256:
        raise ValueError("source hash metadata mismatch")
    if [h.get("key") for h in data.get("headers", [])] != list(fields):
        raise ValueError("column order/membership mismatch")
    rows = data.get("rows")
    if not isinstance(rows, list) or len(rows) != (70 if page == 47 else 25):
        raise ValueError("incorrect table row count")
    parsed = []
    previous = None
    for index, row in enumerate(rows, 1):
        if row.get("source_row") != index:
            raise ValueError("source rows are not consecutive")
        if set(row) != {"source_row", "time_s", "row_top_pdf_points", *fields}:
            raise ValueError("missing or unexpected row fields")
        time = decimal_token(row["time_s"])
        if previous is not None and time <= previous:
            raise ValueError("times must be strictly increasing")
        if page == 47 and time != F(-1) + F(index - 1, 5):
            raise ValueError("Camera 2 nominal grid mismatch")
        previous = time
        output = {"source_row": index, "time_s": time}
        for field in fields:
            token = row[field]
            if token is not None and not re.fullmatch(r"-?\d+\.\d{2}", token if isinstance(token, str) else ""):
                raise ValueError("position/velocity token must have two decimal places")
            output[field] = decimal_token(token, allow_null=(page == 47))
            if field.startswith("ref_") and output[field] is None:
                raise ValueError("missing Camera 2 reference input")
        parsed.append(output)
    if page == 50 and (parsed[0]["time_s"] != 8 or parsed[-1]["time_s"] != F("8.8")):
        raise ValueError("western time coverage mismatch")
    return parsed


def solve_square(matrix, right):
    """Gauss-Jordan elimination over rationals with explicit singular failure."""
    size = len(right)
    if size == 0 or len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("square matrix dimensions required")
    augmented = [[F(entry) for entry in row] + [F(target)]
                 for row, target in zip(matrix, right)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column] != 0), None)
        if pivot is None:
            raise ValueError("singular normal equations")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [a - multiplier * b for a, b in
                              zip(augmented[row], augmented[column])]
    return [row[-1] for row in augmented]


def exact_fit(times, values, degree):
    if degree not in (1, 2):
        raise ValueError("only declared linear and quadratic fits are allowed")
    if len(times) != len(values) or len(times) < degree + 1:
        raise ValueError("insufficient or unequal input lengths")
    if any(not isinstance(value, F) for value in [*times, *values]):
        raise ValueError("fit inputs must be exact Fraction values")
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("fit times must be strictly increasing")
    count = len(times)
    center = sum(times, F(0)) / count
    design = [[(time - center) ** power for power in range(degree + 1)]
              for time in times]
    gram = [[sum((row[i] * row[j] for row in design), F(0))
             for j in range(degree + 1)] for i in range(degree + 1)]
    right = [sum((row[i] * value for row, value in zip(design, values)), F(0))
             for i in range(degree + 1)]
    coefficients = solve_square(gram, right)
    predicted = [sum((a * b for a, b in zip(row, coefficients)), F(0))
                 for row in design]
    residuals = [value - prediction for value, prediction in zip(values, predicted)]
    # The degree-th coefficient is e_d' (X'X)^-1 X' y. The symmetric
    # system makes one solve against e_d sufficient for its input weights.
    functional = [F(0)] * degree + [F(-degree)]
    dual = solve_square(gram, functional)
    weights = [sum((a * b for a, b in zip(row, dual)), F(0)) for row in design]
    acceleration = -degree * coefficients[degree]
    if sum((weight * value for weight, value in zip(weights, values)), F(0)) != acceleration:
        raise ArithmeticError("coefficient and linear-functional routes disagree")
    uncentered = [sum((coefficients[j] * math.comb(j, k) * (-center) ** (j-k)
                      for j in range(k, degree + 1)), F(0))
                  for k in range(degree + 1)]
    sse = sum((value ** 2 for value in residuals), F(0))
    mean = sum(values, F(0)) / count
    sst = sum(((value - mean) ** 2 for value in values), F(0))
    half_width = HALF_DISPLAY * sum(map(abs, weights), F(0))
    return {
        "degree": degree, "n": count, "time_center": center,
        "coefficients_centered": coefficients,
        "coefficients_uncentered": uncentered,
        "predicted": predicted, "residuals_observed_minus_fit": residuals,
        "sse": sse, "mse": sse / count, "rmse_display": math.sqrt(float(sse / count)),
        "r_squared_descriptive": None if sst == 0 else 1 - sse / sst,
        "downward_acceleration": acceleration, "acceleration_input_weights": weights,
        "display_rounding_half_width": half_width,
        "display_rounding_interval": [acceleration-half_width, acceleration+half_width],
    }


def select_window(rows, point, start, end):
    if start >= end:
        raise ValueError("window start must precede end")
    selected = [row for row in rows if start <= row["time_s"] <= end]
    if not selected or selected[0]["time_s"] != start or selected[-1]["time_s"] != end:
        raise ValueError("window endpoint is absent")
    if any(row[point + suffix] is None for row in selected for suffix in ("_y", "_v")):
        raise ValueError("declared fit membership has a missing position/velocity")
    if any(b["time_s"] - a["time_s"] != F("0.2") for a, b in zip(selected, selected[1:])):
        raise ValueError("declared fit membership contains a gap")
    return selected


def window_definitions(rows):
    windows = []
    for point in POINTS:
        if point == "ne_corner":
            starts, ends = ("7.8", "8.0", "8.2"), ("8.8", "9.0", "9.2")
            primary = (F("8.0"), F("9.2"))
        else:
            starts, ends = ("8.0", "8.2", "8.4"), ("10.4", "10.6", "10.8", "11.0")
            primary = (F("8.2"), F("10.6"))
        for start, end in itertools.product(map(F, starts), map(F, ends)):
            windows.append((point, "fixed_grid", start, end, (start, end) == primary))
    if len(windows) != 45:
        raise ArithmeticError("incorrect fixed-window count")
    for point in POINTS:
        available = [row["time_s"] for row in rows
                     if row["time_s"] >= ONSET[point] and row[point + "_v"] is not None]
        if not available or available[0] != ONSET[point]:
            raise ValueError("post-onset velocity sequence does not begin at onset")
        windows.append((point, "whole_post_onset_contrast", ONSET[point], available[-1], False))
    return windows


def fit_windows(rows):
    outputs = []
    for index, (point, kind, start, end, primary) in enumerate(window_definitions(rows), 1):
        selected = select_window(rows, point, start, end)
        times = [row["time_s"] for row in selected]
        for suffix, degree, family in (("_v", 1, "velocity_linear"), ("_y", 2, "position_quadratic")):
            values = [row[point + suffix] for row in selected]
            output = exact_fit(times, values, degree)
            lo, hi = output["display_rounding_interval"]
            target_interval = [TARGET[point] - HALF_DISPLAY, TARGET[point] + HALF_DISPLAY]
            output.update({
                "window_index": index, "point": point, "kind": kind,
                "family": family, "primary": primary, "start": start, "end": end,
                "source_rows": [row["source_row"] for row in selected],
                "times": times, "values": values,
                "reported_target": TARGET[point], "reported_target_interval": target_interval,
                "difference_from_reported_target": output["downward_acceleration"] - TARGET[point],
                "display_intervals_overlap": max(lo, target_interval[0]) <= min(hi, target_interval[1]),
            })
            outputs.append(output)
    return outputs


def derivative_check(rows):
    result = []
    for point in POINTS:
        for index, row in enumerate(rows):
            velocity = row[point + "_v"]
            if velocity is None:
                continue
            entry = {"point": point, "source_row": row["source_row"], "time": row["time_s"],
                     "printed_velocity": velocity}
            if index == 0 or index == len(rows)-1:
                entry.update({"tested": False, "reason": "no printed bracketing row"})
            else:
                previous, following = rows[index-1], rows[index+1]
                if previous[point+"_y"] is None or row[point+"_y"] is None or following[point+"_y"] is None:
                    entry.update({"tested": False, "reason": "missing printed y triple"})
                elif row["time_s"]-previous["time_s"] != F("0.2") or following["time_s"]-row["time_s"] != F("0.2"):
                    raise ValueError("centered derivative requires adjacent nominal grid")
                else:
                    derivative = (following[point+"_y"]-previous[point+"_y"]) / F("0.4")
                    residual = velocity - derivative
                    entry.update({"tested": True, "centered_derivative": derivative,
                                  "residual_printed_minus_derivative": residual,
                                  "rounding_bound": F("0.030"),
                                  "within_rounding_bound": abs(residual) <= F("0.030"),
                                  "position_support_source_rows": [previous["source_row"], row["source_row"], following["source_row"]]})
            result.append(entry)
    return result


def western_check(rows):
    subtractions = []
    for row in rows:
        for point in ("nw_corner", "center", "sw_corner"):
            residual = row[point+"_relative_y"] - (row[point+"_y"]-row["reference_point_y"])
            subtractions.append({"point": point, "source_row": row["source_row"], "time": row["time_s"],
                                 "residual_relative_minus_raw_difference": residual,
                                 "rounding_bound": F("0.015"),
                                 "within_rounding_bound": abs(residual) <= F("0.015")})
    offsets = []
    for point in ("center", "sw_corner"):
        differences = [row[point+"_adjusted_y"]-row[point+"_relative_y"] for row in rows]
        low = max(difference-F("0.01") for difference in differences)
        high = min(difference+F("0.01") for difference in differences)
        offsets.append({"point": point, "per_row_differences": differences,
                        "per_row_intervals": [[value-F("0.01"), value+F("0.01")] for value in differences],
                        "intersection_lower": low, "intersection_upper": high,
                        "nonempty_intersection": low <= high})
    anchors = [row for row in rows if row["time_s"] == F("8.20")]
    if len(anchors) != 1:
        raise ValueError("unique 8.20-second western anchor required")
    anchor = anchors[0]
    columns = ("nw_corner_relative_y", "center_adjusted_y", "sw_corner_adjusted_y")
    displacements, pair_differences = [], []
    for row in rows:
        displacement = {column: row[column]-anchor[column] for column in columns}
        displacements.append({"source_row": row["source_row"], "time": row["time_s"], "displacements": displacement})
        for first, second in itertools.combinations(columns, 2):
            pair_differences.append({"source_row": row["source_row"], "time": row["time_s"],
                                     "first": first, "second": second,
                                     "first_minus_second": displacement[first]-displacement[second]})
    maximum = max(abs(item["first_minus_second"]) for item in pair_differences)
    return {"subtraction_checks": subtractions, "constant_offset_checks": offsets,
            "anchor_time": F("8.20"), "displacements": displacements,
            "pairwise_displacement_differences": pair_differences,
            "maximum_absolute_pairwise_difference": maximum,
            "maximum_locations": [item for item in pair_differences if abs(item["first_minus_second"]) == maximum]}


def convert(value):
    if isinstance(value, F):
        return {"exact": str(value), "display": float(value)}
    if isinstance(value, dict):
        return {key: convert(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [convert(item) for item in value]
    return value


def exclusive_json(path, payload):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(convert(payload), handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")


def run_historical(output, reconciliation):
    unit = Path(__file__).resolve().parent.parent
    reconciliation = Path(reconciliation).resolve(strict=True)
    if not reconciliation.is_file():
        raise ValueError("reconciliation receipt must be an existing file")
    paths = {page: unit / "transcription-independent" / f"table{page}.json" for page in (47, 50)}
    data = {}
    for page, path in paths.items():
        if digest(path) != INPUT_SHA256[page]:
            raise ValueError("frozen independent transcription hash changed")
        data[page] = json.loads(path.read_text(encoding="utf-8"))
    source = Path(data[47]["source_path"])
    if source != Path(data[50]["source_path"]) or digest(source) != SOURCE_SHA256:
        raise ValueError("preserved source bytes mismatch")
    rows47, rows50 = (validate_table(data[page], page) for page in (47, 50))
    result = {
        "schema": "independent-rational-printed-table-audit-v1",
        "method": "exact Fraction Gauss-Jordan normal equations with mean-centered times",
        "evidence_ceiling": "Arithmetic on printed derivative tables; not independent historical measurement validation.",
        "fit_windows": fit_windows(rows47), "centered_derivative_checks": derivative_check(rows47),
        "western_checks": western_check(rows50),
        "analytic_sensitivity": [{"relative_change": change, "spatial_only_acceleration_factor": 1+change,
                                  "clock_only_acceleration_factor": 1/(1+change)**2}
                                 for change in map(F, ("-0.05", "-0.01", "0.01", "0.05"))],
    }
    output = Path(output)
    if output.parent.resolve() != Path(__file__).resolve().parent:
        raise ValueError("oracle output must be a direct child of oracle/")
    output.mkdir(exist_ok=False)
    exclusive_json(output / "results.json", result)
    receipt = {"python": sys.version, "source_sha256": SOURCE_SHA256,
               "input_sha256": {str(page): digest(path) for page, path in paths.items()},
               "code_sha256": digest(__file__), "tests_sha256": digest(unit / "oracle" / "test_exact_oracle.py"),
               "protocol_sha256": digest(unit / "PROTOCOL.md"),
               "reconciliation_receipt": str(reconciliation), "reconciliation_sha256": digest(reconciliation),
               "results_sha256": digest(output / "results.json")}
    exclusive_json(output / "receipt.json", receipt)
    print(json.dumps({"output": str(output), "fit_count": len(result["fit_windows"]),
                      "results_sha256": receipt["results_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--reconciliation", required=True,
                        help="Frozen reconciliation receipt; use only after root confirms release")
    args = parser.parse_args()
    run_historical(args.output, args.reconciliation)
