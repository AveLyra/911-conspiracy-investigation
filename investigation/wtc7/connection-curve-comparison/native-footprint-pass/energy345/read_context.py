"""Fixed second-batch raw contexts; reuse the frozen lossless reader helpers."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
EXPECTED = {
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'PROTOCOL.md': 'be57860a830ab716498ba5d25733021c1c975da1b0427f50f64071af4eaf5f16',
    '../../native-strips01/Im9.jpg': '3154e28ea82ca2f39c465a7bdfe367677216543df296cf918cbbd259248f8129',
    '../../native-strips01/Im10.jpg': 'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
TARGETS = {'E3': [365,30,690,60], 'E4': [440,72,690,92], 'E5': [395,18,690,47]}
CONTEXT = {'E3': [363,28,692,62], 'E4': [438,70,692,92], 'E5': [393,16,692,49]}
SOURCES = {'E3':'Im10.jpg', 'E4':'Im9.jpg', 'E5':'Im9.jpg'}


def pin(path):
    b = path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)}


def inputs():
    result = {k:pin(HERE/k) for k in EXPECTED}
    if any(result[k]['sha256'] != v for k,v in EXPECTED.items()):
        raise ValueError('Frozen dependency changed')
    result['read_context.py'] = pin(Path(__file__))
    return result


def helper():
    # Check code integrity before executing the already-reviewed frozen helper.
    if pin(PARENT/'read_context.py')['sha256'] != EXPECTED['../read_context.py']:
        raise ValueError('Helper changed')
    spec = importlib.util.spec_from_file_location('frozen_native_reader', PARENT/'read_context.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['controls','save01','save02','show'])
    p.add_argument('--pair',choices=list(TARGETS)); p.add_argument('--first',type=int); p.add_argument('--last',type=int)
    args=p.parse_args(); h=helper()
    if args.mode=='controls':
        print(json.dumps(h.controls(),sort_keys=True)); return
    before=inputs(); data={}
    for pair,source in SOURCES.items():
        with Image.open(HERE/'../../native-strips01'/source) as im:
            if im.mode!='RGB' or im.size!=(745,92): raise ValueError('Wrong representation')
            data[pair]=h.cells(im,CONTEXT[pair])
    if before!=inputs(): raise ValueError('Input changed')
    if args.mode=='show':
        if args.pair is None or args.first is None or args.last is None: raise ValueError('Display range required')
        print(f'Native {args.pair}; exact RGB, only exact (255,255,255) omitted; all other context cells shown.')
        for x, rows in h.sparse(data[args.pair],CONTEXT[args.pair],args.first,args.last).items():
            print(str(x)+': '+' '.join(str(y)+':'+','.join(map(str,rgb)) for y,rgb in rows))
        return
    output={'inputs':before, 'sources':SOURCES, 'target_boxes':TARGETS, 'context_boxes':CONTEXT,
            'python':platform.python_version(),'pillow':pillow_version,'cells':data,
            'classification':None,'human_accepted':False}
    target=HERE/('context'+args.mode[-2:]+'.json')
    h.save(target,output)
    print(json.dumps({'output':pin(target),'cells':{k:len(v) for k,v in data.items()}}))


if __name__=='__main__': main()
