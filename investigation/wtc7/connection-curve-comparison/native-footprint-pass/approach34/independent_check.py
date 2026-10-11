"""Independent approach-context, annotation-schema and comparison oracle.

No compare/read_context/force helper is imported. Frozen literal readers are
imported only for labeled expansion replay, never for the independent checks.
The author did not annotate this batch. Outputs remain native ink bookkeeping.
"""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
TARGETS = {"E3": [195, 35, 365, 92], "E4": [195, 0, 440, 92]}
CONTEXTS = {"E3": [193, 33, 367, 92], "E4": [193, 0, 442, 92]}
SOURCE = "../../native-strips01/Im10.jpg"
SOURCE_SHA = "fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3"
READING_SHAS = {
    "reader-E3-primary.json": "82a4ffb05f37501871b1a524ba07893d7abed9c7f9b2a5abb34cb0c0b1212eaa",
    "reader-E3-peer.json": "b93d4745e7b05496a64ebb14c10ae525bfec0b9892cdfeca77b21a7d30352828",
    "reader-E4-primary.json": "d84ba3edbfaaae257967ea6dd471db0b9519cfa35504c0b8d6f82a50b784b588",
    "reader-E4-peer.json": "8614172dd792beb83562aef037045b7bb8c2b1123abcc954f08b7be78512e6b8",
}
STATUSES = {"identified_local_fragment", "fringe_only", "identity_conflict",
            "boundary_truncated", "no_attributable_cells"}
OPERATIONS = ("intersection", "union", "primary_only", "peer_only", "symmetric_difference")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name):
    return json.loads((HERE / name).read_text())


def pin(name):
    content = (HERE / name).read_bytes()
    return {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}


def pin_inputs(declared, collected):
    for name, expected in declared.items():
        require(pin(name) == expected, "dependency pin mismatch: " + name)
        if name in collected:
            require(collected[name] == expected, "conflicting dependency pin: " + name)
        collected[name] = expected


def rgb_at(raw, x, y):
    offset = 3 * (745 * y + x)
    return list(raw[offset:offset + 3])


def context_records(records, box, raw):
    x0, y0, x1, y1 = box
    require(len(records) == (x1 - x0) * (y1 - y0), "context record count")
    coordinates = set()
    for index, row in enumerate(records):
        x = x0 + index % (x1 - x0)
        y = y0 + index // (x1 - x0)
        require(set(row) == {"x", "y", "rgb"}, "context record schema")
        require(type(row["x"]) is int and type(row["y"]) is int
                and (row["x"], row["y"]) == (x, y), "context row-major order/coordinate")
        require(type(row["rgb"]) is list and len(row["rgb"]) == 3
                and all(type(c) is int and 0 <= c <= 255 for c in row["rgb"]), "RGB schema")
        require(row["rgb"] == rgb_at(raw, x, y), "source RGB mismatch")
        coordinates.add((x, y))
    return coordinates


def check_contexts(pins):
    require(pin(SOURCE)["sha256"] == SOURCE_SHA, "Im10 source hash")
    with Image.open(HERE / SOURCE) as image:
        require(image.mode == "RGB" and image.size == (745, 92), "Im10 representation")
        raw = image.tobytes()
    require((HERE / "context01.json").read_bytes() == (HERE / "context02.json").read_bytes(),
            "context bytes differ")
    coordinates = {}
    for name in ("context01.json", "context02.json"):
        data = load(name)
        pins[name] = pin(name)
        pin_inputs(data["inputs"], pins)
        require(data["classification"] is None and data["human_accepted"] is False, "context acceptance")
        require(data["sources"] == {"E3": "Im10.jpg", "E4": "Im10.jpg"}, "context source identities")
        require(data["target_boxes"] == TARGETS and data["context_boxes"] == CONTEXTS, "context boxes")
        require(set(data["cells"]) == {"E3", "E4"}, "context scope")
        for pair in ("E3", "E4"):
            coordinates[pair] = context_records(data["cells"][pair], CONTEXTS[pair], raw)
    require(len(coordinates["E3"] & coordinates["E4"]) == 10266, "context intersection")
    require(len(coordinates["E3"] | coordinates["E4"]) == 22908, "unique source count")
    old_name = "../energy345/context01.json"
    old = load(old_name)
    pins[old_name] = pin(old_name)
    require(old["sources"]["E3"] == "Im10.jpg", "old context source")
    old_source_pin = old["inputs"].get("../../native-strips01/Im10.jpg")
    require(old_source_pin is not None and old_source_pin["sha256"] == SOURCE_SHA,
            "old context source pin")
    old_pixels = {(r["x"], r["y"]): r["rgb"] for r in old["cells"]["E3"]}
    require(len(old_pixels) == len(old["cells"]["E3"]), "old context duplicate coordinates")
    overlap = coordinates["E3"] & set(old_pixels)
    require(len(overlap) == 116, "old E3 terminal-context intersection")
    require(all(old_pixels[x, y] == rgb_at(raw, x, y) for x, y in overlap), "old overlap RGB")
    return raw, {"context_repeat_byte_equal": True, "records_per_context_run": 33174,
        "records_checked_across_two_runs": 66348, "E3_records": 10266,
        "E4_records": 22908, "unique_source_cells": 22908,
        "between_region_intersection": 10266, "old_E3_terminal_context_overlap_verified": 116,
        "old_overlap_is_context_only": True}


