#!/usr/bin/env python3
"""Independent original-box inequality check of all joint witnesses."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

HERE=Path(__file__).resolve().parent
FRAMES=[258]+list(range(288,349,3))

def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def q4(v):
    # Independent integer lattice: all declared inputs and witnesses in this
    # finite test are multiples of one quarter pixel. Reject anything else.
    value=Fraction(v)*4
    assert value.denominator==1
    return value.numerator

def check(inputs,frames,result):
    maps={k:{r['frame']:r for r in rows} for k,rows in inputs.items()}
    included=[];omitted=[];bounds=[];conflicts=[];pairs={}
    for frame in frames:
        reasons=[]
        for name,rows in maps.items():
            for target in ('A','B'):
                if rows[frame][target]['status']!='localized':
                    reasons.append({'observer':name,'feature':target,'status':rows[frame][target]['status']})
        if reasons:
            omitted.append({'frame':frame,'reasons':reasons});continue
        included.append(frame)
        boxes={s:[(q4(rows[frame][s]['ymin']),q4(rows[frame][s]['ymax'])) for rows in maps.values()] for s in ('A','B')}
        for s in ('A','B'):
            if max(v[0] for v in boxes[s])>min(v[1] for v in boxes[s]): conflicts.append((frame,s))
        # Every cross-observer pair imposes a constraint on the same c.
        low=max(a[0]-b[1] for a in boxes['A'] for b in boxes['B'])
        high=min(a[1]-b[0] for a in boxes['A'] for b in boxes['B'])
        bounds.append((low,high));pairs[frame]=boxes
    assert result['selected_frames']==frames and result['included_frames']==included and result['omitted_frames']==omitted
    assert [(c['frame'],c['feature']) for c in result['observer_intersection_conflicts']]==conflicts
    if conflicts:
        assert result['status']=='rejected_empty_observer_intersection' and result['constant_interval'] is None and not result['witness']
        return len(included),0
    assert bounds
    lower=max(a for a,b in bounds);upper=min(b for a,b in bounds)
    assert [q4(v) for v in result['constant_interval']]==[lower,upper]
    if lower>upper:
        assert result['status']=='infeasible_constant_separation_within_supplied_boxes' and result['constant'] is None and not result['witness']
        return len(included),0
    assert result['status']=='feasible_on_included_samples_only'
    c=q4(result['constant']);assert 2*c==lower+upper
    assert [w['frame'] for w in result['witness']]==included
    count=0
    for witness in result['witness']:
        boxes=pairs[witness['frame']];a=q4(witness['A_y']);b=q4(witness['B_y'])
        assert a-b==c==q4(witness['A_minus_B'])
        for lo,hi in boxes['A']: assert lo<=a<=hi;count+=1
        for lo,hi in boxes['B']: assert lo<=b<=hi;count+=1
        feasibleA=[max([v[0] for v in boxes['A']]+[c+v[0] for v in boxes['B']]),
                   min([v[1] for v in boxes['A']]+[c+v[1] for v in boxes['B']])]
        assert [q4(v) for v in witness['A_witness_interval']]==feasibleA
        assert 2*a==sum(feasibleA)
    return len(included),count

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    output=HERE/args.out;assert output.parent==HERE and not output.exists()
    inputs={n:HERE/n for n in ['root-observations.json','independent-observations.json',
       'JOINT-ENVELOPE-ADDENDUM.md','PROTOCOL.md','joint_feasibility.py','joint01/result.json',
       'joint01/controls.json','joint01/receipt.json','verify_joint.py']}
    before={n:pin(p) for n,p in inputs.items()}
    receipt=json.loads(inputs['joint01/receipt.json'].read_text())
    assert receipt['inputs_before']==receipt['inputs_after']
    for n,p in receipt['inputs_before'].items(): assert before[n]==p
    for n,p in receipt['products'].items(): assert before['joint01/'+n]==p
    source={n:json.loads(inputs[n+'-observations.json'].read_text())['rows'] for n in ('root','independent')}
    data=json.loads(inputs['joint01/result.json'].read_text())
    for n,rows in source.items():
        assert [r['frame'] for r in rows]==FRAMES
        for original,stored in zip(rows,data['original_observers'][n]):
            assert original['frame']==stored['frame']
            for s in ('A','B'):
                assert original[s]['status']==stored[s]['status']
                for k in ('y','ymin','ymax'):
                    a,b=original[s][k],stored[s][k]
                    assert (a is None and b is None) or (a is not None and b is not None and q4(a)==q4(b))
    keys={n+'_'+c for n in ('root','independent','combined') for c in ('selected22','late21')}
    assert len(data['scenarios'])==6 and {r['name'] for r in data['scenarios']}==keys
    records=[];memberships=0
    for result in data['scenarios']:
        selection,coverage=result['name'].split('_')
        selected=source if selection=='combined' else {selection:source[selection]}
        frames=FRAMES if coverage=='selected22' else FRAMES[1:]
        n,k=check(selected,frames,result);memberships+=k
        records.append({'name':result['name'],'included':n,'original_box_membership_checks':k,
                        'constant_interval':result['constant_interval'],'constant':result['constant']})
    controls=json.loads(inputs['joint01/controls.json'].read_text());cases=0
    assert len(controls['groups'])==5
    for group in controls['groups']:
        if group['name']=='common_translation':
            for name in ('original','translated'):
                check(group['inputs'][name],group['selected_frames'],group['results'][name]);cases+=1
            a,b=group['results']['original'],group['results']['translated']
            assert a['constant_interval']==b['constant_interval'] and a['constant']==b['constant']
            for x,y,d in zip(a['witness'],b['witness'],group['translations']):
                for k in ('A_y','B_y'): assert q4(y[k])-q4(x[k])==q4(d)
        elif group['name']=='empty_observer_intersection':
            for case in group['cases']: check(case['inputs'],case['selected_frames'],case['result']);cases+=1
        else:
            check(group['inputs'],group['selected_frames'],group['result']);cases+=1
            for k,v in group['expected'].items(): assert group['result'][k]==v
    after={n:pin(p) for n,p in inputs.items()};assert before==after
    result={'status':'pass_exact_independent_original_box_checks','python':platform.python_version(),
      'inputs_before':before,'inputs_after':after,'method':'quarter-pixel integer inequalities from original observer boxes; no producer import',
      'scenarios':records,'witness_rows':sum(r['included'] for r in records),
      'original_box_memberships':memberships,'control_groups':5,'control_solutions':cases,
      'limitations':'only current rational lattice and subjective supplied y boxes; not observations, calibrated uncertainty or a physical rigid-body model'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','witness_rows','original_box_memberships','control_solutions','scenarios')}))

if __name__=='__main__': main()
