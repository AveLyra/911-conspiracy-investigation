#!/usr/bin/env python3
"""Post-freeze Arm A adapter: compare records, never parse/execute raw sources.

Independent producer/results are immutable inputs. The root spring inventory is
covered by repeat equality only, NOT independent source verification here.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import resource
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
PINS = {
 'independent_casea.py':'19657afc02b4d63ba98e3374f153ce86ab1cfbc7575a6275fb64fc289eaa170c',
 'independent-casea01.json':'0dc0c853ca9fe6e58a06f366c3e71febbf3d5e70c235fa9434a47f8f8b5294eb',
 'casea_join.py':'40eb86742ac3348c7c2e49bfd6a497622e2e78a2a174c7939fdc4ad62ce5e6f2',
 'casea-root01.json':'27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
 'casea-root02.json':'4b1fff82bdb8778045bbe880d2bbf708d03788191480c0883b2bbd8fcfab4432',
 'PROTOCOL.md':'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41',
 '../CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
 '../model-member-map/method-source-review.md':'cbea5556de774752fefc82ff5c49ed299bb73ea3fb65af0fcafc7c0e7f24fe5f',
 '../model-member-map/map_members.py':'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b',
 '../model-member-map/run06/receipt.json':'4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d',
 '../c79-contact-geometry/extract_controls.py':'f970de77c746133d5935209e2294e9e623127b17e417a756d88a9ba2e2dd8826',
 '../c79-contact-geometry/contact-damage01.json':'e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479',
 '../c79-contact-geometry/exact-proximity80.json':'25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
 '../c79-contact-geometry/exact-proximity80.npz':'79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
 '../c79-contact-geometry/independent-exact-reference80-root01.json':'4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8',
 '../c79-contact-geometry/stage-root01.json':'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
 '../c79-contact-geometry/stage-root01.npz':'2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
}
SOURCES = {
 'G6A_CaseA_El_Delete_List.k.gz':117, 'discrete_mass.k.gz':119,
 'elem_thick_to-renum.k.gz':120, 'wtc7_global_8a_no-conn-matl.k.gz':121,
 'WTC7_CaseB_400pm.int.gz':118,
}
ROOT_KEYS = {'casea','cross_family','groups','includes','limits',
 'master_alias_membership','relation_columns','relations','selected_coordinates',
 'shells','source_element_counts','source_node_counts','sources',
 'springs_numeric_inventory','transforms','unmatched_shell_ids'}
OWN_KEYS = {'candidate_node_ids','cross_family_coincidences','ground_discrete_count',
 'groups','ignored_keyword_counts','includes','list','master_aliases',
 'master_vertex_ids','membership_ordinal_schema','relations','scope',
 'selected_coordinate_scalars_compared','selected_coordinates','shells',
 'source_element_counts','source_node_counts','unmatched_shell_ids'}

class Failure(Exception): pass
def need(ok, code):
 if not ok: raise Failure(code)
def sha(path):
 with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def schema(obj, keys):
 need(type(obj) is dict and set(obj)==set(keys),'schema_mismatch')
def pin_check():
 got={name:sha(BASE/name) for name in PINS}
 need(got==PINS,'input_pin_mismatch')
 got['consumer']=sha(Path(__file__))
 return got

def equality(left, right):
 """Exact numeric equality, no tolerance; distinguish bool from numeric.

 Arrays are never sorted or deduplicated here. Mismatch values are represented
 by hashes, not arbitrary payload text. Total mismatches survive truncation.
 """
 out={'equal':True,'leaf_comparisons':0,'container_comparisons':0,
      'mismatch_count':0,'mismatches':[]}
 def bad(path,a,b):
  out['equal']=False;out['mismatch_count']+=1
  if len(out['mismatches'])<100:
   out['mismatches'].append({'path':path,'left_sha256':digest(a),'right_sha256':digest(b)})
 def walk(a,b,path):
  if type(a) is dict and type(b) is dict:
   out['container_comparisons']+=1
   if set(a)!=set(b):bad(path+'/keys',sorted(a),sorted(b))
   for k in sorted(set(a)&set(b)):walk(a[k],b[k],path+'/'+str(k))
  elif type(a) is list and type(b) is list:
   out['container_comparisons']+=1
   if len(a)!=len(b):bad(path+'/length',len(a),len(b))
   for i,(x,y) in enumerate(zip(a,b)):walk(x,y,path+'/'+str(i))
  else:
   out['leaf_comparisons']+=1
   numeric=type(a) in (int,float) and type(b) in (int,float)
   same=(math.isfinite(a) and math.isfinite(b) and a==b) if numeric else type(a) is type(b) and a==b
   if not same:bad(path,a,b)
 walk(left,right,'')
 out['left_sha256']=digest(left);out['right_sha256']=digest(right)
 return out

def root_common(result):
 schema(result,ROOT_KEYS)
 # All fields of these result sections are compared, not selected positives.
 direct=['casea','cross_family','groups','master_alias_membership','relation_columns',
  'relations','selected_coordinates','shells','source_element_counts',
  'source_node_counts','unmatched_shell_ids']
 out={k:result[k] for k in direct}
 out['includes']=[]
 for row in result['includes']:
  schema(row,{'included','kind','line','source'})
  need(row['kind'] in ('*INCLUDE','*INCLUDE_TRANSFORM'),'include_kind')
  need(row['included'] in SOURCES and row['source'] in SOURCES,'include_target')
  out['includes'].append({'source':SOURCES[row['source']],
   'target_source':SOURCES[row['included']], 'keyword_line':row['line'],
   'transformed':row['kind']=='*INCLUDE_TRANSFORM'})
 out['transforms']=[]
 for row in result['transforms']:
  schema(row,{'FCTTEM_caveat','cards','coordinate_transform','line','source'})
  need(row['FCTTEM_caveat']=='numeric_1_in_character_conversion_flag_field','FCTTEM_interpretation')
  need(row['coordinate_transform']=='identity','coordinate_transform')
  out['transforms'].append({'source':SOURCES[row['source']],
    'keyword_line':row['line'],'cards':row['cards']})
 out['sources']={}
 for name,row in result['sources'].items():
  schema(row,{'compressed_bytes','compressed_sha256','eof','lines','pin_after','uncompressed_bytes','uncompressed_sha256'})
  need(name in SOURCES and SOURCES[name]!=118,'unexpected_read_source')
  out['sources'][str(SOURCES[name])]=row
 return out

def own_common(result,sources):
 schema(result,OWN_KEYS)
 listed=result['list'];h=listed['header']
 counts=Counter(m['eid'] for m in listed['members'])
 need(listed['unique_ids']==sorted(counts),'own_unique_id_coverage')
 need(listed['duplicates']==[{'eid':k,'count':v} for k,v in sorted(counts.items()) if v>1],'own_duplicate_summary')
 need(listed['duplicate_occurrences']==sum(v-1 for v in counts.values()),'own_duplicate_occurrences')
 derived_members=[];zero=blank=0
 for index,row in enumerate(listed['rows']):
  need(row['row_index']==index and len(row['values'])==8,'own_card_schema')
  for slot,v in enumerate(row['values']):
   if v is None:blank+=1
   elif v==0:zero+=1
   else:
    need(type(v) in (int,float) and int(v)==v and v>0,'own_member_id')
    derived_members.append({'eid':int(v),'line':row['line'],'row_index':index,
     'slot':slot,'positive_ordinal':len(derived_members)+1})
 need(derived_members==listed['members'],'own_complete_card_membership')
 need(zero==listed['explicit_zero_slots'] and blank==listed['blank_slots'],'own_padding_counts')
 out={'casea':{'header':{'source':h['source'],'set_id':int(h['values'][0]),
  'keyword_line':h['keyword_line'],'header_line':h['line'],'values':h['values']},
  'cards':[{'line':r['line'],'values':r['values']} for r in listed['rows']],
  'members':[{'line':m['line'],'slot':m['slot']+1,'ordinal':m['positive_ordinal'],
   'eid':m['eid']} for m in listed['members']],
  'unique_ids':len(listed['unique_ids']),'duplicate_ids':{str(k):v for k,v in sorted(counts.items()) if v>1},
  'zero_slots':zero,'blank_slots':blank}}
 def elem(r):
  return {'source':r['source'],'line':r['line'],'kind':r['family'],'eid':r['eid'],
   'original_pid':r['original_pid'],'pid':r['effective_pid'],'nodes':r['node_slots']}
 out['shells']=[elem(r) for r in result['shells']]
 need([r['eid'] for r in result['shells']]==sorted({r['eid'] for r in result['shells']}),'own_shell_order_duplicate')
 need(sorted(set(counts)-{r['eid'] for r in result['shells']})==result['unmatched_shell_ids'],'own_unmatched_summary')
 need(all(r['family']=='shell' and r['eid'] in counts for r in result['shells']),'own_shell_namespace')
 out['cross_family']={f:[] for f in ('beam','discrete','solid')}
 for row in result['cross_family_coincidences']:
  need(row['family'] in out['cross_family'] and row['eid'] in counts,'own_cross_namespace')
  out['cross_family'][row['family']].append(elem(row))
 for f in out['cross_family']:out['cross_family'][f].sort(key=lambda r:r['eid'])
 out['selected_coordinates']=[{k:r[k] for k in ('nid','source','line','xyz')} for r in result['selected_coordinates']]
 selected_ids=[r['nid'] for r in result['selected_coordinates']]
 need(selected_ids==sorted(set(result['candidate_node_ids'])|set(result['master_vertex_ids'])),'own_coordinate_coverage')
 need(result['selected_coordinate_scalars_compared']==3*len(selected_ids),'own_coordinate_summary')
 out['source_element_counts']={str(s)+':'+f:c for s,v in result['source_element_counts'].items() for f,c in v.items()}
 out['source_node_counts']=result['source_node_counts']
 out['unmatched_shell_ids']=result['unmatched_shell_ids']
 out['relation_columns']=['setting_index','cid','geometry_class','master_index','nid','eid']
 out['relations']=sorted([[r['setting_index'],r['cid'],r['class'],r['master_index'],r['node_id'],
  result['shells'][r['element_index']]['eid']] for r in result['relations']])
 out['groups']=[]
 need([(g['setting_index'],g['cid'],g['class']) for g in result['groups']]==
  [(s,c,k) for s in range(3) for c in (1,2) for k in (0,2,3)],'own_complete_group_coverage')
 for g in result['groups']:
  rels=[r for r in result['relations'] if (r['setting_index'],r['cid'],r['class'])==(g['setting_index'],g['cid'],g['class'])]
  need(g['relation_count']==len(rels)==len(g['relation_indices']),'own_group_relation_count')
  need([result['relations'][i] for i in g['relation_indices']]==rels,'own_group_relation_indices')
  need(sorted({r['node_id'] for r in rels})==g['matching_node_ids'],'own_group_matching_nodes')
  need(sorted({r['element_index'] for r in rels})==g['matching_element_indices'],'own_group_matching_elements')
  out['groups'].append({'setting_index':g['setting_index'],'cid':g['cid'],
   'geometry_class':g['class'],'selected_nodes':g['candidate_node_ids'],
   'matching_nodes':g['matching_node_ids'],
   'matching_eids':sorted(result['shells'][i]['eid'] for i in g['matching_element_indices']),
   'relation_count':g['relation_count']})
 out['master_alias_membership']=[{'master_index':r['master_index'],'eid':r['eid'],
  'source':r['source'],'line':r['line'],'listed':r['matching_element_index'] is not None} for r in result['master_aliases']]
 out['includes']=[{k:r[k] for k in ('source','target_source','keyword_line','transformed')} for r in result['includes']]
 out['transforms']=[{'source':r['source'],'keyword_line':r['keyword_line'],
  'cards':[c['values'] for c in r['cards']]} for r in result['includes'] if r['transformed']]
 out['sources']={}
 for source,row in sources.items():
  schema(row,{'compressed_after','compressed_bytes','compressed_sha256','eof','lines',
   'source','uncompressed_bytes','uncompressed_sha256'})
  need(str(row['source'])==source and row['compressed_after']==row['compressed_sha256'],'own_source_identity')
  out['sources'][source]={k:row[k] for k in ('compressed_bytes','compressed_sha256','eof','lines','uncompressed_bytes','uncompressed_sha256')}
  out['sources'][source]['pin_after']=True
 return out

def controls():
 # Full synthetic inputs and comparison outputs are retained in the receipt.
 fixture={'members':[{'eid':7,'ordinal':1,'slot':1},{'eid':8,'ordinal':2,'slot':2}],
  'shell':{'eid':7,'kind':'shell','source':120,'line':8,'pid':1004,'nodes':[1,2,3,4]},
  'coordinates':[[1.,2.,3.]],'groups':[{'class':0,'matches':[]},{'class':2,'matches':[]}],
  'values':[None,0.,1.],'relations':[[0,1,3,7,2,7]],'unmatched':[],'master':{'listed':False}}
 variants=[]
 def add(name,mutate):
  x=copy.deepcopy(fixture);mutate(x);variants.append((name,x))
 add('changed_record',lambda x:x['shell'].__setitem__('eid',8))
 add('changed_order',lambda x:x['members'].reverse())
 add('changed_coordinate',lambda x:x['coordinates'][0].__setitem__(2,3.0000000000000004))
 add('changed_namespace',lambda x:x['shell'].__setitem__('pid',4))
 add('changed_family',lambda x:x['shell'].__setitem__('kind','beam'))
 add('changed_source',lambda x:x['shell'].__setitem__('source',121))
 add('changed_locator',lambda x:x['shell'].__setitem__('line',9))
 add('missing_zero_group',lambda x:x['groups'].pop())
 add('blank_became_zero',lambda x:x['values'].__setitem__(0,0))
 add('missing_relation',lambda x:x['relations'].clear())
 add('duplicate_member',lambda x:x['members'].append(copy.deepcopy(x['members'][0])))
 add('false_becomes_numeric_zero',lambda x:x['master'].__setitem__('listed',0))
 add('changed_connectivity_order',lambda x:x['shell']['nodes'].reverse())
 add('extra_field',lambda x:x['shell'].__setitem__('extra',0))
 add('missing_negative_list',lambda x:x.pop('unmatched'))
 add('missing_member_slot',lambda x:x['members'][0].pop('slot'))
 rows=[{'name':'unchanged','input':fixture,'output':equality(fixture,fixture),'expected_equal':True}]
 for name,x in variants:rows.append({'name':name,'input':x,'output':equality(fixture,x),'expected_equal':False})
 need(all(r['output']['equal']==r['expected_equal'] for r in rows),'comparison_controls_failed')
 with tempfile.TemporaryDirectory(prefix='casea-comparison-control-') as folder:
  path=Path(folder)/'synthetic';path.touch();original=sha(path)
  refused=False
  try:path.open('x')
  except FileExistsError:refused=True
  need(refused and sha(path)==original,'create_only_control')
 try:schema({'a':1,'extra':2},{'a'})
 except Failure:rejected=True
 else:rejected=False
 need(rejected,'schema_control')
 return {'passed':True,'count':len(rows)+2,'fixture':fixture,'comparisons':rows,
  'create_only_refused':refused,'unexpected_schema_field_rejected':rejected}

def recorded_pins(data, independent):
 need(data['pins_before']==data['pins_after'],'producer_changed_pins')
 for name,value in data['pins_before'].items():
  if independent:path='independent_casea.py' if name=='producer' else name
  else:path=name[len(BASE.name)+1:] if name.startswith(BASE.name+'/') else '../'+name
  need(path in PINS and PINS[path]==value,'producer_recorded_pin')

def calculate():
 own=json.loads((BASE/'independent-casea01.json').read_text())
 first=json.loads((BASE/'casea-root01.json').read_text())
 repeat=json.loads((BASE/'casea-root02.json').read_text())
 need(all(r['status']=='PASS' for r in (own,first,repeat)),'producer_status')
 need(own['controls']=={'count':25,'errors':0,'failures':0,'passed':True},'independent_controls')
 for root in (first,repeat):
  need(root['controls']=={'count':12,'errors':0,'failures':0},'root_controls')
  need(root['code_sha256']==PINS['casea_join.py'],'root_code_pin')
 recorded_pins(own,True);recorded_pins(first,False);recorded_pins(repeat,False)
 a=own_common(own['result'],own['sources']);b=root_common(first['result'])
 sections={k:equality(a[k],b[k]) for k in sorted(a)}
 need(set(a)==set(b),'common_sections')
 # A repeat check covers every root result field, including the separately
 # unverified spring inventory. Only declared runtime/output metadata varies.
 repeat_sections={k:equality(first['result'][k],repeat['result'][k]) for k in sorted(ROOT_KEYS)}
 topkeys={'code_sha256','command','controls','dependency_reuse','elapsed_seconds',
  'maxrss_bytes_darwin','pins_after','pins_before','result','status'}
 schema(first,topkeys);schema(repeat,topkeys)
 metadata={k:equality(first[k],repeat[k]) for k in sorted(topkeys-{'result','command','elapsed_seconds','maxrss_bytes_darwin'})}
 need(first['command'][-2:]==['--output','casea-root01.json'] and repeat['command'][-2:]==['--output','casea-root02.json'],'root_output_command')
 metadata['command_prefix']=equality(first['command'][:-1],repeat['command'][:-1])
 passed=all(x['equal'] for x in list(sections.values())+list(repeat_sections.values())+list(metadata.values()))
 return {'passed':passed,'common_sections':sections,'root_repeat_sections':repeat_sections,
  'root_repeat_metadata':metadata,'repeat_runtime_metadata':[
   {k:r[k] for k in ('elapsed_seconds','maxrss_bytes_darwin','command')} for r in (first,repeat)],
  'counts':{'membership_rows':len(a['casea']['cards']),'member_occurrences':len(a['casea']['members']),
   'unique_ids':a['casea']['unique_ids'],'shells':len(a['shells']),
   'cross_family':{f:len(v) for f,v in a['cross_family'].items()},
   'selected_coordinates':len(a['selected_coordinates']),'xyz_scalars':3*len(a['selected_coordinates']),
   'groups':len(a['groups']),'zero_groups':sum(not g['matching_eids'] and g['relation_count']==0 for g in a['groups']),
   'relations':len(a['relations']),'master_aliases':len(a['master_alias_membership']),
   'listed_master_aliases':sum(r['listed'] for r in a['master_alias_membership']),
   'unmatched_shell_ids':len(a['unmatched_shell_ids']),
   'full_stream_lines':sum(r['lines'] for r in a['sources'].values()),
   'full_stream_bytes':sum(r['uncompressed_bytes'] for r in a['sources'].values())},
  'uncompared_independent_fields':[
   'Raw numeric-row hashes/format, thickness values/card locators, NODE constraint fields and beam/discrete orientation fields are independent-only outputs, not dual numeric verification.',
   'Candidate-pair-row counts and expanded relation provenance/list-index columns have no root counterpart; actual relation lists are empty. Independent internal membership/group checks are recorded, not new source evidence.',
   'Ignored-keyword hashed counts and ground-discrete count are independent-only summaries.'],
  'root_only_scope':[
   'Spring numeric inventory: root repeat equality only; not independently source-verified by this Arm A adapter.',
   'Root freshly checked all selected master-shell rows against frozen aliases. Independent Arm A newly extracted all master-vertex coordinates and CaseA shells, but used frozen master-alias metadata for unlisted alias membership; full nonlisted master-shell connectivity is not a new dual source extraction.',
   'Root global NODE duplicate check is broader than independent selected-NODE duplicate check.'],
  'interpretive_limits':[
   'Exact agreement for saved static membership/coordinate/version fields is not solver activation, physical support, deletion timing, force, historical run authentication or collapse cause.',
   'The 18 zero groups remain fixed candidate-setting/CID/class selections, not an all-building or all-damage exclusion.',
   'Cross-family numeric coincidences do not merge namespaces or establish deletion semantics.',
   'Declared numeric equality permits exact integral int/float equivalence, never a tolerance; booleans remain distinct.']}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--controls',action='store_true')
 parser.add_argument('--out',default='casea-comparison01.json');args=parser.parse_args()
 if args.controls:
  out=controls();print(json.dumps({'passed':out['passed'],'count':out['count']}));return 0
 need(re.fullmatch(r'casea-comparison(?:-root)?[0-9]+\.json',args.out) is not None,'output_scope')
 path=BASE/args.out
 with path.open('x') as handle:
  start=time.monotonic();receipt={'status':'FAIL','command':sys.argv}
  try:
   receipt['controls']=controls()
   receipt['pins_before']=pin_check();receipt['comparison']=calculate()
   receipt['pins_after']=pin_check();need(receipt['pins_before']==receipt['pins_after'],'changed_inputs')
   receipt['status']='PASS' if receipt['comparison']['passed'] else 'FAIL'
  except Exception as exc:
   receipt['failure']={'class':type(exc).__name__,'detail_sha256':hashlib.sha256(str(exc).encode()).hexdigest()}
   if isinstance(exc,Failure):receipt['failure']['code']=str(exc)
  receipt.update(elapsed_seconds=time.monotonic()-start,
   peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
   runtime={'python':sys.version,'executable':sys.executable})
  json.dump(receipt,handle,sort_keys=True,indent=2,allow_nan=False);handle.write('\n')
 print(json.dumps({'status':receipt['status'],'file':path.name,'sha256':sha(path),
  'counts':receipt.get('comparison',{}).get('counts'),'failure':receipt.get('failure')}))
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
