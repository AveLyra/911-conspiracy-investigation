"""Declared three-clock post-result diagnostic; never repairs original outputs."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
from reconcile import reconcile

ROOT=Path(__file__).resolve().parent
CLOCKS={'30':F(30),'30000/1001':F(30000,1001),'2997/100':F(2997,100)}


def row_check(previous,following,printed,span):
    calculated=(F(following)-F(previous))/span
    residual=F(printed)-calculated
    bound=F('.010')/span+F('.005')
    return {'calculated_fraction':str(calculated),'residual_fraction':str(residual),
            'bound_fraction':str(bound),'compatible':abs(residual)<=bound}


def synthetic_tests():
    for span in [12/rate for rate in CLOCKS.values()]:
        # An unrounded exact synthetic line is used only to test the formula.
        test=row_check(F(12),F(12)-3*span,F(-3),span)
        assert test['residual_fraction']=='0' and test['compatible']
        bound=F(test['bound_fraction'])
        assert row_check(F(12),F(12)-3*span,F(-3)+bound,span)['compatible']
        assert not row_check(F(12),F(12)-3*span,F(-3)+bound+F(1,1000000),span)['compatible']
    return {'cases':9,'status':'pass'}


def calculate(rows):
    indexed={F(r['time_s']):r for r in rows}; result=[]; unsupported=[]
    for track in ['ne','ec','wc','nw']:
        for r in rows:
            if r[track+'_v'] is None: continue
            t=F(r['time_s']); p=indexed.get(t-F('.2')); n=indexed.get(t+F('.2'))
            if p is None or n is None or p[track+'_y'] is None or n[track+'_y'] is None:
                unsupported.append({'track':track,'row':r['row'],'time_s':r['time_s']}); continue
            for label,rate in CLOCKS.items():
                span=12/rate
                result.append({'track':track,'row':r['row'],'time_s':r['time_s'],'rate_hypothesis':label,
                               'centered_span_fraction':str(span),**row_check(p[track+'_y'],n[track+'_y'],r[track+'_v'],span)})
    return {'rows':result,'unsupported':unsupported,'synthetic_tests':synthetic_tests(),
            'summary':{label:{'checked':sum(x['rate_hypothesis']==label for x in result),
                              'failures':sum(x['rate_hypothesis']==label and not x['compatible'] for x in result)} for label in CLOCKS}}


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
    assert reconcile()['status']=='exact_agreement'
    data=json.loads((ROOT/'transcription-root/table47.json').read_text())
    result=calculate(data['rows'])
    result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['addendum_sha256']=hashlib.sha256((ROOT/'CLOCK-ADDENDUM.md').read_bytes()).hexdigest()
    result['source_table_sha256']=hashlib.sha256((ROOT/'transcription-root/table47.json').read_bytes()).hexdigest()
    with args.output.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'summary':result['summary'],'synthetic_tests':result['synthetic_tests']}))
