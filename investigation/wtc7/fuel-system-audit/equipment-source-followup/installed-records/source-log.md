> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../../README.md).

# Installed-record lookup and prospective reading

2026-09-11. [Protocol](PROTOCOL.md). Six of six queries used; two of twelve allowed distinct primary-source openings used at this stage. No original installed-generator specification or dated control drawing located in returned results. Search snippets are locators, not authenticated engineering evidence.

## Exact queries and selection

1. `"Salomon Brothers" "1750" generators`
2. `"World Trade Center 7" generator manufacturer`
3. `"W-7004" "W-7005"`
4. `"43D275" "Preferred"`
5. `"7 World Trade Center" "E-R1"`
6. `"Salomon" "generator" "cooling"`

Returned primary leads: already acquired NCSTAR 1-1J, its government mirrors, NIST's revised November 2008 technical briefing, and NIST's September 2006 testimony packet containing report excerpts. NCSTAR 1-1C structural-modification summaries do not identify the cooling package in the displayed result. No manufacturer primary record matching the installed generator was returned. Nonmatching product numbers, other Salomon names, property listings, patents, newer-building records and social-media/commentary results were excluded. No personal/contact information from unrelated search hits is retained in this log. A public court-opinion result was not opened.

The last query was used for the cooling dependency directly rather than a newly found manufacturer lead, because none had emerged. Exact short drawing/submittal searches were noisy; this bounded failure is not evidence that the original record is unavailable everywhere or never existed. No further queries in this branch.

## Selected primary sources

- [NIST-hosted testimony packet](https://www.nist.gov/system/files/documents/2017/05/09/TestimonySept8_06.pdf): web opening reports 21 physical pages. Its displayed excerpt includes NCSTAR 1-1 Chapter 12 and an interview footnote. Select complete physical pages 1–12 before local substantive reading, to cover testimony/context and the entire Chapter 12 excerpt including its end. Verify actual identity and assembly; filename and index title alone do not establish the contents.
- [Revised WTC 7 technical briefing](https://www.nist.gov/el/disasterstudies/wtc/upload/WTC7RevisedTechnicalBriefing_111908.pdf): web opening reports 106 pages. Select complete physical pages 1, 15–16, 49–51: identity, equipment diagram/table and the three fuel-fire slides. This is the same NIST source family, not independent historical corroboration. Do not infer an entire briefing review or inspect operational charge-design slides outside this question.

The web text provides navigation only; full selected pages must be read before adopting table/figure/footnote details. Copies, extraction, receipts and further acquisition results will be recorded here. Original source bytes are preserved; no raw headers or process diagnostics are cleared for disclosure.

## Acquisition and preflight results

Initial local downloads failed DNS (curl exit 6, HTTP 000, zero bytes). Separately approved retries on the same official URLs succeeded: testimony 972,990 bytes, HTTP 200, no redirects; briefing 5,567,334 bytes, HTTP 200, four HTTPS redirects. Separate attempt02 header paths preserve the earlier attempts; headers remain local-only and unprinted. No explicit denial was bypassed.

Local pypdf confirms unencrypted PDFs of 21 and 106 pages. Testimony SHA-256: `999b33d6256b64ca66596fac4346831180a072aa677ed9623c1dfb48c7c17029`. Briefing SHA-256: `b8845c40205a4731d248b6398858dfabedbb927e01f8d6acd1422b40f2fa4850`. Title-page text confirms Sunder's September 8, 2006 NYC Council testimony regarding diesel storage at 60 Hudson Street, and his November 19, 2008 WTC investigation briefing; their WTC 7 content must be read in that context.

The new rendering helper's first preflight failed because its relative font-directory parent index was one level too high. It stopped before creating a run directory or rendering pages. Corrected the index to the existing investigation font configuration; this is a local helper error, not a source failure. Subsequent run receipts distinguish actual rendering from this failed preflight.

Both declared render runs subsequently completed with exit 0. Root visually read all 18 selected complete pages with extracted text aids. Actual testimony coverage is physical 1–12, including NCSTAR 1-1 printed 175–181; the next blank page and later appendix are excluded, narrowing the initial intention to cover the entire appended chapter. Physical labels are one-based; web source indexes were zero-based. The named interview footnote is physical 11/printed 180. All 18 PNG/text outputs reproduced identically in the separate run; details and the tested overwrite refusal are in validation. No new search/open branch followed these readings.
