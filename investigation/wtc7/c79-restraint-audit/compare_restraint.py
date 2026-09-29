#!/usr/bin/env python3
"""Post-freeze exact graph comparison; no mesh reconstruction or contact expansion."""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import time
import unittest

import verify_restraint as independent

BASE=Path(__file__).resolve().parent
PINS={
    'PROTOCOL.md':'b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d',
    'verify_restraint.py':'5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a',
    'independent01.json':'d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7',
    'map_restraint.py':'4d49ed698f9802a859a364d4f71721d54e1d3511b50bd96f7b02f5ac3bc7b520',
    'root01.json':'f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef',
    'root02.json':'179682c5caf5cdfac31c508d88e545a843fb07839bb7150832333790ed9e90e3',
    '../model-member-map/map_members.py':'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b',
}
SOURCE_ALIASES={p[0]:src for src,p in independent.PINS.items()}
SOURCE_ALIASES['WTC7_CaseB_400pm.int.gz']=118


class ComparisonError(Exception):
    pass


def guard(condition,code):
    if not condition:raise ComparisonError(code)


def padded(row,size):
    guard(len(row)<=size,'card_overflow')
    return row+[None]*(size-len(row))


def transform_card(row,size):
    guard(len(row)>=size and all(x is None for x in row[size:]),'nonblank_transform_padding')
    return row[:size]


class Check:
    def __init__(self):
        self.scalar_counts=Counter()
        self.coordinate_scalars=0
        self.failures=[]

    def same(self,where,got,want,coordinate=False):
        if isinstance(want,dict):
            if not isinstance(got,dict) or set(got)!=set(want):
                self.failures.append({'where':where,'kind':'dictionary_keys'});return
            for key in sorted(want):self.same(where+'.'+str(key),got[key],want[key],coordinate)
        elif isinstance(want,list):
            if not isinstance(got,list) or len(got)!=len(want):
                self.failures.append({'where':where,'kind':'ordered_list_length'});return
            for i,(a,b) in enumerate(zip(got,want)):self.same(where+f'[{i}]',a,b,coordinate)
        else:
            kind='null' if want is None else 'boolean' if isinstance(want,bool) else 'numeric' if isinstance(want,(int,float)) else 'string'
            self.scalar_counts[kind]+=1
            if coordinate:self.coordinate_scalars+=1
            valid=True
            if kind=='numeric':
                valid=isinstance(got,(int,float)) and not isinstance(got,bool) and math.isfinite(got) and math.isfinite(want)
                if coordinate:
                    valid=valid and float(got).hex()==float(want).hex()
                else:valid=valid and got==want
            else:valid=type(got)==type(want) and got==want
            if not valid:self.failures.append({'where':where,'kind':kind,'got':got,'expected':want})


def root_record(row):
    return {'source':SOURCE_ALIASES[row['source']],'line':row['line'],'kind':row['kind'],
            'id':row['eid'],'original_part':row['original_pid'],'effective_part':row['pid'],
            'physical_nodes':list(row['nodes']),'orientation_node':row['orientation_node']}


def own_record(row):
    return {k:row[k] for k in ('source','line','kind','id','original_part','effective_part','physical_nodes','orientation_node')}


