#!/usr/bin/env python3
"""Post-freeze exact-certificate consumer. No geometric producer imports."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import resource
import sys
import tempfile
import time
import numpy as np

BASE=Path(__file__).resolve().parent
PINS={'verify_exact_proximity.py':'c850bdb2e02843e4cbdf2c3cb08b309e25d47708d9fa7b1e41bc4dbe9d044e2f',
 'EXACT-ARITHMETIC-ADDENDUM.md':'b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89',
 'independent-exact80-02.json':'df8246830906ba20a814835d69f45c0196301ab76179e84b227c447d0352b11e',
 'independent-exact120-01.json':'ecbde1063f26bbc520fdbae40209c88c5e433542eee97c6e92b212dc08ffab62',
 'independent-exact80-02.npz':'6c4bf3e3bdfeb00c14ef859407c7d685c950123a415a49452e4058e0aecbd8a4',
 'independent-exact120-01.npz':'6c4bf3e3bdfeb00c14ef859407c7d685c950123a415a49452e4058e0aecbd8a4',
 'independent-stage01.json':'ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd',
 'independent-stage01.npz':'fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5'}
MEMORY_CAP=768*1024**2


class Disagreement(Exception):pass


def require(ok,code):
    if not ok:raise Disagreement(code)


def sha(path):
    with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()


def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)


def pins():
    actual={name:sha(BASE/name) for name in PINS};require(actual==PINS,'input_pin')
    actual['comparison_code']=sha(Path(__file__));return actual


def fraction(value):
    require(isinstance(value,list) and len(value)==2 and all(isinstance(v,str) for v in value),'fraction_schema')
    require(re.fullmatch(r'-?(?:0|[1-9][0-9]*)',value[0]) is not None and re.fullmatch(r'[1-9][0-9]*',value[1]) is not None,'fraction_lexical')
    result=Fraction(int(value[0]),int(value[1]))
    require([str(result.numerator),str(result.denominator)]==value,'fraction_canonical')
    return result


def binary(value):
    value=float(value);require(math.isfinite(value),'source_finite')
    return Fraction(*value.as_integer_ratio())


def interval(value):
    require(isinstance(value,list) and len(value)==2,'interval_schema')
    lower,upper=map(fraction,value);require(lower<=upper,'inverted_interval')
    return lower,upper


def valid_sqrt(square,enclosure,bits):
    lower,upper=enclosure;step=Fraction(1,1<<bits)
    require(square>=0 and lower>=0 and lower<=upper,'sqrt_domain')
    require((lower/step).denominator==1,'sqrt_lower_dyadic_grid')
    require(lower*lower<=square<(lower+step)**2,'sqrt_floor_property')
    require(upper==(lower if lower*lower==square else lower+step),'sqrt_upper_definition')
    require(lower*lower<=square<=upper*upper,'sqrt_encloses')


def independent_root_bounds(square,bits):
    scale=1<<bits;floor=math.isqrt((square.numerator*scale*scale)//square.denominator)
    low=Fraction(floor,scale);high=low if low*low==square else low+Fraction(1,scale)
    valid_sqrt(square,(low,high),bits);return low,high


def classified(patch,thresholds,epsilon):
    if thresholds is None:return 0
    if patch[1]<thresholds[0][0]-epsilon:return 3
    if patch[0]>thresholds[1][1]+epsilon:return 1
    return 2


def nested(coarse,fine):require(coarse[0]<=fine[0]<=fine[1]<=coarse[1],'interval_not_nested')


def same(left,right,code):require(left==right,code)


def weighted_corners(original,e):
    h=(e-1)/2
    return tuple(tuple((1-u)*(1-v)*original[0][j]+u*(1-v)*original[1][j]+u*v*original[2][j]+(1-u)*v*original[3][j] for j in range(3))
                 for u,v in ((-h,-h),(1+h,-h),(1+h,1+h),(-h,1+h)))


def distance_squared(a,b):return sum(((x-y)**2 for x,y in zip(a,b)),Fraction(0))


def load_arrays(record):
    receipt=record['receipt'];require(receipt['status']=='PASS','result_not_PASS')
    path=BASE/receipt['array_file'];require(sha(path)==receipt['array_sha256'],'archive_hash')
    with np.load(path,allow_pickle=False) as source:
        require(set(source.files)==set(receipt['array_schema']),'archive_key_coverage')
        arrays={}
        for name in source.files:
            value=source[name];spec=receipt['array_schema'][name]
            require(value.dtype.kind in 'biuf' and value.dtype.str==spec['dtype'] and list(value.shape)==spec['shape'],'array_schema')
            require(hashlib.sha256(value.tobytes(order='C')).hexdigest()==spec['sha256'],'array_pin')
            arrays[name]=value
    return arrays


def source_arrays():
    stage=json.loads((BASE/'independent-stage01.json').read_text());schema=stage['receipt']['array_schema']
    names=('node_ids','node_xyz','node_source','node_line','node_local_corner_thickness_min','node_local_corner_thickness_max',
           'master_identity','master_node_ids','master_node_indices','master_shell_aliases','shell_identity','shell_thickness')
    selected={}
    with np.load(BASE/'independent-stage01.npz',allow_pickle=False) as source:
        for name in names:
            value=source[name];require(hashlib.sha256(value.tobytes(order='C')).hexdigest()==schema[name]['sha256'],'selected_source_array_pin')
            selected[name]=value
    ranges=[]
    for master in range(len(selected['master_identity'])):
        rows=selected['master_shell_aliases'][selected['master_shell_aliases'][:,0]==master]
        require(len(rows)>0,'source_missing_alias')
        values=selected['shell_thickness'][rows[:,1],:4]
        require(np.isfinite(values).all(),'master_thickness_missing')
        ranges.append((binary(np.min(values)),binary(np.max(values))))
    return selected,ranges


def verify_geometry(record,source,master_ranges):
    bits=record['result']['bits'];epsilon=fraction(record['result']['epsilon_exact']);result={}
    for item in record['result']['geometry_certificates']:
        setting=item['setting'];master=item['master_index'];key=(setting,item['CID'],master)
        require(key not in result,'duplicate_geometry_key')
        originals=tuple(tuple(binary(v) for v in p) for p in source['node_xyz'][source['master_node_indices'][master]])
        retained=tuple(tuple(fraction(v) for v in p) for p in item['original_corners'])
        same(originals,retained,'source_original_corners')
        e=binary((1.,1.006,1.025)[setting]);corners=weighted_corners(originals,e)
        same(corners,tuple(tuple(fraction(v) for v in p) for p in item['extended_corners']),'exact_extended_corners')
        diag=min(distance_squared(originals[0],originals[2]),distance_squared(originals[1],originals[3]))
        same(diag,fraction(item['original_diagonal_squared']),'original_diagonal_squared')
        same(tuple(map(fraction,item['master_thickness'])),master_ranges[master],'master_thickness_alias_range')
        radius=fraction(item['broad_phase']['global_slab_radius']);upper=fraction(item['broad_phase']['global_high_upper'])
        same(radius,upper+epsilon,'broad_phase_saved_epsilon')
        mixed=tuple(corners[0][j]-corners[1][j]+corners[2][j]-corners[3][j] for j in range(3))
        w_squared=sum((x*x for x in mixed),Fraction(0))/16
        result[key]=(diag,w_squared,master_ranges[master],corners)
    require(len(result)==3*len(source['master_identity']),'complete_geometry_coverage')
    return result


def verify_pairs(record,arrays,geometry,source):
    bits=record['result']['bits'];epsilon=fraction(record['result']['epsilon_exact']);certificates=record['result']['pair_certificates']
    require(len(certificates)==len(arrays['identities']),'all_pair_certificate_coverage')
    sqrt_checks=0;threshold_checks=0
    for row,item,projections in zip(arrays['identities'],certificates,arrays['projection_flags']):
        same(item['key'],list(map(int,row[[0,1,2,5]])),'proof_identity')
        node=int(row[4]);master=int(row[2]);setting=int(row[0]);cid=int(row[1])
        same(int(row[5]),int(source['node_ids'][node]),'proof_NID')
        same(list(map(int,row[6:8])),[int(source['node_source'][node]),int(source['node_line'][node])],'proof_node_locator')
        same(list(map(int,row[8:12])),list(map(int,source['master_identity'][master])),'proof_master_locator')
        same(tuple(map(fraction,item['slave_coordinate'])),tuple(binary(v) for v in source['node_xyz'][node]),'proof_source_coordinate')
        raw=(source['node_local_corner_thickness_min'][node],source['node_local_corner_thickness_max'][node])
        if np.isnan(raw).all():require(item['slave_supplied_thickness'] is None,'unknown_preserved');slave=None
        else:
            slave=tuple(binary(v) for v in raw);same(tuple(map(fraction,item['slave_supplied_thickness'])),slave,'proof_source_thickness')
        certificate=item['certificate'];intervals={}
        for name in ('dA','dB','w'):
            intervals[name]=interval(certificate[name]);valid_sqrt(fraction(certificate[name+'_squared']),intervals[name],bits);sqrt_checks+=1
        diag,w_squared,master_range,corners=geometry[(setting,cid,master)]
        same(fraction(certificate['w_squared']),w_squared,'w_squared_exact_geometry')
        lower=max(Fraction(0),intervals['dA'][0]-intervals['w'][1],intervals['dB'][0]-intervals['w'][1])
        upper=min(intervals['dA'][1]+intervals['w'][1],intervals['dB'][1]+intervals['w'][1])
        patch=interval(certificate['patch_enclosure']);same(patch,(lower,upper),'patch_combination')
        if slave is None:require(certificate['thresholds'] is None,'unknown_threshold_preserved');threshold=None
        else:
            roots=independent_root_bounds(diag,bits)
            threshold=tuple((max(binary(.6)*(slave[j]+master_range[j]),binary(.05)*roots[0]),
                             max(binary(.6)*(slave[j]+master_range[j]),binary(.05)*roots[1])) for j in (0,1))
            same(tuple(map(interval,certificate['thresholds'])),threshold,'source_threshold_exact');threshold_checks+=2
        cls=classified(patch,threshold,epsilon)
        same(cls,certificate['class'],'certificate_classification');same(cls,int(row[12]),'array_classification')
        same(certificate['projection_flags'],list(map(int,projections)),'array_projection')
        # Exact AABB scalar is independently recombined from the source point and rational patch corners.
        point=tuple(binary(v) for v in source['node_xyz'][node]);box=Fraction(0)
        for j in range(3):
            lo=min(p[j] for p in corners);hi=max(p[j] for p in corners)
            gap=max(lo-point[j],point[j]-hi,Fraction(0));box+=gap*gap
        same(box,fraction(certificate['aabb_squared']),'exact_box_certificate')
        if threshold is not None:require(box<=(threshold[1][1]+epsilon)**2,'admission_certificate')
        for projection,signed in zip(certificate['projection_flags'],certificate['signed_plane_enclosures']):
            require(projection in (-1,0,1),'projection_domain')
            require((signed is None)==(projection==-1),'degenerate_projection_undefined')
            if signed is not None:interval(signed)
    return {'rows':len(certificates),'exact_sqrt_certificates':sqrt_checks,'threshold_intervals':threshold_checks}


def precision_comparison():
    records=[json.loads((BASE/name).read_text()) for name in ('independent-exact80-02.json','independent-exact120-01.json')]
    require([r['result']['bits'] for r in records]==[80,120],'fixed_precisions')
    source,master_ranges=source_arrays();arrays=[load_arrays(r) for r in records]
    require(set(arrays[0])==set(arrays[1]),'precision_array_coverage');slots=0
    for key,value in arrays[0].items():
        require(value.dtype==arrays[1][key].dtype and np.array_equal(value,arrays[1][key],equal_nan=True),'precision_array_mismatch_'+key);slots+=value.size
    verification=[]
    for record,a in zip(records,arrays):
        geometry=verify_geometry(record,source,master_ranges);verification.append(verify_pairs(record,a,geometry,source))
    nested_count=0
    for coarse,fine in zip(records[0]['result']['pair_certificates'],records[1]['result']['pair_certificates']):
        same(coarse['key'],fine['key'],'precision_pair_order')
        for key in ('slave_coordinate','slave_supplied_thickness'):same(coarse[key],fine[key],'precision_source_'+key)
        c=coarse['certificate'];f=fine['certificate']
        for key in ('class','dA_squared','dB_squared','w_squared','projection_flags','aabb_squared'):same(c[key],f[key],'exact_precision_invariant_'+key)
        for key in ('dA','dB','w','patch_enclosure'):
            nested(interval(c[key]),interval(f[key]));nested_count+=1
        if c['thresholds'] is None:same(f['thresholds'],None,'precision_unknown')
        else:
            for x,y in zip(c['thresholds'],f['thresholds']):nested(interval(x),interval(y));nested_count+=1
        for x,y in zip(c['signed_plane_enclosures'],f['signed_plane_enclosures']):
            if x is None:same(y,None,'precision_undefined_plane')
            else:nested(interval(x),interval(y));nested_count+=1
    for c,f in zip(records[0]['result']['geometry_certificates'],records[1]['result']['geometry_certificates']):
        for key in ('setting','CID','master_index','original_corners','extended_corners','master_thickness','original_diagonal_squared'):same(c[key],f[key],'precision_geometry_invariant_'+key)
        for key in ('global_high_upper','global_slab_radius'):require(fraction(f['broad_phase'][key])<=fraction(c['broad_phase'][key]),'precision_broad_bound_nesting')
    return {'status':'PASS','exact_arrays':len(arrays[0]),'array_slots_compared':slots,'pair_certificates_per_precision':verification,
      'nested_pair_intervals':nested_count,'geometry_records_per_precision':len(records[0]['result']['geometry_certificates']),
      'full_population_pairs':sum(item['full_population_pairs'] for item in records[0]['result']['summaries']),
      'summaries':records[0]['result']['summaries'],'float_mask_comparison':records[0]['result']['float_admission_comparison_independent_only'],
      'scope':'Post-freeze internal certificate/source validation and complete 80/120 precision comparison. Cross-implementation exact comparison is separate; this does not independently rederive triangle distances from new source data.'}


def controls():
    passed=[]
    def check(name,ok):require(ok,'control_'+name);passed.append(name)
    def rejects(name,fn):
        try:fn()
        except Disagreement:passed.append(name);return
        raise Disagreement('missed_control_'+name)
    check('canonical_fraction',fraction(['-1','2'])==Fraction(-1,2))
    rejects('noncanonical_fraction_rejected',lambda:fraction(['2','4']))
    rejects('zero_denominator_rejected',lambda:fraction(['1','0']))
    rejects('inverted_interval_rejected',lambda:interval([['2','1'],['1','1']]))
    valid_sqrt(Fraction(2),independent_root_bounds(Fraction(2),80),80);passed.append('valid_exact_root_bounds')
    rejects('bad_root_lower_rejected',lambda:valid_sqrt(Fraction(2),(Fraction(3,2),Fraction(3,2)),80))
    rejects('bad_root_upper_rejected',lambda:valid_sqrt(Fraction(4),(Fraction(2),Fraction(2)+Fraction(1,1<<80)),80))
    rejects('nonnested_interval_rejected',lambda:nested((Fraction(0),Fraction(1)),(Fraction(-1),Fraction(1))))
    check('unknown_priority',classified((Fraction(100),Fraction(100)),None,Fraction(0))==0)
    threshold=((Fraction(1),Fraction(1)),(Fraction(2),Fraction(2)))
    check('strict_low_endpoint_unresolved',classified((Fraction(1),Fraction(1)),threshold,Fraction(0))==2)
    check('strict_high_endpoint_unresolved',classified((Fraction(2),Fraction(2)),threshold,Fraction(0))==2)
    check('inside_and_outside',classified((Fraction(0),Fraction(0)),threshold,Fraction(0))==3 and classified((Fraction(3),Fraction(3)),threshold,Fraction(0))==1)
    rejects('identity_mismatch_rejected',lambda:same([1,2],[2,1],'identity'))
    rejects('class_mismatch_rejected',lambda:same(2,3,'class'))
    return passed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');parser.add_argument('--output',default='independent-exact-precision01.json');args=parser.parse_args()
    started=time.monotonic();test=controls()
    if args.selftest:print(json.dumps({'status':'PASS','count':len(test),'controls':test}));return
    target=BASE/args.output;require(target.parent.resolve()==BASE and re.fullmatch(r'independent-exact-precision[a-z0-9-]+\.json',target.name),'output_scope')
    require(not target.exists(),'existing_output');before={}
    try:
        before=pins();result=precision_comparison();after=pins();require(before==after,'changed_inputs');require(peak()<=MEMORY_CAP,'memory_cap')
        receipt={'status':'PASS','command':sys.argv,'seconds':time.monotonic()-started,'peak_bytes':peak(),'pins_before':before,'pins_after':after,
          'controls':test,'result':result}
    except Exception as exc:
        receipt={'status':'FAIL','code':str(exc) if isinstance(exc,Disagreement) else type(exc).__name__,'command':sys.argv,
          'seconds':time.monotonic()-started,'peak_bytes':peak(),'pins_before':before,'controls':test}
    with target.open('x') as handle:json.dump(receipt,handle,indent=2,sort_keys=True,allow_nan=False);handle.write('\n')
    print(json.dumps({'status':receipt['status'],'output':target.name,'sha256':sha(target),'seconds':receipt['seconds'],'peak_bytes':receipt['peak_bytes'],'controls':len(test)}))
    if receipt['status']!='PASS':raise SystemExit(1)


if __name__=='__main__':main()
