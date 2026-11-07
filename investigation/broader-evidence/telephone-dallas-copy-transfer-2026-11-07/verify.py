"""Verify held-source identity and reading locators, not the historical account.

Usage: python verify.py --pdf /path/to/preserved-packet.pdf --ocr-dir /path/to/renders
OCR files are native-only packet6-NNN.ocr.txt outputs from the six pinned images.
No network, file writes, recording test or historical authentication.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--ocr-dir', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    result = {'report_hash_matches': True, 'pdf_identity_checked': False,
              'ocr_page_groups_checked': 0, 'anchor_fragments_checked': 0,
              'audio_test_performed': False, 'historical_authentication': False}
    if args.pdf:
        from pypdf import PdfReader
        assert args.pdf.stat().st_size == pins['source']['bytes']
        assert hashlib.sha256(args.pdf.read_bytes()).hexdigest() == pins['source']['sha256']
        assert len(PdfReader(args.pdf).pages) == pins['source']['pdf_pages']
        result['pdf_identity_checked'] = True
    if args.ocr_dir:
        for row in pins['reading']:
            image = args.ocr_dir / f"packet6-{row['pdf_page']:03d}.png"
            ocr = args.ocr_dir / f"packet6-{row['pdf_page']:03d}.ocr.txt"
            assert hashlib.sha256(image.read_bytes()).hexdigest() == row['image_sha256']
            assert hashlib.sha256(ocr.read_bytes()).hexdigest() == row['ocr_sha256']
            text = ' '.join(ocr.read_text().split()).casefold()
            for fragment in row['ocr_anchor_fragments']:
                assert fragment.casefold() in text, (row['pdf_page'], fragment)
                result['anchor_fragments_checked'] += 1
            result['ocr_page_groups_checked'] += 1
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