def rows_mask(values, box):
    require(type(values) is list and all(type(y) is int and box[1] <= y < box[3] for y in values),
            "row integer bounds")
    require(values == sorted(set(values)), "row order/uniqueness")
    return sum(1 << y for y in values)


def mask_rows(mask):
    return [y for y in range(92) if mask & (1 << y)]


def inspect_entry(row, box):
    require(type(row["x"]) is int and box[0] <= row["x"] < box[2], "entry column")
    core, fringe = rows_mask(row["core"], box), rows_mask(row["fringe"], box)
    require(not core & fringe, "core/fringe overlap")
    parts = row["fragment_membership"]
    require(type(parts) is list, "membership list")
    member_core = member_fringe = occupied = 0
    identifiers = []
    for member in parts:
        require(set(member) == {"fragment_id", "core", "fringe"}, "membership schema")
        name = member["fragment_id"]
        require(isinstance(name, str) and bool(name.strip()) and name not in identifiers,
                "unique explicit member identity")
        identifiers.append(name)
        c = rows_mask(member["core"], box)
        f = rows_mask(member["fringe"], box)
        require(c | f and not c & f and not occupied & (c | f), "member disjointness/nonempty")
        occupied |= c | f
        member_core |= c
        member_fringe |= f
    require((core, fringe) == (member_core, member_fringe), "exact member class unions")
    require(row["fragment_id"] == (identifiers[0] if len(identifiers) == 1 else None), "outer fragment identity")
    selected = core | fringe
    expected_flags = [name for applies, name in (
        (row["x"] == box[0], "target_left"), (row["x"] == box[2] - 1, "target_right"),
        (selected & (1 << box[1]), "target_top"),
        (selected & (1 << (box[3] - 1)), "target_bottom")) if applies] if selected else []
    require(row["boundary_flags"] == expected_flags, "boundary flags")
    require(isinstance(row["reason"], str) and bool(row["reason"].strip()), "entry reason")
    status = row["status"]
    require(status in STATUSES, "entry status")
    if status == "identified_local_fragment":
        require(bool(core), "identified without core")
    if status == "fringe_only":
        require(not core and bool(fringe), "fringe-only classes")
    if status == "boundary_truncated":
        require(selected and expected_flags, "boundary status without boundary")
    if status == "no_attributable_cells":
        require(not selected and not row["unassigned_band_refs"], "empty status loses ink/conflict")
    refs = row["unassigned_band_refs"]
    require(type(refs) is list and all(isinstance(s, str) and s for s in refs)
            and len(refs) == len(set(refs)), "reference schema/duplicates")
    return core, fringe


