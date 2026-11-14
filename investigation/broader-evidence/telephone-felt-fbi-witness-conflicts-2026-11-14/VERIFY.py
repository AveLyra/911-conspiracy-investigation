#!/usr/bin/env python3
"""Check source hashes and limited text anchors; do not print identifying material."""
from pathlib import Path
import hashlib,re,subprocess
b=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26')
a=b/'telephone-doj-early-packet-delivery-2026-11-09/packet-04.pdf'; c=b/'telephone-request49-production-counterparts-2026-11-06/sources/team1a-843.pdf'
assert hashlib.sha256(a.read_bytes()).hexdigest()=='7ed35efb7825f26cb0c712d334a8b286c74bcc25c5b44e01f227059f446c6dba'
assert hashlib.sha256(c.read_bytes()).hexdigest()=='3b2f5f67f4e649236e77922c8922f93dced518e2e3f8255473da89c1747a92fe'
tool='/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
def page(path,n):return re.sub(r'\s+',' ',subprocess.check_output([tool,'-f',str(n),'-l',str(n),'-layout',str(path),'-']).decode(errors='replace')).lower()
p44,p45,p42,p91,p92=page(a,44),page(a,45),page(c,42),page(a,91),page(a,92)
for s in ['lots of passengers','some sort of explosion']:assert s in p44,s
for s in ['white smoke','constant']:assert s in p45,s
for s in ['intermittent','lost contact']:assert s in p42,s
assert 'pretty empty' in p92
assert not re.search(r'\b(?:smoke|explosion)\b',p91+' '+p92)
print('PASS: pinned FBI-scan hashes, selected reported phrases and extracted-transcript keyword check; audio not tested.')
