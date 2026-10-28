"""Verify two held PDF identities and ten safe derivative/source joins.

python3 verify_sources.py DOT_PDF FAA_PDF DOT_TEXT FAA_TEXT NEW_OUTPUT_JSON
Uses already installed pypdf; does not acquire sources or change their bytes.
No historical authentication, completeness or physical validation is implied.
"""
import hashlib
import io
import json
from pathlib import Path
import sys
import pypdf

root = Path(__file__).resolve().parent
dot_pdf, faa_pdf, dot_text, faa_text, output = map(Path, sys.argv[1:])
pins = json.loads((root / 'SOURCE-PINS.json').read_text())
anchors = json.loads((root / 'SOURCE-ANCHORS.json').read_text())
checks = []


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    checks.append({'check': label, 'passed': True})


def normalized(text):
    return ' '.join(text.split())


for pin, pdf_path, text_path in zip(pins, [dot_pdf, faa_pdf], [dot_text, faa_text]):
    body = pdf_path.read_bytes()
    check(pin['id'] + ' PDF identity',
          len(body) == pin['bytes'] and hashlib.sha256(body).hexdigest() == pin['sha256'])
    reader = pypdf.PdfReader(io.BytesIO(body))
    check(pin['id'] + ' physical page count', len(reader.pages) == pin['physical_pages'])
    text_bytes = text_path.read_bytes()
    check(pin['id'] + ' held derivative hash',
          hashlib.sha256(text_bytes).hexdigest() == pin['text_sha256'])
    pages = text_bytes.decode('utf-8').split('\f')
    if not pages[-1].strip():
        pages.pop()
    check(pin['id'] + ' derivative page count', len(pages) == pin['physical_pages'])
    extracted = {}
    for anchor in [a for a in anchors if a['source'] == pin['id']]:
        n = anchor['physical_page']
        text = pages[n - 1]
        selected = text[anchor['char_start']:anchor['char_end']]
        check(anchor['id'] + ' exact cached locator and excerpt',
              hashlib.sha256(text.encode()).hexdigest() == anchor['page_text_sha256']
              and selected == anchor['text']
              and hashlib.sha256(selected.encode()).hexdigest() == anchor['sha256_utf8']
              and text[:anchor['char_start']].count('\n') + 1 == anchor['line_start']
              and text[:anchor['char_end']].count('\n') + 1 == anchor['line_end'])
        if n not in extracted:
            extracted[n] = reader.pages[n - 1].extract_text()
        check(anchor['id'] + ' fresh PDF extraction contains safe excerpt',
              normalized(selected) in normalized(extracted[n]))
    check(pin['id'] + ' PDF unchanged after read',
          hashlib.sha256(pdf_path.read_bytes()).hexdigest() == pin['sha256'])

result = {'passed': len(checks), 'checks': checks, 'source_pdfs': len(pins),
          'safe_excerpts': len(anchors), 'extractor': 'pypdf ' + pypdf.__version__,
          'scope': 'File identity, page counts and literal derivative/source joins only',
          'historical_or_device_validation': False, 'raw_private_text_printed': False,
          'original_memo_handbook_checklist_or_custody_form_acquired': False}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
print(f'{len(checks)} source/locator checks passed; no historical validation claimed.')
