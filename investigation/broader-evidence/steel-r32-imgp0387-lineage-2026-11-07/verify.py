"""Compare preserved figure-named and camera-style JPEG entities locally.

python verify.py --figure /path/to/figure.jpg --camera /path/to/IMGP0387.JPG
No network, file mutation, physical-origin/custody or historical authentication.
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
    parser.add_argument('--figure', type=Path)
    parser.add_argument('--camera', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    assert bool(args.figure) == bool(args.camera), 'Supply both source files.'
    result = {'report_hash_matches': True, 'entities_checked': 0,
              'physical_identity_custody_or_date_authenticated': False}
    if args.figure:
        from PIL import Image
        raw, pixel = [], []
        for file, label in [(args.figure, 'figure'), (args.camera, 'camera_style')]:
            row = pins[label]
            data = file.read_bytes()
            assert len(data) == row['bytes']
            assert hashlib.sha256(data).hexdigest() == row['sha256']
            with Image.open(file) as image:
                image.load()
                assert image.format == 'JPEG'
                assert list(image.size) == row['size']
                assert dates(image) == pins['comparison']['selected_date_fields']
                rgb = image.convert('RGB').tobytes()
                assert hashlib.sha256(rgb).hexdigest() == pins['comparison']['decoded_RGB_sha256']
            raw.append(data)
            pixel.append(rgb)
            result['entities_checked'] += 1
        assert raw[0] == raw[1]
        assert pixel[0] == pixel[1]
        result.update({'exact_bytes_equal': True, 'decoded_RGB_equal': True})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
