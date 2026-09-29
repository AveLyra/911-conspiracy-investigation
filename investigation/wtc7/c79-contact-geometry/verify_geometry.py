#!/usr/bin/env python3
"""Independent contact geometry first stage. Numeric extraction, not pairing."""
import argparse
from array import array
from collections import Counter, defaultdict
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import time
import numpy as np

BASE=Path(__file__).resolve().parent
PRIOR=BASE.parent/'c79-restraint-audit'
HELPER=PRIOR/'verify_restraint.py'
HELPER_SHA='5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest()==HELPER_SHA
spec=importlib.util.spec_from_file_location('own_frozen_numeric_reader',HELPER)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
PROTOCOL_SHA='b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea'
CONTACT_SHA='b30b8ee5435e7cf8ce2ea979245b07fa4b0577606bf97638dbfd76b21043c7c3'
SEED_SHA='d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7'
MAX_ID=6000001
FAMILIES={'shell':0,'beam':1,'discrete':2,'solid':3}
STATS=[]


def require(ok,code,source=0,line=0):g.require(ok,code,source,line)


def matrix(buffer,width,dtype='<i8'):
    return np.asarray(buffer,dtype=dtype).reshape(-1,width)


def numeric_storage(values):
    return [np.nan if v is None else float(v) for v in values],[v is None for v in values]


def scan_selection(source,stream):
    """Full byte coverage; fresh complete NSET1/SEG2 and numeric CONTROL_CONTACT."""
    stats={'source':source,'phase':'selection_controls','bytes':0,'lines':0,'eof':False}
    STATS.append(stats);h=hashlib.sha256();name=None;header=None;row=0;ended=False
    node=array('q');seg=array('q');attrs=array('d');masks=bytearray();headers=[];controls=[];unparsed=[]
    seen=set();contact_block=None;keyword_line=0
    while True:
        raw=stream.readline(g.LINE_CAP+1)
        if not raw:break
        stats['lines']+=1;stats['bytes']+=len(raw);line=stats['lines'];h.update(raw)
        require(len(raw)<=g.LINE_CAP and stats['bytes']<=g.CAP and b'\0' not in raw,'selection_cap_or_NUL',source,line)
        if line%100000==0:require(g.peak_memory()<=g.MEMORY_CAP,'selection_memory_cap',source,line)
        try:text=raw.decode('ascii')
        except UnicodeDecodeError:raise g.AuditError('selection_nonascii',source,line) from None
        s=text.strip()
        if s.startswith('$'):continue
        if s.startswith('*'):
            require(not ended,'selection_keyword_after_END',source,line)
            require(name not in {'SET_NODE_LIST','SET_SEGMENT'} or header is not None,'selection_missing_header',source,line)
            token=s[1:].split('$',1)[0].strip().upper();keyword_line=line
            if token.startswith(('SET_NODE','SET_SEGMENT')):
                require(token in {'SET_NODE_LIST','SET_SEGMENT'},'selection_set_variant',source,line)
            if token.startswith('CONTROL_CONTACT'):
                require(token=='CONTROL_CONTACT','selection_control_variant',source,line)
            if token.startswith('PART_CONTACT'):
                unparsed.append({'source':source,'line':line,'keyword_sha256':hashlib.sha256(token.encode()).hexdigest()})
            name=token if token in {'SET_NODE_LIST','SET_SEGMENT','CONTROL_CONTACT'} else None
            header=None;row=0;contact_block=None
            if name=='CONTROL_CONTACT':
                contact_block={'source':source,'keyword_line':line,'numeric_cards':[]};controls.append(contact_block)
            ended=token=='END'
            continue
        if ended:
            require(not s,'selection_data_after_END',source,line);continue
        if name=='CONTROL_CONTACT':
            require(len(contact_block['numeric_cards'])<100,'control_card_cap',source,line)
            contact_block['numeric_cards'].append({'line':line,'card':g.fields(text,[10]*8,[],0)});continue
        if name not in {'SET_NODE_LIST','SET_SEGMENT'} or not s:continue
        if header is None:
            card=g.fields(text,[10]*8,[0],1);sid=card[0];key=(name,sid)
            require(key not in seen,'duplicate_set_in_source',source,line);seen.add(key)
            selected=(name=='SET_NODE_LIST' and sid==1) or (name=='SET_SEGMENT' and sid==2)
            header={'source':source,'keyword':name,'keyword_line':keyword_line,'header_line':line,'set_id':sid,'card':card,'selected':selected}
            if selected:headers.append(header)
            continue
        row+=1
        if not header['selected']:continue
        require(row<2000001,'selected_set_row_cap',source,line)
        if name=='SET_NODE_LIST':
            values=g.fields(text,[10]*8,range(8),0)
            for slot,nid in enumerate(values,1):
                if nid in (None,0):continue
                require(0<nid<MAX_ID,'selected_node_ID',source,line);node.extend([source,line,row,slot,nid])
        else:
            values=g.fields(text,[10]*8,range(4),4)
            require(all(0<n<MAX_ID for n in values[:4]),'selected_segment_node_ID',source,line)
            seg.extend([source,line,row,*values[:4]])
            numbers,missing=numeric_storage(values[4:]);attrs.extend(numbers);masks.extend(missing)
    require(name not in {'SET_NODE_LIST','SET_SEGMENT'} or header is not None,'selection_missing_header',source,stats['lines'])
    require(ended,'selection_missing_END',source,stats['lines'])
    stats.update(eof=True,sha256=h.hexdigest())
    return {'headers':headers,'node_members':node,'segment_members':seg,'segment_attributes':attrs,
            'segment_attribute_missing':masks,'controls':controls,'unparsed_PART_CONTACT':unparsed}


