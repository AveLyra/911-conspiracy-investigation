"""Post-freeze integration of the independent fixed synthetic Ruby oracle.

Stdout-only result; no historical data, file writes, expected-value changes or
source registration. The adapter is not an independent implementation itself.
"""

from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parent
PINS = {
    "math-oracle.rb": "90afe295b11e179f14ce4286917cd781d1d39700a4916094dafc688915ef9905",
    "curve_math.py": "7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1",
}


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in PINS}


def run():
    before = hashes()
    if before != PINS:
        raise ValueError("frozen oracle/core hash mismatch")
    from curve_math import (
        ORDER_TAG, SUPPORT_TAG, SupportedBranch, compare_curves, mn_m_to_nm, ordered_area,
    )

    process = subprocess.run(["ruby", str(ROOT / "math-oracle.rb")], cwd=ROOT,
                             capture_output=True, text=True, timeout=10, check=False)
    if process.returncode != 0 or process.stderr:
        raise ValueError("oracle did not complete cleanly with empty stderr")
    oracle = json.loads(process.stdout)
    if oracle.get("status") != "synthetic_only" or oracle.get("assertions") != 39:
        raise ValueError("unexpected oracle scope/status")

    # Exact pre-existing oracle inputs, transcribed as explicit ordinate arrays.
    cases = {
        "identical_different_partition": (
            [[(0, 0), (1, 1)]], [[(0, 0), (Q(1, 3), Q(1, 3)), (1, 1)]]),
        "sign_cancellation": ([[(0, 1), (1, 1)]], [[(0, 0), (1, 2)]]),
        "zero_reference": ([[(0, 0), (1, 0)]], [[(0, 2), (1, 2)]]),
        "narrow_triangle": (
            [[(0, 0), (1, 0)]],
            [[(0, 0), (Q(49, 100), 0), (Q(1, 2), 1), (Q(51, 100), 0), (1, 0)]]),
        "disconnected_support": (
            [[(0, 1), (Q(1, 4), 1)], [(Q(3, 4), 1), (1, 1)]], [[(0, 2), (1, 2)]]),
    }
    fields = {
        "length": "common_length",
        "signed": "signed_difference_area",
        "absolute": "absolute_difference_area",
        "squared": "squared_difference_integral",
        "maximum": "maximum_absolute_difference",
        "reference_area": "reference_area",
        "candidate_area": "candidate_area",
    }
    if set(oracle["comparisons"]) != set(cases):
        raise ValueError("oracle comparison membership changed")
    compared = {}
    for name, (ref, cand) in cases.items():
        reference = tuple(SupportedBranch(f"reference-{i}", SUPPORT_TAG, points)
                          for i, points in enumerate(ref))
        candidate = tuple(SupportedBranch(f"candidate-{i}", SUPPORT_TAG, points)
                          for i, points in enumerate(cand))
        result = compare_curves(reference, candidate, x_axis=(0, 1), y_axis=(0, 2))
        expected = oracle["comparisons"][name]
        if set(expected) != set(fields):
            raise ValueError(f"oracle field membership changed: {name}")
        for oracle_key, core_key in fields.items():
            actual = result[core_key]
            if oracle_key == "maximum":
                actual = actual["value"]
            if actual != Q(expected[oracle_key]):
                raise ValueError(f"independent disagreement: {name}/{oracle_key}")
            compared[f"{name}/{oracle_key}"] = str(actual)

    paths = {
        "reversal": [(0, 0), (1, 1), (0, 0)],
        "vertical_drop": [(0, 0), (1, 1), (1, 0), (2, 0)],
        "elastic_work": [(0, 0), (1, 1)],
    }
    for name, points in paths.items():
        actual = ordered_area(points, order_tag=ORDER_TAG)
        if actual != Q(oracle["ordered"][name]):
            raise ValueError(f"independent disagreement: ordered/{name}")
        compared[f"ordered/{name}"] = str(actual)
    unit = mn_m_to_nm(1)
    if unit != Q(oracle["one_MN_m_in_N_m"]):
        raise ValueError("independent disagreement: unit conversion")
    compared["one_MN_m_in_N_m"] = str(unit)
    if len(compared) != 39 or hashes() != before:
        raise ValueError("incomplete comparison or input mutation")
    return {
        "status": "synthetic_oracle_matches",
        "compared_values": len(compared),
        "oracle_assertions": oracle["assertions"],
        "input_hashes_before_after": before,
        "oracle_stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
        "comparisons": compared,
        "limit": "Fixed synthetic arithmetic only; adapter is post-freeze integration, not independent authorship. No historical measurement or human acceptance.",
    }


if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except Exception as error:
        print(json.dumps({"status": "failed", "reason": str(error)}, sort_keys=True))
        raise SystemExit(1)
