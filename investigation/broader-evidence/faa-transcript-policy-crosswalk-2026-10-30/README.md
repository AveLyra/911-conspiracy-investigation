# FAA transcript policy: what the cited rules can—and cannot—establish

October 30, 2026. The cited order gives precise meanings to transcript scope, timing remarks, uncertainty footnotes and copy handling. **These provisions identify better original-record tests; they do not determine whether the FAA's particular corrections were accurate or implemented.** All conflicting case values and earlier reports remain preserved.

## Primary sources and actual reading

| Retained edition | Source | SHA-256 | Actual page images read now |
|---|---|---|---|
| August 16, 2000 FAA Order 8020.11B; university-hosted primary government document,389 pages |[Retained source URL](https://libraryonline.erau.edu/online-full-text/books-online/1177.pdf)|`4a079eef3618704785a50283ca6a28fb26be694191570a7f0b8549893ef8e3cf`|Physical51,58,59,60; printed 315,322,323,324|
| FAA-hosted copy including May 12, 2003 Change 1,397 pages |[Retained source URL](https://www.faa.gov/documentlibrary/media/order/8020.11b.pdf)|`8144fe5bdb3badb2131a000875d0a7709036c2b5bcb4f0e804d68a4a0cbe00a4`|Physical2,3,51,60,61,62; cover,control chart,printed 317,326–328|

Both files were already acquired in the earlier preservation study. Current full hashes were checked; new redundant copies were saved to the verified Intel store while retaining the existing originals. There was **no network redownload**. One tested legacy Intel-relative file was individually absent; the verified store remained available and the existing research copy matched its pin. No outage, suppression or loss of the source is inferred.

Only the ten listed page images were read now, not all 389/397 pages. Pinned earlier full-text extractions were searched as locators; new selected-page text was extracted with pypdf 6.10.0 after visual inspection. [SOURCE-PINS.json](SOURCE-PINS.json) records physical/printed pages, exact selected-text lines/hashes, clause boundaries, comparisons and edition limits. Four nonfatal Fontconfig warnings appeared during rendering; all ten selected images were legible and read. No source was repaired or overwritten, no redacted case-text layer inspected, and no audio/listening/decoder/clock test performed.

## Policy-to-record findings

The [thirteen-row crosswalk](RECORD-CROSSWALK.json) links the provisions to the [preserved package-correction review](https://github.com/AveLyra/911-conspiracy-investigation/blob/a42d0956202dacc3b971d21f479966d56fefcd60/investigation/broader-evidence/faa-package-version-chain-2026-10-30/README.md). Reading the policy does not replace the missing underlying transcripts, recordings or case-specific directions.

- **Full versus partial concerns selection scope.** Paragraph77a, 2000 physical 58/printed 322, defines the partial transcript around subject-aircraft communications over the stated five-minute-before/after window. A full transcript includes all recorded communications at that operational position over the defined period, regardless of source. Positions are transcribed separately unless integration is requested. Thus a Partial-to-Full label instruction is not itself a measurement of missing duration, and two controller positions are not assumed to have identical content. Whether the actual files meet either definition remains untested. The cited paragraph 76a NOTE and case-specific requests were not newly read here.
- **A first-page memorandum and later certification date are prescribed fields.** Paragraph77d(1), 2000 physical 59–60/printed 323–324, specifies a memorandum first page, certification/signing date, position/UTC coverage and legend. Certification is by the person who transcribed, not automatically a manager. This qualifies what can be inferred from a memo-shaped entity or multiple date fields. It does not supply the missing 26-page OMIC orfive-page 1078body, explain any aircraft/case/footer mismatch, or authenticate any signature/date.
- **The timing method has an explicit record location.** Paragraph77d(3)(a), 2000 physical 60/printed 324, provides for beginning-of-transmission times when a time-announce system exists; otherwise the certification contains a timing-method remark. Those remarks, original time channels and timing/check worksheets are concrete targets for the written−60/+4 second disagreements. No actual offset was measured here. A missing remark is not automatically a violation without knowing whether its condition applied.
- **The uncertainty footnote is conditional.** Paragraph77d(4),same page, distinguishes marking unintelligible sound from interpreting a garbled word/portion. The interpretation is parenthesized/asterisked and accompanied by a note about uncertainty. This is not a universal footer certifying every timestamp or a general test for whether any transcript is complete. The source's declined footnote for sector 55 and requested footnote for line1078 remain distinct, unresolved judgments; inspect the actual marked passages and supporting recording to test them.
- **Copy and original handling are different.** Paragraph77c, 2000 physical 59/printed 323, provides for transcription from a recording copy to protect the original, with original available for checking. Paragraph72c(11),physical 51/printed 315, addresses personal-number sanitization from copies, with a specified exception and retention of those numbers in original documents. These are source-generation/copy requirements, not proof of what happened in this case or authority to alter our evidence.
- **Package numbering differs without proving missing content.** The 2000 order labels Form 8020-3, personnel statements and weather as Sections 11/12/13; the 2002 review uses 10/11/12. The 2003 page also lists transcripts as Section 10, while the packet review uses 9. Preserve both numbering schemes; obtain the underlying case index and organization instructions. No section deletion, governing exception or violation is inferred from the labels alone.

## Edition comparison: preserve differences, do not backdate a later rule

The 2003 page-control chart,physical 3/printed 2, calls for replacing printed 301–346 with 301–350 among other pages. Both original files remain unchanged here. Seven regex-delimited selections were compared after collapsing whitespace **only**; raw clauses and hashes remain preserved. No dehyphenation, glyph repair, punctuation substitution or case-value reconciliation was used to make a match.

| Selection | Recorded comparison result | Scope |
|---|---|---|
| Personal-number note 72c(11) |Matches after whitespace collapse |Only the selected note, not the changed form heading or whole page.|
| Scope 77a |Literal extracted differences retained |Includes line-end `communica-`/`tions` versus `communications`, and `AAI-100` versus extracted `AAI-lOO`; no office-change inference.|
| Recording-copy paragraph 77c |Literal difference retained |Extraction has `separately.` versus `separately,`; no punctuation normalized to force equality.|
| Certification-date 77d(1)(b) |Matches after whitespace collapse |Selected date instruction only.|
| Time-announcement/method 77d(3)(a) |Matches after whitespace collapse |Does not establish actual time equipment or compliance.|
| Digital/cardinal-minute77d(3)(b) |Different; explicit2003 addition |Later text includes transmissions beginning on a minute and permits grouped quiet minutes under stated conditions.|
| Garbled-interpretation/footnote selection 77d(4) |Matches after whitespace collapse |From uncertainty trigger through footnote text, not a claim the entire paragraph/chapter is identical.|

The 2000cardinal-minute instruction provides an exception when a transmission extends through a minute. The 2003 revision explicitly includes a transmission beginning on a minute and allows optional grouping after four or more quiet minutes, with prescribed delimiters and boundary-minute entries (2003 physical 62/printed 328). The nearby spacing instructions also expand in that edition. **Do not apply those later details retroactively to the 2002 review without establishing the applicable version and directions.** A documented public policy revision is not evidence of a case-specific cover-up or an explanation of the particular timing differences.

Initial clause-selection attempts stopped on a source comma inside the Date quotation and a line break in the final footnote. Both failed attempts, selected source text and actual script diffs were retained; delimiters were repaired without changing a source value. The completed comparison's True/False results are observations, not pass/fail judgments about historical compliance.

## Next original records

The already captured [official finding aid](https://www.archives.gov/research/foia/faa-finding-aid-96-107),rows 3125–3130, provides the following **uninspected locators**, retained in SOURCE-PINS.json:

- [AEA1130 /7598367](https://catalog.archives.gov/id/7598367), labelled Completed Accident Package: priority route to the actual package/index and enclosures.
- [AEA1126 /7598364](https://catalog.archives.gov/id/7598364), labelled Full Transcript for sector 55,1248:26–1320:21 UTC, but filename says MEMO: inspect the body before claiming a full transcript.
- [AEA1125 /7598363](https://catalog.archives.gov/id/7598363), May 3 correction-memo label; [AEA1127 /34911617](https://catalog.archives.gov/id/34911617), shipping record; [AEA1128 /7598365](https://catalog.archives.gov/id/7598365) and[AEA1129 /7598366](https://catalog.archives.gov/id/7598366), receipt-email labels. Dates, relationship, enclosures and actual receipt remain unverified from the bodies. Shipping/contact/personnel numbers are excluded here.

No completed search was repeated or new broad query made. Locator reuse does not establish target acquisition, reading, completeness or independent corroboration. Earlier receipt chains may simply repeat in another scan.

TODO: obtain exact original/corrected transcripts with timing-method and uncertainty markings; certification/check history; original→copy→transcript mappings and recording configuration; actual missing sector 42page2/enclosures and receipt; native May 14 attachment binaries; case-specific edition/exception/index directions and the referred paragraph 76a NOTE. Keep the actual May 2003 draft/corrected QFR/delivery, signed action/no-action/reasons and separate recommendation outcomes open. This policy unit does not establish those outcomes.

## Accountability and acceptance

| User/control point | Outcome and evidence | Remaining limit |
|---|---|---|
| Inspect available originals and relevant policy |Two held source hashes verified; ten selected images actually read |Partial policy scope; no new whole-order or case-compliance claim.|
| Preserve conflicts and contrary explanations |Source files, all selected raw values, seven comparison outcomes and thirteen-row crosswalk |No controlling case value selected; source reports remain distinct from proven events.|
| Keep missing inputs as TODOs, advance available work |Specific certification, uncertainty, copy-chain and catalogue targets above |No substantive eighteen-item criterion closed.|
| Deliver exact text changes and source links |[TEXT-CHANGES.diff](TEXT-CHANGES.diff), new dated unit against absent-file baseline |Previous reports and original bytes unchanged; diff is separate from visual reading.|
| Publish only eligible reviewed material as AveLyra |Safe original notes, selected policy comparisons/pins/code/results |No raw source/rasters/fulltext/speech/personnel/contact/signature/private-case material. Separate receipt must verify identity/ref/all published file bodies.|

All five tracks remain active/partial: FAA native correction/disposition, telephone carrier/operator/call-leg originals, recorder authenticated configuration/custody/paired-output/clocks, materials authenticated specimen/native calibration/same-specimen joins, and steel native preservation/transfer/inventory/attribution records. Prior technical tests are preserved within their actual limits. No outreach, new request/fee/filing, private push, deletion, source overwrite or history rewrite occurred. Source integrity, matched clause text and publication do not complete the substantive goal.