def selected_inputs():
    output={'headers':[],'node_members':array('q'),'segment_members':array('q'),
            'segment_attributes':array('d'),'segment_attribute_missing':bytearray(),'controls':[],'unparsed_PART_CONTACT':[]}
    for src,pin in g.PINS.items():
        with gzip.open(g.SOURCE/pin[0],'rb') as f:part=scan_selection(src,f)
        stat=STATS[-1];require((stat['bytes'],stat['sha256'])==(pin[3],pin[4]),'selection_EOF_pin',src)
        for key in output:output[key].extend(part[key])
    require(Counter((r['keyword'],r['set_id']) for r in output['headers'])=={('SET_NODE_LIST',1):1,('SET_SEGMENT',2):1},'selection_header_coverage')
    return output


class Accumulator:
    def __init__(self,ids,flags,masters,max_id=MAX_ID):
        self.ids=np.asarray(ids,dtype='<i8');self.flags=np.asarray(flags,dtype='u1');self.index={int(n):i for i,n in enumerate(ids)}
        require(len(self.index)==len(ids) and len(ids)>0 and len(ids)==len(flags),'selected_ID_shape')
        self.max_id=max_id;self.global_present=np.zeros(max_id,dtype=bool);self.seen=np.zeros((4,max_id),dtype=bool)
        self.xyz=np.full((len(ids),3),np.nan,dtype='<f8');self.node_source=np.zeros(len(ids),dtype='<i4');self.node_line=np.zeros(len(ids),dtype='<i8')
        self.node_present=np.zeros(len(ids),dtype=bool);self.family_counts=np.zeros((len(ids),4),dtype='<i8')
        self.orientation_counts=np.zeros(len(ids),dtype='<i8');self.corner_counts=np.zeros(len(ids),dtype='<i8')
        self.local_min=np.full(len(ids),np.nan);self.local_max=self.local_min.copy()
        self.whole_min=self.local_min.copy();self.whole_max=self.local_min.copy()
        self.shell_id=array('q');self.shell_conn=array('q');self.shell_conn_missing=bytearray()
        self.shell_thic=array('d');self.shell_thic_missing=bytearray();self.corners=array('q');self.nodeparts=array('q')
        self.other_id=array('q');self.other_nodes=array('q');self.other_orientation_missing=bytearray()
        self.master_alias=array('q');self.masters=masters;self.ordered=defaultdict(list);self.unordered=defaultdict(list)
        for i,r in enumerate(masters):
            require(len(r['nodes'])==4,'master_node_width');self.ordered[tuple(r['nodes'])].append(i);self.unordered[tuple(sorted(r['nodes']))].append(i)
        self.element_counts=Counter();self.node_counts=Counter();self.parts={};self.definitions=defaultdict(dict);self.includes=[]

    def node(self,source,line,card):
        nid=card[0];require(type(nid) is int and 0<nid<self.max_id,'node_ID',source,line)
        require(not self.global_present[nid],'duplicate_node',source,line);self.global_present[nid]=True;self.node_counts[source]+=1
        if nid in self.index:
            i=self.index[nid];self.xyz[i]=card[1:4];self.node_source[i]=source;self.node_line[i]=line;self.node_present[i]=True

    def metadata(self,source,line,kind,record):
        offset=1000 if source==120 else 0
        if kind=='part':
            card=record['card'];pid=card[0]+offset;require(pid not in self.parts,'duplicate_part',source,line)
            self.parts[pid]={'source':source,'line':line,'keyword_line':record['keyword_line'],'card':card,
                'effective_part':pid,'effective_section':card[1]+offset,'effective_material':card[2]+offset}
        elif kind=='definition':
            family='material' if record['keyword'].startswith('MAT_') else 'section' if record['keyword'].startswith('SECTION_') else 'hourglass'
            identity=record['id']+offset;require(identity not in self.definitions[family],'duplicate_definition',source,line)
            self.definitions[family][identity]={'source':source,'line':line,'keyword_line':record['keyword_line'],'keyword':record['keyword'],'original_id':record['id'],'effective_id':identity}
        elif kind in {'include','transform'}:self.includes.append({'source':source,'line':line,'kind':kind,**record})

    @staticmethod
    def extrema(low,high,i,values):
        if not values:return
        a,b=min(values),max(values)
        low[i]=a if np.isnan(low[i]) else min(low[i],a)
        high[i]=b if np.isnan(high[i]) else max(high[i],b)

    def element(self,source,line,kind,record):
        card=record['card'];eid,pid=card[:2];family=FAMILIES[kind]
        require(0<eid<self.max_id and not self.seen[family,eid],'duplicate_or_invalid_element',source,line)
        self.seen[family,eid]=True;self.element_counts[(source,kind)]+=1
        nodes=g.physical(kind,card);require(all(type(n) is int and 0<n<self.max_id for n in nodes),'element_node_ID',source,line)
        require(all(self.global_present[n] for n in nodes),'element_missing_node',source,line)
        effective=pid+(1000 if source==120 else 0);hits=[n for n in dict.fromkeys(nodes) if n in self.index]
        orientation=card[4] if kind=='beam' else None
        orientation_hit=orientation in self.index if orientation is not None else False
        for nid in hits:
            i=self.index[nid];self.family_counts[i,family]+=1;self.nodeparts.extend([i,effective,family])
        if orientation_hit:self.orientation_counts[self.index[orientation]]+=1
        if kind=='shell':
            require(len(nodes)==4,'shell_four_slots',source,line)
            unordered=self.unordered.get(tuple(sorted(nodes)),[])
            if not hits and not unordered:return
            shell_index=len(self.shell_id)//6
            self.shell_id.extend([source,line,record['continuation_line'],eid,pid,effective])
            self.shell_conn.extend(0 if v is None else v for v in card);self.shell_conn_missing.extend(v is None for v in card)
            thickness=record['thickness'];values,missing=numeric_storage(thickness)
            self.shell_thic.extend(values);self.shell_thic_missing.extend(missing)
            for slot,nid in enumerate(nodes):
                if nid not in self.index:continue
                i=self.index[nid];self.corners.extend([i,shell_index,slot+1]);self.corner_counts[i]+=1
                self.extrema(self.local_min,self.local_max,i,[] if thickness[slot] is None else [thickness[slot]])
            for nid in hits:self.extrema(self.whole_min,self.whole_max,self.index[nid],[v for v in thickness[:4] if v is not None])
            ordered=set(self.ordered.get(tuple(nodes),[]))
            for master_index in unordered:self.master_alias.extend([master_index,shell_index,int(master_index in ordered)])
        elif hits or orientation_hit:
            self.other_id.extend([source,line,family,eid,pid,effective,0 if orientation is None else orientation,len(nodes)])
            self.other_orientation_missing.append(orientation is None);self.other_nodes.extend(nodes+[0]*(8-len(nodes)))

    def arrays(self):
        pairs=matrix(self.nodeparts,3)
        if len(pairs):unique,counts=np.unique(pairs,axis=0,return_counts=True);partcounts=np.column_stack((unique,counts)).astype('<i8')
        else:partcounts=np.empty((0,4),dtype='<i8')
        return {'node_ids':self.ids,'population_flags':self.flags,'node_xyz':self.xyz,'node_source':self.node_source,
          'node_line':self.node_line,'node_present':self.node_present,'node_family_incidence':self.family_counts,
          'node_beam_orientation_incidence':self.orientation_counts,'node_shell_corner_occurrences':self.corner_counts,
          'node_local_corner_thickness_min':self.local_min,'node_local_corner_thickness_max':self.local_max,
          'node_incident_shell_THIC1to4_min':self.whole_min,'node_incident_shell_THIC1to4_max':self.whole_max,
          'node_part_family_counts':partcounts,'shell_identity':matrix(self.shell_id,6),
          'shell_connectivity':matrix(self.shell_conn,10),'shell_connectivity_missing':matrix(self.shell_conn_missing,10,'?'),
          'shell_thickness':matrix(self.shell_thic,5,'<f8'),'shell_thickness_missing':matrix(self.shell_thic_missing,5,'?'),
          'shell_corner_incidence':matrix(self.corners,3),'master_shell_aliases':matrix(self.master_alias,3),
          'nonshell_identity':matrix(self.other_id,8),'nonshell_physical_nodes':matrix(self.other_nodes,8),
          'nonshell_orientation_missing':np.asarray(self.other_orientation_missing,dtype=bool)}


