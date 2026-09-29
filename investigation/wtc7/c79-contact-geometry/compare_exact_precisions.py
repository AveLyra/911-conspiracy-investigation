#!/usr/bin/env python3
"""Same-author certificate consistency/nesting check; not an independent solver."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
PINS = {
    "exact-proximity80.json": "25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324",
    "exact-proximity80.npz": "79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628",
    "exact-proximity80-proofs.json": "53757ba19edeeacf7ec64222786344977cb02eef5d54d7da2cbae0445e4bd2e6",
    "exact-proximity120.json": "ec72208fb65f7a849efebae77af5c834c4eb17e1180dddca2f1a17fb525d0711",
    "exact-proximity120.npz": "79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628",
    "exact-proximity120-proofs.json": "f653b0d0d4e69bfd42a79bb1321e540c4a18a92bdaa99efd3540bccc13fe80e7",
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def frac(x):
    return F(int(x[0]), int(x[1]))


def interval(x):
    return None if x is None else tuple(map(frac, x))


def run():
    for name, expected in PINS.items():
        assert digest(HERE/name) == expected, "input_pin"
    a, b = [json.loads((HERE/f"exact-proximity{k}-proofs.json").read_bytes()) for k in (80, 120)]
    assert a["constants"] == b["constants"]
    assert len(a["rows"]) == len(b["rows"]) == 11292
    assert len(a["geometry"]) == len(b["geometry"]) == 2226
    epsilon = frac(a["constants"]["epsilon"])
    counts = {"nested_intervals": 0, "root_enclosures": 0, "exact_classes_checked": 0, "patch_formulas_checked": 0}

    def nested(x, y):
        xx, yy = interval(x), interval(y)
        if xx is None or yy is None:
            assert xx is None and yy is None
        else:
            assert xx[0] <= yy[0] <= yy[1] <= xx[1]
            counts["nested_intervals"] += 1

    def root_check(x, squared):
        lo, hi = interval(x)
        assert 0 <= lo <= hi and lo*lo <= squared <= hi*hi
        counts["root_enclosures"] += 1

    gm = []
    for proof in (a, b):
        gm.append({(g["setting"], g["master"]): g for g in proof["geometry"]})
    for ga, gb in zip(a["geometry"], b["geometry"]):
        for key in ("setting", "master", "corners", "w_squared", "original_diagonal_squared"):
            assert ga[key] == gb[key]
        for key in ("w", "shorter_diagonal"):
            nested(ga[key], gb[key])
        assert frac(gb["global_slab_gate_upper"]) <= frac(ga["global_slab_gate_upper"])
        for g in (ga, gb):
            root_check(g["w"], frac(g["w_squared"]))
            root_check(g["shorter_diagonal"], min(map(frac, g["original_diagonal_squared"])))
    with np.load(HERE/"exact-proximity80.npz", allow_pickle=False) as npz:
        assert npz["pairs"].shape == (11292, 6)
        numeric_identities = npz["pairs"][:, :4].tolist()
    for i, (ra, rb) in enumerate(zip(a["rows"], b["rows"])):
        assert ra["row"] == rb["row"] == numeric_identities[i]
        for key in ("dA_squared", "dB_squared", "box_squared"):
            assert ra[key] == rb[key]
        for key in ("dA", "dB", "patch", "delta_low", "delta_high"):
            nested(ra[key], rb[key])
        for x, y in zip(ra["signed_planes"], rb["signed_planes"]):
            nested(x, y)
        for precision_index, r in enumerate((ra, rb)):
            root_check(r["dA"], frac(r["dA_squared"]))
            root_check(r["dB"], frac(r["dB_squared"]))
            lo, hi = interval(r["patch"])
            da, db = interval(r["dA"]), interval(r["dB"])
            w = interval(gm[precision_index][tuple(r["row"][:2])]["w"])
            assert lo == max(0, da[0]-w[1], db[0]-w[1])
            assert hi == min(da[1]+w[1], db[1]+w[1]) and lo <= hi
            counts["patch_formulas_checked"] += 1
            dl, dh = interval(r["delta_low"]), interval(r["delta_high"])
            if dl is None:
                assert dh is None
                expected_class = 0
            else:
                assert 0 <= dl[0] <= dl[1] and dl[0] <= dh[0] <= dh[1]
                expected_class = 3 if hi < dl[0]-epsilon else 1 if lo > dh[1]+epsilon else 2
            assert r["row"][3] == expected_class
            counts["exact_classes_checked"] += 1
    for name, expected in PINS.items():
        assert digest(HERE/name) == expected, "input_changed"
    return {"status": "passed", "rows_per_precision": 11292, "geometry_per_precision": 2226,
            "npz_files_byte_identical": True, **counts,
            "scope": "Same-author internal certificate consistency and nesting; no independent geometric distance recalculation or physical/solver validation.",
            "pins": PINS, "producer_sha256": digest(Path(__file__))}


if __name__ == "__main__":
    destination = HERE/"exact-precision-comparison01.json"
    with destination.open("x") as f:
        try:
            result = run()
        except Exception as error:
            result = {"status": "failed", "error_type": type(error).__name__, "pins": PINS, "producer_sha256": digest(Path(__file__))}
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("pins", "scope")}))
    sys.exit(0 if result["status"] == "passed" else 1)
