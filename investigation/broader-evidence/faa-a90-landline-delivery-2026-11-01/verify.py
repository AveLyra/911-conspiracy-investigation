from pathlib import Path
from collections import Counter,defaultdict
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args();r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
checked=[]
if a.source_map:
 sm=json.loads(Path(a.source_map).read_text())
 for f in json.loads((r/'SOURCE-PINS.json').read_text())['inputs']:
  b=Path(sm[f['id']]).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['id'];checked.append(f['id'])
o=json.loads((r/'OBSERVATIONS.json').read_text())['memo'];ix=json.loads((r/'INDEX-ROWS.json').read_text())
def minute(s):
 assert len(s)==4 and s.isdecimal();h,n=int(s[:2]),int(s[2:]);assert 0<=h<24 and 0<=n<60
 return 60*h+n
body=minute(o['body_end'])-minute(o['body_start']);cert=minute(o['certification_end'])-minute(o['certification_start'])
num=ix['numbered_tabs'];aal=ix['AAL11_tabs'];ual=ix['UAL175_tabs'];labels=defaultdict(list)
for row in num:labels[row['content']].append(row['tab'])
dups={k:v for k,v in labels.items() if len(v)>1};aa={x['content'] for x in aal};ua={x['content'] for x in ual}
explicit=[x['printed_count'] for x in o['attachments'] if x['printed_count'] is not None]
print(json.dumps({'status':'passed','manifest_files':len(m['files']),'source_inputs_checked':checked,'labelled_minutes':{'body_local':body,'certificate_UTC':cert,'span_difference':cert-body,'numeric_start_offset':minute(o['certification_start'])-minute(o['body_start']),'numeric_end_offset':minute(o['certification_end'])-minute(o['body_end'])},'attachment_accounting':{'explicit_count_sum':sum(explicit),'unfilled_count_rows':sum(x['printed_count'] is None for x in o['attachments']),'actual_total':None},'index_accounting':{'numbered_rows':len(num),'numbered_sequence_exact_1_to_65':[x['tab'] for x in num]==list(range(1,66)),'literal_unique_numbered_labels':len(labels),'repeated_label_groups':dups,'AAL11_rows':len(aal),'UAL175_rows':len(ual),'total_rows':len(num)+len(aal)+len(ual),'common_flight_category_labels':len(aa&ua),'AAL11_only':sorted(aa-ua),'UAL175_only':sorted(ua-aa)},'scope':'Byte identity and arithmetic/counts of declared manually transcribed fields only; not actual audio length/speech completeness, originalidentity/delivery/custody, clock alignment or substantivegoal acceptance.'}))
