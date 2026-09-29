#!/usr/bin/env python3
"""Independent Camera 3 dense-annotation arithmetic audit.

Implemented from PROTOCOL.md, frozen annotations and output schema;
does not import or execute analyze.py. Exact Fraction equal-grid symmetry
formulae replace NumPy. Decimal inputs are exact decimals. Tolerances 1e-8
absolute, SSE 1e-7, are arithmetic tolerances, not image accuracy bounds.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import sys

BASE = Path(__file__).resolve().parent
PINS = {
    "root": "20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a",
    "independent": "529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f",
    "root_note": "42a5f3f4ff373c9b10c1d47f81db2fffbf28831b9e97ea326a062fa44491e027",
    "independent_note": "d8ca1032081ea033db9f54e66cd9521e65373a88d4ce2e88e24f5ad52815ef72",
    "points": "f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3",
    "protocol": "7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f",
    "views": "8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161",
}
INPUT_PATHS = {
    "root": BASE / "root-observations.json",
    "independent": BASE / "independent-observations.json",
    "root_note": BASE / "root-observations.md",
    "independent_note": BASE / "independent-observations.md",
    "points": BASE.parent / "camera3-conditional-trajectories/extraction01/points.json",
    "protocol": BASE / "PROTOCOL.md",
    "views": BASE / "views01/receipt.json",
    "code": BASE / "analyze.py",
}
LATE = list(range(288, 349, 3))
SELECTED = [258] + LATE
TOLERANCE = 1e-8
SSE_TOLERANCE = 1e-7


def rational(value):
    if value is None or isinstance(value, bool):
        raise ValueError("nonnumeric_or_missing")
    if isinstance(value, Q):
        return value
    return Q(str(value))


def measure(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def parse(path):
    return json.loads(path.read_text())


def fit_exact(times, values, intervals=None):
    """Equal-grid fit through complete data only; no gap filling."""
    if len(times) != len(values) or len(times) < 3:
        raise ValueError("shape")
    t = [rational(v) for v in times]
    y = [rational(v) for v in values]
    dt = t[1] - t[0]
    if dt <= 0 or any(t[i] - t[i - 1] != dt for i in range(1, len(t))):
        raise ValueError("clock_order_or_unequal_spacing")
    n = len(t)
    center = (t[0] + t[-1]) / 2
    h = (t[-1] - t[0]) / 2
    u = [(v - center) / h for v in t]
    s2, s4 = sum(v * v for v in u), sum(v**4 for v in u)
    # Odd powers cancel, so the odd column decouples. Solve the even
    # 2x2 normal equations exactly; no floating least-squares routine.
    assert sum(u) == 0 and sum(v**3 for v in u) == 0
    sy = sum(y)
    suy = sum(a * b for a, b in zip(u, y))
    su2y = sum(a * a * b for a, b in zip(u, y))
    determinant = n * s4 - s2 * s2
    b1 = suy / s2
    b2 = (n * su2y - s2 * sy) / determinant
    coefficients = {"1": [sy / n, b1], "2": [(sy - s2 * b2) / n, b1, b2]}
    out = {"time_center": center, "halfspan": h, "y": y, "fits": {}}
    for degree, coeff in coefficients.items():
        residuals = [v - sum(b * z**k for k, b in enumerate(coeff)) for v, z in zip(y, u)]
        assert all(sum(r * z**k for r, z in zip(residuals, u)) == 0 for k in range(len(coeff)))
        sse = sum(r * r for r in residuals)
        if degree == "1":
            eigen = [float(n), float(s2)]
        else:
            disc = math.sqrt(float((n - s4)**2 + 4 * s2 * s2))
            eigen = [float(s2), (float(n + s4) - disc) / 2, (float(n + s4) + disc) / 2]
        out["fits"][degree] = {
            "coefficients": coeff, "residuals": residuals, "sse": sse,
            "rmse": math.sqrt(float(sse / n)),
            "condition": math.sqrt(max(eigen) / min(eigen)),
        }
    weights = [2 * (n * z * z - s2) / (h * h * determinant) for z in u]
    acceleration = 2 * b2 / (h * h)
    assert acceleration == sum(w * v for w, v in zip(weights, y))
    assert sum(weights) == 0
    assert sum(w * v for w, v in zip(weights, t)) == 0
    assert sum(w * v * v for w, v in zip(weights, t)) == 2
    out.update(weights=weights, sum_abs_weights=sum(abs(w) for w in weights), acceleration_px_s2=acceleration)
    if intervals is None:
        out.update(input_intervals=None, acceleration_interval_px_s2=None)
    else:
        if len(intervals) != n:
            raise ValueError("interval_shape")
        iv = [[rational(a), rational(b)] for a, b in intervals]
        if any(a > b or not a <= v <= b for (a, b), v in zip(iv, y)):
            raise ValueError("interval_order_or_center")
        # A linear map over a Cartesian product of closed intervals reaches
        # each extremum at the sign-selected endpoint at every coordinate.
        low_vertex = [a if w >= 0 else b for w, (a, b) in zip(weights, iv)]
        high_vertex = [b if w >= 0 else a for w, (a, b) in zip(weights, iv)]
        bounds = [sum(w * v for w, v in zip(weights, vertex)) for vertex in (low_vertex, high_vertex)]
        assert bounds[0] <= acceleration <= bounds[1]
        out.update(input_intervals=iv, acceleration_interval_px_s2=bounds)
    return out


class Audit:
    def __init__(self):
        self.counts = Counter()
        self.max_errors = defaultdict(float)
        self.failures = []

    def check(self, condition, label):
        self.counts["logical_checks"] += 1
        if not condition:
            self.failures.append(label)

    def compare(self, actual, expected, label, category="other"):
        if isinstance(expected, dict):
            self.check(isinstance(actual, dict), label + ":object")
            if not isinstance(actual, dict):
                return
            self.check(set(actual) == set(expected), label + ":keys")
            for key, value in expected.items():
                if key in actual:
                    self.compare(actual[key], value, label + "/" + key, key)
        elif isinstance(expected, (list, tuple)):
            self.check(isinstance(actual, list) and len(actual) == len(expected), label + ":length")
            if isinstance(actual, list):
                for i, (a, e) in enumerate(zip(actual, expected)):
                    self.compare(a, e, label + "/" + str(i), category)
        elif expected is None or isinstance(expected, (str, bool)):
            self.check(actual == expected and type(actual) is type(expected), label + ":exact")
        elif isinstance(expected, (int, float, Q)):
            self.counts["numeric_checks"] += 1
            if isinstance(actual, bool) or not isinstance(actual, (float, int)) or not math.isfinite(actual):
                self.failures.append(label + ":not_finite_number")
                return
            error = abs(float(rational(actual) - rational(expected)))
            self.max_errors[category] = max(error, self.max_errors[category])
            if error > (SSE_TOLERANCE if category == "sse" else TOLERANCE):
                self.failures.append(label + ":numeric_tolerance")
        else:
            raise TypeError("unsupported expected value")


def own_controls(audit):
    """Independent exact controls, including missing-data failures."""
    records = []
    for n in (5, 9, 13, 21):
        t = [Q(i, 5) for i in range(n)]
        for name, y, expected in (
            ("constant", [Q(17)] * n, Q(0)),
            ("linear", [Q(7) - 3 * s for s in t], Q(0)),
            ("quadratic", [Q(9) + 4 * s - Q(7, 2) * s * s for s in t], Q(-7)),
        ):
            result = fit_exact(t, y, [(v - Q(3, 2), v + Q(5, 2)) for v in y])
            audit.check(result["acceleration_px_s2"] == expected, f"own/{n}/{name}/acceleration")
            audit.check(all(v == 0 for v in result["fits"]["2"]["residuals"]), f"own/{n}/{name}/exact_residuals")
            records.append({"name": f"{name}_{n}", "passed": True, "acceleration_exact": str(expected)})
        blank = [Q(0)] * n
        f = fit_exact(t, blank)
        for i in range(n):
            impulse = blank.copy()
            impulse[i] = 1
            audit.check(fit_exact(t, impulse)["acceleration_px_s2"] == f["weights"][i], f"own/{n}/weight/{i}")
        moved = fit_exact([s + 313 for s in t], [v + 999 for v in y])
        audit.check(moved["acceleration_px_s2"] == expected, f"own/{n}/translation")
        records.append({"name": f"impulse_weights_and_translation_{n}", "passed": True, "weights_checked": n})
    times = [Q(i, 5) for i in range(5)]
    ranges = [(Q(i) - Q(1, 3), Q(i) + Q(7, 4)) for i in range(5)]
    fitted = fit_exact(times, [Q(i) for i in range(5)], ranges)
    vertices = [fit_exact(times, [ranges[i][b] for i, b in enumerate(bits)])["acceleration_px_s2"] for bits in itertools.product((0, 1), repeat=5)]
    audit.check([min(vertices), max(vertices)] == fitted["acceleration_interval_px_s2"], "own/exhaustive_vertices")
    records.append({"name": "asymmetric_interval_all32_vertices", "passed": True, "extrema_exact": [str(min(vertices)), str(max(vertices))]})
    for name, t, y in (
        ("missing_middle", times, [0, 1, None, 3, 4]),
        ("duplicate_time", [0, 1, 1, 3, 4], [0, 1, 2, 3, 4]),
        ("nonfinite", times, [0, 1, float("nan"), 3, 4]),
    ):
        rejected = False
        try:
            fit_exact(t, y)
        except ValueError:
            rejected = True
        audit.check(rejected, "own/reject/" + name)
        records.append({"name": name, "passed": rejected})
    return records


def load_datasets(audit):
    datasets = {}
    for observer in ("root", "independent"):
        src = parse(INPUT_PATHS[observer])
        audit.check(src["observer"] == observer, observer + ":label")
        audit.check([r["frame"] for r in src["rows"]] == SELECTED, observer + ":frames")
        datasets[observer] = {r["frame"]: r for r in src["rows"]}
        for row in src["rows"]:
            for target in ("A", "B"):
                p = row[target]
                if p["status"] == "localized":
                    audit.check(p["ymin"] <= p["y"] <= p["ymax"], f"{observer}/{row['frame']}/{target}/y_bracket")
                    if target == "A":
                        audit.check(p["xmin"] <= p["x"] <= p["xmax"], f"{observer}/{row['frame']}/A/x_bracket")
                else:
                    audit.check(p["status"] == "unlocalizable" and all(p[k] is None for k in ("y", "ymin", "ymax")), f"{observer}/{row['frame']}/{target}/missing")
                if target == "B":
                    audit.check(p["x"] == 322, f"{observer}/{row['frame']}/B/fixed_column")
    points = parse(INPUT_PATHS["points"])
    audit.check(len(points["tracks"]) == 2, "points:tracks")
    tracks = {}
    for ordinal, track in enumerate(points["tracks"], 1):
        audit.check(track["track"] == f"track{ordinal:02d}", "points:ordinal_label")
        audit.check([p["frame"] for p in track["points"]] == list(range(138, 349, 3)), "points:71_mark_grid")
        tracks[ordinal] = {p["frame"]: p for p in track["points"]}
        for p in track["points"]:
            for axis in ("x", "y"):
                audit.compare(p[axis], rational(p[axis + "_text"]), f"points/{ordinal}/{p['frame']}/{axis}", "source_decimal")
                audit.counts["source_coordinate_decimal_checks"] += 1
    datasets["saved"] = {}
    for frame in SELECTED:
        datasets["saved"][frame] = {}
        for target, ordinal in (("A", 1), ("B", 2)):
            p = tracks[ordinal][frame]
            datasets["saved"][frame][target] = {
                "x": rational(p["x_text"]), "y": rational(p["y_text"]), "status": "localized",
            }
    return datasets


def series_point(dataset, frame, target, is_saved):
    selected = [dataset[frame][k] for k in (("A", "B") if target == "AminusB" else (target,))]
    if any(p["status"] != "localized" or p["y"] is None for p in selected):
        return None, None
    if target == "AminusB":
        a, b = selected
        y = rational(a["y"]) - rational(b["y"])
        interval = None if is_saved else [rational(a["ymin"]) - rational(b["ymax"]), rational(a["ymax"]) - rational(b["ymin"])]
    else:
        p = selected[0]
        y = rational(p["y"])
        interval = None if is_saved else [rational(p["ymin"]), rational(p["ymax"])]
    return y, interval


def verify_fit_rows(audit, datasets, actual):
    expected_keys, lookup, failed = [], {}, []
    for row in actual:
        key = (row["observer"], row["target"], tuple(row["frames"]))
        audit.check(key not in lookup, "fits:duplicate_key")
        lookup[key] = row
    for observer, dataset in datasets.items():
        for target in ("A", "B", "AminusB"):
            for n in (9, 13, 21):
                for start in range(22 - n):
                    frames = LATE[start:start + n]
                    key = (observer, target, tuple(frames))
                    expected_keys.append(key)
                    audit.check(key in lookup, "fits:missing_key")
                    if key not in lookup:
                        continue
                    t = [Q(f - 138, 15) for f in frames]
                    pairs = [series_point(dataset, f, target, observer == "saved") for f in frames]
                    missing = [f for f, (y, iv) in zip(frames, pairs) if y is None]
                    expected = {"observer": observer, "target": target, "frames": frames, "time": t, "window_points": n}
                    if missing:
                        expected.update(status="uncomputed_missing_localization", missing_frames=missing)
                        failed.append({"observer": observer, "target": target, "first": frames[0], "last": frames[-1], "missing": missing})
                        audit.counts["uncomputed_windows"] += 1
                    else:
                        y = [p[0] for p in pairs]
                        intervals = None if observer == "saved" else [p[1] for p in pairs]
                        result = fit_exact(t, y, intervals)
                        expected.update(status="pass", **result)
                        audit.counts["computed_windows"] += 1
                        audit.counts["computed_" + observer + "_" + target] += 1
                        audit.counts["fit_coefficient_scalars"] += 5
                        audit.counts["fit_residual_scalars"] += 2 * n
                        audit.counts["quadratic_weights"] += n
                        audit.counts["fitted_position_scalars"] += n
                        audit.counts["fit_interval_endpoints"] += 0 if intervals is None else 2
                        if target == "AminusB":
                            fa = fit_exact(t, [series_point(dataset, f, "A", True)[0] for f in frames])
                            fb = fit_exact(t, [series_point(dataset, f, "B", True)[0] for f in frames])
                            audit.check(result["acceleration_px_s2"] == fa["acceleration_px_s2"] - fb["acceleration_px_s2"], "fits:direct_difference_linearity")
                            common = [Q((i * i + 7 * i) % 11, 3) for i in range(n)]
                            shifted_difference = [(rational(dataset[f]["A"]["y"]) + c) - (rational(dataset[f]["B"]["y"]) + c) for f, c in zip(frames, common)]
                            audit.check(shifted_difference == y, "fits:pointwise_common_translation_cancels")
                            audit.counts["difference_linearity_checks"] += 1
                    audit.compare(lookup[key], expected, f"fit/{observer}/{target}/{frames[0]}-{frames[-1]}")
    audit.check(set(lookup) == set(expected_keys) and len(actual) == 207, "fits:exact_207_record_coverage")
    return failed


def verify_comparisons(audit, datasets, actual):
    lookup = {(r["target"], r["frame"]): r for r in actual}
    audit.check(len(lookup) == len(actual) == 44, "comparison:44_unique_rows")
    for frame in SELECTED:
        for target in ("A", "B"):
            source = datasets["saved"][frame][target]
            expected = {"target": target, "frame": frame, "saved_xy": [source["x"], source["y"]], "observers": {}}
            intervals = []
            for observer in ("root", "independent"):
                p = datasets[observer][frame][target]
                entry = {"status": p["status"], "definition_warning": None if target == "A" else "fixed-column silhouette versus saved moving-x query; not equal material identity"}
                if p["status"] == "localized":
                    iv = [p["ymin"], p["ymax"]]
                    intervals.append(iv)
                    entry.update(x=p["x"], y=p["y"], y_interval=iv,
                                 dx_from_saved=rational(p["x"]) - source["x"],
                                 dy_from_saved=rational(p["y"]) - source["y"],
                                 saved_y_inside=iv[0] <= source["y"] <= iv[1])
                    if target == "A":
                        entry.update(x_interval=[p["xmin"], p["xmax"]], saved_x_inside=p["xmin"] <= source["x"] <= p["xmax"])
                    audit.counts["localized_comparison_entries"] += 1
                else:
                    audit.counts["missing_comparison_entries"] += 1
                expected["observers"][observer] = entry
            expected["new_y_intervals_overlap"] = None if len(intervals) != 2 else max(i[0] for i in intervals) <= min(i[1] for i in intervals)
            audit.check((target, frame) in lookup, "comparison:missing_entry")
            if (target, frame) in lookup:
                audit.compare(lookup[(target, frame)], expected, f"comparison/{target}/{frame}")


def verify_producer_controls(audit, actual):
    c = {row["name"]: row for row in actual}
    names = {"constant", "linear", "quadratic", "translation_time_origin", "all32_interval_vertices", "differential_common_translation", "rejections"}
    audit.check(set(c) == names and len(actual) == 7, "controls:seven_groups")
    t = [Q(i, 5) for i in range(9)]
    q = [2 + 3 * s + 4 * s * s for s in t]
    for name, y, a in (("constant", [Q(4)] * 9, 0), ("linear", [3 + 2 * s for s in t], 0), ("quadratic", q, 8)):
        expected = {"name": name, "time": t, "expected_acceleration": a, "result": fit_exact(t, y, [(v - 1, v + 1) for v in y])}
        audit.compare(c[name], expected, "control/" + name)
        audit.counts["producer_full_control_fit_results"] += 1
    base = fit_exact(t, q, [(v - 1, v + 2) for v in q])
    moved = fit_exact([s + 400 for s in t], [v + 500 for v in q], [(v + 499, v + 502) for v in q])
    audit.compare(c["translation_time_origin"], {"name": "translation_time_origin", "base": base, "moved": moved}, "control/translation")
    audit.counts["producer_full_control_fit_results"] += 2
    iv = [(v - 1, v + 2) for v in q[:5]]
    bounded = fit_exact(t[:5], q[:5], iv)
    vertices = []
    for bits in itertools.product((0, 1), repeat=5):
        y = [iv[i][b] for i, b in enumerate(bits)]
        vertices.append({"bits": list(bits), "y": y, "a": fit_exact(t[:5], y)["acceleration_px_s2"]})
    audit.check([min(v["a"] for v in vertices), max(v["a"] for v in vertices)] == bounded["acceleration_interval_px_s2"], "control/producer_vertices_exact_extrema")
    audit.compare(c["all32_interval_vertices"], {"name": "all32_interval_vertices", "time": t[:5], "bounded": bounded, "vertices": vertices}, "control/32vertices")
    audit.counts["producer_full_control_fit_results"] += 1
    audit.counts["producer_control_vertices"] += 32
    aa = [5 + 3 * s + 4 * s * s for s in t]
    bb = [3 + 8 * s + 3 * s * s for s in t]
    common = [7 + 11 * s + 2 * s * s for s in t]
    diff = [a - b for a, b in zip(aa, bb)]
    after = [(a + shift) - (b + shift) for a, b, shift in zip(aa, bb, common)]
    audit.check(diff == after, "control/differential_exact_cancellation")
    audit.compare(c["differential_common_translation"], {"name": "differential_common_translation", "time": t, "A": aa, "B": bb, "common": common, "before": fit_exact(t, diff), "after": fit_exact(t, after)}, "control/differential")
    audit.counts["producer_full_control_fit_results"] += 2
    # Names/reasons only: this is not reproduction of the attempted arrays.
    audit.compare(c["rejections"], {"name": "rejections", "outcomes": [{"name": "duplicate_time", "reason": "clock_order"}, {"name": "nonfinite", "reason": "shape_or_finite"}]}, "control/retained_rejection_labels_only")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="independent-fit-verification01.json")
    args = parser.parse_args()
    output = (BASE / args.output).resolve()
    if output.parent != BASE or output.exists() or not output.name.endswith(".json"):
        raise ValueError("output must be a new JSON file directly in the declared unit")
    audit = Audit()
    before = {name: measure(path) for name, path in INPUT_PATHS.items()}
    for name, expected in PINS.items():
        audit.check(before[name]["sha256"] == expected, "input_pin:" + name)
    if audit.failures:
        raise ValueError("frozen_input_pin_mismatch")
    receipt_path = BASE / "analysis01/receipt.json"
    receipt = parse(receipt_path)
    audit.compare(receipt["inputs_before"], before, "receipt/inputs_before")
    audit.compare(receipt["inputs_after"], before, "receipt/inputs_after")
    products = {name: measure(BASE / "analysis01" / name) for name in ("fits.json", "comparison.json", "controls.json")}
    audit.compare(receipt["products"], products, "receipt/products")
    audit.compare({k: receipt[k] for k in ("computed", "control_groups", "missing_localization", "windows", "status")}, {"computed": 187, "control_groups": 7, "missing_localization": 20, "windows": 207, "status": "pass_conditional_image_only"}, "receipt/counts")
    controls = own_controls(audit)
    datasets = load_datasets(audit)
    failed = verify_fit_rows(audit, datasets, parse(BASE / "analysis01/fits.json"))
    verify_comparisons(audit, datasets, parse(BASE / "analysis01/comparison.json"))
    verify_producer_controls(audit, parse(BASE / "analysis01/controls.json"))
    after = {name: measure(path) for name, path in INPUT_PATHS.items()}
    audit.compare(after, before, "inputs_unchanged")
    audit.compare({name: measure(BASE / "analysis01" / name) for name in products}, products, "products_unchanged")
    result = {
        "status": "pass_arithmetic_with_declared_scope" if not audit.failures else "failed_verification",
        "verifier": measure(Path(__file__)),
        "command": [sys.executable, *sys.argv], "python": platform.python_version(),
        "method": "Independent Fraction equal-grid symmetry normal equations; analytic Gram eigenvalues; exact signed interval extrema; no producer import or execution.",
        "tolerances_absolute": {"general": TOLERANCE, "sse": SSE_TOLERANCE},
        "inputs_before": before, "inputs_after": after,
        "producer_receipt": measure(receipt_path), "producer_products": products,
        "counts": dict(sorted(audit.counts.items())),
        "maximum_absolute_errors": dict(sorted(audit.max_errors.items())),
        "failures": audit.failures, "independent_synthetic_controls": controls,
        "preserved_uncomputed_windows": failed,
        "limits": [
            "Arithmetic reproduction does not authenticate historical media, calibrate placement envelopes, or identify material acceleration, force or cause.",
            "Camera3 images and correlations were not re-decoded or re-annotated in this arithmetic subtask.",
            "Saved track intervals are unknown/null, never zero-width or a measured uncertainty bound.",
            "B is a fixed-column silhouette sample; saved track02 has moving x. Retained dx cannot establish material identity.",
            "Two producer rejection labels lack attempted arrays; independent rejection analogues are checked, but retained producer attempts are not fully reproduced.",
            "Computational independent implementation is not human or licensed-engineering review; results remain research-only.",
        ],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"status": result["status"], "failures": audit.failures, "counts": result["counts"], "maximum_absolute_errors": result["maximum_absolute_errors"], "output_sha256": measure(output)["sha256"]}, sort_keys=True))
    return 0 if not audit.failures else 1


if __name__ == "__main__":
    sys.exit(main())