def part_references(acc,arrays):
    pids=sorted(set(int(v) for v in arrays['node_part_family_counts'][:,1])|set(int(v) for v in arrays['shell_identity'][:,5])|set(int(v) for v in arrays['nonshell_identity'][:,5]))
    result=[]
    for pid in pids:
        part=acc.parts.get(pid)
        if part is None:result.append({'effective_part':pid,'status':'missing_part_definition'});continue
        result.append({**part,'status':'supplied_part_definition',
            'section_definition':acc.definitions['section'].get(part['effective_section']),
            'material_definition':acc.definitions['material'].get(part['effective_material'])})
    return result


def check_include_graph(events,expected):
    assembled=[]
    for event in events:
        if event['kind']=='include':
            assembled.append({k:v for k,v in event.items() if k!='kind'})
            assembled[-1]['transform_cards']=[]
        else:
            require(bool(assembled) and assembled[-1]['keyword']=='INCLUDE_TRANSFORM','transform_without_include')
            assembled[-1]['transform_cards'].append({k:v for k,v in event.items() if k not in {'kind','source'}})
    require(assembled==expected,'include_graph_changed')
    transforms=[e for e in assembled if e['keyword']=='INCLUDE_TRANSFORM']
    require(len(transforms)==1 and transforms[0]['target_source']==120,'transform_scope')
    require([v['card'] for v in transforms[0]['transform_cards']]==[[0,0,1000,1000,0,0,0],[1000],[1,1,1,1,0],[0]],'transform_numeric_gate')
    return assembled


