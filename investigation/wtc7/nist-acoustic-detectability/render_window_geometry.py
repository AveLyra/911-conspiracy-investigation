"""Four fixed complete-page reading derivatives; never overwrite a run."""
from pathlib import Path
import sys

from render import ENV, POPPLER, identity, run, save

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
SOURCE_SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
PAGES = (58, 100, 141, 142)


def main():
    out = HERE / 'window-geometry-render01'
    if out.exists():
        raise FileExistsError('Preserve previous derivatives; no overwrite')
    if identity(SOURCE)['sha256'] != SOURCE_SHA:
        raise ValueError('Source identity changed')
    files = [SOURCE, Path(__file__), HERE / 'render.py',
             HERE / 'WINDOW-GEOMETRY-SCOPE.md', Path(sys.executable),
             POPPLER / 'bin/pdftoppm', POPPLER / 'bin/pdftotext']
    pins = {str(p): identity(p) for p in files}
    out.mkdir()
    save(out / 'start.json', {'pins': pins, 'pages': PAGES, 'dpi': 150,
                            'environment': ENV, 'python': sys.version})
    status = 'incomplete'
    try:
        for page in PAGES:
            target = out / f'p{page}'
            run([POPPLER / 'bin/pdftoppm', '-f', str(page), '-l', str(page),
                 '-singlefile', '-r', '150', '-png', SOURCE, target],
                out / f'p{page}-render')
            run([POPPLER / 'bin/pdftotext', '-f', str(page), '-l', str(page),
                 '-layout', SOURCE, target.with_suffix('.txt')],
                out / f'p{page}-text')
        status = 'commands_complete_not_visual_review'
    finally:
        after = {p: identity(Path(p)) for p in pins}
        save(out / 'receipt.json', {'status': status, 'pins_before': pins,
             'pins_after': after, 'pins_unchanged': pins == after,
             'products': {p.name: identity(p) for p in sorted(out.iterdir())}})
    if pins != after:
        raise ValueError('Pinned input changed during rendering')
    print(status, '4 declared pages; 4 PNGs; 4 text derivatives')


if __name__ == '__main__':
    main()
