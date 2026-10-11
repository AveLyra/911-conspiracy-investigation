"""Read-only held-metadata lookup. JSON output is a locator, not source content."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'municipal-originals-2026-10-04'
PATTERNS = {
    'sheet': r'(?<![A-Za-z0-9])(?:SKS[\s._–-]*S[\s._–-]*[12]|S[\s._–-]*S[\s._–-]*1|S[\s._–-]*1)(?![A-Za-z0-9])',
    'first_floor': r'(?<![A-Za-z0-9])(?:first|1st)[\s._–-]*(?:floor|fl)(?![A-Za-z0-9])',
    'structural_context': r'(?<![A-Za-z0-9])(?:structural|framing|beams?|notch(?:es|ed|ing)?|penetrations?|drawings?|sketch(?:es)?)(?![A-Za-z0-9])',
}
CONTROL_IDS = ['NYC-WTC_000' + n for n in ('166828', '173199', '173529', '173670')]


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: ' + key)
        out[key] = value
    return out


def read(path):
    raw = path.read_bytes()
    return json.loads(raw, object_pairs_hook=unique), {
        'file': str(path.relative_to(SOURCE)), 'bytes': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest()}


def properties(row):
    out = {}
    for prop in row['properties']:
        key = prop['id']
        if key in out:
            raise ValueError('duplicate property: ' + key)
        data = prop['data']
        if len(data) != 1:
            raise ValueError('multivalue property: ' + key)
        values = data[0]['value']
        kinds = [k for k in ('str', 'num') if k in values]
        if len(kinds) != 1:
            raise ValueError('non-scalar property: ' + key)
        value = values[kinds[0]]
        if kinds[0] == 'str' and type(value) is not str:
            raise ValueError('invalid string: ' + key)
        if kinds[0] == 'num' and type(value) not in (int, float):
            raise ValueError('invalid number: ' + key)
        out[key] = value
    for required in ('mes:key', 'title', 'source', 'box_name'):
        if type(out.get(required)) is not str:
            raise ValueError('missing/invalid required property: ' + required)
    if 'folder_name' in out and type(out['folder_name']) is not str:
        raise ValueError('invalid folder property')
    if not re.fullmatch(r'NYC-WTC_\d{9}', out['mes:key']):
        raise ValueError('invalid document key')
    if out['title'] != out['mes:key'] + '.pdf':
        raise ValueError('title/key mismatch')
    return out


def matches(fields):
    return [{'field': field, 'category': category, 'text': match.group(),
             'span': list(match.span())}
            for field, value in fields.items()
            for category, pattern in PATTERNS.items()
            for match in re.finditer(pattern, value, re.I)]


def selected_fields(props):
    return {field: props[field] for field in ('title', 'folder_name') if field in props}


def disposition(source, hits):
    categories = {hit['category'] for hit in hits}
    if not hits:
        return 'no supplied-field match'
    if source != 'WTC 7':
        return 'off-source'
    if 'sheet' in categories:
        return 'sheet-token lead'
    if {'first_floor', 'structural_context'} <= categories:
        return 'subject lead'
    return 'context lead'


def run():
    protocol = (HERE / 'PROTOCOL.md').read_bytes()
    paths = re.findall(r'^\d+\. `([^`]+\.json)`\.$', protocol.decode(), re.M)
    assert len(paths) == 24 and len(set(paths)) == 24
    catalog, pin = read(SOURCE / paths[0])
    pins, folder_hits, controls = [pin], [], {key: [] for key in CONTROL_IDS}
    assert catalog['columns'] == ['source_index', 'box', 'folder', 'documents', 'pages', 'first_bates']
    assert len(catalog['rows']) == catalog['rows_total']
    source_counts = {}
    for ordinal, row in enumerate(catalog['rows'], 1):
        assert len(row) == 6
        source_index, box, folder, documents, pages, first = row
        assert type(source_index) is int and 0 <= source_index < len(catalog['sources'])
        assert all(type(s) is str for s in (box, folder, first))
        assert all(type(n) is int and n > 0 for n in (documents, pages))
        source = catalog['sources'][source_index]
        source_counts[source] = source_counts.get(source, 0) + 1
        hits = matches({'folder': folder})
        item = {'row_ordinal_one_based': ordinal, 'source': source, 'box': box,
                'folder': folder, 'documents': documents, 'pages': pages,
                'first_bates': first, 'matches': hits, 'disposition': disposition(source, hits)}
        if hits:
            folder_hits.append(item)
        if first in controls:
            controls[first].append({'file': paths[0], **item})
    coverage, docs, appearances, missing, disagreements = [], {}, [], [], []
    for rel in paths[1:]:
        data, pin = read(SOURCE / rel)
        pins.append(pin)
        resultset = data['resultset']
        results = resultset.get('results', [])
        assert isinstance(results, list)
        ids = []
        for ordinal, row in enumerate(results, 1):
            props = properties(row)
            key = props['mes:key']
            assert key not in ids, (rel, key, 'duplicate result')
            assert row['id'].endswith(':' + key + ':'), (rel, key, 'result ID')
            ids.append(key)
            fields = selected_fields(props)
            hits = matches(fields)
            ref = {'file': rel, 'result_ordinal_one_based': ordinal}
            appearance = {**ref, 'result_id': row['id'], 'properties': props,
                          'missing_search_fields': [f for f in ('title', 'folder_name') if f not in props],
                          'matches': hits, 'disposition': disposition(props['source'], hits)}
            if hits:
                appearances.append(appearance)
            if 'folder_name' not in props:
                missing.append({**ref, 'key': key, 'field': 'folder_name'})
            if key in controls:
                controls[key].append(appearance)
            if key in docs:
                old = docs[key]['properties']
                if old != props:
                    disagreements.append({**ref, 'key': key, 'earlier': old, 'current': props})
                docs[key]['appearances'].append(ref)
            else:
                docs[key] = {'properties': props, 'appearances': [ref],
                             'matches': hits, 'disposition': disposition(props['source'], hits)}
        coverage.append({'file': rel, 'query': data['search_request']['user']['query']['unparsed'],
                         'requested_count': data['search_request']['count'],
                         'returned': len(results), 'estimated_count': data['estimated_count'],
                         'results_key_present': 'results' in resultset,
                         'next_avail': resultset['next_avail'], 'prev_avail': resultset['prev_avail'],
                         'termination_causes': [s['termination_cause'] for s in resultset['per_service_dataset']],
                         'ids': ids})
    return {'protocol_sha256': hashlib.sha256(protocol).hexdigest(),
            'patterns': PATTERNS, 'pins': pins,
            'catalog': {'captured_at': catalog['captured_at'], 'rows': len(catalog['rows']),
                        'source_row_counts': source_counts, 'matching_rows': folder_hits},
            'coverage': coverage, 'documents': docs, 'matching_appearances': appearances,
            'missing_fields': missing, 'disagreements': disagreements,
            'known_controls': controls,
            'counts': {'query_occurrences': sum(x['returned'] for x in coverage),
                       'unique_document_ids': len(docs), 'matching_appearances': len(appearances),
                       'matching_document_ids': sum(bool(d['matches']) for d in docs.values()),
                       'matching_folder_rows': len(folder_hits), 'missing_folder_appearances': len(missing)}}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
