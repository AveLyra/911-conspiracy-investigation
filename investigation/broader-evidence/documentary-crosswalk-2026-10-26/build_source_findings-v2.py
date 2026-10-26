"""Bounded source findings with explicit attribution, counterevidence and gaps."""
from pathlib import Path
import hashlib, json

R=Path(__file__).resolve().parent
OIG='https://oig.justice.gov/sites/default/files/archive/special/0506/chapter5.htm'
FBI='https://www.govinfo.gov/content/pkg/GOVPUB-J1_14-PURL-gpo159739/pdf/GOVPUB-J1_14-PURL-gpo159739.pdf'
COURT='https://www.nysd.uscourts.gov/sites/default/files/2025-08/03-md-01570%2011182.pdf'
CAT='https://www.govinfo.gov/app/details/GOVPUB-J1_14-PURL-gpo159739'
records=[]

def add(ident,title,claim,source,locators,parents,contrary,gaps,test,scope,propositions):
    records.append(dict(id=ident,title=title,checked_claim=claim,
        assessment_links=parents,source_url=source,exact_locators=locators,
        status='Source content checked; historical inference explicitly bounded',
        evidence_grade=dict(document_content='A: direct current source inspection',historical_inference='B–D depending on the stated proposition; underlying originals are not supplied merely by a summary'),
        contrary_evidence_and_limits=contrary,missing_records=gaps,
        smallest_discriminating_step=test,actually_inspected=scope,
        hypotheses_bearing=propositions,
        inference_exclusions=['No automatic bridge to a demolition mechanism','No collective attribution from nationality or association','No inference of purpose from an unexplained discrepancy alone'],
        independence='Shared document/exhibit chains are not independent corroboration; see source-chain-map-v1.json'))

add('S001','A specific hold instruction, not merely a failure to pass a message',
    'The DOJ OIG reconstructs a CIA-system draft CIR carrying Mihdhar visa/travel information, a same-day hold note attributed to the CIA deputy chief, and a later unanswered query about sending/remaking it. It reports that the draft was not formally disseminated to its FBI addressees.',
    OIG,['Chapter V III.A.4; derived blocks P089–P099; IV.A P439'],['H002'],
    'FBI personnel detailed to the CIA had accessed the visa cables/draft. Therefore “no FBI employee knew” is broader than the reported formal-dissemination failure. Witnesses generally reported no recollection; the hold purpose was not established.',
    ['Original draft CIR with version/access metadata','Original hold annotation and routing/addressee audit','The mid-January email and response search'],
    'Acquire the exact draft/routing record and distinguish individual access from dissemination to FBI operational addressees.',
    'Complete relevant HTML paragraphs P089–P110 and surrounding CIA/FBI-role context were read; original CIR not acquired.',
    ['information handling','possible deliberate nonintervention: unestablished purpose/knowledge bridge'])
add('S002','Conflicting contemporary handling accounts remain side by side',
    'The OIG describes an internal CIA cable saying the visa documents had been passed to the FBI, approximately three hours after the hold note. It found no witness or additional document corroborating that transfer.',
    OIG,['III.A.6; blocks P104–P110'],['H002'],
    'An incorrect statement, an undocumented transfer or other process failure are competing possibilities; the report did not determine why the cable said this. CIA/FBI interviews and access logs do not certify receipt by the named operational addressees.',
    ['Original internal cable and distribution list','Claimed delivery/receipt record','The identities/records underlying the transfer assertion'],
    'Match the original cable statement to a recipient acknowledgment or a complete negative search with scope.',
    'Full quoted report paragraphs inspected; no native CIA cable/receipt supplied.',
    ['information handling','record completeness','intent unresolved'])
add('S003','Later oversight nonproduction is a distinct event',
    'The OIG states that it discovered the CIR title in February 2004 in a list of documents accessed by FBI detailees, after neither it nor the CIA OIG had previously obtained the draft; follow-up work delayed the review.',
    OIG,['I–II background; blocks P021–P028'],['H003'],
    'The OIG lacked independent access to CIA databases. The published account establishes a late-discovery problem, not the reason the document was absent or a demonstrated connection to the 2000 hold decision.',
    ['Oversight requests and search/production logs','The accessed-document list','Original receipt and subsequent interview records'],
    'Compare the exact request terms, searches and production chronology rather than treating every omission as destruction.',
    'Full OIG background and late-discovery paragraph read; underlying oversight production logs not acquired.',
    ['later disclosure/possible concealment','no established pre-attack-purpose bridge'])
