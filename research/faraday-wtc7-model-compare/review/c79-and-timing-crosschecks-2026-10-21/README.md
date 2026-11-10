# Column 79 PDF layers and NIST timing comparisons

October 21, 2026. Public-source research. This adds a UAF PDF-layer discrepancy, another NIST caption conflict, and two parameter/comparison qualifications. It does not establish incorrect native model inputs, a different collapse outcome, concealment or intent. All earlier conflicting records remain unchanged.

## UAF Figure 3.14 has different member labels in different PDF layers

In both held [UAF final-report PDFs](../uaf-pdf-comparison-2026-10-18/README.md), printed p. 86 / physical p. 99, Figure 3.14 contains three distinct records:

| Representation | Recorded member label |
| --- | --- |
| Caption | `W21x44 G3005` |
| Visible vector annotation on the rendered page | `W21x44;  G3005 w/o bracing` |
| Original embedded raster, viewed separately | `W24x55; G3005 w/o bracing` |

The rendered page is therefore consistent with its caption. The discrepancy is between the rendered annotation and the underlying image resource, not between the two visible labels. A filled blue rectangle covers the earlier raster-label region, and yellow vector text supplies the W21 label. The recorded PDF coordinates, image-stream/pixel hashes and alpha-mask hashes are in [observations.json](observations.json). The Figure 3.14 raster and mask match across both final-report versions. This establishes a shared reporting-layer feature, not when or why it was edited.

Initial inspection of the extracted raster suggested a visible caption-versus-plot conflict. Complete-page rendering showed the overlay, so that initial interpretation is not the finding retained here. Both source representations, and the interpretation change, are explicitly preserved.

**Why it matters:** UAF printed p. 84 criticizes NIST for representing G3005 as W24x55 rather than W21x44. The unbraced comparison also bears on buckling and the surrounding framing response near Column 79. The label change could correct stale annotation on an otherwise correct W21 model; it could instead misidentify a W24 result or another export. Neither is established. The visible output-database locator is `Model-10_Nonlinear_10s_No_Support.odb`; a filename is not a verified section assignment. The decisive records are the native member geometry/section assignment, matching result database, and export/version history. No actual section is selected from the labels alone.

The previously recorded Figure 3.4/3.7 case-name and step-time differences remain open. Figure 3.8 also visibly names the modified `Model-16_Linear_10s_No_Protrusion1.odb` case at Step-2, increment 25, step time 1.000 s. That strengthens a figure locator, not a verification of its material or geometric-nonlinearity settings.

## The NIST companion report supplies another conflicting caption

