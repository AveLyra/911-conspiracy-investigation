"""Verify the exact released PDF entity; this does not verify the recording or transcript."""
import argparse,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--pdf',type=Path,required=True);args=parser.parse_args()
source=json.loads((p/'SOURCES.json').read_text())['sources'][0]
b=args.pdf.read_bytes();assert len(b)==source['bytes'];assert hashlib.sha256(b).hexdigest()==source['sha256'];assert b.startswith(b'%PDF-')
import fitz
doc=fitz.open(stream=b,filetype='pdf');assert len(doc)==source['pdf_pages']
print(json.dumps({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'pdf_pages':len(doc),'runtime':fitz.__doc__.splitlines()[0:3],'match':True,'limits':'Source entity and page count only. Dates, transcript readings and source roles were visually read, not automatically authenticated. No recording, clock, custody, voice or source-to-exhibit test.'},indent=2))
