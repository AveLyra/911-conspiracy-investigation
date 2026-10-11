"""Fixed F5/F6 native contexts; reuse tested lossless display, never classify."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
TARGETS = {'F5': [310, 0, 425, 88], 'F6': [270, 55, 340, 88]}
CONTEXTS = {'F5': [308, 0, 427, 88], 'F6': [268, 53, 342, 88]}
SOURCES = {'F5': 'Im3.jpg', 'F6': 'Im1.jpg'}
EXPECTED = {
    'PROTOCOL.md': '1ad63b566212539b9a7011650264d0ac427357fc5d9042670eea6d750fcabedc',
    'READERS.md': 'e2508d4ca55ea9e6f06fef260a7ab17613ecbe533be47376c5c63264c436da2f',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    '../approach34/read_context.py': '384d0bef93d4bc05ed8cb10f5a6d27426ab983ffcb4a3e31d5ca84b116961ac3',
    '../../native-strips01/Im1.jpg': '929f5d00d2f9ab1eba27a4aad8af37320a4fd37f2455f9b51d750ec7e15e8139',
    '../../native-strips01/Im3.jpg': 'af735345f189bba0eab7a836c5c0c6221ab30055febd81b52b331821fe87259b',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}


def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def inputs():
    result = {name: pin(HERE/name) for name in EXPECTED}
    if any(result[name]['sha256'] != sha for name, sha in EXPECTED.items()):
        raise ValueError('Frozen dependency changed')
    result['read_context.py'] = pin(Path(__file__))
    return result


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, HERE/relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['controls', 'save01', 'save02', 'show'])
    parser.add_argument('--pair', choices=list(TARGETS))
    parser.add_argument('--first', type=int)
    parser.add_argument('--last', type=int)
    args = parser.parse_args()
    before = inputs()
    h = module('native_context_base', '../read_context.py')
    display = module('native_lossless_display', '../approach34/read_context.py')
    if args.mode == 'controls':
        result = display.controls(h)
        result['context_counts'] = [(b[2]-b[0])*(b[3]-b[1]) for b in CONTEXTS.values()] == [10472, 2590]
        result['clipped_two_cell_contexts'] = all(CONTEXTS[k] == [max(0,b[0]-2),max(0,b[1]-2),min(745,b[2]+2),min(88,b[3]+2)] for k,b in TARGETS.items())
        if not all(result.values()) or before != inputs():
            raise AssertionError(result)
        print(json.dumps(result, sort_keys=True))
        return
    data = {}
    for pair, source in SOURCES.items():
        with Image.open(HERE/'../../native-strips01'/source) as im:
            if im.mode != 'RGB' or im.size != (745, 88):
                raise ValueError('Wrong source representation')
            data[pair] = h.cells(im, CONTEXTS[pair])
    if before != inputs():
        raise ValueError('Input changed')
    if args.mode == 'show':
        if args.pair is None or args.first is None or args.last is None:
            raise ValueError('Display range required')
        columns = h.sparse(data[args.pair], CONTEXTS[args.pair], args.first, args.last)
        print(f'{args.pair} context {CONTEXTS[args.pair]}. Omitted rows EXACT WHITE 255,255,255. gN=N,N,N; inclusive equal-RGB runs; no thresholds.')
        for x, column in columns.items():
            rendered = display.encode(column)
            if display.decode(rendered) != column:
                raise AssertionError('Display roundtrip')
            print(f'{x}: {rendered}')
        return
    output = {'inputs': before, 'sources': SOURCES, 'target_boxes': TARGETS,
              'context_boxes': CONTEXTS, 'python': platform.python_version(),
              'pillow': pillow_version, 'cells': data, 'classification': None,
              'human_accepted': False}
    target = HERE/('context'+args.mode[-2:]+'.json')
    h.save(target, output)
    if before != inputs():
        raise ValueError('Input changed after save; preserve output as failed')
    print(json.dumps({'output': pin(target), 'cells': {k: len(v) for k,v in data.items()}}))


if __name__ == '__main__':
    main()
