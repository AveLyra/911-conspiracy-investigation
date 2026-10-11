"""Lossless native RGB context for the fixed first E6/E7 footprint batch."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import tempfile
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'native-strips01/Im8.jpg'
EXPECTED_SOURCE = '0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83'
EXPECTED_PROTOCOL = '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd'
TARGETS = {'E6': [515,57,690,85], 'E7': [580,14,690,30]}
CONTEXT = {'E6': [513,55,692,87], 'E7': [578,12,692,32]}


def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')


def cells(image, box):
    x0,y0,x1,y1 = box
    if not (all(type(n) is int for n in box) and 0 <= x0 < x1 <= image.width
            and 0 <= y0 < y1 <= image.height):
        raise ValueError('Invalid region')
    return [{'x':x,'y':y,'rgb':list(image.getpixel((x,y)))}
            for y in range(y0,y1) for x in range(x0,x1)]


def sparse(entries, box, first, last):
    x0,y0,x1,y1 = box
    if not x0 <= first <= last < x1:
        raise ValueError('Display outside context')
    table = {(c['x'],c['y']):c['rgb'] for c in entries}
    return {x: [(y,table[x,y]) for y in range(y0,y1) if table[x,y] != [255,255,255]]
            for x in range(first,last+1)}


def controls():
    image = Image.new('RGB', (4,3), 'white')
    image.putpixel((1,1),(255,254,255)); image.putpixel((2,2),(0,4,7))
    full = cells(image,[1,0,4,3]); compressed = sparse(full,[1,0,4,3],1,3)
    recovered = {(x,y):rgb for x,col in compressed.items() for y,rgb in col}
    checks = {'coverage':len(full)==9,
              'row_major':[(c['x'],c['y']) for c in full]==[(x,y) for y in range(3) for x in range(1,4)],
              'near_white_retained':(1,[255,254,255]) in compressed[1],
              'white_only_omitted':sum(len(c) for c in compressed.values())==2,
              'lossless':all(recovered.get((c['x'],c['y']),[255,255,255])==c['rgb'] for c in full)}
    try: cells(image,[True,0,4,3])
    except ValueError: checks['boolean_boundary_rejected']=True
    else: checks['boolean_boundary_rejected']=False
    try: sparse(full,[1,0,4,3],0,3)
    except ValueError: checks['outside_display_rejected']=True
    else: checks['outside_display_rejected']=False
    with tempfile.TemporaryDirectory(prefix='native-context-control-') as d:
        p=Path(d)/'test.json'; save(p,{'synthetic':True}); original=p.read_bytes()
        try: save(p,{})
        except FileExistsError: checks['overwrite_refused']=p.read_bytes()==original
        else: checks['overwrite_refused']=False
    if not all(checks.values()): raise AssertionError(checks)
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['controls','save01','save02','show'])
    parser.add_argument('--pair',choices=['E6','E7'])
    parser.add_argument('--first',type=int); parser.add_argument('--last',type=int)
    args=parser.parse_args()
    if args.mode=='controls':
        print(json.dumps(controls(),sort_keys=True)); return
    paths=[SOURCE, HERE/'PROTOCOL.md', HERE/'REGIONS.json', Path(__file__)]
    before={str(p):pin(p) for p in paths}
    if pin(SOURCE)['sha256'] != EXPECTED_SOURCE or pin(HERE/'PROTOCOL.md')['sha256'] != EXPECTED_PROTOCOL:
        raise ValueError('Changed frozen source or protocol')
    with Image.open(SOURCE) as image:
        if image.size != (745,92) or image.mode != 'RGB': raise ValueError('Wrong representation')
        data={pair:cells(image,box) for pair,box in CONTEXT.items()}
    if before!={str(p):pin(p) for p in paths}: raise ValueError('Input changed')
    if args.mode=='show':
        if args.pair is None or args.first is None or args.last is None: raise ValueError('Display range required')
        print(f'Native {args.pair} context {CONTEXT[args.pair]}; exact RGB. Omitted cells are exactly (255,255,255), never thresholded.')
        for x,rows in sparse(data[args.pair],CONTEXT[args.pair],args.first,args.last).items():
            print(str(x)+': '+' '.join(str(y)+':'+','.join(map(str,rgb)) for y,rgb in rows))
        return
    output={'source_pin':pin(SOURCE),'protocol_pin':pin(HERE/'PROTOCOL.md'),
            'roster_pin':pin(HERE/'REGIONS.json'),'script_pin':pin(Path(__file__)),
            'python':platform.python_version(),'pillow':pillow_version,
            'target_boxes':TARGETS,'context_boxes':CONTEXT,'cells':data,
            'inputs':before,'classification':None,'human_accepted':False}
    target=HERE/('context'+args.mode[-2:]+'.json'); save(target,output)
    print(json.dumps({'output':pin(target),'cells':{k:len(v) for k,v in data.items()}}))


if __name__=='__main__': main()
