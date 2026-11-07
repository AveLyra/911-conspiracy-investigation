"""Verify this correction's public-report citations, not historical claims.

python verify.py --prior-dir /path/to/three-preserved-public-report-bodies
No download, file mutation, primary-source/audio test or historical validation.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prior-dir', type=Path)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    assert pins['new_historical_record_or_native_input_acquired'] is False
    assert pins['new_audio_or_clock_test_completed'] is False
    result = {'report_hash_matches': True, 'public_reports_checked': 0,
              'exact_report_line_anchors_checked': 0, 'historical_validation': False,
              'native_input_acceptance_completed': False}
    if a.prior_dir:
        for row in pins['sources']:
            f = a.prior_dir / row['file']
            assert f.stat().st_size == row['bytes']
            assert hashlib.sha256(f.read_bytes()).hexdigest() == row['sha256']
            lines = f.read_text().splitlines()
            for anchor in row['line_anchors']:
                assert anchor['fragment'].casefold() in lines[anchor['line'] - 1].casefold()
                result['exact_report_line_anchors_checked'] += 1
            result['public_reports_checked'] += 1
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
