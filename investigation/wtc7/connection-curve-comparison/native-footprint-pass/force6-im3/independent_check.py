"""Independent finite F6-Im3 source, bookkeeping and comparison checker.

No producer, source-display helper or annotation module is imported. Native
row operations use truth-table scans; cross-pair operations use integer masks.
Bookkeeping portions adapt the pinned preceding independent checker. This is
an arithmetic/source audit, not a third perceptual reading or human acceptance.
"""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = HERE.parent / "force56-remainder"
SIZE = (741, 88)
TARGETS = {"F6": [145, 0, 440, 88], "F5": [310, 0, 425, 88]}
CONTEXTS = {"F6": [143, 0, 442, 88], "F5": [308, 0, 427, 88]}
ROLES = ("primary", "peer")
SCOPES = ("solid", "dash", "unassigned")
CLASSES = ("core", "fringe")
STATUSES = {"identified_local_fragment", "fringe_only", "no_attributable_cells",
            "identity_conflict", "boundary_truncated"}
SOURCE_SHA = "af735345f189bba0eab7a836c5c0c6221ab30055febd81b52b331821fe87259b"
CONTEXT_SHA = "8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024"
OLD_CONTEXT_SHA = "6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5"
REFERENCE_SHA = "326cd663a0e5bf8f9eefafb45d1421fa5f81056891a26228ad49168fc28665b0"
COMPATIBILITY_SHA = "6faa9f91d73199e10c76c5e0a522310510c85ee446a3184b8f70a55238741e5a"
MAIN_CHARTER = Path("/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md")
WORKTREE_CHARTER = (HERE / "../../../CHARTER.md").resolve()
FROZEN_READERS = {
    "reader-primary.json": "d53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9",
    "reader-peer.json": "ab84ccc41a395414982489c8ef4e9d874908a4e79c6b08a84a6d3c651ba32f42",
    "../force56-remainder/reader-F5-primary.json": "6ce861b44d73e09a88e3d79e754f7f2f41b9458a0baafb1630c22b2de3f2c2b3",
    "../force56-remainder/reader-F5-peer.json": "dbed8ae98651c5fc21a4a11e2d97c6897ed609eac809e20b1638e376246de5f4",
}
COMPARISON_SHA = "e6b1202512e0615e7f35bb4d7e843edfd9e73127278e12916c6ad11944103a02"
AUTHORITY_CONTEXT = {Path(path).resolve() for path in (
    "/Users/admin/docs/911/AGENTS.md", "/Users/admin/docs/911/START-HERE.md",
    "/Users/admin/docs/911/WORKFLOW.md",
    "/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md",
    "/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md",
    "/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md",
    "/Users/admin/.agents/skills/development-verification/SKILL.md",
    "/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/AGENTS.md",
    "/Users/admin/.codex/skills/evidence-falsification-auditor/references/claim-ledger-template.md",
    "/Users/admin/.codex/skills/source-of-truth-guardian/references/audit-checklist.md",
)} | {WORKTREE_CHARTER}
ENTRY_FIELDS = {"x", "core", "fringe", "fragment_id", "fragment_membership",
                "status", "reason", "boundary_flags", "unassigned_band_refs"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(first, second):
    return json.dumps(first, sort_keys=True, allow_nan=False) == json.dumps(second, sort_keys=True, allow_nan=False)


def load(path):
    return json.loads(Path(path).read_text())


def pin(path):
    raw = Path(path).read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def name(path):
    resolved = Path(path).resolve()
    if resolved not in AUTHORITY_CONTEXT:
        resolved.relative_to(BASE)
    return os.path.relpath(resolved, HERE)


def pin_schema(value):
    require(type(value) is dict and set(value) == {"bytes", "sha256"}, "pin schema")
    require(type(value["bytes"]) is int and value["bytes"] >= 0, "pin byte count")
    digest = value["sha256"]
    require(type(digest) is str and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), "pin digest")


def add_pin(pins, path, expected=None):
    key = name(path)
    observed = pin(HERE / key)
    if expected is not None:
        pin_schema(expected)
        require(exact(observed, expected), "declared dependency changed: " + key)
    require(key not in pins or exact(pins[key], observed), "conflicting dependency: " + key)
    pins[key] = observed
    return key


