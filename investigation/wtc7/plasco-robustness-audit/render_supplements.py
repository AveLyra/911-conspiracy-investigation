"""Two predeclared full-page legibility supplements; not measurements."""
import json
from pathlib import Path
import sys

from PIL import Image
import derive


def main():
    target = derive.HERE / 'supplements01'
    target.mkdir(exist_ok=False)
    paths = {**derive.dependencies(), 'supplement_code': Path(__file__).resolve(),
             'parent_receipt': derive.HERE / 'run02/receipt.json'}
    before = derive.snapshot(paths)
    result = {'status': 'failed', 'pages': [], 'pins_before': before,
              'purpose': 'Full-page legibility only: physical117 Fig3.9 legends; physical120 Fig3.12 legends',
              'command': [sys.executable, *sys.argv], 'dpi': 300}
    try:
        if any('error' in item for item in before.values()):
            raise ValueError('Unreadable dependency')
        if before['parent_receipt']['sha256'] != 'd2c203d1bb9cf243e1cbdfc68a204c3996df358b65528d8df171fe0ec645524c':
            raise ValueError('Parent receipt changed')
        parent = json.loads(paths['parent_receipt'].read_text())
        if parent['status'] != 'complete' or not parent['pins_unchanged']:
            raise ValueError('Parent run incomplete')
        for name, item in parent['pins_after'].items():
            if before[name] != item:
                raise ValueError('Parent dependency changed: ' + name)
        (target / 'font-cache').mkdir()
        env = derive.environment(target)
        result['environment'] = env
        for number in (117, 120):
            stem = target / f'page-{number:03d}'
            row = {'physical_page': number, 'printed_page': number - 15}
            result['pages'].append(row)
            argv = [derive.RENDERER, '-f', str(number), '-l', str(number),
                    '-r', '300', '-singlefile', '-png', derive.SOURCE, stem]
            row['render'] = derive.command(argv, Path(str(stem) + '-render'), env)
            png = stem.with_suffix('.png')
            if row['render']['status'] != 'returned' or row['render']['returncode'] != 0 or not png.is_file():
                raise RuntimeError('Supplement render failed')
            row['png'] = {'path': png.name, **derive.pin(png)}
            with Image.open(png) as picture:
                row['dimensions'] = list(picture.size)
                picture.verify()
        result['status'] = 'complete'
    except Exception as error:
        result['failure'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        result['pins_after'] = derive.snapshot(paths)
        result['pins_unchanged'] = result['pins_after'] == before
        if not result['pins_unchanged']:
            result['status'] = 'failed'
        result['products'] = {p.name: derive.pin(p) for p in sorted(target.iterdir()) if p.is_file()}
        derive.write_json(target / 'receipt.json', result)
    print(json.dumps({'status': result['status'], 'pages': len(result['pages'])}))
    return 0 if result['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
