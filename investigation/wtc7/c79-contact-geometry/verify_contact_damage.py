#!/usr/bin/env python3
"""Independent exact candidate / typed-list join; no raw input or solver execution."""
import argparse
from collections import Counter, defaultdict
import copy
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
PINS = {
    '../CHARTER.md': '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
    'CONTACT-DAMAGE-JOIN-PROTOCOL.md': '36443e2edb37ae596f93b66c58792bceb83b4cd2f902dc4aee1ec13f7ab22cd7',
    'exact-proximity80.json': '25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
    'exact-proximity80.npz': '79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
    'independent-exact-reference80-01.json': '98a4d00dd76241c44345c6b0fab01c0b5ffe710bc17778528cc845708d7e071f',
    'stage-root01.json': 'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
    'stage-root01.npz': '2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
    '../model-member-map/run06/member-map.json': 'eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e',
    '../c79-restraint-audit/candidate-join01.json': 'a29de50566ccfba66001db77a50851f63f765769b40130ae22186f2211cda3d2',
}
SOURCES = {'discrete_mass.k.gz': 119, 'elem_thick_to-renum.k.gz': 120,
           'wtc7_global_8a_no-conn-matl.k.gz': 121}
FAMILIES = ('shell', 'beam', 'discrete')
CLASSES = (0, 2, 3)

class CheckFailure(Exception):
    pass

def need(condition, code):
    if not condition:
        raise CheckFailure(code)

def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def pincheck(base=BASE, expected=PINS):
    actual = {name: digest(base/name) for name in expected}
    need(actual == expected, 'input_pin_mismatch')
    actual['producer'] = digest(__file__)
    return actual

def integer(value, code, minimum=1):
    need(type(value) is int and value >= minimum, code)
    return value

def coordinate(value):
    need(isinstance(value, list) and len(value) == 3, 'coordinate_shape')
    need(all(type(x) in (float, int) and np.isfinite(x) for x in value), 'coordinate_finite')
    return list(value)

def unique_physical(nodes):
    need(isinstance(nodes, list) and len(nodes) > 0, 'physical_nodes_empty')
    return list(dict.fromkeys(integer(n, 'physical_node_id') for n in nodes))

def index_unique(rows, key):
    out = {}
    for row in rows:
        k = key(row)
        need(k not in out, 'duplicate_typed_record')
        out[k] = row
    return out

def canonical_member(row, request):
    family = row['kind']
    need(family in FAMILIES and request == ('beam' if family == 'discrete' else family), 'requested_family')
    need(row['source'] in SOURCES, 'unrecognized_source')
    source = SOURCES[row['source']]
    original = integer(row['original_pid'], 'original_pid')
    effective = integer(row['pid'], 'effective_pid')
    need(effective == original + (1000 if source == 120 else 0), 'part_namespace')
    node_ids = row['node_ids']
    nodes = unique_physical(node_ids)
    need(row['missing_nodes'] == [] and len(row['node_coordinates']) == len(node_ids), 'missing_coordinates')
    coords = {}
    for nid, raw in zip(node_ids, row['node_coordinates']):
        xyz = coordinate(raw)
        need(nid not in coords or coords[nid] == xyz, 'repeated_node_coordinate')
        coords[nid] = xyz
    orientation = row['orientation_node']
    need(orientation is None or (family == 'beam' and type(orientation) is int and orientation >= 0), 'orientation_schema')
    return {'actual_family': family, 'requested_family': request,
            'eid': integer(row['eid'], 'eid'), 'source': source,
            'line': integer(row['line'], 'source_line'), 'effective_part': effective,
            'original_part': original, 'node_ids': nodes,
            'node_coordinates': [coords[n] for n in nodes], 'orientation_node': orientation}

