#!/usr/bin/env python3
"""Post-freeze field-complete adapter; never invokes either historical join."""
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import unittest

BASE=Path(__file__).resolve().parent
PINS={
 'verify_contact_damage.py':'c49436fbe3be336ee936a68bc685d2921261fbac95b148e468821fa51d11b511',
 'independent-contact-damage01.json':'dfc169a0c824f0a0981aea60d0e01a5fac0e4de9af4e26e580bc702b177430de',
 'independent-contact-damage02.json':'60fb501873e30815b74fafa766fcd2b0dd129e4fca2e2978b7df2116569a1a5a',
 'contact_damage_join.py':'537f8b025a851572e17fc3dfb654838efde28e1aa54c50edcd48b39ae870d965',
 'contact-damage01.json':'e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479',
 'contact-damage02.json':'e9b33a59006cf60f722388ad3299a80a50bc5be75233c0a29b9faa98685bdce9',
 'independent-exact-reference80-root01.json':'4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8',
}
ROOT_PIN_NAMES={'protocol':'CONTACT-DAMAGE-JOIN-PROTOCOL.md',
 'geometry':'../model-member-map/run06/member-map.json','lists':'../c79-restraint-audit/candidate-join01.json',
 'stage_json':'stage-root01.json','stage_arrays':'stage-root01.npz',
 'exact_receipt':'exact-proximity80.json','exact_arrays':'exact-proximity80.npz'}
CASEA='not performed; prior direct-graph zero does not answer this expansion'
SCOPE='Exact static candidate-node/list incidence only. No activation, deletion semantics, actual tie, capacity, surviving support or cause finding.'

class Mismatch(Exception): pass
def need(ok,label):
 if not ok: raise Mismatch(label)
def sha(path):
 with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def load(name): return json.loads((BASE/name).read_text())

def exact(a,b,path='result',counts=None):
 if counts is None: counts=Counter()
 need(type(a) is type(b),'type:'+path)
 if isinstance(a,dict):
  need(a.keys()==b.keys(),'keys:'+path)
  for k in a: exact(a[k],b[k],path+'/'+str(k),counts)
 elif isinstance(a,list):
  need(len(a)==len(b),'length:'+path)
  for i,(x,y) in enumerate(zip(a,b)): exact(x,y,path+'/'+str(i),counts)
 else:
  counts[type(a).__name__]+=1
  need(a==b,'value:'+path)
 return counts

def keyed(rows,key):
 keys=[key(r) for r in rows]; need(len(keys)==len(set(keys)),'duplicate_comparison_key')
 return sorted(rows,key=key)
def groupkey(r): return (r['setting_index'],r['cid'],r['geometry_class'],r['actual_family'])
def matchkey(r): return groupkey(r)+(r['eid'],)
def normalized(result):
 r=copy.deepcopy(result)
 r['groups']=keyed(r['groups'],groupkey)
 r['matches']=keyed(r['matches'],matchkey)
 r['master_alias_matches']=keyed(r['master_alias_matches'],lambda x:(x['master_index'],x['eid']))
 return r

def expected_root(own,settings):
 elements=own['elements']; groups=[]; matches=[]
 for g in own['groups']:
  fields={'setting_index':g['setting_index'],'cid':g['cid'],'geometry_class':g['class'],'actual_family':g['family']}
  indices=g['matched_element_indices']
  groups.append({**fields,'selected_unique_nodes':len(g['candidate_nodes']),
   'matching_typed_elements':len(indices),'matching_node_ids':g['matched_node_ids'],
   'matching_element_ids':sorted(elements[x]['eid'] for x in indices),
   'node_master_element_relations':len(g['relation_indices'])})
  buckets=defaultdict(list)
  for ri in g['relation_indices']:
   r=own['relations'][ri]; buckets[r['element_index']].append(r)
  need(set(buckets)==set(indices),'own_group_element_indices')
  for ei,relations in buckets.items():
   el=elements[ei]; contacts=[r['candidate_key']+[r['class']] for r in relations]
   need(len(contacts)==len(set(tuple(x) for x in contacts)),'duplicate_own_contact_relation')
   # Own candidate iteration preserves the exact input pair order.
   matches.append({**fields,'e':settings[g['setting_index']],
    'eid':el['eid'],'effective_part':el['effective_part'],'original_part':el['original_part'],
    'source':el['source'],'element_line':el['line'],
    'matched_node_ids':sorted(set(r['node_id'] for r in relations)),
    'list_source':el['list_source'],'set_id':el['set_id'],'requested_family':el['requested_family'],
    'list_header_line':el['list_header_line'],'list_membership_ordinals':el['list_membership_ordinals'],
    'contact_relations':contacts})
 master=[]
 for a in own['master_aliases']:
  if a['matched_element_index'] is not None:
   master.append({'master_index':a['master_index'],'source':a['source'],'line':a['line'],
                  'eid':a['eid'],'pid':a['effective_part']})
 return normalized({'typed_pool_counts':dict(Counter(x['actual_family'] for x in elements)),
  'reconciled_element_records':len(elements),'groups':groups,'matches':matches,
  'master_alias_matches':master,'casea_contact_join':CASEA,'scope':SCOPE})