def compare_graph(own,root,c,prefix):
    coords={r['nid']:r['xyz'] for r in root['coordinates']}
    guard(len(coords)==len(root['coordinates']),'duplicate_root_coordinate_id')
    own_coords={r['id']:r['xyz'] for r in own['selected_nodes']}
    guard(len(own_coords)==len(own['selected_nodes']),'duplicate_independent_coordinate_id')
    c.same(prefix+'.coordinate_ids',sorted(coords),sorted(own_coords))
    for nid in sorted(own_coords):
        guard(nid in coords,'root_coordinate_missing')
        c.same(prefix+f'.node[{nid}].xyz',coords[nid],own_coords[nid],True)
    for own_key,root_key,is_neighbor in [('seed_elements','seed_records',False),('neighbor_elements','neighbors',True)]:
        expected=own[own_key];actual=root[root_key]
        c.same(prefix+'.'+root_key+'.count',len(actual),len(expected))
        # Explicit identities reject dropped, duplicated or reordered element rows.
        c.same(prefix+'.'+root_key+'.identities',
               [[SOURCE_ALIASES[r['source']],r['kind'],r['eid']] for r in actual],
               [[r['source'],r['kind'],r['id']] for r in expected])
        for i,(r,o) in enumerate(zip(actual,expected)):
            label=prefix+f'.{root_key}[{i}]'
            c.same(label,root_record(r),own_record(o))
            matches=sorted(set(r['nodes']) & set(root['seed_node_ids']))
            c.same(label+'.derived_seed_intersection',matches,o['matched_seed_nodes'])
            if is_neighbor:c.same(label+'.retained_seed_intersection',r['matched_seed_nodes'],o['matched_seed_nodes'])
            for j,nid in enumerate(r['nodes']):
                guard(nid in coords,'element_coordinate_missing')
                c.same(label+f'.vertex[{j}].xyz',coords[nid],o['coordinates'][j],True)
    c.same(prefix+'.seed_nodes',root['seed_node_ids'],own['seed_nodes'])
    c.same(prefix+'.seed_parts',root['partset']['part_ids'],own['seed_parts'])
    total={f'{independent.PINS[int(src)][0]}:{kind}':n for src,counts in own['coverage'].items() for kind,n in counts.items()}
    c.same(prefix+'.all_elements',root['all_element_counts'],total)
    c.same(prefix+'.all_nodes',root['unique_model_nodes'],own['counts']['all_input_nodes'])
    c.same(prefix+'.orientation_only_count',len(root['orientation_only_candidates']),own['counts']['orientation_only_beams_excluded'])
    c.same(prefix+'.incident_parts',len(root['part_definitions']),own['counts']['incident_parts_including_seed'])
    c.same(prefix+'.seed_bounds',root['seed_bounds'],
           [[b[0] for b in own['seed_coordinate_bounds_by_axis']],[b[1] for b in own['seed_coordinate_bounds_by_axis']]],True)


def compare_metadata(own,root,c,prefix):
    a,b=root['diagnostic'],own['diagnostic']
    c.same(prefix+'.diagnostic',
           {'source':SOURCE_ALIASES[a['source']],'keyword_line':a['line'],'id':a['plane_id'],
            'column':a['column_number'],'psid':a['psid'],'cards':[padded(a['plane_card'],8),padded(a['second_plane_card'],8)]},
           {'source':b['source'],'keyword_line':b['keyword_line'],'id':b['id'],
            'column':b['column'],'psid':b['cards'][0]['card'][0],'cards':[x['card'] for x in b['cards']]})
    a,b=root['partset'],own['part_set']
    c.same(prefix+'.partset',{'source':SOURCE_ALIASES[a['source']],'keyword_line':a['line'],'members':a['part_ids'],'id':root['diagnostic']['psid']},
           {'source':b['source'],'keyword_line':b['keyword_line'],'members':b['members'],'id':b['id']})
    a=[{'source':SOURCE_ALIASES[x['source']],'target':SOURCE_ALIASES[x['included']],
        'keyword_line':x['line'],'kind':x['kind'].removeprefix('*')} for x in root['include_graph']]
    b=[{'source':x['source'],'target':x['target_source'],'keyword_line':x['keyword_line'],'kind':x['keyword']} for x in own['include_graph']]
    key=lambda x:(x['source'],x['keyword_line'])
    c.same(prefix+'.includes',sorted(a,key=key),sorted(b,key=key))
    b=[x for x in own['include_graph'] if x['keyword']=='INCLUDE_TRANSFORM']
    c.same(prefix+'.transform_count',len(root['transforms']),len(b))
    for i,(a,b) in enumerate(zip(root['transforms'],b)):
        c.same(prefix+f'.transform[{i}]',
               {'source':SOURCE_ALIASES[a['source']],'keyword_line':a['line'],
                'cards':[transform_card(row,n) for row,n in zip(a['cards'],[7,1,5,1])]},
               {'source':b['source'],'keyword_line':b['keyword_line'],'cards':[x['card'] for x in b['transform_cards']]})
        c.same(prefix+'.transform_card_count',len(a['cards']),4)
        c.same(prefix+'.geometry_identity_description',a['coordinate_transform'],'identity')
    expected=[]
    for p in own['incident_part_references']:
        guard(p['status']=='supplied_part_definition','unsupported_missing_own_part_adapter')
        guard(p['material_status']=='resolved','unsupported_material_status_adapter')
        expected.append({'source':p['source'],'line':p['line'],'original_pid':p['card'][0],
                        'original_section_id':p['card'][1],'original_material_id':p['card'][2],
                        'pid':p['effective_part'],'section_id':p['effective_section'],
                        'material_id':p['effective_material'],'section_defined':p['section_status']=='resolved',
                        'material_keyword':'*'+p['material_definitions'][0]['keyword']})
    actual=[{**{k:v for k,v in p.items() if k!='heading_sha256'},'source':SOURCE_ALIASES[p['source']]} for p in root['part_definitions']]
    c.same(prefix+'.part_references',sorted(actual,key=lambda p:p['pid']),sorted(expected,key=lambda p:p['pid']))


