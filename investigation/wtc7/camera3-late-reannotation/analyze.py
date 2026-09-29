#!/usr/bin/env python3
"""Preserve annotation disagreement and all declared native-coordinate fits."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import re
import numpy as np

HERE=Path(__file__).resolve().parent
INDICES=[258]+list(range(288,349,3))

def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def fit(t,y,intervals):
    t=np.asarray(t,dtype=float)
    y=np.asarray(y,dtype=float)
    if len(t)!=len(y) or len(t)<3 or not np.isfinite(t).all() or not np.isfinite(y).all():
        raise ValueError('shape_or_finite')
    if not np.all(np.diff(t)>0): raise ValueError('clock_order')
    center=(t[0]+t[-1])/2
    half=(t[-1]-t[0])/2
    u=(t-center)/half
    result={'time_center':float(center),'halfspan':float(half),'y':y.tolist(),'fits':{}}
    for degree in (1,2):
        design=np.column_stack([u**j for j in range(degree+1)])
        coef,res,rank,singular=np.linalg.lstsq(design,y,rcond=None)
        if rank!=degree+1: raise ValueError('rank')
        residual=y-design@coef
        result['fits'][str(degree)]={'coefficients':coef.tolist(),'residuals':residual.tolist(),
          'sse':float(residual@residual),'rmse':float(np.sqrt(np.mean(residual**2))),
          'condition':float(singular[0]/singular[-1])}
        if degree==2:
            weights=2*np.linalg.pinv(design)[2]/half**2
            acceleration=float(2*coef[2]/half**2)
            result.update(acceleration_px_s2=acceleration,weights=weights.tolist(),
                          sum_abs_weights=float(np.sum(abs(weights))))
            if intervals is not None:
                bounds=np.asarray(intervals,dtype=float)
                if bounds.shape!=(len(t),2) or not np.isfinite(bounds).all() or not np.all(bounds[:,0]<=y) or not np.all(y<=bounds[:,1]):
                    raise ValueError('interval_shape_or_order')
                low=np.where(weights>=0,bounds[:,0],bounds[:,1])
                high=np.where(weights>=0,bounds[:,1],bounds[:,0])
                result.update(input_intervals=bounds.tolist(),
                  acceleration_interval_px_s2=[float(weights@low),float(weights@high)])
            else:
                result.update(input_intervals=None,acceleration_interval_px_s2=None)
    return result

def controls():
    result=[]
    t=np.arange(9,dtype=float)/5
    for name,y,expect in [('constant',np.ones(9)*4,0),('linear',3+2*t,0),
                          ('quadratic',2+3*t+4*t*t,8)]:
        got=fit(t,y,[[v-1,v+1] for v in y])
        assert abs(got['acceleration_px_s2']-expect)<1e-9
        result.append({'name':name,'time':t.tolist(),'expected_acceleration':expect,'result':got})
    y=2+3*t+4*t*t
    base=fit(t,y,[[v-1,v+2] for v in y])
    moved=fit(t+400,y+500,[[v+499,v+502] for v in y])
    assert abs(base['acceleration_px_s2']-moved['acceleration_px_s2'])<1e-9
    assert np.max(abs(np.array(base['acceleration_interval_px_s2'])-moved['acceleration_interval_px_s2']))<1e-9
    result.append({'name':'translation_time_origin','base':base,'moved':moved})
    short_t=np.arange(5,dtype=float)/5
    short_y=2+3*short_t+4*short_t**2
    bounds=[[v-1,v+2] for v in short_y]
    bounded=fit(short_t,short_y,bounds)
    vertices=[]
    for bits in itertools.product((0,1),repeat=5):
        values=[bounds[i][bit] for i,bit in enumerate(bits)]
        vertices.append({'bits':list(bits),'y':values,'a':fit(short_t,values,None)['acceleration_px_s2']})
    endpoints=[min(r['a'] for r in vertices),max(r['a'] for r in vertices)]
    assert np.max(abs(np.array(endpoints)-bounded['acceleration_interval_px_s2']))<1e-9
    result.append({'name':'all32_interval_vertices','time':short_t.tolist(),'bounded':bounded,'vertices':vertices})
    common=7+11*t+2*t*t
    a=5+3*t+4*t*t
    b=3+8*t+3*t*t
    before=fit(t,a-b,None)
    after=fit(t,(a+common)-(b+common),None)
    assert abs(before['acceleration_px_s2']-after['acceleration_px_s2'])<1e-9
    result.append({'name':'differential_common_translation','time':t.tolist(),'A':a.tolist(),'B':b.tolist(),
                   'common':common.tolist(),'before':before,'after':after})
    rejected=[]
    for name,tt,yy in [('duplicate_time',[0,0,1],[1,2,3]),('nonfinite',[0,1,2],[1,float('nan'),3])]:
        try: fit(tt,yy,None)
        except ValueError as exc: rejected.append({'name':name,'reason':str(exc)})
        else: raise AssertionError('control_not_rejected')
    result.append({'name':'rejections','outcomes':rejected})
    return result

def validate_annotation(doc):
    assert [r['frame'] for r in doc['rows']]==INDICES
    for row in doc['rows']:
        for target in ('A','B'):
            p=row[target]
            assert p['status'] in ('localized','unlocalizable')
            if p['status']=='unlocalizable':
                assert p['y'] is None and p['ymin'] is None and p['ymax'] is None
                continue
            for key in ('x','y','ymin','ymax'):
                assert type(p[key]) is int
            assert 0<=p['ymin']<=p['y']<=p['ymax']<480
            assert 0<=p['x']<720
            if target=='A': assert 0<=p['xmin']<=p['x']<=p['xmax']<720
            else: assert p['x']==322

def interval_overlap(a,b):
    return max(a[0],b[0])<=min(a[1],b[1])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    if not re.fullmatch('[a-z0-9_-]+',args.out): raise ValueError('output_name')
    output=HERE/args.out
    if output.exists(): raise ValueError('output_exists')
    inputs={'root':HERE/'root-observations.json','independent':HERE/'independent-observations.json',
            'root_note':HERE/'root-observations.md','independent_note':HERE/'independent-observations.md',
            'points':HERE.parent/'camera3-conditional-trajectories/extraction01/points.json',
            'views':HERE/'views01/receipt.json','protocol':HERE/'PROTOCOL.md','code':Path(__file__)}
    before={k:pin(v) for k,v in inputs.items()}
    assert before['protocol']['sha256']=='7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f'
    assert before['root']['sha256']=='20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a'
    assert before['independent']['sha256']=='529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f'
    assert before['points']['sha256']=='f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3'
    check=controls()
    docs={name:json.loads(inputs[name].read_text()) for name in ('root','independent')}
    for doc in docs.values(): validate_annotation(doc)
    original=json.loads(inputs['points'].read_text())
    saved={target:{p['frame']:p for p in track['points']} for target,track in zip(('A','B'),original['tracks'])}
    comparison=[]
    for i,frame in enumerate(INDICES):
        for target in ('A','B'):
            old=saved[target][frame]
            row={'frame':frame,'target':target,'saved_xy':[old['x'],old['y']],'observers':{}}
            for name,doc in docs.items():
                p=doc['rows'][i][target]
                details={'status':p['status'],'definition_warning':None if target=='A' else 'fixed-column silhouette versus saved moving-x query; not equal material identity'}
                if p['status']=='localized':
                    details.update(x=p['x'],y=p['y'],y_interval=[p['ymin'],p['ymax']],
                      dx_from_saved=p['x']-old['x'],dy_from_saved=p['y']-old['y'],
                      saved_y_inside=p['ymin']<=old['y']<=p['ymax'])
                    if target=='A': details.update(x_interval=[p['xmin'],p['xmax']],saved_x_inside=p['xmin']<=old['x']<=p['xmax'])
                row['observers'][name]=details
            r,s=row['observers']['root'],row['observers']['independent']
            row['new_y_intervals_overlap']=interval_overlap(r['y_interval'],s['y_interval']) if r['status']==s['status']=='localized' else None
            comparison.append(row)
    fits=[]
    for name in ('root','independent','saved'):
        for length in (9,13,21):
            for start in range(21-length+1):
                frames=INDICES[1:][start:start+length]
                for target in ('A','B','AminusB'):
                    base={'observer':name,'target':target,'frames':frames,'window_points':length,
                          'status':'pass','time':[(f-138)/15 for f in frames]}
                    y=[];bounds=[];missing=[]
                    for frame in frames:
                        if name=='saved':
                            value=saved[target][frame]['y'] if target in ('A','B') else saved['A'][frame]['y']-saved['B'][frame]['y']
                            y.append(value)
                            continue
                        p=docs[name]['rows'][INDICES.index(frame)]
                        targets=('A','B') if target=='AminusB' else (target,)
                        if any(p[k]['status']!='localized' for k in targets):
                            missing.append(frame);continue
                        if target=='AminusB':
                            y.append(p['A']['y']-p['B']['y'])
                            bounds.append([p['A']['ymin']-p['B']['ymax'],p['A']['ymax']-p['B']['ymin']])
                        else:
                            y.append(p[target]['y']);bounds.append([p[target]['ymin'],p[target]['ymax']])
                    if missing: base.update(status='uncomputed_missing_localization',missing_frames=missing)
                    else: base.update(fit(base['time'],y,None if name=='saved' else bounds))
                    fits.append(base)
    assert len(fits)==207
    after={k:pin(v) for k,v in inputs.items()}
    assert before==after
    output.mkdir()
    products={}
    for name,data in [('controls.json',check),('comparison.json',comparison),('fits.json',fits)]:
        path=output/name
        path.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n')
        products[name]=pin(path)
    receipt={'status':'pass_conditional_image_only','python':platform.python_version(),'numpy':np.__version__,
             'inputs_before':before,'inputs_after':after,'products':products,
             'windows':len(fits),'computed':sum(r['status']=='pass' for r in fits),
             'missing_localization':sum(r['status']!='pass' for r in fits),'control_groups':len(check),
             'interval_semantics':'conditional Cartesian product of subjective placement envelopes; no probability or physical-calibration bound'}
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:receipt[k] for k in ('status','windows','computed','missing_localization','control_groups')}))

if __name__=='__main__': main()
