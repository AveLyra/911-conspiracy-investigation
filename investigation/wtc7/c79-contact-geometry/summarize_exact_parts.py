#!/usr/bin/env python3
"""Post-result descriptive node/part dependencies from frozen numeric derivatives.

No raw reader, geometry recomputation, damage join or physical member naming.
The output is create-only. Synthetic controls precede historical-array loading.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import time

import numpy as np

HERE = Path(__file__).resolve().parent
PINS = {
    "PROTOCOL.md": "b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea",
    "EXACT-ARITHMETIC-ADDENDUM.md": "b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89",
    "exact-proximity80.json": "25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324",
    "exact-proximity80.npz": "79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628",
    "stage-root01.json": "deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963",
    "stage-root01.npz": "2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf",
}
CLASSES = (0, 2, 3)
KINDS = {0: "shell", 1: "beam", 2: "discrete", 3: "solid"}
SOURCES = {"discrete_mass.k.gz": 119, "elem_thick_to-renum.k.gz": 120,
           "wtc7_global_8a_no-conn-matl.k.gz": 121}


def need(value, code):
    if not value:
        raise ValueError(code)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def pin(path, expected):
    actual = digest(path)
    need(actual == expected, "pin_mismatch")
    return actual


def source_id(value):
    if isinstance(value, str):
        need(value in SOURCES, "unrecognized_source_alias")
        return SOURCES[value]
    need(isinstance(value, int) and value in (119, 120, 121), "unrecognized_source_id")
    return value


def part_reference(pid, original):
    if original is None:
        return {"effective_pid": pid, "registry_entry_present": False,
                "part_definition_status": "not_available_in_frozen_registry",
                "section_definition_status": "unresolved", "material_definition_status": "unresolved"}
    need(original["pid"] == pid, "part_registry_pid_mismatch")
    part = original.get("part")
    if part is None:
        return {"effective_pid": pid, "registry_entry_present": True,
                "part_definition_status": "absent_per_frozen_registry",
                "section_definition_status": "unresolved", "material_definition_status": "unresolved"}
    need(part["pid"] == pid, "part_definition_pid_mismatch")
    keyword = original.get("material_keyword")
    need(keyword is None or (isinstance(keyword, str) and re.fullmatch(r"\*?MAT_[A-Z0-9_]+", keyword)), "unrecognized_material_keyword")
    defined = original.get("section_defined")
    need(isinstance(defined, bool), "section_status_schema")
    shell = original.get("section_shell")
    shell_locator = None
    if shell is not None:
        shell_locator = {"source_id": source_id(shell["source"]),
                         "keyword_line": int(shell["keyword_line"]),
                         "card_lines": [int(c["line"]) for c in shell["cards"]]}
        need(defined, "shell_locator_but_absent_section")
    return {"effective_pid": pid, "registry_entry_present": True,
            "part_definition_status": "present_per_frozen_registry",
            "part_source_id": source_id(part["source"]), "part_card_line": int(part["line"]),
            "original_pid": int(part["original_pid"]),
            "effective_sid": int(part["section_id"]), "original_sid": int(part["original_section_id"]),
            "effective_mid": int(part["material_id"]), "original_mid": int(part["original_material_id"]),
            "section_definition_status": "present_per_frozen_registry" if defined else "absent_per_frozen_registry",
            "shell_section_locator": shell_locator,
            "material_definition_status": "present_per_frozen_registry" if keyword is not None else "absent_per_frozen_registry",
            "material_keyword": keyword,
            "material_definition_source_and_line": None,
            "locator_limit": "The frozen reference schema does not supply material-definition source/line; a null shell locator does not negate a true section-defined flag."}


def summarize(pairs, master_identity, incidence, node_ids, node_lines, thickness, references, settings):
    need(pairs.ndim == 2 and pairs.shape[1] == 6, "pair_schema")
    need(len(set(map(tuple, pairs[:, :3].tolist()))) == len(pairs), "duplicate_setting_master_node")
    need(master_identity.ndim == 2 and master_identity.shape[1] == 3, "master_schema")
    need(np.all((pairs[:, 0] >= 0) & (pairs[:, 0] < len(settings))), "setting_index")
    need(np.all((pairs[:, 1] >= 0) & (pairs[:, 1] < len(master_identity))), "master_index")
    need(np.all(np.isin(pairs[:, 3], (0, 1, 2, 3))), "class_code")
    need(np.all(np.isin(master_identity[:, 0], (1, 2))), "cid_code")
    need(len(node_ids) == len(set(map(int, node_ids))), "duplicate_node_id")
    index = {int(n): i for i, n in enumerate(node_ids)}
    need(all(int(n) in index for n in pairs[:, 2]), "missing_pair_node")
    need(incidence.ndim == 2 and incidence.shape[1] == 4, "incidence_shape")
    need(len(set(map(tuple, incidence[:, :3].tolist()))) == len(incidence), "duplicate_typed_incidence")
    need(np.all(incidence[:, 3] > 0), "nonpositive_incidence_count")
    need(all(int(x) in KINDS for x in incidence[:, 1]), "unrecognized_element_family")
    inc = defaultdict(list)
    for nid, kind, pid, count in incidence:
        inc[int(nid)].append((int(kind), int(pid), int(count)))
    reference_map = {}
    for ref in references:
        need(ref["pid"] not in reference_map, "duplicate_part_reference")
        reference_map[ref["pid"]] = ref
    chosen = pairs[np.isin(pairs[:, 3], CLASSES)]
    chosen_nodes = set(map(int, chosen[:, 2]))
    typed_universe = sorted({(kind, pid) for nid in chosen_nodes for kind, pid, count in inc[nid]})
    pids = sorted({pid for kind, pid in typed_universe})
    registry = [part_reference(pid, reference_map.get(pid)) for pid in pids]
    registry_map = {r["effective_pid"]: r for r in registry}
    nodes = []
    for nid in sorted(chosen_nodes):
        i = index[nid]
        values = list(map(float, thickness[i]))
        unknown = all(math.isnan(x) for x in values)
        need(unknown or all(math.isfinite(x) and x >= 0 for x in values), "node_thickness_status")
        need(unknown or values[0] <= values[1], "node_thickness_range")
        families = inc[nid]
        nodes.append({"node_id": nid, "node_source_id": source_id(int(node_lines[i, 0])),
                      "node_source_line": int(node_lines[i, 1]),
                      "has_shell_incidence": any(k == 0 for k, p, c in families),
                      "supplied_shell_corner_thickness_unknown": unknown,
                      "supplied_shell_corner_thickness_range": None if unknown else values,
                      "typed_part_incidence": [{"kind_code": k, "family": KINDS[k], "effective_pid": p,
                                                "node_element_incidence_count": c} for k, p, c in sorted(families)]})
    groups, group_nodes = [], {}
    cids = master_identity[pairs[:, 1], 0]
    for si in range(len(settings)):
        for cid in (1, 2):
            for cls in CLASSES:
                rr = pairs[(pairs[:, 0] == si) & (cids == cid) & (pairs[:, 3] == cls)]
                ns = set(map(int, rr[:, 2])); group_nodes[(si, cid, cls)] = ns
                multiplicity = Counter(map(int, rr[:, 2]))
                typed = []
                for kind, pid in typed_universe:
                    members = sorted(n for n in ns if any(k == kind and p == pid for k, p, c in inc[n]))
                    inc_sum = sum(c for n in members for k, p, c in inc[n] if k == kind and p == pid)
                    typed.append({"kind_code": kind, "family": KINDS[kind], "effective_pid": pid,
                                  "node_ids": members, "unique_node_count": len(members),
                                  "node_master_relation_count": sum(multiplicity[n] for n in members),
                                  "node_element_incidence_sum_not_unique_elements": inc_sum,
                                  "part_reference_pid": pid})
                groups.append({"setting_index": si, "setting_value": float(settings[si]), "cid": cid, "class": cls,
                               "node_master_relation_count": len(rr), "unique_slave_node_ids": sorted(ns),
                               "unique_slave_node_count": len(ns), "distinct_master_records": len(set(map(int, rr[:, 1]))),
                               "relations": rr.tolist(), "typed_parts_in_complete_selected_universe": typed,
                               "per_typed_part_node_count_sum_not_unique_nodes": sum(t["unique_node_count"] for t in typed),
                               "nodes_with_multiple_typed_part_incidence": sorted(n for n in ns if len(inc[n]) > 1)})
    reconciliations = []
    for si in range(len(settings)):
        groups_here = {(cid, cls): group_nodes[(si, cid, cls)] for cid in (1, 2) for cls in CLASSES}
        by_cid = {cid: set().union(*(groups_here[(cid, cls)] for cls in CLASSES)) for cid in (1, 2)}
        by_class = {cls: set().union(*(groups_here[(cid, cls)] for cid in (1, 2))) for cls in CLASSES}
        union = by_cid[1] | by_cid[2]
        selected_rows = pairs[(pairs[:, 0] == si) & np.isin(pairs[:, 3], CLASSES)]
        outside_rows = pairs[(pairs[:, 0] == si) & (pairs[:, 3] == 1)]
        overlaps = []
        for (cid1, cls1), (cid2, cls2) in itertools.combinations(groups_here, 2):
            shared = sorted(groups_here[(cid1, cls1)] & groups_here[(cid2, cls2)])
            overlaps.append({"group_a": [cid1, cls1], "group_b": [cid2, cls2], "node_ids": shared, "count": len(shared)})
        membership = []
        for nid in sorted(union):
            combos = [[cid, cls] for (cid, cls), ns in groups_here.items() if nid in ns]
            outside = outside_rows[outside_rows[:, 2] == nid]
            membership.append({"node_id": nid, "selected_cid_class_memberships": combos,
                               "also_outside_class1_relations": [[int(master_identity[r[1], 0]), int(r[1])] for r in outside]})
        reconciliations.append({"setting_index": si, "selected_classes": list(CLASSES),
                                "unique_node_ids_across_selected_cids_classes": sorted(union), "unique_node_count": len(union),
                                "selected_node_master_relation_count": len(selected_rows),
                                "group_unique_node_count_sum_not_unique_total": sum(map(len, groups_here.values())),
                                "cid_unique_node_ids": {str(cid): sorted(ns) for cid, ns in by_cid.items()},
                                "class_unique_node_ids": {str(cls): sorted(ns) for cls, ns in by_class.items()},
                                "shared_cid_node_ids": sorted(by_cid[1] & by_cid[2]),
                                "pairwise_cid_class_overlaps_including_zeros": overlaps,
                                "selected_nodes_with_any_outside_class1_relation": sorted(union & set(map(int, outside_rows[:, 2]))),
                                "node_membership": membership})
    class3_nodes = set(map(int, pairs[pairs[:, 3] == 3, 2]))
    material_missing = []
    for kind, pid in typed_universe:
        ref = registry_map[pid]
        if ref["material_definition_status"] == "absent_per_frozen_registry":
            ns = sorted(n for n in chosen_nodes if any(k == kind and p == pid for k, p, c in inc[n]))
            material_missing.append({"kind_code": kind, "family": KINDS[kind], "effective_pid": pid,
                                     "effective_mid": ref["effective_mid"], "node_ids": ns,
                                     "class3_node_ids": sorted(set(ns) & class3_nodes)})
    return {"selection": {"settings": list(map(float, settings)), "cids": [1, 2], "classes": list(CLASSES),
                           "post_result_descriptive_summary": True, "class1_not_selected_but_overlap_reconciled": True},
            "input_relation_rows": len(pairs), "selected_relation_rows_across_settings": len(chosen),
            "unique_selected_nodes_across_all_settings_cids_classes": sorted(chosen_nodes),
            "unique_selected_node_count_across_all_settings_cids_classes": len(chosen_nodes),
            "typed_part_universe": [{"kind_code": k, "family": KINDS[k], "effective_pid": p} for k, p in typed_universe],
            "part_reference_registry": registry, "node_registry": nodes, "groups": groups,
            "same_setting_reconciliation": reconciliations, "missing_material_dependencies": material_missing,
            "nodes_without_shell_incidence": [n["node_id"] for n in nodes if not n["has_shell_incidence"]],
            "nodes_with_unknown_supplied_shell_thickness": [n["node_id"] for n in nodes if n["supplied_shell_corner_thickness_unknown"]]}


def controls():
    def ref(pid, material=True, section=True):
        return {"pid": pid, "part": {"pid": pid, "original_pid": pid, "section_id": pid+100,
                                       "original_section_id": pid+100, "material_id": pid+200,
                                       "original_material_id": pid+200, "line": pid, "source": "wtc7_global_8a_no-conn-matl.k.gz"},
                "material_keyword": "*MAT_ELASTIC" if material else None, "section_defined": section, "section_shell": None}
    pairs = np.asarray([[0, 0, 1, 3, 0, 0], [0, 1, 1, 3, 0, 0], [0, 0, 2, 2, 0, 0],
                        [0, 1, 2, 3, 0, 0], [0, 0, 3, 0, 0, 0], [0, 1, 3, 0, 0, 0],
                        [0, 2, 1, 1, 0, 0], [1, 0, 1, 3, 0, 0]], dtype=np.int64)
    masters = np.asarray([[1, 1, 100], [2, 3, 200], [1, 1, 101]], dtype=np.int64)
    incidence = np.asarray([[1, 0, 10, 2], [1, 1, 20, 1], [2, 0, 10, 1], [2, 0, 11, 1], [3, 1, 20, 1]], dtype=np.int64)
    args = (pairs, masters, incidence, np.asarray([1, 2, 3]), np.asarray([[121, 10], [121, 11], [121, 12]]),
            np.asarray([[.1, .2], [.1, .1], [math.nan, math.nan]]), [ref(10), ref(11, False, False), ref(20)], np.asarray([1., 1.025]))
    s = summarize(*args)
    need(len(s["groups"]) == 12, "control_complete_zero_groups")
    need(any(g["unique_slave_node_count"] == 0 and len(g["typed_parts_in_complete_selected_universe"]) == 3 for g in s["groups"]), "control_part_zeros")
    rec = s["same_setting_reconciliation"][0]
    need(rec["unique_node_count"] == 3 and rec["shared_cid_node_ids"] == [1, 2, 3], "control_cross_cid_dedup")
    need(rec["selected_nodes_with_any_outside_class1_relation"] == [1], "control_outside_overlap")
    need(s["nodes_without_shell_incidence"] == s["nodes_with_unknown_supplied_shell_thickness"] == [3], "control_unknown_beam")
    need(s["missing_material_dependencies"][0]["effective_pid"] == 11 and s["missing_material_dependencies"][0]["class3_node_ids"] == [2], "control_missing_material")
    need(s["unique_selected_node_count_across_all_settings_cids_classes"] == 3, "control_cross_setting_dedup")
    missing = part_reference(999, None)
    need(missing["material_definition_status"] == "unresolved", "control_missing_registry_not_absence")
    beam = part_reference(20, ref(20))
    need(beam["section_definition_status"].startswith("present") and beam["shell_section_locator"] is None, "control_non_shell_section")
    try:
        summarize(np.vstack([pairs, pairs[0]]), *args[1:])
        raise AssertionError("duplicate_not_rejected")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory(prefix="exact-parts-controls-", dir="/private/tmp") as directory:
        p = Path(directory)/"synthetic"
        with p.open("x") as f:
            f.write("synthetic")
        try:
            p.open("x")
            raise AssertionError("create_not_rejected")
        except FileExistsError:
            pass
        try:
            pin(p, "0"*64)
            raise AssertionError("pin_not_rejected")
        except ValueError:
            pass
    return ["complete_setting_cid_class_zero_groups", "complete_typed_part_zero_entries", "cross_cid_node_dedup",
            "cross_class_and_outside_overlap", "unknown_no_shell_beam_nodes", "missing_material_and_section",
            "cross_setting_node_dedup", "missing_registry_not_definition_absence", "present_non_shell_section_locator_limit",
            "duplicate_relation_rejection", "create_only_guard", "pin_mutation_guard"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(HERE/"exact-parts01.json"))
    args = parser.parse_args()
    out = Path(args.output).resolve()
    need(out.parent == HERE, "output_outside_unit")
    start = time.monotonic()
    receipt = {"status": "running", "producer_sha256": digest(Path(__file__)),
               "command": [sys.executable, "-B", "summarize_exact_parts.py", "--output", str(out)],
               "python": sys.version.split()[0], "numpy": np.__version__}
    with out.open("x") as f:
        try:
            receipt["controls"] = controls()
            receipt["pins_before"] = {n: pin(HERE/n, h) for n, h in PINS.items()}
            sr = json.loads((HERE/"stage-root01.json").read_bytes())["result"]
            er = json.loads((HERE/"exact-proximity80.json").read_bytes())
            need(er["status"] == "passed", "exact_receipt_not_passed")
            with np.load(HERE/"exact-proximity80.npz", allow_pickle=False) as exact, np.load(HERE/"stage-root01.npz", allow_pickle=False) as stage:
                pairs = exact["pairs"]
                selected_nodes = np.unique(pairs[np.isin(pairs[:, 3], CLASSES), 2])
                stage_incidence = stage["node_part_incidence"]
                expected = stage_incidence[np.isin(stage_incidence[:, 0], selected_nodes)]
                existing = exact["admitted_node_part_incidence"]
                existing = existing[np.isin(existing[:, 0], selected_nodes)]
                need(np.array_equal(expected, existing), "frozen_incidence_disagreement")
                receipt["result"] = summarize(pairs, exact["master_identity"], stage_incidence,
                                                stage["node_ids"], stage["node_source_line"], stage["corner_thickness_min_max"],
                                                sr["part_references"], exact["settings"])
            receipt["pins_after"] = {n: pin(HERE/n, h) for n, h in PINS.items()}
            need(digest(Path(__file__)) == receipt["producer_sha256"], "producer_changed")
            receipt["scope"] = "Descriptive arithmetic over already frozen derivatives; no independent new source reconstruction, source labels, physical member identification, damage activation, solver contact, restraint strength or cause conclusion."
            receipt["status"] = "passed"
        except Exception as error:
            receipt["status"] = "failed"
            receipt["error_type"] = type(error).__name__
            if isinstance(error, ValueError) and len(error.args) == 1 and isinstance(error.args[0], str) and error.args[0].replace("_", "").isalnum():
                receipt["error_code"] = error.args[0]
        receipt["elapsed_seconds"] = time.monotonic()-start
        json.dump(receipt, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")
    print(json.dumps({k: receipt[k] for k in ("status", "producer_sha256", "elapsed_seconds")}))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