def coverage_attestation(data):
    coverage, pair, role = data["coverage"], data["pair"], data["reader"]
    context = CONTEXTS[pair]
    if (pair, role) == ("E3", "primary"):
        require(coverage["full_context_inspected"] is True and coverage["whole_strip_and_page_viewed"] is True
                and coverage["counterpart_new_annotation_read"] is False, "E3 primary attestation")
        blocks = [(b["columns"][0], b["columns"][1], b["receipt"]) for b in coverage["raw_blocks"]]
        count = coverage["raw_context_cells"]
    elif (pair, role) == ("E3", "peer"):
        require(coverage["all_context_cells_actually_read"] is True and not coverage["uncompleted_context"],
                "E3 peer attestation")
        require(coverage["row_range_inclusive"] == [33, 91] and bool(coverage["source_orientation"]),
                "E3 peer row/orientation attestation")
        blocks, count = coverage["blocks_inclusive_and_receipt"], coverage["context_cell_count"]
    elif role == "primary":
        require(coverage["complete_source_orientation"] is True and coverage["other_new_annotations_seen"] is False
                and not coverage["uncompleted_context_columns"], "E4 primary attestation")
        require(coverage["actual_rows"] == [0, 91], "E4 primary row attestation")
        require(all(b["truncated"] is False for b in coverage["read_receipts"]), "truncated read receipt")
        blocks = [(b["first"], b["last"], b["exec_chunk_id"]) for b in coverage["read_receipts"]]
        count = coverage["context_cells"]
    else:
        require(coverage["actual_read"] is True and not coverage["uncompleted_context_columns"], "E4 peer attestation")
        require(coverage["context_rows_inclusive"] == [0, 91] and bool(coverage["prior_knowledge"]),
                "E4 peer row/orientation attestation")
        blocks, count = coverage["finite_untruncated_receipts"], coverage["raw_context_cells"]
    require(all(type(a) is int and type(b) is int and a <= b and isinstance(receipt, str) and receipt
                for a, b, receipt in blocks), "finite read receipt schema")
    require([x for a, b, _ in blocks for x in range(a, b + 1)] == list(range(context[0], context[2])),
            "attested column coverage")
    require(count == (context[2] - context[0]) * (context[3] - context[1]), "attested cell count")
    return len(blocks)


def validate_annotation(data, pair, role, check_attestation=True):
    box = TARGETS[pair]
    require(data["pair"] == pair and data["region_id"] == pair + "-Im10" and data["source"] == "Im10.jpg",
            "annotation source identity")
    require(data["reader"] == role and data["target_box"] == box and data["context_box"] == CONTEXTS[pair],
            "annotation role/geometry")
    require(data["human_accepted"] is False and data["physical_support"] is None, "annotation acceptance")
    require(set(data["routes"]) == {"solid", "dash"}, "annotation route scope")
    if check_attestation:
        coverage_attestation(data)
    occupied, bands_by_key, bands_by_x = defaultdict(int), {}, defaultdict(list)
    for band in data["unassigned_bands"]:
        c, f = inspect_entry(band, box)
        key = (band["x"], band["band_id"])
        require(isinstance(key[1], str) and key[1] and key not in bands_by_key, "band identity/duplicate")
        candidates = band["candidate_routes"]
        require(type(candidates) is list and len(candidates) == len(set(candidates))
                and all(route in ("solid", "dash") for route in candidates), "candidate routes")
        require(bool(c | f) == bool(candidates), "band material/candidates")
        require(band["status"] != "identity_conflict" or c | f, "band conflict without ink")
        require(not occupied[band["x"]] & (c | f), "overlapping unassigned bands")
        occupied[band["x"]] |= c | f
        bands_by_key[key] = band
        bands_by_x[band["x"]].append(band)
    route_index = {}
    for route in ("solid", "dash"):
        records = data["routes"][route]
        require([r["x"] for r in records] == list(range(box[0], box[2])), "complete ordered route columns")
        for row in records:
            c, f = inspect_entry(row, box)
            require(not occupied[row["x"]] & (c | f), "duplicate selected source cell")
            occupied[row["x"]] |= c | f
            route_index[route, row["x"]] = row
            for ref in row["unassigned_band_refs"]:
                key = (row["x"], ref)
                require(key in bands_by_key and route in bands_by_key[key]["candidate_routes"],
                        "real route-specific same-column band reference")
            if row["status"] == "identity_conflict":
                require(bool(row["unassigned_band_refs"]), "route conflict without reference")
            if not c | f and row["unassigned_band_refs"]:
                require(row["status"] == "identity_conflict", "empty candidate route loses uncertainty")
    for (x, bid), band in bands_by_key.items():
        for route in band["candidate_routes"]:
            require(bid in route_index[route, x]["unassigned_band_refs"], "missing reciprocal candidate reference")
    return bands_by_x


def family(first, second):
    """Five operations via 92-bit membership, independent of producer sets."""
    a, b = sum(1 << y for y in first), sum(1 << y for y in second)
    return {"intersection": mask_rows(a & b), "union": mask_rows(a | b),
            "primary_only": mask_rows(a & ~b), "peer_only": mask_rows(b & ~a),
            "symmetric_difference": mask_rows(a ^ b)}


