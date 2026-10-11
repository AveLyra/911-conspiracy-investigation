"""Preserve every RGB cell in the declared inspection context; no classifier."""
import hashlib
import json
from pathlib import Path
import platform
from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'native-strips01/Im4.jpg'
EXPECTED = '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd'


def pin(path):
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


def main():
    before = pin(SOURCE)
    if before['sha256'] != EXPECTED:
        raise ValueError('Source changed')
    with Image.open(SOURCE) as image:
        if image.size != (741, 88) or image.mode != 'RGB':
            raise ValueError('Unexpected native representation')
        cells = [{'x': x, 'y': y, 'rgb': list(image.getpixel((x, y)))}
                 for y in range(55) for x in range(298, 310)]
    if pin(SOURCE) != before:
        raise ValueError('Source changed during read')
    result = {'source': str(SOURCE), 'source_pin': before,
              'protocol_pin': pin(HERE / 'PROTOCOL.md'), 'script_pin': pin(Path(__file__)),
              'python': platform.python_version(), 'pillow': pillow_version,
              'coordinates': 'zero-based native pixel cells',
              'context_half_open': [298, 0, 310, 55], 'cells': cells,
              'classification': None, 'human_accepted': False}
    with (HERE / 'raw-context.json').open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'cells': len(cells), 'output': pin(HERE / 'raw-context.json')}))


if __name__ == '__main__':
    main()