[NCSTAR 1-9A](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9a.pdf#page=160), printed p. 109 / physical p. 160, Figure 4-60 presents the same named no-debris collapse sequence as [NCSTAR 1-9 Figure 12-68](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=659), printed p. 593 / physical p. 659. Their descriptions are not interchangeable:

| Source location | Collapse-reference seconds | Parenthetical calculation seconds | Subtracted offset seconds |
| --- | --- | --- | --- |
| Panels in both figures | 6.2; 7.4; 8.5 | 19.5; 20.7; 21.8 | 13.3; 13.3; 13.3 |
| NCSTAR 1-9 Figure 12-68 caption endpoints | 5.5; 7.8 | 21.5; 23.8 | 16.0; 16.0 |
| NCSTAR 1-9A Figure 4-60 caption endpoints | 6.2; 8.5 | 14.5; 21.8 | 8.3; 13.3 |

The companion caption's first calculation time is **five seconds earlier** than its first panel label. Its list of figures, printed p. xiv / physical p. 17, repeats 14.5; that repetition is a dependent publication record, not independent corroboration of a solver event. The adjacent Figure 4-61 has consistent 13.3-second offsets, retained as a control.

No time is repaired or selected as correct. The underlying panel pixels were not certified as identical between the two NIST reports; this comparison concerns the named sequence, labels and captions. Editorial copying, a reference-frame error and a source-run/export discrepancy remain untested possibilities. Figure-generation records, the run-to-frame map and native histories would distinguish them. No new historical video timing or solver defect is demonstrated.

## UAF thermal expansion needs a case-specific baseline

UAF Section 2.1.3.4, printed p. 32 / physical p. 45, states a general constant steel coefficient of 14 microstrain/C, approximately 7.78 microstrain/F. Section 3.2.2, printed pp. 80-81 / physical pp. 93-94, describes an approximately 40-percent increase to 11.5 microstrain/F for named beams in the modified plate case.

**If** the Chapter 2 value was the baseline for that Chapter 3 case, the increase is about **47.8 percent**, using either stated temperature-unit system. The slight difference between 47.8149 percent and 47.8571 percent reflects which published rounded unit value is used; both calculations are recorded rather than collapsed into one exact input.

This is a conditional reporting ambiguity, not proof of a wrongly entered parameter. The Chapter 3 baseline may differ, and the word approximately limits the precision claimed. Its actual material definition has not been recovered. The [existing factorial protocol](../c79-factorial-protocol-2026-10-19/README.md) retains its unknown baseline; it is not silently populated with either 7.78 or 11.5/1.4. The modified case already changes geometry and expansion together, so it remains unsuitable as an isolated measurement of the side plate's effect without the planned controls.

## The earlier-damage control has a finite and shorter reported horizon

NCSTAR 1-9 printed p. 568 / physical p. 634 describes the earlier-damage control as **4.0-hour temperatures with 3.5-hour ANSYS damage**, not a complete independent 3.5-hour temperature-and-damage history. The companion [NCSTAR 1-9A Section 4.4](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9a.pdf#page=156), printed p. 105 / physical p. 156, states that this control was terminated because it had stabilized and no initiating event developed:

| Published calculation-clock item | Seconds |
| --- | --- |
| ANSYS damage application in these debris-damage cases | 8.5 |
| End of the 3.5-hour-damage control | 12.76 |
| Elapsed post-damage followup in that control | 4.26 |
| First Column 79 buckling in the 4.0-hour-damage case, Section 4.3.2 | 14.7 |
| Elapsed post-damage time to that buckling | 6.2 |

Thus the control's stated followup is **1.94 simulation seconds shorter** than the interval to first Column 79 buckling in the higher-damage case. These are solver clocks, not east-penthouse-aligned observation times.

This qualifies a broad statement that the two runs establish a sharp physical threshold. It does not show the control would collapse later. A stabilized lower-damage structure need not wait as long as a collapsing higher-damage structure; elapsed time alone does not invalidate the reported stopping decision. Independent assessment needs the control's full displacement/velocity and kinetic/internal-energy histories, stopping/damping settings, stability criteria, and an extended equal-horizon check. NIST's stated stability finding remains beside, not replaced by, the duration comparison.

## Preservation and verification

The Intel store identity passed before media access. The four source PDF hashes match their preserved pins and remained unchanged. [audit.py](audit.py) passed 27 source-pin, extraction, layer-identity and arithmetic checks using PyMuPDF and pypdf. Manual raster-label transcription and complete-page visual review are separately identified; the script does not infer text from image pixels or verify native solver settings.

Both UAF originals and earlier NIST records remain in their existing preservation locations. This package adds a redundant, unaltered copy of the held NCSTAR 1-9A report, [sources/nist-ncstar-1-9a-original.pdf](sources/nist-ncstar-1-9a-original.pdf). Original means unchanged held bytes, not a first historical edition or newly authenticated master. Fresh direct requests to both official NIST download endpoints returned 403; the web reader separately exceeded its response-size limit. The local source hash, official URLs and access failures are preserved in [sources.json](sources.json), not described as a fresh successful download.

No model archive, solver, third-party contact, private production, case correspondence or litigation record was used or changed. A header-only check of UAF's public direct download confirmed an 834-byte ZIP target; it did not recover a model and is not a new suspicious finding. No aggregate-archive retry or alternative access route was pursued. Earlier source discrepancies, frozen protocols and public history remain unchanged.

To reproduce: `python3 -B audit.py --nist <NCSTAR1-9.pdf> --ara <NCSTAR1-9A.pdf> --uaf <March2020.pdf> --uaf-other <March-2020.pdf>` in an environment containing PyMuPDF and pypdf. This verifies source representations and arithmetic, not collapse physics.
