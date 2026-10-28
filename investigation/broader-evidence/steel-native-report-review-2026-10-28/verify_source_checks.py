"""Documentary checks only: run with V1.pdf V2.pdf I3B.pdf as three arguments.
Requires an already installed PyMuPDF; does not install or acquire sources.
Prints JSON to stdout. Does not modify any source or resolve historical causes.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import sys
import fitz

root = Path(__file__).resolve().parent
docs = {}
checks = []


def check(name, condition):
    checks.append({'check': name, 'passed': bool(condition)})
    assert condition, name


def norm(text):
    return re.sub(r'\s+', '', text).lower()


expected = [('V1', 340, 41360840, '2a5f7edf120d98c7e15a77d7aa1768c6a14cbdde198e622fd70402a499767124'),
            ('V2', 262, 38512189, 'f580a1921fb45bb6d578715ac40ce00088e095b3de3dd4ea5d21d8216fd02d85'),
            ('I3B', 114, 12034476, 'd234d025912dab100a0dd479f826b2adff0fc23acd5acb42efc93a4a8bcd9bc3')]
assert len(sys.argv) == 4, 'Supply the three original PDFs in V1,V2,I3B order.'
for (key, pages, size, sha), arg in zip(expected, sys.argv[1:]):
    data = Path(arg).read_bytes()
    check(key + ' source byte count', len(data) == size)
    check(key + ' source SHA-256', hashlib.sha256(data).hexdigest() == sha)
    docs[key] = fitz.open(stream=data, filetype='pdf')
    check(key + ' physical page count', len(docs[key]) == pages)


def phrase(key, page, text, label):
    check(label, norm(text) in norm(docs[key][page - 1].get_text()))


phrase('V1',296,'WTC 7 steel was not evaluated','Tower-study scope statement at physical296')
phrase('V1',296,'xliii','Printed executive-summary label, not a guessed page offset')
for page, label in [(3,'286'),(4,'285'),(71,'218')]:
    page_obj = docs['V1'][page-1]
    footer_words = [w[4] for w in page_obj.get_text('words') if w[1] > .94 * page_obj.rect.height]
    check('V1 selected numeric footer ' + str(page), label in footer_words)
phrase('V2',173,'SB1341-03-Q-0155','Published WJE order number')
phrase('V2',173,'26 November 2003','Published WJE date label')
phrase('V2',173,'2003.0323.0','Published WJE project number')
phrase('V2',178,'NIST NCSTAR 1-3B (2005)','2005 reference in dated report')
phrase('V2',178,'hand written field notes','Underlying handwritten-note reference')
phrase('V2',178,'all 236 pieces were observed','General coverage statement')
phrase('V2',178,'not possible to make detailed observations on all 236','Detailed coverage limitation')
phrase('V2',184,'surveyed six pieces','Other-structure denominator')
phrase('V2',184,'Over half of the surveyed pieces','Aggregate fire statement preserved')
phrase('V2',241,'not visually assessed for fire effects','C72 unassessed state')
phrase('V2',242,'No distinct indications of fire effects','C78 distinct-indication state')
phrase('V2',243,'Did not visually assess for fire effects','C85 unassessed state')
for page in [239,240,244]:
    phrase('V2',page,'Fire effects','Positive-labelled worksheet physical' + str(page))
phrase('V2',252,'WJE observed eight panels','Eight-panel source statement')
phrase('V2',254,'nine exterior panels and one core column','Nine-panel source statement')
phrase('V2',258,'seven panels where pre-collapse fires were observable','Seven-panel source statement')
phrase('V2',258,'16 continuous minutes','M2 exposure-duration source statement')
phrase('V2',258,'250','Possible-degradation threshold retained as source explanation')
phrase('I3B',87,'C-31 or S-7','Inventory alias source')
phrase('I3B',87,'676','Inventory marking text exists; column role requires image check')
phrase('I3B',88,'C-42','Inventory C42 source')
for name in ['C-72b','C-78','M-11']:
    phrase('I3B',96,name,'Bounded TableA7 membership ' + name)
phrase('I3B',96,'C;85','Actual text-layer C;85 retained; visual C-85 reading is separate')
text_a7 = norm(docs['I3B'][95].get_text())
check('C31 and C42 absent from bounded TableA7 page only', 'c-31' not in text_a7 and 'c-42' not in text_a7)

panels = json.loads((root / 'PANEL-COUNT-COMPARISON.json').read_text())
summary = panels['summary']['panels']
detailed = panels['detailed_review']['panels']
source_detail = '\n'.join(docs['V2'][p-1].get_text() for p in range(254,258))
extracted = re.findall(r'Panel\s+([A-Z]-\d+)',source_detail)
check('Detailed panel headings reproduce nine saved labels', extracted == detailed)
check('Saved summary list contains eight distinct labels', len(summary) == len(set(summary)) == 8)
summary_text = norm(docs['V2'][251].get_text())
check('Saved eight labels occur in summary source', all(norm(x) in summary_text for x in summary))
check('Saved set difference is K1', sorted(set(detailed)-set(summary)) == ['K-1'])

rows = list(csv.DictReader(io.StringIO((root/'OTHER-STRUCTURE-WORKSHEETS.csv').read_text())))
check('Six unique worksheet pages239–244', [int(r['physical_pdf_page_V2']) for r in rows] == list(range(239,245)))
positive = sum(r['fire_assessment_paraphrase'] in ['fire-effects indication','probable fire effects'] for r in rows)
unassessed = sum(r['fire_assessment_paraphrase'] == 'not visually assessed for fire effects' for r in rows)
no_distinct = sum(r['fire_assessment_paraphrase'] == 'no distinct indications of fire effects' for r in rows)
check('Worksheet accounting retains3positive1no-distinct2unassessed', (positive,no_distinct,unassessed) == (3,1,2))
check('Three of six is not over half; no preferred account selected', positive / len(rows) == .5)
lines = (root/'SELECTED-READINGS.md').read_text().splitlines()
locators = json.loads((root/'CLAIM-LOCATORS.json').read_text())
check('All15 exact selected-reading line references', len(locators)==15 and all(lines[r['line']-1].startswith('- '+r['id']+' ') for r in locators))
print(json.dumps({'result': 'PASS', 'checks': checks, 'check_count': len(checks),
                  'software': {'python': sys.version.split()[0], 'pymupdf': fitz.VersionBind},
                  'scope': 'Byte, page, phrase, list and arithmetic checks. Visual column geometry and qualitative readings are separately recorded; historical validity, building origins and scientific calibration are not established.'}, indent=2))
