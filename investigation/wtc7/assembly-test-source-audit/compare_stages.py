#!/usr/bin/env python3
"""Post-freeze comparison of independently computed native-unit stage summaries."""
import argparse
from decimal import Decimal
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys
import verify_stages as independent

BASE=Path(__file__).resolve().parent
DECIMAL_TOLERANCE=F(1,10**30)
PINS={
    **independent.PINS,
    "verify_stages.py":"56a2b2b0552cd447c2658e6cdbb9638d008d0085445d704dd2fb4c8966c1650f",
    "independent-stage-results01.json":"63f51024d9571d769256b567b774d8e4ee887d8020d249a72b956c377a568bbd",
    "thompson-stages-root.json":"3265861472770daee4fe35df339d91a419c175a9bb793c73f225a5cd3adb07ac",
    "calc_stages.py":"50faa90dfa33c74fb7de95415fd15dcd3995702769e44d6bf967ca3aaea4719f",
    "calc_assembly.py":"d4ab1e687c201da7004c14314d060d0b4add6be63319b2a8e75c675a226e4e5b",
    "root-stage-results01.json":"aa3c5b87b1794a427d65f0ed511e35c1dcac9a5b926b8f8128f58179c18262df",
    "root-stage-results02.json":"aa3c5b87b1794a427d65f0ed511e35c1dcac9a5b926b8f8128f58179c18262df",
}


class Checks:
    def __init__(self):
        self.equalities=0
        self.rationals=0
        self.sse_checks=0
        self.sd_cov_checks=0
        self.rational_render_checks=0
        self.max_sd_cov_error=F(0)
        self.max_render_error=F(0)
        self.failures=[]

    def equal(self,label,got,want):
        self.equalities+=1
        if got!=want:
            self.failures.append({"label":label,"got":got,"expected":want})

    def exact(self,label,root,want):
        self.rationals+=1
        value=F(root["fraction"])
        if value!=want:
            self.failures.append({"label":label,"got":str(value),"expected":str(want)})
        printed=Decimal(root["decimal"])
        error=abs(F(printed)-want)
        self.rational_render_checks+=1
        self.max_render_error=max(self.max_render_error,error)
        if error>F(10)**printed.as_tuple().exponent/2:
            self.failures.append({"label":label+".render","error":str(error)})

    def sse(self,label,variance,denominator,want):
        self.sse_checks+=1
        got=variance*denominator
        if got!=want:
            self.failures.append({"label":label,"got":str(got),"expected":str(want)})

    def close(self,label,root,own):
        error=abs(F(root)-F(own))
        self.sd_cov_checks+=1
        self.max_sd_cov_error=max(self.max_sd_cov_error,error)
        if error>DECIMAL_TOLERANCE:
            self.failures.append({"label":label,"absolute_error":str(error),"tolerance":str(DECIMAL_TOLERANCE)})


def compare(own,root,c):
    cohorts={"all_reported_tests":"all_reported",
             "TN_figure_subset_without_5ST1":"figure_subset_without_5ST1"}
    c.equal("scenario count",len(root["groups"]),12)
    keys=[(g["cohort"],g["bolts"],g["rule"]) for g in root["groups"]]
    wants=[(cohorts[g["cohort"]],g["bolts"],g["rule"]) for g in own["scenarios"]]
    c.equal("complete scenario identities",keys,wants)
    selected_count=0
    for actual,expected in zip(root["groups"],own["scenarios"]):
        label=".".join(map(str,(actual["cohort"],actual["bolts"],actual["rule"])))
        c.equal(label+".selected_count",len(actual["selected"]),expected["n"])
        for selected,want in zip(actual["selected"],expected["selected"]):
            selected_count+=1
            for key in ("test","stage","shear","rotation","secondary_available"):
                c.equal(label+"."+want["test"]+"."+key,selected[key],want[key])
            c.equal(label+"."+want["test"]+".secondary_reason",selected["secondary_footnote"],want["secondary_missing_footnote"])
        for root_quantity,own_quantity in (("shear_kip","applied_shear_kip"),("rotation_rad","beam_end_rotation_rad")):
            a=actual[root_quantity]
            e=expected["statistics"][own_quantity]
            qlabel=label+"."+root_quantity
            c.equal(qlabel+".n",a["n"],e["n"])
            c.exact(qlabel+".mean",a["mean"],F(e["mean"]["fraction"]))
            for convention in ("sample","population"):
                c.exact(qlabel+"."+convention+".variance",a[convention]["variance"],F(e[convention]["variance"]["fraction"]))
                c.close(qlabel+"."+convention+".sd",a[convention]["sd"],e[convention]["sd_decimal"])
                c.close(qlabel+"."+convention+".cov_percent",a[convention]["cov_percent"],e[convention]["cov_percent_decimal"])
                # Root does not retain SSE; this is explicitly an implied-SSE
                # cross-check, not a claim that its source output supplied SSE.
                c.sse(qlabel+"."+convention+".implied_SSE",F(a[convention]["variance"]["fraction"]),e[convention]["denominator"],F(e["sum_squared_deviations"]["fraction"]))
    c.equal("contrast record count",len(root["contrasts"]),9)
    populated=0
    for actual,expected in zip(root["contrasts"],own["secondary_contrasts"]):
        c.equal("contrast.test",actual["test"],expected["test"])
        if not expected["secondary_available"]:
            c.equal(actual["test"]+".null_contrast",actual["secondary_minus_initial"],None)
            c.equal(actual["test"]+".missing_reason",actual["secondary_footnote"],expected["secondary_missing_footnote"])
        else:
            populated+=1
            for root_key,own_key in (("shear_kip","shear_difference_kip"),
                                     ("shear_percent_of_initial","shear_percent_change_from_initial"),
                                     ("rotation_rad","rotation_difference_rad")):
                c.exact(actual["test"]+"."+root_key,actual["secondary_minus_initial"][root_key],F(expected["secondary_minus_initial"][own_key]["fraction"]))
    return {"scenarios":12,"quantity_summaries":24,"selected_row_instances":selected_count,
            "contrast_records":9,"populated_contrasts":populated,"missing_contrasts":9-populated}


