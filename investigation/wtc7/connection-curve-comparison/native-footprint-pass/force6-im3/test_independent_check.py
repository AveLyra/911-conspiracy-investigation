"""Synthetic adverse controls for the independent F6-Im3 checker only."""
import copy
import unittest
from unittest.mock import patch

from PIL import Image
import independent_check as checker


def empty_row(x):
    return {"x": x, "core": [], "fringe": [], "fragment_id": None,
            "fragment_membership": [], "status": "no_attributable_cells",
            "reason": "Synthetic inspected nonassignment; not a source reading.",
            "boundary_flags": [], "unassigned_band_refs": []}


def filled_row(x, core, fringe, identity="synthetic"):
    row = empty_row(x)
    row.update(core=core, fringe=fringe, fragment_id=identity,
               fragment_membership=[{"fragment_id": identity, "core": core, "fringe": fringe}],
               status="identified_local_fragment" if core else "fringe_only")
    return row


def fixture(pair="F6", role="primary"):
    box, context = checker.TARGETS[pair], checker.CONTEXTS[pair]
    return {"pair": pair, "region_id": pair+"-Im3", "source": "Im3.jpg", "reader": role,
            "target_box": box, "context_box": context, "human_accepted": False, "physical_support": None,
            "routes": {route: [empty_row(x) for x in range(box[0], box[2])] for route in ("solid", "dash")},
            "unassigned_bands": [], "coverage": {"full_context_inspected": True, "uncompleted_context": [],
                "raw_context_cells": (context[2]-context[0])*88,
                "raw_blocks": [{"columns": [context[0], context[2]-1], "receipt": "synthetic-only"}],
                "rows_covered": [0, 87], "actual_views": [{"path": "Im3.jpg"}, {"path": "page-076.png"}],
                "prior_knowledge": "Synthetic fixture, no historical claim.", "display_convention": "Exact-white omission."}}


