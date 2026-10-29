"""Check downloaded report identity and selected arithmetic, not historical truth.

Usage with the two preserved source PDFs:
    python3 verify_records.py --source-2006 PATH --source-2007 PATH
Requires pypdf only when source files are supplied. Notes-only operation uses
the standard library. No network, source mutation or automatic text repair.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--source-2006', type=Path)
parser.add_argument('--source-2007', type=Path)
args = parser.parse_args()
sources = json.loads((root / 'SOURCES.json').read_text())['documents']
observation = next(x for x in json.loads((root / 'OBSERVATIONS.json').read_text()) if x['id'] == 'SAR05')
assert sum(observation['table_agency_case_counts']) == observation['table_total_visible']
assert observation['table_total_visible'] == 472
assert observation['prose_pending_caseload'] == 473
verified = []
for source in sources:
    path = getattr(args, 'source_' + source['year'])
    if path is None:
        continue
    from pypdf import PdfReader
    body = path.read_bytes()
    assert body.startswith(b'%PDF-')
    assert len(body) == source['bytes']
    assert hashlib.sha256(body).hexdigest() == source['sha256']
    assert base64.b32encode(hashlib.sha1(body).digest()).decode().rstrip('=') == source['cdx_digest']
    assert len(PdfReader(path).pages) == source['physical_pages']
    verified.append(source['id'])
print(json.dumps({'source_identities_checked': verified,
                  'table_sum': sum(observation['table_agency_case_counts']),
                  'printed_table_total': observation['table_total_visible'],
                  'prose_value_preserved': observation['prose_pending_caseload'],
                  'scope': 'Entity identity/page count and selected arithmetic only; manual page readings and historical outcomes are not independently authenticated.'}, indent=2))
