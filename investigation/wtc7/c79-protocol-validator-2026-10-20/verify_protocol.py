"""Read-only replay of the 22 recorded Column 79 protocol checks.

Standard library only. Does not fetch sources, edit the protocol or run a solver.
Usage: python3 -B verify_protocol.py [--bundle ../c79-factorial-protocol-2026-10-19]
"""

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path


BUNDLE_PINS = {
    "README.md": "f45e11d9a87adba5fe72fc34dec4e81840e3fd092288414d73b9cbe66c19c0fc",
    "protocol.json": "90180e549dffc51da0d6a877328576f764ff54a2877416011ab7afeed65d0060",
    "verification.json": "61a0e80788585d6c334a2dad3929a27350cee69d22a0b293ae9ab3b57bfec7d4",
}
SOURCE_PINS = {
    "uaf_march2020": "f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa",
    "uaf_march_2020": "41dd3390627fac24c2bd696160c48f15e05d3213cc05325c4e4e89608df96d27",
    "nist_ncstar_1_9": "30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f",
}
DEFAULT_BUNDLE = Path(__file__).resolve().parent.parent / "c79-factorial-protocol-2026-10-19"


def validate_protocol(protocol, readme):
    """Return named pass/fail checks without modifying either argument.

    These targeted invariants are not an exhaustive JSON schema, a privacy
    clearance, a scientific validation or authorization to execute a model.
    """
    checks = []

    def check(name, predicate):
        try:
            passed = predicate() is True
        except (KeyError, IndexError, TypeError, ValueError, AttributeError, StopIteration):
            passed = False
        checks.append({"name": name, "passed": passed})

    def cases():
        return {case["id"]: case for case in protocol["cases"]}

    def contrast_changes_only(name):
        matches = [c for c in protocol["contrasts"] if c["id"] == name]
        if len(matches) != 1:
            return False
        contrast = matches[0]
        left, right = [cases()[key] for key in contrast["subtract"]]
        changed = [f for f in ("plate", "alpha") if left[f] != right[f]]
        return changed == [contrast["varied_factor"]]

    def compound_changes_both():
        left, right = [cases()[key] for key in protocol["compound_comparison"]["subtract"]]
        return (all(left[f] != right[f] for f in ("plate", "alpha"))
                and protocol["compound_comparison"]["isolates_single_factor"] is False)

    check("complete_two_by_two_design", lambda:
          len(protocol["cases"]) == 4 and
          {(c["plate"], c["alpha"]) for c in protocol["cases"]} ==
          set(product(["P0", "P1"], ["A0", "A1"])))
    check("case_identifiers_unique", lambda: len(cases()) == 4)
    for name in ("plate_at_A0", "plate_at_A1", "alpha_at_P0", "alpha_at_P1"):
        check(name + "_changes_only_declared_factor", lambda name=name: contrast_changes_only(name))
    check("compound_changes_both_and_not_single_factor", compound_changes_both)
    check("interaction_is_difference_of_plate_contrasts", lambda:
          protocol["interaction"]["subtract_contrasts"] == ["plate_at_A1", "plate_at_A0"] and
          protocol["interaction"]["requires_common_predeclared_scalar_observable"] is True)
    check("original_alpha_unknown_not_back_calculated", lambda:
          protocol["factors"]["alpha"]["A0_native_value"] is None and
          protocol["factors"]["alpha"]["infer_A0_by_dividing_A1_by_1_4"] is False)
    check("coefficient_scope_matches_named_four_beams", lambda:
          set(protocol["factors"]["alpha"]["scope_members"]) == {"K3004", "C3004", "B3004", "A3004"} and
          protocol["factors"]["alpha"]["unchanged_named_member"] == "G3005")
    check("coefficient_not_temperature_increase", lambda:
          protocol["factors"]["alpha"]["temperature_increase"] is False and
          protocol["factors"]["alpha"]["A1_report_value"] == "11.5e-6")
    check("no_native_execution_claim", lambda:
          type(protocol["native_case_execution_count"]) is int and
          protocol["native_case_execution_count"] == 0 and
          all(c["executed"] is False for c in protocol["cases"]) and
          protocol["nist_native_reproduction"] is False)
    check("historical_result_unknown", lambda: protocol["historical_prevention"] is None)
    check("numerical_execution_details_explicitly_pending", lambda:
          all(v is None for k, v in protocol["numerical_execution_details"].items() if k != "freeze_status") and
          protocol["status"] == "factorial_design_frozen_execution_blocked")
    check("all_source_pins_match_prior_records_and_readme", lambda:
          len(protocol["source_pins"]) == 3 and
          {s["id"] for s in protocol["source_pins"]} == set(SOURCE_PINS) and
          all(s["sha256"] == SOURCE_PINS[s["id"]] and s["sha256"] in readme
              for s in protocol["source_pins"]))
    check("UAF_page_crosswalk", lambda:
          all(s["printed_pages"] == [77, 78, 79, 80, 81] and
              s["physical_pdf_pages"] == [90, 91, 92, 93, 94]
              for s in protocol["source_pins"] if s["id"].startswith("uaf_")))
    check("NIST_page_crosswalk", lambda:
          next(s for s in protocol["source_pins"] if s["id"] == "nist_ncstar_1_9")
          ["physical_pdf_pages"] == [395, 397, 548, 549])
    check("public_only_sources", lambda:
          all(s["url"].startswith("https://") for s in protocol["source_pins"]) and
          "no_private_case_material" in protocol["exclusions"])
    check("preservation_and_scope_exclusions_present", lambda:
          all(item in protocol["exclusions"] for item in (
              "no_source_overwrite", "no_discrepancy_adjudication", "no_third_party_contact",
              "no_litigation_record_changes", "no_solver_installation_or_run",
              "no_historical_cause_or_intent_inference")))
    check("nonphysical_contact_shortcut_distinguished", lambda:
          "nonphysical numerical diagnostic" in readme and "mass, stiffness and mesh" in readme)
    check("observable_support_loss_distinctions", lambda:
          "seat_contact_area_and_reaction" in protocol["required_outputs"] and
          "Define loss of seat contact separately from loss of all vertical support." in readme)
    check("no_private_local_paths_in_public_payload", lambda:
          all(marker not in readme and marker not in json.dumps(protocol)
              for marker in ("/Users/", "/Volumes/")))
    return checks


