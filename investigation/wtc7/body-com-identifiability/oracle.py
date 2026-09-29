#!/usr/bin/env python3
"""Independent exact synthetic oracle; no historical reconstruction."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import isqrt
from pathlib import Path
import platform
import sys


CHECKS = 0
REJECTIONS = 0
ZERO = Q(0)
ONE = Q(1)
I = ((ONE, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))


def checked(condition):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(f"oracle check {CHECKS} failed")


def rejects(call):
    global REJECTIONS
    try:
        call()
    except ValueError:
        REJECTIONS += 1
        return
    raise AssertionError("expected ValueError")


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b, strict=True))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), ZERO)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def scaled(k, v):
    return tuple(k * x for x in v)


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def unit(v):
    length2 = dot(v, v)
    if length2 == 0:
        raise ValueError("rank deficient marker basis")
    numerator = isqrt(length2.numerator)
    denominator = isqrt(length2.denominator)
    if numerator ** 2 != length2.numerator or denominator ** 2 != length2.denominator:
        raise ValueError("this exact fixture oracle requires rational unit basis")
    return scaled(ONE / Q(numerator, denominator), v)


def basis(points):
    e1 = unit(sub(points[1], points[0]))
    other = sub(points[2], points[0])
    e2 = unit(sub(other, scaled(dot(other, e1), e1)))
    return (e1, e2, cross(e1, e2))


def recover_pose(local, world):
    # Each basis tuple contains three basis vectors, not matrix rows.
    source, target = basis(local), basis(world)
    rotation = tuple(tuple(sum((target[k][i] * source[k][j]
                               for k in range(3)), ZERO)
                           for j in range(3)) for i in range(3))
    translation = sub(world[0], matvec(rotation, local[0]))
    if any(add(matvec(rotation, a), translation) != b
           for a, b in zip(local, world, strict=True)):
        raise ValueError("marker geometry is not congruent")
    return rotation, translation


def curvature(values, h):
    if h <= 0:
        raise ValueError("positive half-span required")
    return (values[0] - 2 * values[1] + values[2]) / h ** 2


def affine_witness(values, h):
    if h <= 0:
        raise ValueError("positive half-span required")
    difference = values[0] - 2 * values[1] + values[2]
    signed = difference / 4
    residual = (signed, -signed, signed)
    line = sub(values, residual)
    checked(curvature(line, h) == 0)
    checked(max(abs(x) for x in residual) == abs(difference) / 4)
    checked(add(line, residual) == tuple(values))
    return {"B_min": abs(difference) / 4,
            "line_at_samples": line,
            "residual_at_samples": residual,
            "line_intercept": line[1],
            "line_slope": (line[2] - line[0]) / (2 * h)}


def envelope_curvature(intervals, h):
    if h <= 0 or any(lo > hi for lo, hi in intervals):
        raise ValueError("invalid interval or half-span")
    lo = (intervals[0][0] - 2 * intervals[1][1] + intervals[2][0]) / h ** 2
    hi = (intervals[0][1] - 2 * intervals[1][0] + intervals[2][1]) / h ** 2
    return lo, hi


def fixtures():
    roof = ((Q(-1), ZERO, ZERO), (ZERO, ZERO, ZERO), (ONE, ZERO, ZERO))
    off = (ZERO, ZERO, ONE)
    hidden_cases, rigid_cases, envelope_cases = [], [], []
    for eta, h, bound in product((Q(1, 4), Q(1, 2)), (Q(1), Q(2)), (Q(1, 10), Q(1, 2))):
        times = (-h, ZERO, h)
        visible = tuple(5 * t ** 2 for t in times)
        hidden_baseline = tuple(p + 4 for p in visible)
        hidden_alternative = tuple(p + 4 - bound / eta * (2 * (t / h) ** 2 - 1)
                                   for p, t in zip(visible, times, strict=True))
        combined = lambda hidden: tuple((1 - eta) * p + eta * q
                                        for p, q in zip(visible, hidden, strict=True))
        z0, z1 = combined(hidden_baseline), combined(hidden_alternative)
        relative = sub(visible, z1)
        witness = affine_witness(relative, h)
        checked(0 < eta < 1)
        checked(curvature(visible, h) == 10)
        checked(curvature(z0, h) == 10)
        checked(curvature(z1, h) == 10 - 4 * bound / h ** 2)
        checked(max(abs(x) for x in sub(hidden_alternative, hidden_baseline)) == bound / eta)
        checked(witness["B_min"] == bound)
        hidden_cases.append({"eta": eta, "h": h, "B": bound, "times": times,
                             "visible_baseline": visible, "visible_alternative": visible,
                             "hidden_baseline": hidden_baseline, "hidden_alternative": hidden_alternative,
                             "combined_baseline": z0, "combined_alternative": z1,
                             "A_visible": curvature(visible, h), "A_COM_baseline": curvature(z0, h),
                             "A_COM_alternative": curvature(z1, h),
                             "net_force_fraction_baseline": 1 - curvature(z0, h) / 10,
                             "net_force_fraction_alternative": 1 - curvature(z1, h) / 10,
                             "relative_point_COM": relative, "affine_removal": witness,
                             "hidden_relative_excursion": bound / eta})

    for h, length, cs in product((Q(1), Q(2)), (Q(1), Q(3)),
                                ((Q(4, 5), Q(3, 5)), (Q(3, 5), Q(4, 5)))):
        cosine, sine = cs
        endpoint = ((ONE, ZERO, ZERO), (ZERO, cosine, -sine), (ZERO, sine, cosine))
        checked(cosine ** 2 + sine ** 2 == 1)
        checked(all(dot(endpoint[i], endpoint[j]) == (1 if i == j else 0)
                    for i in range(3) for j in range(3)))
        checked(dot(endpoint[0], cross(endpoint[1], endpoint[2])) == 1)
        times = (-h, ZERO, h)
        rotations = (endpoint, I, endpoint)
        roof_world, off_world, com_alternative, recovered = [], [], [], []
        for t, rotation in zip(times, rotations, strict=True):
            translation = (ZERO, ZERO, 5 * t ** 2)
            transform = lambda a: add(matvec(rotation, a), translation)
            world_roof = tuple(transform(a) for a in roof)
            checked(world_roof == tuple(add(a, translation) for a in roof))
            world_off = transform(off)
            checked((world_off != add(off, translation)) == (t != 0))
            local_markers = (roof[0], roof[1], off)
            world_markers = tuple(transform(a) for a in local_markers)
            recovered_rotation, recovered_translation = recover_pose(local_markers, world_markers)
            checked(recovered_rotation == rotation and recovered_translation == translation)
            for a, b in product(roof + (off,), repeat=2):
                checked(dot(sub(a, b), sub(a, b)) == dot(sub(transform(a), transform(b)),
                                                          sub(transform(a), transform(b))))
            rejects(lambda: recover_pose(roof, world_roof))
            roof_world.append(world_roof)
            off_world.append(world_off)
            com_alternative.append(transform((ZERO, ZERO, length))[2])
            recovered.append({"rotation": recovered_rotation, "translation": recovered_translation})
        visible = tuple(5 * t ** 2 for t in times)
        com_baseline = tuple(p + length for p in visible)
        correction = curvature(com_alternative, h) - curvature(com_baseline, h)
        checked(correction == -2 * length * (1 - cosine) / h ** 2)
        relative = sub(visible, com_alternative)
        witness = affine_witness(relative, h)
        checked(witness["B_min"] == length * (1 - cosine) / 2)
        checked(curvature(relative, h) == 4 * witness["B_min"] / h ** 2)
        rigid_cases.append({"h": h, "L": length, "cos": cosine, "sin": sine,
                            "times": times, "rotations": rotations, "roof_world": roof_world,
                            "off_axis_world": off_world, "COM_baseline": com_baseline,
                            "COM_alternative": com_alternative, "A_visible": curvature(visible, h),
                            "A_COM_baseline": curvature(com_baseline, h),
                            "A_COM_alternative": curvature(com_alternative, h),
                            "COM_curvature_change": correction,
                            "relative_point_COM": relative, "affine_removal": witness,
                            "recovered_poses": recovered})

    for label, low, high in (("loose", Q(0), Q(2)), ("tight", Q(9, 10), Q(11, 10))):
        intervals = ((low, high),) * 3
        bounds = envelope_curvature(intervals, ONE)
        corners = tuple(product((low, high), repeat=3))
        values = tuple(curvature(q, ONE) for q in corners)
        checked(min(values) == bounds[0] and max(values) == bounds[1])
        mixtures = []
        for a, b in zip(corners, reversed(corners), strict=True):
            mixture = tuple(x / 3 + 2 * y / 3 for x, y in zip(a, b, strict=True))
            checked(all(low <= x <= high for x in mixture))
            checked(bounds[0] <= curvature(mixture, ONE) <= bounds[1])
            mixtures.append({"component_one": a, "component_two": b,
                             "combined": mixture, "A_offset": curvature(mixture, ONE)})
        force_bounds = (-bounds[1] / 10, -bounds[0] / 10)
        checked((force_bounds[1] >= Q(1, 4)) == (label == "loose"))
        envelope_cases.append({"label": label, "h": ONE, "offset_intervals": intervals,
                               "offset_curvature_interval": bounds, "corners": corners,
                               "corner_curvatures": values, "mixture_weights": (Q(1, 3), Q(2, 3)),
                               "fixed_mass_mixtures": mixtures, "A_visible": Q(10),
                               "A_COM_interval": (10 + bounds[0], 10 + bounds[1]),
                               "net_force_fraction_interval": force_bounds,
                               "permits_fraction_at_least_one_quarter": force_bounds[1] >= Q(1, 4)})

    affine_controls = []
    for label, values in (("zero", (Q(0), Q(0), Q(0))),
                          ("linear", (Q(-2), Q(1), Q(4))),
                          ("quadratic", (Q(1), Q(0), Q(1)))):
        witness = affine_witness(values, ONE)
        checked(witness["B_min"] == (Q(1, 2) if label == "quadratic" else Q(0)))
        affine_controls.append({"label": label, "values": values, "witness": witness})
    rejects(lambda: curvature((ZERO, ZERO, ZERO), ZERO))
    rejects(lambda: curvature((ZERO, ZERO, ZERO), Q(-1)))
    rejects(lambda: affine_witness((ZERO, ZERO, ZERO), ZERO))
    rejects(lambda: envelope_curvature(((Q(2), Q(1)),) * 3, ONE))
    rejects(lambda: envelope_curvature(((ZERO, ONE),) * 3, Q(-1)))
    return {"meaning": "Synthetic exact kinematic identification controls; no historical motion or mechanism evidence",
            "units": "arbitrary synthetic length and time", "g_reference": Q(10),
            "hidden": hidden_cases, "rigid": rigid_cases, "envelopes": envelope_cases,
            "affine_controls": affine_controls,
            "verification": {"assertion_checks": CHECKS, "expected_value_errors": REJECTIONS,
                             "hidden_cases": len(hidden_cases), "rigid_cases": len(rigid_cases),
                             "envelope_cases": len(envelope_cases)}}


def serializable(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serializable(item) for item in value]
    return value


def pins():
    directory = Path(__file__).resolve().parent
    dependencies = {"protocol": directory / "PROTOCOL.md", "oracle": Path(__file__).resolve(),
                    "prior_force_report": directory.parent / "finite-interval-force" / "report.md",
                    "runtime": Path(sys.executable).resolve()}
    return {name: {"sha256": sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
            for name, path in dependencies.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    before = pins()
    results = serializable(fixtures())
    after = pins()
    if before != after:
        raise RuntimeError("pinned dependency changed during computation")
    payload = (json.dumps(results, sort_keys=True, indent=2) + "\n").encode()
    receipt = {"dependencies": before, "unchanged_during_computation": True,
               "python_version": platform.python_version(), "runtime_path": str(Path(sys.executable).resolve()),
               "results_sha256": sha256(payload).hexdigest(), "results_bytes": len(payload)}
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "results.json").write_bytes(payload)
    (args.out / "receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"results_sha256": receipt["results_sha256"], **results["verification"]}, sort_keys=True))


if __name__ == "__main__":
    main()
