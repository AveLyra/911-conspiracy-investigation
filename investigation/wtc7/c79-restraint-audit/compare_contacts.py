#!/usr/bin/env python3
"""Post-freeze exact typed-contact comparison; no geometry/contact initialization."""
import argparse
from collections import Counter, OrderedDict
import copy
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parent
SOURCE=Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
ALIASES={'discrete_mass.k.gz':119,'elem_thick_to-renum.k.gz':120,
         'wtc7_global_8a_no-conn-matl.k.gz':121}
PINS={
 'CONTACT-TRACE-PROTOCOL.md':'f367dab9cf29f4958afed5a354a37bfcf1d5cb0f92e8fc39aab3009c2e529c80',
 'verify_contacts.py':'bcc87b26b50de22325a36a3da96343e1306230dd91e3efef240d6cece059b91b',
 'independent-contacts01.json':'b30b8ee5435e7cf8ce2ea979245b07fa4b0577606bf97638dbfd76b21043c7c3',
 'verify_restraint.py':'5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a',
 'independent01.json':'d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7',
 'trace_contacts.py':'ba35168bab6391ddd1126433d00047ec18d3f24dde9b4fb4f9250b29241688d8',
 'contacts-root01.json':'04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859',
 'contacts-root02.json':'27d22a353b601d1bf2797ea80f846bebe4d42e8467f663778413897437770ed5',
 'root01.json':'f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef',
 '../model-member-map/map_members.py':'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b',
}
SET_KEYS={'source','keyword_line','header_line','kind','sid','header','member_rows',
          'member_entries','duplicate_member_entries','selected','unique_members',
          'unique_nodes','duplicate_ordered_segment_rows'}
CONTACT_KEYS={'source','keyword','keyword_line','heading_line','cid','heading_sha256',
              'cards','slave_selection','master_selection'}
FAMILIES={'CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET',
          'CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET','CONTACT_AUTOMATIC_SINGLE_SURFACE_ID'}


class ComparisonError(Exception):pass


def guard(ok,code):
    if not ok:raise ComparisonError(code)


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024**2),b''):h.update(chunk)
    return h.hexdigest()


def unique_object(pairs):
    result={}
    for k,v in pairs:
        guard(k not in result,'duplicate_JSON_key');result[k]=v
    return result


def read_json(name):
    return json.loads((BASE/name).read_text(),object_pairs_hook=unique_object,
                      parse_constant=lambda _:(_ for _ in ()).throw(ComparisonError('nonfinite_JSON')))


class Check:
    def __init__(self):self.counts=Counter();self.failures=[]

    def same(self,got,want,path='result'):
        if isinstance(want,dict):
            if not isinstance(got,dict) or set(got)!=set(want):
                self.failures.append({'path':path,'kind':'dictionary_keys'});return
            for k in sorted(want):self.same(got[k],want[k],path+'.'+k)
        elif isinstance(want,list):
            if not isinstance(got,list) or len(got)!=len(want):
                self.failures.append({'path':path,'kind':'ordered_list_length'});return
            for i,(a,b) in enumerate(zip(got,want)):self.same(a,b,path+f'[{i}]')
        else:
            kind='null' if want is None else 'boolean' if type(want) is bool else 'numeric' if type(want) in (int,float) else 'string'
            self.counts[kind]+=1
            if kind=='numeric':
                ok=type(got) in (int,float) and math.isfinite(got) and math.isfinite(want)
                ok=ok and Fraction(got)==Fraction(want)
                # Float slots preserve the source binary64 representation,
                # including signed zero. Integer-vs-float source fields may
                # differ in JSON type but must have exactly equal values.
                if ok and type(got) is float and type(want) is float:
                    ok=got.hex()==want.hex()
            else:ok=type(got) is type(want) and got==want
            if not ok:self.failures.append({'path':path,'kind':kind})


def source_id(name):
    guard(name in ALIASES,'unknown_source_alias');return ALIASES[name]


