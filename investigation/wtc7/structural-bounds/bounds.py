#!/usr/bin/env python3
"""Deterministic elementary mechanics; no building-specific parameter inputs."""

import argparse
import csv
import hashlib
import io
import json
import math
import platform
from pathlib import Path


def number(x, *, positive=False):
    if isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x):
        raise ValueError("Expected a finite real number, not bool")
    if x < 0 or (positive and x == 0):
        raise ValueError("Expected positive/nonnegative number")
    return float(x)


def transit(mass, kinetic, segments, gravity=9.80665):
    """Downward fixed-mass translation through (stroke, upward resistance) steps.

    SI if mass kg, kinetic J, stroke m, resistance N and gravity m/s^2.
    The same equations also work in a consistently nondimensional unit system.
    A segment is ideal plastic resistance with static holding available at stop.
    """
    m, initial, g = number(mass, positive=True), number(kinetic), number(gravity, positive=True)
    steps = [(number(d, positive=True), number(r)) for d, r in segments]
    if not steps:
        raise ValueError("At least one resistance segment is required")
    energy, distance, gravity_work, resistance_work = initial, 0.0, 0.0, 0.0
    stopped = False
    for d, r in steps:
        slope = m * g - r
        if energy == 0 and slope <= 0:
            stopped = True
            break
        # First root, not just a test of the total area at the final endpoint.
        if slope < 0 and energy <= -slope * d:
            d = energy / -slope
            stopped = True
        gravity_work += m * g * d
        resistance_work += r * d
        energy += slope * d
        distance += d
        if stopped:
            energy = 0.0
            break
    residual = initial + gravity_work - resistance_work - energy
    return {"stopped": stopped, "distance": distance, "kinetic_out": energy,
            "gravity_work": gravity_work, "resistance_work": resistance_work,
            "energy_residual": residual}


def collision(mass, target_mass, velocity, restitution):
    """Impulse-isolated 1D collision; target initially stationary, down positive."""
    m, target = number(mass, positive=True), number(target_mass, positive=True)
    v, e = number(velocity), number(restitution)
    if e > 1:
        raise ValueError("This passive-collision model requires 0 <= e <= 1")
    v1 = (m - e * target) * v / (m + target)
    v2 = (1 + e) * m * v / (m + target)
    before = 0.5 * m * v * v
    after = 0.5 * m * v1 * v1 + 0.5 * target * v2 * v2
    loss = 0.5 * (m * target / (m + target)) * (1 - e * e) * v * v
    return {"moving_velocity_out": v1, "target_velocity_out": v2,
            "kinetic_before": before, "kinetic_after": after,
            "collision_loss": loss,
            "momentum_residual": m * v - m * v1 - target * v2,
            "energy_residual": before - after - loss}


def cascade(resistance_ratio, stroke_ratio, pickup, targets=8):
    """Toy normalized chain; m0 = g = h = 1. Records every visited target.

    R is normalized to *initial* weight, not current accumulated weight.
    Pickup loss and subsequent resistance work must represent distinct processes.
    """
    r, d = number(resistance_ratio), number(stroke_ratio, positive=True)
    if type(pickup) is not bool or type(targets) is not int or targets < 1:
        raise ValueError("Invalid mode/target count")
    mass, energy, total_g, total_r, total_loss = 1.0, 0.0, 0.0, 0.0, 0.0
    rows = []
    for index in range(1, targets + 1):
        gap_work = mass  # M g h, all base units = 1.
        energy += gap_work
        total_g += gap_work
        pre_collision = energy
        loss = 0.0
        if pickup:
            result = collision(mass, 1.0, math.sqrt(2 * energy / mass), 0.0)
            mass += 1.0
            energy = result["kinetic_after"]
            loss = result["collision_loss"]
            total_loss += loss
        post_collision = energy
        step = transit(mass, energy, [(d, r)], gravity=1.0)
        total_g += step["gravity_work"]
        total_r += step["resistance_work"]
        energy = step["kinetic_out"]
        rows.append({"mode": "inelastic_pickup" if pickup else "fixed_mass",
                     "resistance_over_initial_weight": r, "stroke_over_gap": d,
                     "target": index, "moving_mass_over_initial": mass,
                     "kinetic_pre_collision": pre_collision,
                     "kinetic_post_collision": post_collision,
                     "collision_loss": loss, **step,
                     "cumulative_gravity_work": total_g,
                     "cumulative_resistance_work": total_r,
                     "cumulative_collision_loss": total_loss,
                     "cumulative_energy_residual": total_g - total_r - total_loss - energy})
        if step["stopped"]:
            break
    return rows