def normalize_repeat(receipt,own=False):
 r=copy.deepcopy(receipt)
 need(type(r['elapsed_seconds']) is float and r['elapsed_seconds']>=0,'elapsed_schema')
 del r['elapsed_seconds']
 if own:
  need(type(r['peak_bytes']) is int and r['peak_bytes']>0,'peak_schema'); del r['peak_bytes']
  need(len(r['command'])==3 and r['command'][1]=='--out','own_command_schema')
  need(re.fullmatch('independent-contact-damage0[12]\\.json',r['command'][2]) is not None,'own_output_command')
 else:
  need(len(r['command'])==7 and r['command'][1]=='--output','root_command_schema')
  need(re.fullmatch('contact-damage0[12]\\.json',r['command'][2]) is not None,'root_output_command')
 r['command'][2]='DECLARED_OUTPUT_NAME'
 return r

class Tests(unittest.TestCase):
 def test_exact(self): self.assertTrue(exact({'x':[1,2.0,None,False]},{'x':[1,2.0,None,False]}))
 def test_numeric_change(self):
  with self.assertRaises(Mismatch): exact([1.0],[1.00000000001])
 def test_boolean(self):
  with self.assertRaises(Mismatch): exact([1],[True])
 def test_missing_key(self):
  with self.assertRaises(Mismatch): exact({'a':1},{})
 def test_extra_key(self):
  with self.assertRaises(Mismatch): exact({}, {'a':1})
 def test_missing_zero_group(self):
  with self.assertRaises(Mismatch): exact([{'count':0}],[])
 def test_locator(self):
  with self.assertRaises(Mismatch): exact({'line':3},{'line':4})
 def test_family(self):
  with self.assertRaises(Mismatch): exact({'family':'beam'},{'family':'discrete'})
 def test_relation(self):
  with self.assertRaises(Mismatch): exact([[0,4,19,3]],[[0,5,19,3]])
 def test_repeated_membership_order(self):
  with self.assertRaises(Mismatch): exact([2,5],[5,2])
 def test_duplicate_key(self):
  with self.assertRaises(Mismatch): keyed([{'id':1},{'id':1}],lambda r:r['id'])
 def test_normalize_key_order(self):
  self.assertEqual(keyed([{'id':2},{'id':1}],lambda r:r['id']),[{'id':1},{'id':2}])
 def test_repeat_scope(self):
  a={'elapsed_seconds':1.,'command':['x','--output','contact-damage01.json','v','q','h','x'],'result':{'n':1}}
  b=copy.deepcopy(a); b['elapsed_seconds']=2.; b['command'][2]='contact-damage02.json'
  exact(normalize_repeat(a),normalize_repeat(b))
  b['result']['n']=2
  with self.assertRaises(Mismatch): exact(normalize_repeat(a),normalize_repeat(b))
 def test_illegal_repeat_command(self):
  with self.assertRaises(Mismatch): normalize_repeat({'elapsed_seconds':1.,'command':[]})

def controls():
 r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
 return {'count':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'passed':r.wasSuccessful()}

def run_controls(script):
 p=subprocess.run([sys.executable,'-B',str(BASE/script),'--controls'],capture_output=True,text=True)
 need(p.returncode==0,'producer_controls_failed:'+script)
 c=json.loads(p.stdout.strip().splitlines()[-1]); need(c['errors']==c['failures']==0,'producer_control_result')
 return {'exit':p.returncode,'result':c,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),
         'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}