add('S004','FBI-asset tenancy and conflicting disclosures',
    'The OIG reports that Hazmi and Mihdhar boarded with an FBI informational asset in 2000. It records inconsistent accounts about whether the asset told his handler about them, what identities were supplied and what follow-up occurred.',
    OIG,['III.B.3; blocks P199–P211; notes 130–135 at P653–P658'],['B118'],
    'The asset and retired handler were not interviewed directly by OIG, although the handler had spoken to FBI supervisors and congressional investigators. OIG notes an inconclusive polygraph and the San Diego FBI conclusion that the asset was not complicit. None should be dropped.',
    ['Contemporaneous asset contact reports','Complete original post-attack statements','Congressional interview/testimony originals and OIG interview requests'],
    'Cross-reference dated contact notes against each later account and identify which assertions are independently documented.',
    'Complete tenancy/disclosure paragraphs and notes 130–135 read; source interviews remain report-level.',
    ['assistance/contact','FBI source handling','foreknowledge not established'])
add('S005','Documentation criticism differs from a proved policy violation',
    'The OIG criticizes thin annual bona-fides documentation and missing retrievable information, while saying no specific FBI rule required the handler to investigate or record the identities of these boarders.',
    OIG,['IV.B.3; blocks P511–P527; conclusions P594–P596'],['B118'],
    'The lack of a specific boarder rule and disagreement among other agents are contrary to a blanket “proved rule violation” characterization. The policy review still identifies a concrete oversight weakness.',
    ['Controlling contemporaneous asset policies','Annual source evaluations with supporting checks','Contact-report retention/indexing rules'],
    'Inspect the actual evaluation and policy texts, separating a missing policy from failure to follow an existing one.',
    'Full quoted handling-policy and evaluation paragraphs read; original asset file/policies not acquired.',
    ['institutional conduct','source reliability','no automatic attack direction'])
add('S006','A documented payment/closure lead without an established purpose',
    'OIG note 133 reports that the initially unpaid asset received $100,000 and was closed as an asset in July 2003.',
    OIG,['Note 133; derived block P656'],['B118'],
    'The note does not establish what the payment compensated, who approved it or why the asset was closed. A hush-payment or protection theory is a hypothesis, not a result of reading the amount.',
    ['Payment authorization and purpose','Disbursement voucher','Source closeout and approval records'],
    'Obtain the payment/closeout authorization before assigning a motive.',
    'Complete footnote read in context with interview-access limits and reported noncomplicity finding.',
    ['FBI source handling','possible later protection: untested'])
add('S007','Specific assistance and a repayment that changes the financial characterization',
    'The 2016 EC reports translation, travel, lodging and financing assistance and labels coincident transfers anomalous. Separately, OIG reports a same-day reimbursement of the first rent/deposit advance; note 129 gives $1,558 and a nearby $9,900 deposit. The 2025 court also describes repayment.',
    FBI,['Physical PDF p9 / internal p8','OIG III.B.2 P196 and note 129 P652','Court physical p21'],['H006','B211'],
    'A reimbursed advance is not automatically an unrepaid gift or proof of the original source of the hijackers’ funds. Repayment does not erase logistical facilitation. The EC’s broader anomalous-transfer claim cannot be resolved using one summarized transaction.',
    ['Underlying bank statements/checks/deposit records','EC referenced financial-analysis document','Court Pls Ex550 FBI8057; KSA Ex91 FBI2808–09; Bayoumi deposition 737:3–17'],
    'Match the actual debits, credits, timing, amounts and beneficial sources across the whole claimed transfer set.',
    'EC physical p9 visually inspected; complete OIG paragraphs/footnote read; court p21 visually inspected. No raw bank records acquired.',
    ['assistance','knowledge and ultimate financing remain separate'])
