#!/usr/bin/env python3
"""Bounded synthetic bridge pilot; read PROTOCOL.md before authorizing execution.

No target code runs at import. Invoke with isolated Python and a cleared environment.
The audit hook is bounded Python instrumentation, not an OS security sandbox.
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import traceback

ENGINE = Path("/Users/admin/dev/faraday")
ALLOWED_PARENT = Path("/private/tmp/wtc7-faraday-pilot.eGMyO9")
PYTHON = Path("/Users/admin/.pyenv/versions/3.13.7/bin/python3")
PROTOCOL_SHA256 = "d6b9a077c97dc2b207a587739f7e697f1b94c055bedee1f7a536c022da2569da"
ERRATUM_SHA256 = "727bc53e3ee790cfc560630f237297f1ce25ace83596ba293793d4b98096acf8"
PINS = {
    "src/research_machine/application/sherlock_bridge.py": "18a9bba79cbde0df917bdceea592d59c8513a53fcac07ec9571c95e8df5eac79",
    "tests/test_sherlock_bridge.py": "6787df5978a7f273c6df153dd0e0951141182400867ad2d7418bc6a81e17ccbe",
    "src/research_machine/application/service.py": "e739b18f1ca97814d1c6f001435e38280948f66480a9be5310ba520f9c20c933",
    "src/research_machine/interfaces/cli.py": "5fdfed7b4bd63ac9d51df1b6701a1775314daa91d6918ba396a9cf0a9aec67aa",
    "schemas/sherlock-bridge-link.schema.json": "10400ded1ce9cb771197c4e63eb56d8b122798af9f6c6c6dfb020c24c2b9f662",
    "src/research_machine/adapters/filesystem.py": "5b9f428f5f281e517de801f90b46bb14b27d834a05de306f3a77c4bad77bfde4",
    "src/research_machine/domain/models.py": "bb2eb70b9a2247c38729d02b82ed04a6284d77b482eaf7ed585c7920914ad6a6",
    "src/research_machine/application/evidence_admission.py": "6d90cf52f0684801c471aac4568374a3f170bd16cadb1e2d90f9870b34f5a4ef",
    "src/research_machine/addons/registry.py": "e99e60426bd75c40f4642bd1e8a6312d76d3581c60d92234d093dbae354bc5fb",
    "examples/sherlock-bridge-link.json": "34368d23dabb42eeeecbc61340d62435affa631d54dcf4fe9e5bbcff16c9f736",
    "sherlock-integration/.gitignore": "7a3a6c3e50cb75fd8aadb61931d51f311572a45b280e2cf1891b9c8bea66856f",
    "sherlock-integration/project.json": "b84ebae67bc9625c476c33b8adbc8e4a1951d1e36d7c79d13206c868d1ad1d45",
    "sherlock-integration/CHARTER.md": "158aaed7b482924f6f812ade62424cafa0de75a1cce1f6ff18065386b6315f01",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class BoundaryViolation(BaseException):
    """BaseException prevents an application ValueError handler hiding a denial."""


class Guard:
    def __init__(self, root):
        self.root, self.expected, self.denials = root, None, []

    def deny(self, event, detail):
        self.denials.append({"event": event, "detail": str(detail),
                             "expected_control": self.expected})
        raise BoundaryViolation(f"audit boundary denied {event}: {detail}")

    def path(self, value, dir_fd=None):
        # F_GETPATH is Darwin's read-only descriptor lookup. resolve() only reads;
        # none of its stat/readlink events are mutation events handled below.
        if isinstance(value, int):
            return Path(os.fsdecode(fcntl.fcntl(value, 50, bytes(1024)).split(b"\0")[0])).resolve()
        path = Path(os.fsdecode(value))
        if not path.is_absolute() and dir_fd not in (None, -1):
            path = self.path(dir_fd) / path
        return path.resolve(strict=False)

    def check(self, value, event, dir_fd=None):
        try:
            path = self.path(value, dir_fd)
        except (OSError, TypeError, ValueError) as exc:
            self.deny(event, f"unresolved mutation target: {exc}")
        if path != self.root and not path.is_relative_to(self.root):
            self.deny(event, path)

    def __call__(self, event, args):
        if event.startswith(("socket.", "subprocess.", "os.exec", "os.spawn", "os.posix_spawn")) or event in {
            "os.system", "os.fork", "os.forkpty", "os.startfile", "ctypes.dlopen", "ctypes.dlsym",
        }:
            self.deny(event, "network, process creation, or native foreign-call access")
        elif event == "open":
            path, mode, flags = args
            if (mode and any(c in mode for c in "wax+")) or (flags and flags & (
                os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
            )):
                self.check(path, event)
        elif event in {"os.rename", "os.link"}:
            self.check(args[0], event, args[2])
            self.check(args[1], event, args[3])
        elif event == "os.symlink":
            self.check(args[1], event, args[2])
            self.check(self.path(args[1], args[2]).parent / os.fsdecode(args[0]), event)
        elif event in {"os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.chown", "os.utime"}:
            fd_index = {"os.remove": 1, "os.rmdir": 1, "os.mkdir": 2,
                        "os.chmod": 2, "os.chown": 3, "os.utime": 3}[event]
            self.check(args[0], event, args[fd_index])
        elif event in {"os.truncate", "os.chdir", "tempfile.mkstemp", "tempfile.mkdtemp"}:
            self.check(args[0], event)

    def self_controls(self):
        control = self.root / "guard-controls"
        control.mkdir()
        allowed = control / "allowed.txt"
        allowed.write_text("synthetic audit-control only\n")
        fd, temporary = tempfile.mkstemp(dir=control)
        os.close(fd)
        os.replace(temporary, control / "replaced.txt")
        (control / "inside-link").symlink_to(allowed)
        (control / "inside-link").write_text("synthetic in-root symlink write\n")
        outside = self.root.parent / f"guard-refused-{self.root.name}"
        require(not outside.exists(), "outside control target already exists")
        probes = {
            "outside_write": lambda: outside.open("xb"),
            "outside_symlink": lambda: (control / "outside-link").symlink_to(outside),
            "network": lambda: socket.socket(),
            "subprocess": lambda: subprocess.Popen(["/usr/bin/true"]),
        }
        for label, operation in probes.items():
            self.expected = label
            try:
                operation()
            except BoundaryViolation:
                pass
            else:
                raise RuntimeError(f"SAFETY FAILURE: self-control {label} was not refused")
            finally:
                self.expected = None
        require(not outside.exists(), "SAFETY FAILURE: outside file was created")
        return {"allowed_local_write": allowed.is_file(), "allowed_temporary_replace": True,
                "allowed_inroot_symlink": True, "denied_controls": list(probes)}


def inventory(root):
    return {str(p.relative_to(root)): digest(p) for p in sorted(root.rglob("*")) if p.is_file()}


def snapshot(workspace):
    files = inventory(workspace)
    ledger_paths = sorted(workspace.rglob("ledger.jsonl"))
    return {"files": files, "scientific_files": {p: h for p, h in files.items()
            if not p.endswith("/ledger.jsonl")}, "ledger": [json.loads(line)
            for path in ledger_paths for line in path.read_text().splitlines() if line.strip()]}


class Pilot:
    def __init__(self, root, guard, receipt):
        self.root, self.guard, self.receipt = root, guard, receipt
        self.workspace = root / "workspace"
        self.checks = receipt["checks"]

    def check(self, label, condition):
        self.checks.append({"label": label, "passed": bool(condition)})

    def call(self, label, args, *, required=False):
        from research_machine.interfaces.cli import main
        command = ["--workspace", str(self.workspace), "--actor", "codex-synthetic-fixture", "--json", *args]
        record = {"label": label, "argv": command, "before": snapshot(self.workspace)}
        self.receipt["commands"].append(record)
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    code = main(command)
                except SystemExit as exc:
                    code = exc.code
            record["exit_code"] = code
        except BaseException:
            record["exception"] = traceback.format_exc()
            raise
        finally:
            record.update(stdout=out.getvalue(), stderr=err.getvalue(), after=snapshot(self.workspace))
            print(json.dumps({"command_record": record}, sort_keys=True), flush=True)
        require(not any(d["expected_control"] is None for d in self.guard.denials), "unexpected audit denial")
        try:
            record["response"] = json.loads(out.getvalue()) if out.getvalue() else None
        except json.JSONDecodeError:
            record["response"] = None
        if required:
            require(code == 0 and record["response"] and record["response"].get("ok") is True,
                    f"required setup/inspection command failed: {label}")
            return record["response"]["result"]
        return record

    def export(self, label, evidence, *, expected=0, output=None, extra=None, omitted=False):
        output = output or self.root / "exports" / label
        before_output = inventory(output)
        destination = {"case_id": "nonexistent-synthetic-case", "kind": "assertion",
                       "id": "nonexistent-synthetic-reference"}
        options = ["--sherlock-case", destination["case_id"], "--sherlock-kind", destination["kind"]]
        if not omitted:
            options += ["--sherlock-id", destination["id"]]
        options += extra or []
        record = self.call(label, ["sherlock", "export-evidence", "--evidence", evidence["evidence_id"],
                                   "--output", str(output), *options])
        case = {"case": label, "expected_exit": expected, "actual_exit": record["exit_code"],
                "output_before": before_output, "output_after": inventory(output)}
        self.receipt["cases"].append(case)
        before, after = record["before"], record["after"]
        self.check(label + ":scientific_projections_unchanged", before["scientific_files"] == after["scientific_files"])
        if expected is not None:
            self.check(label + ":expected_exit", record["exit_code"] == expected)
        if record["exit_code"] != 0:
            self.check(label + ":refusal_workspace_unchanged", before["files"] == after["files"])
            self.check(label + ":refusal_output_unchanged", before_output == case["output_after"])
            self.check(label + ":refusal_no_new_output", bool(before_output) or not output.exists())
            return case
        additions = after["ledger"][len(before["ledger"]):]
        self.check(label + ":only_one_export_event", after["ledger"][:len(before["ledger"])] == before["ledger"]
                   and len(additions) == 1 and additions[0]["command"] == "sherlock.evidence.export")
        try:
            import jsonschema
            result = record["response"]["result"]
            summary = json.loads((output / "faraday-summary.json").read_text())
            link = json.loads((output / "sherlock-bridge-link.json").read_text())
            jsonschema.Draft202012Validator(self.schema, format_checker=jsonschema.FormatChecker()).validate(link)
            self.check(label + ":published_schema", True)
            self.check(label + ":two_files_only", set(case["output_after"]) == {"faraday-summary.json", "sherlock-bridge-link.json"})
            self.check(label + ":file_hashes_and_paths", all(result[key + "_sha256"] == digest(output / filename)
                       and Path(result[key + "_path"]) == output / filename
                       for key, filename in (("summary", "faraday-summary.json"), ("bridge_link", "sherlock-bridge-link.json"))))
            self.check(label + ":receipt_summary_binding", link["translation"]["summary_sha256"] == digest(output / "faraday-summary.json")
                       and link["translation"]["summary_locator"] == "faraday-summary.json" and result["receipt"] == link)
            for key, value in {"evidence": evidence, "hypothesis": self.hypothesis, "dataset": self.dataset,
                               "claim": self.claim, "inquiry": self.inquiry, "protocol": None, "run": None}.items():
                self.check(label + ":exact_" + key, summary[key] == value)
            evidence_hash = json_digest({k: v for k, v in evidence.items() if k != "admission_checks"})
            self.check(label + ":evidence_commitment", summary["faraday_reference"]["evidence_record_sha256"]
                       == link["faraday_reference"]["evidence_record_sha256"] == evidence_hash)
            self.check(label + ":authority_flags", all(link["authority_boundary"][k] is False for k in (
                "faraday_canonical_state_mutated", "sherlock_note_is_faraday_evidence", "publication_authorized", "review_promotion_authorized"))
                and summary["authority_boundary"]["canonical_state_mutated_by_export"] is False
                and summary["authority_boundary"]["sherlock_note_is_faraday_evidence"] is False)
            self.check(label + ":synthetic_pending_non_scientific", summary["dataset"]["synthetic"] is True
                       and summary["dataset"]["role"] == "exploratory" and summary["hypothesis"]["workflow_state"] == "pending_review"
                       and summary["evidence"]["scientific_evidence_eligible"] is False and summary["evidence"]["exploratory"] is True)
            ceiling = evidence["analysis_claim_ceiling"] or "; ".join(evidence["higher_level_conclusions_unsupported"])
            self.check(label + ":direction_uncertainty_ceiling", link["direction"] == "faraday_export_to_sherlock"
                       and summary["evidence"]["direction"] == evidence["direction"] and summary["evidence"]["uncertainty"] == self.uncertainty
                       and summary["faraday_reference"]["claim_ceiling"] == link["faraday_reference"]["claim_ceiling"] == ceiling)
            destination["id"] = "pending-" + evidence["evidence_id"] if omitted else destination["id"]
            if "--sherlock-artifact-sha256" in options:
                destination["artifact_sha256"] = options[options.index("--sherlock-artifact-sha256") + 1]
            self.check(label + ":exact_destination_values", link["sherlock_reference"] == destination)
            case.update(sherlock_reference=link["sherlock_reference"], known_limitations=summary["known_limitations"],
                        translation_limitations=link["translation"]["known_limitations"],
                        exposed_dataset_artifacts=summary["dataset"]["artifacts"], dataset_metadata=summary["dataset"]["metadata"],
                        raw_locator_retained=str(self.raw) in json.dumps(summary), raw_exists=self.raw.exists(),
                        current_raw_sha256=digest(self.raw) if self.raw.exists() else None,
                        semantic_payload={"evidence_direction": summary["evidence"]["direction"], "uncertainty": summary["evidence"]["uncertainty"],
                                          "synthetic": summary["dataset"]["synthetic"], "workflow_state": summary["hypothesis"]["workflow_state"],
                                          "scientific_evidence_eligible": summary["evidence"]["scientific_evidence_eligible"],
                                          "claim_ceiling": ceiling, "placeholder": omitted,
                                          "destination_digest_retained": link["sherlock_reference"].get("artifact_sha256")})
        except Exception:
            case["inspection_error"] = traceback.format_exc()
            self.check(label + ":export_inspection", False)
        return case

    def matrix(self):
        self.schema = json.loads((ENGINE / "schemas/sherlock-bridge-link.schema.json").read_text())
        self.call("init", ["workspace", "init"], required=True)
        self.inquiry = self.call("inquiry", ["inquiry", "create", "--id", "synthetic-bridge-pilot", "--title",
            "Synthetic bridge plumbing fixture", "--statement", "Does this toy bridge retain declared software-fixture limitations?"], required=True)
        self.claim = self.call("claim", ["claim", "add", "--statement", "The synthetic fixture note contains a toy value.",
            "--level", "measurement_validity", "--scope", "Generated software fixture only; no historical observation."], required=True)
        proposal = self.call("hypothesis", ["hypothesis", "propose", "--statement", "The synthetic toy observation remains unresolved.",
            "--parent-claim", self.claim["claim_id"], "--scope", "Generated software fixture only.",
            "--prediction", "The generated toy note contains value 1.", "--null-model", "The toy note does not contain value 1.",
            "--competing-model", "The toy note contains a different value.", "--falsification", "The generated note contains only value 2.",
            "--support-condition", "The generated note retains value 1.", "--boundary-condition", "No real-world inference is permitted."], required=True)
        self.hypothesis = self.call("stage", ["hypothesis", "stage", proposal["hypothesis_id"], "--confidence", "high",
            "--rationale", "Complete synthetic software fixture for exploratory export checks only; human review remains pending."], required=True)
        self.raw = self.root / "synthetic-fixture.csv"
        self.raw.write_text("value\n1\n")
        (self.root / "synthetic-fixture-original.csv").write_bytes(self.raw.read_bytes())
        self.dataset = self.call("dataset", ["dataset", "register", "--id", "synthetic-dataset", "--name", "Generated synthetic toy source",
            "--role", "exploratory", "--synthetic", "--description", "Software fixture only; not an acquired observation.", "--file", str(self.raw)], required=True)
        self.uncertainty = "Generated toy fixture; no inferential uncertainty estimate or real-world measurement is supplied."
        evidence = {}
        for direction in ("inconclusive", "refutes"):
            evidence[direction] = self.call("evidence-" + direction, ["evidence", "record", "--hypothesis", self.hypothesis["hypothesis_id"],
                "--claim", self.claim["claim_id"], "--direction", direction, "--summary", f"Synthetic source-assessment fixture with {direction} direction; no scientific conclusion.",
                "--dataset", self.dataset["dataset_id"], "--analysis", "synthetic-source-assessment", "--uncertainty", self.uncertainty,
                "--scope", "Generated software fixture only.", "--higher-conclusion-unsupported", "Every real-world scientific, historical, causal, and legal conclusion.",
                "--validation-tag", "source_assessment"], required=True)
        inconclusive = evidence["inconclusive"]
        first_output = self.root / "exports" / "01-ordinary"
        self.export("01-ordinary", inconclusive, output=first_output)
        self.export("02-existing-output", inconclusive, expected=2, output=first_output)
        self.export("03-missing-evidence", {"evidence_id": "evd-missing-synthetic"}, expected=2)
        self.export("04-unsupported-kind", inconclusive, expected=2, extra=["--sherlock-kind", "unsupported-fixture-kind"])
        self.export("05-malformed-digest", inconclusive, expected=2, extra=["--sherlock-artifact-sha256", "not-a-sha256"])
        self.export("06-unverified-destination", inconclusive, expected=None, extra=["--sherlock-artifact-sha256", "d" * 64])
        self.export("07-omitted-id", inconclusive, omitted=True)
        self.export("08-contradicting", evidence["refutes"])
        self.raw.write_text("value\n2\n")
        self.export("09a-changed-raw", inconclusive, expected=None)
        retained = self.root / "synthetic-fixture-missing-retained.csv"
        self.raw.rename(retained)
        self.export("09b-missing-raw", inconclusive, expected=None)
        self.receipt["raw_preservation"] = {"original_copy_sha256": digest(self.root / "synthetic-fixture-original.csv"),
            "changed_copy_path": str(retained), "changed_copy_sha256": digest(retained), "registered_locator_now_missing": not self.raw.exists()}
        for label, args in (("final-audit", ["workspace", "audit"]), ("final-synthesis", ["synthesis", "build"]),
                            ("final-ledger", ["workspace", "verify"])):
            record = self.call(label, args)
            self.check(label + ":command_completed", record["exit_code"] == 0)
            if label == "final-ledger":
                self.check(label + ":valid", bool(record["response"] and record["response"].get("result", {}).get("valid")))
        self.receipt["final_workspace"] = snapshot(self.workspace)
        self.receipt["semantic_result"] = [{k: case.get(k) for k in (
            "case", "actual_exit", "raw_locator_retained", "raw_exists", "current_raw_sha256", "semantic_payload",
            "known_limitations", "translation_limitations", "inspection_error")} for case in self.receipt["cases"]]

    def native(self):
        import pytest
        class Counts:
            def __init__(inner):
                inner.collected, inner.reports = 0, []

            def pytest_collection_finish(inner, session):
                inner.collected = len(session.items)

            def pytest_runtest_setup(inner, item):
                if any(d["expected_control"] is None for d in self.guard.denials):
                    pytest.exit("Unexpected audit denial; stop without broadening boundary", returncode=2)

            def pytest_runtest_logreport(inner, report):
                inner.reports.append({"nodeid": report.nodeid, "when": report.when, "outcome": report.outcome,
                                      "longrepr": str(report.longrepr) if report.longrepr else None})
        counts = Counts()
        config = self.root / "pytest.ini"
        config.write_text("[pytest]\n")
        args = [str(ENGINE / "tests/test_sherlock_bridge.py"), "-q", "-s", "-p", "no:cacheprovider", "--noconftest",
                "--import-mode=importlib", "--rootdir", str(ENGINE), "-c", str(config), "--basetemp", str(self.root / "native-tmp")]
        self.receipt["native"] = {"argv": args, "fixture_limitation": "Unchanged native dataset fixtures omit --synthetic; these tests do not establish typed synthetic propagation."}
        print("pytest.main " + json.dumps(args), flush=True)
        code = int(pytest.main(args, plugins=[counts]))
        stats = {"collected": counts.collected, "passed": sum(r["when"] == "call" and r["outcome"] == "passed" for r in counts.reports),
                 "failed": sum(r["outcome"] == "failed" for r in counts.reports),
                 "skipped": sum(r["outcome"] == "skipped" for r in counts.reports)}
        self.receipt["native"].update(exit_code=code, counts=stats, reports=counts.reports)
        self.check("native:exact_nine_collected", counts.collected == 9)
        self.check("native:all_nine_passed", code == 0 and stats == {"collected": 9, "passed": 9, "failed": 0, "skipped": 0})
        self.receipt["native_files"] = inventory(self.root / "native-tmp")


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def isatty(self):
        # The tee is a retained-log stream, not an interactive terminal.
        return False

    def write(self, text):
        for stream in self.streams:
            stream.write(text)
        return len(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=("native", "matrix"))
    parser.add_argument("--run-root", required=True, type=Path)
    args = parser.parse_args()
    root = args.run_root
    require(root.is_absolute() and root.parent == ALLOWED_PARENT and root.resolve() == root,
            "run root must be an exact absolute, nonsymlinked immediate child of the declared temporary parent")
    require(ALLOWED_PARENT.is_dir() and not root.exists() and not root.is_symlink(), "fresh nonexisting run root required")
    require(sys.flags.isolated and sys.dont_write_bytecode and sys.version_info[:3] == (3, 13, 7)
            and Path(sys.executable).resolve() == PYTHON.resolve() and sys.platform == "darwin", "exact isolated -I -B Python3.13.7 required")
    # macOS may inject this process-local encoding key after the caller's env -i.
    os.environ.pop("__CF_USER_TEXT_ENCODING", None)
    require(not set(os.environ) - {"PATH", "PYTEST_DISABLE_PLUGIN_AUTOLOAD", "LC_CTYPE"}, "caller must clear external environment")
    require(os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD") == "1", "disable pytest plugin autoload")
    require(not any(n == "research_machine" or n.startswith("research_machine.") for n in sys.modules), "core imported before guard")
    guard = Guard(root)
    sys.addaudithook(guard)
    root.mkdir(mode=0o700)
    receipt = {"format_version": 1, "mode": args.mode, "run_root": str(root), "commands": [], "checks": [], "cases": [],
               "runner_sha256": digest(__file__), "invocation": sys.orig_argv, "boundary_limit":
               "Python audit instrumentation only; not a security sandbox, native-call proof, source authenticity, scientific validation, or Sherlock acceptance."}
    with (root / "stdout.log").open("x", encoding="utf-8") as log:
        with contextlib.redirect_stdout(Tee(sys.stdout, log)), contextlib.redirect_stderr(Tee(sys.stderr, log)):
            try:
                tempfile.tempdir = str(root / "tmp")
                Path(tempfile.tempdir).mkdir()
                os.environ["TMPDIR"] = tempfile.tempdir
                sys.pycache_prefix = str(root / "unused-bytecode-cache")
                os.chdir(root)
                receipt["guard_controls"] = guard.self_controls()
                protocol = Path(__file__).with_name("PROTOCOL.md")
                erratum = Path(__file__).with_name("PROTOCOL-ERRATUM.md")
                require(digest(protocol) == PROTOCOL_SHA256, "protocol pin mismatch")
                require(digest(erratum) == ERRATUM_SHA256, "protocol erratum pin mismatch")
                receipt["protocol_sha256"] = digest(protocol)
                receipt["protocol_erratum_sha256"] = digest(erratum)
                receipt["engine_pins_before"] = {p: digest(ENGINE / p) for p in PINS}
                require(receipt["engine_pins_before"] == PINS, "engine/test/schema pin mismatch")
                versions = {p: importlib.metadata.version(p) for p in ("pytest", "jsonschema")}
                require(versions == {"pytest": "8.4.2", "jsonschema": "4.25.1"}, "installed dependency version mismatch")
                entrypoints = list(importlib.metadata.entry_points(group="research_machine.addons"))
                receipt["addon_entrypoints"] = [str(ep) for ep in entrypoints]
                require(not entrypoints, "installed add-on entry points must be empty")
                receipt["runtime"] = {"python": sys.version, "executable": sys.executable, "packages": versions}
                (root / "protocol-input.md").write_bytes(protocol.read_bytes())
                (root / "protocol-erratum-input.md").write_bytes(erratum.read_bytes())
                (root / "runner-input.py").write_bytes(Path(__file__).read_bytes())
                sys.path.insert(0, str(ENGINE / "src"))
                pilot = Pilot(root, guard, receipt)
                getattr(pilot, args.mode)()
                receipt["imported_core_sources"] = {name: {"path": module.__file__, "sha256": digest(module.__file__)}
                    for name, module in sorted(sys.modules.items()) if name == "research_machine" or name.startswith("research_machine.")}
                require(all(Path(v["path"]).resolve().is_relative_to(ENGINE / "src") for v in receipt["imported_core_sources"].values()),
                        "a core module was imported outside the exact engine src tree")
                receipt["engine_pins_after"] = {p: digest(ENGINE / p) for p in PINS}
                require(receipt["engine_pins_after"] == PINS, "engine pins changed during execution")
            except BaseException:
                receipt["fatal_error"] = traceback.format_exc()
                print(receipt["fatal_error"], file=sys.stderr, flush=True)
            finally:
                receipt["expected_denials"] = [d for d in guard.denials if d["expected_control"] is not None]
                receipt["unexpected_denials"] = [d for d in guard.denials if d["expected_control"] is None]
                receipt["passed"] = not receipt.get("fatal_error") and not receipt["unexpected_denials"] and bool(receipt["checks"]) and all(c["passed"] for c in receipt["checks"])
                print(json.dumps({"mode": args.mode, "passed": receipt["passed"], "failed_checks": [c for c in receipt["checks"] if not c["passed"]]}, sort_keys=True), flush=True)
    receipt["stdout_log_sha256"] = digest(root / "stdout.log")
    (root / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
