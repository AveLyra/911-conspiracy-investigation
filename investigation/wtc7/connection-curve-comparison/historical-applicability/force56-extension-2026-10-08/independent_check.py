"""Independent F5/F6 extension audit; no producer or producer-helper imports.

Only two pinned earlier independent oracles are reused: native annotation
bookkeeping (without image reads) and raw-CTM / corner-enumeration arithmetic.
Frozen source labels are not reannotated. Conditional assumptions are untested.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
OLD = "historical-applicability/approach34-extension-2026-10-08/"
GEO = "historical-applicability/conditional-envelopes-2026-10-08/"
SRC = "native-footprint-pass/force56-remainder/"
NEW = "historical-applicability/force56-extension-2026-10-08/"
TARGETS = {"F5": [310, 0, 425, 88], "F6": [270, 55, 340, 88]}
SOURCES = {"F5": "Im3", "F6": "Im1"}
ORDER = [(pair, role) for pair in TARGETS for role in ("primary", "peer")]
REVIEWED_NARRATIVE_SHA = "efd529c9dc3443aaf016733e4a502e41b7aa9348700351263a56dcea48108463"
V1_SHA = "79f63ff2618de2d53ad7467a19372b1f5ba97ff36677f6ca61d13d51ff8c6d8f"
APPENDED_QUALIFICATIONS = {
    "F5": "Older Im2/Im4 peer generic same-column band references can flag an unrelated route; those original references and conditional exclusions remain unchanged.",
    "F6": "A repeated fragment ID across an unknown span does not establish continuity.",
}
AUTHORITY = {Path(p).resolve() for p in (
    "/Users/admin/docs/911/AGENTS.md", "/Users/admin/docs/911/WORKFLOW.md",
    "/Users/admin/docs/911/START-HERE.md",
    "/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md",
    "/Users/admin/.codex/skills/evidence-falsification-auditor/SKILL.md",
    "/Users/admin/.codex/skills/source-of-truth-guardian/SKILL.md")}
FIXED = {
    NEW + "PROTOCOL.md": "fc5ad00dad4358921beef1da8e470751b790c42a90e4049f77566589e28d1d95",
    NEW + "PROTOCOL-V2.md": "56b8b7769371c9bfca10682ce125e21618946027c741d6d80008b74907f0879c",
    NEW + "extend_v2.py": "66d9ad1f7aabab85c5a4f149bf347a91e7e7b9efe48b7b53e9c06ebd697c6c8d",
    NEW + "test_extend_v2.py": "085fa4349169d6064dabebc74b6770619ca81bb824af6ef45e1a7b7222ce44f0",
    NEW + "run01.json": V1_SHA,
    NEW + "run02.json": V1_SHA,
    OLD + "run-v2-01.json": "1c307f8b41d9fb0e1fbe928d4ea1cc177c6bb923ac897ec608fdfae07349a4be",
    OLD + "run-v2-02.json": "1c307f8b41d9fb0e1fbe928d4ea1cc177c6bb923ac897ec608fdfae07349a4be",
    GEO + "independent_check.py": "8f83a8b591de73aef342ecb6d01830cd012eb0593e43731236ba73f553ad69f0",
    SRC + "independent_check.py": "326cd663a0e5bf8f9eefafb45d1421fa5f81056891a26228ad49168fc28665b0",
    SRC + "independent-check.json": "449bdc39b7eaea29cc67fa81a9fcaa0688928dc79f2743e4f33546f873729076",
    "pypdf-representation01.json": "1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(), parse_float=Fraction)


def pin(path):
    raw = Path(path).read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def exact(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def name(path):
    resolved = Path(path).resolve()
    if resolved not in AUTHORITY:
        resolved.relative_to(BASE)
    return os.path.relpath(resolved, BASE)


def pin_schema(value):
    require(type(value) is dict and set(value) == {"bytes", "sha256"}, "pin schema")
    require(type(value["bytes"]) is int and value["bytes"] >= 0, "pin byte type")
    sha = value["sha256"]
    require(type(sha) is str and len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), "pin hash schema")


def merge(target, key, value):
    pin_schema(value)
    require(key not in target or exact(target[key], value), "conflicting normalized pin: " + key)
    target[key] = value


def normalized_map(mapping, base=BASE):
    require(type(mapping) is dict, "pin map schema")
    result = {}
    for key, value in mapping.items():
        require(type(key) is str and key, "pin path schema")
        merge(result, name(base / key), value)
    return result


def closure(roots, read=load, get=pin):
    """JSON dependency maps in this graph use each owning file's directory."""
    result, pending, seen = {}, [], set()
    def add(path, wanted=None):
        key = name(path)
        found = get(BASE / key)
        pin_schema(found)
        require(wanted is None or exact(found, wanted), "changed transitive pin: " + key)
        fresh = key not in result
        merge(result, key, found)
        if fresh and key.endswith(".json"):
            pending.append(key)
    for path in roots:
        add(path)
    while pending:
        key = pending.pop(0)
        if key in seen:
            continue
        seen.add(key)
        file = BASE / key
        data = read(file)
        require(type(data) is dict, "dependency JSON object")
        if "inputs_after" in data:
            require(exact(data["inputs"], data["inputs_after"]), "dependency before/after mismatch")
        for field in ("inputs", "inputs_after", "dependencies", "input_pins"):
            if field in data:
                require(type(data[field]) is dict, "dependency map type")
                for child, wanted in data[field].items():
                    pin_schema(wanted)
                    add(file.parent / child, wanted)
        if "script_pin" in data:
            require(file.name.startswith(("reader-", "comparison-")), "unknown script pin base")
            add(file.with_suffix(".py") if file.name.startswith("reader-") else file.parent / "compare.py", data["script_pin"])
        if "test_pin" in data:
            require(file.name.startswith("comparison-"), "unknown test pin base")
            add(file.parent / "test_compare.py", data["test_pin"])
    return result, sorted(seen)


