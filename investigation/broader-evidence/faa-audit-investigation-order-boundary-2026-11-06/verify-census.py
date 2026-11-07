"""Read pinned local copies and test the public status-snapshot crosswalk."""
from collections import Counter
import hashlib
import json
from pathlib import Path

import fitz
import pypdf

D = Path(__file__).resolve().parent
pins = json.loads((D / 'SOURCE-PINS.json').read_text())
docs = {}
for record in pins['sources']:
    if record['http_status'] != 200:
        continue
    body = (D / 'sources' / record['local_body']).read_bytes()
    assert len(body) == record['bytes']
    assert hashlib.sha256(body).hexdigest() == record['sha256']
    if 'pages' in record:
        docs[record['id']] = fitz.open(stream=body)
        assert len(docs[record['id']]) == record['pages']
        assert len(pypdf.PdfReader(D / 'sources' / record['local_body']).pages) == record['pages']

rows = []
counts = Counter()
by_page = []
letter = docs['letter-2016']
for p in list(letter)[3:]:
    numbers = []
    statuses = []
    for x, y, _, _, word, *_ in p.get_text('words'):
        if 65 < x < 84 and 128 < y < 750 and word.isascii() and word.isdecimal():
            numbers.append((int(word), y))
        if 880 < x < 960 and 128 < y < 750 and word in ('Resolved', 'Unresolved'):
            statuses.append((word, y))
    assert len(numbers) == len(statuses), p.number + 1
    assert all(abs(number_y - status_y) < 1.0 for (_, number_y), (_, status_y) in zip(numbers, statuses))
    rows.extend(num for num, _ in numbers)
    counts.update(status for status, _ in statuses)
    by_page.append({'physical_page': p.number + 1, 'rows': len(numbers)})
assert rows == list(range(1, 515))
assert counts == {'Resolved': 491, 'Unresolved': 23}

anchors = [
    ('letter-2016', 1, 43, 'Open recommendations include'),
    ('letter-2016', 2, 5, '540 open recommendations'),
    ('letter-2016', 2, 6, 'July 18, 2007'),
    ('letter-2016', 2, 15, 'not our practice'),
    ('letter-2016', 3, 7, 'closed, non-public'),
    ('letter-2016', 4, 1, 'Non-Sensitive Open Recommendations'),
    ('letter-2016', 49, 50, '498'),
    ('letter-2016', 49, 51, 'FI2016066'),
    ('letter-2016', 49, 60, 'Resolved'),
    ('letter-2016', 50, 100, '514'),
    ('audit-2016', 10, 27, 'open and unresolved'),
    ('audit-2016', 10, 31, 'Order 8000.6B'),
    ('audit-2016', 15, 42, 'detailed response within 30 days'),
    ('audit-2017', 11, 69, 'FI-2016-066'),
    ('audit-2017', 11, 74, 'Closed'),
    ('audit-2017', 11, 79, 'Closed'),
    ('audit-1997', 59, 14, 'DOT Order 8000.4'),
]
for name, p, n, marker in anchors:
    assert marker in docs[name][p - 1].get_text().splitlines()[n - 1]
web = (D / 'sources' / 'oig-fi2016066-item.body').read_text()
for day, num in [('03.23.2017', 1), ('09.26.2016', 2)]:
    blocks = web.split('<div class="recommendation closed">')[1:]
    matches = [block for block in blocks if f'>{day}</time>' in block]
    assert len(matches) == 1 and f'>No. {num} to OST<' in matches[0]
print(json.dumps({'PyMuPDF':fitz.VersionBind,'pypdf':pypdf.__version__,'numbered_rows':len(rows),
                  'status_counts':counts,'aggregate_reported':540,'difference':540-len(rows),
                  'pdf_anchors':len(anchors),'html_closure_pairs':2,'pages':by_page},indent=2))
