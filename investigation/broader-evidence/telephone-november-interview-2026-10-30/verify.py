from pathlib import Path
import argparse, hashlib, json
p=argparse.ArgumentParser()
p.add_argument('--source-pdf', type=Path, required=True)
p.add_argument('--ocr-directory', type=Path, required=True)
p.add_argument('--counterpart-images', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a=p.parse_args(); root=Path(__file__).parent
s=json.loads((root/'SOURCE-PINS.json').read_text()); checks=[]
def check(label, actual, expected):
    checks.append(dict(label=label, actual=actual, expected=expected, passed=actual==expected))
b=a.source_pdf.read_bytes()
check('new source exact byte count',len(b),s['N19']['bytes'])
check('new source exact SHA256',hashlib.sha256(b).hexdigest(),s['N19']['sha256'])
from pypdf import PdfReader
check('PDF physical page count without hidden text extraction',len(PdfReader(a.source_pdf).pages),9)
for x in s['N19']['image_and_visible_ocr_pins']:
    b=(a.ocr_directory/('page-'+str(x['page'])+'.txt')).read_bytes()
    check('visible OCR identity page'+str(x['page']),hashlib.sha256(b).hexdigest(),x['ocr_sha256'])
for x in s['H08']['reinspected_image_pins']:
    b=(a.counterpart_images/('T02-p'+str(x['page']).zfill(3)+'.png')).read_bytes()
    check('counterpart image identity page'+str(x['page']),hashlib.sha256(b).hexdigest(),x['image_sha256'])
for page,needle in [(1,'November 19, 2003'),(1,'All participants had access'),(2,'7:27'),(2,'does not recollect the precise time'),(2,'cell call'),(2,'old term'),(3,'7:38'),(3,'7:44'),(3,'19 minutes, 39 seconds'),(4,'reset to zero'),(4,'apparently'),(4,'second recording'),(6,'no discussion'),(6,'individual flight dispatchers'),(8,'not on the phone net'),(8,'not in continuous contact')]:
    text=(a.ocr_directory/('page-'+str(page)+'.txt')).read_text()
    check('selected visible OCR anchor p'+str(page)+': '+needle,needle in text,True)
result=dict(checks=checks,passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),scope='Identity, page count and selected visible-OCR anchors only; manual full-page reading separately recorded; no hidden PDF text extraction, historical authentication, event/clock join, continuity/audio or motive test.')
with a.output.open('x') as f: json.dump(result,f,indent=2); f.write('\n')
print(json.dumps({k:result[k] for k in ['passed','failed','scope']}))
raise SystemExit(0 if result['failed']==0 else 1)
