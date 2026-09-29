"""Synthetic schema/comparison controls; no real annotation files are opened."""

import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import summarize as subject


def pins():
    return {asset_id: {"asset_id": asset_id, "path": f"assets/run-01/images/{asset_id}.jpg",
                      "sha256": "a" * 64, "dimensions": [100, 100], "bytes": 10}
            for asset_id in subject.SAMPLE}


def feature(appearance="flame_like", rect=None):
    return {"rect": rect or [10, 10, 30, 30], "appearance": appearance,
            "target_relation": "on_candidate_facade", "reason": "Synthetic irregular luminous detail.",
            "alternatives": ["Illuminated material or reflected light cannot be excluded."]}


def nondetection():
    return {"rect": [20, 20, 40, 40],
            "reason": "No flame form identified on the visible surface; opaque glazing limits interior opportunity."}


def record(reviewer="synthetic-a", source_pins=None):
    source_pins = source_pins or pins()
    return {"reviewer": reviewer, "independence": "Synthetic data; no historical labels read.",
            "protocol_sha256": subject.PROTOCOL_SHA256,
            "provenance_key_sha256": subject.PROVENANCE_KEY_SHA256,
            "assets": [
                {"asset_id": asset_id, "image_sha256": source_pins[asset_id]["sha256"],
                 "dimensions": copy.deepcopy(source_pins[asset_id]["dimensions"]),
                 "complete_native_image_inspected": True,
                 "target_rect": [0, 0, 100, 100], "target_evaluability": "partial_detail",
                 "target_reason": "Synthetic candidate frontage with localized visible detail.",
                 "luminous_features": [],
                 "smoke": {"status": "not_identified", "regions": [],
                           "reason": "No smoke feature identified in this synthetic example."},
                 "nondetection_regions": [],
                 "visibility_limits": ["Synthetic source provides no verified interior view."],
                 "overlay_regions": []}
                for asset_id in subject.SAMPLE]}


def provenance_key():
    entries = [{"asset_id": asset_id, "native_pdf_dimensions": pin["dimensions"],
                "extracted_view": {**pin, "format": "JPEG"}}
               for asset_id, pin in pins().items()]
    entries.extend({"asset_id": f"unselected-{index}"} for index in range(15))
    return {"assets": entries}