def dependency_closure(roots, pins):
    """Verify every declared JSON dependency recursively, with exact script pins."""
    queue = [add_pin(pins, path) for path in roots]
    visited = set()
    while queue:
        key = queue.pop(0)
        if key in visited or not key.endswith(".json"):
            continue
        visited.add(key)
        path = HERE / key
        data = load(path)
        require(type(data) is dict, "dependency JSON object required")
        if "inputs_after" in data:
            require(exact(data["inputs"], data["inputs_after"]), "dependency before/after differs: " + key)
        for field in ("inputs", "inputs_after", "input_pins", "dependencies"):
            if field not in data:
                continue
            require(type(data[field]) is dict, "dependency map required: " + key)
            for child, expected in data[field].items():
                require(type(child) is str, "dependency path string required")
                queue.append(add_pin(pins, path.parent / child, expected))
        if "script_pin" in data:
            require(path.name.startswith(("reader-", "comparison")), "unrecognized script pin: " + key)
            script = path.with_suffix(".py") if path.name.startswith("reader-") else path.parent / "compare.py"
            add_pin(pins, script, data["script_pin"])
        if "test_pin" in data:
            require(path.name.startswith("comparison"), "unrecognized test pin: " + key)
            add_pin(pins, path.parent / "test_compare.py", data["test_pin"])
    return sorted(visited)


def normalized_map(declared, directory=HERE):
    require(type(declared) is dict, "dependency map required")
    result = {}
    for child, expected in declared.items():
        pin_schema(expected)
        key = name(directory / child)
        require(key not in result or exact(result[key], expected), "conflicting normalized dependency aliases")
        result[key] = expected
    return result


def require_dependency_coverage(declared, required, directory=HERE):
    normalized = normalized_map(declared, directory)
    require(all(key in normalized and exact(normalized[key], expected) for key, expected in required.items()),
            "omitted or changed required transitive input")
    return normalized


def validate_image(image):
    require(image.mode == "RGB" and image.size == SIZE, "source must be 741 by 88 RGB")


def check_charter_copies(pins):
    for path in (MAIN_CHARTER, WORKTREE_CHARTER):
        add_pin(pins, path)
    require(MAIN_CHARTER.read_bytes() == WORKTREE_CHARTER.read_bytes(), "worktree charter differs from controlling main charter")


def context_records(records, box, image):
    validate_image(image)
    x0, y0, x1, y1 = box
    require(type(records) is list and len(records) == (x1-x0)*(y1-y0), "context coverage count")
    for index, row in enumerate(records):
        require(type(row) is dict and set(row) == {"x", "y", "rgb"}, "context row schema")
        x, y = x0 + index % (x1-x0), y0 + index // (x1-x0)
        require(type(row["x"]) is int and type(row["y"]) is int and (row["x"], row["y"]) == (x, y),
                "context exact row-major coordinates")
        require(type(row["rgb"]) is list and len(row["rgb"]) == 3 and
                all(type(value) is int and 0 <= value <= 255 for value in row["rgb"]), "context RGB schema")
        require(tuple(row["rgb"]) == image.getpixel((x, y)), "context/source RGB differs")


def check_overlap(new_records, old_records):
    indexed = {(row["x"], row["y"]): row for row in new_records}
    require(len(indexed) == len(new_records), "duplicate new-context coordinate")
    expected = [(x, y) for y in range(88) for x in range(308, 427)]
    require([(row["x"], row["y"]) for row in old_records] == expected, "old overlap coverage/order")
    require(all((row["x"], row["y"]) in indexed and exact(indexed[row["x"], row["y"]], row)
                for row in old_records), "old/new context overlap mismatch")
    return len(expected)


