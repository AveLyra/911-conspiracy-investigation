#!/usr/bin/env python3
"""Post-freeze exact common-field comparison; no new geometry/source scan."""
import argparse
import copy
from collections import Counter
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
PRIOR=BASE.parent/'c79-restraint-audit'
RAW=Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
SOURCES={119:'discrete_mass.k.gz',120:'elem_thick_to-renum.k.gz',121:'wtc7_global_8a_no-conn-matl.k.gz',118:'WTC7_CaseB_400pm.int.gz'}
SOURCE_IDS={name:sid for sid,name in SOURCES.items()}
SOURCE_PINS={119:(70199,'2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7',508372,'8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601',7905),
120:(23162693,'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59',232959541,'7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda',4088491),
121:(47520888,'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d',333947423,'8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf',7196443)}
PINS={
'PROTOCOL.md':'b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea',
'INDEPENDENT-STAGE-PLAN.md':'4b616ea1a57727c7b0ac034cdc55bdb25fc656d355ef805907407bcc11cf506f',
'GROUND-REFERENCE-ADDENDUM.md':'ada80271b18d4de023fc17aafe9931d81c09b39416a3760cdbf33f76b98e86c4',
'verify_geometry.py':'a1e60b3625d00f266e3f31c983ffcbe4b3843a1c38087ccf3924e9f006ec8a06',
'extract_geometry.py':'67c0074e4f873f3b4fb50df77ee740d6c5773b31f0ab23a0c750bb4a0ec1f525',
'independent-stage01.json':'ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd',
'independent-stage01.npz':'fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5',
'stage-root01.json':'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
'stage-root01.npz':'2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
'stage-root02.json':'0a9ff75f944ffa9238c56e01fc234e199f1ca65faccfbed98217c4bd53152a33',
'stage-root02.npz':'2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf'}
DEPENDENCIES={
'own_reader':(PRIOR/'verify_restraint.py','5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a'),
'own_seed':(PRIOR/'independent01.json','d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7'),
'own_contacts':(PRIOR/'independent-contacts01.json','b30b8ee5435e7cf8ce2ea979245b07fa4b0577606bf97638dbfd76b21043c7c3'),
'root_helper':(BASE.parent/'model-member-map/map_members.py','f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'),
'root_contacts':(PRIOR/'contacts-root01.json','04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859')}
COUNTS=Counter()


class Mismatch(Exception):
    def __init__(self,label):self.label=label;super().__init__(label)


def need(ok,label):
    if not ok:raise Mismatch(label)


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()


def equal(a,b,label):
    if isinstance(a,dict):
        need(isinstance(b,dict) and a.keys()==b.keys(),label+'.keys')
        for k,v in a.items():equal(v,b[k],label+'.'+str(k))
    elif isinstance(a,list):
        need(isinstance(b,list) and len(a)==len(b),label+'.length')
        for i,(x,y) in enumerate(zip(a,b)):equal(x,y,label+'.'+str(i))
    elif isinstance(a,bool):need(type(b) is bool and a==b,label);COUNTS['metadata_boolean']+=1
    elif a is None:need(b is None,label);COUNTS['metadata_null']+=1
    elif isinstance(a,(int,float)):
        need(isinstance(b,(int,float)) and not isinstance(b,bool) and a==b,label);COUNTS['metadata_numeric']+=1
    else:need(type(a) is type(b) and a==b,label);COUNTS['metadata_string']+=1


def equal_array(a,b,label):
    need(isinstance(a,np.ndarray) and isinstance(b,np.ndarray),label+'.type')
    need(a.dtype.kind in 'biuf' and b.dtype.kind in 'biuf',label+'.numeric')
    need(a.shape==b.shape,label+'.shape')
    need(a.dtype.kind==b.dtype.kind,label+'.dtype_kind')
    need(np.array_equal(a,b,equal_nan=True),label+'.values')
    COUNTS['array_numeric_slots']+=a.size
    if a.dtype.kind=='f':COUNTS['array_NaN_slots']+=int(np.count_nonzero(np.isnan(a)))
    COUNTS['array_comparisons']+=1