add('S008','Restaurant accounts conflict, with limits on what the witness could observe',
    'The EC contrasts Bayoumi’s claimed overhearing of Arabic while leaving with BIN DON’s account of a front-window position and approach at a distance inconsistent with first hearing the speech. BIN DON is reported not to understand Arabic.',
    FBI,['Physical pp9–10 / internal pp8–9'],['H006'],
    'A witness can report position and movement without knowing the Arabic conversation or an earlier plan. The original statements and their interview dates/references are not reproduced in full. Do not count their later summaries as new witnesses.',
    ['Original Bayoumi 2003 interview','Original BIN DON interview(s)','Restaurant layout and contemporaneous corroboration'],
    'Compare complete statements, opportunity to observe, sequence of questions and any contemporary account.',
    'Both complete scanned pages viewed and OCR checked against images.',
    ['possible arranged assistance','foreknowledge not established merely by approach'])
add('S009','Later court record adds competing statements, not a settled harmonization',
    'The court describes Bayoumi and Morgan giving two-minute versus thirty-minute conversation accounts. It also reports Morgan’s declared belief that the encounter was coincidental, and Bayoumi’s denied offer of help beside a quoted MPS account of offering contact/help.',
    COURT,['Physical pp17–18','Pls Ex120 402:10–20, 725:14–726:16, 726:23–727:2','Ex112 97:15–98:4; Ex92 paragraph19; Ex450 193:11–16'],['H006','B211','B212'],
    'BIN DON and Morgan must not be silently equated or counted as two independent witnesses without an identity/alias crosswalk. The court’s whole-record jurisdiction inference remains stronger than any one isolated inconsistency.',
    ['Complete declarations and deposition transcripts','Original MPS transcript/recording','Witness identity/alias chain'],
    'Join the exact interview/deposition editions and witness identities; preserve two/thirty minutes and the coincidence belief even if a larger inference is supported.',
    'Complete court pp17–18 visually inspected; cited originals not acquired in this pass.',
    ['assistance/coordination','witness consistency','independence'])
add('S010','Substantive preliminary judicial findings should not be minimized',
    'The court’s August 28, 2025 decision made an evidence-based jurisdiction assessment supporting an inference of knowing or deliberately indifferent Saudi-linked assistance. It found the encounters more likely than chance and denied the renewed jurisdictional dismissal motion.',
    COURT,['Physical pp6–7,40–45; especially40–42 and45'],['B211','B212','B215'],
    'This was not mere acceptance of pleaded allegations. It also was not a final merits judgment that the Saudi government ordered the attacks; the opinion expressly reserves disputed credibility/meaning questions for trial. No present appellate status is claimed here.',
    ['Underlying exhibits and complete adversarial record','Later appellate mandate or current docket record'],
    'Test the cited exhibits and competing explanations on their actual contents, while tracking the procedural standard separately.',
    'Whole relevant pages read; pp6,40,41,42,45 visually checked. This is public-record research, not advice for the user’s FOIA case.',
    ['assistance','knowledge/deliberate indifference','judicial finding with procedural limits'])
add('S011','The same court rejected dramatic video inferences',
    'The court did not accept that the apartment gathering video established an attack-preparation welcome party or that the Washington video established terrorist reconnaissance; its assistance inference rested on other record evidence.',
    COURT,['Physical p42, section C'],['B213'],
    'That is an important negative result alongside the jurisdictional findings. This review has not independently examined the complete original videos or adopted the court’s description as a certified audiovisual analysis.',
    ['Pls Ex10K (MPS2023–059) and Ex10K-TR','Pls Ex10F original Washington footage and full metadata'],
    'Obtain complete original recordings and transcripts before converting selected scenes into intent claims.',
    'Full court p42 visually inspected; original videos unacquired.',
    ['negative inference test','assistance distinguished from reconnaissance/intent'])
add('S012','The airplane drawing is a precise missing-exhibit lead',
    'The court discusses an airplane drawing and equations as supporting its knowledge inference but also records a dispute over the drawing’s meaning. It identifies Pls Ex678M, MPS696_1–7.',
    COURT,['Physical pp41,44–45; Pls Ex678M MPS696_1–7'],['B211','B212'],
    'Neither this inventory nor a press image establishes the original page sequence, date of creation, complete context, mathematical purpose or use in attack preparation. The drawing was not independently acquired here.',
    ['Complete exhibit MPS696_1–7','MPS seizure/inventory and authentication','Complete Bayoumi explanation and competing expert analysis'],
    'Obtain the actual exhibit before analyzing the mathematics or asserting target-specific intent.',
    'Court source passages read and p41/p45 visually checked; targeted public searches found later summaries/filings, not the complete underlying exhibit.',
    ['possible knowledge','physical exhibit interpretation remains open'])
