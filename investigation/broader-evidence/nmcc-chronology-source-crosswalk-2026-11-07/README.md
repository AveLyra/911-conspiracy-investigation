# NMCC chronology: official source matching the handwritten numeric range

**November 7, 2026 — operational-record acquisition, TEL03/TEL04 and SOC-N09–N12.** The National Archives' declassified **ISCAP 2012-156, document 14**, supplied in two PDFs, contains the continuous visible Bates range **NCT0010874–NCT0010913**. It is a concrete candidate for the handwritten **10874–10913** reference in the [previously preserved appended notes, physical p. 10](https://github.com/AveLyra/911-conspiracy-investigation/blob/94fa752ab20806e44b5b4a4985bfd1fdd0c08af5/investigation/broader-evidence/telephone-soc-interview-notes-2026-11-07/README.md).

The numbers and operational subject support that association. The handwriting omits the namespace, and its author, date and intended reference remain unauthenticated. This is a source crosswalk, not proof that the note-taker used this exact version, that the account is accurate, or that any original record was destroyed.

## Acquired sources and complete identifier accounting

| Official source | Current acquired entity and identifier range |
| --- | --- |
| [Document 14, part 1](https://www.archives.gov/files/declassification/iscap/pdf/2012-156-doc-14-part-1.pdf) | **18 PDF pages**, **1,032,500 bytes**, SHA-256 **f4771aed5447b8bed585c5df3b8aedfae4964ed6a278d1e8619f65c36b2cd46d**; visible **NCT0010874–NCT0010891**. |
| [Document 14, part 2](https://www.archives.gov/files/declassification/iscap/pdf/2012-156-doc-14-part-2.pdf) | **22 PDF pages**, **895,117 bytes**, SHA-256 **8d9094709629ace8bfe3d985722141f40693a03f1841dd9fb0c5739b6d9cbfd6**; visible **NCT0010892–NCT0010913**. |
| [Gonsalves interview, ISCAP 2011-048, document 19](https://www.archives.gov/files/declassification/iscap/pdf/2011-048-doc19.pdf) | **2 PDF pages**, **964,808 bytes**, SHA-256 **d199e4aa2df504478744267103e9018c675bdd561f4acad444420181df7097ec**. Interview date **May 14, 2004**; declassification stamp **September 29, 2014**. |

All three native PDF response entities were saved from the official host with HTTP **200** on November 7, 2026. Document 14's first-page stamp gives **January 21, 2021** as its declassification date. The old classification markings and remaining redactions are preserved. This review does not reconstruct redacted content.

All **40 chronology footers** were visually checked. Their NCT values run consecutively with no repeated or absent value within this defined range. The second namespace is **NCTA000162726–NCTA000162765**, also consecutive. [SOURCE-PINS.json](SOURCE-PINS.json) records each physical-page mapping. This proves the observed identifier coverage of these released PDFs, not completeness of the historical log, its attachments, events, underlying data or original recording.

A strict text-layer extraction failed to read some labels even where the page image shows them. Its original results remain preserved separately. Manual readings were not silently filled from expected sequence or substituted into the extracted source text. Empty extraction results are not missing historical pages.

## Preserve the packet boundaries and footer dates

The first page prints **Page 1 of 36**. **Part 2, physical p. 18 / NCT0010909** prints **Page 36 of 36**. The next four physical pages form two separately paginated two-page blocks:

- **Part 2, pp. 19–20 / NCT0010910–NCT0010911:** printed **1 of 2 / 2 of 2**, footer date **5/22/2003**.
- **Part 2, pp. 21–22 / NCT0010912–NCT0010913:** printed **1 of 2 / 2 of 2**, footer date **5/29/2003**.

The main 36-page run also shows **5/22/2003** in the checked footers. The footer includes an HTML-file path; its ending differs between the main run and the two-page blocks. These fields are preserved as publication/source-generation leads. They are not authenticated creation or amendment dates, and do not establish an alteration, export sequence or reason for different forms. The parallel blocks remain separate; no deduplication or preferred version is applied. Their complete row-by-row equivalence was not tested.

## A specific FAA-call and recording trail

**Document 14, part 1, physical p. 1 / NCT0010874** has a row labelled **110900** reporting an NMCC call to FAA and information about the first World Trade Center event and American Flight 11. Other rows separately label NOIWON, a Significant Event Conference and transition to an Air Threat Conference. These are distinct printed entries; this review neither decodes/calibrates their time labels nor equates their telephone legs.

The **Gonsalves memorandum, p. 1, 9/11 section**, reports that he made a chronology observable from the DDO and ADDO positions, called FAA through the red switch, and believed the line was recorded at the **SOO station**. That supplies a concrete recording-system and source-log retrieval route. The memorandum supplies no recording, console/session identifier, custody receipt or actual recording-completeness result. It does not identify document 14 by Bates number, so the two chronologies are not automatically treated as identical.

Preserve the limiting material too. Page 1 records an initial recollection involving the World Trade Center and Pentagon and then explicitly says the recall was clarified against a log entry. **Page 2, final paragraph**, limits what could be linked to the FAA call beyond that entry and includes the interviewer's own inference. These are distinct layers: recollection, source consulted during the interview and interviewer interpretation. They are not independent corroboration or evidence of pre-impact knowledge of the Pentagon attack.

The memorandum also distinguishes his earlier FAA contact from conferences and connection efforts in which he said he was not involved. A belief that one call was recorded does not resolve the appended notes' separate unverified side-bar-recording account. Without common line/session keys and contextual provenance, those claims cannot be assumed to concern the same call.

## What remains TODO

- [ ] Authenticate the handwritten reference's namespace, author, date and assembly; identify the original source and exact version consulted.
- [ ] Obtain the native HTML/log/database and its creation, editing, export, delivery and retention history. Join the two-page blocks to the 36-page run without assuming they are identical versions.
- [ ] Obtain the SOO/red-switch recording, recording plan, channel/session logs, console configuration, copy/retention history and any actual negative search/disposition.
- [ ] Obtain Gonsalves's original chronology, interview recording/notes, and the log entry used during the interview; verify whether they join to document 14.
- [ ] Obtain original/consolidated notes and disposition records before evaluating the appended note-disposal claim. Nothing acquired here authenticates that claim or measures an audio gap.
- [ ] Retain the priority FAA corrected answer/receipt and signed disposition, native carrier/operator/caller joins, and the other work-plan inputs. No full-track completion is claimed.

## Actual scope and preservation

The acquisition and identifier census cover both complete chronology PDFs. Substantive reading was limited to the opening notification rows, the two-page-block boundaries/visible context and **both pages** of the interview memorandum. Forty footer strips and selected full pages were inspected; this is not a full substantive audit of all chronology rows or independent verification of their events.

[verify.py](verify.py) checks three source hashes and page counts, the consistency and coverage of the 40-entry manual ledger, and preserved predecessor hashes. It does not independently repeat the visual readings. Image checks establish preservation of the inspected representations; they do not automate handwriting/visual judgments or validate historical content. Raw PDFs, images, full text, private material and reconstructed redactions are excluded from the public derivative. Earlier sources, conflicting accounts, reports and history remain unchanged.
