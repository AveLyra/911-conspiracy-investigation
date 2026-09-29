"""Complete-output descriptive summary and exact two-run reproduction checks."""
import hashlib
import json
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def span(values):
    values=list(values)
    return {'n':len(values),'min':min(values),'max':max(values)} if values else {'n':0,'min':None,'max':None}


def main():
    out=BASE/'summary01.json'
    if out.exists():raise FileExistsError('preserved summary')
    receipts=[]
    for run in ['run01','run02']:
        folder=BASE/run; r=json.loads((folder/'receipt.json').read_text())
        assert r['status']=='completed'
        for name,pin in r['outputs'].items():
            assert sha(folder/name)==pin['sha256'] and (folder/name).stat().st_size==pin['bytes']
        receipts.append(r)
    for key in ['script_sha256','protocol_sha256','prior_pins','python','numpy','pillow','outputs']:
        assert receipts[0][key]==receipts[1][key]
    assert (BASE/'run01/results.json').read_bytes()==(BASE/'run02/results.json').read_bytes()
    with np.load(BASE/'run01/arrays.npz') as a,np.load(BASE/'run02/arrays.npz') as b:
        assert set(a.files)==set(b.files)
        for name in a.files:assert np.array_equal(a[name],b[name])
        arrays_compared=len(a.files)
    source=json.loads((BASE/'run01/results.json').read_text());rows=source['results'];groups={};gammas={}
    for target in ['148','149']:
        subset=[r for r in rows if r['target']==target];groups[target]={};gammas[target]={}
        names=[n for n in subset[0]['baseline'] if n!='F']
        for name in names:
            base=[r['baseline'][name]['metrics'] for r in subset]
            fits=[f['regions'][name] for r in subset for f in r['fits'] if f['gamma']==1]
            groups[target][name]={
                'raw_bias':span(m['bias'] for m in base),'raw_mae':span(m['mae'] for m in base),
                'affine_mae':span(f['metrics']['mae'] for f in fits),
                'spearman':span(r['rank_diagnostics'][name]['spearman'] for r in subset),
                'q10_iou':span(r['rank_diagnostics'][name]['quantiles']['0.1']['iou'] for r in subset),
                'outside_training_range':span(f['extrapolation']['outside_min_max'] for f in fits),
                'outside_training_p01_p99':span(f['extrapolation']['outside_p01_p99'] for f in fits)}
        for gamma in [.5,.75,1.,1.25,1.5,2.,3.]:
            pairs=[(r['baseline'][n]['metrics']['mae'],f['regions'][n]['metrics']['mae'])
                   for r in subset for f in r['fits'] if f['gamma']==gamma for n in names]
            gammas[target][str(gamma)]={'regional_comparisons':len(pairs),
                'mae_lower_than_matching_baseline':sum(y<x for x,y in pairs),
                'mae_equal_to_matching_baseline':sum(y==x for x,y in pairs),
                'mae_higher_than_matching_baseline':sum(y>x for x,y in pairs),
                'mae_change':span(y-x for x,y in pairs)}
    examples=[]
    for r in rows:
        if r['branch']=='180_BILINEAR' and (r['target'],r['frame_index']) in [('148',93),('149',185)]:
            examples.append({'target':r['target'],'frame_index':r['frame_index'],'branch':r['branch'],
                'baseline':r['baseline'],'rank_diagnostics':r['rank_diagnostics'],
                'fits':[f for f in r['fits'] if f['gamma']==1]})
    result={'status':'passed','script_sha256':sha(Path(__file__)),'source_sha256':sha(BASE/'run01/results.json'),
        'reproduction':{'arrays_compared':arrays_compared,'results_bytes_identical':True,'array_archive_bytes_identical':True,
                        'run_receipt_pins':{r:sha(BASE/r/'receipt.json') for r in ['run01','run02']}},
        'coverage':{k:source[k] for k in ['pair_count','branch_count','fit_attempts']},
        'region_ranges':groups,'complete_gamma_transfer_counts':gammas,'prior_leader_examples':examples,
        'limits':'Retrospective descriptive extrema/counts across correlated choices; not uncertainty intervals, event-level replication, equivalence or fire area.'}
    with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['region_ranges','prior_leader_examples']},indent=2))


if __name__=='__main__':main()
