"""Run with award.pdf VolumeII.pdf contracts-DOM.txt; print documentary checks.
No acquisition, installation, source changes or historical-performance validation.
"""
from pathlib import Path
import base64
import csv
import hashlib
import io
import json
import re
import sys
import fitz

root=Path(__file__).resolve().parent
public=root/'public-release'
if not public.exists():
    public=root
checks=[]


def check(name,value):
    checks.append({'check':name,'passed':bool(value)})
    assert value,name


def norm(s):
    return re.sub(r'\s+','',s).lower()


assert len(sys.argv)==4,'Supply award PDF, reused VolumeII PDF and recorded full DOM snapshot.'
data=Path(sys.argv[1]).read_bytes()
check('Archived award entity byte count',len(data)==151979)
check('Archived award entity SHA256',hashlib.sha256(data).hexdigest()=='500ba9d66cd2d4d953bce636424aebf38a3625e23dec6060e983783522171279')
pdf=fitz.open(stream=data,filetype='pdf')
check('Two acquired pages',len(pdf)==2)
sources=json.loads((public/'SOURCES.json').read_text())
index=sources['award_notice']['cdx_row']
check('Exact capture timestamp',index['timestamp']=='20120310003549')
check('Index PDF/status fields retained',index['mimetype']=='application/pdf' and index['statuscode']=='200')
digest=base64.b32encode(hashlib.sha1(data).digest()).decode().rstrip('=')
check('Actual entity SHA1/base32 matches CDXdigest',digest==index['digest']=='HWDULI2PZJSBTLL3Q3WKSPKOLDO753BB')
check('Indexlength preserved separately from body bytes',index['length']=='142769' and sources['award_notice']['bytes']==151979)
text=norm(pdf[0].get_text())
for label,anchor in [('Contract','SB1341-03-W-0313'),('Solicitation','Under solicitation number SB1341-03-Q-0155'),('Award date','6/9/2003'),('Review task5','Provide NIST with a technical review of NIST’s Draft Project 3 Report')]:
    check(label+' actual first-page anchor',norm(anchor) in text)
for n in range(1,6):
    check('Numbered task '+str(n),re.search(r'(?m)^'+str(n)+r'\.\s*',pdf[0].get_text()) is not None)
check('Award PDF creator/producer fields',pdf.metadata['creator']=='Microsoft® Word 2010' and pdf.metadata['producer']=='Microsoft® Word 2010')
check('Award PDF creation/modification labels',pdf.metadata['creationDate']==pdf.metadata['modDate']=="D:20110804094749-04'00'")
vol_data=Path(sys.argv[2]).read_bytes()
check('Reused VolumeII unchanged SHA256',hashlib.sha256(vol_data).hexdigest()=='f580a1921fb45bb6d578715ac40ce00088e095b3de3dd4ea5d21d8216fd02d85')
vol=fitz.open(stream=vol_data,filetype='pdf')
check('Reused VolumeII physical pages',len(vol)==262)
cover=norm(vol[172].get_text())
check('Report cover Q0155 and project0323 labels',norm('SB1341-03-Q-0155') in cover and norm('2003.0323.0') in cover)
check('Report cover date remains26November2003',norm('26 November 2003') in cover)
check('Published methodology2005reference retained',norm('NIST NCSTAR 1-3B (2005)') in norm(vol[177].get_text()))
dom=Path(sys.argv[3]).read_bytes()
check('Captured full DOM snapshot SHA256',hashlib.sha256(dom).hexdigest()==sources['contracts_page']['snapshot_sha256'])
lines=dom.decode().splitlines()
start=sources['contracts_page']['row_start_line']-1;end=sources['contracts_page']['row_end_line']
row='\n'.join(lines[start:end])+'\n'
check('Saved row exact original-line slice',row==(public/'CONTRACTS-WJE-ROW.txt').read_text())
check('Saved row hash',hashlib.sha256(row.encode()).hexdigest()==sources['contracts_page']['row_sha256'])
check('DOM row exact completion/date fields', '- cell "6/9/2003"' in row and '- cell "4/27/05"' in row)
check('DOM link is source award PDF',sources['award_notice']['cdx_row']['original'].replace('http:','https:') in row)
tasks=list(csv.DictReader(io.StringIO((public/'DELIVERABLE-CROSSWALK.csv').read_text())))
check('Five task rows retained separately',[x['award_notice_task_p1'] for x in tasks]==list('12345'))
check('Task5 is not claimed acquired','not acquired' in tasks[4]['still_required'])
reading=(public/'SELECTED-READINGS.md').read_text().splitlines()
locators=json.loads((public/'CLAIM-LOCATORS.json').read_text())
check('Seven exact selected-reading line references',len(locators)==7 and all(reading[r['line']-1].startswith('- '+r['id']+' ') for r in locators))
print(json.dumps({'result':'PASS','check_count':len(checks),'checks':checks,'software':{'python':sys.version.split()[0],'pymupdf':fitz.VersionBind},'selected_award_metadata':{k:pdf.metadata[k] for k in ['format','creator','producer','creationDate','modDate']},'scope':'Byte/page/metadata/phrase/list/DOM-source checks only. Both full-page images read separately; no historical date, contract performance, original review delivery, temperature calibration, steel origin or collapse cause validated.'},indent=2))
