"""Check preserved reference bytes and passive PDF structure. Never extract PDF text.
Usage: verify_sources.py SOURCES.json 326=/path/326.pdf ... 637=/path/637.pdf
Court-index check is optional: index=/path/COURT-INDEX-LOCAL.html
No network, historical inference, hidden-layer/OCR or masked-field recovery.
"""
from pathlib import Path
import sys,json,hashlib
from pypdf import PdfReader
manifest=json.loads(Path(sys.argv[1]).read_text())
paths=dict(x.split('=',1) for x in sys.argv[2:])
results=[]
for s in manifest['documents']:
 p=Path(paths[s['exhibit']]);data=p.read_bytes()
 assert len(data)==s['bytes'] and hashlib.sha256(data).hexdigest()==s['sha256']
 r=PdfReader(p);assert len(r.pages)==s['pages']
 assert not r.is_encrypted
 count=len(list(r.attachments.keys()))
 assert count==0
 results.append({'exhibit':s['exhibit'],'bytes':len(data),'sha256':s['sha256'],'pages':len(r.pages),'embedded_attachment_name_count':count,'matches':True})
if 'index' in paths:
 b=Path(paths['index']).read_bytes();s=manifest['court_index']
 assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256']
 results.append({'court_index':s['url'],'bytes':len(b),'sha256':s['sha256'],'matches':True})
print(json.dumps({'checks':results,'result':'All supplied reference bytes and passive structures match','manual_reading_independently_verified_by_this_code':False,'historical_or_native_authentication_performed':False},indent=2))
