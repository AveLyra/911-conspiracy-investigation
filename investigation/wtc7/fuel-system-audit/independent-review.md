> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](README.md).

# Independent government-source review

2026-09-10. Separate computational source/logic review of `report.md` and `claim-ledger.md`, with `source-log.md` and `validation.md` as coverage controls. Non-blinded: the reviewer read the draft and its questions before inspecting the source pages; not a licensed engineering or forensic expert. No source independence is supplied by a second model reading the same government publications.

Selection frozen before this review's visual inspection: NCSTAR1-9 physical96,104,105,106,107,339,340,344,432,433,434,435,436,437,438,439,440,680,711; NCSTAR1A physical53,54. Existing complete-page PNG derivatives will be inspected, including headings, captions and footnotes. No new rendering, source acquisition or consequential computation.

Status: Completed the frozen 21-page visual review. Three actionable refinements were sent to the coordinating analyst before this receipt was finalized. The reviewed draft's principal documentary claims and limits are supported, subject to those refinements. This review does not revise the collapse-mechanism ranking.

## Findings requiring a response

1. **Acknowledge the fuel-balance premise already present in Scenario1a.** N9 printed369/physical435 explicitly chooses a pool consuming fuel at the rate it is pumped, gives a surface-regression rate and estimated area, then specifies a square pool for the simulation. The draft's pump-stop/burn-out paragraph correctly distinguishes stopping supply from extinguishment, but should first acknowledge this published steady-flow premise. The remaining question is whether the initial/residual pool inventory, drainage, changing ventilation and shutdown transient justify the claimed burn-out time. These pages do not establish a large accumulated reserve; missing transient verification is not positive evidence that a consequential fire persisted.

2. **Retain the distinct Floor7/9 allowances.** N9 printed373–374/physical439–440 explicitly allows diesel to contribute to initial ignition and spread on Floors7/9 and describes conditions under which a significant pumped-supply fire on the south side of Floor7 could remain visually obscured. The stated reason for rejecting a critical structural contribution includes distance/isolation from eastern structural systems. The draft preserves the southwest Floor5 allowance but should also include this Floor7/9 qualification. Use “exclusion of a significant contribution to collapse” rather than an unqualified “diesel exclusion.” Neither allowance establishes that the postulated rupture, supply or fire actually occurred.

3. **Retain NIST's stated structural-heating basis alongside the equipment gap.** N9 printed368/physical434, Fig9-3 and footnote3, models a W14x730 column with 9/16-in thermal insulation and continuous 1100°C exposure, giving approximately seven hours for a 50% strength reduction. The footnote identifies this as reduced insulation relative to nominal 7/8-in thickness. This is a modeled timescale, not a measured historical exposure or verified as-built insulation condition. A short acknowledgment prevents the pump-shutdown critique from implying no column heat-transfer reasoning was supplied. The endpoint should be NIST's predicted significant strength loss, rather than an implication of no earlier heating. The missing equipment-specific thermal/control and power-path verification remains material.

Suggested synthesis: NIST's long-duration case balances pumped inflow against consumption and compares the sustained exposure with a modeled protected-column heating timescale. Its early burn-out inference still depends on generator/cable failure, loss of the relevant pump power and a justified post-shutdown fuel history; those historical and equipment-specific links were not independently verified in this audit.

## Claims confirmed within this coverage

- **Inventory is not consumption.** N9 printed60–63/physical104–107 and NA printed11–12/physical53–54 support the distinction among nominal tank capacity, assumed contents, estimated recovery, day tanks and collecting basins. NA Table1-2 directly supports the three main nominal inventory figures. Neither publication page provides original recovery tickets or gauge measurements.
- **Publication inconsistencies are real but their cause is unresolved.** N9 printed62 says recovery in the days after the attacks and explicitly assumes initial fullness; NA printed12 says several months and states fullness categorically. N9 printed52/60 and NA Table1-2's footnote identify removal of the Floor8 equipment, while the fuel-accounting text retains three day tanks. N9 printed61 and369 give different metric equivalents for the same nominal pump rate. These are verified documentary seams, not independently verified historical errors or demonstrated simulation consequences. Preserve N9's separate `10 m³ ± 10 m³` and NA's `1000 gal ± 1000 gal` formulations as well; the child audit already does so.
- **Empty Salomon tanks do not timestamp fuel consumption.** N9 printed614/physical680 explicitly retains both pre-collapse and burning-rubble alternatives. The draft's two-direction limit is supported.
- **Pump shutdown remains an inference.** N9 printed369–370/physical435–436 describes predicted hot gas and inferred generator/distribution failure. It does not display the actual shutdown history or a manufacturer-specific coolant/engine/cable transient calculation. Its two-hour partition rating is supplied context, not itself an actual cable-failure measurement.
- **Witness and circuit distinctions are correct.** N9 printed295–296/physical339–340 attributes the engineer's account to SSB Interview1, January2004. N9 printed645/physical711 distinguishes utility availability in the substation from power to WTC7 consumers and cites interviews for emergency generation. Neither passage independently supplies a continuous pump run log or establishes a second witness independent of the earlier Commission account.
- **Negative observations have limited coverage.** N9 printed300/physical344 describes particular routes and viewing locations, no fire at an Floor8/9 viewing position, audible fires above and a separate smoky-stair/fire account. It does not establish inspection of every generator compartment. N9 printed372/physical438 explicitly permits southwest obscuration/local column heating in the modeled case. The draft's rejection of a universal non-fire inference is supported.
- **The lower-floor thermal boundary is a disclosed modeling choice.** N9 printed374/physical440 directly links the preceding reasoning to ambient initial temperatures on Floors5/6 with only conductive heating from above, and omission of explicit diesel fuel on Floors7/9. A reproduction using those same choices would not independently establish that the excluded historical exposure was absent. The draft appropriately draws no new causal ranking.

