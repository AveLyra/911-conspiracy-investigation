from pathlib import Path
import argparse, hashlib, json

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--source-map',type=Path)
args=parser.parse_args()
manifest=json.loads((root/'MANIFEST.json').read_text())
for name, expected in manifest['files'].items():
 data=(root/name).read_bytes()
 assert len(data)==expected['bytes'],name
 assert hashlib.sha256(data).hexdigest()==expected['sha256'],name
pins=json.loads((root/'SOURCE-PINS.json').read_text())
for p in pins['source_text_pins']:
 assert hashlib.sha256(p['text'].encode()).hexdigest()==p['sha256_utf8'],p['id']
assert len(pins['source_text_pins'])==14
assert len(pins['manual_image_pins'])==6
assert all(p['viewed'] and p['render_returncode']==0 for p in json.loads((root/'VISUAL-REVIEW.json').read_text())['pages'])
assert len(json.loads((root/'VISUAL-REVIEW.json').read_text())['pages'])==17
print(f"PASS: {len(manifest['files'])} file hashes, 14 stored excerpt hashes, 6 labeled manual readings, 17 recorded visual checks")
if args.source_map:
 from pypdf import PdfReader
 sources=json.loads((root/'SOURCES.json').read_text())['sources']
 paths=json.loads(args.source_map.read_text()); readers={}
 for ident, s in sources.items():
  data=Path(paths[ident]).read_bytes()
  assert len(data)==s['bytes'],ident
  assert hashlib.sha256(data).hexdigest()==s['sha256'],ident
 for p in pins['source_text_pins']:
  ident=p['source']
  if ident not in readers: readers[ident]=PdfReader(paths[ident])
  text=readers[ident].pages[p['physical_page']-1].extract_text() or ''
  assert p['text'] in text,p['id']
  pos=text.index(p['text'])
  assert text[:pos].count('\n')+1==p['line_start_in_page_extraction'],p['id']
 print(f"PASS: {len(sources)} original-source byte hashes and 14 exact PDF substrings re-extracted; manual readings are not revalidated by code")
