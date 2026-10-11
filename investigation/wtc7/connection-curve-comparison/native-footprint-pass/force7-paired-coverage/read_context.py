"""Fixed F7 earlier Im2 native context; lossless display, no pixel classifier."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
TARGET = [220, 0, 330, 88]
CONTEXT = [218, 0, 332, 88]
EXPECTED = {
    'PROTOCOL.md': 'aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19',
    'READERS.md': 'd62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../force56-remainder/READERS.md': 'e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../approach34/read_context.py': '384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def inputs():
    result = {name: pin(HERE/name) for name in EXPECTED}
    for name, expected in EXPECTED.items():
        if result[name]['sha256'] != expected:
            raise ValueError('Changed frozen dependency: ' + name)
    result['read_context.py'] = pin(Path(__file__))
    return result


def module(name, rel):
    if pin(HERE/rel)['sha256'] != EXPECTED[rel]:
        raise ValueError('Changed helper before import')
    spec = importlib.util.spec_from_file_location(name, HERE/rel)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


def representation(im):
    if im.mode != 'RGB' or im.size != (741, 88):
        raise ValueError('Expected native 741 by 88 RGB source')


def controls(base, display):
    checks = display.controls(base)
    checks['context_count'] = (CONTEXT[2]-CONTEXT[0])*(CONTEXT[3]-CONTEXT[1]) == 10032
    checks['clipped_margin'] = CONTEXT == [max(0, TARGET[0]-2), max(0, TARGET[1]-2), min(741, TARGET[2]+2), min(88, TARGET[3]+2)]
    representation(Image.new('RGB', (741, 88)))
    checks['correct_representation'] = True
    for label, mode, size in [('wrong_width', 'RGB', (745, 88)), ('wrong_height', 'RGB', (741, 92)), ('wrong_mode', 'L', (741, 88))]:
        try:
            representation(Image.new(mode, size))
        except ValueError:
            checks[label+'_rejected'] = True
        else:
            checks[label+'_rejected'] = False
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['controls', 'save01', 'save02', 'show'])
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    args = parser.parse_args()
    before = inputs()
    base = module('f7_early_im2_cells', '../read_context.py')
    display = module('f7_early_im2_display', '../approach34/read_context.py')
    if args.mode == 'controls':
        result = controls(base, display)
        if before != inputs():
            raise ValueError('Changed inputs during controls')
        print(json.dumps(result, sort_keys=True))
        return
    with Image.open(HERE/'../../native-strips01/Im2.jpg') as im:
        representation(im)
        data = base.cells(im, CONTEXT)
    if before != inputs():
        raise ValueError('Changed inputs during extraction')
    if args.mode == 'show':
        if args.first is None or args.last is None:
            raise ValueError('Explicit finite display bounds required')
        print(f'F7-Im2-early context {CONTEXT}; rows 0..87; omitted EXACT WHITE only; gN=N,N,N; inclusive equal-RGB runs; no thresholds.')
        for x, col in base.sparse(data, CONTEXT, args.first, args.last).items():
            rendered = display.encode(col)
            if display.decode(rendered) != col:
                raise AssertionError('Non-lossless display')
            print(f'{x}: {rendered}')
        return
    result = {'inputs': before, 'sources': {'F7': 'Im2.jpg'},
              'target_boxes': {'F7': TARGET}, 'context_boxes': {'F7': CONTEXT},
              'source_size': [741, 88], 'python': platform.python_version(),
              'pillow': pillow_version, 'cells': {'F7': data},
              'classification': None, 'human_accepted': False}
    target = HERE/('context'+args.mode[-2:]+'.json')
    base.save(target, result)
    if before != inputs():
        raise ValueError('Changed inputs after save; preserve failed output')
    print(json.dumps({'output': pin(target), 'cells': len(data)}, sort_keys=True))


if __name__ == '__main__':
    main()
