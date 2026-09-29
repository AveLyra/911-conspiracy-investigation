#!/usr/bin/env python3
"""Pinned candidate/typed-graph joins; one small CaseA list scan, never a solver."""
import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import time
import verify_restraint as fields

BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'model-member-map'
CASEA=fields.SOURCE/'G6A_CaseA_El_Delete_List.k.gz'
CASEA_PIN=(103872,'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273',325983,45156,'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25')
PINS={
 'CANDIDATE-JOIN-PROTOCOL.md':'aa8360f3ec379479f79f161c5bacc8cf443321e62710e6701bd98077368213c7',
 'CASEA-ID-EXTENSION.md':'d19acd0497e46b023ebe088dfbc40d35ad0f35751d1c09b46cb8f776cb7a5860',
 'independent01.json':'d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7',
 'verify_restraint.py':'5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a',
 '../model-member-map/run06/member-map.json':'eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e',
 '../model-member-map/run06/receipt.json':'4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d',
 '../model-member-map/validation.md':'390122d5a2205109af3c3961a1ebd92526760bbb866c0972ee79f12f7e52b3c9',
 '../model-member-map/verification01.json':'3d4f810181abc5e7aa3ea6b2e60b6b54c330d85a8a12bfd851e1280a7a4c348c',
 '../model-member-map/verification-root01.json':'c1d3fd6e24e1303da8b77bbfa4cc5da3546fab9bfc3c47af049beff4b85ad9a8',
 '../model-member-map/map_members.py':'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b',
}
ALIASES={v[0]:k for k,v in fields.PINS.items()}


def require(ok,code):
    if not ok:raise fields.AuditError(code)


def distinct(nodes):return list(dict.fromkeys(n for n in nodes if n!=0))


def index_graph(graph):
    tables=[]
    for name in ('seed_elements','neighbor_elements'):
        table={}
        for r in graph[name]:
            key=(r['kind'],r['id']);require(key not in table,'duplicate_graph_typed_ID');table[key]=r
        tables.append(table)
    require(not(set(tables[0])&set(tables[1])),'overlapping_graph_classes')
    coords={r['id']:r['xyz'] for r in graph['selected_nodes']}
    require(len(coords)==len(graph['selected_nodes']),'duplicate_graph_node')
    return tables[0],tables[1],coords,set(graph['seed_nodes'])


def match_record(candidate,index):
    seed,neighbors,coords,seednodes=index
    key=(candidate['kind'],candidate['eid']);a=seed.get(key);b=neighbors.get(key)
    require(candidate['source'] in ALIASES,'candidate_source_alias')
    src=ALIASES[candidate['source']];nodes=distinct(candidate['node_ids'])
    require(all(type(n) is int and n>0 for n in nodes),'candidate_node_ID')
    require(len(candidate['node_ids'])==len(candidate['node_coordinates']),'candidate_coordinate_coverage')
    require(not candidate['missing_nodes'],'candidate_missing_nodes')
    require(candidate['pid']==candidate['original_pid']+(1000 if src==120 else 0),'candidate_part_namespace')
    for hit in (a,b):
        if hit:
            require((src,candidate['line'],candidate['original_pid'],candidate['pid'])==
                    (hit['source'],hit['line'],hit['original_part'],hit['effective_part']),'typed_ID_metadata_mismatch')
            require(nodes==distinct(hit['physical_nodes']),'typed_ID_physical_nodes_mismatch')
    matched=sorted(set(nodes)&seednodes)
    require(not matched or a is not None or b is not None,'graph_missing_incident_candidate')
    coordinate_checks=0
    for nid,xyz in zip(candidate['node_ids'],candidate['node_coordinates']):
        if nid in seednodes or ((a or b) and nid!=0):
            require(nid in coords and len(xyz)==3,'matched_coordinate_missing')
            require(all(type(v) in (int,float) and math.isfinite(v) for v in xyz),'invalid_coordinate')
            require(all(float(x).hex()==float(y).hex() for x,y in zip(xyz,coords[nid])),'matched_coordinate_mismatch')
            coordinate_checks+=3
    orient=candidate['orientation_node']
    return {'source':src,'line':candidate['line'],'actual_family':key[0],'eid':key[1],
            'original_part':candidate['original_pid'],'effective_part':candidate['pid'],
            'distinct_physical_nodes':nodes,'orientation_node':orient,
            'orientation_node_in_seed':orient in seednodes,'seed_typed_EID_match':a is not None,
            'direct_neighbor_typed_EID_match':b is not None,'matched_seed_nodes':matched,
            'coordinate_scalars_checked':coordinate_checks}


