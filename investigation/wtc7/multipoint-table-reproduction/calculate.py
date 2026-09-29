"""Fixed-protocol arithmetic on published rounded tables; not video measurement."""
import argparse
import hashlib
import itertools
import json
import platform
import re
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from reconcile import reconcile, PINS

ROOT = Path(__file__).resolve().parent
PROTOCOL_SHA = '85c1570d523fa8514e9596ecc36e85bc1299586f0a70b0211c38f3725eb59aac'
RECONCILIATION_SHA = '2aba8ca61b1ef8461654cfcab4b4cd86847660259576a9038aa6015e4ccc0fe6'
TARGETS = {'ne':9.30, 'ec':9.79, 'wc':9.81, 'nw':9.92}
NUMERIC = re.compile(r'-?\d+\.\d+\Z')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def validate_table(d, page):
    expected = ['time_s','ref_x','ref_y','ne_y','ne_v','ec_y','ec_v','wc_y','wc_v','nw_y','nw_v'] if page==47 else [
        'time_s','ref_y','nw_y','nw_relative_y','center_y','center_relative_y','center_adjusted_y','sw_y','sw_relative_y','sw_adjusted_y']
    if d['columns'] != expected or len(d['rows']) != (70 if page==47 else 25):
        raise ValueError('unexpected columns or row count')
    last=None
    for i,r in enumerate(d['rows']):
        if r['page']!=page or r['row']!=i+1: raise ValueError('bad row locator')
        for key in expected:
            value=r[key]
            if value is not None and (not isinstance(value,str) or not NUMERIC.fullmatch(value)):
                raise ValueError('invalid numeric token')
        t=F(r['time_s'])
        if last is not None and t<=last: raise ValueError('nonincreasing time')
        if page==47 and last is not None and t-last!=F('0.2'): raise ValueError('bad grid')
        if page==50 and any(r[k] is None for k in expected): raise ValueError('missing western value')
        last=t
    return d['rows']


def fit(times, values, degree):
    t=np.asarray(times,dtype=float); y=np.asarray(values,dtype=float)
    if len(t)<degree+1 or len(t)!=len(y) or not np.all(np.isfinite(t)) or not np.all(np.isfinite(y)):
        raise ValueError('invalid fit input')
    if len(set(t))!=len(t): raise ValueError('duplicate fit times')
    center=float(t.mean()); x=t-center
    design=np.vander(x,N=degree+1,increasing=True)
    coeff,_,rank,_=np.linalg.lstsq(design,y,rcond=None)
    if rank!=degree+1: raise ValueError('rank deficient')
    factor=-1 if degree==1 else -2
    weights=factor*np.linalg.pinv(design)[degree]
    residual=y-design@coeff
    acceleration=float(factor*coeff[degree])
    half_width=float(.005*np.abs(weights).sum())
    return {'center_s':center,'coefficients_centered':coeff.tolist(),'downward_acceleration':acceleration,
            'acceleration_input_weights':weights.tolist(),'display_rounding_half_width':half_width,
            'display_rounding_interval':[acceleration-half_width,acceleration+half_width],
            'residuals':residual.tolist(),'rmse':float(np.sqrt(np.mean(residual**2))),
            'times_s':t.tolist(),'values':y.tolist(),'n':len(t)}


def windows(rows, track):
    starts=['7.8','8.0','8.2'] if track=='ne' else ['8.0','8.2','8.4']
    ends=['8.8','9.0','9.2'] if track=='ne' else ['10.4','10.6','10.8','11.0']
    result=[('grid',a,b) for a,b in itertools.product(starts,ends)]
    onset='8.0' if track=='ne' else '8.2'
    end=max(F(r['time_s']) for r in rows if r[track+'_v'] is not None)
    result.append(('extended',onset,str(float(end))))
    return result


def camera_fits(rows):
    records=[]
    for track,target in TARGETS.items():
        for category,start,end in windows(rows,track):
            selected=[r for r in rows if F(start)<=F(r['time_s'])<=F(end)]
            if any(r[track+'_y'] is None or r[track+'_v'] is None for r in selected):
                raise ValueError('declared interval contains missing target')
            for family,column,degree in [('velocity','v',1),('position','y',2)]:
                item=fit([r['time_s'] for r in selected],[r[track+'_'+column] for r in selected],degree)
                lo,hi=item['display_rounding_interval']
                records.append({'track':track,'category':category,'family':family,'start_s':start,'end_s':end,
                    'primary':category=='grid' and start==('8.0' if track=='ne' else '8.2') and end==('9.2' if track=='ne' else '10.6'),
                    'source_rows':[r['row'] for r in selected],'reported_target':target,
                    'target_difference':item['downward_acceleration']-target,
                    'display_intervals_overlap':lo<=target+.005 and hi>=target-.005,**item})
    return records


