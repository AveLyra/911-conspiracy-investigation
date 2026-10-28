"""Run with V1.pdf V2.pdf I3B.pdf; documentary and explicit-set checks only.
Manual visual readings/row grouping are recorded inputs, not automated native-data decoding.
"""
from pathlib import Path
import csv,hashlib,io,json,re,sys
import fitz
root=Path(__file__).resolve().parent
checks=[]
def check(name,condition):
    checks.append({'check':name,'passed':bool(condition)})
    assert condition,name
def norm(s):return re.sub(r'\s+','',s).lower()
assert len(sys.argv)==4
docs={}
for source,path in zip(json.loads((root/'SOURCES.json').read_text()),sys.argv[1:]):
    data=Path(path).read_bytes();check(source['id']+' original SHA256',hashlib.sha256(data).hexdigest()==source['sha256'])
    docs[source['id']]=fitz.open(stream=data,filetype='pdf');check(source['id']+' physical pages',len(docs[source['id']])==source['physical_pages'])
def phrase(key,page,words,name):check(name,norm(words) in norm(docs[key][page-1].get_text()))
phrase('V1',71,'C-l 1 and M-14, both unidentified','Main selection text retains M14 and unidentified label')
phrase('V1',71,'two samples from WTC 2','Main selection text identifies WTC2 samples')
phrase('V1',71,'M-lOa and M-lOb','Literal extracted label string; visible M10a/M10b read separately')
phrase('V1',71,'21 panels selected','Main text total21')
phrase('V2',177,'non-binding technical review','Published scope non-binding qualification')
phrase('V2',236,'Piece ID Mark: M-4','WJE worksheet identifier')
phrase('V2',257,'Panel M-4 (unidentified)','NIST review M4 label')
phrase('I3B',91,'M-4 or M-5','Inventory M4/M5 alias')
phrase('I3B',93,'N-13 or M-14','Inventory N13/M14 alias')
e1_text=''.join(docs['V2'][p-1].get_text() for p in range(164,171))
check('Visible-label negative control: E1 extraction misses M4', 'm-4' not in norm(e1_text))
rows=list(csv.DictReader(io.StringIO((root/'TABLE-E1-GROUP-INDEX.csv').read_text())))
check('Manual group index has25distinctlabels',len(rows)==len({r['sample_label'] for r in rows})==25)
ext={r['sample_label'] for r in rows if r['group_type']=='exterior'}
core={r['sample_label'] for r in rows if r['group_type']=='core'}
check('Manual group classification21exterior4core',len(ext)==21 and len(core)==4)
check('Source-count arithmetic, not identity validation',16+2+3==len(ext))
check('Bounded index contains M4 not M14','M-4' in ext and 'M-14' not in ext)
check('Source table pages164through170covered',{int(r['physical_V2_page']) for r in rows}==set(range(164,171)))
working=json.loads((root/'CANDIDATE-SEVEN-WORKING-LIST.json').read_text())
fire={r['sample_label'] for r in rows if r['group_type']=='exterior' and r['table_fire_exposure_category']=='observed'}
candidate=sorted(fire-set(working['G3_nine_panel_list']))
check('Conditional set rule exactly reproduced',candidate==working['candidate_panels'])
check('Candidate count7 and exact IDs',candidate==['C-22','C-40','C-55','C-93','M-2','M-26','N-7'])
check('Candidate assumptions and nonauthentication retained',len(working['assumptions'])==3 and 'not the recovered authored' in working['classification'])
check('Different source-list sensitivity changes derived output', sorted(fire-(set(working['G3_nine_panel_list'])|{'C-22'}))!=candidate)
conflicts=json.loads((root/'CONFLICTS.json').read_text())
check('Three separately preserved conflict records',[c['id'] for c in conflicts]==['ID01','ID02','ID03'])
check('ID03 both column values kept', 'Column206' in conflicts[2]['observations'][0]['value'] and 'Column209' in conflicts[2]['observations'][1]['value'])
check('Final checklist covers additional ID03','ID03' in (root/'CHECKLIST-SUPPLEMENT.md').read_text())
reading=(root/'SELECTED-READINGS.md').read_text().splitlines();loc=json.loads((root/'CLAIM-LOCATORS.json').read_text())
check('Exact selected-reading line references',len(loc)==9 and all(reading[r['line']-1].startswith('- '+r['id']+' ') for r in loc))
scope=json.loads((root/'READING-SCOPE.json').read_text())
check('Reading scope13unique pages2details',scope['distinct_full_pages_read']==13 and scope['extra_details_read']==2 and len(scope['images'])==15)
sensitivity=json.loads((root/'CANDIDATE-SENSITIVITY.json').read_text())
g2=sensitivity['G2_summary_eight']
check('G2alternative8panel source labels retained',len(g2)==8 and all(norm(x) in norm(docs['V2'][251].get_text()) for x in g2))
check('Alternative source-list rule gives8includingK1',sorted(fire-set(g2))==sensitivity['alternative_same_set_rule_using_G2'] and len(fire-set(g2))==8 and 'K-1' in fire-set(g2))
check('Actual G2/G3 input difference is K1',set(working['G3_nine_panel_list'])-set(g2)=={'K-1'})
print(json.dumps({'result':'PASS','check_count':len(checks),'checks':checks,'software':{'python':sys.version.split()[0],'pymupdf':fitz.VersionBind},'scope':'Source-byte/page/phrase and manual-index/set/qualification checks. Visual cells were read separately. No native operational record acquisition, independent measurement, historical specimen authentication, temperature/collapse validation or adjudication.'},indent=2))
