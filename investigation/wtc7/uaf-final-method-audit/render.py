"""Create-only reading derivatives; adapted from lateral-geometry-audit/render.py."""
import hashlib
import json
from pathlib import Path
import sys

import pymupdf as fitz

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source/uaf-final-2020.pdf'
SHA = 'f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa'
PAGES = (1, 3, 4, 34, 35, 36, 37, 38, 39, 40, 44, 50, 51, 52,
         65, 66, 67, 68, *range(105, 124))


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def save(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write('\n')


def main():
    out = HERE / 'render01'
    if out.exists():
        raise FileExistsError('Refusing existing reading derivatives')
    assert identity(SOURCE) == {'bytes': 45196602, 'sha256': SHA}
    assert len(PAGES) == len(set(PAGES)) == 37
    paths = (SOURCE, Path(__file__), HERE/'PROTOCOL.md',
             HERE/'PAGE-SELECTION.md', Path(sys.executable))
    before = {str(p): identity(p) for p in paths}
    out.mkdir()
    save(out/'start.json', {'pins': before, 'physical_pages': PAGES, 'dpi': 150,
                            'python': sys.version, 'pymupdf': fitz.VersionBind,
                            'mupdf': fitz.VersionFitz})
    status = 'incomplete'
    pages = []
    try:
        fitz.TOOLS.mupdf_warnings(reset=True)
        with fitz.open(SOURCE) as doc:
            assert doc.is_pdf and not doc.is_repaired and not doc.is_encrypted
            assert len(doc) == 125
            opening_warnings = fitz.TOOLS.mupdf_warnings(reset=True)
            if opening_warnings:
                save(out/'opening-warning.json', opening_warnings)
                raise RuntimeError('PDF opening diagnostics preserved')
            for page in PAGES:
                fitz.TOOLS.mupdf_warnings(reset=True)
                p = doc[page-1]
                pix = p.get_pixmap(dpi=150, alpha=False)
                pix.save(out/f'p{page}.png')
                with (out/f'p{page}.txt').open('x') as stream:
                    stream.write(p.get_text())
                pages.append({'physical_page': page,
                              'dimensions': [pix.width, pix.height],
                              'warnings': fitz.TOOLS.mupdf_warnings(reset=True)})
        status = 'complete_not_visual_review'
    finally:
        after = {str(p): identity(p) for p in paths}
        save(out/'receipt.json', {'status': status, 'pages': pages,
                                 'before': before, 'after': after,
                                 'inputs_unchanged': before == after,
                                 'products': {p.name: identity(p)
                                              for p in sorted(out.iterdir())}})
    assert before == after
    print(json.dumps({'status': status, 'pages': len(pages),
                      'warnings': sum(bool(p['warnings']) for p in pages)}))


if __name__ == '__main__':
    main()
