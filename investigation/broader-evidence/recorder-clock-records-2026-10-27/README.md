# NTSB production and clock records: specific targets, an invalid excerpt label and five agreements

October 27, 2026 research unit; acquisitions continued October 28 UTC. Existing AUD016-A1/G01–G02, AUD016-A5 and AUD005–006 remain in scope. This operational-record addition preserves earlier work and does not independently authenticate an aircraft, recorder, clock or historical mechanism.

## New records and concrete retrieval targets

Five displayed page images of a [public copy of NTSB's July 17, 2003 production letter and inventory](https://www.scribd.com/document/12962758/List-of-NTSB-Documents-Provided-to-9-11-Commission) were acquired, hash-pinned and visually inspected. This is a third-party reader representation, **not an authenticated native agency production or recipient receipt**. The letter describes FBI control/authorization, production to the Commission, and exceptions concerning the Flight 93 CVR recording and an early transcript draft. It does not establish public availability of every underlying product. Page 1's hand-delivery designation is not independent proof of delivery.

The typed inventory has a February 21, 2002 print label. Its AA77 rows list seven products, including a RAPS project file, combined ATC audio/transcript and data tables. The final inventory page identifies radar CD-ROMs and a radar study describing correlations between clocks. Those are specific missing records to pursue; an inventory is not their contents. The July 2003 letter and the older typed status cells remain separately dated assertions. Handwritten additions are excluded from the typed-row count.

The [CDC-hosted scanned print of *Pentagon 9/11*](https://www.cdc.gov/niosh/docket/review/docket261/pdfs/261goldberg.pdf) was also acquired: 4,370,173 bytes, SHA-256 `4fd344667cacfd9b0c3bbfcec4282181ce209d3c132159a2bbca0e343825673d`, 144 PDF pages. Its pages show a printed Navy online edition; the cover identifies the 2007 historical volume. Appendix B explicitly labels its NTSB material as **excerpts from originals** (physical 109 / book 213). Hosting and byte identity do not transform that reprint into a complete original NTSB report or an independently sourced flight observation.

## Executed six-event label comparison

The same six event cues from the earlier FAA source-certification study were retained before computation. No event was dropped because it agreed or conflicted. The book's reprinted ATC table, physical 111 / book 217, was visually read, including a larger detail. The December radar and May associate values were freshly extracted from the same unchanged official FAA/NARA PDF entities used previously. Associations use words and sequence; they are not native event-ID matches.

| Existing event ID | Visible book label | December radar label | May associate label | Conditional comparison |
| --- | --- | --- | --- | --- |
| A1, check-in | 8:40:13 | 1240:13 | 1240:13 | Equal after adding four hours to book label |
| A2, squawk instruction | 8:40:15 | 1240:15 | 1240:15 | Equal under the same convention |
| A3, climb instruction | **8:43:81** | **1243:51** | **1243:51** | Book seconds invalid; no numeric delta assigned |
| A4, climb readback | 8:43:55 | 1243:55 | 1243:55 | Equal under the same convention |
| A5, right-vector instruction | 8:47:16 | 1247:16 | 1247:16 | Equal under the same convention |
| A6, ten-right readback | 8:47:20 | 1247:20 | 1247:20 | Equal under the same convention |

The computation found **five valid labels agreeing under that conditional four-hour convention and one invalid seconds field**. The four-hour addition is a declared label-convention assumption, not a fitted historical clock calibration. The excerpt does not supply the independent synchronization worksheet, native audio or a demonstrated identity with the FDR report's separately referenced Time Correlation Report. No historical offset was selected to produce an impact or alternative trajectory.

The printed `8:43:81` is visible in the scanned source, not merely an error introduced by our OCR. Its source, stage and cause remain unknown. It is a low-weight transcription/version-quality lead; it does not demonstrate altered underlying audio, FDR data, radar or deliberate manipulation. Native NTSB text, the original Navy edition and the underlying recording could locate the stage at which the value appears. Preserve all versions rather than substituting the FAA value into the book.

Our OCR separately misread A5 as `8:47:36`; the page image and enlarged detail show `8:47:16`. Both the OCR artifact and image are retained. That is our extraction discrepancy, not a second historical clock observation. The checker never converts the book's 81 seconds into a later minute or silently changes it to 51. Three strict-parser controls passed; source hashes and frozen inputs remained unchanged. [RESULT.json](RESULT.json), [ANCHOR-INPUTS.json](ANCHOR-INPUTS.json) and [compare_labels.py](compare_labels.py) expose the computation and its limits.

## Quantities and source dependence

The image-based transcription [PRODUCT-ROWS.csv](PRODUCT-ROWS.csv) contains **37 typed product rows**: 35 marked complete, one marked approved but not yet released, and one awaiting FBI approval. Counts describe the typed inventory, not 37 files, 35 independently verified investigations, recipient possession, current availability or a later release decision. Seven rows concern AA77; four concern several general categories including FAA source tapes/transcripts and ACARS. The complete section/status counts are in RESULT.json. Typography and line wrapping are collapsed in the manual transcription; page images govern readings.

The July letter's production assertion, inventory statuses and our present nonacquisition are three different observations. A later production claim does not erase earlier pending cells; earlier cells do not establish continued nonrelease in July 2003. Neither establishes destruction or concealment. The actual enclosures, transfer/receipt record and native media directory are needed to test completeness.

The book's flight-path excerpt gives an impact label of 9:37:45, while the [previously held FDR factual report](https://www.ntsb.gov/about/Documents/AAL77_fdr.pdf#page=4) describes its last recorded datum as 9:37:44. These refer to different claimed events. Keep both without calling their difference a demonstrated clock error or using either to calibrate the archived candidate's terminal samples. The historical agency CSV, actual readout settings/error logs and independent common-event anchors remain missing.

## Original-record queue and current technical state

1. Actual AA77 RAPS project CD contents, file list, hashes, readout/export versions/options and error/fault records; the listed data tables and their version relationship to the factual report attachments.
2. The listed all-aircraft radar study, original radar CD-ROMs and their clock-correlation calculations; establish whether this is the same document as the FDR report's Time Correlation Report, without assuming that join.
3. The combined AA77 ATC waveform/transcript and its source/channel map, offsets, editing history, continuity and clock anchors. A common time-base description is not an independently checked calibration.
4. July 2 request, actual July 17 enclosures, transfer/receipt records and the governing nondisclosure instrument. The public letter's description is not the complete instrument or a ruling about present access.
5. Native Navy/NTSB versions behind the invalid excerpt label; trace the reprint rather than repairing it or treating it as the original recording.

The technical owner's newer raw-frame and page/field test records were inspected before choosing this unit. They document a raw-format candidate and completed calculations; older parent summaries saying no raw input was acquired must not be repeated as current status. We did not rerun those calculations. Their historical custody, format/error-policy, sensor and civil-clock qualifications remain. Materials work similarly remains published-data/conditional analysis until the native same-specimen inputs and measurements are available. These are separate dependencies, not completion claims.

## Scope, preservation and publication

All five product-reader pages were inspected. Of the 144 scanned CDC pages, physical 1–4, 100 and 109–114 were visually inspected: **11 pages**, plus a detail of page 111. The pinned physical page 4 image of the separate official FDR report was also re-viewed. An initial literal-text check failed because that scanned page has no embedded text; the failure was preserved and the image checked. Some additional book pages were rendered for location but not read. No full-book/full-appendix review or OCR of all pages is claimed; only page 111 was OCRed. The appendix's excerpt qualifier was explicitly inspected. Unrelated names, casualty lists and contact/signature material are not adopted into the public analysis.

Twelve indexed queries reached the cap; no stopped endpoint, blocked host, failed TLS route or successful decoder calculation was retried. Ordinary read-only acquisition preserved the five public JPEG entities and the CDC PDF. Temporary asset queries, raw headers, personal/contact material, raw captures and full source images/PDF are excluded from the public payload. Original bytes remain unchanged locally; redundant reviewed notes, pins, row/anchor inputs, code/results, checklist and exact text diffs form the public addition. No source value is normalized away. No outreach, personal mailbox, fee, new request/filing, private push, source replacement, deletion or history rewrite occurred. All five original-record tracks remain active.