def normalize_root(result):
    guard(set(result)=={'scope','sets','contacts'},'root_result_schema')
    guard(result['scope']=='set_membership_not_contact_pairs_or_physical_restraint','root_scope')
    sets=[];seen=set()
    for original in result['sets']:
        guard(set(original)==SET_KEYS,'root_set_schema')
        row=copy.deepcopy(original);row['source']=source_id(row['source'])
        key=(row['kind'],row['sid']);guard(key not in seen,'duplicate_typed_set');seen.add(key)
        sets.append(row)
    contacts=[];seen=set()
    for original in result['contacts']:
        guard(set(original)==CONTACT_KEYS,'root_contact_schema')
        row=copy.deepcopy(original);row['source']=source_id(row['source'])
        guard(row['keyword'].startswith('*') and row['keyword'][1:] in FAMILIES,'root_contact_keyword')
        row['keyword']=row['keyword'][1:]
        guard(row['cid'] not in seen,'duplicate_contact');seen.add(row['cid'])
        for key in ('slave_selection','master_selection'):
            if 'source' in row[key]:row[key]['source']=source_id(row[key]['source'])
        contacts.append(row)
    # The frozen producers both sort typed sets by kind/ID. Do not sort here:
    # dropping or reordering a serialized row must remain detectable.
    return {'sets':sets,'contacts':contacts}


def independent_as_common(own,seed):
    seed_nodes=set(seed['seed_nodes']);seed_parts=set(seed['seed_parts'])
    ordered={};unordered={};by_id={}
    for s in seed['seed_elements']:
        guard(s['kind']=='shell','seed_family')
        a=tuple(s['physical_nodes']);b=frozenset(a)
        guard(a not in ordered and b not in unordered and s['id'] not in by_id,'ambiguous_seed_face')
        ordered[a]=s;unordered[b]=s;by_id[s['id']]=s
    def alias(records,nodes,ordered_rule):
        selected=(ordered.get(tuple(nodes)) if ordered_rule else unordered.get(frozenset(nodes)))
        expected=[] if selected is None else [{'source':selected['source'],'line':selected['line'],'element_id':selected['id']}]
        guard(records==expected,'independent_seed_face_source_alias')
        return None if selected is None else selected['id']
    result=[];own_sets={}
    for s in own['sets']:
        kind=s['kind'];key=(kind,s['set_id']);guard(key not in own_sets,'duplicate_independent_set');own_sets[key]=s
        selected=[]
        if kind=='segment':
            for r in s['matching_records']:
                guard(len(r['nodes'])==4 and len(r['attributes'])==4,'segment_slot_width')
                guard(r['matched_seed_nodes']==sorted(set(r['nodes'])&seed_nodes),'independent_seed_intersection')
                selected.append({'line':r['line'],'nodes':r['nodes'],'attributes':r['attributes'],
                    'matched_seed_nodes':r['matched_seed_nodes'],
                    'same_order_seed_eid':alias(r['ordered_seed_shell_matches'],r['nodes'],True),
                    'same_node_set_seed_eid':alias(r['unordered_seed_shell_matches'],r['nodes'],False)})
            entries=s['membership_rows'];unique=s['unique_ordered_node_lists'];duplicate=s['duplicate_ordered_node_rows']
            unique_nodes=s['unique_node_ids'];duplicate_segment=duplicate
        else:
            grouped=OrderedDict();previous=None
            for r in s['matching_records']:
                order=(r['line'],r['slot']);guard(previous is None or previous<order,'member_source_order');previous=order
                offset=1000 if s['source']==120 and kind=='part' else 0
                guard(r['effective_id']==r['original_id']+offset,'part_member_namespace')
                guard(r['effective_id'] in (seed_parts if kind=='part' else seed_nodes),'independent_nonmatching_member')
                grouped.setdefault(r['line'],[]).append(r['effective_id'])
            selected=[{'line':line,'matched_ids':ids} for line,ids in grouped.items()]
            entries=s['member_occurrences'];unique=s['unique_member_ids'];duplicate=s['duplicate_member_occurrences']
            unique_nodes=unique if kind=='node' else 0;duplicate_segment=None
        result.append({'source':s['source'],'keyword_line':s['keyword_line'],'header_line':s['header_line'],
            'kind':kind,'sid':s['set_id'],'header':s['header_card'],'member_rows':s['membership_rows'],
            'member_entries':entries,'unique_members':unique,'duplicate_member_entries':duplicate,
            'unique_nodes':unique_nodes,'duplicate_ordered_segment_rows':duplicate_segment,'selected':selected})
    common_sets={(s['kind'],s['sid']):s for s in result}
    contacts=[]
    for c in own['contacts']:
        guard(len(c['numeric_cards'])==c['numeric_card_count'],'contact_card_count')
        cards=[]
        for i,r in enumerate(c['numeric_cards'],1):
            guard(r['card_index']==i and len(r['card'])==8,'contact_card_order_or_width')
            cards.append({'line':r['line'],'values':r['card']})
        r={'source':c['source'],'keyword':c['keyword'],'keyword_line':c['keyword_line'],
           'heading_line':c['header_line'],'cid':c['id'],
           'heading_sha256':c['id_heading_card_sha256'],'cards':cards}
        guard([s['side'] for s in c['selectors']]==['slave','master'],'selector_sides')
        for sel in c['selectors']:
            side=sel['side'];v=cards[0]['values'];index=0 if side=='slave' else 1
            guard(sel['selector_id']==v[index] and sel['selector_type']==v[index+2] and sel['card_line']==cards[0]['line'],'independent_selector_card')
            if sel['status']=='not_applicable_single_surface_master':
                guard(side=='master' and c['keyword']=='CONTACT_AUTOMATIC_SINGLE_SURFACE_ID' and sel['selector_id']==0,'single_surface_master')
                x={'sid':sel['selector_id'],'type':sel['selector_type'],'status':'not_applicable_single_surface'}
            else:
                guard(sel['status']=='resolved_typed_set' and sel['set_exists'] is True,'unsupported_or_missing_independent_selector')
                key=(sel['set_kind'],sel['selector_id']);guard(key in common_sets,'missing_independent_reference')
                s=common_sets[key];original=own_sets[key]
                guard(sel['set_source']==s['source'] and sel['set_keyword_line']==s['keyword_line'] and sel['set_header_line']==s['header_line'],'independent_selector_locator')
                guard(sel['set_matched_seed_ids']==original['matched_seed_ids'] and sel['set_has_seed_intersection']==original['has_seed_intersection'],'independent_selector_members')
                x={'sid':sel['selector_id'],'type':sel['selector_type'],'kind':sel['set_kind'],
                   'source':s['source'],'keyword_line':s['keyword_line'],'selected_rows':len(s['selected']),
                   'total_member_rows':s['member_rows'],'unique_members':s['unique_members']}
            r[side+'_selection']=x
        contacts.append(r)
    return {'sets':result,'contacts':contacts}