def import_oracle(key, label):
    require(pin(BASE / key)["sha256"] == FIXED[key], "oracle frozen hash")
    spec = importlib.util.spec_from_file_location(label, BASE / key)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def adapted(original, pair, role, annotation, attest=True):
    annotation.validate_annotation(original, pair, role, attest=attest)
    saved = copy.deepcopy(original)
    result = copy.deepcopy(original)
    for rows in result["routes"].values():
        for row in rows:
            require(not set(row) & {"column", "core_rows", "fringe_rows", "fragments", "band_refs"}, "ambiguous membership/row alias")
            require(type(row["fragment_membership"]) is list, "membership must be list")
            row["fragments"] = row.pop("fragment_membership")
    reversed_copy = copy.deepcopy(result)
    for rows in reversed_copy["routes"].values():
        for row in rows:
            row["fragment_membership"] = row.pop("fragments")
    require(exact(reversed_copy, saved) and exact(original, saved), "copy-only adaptation changed original fields")
    return result


def region(pair):
    return {"source": SOURCES[pair], "target_box": TARGETS[pair], "readers": [
        {"path": SRC + f"reader-{pair}-{role}.json", "route_records": 2 * (TARGETS[pair][2] - TARGETS[pair][0]),
         "target_source_field": "target_box", "human_accepted_field": False, "physical_support_field": None}
        for role in ("primary", "peer")]}


def expected_readings(originals, annotation, geometry):
    representation = load(BASE / "pypdf-representation01.json")
    invocations = {i["name"]: i for i in representation["image_invocations"]}
    require(len(invocations) == len(representation["image_invocations"]) == 12, "twelve distinct image invocations")
    output = []
    for pair, role in ORDER:
        path = SRC + f"reader-{pair}-{role}.json"
        invocation = invocations[SOURCES[pair]]
        require(invocation["native_dimensions"] == [741, 88], "source-specific dimensions")
        rows = geometry.serialized(geometry.expected_rows(adapted(originals[path], pair, role, annotation), region(pair), "F", invocation))
        output.append({"pair": pair, "source": SOURCES[pair], "reader_path": path, "rows": rows,
            "summary": {"records": len(rows), "conditional_windows": sum(r["conditional_window"] for r in rows),
                        "reasons_nonexclusive": dict(Counter(v for row in rows for v in row["reasons"]))}})
    return output


