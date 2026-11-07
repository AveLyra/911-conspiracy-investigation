"""Verify the published catalog locators; no historical authenticity claim.

Run with Python and pypdf 6.10.0:
  python verify.py --pdf /path/to/ms0165.pdf
Optionally pass --sources-dir for the four preserved response entities.
No download, source modification, physical attribution or causal test occurs.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pdf', type=Path)
    ap.add_argument('--sources-dir', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    pins = json.loads((root / 'SOURCE-PINS.json').read_text())
    report = root / ('README.md' if (root / 'README.md').exists() else 'REPORT.md')
    assert sha(report) == pins['report_sha256'], 'Report differs from reviewed text'
    assert all(x is False for x in pins['reading_limits'].values())
    result = {'report_hash_matches': True, 'historical_authentication': False,
              'underlying_files_or_physical_specimens_tested': False,
              'source_hashes_checked': 0, 'catalog_rows_checked': 0,
              'field_anchors_checked': 0}
    if args.sources_dir:
        for row in pins['sources']:
            p = args.sources_dir / Path(row['file']).name
            assert p.stat().st_size == row['size'], row['name']
            assert sha(p) == row['sha256'], row['name']
            result['source_hashes_checked'] += 1
    if args.pdf:
        import pypdf
        assert pypdf.__version__ == pins['pypdf_version'], 'Use the documented extraction version'
        source = next(x for x in pins['sources'] if x['name'] == 'fisher-ms0165')
        assert args.pdf.stat().st_size == source['size']
        assert sha(args.pdf) == source['sha256']
        reader = pypdf.PdfReader(args.pdf)
        assert len(reader.pages) == pins['pdf_pages']
        pages = {}
        wanted = {x['page'] for x in pins['catalog_rows'] + pins['field_anchors']}
        for page in wanted:
            pages[page] = reader.pages[page - 1].extract_text(extraction_mode='layout').splitlines()
        for row in pins['catalog_rows']:
            text = '\n'.join(pages[row['page']][row['start_line'] - 1:row['end_line']])
            pattern = (r'box\s+' + str(row['box']) + r'\s+folder\s+' +
                       re.escape(row['folder']) + r'\s+item\s+' +
                       re.escape(row['item']) + r'(?:\s|$)')
            assert re.search(pattern, text), (row, 'catalog instance mismatch')
            result['catalog_rows_checked'] += 1
        for row in pins['field_anchors']:
            text = ' '.join(pages[row['page']][row['start_line'] - 1:row['end_line']]).casefold()
            text = ' '.join(text.split())
            assert row['fragment'].casefold() in text, (row, 'field mismatch')
            result['field_anchors_checked'] += 1
        result['pdf_size_hash_and_page_count_match'] = True
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
