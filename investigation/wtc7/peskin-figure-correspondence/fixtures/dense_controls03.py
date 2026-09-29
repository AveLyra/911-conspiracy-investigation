"""Versioned synthetic continuation gates; no media, disk census or runner main."""
import argparse
import ast
import contextlib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
EXPECTED = "b76788bf65e74fa464c060ee0a5831aba27eb864f6139f2c6c2f5a604bf2ce59"
CONTINUATION = "f532f8376db02f01f5943ea7f1df99719a016a57eecaee2185db079b320f5156"
FIXTURE01 = "ccdd76b0554b32162d576ec285648f71d054ac5bd775fae081f0b2d1db4d3b0a"


def load(name, path, expected):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("changed synthetic subject/fixture")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, data.decode()


class FakeFile:
    def __init__(self, parts, size, symlink=False):
        self.parts, self.size, self.symlink = parts, size, symlink
    def is_symlink(self): return self.symlink
    def is_file(self): return True
    def relative_to(self, base): return SimpleNamespace(parts=self.parts)
    def stat(self): return SimpleNamespace(st_size=self.size)


def run(module, source, previous):
    receipt = previous.run(module)
    checks = receipt["checks"]
    def check(name, passed):
        checks.append({"name": name, "passed": bool(passed)})
    def rejects(call, exception=ValueError):
        try:
            call()
        except exception:
            return True
        return False
    points = [2502000, 2502033, 2502067]
    for displayed in ("inf", "-inf"):
        check("nonfinite_display_" + displayed, rejects(lambda: module.parse_showinfo(
            previous.fake(points, shown=["2502", displayed, "2502.067"]), 3, 2502, 2510)))
    def storage(files):
        with patch.object(module, "BASE", SimpleNamespace(rglob=lambda pattern: files)):
            return module.storage_check()
    mib = 1024**2
    files = [FakeFile((slot, "synthetic.bin"), cap) for slot, cap in module.SLOTS.items()]
    files.append(FakeFile(("baseline.bin",), 150*mib))
    at_limits = storage(files)
    check("all_slot_limits_and_baseline_accepted", sum(at_limits["slot_bytes"].values())
          + at_limits["baseline_bytes"] == 1940*mib)
    expected_slots = {"dense00": 450, "dense01": 100, "repro00": 10,
                      "dense11": 400, "dense12": 400, "dense13": 400,
                      "repro11": 10, "repro12": 10, "repro13": 10}
    check("exact_declared_slots", module.SLOTS == {k: v*mib for k, v in expected_slots.items()})
    check("declared_total_below_2GiB", sum(module.SLOTS.values())+150*mib < 2*1024**3)
    for name, size in (("baseline.bin", 150*mib+1), ("dense00", 450*mib+1),
                       ("dense01", 100*mib+1), ("dense11", 400*mib+1),
                       ("dense12", 400*mib+1), ("dense13", 400*mib+1),
                       ("repro00", 10*mib+1), ("repro11", 10*mib+1),
                       ("repro12", 10*mib+1), ("repro13", 10*mib+1),
                       ("dense04", 150*mib+1), ("dense02", 150*mib+1)):
        check("storage_reject_"+name, rejects(lambda name=name, size=size:
              storage([FakeFile((name, "synthetic.bin"), size)])))
    check("storage_reject_symlink", rejects(lambda: storage([FakeFile(("x",), 0, True)])))
    tree = ast.parse(source)
    def guard(message):
        candidates = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            for item in node.body:
                if (isinstance(item, ast.Raise) and isinstance(item.exc, ast.Call)
                        and isinstance(item.exc.func, ast.Name)
                        and item.exc.func.id == "ValueError" and item.exc.args
                        and isinstance(item.exc.args[0], ast.Constant)
                        and item.exc.args[0].value == message):
                    candidates.append(node)
        if len(candidates) != 1:
            raise ValueError("nonunique or missing intended guard: " + message)
        return compile(ast.Module(body=[candidates[0]], type_ignores=[]),
                       "synthetic-selected-guard", "exec")
    def exercise(message, env, should_reject, name):
        # Execute only one inspected If/raise guard over explicit synthetic
        # values, not main, its enclosing branches, or any media/file method.
        globals_ = {"Path": Path, "re": re, "get_shortlist": module.get_shortlist}
        globals_.update(env)
        got = rejects(lambda: exec(guard(message), globals_))
        check(name, got == should_reject)
    for chunk in range(1, 4):
        for kind, compare in (("dense", None), ("repro", f"dense1{chunk}")):
            a = SimpleNamespace(chunk=chunk, run=f"{kind}1{chunk}", compare_to=compare)
            exercise("undeclared run slot", {"a": a}, False, f"declared_{kind}1{chunk}")
            if compare:
                exercise("wrong comparison slot", {"a": a}, False, f"correct_compare_{chunk}")
    chunk_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                   and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument"
                   and node.args and isinstance(node.args[0], ast.Constant)
                   and node.args[0].value == "--chunk"]
    if len(chunk_calls) != 1:
        raise ValueError("nonunique chunk argument")
    choices = [kw.value for kw in chunk_calls[0].keywords if kw.arg == "choices"]
    if len(choices) != 1:
        raise ValueError("missing chunk choices")
    allowed = list(eval(compile(ast.Expression(choices[0]), "synthetic-chunk-choices", "eval"), {"range": range}))
    check("parser_admits_only_remaining_chunks", allowed == [1, 2, 3])
    for chunk in (-1, 0, 4):
        check(f"parser_rejects_chunk_{chunk}", chunk not in allowed)
    for run in ("dense00", "dense01", "dense02", "dense03", "repro01", "repro11"):
        exercise("undeclared run slot", {"a": SimpleNamespace(chunk=1, run=run, compare_to=None)},
                 True, "old_or_wrong_production_slot_" + run)
    check("original_and_three_continuations_only", module.PRODUCTION_RUNS == ["dense00", "dense11", "dense12", "dense13"])
    exercise("undeclared run slot", {"a": SimpleNamespace(chunk=1, run="dense12", compare_to=None)},
             True, "wrong_chunk_slot_rejected")
    exercise("wrong comparison slot", {"a": SimpleNamespace(chunk=1, compare_to="dense01")},
             True, "wrong_comparison_slot_rejected")
    exercise("unsafe run name", {"s": "../dense00"}, True, "path_run_rejected")
    for name, pin in module.PINS.items():
        env = {"core": SimpleNamespace(sha=lambda p: "wrong"), "BASE": Path("synthetic"),
               "name": name, "pin": pin}
        exercise("frozen dependency pin changed", env, True, "changed_pin_" + name)
    env = {"core": SimpleNamespace(sha=lambda p: "expected"), "BASE": Path("synthetic"),
           "name": "method", "pin": "expected"}
    exercise("frozen dependency pin changed", env, False, "unchanged_pin_accepted")
    admitted = {"status": "completed", "compare_to": "dense00", "reproduction_surface_comparisons": 480}
    exercise("first chunk reproduction required", {"first_repro": admitted}, False, "completed_first_repro_admitted")
    for field, values in (("status", ["started", "failed"]), ("compare_to", [None, "dense01"]),
                          ("reproduction_surface_comparisons", [0, 479, 481])):
        for value in values:
            fixture = dict(admitted, **{field: value})
            exercise("first chunk reproduction required", {"first_repro": fixture}, True,
                     f"first_repro_reject_{field}_{value}")
    for field in admitted:
        incomplete = dict(admitted)
        del incomplete[field]
        check("first_repro_missing_field_" + field, rejects(
            lambda incomplete=incomplete: exec(guard("first chunk reproduction required"),
                                               {"first_repro": incomplete}), KeyError))
    exercise("control gate", {"control": {"pass": False, "script_sha256": module.CORE_HASH},
             "CORE_HASH": module.CORE_HASH}, True, "failed_controls_rejected")
    for i, raw, wanted in ((274, b"abc", False), (275, b"abc", True), (0, b"ab", True)):
        exercise("partial frame/frame cap", {"i": i, "raw": raw, "size": 3}, wanted,
                 f"frame_guard_{i}_{len(raw)}")
    check("four_production_chunks_cap_1100", len(module.CHUNKS)*275 == 1100)
    exercise("prior not completed production", {"prior": {"status": "failed", "compare_to": None}},
             True, "failed_prior_rejected")
    exercise("prior identity mismatch", {"prior": {"interval": [0, 1]},
             "receipt": {"interval": [1, 2]}, "field": "interval"}, True, "wrong_prior_interval_rejected")
    exercise("prior manifest membership", {"manifests": {"one": {}}, "expected": {"one", "two"}},
             True, "missing_manifest_entry_rejected")
    exercise("prior manifest path", {"name": "../one"}, True, "prior_path_escape_rejected")
    prior = {"shortlist_indices": [0], "native_images": [{"frame_index": 0}, {"frame_index": 0}]}
    exercise("prior native membership", {"prior_native": {0: prior["native_images"][0]}, "prior": prior},
             True, "duplicate_native_indices_rejected")
    rows = [previous.candidate(0, "148", 1, .9)]
    exercise("prior shortlist disagrees with reproduced ranking", {"rows": rows, "prior": {"shortlist_indices": []}},
             True, "omitted_native_shortlist_rejected")
    exercise("prior shortlist disagrees with reproduced ranking", {"rows": rows, "prior": {"shortlist_indices": [0]}},
             False, "correct_recomputed_shortlist_accepted")
    # Evaluate only the reviewed argv list expression over synthetic paths/times;
    # this invokes no decoder, subprocess, filesystem or production main.
    commands = [node.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "argv" for t in node.targets)]
    if len(commands) != 1:
        raise ValueError("nonunique decoder argv")
    command = eval(compile(ast.Expression(commands[0]), "synthetic-decoder-argv", "eval"),
                   {"FFMPEG": "synthetic-ffmpeg", "SOURCE": "synthetic-source", "start": 10, "end": 18})
    check("input_allowance_24_before_input", command[command.index("-t")+1] == "24"
          and command.index("-t") < command.index("-i"))
    check("two_second_requested_leadin_unchanged", command[command.index("-ss")+1] == "8")
    check("half_open_8second_filter_unchanged",
          command[command.index("-vf")+1] == "select='gte(t,10)*lt(t,18)',showinfo")
    check("continuation_pin_declared", module.PINS["DENSE-CONTINUATION-02.md"] == CONTINUATION)
    check("alarm_handler_raises_timeout", rejects(lambda: module.alarm_handler(None, None), TimeoutError))
    receipt.update(status="passed" if all(c["passed"] for c in checks) else "failed",
                   check_count=len(checks), reused_parser_selection_checks=22,
                   scope="synthetic text, fixed scores, in-memory storage metadata and selected guard conditions; no main, media, real unit census or process alarm fired")
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(BASE))
    module, source = load("dense_gates_subject", BASE/"dense_match.py", EXPECTED)
    previous, _ = load("prior_dense_fixture", BASE/"fixtures/dense_controls01.py", FIXTURE01)
    receipt = run(module, source, previous)
    receipt.update(dense_sha256=EXPECTED, prior_fixture_sha256=FIXTURE01,
                   continuation_sha256=CONTINUATION,
                   fixture_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   python=sys.version, argv=sys.argv)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": receipt["status"], "checks": receipt["check_count"],
                      "failures": [r for r in receipt["checks"] if not r["passed"]]}))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())

