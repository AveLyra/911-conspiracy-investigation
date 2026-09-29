#!/usr/bin/env python3
"""Read-only, bounded typed-card inventory; not an LS-DYNA interpreter."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import time
import unittest

BASE = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PINS = {
    'SRC-116': ('Damage_Global_ANSYS_CaseB_4.0hr.k.gz', 5331, '982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da'),
    'SRC-119': ('discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7'),
    'SRC-120': ('elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59'),
    'SRC-121': ('wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d'),
}
MATS = {b'*MAT_PIECEWISE_LINEAR_PLASTICITY', b'*MAT_ELASTIC_VISCOPLASTIC_THERMAL',
        b'*MAT_RIGID', b'*MAT_SPRING_NONLINEAR_ELASTIC', b'*MAT_ELASTIC',
        b'*MAT_PLASTICITY_COMPRESSION_TENSION'}
SECS = {b'*SECTION_SHELL', b'*SECTION_BEAM', b'*SECTION_SOLID', b'*SECTION_DISCRETE'}
ELEMS = {b'*ELEMENT_BEAM': 'beam', b'*ELEMENT_DISCRETE': 'discrete',
         b'*ELEMENT_SHELL_THICKNESS': 'shell', b'*ELEMENT_SOLID': 'solid'}
SETS = {b'*SET_SHELL_LIST': 'shell', b'*SET_BEAM': 'beam', b'*SET_BEAM_LIST': 'beam'}
INCS = {b'elem_thick_to-renum.k': 'SRC-120', b'discrete_mass.k': 'SRC-119',
        b'WTC7_CaseB_400pm.int': 'SRC-118'}
MISSING_SELECTION = {25,33,711,712,713,723,731,733,741,742,743,751,761,762,763,772,773,802,803}

class AuditError(Exception):
    pass

def check(condition, code):
    if not condition:
        raise AuditError(code)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def row(raw, widths):
    if b',' in raw:
        cells = raw.split(b',')
        check(len(cells) <= len(widths), 'csv_too_many_fields')
        cells += [b''] * (len(widths) - len(cells))
    else:
        cells, p = [], 0
        for w in widths:
            cells.append(raw[p:p+w]); p += w
        check(not raw[p:].strip(), 'fixed_trailing_data')
    result = []
    for c in cells:
        c = c.strip()
        if not c:
            result.append(None); continue
        check(re.fullmatch(rb'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?', c) is not None,
              'non_numeric_field')
        val = float(c.replace(b'D', b'E').replace(b'd', b'e'))
        check(math.isfinite(val), 'nonfinite_value')
        result.append(val)
    return result

def ident(v):
    check(v is not None and v > 0 and int(v) == v, 'invalid_positive_id')
    return int(v)

def insert(target, idx, value):
    check(idx not in target, 'duplicate_definition')
    target[idx] = value

def effective(v, offset):
    return ident(v) + offset if v not in (None, 0) else 0

def lines(alias, receipts):
    name, size, pin = PINS[alias]
    path = BASE / name
    check(path.stat().st_size == size and sha(path) == pin, 'source_pin_before')
    h = hashlib.sha256(); count = total = 0
    with gzip.open(path, 'rb') as f:
        while True:
            raw = f.readline(16385)
            if not raw: break
            count += 1; total += len(raw)
            check(len(raw) <= 16384 and total <= 512*1024*1024, 'source_limit')
            h.update(raw)
            yield count, raw.rstrip(b'\r\n')
    check(path.stat().st_size == size and sha(path) == pin, 'source_pin_after')
    receipts[alias] = dict(compressed_bytes=size, compressed_sha256=pin,
        uncompressed_bytes=total, uncompressed_sha256=h.hexdigest(), lines=count, eof=True)

class Map:
    def __init__(self):
        self.parts = {}; self.mats = {}; self.sections = {}; self.curves = {}
        self.counts = defaultdict(Counter); self.source_counts = defaultdict(Counter)
        self.includes = []; self.deletes = []; self.receipts = {}
        self.targets = {}; self.matches = []; self.keywords = defaultdict(Counter)
        self.curve_blocks = []; self.ignored = defaultdict(Counter)

    def metadata(self, alias, key, start, cards, offset):
        loc = dict(source=alias, keyword=key.decode('ascii'), keyword_line=start)
        if key in (b'*INCLUDE', b'*INCLUDE_TRANSFORM'):
            check(cards and cards[0][1].strip() in INCS, 'include_not_allowlisted')
            inc = dict(**loc, included=INCS[cards[0][1].strip()])
            if key == b'*INCLUDE_TRANSFORM':
                check(len(cards) == 5 and inc['included'] == 'SRC-120', 'transform_shape')
                nums = [row(v, [10]*8) for _,v in cards[1:]]
                check(nums[0][:7] == [0,0,1000,1000,0,0,0] and nums[1][0] == 1000
                      and nums[2][:3] == [1,1,1] and (nums[3][0] or 0) == 0, 'transform_values')
                inc['cards'] = [dict(line=n, values=r) for (n,_),r in zip(cards[1:], nums)]
            else: check(len(cards) == 1, 'include_shape')
            self.includes.append(inc); return
        if key in SETS:
            check(cards, 'missing_set_header')
            values = [row(v,[10]*8) for _,v in cards]
            check(values[0][0] == 2, 'unexpected_set')
            kind = SETS[key]; check(kind not in self.targets, 'duplicate_set')
            ids = [ident(x) for vals in values[1:] for x in vals if x not in (None,0)]
            check(len(ids) == len(set(ids)), 'duplicate_set_id')
            self.targets[kind] = {i for i in ids}; return
        if key == b'*PART':
            check(len(cards) == 2, 'part_shape')
            loc['title_sha256'] = hashlib.sha256(cards[0][1]).hexdigest()
            nums = row(cards[1][1], [10]*8)
            obj = dict(**loc, card_line=cards[1][0], values=nums, original_pid=ident(nums[0]),
                       pid=effective(nums[0],offset), sid=effective(nums[1],offset),
                       mid=effective(nums[2],offset), id_offset=offset)
            insert(self.parts,obj['pid'],obj); return
        if key in MATS or key in SECS:
            check(cards, 'empty_definition')
            nums = [dict(line=n, values=row(v,[10]*8)) for n,v in cards]
            raw_id = ident(nums[0]['values'][0]); idx = raw_id+offset
            obj = dict(**loc, original_id=raw_id, effective_id=idx, id_offset=offset, cards=nums)
            insert(self.mats if key in MATS else self.sections,idx,obj); return
        if key == b'*DEFINE_CURVE':
            check(cards, 'curve_empty')
            header = row(cards[0][1],[10]*8)
            cid = ident(header[0])
            # Curve namespace has no offset in the explicit SRC-120 transform.
            vals = [dict(line=n, values=row(v,[20]*2)) for n,v in cards[1:]]
            insert(self.curves,cid,dict(**loc, curve_id=cid, header_line=cards[0][0],
                                       header_values=header, points=vals))

    def parse(self, alias, source, offset=0):
        key = b''; cards=[]; start=0; keep=False; pending=False; ended=False
        for lineno,raw in source:
            s=raw.strip()
            if s.startswith(b'$'): continue
            check(not ended or not s,'data_after_end')
            if s.startswith(b'*'):
                check(not pending,'incomplete_shell')
                if keep: self.metadata(alias,key,start,cards,offset)
                key=s.upper(); start=lineno; cards=[]
                for prefix,allowed in ((b'*MAT_',MATS),(b'*SECTION_',SECS),
                        (b'*ELEMENT_',set(ELEMS)),(b'*PART',{b'*PART'}),
                        (b'*DEFINE_CURVE',{b'*DEFINE_CURVE'})):
                    if key.startswith(prefix): check(key in allowed,'unsupported_required_keyword')
                check(not key.startswith(b'*KEYWORD') or key==b'*KEYWORD','unsupported_global_format')
                keep=key in MATS|SECS|{b'*PART',b'*INCLUDE',b'*INCLUDE_TRANSFORM',b'*DEFINE_CURVE'}
                keep=keep or (alias=='SRC-116' and key in SETS)
                known=keep or key in ELEMS or key in {b'*KEYWORD',b'*END',b'*NODE'}
                if known: self.keywords[alias][key.decode('ascii')]+=1
                else: self.ignored[alias][hashlib.sha256(key).hexdigest()]+=1
                if key.startswith(b'*DELETE_ELEMENT'):
                    check(key in {b'*DELETE_ELEMENT_SHELL',b'*DELETE_ELEMENT_BEAM'},'unknown_delete')
                    self.deletes.append(dict(source=alias,line=lineno,keyword=key.decode('ascii')))
                ended=key==b'*END'; continue
            if keep:
                cards.append((lineno,raw)); check(len(cards)<=10000,'metadata_cap')
            if not s or key not in ELEMS: continue
            kind=ELEMS[key]
            if kind=='shell' and pending:
                vals=row(raw,[16]*5)
                check(all(v is not None and v>=0 for v in vals[:4]),'invalid_thickness')
                pending=False; continue
            widths=[8]*5+[16,8,16] if kind=='discrete' else [8]*10
            vals=row(raw,widths)
            eid,pid=ident(vals[0]),effective(vals[1],offset)
            if kind=='shell':
                check(not any(v for v in vals[6:]),'unsupported_shell_nodes')
                pending=True
            take={'shell':6,'beam':5,'solid':10,'discrete':4}[kind]
            check(all(v is not None and int(v)==v and v>0 for v in vals[:take]),'element_ids')
            self.counts[pid][kind]+=1; self.source_counts[alias][kind]+=1
            sel=kind if kind in ('shell','beam') else ('beam' if kind=='discrete' else None)
            if eid in self.targets.get(sel,set()):
                self.matches.append(dict(source=alias,line=lineno,kind=kind,eid=eid,pid=pid,
                    values=vals,selection='same_family' if sel==kind else 'cross_family_candidate'))
        check(not pending,'incomplete_shell_eof')
        if keep: self.metadata(alias,key,start,cards,offset)

    def result(self):
        check(set(self.counts)<=set(self.parts),'undefined_used_part')
        missing_parts=[p for p in sorted(self.counts) if self.parts[p]['mid'] not in self.mats]
        missing_mids=sorted({self.parts[p]['mid'] for p in missing_parts})
        selected=missing_parts+[98]
        check(set(missing_mids)==MISSING_SELECTION,'selection_changed')
        counterparts=[m for m,v in self.mats.items() if v['id_offset'] and v['original_id'] in missing_mids]
        selected_mats=set(counterparts)|{self.parts[98]['mid']}
        used=[dict(pid=p,mid=self.parts[p]['mid'],sid=self.parts[p]['sid'],
                   elements=dict(v), material_defined=self.parts[p]['mid'] in self.mats,
                   section_defined=self.parts[p]['sid'] in self.sections)
              for p,v in sorted(self.counts.items())]
        return dict(receipts=self.receipts,include_cards=self.includes,active_delete_cards=self.deletes,
            inventory=dict(parts=len(self.parts),materials=len(self.mats),sections=len(self.sections),
                           curves=len(self.curves),used_parts=len(self.counts),
                           per_source_elements={k:dict(v) for k,v in self.source_counts.items()}),
            all_part_references=[self.parts[p] for p in sorted(self.parts)],used_parts=used,
            material_id_index=[{k:v[k] for k in ('source','keyword','keyword_line','original_id','effective_id','id_offset')}
                               for _,v in sorted(self.mats.items())],
            missing_used_material_ids=missing_mids,missing_used_parts=missing_parts,
            selected_parts=[dict(part=self.parts[p],section=self.sections.get(self.parts[p]['sid']),
                                 elements=dict(self.counts[p])) for p in selected],
            selected_materials=[self.mats[m] for m in sorted(selected_mats)],
            transformed_same_original_id_candidates=sorted(counterparts),
            curve_inventory=[self.curves[i] for i in sorted(self.curves)],
            damage_counts={k:len(v) for k,v in self.targets.items()},
            damage_matches=sorted(self.matches,key=lambda v:(v['kind'],v['eid'])),
            keyword_counts={k:dict(v) for k,v in self.keywords.items()},
            uninterpreted_keyword_hash_counts={k:dict(v) for k,v in self.ignored.items()},
            limits=['static_inventory_not_solver_interpretation','curve_ids_not_material_substitutes',
                    'SRC118_thermal_only_dependency_not_rescanned','unknown_keywords_not_interpreted'])

class Controls(unittest.TestCase):
    def test_fixed(self): self.assertEqual(row(b'         1          ',[10,10]),[1,None])
    def test_csv(self): self.assertEqual(row(b'1,,2',[10]*4),[1,None,2,None])
    def test_nonfinite(self):
        with self.assertRaises(AuditError): row(b'1e999',[10])
    def test_duplicate(self):
        with self.assertRaises(AuditError): insert({1:3},1,4)
    def test_offset(self):
        self.assertEqual([effective(25,1000),effective(0,1000),effective(None,1000)],[1025,0,0])
    def test_shell_pair(self):
        m=Map(); m.parse('test',enumerate([b'*ELEMENT_SHELL_THICKNESS',b'1,25,1,2,3,4',b'0.1,0.1,0.1,0.1',b'*END'],1))
        self.assertEqual(dict(m.counts[25]),{'shell':1})
    def test_shell_missing(self):
        with self.assertRaises(AuditError): Map().parse('test',enumerate([b'*ELEMENT_SHELL_THICKNESS',b'1,25,1,2,3,4',b'*END'],1))
    def test_comment_unused(self):
        m=Map(); m.parse('test',enumerate([b'$*MAT_ELASTIC',b'*PART',b'title',b'1,1,1',b'*END'],1))
        self.assertEqual((len(m.parts),len(m.mats),len(m.counts)),(1,0,0))
    def test_curve_namespace(self):
        m=Map(); m.parse('test',enumerate([b'*DEFINE_CURVE',b'25',b'0,0',b'1,1',b'*END'],1),1000)
        self.assertEqual(list(m.curves),[25])
    def test_unknown_required(self):
        with self.assertRaises(AuditError): Map().parse('test',[(1,b'*MAT_UNKNOWN')])
    def test_data_after_end(self):
        with self.assertRaises(AuditError): Map().parse('test',[(1,b'*END'),(2,b'123')])

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
    check(not args.output.exists(),'output_exists')
    t=time.monotonic(); suite=unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
    result=unittest.TestResult(); suite.run(result)
    check(result.wasSuccessful(),'synthetic_controls_failed')
    m=Map()
    for alias in ('SRC-116','SRC-121','SRC-120','SRC-119'):
        m.parse(alias,lines(alias,m.receipts),1000 if alias=='SRC-120' else 0)
    output=m.result(); output['controls_passed']=result.testsRun
    output['producer_sha256']=sha(Path(__file__))
    output['elapsed_seconds']=time.monotonic()-t
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f: json.dump(output,f,sort_keys=True,indent=2); f.write('\n')
    print(json.dumps(dict(output_sha256=sha(args.output),controls=result.testsRun,
                         missing_parts=len(output['missing_used_parts']),
                         missing_materials=len(output['missing_used_material_ids']),
                         seconds=output['elapsed_seconds'])))

if __name__=='__main__':
    try: main()
    except AuditError as e: raise SystemExit(str(e)) from None
