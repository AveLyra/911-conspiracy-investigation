"""Verify exact source entities/page counts; no historical-routing/edit/voice authentication."""
from pathlib import Path
import json,hashlib,argparse
import fitz
p=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--mirror',type=Path,required=True);parser.add_argument('--hearing',type=Path,required=True);args=parser.parse_args()
rows=[]
for source in json.loads((p/'SOURCES.json').read_text())['sources']:
 path=args.mirror if source['id']=='MIRROR' else args.hearing;b=path.read_bytes()
 assert len(b)==source['bytes'] and hashlib.sha256(b).hexdigest()==source['sha256'];assert b.startswith(b'%PDF-')
 doc=fitz.open(stream=b,filetype='pdf');assert len(doc)==source['pdf_pages']
 rows.append({'id':source['id'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pdf_pages':len(doc),'match':True})
print(json.dumps({'sources':rows,'runtime':fitz.__doc__.splitlines()[0:3],'scope':'Entity fingerprints/page counts only; selected page content manually read. Not native notes/media/custody, exact editing, historical phone routing, calibrated clock, voice or historical truth verification.'},indent=2))
