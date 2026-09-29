#!/usr/bin/env python3
"""Independent, conditional bilinear-image geometry diagnostic, not contact."""
from array import array
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import sys
import time
import numpy as np

BASE=Path(__file__).resolve().parent
PINS={'GEOMETRIC-METHOD.md':'73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e',
 'GEOMETRIC-IMPLEMENTATION-ADDENDUM.md':'ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd',
 'PROTOCOL.md':'b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea',
 'independent-stage01.json':'ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd',
 'independent-stage01.npz':'fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5'}
SETTINGS=np.asarray([1.,1.006,1.025],dtype='<f8')
TRIANGLES=np.asarray([[0,1,2],[0,2,3],[0,1,3],[1,2,3]],dtype=np.int64)
MEMORY_CAP=768*1024**2
SECONDS_CAP=300
ADMITTED_CAP=1000000
PROGRESS=[]


class Rejected(Exception):
    def __init__(self,code):self.code=code;super().__init__(code)


def need(ok,code):
    if not ok:raise Rejected(code)


def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)


def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def pins():
    result={name:sha(BASE/name) for name in PINS}
    need(result==PINS,'input_pin');result['independent_proximity_code']=sha(Path(__file__))
    return result


def norm(x):return np.sqrt(np.sum(x*x,axis=-1))


def patch(corners,u,v):
    mixed=corners[0]-corners[1]+corners[2]-corners[3]
    return corners[0]+np.asarray(u)[...,None]*(corners[1]-corners[0])+np.asarray(v)[...,None]*(corners[3]-corners[0])+(np.asarray(u)*np.asarray(v))[...,None]*mixed


def segment_distance(points,a,b):
    edge=b-a;length2=np.dot(edge,edge)
    if length2==0:return norm(points-a)
    t=np.clip((points-a)@edge/length2,0.,1.)
    return norm(points-(a+t[:,None]*edge))


def triangle_query(points,a,b,c):
    """Voronoi closest-point algorithm; projection flags independently use a local orthogonal basis."""
    ab=b-a;ac=c-a;cross=np.cross(ab,ac);crossnorm=float(norm(cross))
    if crossnorm==0:
        distances=np.minimum.reduce([segment_distance(points,a,b),segment_distance(points,b,c),segment_distance(points,c,a)])
        return distances,np.full(len(points),np.nan),np.full(len(points),-1,dtype=np.int8)
    unit=cross/crossnorm;ap=points-a;bp=points-b;cp=points-c
    signed=ap@unit
    # Projection coordinates in the (AB, in-plane perpendicular-to-AB) basis.
    ablen=float(norm(ab));along=ab/ablen;across=np.cross(unit,along)
    acperp=float(np.dot(ac,across));need(acperp!=0,'nonzero_triangle_projection_rank_loss')
    gamma=(ap@across)/acperp;beta=((ap@along)-gamma*np.dot(ac,along))/ablen
    inside=((beta>=0)&(gamma>=0)&(beta+gamma<=1)).astype(np.int8)
    d1=ap@ab;d2=ap@ac;d3=bp@ab;d4=bp@ac;d5=cp@ab;d6=cp@ac
    va=d3*d6-d5*d4;vb=d5*d2-d1*d6;vc=d1*d4-d3*d2
    closest=np.empty_like(points);assigned=np.zeros(len(points),dtype=bool)
    def put(mask,value):
        mask=mask&~assigned
        if not mask.any():return
        closest[mask]=value(mask) if callable(value) else value;assigned[mask]=True
    put((d1<=0)&(d2<=0),a)
    put((d3>=0)&(d4<=d3),b)
    put((vc<=0)&(d1>=0)&(d3<=0),lambda m:a+(d1[m]/(d1[m]-d3[m]))[:,None]*ab)
    put((d6>=0)&(d5<=d6),c)
    put((vb<=0)&(d2>=0)&(d6<=0),lambda m:a+(d2[m]/(d2[m]-d6[m]))[:,None]*ac)
    put((va<=0)&(d4-d3>=0)&(d5-d6>=0),lambda m:b+((d4[m]-d3[m])/((d4[m]-d3[m])+(d5[m]-d6[m])))[:,None]*(c-b))
    remaining=~assigned;den=va+vb+vc
    need(np.all(den[remaining]!=0),'nonzero_triangle_closest_rank_loss')
    closest[remaining]=a+(vb[remaining]/den[remaining])[:,None]*ab+(vc[remaining]/den[remaining])[:,None]*ac
    distance=norm(points-closest);need(np.isfinite(distance).all() and np.isfinite(signed).all(),'triangle_nonfinite')
    return distance,signed,inside


