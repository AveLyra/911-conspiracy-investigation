"""Check the captured Dixon source and selected text locators, not historical execution."""
import argparse,hashlib,json
from pathlib import Path
from pypdf import PdfReader
EXPECTED='6971b7e9b1bdf595e0dd694a2ebf656ed4bafc592140d7e607b7de90107b13a3'
def verify(source):
 p=Path(source);b=p.read_bytes();assert len(b)==120782;assert hashlib.sha256(b).hexdigest()==EXPECTED
 r=PdfReader(p);assert len(r.pages)==9
 t={n:r.pages[n-1].extract_text() for n in [1,8,9]}
 assertions=[(1,'APRIL 26, 2011'),(8,'January 31, 2007'),(8,'I-0094'),(8,'available for testing purposes in the future, if requested.'),(9,'11- 049'),(9,'AG 11 -013')]
 for page,token in assertions:assert token in t[page],(page,token)
 return {'source_sha256':EXPECTED,'source_bytes':len(b),'PDF_pages':len(r.pages),'selected_physical_pages':[1,8,9],'exact_text_locators_matched':len(assertions),'all_checks_passed':True,'manual_reading_scope':'Full visible faces 1, 8 and 9 were separately reviewed at 144 dpi. This script does not prove that review, vote authenticity, signed agreement, custody or actual testing.','representation_note':'Plain extraction includes 11- 049 and AG 11 -013; visible page 9 shows 11-049 and AG 11-013. Both representations are retained and source bytes are unchanged.','historical_test_or_agreement_execution_verified':False}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',required=True);args=a.parse_args();print(json.dumps(verify(args.source),indent=2))
