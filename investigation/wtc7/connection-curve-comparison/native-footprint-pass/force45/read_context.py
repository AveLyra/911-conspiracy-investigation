"""Fixed F4/F5 raw contexts with distinct source-region identities."""
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
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'PROTOCOL.md': '4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../../native-strips01/Im4.jpg': '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
TARGETS = {'F4-Im4': [330,0,425,88], 'F5-Im4': [375,0,475,88],
           'F5-Im2': [225,50,350,88]}
CONTEXT = {'F4-Im4': [328,0,427,88], 'F5-Im4': [373,0,477,88],
           'F5-Im2': [223,48,352,88]}
SOURCES = {'F4-Im4': 'Im4.jpg', 'F5-Im4': 'Im4.jpg', 'F5-Im2': 'Im2.jpg'}
PAIRS = {'F4-Im4': 'F4', 'F5-Im4': 'F5', 'F5-Im2': 'F5'}


def pin(path):
    b = path.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def inputs():
    result = {k: pin(HERE/k) for k in EXPECTED}
    if any(result[k]['sha256'] != v for k, v in EXPECTED.items()):
        raise ValueError('Frozen dependency changed')
    result['read_context.py'] = pin(Path(__file__))
    return result


def helper():
    path = HERE/'../read_context.py'
    if pin(path)['sha256'] != EXPECTED['../read_context.py']:
        raise ValueError('Helper changed')
    spec = importlib.util.spec_from_file_location('frozen_native_reader', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clipped_context(box, size):
    x0, y0, x1, y1 = box
    w, h = size
    if not (all(type(n) is int for n in [*box, *size])
            and 0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
        raise ValueError('Invalid target')
    return [max(0,x0-2), max(0,y0-2), min(w,x1+2), min(h,y1+2)]


def controls(h):
    checks = h.controls()
    checks['full_height_clip'] = clipped_context([3,0,7,8], [10,8]) == [1,0,9,8]
    checks['all_edges_clip'] = clipped_context([0,0,10,8], [10,8]) == [0,0,10,8]
    checks['interior_context'] = clipped_context([3,3,6,6], [10,10]) == [1,1,8,8]
    try:
        clipped_context([True,0,7,8], [10,8])
    except ValueError:
        checks['clip_boolean_rejected'] = True
    else:
        checks['clip_boolean_rejected'] = False
    a = Image.new('RGB', (10,8), (1,2,3))
    b = Image.new('RGB', (10,8), (4,5,6))
    synthetic = {'pair-strip-a': h.cells(a,[3,2,4,3]),
                 'pair-strip-b': h.cells(b,[3,2,4,3])}
    checks['same_pair_coordinates_keep_two_sources'] = (
        synthetic['pair-strip-a'][0]['rgb'] == [1,2,3]
        and synthetic['pair-strip-b'][0]['rgb'] == [4,5,6])
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['controls','save01','save02','show'])
    p.add_argument('--region', choices=list(TARGETS))
    p.add_argument('--first', type=int)
    p.add_argument('--last', type=int)
    args = p.parse_args()
    h = helper()
    if args.mode == 'controls':
        print(json.dumps(controls(h), sort_keys=True))
        return
    before = inputs()
    data = {}
    for region, source in SOURCES.items():
        with Image.open(HERE/'../../native-strips01'/source) as im:
            if im.mode != 'RGB' or im.size != (741,88):
                raise ValueError('Wrong representation')
            if clipped_context(TARGETS[region], im.size) != CONTEXT[region]:
                raise ValueError('Wrong clipped context')
            data[region] = h.cells(im, CONTEXT[region])
    if before != inputs():
        raise ValueError('Input changed')
    if args.mode == 'show':
        if args.region is None or args.first is None or args.last is None:
            raise ValueError('Display range required')
        print(f'Native {args.region}; exact RGB, only exact (255,255,255) omitted; all other context cells shown.')
        for x, rows in h.sparse(data[args.region], CONTEXT[args.region], args.first, args.last).items():
            print(str(x)+': '+' '.join(str(y)+':'+','.join(map(str,rgb)) for y,rgb in rows))
        return
    output = {'inputs': before, 'sources': SOURCES, 'pairs': PAIRS,
              'target_boxes': TARGETS, 'context_boxes': CONTEXT,
              'source_dimensions': {'Im4.jpg': [741,88], 'Im2.jpg': [741,88]},
              'python': platform.python_version(), 'pillow': pillow_version,
              'cells': data, 'classification': None, 'human_accepted': False}
    target = HERE/('context'+args.mode[-2:]+'.json')
    h.save(target, output)
    print(json.dumps({'output': pin(target), 'cells': {k: len(v) for k,v in data.items()}}))


if __name__ == '__main__':
    main()