def geometry(original,extension):
    h=(extension-1)/2.;u=np.asarray([-h,1+h,1+h,-h]);v=np.asarray([-h,-h,1+h,1+h])
    r=patch(original,u,v);mixed=r[0]-r[1]+r[2]-r[3]
    edge=norm(np.roll(r,-1,axis=0)-r)
    origdiag=norm(original[[2,3]]-original[[0,1]])
    extdiag=norm(r[[2,3]]-r[[0,1]])
    cross=[];crossnorm=[];units=[];near=[];areas=[]
    for tri in TRIANGLES:
        a,b,c=r[tri];raw=np.cross(b-a,c-a);length=float(norm(raw))
        maxedge2=max(float(np.dot(b-a,b-a)),float(np.dot(c-b,c-b)),float(np.dot(a-c,a-c)))
        cross.append(raw);crossnorm.append(length);areas.append(length/2)
        units.append(raw/length if length!=0 else np.full(3,np.nan))
        near.append(length<=64*np.finfo(float).eps*max(1.,maxedge2))
    units=np.asarray(units);crossnorm=np.asarray(crossnorm)
    def jac(s,t):return np.cross(r[1]-r[0]+t*mixed,r[3]-r[0]+s*mixed)
    centre=jac(.5,.5);corners=np.asarray([jac(s,t) for s,t in [(0,0),(1,0),(1,1),(0,1)]])
    cn=float(norm(centre));jn=norm(corners);dots=corners@centre
    cosine=np.full(4,np.nan);good=(jn>0)&(cn>0);cosine[good]=dots[good]/(jn[good]*cn)
    warnings=np.column_stack((jn==0,np.full(4,cn==0),dots==0,dots<0))
    return {'extended_corners':r,'edge_lengths':edge,'edge_exact_zero':edge==0,
       'original_diagonals':origdiag,'extended_diagonals':extdiag,'warp_bound':float(norm(mixed))/4.,
       'triangle_cross_products':np.asarray(cross),'triangle_cross_norms':crossnorm,'triangle_unit_normals':units,
       'triangle_areas':np.asarray(areas),'triangle_exact_zero':crossnorm==0,'triangle_near_zero':np.asarray(near,dtype=bool),
       'normal_dot_products':units@units.T,'jacobian_centre':centre,'jacobian_corners':corners,'jacobian_centre_norm':cn,
       'jacobian_corner_norms':jn,'jacobian_dot_centre':dots,'jacobian_cosine_centre':cosine,'jacobian_warnings':warnings}


def aabb_distance(points,corners):
    gap=np.maximum(0,np.maximum(corners.min(axis=0)-points,points-corners.max(axis=0)))
    distance=norm(gap);need(np.isfinite(distance).all(),'nonfinite_AABB_distance');return distance


def thresholds(slave_range,master_range,diagonal):
    need(np.all(np.isfinite(master_range)) and np.all(master_range>=0) and master_range[0]<=master_range[1],'invalid_master_thickness')
    unknown=np.isnan(slave_range).all(axis=1)
    need(np.all(unknown|np.isfinite(slave_range).all(axis=1)),'partially_unknown_slave_thickness')
    need(np.all(slave_range[~unknown]>=0) and np.all(slave_range[~unknown,0]<=slave_range[~unknown,1]),'invalid_slave_thickness')
    need(np.isfinite(diagonal) and diagonal>=0,'invalid_diagonal')
    delta=np.maximum(.60*(slave_range+master_range),.05*diagonal)
    need(np.isfinite(delta[~unknown]).all(),'nonfinite_known_threshold')
    return delta,unknown


def classify(lower,upper,delta,unknown,epsilon):
    need(np.isfinite(lower).all() and np.isfinite(upper).all() and np.isfinite(delta[~unknown]).all(),'nonfinite_known_bounds_or_threshold')
    inversion=lower>upper;need(np.all(lower<=upper+epsilon),'bilinear_enclosure_inversion_over_epsilon')
    classes=np.full(len(lower),2,dtype=np.int8)
    classes[(~unknown)&(lower>delta[:,1]+epsilon)]=1
    classes[(~unknown)&(upper<delta[:,0]-epsilon)]=3
    classes[inversion]=2
    classes[unknown]=0
    return classes,inversion


def admitted_query(points,g,delta,unknown,epsilon,unpruned=False):
    box=aabb_distance(points,g['extended_corners'])
    mask=np.ones(len(points),dtype=bool) if unpruned else unknown|(box<=delta[:,1]+epsilon)
    selected=points[mask];distances=[];signed=[];inside=[]
    for tri in TRIANGLES:
        d,s,f=triangle_query(selected,*g['extended_corners'][tri]);distances.append(d);signed.append(s);inside.append(f)
    distances=np.column_stack(distances);signed=np.column_stack(signed);inside=np.column_stack(inside)
    da=np.minimum(distances[:,0],distances[:,1]);db=np.minimum(distances[:,2],distances[:,3]);w=g['warp_bound']
    lower=np.maximum.reduce([np.zeros(len(selected)),da-w,db-w]);upper=np.minimum(da+w,db+w)
    classes,inversion=classify(lower,upper,delta[mask],unknown[mask],epsilon)
    numbers=np.column_stack((da,db,lower,upper,delta[mask],signed,box[mask]))
    return mask,numbers,inside,classes,inversion


NEEDED={'node_ids','node_xyz','node_source','node_line','node_present','population_flags','node_family_incidence',
 'node_local_corner_thickness_min','node_local_corner_thickness_max','node_part_family_counts',
 'master_identity','master_node_ids','master_node_indices','master_attributes','master_attribute_missing',
 'master_shell_aliases','shell_identity','shell_connectivity','shell_thickness','shell_thickness_missing'}


