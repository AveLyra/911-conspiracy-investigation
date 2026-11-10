"""Descriptive counts over preserved diagnostic outputs; no new fitted model."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def span(rows):
    return None if not rows else {'first_index':rows[0]['index'],'last_index':rows[-1]['index'],
        'first_seconds_exact':rows[0]['seconds_exact'],'last_seconds_exact':rows[-1]['seconds_exact']}


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise FileExistsError('preserve prior summary')
    one,two = HERE/'run01',HERE/'run02'
    before = {str(p.relative_to(HERE)):pin(p) for folder in (one,two) for p in sorted(folder.iterdir())}
    matches = json.loads((one/'matches.json').read_text())
    models = json.loads((one/'transforms.json').read_text())
    names = sorted(p.name for p in one.iterdir())
    result = {'scope':'descriptive image-coordinate diagnostic; not physical motion or cause',
        'summarizer':pin(Path(__file__)),'inputs':before,
        'repeat_membership_equal':names==sorted(p.name for p in two.iterdir()),
        'repeat_equal':[n for n in names if pin(one/n)==pin(two/n)],
        'repeat_unequal':[n for n in names if pin(one/n)!=pin(two/n)],'groups':[]}
    for camera in ('camera2','camera4'):
        for half in (9,13):
            rows = [r for r in matches if r['camera']==camera and r['half']==half]
            fits = [r for r in models if r['camera']==camera and r['half']==half]
            group = {'camera':camera,'half':half,'match_statuses':dict(Counter(r['status'] for r in rows)),
                'flags':dict(Counter(flag for r in rows for flag in r['flags'])),'references':[],'models':{}}
            for reference in sorted(set(r['reference'] for r in rows)):
                selected = [r for r in rows if r['reference']==reference]
                candidates = [r for r in selected if r['status']=='candidate']
                shifts = [[r['candidate_xy'][j]-r['baseline_xy'][j] for j in (0,1)] for r in candidates]
                group['references'].append({'reference':reference,'statuses':dict(Counter(r['status'] for r in selected)),
                    'flags':dict(Counter(f for r in selected for f in r['flags'])),
                    'candidate_span':span(candidates),
                    'accepted_shift_range':[[min(v[j] for v in shifts),max(v[j] for v in shifts)] for j in (0,1)] if shifts else None})
            for model in ('translation','similarity','affine'):
                selected = [r for r in fits if r['model']==model]
                computed = [r for r in selected if r['status']=='computed']
                passing = [r for r in selected if r['passes_consistency_screen']]
                group['models'][model] = {'statuses':dict(Counter(r['status'] for r in selected)),
                    'passing_consistency':len(passing),'passing_span':span(passing),
                    'passing_indices':[r['index'] for r in passing],
                    'maximum_training_residual':max((r['max_residual'] for r in computed),default=None),
                    'maximum_loo_error':max((r['max_loo_error'] for r in computed if r['max_loo_error'] is not None),default=None),
                    'offset_range':[[min(r['offset'][j] for r in computed),max(r['offset'][j] for r in computed)] for j in (0,1)] if computed else None}
            result['groups'].append(group)
    if any(pin(HERE/p)!=identity for p,identity in before.items()):
        raise ValueError('input changed during summary')
    with out.open('x') as stream:
        stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inputs','summarizer')},indent=2))


if __name__=='__main__':
    main()
