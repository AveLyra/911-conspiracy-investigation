"""Create-only full-page reading derivatives, not a measurement or PDF edit."""
import hashlib
import json
from pathlib import Path
import sys

import fitz

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf')
SHA = '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f'
PAGES = (53, 307, 308, 320, 321, 322, 323, 324)


def identity(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(p, d):
    with p.open('x') as f:
        json.dump(d, f, indent=2, sort_keys=True)
        f.write('\n')


def main():
    out = HERE/'render01'
    if out.exists():
        raise FileExistsError('Refusing existing reading derivatives')
    assert identity(SOURCE)['sha256'] == SHA
    paths = (SOURCE, Path(__file__), HERE/'PROTOCOL.md', Path(sys.executable))
    before = {str(p): identity(p) for p in paths}
    out.mkdir()
    save(out/'start.json', {'pins': before, 'physical_pages': PAGES, 'dpi': 150,
                            'python': sys.version, 'pymupdf': fitz.VersionBind,
                            'mupdf': fitz.VersionFitz})
    status = 'incomplete'
    pages = []
    try:
        with fitz.open(SOURCE) as doc:
            for page in PAGES:
                fitz.TOOLS.mupdf_warnings(reset=True)
                p = doc[page-1]
                pix = p.get_pixmap(dpi=150, alpha=False)
                pix.save(out/f'p{page}.png')
                with (out/f'p{page}.txt').open('x') as f:
                    f.write(p.get_text())
                pages.append({'physical_page': page, 'dimensions': [pix.width,pix.height],
                              'warnings': fitz.TOOLS.mupdf_warnings(reset=True)})
        status = 'complete_not_visual_review'
    finally:
        after = {str(p): identity(p) for p in paths}
        save(out/'receipt.json', {'status': status, 'pages': pages,
                                 'before': before, 'after': after,
                                 'inputs_unchanged': before == after,
                                 'products': {p.name: identity(p) for p in sorted(out.iterdir())}})
    assert before == after
    print(json.dumps({'status': status, 'pages': len(pages),
                      'warnings': sum(bool(p['warnings']) for p in pages)}))


if __name__ == '__main__':
    main()