def canonical_list(row):
    family, request = row['actual_family'], row['requested_family']
    need(family in FAMILIES and request == ('beam' if family == 'discrete' else family), 'list_family')
    need(row['source'] in (119, 120, 121), 'list_element_source')
    need(row['list_source'] == 116 and row['set_id'] == 2, 'list_identity')
    need(row['list_header_line'] == (3 if request == 'shell' else 1557), 'list_header')
    ordinals = row['list_membership_ordinals']
    need(isinstance(ordinals, list) and len(ordinals) > 0, 'list_ordinals_empty')
    for x in ordinals: integer(x, 'list_ordinal', 0)
    need(len(set(ordinals)) == len(ordinals), 'duplicate_list_ordinal')
    return {'actual_family': family, 'requested_family': request,
            'eid': integer(row['eid'], 'list_eid'), 'source': row['source'],
            'line': integer(row['line'], 'list_element_line'),
            'effective_part': integer(row['effective_part'], 'list_effective_pid'),
            'original_part': integer(row['original_part'], 'list_original_pid'),
            'node_ids': unique_physical(row['distinct_physical_nodes']),
            'orientation_node': row['orientation_node'], 'list_source': row['list_source'],
            'set_id': row['set_id'], 'list_header_line': row['list_header_line'],
            'list_membership_ordinals': list(ordinals)}

def reconcile(member_rows, list_rows):
    left = index_unique(member_rows, lambda x: (x['actual_family'], x['eid']))
    right = index_unique(list_rows, lambda x: (x['actual_family'], x['eid']))
    need(left.keys() == right.keys(), 'typed_population_mismatch')
    result = []
    node_coords = {}
    for key in sorted(left):
        a, b = left[key], right[key]
        for field in ('actual_family', 'requested_family', 'eid', 'source', 'line',
                      'effective_part', 'original_part', 'orientation_node'):
            need(type(a[field]) is type(b[field]) and a[field] == b[field], 'row_identity_'+field)
        need(set(a['node_ids']) == set(b['node_ids']), 'physical_node_mismatch')
        for nid, xyz in zip(a['node_ids'], a['node_coordinates']):
            need(nid not in node_coords or node_coords[nid] == xyz, 'cross_element_coordinate')
            node_coords[nid] = xyz
        r = dict(a)
        r.update({k: b[k] for k in ('list_source', 'set_id', 'list_header_line', 'list_membership_ordinals')})
        r['independent_list_node_order'] = b['node_ids']
        result.append(r)
    return result, node_coords

def check_xyz(nid, expected, stage):
    need(nid in stage, 'matched_node_missing_from_stage')
    need(expected == stage[nid]['xyz'], 'coordinate_version_mismatch')

def join(candidates, elements, stage):
    """Invert supplied element endpoints, then visit every frozen candidate row."""
    by_node = defaultdict(list)
    for i, el in enumerate(elements):
        for nid, xyz in zip(el['node_ids'], el['node_coordinates']):
            by_node[nid].append((i, xyz))
    relations, candidate_rows = [], []
    keys = set()
    for row in candidates:
        key = tuple(row['key'])
        need(key not in keys, 'duplicate_candidate_key'); keys.add(key)
        need(row['class'] in CLASSES, 'candidate_class')
        nid = key[2]
        need(nid in stage, 'candidate_node_missing')
        matches = []
        for element_index, xyz in by_node.get(nid, []):
            check_xyz(nid, xyz, stage)
            matches.append(len(relations))
            relations.append({'candidate_key': list(key), 'cid': row['cid'], 'class': row['class'],
                              'element_index': element_index, 'node_id': nid,
                              'coordinate': list(xyz), 'stage_source_line': stage[nid]['source_line']})
        candidate_rows.append({**row, 'node_source_line': stage[nid]['source_line'],
                               'coordinate': stage[nid]['xyz'], 'relation_indices': matches})
    groups = []
    for setting in range(3):
        for cid in (1, 2):
            for cls in CLASSES:
                selected = [r for r in candidate_rows if r['key'][0] == setting and r['cid'] == cid and r['class'] == cls]
                for family in FAMILIES:
                    indices = [i for i, r in enumerate(relations) if r['candidate_key'][0] == setting
                               and r['cid'] == cid and r['class'] == cls
                               and elements[r['element_index']]['actual_family'] == family]
                    hits = [relations[i] for i in indices]
                    groups.append({'setting_index': setting, 'cid': cid, 'class': cls, 'family': family,
                                   'candidate_relation_rows': len(selected),
                                   'candidate_nodes': sorted(set(r['key'][2] for r in selected)),
                                   'matched_candidate_keys': sorted(set(tuple(r['candidate_key']) for r in hits)),
                                   'matched_node_ids': sorted(set(r['node_id'] for r in hits)),
                                   'matched_element_indices': sorted(set(r['element_index'] for r in hits)),
                                   'relation_indices': indices,
                                   'node_element_master_relations': len(indices)})
    return {'candidates': candidate_rows, 'relations': relations, 'groups': groups}