def check_contexts(pins):
    new_files = [HERE / f"context{index:02}.json" for index in (1, 2)]
    old_files = [OLD / f"context{index:02}.json" for index in (1, 2)]
    source = BASE / "native-strips01/Im3.jpg"
    require(pin(source)["sha256"] == SOURCE_SHA, "frozen Im3 source changed")
    dependency_closure(new_files + old_files, pins)
    add_pin(pins, source)
    with Image.open(source) as opened:
        validate_image(opened)
        image = opened.copy()
    require(new_files[0].read_bytes() == new_files[1].read_bytes(), "new contexts not byte-identical")
    require(old_files[0].read_bytes() == old_files[1].read_bytes(), "old contexts not byte-identical")
    new_data, old_data = [], []
    for path in new_files:
        require(pin(path)["sha256"] == CONTEXT_SHA, "frozen new context changed")
        data = load(path)
        require(data["classification"] is None and data["human_accepted"] is False, "new context acceptance")
        require(exact(data["source_size"], list(SIZE)) and data["sources"] == {"F6": "Im3.jpg"}, "new context source metadata")
        require(exact(data["target_boxes"], {"F6": TARGETS["F6"]}) and
                exact(data["context_boxes"], {"F6": CONTEXTS["F6"]}), "new context rectangles")
        require(set(data["cells"]) == {"F6"}, "new context pair scope")
        context_records(data["cells"]["F6"], CONTEXTS["F6"], image)
        new_data.append(data)
    for path in old_files:
        require(pin(path)["sha256"] == OLD_CONTEXT_SHA, "frozen old context changed")
        data = load(path)
        require(data["classification"] is None and data["human_accepted"] is False, "old context acceptance")
        require(exact(data["source_size"], list(SIZE)) and data["sources"]["F5"] == "Im3.jpg", "old context source metadata")
        require(exact(data["target_boxes"]["F5"], TARGETS["F5"]) and
                exact(data["context_boxes"]["F5"], CONTEXTS["F5"]), "old context rectangles")
        context_records(data["cells"]["F5"], CONTEXTS["F5"], image)
        old_data.append(data)
    overlaps = [check_overlap(new["cells"]["F6"], old["cells"]["F5"]) for new in new_data for old in old_data]
    require(overlaps == [10472] * 4, "four exact old-context overlap checks")
    return image, {"new_context_copies": 2, "new_cells_per_copy": 26312,
        "old_F5_context_copies": 2, "old_F5_cells_per_copy": 10472,
        "direct_source_records_checked": 73568, "new_distinct_source_cells": 26312,
        "overlap_cells_per_pairing": 10472, "overlap_pairings_checked": 4,
        "source": "Im3.jpg", "source_size": list(SIZE), "contexts_byte_equal_within_batch": True,
        "overlap_is_repeated_same_source_not_new_independent_evidence": True}


def rows_mask(values, box):
    require(type(values) is list and all(type(y) is int and box[1] <= y < box[3] for y in values), "native row bounds/type")
    require(values == sorted(set(values)), "native rows duplicated or unordered")
    return sum(1 << y for y in values)


