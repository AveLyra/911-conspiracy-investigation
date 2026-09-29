"""Synthetic text/selection fixtures only. Never invoke dense main or media tools."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

BASE = Path(__file__).resolve().parents[1]
EXPECTED = "4d8afe6485f37b6bf2b5dd531f6b30664f019d90f68fdd1cf3c96943be527c86"


def fake(points, indices=None, width=1620, height=1080, shown=None, base="1/1000"):
    lines = ["[Parsed_showinfo_1 @ synthetic] config in time_base: " + base]
    for i, pts in enumerate(points):
        n = i if indices is None else indices[i]
        t = str(pts/1000) if shown is None else shown[i]
        lines.append(f"[Parsed_showinfo_1 @ synthetic] n: {n} pts: {pts} pts_time:{t} pos: 1 fmt:rgb24 s:{width}x{height} checksum:0000")
    return "\n".join(lines) + "\n"


def candidate(i, target, static, dynamic, second=None):
    choices = [{"static_score": static, "dynamic_score": dynamic}]
    if second is not None:
        choices.append({"static_score": second, "dynamic_score": second})
    return {"frame_index": i, "target": target, "geometry_candidates": choices}


def run(module):
    checks = []
    def check(name, condition, detail=None):
        row = {"name": name, "passed": bool(condition)}
        if detail is not None:
            row["detail"] = detail
        checks.append(row)
    def reject(name, text, count=3):
        try:
            got = module.parse_showinfo(text, count, 2502, 2510)
            check(name, False, {"unexpected_accepted_rows": len(got)})
        except ValueError:
            check(name, True)
    points = [2502000, 2502033, 2502067]
    parsed = module.parse_showinfo(fake(points), 3, 2502, 2510)
    check("valid_order_and_pts_identity", parsed == [
        {"frame_index": i, "source_pts": pts, "source_time_base": "1/1000"}
        for i, pts in enumerate(points)])
    reject("short_showinfo_list", fake(points[:2]))
    reject("extra_showinfo_list", fake(points + [2502100]))
    reject("duplicate_pts", fake([2502000, 2502033, 2502033]))
    reject("decreasing_pts", fake([2502000, 2502067, 2502033]))
    reject("nonsequential_filter_index", fake(points, indices=[0, 2, 3]))
    reject("out_of_interval_below", fake([2501999, 2502033, 2502067]))
    reject("half_open_end_excluded", fake([2502000, 2502033, 2510000]))
    reject("wrong_geometry", fake(points, width=1619))
    reject("missing_pts", fake(points).replace("pts: 2502033", "pts: NOPTS"))
    reject("missing_timebase", "\n".join(fake(points).splitlines()[1:]))
    reject("wrong_timebase", fake(points, base="1/90000"))
    reject("shown_time_mismatch", fake(points, shown=["2502", "2503", "2502.067"]))
    reject("nonfinite_shown_time", fake(points, shown=["2502", "nan", "2502.067"]))
    rows = [candidate(i, "148", 1, None) for i in range(7)]
    check("ties_select_lowest_four_indices", module.get_shortlist(rows) == {0, 1, 2, 3})
    rows = [candidate(i, "148", 10-i, i) for i in range(8)]
    check("static_dynamic_union", module.get_shortlist(rows) == set(range(8)))
    rows += [candidate(i+8, "149", 10-i, i) for i in range(8)]
    check("both_targets_union_cap_16", module.get_shortlist(rows) == set(range(16)))
    rows = [candidate(i, "148", 10-i, None) for i in range(6)]
    rows += [candidate(i, "149", 10-i, None) for i in range(6)]
    check("same_frame_multiple_keys_deduplicated", module.get_shortlist(rows) == {0, 1, 2, 3})
    rows += [{"frame_index": 40, "target": "148", "geometry_candidates": []}]
    rows += [candidate(41, "other", 1000, 1000)]
    check("empty_and_unselected_target_ignored", module.get_shortlist(rows) == {0, 1, 2, 3})
    rows += [candidate(45, "148", -100, None, second=10000)]
    check("second_geometry_does_not_refit_dynamic_rank", module.get_shortlist(rows) == {0, 1, 2, 3})
    rng = random.Random(14092026)
    history, retained = [], {}
    retention_ok = True
    max_retained = 0
    for i in range(100):
        for target in ("148", "149"):
            history.append(candidate(i, target, rng.randint(0, 6),
                                     None if i % 5 == 0 else rng.randint(0, 6)))
        selected = module.get_shortlist(history)
        if i in selected:
            retained[i] = "synthetic-frame-" + str(i)
        retained = {j: b for j, b in retained.items() if j in selected}
        retention_ok &= set(retained) == selected
        max_retained = max(max_retained, len(retained))
    check("streaming_retention_equals_final_prefix_shortlist", retention_ok)
    check("retention_never_exceeds_16", max_retained <= 16)
    return {"status": "passed" if all(r["passed"] for r in checks) else "failed",
            "checks": checks, "check_count": len(checks),
            "retention_prefix_count": 100, "maximum_retained": max_retained,
            "scope": "synthetic showinfo text and fixed-score shortlist retention only; no media, decode or production results"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = BASE / "dense_match.py"
    if hashlib.sha256(source.read_bytes()).hexdigest() != EXPECTED:
        raise ValueError("dense producer changed before synthetic import")
    sys.path.insert(0, str(BASE))
    spec = importlib.util.spec_from_file_location("dense_synthetic_subject", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    receipt = run(module)
    receipt.update(dense_sha256=EXPECTED,
                   fixture_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   python=sys.version, argv=sys.argv)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": receipt["status"], "checks": receipt["check_count"],
                      "failures": [r for r in receipt["checks"] if not r["passed"]]}))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
