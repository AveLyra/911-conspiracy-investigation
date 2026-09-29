"""Synthetic producer comparison; frozen direct oracle is not modified/imported by producer."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import sys

BASE = Path(__file__).resolve().parents[1]
ORACLE = "f1ecbbb6fc4c48c58786d43287ac65cdeb1a3428b93ca0ae5bec6bccf43a4e71"
PRODUCER = "06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8"


def load(name, filename, digest):
    if hashlib.sha256(filename.read_bytes()).hexdigest() != digest:
        raise ValueError(name + " source changed")
    spec = importlib.util.spec_from_file_location(name, filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    oracle = load("direct_oracle", BASE / "direct_oracle.py", ORACLE)
    producer = load("producer", BASE / "match_screen.py", PRODUCER)
    import numpy as np
    rng = random.Random(29112008)
    checks = []
    metrics = {"surfaces": 0, "offsets": 0, "finite_scores": 0,
               "max_score_error": 0.0, "max_coverage_error": 0.0,
               "max_correlation_error": 0.0}
    def compare(name, source, template, mask, valid, min_count=2, min_cov=0):
        s, t, m, v = [np.array(a, dtype=float) for a in (source, template, mask, valid)]
        scores, coverage = producer.pearson_surface(s, t, m, v, min_cov, min_count)
        shifts = [(y, x) for y in range(s.shape[0]-t.shape[0]+1)
                  for x in range(s.shape[1]-t.shape[1]+1)]
        expected = oracle.pearson_surface(s, t, m, v, shifts=shifts,
                                         minimum_count=min_count, minimum_coverage=min_cov)
        corr = producer.correlate_valid(s, t)
        failures = []
        for row in expected:
            y, x = row["dy"], row["dx"]
            want = row["rho"]
            got = float(scores[y, x])
            if math.isfinite(got) != (want is not None):
                failures.append({"y": y, "x": x, "kind": "admissibility",
                                 "expected": want, "actual": got if math.isfinite(got) else None})
            if want is not None and math.isfinite(got):
                error = abs(got-want)
                metrics["max_score_error"] = max(metrics["max_score_error"], error)
                metrics["finite_scores"] += 1
                if error > 1e-9:
                    failures.append({"y": y, "x": x, "kind": "rho", "error": error})
            error = abs(float(coverage[y, x])-row["coverage"])
            metrics["max_coverage_error"] = max(metrics["max_coverage_error"], error)
            if error > 1e-12:
                failures.append({"y": y, "x": x, "kind": "coverage", "error": error})
            direct = math.fsum(float(s[y+i, x+j])*float(t[i, j])
                               for i in range(t.shape[0]) for j in range(t.shape[1]))
            error = abs(float(corr[y, x])-direct)
            metrics["max_correlation_error"] = max(metrics["max_correlation_error"], error)
            if error > 1e-8:
                failures.append({"y": y, "x": x, "kind": "correlation", "error": error})
        metrics["surfaces"] += 1
        metrics["offsets"] += len(expected)
        checks.append({"name": name, "passed": not failures, "failures": failures})
        return scores
    for number in range(64):
        sh, sw = rng.randint(5, 12), rng.randint(5, 12)
        th, tw = rng.randint(2, min(7, sh)), rng.randint(2, min(7, sw))
        s = [[rng.randint(0, 255) for x in range(sw)] for y in range(sh)]
        t = [[rng.randint(0, 255) for x in range(tw)] for y in range(th)]
        m = [[rng.random() < .75 for x in range(tw)] for y in range(th)]
        m[0][0] = True
        v = [[rng.random() < .8 for x in range(sw)] for y in range(sh)]
        compare("random-" + str(number), s, t, m, v,
                min_count=2 if number % 2 else 32,
                min_cov=0 if number % 3 else .85)
    compare("padding_changes_template_mean", [[0, 3, 5, 9]], [[999, 3, 5]],
            [[1, 1, 1]], [[0, 1, 1, 1]], min_cov=2/3)
    compare("flat_source", [[7]*9]*8, [[1, 2], [3, 4]], [[1, 1], [1, 1]], [[1]*9]*8)
    compare("flat_template", [[i+2*j for i in range(9)] for j in range(8)],
            [[7, 7], [7, 7]], [[1, 1], [1, 1]], [[1]*9]*8)
    compare("no_valid_source", [[2]*9]*8, [[1, 2], [3, 4]], [[1, 1], [1, 1]], [[0]*9]*8)
    tile = [[(i+j) % 2 for i in range(8)] for j in range(6)]
    repeated = compare("repeated_grid", tile, [[0, 1], [1, 0]],
                       [[1, 1], [1, 1]], [[1]*8]*6, min_count=4, min_cov=1)
    checks.append({"name": "repeated_grid_retains_18_aliases", "passed":
                   int(np.sum(np.isfinite(repeated) & (abs(repeated-1) < 1e-9))) == 18})
    t = [[1, 7, 2], [9, 3, 5], [2, 8, 4], [5, 1, 9]]
    s = t[:2] + [[10-x for x in r] for r in t[2:]]
    static = compare("static_unchanged", s, t, [[1]*3]*2+[[0]*3]*2, [[1]*3]*4)
    dynamic = compare("dynamic_changed", s, t, [[0]*3]*2+[[1]*3]*2, [[1]*3]*4)
    checks.append({"name": "static_one_dynamic_minus_one", "passed":
                   abs(float(static[0, 0])-1) < 1e-9 and abs(float(dynamic[0, 0])+1) < 1e-9})
    receipt = {"status": "passed" if all(c["passed"] for c in checks) else "failed",
               "oracle_sha256": ORACLE, "producer_sha256": PRODUCER,
               "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "checks": checks, "metrics": metrics, "python": sys.version,
               "numpy": np.__version__, "argv": sys.argv,
               "scope": "synthetic valid-window core only; no resize, canvas, ranking, image or source-clock validation"}
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(receipt, out, indent=2, sort_keys=True, allow_nan=False)
        out.write("\n")
    print(json.dumps({"status": receipt["status"], "checks": len(checks), "metrics": metrics}))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
