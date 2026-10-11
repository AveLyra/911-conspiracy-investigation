"""Replay the declared legend-only probe; never extracts graph ordinates.

Run with --self-test, or --out a new JSON filename in this directory.
This consolidates previously executed methods, not a preregistered new test.
"""
import argparse
import hashlib
import io
import json
import platform
import statistics
import unittest
from fractions import Fraction as F
from pathlib import Path

import PIL
from PIL import Image
import pypdf

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
SHA = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
BOXES = {'F': (1060,1080,315,460), 'E': (595,615,1148,1290)}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def groups(rows):
    result = []
    for row in rows:
        if not result or row != result[-1][-1] + 1:
            result.append([row])
        else:
            result[-1].append(row)
    return result

def admitted(rgb, threshold):
    return 255 - min(rgb) >= threshold

def membership(n, offset, pitch, lower, upper):
    return [i for i in range(n) if lower <= offset + pitch * F(2*i+1,2*n) < upper]

def collect():
    inventory_path = HERE/'pypdf-representation01.json'
    raw = SOURCE.read_bytes()
    if digest(raw) != SHA:
        raise ValueError('source changed')
    inventory_bytes = inventory_path.read_bytes()
    inventory = json.loads(inventory_bytes)['image_invocations']
    reader = pypdf.PdfReader(io.BytesIO(raw))
    if reader.is_encrypted:
        reader.decrypt('')
    resources = reader.pages[75]['/Resources']['/XObject']
    decoded = []
    for item in inventory:
        data = resources['/'+item['name']].get_data()
        if digest(data) != item['encoded_jpeg_sha256']:
            raise ValueError('encoded source mismatch')
        image = Image.open(io.BytesIO(data)).convert('RGB')
        if list(image.size) != item['native_dimensions']:
            raise ValueError('dimensions changed')
        decoded.append((item,image))
    records, colors = [], []
    for panel, (left,right,top,bottom) in BOXES.items():
        bolt = 3
        for item, image in decoded:
            a,b,c,d,e,f = [F(str(v)) for v in item['ctm']]
            if b or c:
                raise ValueError('unsupported rotation')
            width,height = image.size
            xs = membership(width,e,a,F(left*9,25),F(right*9,25))
            ys = membership(height,792-f-d,d,F(top*9,25),F(bottom*9,25))
            if not xs or not ys:
                continue
            pixel_rows = [[image.getpixel((x,y)) for x in xs] for y in ys]
            for threshold in (32,64,96):
                counts = [sum(admitted(p,threshold) for p in row) for row in pixel_rows]
                active = [y for y,n in zip(ys,counts) if 2*n >= len(xs)]
                runs = groups(active)
                records.append({'panel':panel,'strip':item['name'],'threshold':threshold,
                    'columns':xs,'rows':ys,'counts':counts,
                    'runs_inclusive':[[r[0],r[-1]] for r in runs]})
                if threshold == 32:
                    for run in runs:
                        pixels = [image.getpixel((x,y)) for y in run for x in xs]
                        kept = [p for p in pixels if admitted(p,32)]
                        colors.append({'panel':panel,'bolts':bolt,'strip':item['name'],
                            'rows':run,'columns':xs,'pixels':pixels,'retained':len(kept),
                            'total':len(pixels),
                            'RGB_min':[min(p[k] for p in kept) for k in range(3)],
                            'RGB_median':[statistics.median(p[k] for p in kept) for k in range(3)],
                            'RGB_max':[max(p[k] for p in kept) for k in range(3)]})
                        bolt += 1
        if bolt != 10:
            raise ValueError('expected seven legend groups; do not retune')
    if SOURCE.read_bytes() != raw or inventory_path.read_bytes() != inventory_bytes:
        raise ValueError('input changed during processing')
    return {'status':'legend_only_not_curve_support','source_sha256':SHA,
        'inventory_sha256':digest(inventory_bytes),'script_sha256':digest(Path(__file__).read_bytes()),
        'runtime':{'python':platform.python_version(),'pypdf':pypdf.__version__,'pillow':PIL.__version__},
        'boxes':BOXES,'records':records,'colors':colors,
        'limits':['Same analyst and decoder as prior measurements; not independent human review.',
                  'No curve ordinate, support interval, model identity or uncertainty calibration.']}

class Controls(unittest.TestCase):
    def test_empty(self): self.assertEqual(groups([]),[])
    def test_gaps(self): self.assertEqual(groups([1,2,4,7,8]),[[1,2],[4],[7,8]])
    def test_threshold(self):
        self.assertTrue(admitted((223,255,255),32))
        self.assertFalse(admitted((224,255,255),32))
    def test_cell_membership(self):
        self.assertEqual(membership(4,F(0),F(4),F(1,2),F(5,2)),[0,1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=['legend_probe'],verbosity=2)
    else:
        if not args.out or Path(args.out).name != args.out or args.out in ('.','..'):
            parser.error('a new local output filename is required')
        output = HERE/args.out
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        result = collect()
        with output.open('x') as stream:
            json.dump(result,stream,indent=2,sort_keys=True)
            stream.write('\n')
        print(json.dumps({'output':output.name,'sha256':digest(output.read_bytes()),
                          'records':len(result['records']),'colors':len(result['colors'])}))