class IndependentCheckerTests(unittest.TestCase):
    def test_internal_controls(self):
        self.assertEqual(len(checker.controls()), 8)

    def test_five_operations(self):
        self.assertEqual(checker.operations([0, 1, 87], [1, 2, 87]), {
            "intersection": [1, 87], "union": [0, 1, 2, 87], "primary_only": [0],
            "peer_only": [2], "symmetric_difference": [0, 2]})

    def test_geometry_and_source_corruption(self):
        image = Image.new("RGB", checker.SIZE, (255, 255, 255))
        image.putpixel((1, 0), (254, 255, 255))
        rows = [{"x": 0, "y": 0, "rgb": [255, 255, 255]}, {"x": 1, "y": 0, "rgb": [254, 255, 255]}]
        checker.context_records(rows, [0, 0, 2, 1], image)
        for bad in (rows[::-1], rows[:-1], [rows[0], rows[0]], [rows[0], dict(rows[1], rgb=[255, 255, 255])]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checker.context_records(bad, [0, 0, 2, 1], image)
        for image in (Image.new("RGB", (745, 88)), Image.new("RGB", (741, 92)), Image.new("L", checker.SIZE)):
            with self.assertRaises(ValueError):
                checker.validate_image(image)

    def test_exact_old_source_overlap(self):
        new = [{"x": x, "y": y, "rgb": [254, 255, 255]} for y in range(88) for x in range(143, 442)]
        old = [{"x": x, "y": y, "rgb": [254, 255, 255]} for y in range(88) for x in range(308, 427)]
        self.assertEqual(checker.check_overlap(new, old), 10472)
        altered = copy.deepcopy(old)
        altered[500]["rgb"][0] = 253
        for bad in (old[:-1], old[::-1], altered):
            with self.assertRaises(ValueError):
                checker.check_overlap(new, bad)
        with self.assertRaises(ValueError):
            checker.check_overlap(new+[new[0]], old)

    def test_full_annotation_coverage(self):
        data = fixture()
        checker.validate_annotation(data, "F6", "primary")
        for change in (lambda d: d["routes"]["solid"].pop(),
                       lambda d: d.update(reader="force56_peer"),
                       lambda d: d["coverage"]["raw_blocks"][0].update(columns=[144, 441]),
                       lambda d: d["coverage"]["raw_blocks"][0].update(truncated=True),
                       lambda d: d["coverage"].update(full_context_inspected=False),
                       lambda d: d["coverage"].update(rows_covered=[1, 87]),
                       lambda d: d["coverage"].update(counterpart_new_annotation_read=True)):
            bad = copy.deepcopy(data)
            change(bad)
            with self.assertRaises(ValueError):
                checker.validate_annotation(bad, "F6", "primary")
        old = fixture("F5", "force56_peer")
        checker.validate_annotation(old, "F5", "peer")
        with self.assertRaises(ValueError):
            checker.validate_annotation(old, "F5", "primary")

    def test_fields_classes_membership_and_boundary_corruptions(self):
        row = filled_row(145, [0, 3], [4])
        row["boundary_flags"] = ["target_left", "target_top"]
        checker.validate_entry(row, checker.TARGETS["F6"])
        for change in (lambda d: d.update(core=[False, 3]), lambda d: d.update(core=[0, 0, 3]),
                       lambda d: d.update(fringe=[0]), lambda d: d.update(fragment_membership=[]),
                       lambda d: d.update(boundary_flags=[]), lambda d: d.update(reason=""),
                       lambda d: d.update(status="no_attributable_cells"), lambda d: d.update(extra_field=True)):
            bad = copy.deepcopy(row)
            change(bad)
            with self.assertRaises(ValueError):
                checker.validate_entry(bad, checker.TARGETS["F6"])

    def test_multiple_bands_and_reciprocity(self):
        data = fixture()
        for route, y in (("solid", 60), ("dash", 62)):
            band = filled_row(311, [y], [], route)
            band.update(band_id=route, candidate_routes=[route])
            data["unassigned_bands"].append(band)
            data["routes"][route][311-145].update(status="identity_conflict", unassigned_band_refs=[route])
        self.assertEqual(len(checker.validate_annotation(data, "F6", "primary")[311]), 2)
        for change in (lambda d: d["unassigned_bands"][0].update(candidate_routes=["dash"]),
                       lambda d: d["routes"]["solid"][166].update(unassigned_band_refs=["missing"]),
                       lambda d: d["routes"]["solid"].__setitem__(166, filled_row(311, [60], []))):
            bad = copy.deepcopy(data)
            change(bad)
            with self.assertRaises(ValueError):
                checker.validate_annotation(bad, "F6", "primary")

    def test_exact_legacy_band_metadata_types_and_preservation(self):
        data = fixture("F5")
        band = filled_row(311, [60], [], "legacy")
        band.update(band_id="legacy", candidate_routes=["solid"], other_possible_origins=["synthetic alternative"], continuity_claim=False)
        data["unassigned_bands"] = [band]
        data["routes"]["solid"][1].update(status="identity_conflict", unassigned_band_refs=["legacy"])
        before = copy.deepcopy(data)
        checked = checker.validate_annotation(data, "F5", "primary")
        self.assertEqual(data, before)
        self.assertEqual(checked[311][0], before["unassigned_bands"][0])
        for change in (lambda d: d.update(other_possible_origins="not a list"),
                       lambda d: d.update(other_possible_origins=[False]), lambda d: d.update(other_possible_origins=[""]),
                       lambda d: d.update(continuity_claim=0), lambda d: d.update(continuity_claim=True),
                       lambda d: d.update(unknown_metadata="not allowed")):
            bad = copy.deepcopy(band)
            change(bad)
            with self.assertRaises(ValueError):
                checker.validate_entry(bad, checker.TARGETS["F5"], band=True, legacy_band_metadata=True)
        with self.assertRaises(ValueError):
            checker.validate_entry(band, checker.TARGETS["F6"], band=True)

    def test_fixed_primary_optional_band_refs_and_required_route_refs(self):
        data = fixture()
        band = filled_row(311, [60], [], "fixed-primary")
        band.update(band_id="fixed-primary", candidate_routes=["solid"])
        del band["unassigned_band_refs"]
        data["unassigned_bands"] = [band]
        data["routes"]["solid"][311-145].update(status="identity_conflict", unassigned_band_refs=["fixed-primary"])
        before = copy.deepcopy(data)
        checker.validate_annotation(data, "F6", "primary")
        self.assertEqual(data, before)
        self.assertNotIn("unassigned_band_refs", data["unassigned_bands"][0])
        explicit = copy.deepcopy(data)
        explicit["unassigned_bands"][0]["unassigned_band_refs"] = []
        checker.validate_annotation(explicit, "F6", "primary")
        for change in (lambda d: d.update(reader="peer"),
                       lambda d: d["routes"]["solid"][166].pop("unassigned_band_refs"),
                       lambda d: d["routes"]["solid"][166].update(unassigned_band_refs=[]),
                       lambda d: d["unassigned_bands"][0].update(unassigned_band_refs=["other-band"]),
                       lambda d: d["unassigned_bands"][0].update(unassigned_band_refs=False),
                       lambda d: d["unassigned_bands"][0].update(unknown_field=False)):
            bad = copy.deepcopy(data)
            change(bad)
            with self.assertRaises((ValueError, KeyError)):
                checker.validate_annotation(bad, "F6", "peer" if bad["reader"] == "peer" else "primary")

    def test_coverage_aliases_agree_and_require_exact_integer_rows(self):
        data = fixture()
        del data["coverage"]["rows_covered"]
        for alias in ("rows", "rows_covered", "rows_inspected"):
            one = copy.deepcopy(data)
            one["coverage"][alias] = [0, 87]
            checker.coverage(one, "F6")
        complete = copy.deepcopy(data)
        complete["coverage"].update(rows=[0, 87], rows_covered=[0, 87], rows_inspected=[0, 87])
        checker.coverage(complete, "F6")
        for bad_rows in ([False, 87], [0, 87.0], [0, 86], [1, 87], [], None):
            bad = copy.deepcopy(complete)
            bad["coverage"]["rows"] = bad_rows
            with self.assertRaises(ValueError):
                checker.coverage(bad, "F6")
        with self.assertRaises(ValueError):
            checker.coverage(data, "F6")

    def test_exact_charter_path_exception_and_copy_equality(self):
        self.assertEqual(checker.name(checker.WORKTREE_CHARTER), "../../../CHARTER.md")
        self.assertIn(checker.MAIN_CHARTER, checker.AUTHORITY_CONTEXT)
        with self.assertRaises(ValueError):
            checker.name(checker.WORKTREE_CHARTER.parent / "unapproved-charter-copy.md")
        with patch.object(checker, "add_pin") as pin_mock, patch.object(checker.Path, "read_bytes", side_effect=[b"same", b"same"]):
            checker.check_charter_copies({})
            self.assertEqual(pin_mock.call_count, 2)
        with patch.object(checker, "add_pin"), patch.object(checker.Path, "read_bytes", side_effect=[b"main", b"different"]):
            with self.assertRaises(ValueError):
                checker.check_charter_copies({})

    def test_cross_pair_all_scopes_and_class_directions(self):
        new, old = fixture(), fixture("F5")
        new["routes"]["solid"][320-145] = filled_row(320, [5, 6], [7, 8])
        old["routes"]["dash"][320-310] = filled_row(320, [5, 7], [6, 8])
        expected = {"core_core": [[320, 5]], "core_fringe": [[320, 6]], "fringe_core": [[320, 7]],
                    "fringe_fringe": [[320, 8]], "outer": [[320, 5], [320, 6], [320, 7], [320, 8]]}
        result = checker.cross_intersections(new, old)
        self.assertEqual(len(result), 9)
        self.assertEqual(result[1], {"f6_scope": "solid", "f5_scope": "dash", "cells": expected})
        self.assertTrue(all(not cells for index, item in enumerate(result) if index != 1 for cells in item["cells"].values()))
        pairings = checker.cross_pair_comparisons({role: new for role in checker.ROLES}, {role: old for role in checker.ROLES})
        self.assertEqual([(p["f6_reader"], p["f5_reader"]) for p in pairings],
                         [("primary", "primary"), ("primary", "peer"), ("peer", "primary"), ("peer", "peer")])
        self.assertTrue(all(p["intersections"][1]["cells"] == expected for p in pairings))

    def test_dependency_omission_pin_types_aliases(self):
        required = {"synthetic.json": {"bytes": 10, "sha256": "0"*64}}
        checker.require_dependency_coverage(required, required)
        for bad in ({}, {"synthetic.json": {"bytes": True, "sha256": "0"*64}},
                    {"synthetic.json": {"bytes": 11, "sha256": "0"*64}},
                    required | {"other/../synthetic.json": {"bytes": 11, "sha256": "0"*64}}):
            with self.assertRaises(ValueError):
                checker.require_dependency_coverage(bad, required)

    def test_recursive_dependency_union_and_changed_pin(self):
        names = ("synthetic-root.json", "reader-synthetic.json", "reader-synthetic.py", "synthetic-leaf.txt")
        pins = {name: {"bytes": index+1, "sha256": str(index)*64} for index, name in enumerate(names)}
        documents = {
            "synthetic-root.json": {"inputs": {"reader-synthetic.json": pins["reader-synthetic.json"]}},
            "reader-synthetic.json": {"inputs": {"synthetic-leaf.txt": pins["synthetic-leaf.txt"]},
                                      "script_pin": pins["reader-synthetic.py"]},
        }
        def mocked_pin(path):
            return pins[path.name]
        def mocked_load(path):
            return documents[path.name]
        with patch.object(checker, "pin", mocked_pin), patch.object(checker, "load", mocked_load):
            result = {}
            checker.dependency_closure([checker.HERE / "synthetic-root.json"], result)
            self.assertEqual(result, pins)
            for missing in names:
                incomplete = {name: value for name, value in result.items() if name != missing}
                with self.assertRaises(ValueError):
                    checker.require_dependency_coverage(incomplete, result)
            documents["reader-synthetic.json"]["inputs"]["synthetic-leaf.txt"] = {"bytes": 99, "sha256": "3"*64}
            with self.assertRaises(ValueError):
                checker.dependency_closure([checker.HERE / "synthetic-root.json"], {})

    def test_unassigned_scope_preserves_multiple_pieces(self):
        new, old = fixture(), fixture("F5")
        new["unassigned_bands"] = [filled_row(320, [2], [3], "a"), filled_row(320, [5], [6], "b")]
        old["unassigned_bands"] = [filled_row(320, [2, 6], [3, 5], "c")]
        result = checker.cross_intersections(new, old)[8]
        self.assertEqual(result, {"f6_scope": "unassigned", "f5_scope": "unassigned", "cells": {
            "core_core": [[320, 2]], "core_fringe": [[320, 5]], "fringe_core": [[320, 6]],
            "fringe_fringe": [[320, 3]], "outer": [[320, 2], [320, 3], [320, 5], [320, 6]]}})

    def test_exact_white_and_near_white(self):
        data, image = fixture(), Image.new("RGB", checker.SIZE, (255, 255, 255))
        data["routes"]["solid"][320-145] = filled_row(320, [5], [])
        self.assertEqual(checker.selected_white(data, image), [{"scope": "solid", "class": "core", "x": 320, "y": 5}])
        image.putpixel((320, 5), (254, 255, 255))
        self.assertEqual(checker.selected_white(data, image), [])

    def test_comparison_corruptions(self):
        readers = {role: fixture("F6", role) for role in checker.ROLES}
        old = {role: fixture("F5", role) for role in checker.ROLES}
        bands = {role: checker.validate_annotation(data, "F6", role) for role, data in readers.items()}
        expected = checker.expected_comparison(readers, old, bands, Image.new("RGB", checker.SIZE))
        output = dict(copy.deepcopy(expected), status="native_ink_reconciliation_not_physical_measurement", pair="F6", region_id="F6-Im3",
                      input_pins={}, dependencies={}, script_pin={}, test_pin={}, human_accepted=False,
                      physical_support=None, limits="Synthetic", literal_reproductions={"primary": True, "peer": True},
                      exact_old_context_overlap_cells=10472)
        checker.check_comparison(output, expected)
        for change in (lambda d: d["route_comparisons"][0]["sets"]["core"].update(union=[1]),
                       lambda d: d["visible_ink_comparisons"][0].update(primary_unassigned_originals=[{}]),
                       lambda d: d["cross_pair_comparisons"][0]["intersections"][0]["cells"].update(outer=[[310, 0]]),
                       lambda d: d["summary"].update(status_different=1), lambda d: d.update(prior_F5_readings={}),
                       lambda d: d.update(exact_old_context_overlap_cells=10471), lambda d: d.update(human_accepted=True)):
            bad = copy.deepcopy(output)
            change(bad)
            with self.assertRaises(ValueError):
                checker.check_comparison(bad, expected)


if __name__ == "__main__":
    unittest.main()