def centered_differences(rows):
    indexed={F(r['time_s']):r for r in rows}; result=[]; unsupported=[]
    for track in TARGETS:
        for r in rows:
            if r[track+'_v'] is None: continue
            t=F(r['time_s']); previous=indexed.get(t-F('.2')); following=indexed.get(t+F('.2'))
            if previous is None or following is None or previous[track+'_y'] is None or following[track+'_y'] is None:
                unsupported.append({'track':track,'time_s':r['time_s'],'row':r['row']}); continue
            calculated=(F(following[track+'_y'])-F(previous[track+'_y']))/F('.4')
            residual=F(r[track+'_v'])-calculated
            result.append({'track':track,'time_s':r['time_s'],'row':r['row'],'calculated_v':float(calculated),
                           'residual_fraction':str(residual),'residual':float(residual),'rounding_compatible':abs(residual)<=F('.030')})
    return {'rows':result,'unsupported':unsupported}


def western(rows):
    subtractions=[]; offsets={}; displacement=[]
    for track in ['nw','center','sw']:
        for r in rows:
            residual=F(r[track+'_relative_y'])-F(r[track+'_y'])+F(r['ref_y'])
            subtractions.append({'track':track,'time_s':r['time_s'],'row':r['row'],'residual_fraction':str(residual),
                                 'residual':float(residual),'rounding_compatible':abs(residual)<=F('.015')})
    for track in ['center','sw']:
        diffs=[F(r[track+'_adjusted_y'])-F(r[track+'_relative_y']) for r in rows]
        lo=max(x-F('.01') for x in diffs); hi=min(x+F('.01') for x in diffs)
        offsets[track]={'differences_fraction':list(map(str,diffs)),'intersection_fraction':[str(lo),str(hi)],
                        'intersection':[float(lo),float(hi)],'compatible_common_offset':lo<=hi}
    base=next(r for r in rows if r['time_s']=='8.20')
    columns={'nw':'nw_relative_y','center':'center_adjusted_y','sw':'sw_adjusted_y'}
    for r in rows:
        delta={track:F(r[c])-F(base[c]) for track,c in columns.items()}
        pairs={a+'-'+b:delta[a]-delta[b] for a,b in itertools.combinations(columns,2)}
        displacement.append({'time_s':r['time_s'],'displacements':{k:float(v) for k,v in delta.items()},
                             'pair_differences_fraction':{k:str(v) for k,v in pairs.items()}})
    return {'subtractions':subtractions,'offsets':offsets,'displacements_from_8_20':displacement}


def science(a,b):
    return {'fits':camera_fits(a),'centered_differences':centered_differences(a),'western':western(b),
            'scale_clock_factors':[{'change':str(d),'scale_only_acceleration_factor':float(1+d),
                                   'clock_only_acceleration_factor':float(1/(1+d)**2)} for d in map(F,['-.05','-.01','.01','.05'])],
            'limits':'Printed-data arithmetic at assigned scale and nominal times; no independent historical measurement, physical CI, global force or cause.'}


def run(output):
    if output.exists(): raise FileExistsError(output)
    assert digest(ROOT/'PROTOCOL.md')==PROTOCOL_SHA
    assert digest(ROOT/'reconciliation.json')==RECONCILIATION_SHA
    assert reconcile()['status']=='exact_agreement'
    source=ROOT/'../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf'
    assert digest(source)=='cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394'
    a=validate_table(json.loads((ROOT/'transcription-root/table47.json').read_text()),47)
    b=validate_table(json.loads((ROOT/'transcription-root/table50.json').read_text()),50)
    result=science(a,b)
    output.mkdir()
    with (output/'results.json').open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    receipt={'input_pins':PINS,'protocol_sha256':PROTOCOL_SHA,'reconciliation_sha256':RECONCILIATION_SHA,
             'source_sha256':digest(source),'python':platform.python_version(),'numpy':np.__version__,
             'code_sha256':digest(Path(__file__)),'reconcile_code_sha256':digest(ROOT/'reconcile.py'),
             'results_sha256':digest(output/'results.json'),'fit_count':len(result['fits'])}
    with (output/'receipt.json').open('x') as f:
        json.dump(receipt,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps(receipt))


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True)
    run(p.parse_args().output)
