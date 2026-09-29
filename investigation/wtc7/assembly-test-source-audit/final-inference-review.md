# Final source and inference review

Research-only review, September 13, 2026. **Pass with two necessary wording
corrections and a bounded numerical-review exclusion.** This is not an
independent physical experiment, structural-engineering certification, legal
finding or historical WTC 7 reproduction.

Reviewed `report.md` at SHA-256
`240d1b9ded78ce546c72bd6f76643f8bca1c0235bd3e03e9cc786f4ad18ca48c`;
line references below apply to that 234-line version. The root report and all
source/protocol/calculation files were left unchanged. This note is the only
new worktree artifact written by this reviewer in this pass.

## Necessary corrections

| Report location and wording | Concern and decisive source | Correction |
|---|---|---|
| Lines 198-199: “The physical experiments postdate the2008 WTC7 report” | The original title page establishes the report's **May 2009** date, not the exact dates of laboratory execution. Neither the inspected original methods nor TN1749's citation to Thompson (2009) authenticates a complete dated test log or an earlier transfer. A publication date cannot by itself establish when every experiment occurred. | “Thompson's report (May 2009) and TN1749 (2012/2013) postdate the 2008 WTC7 report. No contemporaneous transfer or use of these experimental records in that investigation is established here.” Retain the separate limit against backdating the later published comparison. |
| Lines 64-66: “the connections were corrected” | In this connection-test report, “connections” could be read as the tested steel specimens. Original pp.95-96 say the **hydraulic lines/hoses** were reconnected correctly before testing and data acquisition restarted. This is not evidence of repairing the shear-tab specimens between the two portions. | Replace with “the hydraulic hose connections were corrected.” |

The first correction is substantive provenance discipline, not affirmative
evidence that the tests were actually available in 2008. The second prevents
an avoidable change in the apparent experimental intervention.

The same chronology qualification applies to the frozen original-source
review's shorthand “2009 physical experiments”: read this as experiments
**reported by Thompson in 2009**, not independently dated laboratory executions.
That earlier note is preserved unchanged; this explicit qualification records
the correction without silently rewriting its source-review history.

## Counterevidence worth making more explicit

The report already retains substantial positive evidence: tangible apparatus,
instrument checks, original failure observations, post-initial-failure reserve
in some tests, physical reasons for hole clearances, and NIST's disclosure of
disagreement. It does not reduce the evidence to two models agreeing with each
other, or infer concealed misconduct from a mismatch.

Two related additions would make the strongest competing reading easier to
evaluate without changing the conclusion:

- **Near competing limit states.** TN1749 physical43/printed25 reports calculated
  bolt-shear capacity of 147 kN and tab ultimate bearing capacity of 159 kN,
  described as only 8% apart. Physical44/printed26 proposes that ordinary
  material-strength variation could shift the governing component. This is a
  plausible, explicitly model-dependent explanation for test-to-test mechanism
  variation, especially where specimen-specific tensile data were unavailable
  (physical42). It does not establish each specimen's actual properties or
  demonstrate that either model predicted the correct failure mechanism. A
  compact sentence after report lines154-159 would preserve both points.
- **Displayed experimental variability.** TN1749 Table3-3 gives load COVs of
  11.3%, 19.5% and 7.1%; Table3-4 gives rotation COVs of 3.4%, 18.8% and 9.6%
  for the three-, four- and five-bolt groups. NIST invokes variability in its
  qualitative assessment on physical43. These are source-reported descriptive
  statistics, not a demonstrated statistical equivalence test, uncertainty
  band for model bias, or authenticated sample membership/SD convention.
  Reporting them alongside the deviation table would distinguish this positive
  context from the newly calculated native-stage COVs.

These additions are refinements, not a reason to remove the report's mechanism,
axial-force or peak-stage discrepancies. A plausible material-variability
explanation and a disclosed fit cannot substitute for per-test prediction.

## Claims that pass within the stated limits

- **Physical foundation and scope:** the bare two-span experiments provide
  reported physical observations relevant to bending, catenary transfer and
  some post-initial-failure load carrying. TN1749 physical41 expressly says the
  same beams were used in all nine tests. Eighteen connection specimens do not
  become eighteen independent assembly tests, and apparatus reuse remains
  visible. The report does not mislabel this as a heated composite-floor or
  sudden support-removal experiment.
- **Fit versus prediction:** TN1749 physical42-45 explicitly assesses gap
  treatment against experimental response and selects quadratic unloading for
  better agreement. “Not wholly an unused prediction” is supported. Calling
  every input arbitrary, every comparison circular, or the historical WTC 7
  run deliberately tuned would not be supported. The report makes none of
  those stronger claims.
- **Failure and stage discrimination:** original pp.103-107 distinguish the
  approximate maximum-moment window, initial failure, secondary failure and
  statics-check state. TN1749 physical44 identifies two later experimental
  peaks (4ST1 and 5ST3) while model peaks occur at initial failure. The report
  preserves that asymmetry, the original three-bolt footnote inconsistency,
  and different reasons for secondary-stage blanks.
