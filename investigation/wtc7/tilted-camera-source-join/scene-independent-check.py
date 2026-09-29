#!/usr/bin/env python3
"""Independent image-content arithmetic; no root imports or video decoding."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import PIL
from PIL import Image

UNIT = Path(__file__).resolve().parent
PINS = {
    "PROTOCOL.md": "0bec10bef245cf59d62800dce2c67913da62b90cbb8b42a42d9d9ce2555614e1",
    "SCENE-ADDENDUM.md": "f54b1eac8df8d069806ba60df36865ce0dcda2c52f163963e28b6059e5d3777d",
    "candidates01/selection.json": "360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552",
    "views01/receipt.json": "4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29",
}
RECTS = {
    "full": (32, 16, 632, 464),
    "left": (40, 270, 300, 460),
    "right": (500, 160, 630, 320),
    "target": (280, 70, 480, 320),
}
COUNTS = {"full": 16800, "left": 3055, "right": 1320, "target": 3100}
BRANCHES = ("NEAREST", "BILINEAR", "BOX")
QUERY_INDICES = (0, 67, 135, 203, 271, 339, 407, 475)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pinned_bytes():
    result = {}
    for name, expected in PINS.items():
        data = (UNIT / name).read_bytes()
        if sha(data) != expected:
            raise RuntimeError(f"pinned source changed: {name}")
        result[name] = data
    return result


def mask_coordinates(rect):
    x0, y0, x1, y1 = rect
    points = [(y, x) for y in range(0, 480, 4) for x in range(0, 640, 4)
              if x0 <= x < x1 and y0 <= y < y1]
    return np.array([p[0] for p in points]), np.array([p[1] for p in points])


def resize_query(native, branch):
    if native.dtype != np.uint8 or native.shape != (480, 720):
        raise ValueError("query must be native 720x480 uint8")
    return np.asarray(Image.fromarray(native).resize((640, 480),
                      resample=getattr(Image.Resampling, branch)), dtype=np.uint8)


def scalar_pair(xs, ys):
    """Python integer control oracle, independent of the historical array path."""
    x, y = list(map(int, xs)), list(map(int, ys))
    n = len(x)
    assert n == len(y) and n > 0
    sx, sy = sum(x), sum(y)
    vx = n * sum(v*v for v in x) - sx*sx
    vy = n * sum(v*v for v in y) - sy*sy
    cov = n * sum(a*b for a, b in zip(x, y)) - sx*sy
    return sum(abs(a-b) for a, b in zip(x, y)), (
        cov / math.sqrt(vx*vy) if vx and vy else None)


def matrix_scores(candidates, query):
    """Integer sums/product correlation; no centered floating point vectors."""
    x = np.asarray(candidates, dtype=np.int64)
    y = np.asarray(query, dtype=np.int64)
    n = y.size
    assert x.ndim == 2 and x.shape[1] == n and n > 0
    assert np.all((x >= 0) & (x <= 255)) and np.all((y >= 0) & (y <= 255))
    sx = x.sum(axis=1, dtype=np.int64)
    sy = int(y.sum(dtype=np.int64))
    sxx = np.einsum("ij,ij->i", x, x, dtype=np.int64)
    syy = int(np.dot(y, y))
    sxy = np.dot(x, y)
    vx = n*sxx - sx*sx
    vy = n*syy - sy*sy
    cov = n*sxy - sx*sy
    sad = np.abs(x-y).sum(axis=1, dtype=np.int64)
    assert n*n*255*255 < np.iinfo(np.int64).max
    assert np.all(vx >= 0) and vy >= 0
    corr = [int(c)/math.sqrt(int(v)*vy) if int(v) and vy else None
            for c, v in zip(cov, vx)]
    return {"n": n, "mae_numerator": sad.tolist(),
            "mae": (sad / n).tolist(), "correlation": corr,
            "candidate_sum": sx.tolist(), "candidate_squares_sum": sxx.tolist(),
            "query_sum": sy, "query_squares_sum": syy,
            "cross_products_sum": sxy.tolist(),
            "covariance_integer": cov.tolist(),
            "candidate_variance_integer": vx.tolist(),
            "query_variance_integer": vy}


def ranking(numerators, indices):
    order = sorted(range(len(indices)), key=lambda p: (numerators[p], indices[p]))
    low = numerators[order[0]]
    best = indices[order[0]]
    return {"order": [indices[p] for p in order], "minimum_index": best,
            "minimum_numerator": low,
            "minimum_ties": sorted(indices[p] for p in order if numerators[p] == low),
            "runner_up_index": indices[order[1]],
            "runner_up_numerator": numerators[order[1]],
            "gap_numerator": numerators[order[1]]-low,
            "boundary_minimum": best in (indices[0], indices[-1])}


def controls():
    done = []
    vectors = [([0, 1, 4, 7], [0, 1, 4, 7], 0, 1.0),
               ([20, 21, 24, 27], [0, 1, 4, 7], 80, 1.0),
               ([0, 1, 4, 7], [20, 21, 24, 27], 80, 1.0),
               ([0, 1, 4, 8], [0, 1, 4, 7], 1, None),
               ([4, 4, 4, 4], [4, 4, 4, 4], 0, None),
               ([5, 5, 5, 5], [0, 1, 4, 7], 12, None),
               ([255, 0], [0, 255], 510, -1.0)]
    names = ["exact_copy", "positive_brightness", "negative_brightness",
             "localized_content", "both_constant", "one_constant", "uint8_subtraction"]
    for name, (x, y, expected_sad, expected_corr) in zip(names, vectors):
        out = matrix_scores(np.array([x], dtype=np.uint8), np.array(y, dtype=np.uint8))
        sad, corr = scalar_pair(x, y)
        assert out["mae_numerator"] == [sad] == [expected_sad]
        assert out["correlation"] == [corr]
        if name != "localized_content":
            assert corr == expected_corr
        else:
            assert corr is not None and corr < 1
        done.append(name)
    tie = ranking([0, 0, 3, 0], [11, 7, 9, 20])
    assert tie["minimum_index"] == 7 and tie["minimum_ties"] == [7, 11, 20]
    assert tie["runner_up_index"] == 11 and tie["gap_numerator"] == 0
    done.append("repeated_tie_lowest_source_index")
    for name, rect in RECTS.items():
        yy, xx = mask_coordinates(rect)
        assert len(xx) == COUNTS[name] and np.all(xx % 4 == 0) and np.all(yy % 4 == 0)
        assert len(set(zip(yy, xx))) == COUNTS[name]
        assert all(rect[0] <= x < rect[2] and rect[1] <= y < rect[3] for y, x in zip(yy, xx))
        if name in ("left", "target"):
            assert yy.min() == (272 if name == "left" else 72)
    done.append("all_global_grid_mask_membership")
    row_pattern = np.broadcast_to((np.arange(480) % 256).astype(np.uint8)[:, None], (480, 720)).copy()
    for branch in BRANCHES:
        got = resize_query(row_pattern, branch)
        assert got.shape == (480, 640)
        assert np.array_equal(got, row_pattern[:, :640])
        ramp = np.broadcast_to((np.arange(720) % 256).astype(np.uint8)[None, :], (480, 720)).copy()
        transformed = resize_query(ramp, branch)
        assert np.all(transformed == transformed[0])
        if branch == "NEAREST":
            lookup = np.floor((np.arange(640)+0.5)*720/640).astype(int)
            assert np.array_equal(transformed[0], ramp[0, lookup])
        done.append("width_only_resize_"+branch)
    return {"passed": len(done), "controls": done,
            "historical_pixels_read_before_controls": False}


def read_image(path, identity, luma_sha, size):
    data = path.read_bytes()
    assert len(data) == identity["bytes"] and sha(data) == identity["sha256"], path.name
    with Image.open(io.BytesIO(data)) as im:
        assert im.format == "PNG" and im.mode == "L" and im.size == size, path.name
        pixels = np.asarray(im).copy()
    assert sha(pixels.tobytes()) == luma_sha, path.name
    return pixels


def historical(test_record):
    source_data = pinned_bytes()
    candidates_manifest = json.loads(source_data["candidates01/selection.json"])
    queries_manifest = json.loads(source_data["views01/receipt.json"])
    cs, qs = candidates_manifest["images"], queries_manifest["selected"]
    indices = [int(c["frame_index_zero_based"]) for c in cs]
    assert indices == list(range(6500, 7201))
    assert [q["index"] for q in qs] == list(QUERY_INDICES)
    assert candidates_manifest["geometry"] == [640, 480] and queries_manifest["geometry"] == [720, 480]
    assert candidates_manifest["checked_frames"] == 8042 and candidates_manifest["exit_code"] == 0
    coords = {key: mask_coordinates(rect) for key, rect in RECTS.items()}
    matrices = {key: [] for key in RECTS}
    for c in cs:
        assert c["png"] == f"f{int(c['frame_index_zero_based']):06d}.png"
        pixels = read_image(UNIT/"candidates01"/c["png"], c["png_identity"], c["luma_sha256"], (640, 480))
        for key, (yy, xx) in coords.items():
            matrices[key].append(pixels[yy, xx])
    matrices = {key: np.asarray(rows, dtype=np.int64) for key, rows in matrices.items()}
    results = []
    for q in qs:
        assert q["png"] == f"frame-{q['index']:04d}.png"
        native = read_image(UNIT/"views01"/q["png"], q, q["luma_sha256"], (720, 480))
        for branch in BRANCHES:
            resized = resize_query(native, branch)
            row = {"query_index": q["index"], "branch": branch,
                   "resized_luma_sha256": sha(resized.tobytes()), "regions": {}}
            for key, (yy, xx) in coords.items():
                out = matrix_scores(matrices[key], resized[yy, xx])
                out["ranking"] = ranking(out["mae_numerator"], indices)
                out["ranking"]["gap_mae"] = out["ranking"]["gap_numerator"]/out["n"]
                row["regions"][key] = out
            results.append(row)
    pinned_bytes()
    sequences = {}
    for branch in BRANCHES:
        selected = [r["regions"]["full"]["ranking"]["minimum_index"] for r in results if r["branch"] == branch]
        sequences[branch] = {"indices": selected,
                             "strictly_increasing": all(a < b for a,b in zip(selected, selected[1:])),
                             "nondecreasing": all(a <= b for a,b in zip(selected, selected[1:]))}
    return {"schema": "independent-scene-arithmetic-v1", "method": "integer SAD and covariance identity",
            "source_pins": PINS, "source_manifests_rechecked": True,
            "script_sha256": sha(Path(__file__).read_bytes()),
            "runtime": {"python": platform.python_version(), "pillow": PIL.__version__, "numpy": np.__version__},
            "controls": test_record, "candidate_indices": indices,
            "source_candidates": cs, "source_queries": qs,
            "regions": {k: {"rectangle": list(v), "grid_origin": [0,0], "stride": 4,
                               "count": COUNTS[k]} for k,v in RECTS.items()},
            "comparisons_mae": len(cs)*len(qs)*len(BRANCHES)*len(RECTS),
            "comparisons_correlation": len(cs)*len(qs)*len(BRANCHES)*len(RECTS),
            "sequences": sequences, "scores": results,
            "root_comparison": "not read in this independent calculation"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    test_record = controls()
    if args.controls_only:
        print(json.dumps(test_record, sort_keys=True))
        return
    if args.output is None or args.output.resolve().parent != UNIT or args.output.name not in (
            "scene-independent01.json", "scene-independent02.json"):
        parser.error("choose one of the two owned independent output files in this unit")
    report = historical(test_record)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": args.output.name, "sha256": sha(args.output.read_bytes()),
                      "controls": test_record["passed"], "comparisons": report["comparisons_mae"],
                      "sequences": report["sequences"]}, sort_keys=True))


if __name__ == "__main__":
    main()