def master_join(masters, elements, stage):
    by_eid = {(r['actual_family'], r['eid']): i for i, r in enumerate(elements)}
    results = []
    for master_index, master in enumerate(masters):
        cid = 1 if master['set_id'] == 1 else 2
        for alias_index, alias in enumerate(master['aliases']):
            index = by_eid.get(('shell', alias['eid']))
            r = {'master_index': master_index, 'alias_index': alias_index, 'cid': cid,
                 'set_id': master['set_id'], 'master_line': master['line'],
                 'eid': alias['eid'], 'source': alias['source'], 'line': alias['line'],
                 'effective_part': alias['pid'], 'original_part': alias['original_pid'],
                 'node_ids': list(alias['nodes']), 'matched_element_index': index}
            if index is not None:
                el = elements[index]
                need((alias['source'], alias['line'], alias['pid'], alias['original_pid']) ==
                     (el['source'], el['line'], el['effective_part'], el['original_part']), 'master_identity_version')
                need(set(alias['nodes']) == set(el['node_ids']), 'master_node_version')
                for nid, xyz in zip(el['node_ids'], el['node_coordinates']): check_xyz(nid, xyz, stage)
            results.append(r)
    return results

def load_arrays(path, schema):
    with np.load(path, allow_pickle=False) as archive:
        need(set(archive.files) == set(schema), 'npz_schema')
        result = {}
        for name in archive.files:
            a, s = archive[name], schema[name]
            need(a.dtype.kind in 'biuf' and list(a.shape) == s['shape'] and str(a.dtype) == s['dtype'], 'array_shape_dtype')
            need(hashlib.sha256(a.tobytes(order='C')).hexdigest() == s['sha256'], 'array_hash')
            result[name] = a
    return result

