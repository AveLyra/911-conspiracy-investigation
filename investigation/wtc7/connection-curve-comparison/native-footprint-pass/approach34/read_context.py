"""Frozen E3/E4 approach contexts; lossless display, no ink classifier."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
EXPECTED = {
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    'PROTOCOL.md': 'cc94c588f9b132318c7ca55fcffe1ed7eafbb92fd131583ffcbc74a13e5e54b7',
    '../../native-strips01/Im10.jpg': 'fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
TARGETS = {'E3': [195,35,365,92], 'E4': [195,0,440,92]}
CONTEXT = {'E3': [193,33,367,92], 'E4': [193,0,442,92]}


def pin(path):
    b = path.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def inputs():
    result = {k: pin(HERE/k) for k in EXPECTED}
    if any(result[k]['sha256'] != v for k,v in EXPECTED.items()):
        raise ValueError('Frozen dependency changed')
    result['read_context.py'] = pin(Path(__file__))
    return result


def helper():
    if pin(HERE/'../read_context.py')['sha256'] != EXPECTED['../read_context.py']:
        raise ValueError('Helper changed before import')
    spec = importlib.util.spec_from_file_location('frozen_context', HERE/'../read_context.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def encode(column):
    """Exact repeated RGB rows; inclusive row ranges, gN means N,N,N."""
    runs = []
    for y, rgb in column:
        if runs and y == runs[-1][1] + 1 and rgb == runs[-1][2]:
            runs[-1][1] = y
        else:
            runs.append([y, y, rgb])
    return ' '.join((str(a) if a == b else f'{a}-{b}') + '=' +
                    (f'g{rgb[0]}' if rgb[0] == rgb[1] == rgb[2]
                     else ','.join(map(str, rgb))) for a,b,rgb in runs)


def decode(text):
    result = []
    for token in text.split():
        rows, value = token.split('=')
        bounds = list(map(int, rows.split('-')))
        a, b = bounds if len(bounds) == 2 else (bounds[0], bounds[0])
        rgb = [int(value[1:])] * 3 if value.startswith('g') else list(map(int, value.split(',')))
        if len(rgb) != 3 or not all(0 <= c <= 255 for c in rgb) or b < a:
            raise ValueError('Invalid exact RGB token')
        result.extend((y, rgb.copy()) for y in range(a,b+1))
    return result


def controls(h):
    checks = h.controls()
    fixtures = [[], [(0,[1,1,1])], [(1,[254,255,255]),(2,[254,255,255]),
                (4,[254,255,255]),(5,[0,0,0]),(6,[0,0,0])],
                [(i,[i,i,i]) for i in range(256)]]
    checks['display_roundtrip'] = all(decode(encode(c)) == c for c in fixtures)
    checks['display_no_gap_bridge'] = encode(fixtures[2]).startswith('1-2=254,255,255 4=254,255,255')
    checks['display_grayscale_exact'] = encode([(9,[253,253,253])]) == '9=g253'
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['controls','save01','save02','show'])
    p.add_argument('--pair', choices=list(TARGETS))
    p.add_argument('--first', type=int)
    p.add_argument('--last', type=int)
    args = p.parse_args()
    h = helper()
    if args.mode == 'controls':
        print(json.dumps(controls(h), sort_keys=True)); return
    before = inputs()
    with Image.open(HERE/'../../native-strips01/Im10.jpg') as im:
        if im.mode != 'RGB' or im.size != (745,92):
            raise ValueError('Wrong representation')
        data = {pair: h.cells(im,box) for pair,box in CONTEXT.items()}
    if before != inputs():
        raise ValueError('Input changed')
    if args.mode == 'show':
        if args.pair is None or args.first is None or args.last is None:
            raise ValueError('Display range required')
        columns = h.sparse(data[args.pair], CONTEXT[args.pair], args.first,args.last)
        print(f'{args.pair} context {CONTEXT[args.pair]}. All rows not listed are EXACT WHITE 255,255,255. gN=N,N,N; row ranges inclusive; no thresholds.')
        for x,col in columns.items():
            rendered = encode(col)
            if decode(rendered) != col:
                raise AssertionError('Historical display roundtrip')
            print(f'{x}: {rendered}')
        return
    output = {'inputs': before, 'sources': {'E3':'Im10.jpg','E4':'Im10.jpg'},
              'target_boxes': TARGETS,'context_boxes': CONTEXT,
              'python': platform.python_version(), 'pillow': pillow_version,
              'cells': data,'classification': None,'human_accepted':False}
    target = HERE/('context'+args.mode[-2:]+'.json')
    h.save(target,output)
    print(json.dumps({'output':pin(target),'cells':{k:len(v) for k,v in data.items()}}))


if __name__ == '__main__':
    main()
