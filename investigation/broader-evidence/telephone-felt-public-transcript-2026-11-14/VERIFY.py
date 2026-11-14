#!/usr/bin/env python3
"""Check source bytes and selected source anchors, not the underlying events."""
import hashlib,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
base=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26')
pdf=base/'telephone-doj-early-packet-delivery-2026-11-09/packet-04.pdf'
html=base/'telephone-felt-public-transcript-2026-11-14/nps-20261114.html'
assert hashlib.sha256(pdf.read_bytes()).hexdigest()=='7ed35efb7825f26cb0c712d334a8b286c74bcc25c5b44e01f227059f446c6dba'
assert hashlib.sha256(html.read_bytes()).hexdigest()=='3521bd59a1c42b8f33a449465336597ce493ae2a64693ee289bd802b9d40f076'
tool='/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
def page(n): return re.sub(r'\s+',' ',subprocess.check_output([tool,'-f',str(n),'-l',str(n),'-layout',str(pdf),'-']).decode(errors='replace')).lower()
p88,p90=page(88),page(90)
for v in ['09/17/2001','original tape recording','entered into evidence','transcript of the call']: assert v in p88,v
for v in ['09/11/2001','verbatim transcription of a recorded']: assert v in p90,v
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,s): self.parts.append(s)
p=Text(); p.feed(html.read_text()); t=re.sub(r'\s+',' ',' '.join(p.parts)).lower()
for v in ['all times are in eastern daylight time','9:58, rear restroom of aircraft (edward felt)','70 seconds','westmoreland county 911 center','the fbi transcript of the call follows']: assert v in t,v
print('PASS: two source hashes and selected page anchors; audio and event claims untested')