def extract():
    selected=selected_inputs();members=matrix(selected['node_members'],5);segments=matrix(selected['segment_members'],7)
    old=json.loads((PRIOR/'independent-contacts01.json').read_text())
    require(old['receipt']['status']=='PASS','prior_contact_not_PASS')
    masters=[]
    for sid in (1,3):
        found=[r for r in old['result']['sets'] if r['kind']=='segment' and r['set_id']==sid]
        require(len(found)==1,'prior_master_set')
        for r in found[0]['matching_records']:masters.append({'source':found[0]['source'],'set_id':sid,**r})
    require([sum(m['set_id']==sid for m in masters) for sid in (1,3)]==[710,32],'prior_master_counts')
    populations=[set(int(v) for v in members[:,4]),set(int(v) for v in segments[:,3:].flat),{n for m in masters for n in m['nodes']}]
    ids=sorted(set.union(*populations));flags=[sum(1<<i for i,s in enumerate(populations) if nid in s) for nid in ids]
    acc=Accumulator(ids,flags,masters)
    for src in g.PINS:
        for kind,line,record in g.source_events(src,'metadata_nodes'):
            if kind=='node':acc.node(src,line,record)
            else:acc.metadata(src,line,kind,record)
    include_graph=check_include_graph(acc.includes,json.loads((PRIOR/'independent01.json').read_text())['result']['include_graph'])
    for src in g.PINS:
        for kind,line,record in g.source_events(src,'geometry'):
            if kind in FAMILIES:acc.element(src,line,kind,record)
    arrays=acc.arrays()
    arrays.update(slave_node_set_members=members,slave_segment_set_members=segments,
        slave_segment_attributes=matrix(selected['segment_attributes'],4,'<f8'),
        slave_segment_attribute_missing=matrix(selected['segment_attribute_missing'],4,'?'),
        master_identity=np.asarray([[m['source'],m['set_id'],m['line'],m['membership_row']] for m in masters],dtype='<i8'),
        master_node_ids=np.asarray([m['nodes'] for m in masters],dtype='<i8'),
        master_node_indices=np.asarray([[acc.index[n] for n in m['nodes']] for m in masters],dtype='<i8'),
        master_attributes=np.asarray([[np.nan if v is None else v for v in m['attributes']] for m in masters],dtype='<f8'),
        master_attribute_missing=np.asarray([[v is None for v in m['attributes']] for m in masters],dtype=bool))
    aliases=arrays['master_shell_aliases'];alias_counts=np.bincount(aliases[:,0],minlength=len(masters)) if len(aliases) else np.zeros(len(masters),dtype=np.int64)
    ordered_counts=np.bincount(aliases[aliases[:,2]==1,0],minlength=len(masters)) if len(aliases) else np.zeros(len(masters),dtype=np.int64)
    arrays['master_unordered_alias_count']=alias_counts.astype('<i8');arrays['master_ordered_alias_count']=ordered_counts.astype('<i8')
    summaries=[]
    for index,name in enumerate(['slave_node_set1','slave_segment_set2_nodes','selected_master_vertices']):
        mask=(acc.flags&(1<<index))!=0;local_min=acc.local_min[mask];local_max=acc.local_max[mask]
        summaries.append({'population':name,'unique_nodes':int(mask.sum()),'missing_node_coordinates':int(np.count_nonzero(mask&~acc.node_present)),
            'no_shell_incidence_nodes':int(np.count_nonzero(mask&(acc.family_counts[:,0]==0))),
            'node_element_incidence_by_family':{name:int(acc.family_counts[mask,i].sum()) for name,i in FAMILIES.items()},
            'nodes_with_non_shell_incidence':int(np.count_nonzero(mask&np.any(acc.family_counts[:,1:]>0,axis=1))),
            'beam_orientation_reference_nodes':int(np.count_nonzero(mask&(acc.orientation_counts>0))),
            'corner_slot_occurrences':int(acc.corner_counts[mask].sum()),
            'different_local_supplied_corner_thickness_nodes':int(np.count_nonzero(np.isfinite(local_min)&(local_min!=local_max)))})
    return arrays,{'set_headers':selected['headers'],'CONTROL_CONTACT':selected['controls'],'unparsed_PART_CONTACT':selected['unparsed_PART_CONTACT'],
      'selected_contact_cards':[c for c in old['result']['contacts'] if c['id'] in (1,2)],
      'population_summaries':summaries,'all_node_records':dict(acc.node_counts),
      'membership_summary':{'node_set1_member_occurrences':len(members),'node_set1_unique_IDs':len(populations[0]),
          'node_set1_repeated_ID_occurrences':len(members)-len(populations[0]),'segment_set2_rows':len(segments),
          'segment_set2_unique_ordered_nodes':len(np.unique(segments[:,3:],axis=0)),
          'retained_shell_elements':len(arrays['shell_identity']),'retained_non_shell_elements_or_orientation_references':len(arrays['nonshell_identity']),
          'union_selected_nodes':len(ids)},
      'all_element_records':[{ 'source':src,'family':family,'count':count} for (src,family),count in sorted(acc.element_counts.items())],
      'part_references':part_references(acc,arrays),'include_graph':include_graph,
      'master_alias_summary':{'records':len(masters),'without_unordered_alias':int(np.count_nonzero(alias_counts==0)),
          'multiple_unordered_aliases':int(np.count_nonzero(alias_counts>1)),'without_ordered_alias':int(np.count_nonzero(ordered_counts==0)),
          'multiple_ordered_aliases':int(np.count_nonzero(ordered_counts>1))},
      'scope':'Complete selected-node memberships/coordinates and element-incidence extraction; no proximity, initialized pairs, effective contact thickness, force, restraint, floor attribution or cause.'}


