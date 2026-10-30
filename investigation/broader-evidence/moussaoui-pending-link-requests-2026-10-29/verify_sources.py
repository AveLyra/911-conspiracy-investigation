#!/usr/bin/env python3
"""Verify supplied PDF entity fingerprints/structure; not historical conclusions."""
import argparse
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('--source', action='append', required=True, metavar='EXHIBIT=PDF')
args = parser.parse_args()
provided = dict(value.split('=', 1) for value in args.source)
root = Path(__file__).resolve().parent
sources = json.loads((root / 'SOURCES.json').read_text())['documents']
assert set(provided) == {x['exhibit'] for x in sources}
checks = []
for record in sources:
    path = Path(provided[record['exhibit']])
    data = path.read_bytes()
    pdf = PdfReader(path)
    assert len(data) == record['bytes']
    assert hashlib.sha256(data).hexdigest() == record['sha256']
    assert len(pdf.pages) == record['pages'] == 1
    if record['exhibit'] in ['636', '637']:
        assert [len(p.extract_text() or '') for p in pdf.pages] == record['extracted_characters_by_page']
        assert list(pdf.attachments.keys()) == record['passively_exposed_attachment_names']
    checks.append({'exhibit': record['exhibit'], 'bytes': len(data), 'sha256': record['sha256'], 'pages': len(pdf.pages), 'integrity_and_structure_match': True})
todos = json.loads((root / 'OPEN-TODOS.json').read_text())['items']
assert [x['id'] for x in todos] == [f'DRAFT-T0{i}' for i in range(1, 7)]
assert all(x['status'].startswith('TODO_INPUT') for x in todos)
report = (root / 'README.md').read_text().splitlines()
for item in json.loads((root / 'OBSERVATIONS.json').read_text())['items']:
    assert report[item['report_line'] - 1].strip()
print(json.dumps({'checks': checks, 'stable_TODO_ids_preserved': True, 'scope': 'Entity fingerprints, supplied page counts, passive new-copy extraction/attachment metadata and ledger structure only; no independent content or historical authentication.'}, indent=2))
