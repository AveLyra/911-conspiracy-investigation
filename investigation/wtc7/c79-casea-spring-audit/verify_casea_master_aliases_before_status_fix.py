#!/usr/bin/env python3
"""Prospective supplement: fresh full-stream master-shell version check.

Reuses only the author's frozen independent CaseA numeric reader. All selected
master alias EIDs from the pinned stage are freshly located in full SRC119–121.
Compare source, physical line, original/effective PID, ordered shell nodes and
paired thickness fields/line. A master face may order its nodes differently
from its shell alias; preserve both orders and the reported ordered-match flag.
Use the frozen fresh CaseA list only for membership, without rescanning SRC117.
No initialized contact, deletion, force, history, solver or spring-law claim.
"""
import argparse
from collections import Counter,defaultdict
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent
READER_SHA='19657afc02b4d63ba98e3374f153ce86ab1cfbc7575a6275fb64fc289eaa170c'
PINS={
 'independent_casea.py':READER_SHA,
 'independent-casea01.json':'0dc0c853ca9fe6e58a06f366c3e71febbf3d5e70c235fa9434a47f8f8b5294eb',
 'compare_casea_independent.py':'7c8c330cca7d9a1a79e454bca1adb5f8eb9a2051c5c9ea2e49b4a5c72fc1cde0',
 'casea-comparison01.json':'6dcd6bd5ff6c41ffcd09f6c748c4c9ff7ac63ed569ae23e15816d01dd32c7a50',
 'PROTOCOL.md':'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41',
 '../CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
 '../c79-contact-geometry/stage-root01.json':'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
}
class Failure(Exception):pass
def need(ok,code):
 if not ok:raise Failure(code)
def sha(path):
 with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()
