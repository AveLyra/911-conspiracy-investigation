from pathlib import Path
from datetime import datetime
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args();r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
checked=[]
if a.source_map:
 sm=json.loads(Path(a.source_map).read_text())
 for f in json.loads((r/'SOURCE-PINS.json').read_text())['inputs']:
  b=Path(sm[f['id']]).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['id'];checked.append(f['id'])
o=json.loads((r/'OBSERVATIONS.json').read_text());c=o['A90_67']['certified_copy'];d=o['A90_67']['DAT']
def hhmm(s):
 s=s.split()[0];assert len(s)==4 and s.isdecimal();h,n=int(s[:2]),int(s[2:]);assert 0<=h<24 and 0<=n<60;return 60*h+n
# Certificate endpoints are same date; DAT endpoints include date andZ, preserved separately.
short=hhmm(c['end'])-hhmm(c['start'])
def endpoint(s):return datetime.strptime(s,'%B %d, %Y, %H%MZ')
long=(endpoint(d['end'])-endpoint(d['start'])).total_seconds()/60
print(json.dumps({'status':'passed','manifest_files':len(m['files']),'source_inputs_checked':checked,'labelled_certified_interval_minutes':short,'labelled_DAT_date_span_minutes':long,'actual_audio_duration_or_completeness':'not tested','scope':'Declared byte integrity and arithmetic of transcribed printed endpoints only; no audio, independent clock, custody/signature, historical cause or substantive-goal acceptance.'}))