SCHEMA={
 'node_ids':['NID'], 'population_flags':['bit1_NSET1_bit2_SEG2nodes_bit4_master_vertices'],
 'node_xyz':['X','Y','Z'], 'node_source':['SRC'], 'node_line':['physical_source_line'], 'node_present':['coordinate_present'],
 'node_family_incidence':['shell','beam_endpoints','discrete_endpoints','solid'],
 'node_beam_orientation_incidence':['orientation_reference_elements'],
 'node_shell_corner_occurrences':['corner_slots'],
 'node_local_corner_thickness_min':['min_local_THIC_slot'], 'node_local_corner_thickness_max':['max_local_THIC_slot'],
 'node_incident_shell_THIC1to4_min':['min_all_four_THIC_values_on_incident_shells'],
 'node_incident_shell_THIC1to4_max':['max_all_four_THIC_values_on_incident_shells'],
 'node_part_family_counts':['node_array_index','effective_PID','family_code','unique_element_count'],
 'shell_identity':['SRC','connectivity_line','thickness_line','EID','original_PID','effective_PID'],
 'shell_connectivity':['EID','original_PID','N1','N2','N3','N4','N5','N6','N7','N8'],
 'shell_connectivity_missing':['EID','original_PID','N1','N2','N3','N4','N5','N6','N7','N8'],
 'shell_thickness':['THIC1','THIC2','THIC3','THIC4','BETA_or_MCID'],
 'shell_thickness_missing':['THIC1','THIC2','THIC3','THIC4','BETA_or_MCID'],
 'shell_corner_incidence':['node_array_index','saved_shell_index','one_based_corner_slot'],
 'master_shell_aliases':['master_index','saved_shell_index','ordered_match_0_or_1'],
 'nonshell_identity':['SRC','source_line','family_code','EID','original_PID','effective_PID','beam_orientation_NID_or_zero','physical_node_count'],
 'nonshell_physical_nodes':['N1','N2','N3','N4','N5','N6','N7','N8'],
 'nonshell_orientation_missing':['no_beam_orientation_field'],
 'slave_node_set_members':['SRC','physical_source_line','one_based_membership_row','one_based_slot','NID'],
 'slave_segment_set_members':['SRC','physical_source_line','one_based_membership_row','N1','N2','N3','N4'],
 'slave_segment_attributes':['A1','A2','A3','A4'], 'slave_segment_attribute_missing':['A1','A2','A3','A4'],
 'master_identity':['SRC','set_ID','physical_source_line','one_based_membership_row'],
 'master_node_ids':['N1','N2','N3','N4'], 'master_node_indices':['N1_index','N2_index','N3_index','N4_index'],
 'master_attributes':['A1','A2','A3','A4'], 'master_attribute_missing':['A1','A2','A3','A4'],
 'master_unordered_alias_count':['same_four_node_multiset_aliases'], 'master_ordered_alias_count':['same_ordered_four_nodes_aliases']}


