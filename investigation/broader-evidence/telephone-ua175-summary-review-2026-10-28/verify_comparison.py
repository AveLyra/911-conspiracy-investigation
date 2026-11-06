"""Check safe supplied readings and, optionally, preserved source entities.

This does not authenticate calls, source glyphs, field definitions or custody.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def selected_field_matches(rows, report, column):
    matches = []
    for time, duration in zip(report['starts'], report['durations_seconds']):
        candidates = [r for r in rows if r['time_label'] == time]
        matches.append(len(candidates) == 1 and candidates[0][column] == duration)
    return matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--new-images', type=Path)
    parser.add_argument('--old-reader26', type=Path)
    parser.add_argument('--t01', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = json.loads((args.directory / 'ROW-FIELDS.json').read_text())['rows']
    inputs = json.loads((args.directory / 'COMPARISON-INPUTS.json').read_text())
    report = inputs['staff_note166']
    checks = []

    def check(name, result, kind):
        checks.append({'check': name, 'passed': bool(result), 'kind': kind})

    check('eleven consecutive row positions', [r['row'] for r in rows] == list(range(1, 12)), 'transcription accounting')
    positive = [r for r in rows if r['connect_candidates'] and all(v > 0 for v in r['connect_candidates'])]
    check('eleven positive Connect readings/candidates', len(positive) == 11, 'supplied-input calculation')
    check('eleven zero Operator readings', sum(r['operator'] == 0 for r in rows) == 11, 'supplied-input calculation')
    check('row6 exact Connect remains unaccepted', rows[5]['connect'] is None and rows[5]['connect_candidates'] == [207, 267], 'uncertainty preservation')
    scp = selected_field_matches(rows, report, 'scp')
    connect = selected_field_matches(rows, report, 'connect')
    check('both note166 numbers match selected SCP numbers', scp == [True, True], 'field comparison')
    check('neither note166 number matches selected Connect number', connect == [False, False], 'contrary field comparison')
    altered = copy.deepcopy(rows)
    altered[1]['scp'] = altered[1]['connect']
    check('altered field does not preserve both matches', selected_field_matches(altered, report, 'scp') != [True, True], 'negative control')
    check('three distinct email start labels and last-negative report', len(set(inputs['email']['ua175_start_labels'])) == 3 and inputs['email']['reported_last_connection'] is False, 'reported-source accounting')
    check('no authenticated network/clock join claimed', inputs['joins']['clock_alignment_authenticated'] is False and inputs['joins']['network_key_join_authenticated'] is False, 'scope gate')

    source_checks = []
    pins = json.loads((args.directory / 'SOURCE-PINS.json').read_text())
    for pin in pins:
        path = None
        if 'asset_base_url' in pin and args.new_images is not None:
            path = args.new_images / ('reader-%s.webp' % pin['reader_page'])
        elif pin.get('reader_page') == 26 and args.old_reader26 is not None:
            path = args.old_reader26
        elif pin.get('id') == 'T01' and args.t01 is not None:
            path = args.t01
        if path is not None:
            expected = pin.get('sha256', pin.get('sha256_captured_entity'))
            ok = path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == expected
            source_checks.append({'source': pin.get('asset_base_url', pin.get('public_asset_url', pin.get('url'))), 'passed': ok})
    check('provided original entities match pins', all(x['passed'] for x in source_checks), 'byte integrity only')
    result = {
        'scope': 'Safe supplied-field calculations, uncertainty and source-entity checks; not source-reading accuracy, native semantics, caller identity, historical authenticity or completion of TEL01–TEL04.',
        'checks': checks,
        'source_checks': source_checks,
        'passed': sum(x['passed'] for x in checks),
        'failed': sum(not x['passed'] for x in checks),
        'computed': {'row_positions': len(rows), 'positive_connect_readings_or_candidates': len(positive),
                     'exact_connect_readings': sum(r['connect'] is not None for r in rows),
                     'uncertain_connect_rows': [r['row'] for r in rows if r['connect'] is None],
                     'zero_operator_readings': sum(r['operator'] == 0 for r in rows),
                     'selected_scp_matches': sum(scp), 'selected_connect_matches': sum(connect),
                     'reported_letter_attempts': len(inputs['letter']['reported_attempts']),
                     'reported_ual_conversations': inputs['letter']['ual_best_determination_conversations'],
                     'reported_note166_completed_calls': report['reported_completed_calls'],
                     'source_entities_checked': len(source_checks)},
        'native_units_established': False, 'actual_conversation_count_established': False,
        'inference_limit': 'A naive positive-Connect-means-completed-conversation rule would conflict with the reported negative third attempt; it is not applied. Neither account is thereby authenticated or preferred.'}
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps({'passed': result['passed'], 'failed': result['failed'], 'computed': result['computed']}, indent=2))
    if result['failed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
