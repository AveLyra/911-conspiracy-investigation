"""Reproduce source identity and visible-page checks; not historical validation.

python3 verify_source.py HELD_SOURCE_PDF NEW_RESULT_JSON
No extraction behind redactions, OCR, network, installation or source mutation.
"""
from pathlib import Path
import hashlib
import io
import json
import sys
import fitz
from PIL import Image

root = Path(__file__).resolve().parent
source, output = map(Path, sys.argv[1:])
pin = json.loads((root / 'SOURCE-PINS.json').read_text())[0]
coverage = json.loads((root / 'READING-COVERAGE.json').read_text())
body = source.read_bytes()
checks = []


def check(name, okay):
    if not okay:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})


check('source SHA256', hashlib.sha256(body).hexdigest() == pin['sha256'])
check('source byte count', len(body) == pin['bytes'])
doc = fitz.open(stream=body, filetype='pdf')
check('physical pages', len(doc) == pin['physical_pages'] == 287)
check('no extractable text in current tool', sum(len(p.get_text()) for p in doc) == 0)
for image in coverage['image_hashes']:
    page = image['physical_page']
    png = doc[page - 1].get_pixmap(matrix=fitz.Matrix(1.65, 1.65), alpha=False).tobytes('png')
    check('read page raster ' + str(page), hashlib.sha256(png).hexdigest() == image['png_sha256'])
ratios = []
for page in range(252, 275):
    pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(.2, .2), alpha=False)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    dark = sum(1 for rgb in im.getdata() if max(rgb) <= 10)
    fraction = dark / (pix.width * pix.height)
    check('visible black-panel area ' + str(page), fraction > .65)
    ratios.append({'physical_page': page, 'dark_fraction': fraction})
check('source unchanged after read', hashlib.sha256(source.read_bytes()).hexdigest() == pin['sha256'])
result = {'passed': len(checks), 'checks': checks, 'dark_fractions': ratios,
          'pymupdf': fitz.__version__, 'scope': 'Byte identity, current text availability, read-page raster joins and visible black coverage only',
          'manual_reading_validation': False, 'historical_clock_or_authorship_validation': False,
          'redaction_legality_or_motive_determined': False, 'covered_content_recovery_attempted': False}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
print(f'{len(checks)} source/render/visibility checks passed; no historical or legal conclusion.')
