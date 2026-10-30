from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=Path(__file__).parent
s=json.loads((root/'SOURCE-PINS.json').read_text());ledger=json.loads((root/'LEDGER.json').read_text());checks=[]
for x in s['L01']['screenshot_derivative_pins']:
 b=(a.captures/x['name']).read_bytes();checks.append({'file':x['name'],'bytes_match':len(b)==x['bytes'],'sha256_match':hashlib.sha256(b).hexdigest()==x['sha256']})
rows=ledger['source_rows']['rows'];pairs=[]
for left,right in zip(rows,rows[1:]):
 x,y=left['time_literal'],right['time_literal']
 if x is None or y is None:continue
 def seconds(v):
  assert len(v)==4 and v.isdigit() and int(v[2:])<60
  return (60*int(v[:2])+int(v[2:]))*60
 pairs.append({'left_row':left['row'],'left_literal':x,'right_row':right['row'],'right_literal':y,'nominal_label_seconds_difference':seconds(y)-seconds(x)})
r={'screenshot_identity_checks':checks,'all_capture_bytes_and_hashes_match':all(x['bytes_match'] and x['sha256_match'] for x in checks),'manual_rows':len(rows),'printed_time_cells':sum(x['time_literal'] is not None for x in rows),'blank_time_cells_preserved':sum(x['time_literal'] is None for x in rows),'adjacent_pairs_with_both_time_cells':pairs,'decreasing_adjacent_labels':[x for x in pairs if x['nominal_label_seconds_difference']<0],'assumptions':'Conditional HHMM arithmetic on manually transcribed table labels; blanks not filled or skipped to create adjacent pairs; no timezone/clock/event/utterance join.','scope':'Checks browser screenshot derivative identities and document-order arithmetic only. Not source-PDF authentication, independent transcription, historical correctness, event delay, clock fit, audio continuity or conspiracy test.'}
a.output.open('x').write(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['all_capture_bytes_and_hashes_match','manual_rows','printed_time_cells','blank_time_cells_preserved','decreasing_adjacent_labels']}))
raise SystemExit(0 if r['all_capture_bytes_and_hashes_match'] else 1)
