# UAL175 accident-package corrections: actual requests, displayed responses and missing versions

Source review: October 30, 2026. **Two official NARA PDFs document a correction process involving transcript timing labels, speaker/agency attribution, recertification, statements and package presentation.** This is a source-pinned version-history lead, not evidence that a transcript was intentionally falsified. The scans report corrections and receipt, but do not supply the underlying recordings, complete before/after transcripts or authenticated final delivery. They are not the missing May 2003 QFR correction or a 2006 personnel-action decision.

## Sources and actual reading scope

| Source | Original link | Entity pin | Read |
|---|---|---|---|
| AEA1124 / NARA7598362, February 5, 2002 formal-package correction memorandum and attachments | [Official PDF](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/4-UAL-175/e-Other/4-AEA-1124-MEMO--FORMAL-ACCIDENT-PACKAGE-REF-ZNY-ARTCC-148-UAL175-ON-CORRECTION-FEB-5-2002.pdf) · [catalogue](https://catalog.archives.gov/id/7598362) |262,340 bytes; SHA-256 `e26e5570efc704df0e24b51259f82337e39ae789a622e99ad4c276caa6c2433c`|All 5 physical page images|
| AEA1122 / NARA7598360, corrections email | [Official PDF](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/4-UAL-175/e-Other/4-AEA-1122-EMAIL--FORMAL-ACCIDENT-PACKAGE-REF-ZNY-ARTCC-148-UAL175-ON-CORRECTIONS-REDACT-SEALED.pdf) · [catalogue](https://catalog.archives.gov/id/7598360) |94,525 bytes; SHA-256 `5c20e3bfb9f554f461a04a1aa44dac90a87f8450631de8a8c64ba55f5c6c69c5`|All 1 physical page image|

Both entities returned HTTP 200 / application/pdf on October 30, 2026; exact UTC times, selected metadata and derivative hashes are in [SOURCE-PINS.json](SOURCE-PINS.json). Those facts authenticate the retrieved bytes and official hosting, not the authorship, native correspondence chain or accuracy of each historical statement. Dates printed in the source are preserved as printed; email times have no verified time zone.

All six images were visually inspected before visible-pixel OCR. There was no hidden PDF-layer text extraction, redaction reconstruction, audio retrieval/listening/decoding or clock fitting. Source PDFs, full OCR, rasters, signatures and personal/contact fields remain outside this public derivative. References below use physical PDF page and actual saved Tesseract 5.5.2 / psm3 line numbers, including blank lines; the image is the reading authority. For example, OCR misreads the visible word Eighth and the case code on one page; we preserve the OCR locally and explicitly use the image reading, not a silent alteration of the original.

## Chronology and source layers, kept separately

| Observation in released scan | Exact locator | Limit |
|---|---|---|
| A forwarded November 15, 2001 7:46 AM message says the UAL175/New York/ZNY-ARTCC-148 accident package was received. |AEA1124 physical 3, visible OCR53–62|A statement of receipt in a later forwarded printout, not authenticated native delivery/receipt evidence.|
| December 18, 2001 8:57 AM message requests changes and return by January 4, 2002. |physical 3, 37–44|Original attachment/version and actual return not acquired.|
| February 1, 2002 8:39 AM message says earlier corrections were received but further attached changes needed;9:22 AM forwarding says additional corrections due February 15; outer header12:14 PM. |physical 3, 1,15–17,23–28|Keep request, reported receipt, deadline and forward times distinct.|
| Cover datedFebruary 5, 2002 says corrections plus requested changes/explanations are attached. An undated note says Changes Posted. |physical 1, 9–11,20–22 and lower-right image note; physical 2,14–16,23–25|Physical1 is presented with an attached note; physical 2 presents the cover without that obscurity. These are two views of related cover content, not independent confirmation of posting.|
| The displayed change sheets are headed UAL175–Change 2, 9/11/01 and have footers Page 1 of 22 and Page 2 of 22. |physical 4,1–4; physical 5,1|The accident-date heading is not independently established as a creation date. Only these two change-sheet pages appear here; the full referenced 22-page document/version is not authenticated or fully supplied by this five-page entity. Do not infer twenty deleted pages.|
| Embedded May 7, 2002 03:30 PM email says corrections received, describes remaining edits as minor, requests expedited shipment for final review and hopefully release; outer forward is May 8 8:54 AM, with intermediate May 7 03:36 PM forward. |AEA1122 physical 1,1; visible date block 20–21;32–35;61–63; intermediate header visually read|The characterization minor is the source's, not our evaluation. Four entries display Correction made, while final-review/release language remains conditional. No independently authenticated final shipment/approval/release is supplied.|

Status-annotation dates are not authenticated: a dated cover or forwarded header does not establish when each Corrected / Correction made annotation was inserted. We do not assign those annotations a correction date.

Printed Word-attachment labels on AEA1124 physical 3,66–67 identify `UAL175 9-11-01.doc` and `UAL175 Change 2.doc`. An icon and filename are leads, not evidence that we possess a native Word attachment or its revision history. Selected PDF capture/HTTP metadata are separately preserved; no authoring chronology is inferred from scan/software dates.

## Conflicting values and correction reports

[CORRECTION-LEDGER.json](CORRECTION-LEDGER.json) preserves **all 33 numbered requests/queries visible here**, with page/line locators, requested target, conflicting values, displayed response and unresolved inputs. The 29 February entries include 22 transcript entries, six personnel-statement entries with names omitted and one weather-orientation query; the May email has four. These overlapping instructions are not 33 independent errors, proven changes or corroborations of wrongdoing.

The most consequential entries are:

| Record | Values and displayed response kept side by side | What remains untested |
|---|---|---|
| Sector 55 radar start | Beginning inconsistent; asks whether 1249 is correct and asks for tape check/possible recertification; marked Corrected. F02: AEA1124 physical 4,15–17. |Previous header value, checked tape, final value and certification.|
| Sector 55 associate ordering |1301:06 versus1301:05 and1305:34 versus1305:33 reported out of order; each marked Corrected. F09–F10: physical 4,40–44. |Replacement timestamps and underlying clock/tape. These are not measured one-second clock errors.|
| TMU Arrival Director attribution |1256:36,1306:55 and1312:01 agency entries requested changed to Unknown; marked Corrected. F12–F13: physical 4,51–55. |Earlier labels, reason for uncertainty and native comparison. Unknown does not identify a hidden actor.|
| OMIC ending |Asked whether header should end 1344 to agree with page 26, tape check requested; marked Corrected. F16: physical 5,12–14. |Earlier header,26-page transcript and actual check.|
| OMIC attribution |1310:29 queried; response says changed to ZOB OMIC, no new legend entry.1333:51 requested changed to ZNY OMIC for consistency; marked Corrected. F17–F18: physical 5,16–21. |Earlier labels and evidence for speaker/agency assignments.|
| Eighth/radarTMU coverage |Add cardinal minutes1245,1246,1247 at start and1316 at end? Header already says1245–1316; requests tape verification, marked Corrected. Missing certification signature also marked Corrected. F19–F22: physical 5,27–39. |Minute markers are not proof extra audio existed, was missing or was recovered. Signed source certification and full transcript remain missing.|
| Personnel-statement cross-aircraft values |Six entries request lining out AAL11 and initialing. One also requests lining out12:42 where two accident times appeared. Each marked Corrected. F23–F28: physical 5,Section 11,49–64; fourth entry in image/58–60. |We have neither the underlying original/amended statements nor remaining call sign/time/reasons. Do not apply these historical directions to our preserved copies or infer which factual value was true.|
| Sector 42 correction after prior correction |May entry at1306:17 requests ZBW IGN; says an earlier requested correction to transmissions changed the agency. It now displays Correction made. M02: AEA1122 physical 1,43–47. |Previous versions, exact change and basis. The email gives a concrete iterative-correction trail; it does not establish why the earlier agency changed.|
| Weather-copy discrepancy |Reviewer says weather products upside down; response says not upside down in original/remaining ZNY-ARTCC-148 copies, followed by??. F29: AEA1124 physical 5,66–68. |Actual compared copies and assembly/orientation history. Both descriptions remain unresolved; this presentation issue does not demonstrate a timing error.|

Other entries concern memo recertification dates, DAL-TCAS/DAL2315,4511/5411 andLOF4511/LOF5411,IPTT/IPPT, page numbering and the May request to add DAL1043 after N90 LIB for a 1300:53 transmission. The ledger retains every requested value rather than silently choosing the proposed replacement. For queries where the sheet says only Corrected or Legend Corrected, we do not invent the final chosen spelling/time.

## Relationship to the already acquired operational records

The [two-page AWA940 OMIC memorandum](https://github.com/AveLyra/911-conspiracy-investigation/blob/191c27f34284bdbbf006db5bb2b41071125f19d7/investigation/broader-evidence/faa-omic-memorandum-2026-10-30/README.md) is datedFebruary 4, 2002, identifies ZNY-ARTCC-148/UAL175 and 1230–1344UTC. Here the February5 correction packet refers to an OMIC transcript of 26 pages and an ending 1344. This is a specific source link by case/position/end label; **it does not authenticate AWA940 as the exact completed correction, delivered enclosure or full 26-page transcript**. AWA940 itself contains no visible timecoded dialogue. A matching end label is not independent confirmation of its accuracy.

The [later Item16 inventory](https://github.com/AveLyra/911-conspiracy-investigation/blob/62a102da31cc82a7216dc41e60bed185a11c8d45/investigation/broader-evidence/faa-response-labels-2026-10-30/README.md) lists a 1245–1316 TMU transcript, and this packet's Eighth transcript asks about those same header endpoints. The earlier [AWA937/line1078 memorandum](https://github.com/AveLyra/911-conspiracy-investigation/blob/0584407dac2190a9f9514ee157124446e60672d5/investigation/broader-evidence/faa-tmu1078-source-2026-10-30/README.md) instead labels 1255–1316 and contains an AAL11 subject versus UAL175 work-file mismatch. Do not equate different TMU positions/ranges from shared organizational labels. The present packet does not resolve that mismatch or establish missing audio.

## Claim strength and competing hypotheses

**Directly established from images:** these released documents display the requests, conflicting tokens, status annotations and version/file references specified above. **Agency reports:** corrections received/made/posted. **Not independently established:** whether the requested tape checks and recertifications occurred, whether the resulting assignments/times were accurate, or which exact version reached final delivery. We have directly acquired the correction records, not an authenticated implemented set.

Routine quality control, cross-aircraft/template contamination, transcription/legend uncertainty, copy-assembly differences and substantive attribution/timing changes are possible explanations for different aspects. Their relative likelihoods have not been measured. Preserving explicit review and correction instructions is counterevidence to an inference that every alteration was concealed; it does not establish that the corrections were correct, fully disclosed or fully implemented. No record here proves deliberate falsification, coordination, attack involvement or a cover-up. There is no legal conclusion from these scans.

## Next records and acceptance tests — TODO, not a stop

| Open dependency | Needed discriminating record/test | Completion criterion |
|---|---|---|
| Exact version chain | Native two named Word attachments; full Change 2 document; complete referenced before/after transcripts for sector 55 radar28pages/associate29, ArrivalDirector12, OMIC26, radarTMU9, andMay sector 42 radar23/associate8 |Source/custody/version pins establish exact packages; compare every changed text/time/agency/date/certification while retaining old bytes. Page counts here are source references, not proof we possess those documents.|
| Tape-check claims | Referred recordings, channel IDs, preservation/certification logs, check worksheets and stable time references |Owner can test stated corrections against identified original signal and clocks; no such listening or timing test performed here.|
| Delivery and final approval | February posting/receipt history;May expedited-shipment enclosure manifest/receipt; final-review/release decision |Authenticated sending/receipt and exact approved version, not merely conditional email language or an icon.|
| Statement changes | Original/amended six statements and explanations/initialing history, reviewed locally under privacy controls |Compare AAL11/12:42 versus actual retained values and reasons; no inference from names or absent versions.|
| Related uninspected originals | [AEA1121/NARA7598359](https://catalog.archives.gov/id/7598359) and[AEA1123/NARA7598361](https://catalog.archives.gov/id/7598361), previously observed table entries |Read actual bodies within a new bounded protocol; they are locators, not assumed support. Not opened in this unit.|
| FAA2003/2006 trail | OriginalMay 2003 drafts/awareness emails, actual corrected QFR plus delivery, signed action/no-action/reasons and separate recommendation implementation/closure/applicable policy |These remain missing; a 2002accident-package correction is not their substitute.|

All five tracks and eighteen substantive acceptance criteria in the adopted work plan remain unfinished/partial. Telephone native carrier/operator/call-leg joins; recorder configuration/custody/paired output/clock anchors; authenticated materials specimens/native calibration/same-specimen tests; and steel preservation/native inventory/attribution/selection/transfer originals remain open. Existing technical tests are not relabeled unperformed, duplicated or completed by this source acquisition. No outreach, new request, fee or filing occurred.

## Revision-accountability checklist

| User/control requirement | Outcome/location | Verification/remaining issue |
|---|---|---|
| Seek underlying operational originals, do not repeat completed searches |Two directly observed official items; all six pages read; source table and chronology |Exact entity hashes/page counts and safe field anchors checked; neither native full transcript nor full Word/email chain obtained.|
| Preserve conflicting values and source links |33-row ledger plus chronology and prior-source comparisons |Images checked, no source updated/replaced; only proposed/claimed corrections reported.|
| Keep missing inputs as TODOs and proceed |Dependency table above; two uninspected companion locators |Specific follow-up records preserved without guessing content or treating absence as concealment.|
| Do not mix 2002 package, 2003 QFR, 2006 disposition or separate technical tracks |Opening, relationship section and TODOs |None of the 18 criteria closed; actual technical tasks remain with assigned owner.|
| Public privacy/provenance and identity |Safe notes/pins/verification only; original PDFs/rasters/full OCR/names/signatures/contact fields excluded |Publication must use documented AveLyra identity and verified exact remote; verified receipt is maintained separately.|
| Actual text diff against prior preserved version |[TEXT-CHANGES.diff](TEXT-CHANGES.diff) |This is a new dated additive unit: README/ledger/pins/code against absent-file baseline. All older reports/source files remain unchanged; diff is not a layout check.|

`verify_sources.py` verifies the exact two PDF entities/page counts and local visible OCR hashes/selected safe anchors. Its pass demonstrates input/locator integrity only, not historical truth, tape accuracy, correction implementation or native authentication. The manifest covers the safe publication files other than itself. Local acquisition and publication/handoff receipts remain separate from source evidence.