def candidates(pairs, originals):
    yes, no = [], []
    for pair in pairs:
        seen = set()
        for target in pair["completed_footprints"]:
            require(len(target["readers"]) == 2, "original role count")
            for role, reader in enumerate(target["readers"]):
                source = originals[reader["path"]]
                routes = source.get("routes")
                if routes is None:
                    routes = {r: [v for v in source["observations"] if v["route"] == r] for r in ("solid", "dash")}
                require(set(routes) == {"solid", "dash"}, "candidate route labels")
                for route, rows in routes.items():
                    if any(row["status"] == "identified_local_fragment" and row["core_rows" if "column" in row else "core"] for row in rows):
                        seen.add((role, route))
        (yes if seen == {(i, r) for i in (0, 1) for r in ("solid", "dash")} else no).append(pair["pair"])
    return yes, no


def check_inventory(found, old, originals):
    require(set(found) == set(old), "inventory schema")
    for key in ("acceptance", "preserved_corrections"):
        require(exact(found[key], old[key]), "inventory protected field: " + key)
    require([p["pair"] for p in found["pairs"]] == [p["pair"] for p in old["pairs"]], "pair order")
    mutable = {"completed_footprints", "additional_batches", "remaining_inventory", "identity_and_topology_limits", "next_evidence_action"}
    changed = []
    for current, previous in zip(found["pairs"], old["pairs"]):
        pair = previous["pair"]
        if pair not in TARGETS:
            require(exact(current, previous), "unaffected pair modified: " + pair)
            continue
        require(set(current) == set(previous) | {"additional_batches"}, "changed pair schema")
        require(exact({k: v for k, v in current.items() if k not in mutable},
                      {k: v for k, v in previous.items() if k not in mutable}), "non-whitelisted pair field")
        require(exact(current["completed_footprints"], previous["completed_footprints"] + [region(pair)]), "old region changed or new region malformed")
        require(exact(current["additional_batches"], previous.get("additional_batches", []) + [
            {"report": SRC + "report.md", "verification": SRC + "independent-check.json"}]), "additional batch references")
        for field in mutable - {"completed_footprints", "additional_batches"}:
            require(type(current[field]) is str and current[field].strip() and current[field] != previous[field], "missing residual narrative update")
        changed.extend(pair + "/" + k for k in sorted(mutable))
    targets = [r for p in found["pairs"] for r in p["completed_footprints"]]
    readers = [r for target in targets for r in target["readers"]]
    expected_counts = {"pairs": 14, "completed_regions": 21, "original_readings": 42, "original_route_records": 13240}
    actual_counts = {"pairs": len(found["pairs"]), "completed_regions": len(targets), "original_readings": len(readers),
                     "original_route_records": sum(r["route_records"] for r in readers)}
    require(exact(found["counts"], expected_counts) and exact(actual_counts, expected_counts), "inventory counts")
    require(len({r["path"] for r in readers}) == 42, "duplicate reading path")
    presence = found["candidate_presence"]
    require(set(presence) == set(old["candidate_presence"]) and presence["criterion"] == old["candidate_presence"]["criterion"], "candidate criterion/schema")
    yes, no = candidates(found["pairs"], originals)
    require(presence["pairs_with_both_style_candidates"] == yes and presence["pairs_without_both_style_candidates"] == no, "candidate counts")
    require(type(presence["limits"]) is str and presence["limits"], "presence limitations")
    require(len(found["claims"]) == 3 and all(set(c) == {"claim", "type", "strength", "support", "falsifier"}
            and all(type(v) is str and v.strip() for v in c.values()) for c in found["claims"]), "claim schema")
    return changed