def expected_streams(own):
    guard(own['receipt']['pins_before']==own['receipt']['pins_after'],'independent_pins_changed')
    result={}
    for s in own['receipt']['streams']:
        p=own['receipt']['pins_before'][str(s['source'])]
        guard(s['eof'] is True,'independent_stream_not_EOF')
        result[str(s['source'])]={'compressed_bytes':p['bytes'],'compressed_sha256':p['sha256'],
            'eof':s['eof'],'lines':s['lines'],'pin_after':True,
            'uncompressed_bytes':s['bytes'],'uncompressed_sha256':s['sha256']}
    guard(set(result)=={'119','120','121'},'source_coverage');return result


def pins(own):
    result={}
    for name,want in PINS.items():
        got=digest(BASE/name);guard(got==want,'frozen_artifact_pin');result[name]=got
    result['comparison_code']=digest(Path(__file__))
    for name,src in ALIASES.items():
        p=own['receipt']['pins_before'][str(src)];path=SOURCE/name
        guard(path.stat().st_size==p['bytes'] and digest(path)==p['sha256'],'compressed_source_pin')
        result['SRC-'+str(src)]=dict(p)
    return result


def producer_controls():
    result=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    for name,args,expected in [('verify_contacts.py',['--selftest'],22),('trace_contacts.py',['--controls'],9)]:
        command=[sys.executable,str(BASE/name),*args]
        ran=subprocess.run(command,cwd=BASE,env=env,capture_output=True,text=True,timeout=60)
        guard(ran.returncode==0,'producer_controls_failed')
        if name=='verify_contacts.py':
            parsed=json.loads(ran.stdout);guard(parsed['status']=='PASS' and len(parsed['controls'])==expected and all(c['status']=='PASS' for c in parsed['controls']),'independent_controls_summary')
        else:guard('Ran 9 tests' in ran.stderr and ran.stderr.rstrip().endswith('OK'),'root_controls_summary')
        result.append({'code':name,'controls':expected,'exit_code':ran.returncode,
                       'stdout_sha256':hashlib.sha256(ran.stdout.encode()).hexdigest(),
                       'stderr_sha256':hashlib.sha256(ran.stderr.encode()).hexdigest()})
    return result


