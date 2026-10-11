"""Versioned F7 peer completion: literal expansion only, never RGB selection.

Old literals and history are imported from the hash-pinned partial script,
not edited or reselected. New literals are confined to x298..329.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import tempfile

HERE = Path(__file__).resolve().parent
EXPECTED_INPUTS = {
    "../../HUMAN-REVIEW-GATE.md": {
        "bytes": 2733,
        "sha256": "5c739ea10b6fe51b719a10205cef52737ff74cc29d1431272dd5dfea90d92c71"
    },
    "../../HUMAN-SAMPLE-SELECTION.md": {
        "bytes": 7783,
        "sha256": "0fc9d115306ed9f429603ee5a4a52b016385ee232012982e28c16b0189509bdb"
    },
    "../../NUMERICAL-PROTOCOL.md": {
        "bytes": 6688,
        "sha256": "e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3"
    },
    "../../PROTOCOL.md": {
        "bytes": 4432,
        "sha256": "1ec6fedc9110f9ef2001f69fd1e13ad3a316a904f057345af26a0118d3216e19"
    },
    "../../native-strips01/Im2.jpg": {
        "bytes": 10754,
        "sha256": "9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9"
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
    "../force56-remainder/PROTOCOL.md": {
        "bytes": 4079,
        "sha256": "1ad63b566212539b9a7011650264d0ac427357fc5d9042670eea6d750fcabedc"
    },
    "../force56-remainder/READERS.md": {
        "bytes": 3332,
        "sha256": "e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f"
    },
    "../read_context.py": {
        "bytes": 4951,
        "sha256": "da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18"
    },
    "COMPLETION-V2.md": {
        "bytes": 5957,
        "sha256": "6d68e22e1410c76302e135a5b73adffde1374bcc51699225133400c9fc69ab4a"
    },
    "PROTOCOL.md": {
        "bytes": 7163,
        "sha256": "aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19"
    },
    "READERS.md": {
        "bytes": 2467,
        "sha256": "d62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417"
    },
    "context01.json": {
        "bytes": 1233648,
        "sha256": "ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f"
    },
    "context02.json": {
        "bytes": 1233648,
        "sha256": "ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f"
    },
    "peer-reread-2026-10-08.md": {
        "bytes": 7121,
        "sha256": "39368d4316acf06f53a7dfd4ed96eaecf45667d858ea4327c6b64b58b33a08d2"
    },
    "read_context.py": {
        "bytes": 4894,
        "sha256": "826e1bc24904d631b0b613ceea73b6ddc14b228438e77db751f291a60c717599"
    },
    "reader-peer.py": {
        "bytes": 15870,
        "sha256": "3d4bf1e066755d0242f287ef02b48a40fc6f27a28941953471e089214c00d98b"
    },
    "report.md": {
        "bytes": 3310,
        "sha256": "6e8477bd2a5c270cdec40b2652bb55523f7c905418bd335401516e8334194d42"
    },
    "validation.md": {
        "bytes": 8322,
        "sha256": "930ebe0d208d19e6c1a544da9a764a748db7fc9a1d2c53456d444f931c8ff11b"
    }
}
ACCEPTED_REREAD = [
    {
        "columns": [
            298,
            301
        ],
        "receipt": "Accepted additive reread exec chunk d474ca; exit 0; 916 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            302,
            305
        ],
        "receipt": "Accepted additive reread exec chunk 40b579; exit 0; 997 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            306,
            309
        ],
        "receipt": "Accepted additive reread exec chunk b7c011; exit 0; 1058 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            310,
            313
        ],
        "receipt": "Accepted additive reread exec chunk 2c0d62; exit 0; 1016 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            314,
            317
        ],
        "receipt": "Accepted additive reread exec chunk e96824; exit 0; 918 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            318,
            321
        ],
        "receipt": "Accepted additive reread exec chunk f42f99; exit 0; 1051 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            322,
            325
        ],
        "receipt": "Accepted additive reread exec chunk 7d4175; exit 0; 933 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            326,
            329
        ],
        "receipt": "Accepted additive reread exec chunk a30639; exit 0; 1024 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    },
    {
        "columns": [
            330,
            331
        ],
        "receipt": "Accepted additive reread exec chunk a3fb37; exit 0; 517 reported tokens; complete beginning/end read; untruncated; peer-reread-2026-10-08.md"
    }
]
REPEATED_RAW_BLOCKS = [
    {
        "columns": [
            298,
            301
        ],
        "receipt": "V2 fresh reread exec chunk e9420f; exit 0; 916 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            302,
            305
        ],
        "receipt": "V2 fresh reread exec chunk c3e923; exit 0; 997 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            306,
            309
        ],
        "receipt": "V2 fresh reread exec chunk 6f0bb3; exit 0; 1058 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            310,
            313
        ],
        "receipt": "V2 fresh reread exec chunk 19702d; exit 0; 1016 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            314,
            317
        ],
        "receipt": "V2 fresh reread exec chunk acb78b; exit 0; 918 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            318,
            321
        ],
        "receipt": "V2 fresh reread exec chunk 137b56; exit 0; 1051 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            322,
            325
        ],
        "receipt": "V2 fresh reread exec chunk 826fb8; exit 0; 933 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            326,
            329
        ],
        "receipt": "V2 fresh reread exec chunk a78f38; exit 0; 1024 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    },
    {
        "columns": [
            330,
            331
        ],
        "receipt": "V2 fresh reread exec chunk 751164; exit 0; 517 reported tokens; full stated bounds read; untruncated; exec budget 4000, enclosing budget 10000"
    }
]

# Manually selected inclusive x runs. No source pixels are opened by this code.
# first,last,fragment_id,core,fringe,reason
ADDED_ATTRIBUTED = {"solid": [], "dash": [
    (298,298,"peer-D10",[],[34,35,36],"Pale lower cap of the already recorded D10; fringe only, not joined to the next body."),
    (299,299,"peer-D11",[],[30,31,32,33,34],"Pale onset of a distinguishable next broken body; tentative attribution only."),
    (300,300,"peer-D11",[31,32],[30,33,34],"Green broken body with a darker center and pale surrounding cells."),
    (301,301,"peer-D11",[30,31,32],[29,33,34],"Distinct green local body below the red stroke."),
    (302,302,"peer-D11",[30,31],[29,32,33],"Green broken body; pale outer rows retained."),
    (303,303,"peer-D11",[30,31],[32,33],"Green body retained; the mixed-color upper edge is separately unassigned."),
    (304,304,"peer-D11",[30,31],[32],"Green body near red material; upper mixed edge not assigned to this route."),
    (305,305,"peer-D11",[31],[30,32,33],"Fading green local body; upper mixed-color edge retained separately."),
    (306,306,"peer-D11",[],[31,32,33],"Pale cap below red; no confidently attributable core and no contact bridge."),
    (308,308,"peer-D12",[],[24,25,26],"Tentative new upper green piece at the red contact; mixed lower cells remain unassigned."),
    (309,309,"peer-D12",[25,26],[24],"Visible green portion above the red contact; mixed lower edge separately unassigned."),
    (310,310,"peer-D12",[24,25,26],[23,27],"Green broken body clearly above the red stroke."),
    (311,311,"peer-D12",[23,24,25],[22,26],"Green body and pale outer rows; native bend retained."),
    (312,312,"peer-D12",[23,24],[22,25,26],"Muted green body approaching its local cap."),
    (313,313,"peer-D12",[],[23,24,25],"Pale green cap retained as fringe only."),
    (315,315,"peer-D13",[],[21,22,23,24],"Tentative onset of the next broken body after an unresolved pale gap column."),
    (316,316,"peer-D13",[21,22,23],[20,24],"New green body and its pale outer rows."),
    (317,317,"peer-D13",[21,22],[20,23,24],"Green broken stroke above red."),
    (318,318,"peer-D13",[20,21,22],[19,23],"Local green body with surrounding pale cells."),
    (319,319,"peer-D13",[20,21],[19,22,23],"Green body fading toward a muted cap."),
    (320,320,"peer-D13",[20,21],[19,22,23],"Muted green local body; no interpolated centerline."),
    (321,321,"peer-D13",[],[19,20,21,22],"Gray-green cap is only tentatively assigned; no confident core."),
    (322,322,"peer-D13",[],[19,20,21],"Lower pale cap kept separate from the next higher broken body."),
    (323,323,"peer-D14",[],[15,16,17,18],"Tentative higher onset of a new broken body, not joined to D13."),
    (324,324,"peer-D14",[14,15,16],[13,17,18],"New green broken stroke and pale outer cells."),
    (325,325,"peer-D14",[13,14,15],[12,16,17],"Green broken body approaches the upper mixed-color neighborhood."),
    (326,326,"peer-D14",[12,13],[11,14,15],"Green body center with yellow-green tentative edge cells."),
    (327,327,"peer-D14",[12,13],[11,14],"Green local body below the separate top-edge red/green neighborhood."),
    (328,328,"peer-D14",[],[12,13,14],"Muted green cap retained as fringe only; top-edge solid-candidate band is separate."),
]}
# x,band_id,candidate_routes,fragment_id,core,fringe,reason
ADDED_UNASSIGNED = [
    (303,"peer-B303-edge",["dash"],"peer-U11edge",[],[29],"Pale mixed red/green edge between the red stroke and D11; unique F7 ownership unresolved."),
    (304,"peer-B304-edge",["dash"],"peer-U11edge",[],[29],"Yellow/red-green upper edge may contain D11 contribution; kept once and unassigned."),
    (305,"peer-B305-edge",["dash"],"peer-U11edge",[],[29],"Mixed upper edge next to D11 is not uniquely attributable."),
    (307,"peer-B307-contact",["dash"],"peer-U11-12-contact",[],[26,27,28,29,30,31],"Red/green contact neighborhood between broken bodies; neither hidden F7 membership nor through-contact continuity established."),
    (308,"peer-B308-edge",["dash"],"peer-U12edge",[],[27,28],"Brown mixed lower edge at red/green contact; distinct from tentative upper D12 cells."),
    (309,"peer-B309-edge",["dash"],"peer-U12edge",[],[27,28],"Mixed green/brown and red edge below the green body; ownership unresolved."),
    (314,"peer-B314-gap",["dash"],"peer-Ugap12-13",[],[22,23,24],"Pale green gap neighborhood has unresolved D12/D13 membership; no gap bridge."),
    (328,"peer-B328-top",["solid"],"peer-Usolid-top",[],[0,1],"Top-clipped brown red/green mixture may contain the approaching green solid; no unique solid assignment."),
    (329,"peer-B329-top",["solid"],"peer-Usolid-top",[],[0,1,2],"Top/right-clipped mixed-color material precedes clear green solid in context only; not an attributed continuation."),
    (329,"peer-B329-dash-contact",["dash"],"peer-U14contact",[],[10,11,12,13,14,15],"Separate lower red/green cap-contact neighborhood at target right; D14 contribution remains unresolved and is not bridged."),
]


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def inputs():
    observed = {name: pin(HERE / name) for name in EXPECTED_INPUTS}
    if observed != EXPECTED_INPUTS:
        raise ValueError("Frozen input changed; preserve failed attempt")
    for name in ("context01.json", "context02.json"):
        context = json.loads((HERE / name).read_text())
        if any(EXPECTED_INPUTS.get(key) != value
               for key, value in context["inputs"].items()):
            raise ValueError("Missing or inconsistent transitive context pin")
    return observed


def partial_module():
    inputs()  # Verify the old source before importing it.
    path = HERE / "reader-peer.py"
    spec = importlib.util.spec_from_file_location("f7_preserved_peer_partial", path)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    if base.FULL_CONTEXT_INSPECTED is not False or base.EXPECTED_INPUTS != {}:
        raise ValueError("Old incomplete state unexpectedly changed")
    if any(last > 297 for values in base.ATTRIBUTED.values()
           for first, last, *_ in values) or any(row[0] > 297 for row in base.UNASSIGNED):
        raise ValueError("Old literal coverage unexpectedly changed")
    return base


def expand(base, attributed, unassigned):
    expanded = {route: {x: [] for x in range(220, 330)} for route in ("solid", "dash")}
    reasons = copy.deepcopy(expanded)
    for route, literals in attributed.items():
        for first, last, fragment, core, fringe, reason in literals:
            if not 220 <= first <= last < 330:
                raise ValueError("Literal outside target")
            for x in range(first, last + 1):
                expanded[route][x].append((fragment, core, fringe))
                reasons[route][x].append(reason)
    bands = []
    refs = {route: {x: [] for x in range(220, 330)} for route in expanded}
    seen_ids = set()
    for x, band_id, candidates, fragment, core, fringe, reason in unassigned:
        if (candidates not in (["solid"], ["dash"], ["solid", "dash"])
                or not 220 <= x < 330 or band_id in seen_ids):
            raise ValueError("Invalid band or duplicate band ID")
        seen_ids.add(band_id)
        item = base.record(x, [(fragment, core, fringe)], reason)
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
            routes[route].append(base.record(x, expanded[route][x], reason, refs[route][x]))
    for x in range(220, 330):
        seen = set()
        for item in [routes["solid"][x-220], routes["dash"][x-220]] + [b for b in bands if b["x"] == x]:
            selected = set(item["core"]) | set(item["fringe"])
            if seen & selected:
                raise ValueError("Shared cell between routes/bands")
            seen |= selected
    return routes, bands


def build():
    before = inputs()
    script_pin = pin(Path(__file__))
    base = partial_module()
    attributed = {route: copy.deepcopy(base.ATTRIBUTED[route]) + ADDED_ATTRIBUTED[route]
                  for route in ("solid", "dash")}
    unassigned = copy.deepcopy(base.UNASSIGNED) + ADDED_UNASSIGNED
    if any(first < 298 for values in ADDED_ATTRIBUTED.values()
           for first, *_ in values) or any(row[0] < 298 for row in ADDED_UNASSIGNED):
        raise ValueError("New literals encroach on preserved columns")
    routes, bands = expand(base, attributed, unassigned)
    old_routes, old_bands = expand(base, base.ATTRIBUTED, base.UNASSIGNED)
    if (any(routes[route][:78] != old_routes[route][:78] for route in routes)
            or [row for row in bands if row["x"] <= 297] != old_bands):
        raise ValueError("Preserved literal expansion changed")
    raw_blocks = copy.deepcopy(base.RAW_BLOCKS) + ACCEPTED_REREAD
    if [x for b in raw_blocks for x in range(b["columns"][0], b["columns"][1]+1)] != list(range(218,332)):
        raise ValueError("Primary coverage must account for context exactly once")
    result = {
        "region_id": "F7-Im2-early", "pair": "F7", "source": "Im2.jpg", "reader": "peer",
        "target_box": [220,0,330,88], "context_box": [218,0,332,88],
        "inputs": before, "script_pin": script_pin,
        "coverage": {
            "full_context_inspected": True, "raw_context_cells": 10032,
            "raw_blocks": raw_blocks, "repeated_raw_blocks": REPEATED_RAW_BLOCKS,
            "actual_views": copy.deepcopy(base.ACTUAL_VIEWS) + [
                {"path": "../../native-strips01/Im2.jpg",
                 "receipt": "V2 repeat: functions.exec label F7-v2-whole-native, view_image detail original; entire 741x88 displayed; no opaque image receipt returned."},
                {"path": "../../render01/page-076.png",
                 "receipt": "V2 repeat: same functions.exec label F7-v2-composed-page, view_image detail original; complete 1700x2200 page displayed resized to 1376x1780; orientation only, not coordinate selection."},
            ],
            "prior_knowledge": base.PRIOR_KNOWLEDGE + (
                " V2 resumes my own preserved partial and coordinator-reviewed additive reread. "
                "New selections x298..329 use fresh finite rereads, not recollection from receipts. "
                "Original 218..297 literals are unchanged. Both rejected completion saves and "
                "disputed earlier displays remain rejected; the additive reread does not certify them."
            ),
            "rows": [0,87], "uncompleted_context": [],
            "counterpart_new_annotations_read": False,
            "display_convention": "Only exact (255,255,255) omitted; gN=N,N,N; inclusive equal-RGB runs.",
            "rejected_history": "Preserved report.md and validation.md; not counted as valid reading receipts.",
        },
        "routes": routes, "unassigned_bands": bands,
        "human_accepted": False, "physical_support": None,
    }
    if inputs() != before or pin(Path(__file__)) != script_pin:
        raise ValueError("Inputs/script changed during expansion")
    return result


def save_exclusive(path, result):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write("\n")


def self_test():
    base = partial_module()
    checks = 0
    row = base.record(329, [("s", [0], [1])], "synthetic")
    assert row["boundary_flags"] == ["target_right", "target_top"]
    assert row["status"] == "boundary_truncated"
    checks += 2
    row = base.record(300, [], "synthetic", ["b"])
    assert row["status"] == "identity_conflict" and row["fragment_membership"] == []
    checks += 1
    for core, fringe in [([2,1], []), ([1,1], []), ([True], []), ([-1], []), ([88], []), ([1],[1])]:
        try:
            base.record(300, [("s", core, fringe)], "synthetic")
        except ValueError:
            checks += 1
        else:
            raise AssertionError("Invalid synthetic cells accepted")
    try:
        expand(base, {"solid": [(300,300,"s",[1],[],"synthetic")], "dash": []},
               [(300,"b",["dash"],"u",[],[1],"synthetic")])
    except ValueError:
        checks += 1
    else:
        raise AssertionError("Shared cell accepted")
    with tempfile.TemporaryDirectory(prefix="f7-peer-v2-synthetic-") as tmp:
        target = Path(tmp)/"synthetic.json"
        save_exclusive(target, {"synthetic": True})
        frozen = target.read_bytes()
        try:
            save_exclusive(target, {"synthetic": False})
        except FileExistsError:
            assert target.read_bytes() == frozen
            checks += 1
        else:
            raise AssertionError("Overwrite accepted")
    inputs()
    print(json.dumps({"synthetic_checks": checks, "passed": True}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("self-test", "check", "save"))
    args = parser.parse_args()
    if args.mode == "self-test":
        self_test()
    else:
        result = build()
        if args.mode == "save":
            output = HERE / "reader-peer-v2.json"
            save_exclusive(output, result)
            if inputs() != result["inputs"] or pin(Path(__file__)) != result["script_pin"]:
                raise ValueError("Changed after save; preserve failed output")
            print(json.dumps({"output": str(output), "pin": pin(output),
                              "route_records": sum(map(len, result["routes"].values())),
                              "unassigned_bands": len(result["unassigned_bands"])}))
        else:
            print(json.dumps({"checked": True, "route_records": sum(map(len, result["routes"].values())),
                              "unassigned_bands": len(result["unassigned_bands"]),
                              "preserved_columns": [220,297], "new_literal_columns": [298,329],
                              "input_count": len(result["inputs"]), "script_pin": result["script_pin"]}))

