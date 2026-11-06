#!/usr/bin/env python3
"""Recompute the bounded FMCSA date-field audit from saved public responses."""
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import json
import re
import statistics

SAMPLES = Path(__file__).resolve().parent / 'samples'

def read(name):
    return json.loads((SAMPLES / name).read_text())

def date(value):
    return datetime.strptime(value, '%m/%d/%Y')

for year in (2001, 2002, 2010, 2020, 2025):
    rows = read(f'revocation-{year}.json')
    counts, deltas = Counter(), []
    for row in rows:
        try:
            delta = (date(row['order2_effective_date']) - date(row['order1_serve_date'])).days
        except (ValueError, KeyError):
            counts['missing_or_unparsed'] += 1
            continue
        counts['parsed'] += 1
        counts['before' if delta < 0 else 'after' if delta > 0 else 'same'] += 1
        deltas.append(delta)
    triples = {(x.get('docket_number'), x.get('order1_serve_date'), x.get('order2_effective_date')) for x in rows}
    print(year, 'rows', len(rows), 'counts', dict(counts), 'distinct_triples', len(triples), 'median_delta', statistics.median(deltas) if deltas else None)
    if year not in (2001, 2002, 2010):
        continue
    insurance = read(f'insurance-{year}.json')
    dockets = list(dict.fromkeys(x['docket_number'] for x in rows if re.fullmatch(r'(?:MC|FF|MX)[0-9]{6}', x.get('docket_number', ''))))[:100]
    by_docket = defaultdict(set)
    for item in insurance:
        by_docket[item.get('docket_number')].add(item.get('cancl_effective_date'))
    triples = {(x['docket_number'], x.get('order1_serve_date'), x['order2_effective_date']) for x in rows if x.get('docket_number') in dockets and x.get('order2_effective_date')}
    print(year, 'selected_dockets', len(dockets), 'distinct_revocation_triples', len(triples), 'insurance_rows', len(insurance), 'same_docket_date_matches', sum(t[2] in by_docket[t[0]] for t in triples))
