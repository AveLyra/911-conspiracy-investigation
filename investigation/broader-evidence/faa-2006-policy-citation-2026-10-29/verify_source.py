#!/usr/bin/env python3
"""Check entity identity and two text-layer observations; no historical validation."""
from pathlib import Path
import argparse, hashlib, json
from pypdf import PdfReader
parser=argparse.ArgumentParser()
parser.add_argument('pdf')
args=parser.parse_args()
root=Path(__file__).resolve().parent
record=json.loads((root/'SOURCES.json').read_text())
data=Path(args.pdf).read_bytes()
assert len(data)==record['source']['bytes']
assert hashlib.sha256(data).hexdigest()==record['source']['sha256']
pdf=PdfReader(args.pdf)
assert len(pdf.pages)==record['source']['pages']
counts={str(n):len(pdf.pages[n-1].extract_text() or '') for n in [105,106]}
assert counts==record['selected_text_characters']
print(json.dumps({'bytes':len(data),'sha256':record['source']['sha256'],'pages':len(pdf.pages),'selected_text_characters':counts,'entity_and_selected_extraction_match':True,'scope':'Integrity and text representation only; visual/manual reading and case applicability are not independently validated.'},indent=2))
