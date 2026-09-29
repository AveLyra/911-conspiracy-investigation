#!/usr/bin/env python3
"""Typed contact/set incidence only; does not initialize or run contact."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest

HERE=Path(__file__).resolve().parent
HELPER=HERE.parent/'model-member-map/map_members.py'
HELPER_SHA='f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
PROTOCOL_SHA='f367dab9cf29f4958afed5a354a37bfcf1d5cb0f92e8fc39aab3009c2e529c80'
SEED_SHA='f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest()==HELPER_SHA
spec=importlib.util.spec_from_file_location('pinned_numeric_reader',HELPER)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CONTACTS={b'*CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET',
          b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET',
          b'*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID'}
SETS={b'*SET_NODE_LIST':'node',b'*SET_SEGMENT':'segment',b'*SET_PART_LIST':'part'}


def row_values(raw):
    values=m.values_card(raw,10,8)
    m.require(len(values)<=8,'numeric_card_width')
    return values+[None]*(8-len(values))


def int_value(value,default=0):
    if value is None:return default
    m.require(not isinstance(value,bool) and int(value)==value,'integer_expected')
    return int(value)


def heading_id(raw):
    first=raw.split(b',',1)[0] if b',' in raw else raw[:10]
    value=m.integer(first)
    m.require(value is not None and value>0,'contact_id_missing')
    return value


class Scanner:
    def __init__(self,nodes,parts,faces):
        self.seed_nodes=set(nodes); self.seed_parts=set(parts)
        self.faces={tuple(row):i for i,row in faces}
        self.face_sets={tuple(sorted(set(row))):i for i,row in faces}
        m.require(len(self.faces)==len(faces) and len(self.face_sets)==len(faces),'ambiguous_seed_face_mapping')
        self.sets={}; self.contacts=[]; self.unknown_families=Counter()

    def scan(self,lines,source,part_offset):
        active=None; block=None; ended=False
        seen_members=set(); all_nodes=set(); segment_keys=set()
        for line,raw in lines:
            s=raw.strip()
            if s.startswith(b'$'):continue
            m.require(not ended or not s,'post_end_content')
            if s.startswith(b'*'):
                if block and active in SETS:
                    block['unique_members']=len(seen_members)
                    block['unique_nodes']=len(all_nodes)
                    block['duplicate_ordered_segment_rows']=block['member_rows']-len(segment_keys) if block['kind']=='segment' else None
                key=s.upper(); active=None; block=None
                if key.startswith(b'*CONTACT'):
                    m.require(key in CONTACTS,'unreviewed_contact_variant')
                    active=key
                elif key.startswith((b'*SET_NODE',b'*SET_SEGMENT',b'*SET_PART')):
                    m.require(key in SETS,'unsupported_set_variant')
                    active=key
                elif key.startswith((b'*CONSTRAINED',b'*BOUNDARY')):
                    raise m.CardError('unexpected_constraint_or_boundary')
                ended=key==b'*END'
                keyword_line=line; seen_members=set(); all_nodes=set(); segment_keys=set()
                continue
            if active is None:continue
            if block is None:
                if active in CONTACTS:
                    cid=heading_id(raw)
                    m.require(not any(c['cid']==cid for c in self.contacts),'duplicate_contact_id')
                    block={'source':source,'keyword':active.decode(),'keyword_line':keyword_line,
                           'heading_line':line,'cid':cid,'heading_sha256':hashlib.sha256(raw).hexdigest(),'cards':[]}
                    self.contacts.append(block)
                else:
                    vals=row_values(raw); sid=int_value(vals[0]); kind=SETS[active]
                    m.require(sid>0 and (kind,sid) not in self.sets,'duplicate_or_missing_set_id')
                    block={'source':source,'keyword_line':keyword_line,'header_line':line,
                           'kind':kind,'sid':sid,'header':vals,'member_rows':0,
                           'member_entries':0,'duplicate_member_entries':0,'selected':[]}
                    self.sets[(kind,sid)]=block
                continue
            vals=row_values(raw)
            if active in CONTACTS:
                m.require(len(block['cards'])<20,'contact_card_cap')
                block['cards'].append({'line':line,'values':vals})
                continue
            if not s:continue
            kind=block['kind']; block['member_rows']+=1
            if kind=='segment':
                vertices=[int_value(v) for v in vals[:4]]
                m.require(all(0<n<m.ID_CAP for n in vertices),'segment_node_id')
                matched=sorted(set(vertices)&self.seed_nodes)
                all_nodes.update(vertices); segment_keys.add(tuple(vertices))
                # Member identity is the ordered four-node segment, not an element ID.
                members=[tuple(vertices)]
                if matched:
                    block['selected'].append({'line':line,'nodes':vertices,'attributes':vals[4:],
                        'matched_seed_nodes':matched,
                        'same_order_seed_eid':self.faces.get(tuple(vertices)),
                        'same_node_set_seed_eid':self.face_sets.get(tuple(sorted(set(vertices))))})
            else:
                raw_ids=[int_value(v) for v in vals if int_value(v)]
                m.require(all(0<n<m.ID_CAP for n in raw_ids),'set_member_id')
                members=[n+part_offset if kind=='part' else n for n in raw_ids]
                if kind=='node':all_nodes.update(members)
                matched=[n for n in members if n in (self.seed_nodes if kind=='node' else self.seed_parts)]
                if matched:block['selected'].append({'line':line,'matched_ids':matched})
            for member in members:
                block['member_entries']+=1
                if member in seen_members:block['duplicate_member_entries']+=1
                seen_members.add(member)
        if block and active in SETS:
            block['unique_members']=len(seen_members); block['unique_nodes']=len(all_nodes)
            block['duplicate_ordered_segment_rows']=block['member_rows']-len(segment_keys) if block['kind']=='segment' else None

    def selection(self,c,side):
        m.require(len(c['cards'])>=3,'contact_mandatory_cards_missing')
        v=c['cards'][0]['values']; master=side=='master'
        sid=int_value(v[1 if master else 0]); typ=int_value(v[3 if master else 2])
        if master and c['keyword']=='*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID':
            m.require(sid==0,'unexpected_single_surface_master')
            return {'type':typ,'sid':sid,'status':'not_applicable_single_surface'}
        kinds={0:'segment',2:'part',4:'node'}
        m.require(typ in kinds and not(master and typ==4),'unreviewed_selection_type')
        obj=self.sets.get((kinds[typ],sid))
        m.require(obj is not None,'missing_typed_selection_set')
        return {'type':typ,'sid':sid,'kind':kinds[typ],'source':obj['source'],
                'keyword_line':obj['keyword_line'],'selected_rows':len(obj['selected']),
                'total_member_rows':obj['member_rows'],'unique_members':obj['unique_members']}

    def result(self):
        return {'sets':[self.sets[k] for k in sorted(self.sets)],
                'contacts':[{**c,'slave_selection':self.selection(c,'slave'),
                             'master_selection':self.selection(c,'master')} for c in self.contacts],
                'scope':'set_membership_not_contact_pairs_or_physical_restraint'}


class Controls(unittest.TestCase):
    def scan(self,lines,nodes=(1,),parts=(179,),faces=((10,(1,2,3,4)),)):
        s=Scanner(nodes,parts,faces); s.scan(enumerate(lines,1),'synthetic',0); return s

    def test_id_header_csv_and_fixed(self):
        self.assertEqual(heading_id(b'3,unexported heading'),3)
        self.assertEqual(heading_id(b'         4unexported heading'),4)

    def test_id_before_offset_and_card_positions(self):
        s=self.scan([b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET',b'3,heading',b'1,2,0,0',b'0',b'0',b'*END'])
        self.assertEqual(s.contacts[0]['cid'],3)
        self.assertEqual(s.contacts[0]['cards'][0]['values'][:4],[1,2,0,0])

    def test_header_not_member_and_duplicates(self):
        s=self.scan([b'*SET_NODE_LIST',b'1,0,0,0,0',b'1,1,2',b'*END'])
        r=s.sets[('node',1)]
        self.assertEqual((r['member_entries'],r['unique_members'],r['duplicate_member_entries']),(3,2,1))
        self.assertEqual(r['selected'][0]['matched_ids'],[1,1])

    def test_namespace_and_part_offset(self):
        s=Scanner({1},{1179},[])
        s.scan(enumerate([b'*SET_PART_LIST',b'1',b'179',b'*SET_NODE_LIST',b'1',b'179',b'*END'],1),'x',1000)
        self.assertEqual(s.sets[('part',1)]['selected'][0]['matched_ids'],[1179])
        self.assertEqual(s.sets[('node',1)]['selected'],[])

    def test_segment_attributes_not_nodes_and_triangle(self):
        s=self.scan([b'*SET_SEGMENT',b'1',b'2,3,4,4,1,1,1,1',b'*END'])
        self.assertEqual(s.sets[('segment',1)]['selected'],[])
        self.assertEqual(s.sets[('segment',1)]['unique_nodes'],3)

    def test_order_and_unordered_face_match_distinct(self):
        s=self.scan([b'*SET_SEGMENT',b'1',b'4,3,2,1,0,0,0,0',b'*END'])
        row=s.sets[('segment',1)]['selected'][0]
        self.assertIsNone(row['same_order_seed_eid']); self.assertEqual(row['same_node_set_seed_eid'],10)

    def test_missing_reference_and_unknown_variant(self):
        s=self.scan([b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET',b'1,h',b'1,2,0,0',b'0',b'0',b'*END'])
        with self.assertRaises(m.CardError):s.result()
        with self.assertRaises(m.CardError):self.scan([b'*SET_NODE_GENERAL'])
        with self.assertRaises(m.CardError):self.scan([b'*CONTACT_UNREVIEWED'])

    def test_single_surface_master_not_missing_set(self):
        s=self.scan([b'*SET_PART_LIST',b'1',b'179',b'*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID',b'1,h',b'1,0,2,0',b'0',b'0',b'*END'])
        self.assertEqual(s.result()['contacts'][0]['master_selection']['status'],'not_applicable_single_surface')

    def test_duplicate_seed_faces_rejected(self):
        with self.assertRaises(m.CardError):
            Scanner({1},{179},[(10,(1,2,3,4)),(11,(4,3,2,1))])


def run(output):
    m.require(output.parent.resolve()==HERE and not output.exists(),'new_unit_output_required')
    m.require(m.digest(HERE/'CONTACT-TRACE-PROTOCOL.md')==PROTOCOL_SHA,'protocol_pin')
    m.require(m.digest(HERE/'root01.json')==SEED_SHA,'seed_pin')
    seed=json.loads((HERE/'root01.json').read_text())['result']
    scanner=Scanner(seed['seed_node_ids'],seed['partset']['part_ids'],
                    [(r['eid'],r['nodes']) for r in seed['seed_records'] if r['kind']=='shell'])
    reader=m.Reader(); started=time.monotonic()
    out={'status':'running','protocol_sha256':PROTOCOL_SHA,'seed_sha256':SEED_SHA,
         'producer_sha256':m.digest(Path(__file__)),'helper_sha256':HELPER_SHA,
         'python':sys.version.split()[0]}
    try:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        tests=unittest.TestResult(); suite.run(tests)
        out['controls']={'run':tests.testsRun,'failures':len(tests.failures),'errors':len(tests.errors)}
        m.require(tests.wasSuccessful(),'controls_failed')
        for name,offset in ((m.MASTER,0),(m.OUTSIDE,1000),(m.MASS,0)):
            scanner.scan(reader.lines(name),name,offset)
            print('contact_scan_complete:'+name,flush=True)
        out.update(status='complete',result=scanner.result())
    except Exception as exc:
        out.update(status='failed',error=exc.code if isinstance(exc,m.CardError) else 'unexpected_'+type(exc).__name__)
    out['sources']=reader.receipts; out['elapsed_seconds']=time.monotonic()-started
    with output.open('x') as stream:
        json.dump(out,stream,indent=2,sort_keys=True,allow_nan=False); stream.write('\n')
    print(json.dumps({'status':out['status'],'error':out.get('error'),'sha256':m.digest(output)}),flush=True)
    return 0 if out['status']=='complete' else 1


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path); p.add_argument('--controls',action='store_true'); a=p.parse_args()
    if a.controls:unittest.main(argv=[sys.argv[0]],exit=True)
    elif a.output:
        try:sys.exit(run(a.output.resolve()))
        except m.CardError as exc:print(json.dumps({'status':'rejected','error':exc.code}));sys.exit(2)
    else:p.error('choose --controls or --output')