def evaluate():
 for name,expected in PINS.items(): need(sha(BASE/name)==expected,'pin:'+name)
 # Import only the frozen independent module's constant pin dictionary; no calculation.
 spec=importlib.util.spec_from_file_location('independent_frozen',BASE/'verify_contact_damage.py')
 module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
 allpins={**module.PINS,**PINS}
 def pins():
  p={k:sha(BASE/k) for k in allpins}; exact(p,allpins,'pins'); p['adapter']=sha(__file__); return p
 before=pins(); own1=load('independent-contact-damage01.json'); own2=load('independent-contact-damage02.json')
 need(own1['status']==own2['status']=='PASS','own_status')
 ownrepeat=exact(normalize_repeat(own1,True),normalize_repeat(own2,True),'own_repeat')
 for own in (own1,own2):
  exact(own['pins_before'],own['pins_after'],'own_unchanged')
  exact(own['pins_before'],{**module.PINS,'producer':PINS['verify_contact_damage.py']},'own_pins')
 # Read settings only from the independently checked exact input, no new geometry calculation.
 with module.np.load(BASE/'exact-proximity80.npz',allow_pickle=False) as z: settings=z['settings'].tolist()
 expected=expected_root(own1['result'],settings)
 reruns={s:run_controls(s) for s in ('verify_contact_damage.py','contact_damage_join.py')}
 roots=[load('contact-damage01.json'),load('contact-damage02.json')]
 repeat=exact(normalize_repeat(roots[0]),normalize_repeat(roots[1]),'root_repeat')
 counters=[]
 verification=load('independent-exact-reference80-root01.json')
 need(verification['status']==verification['result']['status']=='PASS' and verification['result']['precision_bits']==80,'reference_pass')
 for name in ('exact-proximity80.json','exact-proximity80.npz'):
  exact(verification['pins_before'][name],module.PINS[name],'reference_identity')
 for index,r in enumerate(roots,1):
  need(set(r)=={'code_sha256','command','controls','elapsed_seconds','pins_after','pins_before','result','status','verification'},'root_receipt_keys')
  exact(r['status'],'PASS','root_status'); exact(r['code_sha256'],PINS['contact_damage_join.py'],'root_code')
  exact(r['verification'],{'file':'independent-exact-reference80-root01.json','sha256':PINS['independent-exact-reference80-root01.json']},'root_verification')
  exact(r['command'],['contact_damage_join.py','--output',f'contact-damage0{index}.json','--verification',r['verification']['file'],'--verification-sha',r['verification']['sha256']],'root_command')
  pinmap={k:module.PINS[v] for k,v in ROOT_PIN_NAMES.items()}
  exact(r['pins_before'],pinmap,'root_input_pins'); exact(r['pins_after'],pinmap,'root_after_pins')
  exact(r['controls'],reruns['contact_damage_join.py']['result'],'root_controls')
  counters.append(dict(exact(normalized(r['result']),expected,'root_result')))
 exact(own1['controls'],reruns['verify_contact_damage.py']['result'],'own_controls')
 after=pins(); exact(before,after,'after_pins')
 result={'status':'PASS','all_root_result_fields_compared':sorted(expected.keys()),
  'root_result_leaf_comparisons_per_repeat':counters,'root_repeat_leaf_comparisons':dict(repeat),
  'own_repeat_leaf_comparisons':dict(ownrepeat),'groups_compared_per_repeat':len(expected['groups']),
  'positive_groups':sum(g['matching_typed_elements']>0 for g in expected['groups']),
  'zero_groups':sum(g['matching_typed_elements']==0 for g in expected['groups']),
  'matched_element_group_records':len(expected['matches']),
  'contact_relations':sum(len(m['contact_relations']) for m in expected['matches']),
  'independent_source_reconciliation':own1['result']['source_reconciliation'],
  'independent_master_aliases_checked':len(own1['result']['master_aliases']),
  'master_alias_matches':len(expected['master_alias_matches']),
  'normalizations':['Only outer group/match/master lists reorder by explicit unique identity keys.',
   'Own per-node/master/element rows aggregate by exact typed element and group; all node IDs, ordered contact relations, list ordinals and locators compare.',
   'Root repeat excludes only validated elapsed_seconds and output filename command[2]; own repeat additionally excludes validated peak_bytes.',
   'Scope/CaseA strings are exact checked representation of reviewed inference limits, not independent physical evidence.'],
  'coverage_limits':['No raw-source or exact-geometry recalculation in this adapter; both independent calculations use the same preserved derivative sources.',
   'Root does not retain all negative per-element identity/coordinate rows; the independent join separately reconciles all1904 against both derivative inputs and571shared coordinate IDs.',
   'Independent extra candidate rows, all742negative aliases and full coordinate/locator details are not fabricated as root output fields.'],
  'scope':'Exact agreement of this static typed-list join; not actual deletion, pairing, restraint, historical execution or cause.',
  'producer_control_reruns':reruns}
 return result,before,after

def main():
 p=argparse.ArgumentParser(); p.add_argument('--controls',action='store_true'); p.add_argument('--out',default='independent-contact-damage-comparison01.json'); args=p.parse_args()
 c=controls()
 if args.controls: print(json.dumps(c)); return 0 if c['passed'] else 1
 need(re.fullmatch(r'independent-contact-damage-comparison(?:-root)?[0-9]+\.json',args.out) is not None,'output_scope')
 path=BASE/args.out; need(not path.exists(),'existing_output')
 start=time.monotonic(); record={'status':'FAIL','command':sys.argv,'controls':c}
 try:
  need(c['passed'],'comparison_controls_failed'); result,before,after=evaluate()
  record.update(status='PASS',result=result,pins_before=before,pins_after=after)
 except Exception as e: record['error']=str(e) if isinstance(e,Mismatch) else type(e).__name__
 record.update(elapsed_seconds=time.monotonic()-start,peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024))
 with path.open('x') as f: json.dump(record,f,sort_keys=True,indent=2,allow_nan=False); f.write('\n')
 print(json.dumps({'status':record['status'],'receipt':path.name,'sha256':sha(path),'error':record.get('error')}))
 return 0 if record['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