def validate_array(name,value,complete_schema=True):
    require(isinstance(value,np.ndarray) and value.dtype.kind in 'biuf','nonnumeric_array')
    require(value.ndim in (1,2),'array_rank')
    if complete_schema:
        require(name in SCHEMA,'unregistered_array')
        require((value.ndim==1 and len(SCHEMA[name])==1) or (value.ndim==2 and value.shape[1]==len(SCHEMA[name])),'array_column_count')
    require(not (value.dtype.kind=='f' and np.any(np.isinf(value))),'infinite_array')


def array_manifest(arrays):
    require(set(arrays)==set(SCHEMA),'array_schema_coverage')
    result={}
    for name,value in sorted(arrays.items()):
        validate_array(name,value)
        result[name]={'shape':list(value.shape),'dtype':value.dtype.str,'columns':SCHEMA[name],
            'c_order_bytes':value.nbytes,'sha256':hashlib.sha256(value.tobytes(order='C')).hexdigest()}
    return result


def check_nonexisting(paths):
    require(not any(p.exists() for p in paths),'existing_output')


def require_new_outputs(paths):
    require(all(p.parent.resolve()==BASE and re.fullmatch(r'independent-[a-z0-9-]+\.(json|npz)',p.name) for p in paths),'output_scope')
    check_nonexisting(paths)


def pin_inputs():
    result={}
    for alias,path,pin in [('protocol',BASE/'PROTOCOL.md',PROTOCOL_SHA),('own_reader',HELPER,HELPER_SHA),
                           ('own_seed',PRIOR/'independent01.json',SEED_SHA),('own_contacts',PRIOR/'independent-contacts01.json',CONTACT_SHA)]:
        actual=g.sha(path);require(actual==pin,'artifact_pin_'+alias);result[alias]=actual
    result['independent_plan']=g.sha(BASE/'INDEPENDENT-STAGE-PLAN.md')
    result['independent_code']=g.sha(Path(__file__))
    for src,pin in g.PINS.items():
        path=g.SOURCE/pin[0];actual=g.sha(path)
        require((path.stat().st_size,actual)==(pin[1],pin[2]),'compressed_pin',src)
        result['SRC'+str(src)]={'bytes':path.stat().st_size,'sha256':actual}
    return result


