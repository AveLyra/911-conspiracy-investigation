#!/usr/bin/env python3
"""Verify public source bytes and selected passages; not the historical 911 call.
Set PDFTOTEXT if Poppler's pdftotext is not on PATH.
Usage: python3 VERIFY.py PUBLISHER_CHAPTER.pdf COMMISSION_416.pdf
"""
from pathlib import Path
import hashlib,os,subprocess,sys
if len(sys.argv)!=3: raise SystemExit(__doc__)
expected=['50dc5a7eec566e7a9ab9192e40934b785f1f1479006b6ef12f5725222ec4e892','a14b7e47d2225c727415547eccd1d825bb50492302641d8f8b29217372026eee']
texts=[]
for path,sha in zip(sys.argv[1:],expected):
 assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
 t=subprocess.check_output([os.environ.get('PDFTOTEXT','pdftotext'),'-layout',path,'-']).decode('utf-8','replace')
 texts.append(t.split('\f'))
book=' '.join(texts[0][8].lower().split());memo=' '.join(texts[1][0].lower().split())
assert 'airfone operations surveillance center (aosc)' in book
assert 'i later discovered that when the aosc called the local 911 operator' in book
assert 'airplane operations surveillance center (aosc)' in memo
assert 'contacted the fbi, united airlines and perhaps other authorities' in memo
print('Verified both PDF hashes and the selected PDF p.9 / p.1 text fields.')
print('This does not test the identity, timing or origin of a call.')
