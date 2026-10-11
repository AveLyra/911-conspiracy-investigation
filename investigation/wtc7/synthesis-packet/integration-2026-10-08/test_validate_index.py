"""Synthetic-only controls for the local index verifier; no historical decoding."""

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import validate_index as v


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="index-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.unit = self.base / "unit"
        self.unit.mkdir()
        self.baseline_path = self.unit / "baseline-index.json"
        self.inputs_path = self.unit / "inputs.json"
        self.index_path = self.unit / "candidate-index.json"
        self.protocol_path = self.unit / "PROTOCOL.md"
        self.protocol_path.write_text("Synthetic protocol, not historical evidence.\n")
        parents = [{"id": f"Q{i:02d}-parent", "question": f"Q{i:02d}", "claim": "qualified"}
                   for i in range(1, 11)]
        joins = [{"id": f"container-{i}", "parent_claim": p["id"], "atomic_claims": []}
                 for i, p in enumerate(parents)]
        for i in range(26):
            joins[i % 10]["atomic_claims"].append({"id": f"atomic-{i}", "claim": "qualified"})
        joins[5]["adjacent_case_adverse_claim"] = {"id": "Q06-adverse", "claim": "contrary"}
        supplement = {"id": "supplement-container", "parent_question": "Q09", "claims":
                      [{"id": f"Q09-supplement-{i}", "claim": "qualified"} for i in range(3)]}
        source = self.base / "source.txt"
        source.write_text("synthetic source\n")
        self.baseline = {"version": 1, "date": "2026-10-07", "scope": "frozen old scope",
                         "remaining_index_work": "old work", "status": "research only",
                         "sources": {"S": {"path": "source.txt", "sha256": self.sha(source)}},
                         "claims": parents, "primary_source_joins": joins,
                         "adverse_source_join_supplement": supplement,
                         "critical_review": {"reviewed_index_sha256": "dated prior review only"},
                         "cause_ranking_changed": False, "canonical_promotion": False}
        self.save(self.baseline_path, self.baseline)
        parent_map, claim_map = v.baseline_claims(self.baseline)
        self.labels = [f"WP{i % 7} synthetic exact exit component {i}" for i in range(12)]
        frozen_rows = []
        for i in range(1, 38):
            path = self.base / f"input-{i:02d}.txt"
            path.write_text("same synthetic bytes for different possible origins\n")
            if i == 2:
                path = self.baseline_path
            elif i == 5:
                path.write_text("\n".join(f"| {label} | gap |" for label in self.labels))
            frozen_rows.append({"id": f"I{i:02d}", "path": str(path.relative_to(self.base)),
                                "role": "synthetic role", **v.file_state(path)})
        self.inputs = {"path_base": str(self.base), "protocol_sha256": self.sha(self.protocol_path),
                       "inputs": frozen_rows, "baseline_parent_ids": list(parent_map),
                       "baseline_child_ids": [key for key in claim_map if key not in parent_map],
                       "expected_coverage": {"parents": 10, "children": 30, "work_package_exit_rows": 12,
                                             "dependency_ids": [f"D{i}" for i in range(1, 10)],
                                             "causal_link_ordinals": list(range(1, 9))},
                       "cause_ranking_change_authorized": False, "canonical_promotion_authorized": False,
                       "human_acceptance_supplied": False}
        self.save(self.inputs_path, self.inputs)
        self.pins = {"protocol": self.sha(self.protocol_path), "baseline": self.sha(self.baseline_path),
                     "frozen_inputs": self.sha(self.inputs_path)}
        integration = {"version": 1, "artifacts": {row["id"]: {k: val for k, val in row.items() if k != "id"}
                                                     for row in frozen_rows},
                       "wp_components": {f"WP-{i}": {"label": label, "artifact_id": "I05", "locator": f"row {i}"}
                                         for i, label in enumerate(self.labels)},
                       "dependencies": {f"D{i}": self.location(f"D{i}") for i in range(1, 10)},
                       "causal_links": {str(i): self.location(f"link {i}") for i in range(1, 9)},
                       "families": {"F1": self.family("I01"), "F2": self.family("I03"),
                                    "FU": self.family("I04", "unknown")},
                       "transforms": {"T1": {"input_artifacts": ["I01"], "code_artifacts": ["I03"],
                                             "output_artifacts": ["I04"], "verification_artifacts": ["I05"],
                                             "status": "qualified synthetic declaration", "missing": [],
                                             "limit": "Does not establish truth"}},
                       "additional_claims": [{"id": "new-claim", "parent_claim": "Q01-parent",
                                              "claim": "new qualified declaration", "layer": "synthetic",
                                              "grade": "descriptive grade", "ceiling": "bounded",
                                              "alternative": "another origin", "would_change_with": "new record"}],
                       "claim_links": {}, "status_updates": {"Q01-parent": {"disposition": "qualified update",
                            "supporting_claim_ids": ["new-claim"], "limit": "not entire question closure"}}}
        for name, path in (("protocol", self.protocol_path), ("baseline", self.baseline_path),
                           ("frozen_inputs", self.inputs_path)):
            integration[name] = {"path": str(path.relative_to(self.base)), "sha256": self.pins[name]}
        claim_map["new-claim"] = "Q01-parent"
        for cid, parent in claim_map.items():
            integration["claim_links"][cid] = {
                "question": parent_map[parent], "work_packages": [{"id": "WP-0", "role": "process requirement"}],
                "dependencies": [{"id": "D1", "relation": "limits", "scope": "declared metric", "basis": "located gap"}],
                "causal_links": [{"id": "1", "relation": "requires", "scope": "conditional", "basis": "located gap"}],
                "evidence": [self.evidence("I01", "F1")], "transforms": ["T1"],
                "verification_status": {key: "not supplied by this checker" for key in
                    ("source_inspection", "calculation_reproduction", "human_acceptance", "expert_review")},
                "remaining_gap": "Unknown historical origin and interpretation remain"}
        integration["claim_links"]["Q02-parent"]["evidence"].append(self.evidence("I03", "F2"))
        integration["traversals"] = [{"id": tid, "claim_ids": [question + "-parent"],
                                     "artifact_ids": ["I01", "I04"], "transform_ids": ["T1"],
                                     "dependency_ids": ["D1"], "gap": "qualified consequential gap",
                                     "steps": ["Declared evidence to declared transform", "Transform to remaining gap"]}
                                    for tid, question in v.TRAVERSALS.items()]
        self.index = copy.deepcopy(self.baseline)
        self.index.update(version=2, date="2026-10-08", scope="new scope", remaining_index_work="new gaps",
                          integration=integration)

    @staticmethod
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def save(path, value):
        path.write_text(json.dumps(value, indent=2) + "\n")

    @staticmethod
    def location(label):
        return {"label": label, "artifact_id": "I06", "locator": f"table {label}"}

    @staticmethod
    def family(aid, status="identified_at_declared_layer"):
        return {"description": "declared origin", "basis": [{"artifact_id": aid, "locator": "origin declaration"}],
                "origin_status": status, "independence_limit": "not authenticated independence"}

    @staticmethod
    def evidence(aid, fid):
        return {"artifact_id": aid, "locator": "selected subsection", "role": "qualified evidence", "family_id": fid}

    @property
    def integration(self):
        return self.index["integration"]

    def run_check(self):
        self.save(self.index_path, self.index)
        return v.validate(self.index_path, self.baseline_path, self.inputs_path,
                          approved_roots=(self.base,), frozen_pins=self.pins)

    def fails(self, text):
        with self.assertRaisesRegex(v.Invalid, text):
            self.run_check()

    def test_valid_deterministic_counts_and_no_independence_count(self):
        first = self.run_check()
        self.assertEqual(first, self.run_check())
        self.assertEqual((first["baseline_claims"], first["additional_claims"], first["claim_links"]), (40, 1, 41))
        self.assertEqual((first["frozen_artifacts"], first["wp_components"], first["dependencies"], first["causal_links"]),
                         (37, 12, 9, 8))
        self.assertNotIn("independent_source_count", first)
        self.assertFalse(first["optional_independence_declaration_checked"])
        self.assertEqual(first["mechanically_reachable_traversals"], 3)

    def test_total_link_erasure_cannot_pass_roster_counts(self):
        for row in self.integration["claim_links"].values():
            for field in v.EDGE_FIELDS:
                row[field] = []
        self.integration["families"] = {}
        self.integration["transforms"] = {}
        self.fails("explicit absence required")

    def test_new_claim_evidence_or_transform_erasure_requires_specific_gap(self):
        for field in v.EDGE_FIELDS:
            with self.subTest(field=field):
                row = self.integration["claim_links"]["new-claim"]
                original = row[field]
                row[field] = []
                self.fails("explicit absence required")
                row["absences"] = {field: {"kind": "not_applicable", "reason": "Outside this relation registry",
                                           "consequence": "No support or completion is inferred"}}
                self.assertEqual(self.run_check()["status"], "pass")
                row[field] = original
                self.fails("absence contradicts present links")
                del row["absences"]

    def test_missing_link_gap_requires_reason_and_consequence(self):
        row = self.integration["claim_links"]["new-claim"]
        row["evidence"] = []
        row["absences"] = {"evidence": {"kind": "missing", "reason": "No located record"}}
        self.fails("absence.consequence: expected nonempty")
        row["absences"]["evidence"]["consequence"] = "Claim remains unsupported in declared selection"
        self.assertEqual(self.run_check()["status"], "pass")

    def test_traversal_registry_erasure_and_duplicate_ids_rejected(self):
        original = copy.deepcopy(self.integration["traversals"])
        self.integration["traversals"] = []
        self.fails("exact three traversal IDs")
        self.integration["traversals"] = [original[0], original[0], original[2]]
        self.fails("exact three traversal IDs")

    def test_traversal_claim_and_required_step_gap_fields(self):
        row = self.integration["traversals"][0]
        row["claim_ids"] = ["Q07-parent"]
        self.fails("wrong-question claims")
        row["claim_ids"] = ["Q04-parent"]
        row["steps"] = []
        self.fails("steps required")
        row["steps"] = ["declared graph step"]
        row["gap"] = ""
        self.fails("gap: expected nonempty")

    def test_globally_existing_references_must_be_reachable_in_traversal(self):
        row = self.integration["traversals"][0]
        row["artifact_ids"] = ["I37"]
        self.fails("artifact_ids: reference not reachable")
        row["artifact_ids"] = ["I04"]  # Transform output is reachable, not direct evidence.
        self.integration["transforms"]["T2"] = copy.deepcopy(self.integration["transforms"]["T1"])
        row["transform_ids"] = ["T2"]
        self.fails("transform_ids: reference not reachable")
        row["transform_ids"] = ["T1"]
        row["dependency_ids"] = ["D9"]
        self.fails("dependency_ids: reference not reachable")
        row["dependency_ids"] = []  # No universal D1–D9 gate.
        self.assertEqual(self.run_check()["status"], "pass")

    def test_traversal_requires_artifact_and_transform(self):
        row = self.integration["traversals"][0]
        for field in ("artifact_ids", "transform_ids"):
            with self.subTest(field=field):
                original = row[field]
                row[field] = []
                self.fails("at least one ID required")
                row[field] = original

    def test_missing_adverse_claim_link(self):
        del self.integration["claim_links"]["Q06-adverse"]
        self.fails("missing or extra material claim")

    def test_dropped_adverse_baseline_content(self):
        del self.index["primary_source_joins"][5]["adjacent_case_adverse_claim"]
        self.fails("baseline field changed: primary_source_joins")

    def test_missing_supplement_link(self):
        del self.integration["claim_links"]["Q09-supplement-0"]
        self.fails("missing or extra material claim")

    def test_duplicate_new_claim_id(self):
        self.integration["additional_claims"].append(copy.deepcopy(self.integration["additional_claims"][0]))
        self.fails("duplicate claim ID")

    def test_new_claim_cannot_reuse_baseline_id(self):
        self.integration["additional_claims"][0]["id"] = "Q06-adverse"
        self.fails("duplicate claim ID")

    def test_duplicate_json_object_key_rejected(self):
        self.index_path.write_text('{"version": 2, "version": 3}')
        with self.assertRaisesRegex(v.Invalid, "duplicate JSON key"):
            v.load_json(self.index_path)

    def test_non_json_nan_rejected(self):
        self.index_path.write_text('{"value": NaN}')
        with self.assertRaisesRegex(v.Invalid, "non-JSON numeric"):
            v.load_json(self.index_path)

    def test_stale_artifact_hash_same_size(self):
        path = self.base / "input-01.txt"
        value = path.read_bytes()
        path.write_bytes(b"X" + value[1:])
        self.fails("hash mismatch")

    def test_size_mismatch(self):
        (self.base / "input-01.txt").write_text("short")
        self.fails("size mismatch")

    def test_frozen_input_cannot_be_replaced_or_rehashed(self):
        self.integration["artifacts"]["I01"]["sha256"] = "0" * 64
        self.fails("frozen artifact changed/missing")

    def test_frozen_inputs_file_cannot_be_rehashed_into_acceptance(self):
        self.inputs["scope"] = "changed frozen input file"
        self.save(self.inputs_path, self.inputs)
        self.integration["frozen_inputs"]["sha256"] = self.sha(self.inputs_path)
        self.fails("frozen frozen_inputs hash mismatch")

    def test_missing_frozen_artifact(self):
        del self.integration["artifacts"]["I37"]
        self.fails("frozen artifact changed/missing")

    def test_added_artifact_hash_is_checked(self):
        self.integration["artifacts"]["A1"] = {"path": "source.txt", "role": "extra",
            "bytes": (self.base / "source.txt").stat().st_size, "sha256": "0" * 64}
        self.fails("hash mismatch")

    def test_old_critical_review_and_source_roles_preserved(self):
        for key in ("critical_review", "sources", "status"):
            with self.subTest(key=key):
                original = self.index[key]
                self.index[key] = "claimed new review"
                self.fails(f"baseline field changed: {key}")
                self.index[key] = original

    def test_boolean_not_equal_to_integer_in_preserved_fields(self):
        self.index["cause_ranking_changed"] = 0
        self.fails("baseline field changed")

    def test_exact_work_package_labels_and_count(self):
        self.integration["wp_components"]["WP-0"]["label"] += " edited"
        self.fails("WP labels differ")
        self.integration["wp_components"]["WP-0"]["label"] = self.labels[0]
        del self.integration["wp_components"]["WP-11"]
        self.fails("twelve WP component")

    def test_exact_dependency_and_causal_id_coverage(self):
        for field, key in (("dependencies", "D9"), ("causal_links", "8")):
            with self.subTest(field=field):
                original = self.integration[field].pop(key)
                self.fails("exact ID coverage")
                self.integration[field][key] = original

    def test_dangling_artifact_and_empty_locator(self):
        evidence = self.integration["claim_links"]["Q01-parent"]["evidence"][0]
        evidence["artifact_id"] = "missing"
        self.fails("unknown artifact")
        evidence["artifact_id"] = "I01"
        evidence["locator"] = " "
        self.fails("locator: expected nonempty")

    def test_parent_question_contradiction_and_wrong_status_parent(self):
        self.integration["claim_links"]["Q09-supplement-0"]["question"] = "Q01"
        self.fails("contradictory question/parent")
        self.integration["claim_links"]["Q09-supplement-0"]["question"] = "Q09"
        self.integration["status_updates"]["Q01-parent"]["supporting_claim_ids"] = ["Q09-supplement-0"]
        self.fails("contradictory supporting claims")

    def test_unknown_parent_and_transform(self):
        self.integration["additional_claims"][0]["parent_claim"] = "Q99"
        self.fails("unknown parent")
        self.integration["additional_claims"][0]["parent_claim"] = "Q01-parent"
        self.integration["claim_links"]["Q01-parent"]["transforms"] = ["missing"]
        self.fails("unknown transform")

    def test_missing_transform_chain_requires_explicit_gap(self):
        row = self.integration["transforms"]["T1"]
        row["code_artifacts"] = []
        self.fails("empty without explicit gap")
        row["missing"] = ["Code unavailable; calculation not reproduced by this index"]
        self.assertEqual(self.run_check()["status"], "pass")

    def test_all_four_verification_dimensions_required(self):
        del self.integration["claim_links"]["Q01-parent"]["verification_status"]["expert_review"]
        self.fails("expert_review: expected nonempty")

    def test_invalid_relation_not_silently_support(self):
        self.integration["claim_links"]["Q01-parent"]["dependencies"][0]["relation"] = "same-question"
        self.fails("invalid relation")

    def test_unknown_family_requires_basis_but_does_not_fail_default(self):
        row = self.integration["claim_links"]["Q01-parent"]["evidence"][0]
        row["family_id"] = None
        self.fails("unknown evidence family requires explicit basis")
        row["basis"] = "Origin not located; see remaining gap"
        self.assertEqual(self.run_check()["status"], "pass")

    def test_independence_rejects_two_artifacts_in_same_family(self):
        self.integration["claim_links"]["Q02-parent"]["evidence"].append(self.evidence("I04", "F1"))
        self.integration["independent_source_artifacts"] = ["I01", "I04"]
        self.fails("same known family repeated")

    def test_independence_rejects_duplicate_artifact_ids(self):
        self.integration["independent_source_artifacts"] = ["I01", "I01"]
        self.fails("duplicate IDs")

    def test_independence_rejects_unassigned_null_unknown_and_multiple_origins(self):
        self.integration["independent_source_artifacts"] = ["I04"]
        self.fails("unknown/ambiguous family")
        row = self.evidence("I04", None)
        row["basis"] = "origin unknown"
        evidence = self.integration["claim_links"]["Q02-parent"]["evidence"]
        evidence.append(row)
        self.fails("unknown/ambiguous family")
        row["family_id"] = "FU"
        self.fails("unknown origin")
        row["family_id"] = "F1"
        evidence.append(self.evidence("I04", "F2"))
        self.fails("unknown/ambiguous family")

    def test_same_bytes_do_not_merge_different_declared_origins(self):
        self.assertEqual(self.integration["artifacts"]["I01"]["sha256"], self.integration["artifacts"]["I03"]["sha256"])
        self.integration["independent_source_artifacts"] = ["I01", "I03"]
        result = self.run_check()
        self.assertTrue(result["optional_independence_declaration_checked"])
        self.assertIn("not locator accuracy", result["limit"])

    def test_multiple_origins_in_one_artifact_allowed_without_independence_claim(self):
        self.integration["claim_links"]["Q01-parent"]["evidence"].append(self.evidence("I01", "F2"))
        self.assertEqual(self.run_check()["status"], "pass")

    def test_missing_artifact_and_symlink_rejected(self):
        path = self.base / "input-01.txt"
        path.unlink()
        self.fails("missing/non-file")
        path.symlink_to(self.base / "input-03.txt")
        self.fails("symlink path")

    def test_absolute_approved_path_allowed_and_traversal_rejected(self):
        self.integration["artifacts"]["A1"] = {"path": str(self.base / "source.txt"),
                                               "role": "extra", **v.file_state(self.base / "source.txt")}
        self.assertEqual(self.run_check()["status"], "pass")
        self.integration["artifacts"]["A1"]["path"] = "../outside.txt"
        self.fails("relative path traversal")

    def test_unapproved_absolute_path_rejected_before_read(self):
        self.integration["artifacts"]["A1"] = {"path": "/outside-approved-root/source.txt", "role": "extra",
                                               "bytes": 0, "sha256": "0" * 64}
        self.fails("path outside approved roots")

    def test_cli_read_only_success_and_failure(self):
        self.save(self.index_path, self.index)
        args = ["--index", str(self.index_path), "--baseline", str(self.baseline_path), "--inputs", str(self.inputs_path)]
        before = {p: p.read_bytes() for p in self.base.rglob("*") if p.is_file()}
        with mock.patch.object(v, "APPROVED_ROOTS", (self.base,)), mock.patch.object(v, "FROZEN", self.pins):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(v.main(args), 0)
            self.assertEqual(json.loads(output.getvalue())["status"], "pass")
            self.assertEqual(before, {p: p.read_bytes() for p in self.base.rglob("*") if p.is_file()})
            self.index_path.write_text('{"bad": 1}')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(v.main(args), 1)
            self.assertEqual(json.loads(output.getvalue())["status"], "fail")


if __name__ == "__main__":
    unittest.main()