def validate_entry(row, box, band=False, legacy_band_metadata=False, primary_band_refs_optional=False):
    required = ENTRY_FIELDS | ({"band_id", "candidate_routes"} if band else set())
    optional = {"other_possible_origins", "continuity_claim"} if band and legacy_band_metadata else set()
    if band and primary_band_refs_optional:
        required = required - {"unassigned_band_refs"}
        optional = optional | {"unassigned_band_refs"}
    require(type(row) is dict and required <= set(row) <= required | optional, "entry schema")
    if "other_possible_origins" in row:
        require(type(row["other_possible_origins"]) is list and
                all(type(origin) is str and origin.strip() for origin in row["other_possible_origins"]), "legacy band origin metadata")
    if "continuity_claim" in row:
        require(row["continuity_claim"] is False, "legacy band cannot assert continuity")
    x = row["x"]
    require(type(x) is int and box[0] <= x < box[2], "entry column")
    core, fringe = (rows_mask(row[label], box) for label in CLASSES)
    require(not core & fringe, "core/fringe overlap")
    require(type(row["fragment_membership"]) is list, "membership list required")
    member_core = member_fringe = occupied = 0
    identities = []
    for member in row["fragment_membership"]:
        require(type(member) is dict and set(member) == {"fragment_id", "core", "fringe"}, "membership schema")
        identity = member["fragment_id"]
        require(type(identity) is str and identity.strip() and identity not in identities, "duplicate/empty fragment ID")
        identities.append(identity)
        c, f = (rows_mask(member[label], box) for label in CLASSES)
        require(c | f and not c & f and not occupied & (c | f), "empty/overlapping membership")
        member_core |= c
        member_fringe |= f
        occupied |= c | f
    require((core, fringe) == (member_core, member_fringe), "fragment class unions differ")
    require(row["fragment_id"] == (identities[0] if len(identities) == 1 else None), "outer fragment ID")
    selected = core | fringe
    flags = [flag for touched, flag in ((x == box[0], "target_left"), (x == box[2]-1, "target_right"),
             (selected & (1 << box[1]), "target_top"), (selected & (1 << (box[3]-1)), "target_bottom")) if touched] if selected else []
    require(row["boundary_flags"] == flags, "boundary flags differ")
    require(type(row["reason"]) is str and row["reason"].strip(), "missing reason")
    status = row["status"]
    require(status in STATUSES, "unknown status")
    require(status != "identified_local_fragment" or bool(core), "identified status without core")
    require(status != "fringe_only" or (not core and bool(fringe)), "fringe-only status inconsistent")
    require(status != "boundary_truncated" or (bool(selected) and bool(flags)), "boundary status inconsistent")
    refs = row.get("unassigned_band_refs", []) if band and primary_band_refs_optional else row["unassigned_band_refs"]
    require(type(refs) is list and all(type(ref) is str and ref for ref in refs) and len(refs) == len(set(refs)), "band reference schema")
    require(not band or refs == [], "unassigned band must not point to another band")
    require(status != "no_attributable_cells" or (not selected and not refs), "empty status suppresses selection/conflict")
    return core, fringe


def coverage(data, pair):
    declared, box = data["coverage"], CONTEXTS[pair]
    require(declared["full_context_inspected"] is True and declared["uncompleted_context"] == [], "incomplete reading attestation")
    require(type(declared["raw_context_cells"]) is int and declared["raw_context_cells"] == (box[2]-box[0])*(box[3]-box[1]), "attested context count")
    columns = []
    for block in declared["raw_blocks"]:
        first, last = block["columns"]
        require(type(first) is int and type(last) is int and first <= last, "attested block range")
        require(type(block["receipt"]) is str and block["receipt"].strip() and block.get("truncated", False) is False, "read receipt/truncation")
        columns.extend(range(first, last+1))
    require(columns == list(range(box[0], box[2])), "attested exact-once column coverage")
    require(bool(declared["prior_knowledge"]), "prior knowledge attestation required")
    row_fields = [field for field in ("rows", "rows_covered", "rows_inspected") if field in declared]
    require(row_fields and all(type(declared[field]) is list and len(declared[field]) == 2 and
            all(type(value) is int for value in declared[field]) and exact(declared[field], [box[1], box[3]-1])
            for field in row_fields), "attested row coverage")
    require(type(declared["display_convention"]) is str and declared["display_convention"].strip(), "display convention missing")
    views = declared["actual_views"]
    require(type(views) is list and all(type(view) is dict and type(view.get("path")) is str for view in views), "view attestation schema")
    require({"Im3.jpg", "page-076.png"} <= {Path(view["path"]).name for view in views}, "source/page views missing")
    require(declared.get("counterpart_new_annotation_read", False) is False, "counterpart pre-freeze reading declared")
    return len(declared["raw_blocks"])


