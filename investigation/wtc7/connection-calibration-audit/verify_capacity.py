#!/usr/bin/env python3
"""Independent exact arithmetic of a frozen, source-image-based transcription.

No root producer code or values were read to write this implementation.
All intervals are a declared display-rounding possibility, not measured errors.
The CLI creates a new receipt; it never overwrites a previous result.
"""

import argparse
from functools import reduce
from fractions import Fraction as F
import hashlib
import json
from operator import mul
from pathlib import Path
import re
import sys


BASE = Path(__file__).resolve().parent
PINS = {
    "capacity-independent.json": "8a0f3c8bece01776289265d5db5b316032321c7eae70bf7ad8e80d045e4d4b00",
    "PROTOCOL.md": "7bf240b13ff1141ce9d69381d1dcc1ac17cb2c917b4f7e11800f01ba70d28247",
    "ARITHMETIC-PROTOCOL.md": "32b68c94b0a5c60edcc4e3689f1b742aca1666d086b3bffdad3fff5384524e3b",
}
PDF = Path("/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf")
PDF_PIN = "30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def q(value):
    return {"fraction": str(value), "decimal_approx": float(value)}


def bounds(value):
    return [q(value[0]), q(value[1])]


def precision(lexeme):
    if not isinstance(lexeme, str) or not re.fullmatch(r"\d+(?:\.\d+)?", lexeme):
        raise ValueError("nonpositive-format numeric lexeme")
    return len(lexeme.partition(".")[2])


def rounding_box(lexeme):
    p = precision(lexeme)
    center = F(lexeme)
    half = F(1, 2 * 10 ** p)
    if center - half <= 0:
        raise ValueError("rounding box must be wholly positive")
    return (center - half, center + half)


def quotient_box(numerator, denominator):
    if numerator[0] <= 0 or denominator[0] <= 0:
        raise ValueError("nonpositive quotient interval")
    if numerator[0] > numerator[1] or denominator[0] > denominator[1]:
        raise ValueError("reversed interval")
    return numerator[0] / denominator[1], numerator[1] / denominator[0]


def intersection(first, second):
    low, high = max(first[0], second[0]), min(first[1], second[1])
    return None if low > high else (low, high)


