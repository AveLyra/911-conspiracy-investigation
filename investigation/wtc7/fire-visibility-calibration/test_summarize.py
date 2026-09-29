"""Synthetic rule/schema controls; never opens historical or real label files."""

import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import summarize as subject


def row(**changes):
    result = {
        "asset_id": "A-e43e4088a4a2", "unit_id": "U02",
        "candidate_identity": "single_candidate", "opportunity": [0.5, 0.75],
        "cautions": ["minor frame overlap", "unknown glazing"],
        "decisive_exclusions": [], "appearance": "ambiguous_glow",
        "reason": "Synthetic rule-comprehension example, not an image judgment.",
    }
    result.update(changes)
    return result


def geometry(**changes):
    result = {"polygon": [[10, 10], [30, 10], [30, 30], [10, 30]],
              "in_frame_fraction": [1, 1]}
    result.update(changes)
    return result


def labels(reviewer="synthetic-a"):
    return {
        "reviewer": reviewer,
        "independence": "Synthetic data only; no historical annotations inspected.",
        "protocol_sha256": subject.PROTOCOL_SHA256,
        "geometry_sha256": subject.GEOMETRY_SHA256,
        "annotations": [row(asset_id=asset_id, unit_id=unit_id)
                        for asset_id, ids in subject.SAMPLE.items() for unit_id in ids],
    }


def fixture_geometry():
    # Build geometry independently of the preserved source geometry.
    return {"assets": [
        {"asset_id": asset_id, **subject.PINS[asset_id],
         "target_polygon": [[0, 0], [50, 0], [50, 50], [0, 50]],
         "overlay_rectangles": [[0, 0, 1, 1]],
         "units": [{"unit_id": unit_id, **geometry()} for unit_id in unit_ids]}
        for asset_id, unit_ids in subject.SAMPLE.items()
    ]}


