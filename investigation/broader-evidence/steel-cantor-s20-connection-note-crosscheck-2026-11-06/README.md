# Cantor S-20 and Frankel E120 connection notes

November 6, 2026 · Steel track · STL02–STL03 / AUD011 / AUD016 / B188 / H005

The Cantor customer drawing **S-20** and Frankel **E120** give the same general hole diameter of **13/16 in.**, subject to details shown on the drawings. Frankel E120 explicitly names S-20 as its customer drawing. The matching note comes from a linked pair of records. It adds no independent measurement of the recovered piece, for which FEMA recorded a **15/16 in.** hole. [Public 11-209 ZIP with S-20](https://archive.org/download/911datasets/NIST_WTC7_FOIA_11-209.zip) · [Public 12-009 ZIP with E120](https://archive.org/download/911datasets/NIST_WTC7_FOIA_12-009.zip) · [FEMA Appendix D, PDF p. 16](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16)

## Source comparison

The acquired **S-20.tif** title block reads **EAST-WEST WIND BRACING ELEVATIONS** and identifies **7 WORLD TRADE CENTER** and drawing **S-20**. The lower notes block records **RELEASED TO FRANKEL STEEL** on **11/30/84**. The revision table separately records **ISSUED TO PORT AUTHORITY** on **5-10-85**. These are issue annotations on the inspected scan. The original transmittal, received drawing version and change history remain unacquired. [S-20 source path, hash and crop locations](SOURCE-PINS.json)

| Location | Cantor S-20 | Frankel E120 | Comparison |
|---|---|---|---|
| Structural Steel Note **5** | Field inspection and testing provisions. Shop welds to be tested by approved methods and certified. | Same testing and certification language in the inspected block. | A specific record class to seek if a weld test or certificate retains the piece mark. The requirement leaves actual testing and retention open. |
| Structural Steel Note **6** | **HIGH STRENGTH BOLTS A-325F** and **UNFINISHED BOLTS A-307**. The S-20 line is marked with a **D** revision triangle. | **HIGH STRENGTH BOLTS A-325** and **UNFINISHED BOLTS A-307**. | Preserve **A-325F** and **A-325** as printed. The reason for the wording difference, significance of the **F**, and as-installed bolt designation remain unverified. |
| Structural Steel Note **7** | **13/16 in.** hole diameter unless otherwise shown on drawings. | **13/16 in.** hole diameter with the same exception. | Common general value. The bolt-size glyph is outside the verified transcription. |
| Structural Steel Note **13** | Milled stiffeners under column connections and over columns. | Same provision in the previously verified E120 scan. | General requirement without the field specimen's seat or stiffener dimensions. |

The compared note areas do not join the field **15/16 in.** hole to an equivalent shop feature. The previous comparison preserved **13/16**, **1-1/16** and **1-1/4 in.** on different shop features. That variation and the drawing-specific exception limit the value of a comparison to the default. FEMA's **A or W14A**, remark **WTC#7 W14**, and NIST's **W-14A or A** under unidentified wide-flange sections remain separate records. [Prior E120 and shop callout comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/de6091608d43e095592c787bf5292e8ed03e9a6d/investigation/broader-evidence/steel-frankel-wtci-drawing-index-2026-11-06/README.md) · [NIST Table A-7, PDF p. 96](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96)

## Verified scope and open TODOs

The new S-20 scan came from an exact public ZIP member range. Verified the range, member path, length, CRC and SHA-256. Reread the E120 TIFF and its numbered PDF counterpart bytes and checked the selected note blocks visually, including the previously inspected PDF pages. Other S-20 callouts were outside this comparison. [Source ledger](SOURCE-PINS.json)

- [ ] Locate the drawing transmittals and revision packages for S-20 and E120, including the issued copy behind the S-20 Note 6 marker. Test which note applied to an identified connection.
- [ ] Seek Frankel shop-weld test reports, certificates, and field inspection records with piece marks or inspection locations. If available, test whether the records join a candidate part to an installed location.
- [ ] Keep **A2540**, **A2547** and **E117B** open. Obtain equivalent field geometry and original photos, then trace the recovered pieces through yard and laboratory custody to the NIST inventory rationale.
