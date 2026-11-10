from pathlib import Path
import argparse, hashlib, json
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args()
r=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
checked=[]
if a.source_map:
 d=json.loads(Path(a.source_map).read_text());s=json.loads((r/'SOURCE-PINS.json').read_text())
 expected={'AEA1130':(s['bytes'],s['sha256']),'AEA1121':(s['memo_context']['bytes'],s['memo_context']['sha256'])}
 for f in s['new_rasters']:expected['P'+str(f['physical_page'])]=(f['bytes'],f['sha256'])
 for f in s['detail_rasters']:expected['D'+str(f['physical_page'])]=(f['bytes'],f['sha256'])
 for f in s['context_rasters']:expected[f['id']]=(f['bytes'],f['sha256'])
 for key,(size,digest) in expected.items():
  b=Path(d[key]).read_bytes();assert len(b)==size and sha(b)==digest,key;checked.append(key)
print(json.dumps({'status':'passed','manifest_files':len(m['files']),'source_inputs_checked':checked,'scope':'Byte checks only; no historical accuracy, native authenticity, call identity, clock, implementation or whole-goal acceptance proved.'}))
