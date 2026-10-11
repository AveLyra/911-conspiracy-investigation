"""Frozen PRIMARY manual source selections; expansion never reads or classifies RGB."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIR = "F5"
SOURCE = "Im3.jpg"
TARGET = [310,0,425,88]
CONTEXT = [308,0,427,88]
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
SOLID = [[317,[0],[1]],[318,[0,1],[2]],[319,[0,1,2],[3]],[320,[2],[1,3,4]],[321,[2,3],[4,5]],[322,[3,4],[2,5,6]],[323,[4,5,6],[3,7]],[324,[5,6],[4,7]],[325,[6,7],[5,8,9]],[326,[7,8,9],[6,10,11]],[327,[8,9,10],[7,11,12]],[328,[10,11],[9,12,13]],[329,[11,12,13],[10,14,15]],[330,[12,13,14,15],[11,16,17]],[331,[14,15,16],[13,17,18]],[332,[16,17],[14,15,18,19]],[333,[17,18,19],[16,20,21]],[334,[18,19,20],[17,21,22,23]],[335,[20,21],[19,22,23]],[336,[21,22,23],[20,24,25]],[337,[22,23,24,25],[21,26]],[338,[24,25,26],[23,27,28,29]],[339,[25,26,27],[24,28,29]],[340,[27,28,29],[26,30,31]],[341,[28,29,30,31],[27,32,33]],[342,[29,30,31,32],[28,33,34]],[343,[31,32,33],[30,34,35]],[344,[33,34,35],[32,36,37]],[345,[34,35,36,37],[33,38]],[346,[36,37,38],[35,39,40,41]],[347,[37,38,39],[36,40,41]],[348,[39,40,41],[38,42,43,44]],[349,[40,41,42],[39,43,44]],[350,[42,43,44],[41,45,46]],[351,[43,44,45],[42,46,47]],[352,[44,45,46,47],[43,48,49,50]],[353,[46,47,48],[45,49,50,51]],[354,[48,49,50],[47,51,52,53]],[355,[49,50,51,52],[48,53,54,55]],[356,[51,52,53],[50,54,55,56]],[357,[53,54,55],[52,56,57]],[358,[54,55,56],[53,57,58,59]],[359,[56,57,58],[54,55,59,60]],[360,[57,58,59],[56,60,61]],[361,[59,60,61],[58,62,63]],[362,[60,61,62],[59,63,64,65,66]],[363,[62,63,64],[61,65,66,67]],[364,[63,64,65,66],[62,67,68,69]],[365,[65,66,67],[64,68,69,70,71]],[366,[66,67,68,69],[65,70,71]],[367,[68,69,70],[67,71,72]],[368,[70,71,72],[69,73,74,75]],[369,[72,73,74],[70,71,75,76]],[370,[73,74,75],[72,76,77,78]],[371,[74,75,76,77],[73,78,79,80]],[372,[76,77,78,79],[75,80,81]],[373,[78,79,80],[77,81,82,83]],[374,[80,81,82],[79,83,84]],[375,[81,82,83,84],[80,85,86,87]],[376,[83,84,85],[82,86,87]],[377,[85,86,87],[84]],[378,[86,87],[85]],[379,[],[87]]]
DASH = [[368,[4,5],[3,6],"B"],[369,[4,5],[3,6],"B"],[370,[4,5,6],[3],"B"],[371,[5,6,7],[4,8],"B"],[372,[],[6,7],"B"],[372,[10,11],[9],"C"],[373,[10,11,12,13],[9,14],"C"],[374,[12,13,14,15],[11,16],"C"],[375,[14,15,16],[13,17],"C"],[376,[],[15,16],"C"],[378,[],[18,19],"D"],[379,[18,19],[17,20],"D"],[380,[18,19,20],[17,21,22],"D"],[381,[19,20,21],[18,22,23],"D"],[382,[20,21],[19,22,23],"D"],[383,[21,22],[20,23],"D"],[384,[22,23],[21,24],"D"],[385,[22],[21,23],"D"],[387,[26,27],[25,28],"E"],[388,[26,27,28,29],[30,31,32],"E"],[389,[28,29,30,31],[27,32,33],"E"],[390,[31,32],[30,33],"E"],[391,[35,36],[34],"F"],[395,[44,45,46],[47,48],"G"],[396,[44,45,46,47,48],[49,50],"G"],[397,[46,47,48,49,50],[45,51],"G"],[398,[49,50],[48,51],"G"],[398,[54,55],[53,56],"H"],[399,[54,55,56,57,58],[53,59],"H"],[400,[56,57,58,59,60],[54,55,61],"H"],[401,[],[58,59,60],"H"],[401,[63],[62,64,65],"I"],[402,[64,65,66],[63,67],"I"],[403,[66,67],[65],"I"],[414,[],[86,87],"K"],[415,[86,87],[],"K"],[416,[],[86,87],"K"]]
# x, core, fringe, candidate route, explanation. These cells appear only once.
BANDS = [[361,[],[0,1],"dash","Cross-color top-edge material; red/blue attribution unresolved."],[362,[0,1,2],[3],"dash","Dark mixed red-blue contact at clipped top; no unique blue ownership."],[363,[0,1,2],[3],"dash","Mixed red-blue contact; tentative blue-bearing footprint retained once without assigned dash body."],[364,[],[1,2,3],"dash","Mixed-color termination beside red; no unique blue dash-body attribution."],[367,[],[4,5,6],"dash","Red-blue mixture preceding separated blue body; no continuity across the color contact."],[391,[],[37,38],"dash","Blue-bearing edge approaches red material; exact mixed ownership unresolved."],[392,[36,37,38],[35,39,40],"dash","Blue/red intersection; selected visible mixed ink is kept once, not transferred into a joined dash route."],[393,[38,39,40,41],[37,42],"dash","Red-blue intersection has no uniquely attributable blue dash cells."],[394,[],[37,38,39,40,41,42],"dash","Pale mixed contact material may belong to red and/or nearby blue pieces; no body continuation asserted."],[403,[],[68,69],"dash","Terminal blue-bearing material is mixed with neighboring red; body membership unresolved."],[404,[],[68,69],"dash","Pale purple termination not uniquely attributable."],[404,[73,74,75],[72,76],"dash","New mixed blue/red ink near descending routes; no unique dash body assignment."],[405,[72,73,74,75,76],[77,78],"dash","Blue/red superposition; selected mixed ink retained only once."],[406,[74,75,76,77,78],[73,79],"dash","Blue/red superposition; no route continuation inferred across shared ink."],[407,[77,78,79],[76,80,81,82],"dash","Mixed purple/red material separates into pale edges with unresolved blue ownership."],[408,[81,82,83],[80,84,85],"dash","Mixed contact with blue-bearing lower edge; no transferred identity."],[409,[82,83,84,85],[81,86,87],"dash","Mixed red/blue material; shell-body boundary unresolved."],[410,[84,85,86],[83,87],"dash","Mixed-color lower-edge contact; target truncates possible continuation."],[411,[85,86,87],[],"dash","Mixed purple/blue ink at bottom boundary, continuation unobserved."],[412,[87],[85,86],"dash","Mixed-color bottom truncation; no observed continuation."],[413,[],[87],"dash","Pale mixed fringe at bottom boundary, exact blue attribution unresolved."]]
BLOCKS = [[308,315,"fee342"],[316,323,"b9a942"],[324,331,"1d94be"],[332,339,"d59d43"],[340,347,"9f6bbe"],[348,355,"329e4b"],[356,363,"b4c9cd"],[364,371,"d8cfd5"],[372,379,"717aca"],[380,387,"98ecfc"],[388,395,"806237"],[396,403,"b18296"],[404,411,"0f8984"],[412,419,"0738c4"],[420,426,"5b225a"]]

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
            "raw_context_cells":10472,
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

