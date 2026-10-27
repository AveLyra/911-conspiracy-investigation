"""Reproduce selected printed-ID grouping and clock-label arithmetic.

Usage: python verify_event_groups.py CAPTURE_DIR EVENT_OBSERVATIONS_JSON
       LOCAL_IDENTIFIER_TRANSCRIPTIONS_JSON NEW_RESULT_JSON

The local identifier file is a list of rows keyed by id, with csc_call_id and
gs_call_id. Transcribe from the linked source pixels; never infer an unreadable
identifier from the desired grouping. The file may contain the other safe
fields, but raw identifiers are never included in the output. Source hashes
authenticate the held image entity, not the manual transcription or history.
"""
from pathlib import Path
from datetime import datetime
import hashlib,json,sys

captures, observations, identifiers, result_path=map(Path,sys.argv[1:])
safe=json.loads(observations.read_text())
local={r['id']:r for r in json.loads(identifiers.read_text())}
assert set(local)=={r['id'] for r in safe}
checks=[]
entities={}
for row in safe:
 page=row['reader_page']
 path=captures/('reader-page-%02d.jpg'%page)
 if page not in entities:
  body=path.read_bytes()
  match=len(body)==row['source_bytes'] and hashlib.sha256(body).hexdigest()==row['source_sha256']
  entities[page]=dict(reader_page=page,sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),matches=match)
  checks.append(dict(check='Reader%d entity pin'%page,passed=match))
 assert local[row['id']]['csc_call_id'] and local[row['id']]['gs_call_id']
groups={}
for row in safe:groups.setdefault(row['printed_identifier_group'],[]).append(row)
group_results=[]
for name,rows in groups.items():
 csc={local[r['id']]['csc_call_id'] for r in rows}
 gs={local[r['id']]['gs_call_id'] for r in rows}
 matched=len(csc)==1 and len(gs)==1
 checks.append(dict(check=name+' transcribed CSC/GS equality',passed=matched))
 group_results.append(dict(group=name,rows=[r['id'] for r in rows],same_transcribed_csc=len(csc)==1,same_transcribed_gs=len(gs)==1,
   inference_limit='Printed identifier grouping in a qualified mirror; not physical leg/caller/recipient/custody authentication'))
cross=local['E18-M']['csc_call_id']!=local['E25-M']['csc_call_id'] and local['E18-M']['gs_call_id']!=local['E25-M']['gs_call_id']
checks.append(dict(check='Two actual source groups have different transcribed identifiers',passed=cross))
def seconds(t):
 d=datetime.strptime(t,'%H:%M:%S');return d.hour*3600+d.minute*60+d.second
by_id={r['id']:r for r in safe}
def span(a,b):return seconds(b)-seconds(a)
g18=[dict(id=r['id'],printed_duration=r['duration'],start_to_event_seconds=span(r['start_time'],r['event_time'])) for r in groups['G18']]
checks.append(dict(check='G18 two zero fields coexist with 46/59-second label spans',passed=[r['printed_duration'] for r in g18]==[0,0] and [r['start_to_event_seconds'] for r in g18]==[46,59]))
d=by_id['E25-D'];menu=by_id['E25-M'];route=by_id['E25-R']
g25=dict(menu_start_to_event_seconds=span(menu['start_time'],menu['event_time']),
 start_to_disconnect_seconds=span(d['start_time'],d['event_time']),
 start_to_billing_seconds=span(d['start_time'],d['billing_start']),
 billing_to_disconnect_seconds=span(d['billing_start'],d['event_time']),printed_duration=d['duration'],
 route_event_minus_billing_seconds_if_each_reading={t:span(d['billing_start'],t) for t in route['event_time_readings']},
 route_reading_selected=False)
checks.append(dict(check='G25 193 total / 34 pre-billing / 159 billing interval',passed=(g25['start_to_disconnect_seconds'],g25['start_to_billing_seconds'],g25['billing_to_disconnect_seconds'])==(193,34,159) and d['duration']==159))
checks.append(dict(check='Ambiguous routed time preserved; no unique signed offset',passed=g25['route_event_minus_billing_seconds_if_each_reading']=={'07:26:18':-4,'07:26:28':6} and route['event_time'] is None))
result=dict(scope='Manual printed identifier comparison and timestamp-label arithmetic only; no native CDR/schema, clock calibration or caller identification',
 entities=list(entities.values()),groups=group_results,cross_group_identifiers_differ=cross,G18=g18,G25=g25,checks=checks,
 passed=sum(c['passed'] for c in checks),total=len(checks))
with result_path.open('x') as handle:json.dump(result,handle,indent=2)
print(json.dumps({'passed':result['passed'],'total':result['total'],'G18':g18,'G25':g25,'raw_identifiers_in_output':False},indent=2))
if result['passed']!=result['total']:raise SystemExit(1)
