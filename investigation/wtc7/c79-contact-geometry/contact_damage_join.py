#!/usr/bin/env python3
"""Exact typed node membership join; no activation or mechanical simulation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import unittest
import numpy as np

BASE = Path(__file__).resolve().parent
FILES = {
    'protocol': (BASE/'CONTACT-DAMAGE-JOIN-PROTOCOL.md', '36443e2edb37ae596f93b66c58792bceb83b4cd2f902dc4aee1ec13f7ab22cd7'),
    'geometry': (BASE.parent/'model-member-map/run06/member-map.json', 'eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e'),
    'lists': (BASE.parent/'c79-restraint-audit/candidate-join01.json', 'a29de50566ccfba66001db77a50851f63f765769b40130ae22186f2211cda3d2'),
    'stage_json': (BASE/'stage-root01.json', 'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963'),
    'stage_arrays': (BASE/'stage-root01.npz', '2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf'),
    'exact_receipt': (BASE/'exact-proximity80.json', '25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324'),
    'exact_arrays': (BASE/'exact-proximity80.npz', '79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628'),
}
SOURCE = {'wtc7_global_8a_no-conn-matl.k.gz': 121, 'elem_thick_to-renum.k.gz': 120, 'discrete_mass.k.gz': 119}


def require(ok, label):
    if not ok: raise ValueError(label)


def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()


def pins():
    result = {key: sha(path) for key, (path, _) in FILES.items()}
    require(result == {key: expected for key, (_, expected) in FILES.items()}, 'dependency_pin')
    return result


def typed_key(row):
    return row['kind'], row['eid']


def physical_nodes(row):
    return sorted(set(row['node_ids']))


def reconcile(geometry, lists):
    gm = {}
    for row in geometry:
        key = typed_key(row)
        require(key not in gm, 'duplicate_typed_geometry')
        require(not row['missing_nodes'] and len(row['node_ids']) == len(row['node_coordinates']), 'node_coordinate_coverage')
        require(all(n > 0 for n in row['node_ids']), 'physical_node_positive')
        gm[key] = row
    lm = {}
    for row in lists:
        key = row['actual_family'], row['eid']
        require(key not in lm, 'duplicate_typed_list')
        lm[key] = row
    require(gm.keys() == lm.keys(), 'typed_pool_coverage')
    for key, g in gm.items():
        r = lm[key]
        require(SOURCE[g['source']] == r['source'] and g['line'] == r['line'], 'source_locator')
        require([g['pid'], g['original_pid']] == [r['effective_part'], r['original_part']], 'part_namespace')
        require(physical_nodes(g) == sorted(r['distinct_physical_nodes']), 'physical_nodes')
        require(g['orientation_node'] == r['orientation_node'], 'orientation_reference')
        expected_requested = 'beam' if g['kind'] == 'discrete' else g['kind']
        require(r['requested_family'] == expected_requested and r['set_id'] == 2 and r['list_source'] == 116, 'list_role')
    return gm, lm


def intersect_nodes(row, selected, coords):
    found = sorted(set(row['node_ids']) & selected)
    for nid in found:
        for i, node in enumerate(row['node_ids']):
            if node == nid: require(row['node_coordinates'][i] == coords[nid], 'matched_coordinate_disagrees')
    return found


class Tests(unittest.TestCase):
    def row(self):
        return {'kind': 'beam', 'eid': 3, 'pid': 9, 'original_pid': 9, 'node_ids': [1, 2], 'node_coordinates': [[0., 0., 0.], [1., 0., 0.]],
                'orientation_node': 7, 'missing_nodes': [], 'source': 'wtc7_global_8a_no-conn-matl.k.gz', 'line': 30}

    def listed(self):
        return {'actual_family': 'beam', 'eid': 3, 'effective_part': 9, 'original_part': 9, 'distinct_physical_nodes': [1, 2],
                'orientation_node': 7, 'source': 121, 'line': 30, 'requested_family': 'beam', 'set_id': 2, 'list_source': 116,
                'list_header_line': 2, 'list_membership_ordinals': [1, 2]}

    def test_shared_node(self):
        self.assertEqual(intersect_nodes(self.row(), {2}, {2: [1., 0., 0.]}), [2])

    def test_same_coordinate_not_identity(self):
        self.assertEqual(intersect_nodes(self.row(), {8}, {8: [1., 0., 0.]}), [])

    def test_orientation_not_endpoint(self):
        self.assertEqual(intersect_nodes(self.row(), {7}, {7: [0., 0., 0.]}), [])

    def test_bad_coordinate(self):
        with self.assertRaises(ValueError): intersect_nodes(self.row(), {2}, {2: [2., 0., 0.]})

    def test_typed_collision(self):
        other = self.row(); other['kind'] = 'discrete'
        second = self.listed(); second['actual_family'] = 'discrete'
        self.assertEqual(len(reconcile([self.row(), other], [self.listed(), second])[0]), 2)

    def test_repeated_membership_preserved(self):
        _, lm = reconcile([self.row()], [self.listed()])
        self.assertEqual(lm['beam', 3]['list_membership_ordinals'], [1, 2])

    def test_namespace_and_missing(self):
        r = self.listed(); r['effective_part'] += 1000
        with self.assertRaises(ValueError): reconcile([self.row()], [r])
        with self.assertRaises(ValueError): reconcile([self.row()], [])

    def test_duplicate_typed(self):
        with self.assertRaises(ValueError): reconcile([self.row(), self.row()], [self.listed()])

    def test_zero(self):
        self.assertEqual(intersect_nodes(self.row(), set(), {}), [])

    def test_pin_predicate(self):
        with self.assertRaises(ValueError): require('1'*64 == '0'*64, 'dependency_pin')


def controls():
    r = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    require(r.wasSuccessful(), 'controls_failed')
    return {'count': r.testsRun, 'failures': len(r.failures), 'errors': len(r.errors)}


def calculate():
    geometry = json.loads(FILES['geometry'][0].read_text())
    prior = json.loads(FILES['lists'][0].read_text())['result']
    stage = json.loads(FILES['stage_json'][0].read_text())['result']
    rows = geometry['damage_set2']['elements'] + geometry['set2_beam_id_discrete_candidates']['elements']
    oldrows = [r for pool in prior['set2_pools'] for r in pool['records']]
    gm, lm = reconcile(rows, oldrows)
    require({k: sum(row['kind'] == k for row in rows) for k in ('shell', 'beam', 'discrete')} == {'shell': 1543, 'beam': 6, 'discrete': 355}, 'pool_counts')
    with np.load(FILES['stage_arrays'][0], allow_pickle=False) as z: nodeids, xyz = z['node_ids'], z['xyz']
    with np.load(FILES['exact_arrays'][0], allow_pickle=False) as z:
        pairs, masters, master_nodes, settings = z['pairs'], z['master_identity'], z['master_nodes'], z['settings']
    require(np.array_equal(master_nodes, np.array([m['nodes'] for m in stage['master_segments']])), 'master_mapping')
    used = np.unique(pairs[:, 2]); ix = np.searchsorted(nodeids, used)
    require(np.array_equal(nodeids[ix], used), 'candidate_nodes_resolve')
    coords = {int(n): p.tolist() for n, p in zip(used, xyz[ix])}
    groups, matches = [], []
    for ei in range(len(settings)):
        for cid in (1, 2):
            for cls in (3, 2, 0):
                selected_rows = pairs[(pairs[:, 0] == ei) & (masters[pairs[:, 1], 0] == cid) & (pairs[:, 3] == cls)]
                selected = set(map(int, selected_rows[:, 2]))
                for kind in ('shell', 'beam', 'discrete'):
                    matching_elements = []; matchednodes = set(); relations = 0
                    for key, row in gm.items():
                        if key[0] != kind: continue
                        found = intersect_nodes(row, selected, coords)
                        if not found: continue
                        source_list = lm[key]
                        contact_rows = selected_rows[np.isin(selected_rows[:, 2], found)]
                        matching_elements.append(row['eid']); matchednodes.update(found); relations += len(contact_rows)
                        matches.append({'setting_index': ei, 'e': float(settings[ei]), 'cid': cid, 'geometry_class': cls,
                                        'actual_family': kind, 'eid': row['eid'], 'effective_part': row['pid'], 'original_part': row['original_pid'],
                                        'source': SOURCE[row['source']], 'element_line': row['line'], 'matched_node_ids': found,
                                        'list_source': source_list['list_source'], 'set_id': source_list['set_id'], 'requested_family': source_list['requested_family'],
                                        'list_header_line': source_list['list_header_line'], 'list_membership_ordinals': source_list['list_membership_ordinals'],
                                        'contact_relations': contact_rows[:, :4].tolist()})
                    groups.append({'setting_index': ei, 'cid': cid, 'geometry_class': cls, 'actual_family': kind,
                                   'selected_unique_nodes': len(selected), 'matching_typed_elements': len(matching_elements),
                                   'matching_node_ids': sorted(matchednodes), 'matching_element_ids': sorted(matching_elements),
                                   'node_master_element_relations': relations})
    master_matches = []
    for mi, master in enumerate(stage['master_segments']):
        for alias in master['aliases']:
            key = 'shell', alias['eid']
            if key in gm:
                row = gm[key]
                require(alias['source'] == SOURCE[row['source']] and alias['line'] == row['line'] and alias['pid'] == row['pid'], 'master_list_version')
                require(sorted(alias['nodes']) == sorted(row['node_ids']), 'master_list_connectivity')
                master_matches.append({'master_index': mi, 'source': alias['source'], 'line': alias['line'], 'eid': alias['eid'], 'pid': alias['pid']})
    return {'typed_pool_counts': {'shell': 1543, 'beam': 6, 'discrete': 355}, 'reconciled_element_records': len(gm),
            'groups': groups, 'matches': matches, 'master_alias_matches': master_matches,
            'casea_contact_join': 'not performed; prior direct-graph zero does not answer this expansion',
            'scope': 'Exact static candidate-node/list incidence only. No activation, deletion semantics, actual tie, capacity, surviving support or cause finding.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--controls', action='store_true'); p.add_argument('--output', default='contact-damage01.json')
    p.add_argument('--verification'); p.add_argument('--verification-sha'); args = p.parse_args()
    if args.controls: print(json.dumps(controls())); raise SystemExit(0)
    require(re.fullmatch(r'contact-damage[0-9]+\.json', args.output) is not None, 'output_scope')
    out = BASE/args.output; require(not out.exists(), 'output_exists')
    require(args.verification and args.verification_sha and re.fullmatch('[0-9a-f]{64}', args.verification_sha), 'verification_required')
    vp = BASE/args.verification; require(vp.parent.resolve() == BASE and vp.suffix == '.json', 'verification_scope')
    require(sha(vp) == args.verification_sha, 'verification_pin')
    verification = json.loads(vp.read_text()); require(verification['status'] == 'PASS', 'exact_verification_not_passed')
    start = time.monotonic(); before = pins(); tests = controls()
    result = calculate(); after = pins(); require(before == after and sha(vp) == args.verification_sha, 'pins_changed')
    receipt = {'status': 'PASS', 'command': sys.argv, 'code_sha256': sha(Path(__file__)), 'elapsed_seconds': time.monotonic()-start,
               'verification': {'file': vp.name, 'sha256': args.verification_sha}, 'controls': tests,
               'pins_before': before, 'pins_after': after, 'result': result}
    with out.open('x') as f: json.dump(receipt, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n')
    print(json.dumps({'status': 'PASS', 'output': out.name, 'sha256': sha(out), 'match_rows': len(result['matches']), 'master_alias_matches': len(result['master_alias_matches'])}))
