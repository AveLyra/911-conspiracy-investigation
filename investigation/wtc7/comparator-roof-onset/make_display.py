#!/usr/bin/env python3
"""Navigation-only contact sheets from admitted native PNGs, no frame changes."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('window_extract', HERE/'extract_window.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
x = m.x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('display', choices=['display01','display02'])
    args = parser.parse_args()
    out = HERE / args.display
    run = HERE / ('run02' if args.display == 'display01' else 'run03')
    if out.exists():
        raise FileExistsError('Refusing existing display output')
    rows = json.loads((run/'comparator-selected.json').read_text())
    if [r['source_index'] for r in rows] != list(range(239,481)):
        raise ValueError('Wrong fixed sequence')
    for row in rows:
        if x.identity(run/row['png']) != {k:row[k] for k in ['bytes','sha256']}:
            raise ValueError('Input PNG mismatch')
    out.mkdir()
    display_rows = [{**r, 'png':str(run/r['png'])} for r in rows]
    x.sheets(out,'comparator',display_rows)
    x.save(out/'receipt.json', {
        'purpose':'all-frame thumbnail navigation only; not native-pixel measurement',
        'feature_plan':x.identity(HERE/'FEATURES.md'), 'script':x.identity(Path(__file__)),
        'helper':x.identity(m.DEPENDENCY), 'pillow':x.Image.__version__,
        'source_map':x.identity(run/'comparator-selected.json'),
        'source_indices':[r['source_index'] for r in rows],
        'products':{str(p.relative_to(out)):x.identity(p) for p in sorted(out.rglob('*.png'))}
    })
    print({'display':args.display,'frames':len(rows),'sheets':len(list(out.rglob('*.png')))})


if __name__=='__main__':
    main()
