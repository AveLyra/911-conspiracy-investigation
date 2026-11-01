from pathlib import Path
import argparse, hashlib, json
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args()
r=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
d=json.loads((r/'COMPARISON.json').read_text())
comparisons=[]
for row in d['rows']:
 on=row['statement_on']==row['report_on'].replace(':','')
 off=row['statement_off']==row['report_off'].replace(':','')
 comparisons.append({'id':row['id'],'on_string_agrees':on,'off_string_agrees':off,'position_labels':[row['statement_position'],row['report_position']],'physical_clock_alignment':'not tested'})
def minute(t):
 s=t.split()[0];assert len(s)==4 and s.isdecimal()
 h,n=int(s[:2]),int(s[2:]);assert 0<=h<24 and 0<=n<60
 return h*60+n
weather=[{'id':w['id'],'adjacent_minus_body_minutes':minute(w['date_time'].split()[-2])-minute(w['body'])} for w in d['weather_pairs']]
checked=[]
if a.source_map:
 sm=json.loads(Path(a.source_map).read_text());pins=json.loads((r/'SOURCE-PINS.json').read_text())
 for f in pins['inputs']:
  b=Path(sm[f['id']]).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['id'];checked.append(f['id'])
print(json.dumps({'status':'passed','manifest_files':len(m['files']),'source_inputs_checked':checked,'time_field_comparisons':comparisons,'weather_label_arithmetic':weather,'scope':'Integrity of declared bytes and arithmetic/comparison of manually transcribed visible fields only; no native authenticity, independent corroboration, actual clock error, historical accuracy, cause or substantive-goal acceptance established.'}))
