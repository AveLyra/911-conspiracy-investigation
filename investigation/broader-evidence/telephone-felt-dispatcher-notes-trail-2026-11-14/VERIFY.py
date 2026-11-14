#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess
b=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26')
a=b/'telephone-request49-production-counterparts-2026-11-06/sources/team1a-843.pdf';c=b/'telephone-january-presentation-and-may-doj-questions-2026-11-08/team7-may14-doj-questions-264.pdf'
assert hashlib.sha256(a.read_bytes()).hexdigest()=='3b2f5f67f4e649236e77922c8922f93dced518e2e3f8255473da89c1747a92fe'
assert hashlib.sha256(c.read_bytes()).hexdigest()=='63bbdde74e5d44e78a251a75f9647247cb9613b2a9e0013c4cbdfcea57354789'
tool='/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
def page(p,n):return re.sub(r'\s+',' ',subprocess.check_output([tool,'-f',str(n),'-l',str(n),'-layout',str(p),'-']).decode(errors='replace')).lower()
x,y,z=page(a,42),page(c,1),page(c,2)
for s in ['handwritten notes','notes will be maintained in the 1-a section','09/13/2001']:assert s in x,s
assert 'may 14, 2004' in y
for s in ['contemporaneous notes','excluding fbi 302','john shaw (felt ua 93)']:assert s in z,s
print('PASS: source hashes and selected note/request anchors; transfer and receipt untested.')
