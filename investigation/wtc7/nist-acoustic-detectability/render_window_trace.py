"""Reading derivatives for eight declared window-citation pages; no PDF edits."""
from pathlib import Path
import sys

from render import ENV, POPPLER, identity, run, save

HERE = Path(__file__).resolve().parent
BASE = Path('/Users/admin/docs/911/authority/nist/wtc7')
SOURCES = (
    ('ncstar-1-9.pdf', '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f',
     'technical', (165, 166, 168, 290, 303, 304)),
    ('ncstar-1a.pdf', '03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09',
     'summary', (69,)),
    ('wtc7-revised-technical-briefing-111908.pdf',
     'b8845c40205a4731d248b6398858dfabedbb927e01f8d6acd1422b40f2fa4850',
     'briefing', (54,)),
)


def main():
    out = HERE / 'window-source-render01'
    if out.exists():
        raise FileExistsError('Preserve prior derivatives; no overwrite')
    for name, expected, _, _ in SOURCES:
        if identity(BASE / name)['sha256'] != expected:
            raise ValueError(f'Source identity changed: {name}')
    files = [BASE / row[0] for row in SOURCES] + [
        Path(__file__), HERE / 'render.py', HERE / 'WINDOW-SOURCE-TRACE-SCOPE.md',
        Path(sys.executable), POPPLER / 'bin/pdftoppm', POPPLER / 'bin/pdftotext']
    pins = {str(p): identity(p) for p in files}
    out.mkdir()
    save(out / 'start.json', {'pins': pins, 'selection': SOURCES, 'dpi': 120,
                            'environment': ENV, 'python': sys.version})
    status = 'incomplete'
    try:
        for name, _, prefix, pages in SOURCES:
            for page in pages:
                target = out / f'{prefix}-p{page}'
                run([POPPLER / 'bin/pdftoppm', '-f', str(page), '-l', str(page),
                     '-singlefile', '-r', '120', '-png', BASE / name, target],
                    out / f'{prefix}-p{page}-render')
                run([POPPLER / 'bin/pdftotext', '-f', str(page), '-l', str(page),
                     '-layout', BASE / name, target.with_suffix('.txt')],
                    out / f'{prefix}-p{page}-text')
        status = 'commands_complete_not_visual_review'
    finally:
        after = {p: identity(Path(p)) for p in pins}
        save(out / 'receipt.json', {'status': status, 'pins_before': pins,
             'pins_after': after, 'pins_unchanged': pins == after,
             'products': {p.name: identity(p) for p in sorted(out.iterdir())}})
    if pins != after:
        raise ValueError('Pinned input changed during rendering')
    print(status, '8 selected pages', '8 PNGs', '8 text derivatives')


if __name__ == '__main__':
    main()
