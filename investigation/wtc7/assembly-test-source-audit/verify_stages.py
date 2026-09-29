#!/usr/bin/env python3
"""Independent native-unit reported-failure-stage sensitivity.

No root stage implementation or result was read to implement this calculation.
Source transcription preceded systematic arithmetic; rough mental exploration
during source interpretation is acknowledged, not claimed as a blind design.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent
SOURCE=BASE/"sources/MSST_Thompson_2009-sirsi.pdf"
PINS={
    "thompson-independent.json":"7f1ff93025f499e62498a5ec2c21700c0a2b3d58213cb72363dd7757b2c153b9",
    "STAGE-DIAGNOSTIC-PROTOCOL.md":"7f1c6ddb2425891869c369e115c8f66eb77836cfdd2bcddbb034bc4ddfee46c4",
    "ARITHMETIC-PROTOCOL.md":"88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e",
    "PROTOCOL.md":"a06f1bc8f7e4283dbca0c9f54337eba0123045538ca47b411eb3aa8c260d637d",
}
SOURCE_PIN="b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78"
DECIMAL_PRECISION=80


def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def decimal(value):
    return Decimal(value.numerator)/Decimal(value.denominator)


def rational(value):
    with localcontext() as ctx:
        ctx.prec=DECIMAL_PRECISION
        return {"fraction":str(value),"decimal":str(decimal(value))}


def statistics(values):
    if len(values)<2:
        raise ValueError("at least two observations required for both variance conventions")
    n=len(values)
    mean=sum(values,F(0))/n
    if mean<=0:
        raise ValueError("positive mean required for these COV summaries")
    sse=sum(((x-mean)**2 for x in values),F(0))
    out={"n":n,"values":[str(x) for x in values],"mean":rational(mean),"sum_squared_deviations":rational(sse)}
    with localcontext() as ctx:
        ctx.prec=DECIMAL_PRECISION
        mean_dec=decimal(mean)
        for convention,denominator in (("sample",n-1),("population",n)):
            variance=sse/denominator
            sd=decimal(variance).sqrt()
            cov=100*sd/mean_dec
            out[convention]={"denominator":denominator,"variance":rational(variance),
                             "sd_decimal":str(sd),"cov_percent_decimal":str(cov)}
    return out


def choose(initial,secondary,rule):
    if rule=="initial":
        return "initial",initial
    if rule!="maximum_reported_stage":
        raise ValueError("unsupported stage rule")
    if secondary is not None and F(secondary["shear"])>F(initial["shear"]):
        return "secondary",secondary
    return "initial",initial


def contrast(initial,secondary):
    if secondary is None:
        return None
    first=F(initial["shear"])
    if first<=0:
        raise ValueError("positive initial shear required")
    ds=F(secondary["shear"])-first
    dr=F(secondary["rotation"])-F(initial["rotation"])
    return {"shear_difference_kip":rational(ds),
            "shear_percent_change_from_initial":rational(100*ds/first),
            "rotation_difference_rad":rational(dr)}


def controls():
    results=[]
    def check(name,condition,fixture):
        if not condition:
            raise AssertionError(name)
        results.append({"name":name,"status":"PASS","fixture":fixture})
    first={"shear":"2.00","rotation":"0.200"}
    bigger={"shear":"3.00","rotation":"0.100"}
    lesser={"shear":"1.00","rotation":"0.900"}
    tied={"shear":"2.00","rotation":"0.900"}
    check("initial_rule",choose(first,bigger,"initial")==("initial",first),
          "Initial2 retained despite secondary3")
    check("higher_secondary_associated_rotation",choose(first,bigger,"maximum_reported_stage")==("secondary",bigger),
          "Secondary3 selected with its smaller0.100 rotation, not independently maximized0.200")
    check("higher_initial_associated_rotation",choose(first,lesser,"maximum_reported_stage")==("initial",first),
          "Initial2 selected despite secondary's larger rotation0.900")
    check("exact_tie_initial",choose(first,tied,"maximum_reported_stage")==("initial",first),
          "Equal shears choose initial")
    check("missing_secondary",choose(first,None,"maximum_reported_stage")==("initial",first) and contrast(first,None) is None,
          "Missing secondary cannot become zero or an invented contrast")
    stat=statistics([F(1),F(2),F(3)])
    check("sample_population_variance",stat["mean"]["fraction"]=="2" and stat["sample"]["variance"]["fraction"]=="1" and stat["population"]["variance"]["fraction"]=="2/3",
          "Values1,2,3 have mean2,SSE2,sample variance1,population variance2/3")
    check("known_square_root_and_cov",stat["sample"]["sd_decimal"]=="1" and stat["sample"]["cov_percent_decimal"]=="50",
          "Sample SD1 and COV50percent for1,2,3")
    uniform=statistics([F(2),F(2)])
    check("zero_variation",uniform["sample"]["variance"]["fraction"]=="0" and Decimal(uniform["population"]["cov_percent_decimal"])==0,
          "Two equal positive observations retain zero variability")
    failures=0
    for vals in ([F(1)],[F(-1),F(1)]):
        try:
            statistics(vals)
        except ValueError:
            failures+=1
    check("singleton_zero_mean_rejections",failures==2,"Singleton and zero mean rejected, no fake sample SD or COV")
    delta=contrast(first,bigger)
    check("secondary_contrast_signs",delta["shear_difference_kip"]["fraction"]=="1" and delta["shear_percent_change_from_initial"]["fraction"]=="50" and delta["rotation_difference_rad"]["fraction"]=="-1/10",
          "2->3 shear gives+1,+50percent;0.200->0.100 gives-0.100")
    return results


def extract(data):
    tables={t["table"]:t for t in data["tables"]}
    expected=[f"{b}ST{i}" for b in (3,4,5) for i in (1,2,3)]
    out=[]
    initial=[dict(zip(tables["4.2"]["columns"],r)) for r in tables["4.2"]["rows"]]
    secondary=[dict(zip(tables["4.3"]["columns"],r)) for r in tables["4.3"]["rows"]]
    if [r["test"] for r in initial]!=expected or [r["test"] for r in secondary]!=expected:
        raise AssertionError("all nine source test IDs required in both stage tables")
    for first,second in zip(initial,secondary):
        record={"test":first["test"],"bolts":int(first["test"][0]),
                "secondary_missing_footnote":second["footnote"]}
        for stage,row,table in (("initial",first,"4.2"),("secondary",second,"4.3")):
            fields=("controlling_specimen","applied_shear_kip","beam_end_rotation_rad","failure_mechanism")
            if all(row[key] is None for key in fields):
                if stage=="initial":
                    raise AssertionError("unexpected missing initial stage")
                record[stage]=None
            elif any(row[key] is None for key in fields):
                raise AssertionError("partial unknown stage needs explicit separate handling")
            else:
                if F(row["applied_shear_kip"])<=0 or F(row["beam_end_rotation_rad"])<=0:
                    raise AssertionError("positive source values required")
                record[stage]={"shear":row["applied_shear_kip"],"rotation":row["beam_end_rotation_rad"],
                               "specimen":row["controlling_specimen"],"failure":row["failure_mechanism"],
                               "table":table,"physical_page":tables[table]["physical_page"]}
        out.append(record)
    return out


def calculate(data):
    records=extract(data)
    scenarios=[]
    for cohort in ("all_reported_tests","TN_figure_subset_without_5ST1"):
        subset=[r for r in records if cohort=="all_reported_tests" or r["test"]!="5ST1"]
        for bolts in (3,4,5):
            group=[r for r in subset if r["bolts"]==bolts]
            for rule in ("initial","maximum_reported_stage"):
                selected=[]
                for r in group:
                    stage,value=choose(r["initial"],r["secondary"],rule)
                    selected.append({"test":r["test"],"stage":stage,**value,
                                     "secondary_available":r["secondary"] is not None,
                                     "secondary_missing_footnote":r["secondary_missing_footnote"]})
                scenarios.append({"cohort":cohort,"bolts":bolts,"rule":rule,"n":len(group),"selected":selected,
                                  "statistics":{"applied_shear_kip":statistics([F(v["shear"]) for v in selected]),
                                                "beam_end_rotation_rad":statistics([F(v["rotation"]) for v in selected])}})
    differences=[]
    for r in records:
        differences.append({"test":r["test"],"bolts":r["bolts"],"secondary_available":r["secondary"] is not None,
                            "secondary_missing_footnote":r["secondary_missing_footnote"],
                            "initial":r["initial"],"secondary":r["secondary"],
                            "secondary_minus_initial":contrast(r["initial"],r["secondary"])})
    return {"scenarios":scenarios,"secondary_contrasts":differences,
            "scenario_count":len(scenarios),"quantity_summary_count":2*len(scenarios),
            "original_test_count":len(records),"populated_secondary_count":sum(r["secondary"] is not None for r in records),
            "native_units":{"applied_shear":"kip","beam_end_rotation":"rad"},
            "scope":"Initial or maximum reported failure-stage shear, with same-stage rotation. All reported tests and explicitly named figure subset; not acquired-history global peaks or NIST membership.",
            "exclusions":"No2V,unitconversion,anglecorrection,Table4.1/4.4 pooling,NIST means/COV comparison,probabilities,confidence intervals or calibration thresholds."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    if Path(args.output).name!=args.output or not args.output.endswith(".json"):
        parser.error("JSON output basename required")
    output=BASE/args.output
    if output.exists():
        parser.error("refusing existing output")
    paths={name:BASE/name for name in PINS}
    paths.update({"source_pdf":SOURCE,"code":Path(__file__)})
    before={key:sha(path) for key,path in paths.items()}
    for key,pin in PINS.items():
        if before[key]!=pin:
            raise AssertionError("frozen input changed: "+key)
    if before["source_pdf"]!=SOURCE_PIN:
        raise AssertionError("original PDF changed")
    tests=controls()
    result=calculate(json.loads((BASE/"thompson-independent.json").read_text()))
    after={key:sha(path) for key,path in paths.items()}
    if before!=after:
        raise AssertionError("input changed during run")
    receipt={"status":"PASS","command":[sys.executable,*sys.argv],"python":sys.version,
             "decimal_significant_digits":DECIMAL_PRECISION,
             "arithmetic":"Exact rational mean/variance; Decimal square roots and COV at80 significant digits, default ROUND_HALF_EVEN context.",
             "independence":"Original source and stage code frozen before root stage code/results access; exploratory interpretation included rough mental load/length considerations before systematic calculation, not claimed blind.",
             "pins_before":before,"pins_after":after,"controls":tests,"result":result}
    with output.open("x",encoding="utf-8") as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write("\n")
    print(json.dumps({"status":"PASS","scenarios":result["scenario_count"],"summaries":result["quantity_summary_count"],
                      "populated_secondary":result["populated_secondary_count"],"controls":len(tests),"sha256":sha(output)}))


if __name__=="__main__":
    main()
