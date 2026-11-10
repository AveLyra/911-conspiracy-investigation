"""Verify pinned PDFs and limited textual anchors; no historical or physical authentication."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import pypdf

def compact(text):
    return re.sub(r"\s+", "", text)

def verify(pins, supplied):
    entities=[]
    readers={}
    for row in pins:
        path=supplied[row['id']]
        data=path.read_bytes()
        reader=pypdf.PdfReader(path)
        ok=(data.startswith(b'%PDF-') and len(data)==row['bytes']
            and hashlib.sha256(data).hexdigest()==row['sha256']
            and len(reader.pages)==row['pages'])
        entities.append({'id':row['id'],'bytes':len(data),'pages':len(reader.pages),
                         'sha256':hashlib.sha256(data).hexdigest(),'passed':ok})
        readers[row['id']]=reader
    def text(source,page):
        return compact(readers[source].pages[page-1].extract_text() or '')
    checks=[
        ('H1-agreement', 'inApril2005' in text('H1',3)),
        ('H1-photography-range', 'betweenJune2004andMarch2005' in text('H1',4)),
        ('H2-visible-labels', 'HAERNY-6369-A' in text('H2',1) and 'HABSNY-6369-A' in text('H2',2)),
        ('H2-column-details', all(x in text('H2',2) for x in ['heatblisteredpaintoncolumnJ3/10,LevelB2','columnJ4/12atLevelB2','smokedamageatdroppanel'])),
        ('H3-parent-column-details', all(x in text('H3',3) for x in ['NY-6369-31','NY-6369-29','columnJ3/10.LevelB2','columnJ4/12atlevelB2'])),
        ('H3-specific-earlier-date', 'September17,2001' in text('H3',1) and 'June2004' in text('H3',1)),
    ]
    return {'entity_checks':entities,'source_anchor_checks':[{'id':name,'passed':ok} for name,ok in checks],
            'all_passed':all(r['passed'] for r in entities) and all(ok for _,ok in checks),
            'pypdf_version':pypdf.__version__,
            'scope':'PDF byte/page identity and limited text anchors. Whitespace removed only for check navigation; originals and extraction representations preserved. Manual page-image reading is separate.',
            'not_performed':['photograph/negative identity comparison','actual SHPO submission/receipt match','transport-object/specimen custody join','temperature/calibration test','historical cause or intent test'],
            'candidate_caption_pairs':2,'authenticated_photo_pairs':0,'specimen_joins_established':0}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',action='append',required=True,help='H1=path, H2=path, H3=path')
    args=parser.parse_args()
    supplied=dict(item.split('=',1) for item in args.input)
    assert set(supplied)=={'H1','H2','H3'}
    supplied={key:Path(path) for key,path in supplied.items()}
    pins=json.loads((Path(__file__).parent/'SOURCE-PINS.json').read_text())
    result=verify(pins,supplied)
    print(json.dumps(result,indent=2))
    if not result['all_passed']:
        raise SystemExit(1)

if __name__=='__main__':
    main()
