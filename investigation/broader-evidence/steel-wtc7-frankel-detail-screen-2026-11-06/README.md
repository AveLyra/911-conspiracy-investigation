# WTC 7 Frankel shop drawings and the W14A steel attribution

November 6, 2026 · Steel track · STL02–STL03 / AUD011 / AUD016 / B188 / H005

Three marks on Frankel's erection schedule can be joined to shop drawings by mark, column number and section. Two of the drawings identify **Column 14A** and specify a nominal section **20-1/4 in. deep by 17-1/4 in. wide**. The field record for the piece called **A or W14A** gives **16 in. by 15-1/2 in.** This adds a period fabrication source to the [earlier Cantor schedule comparison](https://github.com/AveLyra/911-conspiracy-investigation/commit/89413f62308e80071f8e90ccb33310786e4e8ffc). The measured dimensions weaken the proposed match to these two specific shop pieces. The field attribution to WTC 7 remains unresolved. [Public 12-009 ZIP](https://archive.org/download/911datasets/NIST_WTC7_FOIA_12-009.zip) · [FEMA field table, PDF p. 16](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16)

## Mark-to-drawing joins

| Erection source | Shop source and internal identifiers | Scope |
|---|---|---|
| **E117**, Column **14A**, **W14 × 550**, **A1823** | **1823.TIF**, Frankel sheet **1823**. Lower stock line shows **14A**, **A1823**, **W14 × 550**, and starts its dimensional callout **W 20-1/4 × 17-1/4**. | Title identifies the **12th tier**. The left splice annotation also references **A1499**. |
| **E117**, Column **14A**, **W14 × 550**, **A1499** | **1499.TIF**, Frankel sheet **1499**. Vertical stock line shows **A1499**, **W14X550**, and starts its dimensional callout **W 20-1/4 × 17-1/4**. The adjoining vertical location line reads **COL 14A**. | Title identifies the **11th tier**, **Zone 2**. |
| **E117**, adjacent Column **14**, **W14 × 500**, **A1803** | **1803.TIF**, Frankel sheet **1803**. Lower stock line shows **14**, **A1803**, **W14 × 500**, and starts its dimensional callout **W 19-5/8 × 17**. | Adjacent-column comparison. Title identifies the **12th tier** and **Column 14**. |
| **E118**, Column **14A**, **A2540** | No exact **A2540** or **2540** TIFF basename occurs in the indexed ZIP. The schedule's title region references **CUSTOMER DRAWING S-18**. Its section lettering in this cell is faint. Cantor **S-18** independently shows **W14 × 500** at the previously checked 14A callout. | A distinct locator to pursue. The filename test leaves other naming, combined sheets and other release holdings open. |

The E117 and E118 title areas record contract **84-15**. The three matched shop sheets show **84-152**. The source ledger preserves each string by sheet. The joins use the printed marks, sections and column identifiers. Their relationship to contract administration and drawing-issue history remains open. [Source ledger and drawing coordinates](SOURCE-PINS.json)

## Field records and limits of the geometry screen

| Record | Observations preserved |
|---|---|
| FEMA Appendix D, row 20 | **A or W14A** with remark beginning **WTC#7 W14**. **16 × 15-1/2 in.** depth and flange width, **1-3/16 in.** top flange, seat **8 × 7-1/2 × 3/8 in.**, stiffener **9-5/8 × 5-1/4 × 3/8 in.**, and **15/16 in.** bolt hole. |
| FEMA Appendix D, row 21 | **B or W14B** with remark beginning **WTC#7 W14** and seat **7-1/2 × 7-1/4 × 3/8 in.** Equivalent section measurements are unavailable in this row. |
| NIST final inventory, Table A-7 | **W-14A or A** and **W-14B**, both **Heavy Wide flange** in the unidentified wide flange sections category. The attribution rationale remains unacquired. |
| Frankel 1499 and 1823 | Nominal depth and width exceed the W14A field measurements by **4-1/4 in.** and **1-3/4 in.**, respectively. The visible stock callouts are drawing dimensions. The comparison does not correct for distortion, cutting, orientation or field measurement conditions. |
| Selected hole callouts | Sheet **1499** Section C–C shows **13/16 in.** diameter and the left elevation has **1-1/16 in.** hole callouts. Sheet **1823** Section A–A also shows **13/16 in.** holes, and its right-end detail shows a **1-1/4 in.** drilled hole. Keep these values beside the field **15/16 in.** as feature-specific observations. Their equivalence to the field hole is unverified. |

The selected views yielded no verified joint match to the field seat, stiffener and hole pattern. A drawing of an angled connection, splice or different bolt group cannot establish the size of the particular field feature. The schedule and shop-sheet join identifies drawing pieces. A matching fabrication mark, weld or hole pattern on the recovered steel and its custody chain would be needed to identify the recovered piece. The field-versus-inventory attribution remains open. [FEMA Appendix D, PDF p. 16, rows 20–21](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) · [NIST NCSTAR 1-3B, Table A-7, PDF p. 96](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96)

## Access and reading scope

Acquired **16 exact TIFF members** from the public mirror of release **12-009** using bounded ZIP ranges. Each selected entry was checked against the central-directory name, uncompressed length and CRC. The preserved member bytes were reread and hashed. The ledger records the public URL, access date, member path, range, SHA-256 and checked drawing areas. The visual comparison used the E117/E118 schedule areas and the three identified shop sheets. E117A and E118A were checked for title or context. The remaining acquired sheets were screened by overview or selected title block. The complete ZIP drawing corpus and the NIST/UAF models were outside this screen. [Public archive](https://archive.org/download/911datasets/NIST_WTC7_FOIA_12-009.zip) · [Source ledger](SOURCE-PINS.json)

## Open TODOs

- [ ] Locate **A2540** through a drawing index, splice cross-references, other releases or a differently named sheet. Check other 14A segments and other candidate columns without treating the field label as a drawing identifier.
- [ ] Acquire the original field dimension sheet, scaled images of both faces and any fabrication marks. Compare seat, stiffener, hole diameter and pitch on corresponding features. Obtain a period section reference where the drawing dimensions or revision are uncertain.
- [ ] Obtain yard-to-laboratory transfer and NIST intake records, and the rationale for the inventory classification. Distinguish the identity of each piece from its building attribution.
- [ ] Obtain drawing issue and revision records if needed to verify installed details. The inspected scans give design and fabrication callouts.