def verify_bundle(bundle):
    """Check the frozen files as bytes and rerun the protocol invariants."""
    contents = {name: (bundle / name).read_bytes() for name in BUNDLE_PINS}
    hashes = [{"path": name, "sha256": hashlib.sha256(body).hexdigest(),
               "matches_frozen_pin": hashlib.sha256(body).hexdigest() == BUNDLE_PINS[name]}
              for name, body in contents.items()]
    checks = validate_protocol(json.loads(contents["protocol.json"]), contents["README.md"].decode("utf-8"))
    prior = json.loads(contents["verification.json"])
    names_match = ([c["name"] for c in checks] == [c["name"] for c in prior["checks"]]
                   and len(checks) == prior["check_count"] == 22)
    return {
        "scope": "frozen_protocol_integrity_and_design_checks_not_structural_validation",
        "frozen_file_hash_checks": hashes,
        "design_check_count": len(checks),
        "design_checks": checks,
        "prior_record_check_names_match": names_match,
        "all_passed": names_match and all(c["passed"] for c in checks)
                      and all(h["matches_frozen_pin"] for h in hashes),
        "native_solver_runs": 0,
        "historical_cause_assessment": None,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    args = parser.parse_args(argv)
    try:
        result = verify_bundle(args.bundle)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, UnicodeError) as exc:
        print(json.dumps({"all_passed": False, "error_type": type(exc).__name__,
                          "scope": "protocol_read_or_parse_failure_not_a_model_result"}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
