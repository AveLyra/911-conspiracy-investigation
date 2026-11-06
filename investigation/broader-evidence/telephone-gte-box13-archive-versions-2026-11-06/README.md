# Archived versions of the Box 13 GTE phone-record reader

November 6, 2026 UTC · **TEL02–TEL03 / AUD016-A1**. Two Wayback captures of public document **26103892** were retrieved. Both replay bodies match their corresponding CDX digests. The older capture already displays the **`UAL_flt93.xls`** filename and the FBI evidence identifiers found in the current reader. The October 2026 capture and the live reader yield identical extracted document text. The archived material is HTML and supplies no native workbook. [2015 capture](https://web.archive.org/web/20151126193545id_/https://www.scribd.com/doc/26103892/T7-B13-Flight-GTE-Phone-Records-Fdr-Entire-Contents-788) · [October 2026 capture](https://web.archive.org/web/20261008070001id_/https://www.scribd.com/document/26103892/T7-B13-Flight-GTE-Phone-Records-Fdr-Entire-Contents-788) · [Earlier live-reader study](https://github.com/AveLyra/911-conspiracy-investigation/blob/40fed9bab3fa93b8a929f1210580750a1d8f63dd/investigation/broader-evidence/telephone-gte-box13-public-reader-2026-11-06/README.md)

## Archive index and replay fields

| Capture | CDX row | Saved replay body |
| --- | --- | --- |
| **2015-11-26 19:35:45 UTC**, legacy `/doc/` | **200** · `text/html` · CDX length **39,435** · digest `4TZXSNJ6YARRD2WL6MN7Z6RHHTXM7M37` | Replay **200**, Memento date matches. **188,804 bytes** of HTML. Base32 SHA-1 of the saved body equals the CDX digest. |
| **2026-10-08 07:00:01 UTC**, `/document/` | **200** · `text/html` · CDX length **263,509** · digest `GGM3UV3ARZIWHY6TTH7H3EAK7PDGYWD3` | Replay **200**, Memento date matches. **261,371 bytes** with `Content-Encoding: gzip`. Base32 SHA-1 matches CDX on the saved compressed body. Decoding yields **1,457,294 bytes** of HTML with a different hash. |

Keep CDX lengths, saved response-body lengths and decoded entity lengths as separately labeled observations. This comparison checks the index and replay bodies. The original WARC records and full original response headers were outside the retrieved material. [Exact index queries and SHA-256 pins](SOURCE-PINS.json)

## Document layer comparison

The 2015 HTML uses the heading *T7 B13 Flight GTE Phone Records Fdr- Entire Contents 788*. The later page uses *9/11 United Airlines Phone Records* as its visible heading and retains the earlier title in metadata. The older metadata declares **41 pages**, and the October and live readers display **41 pages**. That number describes the hosted reader. The underlying NARA paper folder and its completeness remain unverified. The earlier three Bates spans count **25 labels** for one item. They represent a different scope and are kept as recorded. [2015 capture](https://web.archive.org/web/20151126193545id_/https://www.scribd.com/doc/26103892/T7-B13-Flight-GTE-Phone-Records-Fdr-Entire-Contents-788) · [NARA file unit 2608326](https://catalog.archives.gov/id/2608326)

| Selected value | 2015 extracted line | October 2026 and live extracted line |
| --- | --- | --- |
| **M-SFA-00006033 / M-SFA-00006046**, **1A-1A30336** | 11, 12, 15 | 1, 2, 5 |
| Relay header **09:35:32-0500** and message date header **08:33:53 -0600** | 3203, 3210 | 967, 974 |
| MIME filename **`UAL_flt93.xls`** | 3230 | 994 |
| **1A-1A65562**, **M-NKA-00001342 / M-NKA-00001341 / M-NKA-00001348** in displayed order | 3232, 3274, 3424 | 996, 1012, 1149 |

The literal filename occurs **once** in the selected 2015 document text and **twice** in both newer extracts. The MIME filename is present in all three. The October and live document extracts are exactly equal under the same parser, including whitespace as extracted. The 2015 extract has **3,424 lines**, compared with **1,149** in both newer extracts. Those are text extraction counts. The 2015 replay body contains no direct document-specific thumbnail URL in an `img src` attribute. The October and live bodies expose the same **ten** thumbnail URLs in that attribute. This checks HTML references only. The archived images and full page inventory were outside this test. [Method and locators](SOURCE-PINS.json)

## Remaining tests

- [ ] **TEL02.** Obtain **`UAL_flt93.xls`**, the native message, and **1A-1A65562** enclosure manifest. Compare the actual sheet and message bytes with the separately reported courier version and July 2002 update. The matching attachment label helps trace the record. It gives no byte-level identity across versions.
- [ ] **TEL02–TEL03.** Obtain the original page/export inventory for the **41-page** public reproduction and the separate scope of **1A-1A30336**. Use actual page images and source rows to test whether layout or content changed. The earlier timestamp differences and unresolved call joins remain open.

The preserved sources are two replay bodies with headers, two index responses, and the live HTML retained in the preceding study. The local verifier checked five source hashes, both CDX comparisons, gzip decoding, exact equality of the two recent document extracts, and nine earlier-to-later anchors. These are copies in one publication lineage. Their agreement establishes visibility in the checked captures and supplies no independent historical verification of the calls.