def candidate_coverage(receipt,model):
    pools=[('shell_list_shell','shell','shell',[r for r in model['damage_set2']['elements'] if r['kind']=='shell']),
           ('beam_list_explicit_beam','beam','beam',[r for r in model['damage_set2']['elements'] if r['kind']=='beam']),
           ('beam_list_discrete_numeric_candidate','beam','discrete',model['set2_beam_id_discrete_candidates']['elements'])]
    require(len(model['damage_set2']['elements'])==len(pools[0][3])+len(pools[1][3]),'unexpected_candidate_family')
    sets={kind:set(v['ids']) for kind,v in receipt['damage_sets'].items()}
    for _,wanted,kind,rows in pools:
        require(all(r['kind']==kind for r in rows),'candidate_pool_family')
        ids=[r['eid'] for r in rows];require(len(ids)==len(set(ids)),'duplicate_candidate_geometry')
        require(set(ids)<=sets[wanted],'candidate_outside_requested_list')
    require({r['eid'] for r in pools[0][3]}==sets['shell'],'missing_shell_candidate_coverage')
    explicit={r['eid'] for r in pools[1][3]};cross={r['eid'] for r in pools[2][3]}
    require(not(explicit&cross) and explicit|cross==sets['beam'],'missing_or_ambiguous_beam_candidate_coverage')
    require(model['damage_set2']['matched']=={'shell':len(pools[0][3]),'beam':len(pools[1][3])},'declared_match_counts')
    require(model['damage_set2']['unmatched']['shell']==[] and set(model['damage_set2']['unmatched']['beam'])==cross,'cross_family_coverage')
    require(model['set2_beam_id_discrete_candidates']['count']==len(cross),'cross_family_count')
    return pools


def scan_casea(stream):
    h=hashlib.sha256();stats={'source':117,'bytes':0,'lines':0,'eof':False};rows=[]
    active=False;header=None;ended=False;keyword_line=None;ordinal=0
    while True:
        raw=stream.readline(16385)
        if not raw:break
        stats['lines']+=1;stats['bytes']+=len(raw);h.update(raw);line=stats['lines']
        require(len(raw)<=16384 and stats['bytes']<=1048576 and b'\0' not in raw,'CaseA_cap_or_NUL')
        try:text=raw.decode('ascii')
        except UnicodeDecodeError:raise fields.AuditError('CaseA_nonascii',117,line) from None
        s=text.split('$',1)[0].strip()
        if not s:continue
        require(not ended,'CaseA_content_after_END')
        if s.startswith('*'):
            token=s[1:].upper();require(token in {'KEYWORD','SET_SHELL_LIST','END'},'CaseA_unknown_keyword')
            if token=='SET_SHELL_LIST':
                require(not active and header is None,'CaseA_duplicate_set');active=True;keyword_line=line
            elif token=='END':ended=True
            else:require(not active and header is None,'CaseA_misplaced_KEYWORD')
            continue
        require(active,'CaseA_data_without_set')
        if header is None:
            card=fields.fields(text,[10]*8,[0],1);require(card[0]==1,'CaseA_not_set1')
            header={'source':117,'set_id':1,'keyword_line':keyword_line,'header_line':line,'header_card':card}
        else:
            card=fields.fields(text,[10]*8,range(8),1)
            for slot,eid in enumerate(card,1):
                if eid in (None,0):continue
                require(type(eid) is int and eid>0,'CaseA_invalid_EID');ordinal+=1
                rows.append({'line':line,'slot':slot,'membership_ordinal':ordinal,'eid':eid})
    require(header is not None and ended,'CaseA_missing_header_or_END')
    stats.update(eof=True,sha256=h.hexdigest())
    return header,rows,stats