class RuleControls(unittest.TestCase):
    def evaluate(self, annotation=None, unit_geometry=None, threshold=0.5):
        return subject.classify(annotation or row(), unit_geometry or geometry(), threshold)

    def test_00_ten_frozen_scenarios(self):
        scenarios = [
            (1, row(), "eligible", "eligible", False),
            (2, row(decisive_exclusions=[{"code": "dominant_obstruction",
                                         "reason": "Obstruction prevents unit-level assessment."}]),
             "excluded", "excluded", False),
            (3, row(candidate_identity="clipped", appearance="flame_structure"),
             "excluded", "excluded", False),
            (4, row(candidate_identity="not_single", appearance="flame_structure"),
             "excluded", "excluded", False),
            (5, row(candidate_identity="unresolved"), "unknown", "unknown", False),
            (6, row(opportunity=[0.25, 0.5]), "unknown", "unknown", False),
            (7, row(opportunity=[0, 0.25]), "excluded", "excluded", False),
            (8, row(opportunity=None), "unknown", "unknown", False),
            (9, row(opportunity=[0.75, 1], appearance="no_flame_discernible"),
             "eligible", "eligible", False),
            (10, row(appearance="non_evaluable"), "eligible", "unknown", True),
        ]
        for index, annotation, preliminary, final, conflict in scenarios:
            with self.subTest(scenario=index):
                result = self.evaluate(annotation)
                self.assertEqual(result["preliminary_status"], preliminary)
                self.assertEqual(result["status"], final)
                self.assertEqual(result["semantic_conflict"], conflict)
                self.assertEqual(result["annotation"], annotation)

    def test_appearance_invariance_of_preliminary_gate(self):
        for appearance in subject.APPEARANCES:
            with self.subTest(appearance=appearance):
                result = self.evaluate(row(appearance=appearance))
                self.assertEqual(result["preliminary_status"], "eligible")
                expected = "unknown" if appearance == "non_evaluable" else "eligible"
                self.assertEqual(result["status"], expected)
        for identity in ("not_single", "unresolved", "clipped"):
            observed = {self.evaluate(row(candidate_identity=identity, appearance=appearance))["status"]
                        for appearance in subject.APPEARANCES}
            self.assertEqual(len(observed), 1)

    def test_caution_count_does_not_veto(self):
        for cautions in ([], ["glazing"], ["glazing", "localized saturation", "blur"]):
            self.assertEqual(self.evaluate(row(cautions=cautions))["status"], "eligible")

    def test_all_unresolved_reasons_survive_exclusion(self):
        result = self.evaluate(
            row(candidate_identity="unresolved", opportunity=None,
                decisive_exclusions=[{"code": "dominant_overlay", "reason": "Target detail hidden."}]),
            geometry(in_frame_fraction=None),
        )
        self.assertEqual(result["status"], "excluded")
        self.assertEqual({r["code"] for r in result["reasons"]["unresolved"]},
                         {"identity_unresolved", "opportunity_unknown", "in_frame_unknown"})

    def test_low_opportunity_excludes_unresolved_identity(self):
        result = self.evaluate(row(candidate_identity="unresolved", opportunity=[0, 0.25]))
        self.assertEqual(result["status"], "excluded")
        self.assertEqual(result["reasons"]["unresolved"][0]["code"], "identity_unresolved")

    def test_in_frame_null_and_zero_and_nonzero_partial(self):
        self.assertEqual(self.evaluate(unit_geometry=geometry(in_frame_fraction=None))["status"], "unknown")
        self.assertEqual(self.evaluate(unit_geometry=geometry(in_frame_fraction=[0, 0]))["status"], "excluded")
        # Protocol does not multiply opportunity by in-frame bounds or threshold in-frame fraction.
        self.assertEqual(self.evaluate(unit_geometry=geometry(in_frame_fraction=[0.1, 0.2]))["status"], "eligible")

    def test_tiny_axis_and_exact_eight_boundary(self):
        for points, expected in [
            ([[10, 10], [17.99, 10], [17.99, 30], [10, 30]], "excluded"),
            ([[10, 10], [30, 10], [30, 17.99], [10, 17.99]], "excluded"),
            ([[10, 10], [18, 10], [18, 18], [10, 18]], "eligible"),
        ]:
            self.assertEqual(self.evaluate(unit_geometry=geometry(polygon=points))["status"], expected)

    def test_exact_threshold_bounds(self):
        for threshold, opportunity, expected in [
            (0.25, [0, 0.25], "unknown"), (0.25, [0.25, 0.5], "eligible"),
            (0.5, [0.25, 0.5], "unknown"), (0.5, [0.5, 0.75], "eligible"),
            (0.75, [0.5, 0.75], "unknown"), (0.75, [0.75, 1], "eligible"),
            (0.75, [0.25, 0.5], "excluded"),
        ]:
            self.assertEqual(self.evaluate(row(opportunity=opportunity), threshold=threshold)["status"], expected)

    def test_non_evaluable_only_conflicts_when_preliminarily_eligible(self):
        for opportunity, expected in [(None, "unknown"), ([0, 0.25], "excluded")]:
            result = self.evaluate(row(appearance="non_evaluable", opportunity=opportunity))
            self.assertFalse(result["semantic_conflict"])
            self.assertEqual(result["status"], expected)

    def test_bad_threshold_rejected(self):
        for threshold in (True, False, 0.6, float("nan"), float("inf")):
            with self.assertRaises(subject.ValidationError):
                self.evaluate(threshold=threshold)


