"""Retrospective cross-panel legend transfer; not historical curve admission.

Prototype rule is fixed before this execution: select the observed retained
RGB triplet with largest squared deficit from white; ties lexicographically.
Use the existing predicate unchanged. Fit on one panel, evaluate the other,
both directions. Prior inspection of both panels means this is NOT a holdout.
"""
import argparse
import hashlib
import json
from pathlib import Path
from raster_uncertainty import candidate

HERE=Path(__file__).resolve().parent
PIN='ea47f78671dfbcae1033808a66f05ac931df4bc3a3e22a2e8ffa6a9bcf61e819'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main(output):
    path=HERE/output
    if Path(output).name!=output or output in ('.','..'):
        raise ValueError('new local filename required')
    if path.exists() or path.is_symlink(): raise FileExistsError(path)
    source=HERE/'legend-probe01.json'
    if sha(source)!=PIN: raise ValueError('legend data changed')
    rows=json.loads(source.read_text())['colors']
    prototypes={}
    for r in rows:
        pixels=[tuple(p) for p in r['pixels'] if 255-min(p)>=32]
        chosen=min(pixels,key=lambda p:(-sum((255-c)**2 for c in p),p))
        prototypes.setdefault(r['panel'],{})[r['bolts']]=chosen
    results=[]
    for training,test in [('F','E'),('E','F')]:
        for r in rows:
            if r['panel']!=test: continue
            counts={'unique_expected':0,'expected_and_other':0,'incorrect_only':0,'none':0}
            pixels=[]
            for p in r['pixels']:
                if 255-min(p)<32: continue
                labels=[b for b,c in sorted(prototypes[training].items()) if candidate(p,c)]
                key=('none' if not labels else 'unique_expected' if labels==[r['bolts']]
                     else 'expected_and_other' if r['bolts'] in labels else 'incorrect_only')
                counts[key]+=1; pixels.append({'rgb':p,'labels':labels})
            assert sum(counts.values())==r['retained']
            results.append({'training_panel':training,'test_panel':test,'bolts':r['bolts'],
                            'counts':counts,'pixels':pixels})
    result={'status':'exploratory_cross_panel_transfer_not_validation',
      'input_sha256':PIN,'script_sha256':sha(Path(__file__)),
      'predicate_sha256':sha(HERE/'raster_uncertainty.py'),
      'prototypes':prototypes,'results':results,
      'limits':['Both panels were previously inspected. Not an unused holdout.',
                'Prototype is an observed pixel, not original ink or model identity.',
                'Legend transfer does not validate crowded, sloped or dashed graph fragments.',
                'No graph measurement, curve support, uncertainty coverage or causal finding.']}
    with path.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'output':output,'sha256':sha(path),'prototypes':prototypes,
                     'summary':[{k:v for k,v in r.items() if k!='pixels'} for r in results]}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();main(a.out)