def compare_receipts(own,root,c,prefix):
    c.same(prefix+'.status',root['status'],'complete')
    c.same(prefix+'.protocol_pin',root['protocol_sha256'],PINS['PROTOCOL.md'])
    c.same(prefix+'.producer_pin',root['producer_sha256'],PINS['map_restraint.py'])
    c.same(prefix+'.helper_pin',root['helper_sha256'],PINS['../model-member-map/map_members.py'])
    c.same(prefix+'.source_phase_count',len(root['sources']),2)
    first={s['source']:s for s in own['receipt']['streams'] if s['phase']=='metadata_nodes'}
    for phase,rows in root['sources'].items():
        c.same(prefix+'.sources'+phase+'.aliases',sorted(SOURCE_ALIASES[name] for name in rows),[119,120,121])
        for name,row in rows.items():
            src=SOURCE_ALIASES[name];pin=independent.PINS[src]
            c.same(prefix+'.sources'+phase+'.'+str(src),row,
                   {'compressed_bytes':pin[1],'compressed_sha256':pin[2],'eof':True,'lines':first[src]['lines'],
                    'pin_after':True,'uncompressed_bytes':pin[3],'uncompressed_sha256':pin[4]})


def comparer_controls():
    base={'source':'wtc7_global_8a_no-conn-matl.k.gz','line':12,'kind':'shell','eid':17,
          'original_pid':179,'pid':179,'nodes':[1,2,2,3],'orientation_node':None}
    normalized=root_record(base);out=[]
    def detects(name,changed):
        c=Check();c.same(name,root_record(changed),normalized)
        guard(bool(c.failures),'control_did_not_detect_'+name);out.append({'name':name,'status':'PASS'})
    for name,key,value in [('source_line','line',13),('element_id','eid',18),('family','kind','beam'),
                           ('original_namespace','original_pid',180),('effective_namespace','pid',1179),
                           ('vertex_order','nodes',[2,1,2,3]),('repeated_vertex_dropped','nodes',[1,2,3]),
                           ('orientation_field','orientation_node',99)]:
        changed=copy.deepcopy(base);changed[key]=value;detects(name,changed)
    changed=copy.deepcopy(base);changed['source']='elem_thick_to-renum.k.gz';detects('source_alias',changed)
    c=Check();c.same('seed_intersection',[1,1],[1]);guard(c.failures,'duplicate_match_control');out.append({'name':'seed_intersection_duplicate','status':'PASS'})
    c=Check();c.same('coordinate',[1.,2.,3.],[1.,2.,math.nextafter(3.,4.)],True)
    guard(c.failures,'ulp_coordinate_control');out.append({'name':'one_ulp_coordinate_difference','status':'PASS'})
    c=Check();c.same('boolean_not_id',True,1);guard(c.failures,'bool_id_control');out.append({'name':'boolean_not_numeric_id','status':'PASS'})
    c=Check();c.same('exact_numeric_card',[179.,None],[179,None]);guard(not c.failures,'numeric_representation_control')
    out.append({'name':'exact_integral_float_card_alias','status':'PASS'})
    try:transform_card([0,None,3],1)
    except ComparisonError:out.append({'name':'nonblank_padding_rejected','status':'PASS'})
    else:raise ComparisonError('padding_control')
    guard(base['nodes']==[1,2,2,3] and root_record(base)==normalized,'comparison_mutated_fixture')
    out.append({'name':'fixture_not_mutated','status':'PASS'})
    return out