def load_reader():
 need(sha(BASE/'independent_casea.py')==READER_SHA,'reader_pin')
 spec=importlib.util.spec_from_file_location('frozen_own_casea_reader',BASE/'independent_casea.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module
def pins(reader):
 result={k:sha(BASE/k) for k in PINS};need(result==PINS,'dependency_pin')
 result['own_reader_dependencies']=reader.pins()
 result['supplement']=sha(Path(__file__))
 return result

def expected_aliases(masters):
 expected=[]
 for mi,m in enumerate(masters):
  need(set(m)=={'aliases','attributes','line','nodes','set_id','xyz'},'master_schema')
  need(m['set_id'] in (1,2),'master_set_id')
  for ai,a in enumerate(m['aliases']):
   need(set(a)=={'eid','line','nodes','ordered_match','original_pid','pid','source','thickness_card','thickness_line'},'alias_schema')
   expected.append({'master_index':mi,'alias_index':ai,'cid':m['set_id'],
    'set_id':m['set_id'],'master_line':m['line'],'master_nodes':m['nodes'],
    'eid':a['eid'],'source':a['source'],'line':a['line'],
    'original_pid':a['original_pid'],'effective_pid':a['pid'],
    'ordered_nodes':a['nodes'],'thickness_values':a['thickness_card'],
    'thickness_line':a['thickness_line'],'ordered_match':a['ordered_match']})
 return expected

def compare_aliases(expected,actual,listed):
 index={}
 for i,r in enumerate(actual):
  need(r['family']=='shell','actual_wrong_family')
  need(r['eid'] not in index,'actual_duplicate_shell')
  index[r['eid']]=i
 requested={r['eid'] for r in expected}
 missing=sorted(requested-set(index));extra=sorted(set(index)-requested)
 rows=[]
 for e in expected:
  i=index.get(e['eid']);r=None if i is None else actual[i]
  fields={key:r is not None and e[key]==r[key] for key in
   ('eid','source','line','original_pid','effective_pid','thickness_values','thickness_line')}
  fields['ordered_nodes']=r is not None and e['ordered_nodes']==r['node_slots']
  fields['master_node_multiset']=r is not None and sorted(e['master_nodes'])==sorted(r['node_slots'])
  fields['ordered_match_flag']=r is not None and type(e['ordered_match']) is bool and e['ordered_match']==(r['node_slots']==e['master_nodes'])
  rows.append({'expected':e,'actual_element_index':i,'field_equal':fields,
   'listed_in_frozen_casea':e['eid'] in listed,'passed':all(fields.values())})
 return {'passed':not missing and not extra and all(r['passed'] for r in rows),
  'missing_eids':missing,'extra_eids':extra,'alias_comparisons':rows,
  'comparison_fields':['eid','source','line','original_pid','effective_pid',
   'thickness_values','thickness_line','ordered_nodes','master_node_multiset','ordered_match_flag']}

def controls(reader):
 old=reader.controls();need(old['passed'],'own_reader_controls_failed')
 e={'master_index':0,'alias_index':0,'cid':1,'set_id':1,'master_line':90,
  'master_nodes':[2,1,4,3],'eid':7,'source':120,'line':50,
  'original_pid':4,'effective_pid':1004,'ordered_nodes':[1,2,3,4],
  'thickness_values':[.1,.2,.3,.4,None],'thickness_line':51,'ordered_match':False}
 r={'eid':7,'family':'shell','source':120,'line':50,'original_pid':4,
  'effective_pid':1004,'node_slots':[1,2,3,4],
  'thickness_values':[.1,.2,.3,.4,None],'thickness_line':51}
 variants=[]
 for key,value in [('source',121),('line',49),('original_pid',5),('effective_pid',4),
  ('node_slots',[2,1,4,3]),('thickness_values',[.1,.2,.3,.5,None]),
  ('thickness_line',52)]:
  x=copy.deepcopy(r);x[key]=value;variants.append((key,[x]))
 variants.extend([('missing',[]),('extra',[r,{**r,'eid':8}])])
 cases=[{'name':'exact_unlisted','expected':[e],'actual':[r],'listed':[],
  'output':compare_aliases([e],[r],set()),'expected_pass':True},
  {'name':'exact_listed','expected':[e],'actual':[r],'listed':[7],
  'output':compare_aliases([e],[r],{7}),'expected_pass':True}]
 for name,actual in variants:
  cases.append({'name':name,'expected':[e],'actual':actual,'listed':[],
   'output':compare_aliases([e],actual,set()),'expected_pass':False})
 changed=copy.deepcopy(e);changed['ordered_match']=True
 cases.append({'name':'incorrect_order_flag','expected':[changed],'actual':[r],
  'listed':[],'output':compare_aliases([changed],[r],set()),'expected_pass':False})
 # Repeated physical vertices and repeated alias references are retained.
 triangle={**e,'master_nodes':[1,2,3,3],'ordered_nodes':[1,2,3,3],'ordered_match':True}
 tr={**r,'node_slots':[1,2,3,3]}
 cases.append({'name':'triangle_repeated_alias','expected':[triangle,triangle],
  'actual':[tr],'listed':[7],'output':compare_aliases([triangle,triangle],[tr],{7}),
  'expected_pass':True})
 need(all(c['output']['passed']==c['expected_pass'] for c in cases),'alias_controls_failed')
 need(cases[0]['output']['alias_comparisons'][0]['listed_in_frozen_casea'] is False and
  cases[1]['output']['alias_comparisons'][0]['listed_in_frozen_casea'] is True,'membership_control')
 rejected={}
 for name,rows in [('duplicate_shell',[r,r]),('wrong_family',[{**r,'family':'beam'}])]:
  try:compare_aliases([e],rows,set())
  except Failure:rejected[name]=True
  else:rejected[name]=False
 need(all(rejected.values()),'alias_rejection_controls')
 with tempfile.TemporaryDirectory(prefix='master-alias-control-') as folder:
  path=Path(folder)/'synthetic';path.touch();before=sha(path)
  try:path.open('x')
  except FileExistsError:refused=True
  else:refused=False
  need(refused and before==sha(path),'output_guard_control')
 return {'passed':True,'own_reader':old,'new_count':len(cases)+3,
  'cases':cases,'rejection_controls':rejected,'create_only_refused':refused}

def calculate(reader,receipt,start):
 stage=json.loads((BASE/'../c79-contact-geometry/stage-root01.json').read_text())
 need(stage['status']=='PASS','stage_status')
 expected=expected_aliases(stage['result']['master_segments'])
 need(len(expected)==742,'alias_coverage')
 old=json.loads((BASE/'independent-casea01.json').read_text())
 need(old['status']=='PASS','original_source_status')
 listed=set(old['result']['list']['unique_ids'])
 prior=old['result']['master_aliases']
 need(len(prior)==len(expected),'prior_alias_coverage')
 for e,r in zip(expected,prior):
  for key in ('master_index','alias_index','cid','set_id','master_line','eid','source',
   'line','original_pid','effective_pid','ordered_nodes'):
   need(e[key]==r[key],'prior_alias_identity')
  need((r['matching_element_index'] is not None)==(e['eid'] in listed),'prior_alias_membership')
 del old,prior,stage
 wanted={e['eid'] for e in expected}
 mesh={'shells':[],'cross_family_coincidences':[],'coordinates':{},'includes':[],
  'node_counts':Counter(),'element_counts':defaultdict(Counter),'ground_discrete_count':0,
  'ignored_keyword_counts':Counter()}
 seen={key:bytearray(reader.ID_CAP) for key in ('shell','beam','discrete','solid')}
 for source in (121,119,120):
  receipt['sources'][source]={}
  reader.scan_mesh(reader.stream(source,receipt['sources'][source],start),source,
   wanted,set(),seen,mesh)
  if source==121:
   need(sorted((r['target_source'],r['transformed']) for r in mesh['includes'])==
    [(118,False),(119,False),(120,True)],'include_graph')
  reader.resource_guard(start)
 mesh['shells'].sort(key=lambda r:(r['eid'],r['source'],r['line']))
 comparison=compare_aliases(expected,mesh['shells'],listed)
 return {'comparison':comparison,'fresh_shell_records':mesh['shells'],
  'cross_family_coincidences':mesh['cross_family_coincidences'],
  'source_element_counts':dict(mesh['element_counts']),
  'source_node_counts':dict(mesh['node_counts']),'includes':mesh['includes'],
  'ground_discrete_count':mesh['ground_discrete_count'],
  'ignored_keyword_counts':dict(mesh['ignored_keyword_counts']),
  'counts':{'aliases':len(expected),'unique_alias_eids':len(wanted),
   'fresh_shell_records':len(mesh['shells']),
   'alias_field_tests':sum(len(r['field_equal']) for r in comparison['alias_comparisons']),
   'failed_alias_rows':sum(not r['passed'] for r in comparison['alias_comparisons']),
   'listed_aliases':sum(r['listed_in_frozen_casea'] for r in comparison['alias_comparisons']),
   'ordered_match_true':sum(r['expected']['ordered_match'] for r in comparison['alias_comparisons']),
   'cross_family_coincidences':len(mesh['cross_family_coincidences']),
   'source_lines':sum(r['lines'] for r in receipt['sources'].values()),
   'source_uncompressed_bytes':sum(r['uncompressed_bytes'] for r in receipt['sources'].values())},
  'scope':'Fresh complete SRC119-121 numeric element streams; selected master shell source/version/connectivity/thickness check only. CaseA membership uses the frozen independent SRC117 pass. No raw SRC117 rescan, new coordinate extraction, spring verification, solver, activation, force, support-capacity, history or cause claim.'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--controls',action='store_true')
 parser.add_argument('--out',default='independent-master-aliases01.json');args=parser.parse_args()
 if args.controls:
  c=controls(load_reader());print(json.dumps({'passed':c['passed'],
   'own_reader_count':c['own_reader']['count'],'new_count':c['new_count']}));return 0
 need(re.fullmatch(r'independent-master-aliases(?:-root)?[0-9]+\.json',args.out) is not None,'output_scope')
 path=BASE/args.out
 with path.open('x') as destination:
  start=time.monotonic();receipt={'status':'FAIL','command':sys.argv,'sources':{}}
  try:
   reader=load_reader();receipt['controls']=controls(reader)
   receipt['pins_before']=pins(reader);receipt['result']=calculate(reader,receipt,start)
   receipt['pins_after']=pins(reader);need(receipt['pins_before']==receipt['pins_after'],'changed_dependencies')
   receipt['status']='PASS' if receipt['result']['comparison']['passed'] else 'FAIL'
  except Exception as exc:
   receipt['failure']={'class':type(exc).__name__,
    'detail_sha256':hashlib.sha256(str(exc).encode()).hexdigest()}
   if isinstance(exc,Failure):receipt['failure']['code']=str(exc)
  receipt.update(elapsed_seconds=time.monotonic()-start,
   peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
   runtime={'python':sys.version,'executable':sys.executable},
   dependency_reuse='Own frozen independent_casea.py; not the root parser.')
  json.dump(receipt,destination,sort_keys=True,indent=2,allow_nan=False);destination.write('\n')
 print(json.dumps({'status':receipt['status'],'file':path.name,'sha256':sha(path),
  'counts':receipt.get('result',{}).get('counts'),'failure':receipt.get('failure')}))
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
