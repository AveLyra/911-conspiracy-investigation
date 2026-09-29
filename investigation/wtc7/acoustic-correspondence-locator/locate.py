"""Read-only, bounded held-record locator; output contains no document bodies."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

import fitz

MAIN = Path('/Users/admin/docs/911')
HERE = Path(__file__).resolve().parent
TREES = ('exhibits/raw', 'exhibits/processed', 'authority/nist')
TEXT = {'.txt', '.md', '.csv', '.json', '.eml', '.html', '.htm', '.xml'}
QUERIES = {
    'organization_ara': r'applied\s+research\s+associat',
    'organization_loizeaux': r'loizeau[xs]?',
    'date_ara': r'(?:31[ ,/-]+Jul[a-z]*[ ,/-]+2008|Jul[a-z]*[ ,/-]+31[ ,/-]+2008|2008[-/]0?7[-/]31|0?7[-/]31[-/]2008)',
    'date_loizeaux': r'(?:0?5[ ,/-]+Aug[a-z]*[ ,/-]+2008|Aug[a-z]*[ ,/-]+0?5[ ,/-]+2008|2008[-/]0?8[-/]0?5|0?8[-/]0?5[-/]2008)',
    'acoustic': r'acoustic|\bnlaws\b|sound\s+propagation|sound\s+pressure|audib',
}


def hits(s):
    s = ' '.join(s.split())
    return [k for k, v in QUERIES.items() if re.search(v, s, re.I)]


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def main():
    destination = HERE/'locator01.json'
    if destination.exists():
        raise FileExistsError('Refusing existing locator record')
    assert hits('Applied\nResearch Associates') == ['organization_ara']
    assert hits('Loizeaux Group International') == ['organization_loizeaux']
    for s in ('31 July 2008', 'July 31, 2008', '2008-07-31', '07/31/2008'):
        assert hits(s) == ['date_ara']
    for s in ('5 August 2008', 'August 05, 2008', '2008-08-05', '08/05/2008'):
        assert hits(s) == ['date_loizeaux']
    assert hits('ordinary unrelated fixture') == []
    command = ['rg', '--files', '--hidden', '--no-ignore', *TREES]
    inventory = subprocess.run(command, cwd=MAIN, capture_output=True, check=True)
    names = sorted(inventory.stdout.decode().splitlines())
    rows = []
    for name in names:
        p = MAIN/name
        row = {'path': name, 'bytes': p.stat().st_size, 'filename_hits': hits(name)}
        if p.is_symlink():
            row['mode'] = 'symlink_not_followed'
            rows.append(row)
            continue
        suffix = p.suffix.lower()
        if suffix in TEXT or suffix == '.zip' or (suffix == '.pdf' and name.startswith('exhibits/')):
            row['sha256_before'] = digest(p)
            try:
                if suffix in TEXT:
                    b = p.read_bytes()
                    s = b.decode('utf-8', errors='replace')
                    row.update(mode='raw_text', hits=hits(s), replacement_characters=s.count('\ufffd'))
                elif suffix == '.zip':
                    with zipfile.ZipFile(p) as z:
                        members = z.infolist()
                        row.update(mode='zip_names_only', members=len(members),
                                   member_hits=[{'name': x.filename, 'hits': hits(x.filename)}
                                                for x in members if hits(x.filename)],
                                   member_extensions=dict(sorted(Counter(Path(x.filename).suffix.lower() for x in members if not x.is_dir()).items())))
                else:
                    fitz.TOOLS.mupdf_warnings(reset=True)
                    with fitz.open(p) as doc:
                        row.update(mode='pdf_text_locator_only', pages=len(doc), page_hits=[], sparse_text_pages=[])
                        for number, page in enumerate(doc, 1):
                            s = page.get_text()
                            if len(s.strip()) < 20:
                                row['sparse_text_pages'].append(number)
                            found = hits(s)
                            if found:
                                row['page_hits'].append({'physical_page': number, 'hits': found})
                    row['mupdf_warnings'] = fitz.TOOLS.mupdf_warnings(reset=True)
            except Exception as e:
                row.update(error_type=type(e).__name__, status='incomplete')
                # Do not copy an exception's potentially private document text.
                row['mupdf_warnings'] = fitz.TOOLS.mupdf_warnings(reset=True)
            row['sha256_after'] = digest(p)
            if row['sha256_before'] != row['sha256_after']:
                row['status'] = 'source_changed_during_read'
        else:
            row['mode'] = 'filename_only'
        rows.append(row)
    result = {'scope': TREES, 'inventory_command': command,
              'inventory_stderr': inventory.stderr.decode(), 'queries': QUERIES,
              'python': sys.version, 'pymupdf': fitz.VersionBind,
              'script_sha256': digest(Path(__file__)), 'protocol_sha256': digest(HERE/'PROTOCOL.md'),
              'rows': rows}
    with destination.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({'files': len(rows), 'modes': dict(Counter(x['mode'] for x in rows)),
                      'incomplete': sum('status' in x for x in rows),
                      'pdf_pages': sum(x.get('pages', 0) for x in rows),
                      'pdf_sparse_pages': sum(len(x.get('sparse_text_pages', [])) for x in rows),
                      'query_hit_files': sum(bool(x.get('hits') or x.get('page_hits') or x.get('member_hits') or x['filename_hits']) for x in rows)}, indent=2))


if __name__ == '__main__':
    main()
