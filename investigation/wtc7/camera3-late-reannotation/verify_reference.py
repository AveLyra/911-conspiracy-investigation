#!/usr/bin/env python3
"""Independent raw-moment NCC verification, without importing the producer."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
INDICES=[258]+list(range(288,349,3))
CENTERS={'R1':(272,400),'R2':(168,348),'R3':(673,292)}
TOL=1e-10

def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def independent_grid(base,current,cx,cy,side):
    h=side//2;n=side*side
    # Integer historical pixels and quarter-valued synthetic controls keep
    # these raw moments exact within binary64. No centered arrays or producer.
    a=base[cy-h:cy+h+1,cx-h:cx+h+1].ravel()
    assert a.size==n
    sa=math.fsum(a); aa=math.fsum(float(v)*float(v) for v in a)
    ea=n*aa-sa*sa
    scores=[];sds=[]
    for dy in range(-6,7):
        for dx in range(-6,7):
            b=current[cy+dy-h:cy+dy+h+1,cx+dx-h:cx+dx+h+1].ravel()
            assert b.size==n
            sb=math.fsum(b);bb=math.fsum(float(v)*float(v) for v in b)
            eb=n*bb-sb*sb
            ab=math.fsum(float(x)*float(y) for x,y in zip(a,b))
            scores.append(None if ea==0 or eb==0 else (n*ab-sa*sb)/math.sqrt(ea*eb))
            sds.append(math.sqrt(eb)/n)
    return scores,sds,sa/n,math.sqrt(ea)/n

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    output=HERE/args.out
    assert output.parent==HERE and not output.exists()
    paths={'code':Path(__file__),'producer':HERE/'reference_diagnostic.py',
           'protocol':HERE/'PROTOCOL.md','preflight':HERE/'reference-preflight.md',
           'views':HERE/'views01/receipt.json','receipt':HERE/'reference01/receipt.json',
           'scores':HERE/'reference01/scores.json','controls':HERE/'reference01/controls.json',
           'summary':HERE/'reference01/summary.json'}
    before={k:pin(p) for k,p in paths.items()}
    assert before['producer']['sha256']=='f2cb0ae86e4d040ede3c6227cc1a83860f2d2cdbb54544dc5db50e18c758e371'
    record=json.loads(paths['receipt'].read_text());views=json.loads(paths['views'].read_text())
    assert record['inputs_before']==record['inputs_after']
    for row in record['products']: assert pin(HERE/'reference01'/row['name'])=={k:row[k] for k in ('bytes','sha256')}
    for k,p in [('protocol',paths['protocol']),('preflight',paths['preflight']),('code',paths['producer']),('views_receipt',paths['views'])]:
        assert pin(p)==record['inputs_before'][k]
    frames={}
    for product in views['products']:
        path=HERE/'views01'/product['name']
        assert pin(path)=={k:product[k] for k in ('bytes','sha256')}
    for frame in INDICES:
        path=HERE/f'views01/frame-{frame:04d}.png'
        assert pin(path)==record['inputs_before'][f'native_{frame:04d}']
        im=Image.open(path);assert im.mode=='L' and im.size==(720,480)
        row=next(r for r in views['rows'] if r['index']==frame)
        assert hashlib.sha256(im.tobytes()).hexdigest()==row['pixel_sha256']
        frames[frame]=np.asarray(im,dtype=float)
    data=json.loads(paths['scores'].read_text());controls=json.loads(paths['controls'].read_text())
    rows=data['rows'];assert len(rows)==132
    assert {(r['frame'],r['reference'],r['side']) for r in rows}=={(i,r,s) for i in INDICES for r in CENTERS for s in (21,31)}
    maxima={'ncc':0.,'sd':0.,'mean':0.,'margin':0.};nreal=0;ncontrol=0
    def close(a,b,kind):
        if a is None or b is None: assert a is b;return
        diff=abs(a-b);maxima[kind]=max(maxima[kind],diff);assert diff<TOL
    def check(row,base,current):
        cx,cy=row['center'];side=row['side']
        scores,sds,mean,sd=independent_grid(base,current,cx,cy,side)
        stored=[v for line in row['scores'] for v in line]
        storedsd=[v for line in row['candidate_population_sds'] for v in line]
        assert len(stored)==len(storedsd)==169
        for a,b in zip(scores,stored): close(a,b,'ncc')
        for a,b in zip(sds,storedsd): close(a,b,'sd')
        close(mean,row['baseline_mean'],'mean');close(sd,row['baseline_population_sd'],'sd')
        assert sum(v is None for v in scores)==row['undefined_score_count']
        finite=[(v,i) for i,v in enumerate(scores) if v is not None]
        if finite:
            maximum=max(v for v,i in finite)
            ties=[i for v,i in finite if abs(maximum-v)<=1e-12]
            w=row['winner'];wi=(w['dy']+6)*13+w['dx']+6
            # Symmetric synthetic ties can select a different representative
            # under floating arithmetic; verify it is in the independent tie set.
            assert wi in ties and len(ties)==len(row['best_ties_within_tolerance'])
            assert w['x']==cx+w['dx'] and w['y']==cy+w['dy']
            close(w['ncc'],maximum,'ncc')
            far=[v for v,i in finite if max(abs(i%13-6-w['dx']),abs(i//13-6-w['dy']))>=3]
            margin=maximum-max(far);close(margin,row['far_margin'],'margin')
            gates=[sd>=10,maximum>=.85,margin>=.02,len(ties)==1,abs(w['dx'])<6 and abs(w['dy'])<6]
        else:
            assert row['winner'] is None
            gates=[sd>=10,False,False,False,False]
        keys=['baseline_population_sd_at_least_10','winner_ncc_at_least_0_85','far_margin_at_least_0_02',
              'unique_best_within_1e_minus_12','winner_not_on_search_boundary']
        assert row['gates']==dict(zip(keys,gates)) and row['pass']==all(gates)
    for row in rows:
        assert row['center']==list(CENTERS[row['reference']])
        check(row,frames[288],frames[row['frame']]);nreal+=169
    for case in controls['cases']:
        check(case['result'],np.array(case['input_baseline']),np.array(case['input_current']));ncontrol+=169
        expected=case['expected'];r=case['result']
        assert r['pass']==expected['pass']
        want=expected['winner_dx_dy_or_unspecified']
        if want is not None: assert [r['winner']['dx'],r['winner']['dy']]==want
        for name in expected['required_failed_gates']: assert not r['gates'][name]
    assert len(controls['cases'])==14
    assert len(data['translations'])==44
    for trans in data['translations']:
        selected=[r for r in rows if r['frame']==trans['frame'] and r['side']==trans['side']]
        assert len(selected)==3
        accepted=all(r['pass'] for r in selected)
        assert trans['all_three_pass']==accepted
        if accepted:
            avg=[math.fsum(r['winner'][k] for r in selected)/3 for k in ('dx','dy')]
            assert trans['mean_dx_dy']==avg
            for r,out in zip(selected,trans['residual_dx_dy']):
                assert out['reference']==r['reference']
                assert out['vector']==[r['winner'][k]-avg[j] for j,k in enumerate(('dx','dy'))]
    after={k:pin(p) for k,p in paths.items()};assert before==after
    result={'status':'pass_independent_arithmetic_not_physical_validation','python':platform.python_version(),
            'numpy':np.__version__,'inputs_before':before,'inputs_after':after,'image_product_pins':len(views['products']),
            'native_pixel_checks':22,'real_rows':132,'real_scores':nreal,'control_cases':14,'control_scores':ncontrol,
            'translation_groups':44,'absolute_tolerance':TOL,'maximum_absolute_errors':maxima,
            'method':'raw moments with math.fsum; no import of centered-product producer',
            'limitations':'shared pixels and fixed baseline candidates; no physical stationarity, subpixel bound or camera calibration'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','real_scores','control_scores','maximum_absolute_errors')}))

if __name__=='__main__': main()