def validate_annotation(data, pair, role, attest=True):
    box = TARGETS[pair]
    aliases = {role} | ({"force56_peer"} if pair == "F5" and role == "peer" else set())
    require(role in ROLES and data["reader"] in aliases and data["pair"] == pair and
            data["region_id"] == pair + "-Im3" and data["source"] == "Im3.jpg", "annotation provenance")
    require(exact(data["target_box"], box) and exact(data["context_box"], CONTEXTS[pair]), "annotation rectangles")
    require(data["human_accepted"] is False and data["physical_support"] is None, "annotation acceptance")
    require(set(data["routes"]) == {"solid", "dash"}, "route scope")
    if attest:
        coverage(data, pair)
    occupied, bands, by_column = defaultdict(int), {}, defaultdict(list)
    for band in data["unassigned_bands"]:
        c, f = validate_entry(band, box, band=True, legacy_band_metadata=pair == "F5",
                              primary_band_refs_optional=pair == "F6" and role == "primary")
        key = band["x"], band["band_id"]
        require(type(key[1]) is str and key[1] and key not in bands, "band key duplicate/invalid")
        candidates = band["candidate_routes"]
        require(type(candidates) is list and len(candidates) == len(set(candidates)) and
                all(route in ("solid", "dash") for route in candidates), "candidate routes")
        require(bool(c | f) == bool(candidates), "band ink/candidates mismatch")
        require(band["status"] != "identity_conflict" or bool(c | f), "empty conflict band")
        require(not occupied[band["x"]] & (c | f), "duplicate band cells")
        occupied[band["x"]] |= c | f
        bands[key] = band
        by_column[band["x"]].append(band)
    route_index = {}
    for route in ("solid", "dash"):
        rows = data["routes"][route]
        require([row["x"] for row in rows] == list(range(box[0], box[2])), "route exact column coverage/order")
        for row in rows:
            c, f = validate_entry(row, box)
            require(not occupied[row["x"]] & (c | f), "duplicate route/band cells")
            occupied[row["x"]] |= c | f
            route_index[route, row["x"]] = row
            for ref in row["unassigned_band_refs"]:
                require((row["x"], ref) in bands and route in bands[row["x"], ref]["candidate_routes"], "missing route-specific band reference")
            require(row["status"] != "identity_conflict" or bool(row["unassigned_band_refs"]), "route conflict without reference")
            require(bool(c | f) or not row["unassigned_band_refs"] or row["status"] == "identity_conflict", "empty conflict route status")
    for (x, identity), band in bands.items():
        for route in band["candidate_routes"]:
            require(identity in route_index[route, x]["unassigned_band_refs"], "nonreciprocal candidate route")
    return by_column


def operations(first, second):
    # Enumerate truth tables over the full native row domain independently.
    truth = {"intersection": (False, False, False, True),
             "union": (False, True, True, True), "primary_only": (False, False, True, False),
             "peer_only": (False, True, False, False), "symmetric_difference": (False, True, True, False)}
    return {label: [y for y in range(88) if table[2*int(y in first)+int(y in second)]] for label, table in truth.items()}


def compare_classes(first, second):
    return {label: operations(first[label], second[label]) for label in CLASSES} | {
        "outer": operations(first["core"]+first["fringe"], second["core"]+second["fringe"])}


def visible(rows):
    return {label: [y for y in range(88) if any(y in row[label] for row in rows)] for label in CLASSES}


def scope_masks(data, scope):
    result = defaultdict(lambda: {"core": 0, "fringe": 0, "outer": 0})
    rows = data["unassigned_bands"] if scope == "unassigned" else data["routes"][scope]
    for row in rows:
        for label in CLASSES:
            result[row["x"]][label] |= sum(1 << y for y in row[label])
        result[row["x"]]["outer"] = result[row["x"]]["core"] | result[row["x"]]["fringe"]
    return result


def cross_intersections(f6, f5):
    output = []
    for f6_scope in SCOPES:
        first = scope_masks(f6, f6_scope)
        for f5_scope in SCOPES:
            second = scope_masks(f5, f5_scope)
            cells = {}
            for label, a, b in (("core_core", "core", "core"), ("core_fringe", "core", "fringe"),
                    ("fringe_core", "fringe", "core"), ("fringe_fringe", "fringe", "fringe"), ("outer", "outer", "outer")):
                cells[label] = [[x, y] for x in range(310, 425) for y in range(88)
                                if (first[x][a] & second[x][b]) & (1 << y)]
            output.append({"f6_scope": f6_scope, "f5_scope": f5_scope, "cells": cells})
    return output


def cross_pair_comparisons(readers, old_readers):
    return [{"f6_reader": f6_role, "f5_reader": f5_role,
             "intersections": cross_intersections(readers[f6_role], old_readers[f5_role])}
            for f6_role in ROLES for f5_role in ROLES]