def file_pins():
    found={}
    for name,want in PINS.items():
        found[name]=sha(BASE/name);need(found[name]==want,'pin.'+name)
    for alias,(path,want) in DEPENDENCIES.items():
        found[alias]=sha(path);need(found[alias]==want,'pin.'+alias)
    found['comparison_code']=sha(Path(__file__))
    for src,pin in SOURCE_PINS.items():
        path=RAW/SOURCES[src];found['SRC'+str(src)]={'bytes':path.stat().st_size,'sha256':sha(path)}
        equal(found['SRC'+str(src)],{'bytes':pin[0],'sha256':pin[1]},'compressed_source.'+str(src))
    return found


def load_arrays(name,schema,hashpin):
    path=BASE/name;need(path.parent==BASE and path.suffix=='.npz','archive_scope')
    need(sha(path)==hashpin,'archive_pin.'+name)
    with np.load(path,allow_pickle=False) as z:
        need(set(z.files)==set(schema),'archive_keys.'+name)
        arrays={k:z[k] for k in z.files}
    for key,a in arrays.items():
        need(a.dtype.kind in 'biuf','archive_nonnumeric.'+key)
        item=schema[key]
        need(list(a.shape)==item['shape'] and np.dtype(item['dtype'])==a.dtype,'archive_schema.'+key)
        need(hashlib.sha256(a.tobytes(order='C')).hexdigest()==item['sha256'],'archive_array_hash.'+key)
        if 'c_order_bytes' in item:need(a.nbytes==item['c_order_bytes'],'archive_array_bytes.'+key)
    return arrays


def mapped_arrays(a):
    """Explicit adapter from the frozen independent extraction, not source input."""
    members=a['slave_node_set_members'];rowids=np.unique(members[:,2]);need(np.array_equal(rowids,np.arange(1,len(rowids)+1)),'NSET_all_rows_positive')
    node_rows=np.zeros((len(rowids),9),dtype=np.int64)
    occupied=np.zeros((len(rowids),8),dtype=bool)
    for source,line,row,slot,nid in members:
        need(source==121 and 1<=slot<=8 and not occupied[row-1,slot-1],'NSET_slot_coverage')
        need(node_rows[row-1,0] in (0,line),'NSET_row_line')
        node_rows[row-1,0]=line;node_rows[row-1,slot]=nid;occupied[row-1,slot-1]=True
    need(np.all(node_rows[:,0]>0),'NSET_empty_rows_not_reconstructable')
    master=a['master_node_ids'];identity=a['master_identity'];ids=a['node_ids']
    need(np.all(identity[:,0]==121),'master_source_alias')
    roles=np.zeros((len(ids),4),dtype=np.uint8)
    roles[:,0]=(a['population_flags']&1)!=0;roles[:,1]=(a['population_flags']&2)!=0
    for col,sid in ((2,1),(3,3)):roles[:,col]=np.isin(ids,np.unique(master[identity[:,1]==sid]))
    need(np.array_equal((a['population_flags']&4)!=0,np.any(roles[:,2:]!=0,axis=1)),'master_role_coverage')
    pairs=a['node_part_family_counts'];part=np.column_stack((ids[pairs[:,0]],pairs[:,2],pairs[:,1],pairs[:,3]))
    part=part[np.lexsort((part[:,2],part[:,1],part[:,0]))]
    corners=a['shell_corner_incidence'];thickness=a['shell_thickness'][corners[:,1],corners[:,2]-1]
    need(np.all(np.isfinite(thickness)),'corner_supplied_value_coverage')
    zero=np.bincount(corners[thickness==0,0],minlength=len(ids))
    counts=np.bincount(corners[:,0],minlength=len(ids))
    equal_array(counts.astype('<i8'),a['node_shell_corner_occurrences'],'derived_corner_counts')
    return {'node_ids':ids,'node_source_line':np.column_stack((a['node_source'],a['node_line'])),
      'xyz':a['node_xyz'],'roles':roles,'incidence_counts':a['node_family_incidence'],
      'corner_thickness_min_max':np.column_stack((a['node_local_corner_thickness_min'],a['node_local_corner_thickness_max'])),
      'corner_thickness_count_zero':np.column_stack((counts,zero)),
      'node_part_incidence':part,'nodeset1_rows':node_rows,
      'segmentset2_rows':a['slave_segment_set_members'][:,[1,3,4,5,6]],
      'segmentset2_attributes':a['slave_segment_attributes']}


