#!/usr/bin/env python3
"""Exact supplied-table diagnostics, not an LS-DYNA constitutive solver."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import unittest

BASE=Path(__file__).resolve().parent
PINS={
    'ARITHMETIC-PROTOCOL.md':'f43d0df31f06b9d735e01d32c4450ba9dd2dd980efbbc46d61462b41db4fdf56',
    'casea-root01.json':'27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
    'spring-manual-review.md':'7631a2b81bcc0f8c638581fdb083edcd2817e474bfe2df973b52e9a35dbd3aee',
}

def require(ok,code):
    if not ok:raise ValueError(code)

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def pins():
    got={p:sha(BASE/p) for p in PINS};require(got==PINS,'dependency_pin');return got

def q(value):
    require(type(value) in (int,float),'not_numeric')
    f=Fraction(value)
    require(max(f.numerator.bit_length(),f.denominator.bit_length())<=8192,'rational_size')
    return f

def exact(value):
    return {'numerator':str(value.numerator),'denominator':str(value.denominator),'approximation':float(value)}

def default(value,want,zero=False):return want if value is None or (zero and value==0) else value

def sign_counts(values):
    c=Counter('negative' if v<0 else 'positive' if v>0 else 'zero' for v in values)
    return {k:c[k] for k in ('negative','zero','positive')}

def diagnose(curve,force_scale=1):
    h=curve['values'];require(len(h)==8,'curve_header_arity')
    require(default(h[1],0) in (0,1,2) and default(h[6],0) in (0,1) and h[7] is None,'unsupported_curve_header')
    sx=q(default(h[2],1,True));sy=q(default(h[3],1,True));ox=q(default(h[4],0));oy=q(default(h[5],0));scale=q(force_scale)
    require(1<=len(curve['points'])<=10000,'curve_point_count')
    vals=[];points=[]
    for p in curve['points']:
        require(len(p['values'])==2,'point_arity');a,o=map(q,p['values'])
        x=sx*(a+ox);y=scale*sy*(o+oy);vals.append((x,y))
        points.append({'line':p['line'],'raw_values':p['values'],'x':exact(x),'y':exact(y)})
    xs,ys=zip(*vals);dx=[b-a for a,b in zip(xs,xs[1:])];dy=[b-a for a,b in zip(ys,ys[1:])]
    secants=[None if x==0 else y/x for x,y in zip(dx,dy)]
    return {'curve_id':curve['curve_id'],'source':curve['source'],'keyword_line':curve['keyword_line'],
        'header_line':curve['header_line'],'header_values':h,'force_scale':exact(scale),
        'effective_transform':{'SFA':exact(sx),'SFO':exact(sy),'OFFA':exact(ox),'OFFO':exact(oy)},
        'points':points,'point_count':len(points),'x_extrema':[exact(min(xs)),exact(max(xs))],
        'y_extrema':[exact(min(ys)),exact(max(ys))],
        'x_step_signs':sign_counts(dx),'y_step_signs':sign_counts(dy),'x_value_signs':sign_counts(xs),'y_value_signs':sign_counts(ys),
        'strict_x_increase':all(v>0 for v in dx) and bool(dx),'strict_x_decrease':all(v<0 for v in dx) and bool(dx),
        'nondecreasing_y':all(v>=0 for v in dy),'nonincreasing_y':all(v<=0 for v in dy),
        'raw_origin_lines':[p['line'] for p in curve['points'] if p['values']==[0,0]],
        'transformed_origin_lines':[p['line'] for p,(x,y) in zip(curve['points'],vals) if x==0 and y==0],
        'secants':[{'left_line':a['line'],'right_line':b['line'],'dx':exact(x),'dy':exact(y),
                    'slope':None if s is None else exact(s)} for a,b,x,y,s in zip(curve['points'],curve['points'][1:],dx,dy,secants)],
        'defined_secant_signs':sign_counts([s for s in secants if s is not None]),
        'undefined_secants':sum(s is None for s in secants),
        'positive_offset_generated_point_branch':ox>0 and default(h[6],0)==0,
        'limits':'Supplied-point diagnostics only; internal resampling, extrapolation formula, load reversal and failure state are not evaluated.'}

def unique_curves(rows):
    result={}
    for row in rows:
        i=row['curve_id'];require(i not in result,'duplicate_curve_reference');result[i]=row
    return result

def calculate(raw):
    s=raw['result']['springs_numeric_inventory'];cards=s['selected_cards'];curves=unique_curves(s['curve_inventory'])
    deps=[];curveids=set();bygroup=defaultdict(list)
    for pid in (820,821,859):
        part=cards[f'*PART:{pid}'];sec=cards[f'*SECTION_DISCRETE:{pid}'];mat=cards[f'*MAT_SPRING_NONLINEAR_ELASTIC:{pid}']
        require(len(part['cards'])==1 and len(sec['cards'])==2 and len(mat['cards'])==1,'selected_card_count')
        p=part['cards'][0]['values'];m=mat['cards'][0]['values'];v=sec['cards'][0]['values'];v2=sec['cards'][1]['values']
        require(p[:3]==[pid,pid,pid] and all(x in (None,0) for x in p[3:]),'part_reference_or_optional_dependency')
        require(m[0]==pid and all(x is None for x in m[3:]) and v[0]==pid and v[1] in (0,1),'material_or_section_shape')
        require(all(x is None for x in v[6:]+v2[2:]),'section_unused_fields')
        lcd=int(m[1]);lcr=int(default(m[2],0));require(lcd==m[1] and lcr==default(m[2],0),'curve_id_not_integral')
        ids={lcd}|({lcr} if lcr else set());require(ids<=curves.keys(),'missing_curve_dependency');curveids|=ids
        elements=[e for e in s['target_elements'] if e['values'][1]==pid]
        require(elements and s['selected_part_counts'][str(pid)]>=len(elements),'selected_part_coverage')
        for e in elements:
            ev=e['values'];require(len(ev)==8 and ev[4]==0,'unresolved_orientation')
            bygroup[(lcd,lcr,q(default(ev[5],1)))].append(e)
        deps.append({'pid':pid,'part':part,'section':sec,'material':mat,'LCD':lcd,'LCR':lcr,
            'selected_element_ids':[int(e['values'][0]) for e in elements],
            'whole_part_element_count':s['selected_part_counts'][str(pid)],
            'semantic_fields':{'DRO':v[1],'KD':v[2],'V0':v[3],'CL':v[4],'FD':v[5],'CDL':v2[0],'TDL':v2[1]},
            'FD_zero_limit':'Explicit zero is preserved; reviewed pages do not provide a zero/default truth table or historical failure state.'})
    require(len(s['target_elements'])==17 and len({e['values'][0] for e in s['target_elements']})==17,'target_eid_coverage')
    scaled=[]
    for (lcd,lcr,scale),elements in sorted(bygroup.items()):
        d=diagnose(curves[lcd],scale.numerator/scale.denominator)
        # Scales in the pinned input are exact binary64 values; this identity guards conversion.
        require(q(scale.numerator/scale.denominator)==scale,'scale_roundtrip')
        scaled.append({'LCD':lcd,'LCR':lcr,'element_records':elements,'table':d})
    return {'dependencies':deps,'curves':[diagnose(curves[i]) for i in sorted(curveids)],'element_scaled_tables':scaled,
        'scope':'Source-point arithmetic and semantic dependencies; no solver, physical units, capacity, state history or cause.'}

class Tests(unittest.TestCase):
    def curve(self,pts=None,header=None):
        return {'curve_id':7,'source':0,'keyword_line':1,'header_line':2,
                'values':header or [7,0,1,1,0,0,0,None],
                'points':[{'line':i+3,'values':p} for i,p in enumerate(pts or [[-1,-2],[0,0],[1,2]])]}
    def value(self,r):return Fraction(int(r['numerator']),int(r['denominator']))
    def test_offset_before_scale(self):
        r=diagnose(self.curve([[1,2]],[7,0,3,4,5,6,0,None]))
        self.assertEqual([self.value(r['points'][0][k]) for k in ('x','y')],[18,32])
        self.assertTrue(r['positive_offset_generated_point_branch'])
    def test_zero_scale_defaults(self):
        r=diagnose(self.curve(header=[7,0,0,0,0,0,0,None]));self.assertEqual(self.value(r['points'][2]['y']),2)
    def test_element_zero_and_blank(self):
        r=diagnose(self.curve(),default(0,1));self.assertEqual(self.value(r['y_extrema'][1]),0)
        self.assertEqual(default(None,1),1)
    def test_rational_binary_distinction(self):self.assertNotEqual(q(.1),Fraction('0.1'))
    def test_duplicate_x(self):
        r=diagnose(self.curve([[1,2],[1,3]]));self.assertEqual(r['undefined_secants'],1);self.assertIsNone(r['secants'][0]['slope'])
    def test_full_order(self):
        r=diagnose(self.curve([[1,1],[0,0],[-1,-1]]));self.assertTrue(r['strict_x_decrease']);self.assertEqual(r['transformed_origin_lines'],[4])
    def test_slope_signs(self):
        r=diagnose(self.curve([[0,0],[1,2],[2,2],[3,1]]));self.assertEqual(r['defined_secant_signs'],{'negative':1,'zero':1,'positive':1})
    def test_scale_half(self):
        r=diagnose(self.curve(),.5);self.assertEqual(self.value(r['secants'][0]['slope']),1)
    def test_dattyp(self):
        r=diagnose(self.curve(header=[7,0,1,1,2,0,1,None]));self.assertFalse(r['positive_offset_generated_point_branch'])
    def test_duplicate_missing_reference(self):
        with self.assertRaises(ValueError):unique_curves([self.curve(),self.curve()])
        with self.assertRaises(ValueError):require(2 in unique_curves([self.curve()]),'missing_curve')
    def test_non_numeric(self):
        with self.assertRaises(ValueError):q(None)
    def test_header(self):
        with self.assertRaises(ValueError):diagnose(self.curve(header=[7,0,1,1,0,0,2,None]))
    def test_pin_and_output(self):
        with self.assertRaises(ValueError):require(PINS['casea-root01.json']=='0'*64,'pin')
        with self.assertRaises(ValueError):require(not BASE.exists(),'output_exists')

def controls():
    r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests));require(r.wasSuccessful(),'controls_failed')
    return {'count':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--controls',action='store_true');p.add_argument('--output');a=p.parse_args()
    if a.controls:print(json.dumps(controls()));return
    require(a.output and re.fullmatch(r'spring-arithmetic[0-9]+\.json',a.output),'output_scope')
    out=BASE/a.output;require(not out.exists(),'output_exists');before=pins();tests=controls();start=time.monotonic()
    r=json.loads((BASE/'casea-root01.json').read_text());require(r['status']=='PASS','source_receipt_failed')
    inventory=r['result']['springs_numeric_inventory']
    available={c['curve_id'] for c in inventory['curve_inventory']}
    requested=set()
    for pid in (820,821,859):
        fields=inventory['selected_cards'][f'*MAT_SPRING_NONLINEAR_ELASTIC:{pid}']['cards'][0]['values']
        requested.update(int(v) for v in fields[1:3] if v not in (None,0))
    missing=sorted(requested-available)
    if missing:
        result={'missing_from_supplied_DEFINE_CURVE_registry':missing,
            'requested_curve_ids':sorted(requested),'available_curve_count':len(available),
            'historical_curve_evaluations':0,
            'limit':'Alternative definition-family closure is separate. No replacement table, law evaluation or cause inference.'}
        status='UNRESOLVED_DEPENDENCY'
    else:
        result=calculate(r);status='PASS'
    after=pins();require(before==after,'changed_dependency')
    receipt={'status':status,'code_sha256':sha(Path(__file__)),'command':sys.argv,'controls':tests,
        'pins_before':before,'pins_after':after,'elapsed_seconds':time.monotonic()-start,'result':result}
    with out.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':status,'output':out.name,'sha256':sha(out),
        'curves':len(result.get('curves',[])), 'missing_curve_ids':missing}))

if __name__=='__main__':main()
