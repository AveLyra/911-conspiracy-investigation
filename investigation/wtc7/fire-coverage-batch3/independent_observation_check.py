#!/usr/bin/env python3
"""Independent standard-library recomputation; imports no comparison code."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

DIRECTORY=Path(__file__).absolute().parent
PINS={
    "PROTOCOL.md":"ecdd7be9123231e05217c456ebc5ffbaa71c7828802d1212e0ed26a784e559c6",
    "TILED-IMAGE-ADDENDUM.md":"bede56a07730055dd16e20d6be22e3e1f32667504ee9028346cbb3e4bbebd724",
    "PAIR-KEY-NOTE.md":"dad716c5bee95ade5269556f2260cfe6659c810f1bbfa11703ad9fbba6717979",
    "anonymous-key.json":"50144e50b2907bdd0dd4a62f398bedf3c8f40dc3008888580486496ddebd094f",
    "anonymous-pair-key.json":"5b01f713bd100c8eda211800b29e93704b023dd6f12aaaa7c7f1210fe79da8e1",
    "root.json":"e8e7b7d23e993c68ecc0ee0df16a39a9204d4b0665f9734e08096e21925044c5",
    "observer.json":"6c4021bd658cc7f7b64af061c320809cdec1cbe923803a690a12e13d0015e1ac",
    "root-pair.json":"d802f84a342b81a3386f1c7472ef3e2342a46133da61b7e7ca3bfee7e0b6fd44",
    "observer-pair.json":"795eb0b549f5883bce3d749cc85f16189ab577b1a8b792546181b70479ef5982",
}
ASSET_FIELDS={"asset_id","image_sha256","dimensions","complete_native_image_inspected",
              "target_rect","target_evaluability","target_reason","luminous_features","smoke",
              "nondetection_regions","visibility_limits","overlay_regions"}
FIELDS=("target_evaluability","target_rect","target_reason","luminous_features","smoke",
        "nondetection_regions","visibility_limits","overlay_regions")
AXES=("target_evaluability","flame_like_identified","ambiguous_glow_identified","smoke_status","nondetection_region_identified")
RUN_PINS={"comparison-full01.json":"9c78daeb0f7c81c71b7031095c3cbe2065bea142d369c2f75f76b83bf4664952",
          "comparison-full02.json":"9c78daeb0f7c81c71b7031095c3cbe2065bea142d369c2f75f76b83bf4664952",
          "comparison-pair01.json":"f2fae74a01b5abc2f956cbc71b95d2610895dd679f0b88b7c8d42a0d9abf68fa",
          "comparison-pair02.json":"f2fae74a01b5abc2f956cbc71b95d2610895dd679f0b88b7c8d42a0d9abf68fa"}
PRODUCER_CODE_SHA="593c51aad319739898aa8f0c3c8fc7e802f22904815b81adad36304327f6a6f7"
REUSED_CODE_SHA="f24bb98a1b988a8eef20ae2095d5ec7fa6819e3520f0516cbca126c733641464"


def check(value,message):
    if not value: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def object_pairs(items):
        result={}
        for name,value in items:
            check(name not in result,"duplicate JSON key")
            result[name]=value
        return result
    def invalid_constant(value): raise ValueError("nonfinite JSON literal")
    def visit(value):
        if isinstance(value,float): check(math.isfinite(value),"nonfinite JSON value")
        elif isinstance(value,list):
            for child in value: visit(child)
        elif isinstance(value,dict):
            for child in value.values(): visit(child)
    result=json.loads(raw,object_pairs_hook=object_pairs,parse_constant=invalid_constant)
    visit(result)
    return result


def path_in(root,value,exists=True):
    root=Path(root).absolute(); path=Path(value)
    check(".." not in path.parts,"path traversal")
    if not path.is_absolute(): path=root/path
    path=path.absolute()
    check(root in path.parents,"path outside batch")
    for p in (path,*path.parents): check(not p.is_symlink(),"symlink input/output")
    check(path.is_file() if exists else path.parent.is_dir(),"invalid file location")
    return path


def words(value): check(isinstance(value,str) and bool(value.strip()),"nonempty reason/string required")


def size(value): check(isinstance(value,list) and len(value)==2 and all(type(x) is int and x>0 for x in value),"invalid dimensions")


def rectangle(rect,dimensions):
    check(isinstance(rect,list) and len(rect)==4,"four coordinate rectangle required")
    check(all(type(v) is int or type(v) is float and math.isfinite(v) for v in rect),"nonfinite/boolean coordinate")
    x0,y0,x1,y1=rect; w,h=dimensions
    check(0<=x0<x1<=w and 0<=y0<y1<=h,"degenerate/out of bounds rectangle")


def rectangles(value,dimensions):
    check(isinstance(value,list),"rectangle list required")
    for rect in value: rectangle(rect,dimensions)


def exact(value,fields): check(isinstance(value,dict) and set(value)==set(fields),"exact field structure required")


def choices(value,options): check(isinstance(value,str) and value in options,"invalid enumeration")


def word_list(value):
    check(isinstance(value,list) and bool(value),"nonempty string list required")
    for item in value: words(item)


def validate(record,membership,key_hash):
    check(isinstance(record,dict),"record object required")
    check({"reviewer","independence","protocol_sha256","provenance_key_sha256","assets"}<=set(record),"missing top-level field")
    words(record["reviewer"])
    independence=record["independence"]
    check(isinstance(independence,str) and bool(independence.strip()) or isinstance(independence,dict) and bool(independence),"empty independence disclosure")
    check(record["protocol_sha256"]==PINS["PROTOCOL.md"] and record["provenance_key_sha256"]==key_hash,"record protocol/key pins differ")
    check(isinstance(record["assets"],list) and len(record["assets"])==len(membership),"record membership count differs")
    found={}
    for asset in record["assets"]:
        exact(asset,ASSET_FIELDS)
        aid=asset["asset_id"]
        check(isinstance(aid,str) and aid in membership and aid not in found,"unknown/duplicate asset ID")
        found[aid]=asset; expected=membership[aid]
        check(asset["image_sha256"]==expected["sha256"],"image pin differs")
        size(asset["dimensions"])
        check(asset["dimensions"]==expected["dimensions"],"dimensions differ")
        check(asset["complete_native_image_inspected"] is True,"complete view not affirmed")
        dims=asset["dimensions"]
        choices(asset["target_evaluability"],{"partial_detail","limited_detail","unresolved_target"})
        if asset["target_evaluability"]=="unresolved_target": check(asset["target_rect"] is None,"unresolved target must have null rectangle")
        else: rectangle(asset["target_rect"],dims)
        words(asset["target_reason"])
        check(isinstance(asset["luminous_features"],list),"luminous list required")
        for feature in asset["luminous_features"]:
            exact(feature,{"rect","appearance","target_relation","reason","alternatives"})
            rectangle(feature["rect"],dims)
            choices(feature["appearance"],{"flame_like","ambiguous_glow"})
            choices(feature["target_relation"],{"on_candidate_facade","uncertain"})
            words(feature["reason"]); word_list(feature["alternatives"])
        smoke=asset["smoke"]
        exact(smoke,{"status","regions","reason"})
        choices(smoke["status"],{"visible","uncertain","not_identified"})
        rectangles(smoke["regions"],dims); words(smoke["reason"])
        if smoke["status"]=="visible": check(bool(smoke["regions"]),"visible smoke requires locator")
        if smoke["status"]=="not_identified": check(not smoke["regions"],"unidentified smoke cannot have locator")
        check(isinstance(asset["nondetection_regions"],list),"nondetection list required")
        for region in asset["nondetection_regions"]:
            exact(region,{"rect","reason"}); rectangle(region["rect"],dims); words(region["reason"])
        word_list(asset["visibility_limits"])
        rectangles(asset["overlay_regions"],dims)
    check(set(found)==set(membership),"record membership differs")
    return found


def jpeg_dimensions(data):
    check(data[:2]==b"\xff\xd8","JPEG SOI missing")
    at=2
    while at<len(data):
        check(data[at]==255,"invalid JPEG marker alignment")
        while at<len(data) and data[at]==255: at+=1
        check(at<len(data),"truncated JPEG marker")
        marker=data[at]; at+=1
        if marker in (0xD8,0x01) or 0xD0<=marker<=0xD7: continue
        check(marker not in (0xD9,0xDA),"JPEG has no preceding SOF")
        check(at+2<=len(data),"truncated JPEG segment")
        length=struct.unpack(">H",data[at:at+2])[0]
        check(length>=2 and at+length<=len(data),"invalid JPEG segment length")
        if 0xC0<=marker<=0xCF and marker not in (0xC4,0xC8,0xCC):
            check(length>=8,"short JPEG SOF")
            h,w=struct.unpack(">HH",data[at+3:at+7])
            check(h>0 and w>0,"invalid JPEG SOF dimensions")
            return [w,h]
        at+=length
    raise ValueError("JPEG SOF not found")


def axes(asset):
    kinds={feature["appearance"] for feature in asset["luminous_features"]}
    return {"target_evaluability":asset["target_evaluability"],"flame_like_identified":"flame_like" in kinds,
            "ambiguous_glow_identified":"ambiguous_glow" in kinds,"smoke_status":asset["smoke"]["status"],
            "nondetection_region_identified":len(asset["nondetection_regions"])>0}


def recompute(left,right,membership):
    result=[]
    for aid in membership:
        a,b=left[aid],right[aid]; aa,bb=axes(a),axes(b)
        result.append({"asset_id":aid,
                       "all_observation_fields":{name:{"left":a[name],"right":b[name],"same":a[name]==b[name]} for name in FIELDS},
                       "axes":{name:{"left":aa[name],"right":bb[name],"same":aa[name]==bb[name]} for name in AXES}})
    return result


def producer_shape(recalculated,left,right):
    """Independent result translated to the producer's saved output contract."""
    def paired(a,b): return {"left":a,"right":b,"identical_json":a==b}
    result=[]
    for item in recalculated:
        aid=item["asset_id"]; a,b=left[aid],right[aid]
        regions={name:paired(a[name],b[name]) for name in ("target_rect","luminous_features","nondetection_regions","overlay_regions")}
        regions["smoke_regions"]=paired(a["smoke"]["regions"],b["smoke"]["regions"])
        descriptions={name:paired(a[name],b[name]) for name in ("target_reason","visibility_limits")}
        descriptions["smoke_reason"]=paired(a["smoke"]["reason"],b["smoke"]["reason"])
        result.append({"asset_id":aid,"axes":{name:{"left":v["left"],"right":v["right"],"comparison":"same" if v["same"] else "different"} for name,v in item["axes"].items()},
                       "regions_without_forced_matching":regions,"descriptions":descriptions})
    return result