def check_payload(result, old, originals, expected, all_sources):
    require(exact(result["readings"][:38], old["readings"]), "38 previous readings changed")
    require(exact(result["readings"][38:], expected), "new decision/rectangle/hull or summary mismatch")
    require(exact(result["new_source_originals"], originals), "new original or band changed")
    require(exact(result["prior_source_originals"], old["new_source_originals"]), "four earlier originals changed")
    for key in ("axis_boxes", "assumptions", "human_accepted", "common_support", "quantile_targets", "model_discrepancies", "shared_axis_parameters"):
        require(exact(result[key], old[key]), "protected bundle field: " + key)
    require(type(result["records"]) is int and result["records"] == 13240 and sum(len(r["rows"]) for r in result["readings"]) == 13240, "bundle record count")
    previous = sum(r["summary"]["conditional_windows"] for r in old["readings"])
    added = sum(r["summary"]["conditional_windows"] for r in expected)
    require(exact(result["conditional_window_counts"], {"prior": previous, "new": added, "total": previous + added}), "conditional counts")
    require(type(result["limits"]) is str and bool(result["limits"]), "bundle limitations")
    return check_inventory(result["inventory"], old["inventory"], all_sources)


def check_v2(result, v1):
    require(type(result["version"]) is int and result["version"] == 2 and
            result["status"] == "conditional_force56_extension_v2_not_accepted_measurement", "V2 status/version")
    copied = copy.deepcopy(v1)
    for pair in copied["inventory"]["pairs"]:
        if pair["pair"] in APPENDED_QUALIFICATIONS:
            pair["identity_and_topology_limits"] += " " + APPENDED_QUALIFICATIONS[pair["pair"]]
    metadata = {"version", "status", "inputs", "inputs_after", "correction_provenance"}
    require(exact({k: v for k, v in result.items() if k not in metadata},
                  {k: v for k, v in copied.items() if k not in metadata}), "V2 changed more than two narrative sentences")
    provenance = result["correction_provenance"]
    require(set(provenance) == {"prior_outputs_preserved", "reason", "appended_qualifications", "all_numerical_and_original_payload_unchanged"}, "correction provenance schema")
    require(provenance["prior_outputs_preserved"] == [NEW + "run01.json", NEW + "run02.json"] and
            exact(provenance["appended_qualifications"], APPENDED_QUALIFICATIONS) and
            provenance["all_numerical_and_original_payload_unchanged"] is True, "correction provenance payload")
    require(provenance["reason"] == "Version-1 current-inventory prose omitted older annotation-reference and continuity qualifications.", "correction reason")


def rejected(label, operation, controls):
    try:
        operation()
    except (ValueError, KeyError, TypeError, AssertionError):
        controls.append(label)
    else:
        raise ValueError("deliberate corruption admitted: " + label)


