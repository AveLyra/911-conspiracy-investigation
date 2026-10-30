#!/usr/bin/env python3
"""Read-only public catalogue verification; no private sources or network required."""
from pathlib import Path
import hashlib,json,re,sys

P=Path(__file__).resolve().parents[1]
meta=json.loads((P/'PUBLICATION.json').read_text())
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
master=json.loads((P/'data/master-leads.json').read_text())['entries']
findings=json.loads((P/'data/source-findings.json').read_text())['findings']
documentary=json.loads((P/'data/documentary-units.json').read_text())['records']
sets={'MASTER-LEADS.md':{f'm{x:03}' for x in range(1,176)},'SOURCE-FINDINGS.md':{x['id'].lower() for x in findings},'EARLIER-CHAT-AUDIT.md':{f'early-{x:02}' for x in range(1,12)},'DOCUMENTARY-CLAIMS.md':{f'documentary-b{x:03}' for x in range(1,234)}|{f'documentary-h{x:03}' for x in range(1,15)},'CONSOLIDATED-AND-RECENT.md':{f'consolidated-{x:02}' for x in range(1,50)}|{f'recent-{x:02}' for x in range(1,14)},'HISTORICAL-CONTEXT.md':{f'historical-{x:02}' for x in range(15,66) if x not in [16,25]}}
sets['MASTER-LEADS.md']|={f'master-family-{x}' for x in range(1,15)}
sets['SOURCE-FINDINGS.md']|={'family-'+re.sub(r'\d','',x['id']).lower() for x in findings}
check('exact175 master research IDs',len(master)==175 and {x['id'] for x in master}=={f'M{x:03}' for x in range(1,176)})
check('370 unique source IDs',len(findings)==370 and len({x['id'] for x in findings})==370)
check('247 original documentary IDs',len(documentary)==247 and {x['id'] for x in documentary}=={f'B{x:03}' for x in range(1,234)}|{f'H{x:03}' for x in range(1,15)})
for name,ids in sets.items():
    actual=set(re.findall(r'<a id="([^"]+)"', (P/name).read_text()))
    check('exact annotation IDs '+name,actual==ids)
check('44 source report bodies',len(set(re.findall(r'<a id="unit-[^"]+"',(P/'LATEST-SOURCE-UNITS.md').read_text())))==44)
for ident in ['fa044','pl022','pl023','pl024','pl025','nr068','nr069','nr070','nr071','nr072','pl026','pl027','nr073','pl028','pl029']:
    text=(P/'SOURCE-FINDINGS.md').read_text().split(f'<a id="{ident}"></a>',1)[1].split('<a id=',1)[0]
    check('addition observation contrary and TODO '+ident,all(word in text for word in ['**Context / contrary evidence:**','**Open TODO:**','**Citations:**']))
for i in range(1,12):
    block=(P/'EARLIER-CHAT-AUDIT.md').read_text().split(f'<a id="early-{i:02}"></a>',1)[1].split('<a id=',1)[0]
    check('recovered context contrary and TODO '+str(i),'**Context / contrary evidence:**' in block and '**Open TODO:**' in block)
