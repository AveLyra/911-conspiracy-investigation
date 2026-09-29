#!/usr/bin/env python3
"""Declared post-view nearest-neighbor endpoint display; no new measurement."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
OUT = HERE / 'refinement01'
BOXES = {'upper': (398,184,432,210), 'lower': (400,377,434,405)}
QUERIES = {'upper': (414.3770672546858,196.24035281146615),
           'lower': (416.95700110253586,390.7276736493937)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUT.exists():
        raise ValueError('Refinement output already exists')
    prior = json.loads((HERE / 'run01/receipt.json').read_text())
    for row in prior['selected']:
        assert sha(Path(row['native']['path'])) == row['native']['sha256']
    OUT.mkdir()
    products = []
    for row in prior['selected']:
        source = Path(row['native']['path'])
        native = Image.open(source)
        for label, box in BOXES.items():
            image = native.crop(box).resize(((box[2]-box[0])*12,(box[3]-box[1])*12),
                                            Image.Resampling.NEAREST)
            plain = OUT / f'{label}-{row["index"]:04d}-unmarked.png'
            image.save(plain)
            marked = image.convert('RGB')
            draw = ImageDraw.Draw(marked)
            # Convention: integer source indices are displayed pixel centres.
            x,y = QUERIES[label]
            u,v = 12*(x-box[0]+0.5)-0.5,12*(y-box[1]+0.5)-0.5
            for coords in [(u-20,v,u-8,v),(u+8,v,u+20,v),
                           (u,v-20,u,v-8),(u,v+8,u,v+20)]:
                draw.line(coords,fill=(255,0,0),width=2)
            overlay = OUT / f'{label}-{row["index"]:04d}-query-overlay.png'
            marked.save(overlay)
            pixels = image.load()
            assert all(pixels[12*a+5,12*b+5] == native.getpixel((box[0]+a,box[1]+b))
                       for a in range(box[2]-box[0]) for b in range(box[3]-box[1]))
            products.append(dict(index=row['index'],region=label,source_sha256=sha(source),
                                 box=list(box),factor=12,query_native=[x,y],
                                 query_display=[u,v],unmarked=dict(path=str(plain),sha256=sha(plain)),
                                 overlay=dict(path=str(overlay),sha256=sha(overlay))))
    receipt=dict(status='display_only',script_sha256=sha(Path(__file__)),
                 declaration_sha256=sha(HERE/'root-observations.md'),
                 prior_receipt_sha256=sha(HERE/'run01/receipt.json'),
                 pillow=pillow_version,products=products,
                 limit='Queries are saved coordinates, not newly localized features; nearest-neighbor blocks add no information')
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='display_only',unmarked_patches=6,query_overlays=6)))


if __name__ == '__main__':
    main()
