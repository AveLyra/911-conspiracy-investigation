#!/usr/bin/env python3
"""Read-only independent set/pin/field audit of the batch 3 coverage join."""
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).absolute().parent
TIMELINE_SHA="08141aa6d221f80bec33501761b5f19030706bb1e0badfd035375bcb93c73aab"
NEW_FIGURES={f"5-{n}" for n in (121,122,123,124,128,129,130,132,133,134,136,138,139,140,141,142,143,144,145,146,152,153,154,155,156,159)}
RECURRENT_FIGURES={f"5-{n}" for n in (125,126,135,137,148,149,150,151,157,158)}


def main():
    snapshot={}; failures=[]; checks=0
    def require(ok,label):
        nonlocal checks
        checks+=1
        if not ok: failures.append(label)
    def read(path,expected=None,size=None):
        p=Path(path)
        if not p.is_absolute():p=HERE/p
        require(not any(x.is_symlink() for x in (p,*p.parents)),"symlink source: "+str(p))
        raw=p.read_bytes(); actual=hashlib.sha256(raw).hexdigest()
        require(expected is None or actual==expected,"hash mismatch: "+str(p))
        require(size is None or len(raw)==size,"size mismatch: "+str(p))
        snapshot[str(p)]=actual
        return raw
    def parse(raw):
        def pairs(items):
            result={}
            for k,v in items:
                if k in result:raise ValueError("duplicate JSON key")
                result[k]=v
            return result
        return json.loads(raw,object_pairs_hook=pairs)
    join=parse(read("coverage-timeline.json",TIMELINE_SHA)); markdown=read("coverage-timeline.md").decode()
    inputs={}
    require(len(join["input_pins"])==10,"ten declared source inputs")
    for pin in join["input_pins"]:
        raw=read(pin["path"],pin["sha256"])
        require(pin["role"] not in inputs,"duplicate input role")
        inputs[pin["role"]]=parse(raw) if pin["path"].endswith(".json") else raw.decode()
    pdf=join["source_pdf"]; read(pdf["path"],pdf["sha256"],pdf["bytes"])
    read("root.json",join["release_gate"]["root_full25_record_sha256"])
    read("observer.json",join["release_gate"]["observer_full25_record_sha256"])
    prior={x["figure_association"]["figure"]:x for x in inputs["prior_inventory"]["assets"] if x["role"]=="report_photographic_image"}
    new={x["figure"]:x for x in inputs["new_attributions"]["figures"]}
    require(len(prior)==25,"25 distinct prior photographic figures")
    require(set(new)==NEW_FIGURES and len(new)==26,"26 declared new figures")
    require(not(set(prior)&set(new)),"prior/new figure sets disjoint")
    rows=join["rows"]; byfigure={x["figure"]:x for x in rows}
    require(len(rows)==len(byfigure)==51 and set(byfigure)==set(prior)|NEW_FIGURES,"exact unique 51-row union")
    oldkey={x["asset_id"]:x for x in inputs["prior_provenance_key"]["assets"]}
    newkey={x["asset_id"]:x for x in inputs["new_extraction_key"]["assets"]}
    anonymous={x["asset_id"]:x for x in inputs["new_anonymous_key"]["assets"]}
    standalone=[]; componentids=[]; field_checks=0
    for row in rows:
        fig=row["figure"]
        require(row["time"]["independently_authenticated"] is False,"unauthenticated clock: "+fig)
        require(row["appearance_labels_imported"] is False and row["model_comparison_result"] is None,"no relabel/model conclusion: "+fig)
        require(bool(row["location"]["report_attributed_floor_scope"]),"floor-meaning qualifier: "+fig)
        if fig in prior:
            source=prior[fig]
            require(row["batch"]=="prior25" and row["asset_ids"]==[source["asset_id"]],"prior row membership: "+fig)
            require(row["image"]==source["image"],"prior full image pin: "+fig)
            require(row["credit"]==source["source_credit_as_displayed"],"prior credit: "+fig)
            for target,original in (("physical","physical_page"),("printed","printed_page"),("render","render"),("context_text","context_text")):
                require(row["source_page"][target]==source["page"][original],"prior page pin: "+fig+":"+target)
        else:
            source=new[fig]
            require(row["batch"]=="new26" and row["asset_ids"]==source["observation_asset_ids"],"new row observation membership: "+fig)
            require(row["native_component_asset_ids"]==source["native_image_object_ids"],"new component membership: "+fig)
            mapping=((row["source_page"]["physical"],source["physical_page"]),(row["source_page"]["printed"],source["printed_page"]),
                     (row["source_page"]["render"],source["source_page"]["render"]),(row["source_page"]["context_text"],source["source_page"]["text"]),
                     (row["location"]["report_attributed_floors"],source["report_attributed_floors"]),(row["location"]["source_label_details"],source["source_added_location_labels"]),
                     (row["location"]["view"],source["report_attributed_view"]),(row["credit"],source["credited_source"]),(row["processing"],source["report_processing"]),
                     (row["limits"],source["prose_and_image_limits"]),(row["time"]["as_reported"],source["report_time"]["label"]),
                     (row["time"]["interval_local_hhmmss"],source["report_time"]["stated_or_arithmetically_expanded_interval_local"]),
                     (row["time"]["basis"],source["report_time"]["basis"]),(row["time"]["source_physical_pages"],source["report_time"]["source_physical_pages"]))
            for actual,expected in mapping:require(actual==expected,"new inherited source field: "+fig)
            field_checks+=len(mapping)
        if row["image"] is not None:
            require(len(row["asset_ids"])==1,"one standalone object: "+fig)
            aid=row["asset_ids"][0]; key=oldkey[aid] if fig in prior else newkey[aid]
            require(row["image"]["sha256"]==key["extracted_view"]["sha256"] and row["image"]["dimensions"]==key["native_pdf_dimensions"],"key image identity/dimensions: "+fig)
            read(row["image"]["path"],row["image"]["sha256"],row["image"]["bytes"])
            standalone.append((aid,row["image"]["sha256"]))
            if fig in new:require(aid in anonymous and anonymous[aid]["extracted_view"]["sha256"]==row["image"]["sha256"],"anonymous key membership: "+fig)
        for pin in (row["source_page"]["render"],row["source_page"]["context_text"]):read(pin["path"],pin["sha256"],pin["bytes"])
        componentids.extend(row.get("native_component_asset_ids",row["asset_ids"]))
    require(len(standalone)==len(set(x[0] for x in standalone))==len(set(x[1] for x in standalone))==50,"50 unique standalone IDs/hashes")
    require(len(componentids)==len(set(componentids))==67,"67 selected distinct native components")
    tiled=[x for x in rows if x["image"] is None]
    require(len(tiled)==1 and tiled[0]["figure"]=="5-121" and tiled[0]["asset_ids"]==[],"one unscored 5-121 representation")
    t=tiled[0];require(t["native_observation_status"]=="unscored_representation_gate_failure","explicit unscored state")
    require(len(t["native_component_asset_ids"])==17,"17 tiled parents")
    for aid in t["native_component_asset_ids"]:
        pin=newkey[aid]["extracted_view"];read(pin["path"],pin["sha256"],pin["bytes"])
    limit=t["representation_limitation"]
    receipt=parse(read(limit["receipt"]["path"],limit["receipt"]["sha256"]))
    read(limit["addendum"]["path"],limit["addendum"]["sha256"])
    require(receipt["accepted"] is False and receipt["png_written"] is False and limit["actual_assembly_performed"] is False,"failed tile gate retained")
    recurrence=join["cross_batch_context_recurrences"]
    context={x["figure"]:x for x in inputs["new_attributions"]["context_only_figures"]}
    actual_recurrence=set(context)&set(prior)
    require(actual_recurrence==RECURRENT_FIGURES=={x["figure"] for x in recurrence} and len(recurrence)==10,"exact ten context recurrences")
    for item in recurrence:
        fig=item["figure"]; aid=prior[fig]["asset_id"]
        require(context[fig]["asset_ids"]==[aid]==byfigure[fig]["asset_ids"] and item["asset_id"]==aid,"recurrent association: "+fig)
        require(item["prior_image_sha256"]==item["new_context_image_sha256"]==prior[fig]["image"]["sha256"]==newkey[aid]["extracted_view"]["sha256"],"recurrent byte identity: "+fig)
        pin=newkey[aid]["extracted_view"];read(pin["path"],pin["sha256"],pin["bytes"])
    require(set(context)-RECURRENT_FIGURES=={"5-120","5-127","5-131","5-147"},"four additional context-only figures excluded")
    groups={g["id"]:g for g in join["dependency_groups"]}
    require(len(groups)==len(join["dependency_groups"]),"unique dependency groups")
    for row in rows:
        require(set(row["dependency_group_ids"])=={g["id"] for g in groups.values() if row["figure"] in g["figures"]},"bidirectional dependency references: "+row["figure"])
    same=[set(g["figures"]) for g in groups.values() if g["type"]=="same_underlying_photograph"]
    require(len(same)==2 and {"5-60","5-61"} in same and {"5-129","5-130"} in same,"two explicit same-exposure pairs")
    require(all(set(g["figures"])<=set(byfigure) for g in groups.values()),"dependency figure membership")
    facade_counts={x["facade"]:x["figure_rows"] for x in join["coverage_by_report_attributed_facade"]}
    for item in join["coverage_by_report_attributed_facade"]:
        actual=[r["figure"] for r in rows if item["facade"] in r["location"]["facades"]]
        require(item["figure_ids"]==actual and item["figure_rows"]==len(actual),"facade tag recomputation: "+item["facade"])
    require(not any("south" in x["location"]["facades"] for x in rows if x["batch"]=="new26"),"no new south tag")
    ids=re.findall(r"^\|[^\n]*?\| (5-\d+) \((prior|new)\)",markdown,re.M)
    require([x[0] for x in ids]==join["timeline_display_order"] and len(ids)==51,"Markdown/JSON exact ordered figure union")
    require(all(byfigure[f]["batch"]==("prior25" if b=="prior" else "new26") for f,b in ids),"Markdown batch attribution")
    require(len(set(join["timeline_display_order"]))==51 and set(join["timeline_display_order"])==set(byfigure),"unique display order")
    fa=join["fa_questions"]
    require(len(fa)==7 and {x["id"] for x in fa}=={f"FA-C0{i}" for i in range(1,8)},"seven exact FA questions")
    require(all(x["matched_figure_links"]==[] and x["matching_status"]=="no_complete_quantity_location_time_match" for x in fa),"zero complete FA matches")
    require(all(x["id"] in inputs["prior_source_map_and_fa_questions"] for x in fa),"FA IDs grounded in pinned source audit")
    expected_counts={"prior_photographic_figures":25,"new_fixed_target_figures":26,"distinct_selected_figure_representations":51,"standalone_jpeg_assets":50,"unique_standalone_asset_ids":50,"unique_standalone_encoded_hashes":50,"unscored_tiled_figures":1,"unscored_tiled_native_objects":17,"selected_native_objects":67,"known_same_exposure_pairs":2,"new_context_recurrences_of_prior_assets":10,"completed_fa_quantity_location_time_matches":0}
    require(join["counts"]==expected_counts,"all declared count fields")
    require(byfigure["5-109"]["time"]["conflict"] and byfigure["5-111"]["time"]["conflict"] and byfigure["5-111"]["time"]["display_anchor_hhmmss"] is None,"AM/PM conflicts retained")
    require(all(byfigure[f]["time"]["interval_local_hhmmss"] is None for f in ("5-122","5-125","5-144","5-145","5-146","5-152","5-157","5-158")),"unbounded/inherited times not made hard intervals")
    require(byfigure["5-156"]["time"]["interval_local_hhmmss"]==["17:17:45","17:21:45"],"late source interval not silently clipped")
    for path,expected in snapshot.items():require(hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected,"input changed: "+path)
    print(json.dumps({"accepted":not failures,"checks":checks,"files_rehashed_before_after":len(snapshot),"new_source_field_equalities":field_checks,"counts":expected_counts,"facade_tags":facade_counts,"failures":failures,"join_sha256":TIMELINE_SHA,"markdown_sha256":snapshot[str(HERE/"coverage-timeline.md")]},indent=2))
    return 0 if not failures else 2


if __name__=="__main__":raise SystemExit(main())