def calculate():
    read = lambda name: json.loads((BASE/name).read_text())
    approved = read('independent-exact-reference80-01.json')
    need(approved['status'] == approved['result']['status'] == 'PASS' and approved['result']['precision_bits'] == 80, 'exact_verification_gate')
    exact = read('exact-proximity80.json')
    need(exact['status'] == 'passed' and exact['precision_bits'] == 80, 'exact_source_status')
    need(approved['pins_before']['exact-proximity80.json'] == PINS['exact-proximity80.json'] and
         approved['pins_before']['exact-proximity80.npz'] == PINS['exact-proximity80.npz'], 'exact_reference_version')
    need(exact['pins_before']['stage-root01.json'] == PINS['stage-root01.json'] and
         exact['pins_before']['stage-root01.npz'] == PINS['stage-root01.npz'], 'exact_stage_version')
    metadata = read('stage-root01.json')['result']
    stage_arrays = load_arrays(BASE/'stage-root01.npz', metadata['arrays'])
    exact_arrays = load_arrays(BASE/'exact-proximity80.npz', exact['array_schema'])
    need(exact['array_sha256'] == PINS['exact-proximity80.npz'], 'exact_archive_pin')
    ids, xyz, loc = stage_arrays['node_ids'], stage_arrays['xyz'], stage_arrays['node_source_line']
    need(ids.ndim == 1 and np.all(np.diff(ids)>0) and xyz.shape == (len(ids),3) and loc.shape == (len(ids),2), 'stage_node_schema')
    need(np.all(np.isfinite(xyz)), 'stage_coordinate_finite')
    stage = {int(n): {'xyz': p.tolist(), 'source_line': q.tolist()} for n,p,q in zip(ids,xyz,loc)}
    member = read('../model-member-map/run06/member-map.json')
    prior = read('../c79-restraint-audit/candidate-join01.json')
    member_rows = [canonical_member(r,r['kind']) for r in member['damage_set2']['elements']]
    member_rows += [canonical_member(r,'beam') for r in member['set2_beam_id_discrete_candidates']['elements']]
    list_rows = []
    for pool in prior['result']['set2_pools']:
        for r in pool['records']:
            need(r['actual_family'] == pool['actual_family'] and r['requested_family'] == pool['requested_family'], 'pool_family')
            list_rows.append(canonical_list(r))
    elements, node_coords = reconcile(member_rows,list_rows)
    need(Counter(r['actual_family'] for r in elements) == {'shell':1543,'beam':6,'discrete':355}, 'historical_population_count')
    shared = set(node_coords).intersection(stage)
    for nid in shared: check_xyz(nid,node_coords[nid],stage)
    masters = metadata['master_segments']
    need(len(masters) == 742 and Counter(m['set_id'] for m in masters) == {1:710,3:32}, 'master_population')
    need(len(exact_arrays['master_identity']) == len(masters), 'master_array_length')
    for i,m in enumerate(masters):
        need(exact_arrays['master_identity'][i].tolist() == [1 if m['set_id']==1 else 2,m['set_id'],m['line']], 'master_reference_identity')
        need(exact_arrays['master_nodes'][i].tolist() == m['nodes'], 'master_reference_nodes')
        for nid,p in zip(m['nodes'],m['xyz']): check_xyz(nid,p,stage)
    pairs = exact_arrays['pairs']
    need(pairs.ndim == 2 and pairs.shape[1] == 6, 'pair_shape')
    candidates = []
    allkeys = set(); excluded = Counter()
    for i, raw in enumerate(pairs):
        setting,mi,nid,cls,sameid,samepart = (int(x) for x in raw)
        need(setting in (0,1,2) and 0 <= mi < len(masters) and cls in (0,1,2,3), 'pair_domain')
        key = (setting,mi,nid)
        need(key not in allkeys,'duplicate_exact_pair'); allkeys.add(key)
        cid = int(exact_arrays['master_identity'][mi,0])
        need(nid in stage and stage_arrays['roles'][np.searchsorted(ids,nid),cid-1] != 0,'candidate_role')
        if cls == 1:
            excluded[(setting,cid)] += 1
            continue
        candidates.append({'key': list(key), 'exact_row': i, 'cid': cid, 'class': cls,
                           'master_source':121, 'master_line': masters[mi]['line']})
    result = join(candidates,elements,stage)
    result['master_aliases'] = master_join(masters,elements,stage)
    result['elements'] = elements
    result['source_reconciliation'] = {'typed_rows':len(elements),'by_family':dict(Counter(r['actual_family'] for r in elements)),
        'distinct_physical_nodes':len(node_coords),'node_coordinates_shared_with_stage':len(shared),
        'coordinate_scalars_compared':3*len(shared), 'master_records':len(masters),
        'all_exact_admitted_rows':len(pairs), 'candidate_rows':len(candidates),
        'candidate_unique_nodes':len(set(r['key'][2] for r in candidates)),
        'outside_rows':[{'setting_index':s,'cid':c,'count':excluded[(s,c)]} for s in range(3) for c in (1,2)],
        'array_fields_verified':len(stage_arrays)+len(exact_arrays)}
    result['group_counts'] = [{k:v for k,v in g.items() if not isinstance(v,list)} |
        {'candidate_unique_nodes':len(g['candidate_nodes']),'matched_candidate_rows':len(g['matched_candidate_keys']),
         'matched_unique_nodes':len(g['matched_node_ids']),'matched_typed_elements':len(g['matched_element_indices'])}
        for g in result['groups']]
    result['master_counts'] = [{'cid':cid,'alias_rows':sum(r['cid']==cid for r in result['master_aliases']),
        'matched_alias_rows':sum(r['cid']==cid and r['matched_element_index'] is not None for r in result['master_aliases'])}
        for cid in (1,2)]
    result['scope'] = 'Static typed-list incidence of exact conditional geometric candidates; no solver deletion, initialized contact, lost restraint, physical member/unit attribution or cause finding. CaseA contact join unperformed.'
    return result

