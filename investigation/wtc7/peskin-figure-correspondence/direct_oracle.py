"""Synthetic-only direct masked Pearson oracle; no image/media reader or FFT.

At displacement (dy, dx), template[y,x] pairs with source[y+dy,x+dx].
Only in-bounds, template-mask and source-valid positions contribute. Means are
recomputed on that exact overlap. Masks are binary, not continuous weights.
Population versus centered-sum variance gating is explicit, not inferred from
the word 'variance' in another implementation. This module performs no I/O on
import. Its CLI runs synthetic controls and optionally creates a new receipt.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys


def _matrix(value, name, binary=False):
    rows = [list(row) for row in value]
    if not rows or not rows[0] or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError(name + " must be a nonempty rectangular matrix")
    out = []
    for row in rows:
        converted = []
        for item in row:
            x = float(item)
            if not math.isfinite(x) or (binary and x not in (0.0, 1.0)):
                raise ValueError(name + " has nonfinite or nonbinary values")
            converted.append(bool(x) if binary else x)
        out.append(converted)
    return out


def pearson_surface(source, template, mask, valid=None, *, shifts=None,
                    minimum_count=32, minimum_coverage=0.85,
                    variance_floor=1e-8, variance_basis="population"):
    """Return every selected offset, including rejected offsets and raw stats.

    With shifts=None, return dy=1-template_height..source_height-1 and the
    analogous dx range, dy-major. A supplied shifts iterable contains (dy,dx).
    Coverage is n / the full template mask count, never n / overlapping area.
    A positive variance exactly equal to variance_floor is accepted ('below'
    is the rejection convention); zero is always rejected. No score clipping.
    """
    s = _matrix(source, "source")
    t = _matrix(template, "template")
    m = _matrix(mask, "mask", True)
    sh, sw, th, tw = len(s), len(s[0]), len(t), len(t[0])
    v = ([[True] * sw for _ in range(sh)] if valid is None
         else _matrix(valid, "valid", True))
    if (len(m), len(m[0])) != (th, tw):
        raise ValueError("template/mask shape mismatch")
    if (len(v), len(v[0])) != (sh, sw):
        raise ValueError("source/valid shape mismatch")
    if (isinstance(minimum_count, bool) or not isinstance(minimum_count, int)
            or minimum_count < 1):
        raise ValueError("minimum_count must be a positive integer")
    if (not math.isfinite(minimum_coverage) or not 0 <= minimum_coverage <= 1
            or not math.isfinite(variance_floor) or variance_floor < 0):
        raise ValueError("invalid coverage or variance threshold")
    if variance_basis not in ("population", "centered_sum"):
        raise ValueError("unknown variance basis")
    if shifts is None:
        shifts = ((dy, dx) for dy in range(1-th, sh)
                  for dx in range(1-tw, sw))
    mask_count = sum(sum(row) for row in m)
    result = []
    for dy, dx in shifts:
        if (isinstance(dy, bool) or isinstance(dx, bool)
                or not isinstance(dy, int) or not isinstance(dx, int)):
            raise ValueError("shifts must contain integer dy,dx pairs")
        pairs = [(s[y+dy][x+dx], t[y][x]) for y in range(th)
                 for x in range(tw) if m[y][x] and 0 <= y+dy < sh
                 and 0 <= x+dx < sw and v[y+dy][x+dx]]
        n = len(pairs)
        row = {"dy": dy, "dx": dx, "n": n, "mask_count": mask_count,
               "coverage": n / mask_count if mask_count else None,
               "source_mean": None, "template_mean": None,
               "source_centered_sum": None, "template_centered_sum": None,
               "cross_centered_sum": None, "source_variance": None,
               "template_variance": None, "raw_rho": None, "rho": None,
               "rejection": None}
        if n:
            sm = math.fsum(p[0] for p in pairs) / n
            tm = math.fsum(p[1] for p in pairs) / n
            ss = math.fsum((a-sm)**2 for a, b in pairs)
            tt = math.fsum((b-tm)**2 for a, b in pairs)
            st = math.fsum((a-sm)*(b-tm) for a, b in pairs)
            if not all(math.isfinite(a) for a in (sm, tm, ss, tt, st)):
                raise ArithmeticError("nonfinite centered statistic")
            row.update(source_mean=sm, template_mean=tm,
                       source_centered_sum=ss, template_centered_sum=tt,
                       cross_centered_sum=st, source_variance=ss/n,
                       template_variance=tt/n)
            if ss > 0 and tt > 0:
                row["raw_rho"] = (st / math.sqrt(ss)) / math.sqrt(tt)
        if not mask_count:
            row["rejection"] = "empty_mask"
        elif n < minimum_count:
            row["rejection"] = "minimum_count"
        elif row["coverage"] < minimum_coverage:
            row["rejection"] = "minimum_coverage"
        else:
            suffix = "variance" if variance_basis == "population" else "centered_sum"
            sv, tv = row["source_" + suffix], row["template_" + suffix]
            if sv <= 0 or tv <= 0 or sv < variance_floor or tv < variance_floor:
                row["rejection"] = "variance"
            else:
                row["rho"] = row["raw_rho"]
        result.append(row)
    return result


def _fraction_expected(source, template, mask, valid, dy, dx):
    """Control-only raw-moment formula using exact rational input values."""
    pairs = []
    for sy, srow in enumerate(source):
        ty = sy-dy
        if not 0 <= ty < len(template):
            continue
        for sx, value in enumerate(srow):
            tx = sx-dx
            if 0 <= tx < len(template[0]) and valid[sy][sx] and mask[ty][tx]:
                pairs.append((Fraction(value), Fraction(template[ty][tx])))
    n = len(pairs)
    if not n:
        return 0, None, None, None
    a, b = sum(x for x, y in pairs), sum(y for x, y in pairs)
    aa = sum(x*x for x, y in pairs)-a*a/n
    bb = sum(y*y for x, y in pairs)-b*b/n
    ab = sum(x*y for x, y in pairs)-a*b/n
    rho = float(ab) / math.sqrt(float(aa*bb)) if aa > 0 and bb > 0 else None
    return n, float(a/n), float(b/n), rho


def controls():
    checks = []
    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
    def at(s, t, m, v=None, **kw):
        kw.setdefault("minimum_count", 2)
        kw.setdefault("minimum_coverage", 0)
        return pearson_surface(s, t, m, v, shifts=[(0, 0)], **kw)[0]
    pad = pearson_surface([[3, 5, 9]], [[999, 3, 5]], [[1, 1, 1]],
                          shifts=[(0, -1)], minimum_count=2,
                          minimum_coverage=2/3)[0]
    check("padding_overlap_mean_not_global", pad["n"] == 2 and
          pad["template_mean"] == 4 and pad["source_mean"] == 4 and
          math.isclose(pad["rho"], 1, abs_tol=1e-14))
    check("coverage_uses_full_template_mask", pad["coverage"] == 2/3)
    hole = at([[1, 400, 3, 5]], [[1, 2, 3]], [[1, 1, 1]], [[1, 0, 1, 1]])
    check("source_valid_hole_excluded", hole["n"] == 2 and hole["source_mean"] == 2)
    check("flat_template_rejected", at([[1, 2], [3, 4]], [[2, 2], [2, 2]],
                                      [[1, 1], [1, 1]])["rejection"] == "variance")
    check("flat_source_rejected", at([[2, 2], [2, 2]], [[1, 2], [3, 4]],
                                    [[1, 1], [1, 1]])["rejection"] == "variance")
    check("empty_mask_rejected", at([[1, 2]], [[1, 2]], [[0, 0]])[
        "rejection"] == "empty_mask")
    check("count_gate", at([[1, 2]], [[1, 2]], [[1, 1]], minimum_count=3)[
        "rejection"] == "minimum_count")
    check("coverage_gate", at([[1, 2]], [[1, 2]], [[1, 1]], [[1, 0]],
                              minimum_count=1, minimum_coverage=.85)[
        "rejection"] == "minimum_coverage")
    near = at([[0, 2e-5]], [[0, 2e-5]], [[1, 1]])
    check("small_population_variance_rejected", near["rejection"] == "variance")
    boundary = at([[0, 2]], [[0, 2]], [[1, 1]], variance_floor=1)
    check("positive_variance_equal_floor_accepted", boundary["rejection"] is None
          and math.isclose(boundary["rho"], 1, abs_tol=1e-14))
    repeated = [[(y+x) % 2 for x in range(8)] for y in range(6)]
    tiled = pearson_surface(repeated, [[0, 1], [1, 0]], [[1, 1], [1, 1]],
                           minimum_count=4, minimum_coverage=1)
    aliases = sum(r["rho"] is not None and r["rho"] > 1-1e-14 for r in tiled)
    check("repeated_grid_multiple_perfect_aliases", aliases > 1)
    t = [[1, 7, 2], [9, 3, 5], [2, 8, 4], [5, 1, 9]]
    s = t[:2] + [[10-x for x in r] for r in t[2:]]
    static = [[1]*3]*2 + [[0]*3]*2
    dynamic = [[0]*3]*2 + [[1]*3]*2
    check("changed_dynamic_does_not_change_static_fit",
          math.isclose(at(s, t, static)["rho"], 1, abs_tol=1e-14))
    check("dynamic_region_exposes_different_content",
          math.isclose(at(s, t, dynamic)["rho"], -1, abs_tol=1e-14))
    rng = random.Random(20260913)
    compared = 0
    max_error = 0.0
    random_ok = True
    for unused in range(64):
        sh, sw, th, tw = [rng.randint(1, 7) for j in range(4)]
        s = [[rng.randint(-20, 20) for x in range(sw)] for y in range(sh)]
        t = [[rng.randint(-20, 20) for x in range(tw)] for y in range(th)]
        m = [[rng.random() < .7 for x in range(tw)] for y in range(th)]
        v = [[rng.random() < .8 for x in range(sw)] for y in range(sh)]
        rows = pearson_surface(s, t, m, v, minimum_count=1,
                               minimum_coverage=0, variance_floor=0)
        for row in rows:
            n, sm, tm, rho = _fraction_expected(s, t, m, v, row["dy"], row["dx"])
            random_ok &= row["n"] == n
            random_ok &= row["source_mean"] == sm and row["template_mean"] == tm
            random_ok &= (row["raw_rho"] is None) == (rho is None)
            if rho is not None:
                error = abs(row["raw_rho"]-rho)
                max_error = max(max_error, error)
                random_ok &= error <= 2e-14
            compared += 1
    check("64_random_surfaces_match_exact_rational_raw_moments", random_ok)
    failures = 0
    for bad in ([[1, float("nan")]], [[1, float("inf")]]):
        try:
            at(bad, [[1, 2]], [[1, 1]])
        except ValueError:
            failures += 1
    check("nonfinite_source_rejected", failures == 2)
    try:
        at([[1, 2]], [[1, 2]], [[1, .5]])
        rejected = False
    except ValueError:
        rejected = True
    check("nonbinary_mask_rejected", rejected)
    return {"status": "passed" if all(c["passed"] for c in checks) else "failed",
            "controls": checks, "control_count": len(checks),
            "random_surface_count": 64, "random_offsets_compared": compared,
            "random_max_rho_error": max_error, "repeated_grid_alias_count": aliases,
            "scope": "synthetic direct arithmetic only; no producer or historical inputs"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", action="store_true", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = controls()
    receipt.update(code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   python=sys.version, argv=sys.argv)
    body = json.dumps(receipt, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(body)
    print(body, end="")
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
