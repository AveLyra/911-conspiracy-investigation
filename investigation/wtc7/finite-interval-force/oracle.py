#!/usr/bin/env python3
"""Independent exact-rational oracle; no producer imports or solver calls."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import re
import sys
from fractions import Fraction as Q

TABLE_HASH = "a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc"
PDF_HASH = "cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394"
G = Q(981, 100)
HALF_CELL = Q(1, 200)
TRIPLES = {
    "NE": ("ne_y", ("8.0", "8.6", "9.2")),
    "EC": ("ec_y", ("8.2", "9.4", "10.6")),
    "WC": ("wc_y", ("8.2", "9.4", "10.6")),
    "NW": ("nw_y", ("8.2", "9.4", "10.6")),
}
CLOCKS = (Q(1), Q(1001, 1000), Q(1000, 999))
RHOS = (Q(0), Q(1, 10), Q(1, 4), Q(1, 2), Q(3, 4), Q(1))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def token_q(token):
    if not isinstance(token, str) or not re.fullmatch(r"-?\d+\.\d+", token):
        raise ValueError("Expected a finite decimal string; nulls are not zero")
    return Q(token)


def selected_rows(table, field, times):
    wanted = tuple(token_q(t) for t in times)
    slots = []
    for target in wanted:
        matches = [(i, row) for i, row in enumerate(table["rows"])
                   if token_q(row["time_s"]) == target]
        if len(matches) != 1:
            raise ValueError("Missing or duplicated requested time")
        slot, row = matches[0]
        source_y = token_q(row[field])
        slots.append({
            "array_index_zero_based": slot,
            "source_row_one_based": row["row"],
            "source_page": row["page"],
            "position_column": field,
            "raw_time_token": row["time_s"],
            "raw_upward_y_token": row[field],
            "downward_position": str(-source_y),
        })
    if wanted[1] - wanted[0] <= 0 or wanted[1] - wanted[0] != wanted[2] - wanted[1]:
        raise ValueError("Requested samples must be equally spaced and increasing")
    return slots


def second_difference(values, half_duration):
    if half_duration <= 0:
        raise ValueError("Half duration must be positive")
    return (values[0] - 2 * values[1] + values[2]) / half_duration ** 2


def hinge(displacement_second_difference_low, half_duration, rho):
    # Integrate force first: q_COM <= h^2*g*(1-rho), and
    # q_COM >= q_point_low - 4B. This form avoids a producer's A-first path.
    return max(Q(0), (displacement_second_difference_low -
                     half_duration ** 2 * G * (1 - rho)) / 4)


def make_results(table):
    cases = []
    all_inputs = []
    for point, (field, times) in TRIPLES.items():
        selected = selected_rows(table, field, times)
        all_inputs.extend(dict(point=point, **entry) for entry in selected)
        nominal_h = (token_q(times[2]) - token_q(times[0])) / 2
        positions = [Q(entry["downward_position"]) for entry in selected]
        q_center = positions[0] - 2 * positions[1] + positions[2]
        q_low = q_center - 4 * HALF_CELL
        for multiplier in CLOCKS:
            h = nominal_h * multiplier
            a = q_center / (h * h)
            printing_half_width = 4 * HALF_CELL / (h * h)
            intercept = (q_low - G * h * h) / 4
            slope = G * h * h / 4
            thresholds = [{"rho": str(rho), "minimum_B": str(hinge(q_low, h, rho))}
                          for rho in RHOS]
            assert all(Q(v["minimum_B"]) == max(Q(0), intercept + slope * Q(v["rho"]))
                       for v in thresholds)
            cases.append({
                "point": point,
                "position_column": field,
                "raw_time_tokens": list(times),
                "source_rows": [v["source_row_one_based"] for v in selected],
                "clock_time_multiplier": str(multiplier),
                "h_assigned_seconds": str(h),
                "q_center_assigned_metres": str(q_center),
                "A_assigned_metres_per_second_squared": str(a),
                "A_printing_half_width": str(printing_half_width),
                "A_printing_interval": [str(a - printing_half_width), str(a + printing_half_width)],
                "B_hinge_intercept_assigned_metres": str(intercept),
                "B_hinge_slope_assigned_metres": str(slope),
                "unclipped_hinge_zero_rho": str(-intercept / slope),
                "thresholds": thresholds,
            })
    assert len(all_inputs) == 12 and len(cases) == 12
    assert sum(len(c["thresholds"]) for c in cases) == 72
    return {
        "meaning": "Conditional necessary displacement for an at-least-rho triangular-weighted signed net upward force fraction",
        "historical_measurement_or_probability": False,
        "g_reference": str(G),
        "rounding_cell_half_width_assigned_metres": str(HALF_CELL),
        "input_slots": all_inputs,
        "cases": cases,
    }


def triangle_moment(power, h):
    # Exact integration: 2/h^2 * integral_0^h (h-s)*s^power ds.
    if power % 2:
        return Q(0)
    return 2 * h ** power / ((power + 1) * (power + 2))


def integrated_monomial_acceleration(power, center, h):
    if power < 2:
        return Q(0)
    return power * (power - 1) * sum(
        (Q(math.comb(power - 2, k)) * center ** (power - 2 - k) * triangle_moment(k, h)
         for k in range(power - 1)), Q(0))


def expect_rejection(fn):
    try:
        fn()
    except (ValueError, KeyError):
        return True
    raise AssertionError("Invalid input was accepted")


def make_controls():
    polynomial = []
    centers = (Q(0), Q(3, 7), Q(-5, 4))
    half_durations = (Q(3, 5), Q(6, 5), Q(5, 4))
    for n, center, h in itertools.product(range(9), centers, half_durations):
        sampled = [(center - h) ** n, center ** n, (center + h) ** n]
        difference = second_difference(sampled, h)
        integral = integrated_monomial_acceleration(n, center, h)
        assert difference == integral
        polynomial.append({"power": n, "center": str(center), "h": str(h),
                           "difference_and_integral": str(integral)})

    vertices = []
    affine_checks = 0
    for h in half_durations:
        for radius in (Q(7, 13), HALF_CELL):
            values = []
            for signs in itertools.product((-1, 1), repeat=3):
                errors = [radius * sign for sign in signs]
                response = second_difference(errors, h)
                values.append(response)
                vertices.append({"h": str(h), "B": str(radius), "signs": list(signs),
                                 "A_error": str(response)})
                for center in centers:
                    times = [center - h, center, center + h]
                    translated = [e + Q(19, 11) - Q(7, 9) * t for e, t in zip(errors, times)]
                    assert second_difference(translated, h) == response
                    affine_checks += 1
            assert min(values) == -4 * radius / h ** 2
            assert max(values) == 4 * radius / h ** 2

    inverse = []
    for h, lower_a, rho in itertools.product(half_durations, (Q(8), G, Q(12)), RHOS):
        minimum = hinge(lower_a * h * h, h, rho)
        at_boundary_upper_R = 1 - (lower_a - 4 * minimum / h ** 2) / G
        assert at_boundary_upper_R >= rho
        if minimum > 0:
            assert at_boundary_upper_R == rho
            below = minimum / 2
            assert 1 - (lower_a - 4 * below / h ** 2) / G < rho
        above = minimum + Q(1, 100)
        assert 1 - (lower_a - 4 * above / h ** 2) / G >= rho
        # r(s)=B*(2*s^2/h^2-1) is bounded by B over [-h,h]
        # and attains the needed positive extremal second difference.
        witness = [minimum, -minimum, minimum]
        assert second_difference(witness, h) == 4 * minimum / h ** 2
        inverse.append({"h": str(h), "a_low": str(lower_a), "rho": str(rho),
                        "B_min": str(minimum), "boundary_R_upper": str(at_boundary_upper_R)})

    invalid = []
    for bad in (None, "NaN", "1/2", "", 1.0, "inf", "--1.00"):
        assert expect_rejection(lambda bad=bad: token_q(bad))
        invalid.append({"kind": "malformed_or_null_decimal", "input": bad, "rejected": True})
    tiny = {"rows": [{"row": i + 1, "page": 47, "time_s": t, "ne_y": "1.00"}
                     for i, t in enumerate(("0.0", "1.0", "2.0"))]}
    mutations = {
        "missing_time": {"rows": tiny["rows"][:2]},
        "duplicate_time": {"rows": tiny["rows"] + [tiny["rows"][0]]},
        "null_position": {"rows": [dict(r, ne_y=None) if r["row"] == 2 else r for r in tiny["rows"]]},
        "missing_position": {"rows": [{k: v for k, v in r.items() if k != "ne_y"} if r["row"] == 2 else r for r in tiny["rows"]]},
    }
    for name, malformed in mutations.items():
        assert expect_rejection(lambda malformed=malformed: selected_rows(malformed, "ne_y", ("0.0", "1.0", "2.0")))
        invalid.append({"kind": name, "rejected": True})
    for bad_h in (Q(0), Q(-1)):
        assert expect_rejection(lambda bad_h=bad_h: second_difference([Q(0)] * 3, bad_h))
        invalid.append({"kind": "nonpositive_half_duration", "h": str(bad_h), "rejected": True})
    # B*cos(omega*(t-tc)) has |r|<=B but r''(tc)=-B*omega^2.
    # This identity is analytic; no sampled trigonometric maximum is claimed.
    oscillatory = [{"omega": str(w), "r_second_at_center_for_B_1": str(-w * w)}
                   for w in (Q(1), Q(10), Q(100), Q(1000))]
    return {
        "polynomial_exact_integrations": polynomial,
        "polynomial_count": len(polynomial),
        "all_eight_sign_vertices_each_B_h": vertices,
        "vertex_count": len(vertices),
        "affine_invariance_count": affine_checks,
        "inverse_boundary_and_sharpness_cases": inverse,
        "inverse_count": len(inverse),
        "invalid_input_checks": invalid,
        "invalid_count": len(invalid),
        "oscillatory_analytic_counterexample": oscillatory,
        "all_assertions_passed": True,
    }


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="Create-only child of oracle01")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    study = base.parent
    source = study / "multipoint-table-reproduction/transcription-root/table47.json"
    pdf = study / "luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf"
    protocol = base / "PROTOCOL.md"
    if digest(source) != TABLE_HASH or digest(pdf) != PDF_HASH:
        raise ValueError("Pinned source changed")
    table = json.loads(source.read_text())
    if table["source_sha256"] != PDF_HASH:
        raise ValueError("Table-to-PDF pin disagrees")
    result = make_results(table)
    controls = make_controls()
    products = {"results.json": encoded(result), "controls.json": encoded(controls)}
    receipt = {
        "source_table_sha256": digest(source),
        "source_pdf_sha256": digest(pdf),
        "protocol_sha256": digest(protocol),
        "oracle_code_sha256": digest(Path(__file__).resolve()),
        "runtime": {"python": sys.version, "executable": sys.executable,
                    "implementation": platform.python_implementation(), "platform": platform.platform()},
        "products": {name: hashlib.sha256(data).hexdigest() for name, data in products.items()},
        "case_count": 12, "threshold_count": 72,
        "calculation": "independently implemented; producer code/results not imported",
        "all_controls_passed": controls["all_assertions_passed"],
    }
    destination = (base / args.out).resolve()
    destination.relative_to(base / "oracle01")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir(exist_ok=False)
    for name, data in products.items():
        with (destination / name).open("xb") as stream:
            stream.write(data)
    with (destination / "receipt.json").open("xb") as stream:
        stream.write(encoded(receipt))
    print(json.dumps({"out": str(destination), "cases": 12, "thresholds": 72,
                      "controls_passed": True, "product_hashes": receipt["products"],
                      "code_sha256": receipt["oracle_code_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
