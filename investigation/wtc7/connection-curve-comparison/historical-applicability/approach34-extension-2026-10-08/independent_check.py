"""Independent check of the bounded approach extension; no producer imports.

Uses two explicitly pinned prior independent oracles: annotation validation
only (no image access), and raw-CTM conditional geometry. The copy adapter,
inventory/preservation checks and corruption controls below are new code.
This is not another annotation reading or a check of the physical hypotheses.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = "historical-applicability/conditional-envelopes-2026-10-08/"
APP = "native-footprint-pass/approach34/"
NEW = "historical-applicability/approach34-extension-2026-10-08/"
RECON = "historical-applicability/footprint-reconciliation-2026-10-08.json"
TARGETS = {"E3": [195, 35, 365, 92], "E4": [195, 0, 440, 92]}
ORDER = [(pair, role) for pair in TARGETS for role in ("primary", "peer")]
REVIEWED_NARRATIVE_SHA = "e9ccc015a282548e0d72ed92ba695faa696040674f0b075c34e9e6b9f34540c0"
FIXED = {
    RECON: "ed4a1ded5e53b7d102c9462f5f939883640359da5c0472220a92fbba1b7a354e",
    OLD + "run01.json": "940947030c60d1b5a4d0b1f9ac4f3191db7fb8b355337b47062b796f4ce73678",
    OLD + "run02.json": "940947030c60d1b5a4d0b1f9ac4f3191db7fb8b355337b47062b796f4ce73678",
    OLD + "independent_check.py": "8f83a8b591de73aef342ecb6d01830cd012eb0593e43731236ba73f553ad69f0",
    APP + "independent_check.py": "15c43d9b2fc119fcbe5e6b6a4ad0c28c0bea03e82dcbb16b4a49d925d0ec63fc",
    APP + "independent-check.json": "fd38b2f372166c124fe46e908e9eeef2bfd20f92e4e3e24fb7d1d375a6072c23",
    NEW + "PROTOCOL.md": "c6c076c087df0d831e93f5680d8c5a1c4b653196fe2ab9731df17d69079d9590",
    NEW + "PROTOCOL-V2.md": "8f7bfe352480c263437bb1e1ac7d9b6653c13a724d50a12dc01be53724f741a2",
    NEW + "extend.py": "18f5862d014c5e9848cd6332da3929437c7ff93031e3ca255730d1f9e0dfc3f0",
    NEW + "test_extend.py": "64e89b9da53ce259c4415166afbdcdd9d3e9caab9d68bf004c49cf5188488981",
    NEW + "run01.json": "eba3bb5fd8913751052c68b71d0efad3f8fd0da12977a579a85fd793c7406ce7",
    NEW + "run02.json": "eba3bb5fd8913751052c68b71d0efad3f8fd0da12977a579a85fd793c7406ce7",
    "pypdf-representation01.json": "1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin(file):
    raw = file.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def load(file):
    return json.loads(file.read_text(), parse_float=Fraction)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def exact(first, second):
    # Unlike Python container equality, distinguish JSON false from numeric 0.
    return digest(first) == digest(second)


def relative(file):
    return str(file.resolve().relative_to(BASE))


def import_oracle(name, relative_path):
    file = BASE / relative_path
    require(pin(file)["sha256"] == FIXED[relative_path], "oracle pin: " + relative_path)
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependency_closure(root_files, read_json=load, get_pin=pin):
    """Breadth-first pin graph, including reached JSONs, not a copied roster.

    These source annotation/context/receipt pin maps are document-directory
    relative. The older conditional bundle is handled separately because its
    pin paths are C-relative. No JSON cell arrays are interpreted here.
    """
    pending, visited, collected = [], set(), {}

    def add(file, wanted=None, sha=None):
        name = relative(file)
        observed = get_pin(BASE / name)
        require(type(observed) is dict and set(observed) == {"bytes", "sha256"}, "pin schema")
        require(wanted is None or observed == wanted, "transitive dependency mismatch: " + name)
        require(sha is None or observed["sha256"] == sha, "transitive SHA mismatch: " + name)
        require(name not in collected or collected[name] == observed, "conflicting transitive pins: " + name)
        if name not in collected:
            collected[name] = observed
            if name.endswith(".json"):
                pending.append(name)

    for file in root_files:
        add(file)
    while pending:
        name = pending.pop(0)
        if name in visited:
            continue
        visited.add(name)
        file = BASE / name
        data = read_json(file)
        require(type(data) is dict, "dependency JSON object")
        if "inputs_after" in data:
            require(data["inputs_after"] == data["inputs"], "transitive before/after mismatch: " + name)
        for key in ("inputs", "inputs_after", "dependencies", "input_pins"):
            if key in data:
                require(type(data[key]) is dict, "dependency map schema: " + name + ":" + key)
                for child, wanted in data[key].items():
                    require(type(wanted) is dict and set(wanted) == {"bytes", "sha256"}, "declared child pin schema")
                    add(file.parent / child, wanted=wanted)
        for key in ("artifact_sha256", "source_sha256"):
            for child, sha in data.get(key, {}).items():
                add(file.parent / child, sha=sha)
        if "script_pin" in data:
            if file.name.startswith("reader-"):
                script = file.with_suffix(".py")
            else:
                require(file.name.startswith("comparison-"), "unknown script-pin schema")
                script = file.parent / "compare.py"
            add(script, wanted=data["script_pin"])
        if "test_pin" in data:
            require(file.name.startswith("comparison-"), "unknown test-pin schema")
            add(file.parent / "test_compare.py", wanted=data["test_pin"])
    return collected, sorted(visited)


def adapt(original, annotation_oracle):
    """Validate first, then change one key on independent deep copies only."""
    annotation_oracle.validate_annotation(original, original["pair"], original["reader"])
    snapshot = copy.deepcopy(original)
    adapted = copy.deepcopy(original)
    for route in ("solid", "dash"):
        for row in adapted["routes"][route]:
            # Any legacy alias is ambiguous even if it happens to agree today.
            require(not set(row) & {"column", "core_rows", "fringe_rows", "fragments", "band_refs"},
                    "ambiguous old/new route aliases")
            membership = row.pop("fragment_membership")
            require(type(membership) is list, "adapter requires list membership")
            row["fragments"] = membership
    require(original == snapshot, "adapter changed original")
    # Invert our sole permitted transformation and demand complete equality.
    round_trip = copy.deepcopy(adapted)
    for route in ("solid", "dash"):
        for row in round_trip["routes"][route]:
            row["fragment_membership"] = row.pop("fragments")
    require(round_trip == original, "adapter changed fields beyond membership key")
    return adapted


def region(pair):
    return {"source": "Im10", "target_box": TARGETS[pair], "readers": [
        {"path": APP + f"reader-{pair}-{role}.json",
         "route_records": 2 * (TARGETS[pair][2] - TARGETS[pair][0]),
         "target_source_field": "target_box", "human_accepted_field": False,
         "physical_support_field": None} for role in ("primary", "peer")]}


def expected_new_readings(originals, annotation_oracle, geometry_oracle, invocation):
    expected = []
    for pair, role in ORDER:
        name = APP + f"reader-{pair}-{role}.json"
        data = adapt(originals[name], annotation_oracle)
        rows = geometry_oracle.serialized(geometry_oracle.expected_rows(data, region(pair), "E", invocation))
        expected.append({"pair": pair, "source": "Im10", "reader_path": name, "rows": rows,
                         "summary": {"records": len(rows),
                                     "conditional_windows": sum(r["conditional_window"] for r in rows),
                                     "reasons_nonexclusive": dict(Counter(k for r in rows for k in r["reasons"]))}})
    return expected


def candidates(pairs, sources):
    present, absent = [], []
    for pair in pairs:
        seen = set()
        for completed in pair["completed_footprints"]:
            require(len(completed["readers"]) == 2, "original role count")
            for role_index, reader in enumerate(completed["readers"]):
                source = sources[reader["path"]]
                routes = source.get("routes")
                if routes is None:
                    routes = {route: [r for r in source["observations"] if r["route"] == route]
                              for route in ("solid", "dash")}
                for route, rows in routes.items():
                    require(route in ("solid", "dash"), "candidate route")
                    if any(r["status"] == "identified_local_fragment" and
                           r["core_rows" if "column" in r else "core"] for r in rows):
                        seen.add((role_index, route))
        (present if seen == {(i, r) for i in (0, 1) for r in ("solid", "dash")} else absent).append(pair["pair"])
    return present, absent


def check_inventory(actual, old, sources):
    require(set(actual) == {"pairs", "counts", "candidate_presence", "preserved_corrections", "acceptance", "claims"},
            "inventory top-level schema")
    require(exact(actual["acceptance"], old["acceptance"]) and
            exact(actual["preserved_corrections"], old["preserved_corrections"]), "acceptance/corrections changed")
    require([p["pair"] for p in actual["pairs"]] == [p["pair"] for p in old["pairs"]], "pair roster/order")
    mutable = {"completed_footprints", "additional_batches", "remaining_inventory",
               "identity_and_topology_limits", "next_evidence_action"}
    changed = []
    for found, prior in zip(actual["pairs"], old["pairs"]):
        pair = prior["pair"]
        if pair not in TARGETS:
            require(exact(found, prior), "nonallowlisted pair changed: " + pair)
            continue
        require(set(found) == set(prior) | {"additional_batches"}, "pair schema changed: " + pair)
        require(exact({k: v for k, v in found.items() if k not in mutable},
                {k: v for k, v in prior.items() if k not in mutable}), "nonallowlisted field changed: " + pair)
        require(exact(found["completed_footprints"], prior["completed_footprints"] + [region(pair)]),
                "appended region differs: " + pair)
        require(found["additional_batches"] == [{"report": APP + "report.md", "verification": APP + "verification.json"}],
                "additional batch links: " + pair)
        for field in sorted(mutable - {"completed_footprints", "additional_batches"}):
            require(isinstance(found[field], str) and found[field].strip() and found[field] != prior[field],
                    "missing residual update: " + pair + ":" + field)
        changed += [pair + "/" + field for field in sorted(mutable)]
    completed = [r for p in actual["pairs"] for r in p["completed_footprints"]]
    readings = [r for c in completed for r in c["readers"]]
    counts = {"pairs": len(actual["pairs"]), "completed_regions": len(completed),
              "original_readings": len(readings), "original_route_records": sum(r["route_records"] for r in readings)}
    require(actual["counts"] == counts == {"pairs": 14, "completed_regions": 19,
            "original_readings": 38, "original_route_records": 12500}, "inventory counts")
    require(len({r["path"] for r in readings}) == 38, "duplicate reading path")
    present, absent = candidates(actual["pairs"], sources)
    presence = actual["candidate_presence"]
    require(set(presence) == {"criterion", "limits", "pairs_with_both_style_candidates", "pairs_without_both_style_candidates"},
            "presence schema")
    require(presence["criterion"] == old["annotation_candidate_presence"]["criterion"], "candidate criterion changed")
    require(presence["pairs_with_both_style_candidates"] == present and
            presence["pairs_without_both_style_candidates"] == absent, "candidate presence mismatch")
    require(isinstance(presence["limits"], str) and bool(presence["limits"]), "presence limits")
    require(len(actual["claims"]) == 3 and all(set(c) == {"claim", "type", "strength", "support", "falsifier"}
            and all(isinstance(v, str) and v.strip() for v in c.values()) for c in actual["claims"]), "claim schema")
    return changed


def check_bundle(actual, prior, inventory, originals, expected, sources):
    require(set(actual) == {"status", "inputs", "inputs_after", "prior_inventory", "prior_conditional_result",
            "inventory", "new_source_originals", "readings", "axis_boxes", "records", "assumptions",
            "human_accepted", "common_support", "quantile_targets", "model_discrepancies",
            "shared_axis_parameters", "conditional_window_counts", "limits"}, "bundle schema")
    require(actual["status"] == "conditional_preparation_extension_not_accepted_measurement", "status")
    require(actual["prior_inventory"] == RECON and actual["prior_conditional_result"] == OLD + "run01.json", "prior references")
    require(exact(actual["readings"][:34], prior["readings"]), "prior 34 readings changed")
    require(exact(actual["readings"][34:], expected), "new conditional reading differs from independent reconstruction")
    require(exact(actual["new_source_originals"], originals), "complete original preservation failed")
    require(exact(actual["axis_boxes"], prior["axis_boxes"]) and exact(actual["assumptions"], prior["assumptions"]), "axes/assumptions changed")
    require(actual["human_accepted"] is False and actual["shared_axis_parameters"] is True, "acceptance/correlation flags")
    require(all(actual[k] is None for k in ("common_support", "quantile_targets", "model_discrepancies")), "downstream claim")
    require(actual["records"] == sum(len(r["rows"]) for r in actual["readings"]) == 12500, "total records")
    before_count = sum(r["summary"]["conditional_windows"] for r in prior["readings"])
    new_count = sum(r["summary"]["conditional_windows"] for r in expected)
    require(actual["conditional_window_counts"] == {"prior": before_count, "new": new_count, "total": before_count + new_count},
            "conditional counts")
    require(isinstance(actual["limits"], str) and bool(actual["limits"]), "bundle limits")
    return check_inventory(actual["inventory"], inventory, sources)


def rejected(name, operation, controls):
    try:
        operation()
    except (ValueError, KeyError, TypeError, AssertionError):
        controls.append(name)
    else:
        raise ValueError("corruption/control wrongly admitted: " + name)


def closure_controls():
    controls = []
    root, child = BASE / NEW / "synthetic/root.json", BASE / NEW / "synthetic/leaf.json"
    pins = {root: {"bytes": 100, "sha256": "0" * 64}, child: {"bytes": 200, "sha256": "1" * 64}}
    documents = {root: {"inputs": {"../synthetic/leaf.json": pins[child]}}, child: {"inputs": {"root.json": pins[root]}}}
    read = lambda file: documents[file]
    get = lambda file: pins[file]
    result, nodes = dependency_closure([root], read, get)
    require(result == {relative(p): v for p, v in pins.items()} and len(nodes) == 2, "normalized cyclic closure")
    controls.append("synthetic_recursive_closure_normalizes_paths_and_terminates_cycle")
    documents[root]["inputs"]["leaf.json"] = {"bytes": 999, "sha256": "2" * 64}
    rejected("synthetic_conflicting_normalized_dependency_rejected", lambda: dependency_closure([root], read, get), controls)
    del documents[root]["inputs"]["leaf.json"]
    documents[root]["inputs_after"] = {}
    rejected("synthetic_dependency_before_after_change_rejected", lambda: dependency_closure([root], read, get), controls)
    del documents[root]["inputs_after"]
    documents[child]["inputs"]["root.json"] = {"bytes": 100, "sha256": "3" * 64}
    rejected("synthetic_changed_descendant_dependency_rejected", lambda: dependency_closure([root], read, get), controls)
    return controls


def synthetic_controls(annotation_oracle, geometry_oracle):
    controls = list(geometry_oracle.manual_checks()) + closure_controls()
    # This complete synthetic original uses real geometry/attestation shapes,
    # but no saved selections or source pixels. All selected cells are invented.
    def row(x, core=(), refs=(), status="no_attributable_cells", fid=None):
        return {"x": x, "core": list(core), "fringe": [], "fragment_id": fid,
                "fragment_membership": ([{"fragment_id": fid, "core": list(core), "fringe": []}] if core else []),
                "status": status, "reason": "synthetic", "boundary_flags": [], "unassigned_band_refs": list(refs)}
    sample = {"pair": "E3", "region_id": "E3-Im10", "source": "Im10.jpg", "reader": "primary",
              "target_box": TARGETS["E3"], "context_box": [193, 33, 367, 92],
              "human_accepted": False, "physical_support": None,
              "coverage": {"full_context_inspected": True, "whole_strip_and_page_viewed": True,
                           "counterpart_new_annotation_read": False, "raw_context_cells": 10266,
                           "raw_blocks": [{"columns": [193, 366], "receipt": "synthetic-not-a-source-receipt"}]},
              "routes": {r: [row(x) for x in range(195, 365)] for r in ("solid", "dash")},
              "unassigned_bands": []}
    for route, selected, bid in (("solid", 60, "band-a"), ("dash", 62, "band-b")):
        band = row(250, [selected], status="identified_local_fragment", fid=bid)
        band.update(band_id=bid, candidate_routes=[route])
        sample["unassigned_bands"].append(band)
        sample["routes"][route][55] = row(250, refs=[bid], status="identity_conflict")
    for x in range(260, 265):
        sample["routes"]["solid"][x - 195] = row(x, [55], status="identified_local_fragment", fid="fragment-a")
    saved = copy.deepcopy(sample)
    adapted = adapt(sample, annotation_oracle)
    require(sample == saved and adapted["unassigned_bands"] == saved["unassigned_bands"], "synthetic copy preservation")
    controls.append("synthetic_copy_only_adapter_preserves_two_route_specific_same_column_bands")
    require("fragments" in adapted["routes"]["solid"][65] and "fragment_membership" not in adapted["routes"]["solid"][65], "synthetic key change")
    controls.append("synthetic_adapter_changes_only_membership_key")
    for alias, value in (("column", 260), ("core_rows", [55]), ("fringe_rows", []), ("fragments", []), ("band_refs", [])):
        bad = copy.deepcopy(sample)
        bad["routes"]["solid"][65][alias] = value
        rejected("synthetic_alias_" + alias, lambda: adapt(bad, annotation_oracle), controls)
    for name, mutate in (
        ("duplicate_membership", lambda s: s["routes"]["solid"][65]["fragment_membership"].append(copy.deepcopy(s["routes"]["solid"][65]["fragment_membership"][0]))),
        ("incorrect_member_union", lambda s: s["routes"]["solid"][65]["fragment_membership"][0]["core"].append(56)),
        ("broken_reciprocal", lambda s: s["unassigned_bands"][0]["candidate_routes"].append("dash")),
        ("route_coverage_loss", lambda s: s["routes"]["solid"].pop()),
        ("attested_coverage_loss", lambda s: s["coverage"]["raw_blocks"][0].update(columns=[194, 366])),
    ):
        bad = copy.deepcopy(sample)
        mutate(bad)
        rejected("synthetic_" + name, lambda: adapt(bad, annotation_oracle), controls)
    invocation = {"native_dimensions": [745, 92], "ctm": [Fraction(745, 3), 0, 0, Fraction(92, 3), 160, 200]}
    decisions = geometry_oracle.expected_rows(adapted, region("E3"), "E", invocation)
    solid = {r["column"]: r for r in decisions if r["route"] == "solid"}
    require([x for x in range(260, 265) if solid[x]["conditional_window"]] == [261, 262, 263], "synthetic noniterative neighbor exclusion")
    require("unassigned_band_reference" in solid[250]["reasons"] and not solid[250]["conditional_window"], "synthetic band exclusion")
    controls += ["synthetic_noniterative_neighbor_guard_after_adaptation", "synthetic_band_reference_withheld_after_adaptation"]
    return controls


def check_all(self_test=False):
    fixed_before = {name: pin(BASE / name) for name in FIXED}
    require(all(fixed_before[name]["sha256"] == sha for name, sha in FIXED.items()), "fixed dependency pin")
    annotation = import_oracle("independent_approach_annotation_oracle", APP + "independent_check.py")
    geometry = import_oracle("independent_prior_conditional_oracle", OLD + "independent_check.py")
    controls = synthetic_controls(annotation, geometry)
    if self_test:
        return {"status": "synthetic_controls_pass", "controls": controls}
    run_pins = {name: pin(HERE / name) for name in ("run-v2-01.json", "run-v2-02.json")}
    require((HERE / "run-v2-01.json").read_bytes() == (HERE / "run-v2-02.json").read_bytes(), "extension V2 repeat bytes")
    checker_pin = pin(Path(__file__))
    review_context = {APP + "report.md": pin(BASE / APP / "report.md")}
    actual, prior, inventory = load(HERE / "run-v2-01.json"), load(BASE / (OLD + "run01.json")), load(BASE / RECON)
    v1 = load(HERE / "run01.json")
    require(actual["version"] == 2 and actual["status"] == "conditional_preparation_extension_v2_not_accepted_measurement", "V2 version/status")
    metadata = {"status", "inputs", "inputs_after", "version", "repair_provenance"}
    require(exact({k: v for k, v in actual.items() if k not in metadata}, {k: v for k, v in v1.items() if k not in metadata}),
            "V2 substantive payload differs from V1")
    provenance = actual["repair_provenance"]
    require(set(provenance) == {"prior_outputs_preserved", "prior_verification_limit", "dependency_map_roots",
            "substantive_payload_identical_to_v1", "new_scientific_result"}, "repair provenance schema")
    require(provenance["prior_outputs_preserved"] == [NEW + "run01.json", NEW + "run02.json"] and
            provenance["substantive_payload_identical_to_v1"] is True and provenance["new_scientific_result"] is False,
            "repair provenance flags")
    require(isinstance(provenance["prior_verification_limit"], str) and provenance["prior_verification_limit"], "V1 limitation missing")
    require(actual["inputs"] == actual["inputs_after"], "producer pins changed")
    before = {name: pin(BASE / name) for name in actual["inputs"]}
    require(all(relative(BASE / name) == name for name in before), "noncanonical or outside-C input path")
    require(before == actual["inputs"], "producer pins differ from files")
    require(v1["inputs"] == v1["inputs_after"], "V1 before/after pins")
    require(all(v1["inputs"].get(name) == wanted for name, wanted in prior["inputs"].items()), "V1 omitted prior pins")
    required = dict(v1["inputs"])
    required.update({name: pin(BASE / name) for name in (RECON, OLD + "run01.json", OLD + "run02.json",
        OLD + "independent-check.json", APP + "verification.json", NEW + "PROTOCOL.md",
        NEW + "extend.py", NEW + "test_extend.py", NEW + "run01.json", NEW + "run02.json",
        NEW + "PROTOCOL-V2.md", NEW + "extend_v2.py", NEW + "test_extend_v2.py")})
    manifest = load(BASE / (APP + "verification.json"))
    for field in ("artifact_sha256", "source_sha256"):
        for name, sha in manifest[field].items():
            canonical = relative(BASE / APP / name)
            observed = pin(BASE / canonical)
            require(observed["sha256"] == sha, "approach manifest pin: " + name)
            required[canonical] = observed
    originals = {}
    for pair, role in ORDER:
        name = APP + f"reader-{pair}-{role}.json"
        originals[name] = load(BASE / name)
        require(pin(BASE / name)["sha256"] == annotation.READING_SHAS[Path(name).name], "original reader pin")
        for dependency, expected_pin in originals[name]["inputs"].items():
            canonical = relative(BASE / APP / dependency)
            require(pin(BASE / canonical) == expected_pin, "original transitive dependency")
            required[canonical] = expected_pin
        require(pin((BASE / name).with_suffix(".py")) == originals[name]["script_pin"], "literal reader script pin")
    root_files = [BASE / APP / name for name in ("verification.json", "independent-check.json", "context01.json", "context02.json")]
    closure, json_nodes = dependency_closure(root_files + [BASE / name for name in originals])
    v1_missing = sorted(set(closure) - set(v1["inputs"]))
    require(v1_missing == ["native-footprint-pass/PROTOCOL.md", "native-footprint-pass/energy345/PROTOCOL.md",
            "native-footprint-pass/energy345/context01.json", "native-footprint-pass/energy345/read_context.py",
            "native-footprint-pass/read_context.py", "native-strips01/Im9.jpg"], "retained V1 closure diagnosis changed")
    for name, wanted in closure.items():
        require(name not in required or required[name] == wanted, "conflicting required pin")
        required[name] = wanted
    require(before == required, "required recursive input union omitted, changed or unexpectedly expanded")
    expected_root_maps = set()
    for name in json_nodes:
        content = load(BASE / name)
        for field in ("inputs", "inputs_after", "dependencies", "input_pins"):
            if field in content:
                expected_root_maps.add((name, field, relative((BASE / name).parent)))
        if name in originals:
            expected_root_maps.add((name, "script_pin", APP.rstrip("/")))
    declared_root_maps = []
    for declared in provenance["dependency_map_roots"]:
        require(set(declared) == {"path", "field", "relative_to"}, "declared dependency root schema")
        file = BASE / declared["path"]
        require(relative(file) in json_nodes, "declared dependency root outside actual graph")
        require(declared["relative_to"] == relative(file.parent), "declared dependency coordinate base")
        content = load(file)
        require(declared["field"] in content and type(content[declared["field"]]) is dict, "declared dependency map missing")
        declared_root_maps.append((declared["path"], declared["field"], declared["relative_to"]))
    require(len(declared_root_maps) == len(set(declared_root_maps)) and set(declared_root_maps) == expected_root_maps,
            "declared dependency root roster incomplete or duplicated")
    invocations = load(BASE / "pypdf-representation01.json")["image_invocations"]
    invocation = [i for i in invocations if i["name"] == "Im10"]
    require(len(invocation) == 1 and invocation[0]["native_dimensions"] == [745, 92], "Im10 invocation identity")
    expected = expected_new_readings(originals, annotation, geometry, invocation[0])
    sources = dict(originals)
    for pair in inventory["pairs"]:
        for completed in pair["completed_footprints"]:
            for reader in completed["readers"]:
                sources[reader["path"]] = load(BASE / reader["path"])
    normalized = {k: v for k, v in actual.items() if k not in {"version", "repair_provenance"}}
    normalized["status"] = v1["status"]
    changed = check_bundle(normalized, prior, inventory, originals, expected, sources)
    # Deliberate changes are strictly in memory; every one must fail the same
    # full comparison used for the untouched result, not a special test-only gate.
    for name, mutate in (
        ("old_reading_decision_changed", lambda b: b["readings"][0]["rows"][0]["reasons"].append("invented")),
        ("old_json_false_changed_to_numeric_zero", lambda b: b["readings"][0]["rows"][0].update(curve_support_established=0)),
        ("new_omitted_exclusion_reason", lambda b: next(r for r in b["readings"][34]["rows"] if r["reasons"])["reasons"].pop()),
        ("new_ordinate_hull_changed", lambda b: next(r for r in b["readings"][34]["rows"] if r["conditional_window"])["physical_windows"][0]["ordinate"].__setitem__(0, "0")),
        ("original_band_lost", lambda b: b["new_source_originals"][APP + "reader-E4-primary.json"]["unassigned_bands"].pop()),
        ("outside_allowlist_pair_changed", lambda b: b["inventory"]["pairs"][0].update(bounds_status="invented")),
        ("allowlist_pair_protected_field_changed", lambda b: next(p for p in b["inventory"]["pairs"] if p["pair"] == "E3").update(bounds_status="invented")),
        ("same_source_old_target_overwritten", lambda b: next(p for p in b["inventory"]["pairs"] if p["pair"] == "E3")["completed_footprints"][0].update(target_box=TARGETS["E3"])),
        ("candidate_presence_removed", lambda b: b["inventory"]["candidate_presence"]["pairs_with_both_style_candidates"].pop()),
    ):
        bad = copy.deepcopy(normalized)
        mutate(bad)
        rejected(name, lambda: check_bundle(bad, prior, inventory, originals, expected, sources), controls)
    for name in v1_missing:
        damaged = dict(before)
        del damaged[name]
        rejected("missing_required_pin_" + name, lambda: require(damaged == required, "required closure pin absent"), controls)
    rows = [r for reading in expected for r in reading["rows"]]
    count = sum(r["conditional_window"] for r in rows)
    narrative = {"pair_residuals": [{k: p[k] for k in ("pair", "remaining_inventory", "identity_and_topology_limits", "next_evidence_action")}
                                   for p in actual["inventory"]["pairs"] if p["pair"] in TARGETS],
                 "claims": actual["inventory"]["claims"], "presence_limits": actual["inventory"]["candidate_presence"]["limits"],
                 "bundle_limits": actual["limits"]}
    require(digest(narrative) == REVIEWED_NARRATIVE_SHA, "narrative differs from manually reviewed text")
    require({name: pin(BASE / name) for name in before} == before, "input changed during independent check")
    require({name: pin(BASE / name) for name in FIXED} == fixed_before, "independent dependency changed")
    require({name: pin(BASE / name) for name in review_context} == review_context, "review context changed")
    require({name: pin(HERE / name) for name in run_pins} == run_pins and pin(Path(__file__)) == checker_pin, "run/checker changed")
    return {"status": "pass_conditional_extension_arithmetic_and_preservation_only",
            "coverage": {"pairs": 14, "regions": 19, "readings": 38, "records": 12500,
                         "exact_preserved_old_readings": 34, "exact_preserved_old_records": 10840,
                         "new_originals": len(originals), "new_route_records": len(rows),
                         "new_original_bands_preserved": sum(len(s["unassigned_bands"]) for s in originals.values()),
                         "new_converted_rectangles": sum(r["native_rectangle"] is not None for r in rows),
                         "new_conditional_windows": count, "new_withheld_records": len(rows) - count,
                         "new_physical_axis_hulls": sum(len(r["physical_windows"] or []) for r in rows),
                         "new_total_conditional_windows": actual["conditional_window_counts"]["total"],
                         "unchanged_pair_objects": 12, "candidate_presence_pairs": len(actual["inventory"]["candidate_presence"]["pairs_with_both_style_candidates"])},
            "new_readings": [{"pair": r["pair"], "reader_path": r["reader_path"], "summary": r["summary"]} for r in expected],
            "allowed_changed_pair_fields": changed, "controls": controls, "controls_count": len(controls),
            "run_pins": run_pins, "checker_pin": checker_pin, "frozen_oracle_and_reference_pins": fixed_before,
            "producer_inputs_verified": len(before), "required_dependency_pins_verified": len(required),
            "checker_review_context_pins": review_context,
            "review_context_limit": "The linked approach report is navigation/review context, not read by the producer calculation and not a declared pin-map dependency. It is pinned separately here; all declared recursive dependencies remain required in the 131 producer inputs.",
            "recursive_dependency_files": len(closure), "recursive_json_nodes": json_nodes,
            "v2_substantive_payload_exactly_equals_v1": True,
            "producer_input_map_sha256": digest(before), "input_pins_unchanged_after_check": True,
            "reviewed_narrative_sha256": digest(narrative),
            "narrative_review": "The exact hashed text was read against the declared protocol and previous inventory: E3/E4 terminal absence remains target-local; out-of-box origin/bend/joins and contact questions remain pending; counts/presence are annotation scope, not curve support. This semantic review is not inferred by string/schema tests.",
            "independence": "New independent adapter and structural checks; pinned previous independent annotation validator and raw-CTM/vertex-enumeration geometry. No producer, producer adapter, classifier, mapping, screen or registration imports; no literal-reader replay or source pixel rereading in this extension check.",
            "limits": "Checks conditional arithmetic and preservation, not Hidentity/Hsupport/Hink0, confidence coverage, continuity, support unions, human acceptance, model discrepancy or historical cause. Prior 10840 decisions are exact preserved objects, not independently recalculated again in this run. Attestations remain saved self-attestations.",
            "retained_failures": [{"artifact": "V1 run01/run02", "failure": "incomplete transitive dependency coverage",
                                   "independent_closure_preflight_receipt": "6fe4a1", "missing_pins": v1_missing,
                                   "repair": "V2 changes only metadata/input closure; V1 preserved; this run checks full recursive closure."},
                                  {"artifact": "independent checker preflight", "failure_receipt": "844ac4", "diagnostic_receipt": "763e0f",
                                   "failure": "Checker expected 132 producer pins by additionally requiring linked approach report.md; actual 131 pins all matched.",
                                   "resolution": "Overstrict input-scope assumption corrected: report is navigation/review context, not a calculation input or declared map dependency. Independently pinned as checker review context. No arithmetic, source or declared dependency requirement removed."}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--save", action="store_true", help="exclusive-create small JSON receipt after a complete pass")
    args = parser.parse_args()
    try:
        require(not (args.save and args.self_test), "cannot save synthetic-only receipt")
        receipt = check_all(args.self_test)
        if args.save:
            with (HERE / "independent-check.json").open("x") as handle:
                json.dump(receipt, handle, indent=2, sort_keys=True)
                handle.write("\n")
        print(json.dumps({k: v for k, v in receipt.items() if k in
              {"status", "coverage", "controls", "controls_count", "run_pins", "checker_pin", "producer_inputs_verified",
               "required_dependency_pins_verified", "reviewed_narrative_sha256"}}, indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, AssertionError, OSError, ImportError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__, "error": str(error)}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