def synthetic_controls(annotation, geometry):
    controls = geometry.manual_checks()
    root, leaf = BASE / NEW / "synthetic/root.json", BASE / NEW / "synthetic/leaf.json"
    pins = {root: {"bytes": 100, "sha256": "0" * 64}, leaf: {"bytes": 200, "sha256": "1" * 64}}
    docs = {root: {"inputs": {"../synthetic/leaf.json": pins[leaf]}}, leaf: {"inputs": {"root.json": pins[root]}}}
    read, get = lambda p: docs[p], lambda p: pins[p]
    graph, nodes = closure([root], read, get)
    require(exact(graph, {name(p): v for p, v in pins.items()}) and len(nodes) == 2, "normalized cyclic closure")
    controls.append("recursive_graph_normalizes_and_terminates_cycle")
    docs[root]["inputs"]["leaf.json"] = {"bytes": 300, "sha256": "2" * 64}
    rejected("conflicting_normalized_dependency", lambda: closure([root], read, get), controls)
    del docs[root]["inputs"]["leaf.json"]
    docs[root]["inputs_after"] = {}
    rejected("dependency_before_after_changed", lambda: closure([root], read, get), controls)
    del docs[root]["inputs_after"]
    pins[leaf] = {"bytes": 201, "sha256": "1" * 64}
    rejected("changed_descendant_bytes", lambda: closure([root], read, get), controls)
    rejected("boolean_pin_size", lambda: pin_schema({"bytes": True, "sha256": "0" * 64}), controls)
    require(len(AUTHORITY) == 6 and all(name(p) for p in AUTHORITY), "six authority paths")
    controls.append("six_exact_authority_paths_allowed")
    rejected("arbitrary_outside_path", lambda: name(Path("/Users/admin/docs/911/not-approved-input.md")), controls)
    def row(x, y=None):
        cells = [] if y is None else [y]
        fid = None if y is None else "invented-fragment"
        return {"x": x, "core": cells, "fringe": [], "fragment_id": fid,
                "fragment_membership": [] if y is None else [{"fragment_id": fid, "core": cells, "fringe": []}],
                "status": "no_attributable_cells" if y is None else "identified_local_fragment",
                "reason": "synthetic, not source ink", "boundary_flags": [], "unassigned_band_refs": []}
    sample = {"pair": "F5", "region_id": "F5-Im3", "source": "Im3.jpg", "reader": "force56_peer",
              "target_box": TARGETS["F5"], "context_box": [308, 0, 427, 88], "human_accepted": False,
              "physical_support": None, "routes": {r: [row(x) for x in range(310, 425)] for r in ("solid", "dash")},
              "unassigned_bands": []}
    for x in range(350, 355):
        sample["routes"]["solid"][x - 310] = row(x, 30)
    original = copy.deepcopy(sample)
    adapted_sample = adapted(sample, "F5", "peer", annotation, attest=False)
    require(exact(sample, original) and adapted_sample["reader"] == "force56_peer", "copy/serialized role")
    controls.append("copy_only_alias_preserves_force56_peer")
    rejected("peer_alias_cannot_be_primary", lambda: adapted(sample, "F5", "primary", annotation, attest=False), controls)
    for label, mutate in (
        ("unknown_role", lambda s: s.update(reader="unknown")),
        ("wrong_source", lambda s: s.update(source="Im1.jpg")),
        ("wrong_target", lambda s: s.update(target_box=[310, 0, 425, 89])),
        ("ambiguous_membership_alias", lambda s: s["routes"]["solid"][40].update(fragments=[])),
        ("boolean_cell", lambda s: s["routes"]["solid"][40].update(core=[True])),
        ("member_union", lambda s: s["routes"]["solid"][40]["fragment_membership"][0].update(core=[31])),
        ("coverage_loss", lambda s: s["routes"]["solid"].pop()),
    ):
        bad = copy.deepcopy(sample)
        mutate(bad)
        rejected(label, lambda: adapted(bad, "F5", "peer", annotation, attest=False), controls)
    invocation = {"native_dimensions": [741, 88], "ctm": [Fraction(741, 3), 0, 0, Fraction(88, 3), 160, 550]}
    decisions = geometry.expected_rows(adapted_sample, region("F5"), "F", invocation)
    accepted = [r["column"] for r in decisions if r["conditional_window"]]
    require(accepted == [351, 352, 353], "one-column noniterative guard")
    controls.append("immediate_neighbor_guard_not_recursively_shrunk_or_bridged")
    banded = copy.deepcopy(sample)
    band = row(352, 40)
    band.update(band_id="synthetic-band", candidate_routes=["solid"])
    banded["unassigned_bands"].append(band)
    banded["routes"]["solid"][42]["unassigned_band_refs"] = ["synthetic-band"]
    band_rows = geometry.expected_rows(adapted(banded, "F5", "peer", annotation, attest=False), region("F5"), "F", invocation)
    require(not any(r["conditional_window"] for r in band_rows) and "unassigned_band_reference" in band_rows[42]["reasons"], "band and neighbor exclusion")
    controls.append("route_band_and_neighbor_exclusion")
    require(not exact(False, 0), "type-sensitive equality")
    controls.append("json_false_not_numeric_zero")
    return controls


