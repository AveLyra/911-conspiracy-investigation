"""Check saved HTML identities and the limited archive-scope statements.

No catalog census, original WTC inventory, specimen identity or historical custody is tested.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.skip = 0
        self.buf = []
        self.rows = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'):
            self.skip += 1
        if tag == 'p':
            if self.depth == 0:
                self.buf = []
            self.depth += 1
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.skip:
            self.skip -= 1
        if tag == 'p' and self.depth:
            self.depth -= 1
            if self.depth == 0:
                s = ' '.join(''.join(self.buf).split())
                if s:
                    self.rows.append(s)
    def handle_data(self, data):
        if self.depth and not self.skip:
            self.buf.append(data)

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--sources', required=True, type=Path, help='Directory containing the three preserved HTML response bodies')
p.add_argument('--pins', type=Path, default=Path(__file__).with_name('SOURCE-PINS.json'))
a = p.parse_args()
pins = json.loads(a.pins.read_text())
paragraphs = {}
for name,item in pins['sources'].items():
    raw = (a.sources / (name+'.html')).read_bytes()
    assert len(raw) == item['bytes'], name
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], name
    parser = Paragraphs()
    parser.feed(raw.decode('utf-8'))
    paragraphs[name] = parser.rows

scope = paragraphs['archive-scope']
assert len(scope) == 3
assert 'business documents, correspondence, emails, and related office materials' in scope[0]
assert 'the Voorsanger Architects Archive does not' in scope[0]
assert 'University of St. Thomas Department of Art History' in scope[1]
assert 'A curated collection of 25 projects' in scope[2]
assert 'physical and digital collections' in paragraphs['university-arts'][11]
assert '25 Voorsanger projects' in paragraphs['university-archive-announcement'][8]
print(json.dumps({'html_bodies_verified':3, 'scope':'Exact saved bytes and selected published scope statements only; no complete archive holdings or WTC item records verified.'},indent=2))