def controls():
    passed=[]
    def check(label,condition):require(condition,'control_'+label);passed.append(label)
    def rejects(label,operation,code):
        try:operation()
        except g.AuditError as exc:check(label,exc.code==code)
        else:raise g.AuditError('control_missing_rejection_'+label)
    b=b'*KEYWORD\n*SET_NODE_LIST\n1,99\n5,0,5,6\n*SET_SEGMENT\n2\n1,2,3,3,0,,4\n*CONTROL_CONTACT\n1,0,,2\n\n*END\n'
    s=scan_selection(0,io.BytesIO(b))
    check('header_not_member_and_preserved_duplicates',matrix(s['node_members'],5).tolist()==[[0,4,1,1,5],[0,4,1,3,5],[0,4,1,4,6]])
    check('segment_repeats_attributes_and_blanks',matrix(s['segment_members'],7).tolist()==[[0,7,1,1,2,3,3]] and matrix(s['segment_attribute_missing'],4,'?').tolist()==[[False,True,False,True]])
    check('control_numeric_zero_blank_cards',s['controls'][0]['numeric_cards']==[{'line':9,'card':[1.,0.,None,2.,None,None,None,None]},{'line':10,'card':[None]*8}])
    for label,raw,code in [('missing_header',b'*SET_NODE_LIST\n*END\n','selection_missing_header'),
             ('unknown_variant',b'*SET_NODE_LIST_GENERATE\n*END\n','selection_set_variant'),
             ('missing_end',b'*KEYWORD\n','selection_missing_END'),
             ('post_end',b'*END\n1\n','selection_data_after_END'),
             ('duplicate_set',b'*SET_NODE_LIST\n1\n*SET_NODE_LIST\n1\n*END\n','duplicate_set_in_source')]:
        rejects(label,lambda raw=raw:scan_selection(0,io.BytesIO(raw)),code)
    masters=[{'nodes':[1,2,3,3]},{'nodes':[3,1,3,2]},{'nodes':[1,2,2,3]},{'nodes':[1,2,3,4]}]
    acc=Accumulator([1,2,3,4,5,6,7],[1]*7,masters,max_id=30)
    for nid in range(1,9):acc.node(121,100+nid,[nid,float(nid),0.,0.,None,None])
    conn=[10,20,1,2,3,3,None,None,None,None]
    acc.element(121,300,'shell',{'card':conn,'continuation_line':301,'thickness':[1.,2.,3.,4.,999.]})
    acc.element(120,400,'shell',{'card':[11,20,3,1,3,2,None,None,None,None],'continuation_line':401,'thickness':[5.,6.,7.,8.,None]})
    acc.element(121,500,'beam',{'card':[12,21,4,5,6,None,None,None,None,None]})
    acc.element(121,501,'discrete',{'card':[13,22,7,0,6,1.,0,0.]})
    a=acc.arrays()
    check('unique_element_not_repeated_corner',a['node_family_incidence'][2,0]==2 and a['node_shell_corner_occurrences'][2]==4)
    check('corner_slot_thickness_not_fifth',a['node_local_corner_thickness_min'][2]==3 and a['node_local_corner_thickness_max'][2]==7 and a['node_incident_shell_THIC1to4_max'][0]==8)
    check('orientation_not_endpoint',a['node_family_incidence'][5].sum()==0 and a['node_beam_orientation_incidence'][5]==1)
    check('ground_and_VID_not_physical',a['node_family_incidence'][6,2]==1 and a['node_family_incidence'][5,2]==0)
    check('zero_shell_retained',a['node_family_incidence'][3,0]==0 and np.isnan(a['node_local_corner_thickness_min'][3]))
    check('ordered_unordered_multiplicity_and_absence',a['master_shell_aliases'].tolist()==[[0,0,1],[1,0,0],[0,1,0],[1,1,1]])
    check('namespace_and_null_connectivity',a['shell_identity'][:,5].tolist()==[20,1020] and a['shell_connectivity_missing'][:,6:].all())
    check('unique_node_part_element_count',a['node_part_family_counts'].tolist().count([2,20,0,1])==1)
    acc.metadata(120,600,'part',{'keyword_line':598,'card':[20,30,40,None,None,None,None,None]})
    acc.metadata(120,602,'definition',{'keyword_line':601,'keyword':'SECTION_SHELL','id':30})
    acc.metadata(121,604,'definition',{'keyword_line':603,'keyword':'MAT_ELASTIC','id':40})
    refs=part_references(acc,a);p=[r for r in refs if r['effective_part']==1020][0]
    check('proper_material_namespace_and_missing_definition',p['effective_material']==1040 and p['material_definition'] is None and p['section_definition']['effective_id']==1030)
    rejects('duplicate_node',lambda:acc.node(121,700,[1,0,0,0,None,None]),'duplicate_node')
    rejects('missing_node',lambda:acc.element(121,701,'beam',{'card':[14,20,1,29,None,None,None,None,None,None]}),'element_missing_node')
    source=b'*ELEMENT_SHELL_THICKNESS\n10,20,1,2,3,3\n1,2,3,4,0\n*END\n'
    parsed=list(g.Stream(0,io.BytesIO(source),'geometry').events())
    check('actual_reader_shell_continuation',parsed==[('shell',2,{'card':conn,'continuation_line':3,'thickness':[1.,2.,3.,4.,0.]})])
    rejects('missing_shell_continuation',lambda:list(g.Stream(0,io.BytesIO(b'*ELEMENT_SHELL_THICKNESS\n10,20,1,2,3,3\n*END\n'),'geometry').events()),'missing_element_continuation')
    rejects('object_array',lambda:validate_array('x',np.asarray([None],dtype=object),False),'nonnumeric_array')
    rejects('output_scope',lambda:require_new_outputs([BASE/'independent-stage-plan.json',BASE/'INDEPENDENT-STAGE-PLAN.md']),'output_scope')
    rejects('existing_output',lambda:check_nonexisting([Path(__file__)]),'existing_output')
    check('nonexisting_output',check_nonexisting([BASE/'independent-control-nonexistent-7e82.json']) is None)
    rejects('changed_digest',lambda:require(hashlib.sha256(b'changed').hexdigest()==hashlib.sha256(b'original').hexdigest(),'pin_mismatch'),'pin_mismatch')
    check('numeric_NPZ_no_pickle_roundtrip',_npz_control(a))
    STATS.clear();g.PROGRESS.clear()
    return passed