def check_all(self_test=False):
    fixed = {key: pin(BASE / key) for key in FIXED}
    require(all(fixed[key]["sha256"] == wanted for key, wanted in FIXED.items()), "frozen reference changed")
    annotation = import_oracle(SRC + "independent_check.py", "source_annotation_independent")
    geometry = import_oracle(GEO + "independent_check.py", "conditional_arithmetic_independent")
    controls = synthetic_controls(annotation, geometry)
    if self_test:
        return {"status": "synthetic_controls_pass", "controls": controls, "controls_count": len(controls)}
    checker_pin = pin(Path(__file__))
    require((BASE / OLD / "run-v2-01.json").read_bytes() == (BASE / OLD / "run-v2-02.json").read_bytes(), "prior repeated outputs differ")
    old = load(BASE / OLD / "run-v2-01.json")
    require(exact(old["inputs"], old["inputs_after"]), "prior input map before/after differs")
    prior_inputs = normalized_map(old["inputs"])
    require(len(prior_inputs) == 131 and exact(prior_inputs, old["inputs"]), "prior flattened map schema")
    require(exact({key: pin(BASE / key) for key in prior_inputs}, prior_inputs), "prior flattened input changed")
    require(len(old["readings"]) == 38 and old["records"] == 12500 and len(old["new_source_originals"]) == 4, "prior scope")
    originals = {}
    for pair, role in ORDER:
        key = SRC + f"reader-{pair}-{role}.json"
        require(pin(BASE / key)["sha256"] == annotation.FROZEN_READERS[Path(key).name], "frozen original changed")
        originals[key] = load(BASE / key)
        annotation.validate_annotation(originals[key], pair, role)
    require(sum(len(s["unassigned_bands"]) for s in originals.values()) == 50, "original band total")
    roots = [BASE / key for key in originals]
    roots += [BASE / SRC / key for key in ("independent-check.json", "context01.json", "context02.json")]
    roots += [BASE / SRC / f"comparison-{pair}-{index:02}.json" for pair in TARGETS for index in (1, 2)]
    required_closure, json_nodes = closure(roots)
    required = dict(prior_inputs)
    for key, value in required_closure.items():
        merge(required, key, value)
    # Direct execution roots are independently declared by the protocol and
    # coordinator before historical runs, not inferred from output keys.
    direct = [OLD + "run-v2-01.json", OLD + "run-v2-02.json", OLD + "extend.py",
              GEO + "calculate.py", SRC + "compare.py", SRC + "independent-check.json",
              NEW + "PROTOCOL.md", NEW + "extend.py", NEW + "test_extend.py"] + list(originals)
    for key in direct:
        merge(required, key, pin(BASE / key))
    outside = {Path(BASE / key).resolve() for key in required if not Path(BASE / key).resolve().is_relative_to(BASE)}
    require(outside == AUTHORITY, "outside authority-context roster differs")
    require((HERE / "run01.json").read_bytes() == (HERE / "run02.json").read_bytes(), "V1 repeat outputs differ")
    v1 = load(HERE / "run01.json")
    require(exact(v1["inputs"], required) and exact(v1["inputs_after"], required), "V1 exact independent required union")
    for filename in ("run01.json", "run02.json", "PROTOCOL-V2.md", "extend_v2.py", "test_extend_v2.py"):
        merge(required, NEW + filename, pin(HERE / filename))
    run_pins = {key: pin(HERE / key) for key in ("run01.json", "run02.json", "run-v2-01.json", "run-v2-02.json")}
    require((HERE / "run-v2-01.json").read_bytes() == (HERE / "run-v2-02.json").read_bytes(), "new V2 repeated outputs differ")
    result = load(HERE / "run-v2-01.json")
    require(set(result) == {"status", "version", "inputs", "inputs_after", "new_dependency_json_nodes", "prior_conditional_result",
            "inventory", "records", "readings", "new_source_originals", "prior_source_originals", "axis_boxes", "assumptions",
            "conditional_window_counts", "human_accepted", "common_support", "quantile_targets", "model_discrepancies",
            "shared_axis_parameters", "limits", "correction_provenance"}, "new bundle schema")
    check_v2(result, v1)
    for label, mutate in (
        ("V2_numerical_payload_changed", lambda b: b["readings"][-1]["summary"].update(records=0)),
        ("V2_prior_qualification_omitted", lambda b: next(p for p in b["inventory"]["pairs"] if p["pair"] == "F5").update(identity_and_topology_limits="missing")),
        ("V2_boolean_version", lambda b: b.update(version=True)),
    ):
        bad = copy.deepcopy(result)
        mutate(bad)
        rejected(label, lambda: check_v2(bad, v1), controls)
    require(result["prior_conditional_result"] == OLD + "run-v2-01.json", "prior bundle reference")
    require(exact(result["inputs"], result["inputs_after"]), "new input map before/after changed")
    declared = normalized_map(result["inputs"])
    require(exact(declared, result["inputs"]) and exact(declared, required), "complete required input union omitted, changed, or expanded")
    require(exact({key: pin(BASE / key) for key in declared}, declared), "declared current input bytes changed")
    require(result["new_dependency_json_nodes"] == json_nodes, "recursive JSON node roster")
    expected = expected_readings(originals, annotation, geometry)
    all_sources = dict(originals)
    for pair in old["inventory"]["pairs"]:
        for target in pair["completed_footprints"]:
            for reader in target["readers"]:
                all_sources[reader["path"]] = load(BASE / reader["path"])
    changes = check_payload(result, old, originals, expected, all_sources)
    for label, mutate in (
        ("prior_decision_changed", lambda b: b["readings"][0]["rows"][0]["reasons"].append("invented")),
        ("prior_false_changed_to_zero", lambda b: b["readings"][0]["rows"][0].update(curve_support_established=0)),
        ("new_exclusion_reason_removed", lambda b: next(r for r in b["readings"][38]["rows"] if r["reasons"])["reasons"].pop()),
        ("new_native_rectangle_changed", lambda b: next(r for r in b["readings"][38]["rows"] if r["native_rectangle"])["native_rectangle"].__setitem__(1, 0)),
        ("new_pdf_rectangle_changed", lambda b: next(r for r in b["readings"][38]["rows"] if r["pdf_rectangle"])["pdf_rectangle"].__setitem__(1, "0")),
        ("new_hull_changed", lambda b: next(r for r in b["readings"][38]["rows"] if r["conditional_window"])["physical_windows"][0]["ordinate"].__setitem__(0, "0")),
        ("new_reader_role_rewritten", lambda b: b["new_source_originals"][SRC + "reader-F5-peer.json"].update(reader="peer")),
        ("new_band_removed", lambda b: b["new_source_originals"][SRC + "reader-F5-primary.json"]["unassigned_bands"].pop()),
        ("prior_embedded_original_changed", lambda b: next(iter(b["prior_source_originals"].values())).update(reader="invented")),
        ("unaffected_pair_changed", lambda b: b["inventory"]["pairs"][0].update(bounds_status="invented")),
        ("protected_F5_field_changed", lambda b: next(p for p in b["inventory"]["pairs"] if p["pair"] == "F5").update(bounds_status="invented")),
        ("old_F5_region_overwritten", lambda b: next(p for p in b["inventory"]["pairs"] if p["pair"] == "F5")["completed_footprints"][0].update(target_box=TARGETS["F5"])),
        ("candidate_presence_dropped", lambda b: b["inventory"]["candidate_presence"]["pairs_with_both_style_candidates"].pop()),
        ("human_acceptance_promoted", lambda b: b.update(human_accepted=True)),
        ("common_support_invented", lambda b: b.update(common_support=[])),
    ):
        bad = copy.deepcopy(result)
        mutate(bad)
        rejected(label, lambda: check_payload(bad, old, originals, expected, all_sources), controls)
    # Exercise omission of each required transitive pin, not a selected sample.
    for key in required:
        bad = dict(declared)
        del bad[key]
        rejected("required_pin_omission:" + key, lambda: require(exact(bad, required), "required pin omitted"), controls)
    narrative = {"pair_residuals": [{k: p[k] for k in ("pair", "remaining_inventory", "identity_and_topology_limits", "next_evidence_action")}
                                   for p in result["inventory"]["pairs"] if p["pair"] in TARGETS],
                 "claims": result["inventory"]["claims"], "presence_limits": result["inventory"]["candidate_presence"]["limits"], "bundle_limits": result["limits"]}
    require(digest(narrative) == REVIEWED_NARRATIVE_SHA, "narrative not yet semantically reviewed or changed")
    require(exact({key: pin(BASE / key) for key in required}, required), "input changed during check")
    require(exact({key: pin(BASE / key) for key in FIXED}, fixed), "frozen dependency changed during check")
    require(exact({key: pin(HERE / key) for key in run_pins}, run_pins) and exact(pin(Path(__file__)), checker_pin), "outputs/checker changed during check")
    rows = [row for reading in expected for row in reading["rows"]]
    count = sum(row["conditional_window"] for row in rows)
    return {"status": "pass_conditional_arithmetic_preservation_and_dependency_closure_only",
        "coverage": {"pairs": 14, "regions": 21, "readings": 42, "records": 13240,
            "exact_preserved_prior_readings": 38, "exact_preserved_prior_records": 12500,
            "exact_preserved_prior_embedded_originals": 4, "new_originals": 4,
            "new_records_checked": len(rows), "new_bands_preserved_and_checked": 50,
            "new_converted_rectangles": sum(r["native_rectangle"] is not None for r in rows),
            "new_conditional_windows": count, "new_excluded_records": len(rows) - count,
            "new_axis_hulls_checked": sum(len(r["physical_windows"] or []) for r in rows),
            "total_conditional_windows": result["conditional_window_counts"]["total"], "unchanged_pair_objects": 12},
        "readings": [{k: r[k] for k in ("pair", "reader_path", "summary")} for r in expected],
        "allowed_changed_inventory_fields": changes, "new_recursive_json_nodes": json_nodes,
        "required_recursive_pin_count": len(required_closure), "required_total_pin_count": len(required),
        "outside_authority_context_count": len(outside), "required_input_map_sha256": digest(required),
        "run_pins": run_pins, "checker_pin": checker_pin, "fixed_reference_pins": fixed,
        "controls": controls, "controls_count": len(controls), "input_pins_unchanged_after_check": True,
        "v2_changes_only_two_qualifications_and_declared_metadata": True,
        "reviewed_narrative_sha256": digest(narrative),
        "narrative_review": "Exact residual and claim text was read against the frozen protocol; completed boxes remain local, bands and clipping remain alternatives, no empty solid F6 route is physical zero, and seams/outside inventory remain unresolved.",
        "independence": "Independent copy-only adapter, preservation/closure checks, pinned independent native annotation validator and independent raw-CTM corner/axis-vertex arithmetic. No new producer, producer adapter, classifier or coordinate mapping imports; no source pixel reads or reader-build execution. Output schema and protocol were known, not blind.",
        "limits": "Conditional arithmetic, provenance and bookkeeping only. Does not establish Hidentity/Hsupport/Hink0, pre-raster enclosure, semantic attribution, continuity, shared support, confidence coverage, human acceptance, model fidelity or historical cause. The 12500 prior decisions are preserved exactly, not recalculated in this check. Source-reading attestations are not independently witnessed perception.",
        "retained_preflight": {"receipt": "5e0a5f", "artifact": "V1 independent checker preflight", "result": "All arithmetic, preservation and 168-pin closure gates passed before intentional pending narrative-review hash stopped the unsaved check. V1 inventory caveats were separately found incomplete; V2 restores them without numerical changes."}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    try:
        require(not (args.self_test and args.save), "only complete checks may be saved")
        result = check_all(args.self_test)
        if args.save:
            with (HERE / "independent-check.json").open("x") as file:
                json.dump(result, file, indent=2, sort_keys=True, allow_nan=False)
                file.write("\n")
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, TypeError, KeyError, AssertionError, OSError) as error:
        print(json.dumps({"status": "fail", "error_type": type(error).__name__, "error": str(error)}, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
