"""Replay the three inspected F3 regions; preserve pixels, never admit support."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import unittest
import PIL
from PIL import Image

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def runs(values):
    result = []
    for value in sorted(values):
        if result and value == result[-1][1]+1:
            result[-1][1] = value
        else:
            result.append([value,value])
    return result

def components(points):
    remaining = set(points)
    result = []
    while remaining:
        first = min(remaining)
        remaining.remove(first)
        stack, found = [first], [first]
        while stack:
            x,y = stack.pop()
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    neighbor = (x+dx,y+dy)
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        stack.append(neighbor)
                        found.append(neighbor)
        xs,ys = zip(*found)
        result.append({'summary':[len(found),min(xs),min(ys),max(xs),max(ys)],
            'column_runs':[[x,runs(y for xx,y in found if xx==x)] for x in sorted(set(xs))]})
    return result

def calculate():
    proposal = HERE/'fragment-proposal-F3-Im4.json'
    conflicts = HERE/'fragment-conflicts-F3.json'
    p = json.loads(proposal.read_text())
    records = [dict(p,box_half_open=p['region_half_open'])] + json.loads(conflicts.read_text())['regions']
    inputs = [proposal,conflicts,Path(__file__).resolve()]+[HERE/r['source'] for r in records]
    pins = {str(f.relative_to(HERE)):sha(f) for f in inputs}
    outputs = []
    for record in records:
        source = HERE/record['source']
        if sha(source) != record['source_sha256']:
            raise ValueError('source mismatch')
        image = Image.open(source).convert('RGB')
        x0,y0,x1,y1 = record['box_half_open']
        if not (0<=x0<x1<=image.width and 0<=y0<y1<=image.height):
            raise ValueError('region outside image')
        for threshold in (32,64,96):
            pixels = {(x,y) for x in range(x0,x1) for y in range(y0,y1)
                if max(image.getpixel((x,y)))-min(image.getpixel((x,y)))<=32
                and 255-max(image.getpixel((x,y)))>=threshold}
            found = components(pixels)
            expected = sorted(record['thresholds'][str(threshold)],key=lambda r:(r[1],r[2]))
            actual = sorted((c['summary'] for c in found),key=lambda r:(r[1],r[2]))
            if actual != expected:
                raise ValueError('saved component disagreement; preserve failure, do not retune')
            recovered = {(x,y) for c in found for x,rr in c['column_runs'] for lo,hi in rr for y in range(lo,hi+1)}
            if recovered != pixels:
                raise ValueError('pixel run roundtrip failed')
            outputs.append({'source':record['source'],'threshold':threshold,
                'box_half_open':record['box_half_open'],'components':found,
                'selected_pixels':len(pixels),'pixel_roundtrip':True})
    if pins != {str(f.relative_to(HERE)):sha(f) for f in inputs}:
        raise ValueError('inputs changed')
    return {'status':'candidate_pixels_not_admitted_curve_support','input_pins':pins,
        'python':platform.python_version(),'pillow':PIL.__version__,'regions':outputs,
        'human_accepted':False,'limits':['Exploratory neutral-pixel selection; same analyst, no model identity validation.',
            'All inspected regions and thresholds retained. No resampling or dash-gap interpolation.',
            'Per-column runs encode selected pixels, not all visible ink or calibrated centreline error.']}

class Controls(unittest.TestCase):
    def test_empty(self): self.assertEqual(components(set()),[])
    def test_diagonal(self): self.assertEqual(len(components({(0,0),(1,1)})),1)
    def test_gap(self): self.assertEqual(len(components({(0,0),(2,0)})),2)
    def test_hole(self):
        c=components({(0,0),(0,2),(1,1)})[0]
        self.assertEqual(c['column_runs'],[[0,[[0,0],[2,2]]],[1,[[1,1]]]])
    def test_input_preservation(self):
        p={(0,0),(1,0)}; components(p); self.assertEqual(p,{(0,0),(1,0)})

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--self-test',action='store_true'); ap.add_argument('--out'); args=ap.parse_args()
    if args.self_test:
        unittest.main(argv=['fragment-replay'],verbosity=2)
    else:
        if not args.out or Path(args.out).name!=args.out or args.out in ('.','..'):
            ap.error('new local output filename required')
        target=HERE/args.out
        if target.exists() or target.is_symlink(): raise FileExistsError(target)
        result=calculate()
        with target.open('x') as f: json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
        print(json.dumps({'output':target.name,'sha256':sha(target),'region_threshold_cases':len(result['regions'])}))