def comparison(first, second):
    return {label: family(first[label], second[label]) for label in ("core", "fringe")} | {
        "outer": family(sorted(first["core"] + first["fringe"]), sorted(second["core"] + second["fringe"]))}


def visible(records):
    masks = {label: 0 for label in ("core", "fringe")}
    for record in records:
        for label in masks:
            for y in record[label]:
                masks[label] |= 1 << y
    return {label: mask_rows(value) for label, value in masks.items()}


def totals(rows):
    return {"entries": len(rows), "outer_different": sum(bool(r["sets"]["outer"]["symmetric_difference"]) for r in rows),
            "class_different": sum(bool(r["sets"]["core"]["symmetric_difference"]
                                         or r["sets"]["fringe"]["symmetric_difference"]) for r in rows)}


def white_cells(data, raw):
    return [{"scope": scope, "class": label, "x": row["x"], "y": y}
            for scope, records in list(data["routes"].items()) + [("unassigned", data["unassigned_bands"])]
            for row in records for label in ("core", "fringe") for y in row[label]
            if rgb_at(raw, row["x"], y) == [255, 255, 255]]


def verify_comparison(output, readings, bands, pair, raw):
    require(output["pair"] == pair and output["region_id"] == pair + "-Im10", "comparison provenance")
    require(output["human_accepted"] is False and output["physical_support"] is None, "comparison acceptance")
    require(output["literal_readings"] == readings, "original annotations not preserved")
    require(output["literal_reproductions"] == {"primary": True, "peer": True}, "literal reproduction declaration")
    expected_routes = []
    for route in ("solid", "dash"):
        for a, b in zip(readings["primary"]["routes"][route], readings["peer"]["routes"][route]):
            expected_routes.append({"x": a["x"], "route": route, "primary_original": a,
                                    "peer_original": b, "sets": comparison(a, b)})
    require(output["route_comparisons"] == expected_routes, "route comparison/original mismatch")
    expected_ink = []
    for index, x in enumerate(range(TARGETS[pair][0], TARGETS[pair][2])):
        selections = {}
        for role in ("primary", "peer"):
            records = [readings[role]["routes"][r][index] for r in ("solid", "dash")]
            selections[role] = visible(records + bands[role].get(x, []))
        expected_ink.append({"x": x, "primary_unassigned_originals": bands["primary"].get(x, []),
            "peer_unassigned_originals": bands["peer"].get(x, []),
            "sets": comparison(selections["primary"], selections["peer"])})
    require(output["visible_ink_comparisons"] == expected_ink, "visible ink comparison/original mismatch")
    summary = {"routes": totals(expected_routes), "visible_ink": totals(expected_ink),
               "status_different": sum(r["primary_original"]["status"] != r["peer_original"]["status"] for r in expected_routes),
               "selected_exact_white_cells": {role: white_cells(data, raw) for role, data in readings.items()}}
    require(output["summary"] == summary, "summary or white-cell mismatch")
    return summary