def selected_white(data, image):
    return [{"scope": scope, "class": label, "x": row["x"], "y": y}
            for scope in SCOPES
            for row in (data["unassigned_bands"] if scope == "unassigned" else data["routes"][scope])
            for label in CLASSES for y in row[label] if image.getpixel((row["x"], y)) == (255, 255, 255)]


def totals(rows):
    return {"entries": len(rows), "outer_different": sum(bool(row["sets"]["outer"]["symmetric_difference"]) for row in rows),
            "class_different": sum(bool(row["sets"]["core"]["symmetric_difference"] or row["sets"]["fringe"]["symmetric_difference"]) for row in rows)}


def expected_comparison(readers, old_readers, bands, image):
    routes = [{"route": route, "x": first["x"], "primary_original": first,
               "peer_original": second, "sets": compare_classes(first, second)}
              for route in ("solid", "dash")
              for first, second in zip(readers["primary"]["routes"][route], readers["peer"]["routes"][route])]
    visible_rows = []
    for index, x in enumerate(range(145, 440)):
        selections = {role: visible([readers[role]["routes"][route][index] for route in ("solid", "dash")]
                                   + bands[role].get(x, [])) for role in ROLES}
        visible_rows.append({"x": x, "primary_unassigned_originals": bands["primary"].get(x, []),
            "peer_unassigned_originals": bands["peer"].get(x, []), "sets": compare_classes(selections["primary"], selections["peer"])})
    summary = {"routes": totals(routes), "visible_ink": totals(visible_rows),
        "status_different": sum(row["primary_original"]["status"] != row["peer_original"]["status"] for row in routes),
        "selected_exact_white_cells": {role: selected_white(readers[role], image) for role in ROLES}}
    return {"literal_readings": readers, "prior_F5_readings": old_readers,
            "route_comparisons": routes, "visible_ink_comparisons": visible_rows,
            "cross_pair_comparisons": cross_pair_comparisons(readers, old_readers), "summary": summary}


def check_comparison(output, expected):
    require(set(output) == {"status", "pair", "region_id", "input_pins", "dependencies", "script_pin", "test_pin",
            "literal_readings", "prior_F5_readings", "literal_reproductions", "route_comparisons", "visible_ink_comparisons",
            "cross_pair_comparisons", "exact_old_context_overlap_cells", "summary", "human_accepted", "physical_support", "limits"}, "comparison schema")
    require(output["status"] == "native_ink_reconciliation_not_physical_measurement", "comparison status")
    require(output["pair"] == "F6" and output["region_id"] == "F6-Im3", "comparison source identity")
    require(output["human_accepted"] is False and output["physical_support"] is None, "comparison acceptance")
    require(output["literal_reproductions"] == {"primary": True, "peer": True}, "literal reproduction declaration")
    require(type(output["exact_old_context_overlap_cells"]) is int and output["exact_old_context_overlap_cells"] == 10472, "comparison source overlap count")
    for field, value in expected.items():
        require(exact(output[field], value), "comparison differs: " + field)
    return expected["summary"]


def reject(label, function, passed):
    try:
        function()
    except (ValueError, KeyError, TypeError, AssertionError):
        passed.append(label)
    else:
        raise ValueError("deliberate corruption accepted: " + label)


def controls():
    passed = []
    require(operations([0, 2], [2, 87]) == {"intersection": [2], "union": [0, 2, 87],
            "primary_only": [0], "peer_only": [87], "symmetric_difference": [0, 87]}, "manual five-operation oracle")
    passed.append("manual_five_operations_native_extremes")
    image = Image.new("RGB", SIZE, (255, 255, 255))
    records = [{"x": 0, "y": 0, "rgb": [255, 255, 255]}]
    context_records(records, [0, 0, 1, 1], image)
    passed.append("one_cell_direct_source_check")
    reject("wrong_width_rejected", lambda: validate_image(Image.new("RGB", (745, 88))), passed)
    reject("wrong_mode_rejected", lambda: validate_image(Image.new("L", SIZE)), passed)
    bad = copy.deepcopy(records)
    bad[0]["rgb"][0] = 254
    reject("source_RGB_corruption_rejected", lambda: context_records(bad, [0, 0, 1, 1], image), passed)
    required = {"synthetic.json": {"bytes": 1, "sha256": "0"*64}}
    require_dependency_coverage(required, required)
    reject("required_dependency_omission_rejected", lambda: require_dependency_coverage({}, required), passed)
    reject("outside_path_rejected", lambda: name(Path("/Users/admin/docs/911/unapproved-input.md")), passed)
    require(not exact(False, 0), "JSON Boolean/numeric equality")
    passed.append("JSON_false_not_numeric_zero")
    return passed


