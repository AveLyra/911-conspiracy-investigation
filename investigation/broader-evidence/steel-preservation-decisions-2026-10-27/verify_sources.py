"""Verify acquired entity pins and the disclosed inventory/return comparison.

Requires PyMuPDF. These checks do not authenticate physical steel or custody.
"""
from pathlib import Path
import argparse,hashlib,json,re
import fitz

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--source-dir',type=Path,required=True)
 ap.add_argument('--nist-html',type=Path,required=True)
 ap.add_argument('--directory',type=Path,default=Path(__file__).parent)
 ap.add_argument('--output',type=Path)
 args=ap.parse_args();checks=[];texts={};entities=[]
 for row in json.loads((args.directory/'SOURCES.json').read_text()):
  path=args.nist_html if row['id']=='NIST2009' else args.source_dir/row['saved_filename']
  body=path.read_bytes();assert len(body)==row['bytes']
  assert hashlib.sha256(body).hexdigest()==row['sha256']
  if row['pages'] is not None:
   with fitz.open(path) as d:
    assert len(d)==row['pages'];texts[row['id']]=[p.get_text() for p in d]
  else:texts[row['id']]=body.decode('utf-8')
  entities.append(dict(id=row['id'],bytes=len(body),sha256=row['sha256'],pages=row['pages'],matches=True))
 checks.append('Five original entity hashes/sizes and four PDF page counts match preserved receipts')
 minute=' '.join(texts['PA2005'][5].split())
 assert 'completed in October 2004' in minute and 'specialized' in minute and 'agreements expired' in minute
 assert 'no specialized maintenance services have been available' in minute
 assert 'leaks that were threatening the artifacts' in minute
 checks.append('2005printed inventory date, specialized-maintenance gap and threat wording present')
 assert 'basic operations and maintenance services' in ' '.join(texts['PA2005'][6].split())
 assert '4-1/2 year' in ' '.join(texts['PA2005'][7].split())
 checks.append('Basic-maintenance contrary context and adopted supplemental term preserved separately')
 blocks={}
 for key in ['LMDC2011','LMDC2012']:
  body=texts[key][4]
  match=re.search(r'4\.\s*ARTIFACT REVIEW PROCESS(.*?)(?=The Preview Site)',body,re.S)
  assert match,'selected section not found in '+key
  raw=match.group(1);normalized=' '.join(raw.split())
  assert 'prepared and completed in 2006' in normalized
  assert 'approximately 230 items' in normalized and 'In 2009' in normalized
  blocks[key]=dict(physical_page=5,normalization='Whitespace only, no word/date/punctuation repair',
    raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),raw_characters=len(raw),
    normalized_sha256=hashlib.sha256(normalized.encode()).hexdigest(),normalized_characters=len(normalized))
  blocks[key]['_normalized']=normalized
 assert blocks['LMDC2011']['_normalized']==blocks['LMDC2012']['_normalized']
 for value in blocks.values():del value['_normalized']
 checks.append('Two selected inventory/return passages identical after disclosed whitespace-only normalization; not independent witnesses')
 html=texts['NIST2009']
 for phrase in ['more than 200 pieces','convoy of 25 tractor trailers','retained all of the samples','A few whole pieces also were retained']:
  assert phrase in html
 checks.append('Official return account retains quantity qualifiers and extracted-sample/whole-piece distinction')
 # The agreement is a scan: no inferred OCR interpretation is certified here.
 checks.append('Agreement byte/page pin checked only;14selected visible-page readings are separately disclosed')
 result=dict(entities=entities,checks=checks,check_count=len(checks),selected_section_comparison=blocks,
   physical_tests_performed=False,clock_or_custody_validation=False,
   limits='Entity/text/qualified version comparison only; no signature authenticity, delivery, damage, item-level attribution, current custody or historical cause proved')
 if args.output:
  with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
