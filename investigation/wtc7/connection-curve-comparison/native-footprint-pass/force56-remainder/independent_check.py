"""Independent finite native-cell/annotation/comparison oracle.

No producer comparator, context runner, force helper or reader is imported for
arithmetic. Selection ownership is not evaluated: only saved source fidelity,
annotation bookkeeping, exact set operations, and declared provenance are.
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
TARGETS = {"F5": [310, 0, 425, 88], "F6": [270, 55, 340, 88]}
CONTEXTS = {"F5": [308, 0, 427, 88], "F6": [268, 53, 342, 88]}
SOURCES = {"F5": "Im3.jpg", "F6": "Im1.jpg"}
SIZE = (741, 88)
CONTEXT_SHA = "6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5"
SOURCE_SHAS = {"Im3.jpg": "af735345f189bba0eab7a836c5c0c6221ab30055febd81b52b331821fe87259b",
               "Im1.jpg": "929f5d00d2f9ab1eba27a4aad8af37320a4fd37f2455f9b51d750ec7e15e8139"}
FROZEN_READERS = {
    "reader-F5-primary.json": "6ce861b44d73e09a88e3d79e754f7f2f41b9458a0baafb1630c22b2de3f2c2b3",
    "reader-F6-primary.json": "4e3dab2e3cf358854da349a987e897fbb1f5915f8ee5c2e67e246cfa06da96be",
    "reader-F5-peer.json": "dbed8ae98651c5fc21a4a11e2d97c6897ed609eac809e20b1638e376246de5f4",
    "reader-F6-peer.json": "b1345970d11e24d552e1bb755279f84f2d251db1232e1d4cedc298b02135310e",
}
COMPARISON_SHAS = {"F5": "d4df145a105099db75d012a38c4b5d7bc5083ab4b75aa965607222dbe5d59205",
                   "F6": "74aa6e596286ffab22ea44db56a9cf060d573c09f7abd575a67bcd2dd28c086d"}
AUTHORITY_CONTEXT = {Path(value).resolve() for value in (
    "/Users/admin/docs/911/AGENTS.md", "/Users/admin/docs/911/START-HERE.md", "/Users/admin/docs/911/WORKFLOW.md",
    "/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md",
    "/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md",
    "/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md")}
METHOD_SHAS = {
    "../force45/compare_force45.py": "932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be",
    "../force69/compare_force69.py": "f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e",
    "../approach34/compare.py": "cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac",
}
STATUSES = {"identified_local_fragment", "fringe_only", "no_attributable_cells", "identity_conflict", "boundary_truncated"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(file):
    return json.loads(Path(file).read_text())


def pin(file):
    raw = Path(file).read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def name(file):
    resolved = Path(file).resolve()
    if resolved not in AUTHORITY_CONTEXT:
        resolved.relative_to(BASE)
    return os.path.relpath(resolved, HERE)


def exact(first, second):
    return json.dumps(first, sort_keys=True, allow_nan=False) == json.dumps(second, sort_keys=True, allow_nan=False)


def add_pin(pins, file, expected=None):
    key = name(file)
    observed = pin(HERE / key)
    require(expected is None or exact(observed, expected), "declared dependency changed: " + key)
    require(key not in pins or pins[key] == observed, "conflicting dependency: " + key)
    pins[key] = observed
    return key


def dependency_closure(roots, pins):
    queue = [add_pin(pins, file) for file in roots]
    visited = set()
    while queue:
        key = queue.pop(0)
        if key in visited or not key.endswith(".json"):
            continue
        visited.add(key)
        file = HERE / key
        data = load(file)
        require(type(data) is dict, "dependency JSON must be an object")
        if "inputs_after" in data:
            require(exact(data["inputs"], data["inputs_after"]), "dependency before/after changed: " + key)
        for field in ("inputs", "inputs_after", "input_pins", "dependencies"):
            if field not in data:
                continue
            require(type(data[field]) is dict, "dependency map malformed: " + key)
            for child, expected in data[field].items():
                require(type(expected) is dict and set(expected) == {"bytes", "sha256"}, "child pin schema")
                queue.append(add_pin(pins, file.parent / child, expected))
        if "script_pin" in data:
            script = file.with_suffix(".py") if file.name.startswith("reader-") else file.parent / "compare.py"
            require(file.name.startswith(("reader-", "comparison-")), "unknown script-pin source")
            add_pin(pins, script, data["script_pin"])
        if "test_pin" in data:
            require(file.name.startswith("comparison-"), "unknown test-pin source")
            add_pin(pins, file.parent / "test_compare.py", data["test_pin"])
    return sorted(visited)


def normalized_map(declared, directory=HERE):
    result = {}
    require(type(declared) is dict, "pin map required")
    for child, expected in declared.items():
        key = name(directory / child)
        require(type(expected) is dict and set(expected) == {"bytes", "sha256"}, "pin entry schema")
        require(key not in result or exact(result[key], expected), "conflicting normalized pin aliases")
        result[key] = expected
    return result


def require_dependency_coverage(declared, required):
    normalized = normalized_map(declared)
    require(all(key in normalized and exact(normalized[key], value) for key, value in required.items()),
            "comparison omitted or changed a required transitive input")
    return normalized


def validate_image(image):
    require(image.mode == "RGB" and image.size == SIZE, "source must be 741 by 88 RGB")


def context_records(records, box, image):
    validate_image(image)
    x0, y0, x1, y1 = box
    require(type(records) is list and len(records) == (x1 - x0) * (y1 - y0), "context coverage count")
    pixels = image.load()
    coordinates = []
    for row_index, y in enumerate(range(y0, y1)):
        for column_index, x in enumerate(range(x0, x1)):
            row = records[row_index * (x1 - x0) + column_index]
            require(set(row) == {"x", "y", "rgb"}, "context row schema")
            require(type(row["x"]) is int and type(row["y"]) is int and (row["x"], row["y"]) == (x, y), "context row-major coordinates")
            require(type(row["rgb"]) is list and len(row["rgb"]) == 3 and
                    all(type(v) is int and 0 <= v <= 255 for v in row["rgb"]), "context RGB schema")
            require(tuple(row["rgb"]) == pixels[x, y], "context/source RGB differs")
            coordinates.append((x, y))
    require(len(set(coordinates)) == len(coordinates), "duplicate context coordinates")
    return coordinates


def check_contexts(pins):
    files = [HERE / f"context{n:02}.json" for n in (1, 2)]
    require(files[0].read_bytes() == files[1].read_bytes(), "context repeat bytes differ")
    require(all(pin(file)["sha256"] == CONTEXT_SHA for file in files), "frozen context SHA")
    dependency_closure(files, pins)
    images = {}
    for pair, source in SOURCES.items():
        file = HERE / "../../native-strips01" / source
        add_pin(pins, file)
        require(pin(file)["sha256"] == SOURCE_SHAS[source], "frozen source SHA")
        with Image.open(file) as opened:
            validate_image(opened)
            images[pair] = opened.copy()
    by_source = set()
    for file in files:
        data = load(file)
        require(data["classification"] is None and data["human_accepted"] is False, "context acceptance")
        require(exact(data["source_size"], list(SIZE)) and data["sources"] == SOURCES, "context source metadata")
        require(data["target_boxes"] == TARGETS and data["context_boxes"] == CONTEXTS, "context rectangle metadata")
        require(set(data["cells"]) == set(TARGETS), "context pair scope")
        for pair in TARGETS:
            coordinates = context_records(data["cells"][pair], CONTEXTS[pair], images[pair])
            by_source.update((SOURCES[pair], x, y) for x, y in coordinates)
    require(len(by_source) == 13062, "distinct source-cell count")
    return images, {"copies": 2, "byte_equal": True, "source_size": list(SIZE),
                    "F5_cells_per_copy": 10472, "F6_cells_per_copy": 2590,
                    "cells_per_copy": 13062, "cell_records_checked": 26124,
                    "distinct_source_cells": 13062,
                    "source_identity_in_coordinate_key": True}


def rows_mask(values, box):
    require(type(values) is list and all(type(y) is int and box[1] <= y < box[3] for y in values), "native row bounds/type")
    require(values == sorted(set(values)), "native rows duplicated or unordered")
    return sum(1 << y for y in values)


def validate_entry(row, box):
    require(type(row["x"]) is int and box[0] <= row["x"] < box[2], "entry column")
    core, fringe = rows_mask(row["core"], box), rows_mask(row["fringe"], box)
    require(not core & fringe, "core/fringe overlap")
    members = row["fragment_membership"]
    require(type(members) is list, "membership list required")
    member_core = member_fringe = occupied = 0
    ids = []
    for member in members:
        require(set(member) == {"fragment_id", "core", "fringe"}, "membership schema")
        identity = member["fragment_id"]
        require(type(identity) is str and identity.strip() and identity not in ids, "duplicate/empty fragment ID")
        ids.append(identity)
        c, f = rows_mask(member["core"], box), rows_mask(member["fringe"], box)
        require(c | f and not c & f and not occupied & (c | f), "empty/overlapping membership")
        member_core |= c
        member_fringe |= f
        occupied |= c | f
    require((core, fringe) == (member_core, member_fringe), "fragment class unions differ")
    require(row["fragment_id"] == (ids[0] if len(ids) == 1 else None), "outer fragment ID")
    selected = core | fringe
    flags = [flag for touched, flag in ((row["x"] == box[0], "target_left"),
             (row["x"] == box[2] - 1, "target_right"), (selected & (1 << box[1]), "target_top"),
             (selected & (1 << (box[3] - 1)), "target_bottom")) if touched] if selected else []
    require(row["boundary_flags"] == flags, "boundary flags differ")
    require(type(row["reason"]) is str and row["reason"].strip(), "missing reason")
    status = row["status"]
    require(status in STATUSES, "unknown status")
    if status == "identified_local_fragment":
        require(bool(core), "identified status without core")
    if status == "fringe_only":
        require(not core and bool(fringe), "fringe-only status inconsistent")
    if status == "boundary_truncated":
        require(bool(selected) and bool(flags), "boundary status inconsistent")
    refs = row["unassigned_band_refs"]
    require(type(refs) is list and all(type(ref) is str and ref for ref in refs) and len(set(refs)) == len(refs), "band reference schema")
    if status == "no_attributable_cells":
        require(not selected and not refs, "empty status suppresses selection/conflict")
    return core, fringe


def coverage(data, pair):
    declared = data["coverage"]
    require(declared["full_context_inspected"] is True and declared["uncompleted_context"] == [], "incomplete reading attestation")
    box = CONTEXTS[pair]
    require(type(declared["raw_context_cells"]) is int and declared["raw_context_cells"] == (box[2]-box[0]) * (box[3]-box[1]), "attested cell count")
    columns = []
    for block in declared["raw_blocks"]:
        first, last = block["columns"]
        require(type(first) is int and type(last) is int and first <= last, "attested block range")
        require(type(block["receipt"]) is str and block["receipt"] and block.get("truncated", False) is False, "read receipt/truncation")
        columns.extend(range(first, last + 1))
    require(columns == list(range(box[0], box[2])), "attested exact-once column coverage")
    require(bool(declared["actual_views"]) and bool(declared["prior_knowledge"]), "orientation/prior-knowledge attestation missing")
    row_fields = [field for field in ("rows_covered", "rows_inspected") if field in declared]
    require(row_fields and all(exact(declared[field], [box[1], box[3] - 1]) for field in row_fields), "attested row coverage")
    require(type(declared["display_convention"]) is str and declared["display_convention"].strip(), "display convention missing")
    views = declared["actual_views"]
    require(type(views) is list and all(type(v) is dict and type(v.get("path")) is str for v in views), "actual-view schema")
    filenames = {Path(v["path"]).name for v in views}
    require({SOURCES[pair], "page-076.png"} <= filenames, "source/page view attestation missing")
    if "counterpart_new_annotation_read" in declared:
        require(declared["counterpart_new_annotation_read"] is False, "counterpart pre-freeze reading declared")
    return len(declared["raw_blocks"])


def validate_annotation(data, pair, role, attest=True):
    box = TARGETS[pair]
    allowed_reader_names = ("primary",) if role == "primary" else ("peer", "force56_peer")
    require(role in ("primary", "peer") and data["pair"] == pair and data["reader"] in allowed_reader_names and data["source"] == SOURCES[pair] and
            data["region_id"] == pair + "-" + SOURCES[pair].removesuffix(".jpg"), "annotation provenance")
    require(data["target_box"] == box and data["context_box"] == CONTEXTS[pair], "annotation rectangles")
    require(data["human_accepted"] is False and data["physical_support"] is None, "annotation acceptance")
    require(set(data["routes"]) == {"solid", "dash"}, "route scope")
    if attest:
        coverage(data, pair)
    occupied, bands, by_column = defaultdict(int), {}, defaultdict(list)
    for band in data["unassigned_bands"]:
        c, f = validate_entry(band, box)
        key = (band["x"], band["band_id"])
        require(type(key[1]) is str and key[1] and key not in bands, "band key duplicate/invalid")
        routes = band["candidate_routes"]
        require(type(routes) is list and len(set(routes)) == len(routes) and all(r in ("solid", "dash") for r in routes), "candidate routes")
        require(bool(c | f) == bool(routes), "band ink/candidates mismatch")
        require(band["status"] != "identity_conflict" or bool(c | f), "unassigned conflict band without ink")
        require(not occupied[band["x"]] & (c | f), "duplicate band cells")
        occupied[band["x"]] |= c | f
        bands[key] = band
        by_column[band["x"]].append(band)
    route_index = {}
    for route in ("solid", "dash"):
        records = data["routes"][route]
        require([r["x"] for r in records] == list(range(box[0], box[2])), "route exact column coverage/order")
        for row in records:
            c, f = validate_entry(row, box)
            require(not occupied[row["x"]] & (c | f), "duplicate route/band cells")
            occupied[row["x"]] |= c | f
            route_index[route, row["x"]] = row
            for ref in row["unassigned_band_refs"]:
                require((row["x"], ref) in bands and route in bands[row["x"], ref]["candidate_routes"], "same-column route-specific reference missing")
            if row["status"] == "identity_conflict":
                require(bool(row["unassigned_band_refs"]), "route conflict without reference")
            if not c | f and row["unassigned_band_refs"]:
                require(row["status"] == "identity_conflict", "empty conflict route status")
    for (x, bid), band in bands.items():
        for route in band["candidate_routes"]:
            require(bid in route_index[route, x]["unassigned_band_refs"], "nonreciprocal candidate route")
    return by_column


def operations(first, second):
    # Truth-table scan across every native row, not producer set expressions.
    tests = {"intersection": lambda a, b: a and b, "union": lambda a, b: a or b,
             "primary_only": lambda a, b: a and not b, "peer_only": lambda a, b: b and not a,
             "symmetric_difference": lambda a, b: a != b}
    return {label: [y for y in range(88) if predicate(y in first, y in second)] for label, predicate in tests.items()}


def compare_classes(first, second):
    return {label: operations(first[label], second[label]) for label in ("core", "fringe")} | {
        "outer": operations(first["core"] + first["fringe"], second["core"] + second["fringe"])}


def visible(records):
    return {label: [y for y in range(88) if any(y in r[label] for r in records)] for label in ("core", "fringe")}


def selected_white(data, image):
    return [{"scope": scope, "class": label, "x": row["x"], "y": y}
            for scope, records in list(data["routes"].items()) + [("unassigned", data["unassigned_bands"])]
            for row in records for label in ("core", "fringe") for y in row[label]
            if image.getpixel((row["x"], y)) == (255, 255, 255)]


def totals(records):
    return {"entries": len(records), "outer_different": sum(bool(r["sets"]["outer"]["symmetric_difference"]) for r in records),
            "class_different": sum(bool(r["sets"]["core"]["symmetric_difference"] or r["sets"]["fringe"]["symmetric_difference"]) for r in records)}


def check_comparison(output, readers, bands, pair, image):
    require(set(output) == {"status", "pair", "region_id", "input_pins", "dependencies", "script_pin", "test_pin",
            "literal_readings", "literal_reproductions", "route_comparisons", "visible_ink_comparisons", "summary",
            "human_accepted", "physical_support", "limits"}, "comparison schema")
    require(output["status"] == "native_ink_reconciliation_not_physical_measurement", "comparison status")
    require(output["pair"] == pair and output["region_id"] == pair + "-" + SOURCES[pair].removesuffix(".jpg"), "comparison source identity")
    require(output["human_accepted"] is False and output["physical_support"] is None, "comparison acceptance")
    require(exact(output["literal_readings"], readers), "complete original preservation")
    require(output["literal_reproductions"] == {"primary": True, "peer": True}, "literal-replay declaration")
    expected_routes = []
    for route in ("solid", "dash"):
        for a, b in zip(readers["primary"]["routes"][route], readers["peer"]["routes"][route]):
            expected_routes.append({"x": a["x"], "route": route, "primary_original": a,
                                    "peer_original": b, "sets": compare_classes(a, b)})
    require(exact(output["route_comparisons"], expected_routes), "route operations or originals differ")
    expected_visible = []
    for index, x in enumerate(range(TARGETS[pair][0], TARGETS[pair][2])):
        selections = {role: visible([readers[role]["routes"][r][index] for r in ("solid", "dash")] + bands[role].get(x, []))
                      for role in ("primary", "peer")}
        expected_visible.append({"x": x, "primary_unassigned_originals": bands["primary"].get(x, []),
            "peer_unassigned_originals": bands["peer"].get(x, []), "sets": compare_classes(selections["primary"], selections["peer"])})
    require(exact(output["visible_ink_comparisons"], expected_visible), "visible-ink operations or bands differ")
    expected_summary = {"routes": totals(expected_routes), "visible_ink": totals(expected_visible),
        "status_different": sum(r["primary_original"]["status"] != r["peer_original"]["status"] for r in expected_routes),
        "selected_exact_white_cells": {role: selected_white(readers[role], image) for role in ("primary", "peer")}}
    require(exact(output["summary"], expected_summary), "comparison summary differs")
    return expected_summary


def rejects(label, function, controls):
    try:
        function()
    except (ValueError, TypeError, KeyError, AssertionError):
        controls.append(label)
    else:
        raise ValueError("deliberate corruption accepted: " + label)


def controls():
    passed = []
    require(operations([0, 2], [2, 87]) == {"intersection": [2], "union": [0, 2, 87], "primary_only": [0],
            "peer_only": [87], "symmetric_difference": [0, 87]}, "manual five operations")
    passed.append("manual_five_operations_including_native_extremes")
    require(visible([{"core": [1], "fringe": [2]}, {"core": [3], "fringe": [4]}]) == {"core": [1, 3], "fringe": [2, 4]}, "multiple visible pieces")
    passed.append("multiple_visible_pieces_retained")
    image = Image.new("RGB", SIZE, (255, 255, 255))
    context_records([{"x": 0, "y": 0, "rgb": [255, 255, 255]}], [0, 0, 1, 1], image)
    passed.append("correct_741_width_context")
    rejects("wrong_745_width_rejected", lambda: validate_image(Image.new("RGB", (745, 88))), passed)
    rejects("in_memory_RGB_corruption_rejected", lambda: context_records([{"x": 0, "y": 0, "rgb": [254, 255, 255]}], [0, 0, 1, 1], image), passed)
    rejects("in_memory_coordinate_corruption_rejected", lambda: context_records([{"x": 1, "y": 0, "rgb": [255, 255, 255]}], [0, 0, 1, 1], image), passed)
    row = {"x": 310, "core": [0], "fringe": [1], "fragment_id": "a", "fragment_membership": [{"fragment_id": "a", "core": [0], "fringe": [1]}],
           "status": "boundary_truncated", "reason": "synthetic", "boundary_flags": ["target_left", "target_top"], "unassigned_band_refs": []}
    validate_entry(row, TARGETS["F5"])
    passed.append("exact_membership_and_boundary_flags")
    for label, change in (("duplicate_rows", lambda r: r.update(core=[0, 0])), ("boolean_row", lambda r: r.update(core=[False])),
            ("class_overlap", lambda r: r.update(fringe=[0])), ("missing_membership", lambda r: r.update(fragment_membership=[])),
            ("missing_boundary", lambda r: r.update(boundary_flags=[]))):
        bad = copy.deepcopy(row)
        change(bad)
        rejects(label + "_rejected", lambda: validate_entry(bad, TARGETS["F5"]), passed)
    require(not exact(False, 0), "type-sensitive equality")
    passed.append("json_false_not_numeric_zero")
    empty = {"x": 310, "core": [], "fringe": [], "fragment_id": None, "fragment_membership": [],
             "status": "no_attributable_cells", "reason": "synthetic inspected empty", "boundary_flags": [], "unassigned_band_refs": []}
    fixture = {"pair": "F5", "region_id": "F5-Im3", "reader": "primary", "source": "Im3.jpg",
               "target_box": TARGETS["F5"], "context_box": CONTEXTS["F5"], "human_accepted": False,
               "physical_support": None, "routes": {r: [dict(copy.deepcopy(empty), x=x) for x in range(310, 425)] for r in ("solid", "dash")},
               "unassigned_bands": [], "coverage": {"full_context_inspected": True, "uncompleted_context": [],
                   "raw_context_cells": 10472, "raw_blocks": [{"columns": [308, 426], "receipt": "synthetic-not-source-reading"}],
                   "actual_views": [{"path": "Im3.jpg", "receipt": "synthetic"}, {"path": "page-076.png", "receipt": "synthetic"}],
                   "prior_knowledge": "synthetic", "rows_covered": [0, 87], "display_convention": "synthetic exact-white convention"}}
    for route, y in (("solid", 60), ("dash", 62)):
        band = dict(copy.deepcopy(empty), x=311, core=[y], fragment_id=route, status="identified_local_fragment",
                    fragment_membership=[{"fragment_id": route, "core": [y], "fringe": []}], band_id=route, candidate_routes=[route])
        fixture["unassigned_bands"].append(band)
        fixture["routes"][route][1].update(status="identity_conflict", unassigned_band_refs=[route])
    require(len(validate_annotation(fixture, "F5", "primary")[311]) == 2, "multiple same-column bands")
    passed.append("two_same_column_route_specific_bands_retained")
    alias = copy.deepcopy(fixture)
    alias["reader"] = "force56_peer"
    validate_annotation(alias, "F5", "peer")
    passed.append("declared_force56_peer_alias_preserved_and_accepted_as_peer")
    rejects("peer_alias_rejected_as_primary", lambda: validate_annotation(alias, "F5", "primary"), passed)
    alias["reader"] = "force56_unknown"
    rejects("unknown_peer_alias_rejected", lambda: validate_annotation(alias, "F5", "peer"), passed)
    for label, change in (
            ("missing_reciprocal", lambda d: d["routes"]["solid"][1].update(status="no_attributable_cells", unassigned_band_refs=[])),
            ("wrong_candidate_route", lambda d: d["unassigned_bands"][0].update(candidate_routes=["dash"])),
            ("orphan_band_reference", lambda d: d["routes"]["solid"][1].update(unassigned_band_refs=["missing-band"])),
            ("missing_route_column", lambda d: d["routes"]["solid"].pop()),
            ("duplicate_fragment", lambda d: d["unassigned_bands"][0]["fragment_membership"].append(copy.deepcopy(d["unassigned_bands"][0]["fragment_membership"][0]))),
            ("lost_attested_column", lambda d: d["coverage"]["raw_blocks"][0].update(columns=[309, 426])),
            ("truncated_attested_block", lambda d: d["coverage"]["raw_blocks"][0].update(truncated=True))):
        bad = copy.deepcopy(fixture)
        change(bad)
        rejects(label + "_rejected", lambda: validate_annotation(bad, "F5", "primary"), passed)
    bad = copy.deepcopy(fixture)
    bad["routes"]["solid"][1].update(core=[60], fragment_id="duplicate", status="identified_local_fragment",
        fragment_membership=[{"fragment_id": "duplicate", "core": [60], "fringe": []}])
    rejects("band_cells_duplicated_in_route_rejected", lambda: validate_annotation(bad, "F5", "primary"), passed)
    white_sample = {"routes": {"solid": [{"x": 0, "core": [0], "fringe": []}]}, "unassigned_bands": []}
    require(selected_white(white_sample, image) == [{"scope": "solid", "class": "core", "x": 0, "y": 0}], "exact white flag")
    image.putpixel((0, 0), (254, 255, 255))
    require(selected_white(white_sample, image) == [], "near-white must not be exact white")
    passed.append("exact_white_flag_and_near_white_retained")
    expected = {"synthetic-pin.json": {"bytes": 4, "sha256": "0" * 64}}
    require_dependency_coverage(expected, expected)
    passed.append("required_dependency_coverage_accepts_complete_map")
    rejects("required_dependency_omission_rejected", lambda: require_dependency_coverage({}, expected), passed)
    aliases = {"synthetic-pin.json": expected["synthetic-pin.json"],
               "unused/../synthetic-pin.json": {"bytes": 5, "sha256": "1" * 64}}
    rejects("conflicting_normalized_alias_rejected", lambda: normalized_map(aliases), passed)
    require(len(AUTHORITY_CONTEXT) == 6 and all(name(p) for p in AUTHORITY_CONTEXT), "six exact authority paths")
    passed.append("six_exact_authority_context_paths_allowed")
    rejects("arbitrary_outside_context_path_rejected", lambda: name(Path("/Users/admin/docs/911/unapproved-checker-input.md")), passed)
    return passed


def check_all(context_only=False):
    passed = controls()
    pins = {"independent_check.py": pin(Path(__file__))}
    images, context_receipt = check_contexts(pins)
    if context_only:
        require(all(pin(HERE / key) == expected for key, expected in pins.items()), "inputs changed during context check")
        return {"status": "pass_context_fidelity_only", "contexts": context_receipt, "controls": passed, "inputs": pins, "inputs_after": pins}
    require(len(FROZEN_READERS) == 4, "four originals not yet frozen for checker")
    all_readers, all_bands, annotations = {}, {}, {}
    for pair in TARGETS:
        all_readers[pair], all_bands[pair] = {}, {}
        for role in ("primary", "peer"):
            filename = f"reader-{pair}-{role}.json"
            file = HERE / filename
            require(pin(file)["sha256"] == FROZEN_READERS[filename], "frozen reader changed")
            data = load(file)
            dependency_closure([file], pins)
            context_pins = load(HERE / "context01.json")["inputs"]
            required = {name(HERE / child): expected for child, expected in context_pins.items()}
            required.update({key: pin(HERE / key) for key in ("context01.json", "context02.json", "READERS.md")})
            declared = {name(HERE / key): expected for key, expected in data["inputs"].items()}
            require(all(declared.get(key) == expected for key, expected in required.items()), "reader omitted required transitive input")
            bands = validate_annotation(data, pair, role)
            all_readers[pair][role], all_bands[pair][role] = data, bands
            annotations[filename] = {"route_records": sum(len(r) for r in data["routes"].values()), "band_records": len(data["unassigned_bands"]),
                "multiple_band_columns": sum(len(v) > 1 for v in bands.values()), "attested_read_blocks": coverage(data, pair),
                "selected_exact_white_cells": len(selected_white(data, images[pair])),
                "statuses": dict(Counter(r["status"] for records in data["routes"].values() for r in records))}
    summaries, array_count = {}, 0
    required_counts = {}
    for pair in TARGETS:
        required = {}
        roots = [HERE / f"reader-{pair}-{role}.json" for role in ("primary", "peer")]
        roots += [HERE / filename for filename in ("context01.json", "context02.json", "PROTOCOL.md", "PROTOCOL-V2.md", "CONSUMER-COMPATIBILITY.md", "READERS.md", "compare.py", "test_compare.py")]
        for filename, sha in METHOD_SHAS.items():
            require(pin(HERE / filename)["sha256"] == sha, "frozen comparison method dependency")
            roots.append(HERE / filename)
        dependency_closure(roots, required)
        required_counts[pair] = len(required)
        files = [HERE / f"comparison-{pair}-{index:02}.json" for index in (1, 2)]
        require(files[0].read_bytes() == files[1].read_bytes(), "comparison repeat bytes differ")
        require(all(pin(file)["sha256"] == COMPARISON_SHAS[pair] for file in files), "frozen comparison changed")
        dependency_closure(files, pins)
        for file in files:
            output = load(file)
            require_dependency_coverage(output["dependencies"], required)
            expected_inputs = {f"reader-{pair}-{role}.json": pin(HERE / f"reader-{pair}-{role}.json") for role in ("primary", "peer")}
            require(exact(output["input_pins"], expected_inputs), "comparison original pin roster")
            summaries[pair] = check_comparison(output, all_readers[pair], all_bands[pair], pair, images[pair])
            array_count += 15 * (len(output["route_comparisons"]) + len(output["visible_ink_comparisons"]))
        bad = copy.deepcopy(output)
        bad["route_comparisons"][0]["sets"]["outer"]["union"] = [87]
        rejects(pair + "_in_memory_set_corruption_rejected", lambda: check_comparison(bad, all_readers[pair], all_bands[pair], pair, images[pair]), passed)
        corrupted_dependencies = dict(output["dependencies"])
        del corrupted_dependencies["read_context_v2.py"]
        rejects(pair + "_in_memory_context_dependency_omission_rejected", lambda: require_dependency_coverage(corrupted_dependencies, required), passed)
    require(all(pin(HERE / key) == expected for key, expected in pins.items()), "input changed during full check")
    return {"status": "pass_native_cell_bookkeeping_only", "contexts": context_receipt, "annotations": annotations,
        "comparison_summaries": summaries, "operation_arrays_checked": array_count,
        "required_comparison_dependency_counts": required_counts,
        "coverage": {"original_readings": len(annotations), "route_records": sum(a["route_records"] for a in annotations.values()),
                     "unassigned_band_records": sum(a["band_records"] for a in annotations.values()), "comparison_files": 4,
                     "all_producer_dependency_maps_cover_independent_required_closures": True},
        "controls": passed, "controls_count": len(passed), "inputs": pins, "inputs_after": pins,
        "input_pin_count": len(pins), "input_pins_unchanged_after_check": True,
        "environment": {"python": platform.python_version(), "pillow": pillow_version},
        "independence": "Standalone native-cell and truth-table arithmetic; no producer, context, force or reader imports. Saved reading attestations are checked for bookkeeping, not independently witnessed perception.",
        "literal_replay_limit": "Reader build() is deliberately not imported or executed by this checker. The coordinator separately performs literal-build reproduction; this checker validates saved original records, their pins and complete preservation.",
        "declared_compatibility": "CONSUMER-COMPATIBILITY.md predates comparisons: exactly force56_peer or peer denotes the peer role only. Six exact pinned main/skill files are authority context, not new scientific evidence. Frozen originals are unchanged; no wider path exception is allowed.",
        "limits": "No semantic ownership, continuity, pre-raster enclosure, physical support, human acceptance, model discrepancy or historical-cause validation. Source decoding uses Pillow as did extraction; this is not an independent JPEG decoder.",
        "retained_failures": [{"receipt": "320519", "artifact": "read_context.py v1", "error": "wrong 745 source width; actual pinned sources are 741 by 88 RGB", "repair": "source bytes/targets unchanged; version-2 protocol and runner preserved separately before annotation"}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    try:
        require(not args.save or not (args.context_only or args.self_test), "save requires complete batch check")
        receipt = {"status": "synthetic_controls_pass", "controls": controls()} if args.self_test else check_all(args.context_only)
        if args.save:
            with (HERE / "independent-check.json").open("x") as output:
                json.dump(receipt, output, indent=2, sort_keys=True, allow_nan=False)
                output.write("\n")
        print(json.dumps({key: value for key, value in receipt.items() if key not in ("inputs", "inputs_after")}, indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, AssertionError, OSError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__, "error": str(error)}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