class Controls(unittest.TestCase):
    def fixture(self,family='shell',eid=8,nodes=None):
        nodes = [1,2] if nodes is None else nodes
        a={'actual_family':family,'requested_family':'beam' if family=='discrete' else family,'eid':eid,'source':121,'line':90,'effective_part':2,'original_part':2,'node_ids':nodes,'node_coordinates':[[float(n),0.,0.] for n in nodes],'orientation_node':None}
        b={k:v for k,v in a.items() if k!='node_coordinates'}
        b.update(list_source=116,set_id=2,list_header_line=3 if family=='shell' else 1557,list_membership_ordinals=[1])
        return a,b
    def stage(self): return {n:{'xyz':[float(n),0.,0.],'source_line':[121,100+n]} for n in range(1,10)}
    def candidate(self,n=1,mi=0,cls=3): return {'key':[0,mi,n],'cid':1,'class':cls}
    def test_reconcile(self):
        a,b=self.fixture(); rows,_=reconcile([a],[b]); self.assertEqual(len(rows),1)
    def test_typed_collision(self):
        a,b=self.fixture(); c,d=self.fixture('discrete'); rows,_=reconcile([a,c],[b,d]); self.assertEqual(len(rows),2)
    def test_missing_population(self):
        a,b=self.fixture()
        with self.assertRaises(CheckFailure): reconcile([a],[])
    def test_duplicate_population(self):
        a,b=self.fixture()
        with self.assertRaises(CheckFailure): reconcile([a,a],[b])
    def test_namespace(self):
        a,b=self.fixture(); b['effective_part']+=1000
        with self.assertRaises(CheckFailure): reconcile([a],[b])
    def test_locator(self):
        a,b=self.fixture(); b['line']+=1
        with self.assertRaises(CheckFailure): reconcile([a],[b])
    def test_requested_family(self):
        a,b=self.fixture('discrete'); b['requested_family']='discrete'
        with self.assertRaises(CheckFailure): reconcile([a],[b])
    def test_physical_nodes(self):
        a,b=self.fixture(); b['node_ids']=[1,3]
        with self.assertRaises(CheckFailure): reconcile([a],[b])
    def test_coordinate_inconsistency(self):
        a,b=self.fixture(); c,d=self.fixture(eid=9); c['node_coordinates'][0][0]+=1
        with self.assertRaises(CheckFailure): reconcile([a,c],[b,d])
    def test_hit_version(self):
        a,b=self.fixture(); a['node_coordinates'][0][0]+=1
        with self.assertRaises(CheckFailure): join([self.candidate()],[a],self.stage())
    def test_shared_id(self):
        a,b=self.fixture(); r=join([self.candidate()],[a],self.stage()); self.assertEqual(len(r['relations']),1)
    def test_coordinate_only_not_id(self):
        a,b=self.fixture(nodes=[2]); a['node_coordinates']=[[1.,0.,0.]]
        self.assertEqual(len(join([self.candidate()],[a],self.stage())['relations']),0)
    def test_orientation_not_endpoint(self):
        a,b=self.fixture('beam',nodes=[2,3]); a['orientation_node']=1
        self.assertEqual(len(join([self.candidate()],[a],self.stage())['relations']),0)
    def test_duplicate_masters_preserved(self):
        a,b=self.fixture(); r=join([self.candidate(mi=0),self.candidate(mi=1)],[a],self.stage())
        self.assertEqual(len(r['relations']),2); self.assertEqual(len(r['groups']),54)
    def test_unknown_and_zero_groups(self):
        a,b=self.fixture(); r=join([self.candidate(cls=0)],[a],self.stage())
        self.assertEqual(r['relations'][0]['class'],0); self.assertEqual(sum(bool(g['relation_indices']) for g in r['groups']),1)
    def test_duplicate_candidate(self):
        a,b=self.fixture()
        with self.assertRaises(CheckFailure): join([self.candidate(),self.candidate()],[a],self.stage())
    def test_master_typed_membership(self):
        a,b=self.fixture('discrete'); m={'set_id':1,'line':60,'aliases':[{'eid':8,'source':121,'line':90,'pid':2,'original_pid':2,'nodes':[1,2]}]}
        self.assertIsNone(master_join([m],[a],self.stage())[0]['matched_element_index'])
        a['actual_family']='shell'; self.assertEqual(master_join([m],[a],self.stage())[0]['matched_element_index'],0)
    def test_master_version(self):
        a,b=self.fixture(); m={'set_id':1,'line':60,'aliases':[{'eid':8,'source':121,'line':91,'pid':2,'original_pid':2,'nodes':[1,2]}]}
        with self.assertRaises(CheckFailure): master_join([m],[a],self.stage())
    def test_duplicate_memberships_preserved(self):
        a,b=self.fixture(); b['list_membership_ordinals']=[1,4]
        self.assertEqual(reconcile([a],[b])[0][0]['list_membership_ordinals'],[1,4])
    def test_canonical_duplicate_ordinal(self):
        a,b=self.fixture(); b['distinct_physical_nodes']=b.pop('node_ids'); b['list_membership_ordinals']=[1,1]
        with self.assertRaises(CheckFailure): canonical_list(b)
    def test_changed_pin(self):
        with tempfile.TemporaryDirectory(prefix='contact-damage-test-') as name:
            p=Path(name)/'x'; p.touch(); expected={'x':digest(p)}; pincheck(Path(name),expected)
            with p.open('ab') as f: f.write(b'mutated synthetic fixture')
            with self.assertRaises(CheckFailure): pincheck(Path(name),expected)
    def test_missing_coordinate(self):
        with self.assertRaises(CheckFailure): coordinate([1.,float('nan'),2.])
    def test_repeat(self):
        a,b=self.fixture(); self.assertEqual(join([self.candidate()],[a],self.stage()),join([self.candidate()],[a],self.stage()))

