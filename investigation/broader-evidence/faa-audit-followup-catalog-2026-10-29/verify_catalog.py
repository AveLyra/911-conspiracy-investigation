#!/usr/bin/env python3
"""Verify the captured HTML and selected label associations, not historical truth."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, hashlib, json
class Fields(HTMLParser):
    def __init__(self):
        super().__init__();self.main=False;self.target=None;self.parts=[];self.label=None;self.rows=[]
    def handle_starttag(self,tag,attrs):
        if tag=='main':self.main=True
        if self.main and tag in ['dt','dd']:self.target=tag;self.parts=[]
    def handle_data(self,text):
        if self.target:self.parts.append(text)
    def handle_endtag(self,tag):
        if tag==self.target:
            text=' '.join(''.join(self.parts).split())
            if tag=='dt':self.label=text
            elif self.label:self.rows.append((self.label,text))
            self.target=None
        if tag=='main':self.main=False
parser=argparse.ArgumentParser();parser.add_argument('html');args=parser.parse_args()
root=Path(__file__).resolve().parent;record=json.loads((root/'SOURCES.json').read_text())
data=Path(args.html).read_bytes()
assert len(data)==record['catalog_entity']['bytes']
assert hashlib.sha256(data).hexdigest()==record['catalog_entity']['sha256']
p=Fields();p.feed(data.decode('utf-8'));rows=dict(p.rows)
selected={label:rows[label] for label in record['selected_fields']}
assert selected==record['selected_fields']
assert "This document's content is unavailable." in rows['Content']
print(json.dumps({'bytes':len(data),'sha256':record['catalog_entity']['sha256'],'selected_fields':selected,'body_unavailable_message_present':True,'entity_and_selected_field_associations_match':True,'scope':'Capturedentity and currentfield associations only; not nativepolicy, effective cancellation, historicalreview or legalapplicability validation.'},indent=2))
