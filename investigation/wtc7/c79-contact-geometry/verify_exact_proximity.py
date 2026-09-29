#!/usr/bin/env python3
"""Independent exact-binary-rational geometry verification core.

Frozen before inspection of the separate exact producer or its certificates.
No root routine is imported. Gram projection, exact segment clamping and
integer square-root enclosures independently reconstruct the geometry.
Source inputs are parsed binary64 values, not original decimal lexemes.
"""
import argparse
from fractions import Fraction as F
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
METHOD_SHA='b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89'
TRIS=((0,1,2),(0,2,3),(0,1,3),(1,2,3))
PINS={'EXACT-ARITHMETIC-ADDENDUM.md':METHOD_SHA,
 'GEOMETRIC-METHOD.md':'73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e',
 'GEOMETRIC-IMPLEMENTATION-ADDENDUM.md':'ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd',
 'independent-stage01.json':'ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd',
 'independent-stage01.npz':'fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5',
 'independent-proximity01.json':'cc50ea1607ee4875610fdd7cdae62e22dc5e423eb776842849f1e6199217543c',
 'independent-proximity01.npz':'26a9c9421e37c38e96e7568bb0521763b0cd0e621a12e7e101f8a9b411a2bef5'}
SETTINGS=(1.,1.006,1.025)
MEMORY_CAP=768*1024**2
SECONDS_CAP=900
ROW_CAP=1000000
PROGRESS=[]


class ExactError(Exception):pass


def require(ok,code):
    if not ok:raise ExactError(code)


def sha(path):
    with path.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()


def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)


def pins():
    actual={name:sha(BASE/name) for name in PINS};require(actual==PINS,'input_pin')
    actual['code']=sha(Path(__file__));return actual


def guard_new(paths):require(not any(path.exists() for path in paths),'existing_output')


def rational_float(value):
    value=float(value);require(math.isfinite(value),'nonfinite_binary_input')
    return F(*value.as_integer_ratio())


def vector(values):return tuple(rational_float(v) for v in values)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def rational_patch(q,u,v):
    mixed=add(sub(q[0],q[1]),sub(q[2],q[3]))
    return add(add(q[0],mul(sub(q[1],q[0]),u)),add(mul(sub(q[3],q[0]),v),mul(mixed,u*v)))


def extended_quad(original,e):
    h=(e-1)/2
    return tuple(rational_patch(original,u,v) for u,v in ((-h,-h),(1+h,-h),(1+h,1+h),(-h,1+h)))


def edge_squared(point,a,b):
    edge=sub(b,a);ap=sub(point,a);length2=dot(edge,edge)
    if length2==0:return dot(ap,ap)
    projection=dot(ap,edge)
    if projection<=0:return dot(ap,ap)
    if projection>=length2:
        bp=sub(point,b);return dot(bp,bp)
    return dot(ap,ap)-projection*projection/length2


def triangle_squared(point,a,b,c):
    """Exact Gram-system barycentric projection; closed edges remain candidates."""
    u=sub(b,a);v=sub(c,a);p=sub(point,a)
    uu=dot(u,u);uv=dot(u,v);vv=dot(v,v);up=dot(u,p);vp=dot(v,p)
    determinant=uu*vv-uv*uv;require(determinant>=0,'negative_Gram_determinant')
    squared=min(edge_squared(point,a,b),edge_squared(point,b,c),edge_squared(point,c,a))
    if determinant==0:return {'squared_distance':squared,'projection':-1,'signed_plane_squared':None,'plane_sign':None}
    beta=(vv*up-uv*vp)/determinant;gamma=(uu*vp-uv*up)/determinant
    inside=beta>=0 and gamma>=0 and beta+gamma<=1
    perpendicular=sub(p,add(mul(u,beta),mul(v,gamma)))
    plane_squared=dot(perpendicular,perpendicular)
    if inside:squared=min(squared,plane_squared)
    oriented=dot(p,cross(u,v));sign=(oriented>0)-(oriented<0)
    require(squared>=0 and plane_squared>=0,'negative_exact_squared_distance')
    return {'squared_distance':squared,'projection':int(inside),'signed_plane_squared':plane_squared,'plane_sign':sign}


