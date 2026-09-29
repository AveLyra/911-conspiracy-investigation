#!/usr/bin/env python3
"""Fixed diagnostic crops of existing pixels; no measurements or new imagery."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import unittest
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'tilted-camera-source-join'/'views01'
INDICES = [0,67,135]
RECTANGLE = (390,130,490,310)
PINS = {'PROTOCOL.md':'6be332d9537498582e7196c3adfa42ce29a7be6954824e4cea5d365665d74947',
        '../tilted-camera-source-join/views01/receipt.json':'4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29'}


def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def crop(image, rectangle, scale):
    if image.mode != 'L':raise ValueError('nonluma')
    if len(rectangle)!=4 or any(type(v) is not int for v in rectangle):raise ValueError('rectangle')
    x0,y0,x1,y1=rectangle
    if not 0<=x0<x1<=image.width or not 0<=y0<y1<=image.height:raise ValueError('bounds')
    if type(scale) is not int or scale<1:raise ValueError('scale')
    native=image.crop(rectangle)
    return native,native.resize((native.width*scale,native.height*scale),Image.Resampling.NEAREST)


class Controls(unittest.TestCase):
    def test_half_open_pixels(self):
        im=Image.frombytes('L',(4,3),bytes(range(12)))
        native,large=crop(im,(1,1,4,3),3)
        self.assertEqual(native.size,(3,2));self.assertEqual(native.tobytes(),bytes([5,6,7,9,10,11]))
        self.assertEqual(large.size,(9,6))
        for y in range(6):
            for x in range(9):self.assertEqual(large.getpixel((x,y)),native.getpixel((x//3,y//3)))
    def test_coordinate_origin(self):
        im=Image.frombytes('L',(4,3),bytes(range(12)))
        self.assertEqual(crop(im,(0,0,2,2),1)[0].getpixel((0,0)),0)
    def test_bad_bounds(self):
        im=Image.new('L',(4,3))
        for rect in [(-1,0,2,2),(0,0,5,3),(2,0,2,1),(0,2,2,1)]:
            with self.assertRaises(ValueError):crop(im,rect,3)
    def test_bad_type(self):
        with self.assertRaises(ValueError):crop(Image.new('RGB',(4,3)),(0,0,1,1),3)
        with self.assertRaises(ValueError):crop(Image.new('L',(4,3)),(0.,0,1,1),3)
    def test_bad_scale(self):
        for scale in [0,-1,1.5,True]:
            with self.assertRaises(ValueError):crop(Image.new('L',(4,3)),(0,0,1,1),scale)


def main(out):
    if out not in ['context01','context02']:raise ValueError('output_scope')
    dest=HERE/out
    if dest.exists():raise ValueError('output_exists')
    for relative,h in PINS.items():
        if sha(HERE/relative)!=h:raise ValueError('source_pin')
    receipt=json.loads((SOURCE/'receipt.json').read_text())
    if receipt['geometry']!=[720,480]:raise ValueError('geometry')
    selected={r['index']:r for r in receipt['selected']}
    products=[]
    for n in INDICES:
        row=selected[n];path=SOURCE/row['png']
        if sha(path)!=row['sha256']:raise ValueError('png_hash')
        with Image.open(path) as im:
            if im.mode!='L' or im.size!=(720,480):raise ValueError('native_geometry')
            if hashlib.sha256(im.tobytes()).hexdigest()!=row['luma_sha256']:raise ValueError('pixel_hash')
            native,large=crop(im,RECTANGLE,3)
        products.append((n,row,native,large))
    dest.mkdir()
    rows=[]
    for n,source,native,large in products:
        saved={}
        for kind,im in [('native',native),('3x',large)]:
            name=f'context-{n:04d}-{kind}.png';path=dest/name
            with path.open('xb') as stream:im.save(stream,format='PNG')
            saved[kind]={'png':name,'sha256':sha(path),'size':list(im.size),
                         'luma_sha256':hashlib.sha256(im.tobytes()).hexdigest()}
        rows.append({'frame':n,'source':source,'rectangle_half_open':RECTANGLE,'outputs':saved})
    for relative,h in PINS.items():
        if sha(HERE/relative)!=h:raise ValueError('source_changed')
    result={'scope':'fixed unmarked nearest-neighbor diagnostic crops; no new measured or synthesized pixels',
            'python':platform.python_version(),'pillow':pillow_version,'script_sha256':sha(Path(__file__)),
            'input_pins':PINS,'rows':rows}
    with (dest/'receipt.json').open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'status':'pass','images':6,'frames':INDICES,'receipt_sha256':sha(dest/'receipt.json')}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--test',action='store_true');p.add_argument('--out');a=p.parse_args()
    if a.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    main(a.out)
