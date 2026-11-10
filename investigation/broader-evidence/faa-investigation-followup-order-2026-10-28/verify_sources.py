"""Check preserved public policy bytes, page renders, OCR anchors and revisions.

Requires existing PyMuPDF and Tesseract. Does not install software. OCR checks
support locators; they do not authenticate historical applicability or case acts.
Optional --local-unit adds preservation/diff checks using the retained originals.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import base64
import datetime
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import fitz as pymupdf

parser = argparse.ArgumentParser()
parser.add_argument('--local-unit', type=Path)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
checks = []


def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)


source = json.loads((root / 'SOURCES.json').read_text())
body = (root / source['public_preserved_source']).read_bytes()
order = source['order']
check('PDF body signature, bytes and SHA-256',
      body.startswith(b'%PDF-') and len(body) == order['bytes'] == 1679636
      and hashlib.sha256(body).hexdigest() == order['sha256'])
check('Body SHA-1/base32 equals indexed digest',
      base64.b32encode(hashlib.sha1(body).digest()).decode() == order['sha1_base32']
      == order['cdx_row']['digest'])
index = json.loads((root / 'ARCHIVE-INDEX.json').read_text())
rows = [dict(zip(index[0], row)) for row in index[1:]]
check('Three indexed captures preserved with separate record lengths',
      [r['timestamp'] for r in rows] == ['20241030203137', '20250205003928', '20260508115415']
      and [r['length'] for r in rows] == ['1668081', '1668284', '1668304']
      and all(r['digest'] == order['sha1_base32'] for r in rows)
      and rows[0] == order['cdx_row'])
doc = pymupdf.open(stream=body, filetype='pdf')
check('15 physical pages, zero native extracted text', len(doc) == 15
      and sum(len(page.get_text()) for page in doc) == 0)
scope = json.loads((root / 'READING-SCOPE.json').read_text())
check('Reading scope distinguishes physical pages and chapters',
      scope['physical_pages_read'] == list(range(1, 16)) and scope['native_text_characters'] == 0)
rendered = []
for i, page in enumerate(doc, 1):
    pixels = page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), alpha=False).tobytes('png')
    expected = scope['images'][i - 1]
    check(f'Physical page {i} reproduces retained source raster',
          expected['physical_page'] == i and len(pixels) == expected['bytes']
          and hashlib.sha256(pixels).hexdigest() == expected['sha256'])
    rendered.append(pixels)
tess = shutil.which('tesseract')
check('Existing Tesseract available; nothing installed', tess is not None)
version = subprocess.run([tess, '--version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]


def ocr(pixels):
    p = subprocess.run([tess, 'stdin', 'stdout', '--psm', '6'], input=pixels,
                       capture_output=True, check=True)
    return re.sub(r'\s+', ' ', p.stdout.decode()).lower()


with ThreadPoolExecutor(max_workers=3) as pool:
    texts = list(pool.map(ocr, rendered))
anchors = {
    1: ['8000.1¢', '7-20-89', '8000.1b'],
    2: ['audits'],
    11: ['investigations', 'assistant inspector general for investigations', 'followup system'],
    12: ['record of resolution action', 'other than those involving personnel actions', 'when warranted'],
    13: ['usually'],
    14: ['records of disclosure', 'reverse side of the report cover', 'number of copies made'],
    15: ['if no action was taken, notification shall include the reasons why.',
         'normally, dot elements will be requested', 'within 60 days', 'closing action']
}
for page, phrases in anchors.items():
    check(f'OCR anchor support on physical page {page}', all(p in texts[page - 1] for p in phrases))
locators = json.loads((root / 'CLAIM-LOCATORS.json').read_text())
check('Ten source/line locators resolve to their recorded IDs',
      len(locators) == 10 and all((root / r['file']).read_text().splitlines()[r['line'] - 1]
                                .startswith('- ' + r['id'] + ' ') for r in locators))
report = (root / 'README.md').read_text()
check('Archive link equals acquired URL and contains no unencoded space',
      f'[Archived PDF]({order["url"]})' in report and ' ' not in order['url'])
check('Reader qualifications retained', all(s in report for s in [
    'normally be requested', 'excludes personnel actions', 'No current FOIA withholding conclusion',
    'PD01–PD04 and all five native-input/testing gates remain open']))
check('No raw local or credential paths in public text',
      all('/Users/' not in p.read_text() and '/Volumes/' not in p.read_text()
          for p in root.rglob('*') if p.is_file() and p.suffix in {'.json', '.md'}))
revision = json.loads((root / 'REVISION-STATUS.json').read_text())
if args.local_unit:
    unit = args.local_unit
    predecessor = unit.parent / 'faa-original-disposition-roots-2026-10-27/REVIEW.md'
    draft = unit / 'publication/README.md'
    check('Prior policy checkpoint unchanged', hashlib.sha256(predecessor.read_bytes()).hexdigest()
          == revision['preceding_policy_checkpoint_sha256'])
    check('Unpublished draft unchanged', hashlib.sha256(draft.read_bytes()).hexdigest()
          == revision['unpublished_draft_sha256'])
    for old, diff, label in [
        (predecessor, 'policy-checkpoint-to-full-order-review.diff', 'preceding-preserved-policy-checkpoint/REVIEW.md'),
        (draft, 'draft-to-final.diff', 'preserved-unpublished-draft/README.md')]:
        expected = ''.join(difflib.unified_diff(old.read_text().splitlines(True), report.splitlines(True),
                                               fromfile=label, tofile='README.md'))
        check('Exact regenerated ' + diff, expected == (root / 'diffs' / diff).read_text())
    acquisition = json.loads((unit / 'POLICY-ACQUISITION-LOCAL.json').read_text())
    check('Intel original and public copy remain identical',
          Path(acquisition['path']).read_bytes() == body)
result = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'checks': checks, 'passed': len(checks), 'failed': 0,
          'pymupdf': pymupdf.VersionBind, 'tesseract': version,
          'ocr_scope': 'All 15 visible-page OCR derivatives regenerated; selected anchors checked. Manual source-image reading recorded separately.',
          'limits': 'Source/derivative integrity and record leads only. No governing-edition authentication, case-specific decision, correction/receipt, laboratory replication or misconduct finding.'}
with args.output.open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
print(f'{len(checks)} checks passed; substantive FAA and other track gates remain open.')