def check_all(context_only=False):
    passed = controls()
    pins = {}
    for path in [HERE / "independent_check.py", HERE / "test_independent_check.py", OLD / "independent_check.py"]:
        add_pin(pins, path)
    require(pin(HERE / "CONSUMER-COMPATIBILITY.md")["sha256"] == COMPATIBILITY_SHA, "frozen compatibility contract changed")
    add_pin(pins, HERE / "CONSUMER-COMPATIBILITY.md")
    check_charter_copies(pins)
    require(pin(OLD / "independent_check.py")["sha256"] == REFERENCE_SHA, "adapted reference checker changed")
    image, context_receipt = check_contexts(pins)
    if context_only:
        require(all(exact(pin(HERE / key), expected) for key, expected in pins.items()), "inputs changed during context check")
        return {"status": "pass_context_fidelity_only", "contexts": context_receipt, "controls": passed,
                "inputs": pins, "inputs_after": pins}
    require(len(FROZEN_READERS) == 4 and COMPARISON_SHA is not None, "both new originals and producer outputs must be frozen")
    readers, old_readers, bands, annotation_receipts = {}, {}, {}, {}
    roots = [HERE / filename for filename in ("context01.json", "context02.json", "PROTOCOL.md", "READERS.md",
        "read_context.py", "compare.py", "test_compare.py", "CONSUMER-COMPATIBILITY.md")]
    roots += [MAIN_CHARTER, WORKTREE_CHARTER]
    roots += [HERE / filename for filename in ("../force56-remainder/compare.py", "../force45/compare_force45.py",
        "../force69/compare_force69.py", "../approach34/compare.py")]
    for pair in ("F6", "F5"):
        for role in ROLES:
            path = HERE / f"reader-{role}.json" if pair == "F6" else OLD / f"reader-F5-{role}.json"
            key = name(path)
            require(pin(path)["sha256"] == FROZEN_READERS[key], "frozen annotation changed: " + key)
            data = load(path)
            dependency_closure([path], pins)
            required = {}
            context_dir = HERE if pair == "F6" else OLD
            dependency_closure([context_dir / "context01.json", context_dir / "context02.json", context_dir / "READERS.md"], required)
            if pair == "F6":
                add_pin(required, OLD / "READERS.md")
            require_dependency_coverage(data["inputs"], required, path.parent)
            by_column = validate_annotation(data, pair, role)
            (readers if pair == "F6" else old_readers)[role] = data
            if pair == "F6":
                bands[role] = by_column
            annotation_receipts[key] = {"route_records": sum(len(rows) for rows in data["routes"].values()),
                "unassigned_band_records": len(data["unassigned_bands"]), "multiple_band_columns": sum(len(rows)>1 for rows in by_column.values()),
                "attested_read_blocks": coverage(data, pair), "selected_exact_white_cells": len(selected_white(data, image)),
                "statuses": dict(Counter(row["status"] for rows in data["routes"].values() for row in rows))}
            roots.append(path)
    roots += [OLD / "context01.json", OLD / "context02.json"]
    required = {}
    dependency_closure(roots, required)
    expected = expected_comparison(readers, old_readers, bands, image)
    files = [HERE / f"comparison{index:02}.json" for index in (1, 2)]
    require(files[0].read_bytes() == files[1].read_bytes(), "comparison repeat bytes differ")
    dependency_closure(files, pins)
    for path in files:
        require(pin(path)["sha256"] == COMPARISON_SHA, "frozen comparison changed")
        output = load(path)
        require_dependency_coverage(output["dependencies"], required)
        expected_inputs = {name(path): pin(path) for path in roots if path.name.startswith("reader-")}
        require(exact(normalized_map(output["input_pins"]), expected_inputs), "comparison four-original pin roster")
        check_comparison(output, expected)
    for field in ("literal_readings", "prior_F5_readings", "summary"):
        bad = copy.deepcopy(output)
        bad[field] = None
        reject("corrupted_" + field + "_rejected", lambda: check_comparison(bad, expected), passed)
    bad = copy.deepcopy(output)
    bad["route_comparisons"][0]["sets"]["outer"]["union"] = [-1]
    reject("corrupted_route_set_rejected", lambda: check_comparison(bad, expected), passed)
    bad = copy.deepcopy(output)
    bad["cross_pair_comparisons"][0]["intersections"][0]["cells"]["outer"] = [[0, 0]]
    reject("corrupted_cross_pair_intersection_rejected", lambda: check_comparison(bad, expected), passed)
    omitted = normalized_map(output["dependencies"])
    del omitted[name(OLD / "reader-F5-peer.py")]
    reject("omitted_old_reader_script_rejected", lambda: require_dependency_coverage(omitted, required), passed)
    require(all(exact(pin(HERE / key), expected_pin) for key, expected_pin in pins.items()), "input changed during complete check")
    cross_counts = [{"f6_reader": row["f6_reader"], "f5_reader": row["f5_reader"],
                     "all_scope_outer_intersections": sum(len(entry["cells"]["outer"]) for entry in row["intersections"])}
                    for row in expected["cross_pair_comparisons"]]
    return {"status": "pass_native_cell_bookkeeping_only", "contexts": context_receipt,
        "annotations": annotation_receipts, "comparison_summary": expected["summary"], "cross_pair_summary": cross_counts,
        "operation_arrays_checked": 2*(15*(590+295)+4*9*5), "comparison_files": 2,
        "required_comparison_dependency_count": len(required), "all_required_recursive_inputs_present": True,
        "controls": passed, "controls_count": len(passed), "inputs": pins, "inputs_after": pins,
        "input_pin_count": len(pins), "input_pins_unchanged_after_check": True,
        "environment": {"python": platform.python_version(), "pillow": pillow_version},
        "independence": "Standalone direct Pillow source checks, native-row truth tables and cross-pair bit masks. No producer comparator, source helper or reader imports. Earlier independent checker inspected and adapted, pinned as a method reference.",
        "literal_replay_limit": "This checker does not execute reader build(). Coordinator literal-build reproduction remains separately evidenced. Saved reading attestations are checked for bookkeeping, not independently witnessed perception.",
        "legacy_metadata_compatibility": "The preserved F5 originals may carry optional band-only other_possible_origins (list of nonempty strings) and continuity_claim:false. Their original fields are preserved exactly, not stripped; these optional fields are not added to the F6 schema.",
        "fixed_primary_compatibility": "The frozen F6 primary may omit outgoing band unassigned_band_refs; any present value must be an empty list. Routes still require every reciprocal reference. Coverage rows/rows_covered/rows_inspected aliases must all be exact integer [0,87]. Originals remain unmodified.",
        "authority_path_compatibility": "The primary pinned the worktree charter. Both exact charter paths are pinned and their bytes are equal; main remains controlling. This does not establish a canonical-main read by the primary or permit other outside paths.",
        "limits": "Same-source overlap and AI reader arithmetic only. No semantic ownership, continuity, pre-raster enclosure, physical support, human acceptance, metric, model discrepancy or historical cause validation. Pillow decoding is not an independent JPEG decoder."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    try:
        require(not args.save or not (args.context_only or args.self_test), "save requires complete check")
        result = {"status": "synthetic_controls_pass", "controls": controls()} if args.self_test else check_all(args.context_only)
        if args.save:
            with (HERE / "independent-check.json").open("x") as output:
                json.dump(result, output, indent=2, sort_keys=True, allow_nan=False)
                output.write("\n")
        print(json.dumps({key: value for key, value in result.items() if key not in ("inputs", "inputs_after")}, indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, AssertionError, OSError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__, "error": str(error)}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