def nulls(values):return [None if np.isnan(v) else float(v) for v in values]


def require_four_distinct(rows,label):
    need(rows.ndim==2 and rows.shape[1]==4 and np.all(np.diff(np.sort(rows,axis=1),axis=1)!=0),label)


def master_metadata(a):
    require_four_distinct(a['master_node_ids'],'actual_masters_four_distinct')
    result=[]
    for idx,identity in enumerate(a['master_identity']):
        src,sid,line,row=map(int,identity);aliases=[]
        for master_index,shell_index,ordered in a['master_shell_aliases'][a['master_shell_aliases'][:,0]==idx]:
            source,connline,thicline,eid,pid,eff=map(int,a['shell_identity'][shell_index]);nodes=a['shell_connectivity'][shell_index,2:6].tolist()
            require_four_distinct(np.asarray([nodes]),'actual_alias_four_distinct')
            aliases.append({'source':source,'line':connline,'thickness_line':thicline,'eid':eid,'original_pid':pid,'pid':eff,
                'nodes':nodes,'ordered_match':bool(ordered),'thickness_card':nulls(a['shell_thickness'][shell_index])})
        aliases.sort(key=lambda x:(x['source'],x['line'],x['eid']))
        result.append({'set_id':sid,'line':line,'nodes':a['master_node_ids'][idx].tolist(),'attributes':nulls(a['master_attributes'][idx]),
            'xyz':a['node_xyz'][a['master_node_indices'][idx]].tolist(),'aliases':aliases})
    return result


def source_receipts(own,root):
    expected=[]
    for src,p in SOURCE_PINS.items():expected.append({'source':src,'bytes':p[2],'lines':p[4],'sha256':p[3],'eof':True})
    for phase in ['selection_controls','metadata_nodes','geometry']:
        records=[{k:r[k] for k in ['source','bytes','lines','sha256','eof']} for r in own['receipt']['source_passes'] if r['phase']==phase]
        equal(sorted(records,key=lambda x:x['source']),expected,'own_EOF.'+phase)
    need(set(root['sources'])=={'1','2'},'root_pass_coverage')
    for phase,group in root['sources'].items():
        need(set(group)=={SOURCES[s] for s in SOURCE_PINS},'root_source_coverage')
        for src,p in SOURCE_PINS.items():
            equal(group[SOURCES[src]],{'compressed_bytes':p[0],'compressed_sha256':p[1],'eof':True,'lines':p[4],
                'pin_after':True,'uncompressed_bytes':p[2],'uncompressed_sha256':p[3]},'root_EOF.'+phase+'.'+str(src))


