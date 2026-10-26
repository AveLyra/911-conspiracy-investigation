"""Finite inventory/preservation checks; no claim of historical validation.

Runs without downloading anything. Optional --receipt writes a NEW receipt.
"""
from pathlib import Path
from collections import Counter
import datetime,hashlib,json,re,sys

R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(n):return json.loads((R/n).read_text())
def check(c,msg):
    if not c:raise AssertionError(msg)

def verify():
    d=read('claim-crosswalk-v2.json');records=d['records']
    check(d['baseline_commit']=='ddd475b4e3c43a92a713426b6dc4c9f350930abd','Frozen M baseline')
    check(len(records)==len({x['id'] for x in records})==247,'All247unique units')
    check(Counter(x['unit_kind'] for x in records)=={'film-or-lead-table-row-with-assessment':188,'assessment-prose-or-methodological-proposal':59},'188rows59prose')
    check(Counter(x['coverage'] for x in records)=={'outside existing register':207,'partly covered':38,'already covered':2},'Exact scope classifications')
    count=0
    for file,account in d['line_accountability'].items():
        lines=(R/file).read_text().splitlines()
        check(sha(R/file)==d['source_hashes'][file],'Assessment source bytes unchanged')
        check([x['line'] for x in account]==list(range(1,len(lines)+1)),'Every original text line accounted')
        for x in records:
            if x['source_file']!=file:continue
            a,b=x['source_line_start'],x['source_line_end']
            check('\n'.join(lines[a-1:b])==x['exact_original_wording'],'Exact original wording '+x['id'])
            check(x['assessment_status']=='CLAIM TO TEST; prior verdict not accepted','No inherited verdict')
            check(not x['film_attribution']['attribution_verified'],'No invented edition/timestamp certification')
            last=0
            for s in x['subclaim_text_spans']:
                left,right=s['character_span'];check(left==last and right>left,'Contiguous text spans')
                check(x['exact_original_wording'][left:right]==s['exact_wording'],'Exact child wording')
                last=right;count+=1
            check(last==len(x['exact_original_wording']),'No child tail dropped')
            check(all(re.fullmatch(r'M(?:00[1-9]|0[1-9][0-9]|1[0-2][0-9]|13[0-4])',m) for m in x['matching_M_ids']),'M-IDs valid')
    check(count==619,'619lossless spans')
    byid={x['id']:x for x in records}
    check(byid['H005']['matching_M_ids'] and not byid['H006']['matching_M_ids'] and byid['H007']['matching_M_ids']==['M113','M114'],'Reviewed highlight cross-references')
    check(byid['B118']['source_line_start']==201 and 'landlord' in byid['B118']['subject'],'Exact landlord target')
    findings=read('source-findings-v2.json')['findings']
    check(len(findings)==14 and len({x['id'] for x in findings})==14,'14source findings')
    for f in findings:
        check(all(i in byid for i in f['assessment_links']),'Source-to-inventory parent link')
        for k in ['checked_claim','source_url','exact_locators','contrary_evidence_and_limits','missing_records','smallest_discriminating_step','actually_inspected','hypotheses_bearing']:check(bool(f[k]),'Bounded source-field '+k)
    for f in findings:
        if f['id'] in ['S004','S005','S006']:check(f['assessment_links']==['B118'],'Landlord linked to landlord claim')
    comp=read('source-version-comparison-v3.json')
    check(len(comp['comparison'])==17 and comp['every_tested_page_component_equal'],'Exact tested representation match')
    check(all(all(p[k] for k in ['content_equal','images_equal','pixels_equal','boxes_equal']) for p in comp['comparison']),'All page comparisons')
    check(comp['representations'][0]['sha256']!=comp['representations'][1]['sha256'],'Whole-file conflict preserved')
    check(comp['catalog_November2013_present'],'Catalog date retained')
    check(read('source-findings-v2.json')['source_scope']['original_bank_records_acquired']==0,'No invented raw bank acquisition')
    manifest=read('MANIFEST.json')
    for name,row in manifest['files'].items():
        p=R/name;check(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact payload '+name)
        if p.suffix in ['.md','.json','.py','.diff']:
            text=p.read_text();check(not re.search(r'/(?:Users|Volumes|private|var)/',text),'No local operational paths '+name)
            check(not re.search(r'(?im)^\s*(?:Set-Cookie:|Authorization:\s*Bearer|-----BEGIN [A-Z ]*PRIVATE KEY)',text),'No raw session/credential material '+name)
    for p in R.glob('*.py'):compile(p.read_text(),str(p),'exec')
    for n in ['README.md','SAUDI-FBI-REVIEW-v2.md','NEXT-RECORDS-v1.md']:
        for target in re.findall(r'\]\(([^)]+)\)',(R/n).read_text()):
            if target.startswith(('http:','https:','#')):continue
            check((R/target.split('#',1)[0]).exists(),'Local publication link '+target)
    return dict(status='PASS: finite inventory, preservation and publication-payload checks',units=247,table_rows=188,prose_or_methodological_units=59,lossless_child_spans=619,source_findings=14,
                film_editions_or_every_historical_claim_verified=False,original_bank_interview_records_acquired=0,
                raw_sources_repaired=False,scope='Integrity/coverage and bounded stated source checks; not historical cause, current appellate status, complete film concordance or validation of every assessment verdict.')

if __name__=='__main__':
    result=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),verifier_sha256=sha(Path(__file__)))
    result.update(verify())
    if '--receipt' in sys.argv:
        with (R/sys.argv[sys.argv.index('--receipt')+1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
