#!/usr/bin/env python3
"""Conditional geometric proximity, not an LS-DYNA initializer or solver."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import resource
import sys
import tempfile
import time
import unittest
import numpy as np

BASE = Path(__file__).resolve().parent
SETTINGS = np.array([1., 1.006, 1.025])
TRIS = ((0, 1, 2), (0, 2, 3), (0, 1, 3), (1, 2, 3))
PINS = {
    'GEOMETRIC-METHOD.md': '73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e',
    'GEOMETRIC-IMPLEMENTATION-ADDENDUM.md': 'ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd',
    'stage-root01.json': 'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
    'stage-root01.npz': '2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
}


class CheckFailure(Exception):
    pass


def need(condition, label):
    if not condition:
        raise CheckFailure(label)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def pins():
    out = {name: sha(BASE / name) for name in PINS}
    need(out == PINS, 'input_pin_mismatch')
    out['producer'] = sha(__file__)
    return out


def fresh(paths):
    need(not any(p.exists() for p in paths), 'existing_output')


def patch(q, u, v):
    return ((1-u)*(1-v)*q[0] + u*(1-v)*q[1] + u*v*q[2] + (1-u)*v*q[3])


def extend(q, e):
    h = (e-1)/2
    return np.array([patch(q, -h, -h), patch(q, 1+h, -h),
                     patch(q, 1+h, 1+h), patch(q, -h, 1+h)])


def edge_distance(points, a, b):
    v = b-a
    length2 = np.dot(v, v)
    if length2 == 0:
        return np.linalg.norm(points-a, axis=1)
    t = np.clip((points-a) @ v / length2, 0., 1.)
    return np.linalg.norm(points-(a+t[:, None]*v), axis=1)


def triangle(points, vertices):
    a, b, c = vertices
    cross = np.cross(b-a, c-a)
    size = np.linalg.norm(cross)
    edges = np.stack([edge_distance(points, a, b), edge_distance(points, b, c),
                      edge_distance(points, c, a)], axis=1)
    distance = edges.min(axis=1)
    if size == 0:
        return distance, np.full(len(points), np.nan), np.full(len(points), -1, dtype=np.int8)
    normal = cross/size
    signed = (points-a) @ normal
    signs = np.stack([np.cross(b-a, points-a) @ normal,
                      np.cross(c-b, points-b) @ normal,
                      np.cross(a-c, points-c) @ normal], axis=1)
    inside = np.all(signs >= 0, axis=1)
    distance[inside] = np.minimum(distance[inside], np.abs(signed[inside]))
    return distance, signed, inside.astype(np.int8)


def face_geometry(q):
    cross = np.array([np.cross(q[b]-q[a], q[c]-q[a]) for a, b, c in TRIS])
    norms = np.linalg.norm(cross, axis=1)
    unit = np.full((4, 3), np.nan)
    good = norms > 0
    unit[good] = cross[good]/norms[good, None]
    scales = np.array([max(1., *(float(np.dot(q[b]-q[a], q[b]-q[a]))
                                for a, b in ((i, j), (j, k), (k, i)))) for i, j, k in TRIS])
    near = norms <= 64*np.finfo(float).eps*scales
    mixed = q[0]-q[1]+q[2]-q[3]
    jac = np.array([np.cross(q[1]-q[0]+v*mixed, q[3]-q[0]+u*mixed)
                    for u, v in ((.5, .5), (0., 0.), (1., 0.), (1., 1.), (0., 1.))])
    return {
        'quad': q, 'w': np.linalg.norm(mixed)/4,
        'diagonals': np.linalg.norm(q[[2, 3]]-q[[0, 1]], axis=1),
        'edges': np.linalg.norm(q[[1, 2, 3, 0]]-q, axis=1),
        'triangle_cross': cross, 'triangle_cross_norm': norms,
        'triangle_unit': unit, 'triangle_near': near,
        'normal_dots': np.array([np.dot(unit[a], unit[b]) for a, b in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))]),
        'jacobian': jac, 'jacobian_dot_center': jac[1:] @ jac[0],
    }


def face_distances(points, q, w):
    values = [triangle(points, q[list(indices)]) for indices in TRIS]
    distances = np.stack([v[0] for v in values], axis=1)
    da = distances[:, :2].min(axis=1)
    db = distances[:, 2:].min(axis=1)
    low = np.maximum(0., np.maximum(da-w, db-w))
    high = np.minimum(da+w, db+w)
    return np.column_stack((da, db, low, high)), np.stack([v[1] for v in values], axis=1), np.stack([v[2] for v in values], axis=1)


def thresholds(slave, master, diagonal):
    return np.maximum(.6*(slave+master), .05*diagonal)


def admit(points, q, high, epsilon):
    displacement = np.maximum(np.maximum(q.min(axis=0)-points, points-q.max(axis=0)), 0.)
    lower = np.linalg.norm(displacement, axis=1)
    return (~np.isfinite(high)) | (lower <= high+epsilon)


def classify(bounds, delta, epsilon):
    need(np.all(np.isfinite(bounds)), 'nonfinite_distance_bound')
    need(np.all(np.isnan(delta) | np.isfinite(delta)), 'nonfinite_threshold')
    need(np.all(np.isnan(delta[:, 0]) == np.isnan(delta[:, 1])), 'incomplete_threshold')
    low, high = bounds[:, 2], bounds[:, 3]
    need(np.all(low <= high+epsilon), 'inverted_enclosure_exceeds_epsilon')
    known = np.all(np.isfinite(delta), axis=1)
    out = np.zeros(len(low), dtype=np.int8)
    out[known] = 2
    normal = known & (low <= high)
    out[normal & (low > delta[:, 1]+epsilon)] = 1
    out[normal & (high < delta[:, 0]-epsilon)] = 3
    return out


def serialize_schema(arrays):
    return {k: {'dtype': str(a.dtype), 'shape': list(a.shape),
                'sha256': hashlib.sha256(a.tobytes(order='C')).hexdigest()}
            for k, a in arrays.items()}


class Controls(unittest.TestCase):
    def setUp(self):
        self.q = np.array([[0., 0., 0.], [1., 0., 0.], [1., 1., 0.], [0., 1., 0.]])

    def test_triangle_interior_edge_vertex(self):
        points = np.array([[.2, .2, 3.], [.7, .7, 0.], [-1., -1., 0.]])
        d, s, i = triangle(points, self.q[[0, 1, 3]])
        np.testing.assert_allclose(d, [3., np.sqrt(.08), np.sqrt(2)], atol=1e-12, rtol=0)
        np.testing.assert_array_equal(i, [1, 0, 0])
        np.testing.assert_allclose(s, [3., 0., 0.])

    def test_reverse_winding(self):
        p = np.array([[.2, .2, 3.]])
        a = triangle(p, self.q[[0, 1, 3]])
        b = triangle(p, self.q[[0, 3, 1]])
        np.testing.assert_allclose(a[0], b[0]); np.testing.assert_allclose(a[1], -b[1])

    def test_degenerate_edges_points(self):
        for q, expected in ((np.zeros((3, 3)), np.sqrt(5)),
                            (np.array([[0., 0., 0.], [1., 0., 0.], [1., 0., 0.]]), 2.)):
            d, s, i = triangle(np.array([[1., 2., 0.]]), q)
            self.assertAlmostEqual(d[0], expected)
            self.assertTrue(np.isnan(s[0])); self.assertEqual(i[0], -1)

    def test_planar_analytic(self):
        p = np.array([[.5, .5, 2.], [2., .5, 0.]])
        b, _, _ = face_distances(p, self.q, 0.)
        np.testing.assert_allclose(b, [[2]*4, [1]*4], atol=1e-12)

    def test_warped_patch_zero_in_enclosure(self):
        q = self.q.copy(); q[2, 2] = .4
        w = face_geometry(q)['w']
        p = np.array([patch(q, u, v) for u in np.linspace(0, 1, 11) for v in np.linspace(0, 1, 11)])
        b, _, _ = face_distances(p, q, w)
        self.assertTrue(np.all(b[:, 2] <= 1e-12)); self.assertTrue(np.all(b[:, 3] >= 0))

    def test_planar_nonparallelogram(self):
        q = self.q.copy(); q[2, 0] = 1.4
        self.assertGreater(face_geometry(q)['w'], 0)
        p = np.array([patch(q, .5, .5)])
        b, _, _ = face_distances(p, q, face_geometry(q)['w'])
        self.assertLessEqual(b[0, 2], 1e-12)

    def test_extension_contains_patch(self):
        q = self.q.copy(); q[2, 2] = .8
        for e in SETTINGS:
            r = extend(q, e); h = (e-1)/2
            p = np.array([patch(q, u, v) for u in np.linspace(-h, 1+h, 9) for v in np.linspace(-h, 1+h, 9)])
            self.assertTrue(np.all(p >= r.min(axis=0)-1e-12)); self.assertTrue(np.all(p <= r.max(axis=0)+1e-12))
            self.assertAlmostEqual(face_geometry(r)['w'], e*e*face_geometry(q)['w'])

    def test_extension_only_candidate(self):
        p = np.array([[1.011, .5, 0.]])
        self.assertFalse(admit(p, self.q, np.array([.001]), 1e-10)[0])
        self.assertTrue(admit(p, extend(self.q, 1.025), np.array([.001]), 1e-10)[0])

    def test_thickness_unknown_and_boundary(self):
        b = np.array([[.03]*4, [.08]*4, [.2]*4, [.08]*4])
        d = np.array([[.06, .12], [.06, .12], [.06, .12], [np.nan, np.nan]])
        np.testing.assert_array_equal(classify(b, d, 1e-10), [3, 2, 1, 0])
        np.testing.assert_allclose(thresholds(np.array([[.02, .04]]), [.08, .16], 1.), [[.06, .12]])

    def test_inversions(self):
        b = np.array([[0., 0., 1.+1e-11, 1.]])
        self.assertEqual(classify(b, np.array([[2., 2.]]), 1e-10)[0], 2)
        self.assertEqual(classify(b, np.array([[np.nan, np.nan]]), 1e-10)[0], 0)
        with self.assertRaises(CheckFailure): classify(b, np.array([[2., 2.]]), 1e-12)

    def test_broadphase_unpruned(self):
        rng = np.random.default_rng(190713)
        for e in SETTINGS:
            q = extend(self.q, e); p = rng.uniform(-.2, 1.2, (500, 3)); d = np.full(500, .1)
            b, _, _ = face_distances(p, q, 0.)
            mask = admit(p, q, d, 1e-10)
            self.assertTrue(np.all(mask[b[:, 2] <= .1]))

    def test_duplicates_and_masks(self):
        p = np.array([[.5, .5, 0.], [100., 0., 0.]])
        masks = np.array([admit(p, self.q, np.array([.1, .1]), 1e-10) for _ in range(2)])
        np.testing.assert_array_equal(masks[0], masks[1])
        np.testing.assert_array_equal(np.unpackbits(np.packbits(masks, axis=1, bitorder='little'), axis=1, bitorder='little')[:, :2], masks)

    def test_normal_warning(self):
        q = np.zeros((4, 3)); g = face_geometry(q)
        self.assertTrue(np.all(g['triangle_near'])); self.assertTrue(np.all(np.isnan(g['triangle_unit'])))
        g = face_geometry(self.q)
        self.assertTrue(np.all(g['jacobian_dot_center'] > 0))

    def test_pin_and_existing_guard(self):
        self.assertNotEqual(sha(__file__), '0'*64)
        with tempfile.TemporaryDirectory(prefix='c79-proximity-control-') as folder:
            p = Path(folder)/'fixture'
            fresh([p]); p.touch()
            with self.assertRaises(CheckFailure): fresh([p])

    def test_unexpected_nonfinite_rejected(self):
        with self.assertRaises(CheckFailure): classify(np.array([[0., 0., np.nan, 0.]]), np.array([[1., 1.]]), 1e-10)
        with self.assertRaises(CheckFailure): classify(np.zeros((1, 4)), np.array([[1., np.inf]]), 1e-10)
        with self.assertRaises(CheckFailure): classify(np.zeros((1, 4)), np.array([[1., np.nan]]), 1e-10)


def control_run():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    return {'count': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'passed': result.wasSuccessful()}


def calculate(a, metadata):
    masters = metadata['master_segments']; nmaster = len(masters)
    ids = a['node_ids']; xyz = a['xyz']; thickness = a['corner_thickness_min_max']
    need(np.all(np.diff(ids) > 0) and np.all(np.isfinite(xyz)), 'nodes_sorted_finite')
    need(np.all(np.isnan(thickness) | (np.isfinite(thickness) & (thickness >= 0))), 'thickness_range')
    need(np.all(np.isnan(thickness[:, 0]) == np.isnan(thickness[:, 1])), 'thickness_unknown_pair')
    epsilon = 1e-10 * max(1., float(np.max(np.abs(xyz))))
    populations = {cid: np.flatnonzero(a['roles'][:, cid-1] != 0) for cid in (1, 2)}
    master_cids = np.array([1 if m['set_id'] == 1 else 2 for m in masters])
    need(set(m['set_id'] for m in masters) == {1, 3}, 'master_set_scope')
    output = {'settings': SETTINGS.copy(), 'master_nodes': np.array([m['nodes'] for m in masters], dtype=np.int64),
              'master_identity': np.array([[int(master_cids[j]), m['set_id'], m['line']] for j, m in enumerate(masters)], dtype=np.int64)}
    master_pids = []; mt = []; original_diag = []
    for m in masters:
        need(len(m['aliases']) >= 1, 'missing_master_alias')
        pids = sorted(set(x['pid'] for x in m['aliases']))
        need(len(pids) == 1, 'ambiguous_master_part')
        master_pids.append(pids[0])
        values = np.array([x['thickness_card'][:4] for x in m['aliases']], dtype=float)
        need(np.all(np.isfinite(values)) and np.all(values >= 0), 'master_thickness')
        mt.append([float(values.min()), float(values.max())])
        q = np.array(m['xyz']); original_diag.append(np.linalg.norm(q[[2, 3]]-q[[0, 1]], axis=1))
    output['master_pids'] = np.array(master_pids, dtype=np.int64)
    output['master_thickness'] = np.array(mt); output['master_original_diagonals'] = np.array(original_diag)
    positions = {cid: {int(j): i for i, j in enumerate(np.flatnonzero(master_cids == cid))} for cid in (1, 2)}
    for cid, ix in populations.items():
        output['slave_ids_cid'+str(cid)] = ids[ix]
        output['broad_mask_cid'+str(cid)] = np.zeros((3, len(positions[cid]), (len(ix)+7)//8), dtype=np.uint8)
    geom = {}; records = []; floats = []; projections = []
    coverage = np.zeros((3, nmaster, 7), dtype=np.int64)
    incidence = a['node_part_incidence']
    same_part_nodes = {pid: np.unique(incidence[incidence[:, 2] == pid, 0]) for pid in set(master_pids)}
    for ei, e in enumerate(SETTINGS):
        current = []
        for mi, m in enumerate(masters):
            cid = int(master_cids[mi]); pop = populations[cid]
            q = extend(np.array(m['xyz']), e); g = face_geometry(q); current.append(g)
            delta = thresholds(thickness[pop], output['master_thickness'][mi], min(original_diag[mi]))
            mask = admit(xyz[pop], q, delta[:, 1], epsilon)
            output['broad_mask_cid'+str(cid)][ei, positions[cid][mi]] = np.packbits(mask, bitorder='little')
            selected = pop[mask]; chosen_delta = delta[mask]
            b, signed, projection = face_distances(xyz[selected], q, g['w'])
            classes = classify(b, chosen_delta, epsilon)
            same_id = np.isin(ids[selected], output['master_nodes'][mi])
            same_part = np.isin(ids[selected], same_part_nodes[master_pids[mi]])
            records.append(np.column_stack((np.full(len(selected), ei), np.full(len(selected), mi), ids[selected], classes, same_id, same_part)).astype(np.int64))
            floats.append(np.column_stack((b, chosen_delta, signed))); projections.append(projection)
            counts = np.bincount(classes, minlength=4)
            coverage[ei, mi] = [len(pop), len(selected), len(pop)-len(selected), *counts.tolist()]
        for key in current[0]:
            geom.setdefault(key, []).append(np.array([g[key] for g in current]))
        print(json.dumps({'stage': 'setting_complete', 'setting': float(e)}), flush=True)
    output.update({'geometry_'+key: np.array(value) for key, value in geom.items()})
    output['pairs'] = np.concatenate(records); output['pair_values'] = np.concatenate(floats)
    output['pair_projection_inside'] = np.concatenate(projections); output['coverage'] = coverage
    chosen_ids = np.unique(output['pairs'][:, 2])
    output['admitted_node_part_incidence'] = incidence[np.isin(incidence[:, 0], chosen_ids)]
    selected_pids = np.unique(output['admitted_node_part_incidence'][:, 2])
    parts = [p for p in metadata['part_references'] if p['pid'] in selected_pids]
    need(len(parts) == len(selected_pids), 'all_admitted_parts_resolve')
    summary = []
    rows = output['pairs']
    for ei, e in enumerate(SETTINGS):
        for cid in (1, 2):
            select = (rows[:, 0] == ei) & (master_cids[rows[:, 1]] == cid)
            rr = rows[select]; cc = coverage[ei, master_cids == cid]
            classes = []
            for cls in range(4):
                r = rr[rr[:, 3] == cls]; unique = np.unique(r[:, 2])
                parts_in = np.unique(incidence[np.isin(incidence[:, 0], unique), 2])
                classes.append({'class': cls, 'rows': len(r), 'unique_nodes': len(unique), 'pids': parts_in.tolist()})
            candidates = rr[np.isin(rr[:, 3], [2, 3])]
            _, multiplicity = np.unique(candidates[:, 2], return_counts=True)
            summary.append({'e': float(e), 'cid': cid, 'population_pairs': int(cc[:, 0].sum()),
                            'admitted_rows': len(rr), 'broad_excluded_pairs': int(cc[:, 2].sum()),
                            'zero_admission_masters': int(np.count_nonzero(cc[:, 1] == 0)),
                            'same_node_rows': int(rr[:, 4].sum()), 'same_part_rows': int(rr[:, 5].sum()),
                            'multiple_candidate_master_nodes': int(np.count_nonzero(multiplicity > 1)),
                            'max_candidate_multiplicity': int(multiplicity.max()) if len(multiplicity) else 0,
                            'classes': classes})
    return output, {'epsilon': epsilon, 'groups': summary, 'admitted_part_references': parts,
                    'small_inversion_rows': int(np.count_nonzero(output['pair_values'][:, 2] > output['pair_values'][:, 3]))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--output', default='proximity-root01')
    args = parser.parse_args()
    if args.controls:
        r = control_run(); print(json.dumps(r)); raise SystemExit(0 if r['passed'] else 1)
    need(re.fullmatch(r'proximity-root[0-9]+', args.output) is not None, 'output_scope')
    js = BASE/(args.output+'.json'); npz = BASE/(args.output+'.npz'); fail = BASE/(args.output+'-failed.json')
    fresh([js, npz, fail]); started = time.monotonic(); before = {}; control = {}
    try:
        control = control_run(); need(control['passed'], 'controls_failed')
        before = pins(); metadata = json.loads((BASE/'stage-root01.json').read_text())['result']
        with np.load(BASE/'stage-root01.npz', allow_pickle=False) as z:
            need(set(z.files) == set(metadata['arrays']), 'input_array_schema')
            a = {k: z[k] for k in z.files}
        for key, value in a.items():
            s = metadata['arrays'][key]
            need(value.dtype.kind in 'biuf' and list(value.shape) == s['shape'] and np.dtype(s['dtype']) == value.dtype, 'input_dtype_shape')
            need(hashlib.sha256(value.tobytes(order='C')).hexdigest() == s['sha256'], 'input_array_pin')
        arrays, result = calculate(a, metadata)
        schema = serialize_schema(arrays)
        with npz.open('xb') as f: np.savez_compressed(f, **arrays)
        with np.load(npz, allow_pickle=False) as z:
            need(set(z.files) == set(arrays), 'output_reopen_schema')
            for key, value in arrays.items(): need(np.array_equal(value, z[key], equal_nan=True), 'output_reopen_values')
        after = pins(); need(before == after, 'pins_changed')
        receipt = {'status': 'PASS', 'command': sys.argv, 'elapsed_seconds': time.monotonic()-started,
                   'peak_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024),
                   'runtime': {'python': sys.version, 'executable': sys.executable, 'numpy': np.__version__},
                   'controls': control, 'pins_before': before, 'pins_after': after,
                   'array_file': npz.name, 'array_sha256': sha(npz), 'array_schema': schema, 'result': result,
                   'schema_notes': {'pairs': ['setting_index', 'global_master_index', 'slave_node_id', 'class_0unknown_1outside_2unresolved_3inside', 'same_node_ID', 'same_incident_part'],
                                    'pair_values': ['dA', 'dB', 'L', 'U', 'delta_low', 'delta_high', 'signed_012', 'signed_023', 'signed_013', 'signed_123'],
                                    'coverage': ['population', 'admitted', 'broad_excluded', 'class0', 'class1', 'class2', 'class3'],
                                    'masks': 'little bit order; settings then CID master order then complete sorted slave order; zero unused padding',
                                    'projection': '-1 undefined plane; 0 outside; 1 inside; TRIS012,023,013,123',
                                    'undefined': 'NaN only for unknown thickness or degenerate triangle unit normal/signed plane/normal-dot metadata',
                                    'jacobian': 'center,(0,0),(1,0),(1,1),(0,1); raw vectors and corner dot center',
                                    'incidence': 'node_id,kind_shell0_beam1_discrete2_solid3,effective_part_id,element_incidence_count'},
                   'scope': 'Conditional undeformed-input geometric diagnostic only; no raw source pass, solver initialization, capacity, historical state, floor/unit assignment or cause finding.'}
        with js.open('x') as f: json.dump(receipt, f, sort_keys=True, indent=2, allow_nan=False); f.write('\n')
        print(json.dumps({'status': 'PASS', 'receipt': js.name, 'sha256': sha(js), 'array_sha256': sha(npz), 'rows': len(arrays['pairs']), 'seconds': receipt['elapsed_seconds']}))
    except Exception as exc:
        record = {'status': 'FAIL', 'error': str(exc) if isinstance(exc, CheckFailure) else type(exc).__name__,
                  'command': sys.argv, 'pins_before': before, 'controls': control, 'elapsed_seconds': time.monotonic()-started}
        with fail.open('x') as f: json.dump(record, f, sort_keys=True, indent=2); f.write('\n')
        print(json.dumps(record)); raise SystemExit(1) from None


if __name__ == '__main__':
    main()