def controls_review(root):
    spec=importlib.util.spec_from_file_location("reviewed_root_stage_controls",BASE/"calc_stages.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results=module.controls()
    if results!=root["controls"] or not all(results.values()):
        raise AssertionError("root stage controls differ or fail")
    return {"count":len(results),"executed":results,"recorded_result_matches":True,
            "coverage":"Tests exercise production select() for initial,secondary,tie,missing,associated-rotation and invalid-rule choices; production stats() for mean,sample/population variance,SD,COV,constant/exact-decimal inputs and singleton/zero-mean/empty rejection.",
            "limit":"Root contrasts are inline in main() and lack a separate root synthetic contrast fixture. All four populated real contrasts and all five null records are independently compared here; the independent implementation also has a synthetic signed contrast fixture. These checks do not validate physical measurements or identify NIST test membership."}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    if Path(args.output).name!=args.output or not args.output.endswith(".json"):
        ap.error("JSON basename required")
    output=BASE/args.output
    if output.exists():
        ap.error("refusing existing output")
    paths={name:BASE/name for name in PINS}
    paths.update({"source_pdf":independent.SOURCE,"comparison_code":Path(__file__)})
    before={name:independent.sha(path) for name,path in paths.items()}
    for name,pin in PINS.items():
        if before[name]!=pin:
            raise AssertionError("frozen input changed: "+name)
    if before["source_pdf"]!=independent.SOURCE_PIN:
        raise AssertionError("original PDF pin changed")
    def read(name):
        return json.loads((BASE/name).read_text())
    own_receipt=read("independent-stage-results01.json")
    own=independent.calculate(read("thompson-independent.json"))
    root=read("root-stage-results01.json")
    c=Checks()
    c.equal("independent recalculation",own,own_receipt["result"])
    for key,want in (("input",PINS["thompson-stages-root.json"]),("source",independent.SOURCE_PIN),
                     ("protocol",PINS["STAGE-DIAGNOSTIC-PROTOCOL.md"]),("code",PINS["calc_stages.py"]),("helper",PINS["calc_assembly.py"])):
        c.equal("root receipt pin."+key,root["pins"][key],want)
    coverage=compare(own,root,c)
    own_controls=independent.controls()
    root_controls=controls_review(root)
    after={name:independent.sha(path) for name,path in paths.items()}
    if before!=after:
        raise AssertionError("input changed during comparison")
    status="PASS" if not c.failures else "FAIL"
    result={"status":status,"coverage":coverage,"exact_rational_comparisons":c.rationals,
            "implied_SSE_crosschecks":c.sse_checks,"sd_cov_comparisons":c.sd_cov_checks,
            "rational_decimal_render_checks":c.rational_render_checks,"metadata_equalities":c.equalities,
            "prospective_sd_cov_absolute_tolerance":str(DECIMAL_TOLERANCE),
            "max_sd_cov_absolute_error":independent.rational(c.max_sd_cov_error),
            "max_rational_decimal_render_error":independent.rational(c.max_render_error),
            "failures":c.failures,
            "schema_mapping":"Two declared cohort-name aliases; root secondary_footnote maps to independent secondary_missing_footnote. Quantity aliases shear_kip/rotation_rad map to source applied_shear_kip/beam_end_rotation_rad. No value,unit or angle conversion.",
            "limitations":"Repeated selected-row instances are not additional experiments. Root omits retained source locators/specimen/failure details in group selections; those common original source fields were separately validated in tn1749-comparison01. No root SSE field exists; implied-SSE checks are derived consistency checks."}
    receipt={"status":status,"post_freeze_schema_adapter":True,"command":[sys.executable,*sys.argv],
             "python":sys.version,"pins_before":before,"pins_after":after,
             "independent_controls":own_controls,"root_controls_review":root_controls,"comparison":result}
    with output.open("x",encoding="utf-8") as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({"status":status,"exact_rationals":c.rationals,"sd_cov":c.sd_cov_checks,
                      "equalities":c.equalities,"failures":len(c.failures),"sha256":independent.sha(output)}))
    return 0 if status=="PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
