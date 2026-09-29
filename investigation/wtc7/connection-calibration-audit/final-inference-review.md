# Final bounded adversarial inference review

Research only, September 12 local / September 13, 2026 UTC. This is an
independent agent's source/inference review, not a credentialed engineering
verification, independent physical experiment, legal clearance or historical
run authentication. Only this file is authored in this review; the earlier
`nist-validation-review.md` remains frozen.

## Candidate reviewed and scope

Read the complete `report.md` at SHA-256
`ffd69a6903be6726cc66fa87d92a1a3ccfb0aa7b4605060cf6a51e3c7440c243`.
Read the complete supporting accounts:

| Artifact | SHA-256 reviewed |
|---|---|
| `paper-source-review.md` | `4fcbe40f6b35efad49b6ab12b7a14d7ba20d60a07b5cba19100977c8be3f8258` |
| `retrospective-context.md` | `e96dd97311cdd4be9e980cce23c4effe41698563f8cb310a674837857782e681` |
| `capacity-verification.md` | `60b687138da6d03209b75626f1a0b8c7703ed20f20159fe121b72fc2b98afdf6` |
| Prior independent NIST extraction | `7391cceb80134aff4981208d4e433d6c77a54b6acb3ecf5548d1a1d12f98a92a` |

My initial NIST extraction was frozen before the paper and retrospective
accounts were read. This final combined review is necessarily no longer blind
to those accounts. It is not an additional independent experiment or an extra
independent source family.

Fresh full-page source inspection for this final pass:

- NCSTAR 1-9A PDF 59 / printed 8, including its footnote, supplementing the
  earlier 18-page full-page review.
- NCSTAR 1-9 PDF 527, 529, 531, 534, 535, 536 and 541 / printed 461, 463, 465,
  468, 469, 470 and 475. Complete pages were rendered to
  `/private/tmp/connection-nist-source.XJeO3Q/nist1-9-p<page>.png` and viewed.
- TN 1749 PDF 33-35 and 41-45 / printed 15-17 and 23-27. Complete existing
  renders at `/private/tmp/retrospective-tn1749.JTkzd4/tn1749-p<page>.png` were
  freshly viewed, including figure axes, captions and footnotes.

