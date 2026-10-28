"""Verify supplied visible-image OCR comparisons; never emits source text.

Usage: python3 verify_controls.py PDF_DIRECTORY OCR_DIRECTORY NEW_RESULT_JSON
Reproduce the visible readings independently from the source pages.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

root = Path(__file__).parent
pdf_dir, ocr_dir, output = map(Path, sys.argv[1:])
pins = json.loads((root / 'SOURCE-PINS.json').read_text())
rows = json.loads((root / 'OCR-OBSERVATIONS.json').read_text())
controls = json.loads((root / 'MANUAL-OCR-CONTROLS.json').read_text())
checks = []

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})

def norm(text):
    return re.sub('[^a-z0-9]', '', text.lower())

for source in pins:
    body = (pdf_dir / source['filename']).read_bytes()
    check(source['id'] + ' source pin',
          len(body) == source['bytes'] and hashlib.sha256(body).hexdigest() == source['sha256'])
check('selected rows and source split', len(rows) == 90 and
      sum(x['source'] == 'DOT-INTERVIEWS' for x in rows) == 77 and
      sum(x['source'] == 'FAA-NEADS' for x in rows) == 13)
check('selected page keys unique', len({(x['source'], x['physical_page']) for x in rows}) == 90)
texts = {}
for row in rows:
    name = row['source'].lower() + '-p' + str(row['physical_page']) + '.txt'
    body = (ocr_dir / name).read_bytes()
    if hashlib.sha256(body).hexdigest() != row['ocr_text_sha256']:
        raise AssertionError('OCR file hash')
    text = body.decode()
    if len(''.join(text.split())) != row['non_whitespace_chars']:
        raise AssertionError('OCR character count')
    texts[(row['source'], row['physical_page'])] = text
check('all90 OCR entity pins and supplied character counts', len(texts) == 90)
for c in controls:
    text = texts[('DOT-INTERVIEWS', c['physical_page'])]
    anchor = c['visible_manual_anchor']
    check('manual anchor comparison p' + str(c['physical_page']),
          (anchor.lower() in text.lower()) is c['literal_present'] and
          (norm(anchor) in norm(text)) is c['alphanumeric_present'] and
          c['literal_present'] is False and c['alphanumeric_present'] is False)
check('positive matcher control', norm('suspicious aircraft') in norm('SUSPICIOUS - AIRCRAFT'))
result = {'passed': len(checks), 'checks': checks, 'source_pdfs': 2, 'selected_ocr_pages': 90,
          'manual_controls': 4, 'scope': 'Pinned bytes and supplied visible-reading/OCR comparisons only',
          'historical_authentication_or_absence_proved': False,
          'correction_receipt_or_administrative_decision_acquired': False,
          'raw_text_emitted': False}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
print(str(len(checks)) + ' scoped checks passed; no historical absence or disposition established.')
