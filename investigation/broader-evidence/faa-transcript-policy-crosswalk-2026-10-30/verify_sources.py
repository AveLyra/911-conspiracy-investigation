#!/usr/bin/env python3
"""Reproduce seven selected historical-policy comparisons from pinned PDFs.
Requires pypdf6.10.0. Read-only, no network or audio. Exact regex-delimited
clauses are hashed raw and after whitespace collapse only; differences stay.
This verifies source/selection reproducibility, not case compliance or intent.
"""
from pathlib import Path
import argparse,difflib,hashlib,json,re,sys
import pypdf

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--original2000',type=Path,required=True)
 p.add_argument('--changed2003',type=Path,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parent
 pins=json.loads((root/'SOURCE-PINS.json').read_text())
 paths={'ORDER2000':a.original2000,'ORDER2003':a.changed2003}
 checks=[];texts={};comparisons=[]
 def check(label,passed):checks.append({'check':label,'passed':bool(passed)})
 for x in pins['sources']:
  data=paths[x['id']].read_bytes();reader=pypdf.PdfReader(paths[x['id']])
  check(x['id']+' pinned source entity and page count',hashlib.sha256(data).hexdigest()==x['sha256'] and len(data)==x['bytes'] and len(reader.pages)==x['total_pdf_pages'])
  for page in pins['selected_physical_pages'][x['id']]:texts[(x['id'],page)]=reader.pages[page-1].extract_text()
 for x in pins['selected_page_pins']:
  t=texts[(x['id'],x['physical_page'])]
  check(x['id']+' selected-page'+str(x['physical_page'])+' text/line pins',hashlib.sha256(t.encode()).hexdigest()==x['text_sha256'] and len(t.splitlines())==x['line_count'])
 for spec in pins['comparisons']:
  computed={};normalized=[]
  for key,x in spec['sources'].items():
   text=texts[(key,x['physical_page'])]
   start=re.search(spec['recipe']['start_regex'],text,re.S)
   if start is None:raise ValueError('Start delimiter not found: '+spec['key'])
   end=re.search(spec['recipe']['end_regex'],text[start.start():],re.S)
   if end is None:raise ValueError('End delimiter not found: '+spec['key'])
   stop=start.start()+end.end();raw=text[start.start():stop];normal=' '.join(raw.split())
   computed[key]={'physical_page':x['physical_page'],'selected_text_lines':[text.count('\n',0,start.start())+1,text.count('\n',0,stop)+1],'raw_clause_sha256':hashlib.sha256(raw.encode()).hexdigest(),'whitespace_only_sha256':hashlib.sha256(normal.encode()).hexdigest(),'raw_characters':len(raw)}
   normalized.append(normal)
  same=normalized[0]==normalized[1]
  diff=list(difflib.unified_diff(normalized[0].split(),normalized[1].split(),fromfile='ORDER2000-'+spec['key'],tofile='ORDER2003-'+spec['key'],lineterm=''))
  ok=computed==spec['sources'] and same==spec['same_after_whitespace_only'] and diff==spec['normalized_token_diff']
  check(spec['key']+' exact selection and comparison reproduced',ok)
  comparisons.append({'key':spec['key'],'same_after_whitespace_only':same,'reproduced':ok})
 src=pins['sources'][0];data=paths[src['id']].read_bytes();mutated=bytearray(data);mutated[len(mutated)//2]^=1
 check('One-byte source mutation rejected',hashlib.sha256(mutated).hexdigest()!=src['sha256'])
 result={'runtime':{'python':sys.version.split()[0],'pypdf':pypdf.__version__},'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'actual_comparisons':comparisons,'scope':'Two source entities, ten selected-page text pins and seven clause comparisons. Equality is an observed value; not all clauses match. No source rewritten, dehyphenation or glyph/punctuation repair.','limits':'Does not establish actual historical compliance, recording completeness, hardware time, implemented correction, native authenticity, delivery, source independence, intent or applicability of a later edition.'}
 print(json.dumps(result,indent=2));return int(result['failed']>0)
if __name__=='__main__':sys.exit(main())
