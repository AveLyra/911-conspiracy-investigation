# Search and verification scope

This is a bounded public-source follow-up, not a certification that every responsive agency record has been located. No agency, witness or third party was contacted. No new FOIA request, fee commitment, private-mailbox access or litigation-record change was made.

## Acquired and held records

- Rechecked the held 429-page DOT OIG production as an unchanged, hashed input. Full-text searches supplied locators; complete selected pages and decisive page images were then examined.
- Acquired the 4,380-page 2021 DOT OIG release and separate 257-page 2011 FAA response from the public GovernmentAttic links. Preserved downloads unchanged, hashed them, extracted all pages with Python 3.13.7 / pypdf 6.10.0 and searched the extracted text. **Full-text indexing is not full substantive review of 4,380 pages.**
- Read targeted drafting, correction, interview and status passages in context. Earlier official report, reproduced answer and public hearing sources were retained and rechecked. The source registry distinguishes agency-hosted material, government records in third-party releases, and public hearing transcripts in the UNT government archive.
- Inspected PDF embedded-file attachment-name trees in all three release PDFs; no attachment names were exposed. No files were carved or executed. This test does not establish the contents of every page or that native attachments never existed.
- Source PDFs, full extractions, acquisition receipts and page rasters remain preserved separately. This public copy contains selected reviewed text/identifiers, not bulk raw production downloads, email addresses, phone numbers or private case data.

## Image inspection versus text search

The 429-page release's case-status screen has almost no extractable text. Its Closed field and date were checked in the image rather than inferred from a keyword search. Likewise, wrapped attachment filenames and printout dates were checked visually.

Physical pages actually inspected visually in this run:

- **DOT-429 (29 pages):**6,7,8,9,10,11,12,13,14,15,16,17,18,19,106,168,169,170,171,172,175,176,177,178,179,180,182,183,184.
- **DOT-INTERVIEWS (41 pages):**2,5,2182,2183,2185,2188,2189,2325,2466,2467,2495,2670,2681,2685,2688,2689,3275,3276,3294,3295,3296,3306,3307,4052,4056,4057,4058,4060,4096,4097,4104,4106,4107,4111,4134,4135,4136,4139,4303,4325,4330.

Additional pages were rendered but are not counted as visually reviewed merely because a PNG exists. This inspection checked content/labels, not a new print-layout/export artifact. No original interview audio was replayed or authenticated.

## Public search scope and access limits

Search strings are preserved in SEARCH-QUERIES.json. They target case/report identifiers, QFRs, correction, administrative action, named public officials, interview releases and archival folders. Searches generated overlapping and irrelevant hits; query count is not an evidence count. Raw search-result bodies were not saved for every query. Acquired source bodies and their hashes are distinguished from search-only pointers.

The GovernmentAttic document menu identified the larger release's exact URL. Initial menu/direct requests returned 403/406 in some attempts; ordinary public GETs later succeeded for the release PDFs. Those access outcomes are logged locally and are not treated as evidence of suppression.

The official DOT library page still links CC-2006-085 but supplies no case-specific final administrative disposition on that page. The official semiannual index links the April–September 2006 and both 2007 reports. Direct PDF downloads returned 403. The web tool could parse them: physical page46 of sar_2006.pdf repeats the recommendation to correct the QFR and consider action. Keyword searches of the 2007 parsed reports for 9/11 and CC-2006-085 did not identify a case-specific disposition. This was **not** a complete audit of personnel files, every semiannual-report page, recommendation-management systems or the entire agency website. No raw-byte hash is assigned to a PDF obtained only as web-tool parsed text.

The January14, 2009 NARA finding aid, physical page94, lists **FAA QFR Responses** in **Box 69, Tom Eldridge's Files**. Surrounding folders concern other topics, so the title alone does not establish this particular liaison answer is inside. A current FAA archival finding-aid table was searched as a locator; no specific original answer/transmission or final administrative decision was identified. Current folder contents and availability remain unverified.

## Excerpt/pin semantics

EXCERPTS.json contains 39 unmodified substring pins and 6 separately labeled manual image-field transcriptions. A substring pin includes source ID, one-based physical page, printed page where known, complete extraction SHA-256, character range, derivative line range and excerpt hash. Those lines are not the historical transcript's original numbered lines. OCR/text-extraction mistakes and visible source errors are retained; neither is silently normalized into an evidentiary correction.

Manual fields have a page-image hash and a description of the supplied punctuation. The archive's full original remains the reference for redactions, layout and context. The public script can mechanically recheck byte hashes and the 39 substring pins when supplied with a local source map. It cannot independently verify manual transcription, authenticity of a reproduced email, witness truthfulness, search completeness, intent or a conspiracy.

## Revision and publication scope

This new directory is an additive supplement to public commit 568b48572cd77c6ec16a7ed33b12c2486affb1ed. It leaves the 175-entry master and earlier studies unchanged. A failed candidate build stopped on an exact substring-boundary mismatch; that incomplete local candidate was retained, the boundary was repaired, and source checks were rerun. No source text was edited to make a check pass. pdftotext was unavailable; its failed attempt was retained and pypdf was used explicitly instead.

TEXT-CHANGES.diff records all new narrative/structured research text against absent new files. The local earlier candidate and final-candidate text comparison are retained separately; no old finding is overwritten. Manifest checks, source re-extraction, manual image reading and remote Git publication checks are reported separately. Successful publication is established by the subsequent commit/ref/blob receipt, not by a statement written into this draft.
