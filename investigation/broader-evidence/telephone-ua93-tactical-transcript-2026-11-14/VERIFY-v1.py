#!/usr/bin/env python3
"""Verify two released PDF bytes and selected transcript passages, not recordings.
Set PDFTOTEXT to the Poppler pdftotext path if it is not on PATH.
Usage: python3 VERIFY.py POSITION14.pdf POSITION15.pdf
"""
import hashlib,os,subprocess,sys
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit(__doc__)
inputs=[('94d348e957240ea2cd8260b310ba8f5406a4b1a4dd95a3c79d3b77078e4e42f4',sys.argv[1]),('20ad384d59650e5a08447c600e8ed8b72e6b6391c66120a2984f00688cabd14c',sys.argv[2])]
texts=[]
for expected,path in inputs:
 b=Path(path).read_bytes(); assert hashlib.sha256(b).hexdigest()==expected
 text=subprocess.check_output([os.environ.get('PDFTOTEXT','pdftotext'),'-layout',path,'-']).decode('utf-8','replace')
 texts.append(text.split('\f'))
a=' '.join((texts[0][59]+' '+texts[0][60]).lower().split())
b=' '.join((texts[1][80]+' '+texts[1][81]).lower().split())
for x in (a,b):
 assert '911 air phone' in x and 'cell phone.' in x and 'oak brook' in x
assert '93, cell phone call received from a passenger.' in b
assert '93, cell phone call received from a passenger.' not in a
assert 'in touch with a passenger.' in a and 'both were pd.' in b
print('Verified source hashes, selected PDF page locations, shared labels and the specified line difference.')
print('This checks transcribed text, not the original call, audio, speakers or clocks.')
