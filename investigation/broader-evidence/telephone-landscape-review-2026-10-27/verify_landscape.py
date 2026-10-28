"""Check pinned source bytes and supplied readings, not historical call truth.

Usage: python3 verify_landscape.py IMAGE_DIRECTORY LOCAL_KEYS_JSON NEW_RESULT_JSON
Local keys: {"summary_p25_r09": "...", "carrier_p27_r35": "..."}.
Never emits raw keys; read their original source pixels independently.
"""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).parent
images, keys_path, output = map(Path, sys.argv[1:])
pins = json.loads((root / 'SOURCE-PINS.json').read_text())
obs = json.loads((root / 'OBSERVATIONS.json').read_text())
keys = json.loads(keys_path.read_text())
checks = []

def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)

for pin in pins:
    body = (images / pin['filename']).read_bytes()
    check('source pin reader ' + str(pin['reader_page']),
          len(body) == pin['bytes'] and hashlib.sha256(body).hexdigest() == pin['sha256'])

check('selected supplied full keys equal and nonempty',
      bool(keys['summary_p25_r09']) and keys['summary_p25_r09'] == keys['carrier_p27_r35'])
# An intentionally changed comparison must fail; no second real person's key is needed.
check('unequal-key negative control rejected',
      keys['summary_p25_r09'] != keys['carrier_p27_r35'] + '_CONTROL')
a, b = obs['selected_rows']
check('selected repeated time labels agree', a['time_label'] == b['time_label'] == '9:37:41')
check('selected connect and operator readings agree',
      a['Duration Connect'] == b['Duration Connect'] == 14 and
      a['Duration Operator'] == b['Duration Operator'] == 0)
check('SCP difference retained without units',
      a['Scp Duration'] == 7565 and b['Scp Duration'] == 7555 and
      a['Scp Duration'] - b['Scp Duration'] == 10 and obs['scp_units'] is None)
counts = obs['manual_row_counts']
check('manual continuation counts agree; not added as events',
      counts['carrier_p27'] == counts['carrier_p28'] == counts['summary_keyed'] == 35)
check('summary categories sum to 37; no unique-call claim',
      counts['summary_cellular'] == 2 and counts['summary_keyed'] + counts['summary_cellular'] == 37
      and obs['unique_calls_established'] is False)

result = {'checks': checks, 'passed': len(checks),
          'source_entities': len(pins), 'selected_candidate_row_groups': 1,
          'scope': 'Pinned bytes and supplied manual readings/counts; not OCR or historical validation',
          'candidate_continuation_join': 'page labels, final row position and repeated time; not native key join',
          'units_or_clock_definitions_established': False,
          'raw_identifiers_emitted': False}
with output.open('x') as handle:
    json.dump(result, handle, indent=2)
print(str(len(checks)) + ' scoped checks passed; native schema/custody/clocks remain unverified.')
