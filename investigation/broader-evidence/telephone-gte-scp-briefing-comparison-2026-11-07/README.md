# GTE duration column: differing text extractions and a conditional table comparison

November 7, 2026 Eastern · **TEL02–TEL03 / AUD016-A1**.

**The same saved carrier PDF produces different numeric strings under three passive text-extraction methods.** A selected-column inspection also records overlapping non-displaying text entries. Separately, arithmetic using an explicit manual reading of the image gives nine positive SCP figures matching the Commission table's nine numeric length labels.

These are source-representation and comparison findings. They do not establish a change in the original carrier records, successful conversations, caller identity, calibrated timing or fabrication. Every extraction is retained without choosing a controlling replacement.

## Sources and reading scope

- **Carrier print:** the held **41-page**, **1,597,265-byte** Team 7 Box 13 GTE scan; SHA-256 **`4e8a891c1b18ed60587d99d50222c7a8bdca2b5e8dbb56c544e2a3b43abd3d8b`**. This unit reads the **SCP DUR** column on physical **p. 13**, entries **1–11**, within PDF points **[265,70,310,210]**. The source is a [public Commission ZIP mirror](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip), not a native workbook. [Exact member and original acquisition](https://github.com/AveLyra/911-conspiracy-investigation/blob/b4b1ce31bf517f0c57e42f175667b7b3a5cd475b/investigation/broader-evidence/telephone-request14-fax-mirror-2026-11-06/README.md).
- **Commission memo:** the previously acquired official [UA175 May 13 briefing, NAID 2609807](https://catalog.archives.gov/medialz/legislative/rg-148/2524787/t-0148-911MFR-00216.pdf#page=3), **515,215 bytes**, SHA-256 **`e581efca33a84473d2f08f577f328123759b176d2513c47adc1ba958bd9c980c`**. Physical **p. 3** was reread in full, including its definition bullets and eleven-row table. It is an official released scan of a briefing record, not a recording or vendor specification.

Neither PDF was newly downloaded. The [October 29 review](https://github.com/AveLyra/911-conspiracy-investigation/blob/681797a20a39d8c30e367c2220be15a191e3a409/investigation/broader-evidence/telephone-may13-briefings-2026-10-29/README.md) already documented the briefers' field explanations: Connect as setup time, SCP as connected duration, and operator involvement separately. Those are attributed explanations already held, not new discoveries or authenticated vendor/error rules. The new work compares the raw print's selected column and tests its extraction.

## Conflicting representations preserved verbatim

| Representation / operation | Selected output in returned order |
| --- | --- |
| Manual image reading, carrier p. 13 | `99, 75, 22, 0, 31, 0, 25, 27, 9, 60, 192` |
| PyMuPDF 1.27.2.2, numeric words selected by word origin | `99, 75, 2, 2, 99, 75, 31, 0, 25, 27, 9, 60, 192` |
| pypdf 6.10.0, selected numeric text chunks | `99, 75, 22, 31, 0, 25, 27, 9, 60, 192` |
| pdfplumber 0.11.8, selected numeric words | `9999, 7755, 2222, 31, 0, 25, 27, 9, 60, 192` |

These comprise **11 visually transcribed entries**, **13 selected PyMuPDF words**, **10 selected pypdf chunks** and **10 selected pdfplumber words**. They are different units and selection/grouping methods, not competing counts of calls. Their regions, parameters, full selected PyMuPDF words including nonnumeric material, and coordinates are preserved in [SOURCE-PINS.json](SOURCE-PINS.json). The pypdf filter excludes compound chunks; its count is not a census of all text entries.

In particular, **`9999` is a returned text string, not a finding of a 9,999-second call**. No parser output was deduplicated, repaired, imputed into another output or used to replace the image reading. The numeric-only selections omit nonnumeric strings in the region and cannot stand in for a complete field transcription. Causes and historical significance remain unresolved.

## Passive PDF-internals observation

In the selected column, PyMuPDF's text trace reports **two spans each** for the strings **99**, **75** and **22**, using **Times-Roman** and **Helvetica**, at overlapping positions. All six selected spans have **type 3**. A separate pypdf parse of the page's root content stream records **59 `Tr` instructions**, each with operand **3**.

The library's [official documentation, get_texttrace Details 2](https://pymupdf.readthedocs.io/en/latest/functions.html#Page.get_texttrace), defines type 3 as nonpainting/ignored text, corresponding to PDF rendering mode `3 Tr`. This is a technical rendering property. It supplies no evidence of secrecy, intentional deception, the person/software that added the text, the order of processing, or the original carrier data. We do not select a historical cause for the differing outputs.

The diagnostic used passive readers only. No PDF cleaning, OCR replacement, redaction reconstruction, source editing or script/attachment execution occurred. A direct documentation-body request returned **403** without a saved body; the relevant definition was read through the official web representation. No unavailable body hash is invented.

## Conditional numeric comparison with the briefing table

The stated manual carrier transcription contains **nine positive figures and two literal zeros**. The unchanged earlier manual MFR input, reread against p. 3, contains **nine numeric length labels and two No Conn labels**.

The nine positive carrier figures and nine numeric memo lengths have the identical sorted multiset:

`9, 22, 25, 27, 31, 60, 75, 99, 192`

This computation is **conditional on those explicit manual transcriptions**. It is not automatic glyph validation. It does not pair the two zeros with either No Conn row, convert No Conn to zero, assign a caller or establish a call-key/clock join. Row order differs between the two lists, and matching length alone is not an authenticated identity link.

The agreement is contrary evidence to a claim that the selected printed figures and the briefing's numeric lengths are wholly inconsistent. Its strongest limitation is source dependence: the briefing describes work from carrier records, so matching numbers are not independent corroboration of the conversations. The differing extractor outputs also show why a numerical comparison built from unexamined extracted text would require its own validation.

## What remains unresolved

- Obtain the original native carrier export/workbook, applicable dictionary and error/default rules, sheet/print relationships, authenticated versions and database-to-report transformation records.
- Obtain earlier PDF/release versions or creation/processing records to test the origin of the overlapping text and different representations. Those possible histories remain untested; this saved PDF cannot date them.
- Preserve the original zeros, No Conn wording, differing parser strings and prior clock, conversion, page-count and name-token observations separately. No historical value or explanation is selected here.
- The [prior eight-key subset join](https://github.com/AveLyra/911-conspiracy-investigation/blob/2393415a5651d182109db93d2ba61fb9ebeefd11/investigation/broader-evidence/telephone-gte-printed-table-join-2026-11-07/README.md) remains a result of its stated rule. This new example does not validate every key's glyph reading or establish the intervening time/duration/caller joins.
- Keep AA77's operator/office records, Keyton and September 20 inputs separate. The FAA corrected QFR/receipt, signed disposition and recommendation outcome, steel chains and recorder/materials owners' dependencies remain open.

All five work-plan tracks and eighteen original requirements retain their scope. No full original-record acceptance criterion is closed. No cover-up, source alteration, attribution or clock conclusion follows from this step.

## Reproduction and preservation

[verify.py](verify.py) checks both PDF byte identities, reproduces the stated extraction operations and passive operator/trace observations, and computes the conditional numeric multiset comparison. It does not certify manual image reading, source independence, historical data accuracy or a call's identity/outcome.

Both original PDFs, the unchanged prior manual input, reading aids, failed first selection, every subsequent output, protocol revision, checklist and text diff remain preserved in native research. The public derivative contains only original research, safe numeric/header observations, source pins and owned verification code. No raw scans/crops, call IDs, phone/card/account/customer values, private correspondence or strategy are published.
