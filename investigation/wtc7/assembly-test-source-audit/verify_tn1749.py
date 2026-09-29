#!/usr/bin/env python3
"""Independent, exact TN1749 displayed-table percent and rounding audit."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "connection-calibration-audit/retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf"
SOURCE_PIN = "5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf"
TRANSCRIPTION_PIN = "638b66018eb46fc2ed1ea07949b053a68964ce29a6a1fbc07b696b3267a05dbe"


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def digits(s):
    if not isinstance(s, str) or not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s):
        raise ValueError("unsupported displayed number")
    return len(s.partition(".")[2])


def box(s):
    half = F(1, 2 * 10 ** digits(s))
    return F(s) - half, F(s) + half


def percent(model, mean):
    if model <= 0 or mean <= 0:
        raise ValueError("positive model and mean required")
    return 100 * (model / mean - 1)


def percent_range(model_box, mean_box):
    if model_box[0] <= 0 or mean_box[0] <= 0:
        raise ValueError("positive complete input intervals required")
    if model_box[0] > model_box[1] or mean_box[0] > mean_box[1]:
        raise ValueError("reversed interval")
    return percent(model_box[0], mean_box[1]), percent(model_box[1], mean_box[0])


def overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    return None if lo > hi else (lo, hi)


def rational(value):
    return {"fraction":str(value), "decimal_approx":float(value)}


def interval(value):
    return None if value is None else [rational(x) for x in value]


def controls():
    records = []
    def check(name, predicate, fixture):
        if not predicate:
            raise AssertionError(name)
        records.append({"name":name, "status":"PASS", "fixture":fixture})
    check("positive_signed_error", percent(F(11), F(10)) == 10, "model11 mean10 -> +10 percent")
    check("negative_signed_error", percent(F(9), F(10)) == -10, "model9 mean10 -> -10 percent")
    check("zero_error", percent(F(7), F(7)) == 0, "model7 mean7 ->0")
    check("signed_precision", digits("+1.8") == 1 and digits("-14.6") == 1 and digits("0.120") == 3,
          "Signed percent lexemes, trailing zero precision")
    model, mean = (F(9), F(11)), (F(19), F(21))
    vertices = [percent(a,b) for a in model for b in mean]
    check("interval_vertex_extrema", percent_range(model,mean) == (min(vertices),max(vertices)),
          "All4 vertices of model[9,11], mean[19,21]")
    check("rounding_only_overlap", not(box("10.1")[0] <= percent(F("11.0"), F("10.0")) <= box("10.1")[1]) and overlap(percent_range(box("11.0"),box("10.0")),box("10.1")) is not None,
          "Point10percent misses10.1+-0.05; input11.0/10.0 boxes allow overlap")
    check("genuine_nonoverlap", overlap(percent_range(box("11.0"),box("10.0")),box("50.0")) is None,
          "Same input boxes cannot reach50percent")
    check("endpoint_tie", overlap((F(-1),F(0)), (F(0),F(1))) == (F(0),F(0)),
          "Intervals[-1,0] and[0,1] retain endpoint-only intersection")
    caught = 0
    for operation in [lambda: percent(F(1),F(0)), lambda: percent_range((F(1),F(2)),(F(0),F(1))), lambda: percent_range((F(2),F(1)),(F(1),F(2)))]:
        try:
            operation()
        except ValueError:
            caught += 1
    check("invalid_interval_rejection",caught == 3,"Zero denominator,zero-crossing mean interval,reversed model interval")
    return records


def calculate(data):
    if [(t["table"],len(t["rows"])) for t in data["tables"]] != [("3-3",3),("3-4",3)]:
        raise AssertionError("table coverage")
    rows = []
    for table in data["tables"]:
        if [r["connection_bolts"] for r in table["rows"]] != [3,4,5]:
            raise AssertionError("connection-size coverage")
        for row in table["rows"]:
            mean = row["experiment"]["mean"]
            if digits(mean) != table["value_decimal_places"] or digits(row["experiment"]["cov_percent"]) != 1:
                raise AssertionError("source precision")
            for model in ("detailed","reduced"):
                value = row[model]["value"]
                printed = row[model]["deviation_percent"]
                if digits(value) != table["value_decimal_places"] or digits(printed) != 1:
                    raise AssertionError("model precision")
                point = percent(F(value),F(mean))
                possible = percent_range(box(value),box(mean))
                printed_box = box(printed)
                shared = overlap(possible,printed_box)
                rows.append({
                    "table":table["table"], "source_physical_page":table["physical_page"],
                    "source_printed_page":table["printed_page"], "row":row["row"],
                    "connection_bolts":row["connection_bolts"], "model":model, "unit":table["unit"],
                    "displayed_model":value,"displayed_experiment_mean":mean,"displayed_deviation_percent":printed,
                    "displayed_cov_percent":row["experiment"]["cov_percent"],
                    "model_decimal_places":digits(value),"mean_decimal_places":digits(mean),
                    "computed_deviation_percent":rational(point),
                    "computed_minus_printed_percentage_points":rational(point-F(printed)),
                    "model_box":interval(box(value)), "mean_box":interval(box(mean)),
                    "possible_deviation_percent":interval(possible), "printed_deviation_percent_box":interval(printed_box),
                    "point_inside_printed_box":printed_box[0] <= point <= printed_box[1],
                    "point_on_printed_endpoint":point in printed_box,
                    "rounding_intersection":interval(shared), "rounding_compatible":shared is not None,
                    "rounding_endpoint_only":shared is not None and shared[0] == shared[1],
                })
    return {"rows":rows, "comparison_count":len(rows),
            "point_outside_count":sum(not r["point_inside_printed_box"] for r in rows),
            "rounding_incompatible_count":sum(not r["rounding_compatible"] for r in rows),
            "rounding_endpoint_only_count":sum(r["rounding_endpoint_only"] for r in rows),
            "mean_cov_status":"Not recomputed from TN1749 summaries; individual original observations are required. Conducted/figure/table counts remain distinct.",
            "interpretation":"Exact displayed arithmetic and conditional rounding feasibility only. No observed physical error bars, confidence intervals, sample-size inference or model validation."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    if Path(args.output).name != args.output or not args.output.endswith(".json"):
        parser.error("JSON output basename required")
    output=BASE/args.output
    if output.exists():
        parser.error("refusing existing output")
    paths={"source_pdf":SOURCE,"transcription":BASE/"tn1749-independent.json",
           "unit_protocol":BASE/"PROTOCOL.md","arithmetic_protocol":BASE/"ARITHMETIC-PROTOCOL.md",
           "code":Path(__file__)}
    before={k:sha(v) for k,v in paths.items()}
    if before["source_pdf"] != SOURCE_PIN or before["transcription"] != TRANSCRIPTION_PIN:
        raise AssertionError("frozen source changed")
    control_receipts=controls()
    result=calculate(json.loads(paths["transcription"].read_text()))
    after={k:sha(v) for k,v in paths.items()}
    if before != after:
        raise AssertionError("inputs changed during run")
    receipt={"status":"PASS","command":[sys.executable,*sys.argv],"python":sys.version,
             "pins_before":before,"pins_after":after,"controls":control_receipts,"result":result}
    with output.open("x",encoding="utf-8") as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({"status":"PASS","comparisons":result["comparison_count"],
                      "point_outside":result["point_outside_count"],
                      "rounding_incompatible":result["rounding_incompatible_count"],
                      "controls":len(control_receipts),"sha256":sha(output)}))


if __name__ == "__main__":
    main()