def manual_controls():
    passed = []
    require(family([1, 2], [2, 3]) == {"intersection": [2], "union": [1, 2, 3],
        "primary_only": [1], "peer_only": [3], "symmetric_difference": [1, 3]}, "manual set arithmetic")
    passed.append("five_manual_set_operations")
    require(family([], [0, 91])["peer_only"] == [0, 91], "extreme/empty mask")
    passed.append("empty_and_native_rows_0_91")
    require(visible([{"core": [2], "fringe": [3]}, {"core": [4], "fringe": [5]}])
            == {"core": [2, 4], "fringe": [3, 5]}, "multiple band aggregation")
    passed.append("multiple_band_ink_retained")
    row = {"x": 195, "core": [35], "fringe": [36], "fragment_id": "piece",
           "fragment_membership": [{"fragment_id": "piece", "core": [35], "fringe": [36]}],
           "status": "boundary_truncated", "reason": "synthetic", "boundary_flags": ["target_left", "target_top"],
           "unassigned_band_refs": []}
    inspect_entry(row, TARGETS["E3"])
    passed.append("manual_membership_class_boundary")
    for label, change in (("duplicate_row", lambda r: r.update(core=[35, 35])),
                          ("class_overlap", lambda r: r.update(fringe=[35])),
                          ("lost_membership", lambda r: r.update(fragment_membership=[])),
                          ("lost_boundary", lambda r: r.update(boundary_flags=[])),
                          ("boolean_row", lambda r: r.update(core=[True]))):
        bad = copy.deepcopy(row)
        change(bad)
        try:
            inspect_entry(bad, TARGETS["E3"])
        except ValueError:
            passed.append(label + "_rejected")
        else:
            raise ValueError(label + " accepted")
    raw = bytes([255, 255, 255]) * (745 * 92)
    sample = [{"x": 0, "y": 0, "rgb": [255, 255, 255]}]
    context_records(sample, [0, 0, 1, 1], raw)
    sample[0]["rgb"][0] = 254
    try:
        context_records(sample, [0, 0, 1, 1], raw)
    except ValueError:
        passed.append("in_memory_RGB_corruption_rejected")
    else:
        raise ValueError("corrupted RGB accepted")
    empty = dict(x=195, core=[], fringe=[], fragment_id=None,
        fragment_membership=[], status="no_attributable_cells", reason="synthetic",
        boundary_flags=[], unassigned_band_refs=[])
    fixture = dict(pair="E3", region_id="E3-Im10", source="Im10.jpg", reader="primary",
        target_box=TARGETS["E3"], context_box=CONTEXTS["E3"], human_accepted=False,
        physical_support=None, routes={}, unassigned_bands=[])
    for route, y in (("solid", 60), ("dash", 70)):
        fixture["routes"][route] = [dict(copy.deepcopy(empty), x=x) for x in range(195, 365)]
        band = dict(copy.deepcopy(empty), x=196, core=[y], fragment_id=route,
            fragment_membership=[{"fragment_id": route, "core": [y], "fringe": []}],
            status="identified_local_fragment", band_id=route, candidate_routes=[route])
        fixture["unassigned_bands"].append(band)
        fixture["routes"][route][1].update(status="identity_conflict", unassigned_band_refs=[route])
    require(len(validate_annotation(fixture, "E3", "primary", False)[196]) == 2,
            "two route-specific synthetic bands lost")
    passed.append("two_same_column_route_specific_bands")
    for label in ("candidate_mismatch", "missing_reciprocal"):
        bad = copy.deepcopy(fixture)
        if label == "candidate_mismatch":
            bad["unassigned_bands"][0]["candidate_routes"] = ["dash"]
        else:
            bad["routes"]["solid"][1].update(status="no_attributable_cells", unassigned_band_refs=[])
        try:
            validate_annotation(bad, "E3", "primary", False)
        except ValueError:
            passed.append(label + "_rejected")
        else:
            raise ValueError(label + " accepted")
    white_fixture = {"routes": {"solid": [{"x": 0, "core": [0], "fringe": []}]}, "unassigned_bands": []}
    require(white_cells(white_fixture, raw) == [{"scope": "solid", "class": "core", "x": 0, "y": 0}],
            "selected exact-white detection")
    near_white_raw = bytes([254, 255, 255]) + raw[3:]
    require(not white_cells(white_fixture, near_white_raw), "near-white falsely omitted")
    passed.append("exact_white_flag_and_near_white_retention")
    return passed


