"""Check documentary locators and bytes; does not validate calls or custody.

python verify.py --official-pdf /path/to/part02.pdf --mirror-pdf /path/to/12page.pdf --ocr
Requires pypdf; --ocr also needs pdftoppm and tesseract English data.
Rasters are processed in memory. No download, source modification or audio test.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def norm(text):
    # OCR and PDF text use different spacing/punctuation; preserve the source bytes.
    return re.sub(r'[^a-z0-9]', '', text.casefold())


def check_pdf(path, expected_size, expected_hash, expected_pages):
    from pypdf import PdfReader
    b = path.read_bytes()
    assert len(b) == expected_size
    assert hashlib.sha256(b).hexdigest() == expected_hash
    r = PdfReader(path)
    assert len(r.pages) == expected_pages
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--official-pdf', type=Path)
    ap.add_argument('--mirror-pdf', type=Path)
    ap.add_argument('--ocr', action='store_true')
    a = ap.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    assert all(pins['unperformed'].values())
    result = {'report_hash_matches': True, 'source_pdfs_checked': 0,
              'official_ocr_groups_checked': 0, 'native_audio_or_clock_test': False,
              'historical_authentication': False}
    if a.official_pdf:
        s = pins['official']
        check_pdf(a.official_pdf, s['bytes'], s['sha256'], s['pages'])
        result['source_pdfs_checked'] += 1
    if a.mirror_pdf:
        s = pins['mirror']
        r = check_pdf(a.mirror_pdf, s['bytes'], s['sha256'], 12)
        fields = pins['mirror_scope']['selected_document_fields']
        for page, names in [(1, ['first_BEGBATES', 'first_BEGPRODNO', 'first_metadata_DATE',
                                  'first_Date_of_transcription', 'first_body_case']),
                            (9, ['second_BEGBATES', 'second_BEGPRODNO', 'second_metadata_DATE',
                                  'second_Date_of_transcription', 'second_body_case'])]:
            text = norm(r.pages[page - 1].extract_text())
            for name in names:
                assert norm(fields[name]) in text, (page, name)
        result['source_pdfs_checked'] += 1
        result['mirror_selected_field_values_checked'] = 10
    if a.ocr:
        if not a.official_pdf:
            ap.error('--ocr requires --official-pdf')
        hashes = {}
        for row in pins['official_locator_groups']:
            page = str(row['page'])
            z = subprocess.run(['pdftoppm', '-f', page, '-l', page, '-singlefile',
                                '-r', '120', '-png', str(a.official_pdf)],
                               capture_output=True, check=True)
            assert z.stdout.startswith(b'\x89PNG\r\n\x1a\n')
            hashes[page] = hashlib.sha256(z.stdout).hexdigest()
            t = subprocess.run(['tesseract', 'stdin', 'stdout', '-l', 'eng', '--psm', '6'],
                               input=z.stdout, capture_output=True, check=True)
            text = norm(t.stdout.decode())
            for fragment in row['fragments']:
                assert norm(fragment) in text, (row['page'], fragment)
            result['official_ocr_groups_checked'] += 1
        result['render_hashes'] = hashes
        result['ocr_version'] = subprocess.run(['tesseract', '--version'],
                                              capture_output=True, text=True, check=True).stdout.splitlines()[0]
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
