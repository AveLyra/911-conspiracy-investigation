#!/usr/bin/env python3
"""Independent exact-rational evaluation of the declared geometric surrogate.

No raw-source reader and no import of either floating proximity implementation.
All authored outputs are create-only. Rational proof endpoints are authoritative;
float arrays are display views. This program does not initialize solver contact.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import tempfile
import time

import numpy as np

HERE = Path(__file__).resolve().parent
PINS = {
    "EXACT-ARITHMETIC-ADDENDUM.md": "b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89",
    "GEOMETRIC-METHOD.md": "73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e",
    "GEOMETRIC-IMPLEMENTATION-ADDENDUM.md": "ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd",
    "stage-root01.json": "deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963",
    "stage-root01.npz": "2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf",
    "proximity-root01.json": "d2201fcd1f0c36f3240a32813b01ec1c8b90f44d019ac0cbb93ce54a99e5f6cc",
    "proximity-root01.npz": "b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca",
    "independent-proximity01.json": "cc50ea1607ee4875610fdd7cdae62e22dc5e423eb776842849f1e6199217543c",
    "independent-proximity01.npz": "26a9c9421e37c38e96e7568bb0521763b0cd0e621a12e7e101f8a9b411a2bef5",
}
TRIS = ((0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3))
ZERO = F(0)
ONE = F(1)


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def pin_check(path, expected):
    actual = digest(path)
    require(actual == expected, "pin_mismatch")
    return actual


def pins():
    return {name: pin_check(HERE / name, value) for name, value in PINS.items()}


def rat(value):
    value = float(value)
    require(math.isfinite(value), "nonfinite_rational_input")
    return F(*value.as_integer_ratio())


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), ZERO)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def squared(a):
    return dot(a, a)


def root_interval(x, bits):
    require(x >= 0, "negative_root")
    scale = 1 << bits
    numerator = x.numerator << (2*bits)
    n = math.isqrt(numerator // x.denominator)
    lo = F(n, scale)
    hi = lo if n*n*x.denominator == numerator else F(n+1, scale)
    require(lo*lo <= x <= hi*hi, "root_enclosure_failure")
    return lo, hi


def outward_float(x, upper):
    try:
        f = float(x)
    except OverflowError:
        f = math.inf if x >= 0 else -math.inf
    if math.isinf(f):
        # Infinite search endpoints are allowed only as conservative sentinels.
        if (upper and f > 0) or (not upper and f < 0):
            return f
        f = math.nextafter(f, 0.0)
    while (rat(f) < x if upper else rat(f) > x):
        f = math.nextafter(f, math.inf if upper else -math.inf)
    require(rat(f) >= x if upper else rat(f) <= x, "outward_conversion_failure")
    return f


def extend(corners, e):
    h = (e-ONE)/2
    result = []
    for u, v in ((-h, -h), (ONE+h, -h), (ONE+h, ONE+h), (-h, ONE+h)):
        weights = ((ONE-u)*(ONE-v), u*(ONE-v), u*v, (ONE-u)*v)
        result.append(tuple(sum((weights[j]*corners[j][k] for j in range(4)), ZERO) for k in range(3)))
    return tuple(result)


def prepare_triangle(vertices):
    n = cross(sub(vertices[1], vertices[0]), sub(vertices[2], vertices[0]))
    edges = tuple((vertices[i], sub(vertices[(i+1) % 3], vertices[i])) for i in range(3))
    return vertices[0], n, squared(n), tuple((a, d, squared(d)) for a, d in edges)


def triangle_squared(point, triangle):
    a, n, n2, edges = triangle
    distances = []
    signs = []
    for start, edge, length2 in edges:
        q = sub(point, start)
        t = max(ZERO, min(ONE, dot(q, edge)/length2)) if length2 else ZERO
        distances.append(squared(tuple(q[k]-t*edge[k] for k in range(3))))
        if n2:
            # Normal translation does not change these oriented triple products.
            signs.append(dot(cross(edge, q), n))
    if not n2:
        return min(distances), -1, None
    inside = int(all(s >= 0 for s in signs))
    numerator = dot(sub(point, a), n)
    plane2 = numerator*numerator/n2
    if inside:
        distances.append(plane2)
    return min(distances), inside, (numerator, n2)


def signed_interval(plane, bits):
    if plane is None:
        return None
    numerator, n2 = plane
    lo, hi = root_interval(numerator*numerator/n2, bits)
    return (-hi, -lo) if numerator < 0 else (lo, hi)


def patch_intervals(point, triangles, w_interval, bits):
    entries = [triangle_squared(point, t) for t in triangles]
    a2, b2 = min(entries[0][0], entries[1][0]), min(entries[2][0], entries[3][0])
    da, db = root_interval(a2, bits), root_interval(b2, bits)
    wl, wh = w_interval
    lower = max(ZERO, da[0]-wh, db[0]-wh)
    upper = min(da[1]+wh, db[1]+wh)
    require(lower <= upper, "exact_enclosure_inverted")
    return (lower, upper), da, db, a2, b2, [x[1] for x in entries], [signed_interval(x[2], bits) for x in entries]


def thresholds(slave, master, diag_interval, c6, c5):
    low = c6*(slave[0]+master[0])
    high = c6*(slave[1]+master[1])
    dl = (max(low, c5*diag_interval[0]), max(low, c5*diag_interval[1]))
    dh = (max(high, c5*diag_interval[0]), max(high, c5*diag_interval[1]))
    require(ZERO <= dl[0] <= dl[1] and dl[0] <= dh[0] <= dh[1], "threshold_order")
    return dl, dh


def classify(bounds, dl, dh, epsilon):
    if dl is None:
        return 0
    require(bounds[0] <= bounds[1], "classification_enclosure_inverted")
    if bounds[1] < dl[0]-epsilon:
        return 3
    if bounds[0] > dh[1]+epsilon:
        return 1
    return 2


def bbox(corners):
    return tuple(min(p[k] for p in corners) for k in range(3)), tuple(max(p[k] for p in corners) for k in range(3))


def box_squared(point, box):
    lo, hi = box
    return sum((max(lo[k]-point[k], ZERO, point[k]-hi[k])**2 for k in range(3)), ZERO)


def slab_candidates(coords, sorted_axes, box, gate):
    ranges = []
    for k in range(3):
        lo = outward_float(box[0][k]-gate, False)
        hi = outward_float(box[1][k]+gate, True)
        order, values = sorted_axes[k]
        left = np.searchsorted(values, lo, side="left")
        right = np.searchsorted(values, hi, side="right")
        ranges.append(order[left:right])
    result = min(ranges, key=len)
    for other in ranges:
        result = np.intersect1d(result, other, assume_unique=True)
    return result


def encode_fraction(x):
    return [str(x.numerator), str(x.denominator)]


def encode_interval(x):
    return None if x is None else [encode_fraction(v) for v in x]


def view_interval(x):
    return math.nan if x is None else float((x[0]+x[1])/2)


def controls():
    passed = []
    for bits in (80, 120):
        for x in (F(0), F(1), F(4), F(2), F(1, 7), F(1, 1 << 400)):
            lo, hi = root_interval(x, bits)
            require(lo*lo <= x <= hi*hi, "control_root")
        require(root_interval(F(4), bits) == (F(2), F(2)), "control_perfect_root")
    passed.append("perfect_inexact_and_subprecision_roots")
    for x in (F(1, 3), -F(1, 3), F(0), F(1, 1 << 1100), -F(1, 1 << 1100)):
        require(rat(outward_float(x, False)) <= x <= rat(outward_float(x, True)), "control_outward")
    passed.append("signed_and_underflow_outward_conversion")
    tri = tuple(tuple(F(x) for x in p) for p in ((0, 0, 0), (1, 0, 0), (0, 1, 0)))
    for point, expected in (((F(1, 4), F(1, 4), F(2)), F(4)), ((F(1), F(1), F(0)), F(1, 2)), ((F(2), F(0), F(0)), F(1))):
        require(triangle_squared(point, prepare_triangle(tri))[0] == expected, "control_triangle")
        require(triangle_squared(point, prepare_triangle(tuple(reversed(tri))))[0] == expected, "control_winding")
    passed.append("interior_edge_vertex_and_reversed_winding")
    deg = ((F(0),)*3, (F(0),)*3, (F(1), F(0), F(0)))
    answer = triangle_squared((F(1, 2), F(1), F(0)), prepare_triangle(deg))
    require(answer == (F(1), -1, None), "control_degenerate")
    passed.append("zero_edge_zero_area_undefined_plane")
    quad = ((ZERO, ZERO, ZERO), (ONE, ZERO, ZERO), (ONE, ONE, ONE), (ZERO, ONE, ZERO))
    for e in (F(1), rat(1.006), rat(1.025)):
        ext = extend(quad, e)
        mixed = tuple(ext[0][k]-ext[1][k]+ext[2][k]-ext[3][k] for k in range(3))
        require(squared(mixed) == e**4, "control_extension_scaling")
        for u, v in ((F(0), F(0)), (F(1, 2), F(1, 2)), (F(1, 4), F(3, 4))):
            p = tuple(sum((weight*ext[j][k] for j, weight in enumerate(((1-u)*(1-v), u*(1-v), u*v, (1-u)*v))), ZERO) for k in range(3))
            ts = [prepare_triangle(tuple(ext[i] for i in ind)) for ind in TRIS]
            out = patch_intervals(p, ts, root_interval(squared(mixed)/16, 80), 80)
            require(out[0][0] == 0 and box_squared(p, bbox(ext)) == 0, "control_patch_zero")
    passed.append("warped_known_patch_points_and_extension_scaling")
    flat = tuple((p[0], p[1], ZERO) for p in quad)
    p = (F(1001, 1000), F(1, 2), ZERO)
    require(box_squared(p, bbox(flat)) > 0 and box_squared(p, bbox(extend(flat, rat(1.006)))) == 0, "control_extension_only")
    passed.append("extension_only_admission")
    coords = np.asarray([[-1., 0., 0.], [0., 0., 0.], [.5, .5, 0.], [1.01, .5, 0.], [3., 3., 3.]])
    sorts = [(np.argsort(coords[:, k], kind="stable"), np.sort(coords[:, k], kind="stable")) for k in range(3)]
    for e in (rat(1.), rat(1.006), rat(1.025)):
        bx, gate = bbox(extend(flat, e)), F(1, 100)
        candidates = set(map(int, slab_candidates(coords, sorts, bx, gate)))
        brute = {i for i, p in enumerate(coords) if box_squared(tuple(map(rat, p)), bx) <= gate*gate}
        require(brute <= candidates, "control_slab_coverage")
        after = {i for i in candidates if box_squared(tuple(map(rat, coords[i])), bx) <= gate*gate}
        require(after == brute, "control_exact_box_coverage")
    passed.append("complete_synthetic_slab_and_exact_box_coverage")
    require(classify((F(2), F(1)), None, None, F(1, 100)) == 0, "control_unknown_priority")
    require(classify((F(0), F(1)), (F(1), F(1)), (F(2), F(2)), ZERO) == 2, "control_boundary")
    require(classify((ZERO, ZERO), (ONE, ONE), (ONE, ONE), ZERO) == 3, "control_inside")
    require(classify((F(3), F(3)), (ONE, ONE), (F(2), F(2)), ZERO) == 1, "control_outside")
    passed.append("unknown_priority_strict_gates_and_overlap")
    try:
        rat(math.nan)
        raise AssertionError("nonfinite_not_rejected")
    except ValueError:
        pass
    passed.append("nonfinite_input_rejection")
    with tempfile.TemporaryDirectory(prefix="exact-proximity-controls-", dir="/private/tmp") as directory:
        path = Path(directory)/"synthetic"
        with path.open("x") as f:
            f.write("synthetic")
        try:
            path.open("x")
            raise AssertionError("create_guard_failed")
        except FileExistsError:
            pass
        try:
            pin_check(path, "0"*64)
            raise AssertionError("pin_guard_failed")
        except ValueError:
            pass
    passed.append("create_only_and_pin_mutation_guards")
    return passed


def evaluate(bits, start):
    stage = json.loads((HERE/"stage-root01.json").read_text())["result"]
    saved = json.loads((HERE/"proximity-root01.json").read_text())
    epsilon = rat(saved["result"]["epsilon"])
    c6, c5 = rat(.6), rat(.05)
    settings = tuple(map(rat, (1., 1.006, 1.025)))
    with np.load(HERE/"stage-root01.npz", allow_pickle=False) as f:
        node_ids, xyz = f["node_ids"], f["xyz"]
        roles, thick = f["roles"], f["corner_thickness_min_max"]
        incidence = f["node_part_incidence"]
    require(np.all(np.isfinite(xyz)) and np.all(node_ids[1:] > node_ids[:-1]), "node_schema")
    require(xyz.shape == (len(node_ids), 3) and thick.shape == (len(node_ids), 2), "node_shapes")
    require(np.array_equal(np.isnan(thick[:, 0]), np.isnan(thick[:, 1])), "unknown_thickness_schema")
    finite = ~np.isnan(thick[:, 0])
    require(np.all(np.isfinite(thick[finite])) and np.all(thick[finite] >= 0) and np.all(thick[finite, 0] <= thick[finite, 1]), "thickness_schema")
    node_index = {int(n): i for i, n in enumerate(node_ids)}
    point_cache, thickness_cache = {}, {}

    def point(i):
        if i not in point_cache:
            point_cache[i] = tuple(map(rat, xyz[i]))
        return point_cache[i]

    def thickness(i):
        if not finite[i]:
            return None
        if i not in thickness_cache:
            thickness_cache[i] = tuple(map(rat, thick[i]))
        return thickness_cache[i]

    masters = stage["master_segments"]
    identities, master_nodes, master_thickness, original, diagonal2 = [], [], [], [], []
    for m in masters:
        cid = {1: 1, 3: 2}[m["set_id"]]
        identities.append((cid, m["set_id"], m["line"]))
        master_nodes.append(m["nodes"])
        pp = tuple(point(node_index[int(n)]) for n in m["nodes"])
        require(pp == tuple(tuple(map(rat, p)) for p in m["xyz"]), "master_coordinate_mismatch")
        original.append(pp)
        require(bool(m["aliases"]), "missing_master_alias")
        supplied = [rat(t) for alias in m["aliases"] for t in alias["thickness_card"][:4]]
        require(all(t >= 0 for t in supplied), "negative_master_thickness")
        master_thickness.append((min(supplied), max(supplied)))
        diagonal2.append((squared(sub(pp[0], pp[2])), squared(sub(pp[1], pp[3]))))
    identities = np.asarray(identities, dtype=np.int64)
    master_nodes = np.asarray(master_nodes, dtype=np.int64)
    populations, sorted_axes, maximum_slave, unknowns, masks, master_orders = {}, {}, {}, {}, {}, {}
    for cid in (1, 2):
        indices = np.flatnonzero(roles[:, cid-1])
        populations[cid] = indices
        coords = xyz[indices]
        sorted_axes[cid] = []
        for axis in range(3):
            order = np.argsort(coords[:, axis], kind="stable")
            sorted_axes[cid].append((order, coords[order, axis]))
        known = finite[indices]
        require(known.any(), "no_known_thickness_population")
        maximum_slave[cid] = rat(np.max(thick[indices[known], 1]))
        unknowns[cid] = np.flatnonzero(~known)
        master_orders[cid] = np.flatnonzero(identities[:, 0] == cid)
        masks[cid] = np.zeros((len(settings), len(master_orders[cid]), (len(indices)+7)//8), dtype=np.uint8)
    part_map = {}
    for nid, kind, pid, count in incidence:
        part_map.setdefault(int(nid), set()).add(int(pid))
    rows, views, projections, proofs, geometry_proofs = [], [], [], [], []
    coverage = np.zeros((len(settings), len(masters), 10), dtype=np.int64)
    geometry = np.empty((len(settings), len(masters), 4, 3), dtype=np.float64)
    w_views = np.empty((len(settings), len(masters)), dtype=np.float64)
    for si, e in enumerate(settings):
        for mi, m in enumerate(masters):
            require(time.monotonic()-start <= 7200, "time_cap")
            require(len(rows) <= 1000000, "admitted_pair_cap")
            cid = int(identities[mi, 0])
            local_master = int(np.searchsorted(master_orders[cid], mi))
            population = populations[cid]
            extended = extend(original[mi], e)
            bx = bbox(extended)
            mixed = tuple(extended[0][k]-extended[1][k]+extended[2][k]-extended[3][k] for k in range(3))
            w2 = squared(mixed)/16
            wi = root_interval(w2, bits)
            di = root_interval(min(diagonal2[mi]), bits)
            mt = master_thickness[mi]
            global_dh = max(c6*(maximum_slave[cid]+mt[1]), c5*di[1])
            gate = global_dh+epsilon
            slab = slab_candidates(xyz[population], sorted_axes[cid], bx, gate)
            candidates = np.union1d(slab, unknowns[cid])
            keep, box_state, th_state = [], {}, {}
            box_ambiguous = 0
            for local in candidates:
                local = int(local)
                i = int(population[local])
                box2 = box_squared(point(i), bx)
                st = thickness(i)
                if st is None:
                    dl = dh = None
                    keep.append(local)
                else:
                    dl, dh = thresholds(st, mt, di, c6, c5)
                    if box2 <= (dh[1]+epsilon)**2:
                        keep.append(local)
                        if box2 > (dh[0]+epsilon)**2:
                            box_ambiguous += 1
                box_state[local] = box2
                th_state[local] = (dl, dh)
            keep = np.asarray(keep, dtype=np.int64)
            bits_row = np.zeros(len(population), dtype=np.uint8)
            bits_row[keep] = 1
            masks[cid][si, local_master] = np.packbits(bits_row, bitorder="little")
            triangles = [prepare_triangle(tuple(extended[j] for j in inds)) for inds in TRIS]
            mpids = {int(a["pid"]) for a in m["aliases"]}
            counts = [0, 0, 0, 0]
            for local in keep:
                local = int(local)
                i = int(population[local]); nid = int(node_ids[i])
                bounds, da, db, a2, b2, flags, signed = patch_intervals(point(i), triangles, wi, bits)
                dl, dh = th_state[local]
                cls = classify(bounds, dl, dh, epsilon)
                counts[cls] += 1
                identity = [si, mi, nid, cls, int(nid in m["nodes"]), int(bool(part_map.get(nid, set()) & mpids))]
                rows.append(identity)
                views.append([view_interval(da), view_interval(db), float(bounds[0]), float(bounds[1]), view_interval(dl), view_interval(dh)] + [view_interval(x) for x in signed])
                projections.append(flags)
                proofs.append({"row": identity[:4], "dA_squared": encode_fraction(a2), "dB_squared": encode_fraction(b2),
                               "dA": encode_interval(da), "dB": encode_interval(db), "patch": encode_interval(bounds),
                               "delta_low": encode_interval(dl), "delta_high": encode_interval(dh),
                               "box_squared": encode_fraction(box_state[local]),
                               "signed_planes": [encode_interval(x) for x in signed]})
            coverage[si, mi] = [len(population), len(slab), len(candidates), len(keep), len(population)-len(keep), box_ambiguous, *counts]
            geometry[si, mi] = [[float(x) for x in p] for p in extended]
            w_views[si, mi] = view_interval(wi)
            geometry_proofs.append({"setting": si, "master": mi, "corners": [[encode_fraction(x) for x in p] for p in extended],
                                    "w_squared": encode_fraction(w2), "w": encode_interval(wi),
                                    "original_diagonal_squared": [encode_fraction(x) for x in diagonal2[mi]],
                                    "shorter_diagonal": encode_interval(di), "global_slab_gate_upper": encode_fraction(gate)})
            if mi % 100 == 0:
                print(json.dumps({"phase": "exact_geometry", "bits": bits, "setting": si, "master": mi, "admitted_processed": len(rows)}), flush=True)
    rows = np.asarray(rows, dtype=np.int64).reshape(-1, 6)
    admitted = np.unique(rows[:, 2])
    arrays = {"pairs": rows, "pair_values": np.asarray(views, dtype=np.float64).reshape(-1, 10),
              "pair_projection_inside": np.asarray(projections, dtype=np.int8).reshape(-1, 4),
              "coverage": coverage, "master_identity": identities, "master_nodes": master_nodes,
              "geometry_quad": geometry, "geometry_w": w_views,
              "settings": np.asarray([float(e) for e in settings]),
              "admitted_node_part_incidence": incidence[np.isin(incidence[:, 0], admitted)]}
    for cid in (1, 2):
        arrays[f"broad_mask_cid{cid}"] = masks[cid]
        arrays[f"slave_ids_cid{cid}"] = node_ids[populations[cid]]
    comparisons = {}
    for name, mask_names in (("proximity-root01.npz", ("broad_mask_cid1", "broad_mask_cid2")),
                             ("independent-proximity01.npz", ("CID1_admission_bits", "CID2_admission_bits"))):
        with np.load(HERE/name, allow_pickle=False) as old:
            require(np.array_equal(old["master_identity"], identities), "floating_master_order")
            entries = {}
            for cid, key in zip((1, 2), mask_names):
                if name.startswith("independent"):
                    old_ids = old["node_ids"][old[f"CID{cid}_slave_node_indices"]]
                else:
                    old_ids = old[f"slave_ids_cid{cid}"]
                require(np.array_equal(old_ids, arrays[f"slave_ids_cid{cid}"]), "floating_slave_order")
                om, nm = old[key], masks[cid]
                require(om.shape == nm.shape, "floating_mask_shape")
                added = int(np.unpackbits(np.bitwise_and(nm, np.bitwise_not(om)), bitorder="little").sum())
                removed = int(np.unpackbits(np.bitwise_and(om, np.bitwise_not(nm)), bitorder="little").sum())
                entries[str(cid)] = {"exact_added_memberships": added, "floating_only_memberships": removed, "equal": bool(np.array_equal(om, nm))}
            comparisons[name] = entries
    groups = []
    for si in range(3):
        for cid in (1, 2):
            select = (rows[:, 0] == si) & (identities[rows[:, 1], 0] == cid)
            rr = rows[select]
            groups.append({"setting_index": si, "cid": cid, "admitted": len(rr),
                           "classes": np.bincount(rr[:, 3], minlength=4).tolist(),
                           "unique_nodes_by_class": {str(k): int(len(np.unique(rr[rr[:, 3] == k, 2]))) for k in range(4)}})
    proof = {"precision_bits": bits, "constants": {"epsilon": encode_fraction(epsilon), "0.6": encode_fraction(c6), "0.05": encode_fraction(c5),
                                                        "settings": [encode_fraction(e) for e in settings]},
             "geometry": geometry_proofs, "rows": proofs}
    return arrays, proof, {"groups": groups, "floating_mask_comparisons": comparisons,
                           "coordinate_cache_nodes": len(point_cache), "proof_rows": len(proofs),
                           "total_population_memberships": int(coverage[:, :, 0].sum()),
                           "total_slab_candidates": int(coverage[:, :, 1].sum()),
                           "total_box_interval_ambiguities": int(coverage[:, :, 5].sum())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, choices=(80, 120), default=80)
    parser.add_argument("--output", required=True, help="Create-only output stem within this unit")
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    stem = Path(args.output).resolve()
    require(stem.parent == HERE, "output_outside_unit")
    paths = {"receipt": Path(str(stem)+".json"), "arrays": Path(str(stem)+".npz"), "proof": Path(str(stem)+"-proofs.json")}
    require(all(not p.exists() for p in paths.values()), "output_exists")
    start = time.monotonic()
    receipt = {"status": "running", "precision_bits": args.bits, "producer_sha256": digest(Path(__file__)),
               "python": sys.version.split()[0], "numpy": np.__version__, "command": ["exact_proximity.py", "--bits", str(args.bits), "--output", stem.name],
               "limits": {"seconds": 7200, "admitted_pairs": 1000000, "no_truncation": True}}
    with paths["receipt"].open("x") as output:
        try:
            receipt["controls"] = controls()
            receipt["pins_before"] = pins()
            if not args.controls_only:
                arrays, proof, result = evaluate(args.bits, start)
                with paths["arrays"].open("xb") as f:
                    np.savez_compressed(f, **arrays)
                with paths["proof"].open("x") as f:
                    json.dump(proof, f, separators=(",", ":"), allow_nan=False)
                    f.write("\n")
                receipt.update({"result": result, "array_file": paths["arrays"].name, "array_sha256": digest(paths["arrays"]),
                                "proof_file": paths["proof"].name, "proof_sha256": digest(paths["proof"]),
                                "array_schema": {k: {"shape": list(v.shape), "dtype": str(v.dtype), "sha256": hashlib.sha256(v.tobytes(order="C")).hexdigest()} for k, v in arrays.items()},
                                "schema_notes": {"pairs": ["setting_index", "global_master_index", "slave_node_id", "class", "same_node_ID", "same_incident_part"],
                                                 "pair_values": ["dA_mid", "dB_mid", "L_lower_view", "U_upper_view", "delta_low_mid", "delta_high_mid", "signed012_mid", "signed023_mid", "signed013_mid", "signed123_mid"],
                                                 "coverage": ["population", "slab_candidates", "slab_plus_unknown", "exact_box_admitted", "broad_excluded", "box_interval_ambiguous", "class0", "class1", "class2", "class3"],
                                                 "proof_fractions": "[numerator_string,denominator_string]; exact inclusive endpoints; null thresholds are unknown",
                                                 "float_views": "not certificates; use rational proof endpoints", "masks": "little bit order; setting,CID master order,packed complete sorted slave order",
                                                 "projection": "-1 undefined plane,0 outside,1 inside including exact boundary", "master_identity": "cid,set_id,source_membership_line"}})
            receipt["pins_after"] = pins()
            require(digest(Path(__file__)) == receipt["producer_sha256"], "producer_changed_during_run")
            receipt["status"] = "passed"
        except Exception as e:
            receipt["status"] = "failed"
            receipt["error_type"] = type(e).__name__
            # Only our fixed diagnostic codes, never raw input/exception text.
            if isinstance(e, ValueError) and len(e.args) == 1 and isinstance(e.args[0], str) and e.args[0].replace("_", "").isalnum():
                receipt["error_code"] = e.args[0]
        finally:
            receipt["elapsed_seconds"] = time.monotonic()-start
            receipt["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            json.dump(receipt, output, indent=2, sort_keys=True, allow_nan=False)
            output.write("\n")
    print(json.dumps({"status": receipt["status"], "receipt": paths["receipt"].name, "elapsed_seconds": receipt["elapsed_seconds"]}), flush=True)
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