class SchemaControls(unittest.TestCase):
    def reject(self, data):
        with self.assertRaises(subject.ValidationError):
            subject.validate_labels(data)

    def test_valid_13_unit_fixture(self):
        self.assertEqual(len(subject.validate_labels(labels())["annotations"]), 13)

    def test_independence_metadata_object_preserved_without_coercion(self):
        data = labels()
        metadata = {"context": "Synthetic only", "prior_labels_seen": False,
                    "limitations": ["Shared frozen geometry"]}
        data["independence"] = metadata
        self.assertIs(subject.validate_labels(data)["independence"], metadata)
        data["independence"] = {}
        self.reject(data)
        data["independence"] = {"nonfinite": float("nan")}
        self.reject(data)

    def test_duplicate_missing_unknown_and_wrong_asset_ids(self):
        changes = [
            lambda data: data["annotations"].append(copy.deepcopy(data["annotations"][0])),
            lambda data: data["annotations"].pop(),
            lambda data: data["annotations"][0].update(unit_id="U99"),
            lambda data: data["annotations"][0].update(asset_id="A-unknown"),
            lambda data: data["annotations"][0].update(unit_id="R01C03"),
        ]
        for change in changes:
            data = labels()
            change(data)
            self.reject(data)

    def test_all_required_fields(self):
        for field in subject.TOP_FIELDS:
            data = labels()
            del data[field]
            self.reject(data)
        for field in subject.ROW_FIELDS:
            data = labels()
            del data["annotations"][0][field]
            self.reject(data)

    def test_invalid_enums_intervals_and_boolean_numbers(self):
        invalid = [
            ("candidate_identity", "opening"), ("candidate_identity", []),
            ("appearance", "fire"), ("appearance", None),
            ("opportunity", [False, 0.25]), ("opportunity", [0.75, True]),
            ("opportunity", [float("nan"), 0.5]),
            ("opportunity", [0, float("inf")]),
            ("opportunity", [0.2, 0.5]), ("opportunity", [0.5, 0.25]),
            ("opportunity", [-0.25, 0]), ("opportunity", [0.75, 2]),
            ("opportunity", [0.5]), ("opportunity", "unknown"),
            ("opportunity", [0, 10 ** 1000]),
        ]
        for field, value in invalid:
            with self.subTest(field=field, value=repr(value)[:80]):
                data = labels()
                data["annotations"][0][field] = value
                self.reject(data)

    def test_strings_reasons_and_list_structure(self):
        for field in ("reviewer", "independence"):
            for value in (" ", None, 3, []):
                data = labels()
                data[field] = value
                self.reject(data)
        for field, value in [
            ("reason", " "), ("reason", None), ("cautions", "haze"),
            ("cautions", [None]), ("cautions", [" "]),
            ("decisive_exclusions", ["obstruction"]),
            ("decisive_exclusions", [{"code": "obstruction"}]),
            ("decisive_exclusions", [{"code": "obstruction", "reason": ""}]),
            ("decisive_exclusions", [{"code": "", "reason": "Blocks assessment"}]),
        ]:
            data = labels()
            data["annotations"][0][field] = value
            self.reject(data)

    def test_hash_mismatches(self):
        for field in ("protocol_sha256", "geometry_sha256"):
            data = labels()
            data[field] = "0" * 64
            self.reject(data)

    def test_duplicate_json_keys_and_nonfinite_values(self):
        for data in ('{"x": 1, "x": 2}', '{"nested": {"x": 1, "x": 2}}',
                     '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}',
                     '{"metadata": [1e999]}'):
            with self.assertRaises(subject.ValidationError):
                subject.decode_json(data)

    def test_geometry_coordinate_and_interval_validation(self):
        for field, value in [
            ("polygon", [[-1, 0], [10, 0], [10, 10]]),
            ("polygon", [[0, 0], [721, 0], [10, 10]]),
            ("polygon", [[0, 0], [10, 479], [10, 10]]),
            ("polygon", [[False, 0], [10, 0], [10, 10]]),
            ("polygon", [[float("nan"), 0], [10, 0], [10, 10]]),
            ("in_frame_fraction", [False, 1]),
            ("in_frame_fraction", [0, 2]),
            ("in_frame_fraction", [0.8, 0.7]),
        ]:
            data = fixture_geometry()
            data["assets"][0]["units"][0][field] = value
            with self.assertRaises(subject.ValidationError):
                subject.validate_geometry(data)

    def test_duplicate_geometry_units_and_missing_sample(self):
        data = fixture_geometry()
        data["assets"][0]["units"].append(copy.deepcopy(data["assets"][0]["units"][0]))
        with self.assertRaises(subject.ValidationError):
            subject.validate_geometry(data)
        data = fixture_geometry()
        data["assets"][0]["units"].pop()
        with self.assertRaises(subject.ValidationError):
            subject.validate_geometry(data)

    def test_source_geometry_pins_and_dimensions(self):
        for field, value in (("path", "different.jpg"), ("sha256", "0" * 64),
                             ("width", 719), ("height", 477)):
            data = fixture_geometry()
            data["assets"][0][field] = value
            with self.assertRaises(subject.ValidationError):
                subject.validate_geometry(data)