add('S013','The EC’s telephone paragraph contains its own timing tension',
    'Internal p14 first describes five Bayoumi–Sudairy calls as occurring while the hijackers were with Bayoumi in San Diego, then lists three in January before the described restaurant meeting and a later date printed only as 02/2000. Both descriptions are preserved.',
    FBI,['Physical p15 / internal p14; compare physical p9 meeting on/about02/01/2000'],['H006'],
    'This could be scope shorthand or an editorial problem, but neither explanation was demonstrated. The narrative does not itself supply the call records or content. Do not silently fill the incomplete date with a guessed day.',
    ['Underlying call-detail records and analysis','Unredacted source reference if lawfully released','Event/location timeline and time-zone conventions'],
    'Rebuild the dated call chronology from original records, preserving direction, missing entries and uncertainty.',
    'Whole scanned p15 viewed; the incomplete date and introductory wording confirmed visually, not merely OCR.',
    ['communication chronology','source-quality discrepancy, not a motive finding'])
add('S014','Catalog date conflict and file-version comparison',
    'GovInfo’s abstract says the interview was November12–13,2013, while its title and the EC identify November2015. The GovInfo and FBI-hosted PDFs have different whole-file hashes/sizes, but all17 tested page content streams, image payloads, decoded RGB pixels and page boxes match.',
    CAT,['Catalog Abstract versus title','EC physical p3 synopsis','source-version-comparison-v3.json'],['H006'],
    'The catalog date remains a preserved mismatch; no edit cause is assigned. Matching page components limit the demonstrated file-version difference in this comparison, not the truth of the report. Two hosts supply one documentary chain.',
    ['Catalog revision provenance','Full PDF object/metadata difference analysis if needed'],
    'Use the original report and both catalog values when requesting the source interview; do not treat a catalog typo hypothesis as an established explanation.',
    'Both originals acquired;17-page structural/image comparison executed; relevant synopsis/catalog representations inspected. Earlier comparator mistakes are preserved as our errors.',
    ['provenance','low direct attack-attribution value'])

def main():
    cross=json.loads((R/'claim-crosswalk-v2.json').read_text());ids={x['id'] for x in cross['records']}
    for r in records:
        for parent in r['assessment_links']:assert parent in ids,parent
    acquisitions=json.loads((R/'acquisition-v2.json').read_text())+json.loads((R/'acquisition-v3.json').read_text())
    output=dict(status='First bounded source tranche; not complete verification of all assessment claims',findings=records,source_pins=acquisitions,
                source_scope=dict(primary_hosted_documents=3,additional_same_chain_FBI_representation=1,catalog_representation=1,original_bank_records_acquired=0,original_CIA_CIR_acquired=0,original_interview_or_deposition_records_acquired=0,native_model_runs=0),
                hypothesis_separation=['assistance','foreknowledge','deliberate nonintervention','demolition','subsequent concealment'])
    with (R/'source-findings-v2.json').open('x') as f:json.dump(output,f,indent=2,ensure_ascii=False);f.write('\n')
    lines=['# Saudi-assistance and FBI-source-handling review','',
           'This is a checked-source first tranche, not acceptance of the documentary assessment. Each S-ID separates the report’s content from an unresolved historical inference. All B/H inventory assertions remain claims to test; these source findings support only their stated narrower propositions.','']
    for r in records:
        lines += [f"## {r['id']}: {r['title']}",'',r['checked_claim'],'',
                  f"Source: [original record]({r['source_url']}); {'; '.join(r['exact_locators'])}.",'',
                  'Contrary evidence and limits: '+r['contrary_evidence_and_limits'],'',
                  'Needed: '+'; '.join(r['missing_records'])+'.','',
                  'Next test: '+r['smallest_discriminating_step'],'']
    with (R/'SAUDI-FBI-REVIEW-v2.md').open('x') as f:f.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(source_findings=len(records),original_bank_or_interview_records_acquired=0,publication_performed=False)))

if __name__=='__main__':main()
