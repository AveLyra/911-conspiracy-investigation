"""Check captured representations and actual portal-link joins; not historical execution."""
from pathlib import Path
import argparse,hashlib,json
from pypdf import PdfReader
AGREEMENT_SHA='2b70b290ee4a228a4aeeac4962163ed7eac42c8e239d379506e43f5f1aeca227'
IMAGE_SHA='d8641a4eb3cad6e4d625e43c0b6f0996b10cee4a0b4b86cd00792c05e76ff488'
def verify(agreement,image,portal,meeting,item):
 a=Path(agreement).read_bytes();b=Path(image).read_bytes()
 assert len(a)==86307 and hashlib.sha256(a).hexdigest()==AGREEMENT_SHA
 assert len(b)==1257562 and hashlib.sha256(b).hexdigest()==IMAGE_SHA
 ar=PdfReader(agreement);ir=PdfReader(image);assert len(ar.pages)==3 and len(ir.pages)==1
 t=[p.extract_text() or '' for p in ar.pages]
 for token in ['Wednesday, June 08, 2016','H-0012','January 31, 2007','December 4, 2009','July 22, 2010']:assert token in t[0],token
 assert '12.' in t[1] and 'signed counterpart' in t[1]
 for path,sha,size in [(portal,'b4b15c922d424cac701768f30a2c9cf2b282c25d5704f7f85b9551c4b84539cf',51960),(meeting,'78f0e20b26010f698dcccd920f017b6fa24e96a084006b40a6271bdc4223d39f',47632),(item,'525a45713f7db87d770bbed9db9d447c4969323ff7dd06aa20ed6c810a877fcc',26047)]:
  raw=Path(path).read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha
 p=Path(portal).read_text();m=Path(meeting).read_text();s=Path(item).read_text()
 assert 'https://woodstockga.iqm2.com/Citizens/Default.aspx' in p
 for token in ['ID=3968','ID=7077','ID=7078','2016-04-15-002 City of Woodstock WTC']:assert token in m,token
 assert 'This file has not yet been converted to a viewable format' in s
 assert 'The Minutes have not been approved.' in s and 'NOT an official record yet.' in s
 return {'all_checks_passed':True,'PDF_entities':2,'PDF_total_bytes':len(a)+len(b),'PDF_pages':[3,1],'agreement_sha256':AGREEMENT_SHA,'image_PDF_sha256':IMAGE_SHA,'HTML_entities_pinned_and_checked':3,'source_links_checked':['officialportal-tolegacy','meeting1331-toLegiFile3968','meeting-toattachment7077and7078'],'agreement_text_locators':7,'portal_conversion_warning_present':True,'portal_draft_warning_present':True,'manual_reading_scope':'Full agreement pages1-3 and sole image-PDFface read via144dpi renders; target portal/meeting/item HTML sections read. Code does not prove manual reading, blank handwritten signatures or lack of a legible item label.','signed_execution_physical_identity_or_custody_authentication':False,'NIST_FEMA_WTC7_building_join_verified':False,'court_attachment_bodies_read_in_this_unit':False,'no_physical_legal_entitlement_or_scientific_test':True}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ['agreement','image','portal','meeting','item']:p.add_argument('--'+n,required=True)
 a=p.parse_args();print(json.dumps(verify(a.agreement,a.image,a.portal,a.meeting,a.item),indent=2))
