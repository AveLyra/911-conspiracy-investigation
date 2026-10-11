"""Peer literal expansion for F7-Im2-early; no pixel selection by code.

Selections and observation receipts are filled only after actual source reading.
This script never loads image pixels or infers historical continuity.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
TARGET = [220, 0, 330, 88]
CONTEXT = [218, 0, 332, 88]
FULL_CONTEXT_INSPECTED = False
EXPECTED_INPUTS = {}
RAW_BLOCKS = [
    {"columns": [218, 225], "receipt": "exec chunk 3cfba7; exit 0; 2248 tokens; untruncated"},
    {"columns": [226, 233], "receipt": "exec chunk 8aab02; exit 0; 2463 tokens; untruncated"},
    {"columns": [234, 241], "receipt": "exec chunk 73c9e1; exit 0; 2492 tokens; untruncated"},
    {"columns": [242, 249], "receipt": "exec chunk f8f6c1; exit 0; 2276 tokens; untruncated"},
    {"columns": [250, 257], "receipt": "exec chunk 848b75; exit 0; 2220 tokens; untruncated"},
    {"columns": [258, 265], "receipt": "exec chunk 7d5da4; exit 0; 2051 tokens; untruncated"},
    {"columns": [266, 273], "receipt": "exec chunk e90838; exit 0; 2047 tokens; untruncated"},
    {"columns": [274, 281], "receipt": "exec chunk 16f608; exit 0; 2316 tokens; untruncated"},
    {"columns": [282, 289], "receipt": "exec chunk f222ff; exit 0; 2168 tokens; untruncated"},
    {"columns": [290, 297], "receipt": "exec chunk 44eba7; exit 0; 1823 tokens; untruncated"},
]
ACTUAL_VIEWS = [
    {"path": "../../native-strips01/Im2.jpg", "receipt": "functions.exec view_image original; whole 741x88 image displayed in peer turn before chunk 3cfba7"},
    {"path": "../../render01/page-076.png", "receipt": "same functions.exec view_image original; whole composed page displayed; page used for style/orientation only, not coordinates"},
]
PRIOR_KNOWLEDGE = (
    "Prior-informed energy/source admission reviewer energy_admission_review; "
    "familiar with graph identity and conditional support limits, not blind. "
    "No counterpart's new F7-Im2-early reading inspected before freeze. "
    "Separate AI reading of shared historical bytes, not independent historical "
    "evidence, human acceptance or a calibrated envelope."
)

# Manually chosen inclusive x runs: first,last,fragment_id,core rows,fringe rows,
# reason. Row sets are literal; overlapping distinct memberships are rejected.
ATTRIBUTED = {"solid": [], "dash": [
    (231,231,"peer-D01",[],[82,83,84],"Very pale green onset adjacent to the first clear lower broken body; tentative only."),
    (232,232,"peer-D01",[83,84],[82,85],"First distinguishable lower green broken body, with pale edge cells."),
    (233,233,"peer-D01",[81,82,83],[80,84,85],"Same local lower broken body; surrounding pale green edge."),
    (234,234,"peer-D01",[79,80,81],[78,82,83],"Distinct lower green broken stroke."),
    (235,235,"peer-D01",[79],[78,80,81],"Lower body's cap; not joined to the separate higher piece."),
    (235,235,"peer-D02",[],[74,75],"Separate pale higher piece; body membership tentative, not a bridge to D01."),
    (236,236,"peer-D02",[73,74,75],[72,76],"Second green broken body above the preceding cap."),
    (237,237,"peer-D02",[72,73,74],[71,75,76],"Green body with a distinct lower pale edge."),
    (238,238,"peer-D02",[71,72,73],[70,74],"Green broken stroke locally separated from the upper blue stroke."),
    (239,239,"peer-D02",[71,72],[70,73],"Green stroke remains below the blue solid material."),
    (240,240,"peer-D02",[70,71],[69,72],"Local green body, with pale outer cells."),
    (241,241,"peer-D02",[70],[69,71,72],"Fading cap of the lower green body; not joined into the higher mixed-color contact."),
    (242,242,"peer-D02",[],[69,70,71],"Pale lower cap remains tentative and separate from the upper mixed-color band."),
    (248,248,"peer-D04",[],[59,60,61,62],"Pale green onset above the blue stroke; tentative new body, not continuity through the contact."),
    (249,249,"peer-D04",[],[58,59,60,61,62],"Pale green material above the blue stroke, preceding the clear local body."),
    (250,250,"peer-D04",[61,62],[60],"Green local body above blue; mixed-color lower edge retained separately."),
    (251,251,"peer-D04",[59,60,61,62],[58],"Distinct green body; lower mixed-color edge is not uniquely assigned."),
    (252,252,"peer-D04",[58,59,60],[57,61,62],"Green broken stroke and pale edges, separated from blue below."),
    (253,253,"peer-D04",[58,59],[57,60,61],"Fading green cap; no continuity claim across the next gap."),
    (254,254,"peer-D04",[],[58,59],"Neutral/pale cap material tentatively retained as fringe only."),
    (256,256,"peer-D05",[60],[58,59],"New green broken-body cap after an unassigned gap column."),
    (257,257,"peer-D05",[59,60],[58,61],"New local green body above blue; outer cells tentative."),
    (258,258,"peer-D05",[56,57,58,59],[55,60],"Green broken body with visible pale outer edge."),
    (259,259,"peer-D05",[55,56,57],[54,58,59],"Green body locally distinct from the blue stroke below."),
    (260,260,"peer-D05",[55],[54,56,57],"Fading upper cap of D05; no joining across the following pale gap."),
    (262,262,"peer-D06",[],[56,57],"Tentative pale onset of the next distinguishable broken body."),
    (263,263,"peer-D06",[56,57],[55,58],"New distinct green broken body."),
    (264,264,"peer-D06",[56,57],[55,58],"Green body and pale outer edges."),
    (265,265,"peer-D06",[55,56,57],[54,58],"Green broken stroke; no inferred dash-gap coverage."),
    (266,266,"peer-D06",[53,54,55,56],[52,57,58],"Local green body and its surrounding pale edge."),
    (267,267,"peer-D06",[53,54],[52,55,56],"Fading cap of this green body."),
    (268,268,"peer-D06",[],[52,53],"Lower pale cap retained separately from the next higher piece."),
    (268,268,"peer-D07",[],[48,49,50],"Separate higher pale onset; not joined to D06."),
    (269,269,"peer-D07",[49,50],[48,51,52],"New green broken body above prior cap."),
    (270,270,"peer-D07",[49,50],[48,51,52],"Local green body with outer pale rows."),
    (271,271,"peer-D07",[50,51],[49,52],"Local green body; native row change retained."),
    (272,272,"peer-D07",[51],[50,52],"Narrow green body and pale neighboring edge."),
    (273,273,"peer-D07",[50,51],[49,52],"Green body; no smoothing of its local bend."),
    (274,274,"peer-D07",[50,51],[49,52],"Green body fading toward its cap."),
    (275,275,"peer-D07",[50],[49,51],"Muted but distinct green cap."),
    (276,276,"peer-D07",[],[50,51],"Lower pale cap, separately identified from higher D08 onset."),
    (276,276,"peer-D08",[],[46,47],"Higher pale onset of a separate local body."),
    (277,277,"peer-D08",[46,47],[45,48],"Distinct green broken body."),
    (278,279,"peer-D08",[46,47],[45,48],"Green broken stroke with pale outer cells."),
    (280,280,"peer-D08",[46,47],[45,48],"Local green body; cap neighborhood remains explicit."),
    (281,281,"peer-D08",[44,45,46],[43,47,48],"Green body bends toward upper rows; no fitted centerline."),
    (282,282,"peer-D08",[44,45],[43,46,47],"Fading green cap with pale edges."),
    (283,283,"peer-D08",[],[43,44,45,46],"Pale cap material only, not positive body support."),
    (284,284,"peer-D09",[40,41],[39,42],"New higher green broken body after the cap."),
    (285,285,"peer-D09",[40,41],[39,42],"Distinct green body and outer pale rows."),
    (286,286,"peer-D09",[40,41,42],[39,43],"Local green body with a retained bend."),
    (287,287,"peer-D09",[41,42],[40,43],"Green body; no smoothing between native columns."),
    (288,288,"peer-D09",[42],[41,43,44],"Narrow green body with pale outer rows."),
    (289,289,"peer-D09",[41,42],[40,43,44],"Green body fading toward local cap."),
    (290,290,"peer-D09",[41,42],[40,43,44],"Muted green cap remains locally distinguishable."),
    (291,291,"peer-D09",[],[41,42],"Lower pale cap kept separate from new higher piece."),
    (291,291,"peer-D10",[],[37,38],"Separate upper pale onset; no continuity with D09."),
    (292,292,"peer-D10",[36,37,38],[35,39],"New higher green broken body."),
    (293,293,"peer-D10",[35,36,37],[34,38],"Green body and pale surrounding cells."),
    (294,294,"peer-D10",[34,35,36],[33,37],"Green body locally separated from red and blue curves."),
    (295,295,"peer-D10",[34,35],[33,36,37],"Green broken stroke with pale edges."),
    (296,296,"peer-D10",[34,35],[33,36],"Green stroke cap, retaining tentative outer cells."),
    (297,297,"peer-D10",[],[34,35,36],"Muted green cap assigned fringe only; no confident core."),
]}
# Manually chosen bands: x,band_id,candidate_routes,fragment_id,core,fringe,reason.
UNASSIGNED = [
    (242,"peer-B242-contact",["dash"],"peer-U03",[],[64,65,66],"Blue/green mixed onset: F7 dash contribution versus blue solid/edge unresolved; separate from lower D02 cap."),
    (243,"peer-B243-contact",["dash"],"peer-U03",[],[63,64,65,66],"Mixed green/cyan/blue contact; no unique F7 dash cell ownership."),
    (244,"peer-B244-contact",["dash"],"peer-U03",[],[63,64,65,66],"Mixed-color broken piece at blue solid contact; preserve unresolved ownership."),
    (245,"peer-B245-contact",["dash"],"peer-U03",[],[63,64,65,66],"Green/cyan/blue contact cells not uniquely attributable to F7 dash."),
    (246,"peer-B246-contact",["dash"],"peer-U03",[],[63,64,65,66],"Mixed-color local piece remains unresolved; no through-contact bridge."),
    (247,"peer-B247-contact",["dash"],"peer-U03",[],[64,65,66],"Blue/cyan cap after the mixed local piece; F7 dash contribution unresolved."),
    (250,"peer-B250-edge",["dash"],"peer-U04edge",[],[63],"Mixed green/blue lower edge next to D04; not duplicated as attributed ink."),
    (251,"peer-B251-edge",["dash"],"peer-U04edge",[],[63],"Pale cyan lower edge may combine green and blue contributions; unassigned."),
    (261,"peer-B261-gap",["dash"],"peer-Ugap05-06",[],[55,56,57,58],"Pale green gap neighborhood has unresolved body membership; not a bridge between D05 and D06."),
]


def pin(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def inputs():
    if not EXPECTED_INPUTS:
        raise ValueError("Input pins not frozen")
    result = {name: pin(HERE / name) for name in EXPECTED_INPUTS}
    if result != EXPECTED_INPUTS:
        raise ValueError("Changed frozen input; preserve prior artifacts")
    return result


def rows(values):
    result = list(values)
    if result != sorted(set(result)):
        raise ValueError("Unsorted or duplicate literal rows")
    if any(type(y) is not int or not 0 <= y < 88 for y in result):
        raise ValueError("Literal rows outside target")
    return result


def flags(x, selected):
    return [name for yes, name in (
        (bool(selected) and x == 220, "target_left"),
        (bool(selected) and x == 329, "target_right"),
        (0 in selected, "target_top"),
        (87 in selected, "target_bottom"),
    ) if yes]


def record(x, pieces, reason, refs=()):
    core, fringe, memberships = [], [], []
    used = set()
    for fragment, c, f in pieces:
        c, f = rows(c), rows(f)
        selected = set(c) | set(f)
        if not selected or set(c) & set(f) or used & selected:
            raise ValueError("Empty, overlapping class or membership")
        used |= selected
        core.extend(c)
        fringe.extend(f)
        memberships.append({"fragment_id": fragment, "core": c, "fringe": f})
    boundary = flags(x, used)
    status = ("identity_conflict" if refs else "boundary_truncated" if boundary
              else "identified_local_fragment" if core else "fringe_only" if fringe
              else "no_attributable_cells")
    return {"x": x, "core": sorted(core), "fringe": sorted(fringe),
            "fragment_id": memberships[0]["fragment_id"] if len(memberships) == 1 else None,
            "fragment_membership": memberships, "status": status,
            "reason": reason, "boundary_flags": boundary,
            "unassigned_band_refs": list(refs)}


def build():
    if not FULL_CONTEXT_INSPECTED:
        raise ValueError("Actual complete source reading not yet recorded")
    before = inputs()
    script_pin = pin(Path(__file__))
    accounted = [x for block in RAW_BLOCKS
                 for x in range(block["columns"][0], block["columns"][1] + 1)]
    if accounted != list(range(218, 332)):
        raise ValueError("Context blocks do not cover exactly once in order")
    expanded = {route: {x: [] for x in range(220, 330)} for route in ATTRIBUTED}
    reasons = {route: {x: [] for x in range(220, 330)} for route in ATTRIBUTED}
    for route, literals in ATTRIBUTED.items():
        for first, last, fragment, core, fringe, reason in literals:
            if not 220 <= first <= last < 330:
                raise ValueError("Literal x outside target")
            for x in range(first, last + 1):
                expanded[route][x].append((fragment, core, fringe))
                reasons[route][x].append(reason)
    bands = []
    refs = {route: {x: [] for x in range(220, 330)} for route in ATTRIBUTED}
    for x, band_id, candidates, fragment, core, fringe, reason in UNASSIGNED:
        if candidates not in (["solid"], ["dash"], ["solid", "dash"]) or not 220 <= x < 330:
            raise ValueError("Invalid unassigned band")
        item = record(x, [(fragment, core, fringe)], reason)
        item.update(band_id=band_id, candidate_routes=candidates, status="identity_conflict")
        bands.append(item)
        for route in candidates:
            refs[route][x].append(band_id)
    routes = {}
    for route in expanded:
        routes[route] = []
        for x in range(220, 330):
            reason = "; ".join(reasons[route][x]) or (
                "Inspected complete context column; no uniquely attributable F7 "
                + route + " cells selected. This is not zero force or model absence."
            )
            if refs[route][x]:
                reason += " Candidate ownership remains in the referenced separate band."
            routes[route].append(record(x, expanded[route][x], reason, refs[route][x]))
    for x in range(220, 330):
        seen = set()
        for item in [routes["solid"][x-220], routes["dash"][x-220]] + [b for b in bands if b["x"] == x]:
            selected = set(item["core"]) | set(item["fringe"])
            if seen & selected:
                raise ValueError("Shared cell between routes or bands")
            seen |= selected
    result = {"region_id": "F7-Im2-early", "pair": "F7", "source": "Im2.jpg",
              "reader": "peer", "target_box": TARGET, "context_box": CONTEXT,
              "inputs": before, "script_pin": script_pin,
              "coverage": {"full_context_inspected": True, "raw_context_cells": 10032,
                           "raw_blocks": RAW_BLOCKS, "actual_views": ACTUAL_VIEWS,
                           "prior_knowledge": PRIOR_KNOWLEDGE, "rows": [0, 87],
                           "uncompleted_context": [],
                           "display_convention": "Only exact (255,255,255) omitted; gN=N,N,N; inclusive equal-RGB runs."},
              "routes": routes, "unassigned_bands": bands,
              "human_accepted": False, "physical_support": None}
    if inputs() != before or pin(Path(__file__)) != script_pin:
        raise ValueError("Inputs/script changed during expansion")
    return result


if __name__ == "__main__":
    result = build()
    output = HERE / "reader-peer.json"
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")
    if inputs() != result["inputs"] or pin(Path(__file__)) != result["script_pin"]:
        raise ValueError("Changed input after save; retain failed output")
    print(json.dumps({"output": str(output), "pin": pin(output),
                      "route_records": sum(map(len, result["routes"].values())),
                      "unassigned_bands": len(result["unassigned_bands"])}))
