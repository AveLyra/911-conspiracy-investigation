#!/usr/bin/env python3
"""Independent full-stream CaseA typed-shell incidence; numeric data only."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import resource
import sys
import tempfile
import time
import unittest
import numpy as np

BASE=Path(__file__).resolve().parent
RAW=Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PINS={
 'PROTOCOL.md':'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41',
 '../CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
 '../model-member-map/method-source-review.md':'cbea5556de774752fefc82ff5c49ed299bb73ea3fb65af0fcafc7c0e7f24fe5f',
 '../model-member-map/run06/receipt.json':'4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d',
 '../c79-contact-geometry/extract_controls.py':'f970de77c746133d5935209e2294e9e623127b17e417a756d88a9ba2e2dd8826',
 '../c79-contact-geometry/exact-proximity80.json':'25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
 '../c79-contact-geometry/exact-proximity80.npz':'79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
 '../c79-contact-geometry/stage-root01.json':'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
 '../c79-contact-geometry/stage-root01.npz':'2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
 '../c79-contact-geometry/independent-exact-reference80-root01.json':'4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8',
}
FILES={
 117:('G6A_CaseA_El_Delete_List.k.gz',103872,'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273',325983,45156,'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25'),
 119:('discrete_mass.k.gz',70199,'2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7',508372,7905,'8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
 120:('elem_thick_to-renum.k.gz',23162693,'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59',232959541,4088491,'7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
 121:('wtc7_global_8a_no-conn-matl.k.gz',47520888,'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d',333947423,7196443,'8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}
ID_CAP=6000001
LINE_CAP=16384
BYTE_CAP=536870912
SECONDS_CAP=300
RSS_CAP=1073741824
NUMBER=re.compile(rb'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?\Z')
ELEMENTS={b'*ELEMENT_SHELL':('shell',[8]*10),b'*ELEMENT_SHELL_THICKNESS':('shell',[8]*10),
 b'*ELEMENT_BEAM':('beam',[8]*10),b'*ELEMENT_DISCRETE':('discrete',[8]*5+[16,8,16]),
 b'*ELEMENT_SOLID':('solid',[8]*10)}

class Failure(Exception): pass
def need(ok,label):
 if not ok: raise Failure(label)
def sha(path):
 with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def digest(raw): return hashlib.sha256(raw).hexdigest()
def pin_equal(actual,expected): need(actual==expected,'pin_mismatch')
def pins():
 p={k:sha(BASE/k) for k in PINS}; pin_equal(p,PINS); p['producer']=sha(__file__); return p
def integer(x,positive=False):
 need(x is not None and type(x) in (float,int) and math.isfinite(x) and int(x)==x,'integer_field')
 v=int(x); need((v>0 if positive else v>=0) and v<ID_CAP,'id_range'); return v
def fields(raw,widths):
 data=raw.rstrip(b'\r\n'); need(b'$' not in data and b'\t' not in data,'inline_or_tab')
 if b',' in data:
  parts=data.split(b','); need(len(parts)<=len(widths),'card_field_count')
  parts+= [b'']*(len(widths)-len(parts)); form='comma'
 else:
  parts=[]; start=0
  for width in widths: parts.append(data[start:start+width]); start+=width
  need(not data[start:].strip(),'card_width_overflow'); form='fixed'
 values=[]
 for rawtoken in parts:
  t=rawtoken.strip()
  if not t: values.append(None); continue
  need(NUMBER.fullmatch(t) is not None,'non_numeric_card')
  v=float(t.replace(b'D',b'E').replace(b'd',b'e')); need(math.isfinite(v),'nonfinite_card')
  values.append(v)
 return values,form

def resource_guard(start):
 need(time.monotonic()-start<=SECONDS_CAP,'time_cap')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
 need(rss<=RSS_CAP,'rss_cap')

def stream(source,receipt,start):
 name,cbytes,cpin,ubytes,lines,upin=FILES[source]; path=RAW/name
 receipt.update(source=source,eof=False,compressed_bytes=path.stat().st_size,compressed_sha256=sha(path),lines=0,uncompressed_bytes=0)
 need(receipt['compressed_bytes']==cbytes and receipt['compressed_sha256']==cpin,'compressed_pin')
 h=hashlib.sha256(); count=size=0
 with gzip.open(path,'rb') as f:
  while True:
   raw=f.readline(LINE_CAP+1)
   if not raw: break
   count+=1; size+=len(raw); h.update(raw)
   receipt.update(lines=count,uncompressed_bytes=size)
   need(len(raw)<=LINE_CAP and size<=BYTE_CAP and size<=ubytes and count<=lines,'stream_cap')
   if count%100000==0: resource_guard(start)
   yield count,raw
 receipt.update(eof=True,uncompressed_sha256=h.hexdigest(),compressed_after=sha(path))
 need((count,size,h.hexdigest())==(lines,ubytes,upin),'eof_pin')
 need(receipt['compressed_after']==cpin and path.stat().st_size==cbytes,'source_changed')

def read_list(lines):
 state=None; header=None; rows=[]; members=[]; occurrence=0; ended=False; seen_keyword=False
 for line,raw in lines:
  s=raw.strip()
  if s.startswith(b'$'): continue
  if s.startswith(b'*'):
   key=s.upper(); need(not ended,'post_end_keyword')
   need(key in (b'*KEYWORD',b'*SET_SHELL_LIST',b'*END'),'unsupported_list_keyword')
   if key==b'*KEYWORD': need(not seen_keyword,'duplicate_keyword'); seen_keyword=True; state=None
   elif key==b'*SET_SHELL_LIST': need(header is None and state is None,'duplicate_list_set'); state='header'; keyword_line=line
   else: ended=True; state=None
   continue
  if not s: continue
  need(not ended and state is not None,'unscoped_list_data')
  values,form=fields(raw,[10]*8)
  if state=='header':
   need(integer(values[0],True)==1,'list_set_id')
   header={'source':117,'keyword_line':keyword_line,'line':line,'values':values,'format':form,'raw_sha256':digest(raw)}
   state='members'; continue
  row_index=len(rows); rows.append({'line':line,'row_index':row_index,'values':values,'format':form,'raw_sha256':digest(raw)})
  for slot,value in enumerate(values):
   if value is None or value==0: continue
   eid=integer(value,True); occurrence+=1
   members.append({'eid':eid,'line':line,'row_index':row_index,'slot':slot,'positive_ordinal':occurrence})
 need(seen_keyword and ended and header is not None and state is None,'incomplete_list')
 counts=Counter(m['eid'] for m in members)
 return {'header':header,'rows':rows,'members':members,'unique_ids':sorted(counts),
         'duplicate_occurrences':sum(n-1 for n in counts.values()),
         'duplicates':[{'eid':eid,'count':n} for eid,n in sorted(counts.items()) if n>1],
         'explicit_zero_slots':sum(v==0 for r in rows for v in r['values'] if v is not None),
         'blank_slots':sum(v is None for r in rows for v in r['values'])}

def element(raw,key,source,line):
 family,widths=ELEMENTS[key]; values,form=fields(raw,widths)
 eid,pid=integer(values[0],True),integer(values[1],True)
 if family=='discrete':
  nodes=[integer(values[2],True),integer(values[3])]; orientation=None
  vid=0 if values[4] is None else integer(values[4])
 elif family=='beam':
  nodes=[integer(values[2],True),integer(values[3],True)]
  orientation=None if values[4] is None else integer(values[4]); vid=None
 else:
  need(all(x is not None for x in values[2:6]),'unsupported_short_element')
  nodes=[integer(x) for x in values[2:] if x is not None]
  need(sum(n>0 for n in nodes)>=3,'element_physical_vertices'); orientation=None; vid=None
 return {'family':family,'eid':eid,'source':source,'line':line,'original_pid':pid,
  'effective_pid':pid+(1000 if source==120 else 0),'node_slots':nodes,
  'physical_nodes':list(dict.fromkeys(n for n in nodes if n>0)),
  'orientation_node':orientation,'discrete_orientation_id':vid,
  'card_values':values,'format':form,'raw_sha256':digest(raw)}

def decode_include(raw):
 token=raw.strip().strip(b'"').replace(b'\\',b'/').split(b'/')[-1]
 names={b'elem_thick_to-renum.k':120,b'discrete_mass.k':119,b'WTC7_CaseB_400pm.int':118}
 if token.endswith(b'.gz'): token=token[:-3]
 need(token in names,'unresolved_include_target')
 return names[token]

def scan_mesh(lines,source,wanted_eids,wanted_nodes,seen,output):
 state=None; pending=None; include=None; ended=False
 def finish():
  need(pending is None,'orphan_shell_thickness')
  if include is not None:
   need('target_source' in include,'missing_include_target')
   if include['transformed']:
    need(len(include['cards'])==4,'include_card_count')
    vals=[r['values'] for r in include['cards']]
    need(include['target_source']==120 and vals[0][:7]==[0,0,1000,1000,0,0,0] and all(x in (None,0) for x in vals[0][7:]),'include_offsets')
    need(vals[1][0]==1000 and all(x in (None,0) for x in vals[1][1:]),'include_section_offset')
    need(vals[2][:5]==[1,1,1,1,0] and all(x in (None,0) for x in vals[2][5:]),'include_factors')
    need(vals[3][0]==0 and all(x in (None,0) for x in vals[3][1:]),'include_geometric_transform')
   else: need(len(include['cards'])==0,'unexpected_plain_include_cards')
 for line,raw in lines:
  s=raw.strip()
  if s.startswith(b'$'): continue
  if s.startswith(b'*'):
   finish(); key=s.upper(); need(not ended,'post_end_keyword')
   pending=None; include=None; state=key
   if key==b'*END': ended=True
   elif key.startswith(b'*ELEMENT'):
    need(key in ELEMENTS,'unsupported_element_variant')
   elif key.startswith(b'*NODE'): need(key==b'*NODE','unsupported_node_variant')
   elif key.startswith(b'*INCLUDE'):
    need(key in (b'*INCLUDE',b'*INCLUDE_TRANSFORM'),'unsupported_include_variant')
    include={'source':source,'keyword_line':line,'transformed':key==b'*INCLUDE_TRANSFORM','cards':[]}
    output['includes'].append(include)
   elif key.startswith(b'*PARAMETER') or (key.startswith(b'*KEYWORD') and key!=b'*KEYWORD'):
    raise Failure('unsupported_global_format_or_parameter')
   else:
    kh=digest(key); output['ignored_keyword_counts'][kh]+=1
   continue
  if not s:
   need(pending is None,'blank_required_thickness')
   continue
  need(not ended,'post_end_data')
  if state==b'*NODE':
   values,form=fields(raw,[8,16,16,16,8,8]); nid=integer(values[0],True)
   need(all(x is not None for x in values[1:4]),'missing_node_coordinate')
   output['node_counts'][source]+=1
   if nid in wanted_nodes:
    need(nid not in output['coordinates'],'duplicate_selected_node')
    output['coordinates'][nid]={'nid':nid,'source':source,'line':line,'xyz':values[1:4],
      'constraint_slots':values[4:],'raw_sha256':digest(raw),'format':form}
  elif state in ELEMENTS:
   if pending is not None:
    values,form=fields(raw,[16]*5); need(all(x is not None and x>=0 for x in values[:4]),'invalid_shell_thickness')
    if pending['eid'] in wanted_eids:
     pending.update(thickness_values=values,thickness_line=line,thickness_raw_sha256=digest(raw),thickness_format=form)
    pending=None; continue
   record=element(raw,state,source,line); family=record['family']; eid=record['eid']
   need(not seen[family][eid],'duplicate_typed_element'); seen[family][eid]=1
   output['element_counts'][source][family]+=1
   if family=='discrete' and 0 in record['node_slots']: output['ground_discrete_count']+=1
   if eid in wanted_eids:
    if family=='shell': output['shells'].append(record)
    else: output['cross_family_coincidences'].append(record)
   if state==b'*ELEMENT_SHELL_THICKNESS': pending=record
  elif include is not None:
   if 'target_source' not in include:
    include.update(target_source=decode_include(raw),filename_line=line,filename_sha256=digest(raw))
   else:
    values,form=fields(raw,[10]*8)
    include['cards'].append({'line':line,'values':values,'format':form,'raw_sha256':digest(raw)})
  # All other bodies are deliberately unexported and uninterpreted.
 finish(); need(ended,'missing_end')

def array_load(name,schema):
 out={}
 with np.load(BASE/name,allow_pickle=False) as z:
  need(set(z.files)==set(schema),'array_schema')
  for k in z.files:
   a=z[k]; s=schema[k]
   need(a.dtype.kind in 'biuf' and list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'],'array_shape_dtype')
   need(digest(a.tobytes(order='C'))==s['sha256'],'array_content_pin'); out[k]=a
 return out

def compare_coordinates(found,wanted,nodeids,xyz,locators):
 need(set(found)==set(wanted),'selected_coordinate_coverage')
 for nid,r in found.items():
  i=int(np.searchsorted(nodeids,nid)); need(i<len(nodeids) and int(nodeids[i])==nid,'stage_selected_missing')
  need(r['xyz']==xyz[i].tolist() and [r['source'],r['line']]==locators[i].tolist(),'selected_coordinate_version')

def make_join(pairs,identities,masters,shells,coords,members):
 by_node=defaultdict(list)
 for i,r in enumerate(shells):
  for nid in r['physical_nodes']: by_node[nid].append(i)
 by_list=defaultdict(list)
 for i,m in enumerate(members): by_list[m['eid']].append(i)
 hits=[]; groups=[]
 for setting in range(3):
  for cid in (1,2):
   for cls in (0,2,3):
    selected=[r for r in pairs if r[0]==setting and identities[r[1]][0]==cid and r[3]==cls]
    local=[]
    for r in selected:
     setting2,mi,nid,_,_,_=r
     for ei in by_node.get(nid,[]):
      local.append(len(hits)); hits.append({'setting_index':setting2,'cid':cid,'class':cls,
       'master_index':mi,'master_source':121,'master_line':masters[mi]['line'],'node_id':nid,
       'node_source':coords[nid]['source'],'node_line':coords[nid]['line'],'xyz':coords[nid]['xyz'],
       'element_index':ei,'list_membership_indices':by_list[shells[ei]['eid']]})
    subset=[hits[x] for x in local]
    groups.append({'setting_index':setting,'cid':cid,'class':cls,
     'candidate_pair_rows':len(selected),'candidate_node_ids':sorted(set(r[2] for r in selected)),
     'matching_node_ids':sorted(set(r['node_id'] for r in subset)),
     'matching_element_indices':sorted(set(r['element_index'] for r in subset)),
     'relation_indices':local,'relation_count':len(local)})
 typed={r['eid']:i for i,r in enumerate(shells)}; aliases=[]
 for mi,m in enumerate(masters):
  for ai,a in enumerate(m['aliases']):
   match=typed.get(a['eid'])
   if match is not None:
    el=shells[match]
    need((a['source'],a['line'],a['pid'],a['original_pid'])==(el['source'],el['line'],el['effective_pid'],el['original_pid']),'master_version')
    need(sorted(a['nodes'])==sorted(n for n in el['node_slots'] if n),'master_connectivity')
   aliases.append({'master_index':mi,'alias_index':ai,'cid':identities[mi][0],'set_id':m['set_id'],
    'master_line':m['line'],'eid':a['eid'],'source':a['source'],'line':a['line'],'effective_pid':a['pid'],
    'original_pid':a['original_pid'],'ordered_nodes':a['nodes'],'matching_element_index':match})
 return {'groups':groups,'relations':hits,'master_aliases':aliases}

def calculate(receipt,start):
 read=lambda n:json.loads((BASE/n).read_text())
 reference=read('../c79-contact-geometry/independent-exact-reference80-root01.json')
 need(reference['status']==reference['result']['status']=='PASS' and reference['result']['precision_bits']==80,'exact_reference_status')
 for n in ('exact-proximity80.json','exact-proximity80.npz'):
  need(reference['pins_before'][n]==PINS['../c79-contact-geometry/'+n],'exact_reference_pin')
 exact=read('../c79-contact-geometry/exact-proximity80.json')
 stage=read('../c79-contact-geometry/stage-root01.json')['result']
 a=array_load('../c79-contact-geometry/exact-proximity80.npz',exact['array_schema'])
 st=array_load('../c79-contact-geometry/stage-root01.npz',stage['arrays'])
 pairs=a['pairs'].tolist(); identities=a['master_identity'].tolist(); masters=stage['master_segments']
 candidates=sorted(set(r[2] for r in pairs if r[3] in (0,2,3)))
 master_nodes=sorted(set(n for m in masters for n in m['nodes'])); wanted_nodes=set(candidates)|set(master_nodes)
 need(len(masters)==742 and len(identities)==742,'master_population')
 for i,m in enumerate(masters):
  need(identities[i]==[1 if m['set_id']==1 else 2,m['set_id'],m['line']] and a['master_nodes'][i].tolist()==m['nodes'],'master_geometry_identity')
 need(len(set(tuple(r[:3]) for r in pairs))==len(pairs),'duplicate_exact_pair')
 source_receipts={}; receipt['sources']=source_receipts
 source_receipts[117]={}; listed=read_list(stream(117,source_receipts[117],start))
 requested=set(listed['unique_ids']); need(len(requested)==45152,'list_coverage_check')
 mesh={'shells':[],'cross_family_coincidences':[],'coordinates':{},'includes':[],
  'node_counts':Counter(),'element_counts':defaultdict(Counter),'ground_discrete_count':0,'ignored_keyword_counts':Counter()}
 seen={k:bytearray(ID_CAP) for k in ('shell','beam','discrete','solid')}
 # Master first validates the include graph before processing the transformed include.
 for source in (121,119,120):
  source_receipts[source]={}
  scan_mesh(stream(source,source_receipts[source],start),source,requested,wanted_nodes,seen,mesh)
  if source==121:
   need(sorted((r['target_source'],r['transformed']) for r in mesh['includes'])==[(118,False),(119,False),(120,True)],'include_graph')
  resource_guard(start)
 nodeids=st['node_ids']; xyz=st['xyz']; sl=st['node_source_line']
 compare_coordinates(mesh['coordinates'],wanted_nodes,nodeids,xyz,sl)
 mesh['shells'].sort(key=lambda r:(r['eid'],r['source'],r['line']))
 matched={r['eid'] for r in mesh['shells']}; unmatched=sorted(requested-matched)
 join=make_join(pairs,identities,masters,mesh['shells'],mesh['coordinates'],listed['members'])
 return {'list':listed,'shells':mesh['shells'],'unmatched_shell_ids':unmatched,
  'cross_family_coincidences':mesh['cross_family_coincidences'],
  'selected_coordinates':[mesh['coordinates'][n] for n in sorted(wanted_nodes)],
  'candidate_node_ids':candidates,'master_vertex_ids':master_nodes,'includes':mesh['includes'],
  'source_node_counts':dict(mesh['node_counts']),'source_element_counts':dict(mesh['element_counts']),
  'ground_discrete_count':mesh['ground_discrete_count'],'ignored_keyword_counts':dict(mesh['ignored_keyword_counts']),
  'membership_ordinal_schema':'positive_ordinal is1based over nonzero IDs; row_index/slot are0based; raw cards preserve blank versus zero.',
  'selected_coordinate_scalars_compared':3*len(wanted_nodes),**join,
  'scope':'CaseA static shell-list incidence only; no solver activation, deleted-node inference, initialized contact, force/capacity, member/unit attribution or cause. ArmB not performed by this producer.'}

class Controls(unittest.TestCase):
 def lines(self,data): return enumerate(data,1)
 def out(self): return {'shells':[],'cross_family_coincidences':[],'coordinates':{},'includes':[],'node_counts':Counter(),'element_counts':defaultdict(Counter),'ground_discrete_count':0,'ignored_keyword_counts':Counter()}
 def seen(self): return {k:bytearray(100) for k in ('shell','beam','discrete','solid')}
 def test_list_header_padding(self):
  r=read_list(self.lines([b'*KEYWORD\n',b'*SET_SHELL_LIST\n',b'1,0\n',b'8,,0,9\n',b'*END\n']))
  self.assertEqual(r['unique_ids'],[8,9]); self.assertEqual(r['explicit_zero_slots'],1); self.assertEqual(r['members'][1]['slot'],3)
 def test_list_duplicates(self):
  r=read_list(self.lines([b'*KEYWORD\n',b'*SET_SHELL_LIST\n',b'1\n',b'8,8\n',b'*END\n']))
  self.assertEqual(r['duplicate_occurrences'],1)
 def test_unsupported_set(self):
  with self.assertRaises(Failure): read_list(self.lines([b'*KEYWORD\n',b'*SET_SHELL_LIST_GENERATE\n']))
 def test_postend(self):
  with self.assertRaises(Failure): read_list(self.lines([b'*KEYWORD\n',b'*END\n',b'8\n']))
 def test_thickness_separation(self):
  o=self.out(); scan_mesh(self.lines([b'*KEYWORD\n',b'*ELEMENT_SHELL_THICKNESS\n',b'8,1,2,3,4,5\n',b'.1,.2,.3,.4\n',b'*END\n']),121,{8},set(),self.seen(),o)
  self.assertEqual(len(o['shells']),1); self.assertEqual(o['shells'][0]['thickness_line'],4)
 def test_orphan_thickness(self):
  with self.assertRaises(Failure): scan_mesh(self.lines([b'*ELEMENT_SHELL_THICKNESS\n',b'8,1,2,3,4,5\n',b'*END\n']),121,{8},set(),self.seen(),self.out())
 def test_blank_thickness(self):
  with self.assertRaises(Failure): scan_mesh(self.lines([b'*ELEMENT_SHELL_THICKNESS\n',b'8,1,2,3,4,5\n',b'\n']),121,{8},set(),self.seen(),self.out())
 def test_typed_collision(self):
  o=self.out(); scan_mesh(self.lines([b'*ELEMENT_SHELL\n',b'8,1,2,3,4,5\n',b'*ELEMENT_BEAM\n',b'8,1,2,3,7\n',b'*END\n']),121,{8},set(),self.seen(),o)
  self.assertEqual(len(o['shells']),1); self.assertEqual(len(o['cross_family_coincidences']),1)
 def test_typed_duplicate(self):
  with self.assertRaises(Failure): scan_mesh(self.lines([b'*ELEMENT_SHELL\n',b'8,1,2,3,4,5\n',b'8,1,2,3,4,5\n',b'*END\n']),121,{8},set(),self.seen(),self.out())
 def test_beam_orientation(self):
  r=element(b'8,1,2,3,7\n',b'*ELEMENT_BEAM',121,3)
  self.assertEqual(r['physical_nodes'],[2,3]); self.assertEqual(r['orientation_node'],7)
 def test_ground(self):
  r=element(b'8,1,2,0,7,1,0,0\n',b'*ELEMENT_DISCRETE',121,3)
  self.assertEqual(r['physical_nodes'],[2]); self.assertEqual(r['discrete_orientation_id'],7)
 def test_solid_single(self):
  r=element(b'8,1,2,3,4,5,6,7,8,9\n',b'*ELEMENT_SOLID',119,3)
  self.assertEqual(len(r['physical_nodes']),8)
 def test_solid_unsupported_short(self):
  with self.assertRaises(Failure): element(b'8,1\n',b'*ELEMENT_SOLID',119,3)
 def test_namespace(self):
  self.assertEqual(element(b'8,1,2,3,4,5\n',b'*ELEMENT_SHELL',120,3)['effective_pid'],1001)
 def test_fixed_node(self):
  raw=b'%8d%16.8f%16.8f%16.8f%8d%8d\n'%(8,-1.2,3.4,5.6,0,0)
  self.assertEqual(fields(raw,[8,16,16,16,8,8])[0],[8.,-1.2,3.4,5.6,0.,0.])
 def test_nonfinite_and_inline(self):
  for raw in (b'1e999\n',b'1 $ secret\n',b'not numeric\n'):
   with self.assertRaises(Failure): fields(raw,[10]*8)
 def test_include(self):
  o=self.out(); scan_mesh(self.lines([b'*INCLUDE_TRANSFORM\n',b'elem_thick_to-renum.k\n',b'0,0,1000,1000,0,0,0\n',b'1000\n',b'1,1,1,1,0\n',b'0\n',b'*END\n']),121,set(),set(),self.seen(),o)
  self.assertEqual(o['includes'][0]['target_source'],120)
 def test_include_changed(self):
  with self.assertRaises(Failure): scan_mesh(self.lines([b'*INCLUDE_TRANSFORM\n',b'elem_thick_to-renum.k\n',b'0,0,2,1000,0,0,0\n',b'1000\n',b'1,1,1,1,0\n',b'0\n',b'*END\n']),121,set(),set(),self.seen(),self.out())
 def test_selected_duplicate(self):
  with self.assertRaises(Failure): scan_mesh(self.lines([b'*NODE\n',b'8,1,2,3\n',b'8,1,2,3\n',b'*END\n']),121,set(),{8},self.seen(),self.out())
 def test_complete_selected(self):
  o=self.out(); scan_mesh(self.lines([b'*NODE\n',b'8,1,2,3\n',b'*END\n']),121,set(),{8},self.seen(),o)
  self.assertEqual(set(o['coordinates']),{8})
 def test_groups_and_id_not_coordinate(self):
  shells=[element(b'8,1,2,3,4,5\n',b'*ELEMENT_SHELL',121,3)]
  masters=[{'line':1,'aliases':[]}]; coords={7:{'source':121,'line':9,'xyz':[0,0,0]}}
  r=make_join([[0,0,7,0,0,0]],[[1,1,1]],masters,shells,coords,[{'eid':8}])
  self.assertEqual(len(r['groups']),18); self.assertEqual(r['relations'],[])
 def test_positive_unknown_duplicates(self):
  shells=[element(b'8,1,2,3,4,5\n',b'*ELEMENT_SHELL',121,3)]
  masters=[{'line':1,'aliases':[]},{'line':2,'aliases':[]}]; coords={2:{'source':121,'line':9,'xyz':[0,0,0]}}
  r=make_join([[0,0,2,0,0,0],[0,1,2,0,0,0]],[[1,1,1],[1,1,2]],masters,shells,coords,[{'eid':8},{'eid':8}])
  self.assertEqual(len(r['relations']),2); self.assertEqual(r['relations'][0]['list_membership_indices'],[0,1])
 def test_createonly_changed_pin(self):
  with tempfile.TemporaryDirectory(prefix='casea-control-') as folder:
   p=Path(folder)/'fixture'; p.touch(); before=sha(p)
   with self.assertRaises(FileExistsError): p.open('x')
   with p.open('ab') as f:f.write(b'synthetic mutation')
   with self.assertRaises(Failure): pin_equal(before,sha(p))
 def test_coordinate_version_guard(self):
  actual={8:{'xyz':[1.,2.,3.],'source':121,'line':4}}
  ids=np.array([8]); xyz=np.array([[1.,2.,3.]]); loc=np.array([[121,4]])
  compare_coordinates(actual,{8},ids,xyz,loc)
  with self.assertRaises(Failure): compare_coordinates(actual,{8,9},ids,xyz,loc)
  with self.assertRaises(Failure): compare_coordinates(actual,{8},ids,xyz+1,loc)
  with self.assertRaises(Failure): compare_coordinates(actual,{8},ids,xyz,loc+1)
 def test_full_stream_fixture(self):
  global RAW
  old=RAW
  try:
   with tempfile.TemporaryDirectory(prefix='casea-eof-control-') as folder:
    RAW=Path(folder); data=b'*KEYWORD\n*END\n'; compressed=gzip.compress(data)
    p=RAW/'fixture.gz'
    with p.open('xb') as f:f.write(compressed)
    FILES[999]=('fixture.gz',len(compressed),digest(compressed),len(data),2,digest(data))
    rec={}; self.assertEqual(len(list(stream(999,rec,time.monotonic()))),2); self.assertTrue(rec['eof'])
    FILES[999]=('fixture.gz',len(compressed),'0'*64,len(data),2,digest(data))
    with self.assertRaises(Failure): list(stream(999,{},time.monotonic()))
    FILES[999]=('fixture.gz',len(compressed),digest(compressed),len(data)-1,2,digest(data))
    with self.assertRaises(Failure): list(stream(999,{},time.monotonic()))
  finally:
   RAW=old; FILES.pop(999,None)

def controls():
 r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
 return {'count':r.testsRun,'errors':len(r.errors),'failures':len(r.failures),'passed':r.wasSuccessful()}

def main():
 p=argparse.ArgumentParser(); p.add_argument('--controls',action='store_true'); p.add_argument('--out',default='independent-casea01.json'); args=p.parse_args()
 if args.controls:
  c=controls(); print(json.dumps(c)); return 0 if c['passed'] else 1
 need(re.fullmatch(r'independent-casea[0-9]+\.json',args.out) is not None,'output_scope')
 path=BASE/args.out
 # Reserve the exact output before opening any historical stream.
 with path.open('x') as destination:
  start=time.monotonic(); record={'status':'FAIL','command':sys.argv,'controls':{},'sources':{}}
  try:
   record['controls']=controls(); need(record['controls']['passed'],'controls_failed')
   before=pins(); record['pins_before']=before
   result=calculate(record,start); after=pins(); need(before==after,'changed_dependencies')
   record.update(status='PASS',result=result,pins_after=after)
  except Exception as e:
   record['error']=str(e) if isinstance(e,Failure) else type(e).__name__
  record.update(elapsed_seconds=time.monotonic()-start,peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
   runtime={'python':sys.version,'executable':sys.executable,'numpy':np.__version__},
   limits={'id_cap_exclusive':ID_CAP,'line_bytes':LINE_CAP,'source_bytes':BYTE_CAP,'seconds':SECONDS_CAP,'peak_bytes':RSS_CAP})
  json.dump(record,destination,sort_keys=True,indent=2,allow_nan=False); destination.write('\n')
 print(json.dumps({'status':record['status'],'output':path.name,'sha256':sha(path),'error':record.get('error'),'seconds':record['elapsed_seconds']}))
 return 0 if record['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