class RuleControls(unittest.TestCase):
    def test_01_smoke_and_qualified_nondetection_coexist(self):
        data = record()
        asset = data["assets"][0]
        asset["smoke"] = {"status": "visible", "regions": [[0, 0, 60, 60]],
                          "reason": "A veil overlaps the facade; emitting source remains unresolved."}
        asset["nondetection_regions"] = [nondetection()]
        subject.validate_labels(data, pins())
        axes = subject.axis_values(asset)
        self.assertEqual(axes["smoke_status"], "visible")
        self.assertTrue(axes["nondetection_region_identified"])
        self.assertFalse(axes["flame_like_identified"])
        self.assertNotIn("conflict", json.dumps(axes))

    def test_02_unresolved_target_preserved_without_absence_inference(self):
        data = record()
        data["assets"][0].update(target_evaluability="unresolved_target", target_rect=None,
                                 target_reason="Candidate cannot be securely localized behind foreground.")
        subject.validate_labels(data, pins())
        axes = subject.axis_values(data["assets"][0])
        self.assertEqual(axes["target_evaluability"], "unresolved_target")
        self.assertFalse(axes["flame_like_identified"])
        self.assertEqual(set(axes), {"target_evaluability", "flame_like_identified",
                                    "ambiguous_glow_identified", "smoke_status",
                                    "nondetection_region_identified"})

    def test_03_smooth_glow_remains_distinct_from_flame_like(self):
        data = record()
        data["assets"][0]["luminous_features"] = [feature("ambiguous_glow")]
        subject.validate_labels(data, pins())
        axes = subject.axis_values(data["assets"][0])
        self.assertTrue(axes["ambiguous_glow_identified"])
        self.assertFalse(axes["flame_like_identified"])
        self.assertNotIn("temperature", axes)

    def test_04_printed_numeral_remains_overlay(self):
        data = record()
        data["assets"][0]["overlay_regions"] = [[5, 5, 15, 15]]
        subject.validate_labels(data, pins())
        axes = subject.axis_values(data["assets"][0])
        self.assertFalse(axes["flame_like_identified"])
        self.assertFalse(axes["ambiguous_glow_identified"])

    def test_05_overlapping_boxes_no_area_or_physical_counts(self):
        left, right = record(), record("synthetic-b")
        left["assets"][0]["luminous_features"] = [feature(), feature(rect=[15, 15, 35, 35])]
        right["assets"][0]["luminous_features"] = [feature(rect=[10, 10, 35, 35])]
        subject.validate_labels(left, pins())
        subject.validate_labels(right, pins())
        comparison = subject.compare_records([left, right])[0]["assets"][0]
        self.assertEqual(comparison["axes"]["flame_like_identified"]["comparison"], "same")
        self.assertFalse(comparison["regions_without_forced_matching"]["luminous_features"]["identical_json"])
        self.assertEqual(comparison["regions_without_forced_matching"]["luminous_features"]["left"],
                         left["assets"][0]["luminous_features"])
        serialized = json.dumps(comparison)
        for forbidden in ("area_total", "fire_count", "window_count", "percentage", "extent_score"):
            self.assertNotIn(forbidden, serialized)

    def test_06_repeated_source_bytes_do_not_become_corroboration(self):
        # All synthetic image pins deliberately share a digest; IDs stay separate.
        data = record()
        subject.validate_labels(data, pins())
        comparisons = subject.compare_records([data, record("synthetic-b")])[0]["assets"]
        self.assertEqual([item["asset_id"] for item in comparisons], list(subject.SAMPLE))
        self.assertNotIn("independent_corroboration", json.dumps(comparisons))
        self.assertNotIn("event_count", json.dumps(comparisons))

    def test_all_observation_axes_may_coexist(self):
        data = record()
        asset = data["assets"][0]
        asset["luminous_features"] = [feature(), feature("ambiguous_glow")]
        asset["smoke"] = {"status": "visible", "regions": [[0, 0, 50, 50]], "reason": "Synthetic veil."}
        asset["nondetection_regions"] = [nondetection()]
        subject.validate_labels(data, pins())
        axes = subject.axis_values(asset)
        self.assertTrue(axes["flame_like_identified"])
        self.assertTrue(axes["ambiguous_glow_identified"])
        self.assertTrue(axes["nondetection_region_identified"])
        self.assertEqual(axes["smoke_status"], "visible")


