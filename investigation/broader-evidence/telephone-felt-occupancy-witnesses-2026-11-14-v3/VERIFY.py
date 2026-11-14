#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess
b=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26');a=b/'telephone-request49-production-counterparts-2026-11-06/sources/team1a-843.pdf';c=b/'telephone-doj-early-packet-delivery-2026-11-09/packet-04.pdf'
assert hashlib.sha256(a.read_bytes()).hexdigest()=='3b2f5f67f4e649236e77922c8922f93dced518e2e3f8255473da89c1747a92fe'
assert hashlib.sha256(c.read_bytes()).hexdigest()=='7ed35efb7825f26cb0c712d334a8b286c74bcc25c5b44e01f227059f446c6dba'
tool='/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
def p(f,n):return re.sub(r'\s+',' ',subprocess.check_output([tool,'-f',str(n),'-l',str(n),'-layout',str(f),'-']).decode(errors='replace')).lower()
assert 'lots of passengers' in p(a,40)
assert 'not a lot of passengers on board' in p(a,42)
assert 'pretty empty' in p(c,92)
print('PASS: two source hashes and three extracted occupancy anchors; audio and actual occupancy untested.')