def carry_forward(pair,full):
    result={aid:pair[aid]==full.get(aid) for aid in pair}
    check(all(result.values()),"frozen pair row changed in full record")
    return result


def verify_producer(report,records,recalculated,membership,scope,key_hash):
    check(report["scope"]==scope and report["batch"]==3 and report["schema_version"]==2,"producer report identity differs")
    check(report["sample_asset_ids"]==list(membership),"producer membership/order differs")
    check(report["raw_records"]==records,"producer raw records differ")
    check(report["source_hashes"]["protocol_sha256"]==PINS["PROTOCOL.md"] and report["source_hashes"]["provenance_key_sha256"]==key_hash,"producer source pins differ")
    lhs={a["asset_id"]:a for a in records[0]["assets"]}; rhs={a["asset_id"]:a for a in records[1]["assets"]}
    expected=[{"left_reviewer":records[0]["reviewer"],"right_reviewer":records[1]["reviewer"],"assets":producer_shape(recalculated,lhs,rhs)}]
    check(report["comparisons"]==expected,"producer comparison differs from independent recomputation")
    return True


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-runs",nargs=2,required=True)
    parser.add_argument("--pair-runs",nargs=2)
    parser.add_argument("--out",default="independent-observation-check01")
    args=parser.parse_args(argv)
    snapshot={}; decoded={}
    def take(relative,expected=None):
        path=path_in(DIRECTORY,relative); raw=path.read_bytes(); actual=sha(raw)
        if expected is not None: check(actual==expected,"frozen input hash mismatch: "+str(relative))
        snapshot[str(path.relative_to(DIRECTORY))]=actual
        return raw
    for path,expected in PINS.items():
        raw=take(path,expected)
        if path.endswith(".json"): decoded[path]=parse(raw)
    take(Path(__file__).name)
    take("test_independent_observation_check.py")
    take("compare.py",PRODUCER_CODE_SHA)  # Hash only; never imported/executed.
    dependency=path_in(DIRECTORY.parent,"fire-coverage-batch2/summarize.py")
    check(sha(dependency.read_bytes())==REUSED_CODE_SHA,"producer reused-code pin differs")
    fullkey=decoded["anonymous-key.json"]; pairkey=decoded["anonymous-pair-key.json"]
    membership={}
    for entry in fullkey["assets"]:
        aid=entry["asset_id"]; check(aid not in membership,"duplicate key asset")
        view=entry["extracted_view"]; size(view["dimensions"])
        check(entry["native_pdf_dimensions"]==view["dimensions"],"key native dimension mismatch")
        check(view["path"]==f"assets/run01/images/{aid}.jpg" and view["format"]=="JPEG","image format/path mismatch")
        raw=take(view["path"],view["sha256"])
        check(type(view["bytes"]) is int and view["bytes"]==len(raw),"image byte count differs")
        check(jpeg_dimensions(raw)==view["dimensions"],"independent JPEG SOF dimensions differ")
        membership[aid]=view
    check(len(membership)==25,"frozen full key must contain 25 JPEGs")
    check(list(membership)==fullkey["selected_asset_ids"],"full membership order differs")
    pairids=pairkey["sample_asset_ids"]
    check(len(pairids)==len(set(pairids))==2 and pairids==fullkey["pair_asset_ids"]==list(membership)[:2],"pair membership differs")
    check(pairkey["assets"]==fullkey["assets"][:2],"pair/full key rows differ")
    pairmembers={aid:membership[aid] for aid in pairids}
    collections={}
    for scope,paths,keyname,members in (("full",["root.json","observer.json"],"anonymous-key.json",membership),
                                       ("pair",["root-pair.json","observer-pair.json"],"anonymous-pair-key.json",pairmembers)):
        records=[decoded[p] for p in paths]
        check(records[0]["reviewer"]!=records[1]["reviewer"],"duplicate reviewer identity")
        rows=[validate(r,members,PINS[keyname]) for r in records]
        collections[scope]={"records":records,"rows":rows,"comparisons":recompute(*rows,members)}
    preserved=[carry_forward(p,f) for p,f in zip(collections["pair"]["rows"],collections["full"]["rows"])]
    run_checks={}
    for scope,runs,keyname,members in (("full",args.full_runs,"anonymous-key.json",membership),
                                     ("pair",args.pair_runs,"anonymous-pair-key.json",pairmembers)):
        if runs is None:
            run_checks[scope]={"producer_runs_checked":False,"reason":"No pair producer runs supplied; independent pair recomputation retained."}
            continue
        check(all(p in RUN_PINS for p in runs),"unknown producer run filename")
        raws=[take(p,RUN_PINS[p]) for p in runs]
        check(raws[0]==raws[1],"producer repeated runs are not byte-identical")
        for raw in raws:
            report=parse(raw)
            verify_producer(report,collections[scope]["records"],collections[scope]["comparisons"],members,scope,PINS[keyname])
            labelpaths=["root.json","observer.json"] if scope=="full" else ["root-pair.json","observer-pair.json"]
            expected_labels=[{"path":p,"sha256":PINS[p],"reviewer":decoded[p]["reviewer"]} for p in labelpaths]
            check(report["source_hashes"]["labels"]==expected_labels,"producer label pin differs")
            check(report["source_hashes"]["images"]==[{"asset_id":aid,**pin} for aid,pin in members.items()],"producer image pins/order differ")
            check(report["source_hashes"]["code_sha256"]==PRODUCER_CODE_SHA and report["source_hashes"]["batch2_code_sha256"]==REUSED_CODE_SHA,"producer code pins differ")
        run_checks[scope]={"producer_runs_checked":True,"run_paths":runs,"byte_identical":True,"comparison_matches_independent":True}
    results={"schema_version":1,"scope":"Independent recomputation of frozen batch3 image descriptions",
             "full":{"sample_asset_ids":list(membership),"comparisons":collections["full"]["comparisons"]},
             "pair":{"sample_asset_ids":pairids,"comparisons":collections["pair"]["comparisons"]},
             "pair_rows_identical_in_full_by_reviewer":preserved,"producer_run_checks":run_checks,
             "limitations":["No image pixels/captions were inspected by this checker.","Same/different describes saved labels, not measurement accuracy or consensus.","Counts of descriptions are not counts of fires, windows or independent exposures.","Text reasons are checked for presence; their substantive adequacy remains a human review question."]}
    counts={scope:{axis:sum(not x["axes"][axis]["same"] for x in data["comparisons"]) for axis in AXES} for scope,data in collections.items()}
    for relative,expected in snapshot.items(): check(sha(path_in(DIRECTORY,relative).read_bytes())==expected,"input changed during independent calculation")
    check(sha(dependency.read_bytes())==REUSED_CODE_SHA,"producer reused-code changed during independent calculation")
    output=path_in(DIRECTORY,args.out,exists=False); output.mkdir(exist_ok=False)
    data=(json.dumps(results,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with (output/"comparisons.json").open("xb") as f:f.write(data)
    receipt={"accepted":True,"python":sys.version,"input_snapshot":snapshot,"record_hashes":{p:PINS[p] for p in ("root.json","observer.json","root-pair.json","observer-pair.json")},
             "outputs":{"comparisons.json":sha(data)},"source_image_count":25,"pair_image_count":2,
             "pair_rows_unchanged":True,"producer_run_checks":run_checks,"axis_difference_counts":counts,
             "external_code_snapshot":{str(dependency):REUSED_CODE_SHA},
             "standard_library_only":True,"producer_code_imported":False,"pixels_decoded":False}
    with (output/"receipt.json").open("x") as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write("\n")
    print(json.dumps({"accepted":True,"full":25,"pair":2,"pair_rows_unchanged":True,"run_checks":run_checks,"axis_difference_counts":counts}))


if __name__=="__main__": main()