Source pins: NCSTAR 1-9A
`cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`;
NCSTAR 1-9
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`;
TN 1749
`5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf`.
No new experiment reports or held sources were acquired. Arithmetic reproduction
and manifest counts belong to their separately documented reviewers; this pass
checks their inferential use rather than re-executing the arithmetic, reading
raw inventories or asserting a third independent transcription.

The absent `validation.md` link was an announced pending closeout artifact, not
treated as a broken substantive evidence chain or silently treated as reviewed.

## Result: two concrete narrowing corrections

The report is substantively bounded overall. It does not dismiss calibration as
worthless, authenticate unknown inputs by arithmetic, infer fabrication from
rounding differences, backfill the 2008 model with a later report, or assign a
concealed causal ranking. Two local passages in the candidate need correction
before final closeout.

### 1. Include the same report's explicit 44 ksi Algoma treatment

**Exact candidate location:** `report.md` lines 87-92, especially the contrast
between NCSTAR 1-9 PDF 527's 44W plate and NCSTAR 1-9A PDF 55-56's nominal
42 ksi description. The candidate already says that this does not prove which
value governed a calibrated card; that qualification is useful but incomplete.

**Missing contrary context:** NCSTAR 1-9A PDF 59, section 2.2.2, expressly gives
CSA G40.21-44W, 44 ksi yield and 75 ksi ultimate strength for Algoma plate.
Section 2.2.3 describes 44 ksi thermal interpolation and separately refers to
the few components made of 42 ksi steel. Its footnote says the Algoma model
was applied only to seats of seated connections, while other connection
components used custom strength models. The footnote also preserves a
70.6-versus-75 ksi ultimate-strength distinction, not resolved by this review.

**Plausible adverse inference:** readers could mistakenly conclude that one
report used 42 ksi throughout where the other used 44 ksi, or that the apparent
cross-report difference directly demonstrates weakened global connection
properties. The published explanation itself gives a more specific branch
distinction and restricts that inference.

**Required correction:** include PDF 59 and characterize the problem as an
internal description/grade-to-property mapping question, alongside the explicit
44 ksi treatment, rather than principally a disagreement between reports.
Retain the unresolved actual location/custom-property mapping. Do not replace
42 with 44 in source data or declare the actual historical inputs reconciled.
This correction is supported by a fresh full-page source view, not deference
to NIST's authority.

### 2. Limit the table's calibration claim to its demonstrated family

**Exact candidate wording:** line 192, “WTC7 shell connections were calibrated
to spring output, not independently measured in Figures3-4/3-5”.

**Scope risk:** the seven plotted pairs are fin connections. The text describes
header/knife development as similar; seated and other connections follow
distinct accounts. The broad phrase can be read as encompassing every shell
connection family, although the body of the report handles this distinction
correctly.

**Required correction:** use “The displayed WTC7 fin-shell connection models
were calibrated to spring output” (or an equally explicit family restriction).
This is a wording-scope correction, not a finding that the fin calibration
claim is false.

Both findings were sent to root with exact source locations. Correction status
must be checked against a later pinned candidate, not presumed from delivery.

## Tests of the remaining claims

### Calibration is neither physical proof nor worthless self-comparison

The report explicitly retains the engineering drawing basis, nonzero capacities,
reported steel tests, and successful aspects of curve reproduction. Its table
also says not to treat fitted agreement as worthless. The selected source pages
do support a narrower, useful criticism: fitting a shell representation to a
spring target primarily checks target reproduction; agreement between two
formulations can expose implementation differences but cannot by itself expose
an assumption both share. Missing holdout evidence is described as a validation
limit, not proof that the model is wrong.

The fin energy/force contrast and slab/coarse-steel observations match my earlier
independent source reading. They remain qualitative, observable-specific and
explicitly not estimates of whole-building error. Displacement is not confused
with time. The two resistance directions are retained, preventing an inference
that every approximation necessarily promotes collapse.

### Strongest physical and modeling counterevidence remains visible

NCSTAR 1-9A's tensile comparisons provide genuine reported experimental
constraints, though not recovered WTC7 connection tests. Added vertical discrete
resistance and seated-connection contact/bearing contradict a blanket assertion
that all secondary support was omitted. NCSTAR 1-9 PDF 531's bolt assumptions
raise calculated resistance, and PDF 529's resistance-factor choice aims at
ultimate capacity rather than reduced design capacity. Correct arithmetic does
not establish their physical applicability; the report does not claim it does.

TN 1749 compares with actual reported component and assembly tests, reproduces
broad stages and sharp resistance drops, and reports relatively close ultimate
load comparisons. Those are affirmative constraints even though the source
also admits incomplete post-ultimate measurements, mismatch of failure modes
and fit-informed unloading choices. None of those affirmative comparisons is
silently discarded because a held-out validation population is not shown.

### Later TN 1749 is not substituted for the inaccessible 2008 paper

Fresh full-page inspection confirms the key limitations in the report:
Rex/Easterling's displayed experimental endpoint precedes the simulated
post-ultimate branch; Richard's curve is a best fit to several tests, and its
endpoint is not reported as fracture; the nine Thompson executions reuse beams
and suppress beam-web bearing deformation with doublers; eight histories are
displayed; experimental failure modes and later peaks are not all reproduced;
and quadratic unloading was selected for better agreement.

The report expressly identifies TN 1749 as a 2012/2013 source, primary for its
own model choices but secondary to the original physical reports. It separates
the 2008 spring-law attribution from an authenticated WTC7 implementation. This
is the correct evidentiary ceiling. In particular, numerical bolt cooling is
not relabeled as a physical fire experiment, and model gaps/unloading choices
are not called evidence of misconduct.

### Rounding, labels and absence do not become fabrication findings

The arithmetic section says all row intervals are compatible with a declared
rounding possibility, not that these were NIST's actual unrounded values. It
retains the 79/16 row and printed maximum issue rather than erasing it; it
separately preserves the stud formula's displayed precision discrepancy without
silently imposing a favorable parameter envelope. These distinctions avoid
both accusation and unwarranted authentication.

The report's numerical claims agree with the complete independent verification
account at the reviewed hash. This is a consistency review of that account,
not a new numerical execution. The verification account separately discloses
source-label aliases, unsupported “Beams” additions in four root labels,
unmatched failure-mode metadata and failed stages. Nothing in `report.md`
claims exact source-label identity, all source metadata independently agreed,
or a failure-free execution history.

The inventory paragraph correctly restricts its negative result to extensions
in a manifest; it does not conclude that spreadsheet data were never released.
It cannot by itself close the location/calibration-mapping gap. This pass did
not independently recount that manifest and relies on the promised closeout
receipt for its count and coverage.

### No cause ranking is smuggled into the grades

Grades apply to stated methodological propositions, not probabilities of fire
or intervention. The report does not infer that model gaps identify a historical
actor, that a discrepancy rules out all fire pathways, or that a partial
validation favors innocence. Equally, it does not demand proof of a conspiracy
before treating a concrete modeling uncertainty as worth investigating.
It keeps the next task finite: trace original experiments and their precise
comparison to later models. That is scientific source work, not authorization
for solver changes, legal steps, outreach or new sensitive disclosure.

## Closeout status

Conditional source/inference acceptance after the two corrections above and
the announced validation/navigation closeout. No other material overstatement
was found within the selected-page scope. This is not a guarantee about pages,
experiments, solver inputs, raw production contents or global collapse physics
that this bounded review did not inspect.

## Revised-candidate closeout

After the review above, root preserved the original complete report as
`report-before-source-context-review.md`; its SHA-256 still exactly equals
`ffd69a6903be6726cc66fa87d92a1a3ccfb0aa7b4605060cf6a51e3c7440c243`.
I read the complete revised `report.md` and compared its full text against that
preserved candidate. Revised SHA-256:
`9b4d9c4b6a3a54b2abb4d1751fbc46d325d7ea981f76c832425c293c03c6e1ff`.

The diff contains three localized changed passages:

1. The material-grade passage now includes PDF 59's explicit 44 ksi Algoma
   model, its seat-only application and separate custom connection models,
   alongside the few 42 ksi components. It expressly rejects the inference
   that the global model lacked a 44 ksi representation, while preserving the
   unresolved grade/location/custom-card mapping. **Finding 1 is resolved.**
   The added statement about the same room/elevated-temperature failure-strain
   criterion is also present on the previously fully viewed PDF 59. It is
   correctly kept distinct from the report's temperature-dependent strength
   treatment and does not authenticate a particular historical input card.
2. The table discussion now states that the ratios are room-temperature F/H/K
   capacities, not seated-connection vertical capacities at Columns 79/81.
   NCSTAR 1-9 PDF 535-536, already fully viewed in this review, supports that
   limitation. It strengthens the existing warning against using these ratios
   as a floor-impact capacity or whole-building safety factor.
3. The claim-strength row is now restricted to the displayed WTC7 fin-shell
   models. **Finding 2 is resolved.** No broader family validation is introduced.

No additional substantive change appeared in the full-text diff. The revised
report retains the affirmative physical/modeling evidence, uncertainty about
rounding and historical mappings, retrospective-source limit, and no-ranking
conclusion assessed above. The three pinned PDFs were rehashed and still
matched their recorded hashes. The earlier independent NIST extraction remains
unchanged at `7391cceb80134aff4981208d4e433d6c77a54b6acb3ecf5548d1a1d12f98a92a`.

**Source/inference closeout: accepted for this exact revised report within the
stated bounded scope.** The two requested substantive corrections are verified,
not merely reported as applied. Root's validation/navigation artifact was still
being prepared at this check and has not been reviewed here; this closeout is
not a claim that all unit packaging or independent numerical reruns are complete.
No previous review text, source PDF, raw/model input, legal file or other
reviewer's file was altered by this reviewer.
