"""Reproduce the reading qualification without overwriting source or prior research files."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib
from pypdf import PdfReader
OLD_SHA='662deb4043786fe6def1eb4d34e5bf390b903b599d6f7d4e5dff6c807af8a95d'
CANDIDATE_SHA='7c53814826fc1b21b59b91223eee5406fa1eada87cb8a793f49694ce916564ba'
JULY_SHA='6d60fd5e30f77662d4fb77a47bdc5c48e49b27b7818ba317e1a64b0580067475'
def checked(path,sha):
 raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
 return json.loads(raw)
def counts(rows,july):
 labels=[r['identifier_verbatim'] for r in rows if isinstance(r['identifier_verbatim'],str)]
 a=Counter(labels);b=Counter(r['identifier_verbatim'] for r in july)
 return {'source_rows':len(rows),'currently_readable_label_rows':len(labels),'unresolved_rows':len(rows)-len(labels),'distinct_readable_strings':len(a),'common_readable_strings':sorted(a.keys()&b.keys()),'readable_December_strings_not_in_July':len(a.keys()-b.keys()),'July_strings_not_matched_by_readable_subset':len(b.keys()-a.keys()),'scope':'Readability-filtered literal comparison; unmatched July may still have a counterpart in the unresolved cell. No object/alias/loss conclusion.'}
def verify(original_ledger,candidate,july_ledger,nist_pdf,court_pdf):
 old=checked(original_ledger,OLD_SHA);new=checked(candidate,CANDIDATE_SHA);j=checked(july_ledger,JULY_SHA)
 assert len(old)==len(new)==354
 changes=[i+1 for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert changes==[350,354]
 for i in [349,353]:
  assert new[i]['prior_identifier_verbatim']==old[i]['identifier_verbatim']
  assert new[i]['ledger_row']==old[i]['ledger_row'] and new[i]['physical_pdf_page']==old[i]['physical_pdf_page']==9
 assert old[349]['identifier_verbatim']=='U-4' and new[349]['identifier_verbatim']=='U-6'
 assert old[353]['identifier_verbatim']=='n-141' and new[353]['identifier_verbatim'] is None and new[353]['visible_suffix']=='-141'
 sources=[]
 for role,path,sha,size,pages in [('NIST published report',nist_pdf,'d234d025912dab100a0dd479f826b2adff0fc23acd5acb42efc93a4a8bcd9bc3',12034476,114),('City court-copy source',court_pdf,'fd1eeb230cdba27ffc4bde627b208fcce24fc6dc7c4d7f27eca5e34f9de1119d',224690,9)]:
  raw=Path(path).read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha and len(PdfReader(path).pages)==pages
  sources.append({'role':role,'sha256':sha,'bytes':size,'PDF_pages':pages})
 return {'all_documentary_and_reproducibility_checks_passed':True,'old_ledger_sha256':OLD_SHA,'candidate_sha256':CANDIDATE_SHA,'July_ledger_sha256':JULY_SHA,'changed_research_rows':changes,'earlier_frozen_transcription_result':counts(old,j),'qualified_readable_subset_result':counts(new,j),'source_checks':sources,'visual_reading_not_proven_by_hash_or_code':True,'all_other_old_rows_preserved_not_independently_certified':True,'native_alias_custody_or_scientific_test_complete':False,'prior_sources_or_research_modified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['original-ledger','candidate','july-ledger','nist-pdf','court-pdf']:p.add_argument('--'+name,required=True)
 a=p.parse_args();print(json.dumps(verify(a.original_ledger,a.candidate,a.july_ledger,a.nist_pdf,a.court_pdf),indent=2))