def _npz_control(arrays):
    buf=io.BytesIO();np.savez_compressed(buf,**arrays);buf.seek(0)
    with np.load(buf,allow_pickle=False) as saved:
        return set(saved.files)==set(arrays) and all(np.array_equal(saved[k],a,equal_nan=True) for k,a in arrays.items())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--output',default='independent-stage01.json');args=parser.parse_args()
    started=time.monotonic();tests=controls()
    if args.selftest:
        print(json.dumps({'status':'PASS','controls':tests,'count':len(tests)},sort_keys=True));return
    path=BASE/args.output;npz=path.with_suffix('.npz');failure=path.with_name(path.stem+'-failed.json')
    require_new_outputs([path,npz,failure]);before={}
    try:
        before=pin_inputs();arrays,result=extract();manifest=array_manifest(arrays)
        require(g.peak_memory()<=g.MEMORY_CAP,'memory_cap_after_arrays')
        after=pin_inputs();require(before==after,'inputs_changed_during_run')
        # Metadata inspection gate: no object/string arrays, no full global node dump.
        with npz.open('xb') as f:np.savez_compressed(f,**arrays)
        with np.load(npz,allow_pickle=False) as saved:
            require(set(saved.files)==set(arrays),'saved_array_coverage')
            for key,array_value in arrays.items():
                require(np.array_equal(saved[key],array_value,equal_nan=True),'saved_array_changed')
        final=pin_inputs();require(final==before,'inputs_changed_during_save')
        require(g.peak_memory()<=g.MEMORY_CAP,'memory_cap_after_save')
        receipt={'status':'PASS','command':sys.argv,'seconds':time.monotonic()-started,'peak_bytes':g.peak_memory(),
            'controls':tests,'pins_before':before,'pins_after':final,'source_passes':STATS+g.PROGRESS,
            'array_file':npz.name,'array_file_sha256':g.sha(npz),'array_file_bytes':npz.stat().st_size,
            'array_schema':manifest,'array_missing_policy':'Float NaN denotes absent coordinate/value; explicit masks preserve numeric-card blank versus zero. Padded nonshell vertices are zero outside physical_node_count. All indices zero-based except named source rows/slots.',
            'family_codes':FAMILIES,'namespace':'Source120 PID/MID/SECID/HGID +1000; NID/EID/set IDs unchanged. FCTLEN1, TRANID0; FCTTEM numeric1 not interpreted as temperature multiplier.'}
        with path.open('x') as f:json.dump({'receipt':receipt,'result':result},f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'status':'PASS','output':path.name,'sha256':g.sha(path),'array_sha256':g.sha(npz),'controls':len(tests),
            'source_passes':len(receipt['source_passes']),'populations':result['population_summaries'],'master_alias_summary':result['master_alias_summary'],
            'seconds':receipt['seconds'],'peak_bytes':receipt['peak_bytes']},sort_keys=True))
    except Exception as exc:
        code=exc.code if isinstance(exc,g.AuditError) else type(exc).__name__
        record={'status':'FAIL','code':code,'source':getattr(exc,'source',0),'line':getattr(exc,'line',0),
            'command':sys.argv,'seconds':time.monotonic()-started,'peak_bytes':g.peak_memory(),'controls':tests,
            'pins_before':before,'source_passes':STATS+g.PROGRESS,'array_file_exists':npz.exists(),'result_file_exists':path.exists()}
        try:record['pins_after']=pin_inputs()
        except Exception as pin_exc:record['after_pin_error_code']=getattr(pin_exc,'code',type(pin_exc).__name__)
        with failure.open('x') as f:json.dump(record,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'status':'FAIL','code':code,'source':record['source'],'line':record['line'],'receipt':failure.name},sort_keys=True));raise SystemExit(1) from None


if __name__=='__main__':main()
