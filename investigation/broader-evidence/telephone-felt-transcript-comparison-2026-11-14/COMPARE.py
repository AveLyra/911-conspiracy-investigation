#!/usr/bin/env python3
"""Compare bounded non-identifying transcript segments; raw contact details never printed."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,re,subprocess,difflib
root=Path('/Users/admin/docs/911-worktrees/broader-evidence-review-2026-10-26/research/broader-evidence-review-2026-10-26')
pdf=root/'telephone-doj-early-packet-delivery-2026-11-09/packet-04.pdf'
html=root/'telephone-felt-public-transcript-2026-11-14/nps-20261114.html'
assert hashlib.sha256(pdf.read_bytes()).hexdigest()=='7ed35efb7825f26cb0c712d334a8b286c74bcc25c5b44e01f227059f446c6dba'
assert hashlib.sha256(html.read_bytes()).hexdigest()=='3521bd59a1c42b8f33a449465336597ce493ae2a64693ee289bd802b9d40f076'
tool='/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftotext'
def page(n): return subprocess.check_output([tool,'-f',str(n),'-l',str(n),'-layout',str(pdf),'-']).decode(errors='replace').splitlines()
a,b=page(91),page(92)
assert 'Caller:' in a[11] and 'name sir' in b[15].lower() and 'how big' in b[23].lower()
source=' '.join(a[11:38]+b[11:16]+b[23:40])
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
p=Text();p.feed(html.read_text());t=re.sub(r'\s+',' ',' '.join(p.parts))
head='the fbi transcript of the call follows:';t=t[t.lower().index(head)+len(head):];end='(call terminated)';t=t[:t.lower().index(end)+len(end)]
t=t[:t.lower().index('caller: “edward felt.')]+t[t.lower().index('911: “how big of a plane sir?'):]
assert len(re.findall(r'\(UI\)',' '.join(a[11:38]+b[23:40]),re.I))==4
assert len(re.findall(r'\(unintelligible\)',t,re.I))==4
def norm(s):
 s=s.lower().replace('(ui)',' unintelligible ')
 s=re.sub(r'caller\s*:|9\s*1[.\s]*1\s*:',' ',s)
 return re.findall(r'[a-z]+|\d+',s)
x,y=norm(source),norm(t);m=difflib.SequenceMatcher(a=x,b=y,autojunk=False)
diffs=[(op,x[i:j],y[k:l]) for op,i,j,k,l in m.get_opcodes() if op!='equal']
assert len(x)==len(y)==273 and sum(z.size for z in m.get_matching_blocks())==272
assert diffs==[('replace',['highjacking'],['hijacking'])]
print('PASS: pinned bytes; four marker positions and 272/273 normalized non-identifying tokens. Audio untested.')
