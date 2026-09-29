#!/usr/bin/env python3
"""Complete post-freeze proximity comparison, retaining exact-rule failures."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import numpy as np

BASE=Path(__file__).resolve().parent
PINS={
 'GEOMETRIC-METHOD.md':'73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e',
 'GEOMETRIC-IMPLEMENTATION-ADDENDUM.md':'ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd',
 'verify_proximity.py':'cd3559d84e332ea7a3877a15fe8ef0e7ec8717b9cc2c73746d610e3364a31d9e',
 'proximity.py':'111f5e99646e05096838997d9aa4cddc0574d9767f784b860cb04dbcf52f0bb2',
 'independent-proximity01.json':'cc50ea1607ee4875610fdd7cdae62e22dc5e423eb776842849f1e6199217543c',
 'independent-proximity01.npz':'26a9c9421e37c38e96e7568bb0521763b0cd0e621a12e7e101f8a9b411a2bef5',
 'proximity-root01.json':'d2201fcd1f0c36f3240a32813b01ec1c8b90f44d019ac0cbb93ce54a99e5f6cc',
 'proximity-root02.json':'962f378986ad225276c1d1d8f796218b3ce729d1079ce65de5cb3664f615601b',
 'proximity-root01.npz':'b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca',
 'proximity-root02.npz':'b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca',
 'stage-root01.json':'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
 'independent-stage01.json':'ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd'}


class Error(Exception):pass
def need(ok,label):
    if not ok:raise Error(label)
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin_files():
    found={k:sha(BASE/k) for k in PINS};need(found==PINS,'file_pin')
    found['comparison_code']=sha(Path(__file__));return found
def load(name,schema):
    need(name in PINS and name.endswith('.npz'),'array_file_scope')
    with np.load(BASE/name,allow_pickle=False) as z:
        need(set(z.files)==set(schema),'array_schema_keys');out={k:z[k] for k in z.files}
    for key,a in out.items():
        s=schema[key];need(a.dtype.kind in 'biuf' and list(a.shape)==s['shape'] and a.dtype==np.dtype(s['dtype']),'array_schema')
        need(hashlib.sha256(a.tobytes(order='C')).hexdigest()==s['sha256'],'array_pin')
    return out


def exact(a,b):
    need(a.shape==b.shape and a.dtype.kind in 'biu' and b.dtype.kind in 'biu','exact_array_schema')
    mismatch=a!=b
    return {'kind':'exact','shape':list(a.shape),'slots':a.size,'mismatches':int(mismatch.sum()),'pass':not mismatch.any()}


def numeric(a,b,tolerance,units):
    need(a.shape==b.shape and a.dtype.kind=='f' and b.dtype.kind=='f','numeric_array_schema')
    need(not np.isinf(a).any() and not np.isinf(b).any(),'infinite_numeric_data')
    unknown=np.isnan(a);other=np.isnan(b);mismatch=unknown!=other;finite=~unknown&~other
    error=np.abs(a[finite]-b[finite]);maxerror=float(error.max()) if len(error) else 0.
    return {'kind':'numeric','shape':list(a.shape),'slots':a.size,'finite_slots':int(finite.sum()),
        'undefined_positions_mismatched':int(mismatch.sum()),'max_absolute_error':maxerror,
        'absolute_tolerance':tolerance,'relative_tolerance':0,'dimensional_type':units,
        'over_tolerance':int(np.count_nonzero(error>tolerance)),'pass':not mismatch.any() and maxerror<=tolerance}


def pair_order(rows,columns):
    keys=rows[:,columns];order=np.lexsort(tuple(keys[:,j] for j in reversed(range(keys.shape[1]))))
    sortedkeys=keys[order];need(not np.any(np.all(sortedkeys[1:]==sortedkeys[:-1],axis=1)),'duplicate_pair_key')
    return order


def normalize(own):
    rows=own['candidate_integers'];order=pair_order(rows,[0,2,5]);r=rows[order];flags=own['candidate_flags'][order]
    master=own['master_identity'];master_cids=np.where(master[:,1]==1,1,2)
    parts=[]
    for i in range(len(master)):
        pids=np.unique(own['master_alias_identity'][own['master_alias_identity'][:,0]==i,6]);need(len(pids)==1,'actual_master_part_not_single')
        parts.append(int(pids[0]))
    incidence=own['node_part_family_counts'];chosen=incidence[np.isin(incidence[:,0],np.unique(r[:,4]))]
    incidence=np.column_stack((own['node_ids'][chosen[:,0]],chosen[:,2],chosen[:,1],chosen[:,3]))
    incidence=incidence[np.lexsort((incidence[:,2],incidence[:,1],incidence[:,0]))]
    jac=np.concatenate((own['geometry_jacobian_centre'][:,:,None,:],own['geometry_jacobian_corners']),axis=2)
    normalpairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    dots=np.stack([own['geometry_normal_dot_products'][:,:,i,j] for i,j in normalpairs],axis=-1)
    pairs=np.column_stack((r[:,0],r[:,2],r[:,5],r[:,11],flags[:,:2])).astype(np.int64)
    normed={'admitted_node_part_incidence':incidence,'broad_mask_cid1':own['CID1_admission_bits'],'broad_mask_cid2':own['CID2_admission_bits'],
       'coverage':own['per_master_counts'][:,:,:7],'geometry_diagonals':own['geometry_extended_diagonals'],
       'geometry_edges':own['geometry_edge_lengths'],'geometry_jacobian':jac,'geometry_jacobian_dot_center':own['geometry_jacobian_dot_centre'],
       'geometry_normal_dots':dots,'geometry_quad':own['geometry_extended_corners'],'geometry_triangle_cross':own['geometry_triangle_cross_products'],
       'geometry_triangle_cross_norm':own['geometry_triangle_cross_norms'],'geometry_triangle_near':own['geometry_triangle_near_zero'],
       'geometry_triangle_unit':own['geometry_triangle_unit_normals'],'geometry_w':own['geometry_warp_bound'],
       'master_identity':np.column_stack((master_cids,master[:,1],master[:,2])),'master_nodes':own['master_node_ids'],
       'master_original_diagonals':own['geometry_original_diagonals'][0],
       'master_pids':np.asarray(parts,dtype=np.int64),'master_thickness':own['master_supplied_thickness_range'],
       'pair_projection_inside':own['candidate_projection_inside'][order],'pair_values':own['candidate_values'][order,:10],
       'pairs':pairs,'settings':own['extension_factors'],
       'slave_ids_cid1':own['node_ids'][own['CID1_slave_node_indices']],
       'slave_ids_cid2':own['node_ids'][own['CID2_slave_node_indices']]}
    return normed,r,order


def derived_groups(arrays):
    pairs=arrays['pairs'];incidence=arrays['admitted_node_part_incidence'];cids=arrays['master_identity'][:,0];coverage=arrays['coverage'];result=[]
    for ei,e in enumerate(arrays['settings']):
        for cid in (1,2):
            rows=pairs[(pairs[:,0]==ei)&(cids[pairs[:,1]]==cid)];perclass=[];cc=coverage[ei,cids==cid]
            for cls in range(4):
                r=rows[rows[:,3]==cls];nodes=np.unique(r[:,2]);pids=np.unique(incidence[np.isin(incidence[:,0],nodes),2])
                perclass.append({'class':cls,'rows':len(r),'unique_nodes':len(nodes),'pids':pids.tolist()})
            selected=rows[np.isin(rows[:,3],[2,3])];_,counts=np.unique(selected[:,2],return_counts=True)
            result.append({'e':float(e),'cid':cid,'population_pairs':int(cc[:,0].sum()),'admitted_rows':len(rows),
              'broad_excluded_pairs':int(cc[:,2].sum()),'zero_admission_masters':int(np.count_nonzero(cc[:,1]==0)),
              'same_node_rows':int(rows[:,4].sum()),'same_part_rows':int(rows[:,5].sum()),
              'multiple_candidate_master_nodes':int(np.count_nonzero(counts>1)),
              'max_candidate_multiplicity':int(counts.max()) if len(counts) else 0,'classes':perclass})
    return result


def compare_repeat(first,second):
    x=copy.deepcopy(first);y=copy.deepcopy(second)
    for obj in (x,y):
        for key in ('elapsed_seconds','peak_bytes'):obj.pop(key)
    need(x['command'][:-1]==y['command'][:-1] and x['command'][-1]=='proximity-root01' and y['command'][-1]=='proximity-root02','repeat_command')
    need(x['array_file']=='proximity-root01.npz' and y['array_file']=='proximity-root02.npz','repeat_archive_name')
    x.pop('command');y.pop('command');x.pop('array_file');y.pop('array_file')
    need(x==y,'root_repeat_extra_difference')


def one_comparison(own,root,ownmeta,rootmeta,tols):
    n,rows,order=normalize(own);root=copy.copy(root);rp=pair_order(root['pairs'],[0,1,2])
    for name in ('pairs','pair_values','pair_projection_inside'):root[name]=root[name][rp]
    need(n.keys()==root.keys(),'complete_root_array_coverage');checks={}
    length={'geometry_diagonals','geometry_edges','geometry_quad','geometry_w','master_original_diagonals','master_thickness','pair_values'}
    power2={'geometry_jacobian','geometry_triangle_cross','geometry_triangle_cross_norm'}
    dimensionless={'geometry_normal_dots','geometry_triangle_unit','settings'}
    for name,expected in n.items():
        observed=root[name]
        if expected.dtype.kind in 'biu':checks[name]=exact(expected,observed)
        elif name in length:checks[name]=numeric(expected,observed,tols['length'],'length')
        elif name in power2:checks[name]=numeric(expected,observed,tols['length_squared'],'length_squared')
        elif name in dimensionless:checks[name]=numeric(expected,observed,tols['dimensionless'],'dimensionless')
        elif name=='geometry_jacobian_dot_center':checks[name]=numeric(expected,observed,tols['length_fourth'],'length_fourth')
        else:raise Error('unclassified_array_units')
    # Explicit identity/non-class fields must still be audited when class differences exist.
    checks['pair_identity_fields']=exact(n['pairs'][:,[0,1,2,4,5]],root['pairs'][:,[0,1,2,4,5]])
    need(checks['pair_identity_fields']['pass'],'pair_identity_mismatch_prevents_aligned_review')
    checks['coverage_population_admission_exclusion']=exact(n['coverage'][:,:,:3],root['coverage'][:,:,:3])
    fieldnames=['dA','dB','L','U','delta_low','delta_high','signed_012','signed_023','signed_013','signed_123']
    for j,name in enumerate(fieldnames):checks['pair_field_'+name]=numeric(n['pair_values'][:,j],root['pair_values'][:,j],tols['length'],'length')
    rootzero=root['geometry_triangle_cross_norm']==0
    checks['derived_exact_zero_triangles']=exact(own['geometry_triangle_exact_zero'],rootzero)
    checks['derived_exact_zero_edges']=exact(own['geometry_edge_exact_zero'],root['geometry_edges']==0)
    checks['derived_triangle_areas']=numeric(own['geometry_triangle_areas'],root['geometry_triangle_cross_norm']/2,tols['length_squared'],'length_squared')
    jac=root['geometry_jacobian'];cn=np.linalg.norm(jac[:,:,0],axis=-1);jn=np.linalg.norm(jac[:,:,1:],axis=-1);dots=root['geometry_jacobian_dot_center']
    rootwarnings=np.stack((jn==0,np.broadcast_to((cn==0)[:,:,None],jn.shape),dots==0,dots<0),axis=-1)
    checks['derived_jacobian_warning_flags']=exact(own['geometry_jacobian_warnings'],rootwarnings)
    need(derived_groups(root)==rootmeta['result']['groups'],'root_summaries_do_not_recompute')
    need(rootmeta['result']['small_inversion_rows']==int(np.count_nonzero(root['pair_values'][:,2]>root['pair_values'][:,3])),'root_inversion_summary')
    # Root's selected references must be copied unchanged from its frozen stage.
    rootstage=json.loads((BASE/'stage-root01.json').read_text())['result'];pids=set(map(int,root['admitted_node_part_incidence'][:,2]))
    copied=[p for p in rootstage['part_references'] if p['pid'] in pids]
    need(copied==rootmeta['result']['admitted_part_references'],'root_admitted_reference_copy')
    independent_parts={p['effective_part']:p for p in ownmeta['result']['part_references']}
    for ref in copied:
        ownpart=independent_parts[ref['pid']];part=ref['part'];need(part is not None and ownpart['status']=='supplied_part_definition','admitted_missing_part')
        need([part['pid'],part['original_pid'],part['section_id'],part['material_id'],part['original_section_id'],part['original_material_id'],part['line']]==
             [ownpart['effective_part'],ownpart['card'][0],ownpart['effective_section'],ownpart['effective_material'],ownpart['card'][1],ownpart['card'][2],ownpart['line']], 'admitted_part_namespace_or_locator')
        need(ref['section_defined']==(ownpart['section_definition'] is not None),'admitted_section_status')
        need(ref['material_keyword']==(None if ownpart['material_definition'] is None else '*'+ownpart['material_definition']['keyword']),'admitted_material_status')
    class_difference=np.flatnonzero(n['pairs'][:,3]!=root['pairs'][:,3]);projection_difference=np.argwhere(n['pair_projection_inside']!=root['pair_projection_inside'])
    oi=n['pair_values'][:,2]>n['pair_values'][:,3];ri=root['pair_values'][:,2]>root['pair_values'][:,3]
    classes=[]
    for idx in class_difference:
        classes.append({'pair_key':n['pairs'][idx,:3].tolist(),'CID':int(rows[idx,1]),'node_source_line':rows[idx,6:8].tolist(),
           'master_source_line':rows[idx,9:11].tolist(),'independent_class':int(n['pairs'][idx,3]),'root_class':int(root['pairs'][idx,3]),
           'independent_inverted':bool(oi[idx]),'root_inverted':bool(ri[idx]),
           'independent_L_minus_U':float(n['pair_values'][idx,2]-n['pair_values'][idx,3]),
           'root_L_minus_U':float(root['pair_values'][idx,2]-root['pair_values'][idx,3]),
           'max_length_field_error':float(np.nanmax(np.abs(n['pair_values'][idx]-root['pair_values'][idx])))})
    projections=[{'pair_key':n['pairs'][idx,:3].tolist(),'triangle_index':int(tri),'independent_flag':int(n['pair_projection_inside'][idx,tri]),
        'root_flag':int(root['pair_projection_inside'][idx,tri])} for idx,tri in projection_difference]
    groups=derived_groups(n)
    saved_groups={(g['setting_index'],g['cid']):g for g in ownmeta['result']['summary']['groups']}
    for g in groups:
        setting=int(np.flatnonzero(n['settings']==g['e'])[0]);saved=saved_groups[(setting,g['cid'])]
        need([g['population_pairs'],g['admitted_rows'],g['broad_excluded_pairs'],g['zero_admission_masters'],g['same_node_rows'],g['same_part_rows'],g['multiple_candidate_master_nodes']]==
             [saved['complete_pairs'],saved['admitted_rows'],saved['broad_phase_excluded_pairs'],saved['masters_with_zero_admitted_rows'],saved['same_node_ID_rows'],saved['same_effective_part_rows'],saved['nodes_with_multiple_known_nonoutside_master_records']], 'independent_group_summary')
        need(g['classes']==[{'class':c['class'],'rows':c['rows'],'unique_nodes':c['unique_nodes'],'pids':c['incident_part_ids']} for c in saved['per_class']], 'independent_class_summary')
    ownclasses=np.zeros((4,4),dtype=np.int64)
    for a,b in zip(n['pairs'][:,3],root['pairs'][:,3]):ownclasses[a,b]+=1
    numeric_pass=all(v['pass'] for v in checks.values() if v['kind']=='numeric')
    exact_pass=all(v['pass'] for v in checks.values() if v['kind']=='exact')
    return {'checks':checks,'numeric_checks_pass':numeric_pass,'all_exact_checks_pass':exact_pass,
       'all_root_array_fields_covered':len(n),'pair_rows':len(rows),'class_disagreement_count':len(classes),
       'projection_flag_disagreement_count':len(projections),'class_disagreements':classes,'projection_disagreements':projections,
       'class_matrix_independent_rows_root_columns':ownclasses.tolist(),
       'all_class_disagreements_have_different_inversion_flag':bool(np.all(oi[class_difference]!=ri[class_difference])),
       'independent_small_inversion_rows':int(oi.sum()),'root_small_inversion_rows':int(ri.sum()),
       'independent_max_positive_L_minus_U':float(np.maximum(0,n['pair_values'][:,2]-n['pair_values'][:,3]).max()),
       'root_max_positive_L_minus_U':float(np.maximum(0,root['pair_values'][:,2]-root['pair_values'][:,3]).max()),
       'independent_groups_normalized_to_root_schema':groups,'root_groups':rootmeta['result']['groups'],
       'admitted_part_references_common_verified':len(copied)}


def controls():
    names=[]
    a=np.asarray([1.,np.nan]);b=a.copy()
    need(numeric(a,b,1e-10,'length')['pass'],'control_equal');names.append('equal_numeric_and_NaN')
    b[0]+=1e-9;need(not numeric(a,b,1e-10,'length')['pass'],'control_changed');names.append('over_tolerance_retained')
    b=a.copy();b[1]=0.;need(not numeric(a,b,1e-10,'length')['pass'],'control_NaN');names.append('undefined_zero_mismatch')
    need(not exact(np.asarray([1,2]),np.asarray([1,3]))['pass'],'control_exact');names.append('exact_class_mutation')
    need(not exact(np.asarray([0,1],dtype=np.int8),np.asarray([1,1],dtype=np.int8))['pass'],'control_projection');names.append('projection_mutation')
    for label,x,y in [('ID',1,2),('namespace',179,1179),('source_line',10,11),('mask',0,1)]:
        need(not exact(np.asarray([x]),np.asarray([y]))['pass'],'control_'+label);names.append(label+'_mutation')
    try:pair_order(np.asarray([[0,1,2],[0,1,2]]),[0,1,2])
    except Error:names.append('duplicate_pair_key_refused')
    else:raise Error('control_duplicate')
    pair={'command':['proximity.py','--output','proximity-root01'],'array_file':'proximity-root01.npz','elapsed_seconds':1.,'peak_bytes':1,'result':{'count':1}}
    other=copy.deepcopy(pair);other['command'][-1]='proximity-root02';other['array_file']='proximity-root02.npz';other['elapsed_seconds']=2.;other['peak_bytes']=2
    compare_repeat(pair,other);names.append('root_repeat_named_exclusions');other['result']['count']=2
    try:compare_repeat(pair,other)
    except Error:names.append('root_repeat_result_mutation_refused')
    else:raise Error('control_repeat')
    return names


def rerun_controls():
    results=[]
    for name,flag,count in [('verify_proximity.py','--selftest',35),('proximity.py','--controls',15)]:
        command=[sys.executable,'-B',str(BASE/name),flag];p=subprocess.run(command,capture_output=True,timeout=30)
        need(p.returncode==0,'control_consumer_returncode');out=json.loads(p.stdout)
        need(out.get('count')==count and out.get('passed',out.get('status')=='PASS'),'control_consumer_count')
        results.append({'command':command,'count':count,'returncode':p.returncode,
          'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
    return results


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='proximity-comparison01.json');parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    test=controls()
    if args.selftest:print(json.dumps({'status':'PASS','controls':test,'count':len(test)}));return
    output=BASE/args.output;errorpath=output.with_name(output.stem+'-error.json')
    need(output.parent.resolve()==BASE and re.fullmatch(r'proximity-comparison[a-z0-9-]+\.json',output.name) and not output.exists() and not errorpath.exists(),'output_scope_or_exists')
    started=time.monotonic();before={}
    try:
        before=pin_files();im=json.loads((BASE/'independent-proximity01.json').read_text());roots=[json.loads((BASE/('proximity-root0'+str(i)+'.json')).read_text()) for i in (1,2)]
        need(im['receipt']['status']=='PASS' and im['receipt']['pins_before']==im['receipt']['pins_after'],'independent_receipt')
        own=load(im['receipt']['array_file'],im['receipt']['array_schema'])
        longest=float(np.linalg.norm(np.roll(own['master_original_corners'],-1,axis=1)-own['master_original_corners'],axis=-1).max())
        scale=max(1.,longest);epsilon=im['result']['epsilon']
        tols={'length':epsilon,'dimensionless':1e-10,'length_squared':1e-10*scale**2,'length_fourth':1e-10*scale**4}
        results=[]
        for rm in roots:
            need(rm['status']=='PASS' and rm['pins_before']==rm['pins_after'] and rm['result']['epsilon']==epsilon,'root_receipt')
            root=load(rm['array_file'],rm['array_schema']);results.append(one_comparison(own,root,im,rm,tols))
        compare_repeat(*roots);need(results[0]==results[1],'comparisons_root_repeat_disagree')
        consumer=rerun_controls();after=pin_files();need(before==after,'pins_changed')
        passed=results[0]['numeric_checks_pass'] and results[0]['all_exact_checks_pass']
        receipt={'status':'PASS' if passed else 'FAIL_EXACT_REPRODUCTION','comparison_completed':True,'command':sys.argv,
          'seconds':time.monotonic()-started,'peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
          'pins_before':before,'pins_after':after,'comparison_controls':test,'producer_control_consumers':consumer,
          'tolerances':tols,'longest_original_master_edge':longest,
          'tolerance_meaning':'Comparison-only thresholds approved before numerical field comparison, not certified floating error, measurement uncertainty or physical bounds. Zero relative tolerance.',
          'root_repeat':'All fields equal except command output argument, NPZ filename, elapsed seconds and peak bytes; NPZ bytes identical.',
          'result':results[0],
          'normalizations':['Sort rows by setting/master-record/NID; do not collapse duplicate master records.',
             'Map independent global selected-node indices to NIDs and frozen source locators; master-source SRC121 is inherited from the exactly compared stage.',
             'Match all 26 root arrays. Root normal-dot six-pair order maps independent full4x4 matrix; root Jacobian center-first maps separate independent center/corners.',
             'Root exact-zero edge/triangle and orientation flags derived from its retained raw arrays; independent areas compared with half root cross norms.',
             'Root admitted PART reference copies checked against root frozen stage, and common namespace/line/material/section-presence fields independently checked. Additional root section-card/heading contents are not independently re-extracted.'],
          'ceiling':'Reproduction disagreements are retained. No thresholds changed, inversion discarded, class repaired, effective tie inferred or physical candidate robustness claimed.'}
        with output.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
        print(json.dumps({'status':receipt['status'],'completed':True,'sha256':sha(output),'numeric_checks_pass':results[0]['numeric_checks_pass'],
          'class_disagreements':results[0]['class_disagreement_count'],'projection_disagreements':results[0]['projection_flag_disagreement_count'],
          'controls':len(test)},sort_keys=True))
        if not passed:raise SystemExit(1)
    except Exception as exc:
        error={'status':'ERROR','code':str(exc) if isinstance(exc,Error) else type(exc).__name__,'command':sys.argv,'pins_before':before,'comparison_controls':test}
        with errorpath.open('x') as f:json.dump(error,f,indent=2,sort_keys=True);f.write('\n')
        print(json.dumps({'status':'ERROR','code':error['code'],'receipt':errorpath.name}));raise SystemExit(2) from None


if __name__=='__main__':main()
