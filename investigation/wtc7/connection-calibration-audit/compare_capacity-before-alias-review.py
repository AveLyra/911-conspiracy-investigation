#!/usr/bin/env python3
"""Post-freeze schema adapter: no root producer implementation is imported."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import verify_capacity as independent


BASE = Path(__file__).resolve().parent
EXPECTED = {
    "capacity-independent.json": "8a0f3c8bece01776289265d5db5b316032321c7eae70bf7ad8e80d045e4d4b00",
    "verify_capacity.py": "59f3da69a009c98c8fdd1d5e8f6fdef2ff3e3ec1bdd36afa9c22bf155b38b5da",
    "capacity-independent-results01.json": "2aa98dff2474c38d7b0ed674999df7be1886437a65c2294ee6e3a23d7394b165",
    "capacity-root.json": "476051df3c2c58689b8dccc20a8a6a6f3ba9d246cca1445ca1d0a40596eebcf4",
    "root-results01.json": "02fe6a43dab1f66d4994c855ae69d3620748aeff15fd1e8a8dbff00675246a6b",
    "root-results02.json": "02fe6a43dab1f66d4994c855ae69d3620748aeff15fd1e8a8dbff00675246a6b",
    "calc_capacity.py": "e4a3cb1a1cbdc4d26b3ae33f58e677cc8c45b0f6b439e484950f07251277ade2",
    **{k: v for k, v in independent.PINS.items() if k != "capacity-independent.json"},
}


class Checks:
    def __init__(self):
        self.equalities = 0
        self.rational_checks = 0
        self.decimal_checks = 0
        self.max_decimal_error = F(0)
        self.failures = []

    def equal(self, label, a, b):
        self.equalities += 1
        if a != b:
            self.failures.append({"label": label, "actual": a, "expected": b})

    def rational(self, label, root_value, value):
        self.rational_checks += 1
        actual = F(root_value["fraction"])
        if actual != value:
            self.failures.append({"label": label, "actual": str(actual), "expected": str(value)})
        # The fixed16-decimal rendering is separate from the exact comparison.
        displayed = F(root_value["decimal_16dp"])
        error = abs(displayed - value)
        self.decimal_checks += 1
        self.max_decimal_error = max(self.max_decimal_error, error)
        if error > F(1, 2 * 10 ** 16):
            self.failures.append({"label": label + ".decimal16", "error": str(error)})


def compare(source, own_receipt, root_source, root):
    c = Checks()
    own_result = independent.calculate(source)
    c.equal("independent result reproducible", own_result, own_receipt["result"])
    c.equal("table coverage", list(root_source["tables"]), [t["table"] for t in source["tables"]])
    c.equal("root result table coverage", list(root["tables"]), [t["table"] for t in source["tables"]])
    c.equal("source pdf pin", root_source["source"]["sha256"], independent.PDF_PIN)
    c.equal("source physical pages", root_source["source"]["physical_pages"], [536, 537, 538])
    c.equal("source printed pages", root_source["source"]["printed_pages"], [470, 471, 472])
    c.equal("root code pin", root["code_sha256"], EXPECTED["calc_capacity.py"])
    c.equal("root source pin", root["pins"]["source"], independent.PDF_PIN)
    c.equal("root transcription pin", root["pins"]["transcription"], EXPECTED["capacity-root.json"])
    c.equal("root protocol pin", root["pins"]["protocol"], EXPECTED["ARITHMETIC-PROTOCOL.md"])
    c.equal("root controls count as recorded", root["controls_passed"], 14)
    aliases = []
    schema_aliases = {
        "11-2": {"South Tenant Floor": "South Tenant", "East Tenant Floor": "East Tenant", "North Tenant Floor": "North Tenant", "West Tenant Floor": "West Tenant"},
        "11-3": {"South Floor": "South Core", "North Floor": "North Core"},
        "11-4": {"South Floor": "South Floor Beams", "North Floor": "North Floor Beams", "South Girders": "South Girders", "Middle Girders": "Middle Girders", "North Girders": "North Girders"},
    }
    for table, own_table in zip(source["tables"], own_result["tables"]):
        name = table["table"]
        rs = root_source["tables"][name]
        rr = root["tables"][name]
        c.equal(name + ".source row count", len(rs["rows"]), len(table["rows"]))
        c.equal(name + ".result row count", len(rr["rows"]), len(table["rows"]))
        c.equal(name + ".count", rr["count"], own_table["row_count"])
        c.equal(name + ".direct outside", rr["direct_outside_rows"], own_table["point_outside_printed_box_rows"])
        c.equal(name + ".rounding incompatible", rr["rounding_disjoint_rows"], own_table["rounding_incompatible_rows"])
        c.equal(name + ".rounding endpoints", rr["rounding_endpoint_only_rows"], own_table["rounding_endpoint_only_rows"])
        for src, result, root_src, root_row in zip(table["rows"], own_table["rows"], rs["rows"], rr["rows"]):
            label = name + "." + str(src["row"])
            expected_region = schema_aliases[name][src["region"]]
            expected_row = [src["row"], src["physical_page"], expected_region, src["member"].replace("X", "x"), src["connection"], src["failure_load_kip"], src["design_shear_load_kip"], src["printed_ratio"]]
            c.equal(label + ".source fields", root_src, expected_row)
            if src["member"] != expected_row[3] or src["region"] != expected_region:
                aliases.append({"table": name, "row": src["row"], "source_region": src["region"], "root_region_alias": expected_region,
                                "source_member": src["member"], "root_member_alias": expected_row[3],
                                "incorrect_beams_addition": name == "11-4" and src["row"] <= 4})
            for key, value in [("row", src["row"]), ("pdf_page", src["physical_page"]), ("connection", src["connection"]), ("member", expected_row[3]), ("location_alias", expected_region),
                               ("displayed", expected_row[5:]), ("display_half_units", [str(F(1, 2 * 10 ** p)) for p in src["decimal_places"]])]:
                c.equal(label + ".result." + key, root_row[key], value)
            c.rational(label + ".quotient", root_row["quotient"], F(result["point_quotient"]["fraction"]))
            c.rational(label + ".difference_sign_reversal", root_row["quotient_minus_printed"], -F(result["printed_minus_point"]["fraction"]))
            for root_key, own_key in [("input_rounding_quotient_interval", "possible_quotient_box"), ("printed_ratio_interval", "printed_ratio_box")]:
                c.equal(label + ".interval length", len(root_row[root_key]), 2)
                for index in range(2):
                    c.rational(label + "." + root_key + "." + str(index), root_row[root_key][index], F(result[own_key][index]["fraction"]))
            possibility = root_row["rounding_possibility"]
            c.equal(label + ".point interval disposition", root_row["exact_quotient_within_printed_ratio_interval"], result["point_inside_closed_printed_box"])
            c.equal(label + ".rounding compatible", possibility["possible"], result["rounding_compatible"])
            c.equal(label + ".rounding endpoint only", possibility["endpoint_only"], result["rounding_endpoint_only"])
            for root_key, index in [("intersection_low", 0), ("intersection_high", 1)]:
                if result["rounding_intersection"] is None:
                    c.equal(label + "." + root_key, possibility[root_key], None)
                else:
                    c.rational(label + "." + root_key, possibility[root_key], F(result["rounding_intersection"][index]["fraction"]))
        for rk, ik in [("mean", "average"), ("minimum", "minimum"), ("maximum", "maximum")]:
            c.equal(name + ".source summary." + rk, rs["printed_summary"][rk], table["printed_summary"][ik])
            c.equal(name + ".result source summary." + rk, rr["source_summary"][rk], table["printed_summary"][ik])
            for rt, it in [("printed_ratios", "displayed_row_ratios"), ("quotients", "quotients_from_displayed_loads")]:
                own_stat = own_table["unweighted_summary"][it][ik]
                root_stat = rr["summary"][rt][rk]
                c.rational(name + "." + rt + "." + rk, root_stat, F(own_stat["value"]["fraction"]))
                c.equal(name + ".summary interval disposition", root_stat["within_printed_summary_rounding_interval"], own_stat["inside_closed_printed_box"])
    c.equal("formula count", len(root["formulas"]), len(own_result["source_arithmetic"]))
    expressions = ["60/0.8", "75/0.8", "0.601*75", "0.68*1*1*0.44*65", "(21.5+17.2)/2"]
    for own, root_formula, expression in zip(own_result["source_arithmetic"], root["formulas"], expressions):
        label = own["id"]
        c.equal(label + ".expression", root_formula["expression"], expression)
        c.equal(label + ".page", root_formula["pdf_page"], own["physical_page"])
        c.equal(label + ".units", root_formula["units"], own["unit"])
        c.equal(label + ".printed", root_formula["source_printed"], own["printed_result"])
        value = F(own["computed"]["fraction"])
        c.rational(label + ".value", root_formula["value"], value)
        c.rational(label + ".difference", root_formula["difference_from_printed"], -F(own["printed_minus_computed"]["fraction"]))
        box = independent.rounding_box(own["printed_result"])
        c.equal(label + ".printed interval disposition", root_formula["within_printed_rounding_interval"], box[0] <= value <= box[1])
    return {"status": "PASS" if not c.failures else "FAIL", "exact_rational_checks": c.rational_checks,
            "metadata_value_and_disposition_equality_checks": c.equalities,
            "fixed16_decimal_checks": c.decimal_checks, "fixed16_decimal_tolerance": "1/20000000000000000",
            "max_fixed16_decimal_error": independent.q(c.max_decimal_error),
            "exact_rational_disagreements": len([f for f in c.failures if "decimal16" not in f["label"]]),
            "failures": c.failures, "normalization_records": aliases,
            "coverage": {"source_rows":55,"displayed_load_and_ratio_values":165,"printed_summary_values":9,"summary_calculations":18,"formulas":5},
            "source_label_limitation": "Four root rows in Table11-4 add Beams to the printed South/North Floor subgroup labels; not supported by source. The table title says core floor girders. Numeric and row membership matches are separate from this labeling error.",
            "not_compared": ["Failure-mode labels appear only in independent source transcription, not root schema.",
                             "Root14 synthetic groups are count-pinned here, not independently executed or examined by this adapter.",
                             "No upstream specimen data, model run, connection calibration, or physical validation is reproduced."]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    if Path(args.output).name != args.output or not args.output.endswith(".json"):
        ap.error("output must be a JSON basename")
    output = BASE / args.output
    if output.exists():
        ap.error("refusing existing output")
    before = {name: independent.digest(BASE / name) for name in EXPECTED}
    before["comparison_code"] = independent.digest(Path(__file__))
    before["source_pdf"] = independent.digest(independent.PDF)
    for name, expected in EXPECTED.items():
        if before[name] != expected:
            raise AssertionError("input pin changed: " + name)
    if before["source_pdf"] != independent.PDF_PIN:
        raise AssertionError("PDF pin changed")
    def read(name):
        return json.loads((BASE / name).read_text())
    result = compare(read("capacity-independent.json"), read("capacity-independent-results01.json"), read("capacity-root.json"), read("root-results01.json"))
    test_receipts = independent.controls()
    after = {name: independent.digest(BASE / name) for name in EXPECTED}
    after["comparison_code"] = independent.digest(Path(__file__))
    after["source_pdf"] = independent.digest(independent.PDF)
    if before != after:
        raise AssertionError("input changed during comparison")
    receipt = {"status": result["status"], "command": [sys.executable, *sys.argv], "python":sys.version,
               "post_schema_adapter":True, "pins_before":before, "pins_after":after,
               "independent_arithmetic_controls":test_receipts, "comparison":result}
    with output.open("x", encoding="utf-8") as f:
        json.dump(receipt, f, sort_keys=True, indent=2)
        f.write("\n")
    print(json.dumps({"status":result["status"], "rational_checks":result["exact_rational_checks"],
                      "equality_checks":result["metadata_value_and_disposition_equality_checks"],
                      "failures":len(result["failures"]),"sha256":independent.digest(output)}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
