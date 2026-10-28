"""Check preserved notice/PDF entities and short anchors, not historical truth."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,json,re
import fitz

class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
        if t in ('p','br','tr','h1','h2','h3'):self.parts.append(' ')
    def handle_endtag(self,t):
        if t in ('script','style'):self.skip-=1
        if t in ('p','tr','h1','h2','h3'):self.parts.append(' ')
    def handle_data(self,t):
        if not self.skip:self.parts.append(t)

p=argparse.ArgumentParser()
for n in ['p01','p02','fema','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();root=Path(__file__).parent
pins={x['id']:x for x in json.loads((root/'SOURCES.json').read_text())}
files={'P01':a.p01,'P02':a.p02,'FEMA-D':a.fema}
texts={};checks=[]
for sid,path in files.items():
    b=path.read_bytes();assert hashlib.sha256(b).hexdigest()==pins[sid]['sha256'] and len(b)==pins[sid]['bytes'],sid
    checks.append(dict(id=sid,bytes=len(b),sha256=pins[sid]['sha256']))
    if sid!='FEMA-D':
        v=Visible();v.feed(b.decode('windows-1252'));texts[sid]=' '.join(''.join(v.parts).split())
with fitz.open(a.fema) as pdf:
    texts['FEMA-D']=' '.join(pdf[0].get_text(sort=True).split())
    assert len(pdf)==27
observations=[]
for row in json.loads((root/'SOURCE-ANCHORS.json').read_text()):
    text=texts[row['source']];anchor=' '.join(row['anchor'].split());offset=text.find(anchor)
    assert offset>=0,row['id']
    observations.append(dict(id=row['id'],source=row['source'],physical_page=row.get('physical_page'),normalized_text_offset=offset,meaning=row['meaning']))
unchanged={sid:hashlib.sha256(path.read_bytes()).hexdigest()==pins[sid]['sha256'] for sid,path in files.items()}
assert all(unchanged.values())
r=dict(source_checks=checks,anchor_checks=observations,source_hashes_unchanged=unchanged,pymupdf_version=fitz.VersionBind,scope='Three source-identity and eight literal/context-locator checks; no specimen, payroll, timing or funding authentication',native_workbook_acquired=False,candidate_specific_custody_verified=False,conflicting_scope_descriptions_preserved=True,location_strings_preserved=['Staten Island, NY','Staten Island, NJ'])
a.out.mkdir(parents=True,exist_ok=False)
(a.out/'RESULT.json').open('x').write(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
