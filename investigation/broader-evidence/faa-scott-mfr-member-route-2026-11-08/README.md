# Scott memorandum candidate: preserve the filename/body mismatch

November 8, 2026 · **B129 / PD01–PD04 / FAA01**. A specifically named Commission ZIP member was acquired and inspected. Its filename identifies a Scott interview record; its actual PDF is a one-page withdrawal notice whose displayed fields do not match that description. **The six-page Scott memorandum remains unacquired. The notice's association with Scott is unverified.** [Official MFR index](https://www.archives.gov/research/9-11/commission-memoranda.html#:~:text=2609763) · [Public ZIP mirror](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip).

## Three observations retained separately

| Source | Actual observation | Limit |
|---|---|---|
| NARA's MFR index, rendered line283; legend lines61–66 | **NAID2609763**, **Scott, William A.**, **CONR**, **2/4/2004**, **6 pages**, status **O** (open), box **4** | Catalog metadata; it does not authenticate this ZIP member or notice. |
| Preserved ZIP index and verified member header | Filename **MFR NARA- T8- DOD-CONR- Scott William A- 2-4-04- WN- 00177.pdf**; declared **164,126 bytes**, CRC32 **64d4d002** | A descriptive mirror filename is not the underlying interview's content or an official NAID crosswalk. |
| Acquired PDF, physical p.1 | **WITHDRAWAL NOTICE**; **RG148**, box **00007**, folder **0002p**, document **4**; document date **11-18-2003**; type **Memo of Conversation**; classification-review-pending folder/subject | No Scott name is visible and From/To fields are blank. It cannot presently serve as the missing six-page interview memorandum. |

The notice also displays **NND161**, withdrawn **11-17-2008**, retrieval **161 00007 0002p 4** in the image, and **SystemDocID5803**. These are lookup fields on this notice, not authenticated identifiers for the Scott interview. The extracted line17 instead renders the retrieval field as **RETRIEVAL #:16100007 0002p4**; both representations remain preserved without selecting a preferred form. The notice's Pages field contains overlaid/handwritten marks: visually, an apparent marked-over **0** and a mark resembling **9**; the existing text layer renders the field as **y''1**. Preserve those uncertain representations without assigning a corrected page count. The file itself has **one PDF page**. Reviewer initials/signature are excluded from publication.

Do not equate the notice's date, page field or box with the NARA index's Scott fields. Do not infer that the Scott memorandum was restricted, subsequently opened, removed, replaced or deliberately misdescribed. The relationship and cause of the discrepancy remain unresolved. The ZIP's title includes January14,2009; that label does not authenticate a capture date or establish a release chronology.

## What was acquired and actually checked

The saved **8,363-member** ZIP index was reused; no full archive was downloaded. An exact filename match selected this candidate. A single bounded request returned **HTTP206**, with the expected Content-Range and archive ETag. The ZIP local header matched the indexed name, method, lengths and CRC; decompression and the resulting PDF's CRC/length/magic passed. The **164,126-byte** PDF has SHA-256 **1cb051a2f6874f7e9cf6a0466f5b5ef988df875612b437d6961d4f248921354a**. These integrity checks establish the bytes obtained from the named member; they do not validate its descriptive filename or governmental provenance.

Both the PDF reader and renderer reported one page. That whole page was visually read. The standard catalog `/Names /EmbeddedFiles` and catalog/page `/AF` checks found no corresponding entries; this bounded structure check does not rule out every possible hidden byte or external counterpart. It did not recover an attached six-page memorandum. No original interview audio, native authoring file or agency scan was obtained. [Exact source, range, hash and field locators](SOURCE-PINS.json).

The first render attempt encountered a sandbox write restriction after the media-store guard succeeded. Authorized rendering to the same guarded store subsequently succeeded. This was a local execution issue, not evidence concerning historical custody or suppression. Source bytes, the initial failure, extraction and rendered derivative remain preserved unchanged; raw PDF/image/range-response bytes and headers are excluded from publication.

## Consequences for the investigation

The missing-source status is unchanged, but this specific mirror candidate has now been tested rather than accepted by filename. The retrieval target remains the actual six-page **NAID2609763** memorandum, with its original title/header/date, page sequence, source scan and release/version history. Obtain the original mapping or scan behind this member and the notice's SystemDocID5803 entry before associating the two. No account is selected as controlling and no explanatory hypothesis is treated as tested.

The **23-page ISCAP handwritten notes** remain a separate acquired source; they are not substituted for the missing six-page memorandum. The five-page archival hearing charts acquired in the [preceding study](https://github.com/AveLyra/911-conspiracy-investigation/blob/38621ff87ec3448b1f9f8e47de84ac39ecbb4888/investigation/broader-evidence/faa-scott-archival-chart-comparison-2026-11-08/README.md) remain acquired. Their selected-label agreement, the chart/transcript/host differences and the latest Marr AA77-call qualification remain preserved; none is resolved by this withdrawal sheet.

Keep native projected-deck/revision/approval/dispatch records, the February23 revised chronology/transmittal, actual FAA corrected QFR and recipient acknowledgment, signed administrative outcome and recommendation-specific dispositions as TODOs. All five tracks and eighteen broad original-record/test groups remain open. This is an original-source access/provenance finding, not a new operational timing test or evidence of conspiracy. Earlier records are unchanged; [exact comparative text diff](TEXT-CHANGES.diff).
