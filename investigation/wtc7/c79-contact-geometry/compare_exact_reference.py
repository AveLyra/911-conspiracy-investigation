#!/usr/bin/env python3
"""Post-freeze reference-schema adapter for the separately reproduced exact geometry.

Imports only the hash-pinned independent certificate consumer, never a producer.
The mathematical implementation and source extraction were frozen before this
adapter inspected the reference schema. Float views are compared as views only.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import numpy as np

BASE=Path(__file__).resolve().parent
HELPER_SHA='9854b4d2df68ae14b03a834539c79163a66961407c0cee193ace2361f9edd7e3'
REFERENCE_PINS={80:{
 'exact-proximity80.json':'25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
 'exact-proximity80.npz':'79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
 'exact-proximity80-proofs.json':'53757ba19edeeacf7ec64222786344977cb02eef5d54d7da2cbae0445e4bd2e6'},120:{
 'exact-proximity120.json':'ec72208fb65f7a849efebae77af5c834c4eb17e1180dddca2f1a17fb525d0711',
 'exact-proximity120.npz':'79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
 'exact-proximity120-proofs.json':'f653b0d0d4e69bfd42a79bb1321e540c4a18a92bdaa99efd3540bccc13fe80e7'}}
REPLAY_PINS={
 'exact-proximity80.json':'25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
 'exact-proximity80-root01.json':'60e12bb8f70944cb0c8996e7a1e8387c3405de7e5b341e5d6bfd2c84e08843f3',
 'exact-proximity80-root01.npz':'79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
 'exact-proximity80-root01-proofs.json':'53757ba19edeeacf7ec64222786344977cb02eef5d54d7da2cbae0445e4bd2e6'}
REFERENCE_CODE_SHA='032804acb5862b6202d7037b864b2421c10b0f8383b0f2382a856810423dc25f'
MEMORY_CAP=768*1024**2
COUNTS={'array_fields':0,'array_slots':0,'numeric_leaves':0,'string_leaves':0,'nulls':0,'bools':0,'pair_proofs':0,'geometry_proofs':0}


class Mismatch(Exception):pass


def require(value,code):
    if not value:raise Mismatch(code)


def sha(path):
    with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()


require(sha(BASE/'compare_exact_proximity.py')==HELPER_SHA,'helper_pin')
spec=importlib.util.spec_from_file_location('independent_exact_certificate_consumer',BASE/'compare_exact_proximity.py')
H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)


def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)


def equal(x,y,path):
    require(type(x)==type(y),path+'_type')
    if isinstance(x,dict):
        require(set(x)==set(y),path+'_keys')
        for key in x:equal(x[key],y[key],path+'/'+key)
    elif isinstance(x,list):
        require(len(x)==len(y),path+'_length')
        for i,(a,b) in enumerate(zip(x,y)):equal(a,b,path+'/'+str(i))
    else:
        require(x==y,path+'_value')
        if x is None:COUNTS['nulls']+=1
        elif isinstance(x,bool):COUNTS['bools']+=1
        elif isinstance(x,str):COUNTS['string_leaves']+=1
        elif isinstance(x,(int,float)):COUNTS['numeric_leaves']+=1
        else:raise Mismatch(path+'_unsupported_type')


def equal_array(x,y,path):
    require(x.dtype==y.dtype and x.shape==y.shape,path+'_schema')
    require(np.array_equal(x,y,equal_nan=True),path+'_values')
    COUNTS['array_fields']+=1;COUNTS['array_slots']+=x.size


def encoded(f):return [str(f.numerator),str(f.denominator)]
def interval_encoded(v):return [encoded(f) for f in v]
def midpoint(v):return math.nan if v is None else float(sum(map(H.fraction,v),Fraction(0))/2)


def outward(value,upper):
    result=float(value);require(math.isfinite(result),'finite_slab_conversion')
    while (H.binary(result)<value if upper else H.binary(result)>value):
        result=math.nextafter(result,math.inf if upper else -math.inf)
    return result


def pin_all(bits):
    expected=dict(H.PINS);expected.update(REFERENCE_PINS[bits]);expected.update(REPLAY_PINS);expected.update({'compare_exact_proximity.py':HELPER_SHA,'exact_proximity.py':REFERENCE_CODE_SHA})
    actual={name:sha(BASE/name) for name in expected};require(actual==expected,'input_pin')
    actual['adapter_code']=sha(Path(__file__));return actual


def read_reference(bits):
    record=json.loads((BASE/f'exact-proximity{bits}.json').read_text())
    require(record['status']=='passed' and record['precision_bits']==bits,'reference_status_bits')
    require(record['producer_sha256']==REFERENCE_CODE_SHA,'reference_producer_pin')
    equal(record['pins_before'],record['pins_after'],'reference_unchanged_inputs')
    for name,expected in record['pins_before'].items():require(sha(BASE/name)==expected,'reference_fresh_input_pin')
    proof_path=BASE/record['proof_file'];require(sha(proof_path)==record['proof_sha256'],'reference_proof_pin')
    proofs=json.loads(proof_path.read_text());require(proofs['precision_bits']==bits,'reference_proof_bits')
    path=BASE/record['array_file'];require(sha(path)==record['array_sha256'],'reference_array_pin')
    with np.load(path,allow_pickle=False) as source:
        require(set(source.files)==set(record['array_schema']),'reference_array_coverage');arrays={}
        for name in source.files:
            value=source[name];s=record['array_schema'][name]
            require(value.dtype.kind in 'biuf' and str(value.dtype)==s['dtype'] and list(value.shape)==s['shape'],'reference_array_schema')
            require(hashlib.sha256(value.tobytes(order='C')).hexdigest()==s['sha256'],'reference_array_content_pin')
            arrays[name]=value
    return record,proofs,arrays


def extra_source():
    stage=json.loads((BASE/'independent-stage01.json').read_text());arrays={}
    with np.load(BASE/'independent-stage01.npz',allow_pickle=False) as source:
        for name in ('node_part_family_counts','population_flags'):
            value=source[name];require(hashlib.sha256(value.tobytes(order='C')).hexdigest()==stage['receipt']['array_schema'][name]['sha256'],'extra_source_array_pin')
            arrays[name]=value
    return arrays


def reference_replay80():
    original=json.loads((BASE/'exact-proximity80.json').read_text());replay=json.loads((BASE/'exact-proximity80-root01.json').read_text())
    differences=[]
    def visit(x,y,path=''):
        require(type(x)==type(y),'replay_type')
        if isinstance(x,dict):
            require(set(x)==set(y),'replay_keys')
            for key in x:visit(x[key],y[key],path+'/'+key)
        elif isinstance(x,list):
            require(len(x)==len(y),'replay_list_length')
            for i,(left,right) in enumerate(zip(x,y)):visit(left,right,path+'/'+str(i))
        elif x!=y:differences.append({'path':path,'original':x,'replay':y})
    visit(original,replay)
    allowed={'/command/4','/array_file','/proof_file','/elapsed_seconds','/peak_rss_bytes'}
    require(all(item['path'] in allowed for item in differences),'unexpected_reference_replay_difference')
    require(replay['status']=='passed' and replay['array_sha256']==original['array_sha256'] and replay['proof_sha256']==original['proof_sha256'],'reference_replay_products')
    require(sha(BASE/replay['array_file'])==replay['array_sha256'] and sha(BASE/replay['proof_file'])==replay['proof_sha256'],'reference_replay_product_pins')
    return {'status':'PASS','differences_excluded':differences,'all_other_receipt_fields_equal':True,'array_and_proof_bytes_equal_by_SHA256':True}


def compare(bits):
    own_name='independent-exact80-02.json' if bits==80 else 'independent-exact120-01.json'
    own=json.loads((BASE/own_name).read_text());a=H.load_arrays(own);source,ranges=H.source_arrays();extra=extra_source()
    reference,proof,r=read_reference(bits)
    epsilon=H.fraction(own['result']['epsilon_exact'])
    expected_constants={'epsilon':encoded(epsilon),'0.6':encoded(H.binary(.6)),'0.05':encoded(H.binary(.05)),
      'settings':[encoded(H.binary(v)) for v in (1.,1.006,1.025)]}
    equal(proof['constants'],expected_constants,'constants')
    own_rows=a['identities'];order=np.lexsort((own_rows[:,5],own_rows[:,2],own_rows[:,0]));sorted_rows=own_rows[order]
    mapped_rows=sorted_rows[:,[0,2,5,12,13,14]].copy()
    equal_array(mapped_rows,r['pairs'],'pairs_all_fields')
    equal_array(a['projection_flags'][order],r['pair_projection_inside'],'projection_flags')
    equal_array(a['master_node_ids'],r['master_nodes'],'ordered_master_nodes')
    mi=a['master_source_identity'];require(np.all(mi[:,0]==121),'master_SRC_alias')
    cid=np.where(mi[:,1]==1,1,np.where(mi[:,1]==3,2,-1));require(np.all(cid>0),'CID_set_mapping')
    master_identity=np.column_stack([cid,mi[:,1:3]]).astype(np.int64)
    equal_array(master_identity,r['master_identity'],'master_CID_set_line')
    equal_array(np.asarray([1.,1.006,1.025]),r['settings'],'settings_binary')
    for cid_value in (1,2):
        equal_array(a[f'CID{cid_value}_admission_bits'],r[f'broad_mask_cid{cid_value}'],'whole_population_mask_'+str(cid_value))
        equal_array(source['node_ids'][a[f'CID{cid_value}_population_indices']],r[f'slave_ids_cid{cid_value}'],'slave_ID_order_'+str(cid_value))
    incidence=extra['node_part_family_counts'];selected=incidence[np.isin(incidence[:,0],np.unique(own_rows[:,4]))]
    mapped_incidence=np.column_stack([source['node_ids'][selected[:,0]],selected[:,2],selected[:,1],selected[:,3]])
    mapped_incidence=mapped_incidence[np.lexsort((mapped_incidence[:,2],mapped_incidence[:,1],mapped_incidence[:,0]))]
    equal_array(mapped_incidence,r['admitted_node_part_incidence'],'all_admitted_node_part_family_incidence')

    # Schema-only normalization of the fully frozen independent proof rows.
    require(len(proof['rows'])==len(order),'proof_pair_count')
    views=[];pair_mapping={'dA_squared':'dA_squared','dB_squared':'dB_squared','dA':'dA','dB':'dB',
      'patch_enclosure':'patch','aabb_squared':'box_squared','signed_plane_enclosures':'signed_planes'}
    for position,independent_index in enumerate(order):
        ownproof=own['result']['pair_certificates'][int(independent_index)];cert=ownproof['certificate'];rr=proof['rows'][position]
        mapped={reference_key:cert[own_key] for own_key,reference_key in pair_mapping.items()}
        mapped['row']=list(map(int,mapped_rows[position,:4]))
        mapped['delta_low']=None if cert['thresholds'] is None else cert['thresholds'][0]
        mapped['delta_high']=None if cert['thresholds'] is None else cert['thresholds'][1]
        equal(mapped,rr,'exact_pair_proof/'+str(position));COUNTS['pair_proofs']+=1
        # Independently reclassify the reference certificates, including unknown priority and strict epsilon endpoints.
        thresholds=None if rr['delta_low'] is None else (H.interval(rr['delta_low']),H.interval(rr['delta_high']))
        require(H.classified(H.interval(rr['patch']),thresholds,epsilon)==int(r['pairs'][position,3]),'reference_certificate_class')
        for name in ('dA','dB'):H.valid_sqrt(H.fraction(rr[name+'_squared']),H.interval(rr[name]),bits)
        views.append([midpoint(cert['dA']),midpoint(cert['dB']),float(H.fraction(cert['patch_enclosure'][0])),float(H.fraction(cert['patch_enclosure'][1])),
                      midpoint(mapped['delta_low']),midpoint(mapped['delta_high']),*[midpoint(v) for v in cert['signed_plane_enclosures']]])
    equal_array(np.asarray(views,dtype=np.float64),r['pair_values'],'all_float_views_of_exact_proofs')

    geometries={(g['setting'],g['master_index']):g for g in own['result']['geometry_certificates']}
    require(len(geometries)==len(proof['geometry'])==3*len(mi),'geometry_certificate_count')
    coverage=np.empty_like(r['coverage']);quad_views=np.empty_like(r['geometry_quad']);w_views=np.empty_like(r['geometry_w'])
    all_cached_nodes=set(map(int,np.unique(a['master_node_ids'])));slab_definition_differences=[]
    for item in proof['geometry']:
        setting=item['setting'];master=item['master'];g=geometries[(setting,master)];cid_value=int(cid[master])
        corners=tuple(tuple(H.fraction(v) for v in p) for p in g['extended_corners'])
        original=tuple(tuple(H.binary(v) for v in p) for p in source['node_xyz'][source['master_node_indices'][master]])
        diag2=[H.distance_squared(original[0],original[2]),H.distance_squared(original[1],original[3])]
        short=H.independent_root_bounds(min(diag2),bits)
        mixed=tuple(corners[0][k]-corners[1][k]+corners[2][k]-corners[3][k] for k in range(3))
        w2=sum((v*v for v in mixed),Fraction(0))/16;wi=H.independent_root_bounds(w2,bits)
        gate=H.fraction(g['broad_phase']['global_slab_radius'])
        expected={'setting':setting,'master':master,'corners':g['extended_corners'],'w_squared':encoded(w2),'w':interval_encoded(wi),
          'original_diagonal_squared':[encoded(d) for d in diag2],'shorter_diagonal':interval_encoded(short),'global_slab_gate_upper':encoded(gate)}
        equal(expected,item,'exact_geometry_proof/'+str(setting)+'/'+str(master));COUNTS['geometry_proofs']+=1
        quad_views[setting,master]=[[float(v) for v in p] for p in corners];w_views[setting,master]=float(sum(wi)/2)
        population=a[f'CID{cid_value}_population_indices'];points=source['node_xyz'][population]
        unknown=np.isnan(source['node_local_corner_thickness_min'][population])
        # Post-schema broad-slab count check: outer binary64 bounds on ALL nodes,
        # matching reference's counter definition, not substituting own known/exact counter.
        slab=np.ones(len(population),dtype=bool)
        for axis in range(3):
            low=outward(min(p[axis] for p in corners)-gate,False)
            high=outward(max(p[axis] for p in corners)+gate,True)
            slab&=(points[:,axis]>=low)&(points[:,axis]<=high)
        candidates=slab|unknown;own_count=a['coverage'][setting,master]
        all_cached_nodes.update(map(int,source['node_ids'][population[candidates]]))
        coverage[setting,master]=[len(population),int(slab.sum()),int(candidates.sum()),int(own_count[5]),int(own_count[6]),int(own_count[11]),*map(int,own_count[7:11])]
        known_outer=int(np.count_nonzero(slab&~unknown));known_exact=int(own_count[3])
        if known_outer!=known_exact or np.count_nonzero(slab&unknown):
            slab_definition_differences.append({'setting':setting,'master':master,'known_outer_float_slab':known_outer,'known_exact_slab':known_exact,'unknown_in_outer_slab':int(np.count_nonzero(slab&unknown))})
    equal_array(coverage,r['coverage'],'all_reference_coverage_fields')
    equal_array(quad_views,r['geometry_quad'],'extended_corner_float_views')
    equal_array(w_views,r['geometry_w'],'w_midpoint_float_views')
    require(COUNTS['array_fields']==len(r),'all_reference_array_fields_accounted')
    groups=[]
    for setting in range(3):
        for cid_value in (1,2):
            selected=sorted_rows[(sorted_rows[:,0]==setting)&(sorted_rows[:,1]==cid_value)]
            groups.append({'setting_index':setting,'cid':cid_value,'admitted':len(selected),'classes':np.bincount(selected[:,12],minlength=4).tolist(),
              'unique_nodes_by_class':{str(cls):len(np.unique(selected[selected[:,12]==cls,5])) for cls in range(4)}})
    expected_result={'groups':groups,'coordinate_cache_nodes':len(all_cached_nodes),'proof_rows':len(own_rows),
      'total_population_memberships':int(coverage[:,:,0].sum()),'total_slab_candidates':int(coverage[:,:,1].sum()),
      'total_box_interval_ambiguities':int(coverage[:,:,5].sum())}
    float_comp={}
    for filename,keys in [('independent-proximity01.npz',('CID1_admission_bits','CID2_admission_bits')),('proximity-root01.npz',('broad_mask_cid1','broad_mask_cid2'))]:
        with np.load(BASE/filename,allow_pickle=False) as old:
            bycid={}
            for cid_value,key in zip((1,2),keys):
                former=old[key];current=r[f'broad_mask_cid{cid_value}'];require(np.array_equal(former,current),'frozen_float_mask_agreement')
                bycid[str(cid_value)]={'equal':True,'exact_added_memberships':0,'floating_only_memberships':0}
            float_comp[filename]=bycid
    expected_result['floating_mask_comparisons']=float_comp
    equal(expected_result,reference['result'],'reference_all_result_summaries')
    return {'status':'PASS','precision_bits':bits,'counts':dict(COUNTS),'slab_definition_discrepancies':slab_definition_differences,
      'reference_summaries':expected_result,'normalizations':[
        'Own CID/master/setting traversal is reordered by exact setting/master/NID keys; no class or source slot is dropped.',
        'Own15-column identity retains source locators and membership row. Reference6-column pairs matched on all6; reference masterCID/set/line and ordered nodes checked separately.',
        'All rational strings matched as canonical numerator/denominator pairs. dA/dB squared distances, both root intervals, patch, thresholds, signed planes and exact box distances match.',
        'Original two diagonal squared values are independently recombined post-schema from the frozen original coordinates; own frozen result retained only their minimum.',
        'Reference slab count is the outer float slab over all nodes. It is independently recomputed, not coerced to own exact-slab known-node count.',
        'Root float views match exact rational midpoint/endpoints converted to binary64; these are views, not certified outward floating bounds.',
        'Part-family incidence is normalized from own source node index/effectivePID/family to exact NID/family/effectivePID/count.'],
      'independence':'All own source and rational computations froze before reference access. This later adapter checks the schema exhaustively and recomputes the specifically disclosed additional counter/diagonal views; it is not a third independently blind discovery.',
      'scope_ceiling':'Exact reproducibility of this parsed-input geometric surrogate, not physical accuracy or actual contact, restraint, capacity, run provenance or collapse cause.'}


def controls():
    passed=[]
    def reject(name,fn):
        try:fn()
        except Mismatch:passed.append(name);return
        raise Mismatch('missed_mutation_'+name)
    equal([1,None,True,'2'],[1,None,True,'2'],'positive');passed.append('recursive_exact_positive')
    reject('identity_order_mutation',lambda:equal([1,2],[2,1],'ids'))
    reject('missing_proof_field',lambda:equal({'x':1},{},'keys'))
    reject('fraction_string_mutation',lambda:equal(['1','2'],['2','4'],'canonical'))
    reject('null_threshold_changed_to_zero',lambda:equal(None,['0','1'],'unknown'))
    reject('integer_bool_coercion',lambda:equal(1,True,'types'))
    reject('class_mutation',lambda:equal(3,2,'class'))
    reject('projection_mutation',lambda:equal_array(np.asarray([0],dtype=np.int8),np.asarray([1],dtype=np.int8),'projection'))
    reject('mask_bit_mutation',lambda:equal_array(np.asarray([1],dtype=np.uint8),np.asarray([2],dtype=np.uint8),'mask'))
    reject('coordinate_view_mutation',lambda:equal_array(np.asarray([1.]),np.asarray([np.nextafter(1.,2.)]),'view'))
    equal_array(np.asarray([math.nan]),np.asarray([math.nan]),'defined_NaN');passed.append('same_undefined_positions')
    reject('NaN_changed_to_zero',lambda:equal_array(np.asarray([math.nan]),np.asarray([0.]),'undefined'))
    for key in COUNTS:COUNTS[key]=0
    return passed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bits',type=int,choices=(80,120),default=80);parser.add_argument('--output',default='independent-exact-reference80-01.json');parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    started=time.monotonic();test=controls()
    if args.selftest:print(json.dumps({'status':'PASS','count':len(test),'controls':test}));return
    require(args.bits in REFERENCE_PINS,'reference_precision_not_yet_pinned')
    path=BASE/args.output;require(path.parent.resolve()==BASE and re.fullmatch(r'independent-exact-reference(?:80|120)-[a-z0-9]+\.json',path.name),'output_scope');require(not path.exists(),'existing_output')
    before={}
    try:
        before=pin_all(args.bits);result=compare(args.bits);result['actual_reference80_replay']=reference_replay80();after=pin_all(args.bits);require(before==after,'pins_changed');require(peak()<=MEMORY_CAP,'memory_cap')
        receipt={'status':'PASS','command':sys.argv,'elapsed_seconds':time.monotonic()-started,'peak_bytes':peak(),'pins_before':before,'pins_after':after,'controls':test,'result':result}
    except Exception as exc:
        receipt={'status':'FAIL','code':str(exc) if isinstance(exc,(Mismatch,H.Disagreement)) else type(exc).__name__,'command':sys.argv,
          'elapsed_seconds':time.monotonic()-started,'peak_bytes':peak(),'pins_before':before,'controls':test,'counts_before_failure':dict(COUNTS)}
        try:receipt['pins_after']=pin_all(args.bits)
        except Exception as later:receipt['after_pin_error']=type(later).__name__
    with path.open('x') as handle:json.dump(receipt,handle,indent=2,sort_keys=True,allow_nan=False);handle.write('\n')
    print(json.dumps({'status':receipt['status'],'output':path.name,'sha256':sha(path),'controls':len(test),'seconds':receipt['elapsed_seconds'],'peak_bytes':receipt['peak_bytes']}))
    if receipt['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
