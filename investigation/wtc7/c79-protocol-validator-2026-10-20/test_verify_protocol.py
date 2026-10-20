"""Synthetic controls for protocol checking, not finite-element tests."""

import contextlib
import copy
import io
import json
import unittest
from unittest.mock import patch

import verify_protocol as verifier


def set_value(protocol, route, value):
    target = protocol
    for key in route[:-1]:
        target = target[key]
    target[route[-1]] = value


class ProtocolControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = json.loads((verifier.DEFAULT_BUNDLE / "protocol.json").read_text())
        cls.readme = (verifier.DEFAULT_BUNDLE / "README.md").read_text()

    def test_original_replays_all_22_checks_and_three_pins(self):
        result = verifier.verify_bundle(verifier.DEFAULT_BUNDLE)
        self.assertTrue(result["all_passed"])
        self.assertEqual(result["design_check_count"], 22)
        self.assertEqual(len(result["frozen_file_hash_checks"]), 3)
        self.assertTrue(result["prior_record_check_names_match"])

    def test_one_targeted_negative_control_for_every_check(self):
        mutations = [
            ("complete_two_by_two_design", ["cases", 3, "plate"], "P0"),
            ("case_identifiers_unique", ["cases", 3, "id"], "P0_A0"),
            ("plate_at_A0_changes_only_declared_factor", ["contrasts", 0, "subtract"], ["P1_A1", "P0_A0"]),
            ("plate_at_A1_changes_only_declared_factor", ["contrasts", 1, "subtract"], ["P1_A1", "P0_A0"]),
            ("alpha_at_P0_changes_only_declared_factor", ["contrasts", 2, "subtract"], ["P1_A1", "P0_A0"]),
            ("alpha_at_P1_changes_only_declared_factor", ["contrasts", 3, "subtract"], ["P1_A1", "P0_A0"]),
            ("compound_changes_both_and_not_single_factor", ["compound_comparison", "isolates_single_factor"], True),
            ("interaction_is_difference_of_plate_contrasts", ["interaction", "subtract_contrasts"], ["plate_at_A0", "plate_at_A1"]),
            ("original_alpha_unknown_not_back_calculated", ["factors", "alpha", "A0_native_value"], 1.0),
            ("coefficient_scope_matches_named_four_beams", ["factors", "alpha", "scope_members"], ["G3005"]),
            ("coefficient_not_temperature_increase", ["factors", "alpha", "temperature_increase"], True),
            ("no_native_execution_claim", ["native_case_execution_count"], 1),
            ("historical_result_unknown", ["historical_prevention"], False),
            ("numerical_execution_details_explicitly_pending", ["numerical_execution_details", "output_sampling"], 0.1),
            ("all_source_pins_match_prior_records_and_readme", ["source_pins", 0, "sha256"], "0" * 64),
            ("UAF_page_crosswalk", ["source_pins", 0, "physical_pdf_pages"], [91, 92, 93, 94, 95]),
            ("NIST_page_crosswalk", ["source_pins", 2, "physical_pdf_pages"], [1]),
            ("public_only_sources", ["source_pins", 0, "url"], "http://example.invalid/"),
            ("preservation_and_scope_exclusions_present", ["exclusions"], []),
            ("nonphysical_contact_shortcut_distinguished", None, "nonphysical numerical diagnostic"),
            ("observable_support_loss_distinctions", None, "Define loss of seat contact separately from loss of all vertical support."),
            ("no_private_local_paths_in_public_payload", None, "/Users/synthetic-fixture/"),
        ]
        expected = {c["name"] for c in verifier.validate_protocol(self.protocol, self.readme)}
        self.assertEqual({name for name, _, _ in mutations}, expected)
        for name, route, value in mutations:
            with self.subTest(control=name):
                protocol, readme = copy.deepcopy(self.protocol), self.readme
                if route is not None:
                    set_value(protocol, route, value)
                elif name == "no_private_local_paths_in_public_payload":
                    readme += value
                else:
                    readme = readme.replace(value, "")
                checks = {c["name"]: c["passed"] for c in verifier.validate_protocol(protocol, readme)}
                self.assertFalse(checks[name])

    def test_unknown_is_not_false_zero_or_empty_string(self):
        for value in (False, 0, "", True):
            with self.subTest(value=repr(value)):
                protocol = copy.deepcopy(self.protocol)
                protocol["historical_prevention"] = value
                check = next(c for c in verifier.validate_protocol(protocol, self.readme)
                             if c["name"] == "historical_result_unknown")
                self.assertFalse(check["passed"])

    def test_missing_fields_do_not_create_a_pass_or_uncaught_error(self):
        for field in self.protocol:
            with self.subTest(field=field):
                if field not in {"cases", "contrasts", "factors", "source_pins", "historical_prevention", "exclusions"}:
                    continue
                protocol = copy.deepcopy(self.protocol)
                del protocol[field]
                self.assertTrue(any(not c["passed"] for c in verifier.validate_protocol(protocol, self.readme)))

    def test_deterministic_and_read_only(self):
        before = json.dumps(self.protocol, sort_keys=True)
        first = verifier.validate_protocol(self.protocol, self.readme)
        self.assertEqual(first, verifier.validate_protocol(self.protocol, self.readme))
        self.assertEqual(before, json.dumps(self.protocol, sort_keys=True))

    def test_malformed_input_fails_closed(self):
        self.assertFalse(any(c["passed"] for c in verifier.validate_protocol(None, None)))

    def test_cli_success_has_no_model_result(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = verifier.main(["--bundle", str(verifier.DEFAULT_BUNDLE)])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result["native_solver_runs"], 0)
        self.assertIsNone(result["historical_cause_assessment"])

    def test_cli_parse_failure_and_nonzero_exit(self):
        for error in (ValueError("synthetic parse failure"), OSError("synthetic read failure")):
            with self.subTest(error=type(error).__name__):
                output = io.StringIO()
                with patch.object(verifier, "verify_bundle", side_effect=error), contextlib.redirect_stdout(output):
                    code = verifier.main([])
                self.assertEqual(code, 1)
                self.assertFalse(json.loads(output.getvalue())["all_passed"])

    def test_cli_failed_check_is_nonzero(self):
        output = io.StringIO()
        with patch.object(verifier, "verify_bundle", return_value={"all_passed": False}), contextlib.redirect_stdout(output):
            self.assertEqual(verifier.main([]), 1)

    def test_changed_bytes_fail_even_when_design_checks_pass(self):
        original_read = verifier.Path.read_bytes

        def changed_read(path):
            body = original_read(path)
            return body + b"\n" if path.name == "README.md" else body

        with patch.object(verifier.Path, "read_bytes", changed_read):
            result = verifier.verify_bundle(verifier.DEFAULT_BUNDLE)
        self.assertTrue(all(c["passed"] for c in result["design_checks"]))
        self.assertFalse(result["all_passed"])
        self.assertFalse(result["frozen_file_hash_checks"][0]["matches_frozen_pin"])

    def test_actual_malformed_json_is_rejected_by_cli(self):
        original_read = verifier.Path.read_bytes

        def malformed_read(path):
            return b"{" if path.name == "protocol.json" else original_read(path)

        output = io.StringIO()
        with patch.object(verifier.Path, "read_bytes", malformed_read), contextlib.redirect_stdout(output):
            self.assertEqual(verifier.main([]), 1)
        self.assertEqual(json.loads(output.getvalue())["error_type"], "JSONDecodeError")


if __name__ == "__main__":
    unittest.main(verbosity=2)