def compare_metadata(i,a,r,mapped):
    expected_headers={}
    for h in i['set_headers']:
        key='node1' if h['keyword']=='SET_NODE_LIST' else 'segment2'
        expected_headers[key]={'source':h['source'],'keyword_line':h['keyword_line'],'header_line':h['header_line'],'values':h['card']}
    equal(expected_headers,r['headers'],'headers')
    expected_masters=master_metadata(a);masters=copy.deepcopy(r['master_segments'])
    for row in masters:row['aliases'].sort(key=lambda x:(x['source'],x['line'],x['eid']))
    equal(expected_masters,masters,'all_master_records')
    equal({SOURCES[int(src)]:count for src,count in i['all_node_records'].items()},r['all_node_counts'],'global_node_counts')
    equal(sum(i['all_node_records'].values()),r['unique_model_nodes'],'global_unique_nodes')
    equal({SOURCES[x['source']]+':'+x['family']:x['count'] for x in i['all_element_records']},r['all_element_counts'],'global_element_counts')
    ownparts={p['effective_part']:p for p in i['part_references']};rootparts={p['pid']:p for p in r['part_references']}
    equal(sorted(ownparts),sorted(rootparts),'part_reference_coverage')
    for pid,part in ownparts.items():
        row=rootparts[pid];label='part.'+str(pid)
        need(part['status']=='supplied_part_definition','own_part_status')
        equal({k:row['part'][k] for k in ('source','line','original_pid','pid','original_section_id','section_id','original_material_id','material_id')},
          {'source':SOURCES[part['source']],'line':part['line'],'original_pid':part['card'][0],'pid':pid,
           'original_section_id':part['card'][1],'section_id':part['effective_section'],
           'original_material_id':part['card'][2],'material_id':part['effective_material']},label+'.common_PART')
        section=part['section_definition'];material=part['material_definition']
        equal(section is not None,row['section_defined'],label+'.section_defined')
        equal(None if material is None else '*'+material['keyword'],row['material_keyword'],label+'.material_keyword')
        if row['section_shell'] is not None:
            need(section is not None and section['keyword']=='SECTION_SHELL',label+'.section_kind')
            card=row['section_shell'];equal([card['source'],card['keyword_line'],card['cards'][0]['line'],card['cards'][0]['values'][0]],
                [section['source'],section['keyword_line'],section['line'],section['original_id']],label+'.section_locator_ID')
        else:need(section is None or section['keyword']!='SECTION_SHELL',label+'.missing_section_card')
    includes=[];transforms=[]
    for edge in i['include_graph']:
        includes.append({'source':SOURCES[edge['source']],'kind':'*'+edge['keyword'],'line':edge['keyword_line'],'included':SOURCES[edge['target_source']]})
        if edge['transform_cards']:
            transforms.append({'source':SOURCES[edge['source']],'line':edge['keyword_line'],
                'cards':[c['card']+[None]*(8-len(c['card'])) for c in edge['transform_cards']],
                'coordinate_transform':'identity','FCTTEM_caveat':'numeric_1_in_character_conversion_flag_field'})
    equal(includes,r['include_graph'],'include_graph');equal(transforms,r['transforms'],'transform_numeric_cards')
    summaries=[];diagnostics=[]
    for cid in (1,2):
        ix=mapped['roles'][:,cid-1]!=0;mn=mapped['corner_thickness_min_max'][ix,0];mx=mapped['corner_thickness_min_max'][ix,1];has=np.isfinite(mn)
        summaries.append({'cid':cid,'nodes':int(ix.sum()),'nodes_without_shell_incidence':int(np.count_nonzero(~has)),
            'nodes_with_unequal_corner_thickness':int(np.count_nonzero(has&(mn!=mx))),
            'supplied_corner_thickness_min':float(np.min(mn[has])) if has.any() else None,
            'supplied_corner_thickness_max':float(np.max(mx[has])) if has.any() else None,
            'element_node_incidence_by_kind':mapped['incidence_counts'][ix].sum(axis=0).tolist()})
        coords=mapped['xyz'][ix]
        diagnostics.append({'population':cid,'axis_min':coords.min(axis=0).tolist(),'axis_max':coords.max(axis=0).tolist()})
    equal(summaries,r['slave_populations'],'slave_summaries')
    no_shell=(mapped['roles'][:,0]!=0)&(mapped['incidence_counts'][:,0]==0)
    no_shell_rows=[{'node':int(mapped['node_ids'][j]),'source':int(mapped['node_source_line'][j,0]),'line':int(mapped['node_source_line'][j,1]),
       'xyz':mapped['xyz'][j].tolist(),'incidence':mapped['incidence_counts'][j].tolist()} for j in np.flatnonzero(no_shell)]
    return {'master_records':len(expected_masters),'master_four_distinct':True,'master_alias_records':sum(len(m['aliases']) for m in expected_masters),
        'ordered_alias_records':sum(a['ordered_match'] for m in expected_masters for a in m['aliases']),
        'part_references':len(ownparts),'slave_populations':summaries,'coordinate_bounds_source_units':diagnostics,'slave1_no_shell_nodes':no_shell_rows}


def compare_root_pair(first,second):
    a=copy.deepcopy(first);b=copy.deepcopy(second)
    a.pop('elapsed_seconds');b.pop('elapsed_seconds')
    need(a['result']['array_archive']=='stage-root01.npz' and b['result']['array_archive']=='stage-root02.npz','root_pair_archive_names')
    a['result'].pop('array_archive');b['result'].pop('array_archive')
    equal(a,b,'root_repetition_except_elapsed_archive_filename')


