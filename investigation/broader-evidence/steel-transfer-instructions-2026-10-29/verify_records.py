#!/usr/bin/env python3
"""Reproduce a documentary source-reference test; no historical adjudication."""
import argparse,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
P=argparse.ArgumentParser()
P.add_argument('--clearwater-pdf',required=True)
P.add_argument('--beverly-pdf',required=True)
a=P.parse_args();base=Path(__file__).parent
sources=json.loads((base/'SOURCES.json').read_text());checks=[];readers={}
def check(label,value):
 checks.append({'check':label,'passed':bool(value)})
 if not value:raise AssertionError(label)
for key,path in [('CW2010',a.clearwater_pdf),('BH2011',a.beverly_pdf)]:
 b=Path(path).read_bytes();s=sources[key]
 check(key+' entity SHA256',hashlib.sha256(b).hexdigest()==s['sha256'])
 check(key+' bytes',len(b)==s['bytes'])
 r=PdfReader(path);readers[key]=r
 check(key+' pages',len(r.pages)==s['pages'])
def compact(t):return re.sub(r'\s+','',t).casefold()
def text(k,page):return readers[k].pages[page-1].extract_text() or ''
c3=text('CW2010',3);c4=text('CW2010',4);b2=text('BH2011',2);b8=text('BH2011',8)
b11=text('BH2011',11);b12=text('BH2011',12)
for label,full,fragment in [
 ('CW item',c3,'Authorize the Fire Chief to sign'),
 ('CW identifier',c4,'G-0006'),
 ('CW inventory date',c4,'January 31, 2007'),
 ('CW cutting condition',c4,'be cut into two pieces if requested'),
 ('CW identification wording',c4,'no visible identification marks'),
 ('CW unusual indemnity wording',c4,'holds neither'),
 ('BH nonalteration account',b2,'not alter the Artifact'),
 ('BH inventory date',b8,'January31,2007'),
 ('BH raw extracted identifier',b11,'1-0137'),
 ('BH inspection right',b12,'inspect and test'),
 ('BH notice',b12,'ten days notice')]:check(label,compact(fragment) in compact(full))
result={'scope':'Entity/text-anchor and reference comparison only; page-image readings separately recorded.',
 'checks':checks,'passed':len(checks),
 'reference_comparison':{'same_inventory_date_referenced':True,'same_artifact_identifier':False,
  'CW_staff_reported_cutting_conditional':True,'BH_staff_reported_nonalteration':True,
  'actual_CW_agreement_or_inventory_acquired':False,'actual_cutting_tested':False,
  'same_object_conflict_established':False,'W14_C12_or_NIST_coupon_join_established':False},
 'limits':'Whitespace and case normalized for anchor matching only. Raw sources and conflicting extraction/image prefixes unchanged. A shared date does not authenticate a volume or physical-object identity. No historical cause, custody, contract enforceability or actual performance test.'}
print(json.dumps(result,indent=2,ensure_ascii=False))
