"""Verify the preserved packet and selected representation-specific locators only."""
import argparse,hashlib,json
from pathlib import Path
from pypdf import PdfReader
EXPECTED='c0c9d3b23f3945259a6d0f9a66c3f48308f852b160c73c15425f375754667c0a'
def verify(source):
 b=Path(source).read_bytes();assert len(b)==12687834 and hashlib.sha256(b).hexdigest()==EXPECTED
 r=PdfReader(source);assert len(r.pages)==252
 pages=[1,2,201,202,206];text={n:r.pages[n-1].extract_text() or '' for n in pages}
 checks=[(1,'July 11, 2016'),(2,'Approval of Minutes - 6/13/2016'),(201,'4013'),(201,'Pending'),(201,'07/11/2016 7:00 PM'),(202,'June 13, 2016'),(202,'06132016 1st draft'),(206,'Steel Transfer Agreement [APPROVED]'),(206,'7.1 through 7.12')]
 for page,token in checks:assert token in text[page],(page,token)
 repeated=text[206].count('Motion carried 6-0.')
 assert repeated==6
 return {'all_checks_passed':True,'source_sha256':EXPECTED,'source_bytes':len(b),'source_pages':len(r.pages),'selected_physical_pages':pages,'matched_exact_text_locators':len(checks),'repeated_six_zero_motion_strings_on_page206':repeated,'count_scope':'Occurrences in one page text, not independent votes, tests, witnesses or approvals. Actual meeting motion count not verified.','historical_signature_transfer_custody_testing_or_city_byte_equivalence_verified':False,'manual_reading':'Full144dpi faces1/2/201/202/206 reviewed separately; this code does not prove human reading or historical truth.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);a=p.parse_args();print(json.dumps(verify(a.source),indent=2))
