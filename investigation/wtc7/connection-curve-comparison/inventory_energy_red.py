"""Classify every probed column; never assign identities or admit support."""
import argparse
import json
from pathlib import Path
from replay_neutral_fragments import runs, sha

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'energy-red-expanded01.json'
EXPECTED = 'b67003c9855b9a56ecb8d70a12390d69108e43095355251a85f767e802be6262'

def classify(bands, boundary):
    if boundary:
        return 'crop_contact'
    if all(len(b)==2 for b in bands):
        # Inclusive pixel indices become cell edges: a one-row empty gap
        # requires lower start > upper inclusive end + 1.
        upper_end=max(b[0][1] for b in bands)
        lower_start=min(b[1][0] for b in bands)
        if lower_start > upper_end+1:
            return 'two_separate_candidate_bands'
    return 'gap_merge_or_threshold_ambiguity'

def calculate():
    if sha(SOURCE)!=EXPECTED: raise ValueError('input mismatch')
    data=json.loads(SOURCE.read_text())
    x0,y0,x1,y1=data['region_half_open']
    maps=[]
    for case in data['cases']:
        columns={}
        for component in case['components']:
            for x,rr in component['column_runs']:
                columns.setdefault(x,set()).update(y for lo,hi in rr for y in range(lo,hi+1))
        maps.append(columns)
    rows=[]
    for x in range(x0,x1):
        bands=[runs(c.get(x,set())) for c in maps]
        boundary=(x in (x0,x1-1) or any(y0 in c.get(x,set()) or y1-1 in c.get(x,set()) for c in maps))
        rows.append({'x':x,'runs_at_32_64_96':bands,'classification':classify(bands,boundary)})
    labels=sorted(set(r['classification'] for r in rows))
    return {'status':'candidate_column_inventory_not_model_support',
        'input_sha256':EXPECTED,'input':SOURCE.name,'code_sha256':sha(Path(__file__)),
        'rows':rows,'counts':{s:sum(r['classification']==s for r in rows) for s in labels},
        'inclusive_column_ranges':{s:runs(r['x'] for r in rows if r['classification']==s) for s in labels},
        'method':'All290 columns; crop contact takes precedence. Two bands must exist at every retained threshold with disjoint cross-threshold pixel-cell envelopes. All other columns unresolved; no interpolation.',
        'limits':['Retrospective exploratory rule, not a frozen historical measurement method.',
                  'Upper/lower ordering is not spring/shell identity.',
                  'Threshold agreement does not validate unselected ink or physical uncertainty.',
                  'No fraction of the physical curve support or final quantile targets follows.'],
        'model_support':None,'human_accepted':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    if Path(args.out).name!=args.out or args.out in ('.','..'):ap.error('new local filename required')
    target=HERE/args.out
    if target.exists() or target.is_symlink():raise FileExistsError(target)
    result=calculate()
    with target.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'output':target.name,'sha256':sha(target),'counts':result['counts']}))