class ReportControls(unittest.TestCase):
    def test_independent_axes_preserve_all_differences(self):
        left, right = labels(), labels("synthetic-b")
        right["annotations"][0].update(
            candidate_identity="clipped", opportunity=None, cautions=["haze"],
            decisive_exclusions=[{"code": "material", "reason": "Target is hidden."}],
            appearance="flame_structure", reason="Second synthetic judgment.",
        )
        comparison = subject.differences([left, right])[0]
        self.assertEqual(comparison["counts"], {axis: 1 for axis in subject.DIFFERENCE_AXES})
        for axis in subject.DIFFERENCE_AXES:
            self.assertEqual(comparison["axes"][axis][0]["left"], left["annotations"][0][axis])
            self.assertEqual(comparison["axes"][axis][0]["right"], right["annotations"][0][axis])

    def test_empty_eligible_subsets_stay_empty_and_arithmetic_is_independent(self):
        data = labels()
        for annotation in data["annotations"]:
            annotation["candidate_identity"] = "not_single"
            annotation["appearance"] = "flame_structure"
        unit_geometry = subject.validate_geometry(fixture_geometry())
        report = subject.reviewer_summary(data, unit_geometry)
        for image in report["images"]:
            for threshold in image["thresholds"]:
                self.assertEqual(threshold["counts"]["eligible"], 0)
                self.assertEqual(threshold["counts"]["unknown"], 0)
                self.assertEqual(threshold["counts"]["excluded"], image["sample_count"])
                flattened = [item for subset in threshold["subsets"].values() for item in subset]
                self.assertEqual(len(flattened), image["sample_count"])
                self.assertTrue(all(item["annotation"]["appearance"] == "flame_structure" for item in flattened))

    def test_preliminary_counts_preserved_with_conflicts(self):
        data = labels()
        for annotation in data["annotations"]:
            annotation["appearance"] = "non_evaluable"
        report = subject.reviewer_summary(data, subject.validate_geometry(fixture_geometry()))
        for image in report["images"]:
            middle = image["thresholds"][1]
            self.assertEqual(middle["preliminary_counts"]["eligible"], image["sample_count"])
            self.assertEqual(middle["counts"]["unknown"], image["sample_count"])
            self.assertEqual(middle["counts"]["eligible"], 0)

    def test_real_sources_readonly_with_synthetic_labels_and_deterministic_output(self):
        # Only protocol, geometry and JPEGs are read from preserved input locations.
        with tempfile.TemporaryDirectory(prefix="visibility-synthetic-") as directory:
            directory = Path(directory)
            left_path, right_path = directory / "synthetic-a.json", directory / "synthetic-b.json"
            left_data, right_data = labels(), labels("synthetic-b")
            right_data["annotations"][0]["appearance"] = "non_evaluable"
            left_path.write_text(json.dumps(left_data), encoding="utf-8")
            right_path.write_text(json.dumps(right_data), encoding="utf-8")
            first = subject.build_report([left_path, right_path])
            second = subject.build_report([left_path, right_path])
            out_a, out_b = directory / "output-a.json", directory / "output-b.json"
            subject.write_report(first, out_a)
            subject.write_report(second, out_b)
            self.assertEqual(out_a.read_bytes(), out_b.read_bytes())
            self.assertEqual(first["raw_label_sets"], [left_data, right_data])
            self.assertEqual(first["source_hashes"]["labels"][0]["sha256"],
                             subject.sha256_bytes(left_path.read_bytes()))
            self.assertEqual(first["source_hashes"]["code_sha256"],
                             subject.sha256_bytes(Path(subject.__file__).read_bytes()))
            self.assertEqual(first["source_hashes"]["geometry_sha256"], subject.GEOMETRY_SHA256)
            self.assertEqual(first["source_hashes"]["protocol_sha256"], subject.PROTOCOL_SHA256)
            for reviewer in first["reviewers"]:
                for image in reviewer["images"]:
                    for threshold in image["thresholds"]:
                        flattened = [r for items in threshold["subsets"].values() for r in items]
                        self.assertEqual({r["unit_id"] for r in flattened}, set(subject.SAMPLE[image["asset_id"]]))
                        for status, count in threshold["counts"].items():
                            self.assertEqual(count, sum(r["status"] == status for r in flattened))

    def test_output_refuses_overwrite_and_symlink(self):
        with tempfile.TemporaryDirectory(prefix="visibility-output-control-") as directory:
            path = Path(directory) / "existing.json"
            path.write_text("preserve me", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                subject.write_report({}, path)
            self.assertEqual(path.read_text(), "preserve me")
            link = Path(directory) / "link.json"
            link.symlink_to(path)
            with self.assertRaises(FileExistsError):
                subject.write_report({}, link)
            with patch("sys.stderr", new=io.StringIO()):
                self.assertEqual(subject.main(["--labels", "unread-real-labels.json", "--out", str(path)]), 2)
            self.assertEqual(path.read_text(), "preserve me")

    def test_bad_protocol_pin_before_label_read(self):
        with tempfile.TemporaryDirectory(prefix="visibility-pin-control-") as directory:
            protocol = Path(directory) / "PROTOCOL.md"
            protocol.write_text("Not the frozen protocol", encoding="utf-8")
            with self.assertRaisesRegex(subject.ValidationError, "protocol SHA-256 mismatch"):
                subject.build_report(["unread-real-labels.json"], protocol_path=protocol)

    def test_geometry_and_image_hash_mismatches(self):
        real_read = subject.read_json
        def changed_geometry(path):
            value, _ = real_read(path)
            return value, "0" * 64
        with patch.object(subject, "read_json", side_effect=changed_geometry):
            with self.assertRaisesRegex(subject.ValidationError, "geometry SHA-256 mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))
        real_hash = subject.sha256_bytes
        def changed_jpeg(data):
            return "0" * 64 if data[:2] == b"\xff\xd8" else real_hash(data)
        with patch.object(subject, "sha256_bytes", side_effect=changed_jpeg):
            with self.assertRaisesRegex(subject.ValidationError, "image SHA-256 mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))

    def test_full_source_jpeg_dimensions_independently_checked(self):
        with patch.object(subject.Image, "open") as fake_open:
            fake = fake_open.return_value.__enter__.return_value
            fake.format = "JPEG"
            fake.size = (1, 1)
            with self.assertRaisesRegex(subject.ValidationError, "full-source dimensions mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))

    def test_duplicate_reviewer_rejected(self):
        with tempfile.TemporaryDirectory(prefix="visibility-reviewer-control-") as directory:
            source = Path(directory) / "synthetic.json"
            source.write_text(json.dumps(labels()), encoding="utf-8")
            with self.assertRaisesRegex(subject.ValidationError, "duplicate reviewer identity"):
                subject.build_report([source, source])

    def test_modified_input_detected_after_initial_read(self):
        with tempfile.TemporaryDirectory(prefix="visibility-snapshot-control-") as directory:
            source = Path(directory) / "synthetic.json"
            source.write_text(json.dumps(labels()), encoding="utf-8")
            original_summary = subject.reviewer_summary
            def summary_and_change(data, geometry_data):
                result = original_summary(data, geometry_data)
                source.write_text(json.dumps(labels("changed-during-run")), encoding="utf-8")
                return result
            with patch.object(subject, "reviewer_summary", side_effect=summary_and_change):
                with self.assertRaisesRegex(subject.ValidationError, "input changed during summary: labels"):
                    subject.build_report([source])


if __name__ == "__main__":
    unittest.main(verbosity=2)
