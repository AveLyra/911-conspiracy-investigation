# WTC 7 column schedules and the W14A steel attribution check

November 6, 2026 · Steel track, AUD011 / AUD016 / B188 / H005

I acquired five original drawing scans from a public mirror of the NIST **11-209** release. Three are the Cantor column schedules **S-17, S-17A and S-18**. The schedules provide column numbers, floor bands and specified sections that can be checked against the field measurements. The first scoped check tested the similar-looking **14A** drawing number against two scheduled section callouts. The field specimen's building attribution remains unresolved. [Public 11-209 ZIP](https://archive.org/download/911datasets/NIST_WTC7_FOIA_11-209.zip) · [NIST NCSTAR 1-9A, §3.2.1](https://www.govinfo.gov/content/pkg/GOVPUB-C13-8bdab3b44f45453326a423f57e4bf3e1/pdf/GOVPUB-C13-8bdab3b44f45453326a423f57e4bf3e1.pdf)

## What the release and scans show

The two-page PDF accompanying the mirror has an **August 17, 2011** request on p. 1 and a **September 20, 2011** final response on p. 2. The response states that **41 electronic files** were being released on disk. The mirror's central directory lists **41 TIFFs and one PDF**. The TIFFs are under a folder with **2011-09-23** in its name. A contemporary publication describes **42 files**. Keep the response count, mirror file count, public description, and folder date separate. The directory count includes the correspondence PDF. The original disk manifest and the relationship of the folder date to the response remain open. [Public ZIP](https://archive.org/download/911datasets/NIST_WTC7_FOIA_11-209.zip) · [Contemporary release description](https://www1.ae911truth.org/en/evidence/611-wtc-7-blueprints-exposed-via-foia-request.html)

| TIFF member | Drawing title read from the face | Selected title-block observation |
|---|---|---|
| **S-17** | **Column Schedule No. 1** | **8-5-85** appears beside **REVISED AS CIRCLED**. **5-10-85** appears beside **ISSUED TO PORT AUTHORITY**. |
| **S-17A** | **Column Schedule No. 2** | **5-10-85** appears beside **ISSUED TO PORT AUTHORITY**. |
| **S-18** | **Column Schedule No. 3** | **10-8-85** appears beside **REVISED AS CIRCLED**. The sheet also shows Port Authority issue entries **8-2-85** and **5-10-85**. |
| **S-1** | **1st Fl. Framing Plan** | The checked revision block includes entries from **1984** through **1987**. |
| **S-19** | **North-South Wind Bracing Elevations** | The checked block includes **5-10-85** beside **ISSUED TO PORT AUTHORITY**. |

The revision and issue entries apply to their own sheets. They do not date the recovered specimen, establish a common drawing issue, or certify an as-built condition. NIST's published methodology identifies the Cantor drawing sets as a source for the building model and identifies fabrication shop drawings separately for connection details. [NIST NCSTAR 1-9A, printed p. 19](https://www.govinfo.gov/content/pkg/GOVPUB-C13-8bdab3b44f45453326a423f57e4bf3e1/pdf/GOVPUB-C13-8bdab3b44f45453326a423f57e4bf3e1.pdf)

## Field label and design number

FEMA's field row says **A or W14A** and the remark begins **WTC#7 W14**. It gives depth **16 in.**, flange width **15-1/2 in.** and top-flange thickness **1-3/16 in.** NIST's final inventory lists **W-14A or A** and **W-14B** among unidentified wide-flange sections. Both descriptions remain preserved. [FEMA Appendix D, PDF p. 16, rows 20–21](https://www.fema.gov/pdf/library/fema403_apd.pdf#page=16) · [NIST NCSTAR 1-3B, Table A-7, PDF p. 96](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-3b.pdf#page=96)

The schedules use **14A** as a column number in a table whose neighboring headers include **14** and **15**. In **S-17**, the upper section callout immediately below the 23rd-floor band in column **14A** reads **W14 × 550**. The adjacent column **14** callout reads **W14 × 500**. In **S-18**, the lower section callout immediately above the 23rd-floor band under **14A** reads **W14 × 500**. Its adjacent column **14** callout reads **W14 × 426**. These are selected reads near the two schedules' 23rd-floor boundary. Other floor bands were not screened. Exact crop coordinates are in [SOURCE-PINS.json](SOURCE-PINS.json).

Using the modern AISC dimensions already checked in the [previous 38-shape screen](https://github.com/AveLyra/911-conspiracy-investigation/blob/5317f50fed4a93b47e52f6cdd50f6223f29cbef9/investigation/broader-evidence/steel-w14a-section-dimension-screen-2026-11-06/README.md), the two selected **14A** section callouts differ from the field tuple by the following amounts. This is a section-label comparison using reference dimensions.

| Scheduled section | Reference depth × flange width × flange thickness, inches | Reference minus field, inches |
|---|---:|---:|
| **W14 × 550**, S-17, AISC row 188 | 20.2 × 17.2 × 3.82 | +4.2 × +1.7 × +2.6325 |
| **W14 × 500**, S-18, AISC row 189 | 19.6 × 17.0 × 3.50 | +3.6 × +1.5 × +2.3125 |

The selected sections are substantially larger on all three recorded dimensions. Their comparison weakens a proposed match to these particular callouts based on the label resemblance alone. It leaves other 14A segments, other columns, built-up pieces, historical section properties, and the field measurement conditions open. The sheets did not supply an item-specific seat match or a link to a recovered piece.

## Open TODOs

- [ ] Obtain the applicable Frankel fabrication and erection sheets and a period section reference. Compare the recorded seat, stiffener, and bolt-hole geometry jointly. The public **12-009** ZIP directory was acquired as a locator. No member from that archive was read in this pass. [Public 12-009 ZIP](https://archive.org/download/911datasets/NIST_WTC7_FOIA_12-009.zip)
- [ ] Obtain the field measurements and photos tied to an original fabrication mark, the yard transfer and NIST intake records, and the item-specific attribution rationale. The field mark, structural number and laboratory inventory label require a source-level join.
- [ ] Verify the original 11-209 disk manifest or an independent complete release copy and any later drawing versions. This pass checked six exact members and both central directories. The archive identity, decompressed length and CRC were checked for each acquired member. See the [source ledger](SOURCE-PINS.json).
