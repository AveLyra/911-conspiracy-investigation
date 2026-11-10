> **Historical research:** This document records the September 2026 review, not a fresh acquisition or instruction. Some local file links are marked as unavailable in this package. See the [publication note](README.md).

# Source and edition inventory

Acquisition date: 2026-09-09 America/New_York (2026-09-10 UTC). Research-only; no new SRC/FACT/EXH identifiers. SHA-256 pins the retrieved bytes, not the truth of a historical attribution. All headers are retained locally; cookie/session values must not be printed, exported or transmitted.

## Acquired bodies

| ID | Source / edition / family | Local object and coverage | Size and SHA-256 |
|---|---|---|---|
| IF-S01 | [Official FEMA Appendix D](https://www.fema.gov/pdf/library/fema403_apd.pdf), *WTC Steel Data Collection*, by Gilsanz/Massa; spreadsheet as of March 15, 2002; cover note updated May 2002. **FEMA-SEAoNY-COLLECTION**, same historical inventory as the prior mirror, not independent corroboration. | fema403-apd-official.pdf (historical local reference `sources/fema403-apd-official.pdf`; not included here); 27 pages: D-1–D-13, spreadsheet cover, summaries 1–13. Physical 1–3 and 14–27 fully visually inspected. Completed public curl HTTP200, local body timestamp 2026-09-09T22:32:50-0400. | 2,333,446 bytes; `e054a70f9410b1fe0b141f0ec2401244183f67da4d0a703df5ffb18483d6f6fc` |
| IF-S02 | [Public May 25, 2020 syndicated attachment locator](https://sonsoflibertymedia.com/architects-engineers-for-9-11-truth-families-pressure-nist-to-retract-claims-wtc-7-was-destroyed-by-fires-following-university-of-alaska-study/). **AE-RFC-DERIVATIVE-LOCATOR**. Its commentary is not used as technical evidence. | exhibit-e-link-locator.html (historical local reference `sources/exhibit-e-link-locator.html`; not included here); only RFC/Exhibit E link identification used. Completed curl HTTP200, 2026-09-09T22:32:27-0400. Contains unrelated public page material; do not promote it into evidence or create person profiles from it. | 193,442 bytes; `8f1a6076026f3ce84ce293d307237ba1de044874a2e7c4cfc166beb4766c30ba` |

IF-S01 PDF metadata: title `FEMA 403 -- Appendix D`; subject `WTC Steel Data Collection`; creator Adobe PageMaker 7.0; producer Acrobat Distiller 5.0.5 for Macintosh; creation May 7, 2002 23:48:50 EDT and modification May 15, 2002 09:35:43 EDT. These are embedded metadata, not independently authenticated release timestamps. PDF1.4, tagged, no form or JavaScript; Poppler reports RC4 encryption with printing allowed. The original was not decrypted, rewritten, repaired or normalized. Ordinary rendering was used for read-only review. `file` misleadingly described “11 pages”; actual parsed count and complete rendering establish 27. Preserve that diagnostic discrepancy rather than using the superficial count as coverage.

## Acquisition receipts, not evidence bodies

| Receipt | What it records | Bytes / SHA-256 |
|---|---|---|
| `sources/fema403-apd-attempt.headers.txt` | Successful official HTTP200 receipt; filename retains “attempt” but terminal completion and PDF validation established acquisition. | 320; `5f377754277c30dcb8696b110a64ab627eac54a5f9414c04a3452d5c865dc579` |
| `sources/locator.headers.txt` | Successful HTTP200 locator receipt; the sandbox DNS failure had yielded no body before the approved public retrieval. | 1,299; `a869cb8c41d6cf24c6068279acc9a2d3b48e1424aa9c219f7f8a3dc5f444a5a1` |
| `sources/exhibit-e.headers.txt` | HTTP404 at the exact linked public attachment; **no acquired PDF body**. | 133; `2152c0309dcf68f8dad508605037a93388e36626dd3a1ec236b5cced065dac24` |

Exact unresolved attachment: `https://files.wtc7report.org/file/public-download/EXHIBIT-E-Documentation-Indicating-WTC7-Steel-Shipped-to-NIST.pdf`. A title, a link, and a response receipt are not the attachment's contents.

## Existing dependencies, unchanged

- Sample-provenance report (historical local reference `../sample-provenance/report.md`; not included here), claim/lead ledger (historical local reference `../sample-provenance/claim-lead-ledger.md`; not included here), source inventory (historical local reference `../sample-provenance/source-inventory.md`; not included here): prior scope and unresolved SP-L04/SP-L05.
- Earlier 14-page Appendix D mirror (historical local reference `../sample-provenance/sources/fema403-appendix-d-mirror.pdf`; not included here): 2,263,624 bytes, SHA256 `315062f7fdf5495f4fe7a1ffaf4809234d26ec8a82b112d79a401a3a3de192eb`. It contains no actual spreadsheet rows. No full byte/content equivalence of its first 14 pages to IF-S01 is asserted. Same FEMA/SEAoNY source family.
- Existing `research/wtc7-video-comparison/sources/RFC-to-NIST-WTC7-Report-04-15-20.pdf`: 106 pages, 29,676,723 bytes, SHA256 `ccb2ebea1f8d4ba1759c82afb991d1860d9f3ab678007d599f7d332df6d92ae9`. Physical 84–85 visually rechecked through existing derivatives. Its four-entry and Exhibit E references are routing leads; original records control. A read-only pypdf annotation check emitted 19 pre-existing wrong-object-pointer warnings and returned no relevant URI. No repair was attempted.

## Derivatives

`derivatives/fema-d-01` through `03`, and `14` through `27`, each have PNG and OCR TXT partners. Poppler 26.05.0 rendered full pages; Tesseract 5.5.2 English, PSM3 supplied search aids. Physical 1–3 rendered with long edge 1800; 14–27 with long edge 2400. All 17 PNG pages were visually inspected. OCR is explicitly fallible: tables lose letter identifiers, merge cells and misread fractions. The report's decisive values were read from page images, not silently promoted from OCR.

All source bodies, receipts and derivatives are pinned in [SHA256SUMS](SHA256SUMS). Research documents are intentionally excluded from that data manifest so later clearly marked analysis edits do not masquerade as changed source bytes.
