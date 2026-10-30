#!/usr/bin/env python3
"""Check fixed source bytes, page boundaries and visible-raster OCR pins.
No network access, PDF text extraction, hidden-layer analysis or media decoding.
Dependencies: Python3 and pypdf. OCR inputs must be the separately preserved
Tesseract5.5.2/psm3 outputs specified in SOURCE-PINS.json, not substituted PDF text.
This verifies integrity and selected locators, not historical correctness.
"""
from pathlib import Path
import argparse,hashlib,json,sys
from pypdf import PdfReader


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--memo',required=True,type=Path)
 parser.add_argument('--email',required=True,type=Path)
 parser.add_argument('--ocr-dir',required=True,type=Path)
 args=parser.parse_args()
 root=Path(__file__).resolve().parent
 pins=json.loads((root/'SOURCE-PINS.json').read_text())
 ledger=json.loads((root/'CORRECTION-LEDGER.json').read_text())
 checks=[]
 def check(label,passed):checks.append({'check':label,'passed':bool(passed)})
 paths={'AEA1124':args.memo,'AEA1122':args.email}
 for source in pins['sources']:
  data=paths[source['id']].read_bytes()
  check(source['id']+' SHA256',hashlib.sha256(data).hexdigest()==source['sha256'])
  check(source['id']+' byte length',len(data)==source['bytes'])
  check(source['id']+' page count',len(PdfReader(paths[source['id']]).pages)==source['pages'])
 texts={}
 for page in pins['raster_and_visible_ocr_integrity']:
  path=args.ocr_dir/(page['page']+'.txt')
  data=path.read_bytes()
  texts[page['page']]=data.decode('utf-8').splitlines()
  check(page['page']+' visible OCR SHA256',hashlib.sha256(data).hexdigest()==page['visible_ocr_sha256'])
  check(page['page']+' visible OCR line count',len(texts[page['page']])==page['ocr_lines'])
 expected=['F'+str(i).zfill(2) for i in range(1,30)]+['M'+str(i).zfill(2) for i in range(1,5)]
 check('33 unique numbered request/query rows in defined source scope',[r['id'] for r in ledger['rows']]==expected)
 for row in ledger['rows']:
  key=row['source']+'-'+str(row['physical_page'])
  a,b=row['visible_ocr_lines']
  check(row['id']+' physical-page/OCR locator exists',key in texts and 1<=a<=b<=len(texts[key]))
 anchors=[('AEA1124-2',14,16,['FEB 5 2002','UAL175']),
 ('AEA1124-3',1,1,['2/1/2002 12:14 PM']),
 ('AEA1124-3',17,17,['Feb 15, 2002']),
 ('AEA1124-3',44,44,['January 4, 2002']),
 ('AEA1124-3',53,53,['11/15/2001 7:46 AM']),
 ('AEA1124-4',1,1,['Page 1 of 22']),
 ('AEA1124-4',15,17,['1249','Corrected']),
 ('AEA1124-4',26,33,['1308:45','1308:56','1311:22','1311:25','1313:05','LOF5411','LOF4511']),
 ('AEA1124-4',40,44,['1301:06','1301:05','1305:34','1305:33']),
 ('AEA1124-4',51,55,['1256:36','1306:55','1312:01','Unknown']),
 ('AEA1124-4',57,58,['1321:54','1321:56','1322:09','IPTT','IPPT']),
 ('AEA1124-5',1,1,['Page 2 of 22']),
 ('AEA1124-5',12,14,['1344','page 26','Corrected']),
 ('AEA1124-5',16,21,['1310:29','ZOB OMIC','1333:51','ZNY OMIC']),
 ('AEA1124-5',30,39,['Missing certification signature','1245','1246','1247','1316']),
 ('AEA1124-5',66,68,['up-side down','not upside down','ZNY-ARTCC-148']),
 ('AEA1122-1',1,1,['5/8/2002 8:54 AM']),
 ('AEA1122-1',20,21,['05/07/2002','03:30 PM']),
 ('AEA1122-1',43,47,['1306:17','ZBW IGN','Correction made']),
 ('AEA1122-1',55,59,['DAL1043','N90 LIB','1300:53','Correction made']),
 ('AEA1122-1',61,63,['federal express','final review','hopefully release'])]
 for key,a,b,needles in anchors:
  text=' '.join(texts[key][a-1:b])
  check(key+' lines'+str(a)+'-'+str(b)+' selected visible field anchors',all(n in text for n in needles))
 # Failure controls demonstrate byte-integrity rejection, not textual truth.
 first=pins['sources'][0]
 data=paths[first['id']].read_bytes()
 changed=bytearray(data)
 changed[len(changed)//2]^=1
 check('one-byte source mutation rejected',hashlib.sha256(changed).hexdigest()!=first['sha256'])
 check('truncated source rejected',hashlib.sha256(data[:-1]).hexdigest()!=first['sha256'])
 result={'method':'Pinned original entities/page counts, visible-pixel OCR hashes/line boundaries and selected field anchors only; no hidden text extraction or speech processing','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'limits':'Passing does not establish correction accuracy, implementation, tape/clock authenticity, completeness, intent, final delivery or source independence. Image readings and disclosed OCR errors remain separate.'}
 print(json.dumps(result,indent=2))
 return int(result['failed']>0)

if __name__=='__main__':sys.exit(main())
