"""Check source entities and exact PDF anchors; do not authenticate steel origin.

Usage: python verify_candidate_control.py IMAGE_DIR FEMA_PDF NIST_PDF NEW_OUTPUT
Requires Pillow and pypdf. Images may be acquired from the anonymous public
URLs in IMAGE-SOURCES.json. Existing result files are refused.
"""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image
from pypdf import PdfReader

image_dir, fema, nist, output = map(Path, sys.argv[1:])
pins = [
    (image_dir/'C-13a Markings.jpg',955550,'ae556c181c7dc3e2cf7ea82b1d738dc5b85a741eef9089fa424dc731463453f9'),
    (image_dir/'C-13a OVERALL #1.jpg',531437,'332483b50a89baf5e4d4ed59a73758d186c49baef9a9dd787fa2c3d21320809c'),
    (fema,2333446,'e054a70f9410b1fe0b141f0ec2401244183f67da4d0a703df5ffb18483d6f6fc'),
    (nist,12034476,'d234d025912dab100a0dd479f826b2adff0fc23acd5acb42efc93a4a8bcd9bc3'),
]
result = {'scope':'Current entities and exact text locations only; visual readings separately logged.',
          'entities':[], 'images':[], 'pdf_pages':[], 'checks':[]}
for p, size, sha in pins:
    b=p.read_bytes()
    actual=hashlib.sha256(b).hexdigest()
    match=len(b)==size and actual==sha
    result['entities'].append(dict(filename=p.name,bytes=len(b),sha256=actual,pin_matches=match))
    result['checks'].append(dict(name=p.name+' entity',passed=match))
for filename, dimensions in [('C-13a Markings.jpg',(2272,1704)),('C-13a OVERALL #1.jpg',(1200,1600))]:
    with Image.open(image_dir/filename) as im:
        im.load()
        row=dict(filename=filename,format=im.format,width=im.width,height=im.height,
                 mode=im.mode,recognized_exif_entries=len(im.getexif()),
                 reading_limit='Zero recognized EXIF entries does not exclude all application or embedded metadata.')
        result['images'].append(row)
        result['checks'].append(dict(name=filename+' full raster decode/dimensions',passed=im.format=='JPEG' and im.size==dimensions))
for pdf, page, anchors in [
    (fema,16,['C12a','C12b','C13a','321 B200 92 90 3T <569>','1/25/02:#15-19']),
    (nist,87,['C-13aorS-19','B200;90-92','C-13orS-11'])
]:
    reader=PdfReader(pdf)
    text=reader.pages[page-1].extract_text()
    # The extraction is retained verbatim. Whitespace-only folding is used for
    # a bounded locator check, never to replace source wording or source values.
    folded=''.join(text.split())
    found={a:''.join(a.split()) in folded for a in anchors}
    result['pdf_pages'].append(dict(filename=pdf.name,page_count=len(reader.pages),physical_page=page,raw_extraction=text,anchors=found))
    result['checks'].append(dict(name=pdf.name+' selected extraction anchors',passed=all(found.values())))
result['passed']=sum(c['passed'] for c in result['checks'])
result['total']=len(result['checks'])
with output.open('x') as handle: json.dump(result,handle,indent=2)
print(json.dumps({'passed':result['passed'],'total':result['total'],'checks':result['checks']},indent=2))
if result['passed'] != result['total']: raise SystemExit(1)