- **Load definition:** original p.106 compares the sum of side reactions with
  `V_app`, while p.107 repeats the reported value on L/R rows. This does not
  uniquely authenticate a table/channel normalization. TN1749 physical47,
  Eq.(3.6), distinguishes total center load from local beam transverse shear
  and includes the vertical component of axial tension. The report does not
  silently multiply the original shear by two or infer a convention because
  a mean becomes closer.
- **Rotation definition:** original p.78 visibly prints the reciprocal
  arctangent ratio; TN1749 physical44 discloses a different reference length,
  and physical47 gives its displacement/chord formula. The report correctly
  confines the observed defect to the printed equation/definition pair. It
  neither silently repairs the original processing nor claims the plotted
  histories necessarily used the literal printed ratio.
- **Missing and defective records:** 5ST1's interrupted early record is not an
  absent experiment or an established exclusion from the NIST tables. The
  questioned left-side 3STL3 data do not by themselves invalidate every
  channel/event in 3ST3. Appendix G, original p.182, identifies separately
  obtainable data without proving present-day availability or completeness.
- **Statistical ceiling:** the stage diagnostic's paired event/rotation rule,
  missing-stage retention, two declared cohorts and sample/population
  distinction are conceptually appropriate for descriptive sensitivity on
  printed values. Additional arithmetic digits are expressly not measurement
  precision; COV is not a confidence interval; a 5ST3 stage difference is not
  labeled significant. Matching rounded summaries would still not identify
  source histories, selection rules or experimental uncertainty.
- **Causal ceiling:** the report does not infer guilt, intent, deliberate
  collapse, historical authenticity, or validity/invalidity of a withholding
  from these engineering discrepancies. A later connection comparison is
  kept separate from a WTC 7 material/member/run transfer and collapse cause.

## Numerical certification excluded from this review

I visually checked all six TN1749 table rows and both model columns against
the displayed source entries in report lines137-144. That is a source-reading
check, **not** independent reproduction of the root's interval calculations,
stage means/COVs, synthetic controls, consumer reruns or cross-schema comparison.
No result JSON, numeric implementation or pending validation output was read or
executed for this review. The report's displayed arithmetic and claims of two
independent implementations remain subject to the separately assigned completed
validation record. Filenames alone do not establish that record.

The report's conditional rounding interpretation is appropriately narrower
than “NIST arithmetic is proved correct.” Even if all interval results verify,
it establishes compatibility with a declared display-rounding hypothesis, not
the actual hidden digits, rounding implementation or experimental means.

## Actual source and control coverage

Read current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`; the investigation
charter; and complete unit `PROTOCOL.md`, `ARITHMETIC-PROTOCOL.md` and
`STAGE-DIAGNOSTIC-PROTOCOL.md`. Applied source-of-truth, evidence-falsification
and PDF skills. Read the complete report, unchanged original-source review,
and definition-crosswalk review. The latter's inspected hash was
`62e7c61d6b09738dd8e1d3f85abbc80d0c9d7b898dcc8267a6be19c9a1b7759a`.

Fresh complete visual views in this pass, including headings, axes, captions,
table bodies and footnotes:

- **Thompson:** physical/printed **1, 78, 95-96, 103-107, 182** (10 pages).
  Preserved source `sources/MSST_Thompson_2009-sirsi.pdf`, SHA-256
  `b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78`.
  [Institutional asset route](https://milwaukee.ent.sirsi.net/client/en_US/search/asset/901/0).
  Renders reused from `/private/tmp/thompson-original.ciObe5/thompson-p{page}.png`
  and `/private/tmp/thompson-definitions.15hHF2/p182.png`.
- **NIST TN1749:** physical **41-47**, printed **23-29** (7 pages), July2012
  report with February2013 corrections. Preserved source
  `../connection-calibration-audit/retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf`,
  SHA-256 `5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf`.
  [Official source](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1749.pdf).
  Renders41-45 in `/private/tmp/retrospective-tn1749.JTkzd4/tn1749-p{page}.png`;
  46 in `/private/tmp/thompson-inference.FTRSDo/tn1749-p46.png`; 47 in
  `/private/tmp/thompson-definitions.15hHF2/tn1749-p47.png`.

Earlier setup/source coverage by this reviewer remains listed, not expanded,
in `original-source-review.md` and the separate prior retrospective note.
No restrictive markings were observed on this selected technical-page set;
that is not blanket clearance. Thompson approval/signature page183 was not
rendered, displayed, searched or used. No new public search, source acquisition,
raw production inspection, data export, transmission, outreach, solver or
canonical/legal mutation occurred in this pass. Source byte hashes were
rechecked; preserving integrity is not authentication of laboratory execution.
