#!/usr/bin/env python3
"""Check retained acquisition integrity and coverage; does not validate an assay."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
manifest = json.loads((root / 'source-manifest.json').read_text())
failures = []
for entry in manifest:
    path = root / entry['path']
    if not path.is_file():
        failures.append(f"Missing: {entry['path']}")
        continue
    data = path.read_bytes()
    if len(data) != entry['bytes']:
        failures.append(f"Size mismatch: {entry['path']}")
    if hashlib.sha256(data).hexdigest() != entry['sha256']:
        failures.append(f"SHA-256 mismatch: {entry['path']}")
    if entry.get('archive_md5') and hashlib.md5(data).hexdigest() != entry['archive_md5']:
        failures.append(f"Archive MD5 mismatch: {entry['path']}")

core_count = 0
initial_empty = []
expected = {1: 141, 2: 87, 3: 100, 4: 16, 5: 141, 6: 94}
for number, page_count in expected.items():
    pages = json.loads((root / f'derived/section-{number}-ocr-pages.json').read_text())
    core_count += len(pages)
    if len(pages) != page_count:
        failures.append(f"OCR page count mismatch: section {number}")
    initial_empty.extend((number, i + 1) for i, text in enumerate(pages) if not text.strip())
fallback = json.loads((root / 'derived/core-blank-page-fallback-ocr.json').read_text())
if set(initial_empty) != {(r['section'], r['page']) for r in fallback}:
    failures.append('Initially empty OCR pages are not fully covered by fallback records')
for row in fallback:
    if not (root / 'page-images' / row['image']).is_file():
        failures.append(f"Missing fallback page image: {row['image']}")

irmep_count = 0
for number in range(15):
    name = f'irmep-{number}-ocr-pages.json' if number in (13, 14) else f'irmep-{number}-pages.json'
    pages = json.loads((root / 'derived' / name).read_text())
    irmep_count += len(pages)
if irmep_count != 180:
    failures.append(f'IRmep unique PDF coverage mismatch: {irmep_count}')

originals = [e for e in manifest if e['role'] == 'downloaded-original-pdf']
archive_matches = sum(bool(e.get('archive_md5')) for e in manifest)
print(f'Retained file hashes checked: {len(manifest)}')
print(f'Original PDFs: {len(originals)}; PDF pages: {sum(e["pages"] for e in originals)}')
print(f'Internet Archive metadata MD5 comparisons: {archive_matches}')
print(f'Core OCR coverage: {core_count} pages; initially empty pages with fallback and images: {len(initial_empty)}')
print(f'IRmep unique PDF OCR/text coverage: {irmep_count} pages, including 3 cover-letter pages')
print('Scope: acquisition integrity and page coverage only; redactions, authenticity, and chemical outcome remain separate questions.')
if failures:
    print('\n'.join(failures))
    raise SystemExit(1)
print('PASS: retained bytes and declared page coverage match the acquisition manifest.')