def sqrt_enclosure(value,bits):
    require(isinstance(value,F) and value>=0 and isinstance(bits,int) and bits>0,'sqrt_input')
    numerator=value.numerator<<(2*bits);denominator=value.denominator
    n=math.isqrt(numerator//denominator);scale=1<<bits
    lo=F(n,scale);hi=lo if n*n*denominator==numerator else F(n+1,scale)
    require(lo*lo<=value<=hi*hi,'sqrt_certificate_failed')
    return lo,hi


def outward_float(value,direction):
    require(direction in (-1,1),'outward_direction')
    result=float(value);require(math.isfinite(result),'outward_conversion_nonfinite')
    while (rational_float(result)>value if direction==-1 else rational_float(result)<value):
        result=float(np.nextafter(result,-math.inf if direction==-1 else math.inf))
        require(math.isfinite(result),'outward_adjustment_nonfinite')
    return result


def aabb_squared(point,corners):
    total=F(0)
    for axis in range(3):
        low=min(c[axis] for c in corners);high=max(c[axis] for c in corners)
        gap=low-point[axis] if point[axis]<low else point[axis]-high if point[axis]>high else F(0)
        total+=gap*gap
    return total


def threshold_enclosures(slave,master,diagonal_squared,bits):
    if slave is None:return None
    require(len(slave)==2 and slave[0]>=0 and slave[1]>=slave[0] and len(master)==2 and master[0]>=0 and master[1]>=master[0],'thickness_ranges')
    diagonal=sqrt_enclosure(diagonal_squared,bits);scale=rational_float(.05);factor=rational_float(.6)
    return tuple((max(factor*(slave[j]+master[j]),scale*diagonal[0]),
                  max(factor*(slave[j]+master[j]),scale*diagonal[1])) for j in (0,1))


def exact_pair(point,original,extension,slave,master,epsilon,bits):
    q=extended_quad(original,extension);triangles=[triangle_squared(point,*[q[k] for k in indices]) for indices in TRIS]
    da2=min(t['squared_distance'] for t in triangles[:2]);db2=min(t['squared_distance'] for t in triangles[2:])
    mixed=add(sub(q[0],q[1]),sub(q[2],q[3]));w2=dot(mixed,mixed)/16
    a=sqrt_enclosure(da2,bits);b=sqrt_enclosure(db2,bits);w=sqrt_enclosure(w2,bits)
    lower=max(F(0),a[0]-w[1],b[0]-w[1]);upper=min(a[1]+w[1],b[1]+w[1])
    require(lower<=upper,'exact_enclosure_inverted')
    diag2=min(dot(sub(original[2],original[0]),sub(original[2],original[0])),dot(sub(original[3],original[1]),sub(original[3],original[1])))
    threshold=threshold_enclosures(slave,master,diag2,bits)
    cls=0 if threshold is None else 3 if upper<threshold[0][0]-epsilon else 1 if lower>threshold[1][1]+epsilon else 2
    signed=[]
    for t in triangles:
        if t['signed_plane_squared'] is None:signed.append(None)
        else:
            interval=sqrt_enclosure(t['signed_plane_squared'],bits)
            signed.append(tuple(-v for v in reversed(interval)) if t['plane_sign']<0 else interval)
    return {'class':cls,'dA_squared':da2,'dB_squared':db2,'w_squared':w2,'diagonal_squared':diag2,
        'dA':a,'dB':b,'w':w,'patch_enclosure':(lower,upper),'thresholds':threshold,
        'projection_flags':tuple(t['projection'] for t in triangles),'signed_plane_enclosures':tuple(signed),
        'aabb_squared':aabb_squared(point,q),'extended_corners':q}


def encode_fraction(value):return [str(value.numerator),str(value.denominator)]


def encode_exact(value):
    if isinstance(value,F):return encode_fraction(value)
    if isinstance(value,dict):return {k:encode_exact(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode_exact(v) for v in value]
    require(value is None or isinstance(value,(str,int,bool)),'non_exact_proof_value')
    return value


def original_diagonal_squared(corners):
    return min(dot(sub(corners[j],corners[i]),sub(corners[j],corners[i])) for i,j in ((0,2),(1,3)))


def population_index(points,unknown):
    require(points.ndim==2 and points.shape[1]==3 and np.isfinite(points).all(),'population_coordinates')
    require(unknown.shape==(len(points),) and unknown.dtype.kind=='b','population_unknown_schema')
    known=np.flatnonzero(~unknown)
    return [(known[np.argsort(points[known,axis],kind='stable')],
             np.sort(points[known,axis],kind='stable')) for axis in range(3)]


def packed_difference_counts(first,second):
    require(first.dtype==second.dtype==np.dtype('uint8') and first.shape==second.shape,'packed_comparison_schema')
    lookup=np.asarray([i.bit_count() for i in range(256)],dtype=np.uint8);added=removed=0
    # At most one final-axis row is expanded to byte-popcounts, never full bits.
    for a,b in zip(first.reshape(-1,first.shape[-1]),second.reshape(-1,second.shape[-1])):
        added+=int(lookup[a & ~b].sum());removed+=int(lookup[b & ~a].sum())
    return added,removed


def slab_indices(points,index,corners,radius,cache):
    """Outward float search followed by exact slab membership, never rounded inward."""
    bounds=[(min(p[axis] for p in corners)-radius,max(p[axis] for p in corners)+radius) for axis in range(3)]
    selection=None
    for axis,(low,high) in enumerate(bounds):
        order,values=index[axis]
        left=np.searchsorted(values,outward_float(low,-1),side='left')
        right=np.searchsorted(values,outward_float(high,1),side='right')
        items=order[left:right]
        selection=np.sort(items) if selection is None else np.intersect1d(selection,items,assume_unique=True)
    retained=[]
    for local in selection:
        local=int(local)
        if local not in cache:cache[local]=vector(points[local])
        p=cache[local]
        if all(low<=p[axis]<=high for axis,(low,high) in enumerate(bounds)):retained.append(local)
    return np.asarray(retained,dtype=np.int64)


def exact_broadphase(points,index,unknown,slave_ranges,corners,master_range,diagonal_squared,epsilon,bits,cache):
    known=np.flatnonzero(~unknown)
    require(len(known)>0,'no_known_population_thickness')
    maximum=rational_float(np.max(slave_ranges[known,1]))
    global_threshold=threshold_enclosures((maximum,maximum),master_range,diagonal_squared,bits)[1][1]
    slab=slab_indices(points,index,corners,global_threshold+epsilon,cache)
    kept=[];threshold_cache={};straddling=0
    for local in slab:
        local=int(local);thickness_key=tuple(float(v) for v in slave_ranges[local])
        if thickness_key not in threshold_cache:threshold_cache[thickness_key]=threshold_enclosures(vector(thickness_key),master_range,diagonal_squared,bits)
        threshold=threshold_cache[thickness_key][1]
        distance2=aabb_squared(cache[local],corners)
        if distance2<=(threshold[1]+epsilon)**2:
            kept.append(local)
            if distance2>(threshold[0]+epsilon)**2:straddling+=1
    mask=np.zeros(len(points),dtype=bool);mask[kept]=True;mask[unknown]=True
    return mask,{'known_slab_count':len(slab),'known_box_count':len(kept),'box_interval_straddles':straddling,
                 'global_high_upper':global_threshold,'global_slab_radius':global_threshold+epsilon}


def load_source():
    """Own extraction arrays; no root helper or new original-source read."""
    stage=json.loads((BASE/'independent-stage01.json').read_text())
    require(stage['receipt']['status']=='PASS','source_status')
    require(stage['receipt']['array_file_sha256']==PINS['independent-stage01.npz'],'source_archive_reference')
    schema=stage['receipt']['array_schema'];arrays={}
    retain={'node_ids','node_xyz','node_source','node_line','node_present','population_flags',
      'node_local_corner_thickness_min','node_local_corner_thickness_max','node_family_incidence',
      'master_identity','master_node_ids','master_node_indices','master_shell_aliases',
      'shell_identity','shell_connectivity','shell_thickness','node_part_family_counts'}
    with np.load(BASE/'independent-stage01.npz',allow_pickle=False) as source:
        require(set(source.files)==set(schema) and retain<=set(source.files),'source_array_coverage')
        for key in source.files:
            value=source[key];spec=schema[key]
            require(value.dtype.kind in 'biuf' and value.dtype.str==spec['dtype'] and list(value.shape)==spec['shape'],'source_array_schema')
            require(hashlib.sha256(value.tobytes(order='C')).hexdigest()==spec['sha256'],'source_array_hash')
            if key in retain:arrays[key]=value
    require(arrays['node_present'].all() and np.isfinite(arrays['node_xyz']).all(),'complete_source_coordinates')
    require(np.all(np.diff(arrays['node_ids'])>0),'node_order')
    thickness=np.column_stack([arrays['node_local_corner_thickness_min'],arrays['node_local_corner_thickness_max']])
    unknown=np.isnan(thickness).all(axis=1)
    require(np.array_equal(unknown,arrays['node_family_incidence'][:,0]==0),'unknown_requires_no_shell')
    require(np.array_equal(np.isnan(thickness).any(axis=1),unknown),'partial_missing_thickness')
    require(np.isfinite(thickness[~unknown]).all() and np.all(thickness[~unknown]>=0) and np.all(thickness[~unknown,0]<=thickness[~unknown,1]),'invalid_source_thickness')
    master_ranges=[];master_parts=[];aliases=[]
    for master,nodes in enumerate(arrays['master_node_ids']):
        matches=arrays['master_shell_aliases'][arrays['master_shell_aliases'][:,0]==master]
        require(len(matches)>0,'missing_master_alias');values=[];parts=set()
        for _,shell,ordered in matches:
            connectivity=arrays['shell_connectivity'][shell,2:6]
            require(sorted(connectivity)==sorted(nodes),'alias_node_multiset')
            require(bool(ordered)==np.array_equal(connectivity,nodes),'alias_order_flag')
            ts=arrays['shell_thickness'][shell,:4]
            require(np.isfinite(ts).all() and np.all(ts>=0),'master_supplied_thickness')
            values.extend(float(v) for v in ts);parts.add(int(arrays['shell_identity'][shell,5]))
            aliases.append([master,*map(int,arrays['shell_identity'][shell]),int(ordered)])
        master_ranges.append((min(values),max(values)));master_parts.append(parts)
    require(np.array_equal(arrays['node_ids'][arrays['master_node_indices']],arrays['master_node_ids']),'master_node_indices')
    saved=json.loads((BASE/'independent-proximity01.json').read_text())
    epsilon=float(saved['result']['epsilon'])
    require(epsilon==1e-10*max(1.,float(np.max(np.abs(arrays['node_xyz'])))),'saved_epsilon_definition')
    return {'ids':arrays['node_ids'],'xyz':arrays['node_xyz'],
      'source_line':np.column_stack([arrays['node_source'],arrays['node_line']]),'flags':arrays['population_flags'],
      'thickness':thickness,'unknown':unknown,'nodeparts':arrays['node_part_family_counts'],
      'master_identity':arrays['master_identity'],'master_nodes':arrays['master_node_ids'],
      'master_coords':arrays['node_xyz'][arrays['master_node_indices']],
      'master_ranges':np.asarray(master_ranges),'master_parts':master_parts,'alias_identity':np.asarray(aliases,dtype=np.int64),
      'epsilon':epsilon,'part_references':stage['result']['part_references']}


def compute_source(data,bits):
    start=time.monotonic();epsilon=rational_float(data['epsilon']);mcount=len(data['master_identity'])
    populations={cid:np.flatnonzero((data['flags']&flag)!=0) for cid,flag in ((1,1),(2,2))}
    master_groups={cid:np.flatnonzero(data['master_identity'][:,1]==sid) for cid,sid in ((1,1),(2,3))}
    require(sum(len(v) for v in master_groups.values())==mcount,'master_group_coverage')
    masks={cid:np.zeros((3,len(master_groups[cid]),(len(populations[cid])+7)//8),dtype=np.uint8) for cid in (1,2)}
    counts=np.zeros((3,mcount,12),dtype=np.int64);rows=[];flags=[];proof=[];geometries=[];progress_count=0
    nodeparts={int(n):[] for n in np.unique(data['nodeparts'][:,0])}
    for n,p,f,c in data['nodeparts']:nodeparts[int(n)].append((int(p),int(f),int(c)))
    for cid in (1,2):
        pop=populations[cid];points=data['xyz'][pop];unknown=data['unknown'][pop];thickness=data['thickness'][pop]
        index=population_index(points,unknown);point_cache={};known_count=int((~unknown).sum());unknown_count=int(unknown.sum())
        for local_master,master in enumerate(master_groups[cid]):
            master=int(master);original=tuple(vector(v) for v in data['master_coords'][master]);master_range=vector(data['master_ranges'][master])
            diag2=original_diagonal_squared(original)
            for setting,e in enumerate(SETTINGS):
                extension=rational_float(e);corners=extended_quad(original,extension)
                mask,broad=exact_broadphase(points,index,unknown,thickness,corners,master_range,diag2,epsilon,bits,point_cache)
                local_indices=np.flatnonzero(mask);classes=[]
                masks[cid][setting,local_master]=np.packbits(mask,bitorder='little')
                geometry={'setting':setting,'CID':cid,'master_index':master,'original_corners':original,'extended_corners':corners,
                  'master_thickness':master_range,'original_diagonal_squared':diag2,'broad_phase':broad}
                geometries.append(encode_exact(geometry))
                for local in local_indices:
                    local=int(local);node=int(pop[local]);nid=int(data['ids'][node])
                    if local not in point_cache:point_cache[local]=vector(points[local])
                    slave=None if unknown[local] else vector(thickness[local])
                    result=exact_pair(point_cache[local],original,extension,slave,master_range,epsilon,bits)
                    same_node=nid in data['master_nodes'][master]
                    same_part=any(p in data['master_parts'][master] for p,_,_ in nodeparts[node])
                    row=[setting,cid,master,local,node,nid,*map(int,data['source_line'][node]),*map(int,data['master_identity'][master]),result['class'],int(same_node),int(same_part)]
                    rows.append(row);flags.append(result['projection_flags']);classes.append(result['class'])
                    result.pop('extended_corners');result.pop('diagonal_squared')
                    proof.append({'key':[setting,cid,master,nid],'slave_coordinate':encode_exact(point_cache[local]),
                                  'slave_supplied_thickness':encode_exact(slave),'certificate':encode_exact(result)})
                    require(len(rows)<=ROW_CAP,'row_cap')
                classcounts=np.bincount(classes,minlength=4)
                counts[setting,master]=[len(pop),known_count,unknown_count,broad['known_slab_count'],broad['known_box_count'],
                  len(local_indices),len(pop)-len(local_indices),*map(int,classcounts),broad['box_interval_straddles']]
                progress_count+=1
                if progress_count%100==0:
                    require(peak()<=MEMORY_CAP,'memory_cap');require(time.monotonic()-start<=SECONDS_CAP,'compute_time_cap')
            if local_master%100==0:PROGRESS.append({'CID':cid,'last_complete_master_local':local_master})
        PROGRESS.append({'CID':cid,'complete':True})
    arrays={'identities':np.asarray(rows,dtype=np.int64),'projection_flags':np.asarray(flags,dtype=np.int8),'coverage':counts,
      'CID1_admission_bits':masks[1],'CID2_admission_bits':masks[2],
      'CID1_population_indices':populations[1],'CID2_population_indices':populations[2],
      'CID1_master_indices':master_groups[1],'CID2_master_indices':master_groups[2],
      'master_source_identity':data['master_identity'],'master_node_ids':data['master_nodes'],'master_alias_identity':data['alias_identity']}
    require(arrays['identities'].shape==(len(proof),15),'identity_schema')
    summaries=[]
    for cid in (1,2):
        for setting in range(3):
            selected=arrays['identities'][(arrays['identities'][:,0]==setting)&(arrays['identities'][:,1]==cid)]
            nodes=np.unique(selected[:,4]);parts=sorted({p for n in nodes for p,_,_ in nodeparts[int(n)]})
            summaries.append({'CID':cid,'setting':setting,'extension_exact':encode_fraction(rational_float(SETTINGS[setting])),
              'full_population_pairs':len(populations[cid])*len(master_groups[cid]),'admitted_rows':len(selected),
              'unique_nodes':len(nodes),'parts':parts,'class_counts':np.bincount(selected[:,12],minlength=4).tolist(),
              'same_node_count':int(selected[:,13].sum()),'same_part_count':int(selected[:,14].sum())})
    # Same input populations, but this check does not presume float admission correctness.
    floating_difference={}
    with np.load(BASE/'independent-proximity01.npz',allow_pickle=False) as prior:
        for cid in (1,2):
            exact=masks[cid];old=prior[f'CID{cid}_admission_bits'];require(exact.shape==old.shape,'floating_mask_shape')
            added,removed=packed_difference_counts(exact,old)
            floating_difference[str(cid)]={'exact_only':added,'floating_only':removed}
    validate_output(arrays,proof)
    return arrays,{'bits':bits,'epsilon_exact':encode_fraction(epsilon),'summaries':summaries,
      'float_admission_comparison_independent_only':floating_difference,'geometry_certificates':geometries,'pair_certificates':proof,
      'part_references':data['part_references'],'source_scope':'Frozen independently extracted binary64 source arrays; no raw source reread.',
      'meaning':'Certified arithmetic within the declared geometric surrogate on exact parsed binary values; not contact initialization, physical restraint, capacity or cause.'}


def validate_output(arrays,proof):
    rows=arrays['identities'];require(len(rows)==len(proof) and len(rows)==len(arrays['projection_flags']),'proof_row_coverage')
    require(len({tuple(row[[0,1,2,5]]) for row in rows})==len(rows),'duplicate_pair_identity')
    for row,item in zip(rows,proof):require(list(map(int,row[[0,1,2,5]]))==item['key'],'proof_row_identity')
    for cid in (1,2):
        pop=arrays[f'CID{cid}_population_indices'];masters=arrays[f'CID{cid}_master_indices']
        for setting in range(3):
            for local,master in enumerate(masters):
                mask=np.unpackbits(arrays[f'CID{cid}_admission_bits'][setting,local],bitorder='little')
                require(not mask[len(pop):].any(),'nonzero_padding')
                selected=rows[(rows[:,0]==setting)&(rows[:,1]==cid)&(rows[:,2]==master)]
                require(np.array_equal(np.flatnonzero(mask[:len(pop)]),selected[:,3]),'mask_pair_bijection')
                require(np.array_equal(pop[selected[:,3]],selected[:,4]),'population_identity')
                require(len(selected)==arrays['coverage'][setting,master,5],'coverage_admission')
                require(np.array_equal(np.bincount(selected[:,12],minlength=4),arrays['coverage'][setting,master,7:11]),'coverage_classes')


def array_manifest(arrays):
    result={}
    for name,value in arrays.items():
        require(value.dtype.kind in 'biuf','array_non_numeric')
        result[name]={'dtype':value.dtype.str,'shape':list(value.shape),'bytes':value.nbytes,
                     'sha256':hashlib.sha256(value.tobytes(order='C')).hexdigest()}
    return result


def controls():
    passed=[]
    def check(name,value):require(value,'control_'+name);passed.append(name)
    check('binary_input_not_decimal_rational',rational_float(.1)!=F(1,10) and rational_float(.5)==F(1,2))
    for value in (F(0),F(4),F(1,4),F(2),F(1,3)):
        lo,hi=sqrt_enclosure(value,80);lo2,hi2=sqrt_enclosure(value,120)
        check('sqrt_'+str(value).replace('/','_'),lo*lo<=value<=hi*hi and lo<=lo2<=hi2<=hi)
    check('perfect_roots_exact',sqrt_enclosure(F(4),80)==(F(2),F(2)) and sqrt_enclosure(F(1,4),80)==(F(1,2),F(1,2)))
    for x in (F(1,10),F(-1,10),F(1,3),F(3,2),F(0)):
        check('outward_'+str(x).replace('/','_'),rational_float(outward_float(x,-1))<=x<=rational_float(outward_float(x,1)))
    tri=[vector([0,0,0]),vector([1,0,0]),vector([0,1,0])]
    for p,sq,inside in (([.25,.25,2],F(4),1),([.5,-.5,0],F(1,4),0),([-1,-1,0],F(2),0),([.5,0,0],F(0),1)):
        actual=triangle_squared(vector(p),*tri);reverse=triangle_squared(vector(p),tri[0],tri[2],tri[1])
        check('triangle_'+str(len(passed)),actual['squared_distance']==sq and actual['projection']==inside and reverse['squared_distance']==sq and reverse['projection']==inside)
    degenerate=triangle_squared(vector([.5,1,0]),tri[0],tri[1],tri[1])
    check('degenerate_plane_unknown_edges_exact',degenerate['squared_distance']==1 and degenerate['projection']==-1 and degenerate['signed_plane_squared'] is None)
    q=tuple(vector(v) for v in [[0,0,0],[1,0,0],[1,1,.25],[0,1,0]])
    point=rational_patch(q,F(1,3),F(2,5));eps=rational_float(1e-10)
    result=exact_pair(point,q,F(1),(F(1),F(1)),(F(1),F(1)),eps,80)
    check('known_warped_patch_zero_in_enclosure',result['patch_enclosure'][0]==0 and result['class']==3)
    unknown=exact_pair(vector([100,100,100]),q,F(1),None,(F(1),F(1)),eps,80)
    check('unknown_priority',unknown['class']==0 and unknown['thresholds'] is None)
    square=tuple(vector(v) for v in [[0,0,0],[1,0,0],[1,1,0],[0,1,0]])
    overlap=exact_pair(vector([.5,.5,.1]),square,F(1),(F(0),F(1)),(F(0),F(1)),eps,80)
    check('thickness_interval_unresolved',overlap['class']==2)
    extended=extended_quad(square,rational_float(1.025));p=vector([1.08,.5,0])
    threshold=threshold_enclosures((F(0),F(0)),(F(0),F(0)),F(2),80)[1][1]
    check('extended_domain_only_box_admission',aabb_squared(p,square)>threshold**2 and aabb_squared(p,extended)<=threshold**2)
    r80=exact_pair(vector([.3,.4,.5]),q,rational_float(1.006),(F(0),F(1)),(F(0),F(1)),eps,80)
    r120=exact_pair(vector([.3,.4,.5]),q,rational_float(1.006),(F(0),F(1)),(F(0),F(1)),eps,120)
    check('full_pair_enclosure_nesting',r80['patch_enclosure'][0]<=r120['patch_enclosure'][0]<=r120['patch_enclosure'][1]<=r80['patch_enclosure'][1])
    check('exact_squared_invariants_across_precision',all(r80[k]==r120[k] for k in ('dA_squared','dB_squared','w_squared','diagonal_squared','projection_flags','aabb_squared','extended_corners')))
    check('pin_mutation_detectable',hashlib.sha256(b'changed').hexdigest()!=hashlib.sha256(b'original').hexdigest())
    # Exercise the actual output-refusal guard, not merely a fixture classifier.
    with tempfile.TemporaryDirectory(prefix='independent-exact-control-') as temp:
        existing=Path(temp)/'existing';existing.touch();new=Path(temp)/'new'
        guard_new([new]);rejected=False
        try:guard_new([new,existing])
        except ExactError as exc:rejected=str(exc)=='existing_output'
        check('actual_create_only_guard',rejected and existing.exists() and not new.exists())
    points=np.asarray([[.5,.5,0.],[.5,.5,.08],[1.08,.5,0.],[10.,10.,10.],[.5,.5,.075],[.5,.5,-.075]])
    unknown=np.asarray([False,False,False,True,False,False]);ranges=np.zeros((6,2));ranges[unknown]=np.nan
    index=population_index(points,unknown);e2=rational_float(.01);master=(F(0),F(0))
    for factor in (1.,1.025):
        quad=extended_quad(square,rational_float(factor));cache={}
        admitted,broad=exact_broadphase(points,index,unknown,ranges,quad,master,F(2),e2,80,cache)
        expected=[]
        for local,p in enumerate(points):
            if unknown[local]:expected.append(True)
            else:
                threshold=threshold_enclosures((F(0),F(0)),master,F(2),80)[1][1]
                expected.append(aabb_squared(vector(p),quad)<=(threshold+e2)**2)
        check('unpruned_whole_population_'+str(factor),np.array_equal(admitted,expected) and admitted[3])
        repeat,_=exact_broadphase(points,index,unknown,ranges,quad,master,F(2),e2,80,{})
        check('duplicate_master_broadphase_'+str(factor),np.array_equal(admitted,repeat))
    buffered,_=exact_broadphase(points,index,unknown,ranges,square,master,F(2),e2,80,{})
    check('epsilon_band_kept_both_signs',bool(buffered[4]) and bool(buffered[5]))
    nonfinite=False
    try:rational_float(float('inf'))
    except ExactError:nonfinite=True
    check('nonfinite_binary_rejected',nonfinite)
    mask_a=np.arange(256,dtype=np.uint8).reshape(2,4,32);mask_b=np.flip(mask_a,axis=-1).copy()
    changes=packed_difference_counts(mask_a,mask_b)
    check('bounded_byte_popcount_equals_full_bits',changes==(int(np.unpackbits(mask_a & ~mask_b).sum()),int(np.unpackbits(mask_b & ~mask_a).sum())))
    return passed


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');parser.add_argument('--bits',type=int,choices=(80,120),default=80)
    parser.add_argument('--output',default='independent-exact80-01.json');args=parser.parse_args()
    started=time.monotonic();require(sha(BASE/'EXACT-ARITHMETIC-ADDENDUM.md')==METHOD_SHA,'method_pin');test=controls()
    if args.selftest:print(json.dumps({'status':'PASS','count':len(test),'controls':test}));return
    target=BASE/args.output;archive=target.with_suffix('.npz');failure=target.with_name(target.stem+'-failed.json')
    require(target.parent.resolve()==BASE and re.fullmatch(r'independent-exact(?:80|120)-[0-9]+\.json',target.name),'output_scope')
    guard_new([target,archive,failure]);before={}
    try:
        before=pins();data=load_source();arrays,result=compute_source(data,args.bits);manifest=array_manifest(arrays)
        require(before==pins(),'changed_inputs_or_code');require(peak()<=MEMORY_CAP,'memory_cap_before_save')
        with archive.open('xb') as handle:np.savez_compressed(handle,**arrays)
        with np.load(archive,allow_pickle=False) as saved:
            require(set(saved.files)==set(arrays),'saved_array_coverage')
            for key,value in arrays.items():require(np.array_equal(saved[key],value,equal_nan=True),'saved_array_roundtrip')
        after=pins();require(before==after,'changed_inputs_after_save')
        receipt={'status':'PASS','command':sys.argv,'seconds':time.monotonic()-started,'peak_bytes':peak(),
          'controls':test,'input_pins_before':before,'input_pins_after':after,'array_file':archive.name,'array_sha256':sha(archive),
          'array_schema':manifest,'bits':args.bits,'progress':PROGRESS,'numpy':np.__version__,
          'limits':{'compute_seconds':SECONDS_CAP,'memory_bytes':MEMORY_CAP,'admitted_rows':ROW_CAP},
          'identity_columns':['setting','CID','master_index','slave_local_index','node_global_index','NID','node_SRC','node_line','master_SRC','master_set_ID','master_line','master_membership_row','class','same_NID','same_PID'],
          'coverage_columns':['population','known','unknown','known_exact_slab','known_exact_box','admitted','excluded','class0','class1','class2','class3','box_interval_straddles'],
          'proof_fraction_encoding':'Every rational is [base10 numerator string, positive denominator string], exact canonical Fraction form.',
          'mask_encoding':'setting, master in CID frozen order, full slave in CID frozen order, little packed bit order, zero final padding.',
          'classes':{'0':'unknown supplied thickness','1':'certified outside high gate plus saved epsilon','2':'not certified class1 or3','3':'certified inside low gate minus saved epsilon'},
          'independence':'Own frozen source extraction; Gram barycentric projection and rational edge distances. No separate exact producer code or output inspected before this implementation and first results.'}
        require(peak()<=MEMORY_CAP,'memory_cap_final')
        with target.open('x') as handle:json.dump({'receipt':receipt,'result':result},handle,sort_keys=True,indent=2,allow_nan=False);handle.write('\n')
        print(json.dumps({'status':'PASS','output':target.name,'sha256':sha(target),'array_sha256':sha(archive),'controls':len(test),'seconds':receipt['seconds'],'peak_bytes':receipt['peak_bytes']}))
    except Exception as exc:
        record={'status':'FAIL','code':str(exc) if isinstance(exc,ExactError) else type(exc).__name__,'command':sys.argv,
          'seconds':time.monotonic()-started,'peak_bytes':peak(),'controls':test,'input_pins_before':before,'progress':PROGRESS,
          'result_exists':target.exists(),'array_exists':archive.exists()}
        try:record['input_pins_after']=pins()
        except Exception as later:record['after_pin_error']=str(later) if isinstance(later,ExactError) else type(later).__name__
        with failure.open('x') as handle:json.dump(record,handle,indent=2,sort_keys=True,allow_nan=False);handle.write('\n')
        print(json.dumps({'status':'FAIL','code':record['code'],'receipt':failure.name}));raise SystemExit(1) from None


if __name__=='__main__':main()