def controls():
    passed=[]
    def check(name,value):require(value,'control_'+name);passed.append(name)
    def rejects(name,fn):
        try:fn()
        except fields.AuditError:passed.append(name);return
        raise fields.AuditError('control_unrejected_'+name)
    g={'seed_nodes':[1,2,3],'seed_elements':[{'kind':'shell','id':7,'source':121,'line':11,'original_part':179,'effective_part':179,'physical_nodes':[1,2,3,3]}],
       'neighbor_elements':[],'selected_nodes':[{'id':i,'xyz':[float(i),0.,0.]} for i in [1,2,3]]}
    ix=index_graph(g);c={'source':'wtc7_global_8a_no-conn-matl.k.gz','line':11,'kind':'shell','eid':7,'original_pid':179,'pid':179,
        'node_ids':[1,2,3],'node_coordinates':[[float(i),0.,0.] for i in [1,2,3]],'missing_nodes':[],'orientation_node':None}
    check('typed_seed_and_repeated_vertex_membership',match_record(c,ix)['seed_typed_EID_match'])
    b={**c,'kind':'beam','node_ids':[8,9],'node_coordinates':[[0.,0.,0.]]*2,'orientation_node':1}
    r=match_record(b,ix);check('same_EID_different_family_and_orientation_exclusion',not r['seed_typed_EID_match'] and r['matched_seed_nodes']==[] and r['orientation_node_in_seed'])
    z={**b,'kind':'discrete','node_ids':[8,0],'orientation_node':None};check('ground_zero_excluded',match_record(z,ix)['distinct_physical_nodes']==[8])
    for name,key,value in [('source','source','discrete_mass.k.gz'),('part','pid',1179),('nodes','node_ids',[3,2,1]),('coordinate','node_coordinates',[[99.,0.,0.]]*3)]:
        v=copy.deepcopy(c);v[key]=value;rejects('matching_'+name+'_mismatch',lambda v=v:match_record(v,ix))
    v=copy.deepcopy(c);v['eid']=8;rejects('incomplete_direct_graph',lambda:match_record(v,ix))
    v=copy.deepcopy(g);v['seed_elements']*=2;rejects('duplicate_graph_typed_ID',lambda:index_graph(v))
    check('no_match',match_record({**b,'orientation_node':None},ix)['matched_seed_nodes']==[])
    raw=b'*KEYWORD\n*SET_SHELL_LIST\n1,0,0,0,0\n7,7,8 $ comment\n*END\n'
    h,rows,s=scan_casea(io.BytesIO(raw))
    check('CaseA_header_duplicates_slots_comments',h['header_line']==3 and [r['eid'] for r in rows]==[7,7,8] and [r['slot'] for r in rows]==[1,2,3])
    check('CaseA_EOF_hash',s['eof'] and s['sha256']==hashlib.sha256(raw).hexdigest())
    for name,raw in [('unknown',b'*UNKNOWN\n'),('missing_header',b'*SET_SHELL_LIST\n*END\n'),('post_END',b'*SET_SHELL_LIST\n1\n*END\n7\n'),('invalid_ID',b'*SET_SHELL_LIST\n1\n1.5\n*END\n')]:
        rejects('CaseA_'+name,lambda raw=raw:scan_casea(io.BytesIO(raw)))
    rc={'damage_sets':{'shell':{'ids':[7]},'beam':{'ids':[]}}};mo={'damage_set2':{'elements':[],'matched':{'shell':0,'beam':0},'unmatched':{'shell':[7],'beam':[]}},'set2_beam_id_discrete_candidates':{'elements':[],'count':0}}
    rejects('missing_candidate_coverage',lambda:candidate_coverage(rc,mo))
    return passed


def pins():
    out={}
    for name,want in PINS.items():
        got=fields.sha(BASE/name);require(got==want,'artifact_pin');out[name]=got
    require(CASEA.stat().st_size==CASEA_PIN[0] and fields.sha(CASEA)==CASEA_PIN[1],'CaseA_compressed_pin')
    out['SRC117']={'bytes':CASEA_PIN[0],'sha256':CASEA_PIN[1]};out['code']=fields.sha(Path(__file__))
    return out


