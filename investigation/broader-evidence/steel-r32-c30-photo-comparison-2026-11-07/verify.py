"""Recheck preserved C30-group JPEG entities and optional reference identity.

python verify.py --photo-root /path/to/four/photos --reference /path/to/IMGP0388.JPG
No network, source writes, visual matching or historical authentication.
"""
import argparse
import hashlib
import json
from pathlib import Path


def dates(image):
    ex = image.getexif()
    sub = ex.get_ifd(34665) if ex.get(34665) is not None else {}
    out = {}
    for tag in [306, 36867, 36868]:
        if ex.get(tag) is not None:
            out[f'top:{tag}'] = ex[tag]
        if sub.get(tag) is not None:
            out[f'exif_ifd:{tag}'] = sub[tag]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--photo-root', type=Path)
    parser.add_argument('--reference', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    result = {'report_hash_matches': True, 'target_entities_checked': 0,
              'reference_identity_checked': False, 'physical_same_piece_accepted': False,
              'origin_custody_or_date_authenticated': False}
    if args.photo_root:
        from PIL import Image
        for row in pins['photos']:
            file = args.photo_root / row['file']
            assert file.stat().st_size == row['bytes'] == row['declared_bytes']
            assert hashlib.sha256(file.read_bytes()).hexdigest() == row['sha256']
            with Image.open(file) as image:
                image.load()
                assert image.format == 'JPEG'
                assert list(image.size) == row['size']
                assert image.mode == row['mode']
                assert dates(image) == row['selected_dates']
            result['target_entities_checked'] += 1
    if args.reference:
        assert args.reference.stat().st_size == pins['reference']['bytes']
        assert hashlib.sha256(args.reference.read_bytes()).hexdigest() == pins['reference']['sha256']
        result['reference_identity_checked'] = True
    assert pins['feature_review']['overall_acceptance'] == 'unconfirmed'
    assert pins['feature_review']['blind_or_independent_review_performed'] is False
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
