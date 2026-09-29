#!/usr/bin/env python3
"""Post-freeze TN1749 and original-stage source comparison, not stage statistics.

Independent arithmetic comes only from the separately frozen verify_tn1749
implementation. Reviewed root code is imported solely to execute/audit its
synthetic controls; its calculate function supplies no comparison truth.
"""
import argparse
from decimal import Decimal
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys

import verify_tn1749 as independent

BASE = Path(__file__).resolve().parent
PINS = {
    "tn1749-independent.json":"638b66018eb46fc2ed1ea07949b053a68964ce29a6a1fbc07b696b3267a05dbe",
    "thompson-independent.json":"7f1ff93025f499e62498a5ec2c21700c0a2b3d58213cb72363dd7757b2c153b9",
    "verify_tn1749.py":"f6955dcda59cb1bb09b911c8aa90f3579ffd41619c79a81faac1ee25d3d1c24f",
    "tn1749-independent-results01.json":"18970dbeff47ea2fe562fc8765997bb63544f45130c57ad4a71ec800a1e8010b",
    "tn1749-root.json":"2a9ed1412e592f053c4f75c6fdc001858afb55557d69d3720f04ed1bbf0d4aca",
    "thompson-stages-root.json":"3265861472770daee4fe35df339d91a419c175a9bb793c73f225a5cd3adb07ac",
    "calc_assembly.py":"d4ab1e687c201da7004c14314d060d0b4add6be63319b2a8e75c675a226e4e5b",
    "root-results01.json":"57c68de1adc72eba267b6138338d1113963de90c4ecb967ac12ebe486526cb9f",
    "PROTOCOL.md":"a06f1bc8f7e4283dbca0c9f54337eba0123045538ca47b411eb3aa8c260d637d",
    "ARITHMETIC-PROTOCOL.md":"88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e",
}
ORIGINAL = BASE / "sources/MSST_Thompson_2009-sirsi.pdf"
ORIGINAL_PIN = "b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78"


class Audit:
    def __init__(self):
        self.equalities = 0
        self.rationals = 0
        self.decimals = 0
        self.max_decimal_error = F(0)
        self.numeric_disagreements = 0
        self.failures = []
        self.normalizations = []

    def same(self, where, got, expected):
        self.equalities += 1
        if got != expected:
            self.failures.append({"where":where,"got":got,"expected":expected})

    def numeric_lexeme(self, where, got, expected):
        # Only optional leading plus is normalized. Minus and trailing zero
        # changes are never erased. The source's explicit plus remains saved.
        self.same(where, got.removeprefix("+"), expected.removeprefix("+"))
        self.same(where+".precision", independent.digits(got), independent.digits(expected))
        if got != expected:
            self.normalizations.append({"where":where,"root":got,"independent_source":expected,
                                        "recipe":"optional leading plus only"})

    def exact(self, where, root, expected):
        self.rationals += 1
        value = F(root["fraction"])
        if value != expected:
            self.numeric_disagreements += 1
            self.failures.append({"where":where,"got":str(value),"expected":str(expected)})
        displayed = Decimal(root["decimal"])
        error = abs(F(displayed)-expected)
        unit = F(10) ** displayed.as_tuple().exponent
        self.max_decimal_error = max(self.max_decimal_error,error)
        self.decimals += 1
        if error > unit/2:
            self.failures.append({"where":where+".decimal","error":str(error),"half_last_place":str(unit/2)})


