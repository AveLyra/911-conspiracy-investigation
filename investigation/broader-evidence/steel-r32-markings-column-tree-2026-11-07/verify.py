"""Recheck the two preserved public JPEG entities and selected metadata.

python verify.py --image-root /path/to/preserved/sources
No network, mutation, OCR, visual identification or historical authentication.
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
    parser.add_argument('--image-root', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    checked = 0
    if args.image_root:
        from PIL import Image
        for row in pins['photos']:
            p = args.image_root / row['file']
            assert p.stat().st_size == row['bytes'] == row['declared_catalog_bytes']
            assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
            with Image.open(p) as image:
                image.load()
                assert image.format == 'JPEG'
                assert list(image.size) == row['size']
                assert image.mode == row['mode']
                assert dates(image) == row['selected_date_fields']
            checked += 1
    print(json.dumps({'report_hash_matches': True,
                      'source_entities_and_metadata_checked': checked,
                      'physical_identity_or_custody_verified': False,
                      'date_or_origin_authenticated': False}, indent=2))


if __name__ == '__main__':
    main()
