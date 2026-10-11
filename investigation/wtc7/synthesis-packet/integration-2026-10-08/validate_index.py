"""Read-only preservation/reference checks; not source or scientific acceptance.

Locators and status/basis prose are required declarations, not mechanically
verified semantic support. Hashing never decodes media or authenticates origins.
The optional independence list receives necessary structural checks only.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
APPROVED_ROOTS = (Path("/Users/admin/docs/911"),
                  Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation"))
FROZEN = {
    "protocol": "fbfc63b9c4559d2b7e99cf0daeb67db4f078322a74f2080da5cad2b2af78b888",
    "frozen_inputs": "f2458dd600accc1234c58738de11525b433cd55017e56f55295a2fee01b17fe8",
    "baseline": "fcc7eef21ad67f61bfe46c8cd9a326974c19979ac0a838cc386680c144ed9d61",
}
MUTABLE = {"version", "date", "scope", "remaining_index_work"}
RELATIONS = {"supports", "contradicts", "limits", "requires"}
ORIGIN_STATES = {"identified_at_declared_layer", "unknown"}
EDGE_FIELDS = ("work_packages", "dependencies", "causal_links", "evidence", "transforms")
TRAVERSALS = {"Q04-body-boundary": "Q04", "Q06-native-state": "Q06", "Q09-SEC-access": "Q09"}
LIMIT = ("Structural preservation, declared-reference coverage and pinned bytes only; "
         "not locator accuracy, evidentiary support, source independence/authenticity, "
         "scientific truth, calculation reproduction, human acceptance or expert review.")


class Invalid(ValueError):
    """A failed check; validation stops without a partial-pass claim."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, where):
    require(isinstance(value, dict), f"{where}: expected object")
    return value


def seq(value, where):
    require(isinstance(value, list), f"{where}: expected list")
    return value


def string(value, where):
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonempty string")
    return value


def strings(value, where, unique=False):
    items = [string(x, where) for x in seq(value, where)]
    require(not unique or len(items) == len(set(items)), f"{where}: duplicate IDs")
    return items


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":"))


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path):
    def bad_constant(value):
        raise Invalid(f"non-JSON numeric constant: {value}")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys,
                      parse_constant=bad_constant)


def resolve_file(value, base, roots):
    raw = Path(string(value, "path"))
    require(raw.is_absolute() or ".." not in raw.parts, "relative path traversal")
    path = raw if raw.is_absolute() else base / raw
    require(not any(p.is_symlink() for p in (path, *path.parents)), f"symlink path: {path}")
    path = path.resolve()
    require(any(path.is_relative_to(root) for root in roots), f"path outside approved roots: {path}")
    require(path.is_file(), f"missing/non-file artifact: {path}")
    return path


def file_state(path):
    before = path.stat()
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    after = path.stat()
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
    require(all(getattr(before, f) == getattr(after, f) for f in fields), f"file changed while hashing: {path}")
    return {"bytes": size, "sha256": digest.hexdigest()}


def check_pin(record, base, roots, size_required=True):
    obj(record, "pin")
    digest = string(record.get("sha256"), "sha256")
    require(re.fullmatch(r"[0-9a-f]{64}", digest), "invalid sha256")
    path = resolve_file(record.get("path"), base, roots)
    actual = file_state(path)
    if size_required:
        require(type(record.get("bytes")) is int and record["bytes"] >= 0, "invalid byte count")
        require(record["bytes"] == actual["bytes"], f"size mismatch: {path}")
    require(digest == actual["sha256"], f"hash mismatch: {path}")
    return path


