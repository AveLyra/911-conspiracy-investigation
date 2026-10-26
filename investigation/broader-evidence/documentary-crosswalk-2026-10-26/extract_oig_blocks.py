"""Reproduce local paragraph locators from the pinned OIG HTML bytes.

Usage: python3 extract_oig_blocks.py path/to/doj-oig-chapter5.html
Explicit cp1252 decoding is a reader choice, not a server-encoding claim.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows=[]; self.parts=[]; self.skip=0
    def flush(self):
        text=' '.join(' '.join(self.parts).split())
        if text:self.rows.append(text)
        self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']:self.skip+=1
        if tag in ['p','li','h1','h2','h3','h4','br','tr']:self.flush()
    def handle_endtag(self,tag):
        if tag in ['p','li','h1','h2','h3','h4','tr']:self.flush()
        if tag in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)

def extract(path):
    p=Blocks();p.feed(Path(path).read_bytes().decode('cp1252'));p.flush()
    return '\n'.join(f'P{i:03d}\t{b}' for i,b in enumerate(p.rows,1))+'\n'

if __name__=='__main__':
    sys.stdout.write(extract(sys.argv[1]))
