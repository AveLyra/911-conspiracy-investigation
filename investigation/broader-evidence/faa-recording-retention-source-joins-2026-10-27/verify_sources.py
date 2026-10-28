"""Recheck exact safe anchors against the held released PDF; no raw text output.

Usage: python3 verify_sources.py SOURCE_PDF NEW_RESULT_JSON
Manual handwriting observations and source associations require separate review.
"""
from pathlib import Path
import hashlib
import json
import sys
import fitz

root = Path(__file__).parent
source, output = map(Path, sys.argv[1:])
pin = json.loads((root / 'SOURCE-PINS.json').read_text())[0]
body = source.read_bytes()
checks = []

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})

check('held source bytes/length',
      hashlib.sha256(body).hexdigest() == pin['sha256'] and len(body) == pin['bytes'])
doc = fitz.open(source)
check('physical source-page count', len(doc) == pin['physical_pages'] == 4380)
for anchor in json.loads((root / 'TYPED-PINS.json').read_text()):
    text = doc[anchor['physical_page'] - 1].get_text(sort=True)
    selected = text[anchor['char_start']:anchor['char_end']]
    lines = text.splitlines(True)
    check('source anchor ' + anchor['id'],
          hashlib.sha256(text.encode()).hexdigest() == anchor['page_text_sha256'] and
          selected == anchor['text'] == ''.join(lines[anchor['line_start'] - 1:anchor['line_end']]) and
          hashlib.sha256(selected.encode()).hexdigest() == anchor['sha256_utf8'])
check('source unchanged after read', hashlib.sha256(source.read_bytes()).hexdigest() == pin['sha256'])
result = {'checks': checks, 'passed': len(checks), 'typed_source_anchors': 10,
          'renderer_extractor': 'PyMuPDF ' + fitz.__version__,
          'scope': 'Source bytes and literal derivative anchors only; not handwriting or historical authentication',
          'redacted_identity_reconstruction': False, 'raw_text_output': False,
          'native_correction_receipt_or_disposition_acquired': False}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
print(str(len(checks)) + ' source/locator checks passed; source-association and historical limits remain.')
