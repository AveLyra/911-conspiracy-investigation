"""Recheck photo entities/metadata and optional static-catalog selections.

python verify.py --photo-root /path/to/sources
Optional: --manifest /path/to/catalog.torrent --catalog-reader /path/to/inspect_release32.py
No network, peer client, source mutation or visual/physical identification.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re


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
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--catalog-reader', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert hashlib.sha256(report.read_bytes()).hexdigest() == pins['report_sha256']
    result = {'report_hash_matches': True, 'photo_entities_checked': 0,
              'catalog_selection_checked': False,
              'visual_code_namespace_origin_or_custody_verified': False}
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
                assert dates(image) == row['selected_dates']
            result['photo_entities_checked'] += 1
    if args.manifest:
        assert args.catalog_reader is not None
        assert hashlib.sha256(args.manifest.read_bytes()).hexdigest() == pins['catalog']['sha256']
        assert hashlib.sha256(args.catalog_reader.read_bytes()).hexdigest() == pins['catalog_reader']['sha256']
        spec = importlib.util.spec_from_file_location('pinned_catalog_reader', args.catalog_reader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        raw = module.read_bencode(args.manifest.read_bytes())[b'info'][b'files']
        rows = [{'catalog_index': i, 'path': '/'.join(v.decode('utf-8') for v in r[b'path']),
                 'declared_bytes': r[b'length']} for i, r in enumerate(raw)]
        assert len(rows) == pins['catalog']['all_paths']
        folder = pins['folder']['literal']
        folder_rows = [r for r in rows if folder in r['path'].split('/')]
        assert len(folder_rows) == pins['folder']['entry_count']
        for token, expected in pins['token_lookup'].items():
            rx = re.compile(r'(?<![A-Za-z0-9])' + re.escape(token) + r'(?![A-Za-z0-9])', re.I)
            actual = [r for r in rows if rx.search(r['path'])]
            assert actual == expected
        result['catalog_selection_checked'] = True
        result['token_match_counts'] = {k: len(v) for k, v in pins['token_lookup'].items()}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
