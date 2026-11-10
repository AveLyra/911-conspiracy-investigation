from pathlib import Path
import argparse, hashlib, json
p=argparse.ArgumentParser();p.add_argument('--source-map');a=p.parse_args()
root=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((root/'MANIFEST.json').read_text())
for f in manifest['files']:
 b=(root/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['name']
checked=[]
if a.source_map:
 mapping=json.loads(Path(a.source_map).read_text());s=json.loads((root/'SOURCE-PINS.json').read_text())
 b=Path(mapping['PDF']).read_bytes();assert len(b)==s['bytes'] and sha(b)==s['sha256'];checked.append('PDF')
 for f in s['raster_records']:
  key='PAGE'+str(f['physical_page']);b=Path(mapping[key]).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],key;checked.append(key)
print(json.dumps({'status':'passed','manifest_files':len(manifest['files']),'source_inputs_checked':checked,'scope':'Exact bytes only. Visual interpretation, historical accuracy, call identity, clocks, native authorship and substantive goal acceptance are not proved by this verifier.'}))