def test_comparer():
    tests=[]
    def rejects(label,fn):
        try:fn()
        except Mismatch:tests.append(label)
        else:raise Mismatch('control_missing_rejection.'+label)
    x=np.asarray([[1.,2.,np.nan]])
    equal_array(x,x.copy(),'control.exact');tests.append('exact_and_matching_NaN')
    rejects('coordinate_tiny_change',lambda:equal_array(x,np.asarray([[1.+1e-12,2.,np.nan]]),'control'))
    rejects('NaN_changed_to_zero',lambda:equal_array(x,np.asarray([[1.,2.,0.]]),'control'))
    rejects('shape_change',lambda:equal_array(x,x.reshape(3,1),'control'))
    rejects('integer_float_dtype',lambda:equal_array(np.asarray([1]),np.asarray([1.]),'control'))
    rejects('object_array',lambda:equal_array(np.asarray([1],dtype=object),np.asarray([1]),'control'))
    rejects('node_order_change',lambda:equal([1,2,3,4],[2,1,3,4],'control'))
    rejects('namespace_change',lambda:equal({'PID':179},{'PID':1179},'control'))
    rejects('source_line_change',lambda:equal({'line':101},{'line':102},'control'))
    rejects('missing_attribute',lambda:equal([0,None],[0,0],'control'))
    rejects('extra_alias',lambda:equal([{'EID':5}],[{'EID':5},{'EID':6}],'control'))
    rejects('omitted_metadata_key',lambda:equal({'a':1},{},'control'))
    rejects('boolean_as_integer',lambda:equal(True,1,'control'))
    rejects('repeated_slot_not_set_equivalent',lambda:require_four_distinct(np.asarray([[1,2,3,3]]),'control'))
    need(set([1,2,3,3])==set([1,2,2,3]) and sorted([1,2,3,3])!=sorted([1,2,2,3]),'control.set_multiset_distinction');tests.append('set_multiset_difference_demonstrated')
    pair={'elapsed_seconds':1.,'result':{'array_archive':'stage-root01.npz','count':2}}
    other=copy.deepcopy(pair);other['elapsed_seconds']=2.;other['result']['array_archive']='stage-root02.npz'
    compare_root_pair(pair,other);tests.append('root_pair_only_named_exclusions')
    other['result']['count']=3
    rejects('root_pair_numeric_mutation',lambda:compare_root_pair(pair,other))
    COUNTS.clear();return tests