for row in documentary:check('documentary prior verdict not adopted '+row['id'],'prior verdict not accepted' in row['assessment_status'])
text=(P/'LATEST-SOURCE-UNITS.md').read_text()
check('current method publication distinguished from dated local-only state','## Publication status reconciliation' in text and 'b30daf0f664b8688b18dea4fa08587a12dbefa97' in text and 'independent decoder validation' in text)
check('unperformed same-content tests remain open','Re-encoding can change bytes' in text and 'waveform alignment' in text and 'Open TODO' in text)
check('FAA preservation source clocks and qualifications retained',all(v in text for v in ['110000 UTC to 120400 UTC','2000 - 2400 local','0000 - 2400 local','09/14/2001 01:00 PM','header zone unverified','not independent witnesses','documented deviation','withdrawal/amendment']))
check('FAA handoff and verified publication states distinguished','## Update 051 publication verified after handoff' in text and 'handoff-time status' in text and '45ee3925dc1edd3137cf85182570bfc8440afcac' in text)
check('FAA052 conditional labels matching control and no sum',all(v in text for v in ['1230–1331 and 1331–1340','1230–1344','1245–1314','1245–1316','1255–1315','1255–1316','1232–1259','4, 2, 1 and 0 minutes','matching Boston pair','Do not sum','Unique tape/channel IDs']))
check('FAA052 actual reading routing and instruments remain qualified',all(v in text for v in ['1,2,3,4,8,15,16,26','eighteen pages remain unread','AAT-20','AAT-200','partly occluded footer','underlying instruments','corrected May2003','62a102da31cc82a7216dc41e60bed185a11c8d45']))
check('FAA053 candidate and all distinct fields preserved',all(v in text for v in ['TMU commercial line1078','1255–1316 UTC','not the initially sought Operations Manager1230–1344','Fill Transcript','Full Transcript','AAL11','ZBW-ARTCC-148','UAL175_R42_memo.doc','1300:41','09/27/2001','D:20051222232254','D:20131106161605']))
check('FAA053 sparse dialogue and search limits remain open',all(v in text for v in ['does not prove missing speech','pertaining to the subject accident','no correct flight label is selected','title-only/unopened','NOM audio remains metadata-only/unmapped','0584407dac2190a9f9514ee157124446e60672d5']))
check('FAA054 memo acquired dialogue and media remain open',all(v in text for v in ['Previously title-only AWA940','31,742 bytes','OMIC1230–1344','UAL175_MEMO.doc','ZNY-ARTCC-148','February 4, 2002','09/25/2001','need not contain the transcript body','No missing speech, trimming or measured gap']))
check('FAA054 roles matching control and unopened corrections preserved',all(v in text for v in ['ZNY OMIC and CC-NOM separately','not timestamped communications','subject and work-file aircraft labels both say UAL175','neither corrects AWA937','Title-only/unopened NARA7598362','companion7598360','not a proven replacement relationship or the May2003 QFR correction','191c27f34284bdbbf006db5bb2b41071125f19d7']))
check('FAA055 all33 rows acquisition and different correction stages retained',all(v in text for v in ['Previously title-only AEA1124','AEA1122/NARA7598360 are now acquired','All33 visible requests/queries','F01–F29','M01–M04','separate evidentiary stages','conditional release are distinct','608171664400ed8d1e95f70277ea994702a3cbd7']))
check('FAA055 disputed values contrary evidence and native tests stay open',all(v in text for v in ['1301:06/1301:05','1305:34/1305:33','ZBW IGN at1306:17','contrary original/remaining-copy response','contrary evidence to assuming every change was concealed','UAL175 9-11-01.doc','UAL175 Change 2.doc','do not infer twenty deleted pages','AEA1121/NARA7598359','AEA1123/NARA7598361','Actual May2003 draft/corrected QFR/receipt']))
check('FAA056 acquired entities and exact publication',all(v in text for v in ['AEA1121/NARA7598359 and AEA1123/NARA7598361 are now acquired','464,135 bytes','190,274 bytes','a42d0956202dacc3b971d21f479966d56fefcd60']))
check('FAA056 missing page dispatch and receipt distinct',all(v in text for v in ['page 2 of the 23-page','two copies enclosed','not in the acquired three-page scan','Friday as certified','5/14/02','actual receipt and approval','Native filenames']))
check('FAA056 timestamp pairs not measured clocks',all(v in text for v in ['1245:58/1245:59','1244:58/1244:59','1302:00/1302:02','1302:04/1302:06','−60, −60, +4, +4 seconds','not measured hardware-clock offsets','1301:37/1301:35','1311:06 following 1311:09']))
check('FAA056 contrary source explanations attributed',all(v in text for v in ['both correct or no change','not independently verified equipment behavior','radio/landline coordination','channel-specific reception','1258:18','1305:22/1310:46']))
check('FAA056 version and line1078 distinctions preserved',all(v in text for v in ['28 pages for the fourth/associate55','page 19 placed after page 9','four Correction made annotations','five-page Ninth','Eighth nine-page','does not authenticate the two-page AWA937','not independent corroboration']))
check('FAA056 selected ledger and count limits preserved',all(v in text for v in ['30 selected FIELD-LEDGER observations V01–V30','135 numbered transcript-review items','19+26+24+41+6+7+7+5','not 135 independent errors or events','Prior update055’s 33 rows']))
check('FAA056 policy originals copies and acceptance gaps preserved',all(v in text for v in ['from copies of Form8020-3','not destruction of the original','2000 FAA Order8020.11B','2003 Change 1','not newly read here','72c(11)/77d(4)','May 2003 QFR drafting/correction/delivery','five tracks/eighteen substantive criteria remain incomplete/partial','not a new independent twelve-page image review']))
pattern=re.compile(r'\]\((?:<([^>]+)>|([^\)\n]+))\)');broken=[];links=0
for f in P.glob('*.md'):
    for angled,plain in pattern.findall(f.read_text()):
        value=angled or plain
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',value):continue
        links+=1;name,_,anchor=value.partition('#');target=f.parent/name if name else f
        if value.startswith('/') or not target.is_file():broken.append([f.name,value,'missing or absolute target']);continue
        if anchor and f'id="{anchor}"' not in target.read_text():broken.append([f.name,value,'missing stable anchor'])
check('all local public reader links',not broken)
private=re.compile(r'(?i:\bRule\s*26\b|\bVaughn\b|\bCORR-\d|\bSRC-\d|@gmail\.com|@proton\.(?:me|mail\.com)|case-management|\.eml\b|drive\.google\.com|docs\.google\.com)|(?<![A-Za-z])/Users/|/Volumes/|/private/var/|/var/folders/|-----BEGIN [A-Z ]*PRIVATE KEY-----')
privacy=[]
for f in list(P.glob('*.md'))+list((P/'data').glob('*.json')):
    if private.search(f.read_text()):privacy.append(str(f.relative_to(P)))
check('private case correspondence credential and locator exclusions',not privacy)
check('no symlinks',not any(f.is_symlink() for f in P.rglob('*')))
listed={r['path'] for r in meta['files']}
actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name!='PUBLICATION.json' and '__pycache__' not in f.parts}
check('complete unique public payload inventory',listed==actual and len(listed)==len(meta['files']))
for row in meta['files']:
    f=P/row['path'];check('public payload bytes '+row['path'],f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'])
result={'status':'passed' if all(c['passed'] for c in checks) else 'failed','passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'local_reader_links':links,'broken_links':broken,'privacy_matches':privacy,'failures':[c['name'] for c in checks if not c['passed']],'source_or_causal_validation':False}
print(json.dumps(result,indent=2));sys.exit(0 if result['status']=='passed' else 1)
