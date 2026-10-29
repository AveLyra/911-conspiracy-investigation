#!/usr/bin/env python3
"""Source entity/header checks and accounting of supplied image transcriptions."""
import argparse,hashlib,json,re,sys
from pathlib import Path
import pypdf
from pypdf import PdfReader
P=argparse.ArgumentParser();P.add_argument('--agenda',required=True);P.add_argument('--binder',required=True);P.add_argument('--prior-minutes',required=True);a=P.parse_args()
b=Path(__file__).parent;s=json.loads((b/'SOURCES.json').read_text());checks=[];pdf={}
def ck(name,condition,kind):
 checks.append({'check':name,'passed':bool(condition),'kind':kind})
 if not condition:raise AssertionError(name)
def compact(x):return re.sub(r'\s+','',x).casefold()
for key,path in [('AGENDA',a.agenda),('BINDER',a.binder),('PRIOR-MINUTES',a.prior_minutes)]:
 data=Path(path).read_bytes();q=s[key]
 ck(key+' SHA256',hashlib.sha256(data).hexdigest()==q['sha256'],'entity')
 ck(key+' bytes',len(data)==q['bytes'],'entity')
 pdf[key]=PdfReader(path);ck(key+' pages',len(pdf[key].pages)==q['pages'],'entity')
for page in range(64,67):
 t=compact(pdf['AGENDA'].pages[page-1].extract_text() or '')
 ck('Letter attachment marker p'+str(page),'attachmentnumber1' in t and 'page'+str(page-63)+'of3' in t,'exposed-header-only')
for page in range(67,78):
 t=compact(pdf['AGENDA'].pages[page-1].extract_text() or '')
 ck('Court attachment header p'+str(page),'document1509' in t and '07/22/2010' in t and 'page'+str(page-66)+'of11' in t,'exposed-header-only')
for page,num in [(10,1),(19,10),(20,11),(21,12)]:
 t=compact(pdf['BINDER'].pages[page-1].extract_text() or '')
 ck('Retained minute wrapper p'+str(page),'attachmentnumber1' in t and 'page'+str(num)+'of21' in t,'exposed-header-only')
t=compact(pdf['PRIOR-MINUTES'].pages[3].extract_text() or '')
ck('Prior conditional cutting wording','becutintotwopiecesifrequested' in t,'extracted-text-anchor')
ck('Prior indemnity wording','holdsneither' in t,'extracted-text-anchor')
manual=json.loads((b/'NIST-LABELS.json').read_text());rows=manual['rows'];fromcollections=None
ck('Supplied label count',len(rows)==104,'supplied-transcription-accounting')
ck('Supplied label uniqueness',len({r['identifier'] for r in rows})==104,'supplied-transcription-accounting')
ck('Supplied page76 labels',sum(r['physical_page']==76 for r in rows)==61,'supplied-transcription-accounting')
ck('Supplied page77 labels',sum(r['physical_page']==77 for r in rows)==43,'supplied-transcription-accounting')
obs=json.loads((b/'OBSERVATIONS.json').read_text());dup=next(x for x in obs if x['id']=='CW-A06')['rows']
ck('Duplicate observations retained',len(dup)==2 and [x['id'] for x in dup]==['G-0086','G-0086'],'supplied-transcription-accounting')
result={'method':'Three entity and page counts, PDF-exposed header/anchor tests and counts of supplied manual observations; no body OCR or independent glyph validation.',
 'runtime':{'python':sys.version.split()[0],'pypdf':pypdf.__version__},'checks':checks,'passed':len(checks),
 'label_accounting':{'rows':104,'unique_supplied_labels':104,'by_page':{'76':61,'77':43},'complete_list_total':'not counted','physical_piece_count':'not established','nativeNIST236_or_W14_C12_join':False},
 'states_preserved':{'unsigned_letter':True,'draft_unapproved_minutes':True,'staff_letter_wording_difference_unresolved':True,'alternative_order_assembly_unresolved':True,'actualexecution_receipt_cutting_unverified':True},
 'limits':'Passes do not authenticate authoring, signatures, approved status, actual transfer, contract effect, specimen origin, image-transcription completeness, conspiracy or goal completion. Whitespace/case normalization is for exposed text checks only; source bytes and literal observations are unchanged.'}
print(json.dumps(result,indent=2))
