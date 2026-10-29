"""Recalculate the held attachment's row accounting; no source-authentication claim."""
import collections
import json
from pathlib import Path

root = Path(__file__).resolve().parent
rows = json.loads((root / 'IDENTIFIER-ROWS.json').read_text())
saved = json.loads((root / 'COUNT-RESULTS.json').read_text())
assert [r['ledger_row'] for r in rows] == list(range(1, len(rows) + 1))
by_page = collections.defaultdict(list)
for row in rows:
    assert row['printed_exhibit_page'] == row['physical_pdf_page'] - 68
    by_page[row['physical_pdf_page']].append(row)
assert sorted(by_page) == list(range(69, 78))
for page, page_rows in by_page.items():
    assert [r['identifier_row_on_page'] for r in page_rows] == list(range(1, len(page_rows) + 1))
labels = [r['identifier_verbatim'] for r in rows]
frequencies = collections.Counter(labels)
actual = {
    'identifier_rows': len(rows),
    'distinct_identifier_strings': len(frequencies),
    'by_physical_page': {str(p): len(a) for p, a in by_page.items()},
    'by_prefix': dict(sorted(collections.Counter(s.split('-')[0] for s in labels).items())),
    'repeated_identifiers': {
        label: [{k: r[k] for k in ['physical_pdf_page', 'printed_exhibit_page', 'identifier_row_on_page', 'ledger_row']} for r in rows if r['identifier_verbatim'] == label]
        for label, count in sorted(frequencies.items()) if count > 1
    },
}
for key, value in actual.items():
    assert saved[key] == value, key
descriptors = json.loads((root / 'SELECTED-DESCRIPTORS.json').read_text())
for descriptor in descriptors:
    row = rows[descriptor['ledger_row'] - 1]
    assert all(descriptor[k] == v for k, v in row.items())
print(json.dumps({'recalculated': actual, 'selected_descriptor_locators_valid': len(descriptors),
                  'scope': 'Accounting/locator consistency only; not independent visual reading, physical-object counting, custody, origin or historical authentication.'}, indent=2))
