"""Check the NTAP extraction through separate token counting and exact byte spans."""
import argparse
import hashlib
import json
from pathlib import Path

cli = argparse.ArgumentParser(description=__doc__)
cli.add_argument('input', type=Path)
cli.add_argument('result', type=Path)
cli.add_argument('--output', required=True, type=Path)
a = cli.parse_args()
b = a.input.read_bytes()
r = json.loads(a.result.read_text())
assert hashlib.sha256(b).hexdigest() == r['source_sha256']
lines = b.decode('latin1').splitlines()
second = []
for number in range(r['block_start_line'] + 3, r['block_end_line_exclusive']):
    tokens = lines[number-1].split()
    for i, token in enumerate(tokens):
        if token in ['3743', '6553'] and i+3 < len(tokens):
            alt, hhmm, ss = tokens[i+1:i+4]
            if len(alt)==3 and len(hhmm)==4 and len(ss)==2 and all(x.isdigit() for x in [alt,hhmm,ss]):
                second.append((number, token, alt, hhmm+':'+ss))
first = [(x['source_line'], x['code'], x['alt_raw'], x['printed_time']) for x in r['rows']]
assert second == first
for x in r['rows']:
    i = x['byte_offset_zero_based']
    span = x['matched_source_text'].encode('latin1')
    assert b[i:i+len(span)] == span
checks = {
    'source_sha256': hashlib.sha256(b).hexdigest(),
    'independent_space_token_counter_entries': len(second),
    'regex_and_token_tuples_identical': second == first,
    'all94_matched_byte_spans_preserved': True,
    'manual_controls': r['manual_row_controls'],
    'source_unchanged': True,
    'scope': 'Source/representation reproducibility only. Does not authenticate clock time, source radar or aircraft identity.'
}
with a.output.open('x') as stream:
    json.dump(checks, stream, indent=2)
    stream.write('\n')
print('Token and byte-span checks matched', len(second), 'entries; no historical clock validation.')