GF12, GF14 and GF15 grade conditional overstatements, not authenticated quotations asserting that NIST made those exact universal claims. Keep that distinction when using the ledger downstream. No central source-pin error was found in the checked draft claims.

## Exact coverage and integrity

Completed whole-page visual inspection, including figures/captions/footnotes, of every frozen page:

- N9 physical96 (printed52),104–107 (60–63),339–340 (295–296),344 (300),432–440 (366–374),680 (614),711 (645): 19 pages.
- NA physical53–54 (printed11–12): 2 pages.

Images were the existing `nist-source-review/derivatives/ncstar-1-9-physical-NNN.png` and `ncstar-1a-physical-NNN.png` files, read as individual complete pages. This reviewer did not rerender them or independently reproduce their image hashes; the coordinating analyst owns the separate reproduction/integrity check. No source page was cropped to replace complete-page review. Some selected pages contain adjoining out-of-scope text; reading that text did not expand the conclusions.

The command `shasum -a 256 authority/nist/wtc7/ncstar-1-9.pdf authority/nist/wtc7/ncstar-1a.pdf` independently returned:

| Source | SHA256 |
|---|---|
| NCSTAR1-9 (historical local reference `../../../authority/nist/wtc7/ncstar-1-9.pdf`; not included here) | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| NCSTAR1A (historical local reference `../../../authority/nist/wtc7/ncstar-1a.pdf`; not included here) | `03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09` |

Hashes identify the reviewed bytes; this review does not newly authenticate their acquisition history or validate their underlying claims. Source preservation and research-only boundaries follow WORKFLOW.md, START-HERE.md and CHARTER.md. The evidence/source-preservation/PDF skills informed the separation of observation, inference and visual coverage. Only this review file was changed for this assignment.

## Open limits

The Commission MFR was not re-inspected in this assignment; its exact wording, arithmetic and prior custody remain dependent on the earlier review and the coordinating analyst's checks. This review therefore does not independently certify all GF01–GF10 source transcriptions. No fuel accounting original, operating/control record, native simulation deck, coolant inventory or equipment-specific transient model was newly acquired or reproduced. The broader coolant claim should retain its bounded “reviewed sources” wording. Findings describe the draft as received; any later revision requires an explicit response check before claiming those findings resolved.

## Response check appended 2026-09-10

The original review and its initial findings/status above are retained. Its SHA256 before this appended response check was `1f11f957308825beb43665387ae9c4529a28e13f049640f8c14617d452b85c5b`. The revised `report.md` was fully reread; its reviewed SHA256 was `ab2288d5dbf47960d36ee37e4e90ffc0b22400e9b235e4db9e3e2810d85c607e`.

All three findings are resolved in that report revision:

1. The pump-stop paragraph now acknowledges the prescribed inflow/consumption balance, limits the outstanding issue to residual/transient verification and disclaims the inference that NIST supplied no balance reasoning.
2. The added Floor7/9 paragraph retains ignition/spread and potentially obscured south-Floor7 contributions as conditional possibilities. The opening now limits the rejection to a significant contribution to collapse.
3. The added Fig9-3 paragraph preserves the modeled column, insulation and heating timescale, distinguishes them from historical measurements or a universal failure threshold, and the shutdown paragraph now identifies significant predicted strength loss as the endpoint.

No unresolved corrective finding remains in the reviewed government-source report passages. This disposition addresses wording, source representation and inference boundaries; it does not resolve the missing historical records, validate the underlying physical models, independently certify the MFR transcription or alter the review's non-blinded/computational limits.