def calculate():
    load=lambda p:json.loads(p.read_text())
    model=load(OLD/'run06/member-map.json');receipt=load(OLD/'run06/receipt.json')
    verified=load(OLD/'verification01.json');consumer=load(OLD/'verification-root01.json')
    graph_receipt=load(BASE/'independent01.json');graph=graph_receipt['result']
    require(receipt['status']=='complete' and receipt['result_sha256']==PINS['../model-member-map/run06/member-map.json'],'old_receipt_result')
    require(verified['status']=='PASS' and not verified['failures'] and verified['input_hashes_before']==verified['input_hashes_after'],'old_verification')
    require({k:v for k,v in verified.items() if k!='command'}=={k:v for k,v in consumer.items() if k!='command'},'old_consumer_equality')
    require(all(s['eof'] is True and s['pin_after'] is True for s in receipt['sources'].values()),'old_source_EOF')
    require(graph_receipt['receipt']['status']=='PASS' and len(graph['seed_nodes'])==873 and len(graph['seed_elements'])==952 and len(graph['neighbor_elements'])==20,'graph_scope')
    pools=candidate_coverage(receipt,model);ix=index_graph(graph);results=[]
    for label,wanted,actual,records in pools:
        positions=defaultdict(list)
        for i,eid in enumerate(receipt['damage_sets'][wanted]['ids'],1):positions[eid].append(i)
        joined=[]
        for r in records:
            joined.append({**match_record(r,ix),'requested_family':wanted,'set_id':2,'list_source':116,
                'list_header_line':receipt['damage_sets'][wanted]['header_line'],
                'list_membership_ordinals':positions[r['eid']]})
        summary={'candidate_records':len(joined),'requested_list_occurrences':len(receipt['damage_sets'][wanted]['ids']),
                 'requested_list_unique_IDs':len(positions),'requested_list_duplicate_occurrences':sum(len(p)-1 for p in positions.values()),
                 'seed_typed_EID_matches':sum(r['seed_typed_EID_match'] for r in joined),
                 'direct_neighbor_typed_EID_matches':sum(r['direct_neighbor_typed_EID_match'] for r in joined),
                 'records_sharing_seed_nodes':sum(bool(r['matched_seed_nodes']) for r in joined),
                 'distinct_shared_seed_nodes':len({n for r in joined for n in r['matched_seed_nodes']}),
                 'orientation_only_seed_records':sum(r['orientation_node_in_seed'] and not r['matched_seed_nodes'] for r in joined),
                 'coordinate_scalars_checked':sum(r['coordinate_scalars_checked'] for r in joined)}
        results.append({'pool':label,'requested_family':wanted,'actual_family':actual,'summary':summary,'records':joined})
    with gzip.open(CASEA,'rb') as f:header,rows,stream=scan_casea(f)
    require((stream['bytes'],stream['lines'],stream['sha256'])==CASEA_PIN[2:],'CaseA_EOF_pin')
    old=receipt['casea_sets']['shell'];ids=[r['eid'] for r in rows]
    require(header['set_id']==old['set_id'] and header['header_line']==old['header_line'] and len(set(ids))==old['count'],'CaseA_old_count_header')
    seed,neighbors,coords,seednodes=ix;selected=[]
    for row in rows:
        key=('shell',row['eid']);a=seed.get(key);b=neighbors.get(key);hit=a or b
        if hit:selected.append({**row,'actual_family':'shell','seed_typed_EID_match':a is not None,
            'direct_neighbor_typed_EID_match':b is not None,'geometry_source':hit['source'],'geometry_line':hit['line'],
            'effective_part':hit['effective_part'],'distinct_physical_nodes':distinct(hit['physical_nodes']),
            'matched_seed_nodes':sorted(set(hit['physical_nodes'])&seednodes)})
    casea={'source':117,'set_header':header,'membership_occurrences':len(ids),'unique_IDs':len(set(ids)),
        'duplicate_occurrences':len(ids)-len(set(ids)),'normalized_membership_sha256':hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),
        'selected_membership_records':selected,'seed_unique_EID_matches':len({r['eid'] for r in selected if r['seed_typed_EID_match']}),
        'neighbor_unique_EID_matches':len({r['eid'] for r in selected if r['direct_neighbor_typed_EID_match']}),
        'unique_elements_sharing_seed_nodes':len({r['eid'] for r in selected if r['matched_seed_nodes']}),
        'distinct_shared_seed_nodes':len({n for r in selected for n in r['matched_seed_nodes']}),
        'derivation':'One new typed-list source scan joined to the complete frozen direct graph; no full CaseA geometry extraction.',
        'stream':stream}
    return {'set2_pools':results,'CaseA_set1':casea,'old_verification_coverage':verified['coverage'],
            'ceiling':'Candidate relationships only. No activation, deletion semantics, solver execution, contact/proximity coverage, directional restraint, capacity or historical cause.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selftest',action='store_true');p.add_argument('--output');a=p.parse_args()
    if a.selftest:print(json.dumps({'status':'PASS','controls':controls()}));return 0
    require(a.output and Path(a.output).name==a.output and a.output.endswith('.json'),'output_basename')
    dest=BASE/a.output;require(not dest.exists(),'output_exists');start=time.monotonic();tests=controls();before=pins()
    try:result=calculate();status='PASS';error=None
    except fields.AuditError as e:result=None;status='FAIL';error={'code':e.code,'source':e.source,'line':e.line}
    after=pins();require(before==after,'pins_changed')
    out={'status':status,'error':error,'pins_before':before,'pins_after':after,'controls':tests,'result':result,
         'command':[sys.executable,*sys.argv],'elapsed_seconds':time.monotonic()-start,'peak_rss_bytes':fields.peak_memory()}
    with dest.open('x') as f:json.dump(out,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':status,'error':error,'sha256':fields.sha(dest),'controls':len(tests),
                     'set2_summaries':[{r['pool']:r['summary']} for r in result['set2_pools']] if result else None,
                     'CaseA_summary':{k:result['CaseA_set1'][k] for k in ['membership_occurrences','unique_IDs','seed_unique_EID_matches','neighbor_unique_EID_matches','unique_elements_sharing_seed_nodes','distinct_shared_seed_nodes']} if result else None}))
    return 0 if status=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except fields.AuditError as e:print(json.dumps({'status':'FAIL','code':e.code,'source':e.source,'line':e.line}));raise SystemExit(1)
