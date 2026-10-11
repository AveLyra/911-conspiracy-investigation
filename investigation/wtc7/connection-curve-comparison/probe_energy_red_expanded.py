"""Preserve original E6 probe; expand only its clipped upper crop boundary."""
import argparse
import json
from pathlib import Path
import probe_energy_red as original

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if Path(args.out).name != args.out or args.out in ('.','..'):
        parser.error('new local filename required')
    target = original.HERE / args.out
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    original.BOX = (400,60,690,92)
    result = original.calculate()
    result['wrapper_code_sha256'] = original.sha(Path(__file__))
    result['revision_reason'] = 'Prior region clipped the upper red stroke at y70; only top edge changed to y60. Prior outputs and source code preserved. All thresholds retained. This is a retrospective crop repair, not independent validation.'
    with target.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True)
        f.write('\n')
    print(json.dumps({'output':target.name,'sha256':original.sha(target),
        'cases':[[c['threshold'],c['selected_pixels'],len(c['components'])] for c in result['cases']]}))
