"""Reproduce static court-text and early minute-label comparisons.

python3 verify_comparison.py --court-zip /path/to/court-flights.zip
Uses only the published courtZIP; never executes Flash. The early report's
manual transcription remains an explicit input, not independently decoded
carrier data. An eight-minute match does not establish identity/connection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from extract_swf_text import extract

parser=argparse.ArgumentParser()
parser.add_argument('--court-zip',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parent
pins=json.loads((root/'COURT-PINS.json').read_text())
cross=json.loads((root/'MINUTE-CROSSWALK.json').read_text())
b=args.court_zip.read_bytes()
if hashlib.sha256(b).hexdigest()!=pins['zip_sha256']:
    raise ValueError('court ZIP hash differs; preserve separately and review')
with zipfile.ZipFile(args.court_zip) as z:
    names=[n for n in z.namelist() if Path(n).name==pins['member']]
    if len(names)!=1:raise ValueError('ambiguous SWF member')
    raw=z.read(names[0])
if hashlib.sha256(raw).hexdigest()!=pins['member_sha256']:
    raise ValueError('SWF hash differs')
d=extract(raw)
by_id={x['id']:x for x in d['text_definitions']}
checks=[]
for pin in pins['pins']:
    item=by_id[pin['id']]
    if any(item[k]!=pin[k] for k in ['tag','offset','text']):
        raise ValueError('static pin differs: '+str(pin['id']))
    checks.append(pin['id'])
rows=[]
for row in cross['rows']:
    text=by_id[row['later_time_id']]['text']
    agree=text[:5]==row['early_minute_transcription']
    if not agree:raise ValueError('minute-label mismatch')
    rows.append(dict(early_table_row=row['early_table_row'],
                     early_minute=row['early_minute_transcription'],
                     court_text=text,minute_labels_agree=agree))
if [r['early_table_row'] for r in cross['rows']]!=list(range(1,9)):
    raise ValueError('early numbered rows changed')
print(json.dumps(dict(zip_hash_verified=True,swf_hash_verified=True,
      static_pins_checked=len(checks),candidate_minute_matches=rows,
      early_numbered_rows=len(rows),all_eight_minute_labels_agree=all(x['minute_labels_agree'] for x in rows),
      scope='Integrity, static text and candidate minute-label accounting only; not native carrier decoding, call identity, clock calibration, eight completed calls, or proof of the reason for later omission.'),indent=2))
