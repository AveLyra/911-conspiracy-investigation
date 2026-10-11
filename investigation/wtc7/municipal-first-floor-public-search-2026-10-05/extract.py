"""Read-only four-query extraction using the inspected existing contract."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'municipal-originals-2026-10-04'
sys.path.insert(0, str(OLD / 'job1854-followup-locator'))
import diagnose_metadata as diagnostic

LABELS = ('control', 'ss1', 'skss2', 's1_first')


def calculate():
    if not __debug__:
        raise RuntimeError('Assertions are required')
    prior = diagnostic.m.prior
    queries, query_pin = prior.read(HERE / 'queries.json')
    assert tuple(queries) == LABELS
    pins, rows, documents, exceptions = [query_pin], [], {}, []
    for label in LABELS:
        request, rp = prior.read(HERE / f'{label}-request.json')
        response, sp = prior.read(HERE / f'{label}-response.json')
        pins.extend((rp, sp))
        row, found, missing = diagnostic.diagnose_query(label, queries[label], request, response)
        rows.append(row)
        exceptions.extend(missing)
        raw_rows = response['resultset'].get('results', [])
        for ordinal, (key, record) in enumerate(found.items(), 1):
            result_id = raw_rows[ordinal-1]['id']
            assert result_id.endswith(':' + key + ':'), (label, key, 'result ID mismatch')
            membership = {'query': label, 'ordinal_one_based': ordinal, 'result_id': result_id}
            if key in documents:
                assert documents[key]['record'] == record, (key, 'cross-query conflict')
                documents[key]['memberships'].append(membership)
            else:
                documents[key] = {'record': record, 'memberships': [membership]}
    dependencies = []
    for rel in ('job1854-followup-locator/diagnose_metadata.py',
                'job1854-followup-locator/check_metadata.py',
                'test-acceptance-locator/check_metadata.py'):
        raw = (OLD / rel).read_bytes()
        dependencies.append({'path': str((OLD / rel).relative_to(HERE.parent)),
                             'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    control = 'NYC-WTC_000166828'
    return {'status': 'complete_supplied_property_sets' if not exceptions else 'explicit_metadata_exceptions',
            'queries': rows, 'documents': documents, 'exceptions': exceptions,
            'unique_count': len(documents), 'query_occurrences': sum(r['returned'] for r in rows),
            'unique_reported_pages': sum(int(d['record']['properties']['page_count']) for d in documents.values()),
            'control_present': control in rows[0]['ids'],
            'control_target_memberships': [r['label'] for r in rows[1:] if control in r['ids']],
            'pins': pins, 'dependencies': dependencies,
            'protocol_sha256': hashlib.sha256((HERE / 'PROTOCOL.md').read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(calculate(), sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False))