def root_controls():
    spec=importlib.util.spec_from_file_location('reviewed_root_restraint_controls',BASE/'map_restraint.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(module.m.Controls),
                             unittest.defaultTestLoader.loadTestsFromTestCase(module.Controls)])
    result=unittest.TestResult();suite.run(result)
    guard(result.wasSuccessful(),'root_controls_failed')
    return {'run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}


def pins():
    got={name:independent.sha(BASE/name) for name in PINS}
    guard(got==PINS,'frozen_artifact_pin_changed')
    got['comparison_code']=independent.sha(Path(__file__))
    # Compressed-only integrity reread, not a new mesh or source-body scan.
    for src,pin in independent.PINS.items():
        path=independent.SOURCE/pin[0]
        guard(path.stat().st_size==pin[1] and independent.sha(path)==pin[2],'compressed_source_pin_changed')
        got['source_'+str(src)]=pin[2]
    return got


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True);args=ap.parse_args()
    guard(Path(args.output).name==args.output and args.output.endswith('.json'),'output_basename')
    output=BASE/args.output;guard(not output.exists(),'output_exists')
    started=time.monotonic();before=pins();tests=comparer_controls()
    own=json.loads((BASE/'independent01.json').read_text());roots=[json.loads((BASE/f'root0{i}.json').read_text()) for i in (1,2)]
    c=Check();c.same('own_status',own['receipt']['status'],'PASS')
    c.same('own_before_after_pins',own['receipt']['pins_before'],own['receipt']['pins_after'])
    c.same('own_stream_count',len(own['receipt']['streams']),9)
    for row in own['receipt']['streams']:c.same('own_eof',row['eof'],True)
    pair_keys=[k for k in sorted(set(roots[0])|set(roots[1])) if roots[0].get(k)!=roots[1].get(k)]
    c.same('root_pair_differences',pair_keys,['elapsed_seconds'])
    for i,r in enumerate(roots,1):
        compare_graph(own['result'],r['result'],c,f'root0{i}')
        compare_metadata(own['result'],r['result'],c,f'root0{i}')
        compare_receipts(own,r,c,f'root0{i}')
    own_tests=independent.controls();root_tests=root_controls()
    for i,r in enumerate(roots,1):c.same(f'root0{i}.controls_replay',root_tests,r['controls'])
    after=pins();guard(before==after,'pins_changed_during_comparison')
    status='PASS' if not c.failures else 'FAIL'
    result={'status':status,'scalar_comparisons':dict(c.scalar_counts),'coordinate_scalar_comparisons':c.coordinate_scalars,
            'tolerance':'none; coordinate binary64 hex equality; other finite numeric values exact',
            'root_pair_different_fields':pair_keys,'failures':c.failures,
            'coverage_per_root':{'seed_elements':952,'neighbor_elements':20,'selected_node_coordinates':891,
                'seed_node_ids':873,'part_references':2,'include_edges':3,'transform_cards':4,'geometry_count_groups':5},
            'normalizations':['Preserved source filename to approved SRC alias.','Element/part field-name aliases; record order and repeated vertex slots unchanged.',
                'Diagnostic/set/include root line denotes keyword line, matched to independent keyword_line.',
                'Plane first-card omitted trailing blank padded with None; transform fixed-width trailing slots required None before trimming.',
                'Exact integer-valued float metadata allowed to equal integer numeric value; no rounding/tolerance.',
                'Root min/max vectors transposed from independent per-axis bounds.'],
            'not_independently_compared':['Root CONTACT/NSET inventories and TC/RC fields, including global nonzero constraint-field count.',
                '891 node source/line locators retained only by independent output; root coordinate schema omits them.',
                'Independent shell thickness/continuation cards and individual diagnostic/part-set/transform card row locators omitted by root.',
                'Heading hashes use different recipes: root hashes ID+heading card, independent hashes stripped heading; part headings absent independently.',
                'Independent full PART cards and section/material definition line locators beyond common reference fields omitted by root.',
                'Seed intersections and per-element coordinates are derived from retained root nodes/global coordinates, not separate root output fields.'],
            'independence':'Independent extraction froze before root outputs/code access. Root had received independent summary counts/part1179 conclusion before root code freeze, but not arrays/code; algorithmic independence, not blind count discovery.',
            'interpretation':'Shared-node graph reproducibility only; no contact expansion, directional restraint, stiffness, capacity, historical state or cause.'}
    receipt={'status':status,'command':[sys.executable,*sys.argv],'elapsed_seconds':time.monotonic()-started,
             'pins_before':before,'pins_after':after,'comparer_controls':tests,'independent_controls_replayed':own_tests,
             'root_controls_replayed':root_tests,'comparison':result,
             'controls_limit':'Root27 includes17 prior helper tests and10 graph tests. Actual selected elements are shells; no blanket parser branch, beam/ground-discrete-neighbor, contact or physical verification claim.'}
    with output.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':status,'sha256':independent.sha(output),'scalar_comparisons':dict(c.scalar_counts),
                      'coordinate_scalars':c.coordinate_scalars,'failures':len(c.failures),'comparer_controls':len(tests)}))
    return 0 if status=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except ComparisonError as exc:
        print(json.dumps({'status':'FAIL','code':str(exc)}));raise SystemExit(1)
