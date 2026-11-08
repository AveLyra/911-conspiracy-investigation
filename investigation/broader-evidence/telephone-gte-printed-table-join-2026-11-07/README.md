# Printed GTE tables: partial key join and unverified fields

November 7, 2026 Eastern · **TEL02–TEL03 / AUD016-A1**.

**Eight identical call-key strings can be joined between two separated pages of the held carrier scan. Three literal `#NAME?` entries also appear on another page.** This is a limited documentary/data-quality result. It does not establish caller identity, complete call counts, field semantics, native workbook accuracy or fabrication.

## Source and actual scope

The source is the already preserved **41-page**, **1,597,265-byte** Team 7 Box 13 GTE PDF, SHA-256 **`4e8a891c1b18ed60587d99d50222c7a8bdca2b5e8dbb56c544e2a3b43abd3d8b`**, from the public [January 2009 Commission ZIP mirror](https://archive.org/download/911datasets/NARA_9-11_Commission_Records_Released_Jan_14_2009.zip). Its exact member path, byte offset, CRC, page references and original acquisition date are in [SOURCE-PINS.json](SOURCE-PINS.json). This unit reused those bytes rather than downloading another copy. A scan is not the native carrier database, workbook or email.

The [earlier review](https://github.com/AveLyra/911-conspiracy-investigation/blob/b4b1ce31bf517f0c57e42f175667b7b3a5cd475b/investigation/broader-evidence/telephone-request14-fax-mirror-2026-11-06/README.md) established wrappers, page-count differences, attachment references and receipt/version targets. This supplement examines previously untested table content. Human image reading covered physical pages **1, 2, 3, 5, 12 and 13**; mechanical header/token extraction covered pages **1–14**. It was not a full 41-page visual or call-by-call audit.

## What the test establishes

| Observation/test | Result | Limit |
| --- | --- | --- |
| Page 1, item and call-key region | **11 visible item rows**. The frozen strict word rule accepts **9** key strings. | Visible rows, accepted text-layer strings and successful calls are different quantities. No flight-wide count follows. |
| Page 13, call-key region | The same strict rule accepts **9** strings. | OCR/word segmentation, page visibility and region selection limit the subset. No missing-call claim follows from rejected/unreadable positions. |
| Exact equality join | **8** accepted strings occur on both pages; one accepted string on each page is outside that intersection. | Equality verifies a connection within these printed representations. It does not prove person attribution or historical event accuracy. The unmatched parsed subsets are retained; their cause is not resolved or corrected. |
| Page 3, right-hand name-expression field area | **3 literal `#NAME?` tokens**, seen on the image and reproduced from its text layer. | Their generating application, formula, processing stage and effect remain unknown. A printed token does not prove an error in the underlying carrier record or identify who introduced it. |
| Page 12 versus page 1 | Page 12 shows **2 data rows**, versus the **11 item rows** on page 1. | This defeats a blanket assumption that every page has the same row positions. It does not establish that particular adjacent pages cannot align under a verified rule. |

The name-expression header's extracted text includes **`CCS.NAMEIICHR(95)`**. The image separator has vertical-bar/letter-like ambiguity at the inspected scale. Both the extraction and the reading uncertainty remain recorded; no corrected source header is adopted. This is a reading limitation, separate from the directly visible three tokens.

The strict key rule was frozen after the layout pilot, before the count computation: **`^(20010911[0-9]{6})(?:$|[^0-9])`** at the start of an extracted word, within the two specified page regions. Whole raw words remain preserved locally. No digit was repaired, merged numeric string split, masked key completed or preferred OCR value substituted. The test rejects duplicate accepted keys within each selected region. It is deterministic and uses these already selected pages; it is not a blind or independent validation.

## Timing and duration remain unresolved

Page 2 displays date/minute-time fields. Page 5 displays **`DURATIONCONNECT`** and **`DURATION OPERATOR`** headers; page 13 separately displays **`SCP DUR`** and a truncated **`DURATIO`** header. Their coexistence makes field definitions and exact row linkage necessary. It does not, by itself, make the values contradictory or explain why fields differ.

The page 1/page 13 key match does **not** supply a key on every intervening page. No row-order join to page 2 times or page 5 duration values was accepted. No seconds conversion, clock fit, caller match, completion classification or comparison with the court animation was performed here. In particular, these United Airlines tables cannot determine the meaning of Flight 77's separately disputed zero-duration row.

The strongest contrary evidence to a sweeping unreliability claim is that eight key strings match exactly across separated pages. The strongest limitation on attributing the error-looking tokens to a historical processing mistake is that in this review only the later reproduced print is available: native formulas, exports, field dictionaries and version joins have not been recovered. Neither result establishes alteration, concealment or conspiracy.

## Next discriminating records and TODOs

- Obtain the native workbook/database export, sheet and column definitions, print settings and row/child-table relationships. Test whether the two-row and eleven-row regions describe different record types rather than forcing a common row order.
- Locate the original values/formulas behind the three `#NAME?` positions, with an authenticated version history. Compare the carrier export, CACI processing and later print without presuming where the tokens arose or whether they affected attribution.
- Join printed keys to the November, March-corrected, Appendix A-3 and July versions using original stable identifiers. Retain the prior conversion, delivery-date, clock-label and page-count records unchanged.
- Obtain the carrier/operator event definitions, original timestamps and time-zone/calibration records before interpreting any connect, operator, SCP or other duration field. The separate AA77, Keyton, office-switch and September 20 inputs remain TODOs.
- FAA's actual corrected QFR/delivery acknowledgment, signed action/no-action and recommendation-disposition chain also remain TODOs. This telephone step does not replace them or the recorder/materials owners' unperformed tests.

All five tracks and the eighteen original requirements retain their scope. No full original-record acceptance criterion was closed. This is partial table-linkage testing of an available source, not completion of the investigation.

## Verification and preservation

[verify.py](verify.py) checks the PDF hash/page count, frozen key-region parsing, duplicate rejection, exact join and three literal tokens. It prints aggregate results only, with no raw call, phone, customer or payment values. A pass reproduces the stated text-layer observations, not the human readings or historical claims.

Native research retains the unchanged source and local reading/key details, diagnostic images, protocol, frozen rule, checklist and text diff. The public addition contains original research notes, safe source pins and owned verification code. Raw scans, crops, billing/customer details, private case correspondence and strategy are excluded. Earlier sources, reports and unresolved values remain unchanged.
