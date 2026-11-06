# W14A steel section dimensions and source attribution

November 6, 2026 · Original-records work plan, steel track · Bounded public-source comparison

## Records preserved

| Record | Reported identification | Exact locator |
|---|---|---|
| SEAoNY field table published by FEMA | Row 20, `A or W14A`, and row 21, `B or W14B`. Both remarks begin `WTC#7 W14`. The trip date is `12/19/01`. | [FEMA 403 Appendix D, physical p. 16, Steel Data Collection Summary 2 of 13](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) |
| NIST final inventory | `W-14A or A` and `W-14B` appear under unidentified wide-flange sections, each described as `Heavy Wide flange`. | [NIST NCSTAR 1-3B, Table A-7, printed p. 68 / physical p. 96](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96) |

The field attribution and the inventory classification remain unresolved. This pass adds a dimension comparison to the [earlier attribution and custody review](https://github.com/AveLyra/911-conspiracy-investigation/commit/88831b1b5436958547c9399306ff3c60ad8e1baf). It tests what the recorded dimensions can establish by themselves.

## Observations and result

FEMA row 20 records depth **16 in.**, flange width **15-1/2 in.**, and top-flange thickness **1-3/16 in.** The web-thickness and bottom-flange-thickness cells are blank. The remarks separately give seat dimensions **8 × 7-1/2 × 3/8 in.**, stiffener dimensions **9-5/8 × 5-1/4 × 3/8 in.**, and photo reference **DKoutsoubis:1/30/02:#68-73**. Row 21 gives seat dimensions **7-1/2 × 7-1/4 × 3/8 in.** and photo reference **DKoutsoubis:1/30/02:#63-67**. The main section dimensions needed for the same test are absent from row 21. [FEMA field table, rows 20–21](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16)

**None of the 38 W14 entries in the checked AISC v16.0 table matches all three W14A measurements exactly.** The result holds separately for the regular dimensions and the detailing dimensions. The detailing columns match each field value exactly in a different row.

| Field dimension | FEMA value in inches | AISC detailing row with exact value | AISC detailing depth × flange width × flange thickness in inches |
|---|---:|---|---|
| Depth | 16 | W14×233, row 198 | 16 × 15.875 × 1.75 |
| Flange width | 15.5 | W14×145, row 203 | 14.75 × 15.5 × 1.0625 |
| Top-flange thickness | 1.1875 | W14×159, row 202 | 15 × 15.625 × 1.1875 |

With an illustrative band of **±1/4 in. per dimension**, neither set of columns yields a candidate. At **±1/2 in.**, both yield W14×211 and W14×193. At **±1 in.**, both yield seven candidates. These bands show sensitivity to the chosen threshold. The field sheet supplies no measurement tolerance to justify treating any band as an identification criterion. [Purdue-hosted AISC workbook copy](https://web.ics.purdue.edu/~jhunjhu0/Steel%20Design/aisc-shapes-database-v16.0.xlsx) · [OpenCivil-hosted AISC workbook copy](https://raw.githubusercontent.com/OpenCivil-Project/Open-Structures/main/app/resources/aisc-shapes-database-v16.0.xlsx)

## Reading scope and limitations

The two workbook copies have different file hashes and worksheet lists. The checked W14 labels, row numbers and six dimensional columns agree in both. They are copies of the same reference table and provide a cross-check of the transcription. The study uses the current v16.0 table, so period-specific, modified, and built-up sections remain outside the test. NIST describes W14 shapes in WTC 7 and includes built-up sections in its description. A generic W14 shape match would still need a connection detail, piece mark, or custody record to tie it to a particular building or location. [AISC workbook catalog](https://www.aisc.org/aisc/publications/steel-construction-manual/shapes-database-v160/) · [NIST NCSTAR 1-9, §2.4.4, printed pp. 28–29](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf)

The test leaves open whether the recorded dimensions reflect field measurement practice, the condition of recovered steel, the original section, or another factor. No deformation correction, rounding allowance, or tolerance was applied to the exact match. The seat, stiffener and bolt-hole geometry were transcribed for a later drawing comparison. No shop-drawing match, column assignment, or change to the building attribution follows from this screen.

## Reproduction

In the `Database v16.0` sheet, select rows with column A equal to `W` and column C matching `^W14X[0-9]+$`. The 38 selected rows are 183–220 in both copies. Subtract the field vector `(16, 15.5, 1.1875)` from the values in columns G, L and T. Repeat separately for columns H, M and U. For each threshold, count a row only when the absolute difference is at or below the threshold for all three dimensions. Use exact decimal comparison of the stored values. The `Readme` sheet defines those columns in rows 46, 48, 52, 53, 62 and 63. Exact source locators, source hashes and summary results are in [SOURCE-PINS.json](SOURCE-PINS.json).

## Open TODOs

- [ ] Locate a period-appropriate shape reference and WTC 7 column schedules and seat/shop drawings. Compare the recorded seat, stiffener and bolt holes as a joint pattern before attempting any position attribution.
- [ ] Locate the original field notes and any scaled closeups or remeasurement records. Check measurement locations, specimen condition and the absent web and bottom-flange dimensions. W14B also needs its own section measurements.
- [ ] Locate the candidate-specific NIST intake or transfer documents and attribution worksheet, including the relevant disposition of the W14B records request. Compare identifiers and attachment details to determine whether the field and inventory entries refer to the same pieces and how each classification was reached. [Earlier W14B archive review](https://github.com/AveLyra/911-conspiracy-investigation/search?q=DOC-NIST-2013-001311&type=code)
