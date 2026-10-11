"""Frozen PRIMARY manual source selections; expansion never reads or classifies RGB."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIR = "F6"
SOURCE = "Im1.jpg"
TARGET = [270,55,340,88]
CONTEXT = [268,53,342,88]
PINS = {
  "../../native-strips01/Im1.jpg": {
    "bytes": 9292,
    "sha256": "929f5d00d2f9ab1eba27a4aad8af37320a4fd37f2455f9b51d750ec7e15e8139"
  },
  "../../native-strips01/Im3.jpg": {
    "bytes": 13212,
    "sha256": "af735345f189bba0eab7a836c5c0c6221ab30055febd81b52b331821fe87259b"
  },
  "../../render01/page-076.png": {
    "bytes": 943120,
    "sha256": "0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6"
  },
  "../PROTOCOL.md": {
    "bytes": 5438,
    "sha256": "2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd"
  },
  "../approach34/read_context.py": {
    "bytes": 5071,
    "sha256": "384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3"
  },
  "../read_context.py": {
    "bytes": 4951,
    "sha256": "da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18"
  },
  "PROTOCOL-V2.md": {
    "bytes": 1365,
    "sha256": "181a5eda9115ffedd282ae1e83b05c55a07659d6e44b44378b2101388d458b28"
  },
  "PROTOCOL.md": {
    "bytes": 4079,
    "sha256": "1ad63b566212539b9a7011650264d0ac427357fc5d9042670eea6d750fcabedc"
  },
  "READERS.md": {
    "bytes": 3332,
    "sha256": "e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f"
  },
  "read_context.py": {
    "bytes": 4421,
    "sha256": "7eb45a46ea63716e20b9b00dcc7b4757f6a3c021e25cc0c170c97e5cab46951b"
  },
  "read_context_v2.py": {
    "bytes": 3898,
    "sha256": "02bf4d365183f458ba3577a18ff638526a0c63e2742ec05b26c256cd1967e829"
  },
  "context01.json": {
    "sha256": "6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5",
    "bytes": 1606454
  },
  "context02.json": {
    "sha256": "6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5",
    "bytes": 1606454
  },
  "../approach34/reader-E3-primary.py": {
    "sha256": "02db3fc58aa93e1bd5f83e47d6a86d6cdf2f86815061075fc18d2b9087b7df5d",
    "bytes": 9690
  },
  "../../remaining-route-inventory/reader-root.json": {
    "sha256": "4cf6791b358e89b19a47adfe0402d6825168a15b0060aea48d43e4eda4d22981",
    "bytes": 30190
  },
  "../../remaining-route-inventory/force-reconciliation.json": {
    "sha256": "9cb2c2003ab6eb014a665f1657fa2858dec9dffc383fbaa9e6e1fcef227e1222",
    "bytes": 2519
  },
  "../../../../../../../911/research/sherlock-wtc7-investigation/CHARTER.md": {
    "sha256": "54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd",
    "bytes": 24068
  },
  "../../../../../../../911/AGENTS.md": {
    "sha256": "934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857",
    "bytes": 15240
  },
  "../../../../../../../911/WORKFLOW.md": {
    "sha256": "17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a",
    "bytes": 5868
  },
  "../../../../../../../911/START-HERE.md": {
    "sha256": "b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560",
    "bytes": 6383
  },
  "../../../../../../../../.codex/skills/evidence-falsification-auditor/SKILL.md": {
    "sha256": "7894e7c6150319ec9591ec39ee1d11c3687f37deaf494d8a7c97b515f29c48a2",
    "bytes": 4215
  },
  "../../../../../../../../.codex/skills/source-of-truth-guardian/SKILL.md": {
    "sha256": "d283182d3b1f493001ad8952102ff70ebf4d7d0575cbfa1891a38df80e313ab5",
    "bytes": 4218
  }
}
# Literal manually selected native cells. Each tuple is x, core, fringe[, local body].
SOLID = []
DASH = [[283,[87],[86],"A"],[284,[86,87],[85],"A"],[285,[85,86,87],[84],"A"],[286,[84,85],[83,86,87],"A"],[287,[83,84],[82,85],"A"],[288,[83],[82,84],"A"],[291,[81,82],[80,83],"B"],[292,[81],[80,82],"B"],[293,[80,81],[79,82],"B"],[294,[78,79,80],[77,81],"B"],[295,[77,78,79],[76,80],"B"],[296,[77],[76,78],"B"],[298,[73,74],[75],"C"],[299,[73,74],[72,75],"C"],[300,[73,74],[72,75],"C"],[301,[73,74],[72,75],"C"],[302,[73,74],[72,75],"C"],[303,[73],[74,75],"C"],[306,[68],[67,69],"D"],[307,[66,67,68],[65,69],"D"],[308,[65,66,67],[64,68],"D"],[309,[65,66],[64,67],"D"],[310,[65,66],[64,67],"D"],[311,[66],[65,67],"D"],[312,[],[66,67],"D"],[313,[],[69,70],"E"],[314,[70,71],[69,72],"E"],[315,[70,71,72],[69,73],"E"],[316,[71,72,73],[70,74],"E"],[317,[72,73,74],[71,75],"E"],[318,[73,74,75],[72,76],"E"],[319,[74,75],[73,76],"E"],[320,[75],[74,76],"E"],[322,[],[77,78],"F"],[323,[77,78],[76,79],"F"],[324,[77,78,79,80],[76,81],"F"],[325,[79,80,81],[78],"F"],[326,[81,82],[80,83],"F"]]
# x, core, fringe, candidate route, explanation. These cells appear only once.
BANDS = [[303,[],[71,72],"dash","Red and green near-contact produces brown edge cells with unresolved red ownership."],[304,[72],[73],"dash","Mixed red/green termination; no continuous red path across the contact inferred."],[325,[],[82,83],"dash","Red fringe meets green ink; exact mixed ownership unresolved."],[326,[],[85,86,87],"dash","Separate bottom mixed red-green ink cannot be allocated uniquely to a red dash body."],[327,[86,87],[85],"dash","Brown red-green contact at bottom target edge; no unique red membership."],[328,[],[86,87],"dash","Green-dominant/brown edge cells may retain red contact fringe; kept unresolved, not connected."]]
BLOCKS = [[268,275,"37a7fa"],[276,283,"76b380"],[284,291,"6444aa"],[292,299,"7f9fd6"],[300,307,"ae04e9"],[308,315,"d192cc"],[316,323,"55d566"],[324,331,"c0c8b5"],[332,341,"ec5112"]]

def pin(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

def inputs():
    actual = {name: pin(HERE/name) for name in PINS}
    if actual != PINS:
        raise ValueError("A frozen input changed")
    for name in ("context01.json", "context02.json"):
        context_inputs = json.loads((HERE/name).read_text())["inputs"]
        if any(actual.get(k) != v for k,v in context_inputs.items()):
            raise ValueError("Transitive context dependency omitted or changed")
    return actual

def flags(x, core, fringe):
    selected = set(core) | set(fringe)
    if not selected:
        return []
    result = []
    if x == TARGET[0]: result.append("target_left")
    if x == TARGET[2]-1: result.append("target_right")
    if TARGET[1] in selected: result.append("target_top")
    if TARGET[3]-1 in selected: result.append("target_bottom")
    return result

def record(x, members, reason, refs=None, conflict=False):
    core = sorted(y for m in members for y in m["core"])
    fringe = sorted(y for m in members for y in m["fringe"])
    bounds = flags(x, core, fringe)
    refs = refs or []
    status = ("identity_conflict" if conflict else
              "boundary_truncated" if bounds else
              "identity_conflict" if refs else
              "identified_local_fragment" if core else
              "fringe_only" if fringe else "no_attributable_cells")
    return {"x":x, "core":core, "fringe":fringe,
            "fragment_id": members[0]["fragment_id"] if len(members)==1 else None,
            "fragment_membership":members, "status":status, "reason":reason,
            "boundary_flags":bounds, "unassigned_band_refs":refs}

def validate(result):
    x0,y0,x1,y1 = TARGET
    seen = {}
    band_lookup = {(b["x"],b["band_id"]):b for b in result["unassigned_bands"]}
    for route,rows in result["routes"].items():
        if [r["x"] for r in rows] != list(range(x0,x1)):
            raise ValueError("Missing route column")
        for row in rows:
            wanted = [b["band_id"] for b in result["unassigned_bands"]
                      if b["x"]==row["x"] and route in b["candidate_routes"]]
            if row["unassigned_band_refs"] != wanted:
                raise ValueError("Nonreciprocal band references")
    for label,rows in list(result["routes"].items()) + [("unassigned",result["unassigned_bands"])]:
        for row in rows:
            c,f = row["core"],row["fringe"]
            if c != sorted(set(c)) or f != sorted(set(f)) or set(c)&set(f):
                raise ValueError("Classes not sorted, unique and disjoint")
            if not (x0 <= row["x"] < x1 and all(type(y) is int and y0 <= y < y1 for y in c+f)):
                raise ValueError("Cell outside target")
            mc = [y for m in row["fragment_membership"] for y in m["core"]]
            mf = [y for m in row["fragment_membership"] for y in m["fringe"]]
            if sorted(mc) != c or sorted(mf) != f:
                raise ValueError("Member union mismatch")
            if row["fragment_id"] != (row["fragment_membership"][0]["fragment_id"]
                                      if len(row["fragment_membership"])==1 else None):
                raise ValueError("Outer fragment mismatch")
            if row["boundary_flags"] != flags(row["x"],c,f):
                raise ValueError("Boundary flags")
            if not c and not f and row["unassigned_band_refs"] and row["status"]!="identity_conflict":
                raise ValueError("Empty conflict mislabeled")
            for y in c+f:
                key = row["x"],y
                if key in seen:
                    raise ValueError("A selected cell was duplicated")
                seen[key] = label
    coverage = [x for a,b,_ in BLOCKS for x in range(a,b+1)]
    if coverage != list(range(CONTEXT[0],CONTEXT[2])):
        raise ValueError("Raw column coverage")
    return result

def build():
    before = inputs()
    bands = []
    for i,(x,c,f,candidate,reason) in enumerate(BANDS):
        band_id = f"{PAIR}-primary-unassigned-{i:02d}"
        member = {"fragment_id":band_id, "core":c, "fringe":f}
        band = record(x,[member],reason,conflict=True)
        band.update(band_id=band_id,candidate_routes=[candidate],
                    other_possible_origins=["other-colored stroke","compression fringe"],
                    continuity_claim=False)
        bands.append(band)
    routes = {}
    for route,table in [("solid",SOLID),("dash",DASH)]:
        rows = []
        for x in range(TARGET[0],TARGET[2]):
            members = []
            for entry in table:
                if entry[0] != x:
                    continue
                _,c,f,*body = entry
                fragment = f"{PAIR}-primary-{route}-" + (body[0] if body else "A")
                members.append({"fragment_id":fragment,"core":c,"fringe":f})
            refs = [b["band_id"] for b in bands if b["x"]==x and route in b["candidate_routes"]]
            if members:
                reason = ("Locally identified blue solid descent; core and tentative fringe manually read."
                          if route=="solid" else
                          "Locally distinguishable broken stroke body; core and tentative fringe manually read. No gap bridge.")
                if len(members)>1:
                    reason += " Separate bodies in this column remain separate memberships."
            elif PAIR=="F6" and route=="solid":
                reason = ("No cells assigned to a solid red route after reading this column; observed red pieces have broken style, "
                          "and the earlier corrected inventory locates the solid crest in Im2. This is not model absence or zero.")
            else:
                reason = ("No route-specific cells attributed after reading this column. Other-colored strokes and "
                          "unassigned compression material do not supply missing curve cells; this is not physical absence or zero.")
            if refs:
                reason += " Unresolved same-column ink is referenced once, without assigning its body identity."
            row = record(x,members,reason,refs)
            if row["boundary_flags"]:
                row["reason"] += " Selected cells touch the target boundary, not a physical endpoint."
            rows.append(row)
        routes[route] = rows
    result = {
        "region_id":PAIR+"-"+SOURCE.split(".")[0], "pair":PAIR, "source":SOURCE,
        "reader":"primary", "target_box":TARGET, "context_box":CONTEXT,
        "inputs":before, "script_pin":pin(Path(__file__)),
        "coverage":{
            "full_context_inspected":True,
            "raw_context_cells":2590,
            "raw_blocks":[{"columns":[a,b],"receipt":receipt} for a,b,receipt in BLOCKS],
            "rows_covered":[CONTEXT[1],CONTEXT[3]-1],
            "display_convention":"Only exact (255,255,255) omitted; gN=(N,N,N); inclusive equal-RGB runs. No threshold.",
            "actual_views":[
                {"path":"../../native-strips01/Im3.jpg","receipt":None,"description":"Complete unchanged 741 by 88 strip through view_image in primary reader turn."},
                {"path":"../../native-strips01/Im1.jpg","receipt":None,"description":"Complete unchanged 741 by 88 strip through view_image in primary reader turn."},
                {"path":"../../render01/page-076.png","receipt":None,"description":"Complete composed page through view_image; displayed resized from 1700x2200 to 1376x1780, orientation only."}
            ],
            "view_receipt_limit":"view_image returned no chunk_id; actual command blocks have their returned chunk IDs above.",
            "prior_knowledge":"Prospective primary designation and fixed targets; full-strip/page orientation, both protocols, width correction, corrected earlier F5/F6 inventory and F6 location. An initial mistaken full prior-inventory dump was truncated and included other-pair excerpts; relevant F5/F6 entries were then fully read at f6b943. No current counterpart annotations read.",
            "uncompleted_context":[],
            "counterpart_new_annotation_read":False,
            "controls_receipt":"6f36ac",
            "controls_limit":"15 reused controls passed in this reader turn; coordinator had already saved the identical contexts after its controls."
        },
        "routes":routes, "unassigned_bands":bands,
        "human_accepted":False, "physical_support":None,
        "limits":"Native annotation confidence only, not calibrated pre-raster bounds. Bodies are local, with no seam join, smoothness-based bridge, hidden continuation or centerline. Mixed ink may have competing other-color origins; unassigned bands indicate this reader's uncertainty, not universal impossibility. No whole-curve discrepancy, causal conclusion or human acceptance."
    }
    validate(result)
    if inputs() != before:
        raise ValueError("Input changed during expansion")
    return result

if __name__=="__main__":
    result = build()
    target = HERE/f"reader-{PAIR}-primary.json"
    with target.open("x") as handle:
        json.dump(result,handle,indent=2,sort_keys=True,allow_nan=False)
        handle.write("\n")
    if inputs() != result["inputs"]:
        raise ValueError("Input changed after save; preserve this output as failed")
    print(json.dumps({"output":pin(target),"rows":sum(map(len,result["routes"].values())),
                      "bands":len(result["unassigned_bands"]),"human_accepted":False}))

