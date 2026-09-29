#!/usr/bin/env python3
"""All prospectively declared position windows; conditional units, no causal fit."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import numpy as np

HERE=Path(__file__).resolve().parent
LENGTHS=(5,9,13,21)
G_REFERENCE=9.80665


def pin(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def polynomial(t,xy,degree):
    t=np.asarray(t,dtype=float)
    xy=np.asarray(xy,dtype=float)
    if (t.ndim!=1 or xy.shape!=(len(t),2) or len(t)<degree+1
        or not np.isfinite(t).all() or not np.isfinite(xy).all()
        or not (np.diff(t)>0).all()):
        raise ValueError('invalid_fit_domain')
    center=(t[0]+t[-1])/2
    half=(t[-1]-t[0])/2
    if half<=0: raise ValueError('degenerate_span')
    tau=(t-center)/half
    design=np.column_stack([tau**k for k in range(degree+1)])
    coef,resid_unused,rank,singular=np.linalg.lstsq(design,xy,rcond=None)
    if rank!=degree+1: raise ValueError('rank_deficient')
    residual=xy-design@coef
    out={'degree':degree,'center_seconds':float(center),'halfspan_seconds':float(half),
         'coefficients_xy':coef.tolist(),'residual_xy_pixels':residual.tolist(),
         'sse_xy_pixels2':np.sum(residual**2,axis=0).tolist(),
         'rmse_xy_pixels':np.sqrt(np.mean(residual**2,axis=0)).tolist(),
         'max_abs_residual_xy_pixels':np.max(np.abs(residual),axis=0).tolist(),
         'condition_2':float(singular[0]/singular[-1]),'rank':int(rank),
         'center_velocity_xy_pixels_per_s':(coef[1]/half).tolist()}
    if degree>=2:
        out['center_acceleration_xy_pixels_per_s2']=(2*coef[2]/half**2).tolist()
    if degree==2:
        weights=2*np.linalg.pinv(design)[2]/half**2
        out['acceleration_response_weights_per_s2']=weights.tolist()
        out['single_point_unit_response_max_per_s2']=float(np.max(np.abs(weights)))
        out['simultaneous_unit_response_bound_per_s2']=float(np.sum(np.abs(weights)))
    return out


def transform(xy,angle,scale,factor=1):
    rad=math.radians(angle)
    matrix=np.array([[math.cos(rad),-math.sin(rad)],[math.sin(rad),math.cos(rad)]])
    return np.asarray(xy)@matrix.T*(factor/scale)


def controls():
    results=[]
    t=np.linspace(0,4,21)
    for name,degree,coef in [('constant',2,[4,0,0]),('linear',2,[4,3,0]),
                             ('quadratic',2,[4,3,2]),('cubic',3,[4,3,2,0.4])]:
        y=sum(c*t**k for k,c in enumerate(coef))
        xy=np.column_stack([y,-2*y])
        result=polynomial(t,xy,degree)
        tc=result['center_seconds']
        expected_v=sum(k*c*tc**(k-1) for k,c in enumerate(coef) if k>=1)
        expected_a=sum(k*(k-1)*c*tc**(k-2) for k,c in enumerate(coef) if k>=2)
        assert np.max(np.abs(result['residual_xy_pixels']))<1e-9
        assert np.allclose(result['center_velocity_xy_pixels_per_s'],[expected_v,-2*expected_v],atol=1e-9,rtol=0)
        assert np.allclose(result['center_acceleration_xy_pixels_per_s2'],[expected_a,-2*expected_a],atol=1e-9,rtol=0)
        results.append({'name':name,'pass':True})
    irregular=np.array([0,.13,.4,.9,1.35,2.1,3.0])
    xy=np.column_stack([3+2*irregular+4*irregular**2,7-3*irregular+2*irregular**2])
    base=polynomial(irregular,xy,2)
    assert np.allclose(base['center_acceleration_xy_pixels_per_s2'],[8,4],atol=1e-9,rtol=0)
    results.append({'name':'irregular_clock_quadratic','pass':True})
    for name,tt,zz in [('duplicate_time',[0,1,1,2],np.zeros((4,2))),
                        ('insufficient_rank_domain',[0,1],np.zeros((2,2)))]:
        try: polynomial(tt,zz,2)
        except ValueError: results.append({'name':name,'pass':True})
        else: raise AssertionError('rejection_control_failed')
    assert np.allclose(transform([[1,0],[0,1]],0,2),[[.5,0],[0,.5]],atol=1e-9,rtol=0)
    assert np.allclose(transform([[1,0],[0,1]],90,2),[[0,.5],[-.5,0]],atol=1e-9,rtol=0)
    results.append({'name':'transform_basis_signs','pass':True})
    for factor in [14/15,16/15]:
        scaled=polynomial(irregular*1.25,xy*factor,2)
        assert np.allclose(scaled['center_acceleration_xy_pixels_per_s2'],np.array([8,4])*factor/1.25**2,atol=1e-9,rtol=0)
    results.append({'name':'length_and_clock_rate_laws','pass':True})
    shifted=polynomial(irregular+37,xy+[80,-40],2)
    assert np.allclose(shifted['center_acceleration_xy_pixels_per_s2'],[8,4],atol=1e-9,rtol=0)
    results.append({'name':'time_and_position_translation','pass':True})
    changed=xy.copy(); changed[2,0]+=1
    perturbed=polynomial(irregular,changed,2)
    response=perturbed['center_acceleration_xy_pixels_per_s2'][0]-base['center_acceleration_xy_pixels_per_s2'][0]
    assert abs(response-base['acceleration_response_weights_per_s2'][2])<1e-9
    results.append({'name':'one_pixel_response','pass':True})
    piecewise=np.maximum(t-2,0)**2
    turn=polynomial(t,np.column_stack([piecewise,piecewise]),2)
    assert abs(turn['center_acceleration_xy_pixels_per_s2'][0]-1)<1e-9
    results.append({'name':'continuous_piecewise_acceleration_average','pass':True,
                    'true_acceleration_before':0,'true_acceleration_after':2,
                    'straddling_window_acceleration':turn['center_acceleration_xy_pixels_per_s2'][0]})
    return results


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    if not re.fullmatch(r'[a-z0-9_-]+',args.out): raise ValueError('invalid_output_name')
    output=HERE/args.out
    if output.exists(): raise ValueError('output_exists')
    inputs={'points':HERE/'extraction01/points.json','extraction_receipt':HERE/'extraction01/receipt.json',
            'protocol':HERE/'PROTOCOL.md','producer':Path(__file__)}
    before={k:pin(v) for k,v in inputs.items()}
    receipt=json.loads(inputs['extraction_receipt'].read_text())
    assert before['points']==receipt['points']
    assert before['protocol']==receipt['inputs_before']['protocol']
    tests=controls()
    # Historical values are loaded only after synthetic fit controls pass.
    data=json.loads(inputs['points'].read_text())
    configuration=data['configuration']
    scale=configuration['xscale']['value']; angle=configuration['angle']['value']
    assert scale==configuration['yscale']['value'] and scale>0
    clock_rows={row['index']:row for row in data['current_diagnostic_clock']}
    def encoded(n):
        row=clock_rows[n]
        return Fraction(row['pts'])*Fraction(row['time_base'])
    clocks={name:[] for name in ('nominal','encoded')}
    for n in range(138,349,3):
        clocks['nominal'].append(Fraction(n-138,15))
        clocks['encoded'].append(encoded(n)-encoded(138))
    assert len(clocks['nominal'])==71
    windows=[(start,start+length) for length in LENGTHS for start in range(72-length)]+[(0,71)]
    assert len(windows)==241
    records=[]; trajectories=[]
    for track in data['tracks']:
        points=track['points']
        xy=np.array([[p['x'],p['y']] for p in points])
        geometries=[]
        for a_name,a in [('zero',0),('saved',angle)]:
            for count in (14,15,16):
                geom={'angle':a_name,'intervals':count,'angle_degrees':a,'length_factor':count/15}
                world=transform(xy-xy[0],a,scale,count/15)
                geometries.append({**geom,'displacement_X_D_assigned_m':world.tolist()})
        trajectories.append({'track':track['track'],'frames':[p['frame'] for p in points],
                             'image_displacement_xy_pixels':(xy-xy[0]).tolist(),'geometry_scenarios':geometries})
        for clock,t_exact in clocks.items():
            for start,stop in windows:
                record={'track':track['track'],'clock':clock,'start_mark':start,'stop_mark_exclusive':stop,
                        'first_frame':points[start]['frame'],'last_frame':points[stop-1]['frame'],
                        'count':stop-start,'time_exact':[str(q) for q in t_exact[start:stop]]}
                try:
                    t=[float(q) for q in t_exact[start:stop]]
                    fits={str(d):polynomial(t,xy[start:stop],d) for d in (1,2,3)}
                    q=fits['2']; converted=[]
                    for geom in geometries:
                        converted.append({'angle':geom['angle'],'intervals':geom['intervals'],
                            'velocity_X_D_assigned_m_per_s':transform(q['center_velocity_xy_pixels_per_s'],geom['angle_degrees'],scale,geom['length_factor']).tolist(),
                            'acceleration_X_D_assigned_m_per_s2':transform(q['center_acceleration_xy_pixels_per_s2'],geom['angle_degrees'],scale,geom['length_factor']).tolist()})
                    record.update(status='pass',fits=fits,geometry_scenarios=converted)
                except ValueError as exc:
                    record.update(status='failed',reason=str(exc))
                records.append(record)
    assert len(records)==964
    summary={'status':'conditional_saved_point_reconstruction','record_count':len(records),
             'failed_count':sum(r['status']!='pass' for r in records),
             'clock_rows_equal_exactly':clocks['nominal']==clocks['encoded'],
             'conventional_gravity_reference_m_per_s2':G_REFERENCE,'groups':[]}
    for track in data['tracks']:
        for count in (*LENGTHS,71):
            group=[r for r in records if r['track']==track['track'] and r['clock']=='nominal' and r['count']==count and r['status']=='pass']
            values=[next(g['acceleration_X_D_assigned_m_per_s2'][1] for g in r['geometry_scenarios'] if g['angle']=='saved' and g['intervals']==15) for r in group]
            summary['groups'].append({'track':track['track'],'window_points':count,'windows':len(values),
                                      'min_D_acceleration':min(values) if values else None,
                                      'max_D_acceleration':max(values) if values else None})
    after={k:pin(v) for k,v in inputs.items()}
    assert before==after
    output.mkdir()
    products={'controls.json':tests,'fits.json':records,'trajectories.json':trajectories,
              'clocks.json':{k:[str(q) for q in v] for k,v in clocks.items()},'summary.json':summary}
    for name,value in products.items():
        (output/name).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
    result={'status':summary['status'],'python':platform.python_version(),'numpy':np.__version__,
            'inputs_before':before,'inputs_after':after,'products':{name:pin(output/name) for name in products},
            'controls_passed':len(tests),'record_count':len(records),'failed_count':summary['failed_count']}
    (output/'receipt.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':summary['status'],'controls':len(tests),'fits':len(records),'failures':summary['failed_count'],'clocks_equal':summary['clock_rows_equal_exactly']}))


if __name__=='__main__': main()
