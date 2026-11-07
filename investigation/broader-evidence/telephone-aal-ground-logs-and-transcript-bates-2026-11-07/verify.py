"""Verify the two held source copies and the selected printed-field crosswalk.

Requires pypdf. Source locators are in SOURCE-PINS.json.
No audio, call identity, delivery, search completeness or clock test is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zlib

from pypdf import PdfReader

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--counsel', required=True, type=Path)
p.add_argument('--request', required=True, type=Path)
p.add_argument('--pins', type=Path, default=Path(__file__).with_name('SOURCE-PINS.json'))
a = p.parse_args()
pins = json.loads(a.pins.read_text())
readers = {}
for key in ('counsel', 'request'):
    raw = getattr(a,key).read_bytes()
    s = pins['sources'][key]
    assert raw.startswith(b'%PDF-')
    assert len(raw) == s['bytes']
    assert hashlib.sha256(raw).hexdigest() == s['sha256']
    assert f'{zlib.crc32(raw):08x}' == s['crc32']
    readers[key] = PdfReader(getattr(a,key))
    assert len(readers[key].pages) == s['pdf_pages']

checks = [
    ('counsel',9,r'12/4/03 UNTRANSMITTED DOCUMENT REQUEST NO\. 2'),
    ('counsel',9,r'February 9, 2004'),
    ('counsel',9,r'including at Suzanne Clark'),
    ('counsel',11,r'the SOC did not maintain any logs'),
    ('counsel',11,r'American is still investigating'),
    ('counsel',11,r'Southeast Regional Reservations Office'),
    ('counsel',11,r'Logan Flight Service Office'),
    ('counsel',13,r'On November 14, 2003'),
    ('counsel',13,r'transcripts of five telephone calls'),
    ('counsel',13,r'006376-006388'),
    ('counsel',13,r'American is unaware of any other calls'),
    ('request',3,r'August\s+1\s*,\s*2003'),
    ('request',4,r'December 4, 2003'),
    ('request',3,r'Suzanne Clarke'),
    ('request',3,r'from all phones in the SOC'),
    ('request',1,r'forwarded to FO and/or American counsel'),
]
for key,page,pattern in checks:
    text = ' '.join(readers[key].pages[page-1].extract_text(extraction_mode='layout').split())
    assert re.search(pattern,text), (key,page,pattern)
print(json.dumps({'source_copies_verified':2,'printed_field_checks_passed':len(checks),
                  'scope':'Source bytes, page counts and selected printed fields only. Counsel representations, transmission, search completeness and calls remain unverified.'},indent=2))
