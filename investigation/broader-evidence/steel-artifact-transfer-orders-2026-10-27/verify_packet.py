"""Verify disclosed source/text joins; not physical custody or legal validation."""
from pathlib import Path
import argparse,hashlib,json
import fitz

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--source-pdf',type=Path,required=True)
 ap.add_argument('--directory',type=Path,default=Path(__file__).parent)
 ap.add_argument('--output',type=Path)
 args=ap.parse_args();source=json.loads((args.directory/'SOURCE.json').read_text())
 body=args.source_pdf.read_bytes();assert len(body)==source['bytes']
 assert hashlib.sha256(body).hexdigest()==source['sha256']
 with fitz.open(args.source_pdf) as doc:
  assert len(doc)==source['pages']==12;text=[p.get_text() for p in doc]
 checks=['Original acquired entity SHA256/size and12page count match']
 ids={str(n):text[n-1].count('1-0137') for n in [4,8,11]}
 assert ids=={'4':1,'8':1,'11':2}
 checks.append('Four exact raw1-0137mentions located across three related documents; visualIreading not substituted')
 assert text[10].strip().endswith('right of')
 second=' '.join(text[11].split())
 assert second.startswith('any party to the September 11 Litigations or their representatives to inspect and test said')
 assert 'upon ten days notice' in second
 checks.append('Reserved testing condition spans the two order pages; first page alone would be incomplete')
 assert 'Court Order' in text[8] and 'annexed hereto as Exhibit A' in text[8]
 assert 'Error! Unknown document property name.' in text[5]
 checks.append('Agreement incorporation and divider text anchors retained without source repair')
 result=dict(source_sha256=source['sha256'],checks=checks,check_count=len(checks),
 raw_id_counts_by_physical_page=ids,raw_prefix='1',visual_prefix='I, manual reading',
 independently_reviewed_visible_pages=list(range(1,13)),
 limits='Source byte/page/text checks only; no signature authenticity, complete court docket, provenance, delivery, condition, physical experiment, legal standing or current enforceability determined')
 if args.output:
  with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