def nearest_half_up(value, digits):
    """One explicitly chosen point diagnostic; not NIST's established rule."""
    if value < 0:
        raise ValueError("nonnegative-only half-up diagnostic")
    scale = 10 ** digits
    return F((value * scale + F(1, 2)).numerator // (value * scale + F(1, 2)).denominator, scale)


def stats(values):
    if not values:
        raise ValueError("no values")
    return {"average": sum(values, F(0)) / len(values), "minimum": min(values), "maximum": max(values)}


def controls():
    receipts = []

    def test(name, passed, detail):
        if not passed:
            raise AssertionError(name)
        receipts.append({"name": name, "status": "PASS", "detail": detail})

    test("decimal_precision", precision("73.4") == 1 and precision("6.0") == 1 and precision("217") == 0,
         "Trailing zero precision and integer precision preserved.")
    test("different_rounding_widths", rounding_box("10") == (F(19, 2), F(21, 2)) and rounding_box("10.0") == (F(199, 20), F(201, 20)),
         "Integer halfwidth 1/2; one-decimal halfwidth 1/20.")
    n, d = (F(3), F(5)), (F(2), F(4))
    vertices = [a / b for a in n for b in d]
    test("positive_quotient_extrema", quotient_box(n, d) == (min(vertices), max(vertices)) == (F(3, 4), F(5, 2)),
         "All four rational vertices independently checked against interval formula.")
    test("endpoint_only_intersection", intersection((F(1), F(2)), (F(2), F(3))) == (F(2), F(2)),
         "Closed-endpoint tie is retained, not rejected.")
    test("strict_separation", intersection((F(1), F(2)), (F(201, 100), F(3))) is None,
         "Positive gap cannot be turned into overlap by float tolerance.")
    test("rational_half_up_tie", nearest_half_up(F(15, 4), 1) == F(19, 5) and nearest_half_up(F(749, 200), 1) == F(37, 10),
         "3.75 rounds to3.8 under declared half-up;3.745 rounds to3.7.")
    rejected = 0
    for action in [lambda: rounding_box("0"), lambda: quotient_box((F(1), F(2)), (F(0), F(1))), lambda: quotient_box((F(2), F(1)), (F(1), F(2))), lambda: precision("NaN")]:
        try:
            action()
        except ValueError:
            rejected += 1
    test("invalid_inputs_rejected", rejected == 4, "Four explicit invalid or unsupported input fixtures rejected.")
    test("rounding_can_resolve_point_difference", intersection(quotient_box(rounding_box("10"), rounding_box("3")), rounding_box("3.2")) is not None and nearest_half_up(F(10, 3), 1) != F("3.2"),
         "A point-division mismatch need not contradict the declared input boxes.")
    test("rounding_cannot_resolve_every_difference", intersection(quotient_box(rounding_box("10"), rounding_box("3")), rounding_box("9.0")) is None,
         "A large incompatible ratio remains incompatible.")
    test("unweighted_stats", stats([F(1), F(2), F(6)]) == {"average": F(3), "minimum": F(1), "maximum": F(6)},
         "Three-element hand solution; no load or count weighting.")
    return receipts


def calculate(data):
    expected_counts = {"11-2": 22, "11-3": 13, "11-4": 20}
    if [t["table"] for t in data["tables"]] != list(expected_counts):
        raise AssertionError("table coverage")
    result_tables = []
    for table in data["tables"]:
        count = expected_counts[table["table"]]
        if [r["row"] for r in table["rows"]] != list(range(1, count + 1)):
            raise AssertionError("row coverage")
        rows, point_values, printed_values = [], [], []
        for row in table["rows"]:
            f, d, r = [row[k] for k in ("failure_load_kip", "design_shear_load_kip", "printed_ratio")]
            if [precision(v) for v in (f, d, r)] != row["decimal_places"]:
                raise AssertionError("display precision metadata")
            if precision(r) != 1:
                raise AssertionError("one-decimal printed ratio")
            expected_page = 536 if table["table"] == "11-2" and row["row"] <= 16 else 537 if table["table"] in ("11-2", "11-3") else 538
            if row["physical_page"] != expected_page:
                raise AssertionError("physical page locator")
            numerator, denominator, ratio = F(f), F(d), F(r)
            if min(numerator, denominator, ratio) <= 0:
                raise AssertionError("positive table values")
            value = numerator / denominator
            fb, db, rb = rounding_box(f), rounding_box(d), rounding_box(r)
            qb = quotient_box(fb, db)
            overlap = intersection(qb, rb)
            point_values.append(value)
            printed_values.append(ratio)
            rows.append({
                "row": row["row"], "physical_page": row["physical_page"],
                "member": row["member"], "connection": row["connection"],
                "point_quotient": q(value), "printed_minus_point": q(ratio - value),
                "point_nearest_half_up_one_decimal": q(nearest_half_up(value, 1)),
                "point_half_up_equals_printed": nearest_half_up(value, 1) == ratio,
                "point_inside_closed_printed_box": rb[0] <= value <= rb[1],
                "point_on_printed_box_endpoint": value in rb,
                "failure_box": bounds(fb), "design_box": bounds(db),
                "possible_quotient_box": bounds(qb), "printed_ratio_box": bounds(rb),
                "rounding_intersection": None if overlap is None else bounds(overlap),
                "rounding_compatible": overlap is not None,
                "rounding_endpoint_only": overlap is not None and overlap[0] == overlap[1],
            })
        aggregate = {}
        for kind, values in [("displayed_row_ratios", printed_values), ("quotients_from_displayed_loads", point_values)]:
            values_stats = stats(values)
            aggregate[kind] = {}
            for name, value in values_stats.items():
                printed_lexeme = table["printed_summary"][name]
                printed = F(printed_lexeme)
                pb = rounding_box(printed_lexeme)
                aggregate[kind][name] = {
                    "value": q(value), "printed_summary": printed_lexeme,
                    "printed_minus_computed": q(printed - value),
                    "nearest_half_up_one_decimal": q(nearest_half_up(value, 1)),
                    "half_up_equals_printed": nearest_half_up(value, 1) == printed,
                    "inside_closed_printed_box": pb[0] <= value <= pb[1],
                    "on_printed_box_endpoint": value in pb,
                }
        result_tables.append({"table": table["table"], "row_count": count,
                              "point_half_up_mismatch_rows": [r["row"] for r in rows if not r["point_half_up_equals_printed"]],
                              "point_outside_printed_box_rows": [r["row"] for r in rows if not r["point_inside_closed_printed_box"]],
                              "rounding_incompatible_rows": [r["row"] for r in rows if not r["rounding_compatible"]],
                              "rounding_endpoint_only_rows": [r["row"] for r in rows if r["rounding_endpoint_only"]],
                              "rows": rows, "unweighted_summary": aggregate})
    calculations = []
    for source in data["source_arithmetic_inputs"]:
        values = [F(v) for v in source["operands"]]
        op = source["operation"]
        if op == "divide" and len(values) == 2:
            value = values[0] / values[1]
        elif op == "multiply":
            value = reduce(mul, values, F(1))
        elif op == "mean" and values:
            value = sum(values, F(0)) / len(values)
        else:
            raise ValueError("unsupported formula fixture")
        printed = F(source["printed_result"])
        digits = precision(source["printed_result"])
        calculations.append({"id": source["id"], "physical_page": source["physical_page"],
                             "operation": op, "operands": source["operands"], "unit": source["unit"],
                             "computed": q(value), "printed_result": source["printed_result"],
                             "printed_minus_computed": q(printed - value),
                             "nearest_half_up_at_printed_precision": q(nearest_half_up(value, digits)),
                             "half_up_equals_printed": nearest_half_up(value, digits) == printed})
    all_rows = [r for t in result_tables for r in t["rows"]]
    return {
        "scope": "All 55 rows and 9 summaries. Exact rational arithmetic; all displayed loads treated as positive. Both printed-row-ratio and displayed-load-quotient summaries are unweighted.",
        "interpretation_limit": "Closed display-rounding boxes are a possibility test only; unknown real rounding, hidden digits, weighting, connection accuracy and physics are not validated. Formula calculations do not impose rounding boxes on engineering parameters.",
        "row_count": len(all_rows),
        "point_half_up_mismatch_count": sum(not r["point_half_up_equals_printed"] for r in all_rows),
        "point_outside_printed_box_count": sum(not r["point_inside_closed_printed_box"] for r in all_rows),
        "rounding_incompatible_count": sum(not r["rounding_compatible"] for r in all_rows),
        "rounding_endpoint_only_count": sum(r["rounding_endpoint_only"] for r in all_rows),
        "tables": result_tables,
        "source_arithmetic": calculations,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Create-only JSON basename within this unit")
    args = parser.parse_args()
    name = Path(args.output)
    if name.name != args.output or name.suffix != ".json":
        parser.error("output must be a JSON basename")
    output = BASE / name
    if output.exists():
        parser.error("refusing existing output")
    control_results = controls()
    before = {name: digest(BASE / name) for name in PINS}
    before["source_pdf"] = digest(PDF)
    before["verifier_code"] = digest(Path(__file__))
    for name, pin in PINS.items():
        if before[name] != pin:
            raise AssertionError("pinned input changed: " + name)
    if before["source_pdf"] != PDF_PIN:
        raise AssertionError("source PDF changed")
    source = json.loads((BASE / "capacity-independent.json").read_text())
    result = calculate(source)
    after = {name: digest(BASE / name) for name in PINS}
    after["source_pdf"] = digest(PDF)
    after["verifier_code"] = digest(Path(__file__))
    if before != after:
        raise AssertionError("input changed during run")
    receipt = {"status": "PASS", "command": [sys.executable, *sys.argv],
               "python": sys.version, "pins_before": before, "pins_after": after,
               "controls": control_results, "result": result}
    with output.open("x", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": "PASS", "output": output.name, "sha256": digest(output),
                      "controls": len(control_results), "rows": result["row_count"],
                      "point_half_up_mismatches": result["point_half_up_mismatch_count"],
                      "rounding_incompatible": result["rounding_incompatible_count"]}))


if __name__ == "__main__":
    main()
