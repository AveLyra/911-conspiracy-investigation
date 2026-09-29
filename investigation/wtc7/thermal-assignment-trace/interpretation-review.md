# Interpretation review of the thermal-assignment trace

2026-09-12. Bounded review of the draft's reasoning, source attribution, and competing readings. This is not a second numerical reconstruction. The reviewer read `report.md` in full and compared it with the frozen `method-source-review.md`; no produced JSON, raw model data, solver output, or independent-reader result was opened. The source-of-truth and evidence-falsification controls continue to apply.

Reviewed draft SHA-256: `69250a304cd0c57eabe86db382c725215f50ddaa871213f5a5b0ac414d160787`. Frozen methods-note SHA-256: `8a24d3140fb3829606185b9867e83949c8e25085b812537b98aaf21deb16409d`. Line numbers below refer to that draft snapshot. The numerical comparison was still marked pending in the reviewed text.

## Two concrete corrections

1. **Line 156 changes the counted entity from nodes to assignments.** The claim-table text is: "The selected63 unequal regional assignments occur at single-part nodes." Lines 12-13 and the table at 67-71 instead describe **63 nodes, each carrying two assignments**. The claim-table wording can be read as only 63 assignment rows, obscuring the total of 126 rows for these nodes. Replace it with: **"The 63 selected regional nodes carrying unequal TS coefficients connect only to PID 179 in the examined mesh."** This preserves the actual topology claim without compressing nodes and assignments into one unit. It is a report-internal consistency correction; this reviewer has not independently certified the numerical count.

2. **Lines 166-167 prematurely name the pattern's cause.** The text says the next records can "test whether the repeating spatial boundaries were intentional, consolidated before processing, or handled by the solver as intended." The observed quantities are repeating rows and seven elevation groups. Lines 96-100 correctly present spatial-segment boundaries as a hypothesis to check. Calling them "the repeating spatial boundaries" later promotes that hypothesis into an identified feature. It also leaves "consolidated" grammatically attached to boundaries rather than rows. Replace the passage with: **"These records can test whether the repeated rows arose from overlapping spatial selections, another documented export convention, or an error, and establish how preprocessing and the solver resolved them. The seven elevation groups do not themselves identify spatial-segment boundaries."** This retains both benign and erroneous possibilities without assuming intent, interpolation, or a solver policy.

## Useful disconfirming detail already present in the table

The table at lines 86-94 contains a directional check that the prose does not mention: the later TS is lower in **five** groups and higher in **two**. Because each group contains nine nodes, that is **45 nodes with lower later coefficients and 18 with higher later coefficients**, as arithmetic from the draft table. This is not an independent input result or a claim about which coefficient operated historically.

A useful optional sentence after the table is: **"In file order, the later supplied coefficient is lower for 45 of these nodes and higher for 18, so the differences do not all run in one direction. This comparison does not select an effective solver temperature."** It explicitly disconfirms a uniform upward change in the displayed coefficients while leaving the unknown composition rule open. It does not disprove temperature inflation under every possible rule, and should not be used that way.

## Specific interpretations that are supported at the stated ceiling

- **Single-part counterexample:** Lines 73-78 correctly refute the explanation that every regional repetition is solely attributable to sharing nodes between distinct incident structural parts. They retain different thermal segments or export selections within one part as unresolved possibilities. The 18 shared regional nodes with no repetitions provide a useful contrasting observation; shared-part membership alone is neither necessary nor sufficient for repetition in this selected region. This conclusion remains conditional on the independently checked incidence reconstruction, not on PID being a thermal-region identifier.
- **Seven groups:** Lines 80-100 clearly label the grouping as a post-result description and deny inferred floor names, export batches, interpolation, intent, or policy. Regular spacing makes a boundary-related export convention worth checking but does not identify one. Correction 2 restores the same ceiling at the close of the report.
- **Nine rows:** Lines 52-55 and 121-126 distinguish assignment records from time steps. The common TB/LCID statement, the single keyword-block account, and the primary source's one transferred profile support preserving that distinction. They do not prove why the export generated nine records or establish which values the historical solver used.
- **Positive model association:** Lines 144-150 include the matching published shell/beam/solid/discrete counts and explicitly leave rigid entities unreconstructed. That is meaningful correspondence with the reported model size. The stated limits on executable identity, properties, temperatures, and physical validity are appropriate. This reviewer confirms the NIST side from the earlier complete-page inspection; the released-count side is still conditional on the separate numerical work.
- **Build identity:** Lines 25-29 distinguish the NIST-reported `mpp971dR4 beta, revision 41161` from an authenticated executable/deck match. This accurately reflects the frozen source review.

The passages denying established error, inflated temperatures, manipulation, and causal ranking are supported by the unresolved implementation and run-state dependencies. No additional physical conclusion follows from this review.

## Small clarity edit

Restore spaces between words and quantities throughout the draft, particularly `all63`, `revision41161`, `finds952`, and `by3.8862`. Use `TB = 0` and `LCID = 2` where reporting parameter values. This is a readability correction, not a change to the recorded numbers.

No frozen artifact or draft was edited by this reviewer. This review does not certify completion of the separate numerical comparison.
