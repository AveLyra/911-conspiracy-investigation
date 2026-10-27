"""Verify held NARA PDF entities and selected extraction locators; not historical claims."""
import argparse,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import fitz
parser=argparse.ArgumentParser()
parser.add_argument('source_root',type=Path)
parser.add_argument('release',type=Path)
parser.add_argument('output',type=Path)
a=parser.parse_args()
assert not a.output.exists(),'Preserve the earlier receipt and choose a new output'
pins=json.loads((a.release/'SOURCES.json').read_text())
checks=[];docs={}
for pin in pins:
 path=a.source_root/pin['source_subdirectory']/pin['filename']
 body=path.read_bytes()
 with fitz.open(path) as doc:
  pages=[p.get_text() for p in doc]
  actual={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'pdf_pages':len(pages),'page_text_sha256':[hashlib.sha256(p.encode()).hexdigest() for p in pages]}
 expected={k:pin[k] for k in actual}
 passed=body.startswith(b'%PDF-') and actual==expected
 checks.append({'id':pin['id'],'filename':pin['filename'],'actual':actual,'expected':expected,'passed':passed})
 docs[pin['id']]=pages
excerpts=json.loads((a.release/'SOURCE-EXCERPTS.json').read_text())['excerpts']
line_checks=[]
for e in excerpts:
 actual=docs[e['source']][e['pdf_page']-1].splitlines()
 ok=all(actual[row['line']-1]==row['text'] for row in e['extracted_lines'])
 line_checks.append({'source':e['source'],'page':e['pdf_page'],'lines':len(e['extracted_lines']),'passed':ok})
completed=[sum(s.strip()=='Completed' for s in t.splitlines()) for t in docs['F01']]
status={'scope':'Literal text-layer Completed markers only; manual person/group classification is not software-proven','by_pdf_page':completed,'expected':[15,12],'total':sum(completed),'passed':completed==[15,12]}
result={'verified_utc':datetime.now(timezone.utc).isoformat(),'fitz_version':fitz.VersionBind,
 'scope':'Five PDF entities/page-text hashes and selected exact text-layer lines; not truth/authorship, full human reading, historical completeness/receipt or five-track completion',
 'pdf_entities':len(checks),'pdf_pages':sum(len(p) for p in docs.values()),'bytes':sum(x['actual']['bytes'] for x in checks),
 'checks':checks,'excerpt_checks':line_checks,'literal_status_count':status,
 'all_passed':all(x['passed'] for x in checks+line_checks+[status])}
with a.output.open('x') as h:json.dump(result,h,indent=2)
print(json.dumps({k:result[k] for k in ['pdf_entities','pdf_pages','bytes','fitz_version','all_passed']},indent=2))
print('Exact excerpt groups:',len(line_checks),'Literal Completed markers:',sum(completed))
assert result['all_passed']