def compare_tn(source, result, own_result, root_source, audit):
    tables = source["tables"]
    original_rows = [(table,row) for table in tables for row in table["rows"]]
    audit.same("TN source count",len(root_source["rows"]),len(original_rows))
    audit.same("TN PDF pin",root_source["source_sha256"],independent.SOURCE_PIN)
    audit.same("TN physical page",root_source["physical_page"],46)
    audit.same("TN printed page",root_source["printed_page"],28)
    audit.same("root result input pin",result["pins"]["input"],PINS["tn1749-root.json"])
    audit.same("root result source pin",result["pins"]["source"],independent.SOURCE_PIN)
    audit.same("root result protocol pin",result["pins"]["protocol"],PINS["ARITHMETIC-PROTOCOL.md"])
    audit.same("root result code pin",result["pins"]["code"],PINS["calc_assembly.py"])
    for root,(table,row) in zip(root_source["rows"],original_rows):
        tag=table["table"]+"."+str(row["connection_bolts"])
        for key,want in [("table",table["table"]),("bolts",row["connection_bolts"]),("unit",table["unit"]),
                         ("n",row["experiment"]["sample_n_stated_in_table"]),
                         ("quantity","ultimate_vertical_load" if table["table"]=="3-3" else "rotation_at_ultimate_load")]:
            audit.same(tag+"."+key,root[key],want)
        audit.numeric_lexeme(tag+".mean",root["mean"],row["experiment"]["mean"])
        audit.numeric_lexeme(tag+".cov",root["cov"],row["experiment"]["cov_percent"])
        for model in ("detailed","reduced"):
            audit.numeric_lexeme(tag+"."+model+".value",root[model]["value"],row[model]["value"])
            audit.numeric_lexeme(tag+"."+model+".deviation",root[model]["deviation"],row[model]["deviation_percent"])
    audit.same("TN comparison count",len(result["comparisons"]),12)
    for root,own in zip(result["comparisons"],own_result["rows"]):
        tag=own["table"]+"."+str(own["connection_bolts"])+"."+own["model"]
        for key,want in [("table",own["table"]),("bolts",own["connection_bolts"]),("model",own["model"]),("unit",own["unit"]),("n",None)]:
            audit.same(tag+"."+key,root[key],want)
        for key,own_key in [("mean","displayed_experiment_mean"),("value","displayed_model"),
                            ("cov","displayed_cov_percent"),("printed_deviation","displayed_deviation_percent")]:
            audit.numeric_lexeme(tag+"."+key,root[key],own[own_key])
        for root_key,own_key in [("point_percent","computed_deviation_percent"),("point_minus_printed_pp","computed_minus_printed_percentage_points")]:
            audit.exact(tag+"."+root_key,root[root_key],F(own[own_key]["fraction"]))
        for root_key,own_key in [("computed_interval","possible_deviation_percent"),("printed_interval","printed_deviation_percent_box"),("intersection","rounding_intersection")]:
            if own[own_key] is None:
                audit.same(tag+"."+root_key,root[root_key],None)
            else:
                audit.same(tag+"."+root_key+".length",len(root[root_key]),2)
                for index in (0,1):
                    audit.exact(tag+"."+root_key+"."+str(index),root[root_key][index],F(own[own_key][index]["fraction"]))
        expected_relation = "disjoint" if not own["rounding_compatible"] else "endpoint_only" if own["rounding_endpoint_only"] else "overlap"
        audit.same(tag+".relation",root["relation"],expected_relation)
        audit.same(tag+".point_disposition",root["point_within_printed_interval"],own["point_inside_printed_box"])


def compare_stages(source,root,audit):
    tables={t["table"]:t for t in source["tables"]}
    initial=tables["4.2"]
    secondary=tables["4.3"]
    initial_rows=[dict(zip(initial["columns"],r)) for r in initial["rows"]]
    secondary_rows=[dict(zip(secondary["columns"],r)) for r in secondary["rows"]]
    audit.same("original source pin",root["source_sha256"],ORIGINAL_PIN)
    audit.same("original page coverage",root["physical_and_printed_pages"],[104,105])
    audit.same("original source table locators",[(initial["physical_page"],initial["printed_page"]),(secondary["physical_page"],secondary["printed_page"])],[(104,104),(105,105)])
    audit.same("original root test coverage",[r["test"] for r in root["records"]],[r["test"] for r in initial_rows])
    audit.same("original secondary test coverage",[r["test"] for r in secondary_rows],[r["test"] for r in initial_rows])
    filled=missing=numeric_values=0
    for result,first,second in zip(root["records"],initial_rows,secondary_rows):
        for stage,record in (("initial",first),("secondary",second)):
            tag=record["test"]+"."+stage
            node=result[stage]
            if record["controlling_specimen"] is None:
                missing+=1
                audit.same(tag+".null",node,None)
                for key in ("applied_shear_kip","measured_moment_kip_in","measured_axial_kip","beam_end_rotation_rad","failure_mechanism"):
                    audit.same(tag+".source_null."+key,record[key],None)
            else:
                filled+=1
                for key,field in (("specimen","controlling_specimen"),("failure","failure_mechanism")):
                    audit.same(tag+"."+key,node[key],record[field])
                for key,field in (("shear","applied_shear_kip"),("rotation","beam_end_rotation_rad")):
                    audit.numeric_lexeme(tag+"."+key,node[key],record[field])
                    numeric_values+=1
            if stage=="initial":
                audit.same(tag+".footnote",node["footnote"],record["footnote"])
            else:
                audit.same(tag+".footnote",result["secondary_footnote"],record["footnote"])
    return {"test_ids":9,"stage_slots":18,"populated_stages":filled,"null_stages":missing,
            "compared_shear_rotation_values":numeric_values,
            "not_compared":["Original Table4.1 and4.4 values are independently transcribed but absent from root stage schema.",
                            "Original stage moment and axial-force fields are retained only in independent source JSON.",
                            "Footnote codes and dispositions are matched; prose footnotes were manually reviewed for meaning, not claimed verbatim equality.",
                            "No stage selections, means, COVs, load conversions or rotation conversions are performed."]}


