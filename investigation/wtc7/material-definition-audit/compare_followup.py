#!/usr/bin/env python3
"""Compare frozen five-field receipts only; never reads native source."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    'FOLLOWUP-PROTOCOL.md': '5cced3d7159405e035c2c4c0c0eca4995b2052371992977735c618a90ae54fd5',
    'followup-targets.json': 'e29a710e92720686d6be306c45fa5d9562f3f5dc47b1d585638d8f74b1324dae',
    'element-allowlist.json': '423426c4f3579e241eddff94f603556debc3380edf95f5812b41b425ac122b9d',
    'followup.py': 'bc881f3f23ee4c988df4fda1dba8bdf8399fadc6f739a86311d6257c5cae8408',
    'independent_followup.py': 'a9443bed6460d4de33c4caf5e97d611648891800aad21fb197f738d02418596e',
}
SOURCE_SHA = 'e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64'
MANIFEST_SHA = '30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf'
DENSITY_CLASSES = {'blank', 'over_cap', 'quote_bearing', 'numeric_literal', 'identifier',
                   'identifier_arithmetic', 'numeric_arithmetic', 'unsupported'}


def require(test):
    if not test:
        raise ValueError('comparison_failed')


def validate_rows(rows, targets, names):
    require(type(rows) is list and len(rows) == 5)
    for row, target in zip(rows, targets):
        require(all(row.get(key) == value for key, value in target.items()))
        extra = {'classification'}
        if target['command'] == 'ET':
            require(row['classification'] in {'official_name_match', 'unresolved'})
            if row['classification'] == 'official_name_match':
                extra.add('name')
                require(row.get('name') in names)
        else:
            require(row['classification'] in DENSITY_CLASSES)
        require(set(row) == set(target) | extra)


def compare_rows(left, right, targets, names):
    validate_rows(left, targets, names)
    validate_rows(right, targets, names)
    require(left == right)


def main():
    for name, pin in PINS.items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == pin)
    targets = json.loads((HERE / 'followup-targets.json').read_text())
    names = set(json.loads((HERE / 'element-allowlist.json').read_text())['names'])
    payloads = [(HERE / name).read_bytes() for name in (
        'followup-producer-run01.json', 'followup-producer-run02.json',
        'followup-independent-run01.json', 'followup-independent-run02.json')]
    require(payloads[0] == payloads[1] and payloads[2] == payloads[3])
    producer, independent = json.loads(payloads[0]), json.loads(payloads[2])
    require(producer['status'] == 'PASS' and independent['status'] == 'ok')
    require(producer['schema'] == 'five-field-followup-v1')
    require(independent['scope'] == 'five_field_lexical_only' and independent['pins_rechecked'] is True)
    for item in (producer, independent):
        require(item['source_sha256'] == SOURCE_SHA and item['manifest_sha256'] == MANIFEST_SHA)
        require(item['source_alias'] == 'APDL01' and item['source_bytes'] == 212384)
    for name in ('FOLLOWUP-PROTOCOL.md', 'followup-targets.json', 'element-allowlist.json', 'followup.py'):
        require(producer['pins'][name] == PINS[name])
    for field, name in (('protocol_sha256', 'FOLLOWUP-PROTOCOL.md'), ('targets_sha256', 'followup-targets.json'),
                        ('allowlist_sha256', 'element-allowlist.json'), ('code_sha256', 'independent_followup.py')):
        require(independent[field] == PINS[name])
    compare_rows(producer['rows'], independent['rows'], targets, names)
    perturbations = []
    for index in range(5):
        changed = deepcopy(independent['rows'])
        changed[index]['field_sha256'] = '0' * 64
        perturbations.append(changed)
    for key, value in (('classification', 'unsupported'), ('name', 'PRIVATE_SENTINEL'), ('extra', 'PRIVATE_SENTINEL')):
        changed = deepcopy(independent['rows'])
        changed[0][key] = value
        perturbations.append(changed)
    perturbations.extend([independent['rows'][:-1], list(reversed(independent['rows']))])
    for changed in perturbations:
        try:
            compare_rows(producer['rows'], changed, targets, names)
        except (ValueError, KeyError):
            continue
        raise ValueError('perturbation_not_detected')
    print(json.dumps({'status': 'PASS', 'rows': 5, 'matching_repeated_pairs': 2,
                      'perturbations_detected': len(perturbations),
                      'producer_receipt_sha256': hashlib.sha256(payloads[0]).hexdigest(),
                      'independent_receipt_sha256': hashlib.sha256(payloads[2]).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('{"status":"FAIL","code":"comparison_failed"}')
        raise SystemExit(1)