def euler_load(modulus, inertia, length, k_factor=1.0):
    e, i, length, k = [number(x, positive=True) for x in (modulus, inertia, length, k_factor)]
    return math.pi ** 2 * e * i / (k * length) ** 2


def gravity_time(distance, initial_speed=0.0, gravity=9.80665):
    d, v, g = number(distance), number(initial_speed), number(gravity, positive=True)
    # Rationalized positive root avoids cancellation for small distance / large v.
    return 0.0 if d == 0 else 2 * d / (math.sqrt(v * v + 2 * g * d) + v)


def csv_bytes(rows):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode()


def products():
    single = []
    for delta in (0.05, 0.1, 0.5):
        for q in (0, 2, 5, 10, 20, 50):
            result = transit(1, 1, [(delta, q)], gravity=1)
            single.append({"stroke_over_drop": delta, "resistance_over_weight": q,
                           "constant_resistance_stop_threshold": 1 + 1 / delta,
                           **result})
    impacts = []
    for ratio in (0.25, 1, 4):
        for e in (0, 0.5, 1):
            impacts.append({"target_mass_ratio": ratio, "restitution": e,
                            **collision(1, ratio, 1, e)})
    chain, summary = [], []
    for pickup in (False, True):
        for delta in (0.05, 0.1, 0.5):
            for q in (0, 2, 5, 10, 20, 50):
                rows = cascade(q, delta, pickup)
                chain.extend(rows)
                summary.append({"mode": rows[0]["mode"], "stroke_over_gap": delta,
                                "resistance_over_initial_weight": q,
                                "first_stop_target": rows[-1]["target"] if rows[-1]["stopped"] else "none_in_8",
                                "targets_traversed": len(rows) - int(rows[-1]["stopped"]),
                                "kinetic_at_end": rows[-1]["kinetic_out"]})
    euler = []
    for stiffness in (1, 0.7, 0.4):
        for effective_length in (1, 2, 4, 8):
            euler.append({"modulus_ratio": stiffness, "inertia_ratio": 1,
                          "effective_length_ratio": effective_length,
                          "euler_critical_load_ratio": stiffness / effective_length ** 2})
    travel = [{"distance_m": d, "initial_downward_speed_m_per_s": v,
               "gravity_m_per_s2": 9.80665, "travel_time_s": gravity_time(d, v)}
              for d in (0.1, 1, 4, 10, 30) for v in (0, 5)]
    return {"single-target.csv": csv_bytes(single), "collisions.csv": csv_bytes(impacts),
            "eight-target-detail.csv": csv_bytes(chain), "eight-target-summary.csv": csv_bytes(summary),
            "euler-ratios.csv": csv_bytes(euler), "gravity-times.csv": csv_bytes(travel)}


def save(out):
    out.mkdir(parents=True, exist_ok=False)
    here = Path(__file__).resolve().parent
    inputs = {name: hashlib.sha256((here / name).read_bytes()).hexdigest()
              for name in ("bounds.py", "test_bounds.py", "PROTOCOL.md")}
    manifest = {"protocol": "v1", "status": "started", "inputs_sha256": inputs,
                "python_version": platform.python_version(), "outputs_sha256": {}}
    manifest_path = out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    try:
        for name, data in products().items():
            (out / name).write_bytes(data)
            manifest["outputs_sha256"][name] = hashlib.sha256(data).hexdigest()
        manifest["status"] = "complete"
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["failure_type"] = type(exc).__name__
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    print(json.dumps(save(parser.parse_args().out), indent=2, sort_keys=True))