def load_frozen():
    receipt=json.loads((BASE/'independent-stage01.json').read_text());need(receipt['receipt']['status']=='PASS','stage_not_PASS')
    need(receipt['receipt']['array_file_sha256']==PINS['independent-stage01.npz'],'stage_archive_reference')
    schema=receipt['receipt']['array_schema'];a={}
    with np.load(BASE/'independent-stage01.npz',allow_pickle=False) as z:
        need(set(z.files)==set(schema) and NEEDED<=set(z.files),'stage_schema_coverage')
        for name in z.files:
            value=z[name];s=schema[name]
            need(value.dtype.kind in 'biuf' and list(value.shape)==s['shape'] and value.dtype.str==s['dtype'],'stage_array_schema')
            need(hashlib.sha256(value.tobytes(order='C')).hexdigest()==s['sha256'],'stage_array_pin')
            if name in NEEDED:a[name]=value
    need(np.isfinite(a['node_xyz']).all() and a['node_present'].all(),'selected_coordinate_coverage')
    nodeparts=a['node_part_family_counts'];need(np.all(np.diff(nodeparts[:,0])>=0),'nodepart_order')
    offsets=np.concatenate(([0],np.cumsum(np.bincount(nodeparts[:,0],minlength=len(a['node_ids'])))))
    masterrange=[];masterparts=[];aliasidentity=[];aliasnodes=[];aliasthic=[];aliasmissing=[]
    for midx in range(len(a['master_identity'])):
        matches=a['master_shell_aliases'][a['master_shell_aliases'][:,0]==midx]
        need(len(matches)>0,'missing_master_shell_alias');values=[];parts=set()
        for _,sidx,ordered in matches:
            identity=a['shell_identity'][sidx];thic=a['shell_thickness'][sidx]
            need(np.isfinite(thic[:4]).all() and np.all(thic[:4]>=0),'invalid_alias_THIC1to4')
            need(sorted(a['shell_connectivity'][sidx,2:6])==sorted(a['master_node_ids'][midx]),'master_alias_nodes')
            values.extend(thic[:4]);parts.add(int(identity[5]))
            aliasidentity.append([midx,*identity,int(ordered)]);aliasnodes.append(a['shell_connectivity'][sidx,2:6]);aliasthic.append(thic);aliasmissing.append(a['shell_thickness_missing'][sidx])
        masterrange.append([min(values),max(values)]);masterparts.append(parts)
    thickness=np.column_stack((a['node_local_corner_thickness_min'],a['node_local_corner_thickness_max']))
    need(np.array_equal(np.isnan(thickness).all(axis=1),a['node_family_incidence'][:,0]==0),'no_shell_unknown_equivalence')
    return {'ids':a['node_ids'],'xyz':a['node_xyz'],'node_source_line':np.column_stack((a['node_source'],a['node_line'])),
       'node_thickness':thickness,'nodeparts':nodeparts,'nodepart_offsets':offsets,'flags':a['population_flags'],
       'master_identity':a['master_identity'],'master_nodes':a['master_node_ids'],'master_coords':a['node_xyz'][a['master_node_indices']],
       'master_thickness':np.asarray(masterrange),'master_parts':masterparts,'master_attributes':a['master_attributes'],'master_attribute_missing':a['master_attribute_missing'],
       'alias_identity':np.asarray(aliasidentity,dtype=np.int64),'alias_nodes':np.asarray(aliasnodes,dtype=np.int64),
       'alias_thickness':np.asarray(aliasthic),'alias_thickness_missing':np.asarray(aliasmissing,dtype=bool),
       'part_references':receipt['result']['part_references']}


