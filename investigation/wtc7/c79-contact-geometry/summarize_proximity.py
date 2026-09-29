#!/usr/bin/env python3
"""Post-result descriptive summary; preserves frozen diagnostic classifications."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
PINS = {
    'proximity-root01.json': 'd2201fcd1f0c36f3240a32813b01ec1c8b90f44d019ac0cbb93ce54a99e5f6cc',
    'proximity-root02.json': '962f378986ad225276c1d1d8f796218b3ce729d1079ce65de5cb3664f615601b',
    'proximity-root01.npz': 'b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca',
    'proximity-root02.npz': 'b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca',
    'stage-root01.npz': '2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize():
    before = {k: sha(BASE/k) for k in PINS}
    assert before == PINS
    roots = [json.loads((BASE/f'proximity-root0{i}.json').read_text()) for i in (1, 2)]
    stripped = []
    for obj in roots:
        clone = dict(obj)
        for key in ('command', 'elapsed_seconds', 'peak_bytes', 'array_file'): clone.pop(key)
        stripped.append(clone)
    assert stripped[0] == stripped[1]
    with np.load(BASE/'proximity-root01.npz', allow_pickle=False) as z: a = {k: z[k] for k in z.files}
    with np.load(BASE/'proximity-root02.npz', allow_pickle=False) as z:
        assert set(z.files) == set(a)
        for k, v in a.items(): assert np.array_equal(v, z[k], equal_nan=True)
    with np.load(BASE/'stage-root01.npz', allow_pickle=False) as z:
        ids, xyz, incidence = z['node_ids'], z['xyz'], z['node_part_incidence']
    r, f = a['pairs'], a['pair_values']; master_cid = a['master_identity'][:, 0]
    inversions = f[:, 2] > f[:, 3]
    rows = []; node_sets = {}; pair_sets = {}
    for ei, e in enumerate(a['settings']):
        for cid in (1, 2):
            group = (r[:, 0] == ei) & (master_cid[r[:, 1]] == cid)
            cand = group & np.isin(r[:, 3], [2, 3]); nodes = np.unique(r[cand, 2])
            node_sets[ei, cid] = set(map(int, nodes))
            pair_sets[ei, cid] = set(map(tuple, r[cand, 1:3].tolist()))
            hit = np.searchsorted(ids, nodes); assert np.array_equal(ids[hit], nodes)
            vals = f[cand]; present_masters = np.unique(r[cand, 1])
            rows.append({'e': float(e), 'cid': cid, 'candidate_rows_class2_or3': int(cand.sum()),
                         'candidate_nodes': len(nodes), 'master_records_with_candidates': len(present_masters),
                         'master_records_without_candidates': int(np.count_nonzero(master_cid == cid))-len(present_masters),
                         'inverted_enclosures': int(np.count_nonzero(group & inversions)),
                         'class2_not_inverted': int(np.count_nonzero(group & (r[:, 3] == 2) & ~inversions)),
                         'candidate_xyz_min': xyz[hit].min(axis=0).tolist(), 'candidate_xyz_max': xyz[hit].max(axis=0).tolist(),
                         'low_gate_minus_upper_min': float(np.min(vals[:, 4]-vals[:, 3])),
                         'low_gate_minus_upper_max': float(np.max(vals[:, 4]-vals[:, 3]))})
    changes = []
    for cid in (1, 2):
        for ei in (1, 2):
            changes.append({'cid': cid, 'e': float(a['settings'][ei]),
                            'new_nodes_vs_e1': sorted(node_sets[ei, cid]-node_sets[0, cid]),
                            'lost_nodes_vs_e1': sorted(node_sets[0, cid]-node_sets[ei, cid]),
                            'new_pairs_vs_e1': sorted(pair_sets[ei, cid]-pair_sets[0, cid]),
                            'lost_pairs_vs_e1': sorted(pair_sets[0, cid]-pair_sets[ei, cid])})
    all_candidates = np.unique(r[np.isin(r[:, 3], [2, 3]), 2])
    part_rows = []
    for pid in np.unique(incidence[np.isin(incidence[:, 0], all_candidates), 2]):
        entry = incidence[(incidence[:, 2] == pid) & np.isin(incidence[:, 0], all_candidates)]
        nodes = np.unique(entry[:, 0]); hit = np.searchsorted(ids, nodes)
        part_rows.append({'pid': int(pid), 'candidate_nodes': len(nodes),
                          'family_node_counts': {str(int(k)): int(np.count_nonzero(entry[:, 1] == k)) for k in np.unique(entry[:, 1])},
                          'element_node_incidence_by_family': {str(int(k)): int(entry[entry[:, 1] == k, 3].sum()) for k in np.unique(entry[:, 1])},
                          'xyz_min': xyz[hit].min(axis=0).tolist(), 'xyz_max': xyz[hit].max(axis=0).tolist()})
    after = {k: sha(BASE/k) for k in PINS}; assert before == after
    return {'status': 'PASS', 'pins_before': before, 'pins_after': after,
            'summary_code_sha256': sha(Path(__file__)),
            'root_repeat_exclusions': ['command', 'elapsed_seconds', 'peak_bytes', 'array_file'],
            'all_other_root_json_and_all_arrays_exact': True,
            'groups': rows, 'extension_changes': changes, 'candidate_part_rows': part_rows,
            'maximum_enclosure_inversion': float(np.max(f[inversions, 2]-f[inversions, 3])) if inversions.any() else 0.,
            'geometry': {'maximum_w': float(np.max(a['geometry_w'])),
                         'zero_triangle_areas': int(np.count_nonzero(a['geometry_triangle_cross_norm'] == 0)),
                         'near_zero_triangles': int(np.count_nonzero(a['geometry_triangle_near'])),
                         'zero_edges': int(np.count_nonzero(a['geometry_edges'] == 0)),
                         'nonpositive_corner_center_jacobian_dots': int(np.count_nonzero(a['geometry_jacobian_dot_center'] <= 0)),
                         'min_triangle_normal_dot': float(np.nanmin(a['geometry_normal_dots']))},
            'scope': 'Descriptive post-result summary of frozen conditional geometry; no new classification, source reconstruction, solver or physical claim.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', default='proximity-summary01.json'); args = p.parse_args()
    out = BASE/args.output
    assert out.parent.resolve() == BASE and out.name.startswith('proximity-summary') and out.suffix == '.json' and not out.exists()
    result = summarize()
    with out.open('x') as stream: json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False); stream.write('\n')
    print(json.dumps({'status': 'PASS', 'output': out.name, 'sha256': sha(out), 'groups': result['groups'],
                      'maximum_enclosure_inversion': result['maximum_enclosure_inversion'], 'geometry': result['geometry']}))