def check_all(context_only=False):
    controls = manual_controls()
    pins = {"independent_check.py": pin("independent_check.py")}
    raw, context_receipt = check_contexts(pins)
    if context_only:
        require(all(pin(name) == expected for name, expected in pins.items()), "inputs changed during context check")
        return {"status": "context_fidelity_only_pass", "contexts": context_receipt,
                "synthetic_controls": controls, "inputs": pins, "inputs_after": pins}
    all_readings, all_bands, annotation_receipts = {}, {}, {}
    for pair in ("E3", "E4"):
        all_readings[pair], all_bands[pair] = {}, {}
        for role in ("primary", "peer"):
            name = f"reader-{pair}-{role}.json"
            require(pin(name)["sha256"] == READING_SHAS[name], "frozen annotation changed: " + name)
            pins[name] = pin(name)
            data = load(name)
            required = {"PROTOCOL.md", "READERS.md", "context01.json", "context02.json", SOURCE}
            require(required <= set(data["inputs"]), "reader required input roster")
            pin_inputs(data["inputs"], pins)
            script = name.replace(".json", ".py")
            pin_inputs({script: data["script_pin"]}, pins)
            # Literal-build replay only; independent validation below uses no
            # reader validation/classification/row-expansion function.
            spec = importlib.util.spec_from_file_location("literal_" + pair + "_" + role, HERE / script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            first, second = module.build(), module.build()
            require(first == second == data, "literal build replay mismatch: " + name)
            reconstructed = (json.dumps(first, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
            require(reconstructed == (HERE / name).read_bytes(), "literal serialized bytes mismatch: " + name)
            bands = validate_annotation(data, pair, role)
            all_readings[pair][role], all_bands[pair][role] = data, bands
            annotation_receipts[name] = {"route_records": sum(len(v) for v in data["routes"].values()),
                "band_records": len(data["unassigned_bands"]), "multiple_band_columns": sum(len(v) > 1 for v in bands.values()),
                "read_receipt_blocks": coverage_attestation(data), "two_literal_builds_and_saved_bytes_equal": True,
                "selected_exact_white_count": len(white_cells(data, raw)),
                "band_status_counts": dict(Counter(b["status"] for b in data["unassigned_bands"]))}
    summaries, operation_count = {}, 0
    for pair in ("E3", "E4"):
        first_name, second_name = f"comparison-{pair}-01.json", f"comparison-{pair}-02.json"
        require((HERE / first_name).read_bytes() == (HERE / second_name).read_bytes(), "comparison repeat bytes")
        for name in (first_name, second_name):
            pins[name] = pin(name)
            output = load(name)
            pin_inputs(output["input_pins"], pins)
            pin_inputs(output["dependencies"], pins)
            pin_inputs({"compare.py": output["script_pin"], "test_compare.py": output["test_pin"]}, pins)
            summaries[pair] = verify_comparison(output, all_readings[pair], all_bands[pair], pair, raw)
            operation_count += 15 * (len(output["route_comparisons"]) + len(output["visible_ink_comparisons"]))
        corrupted = copy.deepcopy(output)
        corrupted["route_comparisons"][0]["sets"]["outer"]["union"] = [0]
        try:
            verify_comparison(corrupted, all_readings[pair], all_bands[pair], pair, raw)
        except ValueError as error:
            require("route comparison" in str(error), "corruption failed for unexpected reason")
            controls.append(pair + "_in_memory_set_corruption_rejected")
        else:
            raise ValueError("corrupted comparison accepted")
    after = {name: pin(name) for name in pins}
    require(after == pins, "inputs changed during independent check")
    route_count = sum(r["route_records"] for r in annotation_receipts.values())
    band_count = sum(r["band_records"] for r in annotation_receipts.values())
    require(route_count == 1660 and band_count == 228 and operation_count == 37350, "full scope count")
    return {"status": "pass_native_ink_bookkeeping_only", "contexts": context_receipt,
            "annotations": annotation_receipts, "comparisons": summaries,
            "coverage": {"original_annotations": 4, "route_records": route_count, "band_records": band_count,
                         "comparison_files": 4, "operation_arrays_checked": operation_count},
            "synthetic_controls": controls, "inputs": pins, "inputs_after": after,
            "environment": {"python": platform.python_version(), "pillow": pillow_version, "executable": sys.executable},
            "independence": "Checker author did not annotate this batch. Raw source bytes/RGB, schema and 92-bit arithmetic independently checked; four frozen reader builds imported only for replay. No compare/read_context/force helper imported.",
            "failures_and_repairs": [
                "Preflight system python3 lacked PIL (receipt 721f30); bundled Python used. No source or annotation repaired.",
                "First --save completed checks but receipt creation was denied by the exec filesystem sandbox (PermissionError, receipt f549df). No receipt was created; exact local save requested through sandbox escalation."],
            "limits": ["Reading receipts are computational-reader self-attestations, not independently witnessed perception.",
                       "RGB equality and set operations establish bookkeeping, not historical curve identity, support, physical envelopes, model accuracy or cause.",
                       "All original annotations, multiple bands, reader differences and exact-white selections remain preserved."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context-only", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    require(not(args.context_only and args.save), "context-only receipt is stdout only")
    target = HERE / "independent-check.json"
    if args.save and target.exists():
        raise FileExistsError("Existing independent receipt preserved")
    try:
        result = check_all(args.context_only)
    except (AssertionError, KeyError, ValueError, TypeError, OSError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__, "error": str(error)}, indent=2))
        return 1
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.save:
        with target.open("x") as stream:
            stream.write(encoded)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