def baseline_claims(baseline):
    """Map exactly the declared containers, including adjacent adverse/supplement."""
    parents, claims = {}, {}
    for row in seq(baseline.get("claims"), "baseline.claims"):
        obj(row, "parent")
        claim_id = string(row.get("id"), "parent.id")
        require(claim_id not in parents, f"duplicate claim ID: {claim_id}")
        parents[claim_id] = string(row.get("question"), "parent.question")
    require(len(parents) == 10 and set(parents.values()) == {f"Q{i:02d}" for i in range(1, 11)},
            "expected ten unique question parents")
    claims.update({key: key for key in parents})

    def add(row, parent):
        obj(row, "child")
        claim_id = string(row.get("id"), "child.id")
        require(claim_id not in claims, f"duplicate claim ID: {claim_id}")
        require(parent in parents, f"unknown parent: {parent}")
        claims[claim_id] = parent

    atomic_count = adverse_count = 0
    for join in seq(baseline.get("primary_source_joins"), "baseline.primary_source_joins"):
        obj(join, "join")
        parent = join.get("parent_claim")
        require(parent in parents, "join has unknown parent")
        for row in seq(join.get("atomic_claims"), "join.atomic_claims"):
            add(row, parent)
            atomic_count += 1
        if "adjacent_case_adverse_claim" in join:
            add(join["adjacent_case_adverse_claim"], parent)
            adverse_count += 1
    supplement = obj(baseline.get("adverse_source_join_supplement"), "supplement")
    matches = [p for p, q in parents.items() if q == supplement.get("parent_question")]
    require(len(matches) == 1, "supplement must map to one question parent")
    extra = seq(supplement.get("claims"), "supplement.claims")
    for row in extra:
        add(row, matches[0])
    require((atomic_count, adverse_count, len(extra), len(claims)) == (26, 1, 3, 40),
            "baseline must retain 26 atomic, one adjacent adverse and three supplement claims")
    return parents, claims


