"""Verify held policy bytes and visible-role locators, not case applicability.

python verify.py --pdf /path/to/recovered-order.pdf --check-ocr
Needs pypdf, pdftoppm and tesseract with English data. Page images stay in memory.
Without --pdf, only the reviewed report hash and explicit open-gate declarations
are checked. No download, source write or historical authentication occurs.
"""
import argparse
import base64
import hashlib
import json
import subprocess
from pathlib import Path


def normalized(text):
    return ' '.join(text.split()).casefold()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pdf', type=Path)
    ap.add_argument('--check-ocr', action='store_true')
    a = ap.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    assert not any(pins['case_gates'].values())
    result = {'report_hash_matches': True, 'case_completion_claimed': False,
              'policy_bytes_checked': False, 'historical_authentication': False,
              'ocr_page_count': 0, 'ocr_anchors_checked': 0}
    if a.check_ocr and not a.pdf:
        ap.error('--check-ocr requires --pdf')
    if a.pdf:
        import pypdf
        b = a.pdf.read_bytes()
        assert len(b) == pins['policy']['bytes']
        assert hashlib.sha256(b).hexdigest() == pins['policy']['sha256']
        digest = base64.b32encode(hashlib.sha1(b).digest()).decode().rstrip('=')
        assert digest == pins['policy']['archive_index']['digest']
        r = pypdf.PdfReader(a.pdf)
        assert len(r.pages) == pins['policy']['pages']
        assert not list(r.attachments)
        assert sum(len(p.extract_text()) for p in r.pages) == 0
        result.update(policy_bytes_checked=True, pdf_pages=len(r.pages),
                      cdx_digest_matches=True, embedded_text_characters=0)
        if a.check_ocr:
            texts = {}
            hashes = {}
            for page in sorted({x['page'] for x in pins['ocr_anchors']}):
                command = ['pdftoppm', '-f', str(page), '-l', str(page),
                           '-singlefile', '-r', '130', '-png', str(a.pdf)]
                render = subprocess.run(command, capture_output=True, check=True)
                assert render.stdout.startswith(b'\x89PNG\r\n\x1a\n')
                hashes[str(page)] = hashlib.sha256(render.stdout).hexdigest()
                ocr = subprocess.run(['tesseract', 'stdin', 'stdout', '-l', 'eng', '--psm', '6'],
                                     input=render.stdout, capture_output=True, check=True)
                texts[page] = ocr.stdout.decode().splitlines()
            for row in pins['ocr_anchors']:
                text = normalized('\n'.join(texts[row['page']][row['start_line']-1:row['end_line']]))
                for fragment in row['fragments']:
                    assert normalized(fragment) in text, (row['page'], row['role'], fragment)
                result['ocr_anchors_checked'] += 1
            result['ocr_page_count'] = len(texts)
            result['render_hashes'] = hashes
            result['ocr_version'] = subprocess.run(['tesseract', '--version'],
                                                  capture_output=True, text=True, check=True).stdout.splitlines()[0]
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
