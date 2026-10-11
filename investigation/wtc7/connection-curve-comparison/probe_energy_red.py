"""Exploratory E6 terminal pixels; no historical ordinate or support admission."""
import argparse
import json
import platform
from pathlib import Path
import PIL
from PIL import Image
from replay_neutral_fragments import components, sha

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'native-strips01/Im8.jpg'
EXPECTED = '0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83'
BOX = (400, 70, 690, 92)

def selected(rgb, threshold):
    r, g, b = rgb
    return r - max(g, b) > 32 and 255 - min(g, b) >= threshold

def calculate():
    if sha(SOURCE) != EXPECTED:
        raise ValueError('source hash mismatch')
    im = Image.open(SOURCE).convert('RGB')
    x0, y0, x1, y1 = BOX
    assert 0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height
    cases = []
    for threshold in (32, 64, 96):
        pixels = {(x,y) for x in range(x0,x1) for y in range(y0,y1)
                  if selected(im.getpixel((x,y)), threshold)}
        found = components(pixels)
        recovered = {(x,y) for c in found for x,rr in c['column_runs']
                     for lo,hi in rr for y in range(lo,hi+1)}
        if recovered != pixels:
            raise ValueError('pixel roundtrip failed')
        cases.append({'threshold':threshold, 'selected_pixels':len(pixels),
                      'components':found, 'pixel_roundtrip':True})
    return {'status':'exploratory_candidate_pixels_not_admitted_support',
            'source':'native-strips01/Im8.jpg', 'source_sha256':EXPECTED,
            'code_sha256':sha(Path(__file__)),
            'component_code_sha256':sha(HERE/'replay_neutral_fragments.py'),
            'python':platform.python_version(), 'pillow':PIL.__version__,
            'region_half_open':BOX,
            'selection':'AI visually selected red terminal region; not a final quantile sample.',
            'predicate':'R-max(G,B)>32 and 255-min(G,B)>=threshold',
            'cases':cases,
            'limits':['RGB predicate is exploratory, not a validated color classifier.',
                      'No component discarded, merged, interpolated or assigned a model identity.',
                      'Crop boundaries are not physical endpoints; disconnected pixels need not be true dashes.',
                      'Pixel runs are not calibrated stroke uncertainty or complete supported domains.'],
            'human_accepted':False, 'quantitative_support':None}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if Path(args.out).name != args.out or args.out in ('.','..'):
        parser.error('new local filename required')
    target = HERE/args.out
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    result = calculate()
    with target.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({'output':target.name, 'sha256':sha(target),
        'cases':[[c['threshold'],c['selected_pixels'],len(c['components'])] for c in result['cases']]}))
