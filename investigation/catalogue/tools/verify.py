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
check('38 source report bodies',len(set(re.findall(r'<a id="unit-[^"]+"',(P/'LATEST-SOURCE-UNITS.md').read_text())))==38)
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