class SchemaControls(unittest.TestCase):
    def reject(self, data):
        with self.assertRaises(subject.ValidationError):
            subject.validate_labels(data, pins())

    def test_exact_13_unique_sample_assets(self):
        self.assertIsNotNone(subject.validate_labels(record(), pins()))
        mutations = [lambda d: d["assets"].pop(),
                     lambda d: d["assets"].append(copy.deepcopy(d["assets"][0])),
                     lambda d: d["assets"][0].update(asset_id="unknown")]
        for mutate in mutations:
            data = record()
            mutate(data)
            self.reject(data)

    def test_required_top_and_exact_asset_fields(self):
        for field in subject.TOP_FIELDS:
            data = record()
            del data[field]
            self.reject(data)
        for field in subject.ASSET_FIELDS:
            data = record()
            del data["assets"][0][field]
            self.reject(data)
        data = record()
        data["assets"][0]["invented_score"] = 1
        self.reject(data)

    def test_independence_string_and_object_without_coercion(self):
        data = record()
        metadata = {"previous_labels_seen": False, "limits": ["Synthetic only"]}
        data["independence"] = metadata
        self.assertIs(subject.validate_labels(data, pins())["independence"], metadata)
        for value in (None, True, 1, [], {}, " ", {"nonfinite": float("nan")}):
            data["independence"] = value
            self.reject(data)

    def test_nonempty_strings_and_lists(self):
        for field, value in [("target_reason", " "), ("target_reason", None),
                             ("visibility_limits", []), ("visibility_limits", "glazing"),
                             ("visibility_limits", [""]), ("visibility_limits", [False])]:
            data = record()
            data["assets"][0][field] = value
            self.reject(data)
        for field in ("reason", "alternatives"):
            for value in (None, "", [], [""]):
                data = record()
                item = feature()
                item[field] = value
                data["assets"][0]["luminous_features"] = [item]
                self.reject(data)

    def test_record_hashes_and_positive_integer_dimensions(self):
        for field in ("protocol_sha256", "provenance_key_sha256"):
            data = record()
            data[field] = "0" * 64
            self.reject(data)
        for field, value in [("image_sha256", "0" * 64), ("dimensions", [99, 100]),
                             ("dimensions", [True, 100]), ("dimensions", [100.0, 100]),
                             ("dimensions", [0, 100]), ("dimensions", [-1, 100]),
                             ("dimensions", [100]), ("dimensions", [100, float("inf")]),
                             ("complete_native_image_inspected", False),
                             ("complete_native_image_inspected", 1)]:
            data = record()
            data["assets"][0][field] = value
            self.reject(data)

    def test_rectangles_every_locator_path(self):
        invalid_rects = [[0, 0, 0, 1], [2, 1, 1, 2], [-1, 0, 1, 1], [0, 0, 101, 100],
                         [0, 0, 100, 101], [False, 0, 1, 1], [0, 0, True, 1],
                         [0, 0, float("nan"), 1], [0, 0, float("inf"), 1],
                         [0, 0, 10 ** 1000, 1], [0, 0, 1], None, "0,0,1,1"]
        for rect in invalid_rects:
            for locator in ("target", "luminous", "smoke", "nondetection", "overlay"):
                with self.subTest(locator=locator, rect=repr(rect)[:50]):
                    data = record()
                    asset = data["assets"][0]
                    if locator == "target":
                        asset["target_rect"] = rect
                    elif locator == "luminous":
                        item = feature()
                        item["rect"] = rect
                        asset["luminous_features"] = [item]
                    elif locator == "smoke":
                        asset["smoke"].update(status="visible", regions=[rect])
                    elif locator == "nondetection":
                        asset["nondetection_regions"] = [{"rect": rect, "reason": "Limited synthetic opportunity."}]
                    else:
                        asset["overlay_regions"] = [rect]
                    self.reject(data)

    def test_native_edge_and_fractional_rectangles_valid(self):
        data = record()
        data["assets"][0]["target_rect"] = [0, 0, 100, 100]
        data["assets"][0]["overlay_regions"] = [[0.25, 0.5, 1.25, 1.5]]
        subject.validate_labels(data, pins())

    def test_target_null_consistency_and_enums(self):
        for status, rect in [("unresolved_target", [0, 0, 100, 100]),
                             ("partial_detail", None), ("limited_detail", None),
                             ("clear", [0, 0, 100, 100]), ([], None)]:
            data = record()
            data["assets"][0].update(target_evaluability=status, target_rect=rect)
            self.reject(data)
        for field, value in [("appearance", "fire"), ("appearance", []),
                             ("target_relation", "verified_building"), ("target_relation", None)]:
            data = record()
            item = feature()
            item[field] = value
            data["assets"][0]["luminous_features"] = [item]
            self.reject(data)

    def test_smoke_consistency_and_reason(self):
        for smoke in [
            {"status": "visible", "regions": [], "reason": "Veil."},
            {"status": "not_identified", "regions": [[0, 0, 10, 10]], "reason": "None."},
            {"status": "no_smoke", "regions": [], "reason": "None."},
            {"status": "uncertain", "regions": [], "reason": " "},
            {"status": "uncertain", "regions": []},
        ]:
            data = record()
            data["assets"][0]["smoke"] = smoke
            self.reject(data)
        for regions in ([], [[0, 0, 10, 10]]):
            data = record()
            data["assets"][0]["smoke"].update(status="uncertain", regions=regions)
            subject.validate_labels(data, pins())

    def test_exact_feature_and_nondetection_structure(self):
        for field, value in [("luminous_features", {}), ("luminous_features", ["bright"]),
                             ("nondetection_regions", "none"),
                             ("nondetection_regions", [{"rect": [0, 0, 1, 1]}]),
                             ("nondetection_regions", [{"rect": [0, 0, 1, 1], "reason": ""}])]:
            data = record()
            data["assets"][0][field] = value
            self.reject(data)
        for field in subject.LUMINOUS_FIELDS:
            data = record()
            item = feature()
            del item[field]
            data["assets"][0]["luminous_features"] = [item]
            self.reject(data)

    def test_duplicate_json_keys_and_nonfinite_metadata(self):
        for raw in ('{"x": 1, "x": 2}', '{"a": {"x": 1, "x": 2}}',
                    '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', '{"x": [1e999]}'):
            with self.assertRaises(subject.ValidationError):
                subject.decode_json(raw)

    def test_provenance_pins_membership_and_structure(self):
        self.assertEqual(set(subject.extract_pins(provenance_key())), set(subject.SAMPLE))
        mutations = [
            lambda k: k["assets"].pop(),
            lambda k: k["assets"][0].update(asset_id="not-sample"),
            lambda k: k["assets"][1].update(asset_id=k["assets"][0]["asset_id"]),
            lambda k: k["assets"][0]["extracted_view"].update(path="../bad.jpg"),
            lambda k: k["assets"][0]["extracted_view"].update(sha256="bad"),
            lambda k: k["assets"][0]["extracted_view"].update(dimensions=[True, 100]),
            lambda k: k["assets"][0].update(native_pdf_dimensions=[99, 100]),
            lambda k: k["assets"][0]["extracted_view"].update(format="PNG"),
            lambda k: k["assets"][0]["extracted_view"].update(bytes=True),
        ]
        for mutation in mutations:
            key = provenance_key()
            mutation(key)
            with self.assertRaises(subject.ValidationError):
                subject.extract_pins(key)


