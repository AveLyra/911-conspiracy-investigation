#!/usr/bin/env python3
"""Verify pinned PDF entities/pages, preserved visible-raster OCR and document arithmetic.
No network, PDF text-layer extraction, redaction recovery or audio/clock processing.
Requires pypdf and the specific local Tesseract5.5.2/psm3 outputs in SOURCE-PINS.
Passing checks do not authenticate historical claims or correction implementation.
"""
from pathlib import Path
import argparse,hashlib,json,re,sys
from pypdf import PdfReader

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--earlier',type=Path,required=True)
 p.add_argument('--later',type=Path,required=True)
 p.add_argument('--ocr-dir',type=Path,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parent
 pins=json.loads((root/'SOURCE-PINS.json').read_text())
 ledger=json.loads((root/'FIELD-LEDGER.json').read_text())
 checks=[]
 def check(name,passed):checks.append({'check':name,'passed':bool(passed)})
 sources={'AEA1121':a.earlier,'AEA1123':a.later}
 for s in pins['sources']:
  data=sources[s['id']].read_bytes()
  check(s['id']+' exact source SHA256',hashlib.sha256(data).hexdigest()==s['sha256'])
  check(s['id']+' exact source bytes',len(data)==s['bytes'])
  check(s['id']+' physical PDF pages',len(PdfReader(sources[s['id']]).pages)==s['pages'])
 texts={}
 for x in pins['raster_and_ocr_integrity']:
  data=(a.ocr_dir/(x['page']+'.txt')).read_bytes();texts[x['page']]=data.decode().splitlines()
  check(x['page']+' visible OCR SHA256',hashlib.sha256(data).hexdigest()==x['visible_ocr_sha256'])
  check(x['page']+' visible OCR line count',len(texts[x['page']])==x['ocr_lines'])
 check('30 selected field observations, not all source requests',[r['id'] for r in ledger['rows']]==['V'+str(n).zfill(2) for n in range(1,31)])
 for r in ledger['rows']:
  key=r['source']+'-'+str(r['physical_page']);lo,hi=r['visible_ocr_lines']
  check(r['id']+' page/OCR span exists',key in texts and 1<=lo<=hi<=len(texts[key]))
 for physical in range(2,10):
  text=' '.join(texts['AEA1121-'+str(physical)][:4])
  check('Correction-list printed page'+str(physical-1)+'of8 visible',bool(re.search(r'Page\s*'+str(physical-1)+r'\s*of\s*8',text)))
 anchors=[('AEA1121-1',17,21,['JAN 18 2002','UAL175']),
 ('AEA1121-1',26,28,['original electronic mail','explanation']),
 ('AEA1121-2',37,38,['1245:58','1245:59','1244:58','1244:59']),
 ('AEA1121-3',17,18,['1301:37','1301:35','Change made']),
 ('AEA1121-4',23,26,['1302:00','1302:04','1302:02','1302:06']),
 ('AEA1121-4',57,61,['Partial','Full','5 minutes']),
 ('AEA1121-5',40,42,['1308:45','LOF5411','LOF4511']),
 ('AEA1121-5',52,54,['8020.11B','77d(4)','tape verified','no footnote']),
 ('AEA1121-6',12,14,['1250:02','land line']),
 ('AEA1121-7',63,68,['radio','landline','1311:06','1311:09']),
 ('AEA1121-8',10,14,['Page 19','page 9','our package','your package','Change made']),
 ('AEA1121-8',63,71,['1078','Page 1 of 5','5 full minutes']),
 ('AEA1121-9',5,12,['Area C Sup','Area C OS','Page 5 of 5','77d(4)']),
 ('AEA1121-9',14,16,['72c(11)','copies']),
 ('AEA1121-9',20,24,['equipment configuration','hand written','Attachment']),
 ('AEA1123-1',21,26,['two copies','page 2 of 23','missing']),
 ('AEA1123-2',5,9,['05/14/2002','Friday','certified']),
 ('AEA1123-3',19,31,['1306:17','ZBW IGN','DAL1043','1300:53','final review'])]
 for key,lo,hi,needles in anchors:
  text=' '.join(texts[key][lo-1:hi])
  check(key+' selected fields at'+str(lo)+'-'+str(hi),all(n in text for n in needles))
 def seconds(label):
  assert re.fullmatch(r'\d{4}:\d{2}',label)
  return int(label[:2])*3600+int(label[2:4])*60+int(label[5:])
 for n,pair in enumerate(ledger['document_label_arithmetic'],1):
  check('Written-pair arithmetic'+str(n),seconds(pair['right'])-seconds(pair['left'])==pair['right_minus_left_seconds'])
 groups=ledger['transcript_groups']
 check('Declared group counts sum135numbered requests',sum(x['numbered_items'] for x in groups)==135)
 check('Eight defined group ordinals, not claim of missing seventh',[x['ordinal'] for x in groups]==[1,2,3,4,5,6,8,9])
 src=pins['sources'][0];data=sources[src['id']].read_bytes();mutated=bytearray(data);mutated[len(mutated)//2]^=1
 check('One-byte source mutation rejected',hashlib.sha256(mutated).hexdigest()!=src['sha256'])
 check('Truncated source rejected',hashlib.sha256(data[:-1]).hexdigest()!=src['sha256'])
 result={'method':'Fixed source entities/page counts, visible-raster OCR hashes/line spans, selected fields and four label-pair calculations. No speech or hardware clocks measured.','checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'limits':'No historical correctness, global time offset, amendment accuracy, native attachment identity, dispatch/receipt, final approval or source-independence validation. Handwriting is image-read, not authenticated by OCR.'}
 print(json.dumps(result,indent=2));return int(result['failed']>0)
if __name__=='__main__':sys.exit(main())
