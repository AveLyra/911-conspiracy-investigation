# Earlier GTE handoff patent: reference numbering before September 2001

TEL03 · November 25, 2026 · additive source follow-up

## Observation

[U.S. Patent 6,104,926, “Call handoff”](https://patentimages.storage.googleapis.com/7f/7e/0b/ba36d8f87fccbf/US6104926.pdf), GTE Airfone, identifies application 08/509,703 and an August 15, 2000 issue date. The source PDF, accessed November 25, 2026, has SHA-256 `c5cef8a1d6aac88592ab550342b8c30c765daf6fb679efe784023c1bb0e5ccf7`. On physical PDF page 38, printed column 14, the patent describes allocating a call reference number to distinguish calls from the same aircraft and starting the sequence at 1 when the aircraft phone system powers up. The relevant page text was extracted and compared with the [public transcription](https://www.freepatentsonline.com/6104926.html), lines 279–282; extraction may introduce OCR errors. The retained PDF is the source record.

The [later patent review](https://github.com/AveLyra/911-conspiracy-investigation/blob/225b7df9d9d6ea30087b7390481d3549603a4053/investigation/broader-evidence/telephone-gte-patent-handoff-identifiers-2026-11-25/README.md) described the same rule in patent 6,430,412, issued in 2002. That later patent identifies application 08/509,703 as its parent. The 2000 patent therefore shows the description in an issued patent before the attacks, subject to verification of the actual historical distribution and applicable implementation. These related patents are not independent corroboration of deployment.

## Limits and remaining work

Neither patent establishes Flight 93's installed equipment or software, its actual operations, whether resets occurred, or a mapping from the airborne reference to the **ACIS call ID** described in an FBI interview. The two identifiers could be different; no contradiction or reuse of ACIS IDs has been established. This finding does not resolve the previously preserved differing `0`, `130`, and `138` readings, identify a caller, demonstrate a completed call, or establish intent.

- [ ] Obtain the applicable aircraft equipment and software configuration, vendor protocol and ACIS field dictionaries, and identifier translation rules.
- [ ] Obtain original spreadsheet versions, event logs, switch and power-cycle records, and source-to-exhibit worksheets. Test any claimed join against identifiers, clock domains, and reset boundaries; no such test is reported here.
- [ ] Preserve the [existing field correction and unresolved values](https://github.com/AveLyra/911-conspiracy-investigation/blob/04a89d22226600e8bb8ed6e2a5c12fbac3150ccf/investigation/broader-evidence/telephone-ua93-office-call-field-correction-2026-11-25/README.md) without selecting a value.

Scope: source identification and the numbered page's extracted text; no full patent comparison, installation test, carrier log inspection or original call reconstruction. This note supersedes no earlier record. The native study retains the source PDF; the public derivative contains the link and analysis.