def compute(data):
    started=time.monotonic();epsilon=1e-10*max(1.,float(np.max(np.abs(data['xyz']))))
    populations={cid:np.flatnonzero((data['flags']&bit)!=0) for cid,bit in [(1,1),(2,2)]}
    mastergroups={cid:np.flatnonzero(data['master_identity'][:,1]==sid) for cid,sid in [(1,1),(2,3)]}
    mcount=len(data['master_identity']);masks={cid:np.zeros((3,len(mastergroups[cid]),(len(populations[cid])+7)//8),dtype=np.uint8) for cid in (1,2)}
    need(all(len(v)>0 for v in populations.values()) and sum(len(v) for v in mastergroups.values())==mcount,'population_master_coverage')
    geometries={};rowchunks=[];floatchunks=[];projectchunks=[];flagchunks=[];total=0
    per_master=np.zeros((3,mcount,10),dtype=np.int64)
    for cid in (1,2):
        pop=populations[cid];points=data['xyz'][pop];slavethick=data['node_thickness'][pop]
        for local_master,master in enumerate(mastergroups[cid]):
            original=data['master_coords'][master]
            diag=float(np.min(norm(original[[2,3]]-original[[0,1]])))
            delta,unknown=thresholds(slavethick,data['master_thickness'][master],diag)
            for setting,extension in enumerate(SETTINGS):
                geom=geometry(original,float(extension))
                for key,value in geom.items():
                    value=np.asarray(value)
                    if key not in geometries:geometries[key]=np.empty((3,mcount)+value.shape,dtype=value.dtype)
                    geometries[key][setting,master]=value
                mask,numbers,projection,classes,inversion=admitted_query(points,geom,delta,unknown,epsilon)
                masks[cid][setting,local_master]=np.packbits(mask,bitorder='little')
                local=np.flatnonzero(mask);ix=pop[local];count=len(ix);total+=count
                need(total<=ADMITTED_CAP,'admitted_storage_cap')
                src,sid,line,membership_row=map(int,data['master_identity'][master])
                same_node=np.isin(data['ids'][ix],data['master_nodes'][master])
                same_part=np.asarray([any(int(p) in data['master_parts'][master] for p in data['nodeparts'][data['nodepart_offsets'][n]:data['nodepart_offsets'][n+1],1]) for n in ix],dtype=bool)
                rows=np.column_stack((np.full(count,setting),np.full(count,cid),np.full(count,master),local,ix,data['ids'][ix],
                    data['node_source_line'][ix],np.full(count,sid),np.full(count,src),np.full(count,line),classes,
                    data['nodepart_offsets'][ix],data['nodepart_offsets'][ix+1])).astype('<i8')
                need(rows.shape==(count,14) and numbers.shape==(count,11),'candidate_row_width')
                rowchunks.append(rows);floatchunks.append(numbers);projectchunks.append(projection)
                flagchunks.append(np.column_stack((same_node,same_part,inversion)))
                classcounts=np.bincount(classes,minlength=4)
                per_master[setting,master]=[len(pop),count,len(pop)-count,*classcounts,int(same_node.sum()),int(same_part.sum()),int(np.count_nonzero(classes>=2))]
            if local_master%25==0:
                need(peak()<=MEMORY_CAP,'memory_cap');need(time.monotonic()-started<=SECONDS_CAP,'time_cap')
        PROGRESS.append({'cid':cid,'complete':True})
    arrays={'candidate_integers':np.concatenate(rowchunks),'candidate_values':np.concatenate(floatchunks),
        'candidate_projection_inside':np.concatenate(projectchunks).astype(np.int8),
        'candidate_flags':np.concatenate(flagchunks),'per_master_counts':per_master,
        'CID1_admission_bits':masks[1],'CID2_admission_bits':masks[2],
        'CID1_slave_node_indices':populations[1],'CID2_slave_node_indices':populations[2],
        'CID1_master_indices':mastergroups[1],'CID2_master_indices':mastergroups[2],
        'node_ids':data['ids'],'node_source_line':data['node_source_line'],'node_xyz':data['xyz'],
        'node_supplied_thickness_range':data['node_thickness'],'node_part_family_counts':data['nodeparts'],'node_part_offsets':data['nodepart_offsets'],
        'master_identity':data['master_identity'],'master_node_ids':data['master_nodes'],'master_original_corners':data['master_coords'],
        'master_supplied_thickness_range':data['master_thickness'],'master_attributes':data['master_attributes'],'master_attribute_missing':data['master_attribute_missing'],
        'master_alias_identity':data['alias_identity'],'master_alias_nodes':data['alias_nodes'],'master_alias_thickness':data['alias_thickness'],
        'master_alias_thickness_missing':data['alias_thickness_missing'],'extension_factors':SETTINGS.copy()}
    arrays.update({'geometry_'+k:v for k,v in geometries.items()})
    summarize=summaries(arrays,data,epsilon)
    need(peak()<=MEMORY_CAP,'memory_cap_end');need(time.monotonic()-started<=SECONDS_CAP,'time_cap_end')
    return arrays,{'epsilon':epsilon,'max_abs_selected_coordinate':float(np.max(np.abs(data['xyz']))),
       'summary':summarize,'part_references':data['part_references'],'input_scope':'Frozen independently extracted selected numeric arrays; no raw mesh pass.',
       'interpretation_ceiling':'Conditional geometric image-set diagnostic, not effective LS-DYNA defaults, initialization, active ties, restraint, physical units/floors, capacity or collapse cause.'}


def summaries(a,data,epsilon):
    rows=a['candidate_integers'];flags=a['candidate_flags'];groups=[];transitions=[]
    def parts_for(indices):
        return sorted(int(v) for v in np.unique(data['nodeparts'][np.isin(data['nodeparts'][:,0],indices),1]))
    for cid in (1,2):
        n=len(a['CID'+str(cid)+'_slave_node_indices']);m=len(a['CID'+str(cid)+'_master_indices'])
        maps=[]
        for setting,e in enumerate(SETTINGS):
            pick=(rows[:,0]==setting)&(rows[:,1]==cid);group=rows[pick];gflags=flags[pick]
            perclass=[]
            for cls in range(4):
                r=group[group[:,11]==cls];ids=np.unique(r[:,4]);partids=parts_for(ids)
                perclass.append({'class':cls,'rows':len(r),'unique_nodes':len(ids),'incident_part_ids':partids,
                    'nodes_with_multiple_master_records':int(np.count_nonzero(np.bincount(r[:,3],minlength=n)>1))})
            known=group[group[:,11]>=2];partids=parts_for(np.unique(group[:,4]))
            mids=a['CID'+str(cid)+'_master_indices'];counts=a['per_master_counts'][setting,mids]
            groups.append({'cid':cid,'setting_index':setting,'extension_factor':float(e),'complete_pairs':n*m,
                'admitted_rows':len(group),'broad_phase_excluded_pairs':n*m-len(group),'per_class':perclass,
                'unique_admitted_nodes':len(np.unique(group[:,4])),'admitted_incident_part_ids':partids,
                'unique_known_nonoutside_nodes':len(np.unique(known[:,4])),
                'masters_with_zero_admitted_rows':int(np.count_nonzero(counts[:,1]==0)),
                'masters_with_zero_known_nonoutside_rows':int(np.count_nonzero(counts[:,9]==0)),
                'nodes_with_multiple_admitted_master_records':int(np.count_nonzero(np.bincount(group[:,3],minlength=n)>1)),
                'nodes_with_multiple_known_nonoutside_master_records':int(np.count_nonzero(np.bincount(known[:,3],minlength=n)>1)),
                'same_node_ID_rows':int(gflags[:,0].sum()),'same_effective_part_rows':int(gflags[:,1].sum()),
                'small_inversion_rows':int(gflags[:,2].sum()),
                'same_node_ID_per_class':[int(np.count_nonzero(gflags[:,0]&(group[:,11]==c))) for c in range(4)],
                'same_effective_part_per_class':[int(np.count_nonzero(gflags[:,1]&(group[:,11]==c))) for c in range(4)]})
            maps.append({(int(r[2]),int(r[3])):int(r[11]) for r in group})
        for setting in (1,2):
            old,new=maps[0],maps[setting];common=old.keys()&new.keys();counts=np.zeros((4,4),dtype=np.int64)
            for key in common:counts[old[key],new[key]]+=1
            transitions.append({'cid':cid,'from_setting':0,'to_setting':setting,'new_admissions':len(new.keys()-old.keys()),
                'lost_admissions':len(old.keys()-new.keys()),'common_pairs':len(common),'class_transition_counts':counts.tolist()})
    warnings=[]
    for setting in range(3):
        warnings.append({'setting_index':setting,'zero_edges':int(a['geometry_edge_exact_zero'][setting].sum()),
            'zero_triangles':int(a['geometry_triangle_exact_zero'][setting].sum()),'near_zero_triangles':int(a['geometry_triangle_near_zero'][setting].sum()),
            'zero_corner_jacobians':int(a['geometry_jacobian_warnings'][setting,:, :,0].sum()),
            'zero_centre_jacobian_master_records':int(np.count_nonzero(a['geometry_jacobian_centre_norm'][setting]==0)),
            'zero_corner_centre_dot':int(a['geometry_jacobian_warnings'][setting,:,:,2].sum()),
            'negative_corner_centre_dot':int(a['geometry_jacobian_warnings'][setting,:,:,3].sum())})
    aliases=np.bincount(data['alias_identity'][:,0],minlength=len(data['master_identity']))
    return {'groups':groups,'extension_sensitivity':transitions,'geometry_warning_counts':warnings,
        'masters_with_multiple_aliases':int(np.count_nonzero(aliases>1)),'masters_with_no_aliases':int(np.count_nonzero(aliases==0)),
        'all_admitted_rows':len(rows),'all_class_counts':np.bincount(rows[:,11],minlength=4).tolist(),
        'total_complete_pairs_all_settings':sum(g['complete_pairs'] for g in groups),'epsilon':epsilon}


ARRAY_COLUMNS={
 'candidate_integers':['setting_index','CID','master_record_index','slave_population_index','global_selected_node_index','NID','node_SRC','node_line','master_set_ID','master_SRC','master_line','class','node_part_start','node_part_stop'],
 'candidate_values':['dA','dB','L','U','delta_low','delta_high','signed_012','signed_023','signed_013','signed_123','AABB_distance'],
 'candidate_projection_inside':['triangle_012','triangle_023','triangle_013','triangle_123'],
 'candidate_flags':['same_node_ID','same_effective_part','L_greater_than_U'],
 'per_master_counts':['complete_population','admitted','broad_excluded','class0','class1','class2','class3','same_node_ID','same_effective_part','known_nonoutside'],
 'master_identity':['SRC','set_ID','source_line','membership_row'],
 'master_alias_identity':['master_record_index','shell_SRC','shell_connectivity_line','shell_thickness_line','EID','original_PID','effective_PID','ordered_alias'],
 'node_part_family_counts':['global_selected_node_index','effective_PID','family_code','unique_element_count'],
 'geometry_jacobian_warnings':['zero_corner_jacobian','zero_centre_jacobian','zero_dot','negative_dot']}


def array_manifest(arrays):
    result={}
    for key,value in sorted(arrays.items()):
        need(isinstance(value,np.ndarray) and value.dtype.kind in 'biuf','non_numeric_output_array')
        need(not (value.dtype.kind=='f' and np.isinf(value).any()),'infinite_output_array')
        result[key]={'shape':list(value.shape),'dtype':value.dtype.str,'sha256':hashlib.sha256(value.tobytes(order='C')).hexdigest(),
            'bytes':value.nbytes,'columns_if_applicable':ARRAY_COLUMNS.get(key)}
    return result


def validate_masks(arrays):
    rows=arrays['candidate_integers']
    for cid in (1,2):
        pop=arrays['CID'+str(cid)+'_slave_node_indices'];masters=arrays['CID'+str(cid)+'_master_indices'];packed=arrays['CID'+str(cid)+'_admission_bits']
        for setting in range(3):
            for local,master in enumerate(masters):
                bits=np.unpackbits(packed[setting,local],bitorder='little')
                need(not bits[len(pop):].any(),'nonzero_mask_padding')
                selected=rows[(rows[:,0]==setting)&(rows[:,1]==cid)&(rows[:,2]==master),3]
                need(np.array_equal(np.flatnonzero(bits[:len(pop)]),selected),'mask_admitted_row_bijection')


def ensure_new(paths):need(not any(p.exists() for p in paths),'existing_output')


def synthetic_dataset():
    square=np.asarray([[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.]])
    points=np.concatenate((np.asarray([[.5,.5,0.],[.5,.5,.2],[1.08,.5,0.],[10.,10.,10.],[.5,.5,0.]]),square))
    thickness=np.zeros((9,2));thickness[3]=np.nan
    nodeparts=np.asarray([[i,20 if i==3 else 10,1 if i==3 else 0,1] for i in range(9)],dtype=np.int64)
    identities=np.asarray([[121,1,100,1],[121,1,101,2],[121,3,102,1]],dtype=np.int64)
    alias=np.asarray([[i,121,200+i*2,201+i*2,1000+i,10,10,1] for i in range(3)],dtype=np.int64)
    return {'ids':np.arange(1,10,dtype=np.int64),'xyz':points,'flags':np.asarray([1,1,1,1,2,4,4,4,4],dtype=np.uint8),
       'node_source_line':np.column_stack((np.full(9,121),np.arange(10,19))),
       'node_thickness':thickness,'nodeparts':nodeparts,'nodepart_offsets':np.arange(10,dtype=np.int64),
       'master_identity':identities,'master_nodes':np.tile(np.arange(6,10),(3,1)),
       'master_coords':np.tile(square,(3,1,1)),'master_thickness':np.zeros((3,2)),'master_parts':[{10},{10},{10}],
       'master_attributes':np.zeros((3,4)),'master_attribute_missing':np.zeros((3,4),dtype=bool),
       'alias_identity':alias,'alias_nodes':np.tile(np.arange(6,10),(3,1)),
       'alias_thickness':np.column_stack((np.zeros((3,4)),np.full(3,np.nan))),
       'alias_thickness_missing':np.tile([False,False,False,False,True],(3,1)),
       'part_references':[{'effective_part':10},{'effective_part':20}]}


def controls():
    tested=[];epsilon=1e-10
    def check(label,condition):need(condition,'control_'+label);tested.append(label)
    def reject(label,fn,expected):
        try:fn()
        except Rejected as exc:check(label,exc.code==expected)
        else:raise Rejected('control_missing_rejection_'+label)
    tri=np.asarray([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
    p=np.asarray([[.2,.2,2.],[.6,-.4,0.],[-1.,-1.,0.],[2.,0.,0.],[0.,2.,0.],[.8,.8,0.],[.5,0.,0.],[0.,0.,0.]])
    d,s,f=triangle_query(p,*tri)
    check('interior_edge_vertices_and_BC_distance',np.allclose(d,[2.,.4,np.sqrt(2),1.,1.,np.sqrt(.18),0.,0.],atol=epsilon,rtol=0))
    check('signed_distance_and_inside_flags',np.allclose(s,[2.,0,0,0,0,0,0,0],atol=epsilon,rtol=0) and f.tolist()==[1,0,0,0,0,0,1,1])
    dr,sr,fr=triangle_query(p,*tri[[0,2,1]])
    check('reversed_winding',np.allclose(dr,d,atol=epsilon,rtol=0) and np.allclose(sr,-s,atol=epsilon,rtol=0) and np.array_equal(fr,f))
    dd,ss,ff=triangle_query(np.asarray([[.2,1.,0.]]),tri[0],tri[1],tri[1])
    check('zero_area_reduces_to_edges_unknown_plane',np.allclose(dd,[1.],atol=epsilon,rtol=0) and np.isnan(ss).all() and (ff==-1).all())
    dz,sz,fz=triangle_query(np.asarray([[1.,2.,2.]]),tri[0],tri[0],tri[0])
    check('all_zero_edges_vertex_distance',dz.tolist()==[3.] and np.isnan(sz).all() and fz.tolist()==[-1])
    square=np.asarray([[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.]])
    g=geometry(square,1.)
    check('planar_rectangle_w_zero_diagonals',g['warp_bound']==0 and np.allclose(g['original_diagonals'],np.sqrt(2),atol=epsilon,rtol=0))
    sample=np.asarray([[.2,.3,1.],[.6,-.3,.4],[1.2,1.3,0.]])
    delta=np.full((3,2),10.);unk=np.zeros(3,dtype=bool)
    mask,numbers,inside,classes,inversion=admitted_query(sample,g,delta,unk,epsilon)
    check('analytic_planar_enclosure',np.allclose(numbers[:,0],[1.,.5,np.sqrt(.13)],atol=epsilon,rtol=0) and np.allclose(numbers[:,0],numbers[:,1],atol=epsilon,rtol=0) and np.allclose(numbers[:,2],numbers[:,3],atol=epsilon,rtol=0))
    warped=square.copy();warped[2,2]=.2;gw=geometry(warped,1.)
    grid=np.asarray([(u,v) for u in np.linspace(0,1,7) for v in np.linspace(0,1,7)])
    patchpoints=patch(warped,grid[:,0],grid[:,1]);mw,nw,_,_,_=admitted_query(patchpoints,gw,np.full((49,2),1.),np.zeros(49,dtype=bool),epsilon)
    check('warped_patch_points_zero_true_distance_inside_enclosure',mw.all() and (nw[:,2]<=epsilon).all() and (nw[:,3]>=0).all() and gw['warp_bound']>0)
    trapezoid=square.copy();trapezoid[1,0]=2.;trapezoid[2,0]=1.4;gt=geometry(trapezoid,1.)
    tp=patch(trapezoid,.3,.7)+[0,0,1.]
    _,nt,_,_,_=admitted_query(np.asarray([tp]),gt,np.asarray([[10.,10.]]),np.asarray([False]),epsilon)
    check('planar_nonparallelogram_nonzero_w',gt['warp_bound']>0 and nt[0,2]<=1.<=nt[0,3])
    for e in SETTINGS:
        h=(e-1)/2;ge=geometry(warped,float(e));uv=np.asarray([(u,v) for u in np.linspace(-h,1+h,5) for v in np.linspace(-h,1+h,5)])
        xyz=patch(warped,uv[:,0],uv[:,1]);check('extended_AABB_containment_'+str(e),(aabb_distance(xyz,ge['extended_corners'])<=epsilon).all())
    distancegate=np.full((1,2),.05*np.sqrt(2));point=np.asarray([[1.08,.5,0.]])
    admissions=[bool(admitted_query(point,geometry(square,float(e)),distancegate,np.asarray([False]),epsilon)[0][0]) for e in SETTINGS]
    check('known_point_only_after_extension',admissions==[False,False,True])
    th,u=thresholds(np.asarray([[.01,.10],[np.nan,np.nan]]),np.asarray([.02,.20]),1.)
    check('supplied_value_threshold_formula',np.allclose(th[0],[.05,.18],atol=epsilon,rtol=0) and np.isnan(th[1]).all() and u.tolist()==[False,True])
    _,nt,_,cl,_=admitted_query(np.asarray([[.5,.5,.1],[100.,100.,100.]]),g,th,u,epsilon)
    check('thickness_sensitive_and_unknown_always_admitted',cl.tolist()==[2,0] and len(nt)==2)
    cl,_=classify(np.asarray([.1,.2+2*epsilon,.1-2*epsilon]),np.asarray([.1,.2+2*epsilon,.1-2*epsilon]),np.asarray([[.1,.2]]*3),np.zeros(3,dtype=bool),epsilon)
    check('strict_boundary_inside_outside',cl.tolist()==[2,1,3])
    ci,inv=classify(np.asarray([1.+epsilon/2,1.+epsilon/2]),np.ones(2),np.asarray([[10.,10.],[np.nan,np.nan]]),np.asarray([False,True]),epsilon)
    check('small_inversion_preserved_class2_unknown0',ci.tolist()==[2,0] and inv.all())
    reject('large_inversion',lambda:classify(np.asarray([1.+2*epsilon]),np.asarray([1.]),np.asarray([[10.,10.]]),np.asarray([False]),epsilon),'bilinear_enclosure_inversion_over_epsilon')
    reject('negative_thickness',lambda:thresholds(np.asarray([[-1.,0.]]),np.zeros(2),1.),'invalid_slave_thickness')
    reject('partial_unknown_thickness',lambda:thresholds(np.asarray([[np.nan,0.]]),np.zeros(2),1.),'partially_unknown_slave_thickness')
    reject('nonfinite_known_threshold',lambda:classify(np.asarray([0.]),np.asarray([1.]),np.asarray([[0.,np.inf]]),np.asarray([False]),epsilon),'nonfinite_known_bounds_or_threshold')
    thin=square.copy();thin[:,1]*=1e-16;gn=geometry(thin,1.)
    check('near_degeneracy_not_zero_repair',gn['triangle_near_zero'].all() and not gn['triangle_exact_zero'].any())
    zero=np.zeros((4,3));gz=geometry(zero,1.)
    check('degenerate_normals_and_projection_metadata',np.isnan(gz['triangle_unit_normals']).all() and gz['edge_exact_zero'].all() and gz['triangle_exact_zero'].all())
    bowtie=square[[0,2,3,1]];gb=geometry(bowtie,1.)
    check('orientation_warning_not_repaired',gb['jacobian_warnings'].any())
    meshpoints=np.asarray([(x,y,z) for x in [-.3,.2,.8,1.3] for y in [-.3,.4,1.3] for z in [0.,.04,.3]])
    th=np.full((len(meshpoints),2),.1);unknown=np.zeros(len(meshpoints),dtype=bool)
    for e in SETTINGS:
        ge=geometry(square,float(e));mask,n1,_,c1,_=admitted_query(meshpoints,ge,th,unknown,epsilon)
        _,n2,_,c2,_=admitted_query(meshpoints,ge,th,unknown,epsilon,True)
        check('broad_phase_against_unpruned_'+str(e),np.all(c2[~mask]==1) and np.allclose(n1,n2[mask],atol=epsilon,rtol=0) and np.array_equal(c1,c2[mask]))
    tiny=synthetic_dataset();a,r=compute(tiny);a2,r2=compute(tiny)
    check('complete_synthetic_repeat',r==r2 and a.keys()==a2.keys() and all(np.array_equal(v,a2[k],equal_nan=True) for k,v in a.items()))
    validate_masks(a);check('complete_masks_rows_and_duplicate_masters',np.array_equal(a['CID1_admission_bits'][:,0],a['CID1_admission_bits'][:,1]))
    check('synthetic_join_and_unknown_preservation',any(x['class']==0 and x['incident_part_ids']==[20] for x in r['summary']['groups'][0]['per_class']) and a['candidate_flags'][:,1].any())
    altered={k:v.copy() for k,v in a.items()};altered['CID1_admission_bits'][0,0,0]^=1
    reject('mutated_mask_rejected',lambda:validate_masks(altered),'mask_admitted_row_bijection')
    reject('existing_output_refusal',lambda:ensure_new([Path(__file__)]),'existing_output')
    reject('mutated_input_pin_refusal',lambda:need(hashlib.sha256(b'changed').hexdigest()==hashlib.sha256(b'original').hexdigest(),'input_pin'),'input_pin')
    reject('object_array_rejected',lambda:array_manifest({'x':np.asarray([None],dtype=object)}),'non_numeric_output_array')
    buffer=io.BytesIO();np.savez_compressed(buffer,**a);buffer.seek(0)
    with np.load(buffer,allow_pickle=False) as z:check('numeric_archive_roundtrip',all(np.array_equal(z[k],v,equal_nan=True) for k,v in a.items()))
    PROGRESS.clear();return tested


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='independent-proximity01.json');parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args();started=time.monotonic();tested=controls()
    if args.selftest:print(json.dumps({'status':'PASS','controls':tested,'count':len(tested)}));return
    target=BASE/args.output;archive=target.with_suffix('.npz');failed=target.with_name(target.stem+'-failed.json')
    need(target.parent.resolve()==BASE and re.fullmatch(r'independent-proximity[a-z0-9-]+\.json',target.name),'output_scope')
    ensure_new([target,archive,failed]);before={}
    try:
        before=pins();data=load_frozen();arrays,result=compute(data);validate_masks(arrays);manifest=array_manifest(arrays)
        after=pins();need(before==after,'inputs_changed')
        with archive.open('xb') as f:np.savez_compressed(f,**arrays)
        with np.load(archive,allow_pickle=False) as z:
            need(set(z.files)==set(arrays),'saved_array_keys')
            for k,v in arrays.items():need(np.array_equal(z[k],v,equal_nan=True),'saved_array_changed')
        final=pins();need(before==final,'inputs_changed_during_save');need(peak()<=MEMORY_CAP,'final_memory_cap')
        receipt={'status':'PASS','command':sys.argv,'seconds':time.monotonic()-started,'peak_bytes':peak(),'numpy':np.__version__,
          'controls':tested,'pins_before':before,'pins_after':final,'progress':PROGRESS,'array_file':archive.name,'array_sha256':sha(archive),
          'array_schema':manifest,'limits':{'seconds_compute':SECONDS_CAP,'memory_bytes':MEMORY_CAP,'admitted_rows':ADMITTED_CAP},
          'mask_schema':'CID arrays: setting, master-within-CID in frozen order, packed complete slave-in-CID order; little bit order; unused trailing bits zero.',
          'indices':'All array indices zero-based. Source lines, source IDs, master membership rows and node IDs retain frozen input meanings.',
          'geometry_axes':'Geometry arrays: setting, global master record, then documented triangle/corner axes. Triangle order 012,023,013,123.',
          'missing_policy':'No-shell thresholds NaN and class0. Exactly zero-area triangle unit normals/signed distances NaN, projection flags -1. Nondegenerate projection flags 0/1. Small enclosure inversion retained; known thickness class2, unknown class0.',
          'class_schema':{'0':'unknown thickness','1':'outside high gate','2':'unresolved_boundary_or_thickness_sensitive','3':'inside low gate'},
          'family_codes':{'shell':0,'beam':1,'discrete':2,'solid':3},'comparison_tolerance':'epsilon absolute, zero relative for finite distances/bounds; exact IDs/masks/classes; undefined positions preserved.'}
        with target.open('x') as f:json.dump({'receipt':receipt,'result':result},f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
        # No historical result counts are printed before the parent's root freeze.
        print(json.dumps({'status':'PASS','output':target.name,'sha256':sha(target),'array_sha256':sha(archive),'controls':len(tested),
            'seconds':receipt['seconds'],'peak_bytes':receipt['peak_bytes']},sort_keys=True))
    except Exception as exc:
        failure={'status':'FAIL','code':exc.code if isinstance(exc,Rejected) else type(exc).__name__,'command':sys.argv,
          'seconds':time.monotonic()-started,'peak_bytes':peak(),'controls':tested,'pins_before':before,'progress':PROGRESS,
          'array_file_exists':archive.exists(),'result_file_exists':target.exists()}
        try:failure['pins_after']=pins()
        except Exception as later:failure['after_pin_error']=later.code if isinstance(later,Rejected) else type(later).__name__
        with failed.open('x') as f:json.dump(failure,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'status':'FAIL','code':failure['code'],'receipt':failed.name}));raise SystemExit(1) from None


if __name__=='__main__':main()