def controls():
    tests=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    r=unittest.TextTestRunner(verbosity=1).run(tests)
    return {'count':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'passed':r.wasSuccessful()}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--controls',action='store_true'); parser.add_argument('--out',default='independent-contact-damage01.json')
    args=parser.parse_args()
    if args.controls:
        c=controls(); print(json.dumps(c)); return 0 if c['passed'] else 1
    need(re.fullmatch(r'independent-contact-damage[0-9]+\.json',args.out) is not None,'output_scope')
    path=BASE/args.out; need(not path.exists(),'existing_output')
    started=time.monotonic(); receipt={'status':'FAIL','command':sys.argv,'pins_before':{},'controls':{}}
    try:
        c=controls(); receipt['controls']=c; need(c['passed'],'controls_failed')
        before=pincheck(); receipt['pins_before']=before
        result=calculate(); after=pincheck(); need(before==after,'pins_changed')
        receipt.update(status='PASS',result=result,pins_after=after)
    except Exception as exc:
        receipt['error']=str(exc) if isinstance(exc,CheckFailure) else type(exc).__name__
    receipt.update(elapsed_seconds=time.monotonic()-started,
        peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        runtime={'python':sys.version,'executable':sys.executable,'numpy':np.__version__})
    with path.open('x') as f: json.dump(receipt,f,sort_keys=True,indent=2,allow_nan=False); f.write('\n')
    check=json.loads(path.read_text()); need(check['status']==receipt['status'],'output_reopen')
    print(json.dumps({'status':receipt['status'],'receipt':path.name,'sha256':digest(path),
        'seconds':receipt['elapsed_seconds'],'error':receipt.get('error')}))
    return 0 if receipt['status']=='PASS' else 1

if __name__=='__main__': raise SystemExit(main())
