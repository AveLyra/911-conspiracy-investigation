"""Check the three source copies and the limited source-field comparisons.

Requires pypdf. Obtain PDFs independently using the member locators in SOURCE-PINS.json.
This verifies documentary fields, not authenticity, delivery, call routing or clock calibration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zlib

from pypdf import PdfReader

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--request', required=True, type=Path)
parser.add_argument('--briefing', required=True, type=Path)
parser.add_argument('--reply', required=True, type=Path)
parser.add_argument('--pins', type=Path, default=Path(__file__).with_name('SOURCE-PINS.json'))
args = parser.parse_args()
pins = json.loads(args.pins.read_text())
pages = {}
for key in ('request', 'briefing', 'reply'):
    path = getattr(args, key)
    raw = path.read_bytes()
    record = pins['sources'][key]
    assert raw.startswith(b'%PDF-'), key
    assert len(raw) == record['bytes'], key
    assert hashlib.sha256(raw).hexdigest() == record['sha256'], key
    assert f'{zlib.crc32(raw):08x}' == record['crc32'], key
    reader = PdfReader(path)
    assert len(reader.pages) == record['pdf_pages'], key
    pages[key] = [' '.join(p.extract_text(extraction_mode='layout').split()) for p in reader.pages]

checks = [
    ('deadline', 'request', 3, r'August\s+1\s*,\s*2003'),
    ('closing date', 'request', 4, r'December\s+4,\s*2003'),
    ('forwarding question', 'request', 1, r'forwarded to FO and/or American counsel'),
    ('request 1 grouping', 'request', 1, r'responsive to AAL Doc Request No\. 1, Item 1'),
    ('onboard log request', 'request', 1, r'GTE air phone logs itemizing the calls'),
    ('voice request', 'request', 1, r'Recordings and/or transcripts'),
    ('desk log request', 'request', 3, r'calls received at the desk'),
    ('SOC log request', 'request', 3, r'from all phones in the SOC'),
    ('SERO endpoint', 'request', 3, r'Southeast Regional Reservations Office \(SERO\)'),
    ('Logan endpoint', 'request', 3, r'Logan Flight Services Office'),
    ('rolling production', 'request', 4, r'rolling'),
    ('location referral', 'request', 4, r'where such documents may be located'),
    ('briefing identity', 'briefing', 1, r'FBI BRIEFING REQUEST NO\. 5'),
    ('briefing date', 'briefing', 1, r'July 29, 2003'),
    ('reply date', 'reply', 1, r'January 20, 2004'),
    ('reply provider', 'reply', 1, r'AT&T Claircom'),
    ('reply limited scope', 'reply', 1, r'monthly system wide reliability reports'),
]
for label,key,page,pattern in checks:
    assert re.search(pattern, pages[key][page-1]), label
print(json.dumps({'source_files_verified':len(pages), 'source_field_checks_passed':len(checks),
                  'scope':'Hash/CRC/page checks and printed field anchors only. No call event, clock, delivery or historical inference tested.'}, indent=2))