class OutputControls(unittest.TestCase):
    def test_all_five_axes_reported_independently(self):
        left, right = record(), record("synthetic-b")
        right["assets"][0].update(target_evaluability="limited_detail",
                                  luminous_features=[feature(), feature("ambiguous_glow")],
                                  nondetection_regions=[nondetection()])
        right["assets"][0]["smoke"].update(status="visible", regions=[[0, 0, 50, 50]])
        comparison = subject.compare_records([left, right])[0]["assets"][0]
        self.assertEqual(len(comparison["axes"]), 5)
        self.assertTrue(all(axis["comparison"] == "different" for axis in comparison["axes"].values()))
        self.assertEqual(comparison["regions_without_forced_matching"]["nondetection_regions"]["right"],
                         right["assets"][0]["nondetection_regions"])

    def test_input_order_does_not_create_asset_mismatches(self):
        left, right = record(), record("synthetic-b")
        right["assets"].reverse()
        compared = subject.compare_records([left, right])[0]["assets"]
        self.assertEqual([asset["asset_id"] for asset in compared], list(subject.SAMPLE))
        self.assertTrue(all(axis["comparison"] == "same" for asset in compared for axis in asset["axes"].values()))

    def test_full_readonly_source_pins_and_deterministic_synthetic_reports(self):
        source_pins, sources = subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))
        self.assertEqual(len(sources["images"]), 13)
        self.assertEqual(set(source_pins), set(subject.SAMPLE))
        with tempfile.TemporaryDirectory(prefix="coverage-synthetic-") as directory:
            directory = Path(directory)
            paths = [directory / "synthetic-a.json", directory / "synthetic-b.json"]
            inputs = [record("synthetic-a", source_pins), record("synthetic-b", source_pins)]
            inputs[1]["assets"][0]["luminous_features"] = [feature("ambiguous_glow")]
            for path, data in zip(paths, inputs):
                path.write_text(json.dumps(data), encoding="utf-8")
            first, second = subject.build_report(paths), subject.build_report(paths)
            outputs = [directory / "one.json", directory / "two.json"]
            for report, path in zip((first, second), outputs):
                subject.write_report(report, path)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            self.assertEqual(first["raw_records"], inputs)
            self.assertEqual(first["source_hashes"]["code_sha256"], subject.sha256_bytes(Path(subject.__file__).read_bytes()))
            self.assertEqual(first["source_hashes"]["labels"][0]["sha256"], subject.sha256_bytes(paths[0].read_bytes()))
            self.assertEqual(first["source_hashes"]["protocol_sha256"], subject.PROTOCOL_SHA256)
            self.assertEqual(first["source_hashes"]["provenance_key_sha256"], subject.PROVENANCE_KEY_SHA256)
            # Independent expected change: one image differs on ambiguous glow only.
            for index, comparison in enumerate(first["comparisons"][0]["assets"]):
                for axis_name, axis in comparison["axes"].items():
                    expected = "different" if index == 0 and axis_name == "ambiguous_glow_identified" else "same"
                    self.assertEqual(axis["comparison"], expected)

    def test_source_pins_and_jpeg_header_failures(self):
        protocol = Path(subject.__file__).with_name("PROTOCOL.md")
        original_read = subject.read_json
        def wrong_key(path):
            data, _ = original_read(path)
            return data, "0" * 64
        with patch.object(subject, "read_json", side_effect=wrong_key):
            with self.assertRaisesRegex(subject.ValidationError, "provenance key SHA-256 mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, protocol)
        original_hash = subject.sha256_bytes
        def wrong_jpeg(data):
            return "0" * 64 if data[:2] == b"\xff\xd8" else original_hash(data)
        with patch.object(subject, "sha256_bytes", side_effect=wrong_jpeg):
            with self.assertRaisesRegex(subject.ValidationError, "image SHA-256 mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, protocol)
        with patch.object(subject.Image, "open") as fake_open:
            image = fake_open.return_value.__enter__.return_value
            image.format, image.size = "JPEG", (1, 1)
            with self.assertRaisesRegex(subject.ValidationError, "full-source dimensions mismatch"):
                subject.verify_sources(subject.SOURCE_DIR, protocol)

    def test_no_pixel_decoding_or_image_writes(self):
        with patch.object(subject.Image.Image, "load", side_effect=AssertionError("pixel decode forbidden")), \
             patch.object(subject.Image.Image, "save", side_effect=AssertionError("image save forbidden")):
            source_pins, _ = subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))
            self.assertEqual(len(source_pins), 13)

    def test_wrong_protocol_stops_before_annotation_reads(self):
        with tempfile.TemporaryDirectory(prefix="coverage-protocol-") as directory:
            protocol = Path(directory) / "PROTOCOL.md"
            protocol.write_text("wrong protocol", encoding="utf-8")
            with self.assertRaisesRegex(subject.ValidationError, "protocol SHA-256 mismatch"):
                subject.build_report(["unread-real-a.json", "unread-real-b.json"], protocol_path=protocol)

    def test_no_overwrite_existing_or_symlink_or_failed_attempt(self):
        with tempfile.TemporaryDirectory(prefix="coverage-existing-") as directory:
            output = Path(directory) / "old.json"
            output.write_text("preserve failed attempt", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                subject.write_report({}, output)
            symlink = Path(directory) / "link.json"
            symlink.symlink_to(output)
            with self.assertRaises(FileExistsError):
                subject.write_report({}, symlink)
            dangling = Path(directory) / "dangling.json"
            dangling.symlink_to(Path(directory) / "absent.json")
            with self.assertRaises(FileExistsError):
                subject.write_report({}, dangling)
            with patch("sys.stderr", new=io.StringIO()):
                self.assertEqual(subject.main(["--labels", "unread-a.json", "unread-b.json", "--out", str(output)]), 2)
            self.assertEqual(output.read_text(), "preserve failed attempt")

    def test_duplicate_reviewers_and_input_changes_rejected(self):
        source_pins, _ = subject.verify_sources(subject.SOURCE_DIR, Path(subject.__file__).with_name("PROTOCOL.md"))
        with tempfile.TemporaryDirectory(prefix="coverage-snapshot-") as directory:
            paths = [Path(directory) / "synthetic-a.json", Path(directory) / "synthetic-b.json"]
            for path, reviewer in zip(paths, ("synthetic-a", "synthetic-b")):
                path.write_text(json.dumps(record(reviewer, source_pins)), encoding="utf-8")
            with self.assertRaisesRegex(subject.ValidationError, "duplicate reviewer identity"):
                subject.build_report([paths[0], paths[0]])
            original_compare = subject.compare_records
            def compare_then_modify(inputs):
                result = original_compare(inputs)
                paths[0].write_text(json.dumps(record("modified", source_pins)), encoding="utf-8")
                return result
            with patch.object(subject, "compare_records", side_effect=compare_then_modify):
                with self.assertRaisesRegex(subject.ValidationError, "input changed during comparison: observation record"):
                    subject.build_report(paths)


if __name__ == "__main__":
    unittest.main(verbosity=2)
