"""Compare separately transcribed visible UA93 rows; never emit full keys.

Usage: python3 compare_tables.py LOCAL_TRANSCRIPTIONS LOCAL_PINS NEW_RESULT
Pins must reference locally held source images using verified_path. The input
contains private-to-this-analysis identifiers and is deliberately unpublished.
Readers can independently transcribe the linked source images and rerun.
This tests accounting of supplied readings, not their historical truth.
"""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json
import sys

inputs, pins_file, output = map(Path, sys.argv[1:])
data = json.loads(inputs.read_text())
pins = json.loads(pins_file.read_text())
checks = []


def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)


check('Three input image pins present', sorted(p['reader_page'] for p in pins) == [25, 27, 28])
for pin in pins:
    body = Path(pin['verified_path']).read_bytes()
    check('Unchanged source entity ' + str(pin['reader_page']),
          len(body) == pin['bytes'] and hashlib.sha256(body).hexdigest() == pin['sha256'])
s, c = data['summary'], data['carrier']
for label, rows in [('summary', s), ('carrier', c)]:
    check(label + ' accounts for all 35 source row positions',
          [r['row'] for r in rows] == list(range(1, 36)))
    check(label + ' retains unknown key fields',
          all(r['full_key'] is None or r['full_key'].isdigit() for r in rows)
          and all(r['key_uncertainty'] for r in rows if r['full_key'] is None))


def duplicates(values):
    return [n for n in Counter(values).values() if n > 1]


sk = [r['full_key'] for r in s if r['full_key'] is not None]
ck = [r['full_key'] for r in c if r['full_key'] is not None]
check('Accepted full-key subsets have no duplicate supplied key',
      not duplicates(sk) and not duplicates(ck))
check('Accepted full-key subsets match without source-order matching', set(sk) == set(ck))
carrier_index = {r['full_key']: r for r in c if r['full_key'] is not None}
pairs = []
for row in s:
    if row['full_key'] is not None:
        other = carrier_index[row['full_key']]
        join = 'matching supplied full printed key'
    else:
        possible = [r for r in c if r['full_key'] is None
                    and (r['time_label'], r['connect']) == (row['time_label'], row['connect'])]
        check('Uncertain-key row has exactly one limited candidate', len(possible) == 1)
        other = possible[0]
        join = 'candidate time/connect association; full key NOT accepted'
    pairs.append((row, other, join))
check('Candidate map covers each carrier row once', sorted(b['row'] for a, b, j in pairs) == list(range(1, 36)))
check('Reversed source order does not change full-key associations',
      all(next(r for r in reversed(c) if r['full_key'] == a['full_key'])['row'] == b['row']
          for a, b, j in pairs if a['full_key'] is not None))
check('Altered-key negative control cannot join',
      sk[0] + '_CONTROL' not in carrier_index)
time_collisions = {name: len(duplicates([r['time_label'] for r in rows]))
                   for name, rows in [('summary', s), ('carrier', c)]}
check('Time-only matching demonstrably ambiguous', all(n > 0 for n in time_collisions.values()))
check('All paired printed time strings agree', all(a['time_label'] == b['time_label'] for a, b, j in pairs))
check('All paired supplied Connect fields agree', all(a['connect'] == b['connect'] for a, b, j in pairs))


def compatible(a, b):
    return len(a) == len(b) and all(x == y or x == '?' or y == '?' for x, y in zip(a, b))


safe = []
for a, b, join in pairs:
    safe.append({'summary_row': a['row'], 'carrier_row': b['row'], 'association': join,
                 'time_label': a['time_label'], 'summary_zone': a['time_zone'], 'carrier_zone': None,
                 'connect_summary': a['connect'], 'connect_carrier': b['connect'],
                 'operator_summary': a['operator_reading'], 'operator_carrier': b['operator_reading'],
                 'operator_readings_compatible': compatible(a['operator_reading'], b['operator_reading']),
                 'scp_summary': a['scp'], 'scp_carrier': b['scp'],
                 'scp_comparison': 'unaccepted/blank; not zero' if a['scp'] is None or b['scp'] is None
                 else ('same supplied number' if a['scp'] == b['scp'] else 'different supplied numbers')})
counts = {'source_rows_per_representation': 35,
          'full_key_pairs': sum(a['full_key'] is not None for a, b, j in pairs),
          'uncertain_key_candidate_pairs': sum(a['full_key'] is None for a, b, j in pairs),
          'time_only_duplicate_groups': time_collisions,
          'matching_connect_pairs': sum(a['connect'] == b['connect'] for a, b, j in pairs),
          'positive_connect_fields_per_representation': {name: sum(r['connect'] > 0 for r in rows)
                                                        for name, rows in [('summary', s), ('carrier', c)]},
          'operator_zero_fields_per_representation': {name: sum(r['operator_reading'] == '0' for r in rows)
                                                     for name, rows in [('summary', s), ('carrier', c)]},
          'operator_incompatible_reading_pairs': sum(not r['operator_readings_compatible'] for r in safe),
          'scp_both_numeric_pairs': sum(r['scp_summary'] is not None and r['scp_carrier'] is not None for r in safe),
          'scp_equal_numeric_pairs': sum(r['scp_comparison'] == 'same supplied number' for r in safe),
          'scp_different_numeric_pairs': sum(r['scp_comparison'] == 'different supplied numbers' for r in safe),
          'scp_not_numerically_compared_pairs': sum(r['scp_comparison'].startswith('unaccepted') for r in safe)}
result = {'performed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'input_sha256': hashlib.sha256(inputs.read_bytes()).hexdigest(),
          'counts': counts, 'pairs': safe, 'checks': checks, 'passed': len(checks),
          'scope': 'Supplied manual readings, source-byte pins and candidate row accounting only; same analyst, not independent blinded replication.',
          'not_established': ['Native carrier/release authentication', 'Global uniqueness of Acis keys',
                              'Unique calls, people, completed conversations or duration units',
                              'Clock calibration or timezone alignment', 'Historical cause of differing fields',
                              'AA77 operator/office/caller mapping', 'Any of five full goal gates']}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
print(json.dumps({'passed': len(checks), 'counts': counts}, indent=2))
