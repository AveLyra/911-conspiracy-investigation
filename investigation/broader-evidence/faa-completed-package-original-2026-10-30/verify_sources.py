#!/usr/bin/env python3
"""Verify a fixed released PDF entity and selected visible-raster OCR field pins.
Requires pypdf6.10.0. No network, text-layer extraction, redaction recovery,
speech/audio processing or hardware-clock test. Input OCR is the separately
preserved Tesseract5.5.2/psm3 derivative in SOURCE-PINS, not substituted PDF text.
Checks reproduce integrity/locators only, not historical accuracy or delivery.
"""
from pathlib import Path
import argparse,hashlib,json,sys
import pypdf

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--pdf',type=Path,required=True)
 p.add_argument('--ocr-dir',type=Path,required=True)
 a=p.parse_args();root=Path(__file__).resolve().parent
 pins=json.loads((root/'SOURCE-PINS.json').read_text());obs=json.loads((root/'OBSERVATIONS.json').read_text())
 source=pins['source'];data=a.pdf.read_bytes();checks=[];texts={}
 def check(name,passed):checks.append({'check':name,'passed':bool(passed)})
 check('Exact whole-source entity SHA256/bytes/pages',hashlib.sha256(data).hexdigest()==source['sha256'] and len(data)==source['bytes'] and len(pypdf.PdfReader(a.pdf).pages)==source['physical_pages'])
 for x in pins['selected_page_pins']:
  raw=(a.ocr_dir/('AEA1130-p'+str(x['physical_page'])+'.txt')).read_bytes();lines=raw.decode().splitlines();texts[x['physical_page']]=lines
  check('Physical'+str(x['physical_page'])+' visibleOCR hash/line count',hashlib.sha256(raw).hexdigest()==x['visible_ocr_sha256'] and len(lines)==x['ocr_lines'])
 check('Exact sixteen-image scope and221unread',sorted(texts)==pins['actual_images_read'] and len(texts)==16 and source['physical_pages']-len(texts)==pins['unread_pages']==221)
 anchors=[(1,2,6,['UAL','1303','DESTROY','March 11, 2004']),
 (3,24,28,['Voice Recordings','8020-3','Personnel Statements','Weather Products','Stored Flight Plan']),
 (48,7,21,['Full Transcript','May 8, 2002','1235','1307:58']),
 (49,4,16,['Page 2 of 23','certify','UAL175']),
 (55,20,22,['1244:58','ZBW IGN','1244:59','R42']),
 (107,17,26,['Full Transcript','May 2, 2002','1248','1317']),
 (120,5,5,['Page 14 of 29']),
 (148,17,26,['February 4, 2002','1230','1344']),
 (177,11,23,['May 2, 2002','1245','1316']),
 (178,5,5,['Page 2 of 9']),
 (180,4,4,['Page 3 of 9']),
 (186,17,29,['January 17, 2002','1078','1255','1316']),
 (186,39,40,['certify','UAL175']),
 (186,54,54,['1300:41','AD1']),
 (187,5,5,['Page 2 of 5']),
 (190,3,37,['Page 5 of 5','1310:14','1316','best','interpretation','End of Transcript'])]
 for page,lo,hi,needles in anchors:
  text=' '.join(texts[page][lo-1:hi]);check('Physical'+str(page)+' safe field anchors at'+str(lo)+'-'+str(hi),all(n in text for n in needles))
 check('Fourteen selected observation locators exist',len(obs['rows'])==14 and all(r['physical_page'] in texts and 1<=r['visible_ocr_lines'][0]<=r['visible_ocr_lines'][1]<=len(texts[r['physical_page']]) for r in obs['rows']))
 mutated=bytearray(data);mutated[len(mutated)//2]^=1
 check('One-byte source mutation rejected',hashlib.sha256(mutated).hexdigest()!=source['sha256'])
 result={'runtime':{'python':sys.version.split()[0],'pypdf':pypdf.__version__},'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'scope':'One released source entity; sixteen image/OCR inputs and selected safe field/locator integrity. No public speech/personnel/signature data. No PDF text-layer extraction.','limits':'Passing does not prove original-record completeness, interpretation, source-clock accuracy, signing, delivery, which version controls, change date/cause, intent, actual destruction or source independence.'}
 print(json.dumps(result,indent=2));return int(result['failed']>0)
if __name__=='__main__':sys.exit(main())