def rerun_controls():
    runs=[]
    for script,flag,expected in [('verify_geometry.py','--selftest',27),('extract_geometry.py','--controls',11)]:
        command=[sys.executable,'-B',str(BASE/script),flag]
        p=subprocess.run(command,capture_output=True,timeout=30)
        need(p.returncode==0,'control_command.'+script)
        if flag=='--selftest':
            obj=json.loads(p.stdout);need(obj['status']=='PASS' and obj['count']==expected,'independent_controls_count')
        else:need(re.search(rb'Ran '+str(expected).encode()+rb' tests? in ',p.stderr) and p.stderr.rstrip().endswith(b'OK'),'root_controls_count')
        runs.append({'script':script,'command':command,'returncode':p.returncode,'tests':expected,
            'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()})
    return runs


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='comparison01.json')
    parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    controls=test_comparer()
    if args.selftest:print(json.dumps({'status':'PASS','controls':controls,'count':len(controls)}));return
    output=BASE/args.output;failure=output.with_name(output.stem+'-failed.json')
    need(output.parent.resolve()==BASE and re.fullmatch(r'(?:comparison|independent-comparison)[a-z0-9-]*\.json',output.name),'output_scope')
    need(not output.exists() and not failure.exists(),'existing_output')
    started=time.monotonic();before={}
    try:
        before=file_pins()
        own=json.loads((BASE/'independent-stage01.json').read_text())
        roots=[json.loads((BASE/('stage-root0'+str(n)+'.json')).read_text()) for n in (1,2)]
        root2pin=sha(BASE/'stage-root02.json');before['stage-root02.json']=root2pin
        need(own['receipt']['status']=='PASS' and all(x['status']=='complete' for x in roots),'successful_inputs')
        equal(own['receipt']['pins_before'],own['receipt']['pins_after'],'independent_input_pins')
        a=load_arrays(own['receipt']['array_file'],own['receipt']['array_schema'],own['receipt']['array_file_sha256'])
        mapped=mapped_arrays(a);diagnostics=[]
        for index,root in enumerate(roots,1):
            equal(root['pins'],root['pins_after'],'root_pins.'+str(index))
            source_receipts(own,root)
            r=root['result'];b=load_arrays(r['array_archive'],r['arrays'],r['array_archive_sha256'])
            need(mapped.keys()==b.keys(),'root_all_array_coverage')
            for key,value in mapped.items():equal_array(value,b[key],'root'+str(index)+'.'+key)
            need(np.array_equal(np.isnan(a['slave_segment_attributes']),a['slave_segment_attribute_missing']),'own_segment_mask')
            diagnostics.append(compare_metadata(own['result'],a,r,mapped))
        compare_root_pair(*roots)
        equal(diagnostics[0],diagnostics[1],'diagnostics_repeated')
        reruns=rerun_controls();after=file_pins();after['stage-root02.json']=sha(BASE/'stage-root02.json')
        equal(before,after,'fresh_pins_before_after')
        receipt={'status':'PASS','command':sys.argv,'elapsed_seconds':time.monotonic()-started,
          'peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
          'pins_before':before,'pins_after':after,'counts':dict(COUNTS),'mutation_controls':controls,'control_reruns':reruns,
          'diagnostics':diagnostics[0],'comparison_tolerance':'Exact equality of parsed numeric values; no floating tolerance; matching NaN positions required.',
          'scope':'Post-freeze independent output comparison and compressed-source byte hashes; no new raw source reconstruction or physical contact inference.',
          'schema_normalizations':['Own node indices resolved to exact node IDs; node-part-family rows sorted as node/family/effectivePID.',
            'Own master union split using frozen SEG1/SEG3 master membership; all root roles compared.',
            'NSET positive occurrences rebuilt into source-line plus eight slots; absent-positive slots use root zero-padding convention. Own extraction does not distinguish source blank versus numeric zero for omitted NSET slots.',
            'All 742 actual master rows and aliases have four distinct vertices; root node-set aliases therefore equal independent four-slot multiset aliases for this data only.',
            'Source aliases resolved by fixed SRC-to-pinned-basename mapping; numeric JSON integer versus integral-float values compared as exact numeric values.',
            'Root repetition excludes elapsed_seconds and the declared NPZ archive filename only.'],
          'not_dual_verified':['Root full SECTION_SHELL numeric cards beyond first ID/source locator; root PART heading hashes.',
            'Root global ground-discrete counter: no global endpoint arrays retained independently, although the independent parser omits zero endpoints and both global family counts agree.',
            'Independent full 207820 shell and 33059 nonshell element-record arrays beyond root master aliases; incident-shell THIC1-4 extrema; orientation-specific arrays; independent CONTROL_CONTACT cards.',
            'No effective/default contact settings, units/floors, pairing, projection, restraint, capacity or cause are verified.']}
        with output.open('x') as f:json.dump(receipt,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'status':'PASS','output':output.name,'sha256':sha(output),'counts':dict(COUNTS),'controls':len(controls),
           'master_records':diagnostics[0]['master_records'],'part_references':diagnostics[0]['part_references'],'seconds':receipt['elapsed_seconds']},sort_keys=True))
    except Exception as exc:
        record={'status':'FAIL','code':exc.label if isinstance(exc,Mismatch) else type(exc).__name__,'command':sys.argv,
            'elapsed_seconds':time.monotonic()-started,'counts':dict(COUNTS),'pins_before':before,'mutation_controls':controls}
        try:record['pins_after']=file_pins()
        except Exception as later:record['pin_check_error']=later.label if isinstance(later,Mismatch) else type(later).__name__
        with failure.open('x') as f:json.dump(record,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
        print(json.dumps({'status':'FAIL','code':record['code'],'receipt':failure.name},sort_keys=True));raise SystemExit(1) from None


if __name__=='__main__':main()