def negative_controls(actual,expected):
    result=[]
    def test(name,mutate):
        altered=copy.deepcopy(actual);mutate(altered)
        try:
            c=Check();c.same(normalize_root(altered),expected);rejected=bool(c.failures)
        except (ComparisonError,KeyError,TypeError):rejected=True
        guard(rejected,'negative_control_missed_'+name);result.append({'name':name,'status':'PASS'})
    # Exercise the real post-schema adapter, not a separate mock classifier.
    si=next(i for i,s in enumerate(actual['sets']) if s['kind']=='segment' and s['selected'])
    pi=next(i for i,s in enumerate(actual['sets']) if s['kind']=='part' and s['selected'])
    ni=next(i for i,s in enumerate(actual['sets']) if s['kind']=='node' and not s['selected'])
    test('unknown_field',lambda d:d['sets'][0].update(unexpected_numeric=1))
    test('missing_zero_intersection_set',lambda d:d['sets'].pop(ni))
    test('set_namespace',lambda d:d['sets'][ni].update(kind='segment'))
    test('set_source',lambda d:d['sets'][si].update(source='discrete_mass.k.gz'))
    test('set_header_line',lambda d:d['sets'][si].update(header_line=d['sets'][si]['header_line']+1))
    test('set_header_null_not_zero',lambda d:d['sets'][si]['header'].__setitem__(7,0))
    test('segment_member_semantics',lambda d:d['sets'][si].update(unique_members=d['sets'][si]['unique_nodes']))
    test('ordered_duplicate_count',lambda d:d['sets'][si].update(duplicate_ordered_segment_rows=0))
    test('missing_segment',lambda d:d['sets'][si]['selected'].pop())
    test('segment_source_line',lambda d:d['sets'][si]['selected'][0].update(line=1))
    test('ordered_vertices',lambda d:d['sets'][si]['selected'][0]['nodes'].reverse())
    test('repeated_vertex_not_dropped',lambda d:d['sets'][si]['selected'][0]['nodes'].append(d['sets'][si]['selected'][0]['nodes'][-1]))
    test('attribute_not_null',lambda d:d['sets'][si]['selected'][0]['attributes'].__setitem__(0,None))
    test('seed_intersection',lambda d:d['sets'][si]['selected'][0]['matched_seed_nodes'].pop())
    test('seed_face_alias',lambda d:d['sets'][si]['selected'][0].update(same_order_seed_eid=999999))
    test('part_namespace',lambda d:d['sets'][pi]['selected'][0]['matched_ids'].__setitem__(0,1179))
    test('contact_ID',lambda d:d['contacts'][0].update(cid=999))
    test('contact_keyword',lambda d:d['contacts'][0].update(keyword='*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID'))
    test('contact_heading_hash',lambda d:d['contacts'][0].update(heading_sha256='0'*64))
    test('card_null_not_zero',lambda d:d['contacts'][0]['cards'][0]['values'].__setitem__(4,0))
    test('card_source_line',lambda d:d['contacts'][0]['cards'][0].update(line=1))
    test('card_order',lambda d:d['contacts'][0]['cards'].reverse())
    test('bool_not_integer',lambda d:d['contacts'][0]['cards'][0]['values'].__setitem__(0,True))
    test('selector_type',lambda d:d['contacts'][0]['master_selection'].update(type=4))
    test('selector_ID',lambda d:d['contacts'][0]['master_selection'].update(sid=2))
    test('selector_rows',lambda d:d['contacts'][0]['master_selection'].update(selected_rows=0))
    ai=next(i for i,c in enumerate(actual['contacts']) if c['keyword']=='*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID')
    test('single_surface_master_not_missing',lambda d:d['contacts'][ai]['master_selection'].update(status='missing'))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);args=p.parse_args()
    guard(Path(args.output).name==args.output and args.output.endswith('.json'),'output_basename')
    dest=BASE/args.output;guard(not dest.exists(),'output_exists');start=time.monotonic()
    own=read_json('independent-contacts01.json');before=pins(own)
    out={'status':'RUNNING','command':[sys.executable,*sys.argv],'pins_before':before}
    try:
        guard(own['receipt']['status']=='PASS','independent_not_PASS')
        seed=read_json('independent01.json')['result'];expected=independent_as_common(own['result'],seed)
        root1=read_json('contacts-root01.json');root2=read_json('contacts-root02.json')
        pair=Check();pair.same({k:v for k,v in root1.items() if k!='elapsed_seconds'},
                              {k:v for k,v in root2.items() if k!='elapsed_seconds'},'root_repeat')
        guard(not pair.failures,'root_repeat_difference')
        checks=[]
        for name,root in [('contacts-root01.json',root1),('contacts-root02.json',root2)]:
            guard(root['status']=='complete' and root['controls']=={'run':9,'failures':0,'errors':0},'root_status_controls')
            guard(root['producer_sha256']==PINS['trace_contacts.py'] and root['helper_sha256']==PINS['../model-member-map/map_members.py'] and root['protocol_sha256']==PINS['CONTACT-TRACE-PROTOCOL.md'] and root['seed_sha256']==PINS['root01.json'],'root_receipt_dependency_pin')
            c=Check();c.same(normalize_root(root['result']),expected)
            c.same({str(source_id(k)):v for k,v in root['sources'].items()},expected_streams(own),'source_receipts')
            checks.append({'artifact':name,'status':'PASS' if not c.failures else 'FAIL','scalar_counts':dict(c.counts),'failures':c.failures})
        out['comparisons']=checks
        guard(all(c['status']=='PASS' for c in checks),'source_extractions_disagree')
        out['negative_controls']=negative_controls(root1['result'],expected)
        out['producer_controls_rerun']=producer_controls()
        out.update(status='PASS',root_repeat_equal_except_elapsed=True,
            coverage={'typed_sets':len(expected['sets']),'sets_by_kind':dict(Counter(s['kind'] for s in expected['sets'])),
              'selected_segment_records':sum(len(s['selected']) for s in expected['sets'] if s['kind']=='segment'),
              'selected_nonsegment_rows':sum(len(s['selected']) for s in expected['sets'] if s['kind']!='segment'),
              'zero_intersection_sets':sum(not s['selected'] for s in expected['sets']),
              'contact_records':len(expected['contacts']),'contact_numeric_cards':sum(len(c['cards']) for c in expected['contacts']),
              'contact_numeric_slots':sum(len(r['values']) for c in expected['contacts'] for r in c['cards']),
              'selector_records':2*len(expected['contacts']),'source_EOF_receipt_comparisons_per_root':3},
            numeric_policy='Exact rational numeric equality; float/float slots additionally require identical binary64 hex including signed zero. Boolean is never numeric. No tolerance.',
            aliases=['Source basenames map only to SRC119/120/121; leading keyword asterisk removed.',
              'Root segment member_entries means rows, unique_members means ordered four-node lists, duplicate_member_entries means repeated ordered rows; not node occurrences, full attributes or unordered sets.',
              'Root node/part member_entries and unique_members are ID occurrences/unique IDs. Part unique_nodes is zero by root schema, not an absence of incident geometry.',
              'Independent source/line/EID face records reduce to root EID aliases only after checking them against the frozen seed.',
              'Independent nonsegment matching occurrences group by physical line for root matched_ids, preserving duplicates and within-line order.',
              'Heading hashes both cover the full CID+heading card excluding CR/LF; stripped-heading-only independent hash is excluded.'],
            exclusions=['Independent-only segment full-attribute/unordered duplicate totals and distinct repeated-node counts are not supplied by root; no cross-implementation equality is claimed for them.',
              'Independent membership-row ordinals and nonsegment slot/original-ID details are not root fields. Independent alias checks retain their own consistency but do not invent root source locators.',
              'Independent typed-selector existence/intersection summaries are validated through complete common selected rows and typed references; root does not retain identical summary fields.',
              'No fresh decompressed source/mesh pass in this comparer. Fresh compressed-source hashes before/after and independently retained EOF receipts are checked.',
              'No contact-pair, initialization, force, restraint, floor/direction, solver-version or historical-run validation.'])
    except ComparisonError as exc:out.update(status='FAIL',error=str(exc))
    after=pins(own);guard(before==after,'comparison_pins_changed')
    out.update(pins_after=after,elapsed_seconds=time.monotonic()-start)
    with dest.open('x') as f:json.dump(out,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':out['status'],'error':out.get('error'),'sha256':digest(dest),
                      'coverage':out.get('coverage'),'comparison_scalar_counts':[c['scalar_counts'] for c in out.get('comparisons',[])],
                      'negative_controls':len(out.get('negative_controls',[]))}))
    return 0 if out['status']=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except ComparisonError as exc:print(json.dumps({'status':'FAIL','error':str(exc)}));raise SystemExit(1)
