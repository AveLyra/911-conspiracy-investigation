"""Verify captured source bytes and extractable locators; no visual or historical authentication."""
from pathlib import Path
import argparse, hashlib, json
from pypdf import PdfReader

DEC = ('fd1eeb230cdba27ffc4bde627b208fcce24fc6dc7c4d7f27eca5e34f9de1119d',224690,9,'1506','12/04/2009')
JUL = ('d28acba7420a8273e5d797e36f2a60f65bfa1b219505c4f641f04b674883dbdf',148109,11,'1509','07/22/2010')
MEETING_SHA = '78f0e20b26010f698dcccd920f017b6fa24e96a084006b40a6271bdc4223d39f'
AGREEMENT_SHA = '2b70b290ee4a228a4aeeac4962163ed7eac42c8e239d379506e43f5f1aeca227'
LEDGER_SHA = '6d60fd5e30f77662d4fb77a47bdc5c48e49b27b7818ba317e1a64b0580067475'

def verify(december,july,meeting,agreement,prior_ledger):
    out=[]
    for path,spec in [(december,DEC),(july,JUL)]:
        raw=Path(path).read_bytes();sha,size,count,doc,date=spec
        assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha
        reader=PdfReader(path);assert len(reader.pages)==count
        for n,page in enumerate(reader.pages,1):
            text=page.extract_text() or ''
            for token in ['1:21-mc-00097-AKH-THK','Document '+doc,'Filed '+date,f'Page {n} of {count}']:
                # Whitespace normalization here is only a locator test; original bytes and header values remain pinned.
                assert token in ' '.join(text.split()),(doc,n,token)
        out.append({'sha256':sha,'bytes':size,'PDF_pages':count,'all_header_locators_passed':True})
    m=Path(meeting).read_bytes();assert len(m)==47632 and hashlib.sha256(m).hexdigest()==MEETING_SHA
    text=m.decode()
    for token in ['FileOpen.aspx?Type=4&amp;ID=7075&amp;MeetingID=1331','FileOpen.aspx?Type=4&amp;ID=7076&amp;MeetingID=1331']:
        # HTML source may use literal ampersands. Accept either serialization, preserving the captured entity hash.
        assert token in text or token.replace('&amp;','&') in text,token
    a=Path(agreement).read_bytes();assert len(a)==86307 and hashlib.sha256(a).hexdigest()==AGREEMENT_SHA
    t=PdfReader(agreement).pages[0].extract_text() or ''
    for token in ['H-0012','December 4, 2009','July 22, 2010','January 31, 2007']: assert token in t,token
    raw=Path(prior_ledger).read_bytes();assert hashlib.sha256(raw).hexdigest()==LEDGER_SHA
    rows=json.loads(raw);hits=[r for r in rows if r['identifier_verbatim']=='H-0012']
    assert len(hits)==1 and hits[0]['physical_pdf_page']==72 and hits[0]['identifier_row_on_page']==25 and hits[0]['ledger_row']==208
    return {'all_checks_passed':True,'new_PDF_entity_checks':out,'new_PDF_total_bytes':DEC[1]+JUL[1],
            'extractable_headers_checked':20,'reused_meeting_hash_and_two_literal_links_checked':True,
            'reused_agreement_hash_and_four_locator_tokens_checked':True,'prior_July_ledger_hash_and_H0012_locator_checked':True,
            'reading_scope':'Manual full-page inspection: December 1,2,3,5,6,7; July 1,2,6. Not proven by this code.',
            'manual_claims_not_machine_verified':['scanned order wording','handwritten date reading','H-0012 description','selected December item descriptions'],
            'native_court_authentication_full_list_comparison_custody_and_empirical_testing_performed':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for name in ['december','july','meeting','agreement','prior-ledger']:parser.add_argument('--'+name,required=True)
    a=parser.parse_args();print(json.dumps(verify(a.december,a.july,a.meeting,a.agreement,a.prior_ledger),indent=2))
