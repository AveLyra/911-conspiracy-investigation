"""Preserve the declared native corridor; print lossless sparse column blocks."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'native-strips01/Im4.jpg'
SOURCE_SHA = '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd'
PROTOCOL_SHA = '12525bcb149368f18d85e3611f32137ccdeef723cc95df93cf2b5d9b13f2aa27'


def pin(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['save', 'show'])
    parser.add_argument('--first', type=int, default=270)
    parser.add_argument('--last', type=int, default=284)
    args = parser.parse_args()
    if not 268 <= args.first <= args.last <= 361:
        raise ValueError('Display outside declared context')
    before = pin(SOURCE)
    protocol = pin(HERE / 'PROTOCOL.md')
    if before['sha256'] != SOURCE_SHA or protocol['sha256'] != PROTOCOL_SHA:
        raise ValueError('Source or protocol changed')
    with Image.open(SOURCE) as raster:
        if raster.size != (741, 88) or raster.mode != 'RGB':
            raise ValueError('Unexpected native source representation')
        cells = [{'x': x, 'y': y, 'rgb': list(raster.getpixel((x, y)))}
                 for y in range(88) for x in range(268, 362)]
    if pin(SOURCE) != before:
        raise ValueError('Source changed during read')
    if args.mode == 'save':
        result = {'source': str(SOURCE), 'source_pin': before, 'protocol_pin': protocol,
                  'script_pin': pin(Path(__file__)), 'python': platform.python_version(),
                  'pillow': pillow_version, 'context_half_open': [268, 0, 362, 88],
                  'coordinates': 'zero-based native cells', 'cells': cells,
                  'row_major_rgb_sha256': hashlib.sha256(bytes(v for c in cells for v in c['rgb'])).hexdigest(),
                  'classification': None, 'human_accepted': False}
        with (HERE / 'raw-context.json').open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
            stream.write('\n')
        print(json.dumps({'cells': len(cells), 'output': pin(HERE / 'raw-context.json')}))
    else:
        print('Exact RGB; omitted rows are exactly (255,255,255). g denotes (g,g,g); other triples explicit. No threshold. All rows 0..87 represented by values or this omission convention.')
        for x in range(args.first, args.last + 1):
            values = []
            for c in cells:
                if c['x'] == x and c['rgb'] != [255, 255, 255]:
                    r, g, b = c['rgb']
                    value = str(r) if r == g == b else f'({r},{g},{b})'
                    values.append(f"{c['y']}:{value}")
            print(f'x={x} ' + ' '.join(values))


if __name__ == '__main__':
    main()