def validate(index_path, baseline_path, inputs_path, *, approved_roots=None, frozen_pins=None):
    """Return deterministic counts or raise Invalid; overrides are for synthetic tests.

    CLI always uses the fixed investigation roots and frozen control hashes.
    No files are written. Byte equality is not evidence-family equivalence.
    """
    roots = tuple(Path(p).resolve() for p in (approved_roots or APPROVED_ROOTS))
    frozen = FROZEN if frozen_pins is None else frozen_pins
    paths = {name: resolve_file(str(path), HERE, roots) for name, path in
             (("index", index_path), ("baseline", baseline_path), ("frozen_inputs", inputs_path))}
    paths["protocol"] = resolve_file(str(paths["frozen_inputs"].parent / "PROTOCOL.md"), HERE, roots)
    before = {name: file_state(path) for name, path in paths.items()}
    for name in FROZEN:
        require(before[name]["sha256"] == frozen[name], f"frozen {name} hash mismatch")
    index, baseline, inputs = (obj(load_json(paths[name]), name)
                               for name in ("index", "baseline", "frozen_inputs"))
    require(set(index) == set(baseline) | {"integration"}, "unexpected or missing top-level keys")
    for key, value in baseline.items():
        if key not in MUTABLE:
            require(encoded(index[key]) == encoded(value), f"baseline field changed: {key}")
    require(type(index.get("version")) is int and index["version"] > baseline["version"],
            "candidate version must advance the baseline")
    for key in sorted(MUTABLE - {"version"}):
        string(index.get(key), key)
    base = Path(string(inputs.get("path_base"), "inputs.path_base"))
    require(base.is_absolute() and any(base.resolve().is_relative_to(r) for r in roots), "invalid path_base")
    for key in ("cause_ranking_change_authorized", "canonical_promotion_authorized", "human_acceptance_supplied"):
        require(inputs.get(key) is False, f"frozen authority flag changed: {key}")
    require(inputs.get("protocol_sha256") == frozen["protocol"], "inputs protocol pin mismatch")
    integration = obj(index.get("integration"), "integration")
    require(type(integration.get("version")) is int and integration["version"] == 1, "integration version must be 1")
    for name in FROZEN:
        meta = obj(integration.get(name), f"integration.{name}")
        require(meta.get("sha256") == frozen[name], f"metadata {name} pin mismatch")
        require(check_pin(meta, base, roots, False) == paths[name], f"metadata {name} path mismatch")

    artifacts = obj(integration.get("artifacts"), "artifacts")
    frozen_rows = seq(inputs.get("inputs"), "inputs.inputs")
    frozen_ids = [obj(row, "input").get("id") for row in frozen_rows]
    require(len(frozen_ids) == 37 and set(frozen_ids) == {f"I{i:02d}" for i in range(1, 38)},
            "expected exact I01–I37 frozen input IDs")
    for row in frozen_rows:
        require(encoded(artifacts.get(row["id"])) == encoded({k: v for k, v in row.items() if k != "id"}),
                f"frozen artifact changed/missing: {row['id']}")
    artifact_paths = {}
    for aid, row in artifacts.items():
        string(aid, "artifact ID")
        obj(row, f"artifact {aid}")
        string(row.get("role"), f"artifact {aid}.role")
        artifact_paths[aid] = check_pin(row, base, roots)
    require(artifact_paths["I02"] == paths["baseline"], "I02 is not the supplied baseline")
    for source in obj(baseline.get("sources"), "baseline.sources").values():
        check_pin(source, base, roots, False)

    parents, claims = baseline_claims(baseline)
    for key, expected in (("baseline_parent_ids", set(parents)),
                          ("baseline_child_ids", set(claims) - set(parents))):
        require(set(strings(inputs.get(key), key, True)) == expected, f"{key} coverage mismatch")
    expected = {"parents": 10, "children": 30, "work_package_exit_rows": 12,
                "dependency_ids": [f"D{i}" for i in range(1, 10)], "causal_link_ordinals": list(range(1, 9))}
    require(encoded(inputs.get("expected_coverage")) == encoded(expected), "frozen expected coverage mismatch")

    def ref(row, where):
        obj(row, where)
        require(row.get("artifact_id") in artifacts, f"{where}: unknown artifact")
        string(row.get("locator"), f"{where}.locator")

    wp = obj(integration.get("wp_components"), "wp_components")
    wp_labels = [line.split("|")[1].strip() for line in artifact_paths["I05"].read_text().splitlines()
                 if re.match(r"^\| WP[0-6] ", line)]
    require(len(wp_labels) == len(set(wp_labels)) == 12, "I05 twelve-component table not found")
    require(len(wp) == 12, "expected twelve WP component aliases")
    for alias, row in wp.items():
        string(alias, "WP alias")
        ref(row, f"WP {alias}")
        require(row["artifact_id"] == "I05", "WP component must locate frozen I05")
    require(sorted(row.get("label", "") for row in wp.values()) == sorted(wp_labels), "WP labels differ from I05")
    dependencies = obj(integration.get("dependencies"), "dependencies")
    causal = obj(integration.get("causal_links"), "causal_links")
    for rows, required, name in ((dependencies, {f"D{i}" for i in range(1, 10)}, "dependencies"),
                                  (causal, {str(i) for i in range(1, 9)}, "causal_links")):
        require(set(rows) == required, f"{name}: exact ID coverage required")
        for key, row in rows.items():
            ref(row, f"{name}.{key}")
            string(row.get("label"), f"{name}.{key}.label")

    families = obj(integration.get("families"), "families")
    for fid, row in families.items():
        string(fid, "family ID")
        obj(row, f"family {fid}")
        for key in ("description", "independence_limit"):
            string(row.get(key), f"family {fid}.{key}")
        require(row.get("origin_status") in ORIGIN_STATES, f"family {fid}: explicit origin_status required")
        basis = seq(row.get("basis"), f"family {fid}.basis")
        require(bool(basis), f"family {fid}: basis required")
        for item in basis:
            ref(item, f"family {fid}.basis")
    transforms = obj(integration.get("transforms"), "transforms")
    for tid, row in transforms.items():
        string(tid, "transform ID")
        obj(row, f"transform {tid}")
        for key in ("status", "limit"):
            string(row.get(key), f"transform {tid}.{key}")
        missing = strings(row.get("missing"), f"transform {tid}.missing")
        for key in ("input_artifacts", "code_artifacts", "output_artifacts", "verification_artifacts"):
            ids = strings(row.get(key), f"transform {tid}.{key}", True)
            require(all(aid in artifacts for aid in ids), f"transform {tid}.{key}: unknown artifact")
            require(bool(ids) or bool(missing), f"transform {tid}.{key}: empty without explicit gap")

    additions = seq(integration.get("additional_claims"), "additional_claims")
    for row in additions:
        obj(row, "additional claim")
        for key in ("id", "parent_claim", "claim", "layer", "grade", "ceiling", "alternative", "would_change_with"):
            string(row.get(key), f"additional claim.{key}")
        require(row["id"] not in claims, f"duplicate claim ID: {row['id']}")
        require(row["parent_claim"] in parents, "additional claim has unknown parent")
        claims[row["id"]] = row["parent_claim"]
    links = obj(integration.get("claim_links"), "claim_links")
    require(set(links) == set(claims), "claim_links: missing or extra material claim IDs")
    memberships = {aid: set() for aid in artifacts}
    for cid, row in links.items():
        obj(row, f"claim link {cid}")
        require(row.get("question") == parents[claims[cid]], f"claim {cid}: contradictory question/parent")
        string(row.get("remaining_gap"), f"claim {cid}.remaining_gap")
        absences = obj(row.get("absences", {}), f"claim {cid}.absences")
        require(set(absences) <= set(EDGE_FIELDS), f"claim {cid}: unknown absence field")
        for field in EDGE_FIELDS:
            edges = seq(row.get(field), f"claim {cid}.{field}")
            if edges:
                require(field not in absences, f"claim {cid}.{field}: absence contradicts present links")
            else:
                absence = obj(absences.get(field), f"claim {cid}.{field}: explicit absence required")
                require(absence.get("kind") in {"not_applicable", "missing"}, f"claim {cid}.{field}: invalid absence kind")
                for key in ("reason", "consequence"):
                    string(absence.get(key), f"claim {cid}.{field}.absence.{key}")
        for item in seq(row.get("work_packages"), f"claim {cid}.work_packages"):
            obj(item, "WP link")
            require(item.get("id") in wp, f"claim {cid}: unknown WP alias")
            string(item.get("role"), "WP role")
        for field, registry in (("dependencies", dependencies), ("causal_links", causal)):
            for item in seq(row.get(field), f"claim {cid}.{field}"):
                obj(item, field)
                require(item.get("id") in registry, f"claim {cid}: unknown {field} ID")
                require(item.get("relation") in RELATIONS, f"claim {cid}: invalid relation")
                for key in ("scope", "basis"):
                    string(item.get(key), f"claim {cid}.{field}.{key}")
        for item in seq(row.get("evidence"), f"claim {cid}.evidence"):
            ref(item, f"claim {cid}.evidence")
            string(item.get("role"), "evidence.role")
            require("family_id" in item, "evidence.family_id must be explicit")
            fid = item["family_id"]
            require(fid is None or fid in families, f"claim {cid}: unknown family ID")
            if fid is None:
                string(item.get("basis"), "unknown evidence family requires explicit basis")
            memberships[item["artifact_id"]].add(fid)
        tids = strings(row.get("transforms"), f"claim {cid}.transforms", True)
        require(all(tid in transforms for tid in tids), f"claim {cid}: unknown transform")
        statuses = obj(row.get("verification_status"), f"claim {cid}.verification_status")
        for key in ("source_inspection", "calculation_reproduction", "human_acceptance", "expert_review"):
            string(statuses.get(key), f"claim {cid}.verification_status.{key}")
    for parent, row in obj(integration.get("status_updates"), "status_updates").items():
        require(parent in parents, "status update must refer to baseline parent")
        obj(row, "status update")
        for key in ("disposition", "limit"):
            string(row.get(key), f"status update.{key}")
        ids = strings(row.get("supporting_claim_ids"), "supporting_claim_ids", True)
        require(bool(ids) and all(cid in claims and claims[cid] == parent for cid in ids),
                "status update has absent, unknown or contradictory supporting claims")

    # These checks establish graph reachability, not the semantic usefulness of
    # the prose steps, evidence roles, declared gaps or dependency assignments.
    traversals = seq(integration.get("traversals"), "traversals")
    traversal_ids = [obj(row, "traversal").get("id") for row in traversals]
    require(len(traversal_ids) == 3 and set(traversal_ids) == set(TRAVERSALS),
            "traversals: exact three traversal IDs required")
    for row in traversals:
        tid = row["id"]
        cids = strings(row.get("claim_ids"), f"traversal {tid}.claim_ids", True)
        require(bool(cids) and all(cid in claims and cid.startswith(TRAVERSALS[tid] + "-")
                                  and links[cid]["question"] == TRAVERSALS[tid] for cid in cids),
                f"traversal {tid}: unknown or wrong-question claims")
        reachable_transforms = {t for cid in cids for t in links[cid]["transforms"]}
        reachable_dependencies = {d["id"] for cid in cids for d in links[cid]["dependencies"]}
        reachable_artifacts = {e["artifact_id"] for cid in cids for e in links[cid]["evidence"]}
        for transform in reachable_transforms:
            for field in ("input_artifacts", "code_artifacts", "output_artifacts", "verification_artifacts"):
                reachable_artifacts.update(transforms[transform][field])
        for field, reachable, nonempty in (("artifact_ids", reachable_artifacts, True),
                                            ("transform_ids", reachable_transforms, True),
                                            ("dependency_ids", reachable_dependencies, False)):
            ids = strings(row.get(field), f"traversal {tid}.{field}", True)
            require(not nonempty or bool(ids), f"traversal {tid}.{field}: at least one ID required")
            require(set(ids) <= reachable, f"traversal {tid}.{field}: reference not reachable through named claims")
        string(row.get("gap"), f"traversal {tid}.gap")
        require(bool(strings(row.get("steps"), f"traversal {tid}.steps")), f"traversal {tid}: steps required")

    if "independent_source_artifacts" in integration:
        declared = strings(integration["independent_source_artifacts"], "independent_source_artifacts", True)
        used = set()
        for aid in declared:
            require(aid in artifacts, "independence declaration: unknown artifact")
            assigned = memberships[aid]
            require(len(assigned) == 1 and None not in assigned, "independence declaration: unknown/ambiguous family")
            fid = next(iter(assigned))
            require(families[fid]["origin_status"] == "identified_at_declared_layer",
                    "independence declaration: unknown origin")
            require(fid not in used, "independence declaration: same known family repeated")
            used.add(fid)
    require(all(file_state(path) == before[name] for name, path in paths.items()), "control file changed during validation")
    return {"status": "pass", "baseline_parents": 10, "baseline_children": 30,
            "baseline_claims": 40, "additional_claims": len(additions), "claim_links": len(links),
            "frozen_artifacts": 37, "artifacts": len(artifacts), "wp_components": len(wp),
            "dependencies": len(dependencies), "causal_links": len(causal),
            "families": len(families), "transforms": len(transforms),
            "mechanically_reachable_traversals": len(traversals),
            "optional_independence_declaration_checked": "independent_source_artifacts" in integration,
            "index_sha256": before["index"]["sha256"], "limit": LIMIT}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=HERE / "candidate-index.json")
    parser.add_argument("--baseline", type=Path, default=HERE / "baseline-index.json")
    parser.add_argument("--inputs", type=Path, default=HERE / "inputs.json")
    args = parser.parse_args(argv)
    try:
        result = validate(args.index.absolute(), args.baseline.absolute(), args.inputs.absolute())
    except (Invalid, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "fail", "error": str(exc), "limit": LIMIT}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