def root_control_review(root_result):
    # This reviewed, authored numeric module is loaded only after both
    # independent source and arithmetic freezes. Its main routine is not run.
    spec=importlib.util.spec_from_file_location("root_tn_controls_reviewed",BASE/"calc_assembly.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    checks=module.controls()
    if checks != root_result["controls"] or not all(checks.values()):
        raise AssertionError("root synthetic-control result mismatch")
    fixture=module.calculate("1.50","1.00","50.5")
    return {"reviewed_code_sha256":PINS["calc_assembly.py"],"executed_checks":checks,
            "count":len(checks),"recorded_result_exact_match":True,
            "so_named_endpoint_fixture_actual_production_relation":fixture["relation"],
            "endpoint_coverage_limit":"The endpoint_only assertion calls a separate local interval classifier, not calculate(). The calculate(1.50,1.00,50.5) fixture is asserted only to have point_percent50; its production relation is overlap, not endpoint_only. Production endpoint_only branch is therefore not established by this control suite.",
            "other_coverage":"Production calculate is exercised for overlap, disjointness, nonpositive denominator interval and negative model interval. Direct percent tests cover zero, positive/negative sign and denominator rejection; precision and Fraction serialization have separate controls.",
            "independent_control_limit":"The independent interval endpoint test also calls its overlap helper; actual TN rows provide no endpoint-only cases. Neither suite should be described as full production-branch coverage.",
            "protocol_range_limit":"Root permits a model-box lower endpoint exactly zero whereas the independent checker requires a wholly positive model box. The12 actual TN comparisons have positive lower bounds, so this admission difference does not affect the compared results.",
            "not_validation":"These are synthetic software checks, not specimen evidence or model-physics validation."}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    if Path(args.output).name != args.output or not args.output.endswith(".json"):
        ap.error("JSON basename required")
    output=BASE/args.output
    if output.exists():
        ap.error("refusing existing output")
    paths={name:BASE/name for name in PINS}
    paths.update({"tn_pdf":independent.SOURCE,"original_pdf":ORIGINAL,"comparison_code":Path(__file__)})
    before={name:independent.sha(path) for name,path in paths.items()}
    for name,pin in PINS.items():
        if before[name] != pin:
            raise AssertionError("frozen input pin changed: "+name)
    if before["tn_pdf"] != independent.SOURCE_PIN or before["original_pdf"] != ORIGINAL_PIN:
        raise AssertionError("source PDF pin changed")
    def read(name):
        return json.loads((BASE/name).read_text())
    source=read("tn1749-independent.json")
    own_receipt=read("tn1749-independent-results01.json")
    root_result=read("root-results01.json")
    audit=Audit()
    recalculated=independent.calculate(source)
    audit.same("independent calculation reproducible",recalculated,own_receipt["result"])
    compare_tn(source,root_result,recalculated,read("tn1749-root.json"),audit)
    stage_coverage=compare_stages(read("thompson-independent.json"),read("thompson-stages-root.json"),audit)
    independent_controls=independent.controls()
    control_review=root_control_review(root_result)
    after={name:independent.sha(path) for name,path in paths.items()}
    if before != after:
        raise AssertionError("input changed during comparison")
    status="PASS" if not audit.failures else "FAIL"
    result={"status":status,"tn_source_rows":6,"tn_printed_numeric_values":36,"tn_comparisons":12,
            "exact_rational_comparisons":audit.rationals,"decimal_render_checks":audit.decimals,
            "decimal_tolerance_rule":"Half of the last displayed place in each root40-significant-digit decimal rendering; rational comparison is exact.",
            "max_decimal_render_error":independent.rational(audit.max_decimal_error),
            "exact_numeric_disagreements":audit.numeric_disagreements,"equality_checks":audit.equalities,
            "normalizations":audit.normalizations,"stage_source_coverage":stage_coverage,
            "failures":audit.failures}
    receipt={"status":status,"post_freeze_schema_adapter":True,
             "command":[sys.executable,*sys.argv],"python":sys.version,
             "pins_before":before,"pins_after":after,
             "independent_synthetic_controls":independent_controls,
             "root_control_execution_and_review":control_review,"comparison":result}
    with output.open("x",encoding="utf-8") as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({"status":status,"exact_rationals":audit.rationals,"equalities":audit.equalities,
                      "numeric_disagreements":audit.numeric_disagreements,"failures":len(audit.failures),
                      "sha256":independent.sha(output)}))
    return 0 if status=="PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
