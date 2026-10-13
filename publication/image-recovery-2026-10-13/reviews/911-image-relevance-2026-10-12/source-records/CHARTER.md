# Sherlock-assisted WTC 7 investigation charter

**Version:** 1 — 2026-09-08  
**Status:** Active research goal; investigation not completed; not an expert report or litigation finding.  
**Authority:** This file controls investigation scope and method commitments. Source records control evidence; Sherlock structured records control recorded case state once a conforming case is initialized. Generated reports are views, not independent evidence.

## Objective and decision

Determine how far accessible evidence and defensible physical analysis can distinguish explanations of the WTC 7 collapse. Test the strongest technically specified versions of competing explanations, including deliberate intervention, without presuming either official correctness or wrongdoing. Identify which observations each explanation accounts for, what it requires but has not demonstrated, what contradicts it, and what new evidence could change the assessment.

The deliverable is an independently checkable investigation, not a promise to identify a unique cause. Missing evidence may impose a real limit. A scientifically defensible unresolved result is preferable to an invented probability or an unsupported verdict.

The user owns decisions on new costs, outreach, publication, confidential disclosures, filings, and research-to-case promotion. The active goal authorizes local research and ordinary, non-sensitive public-source retrieval. No token budget was specified. Expensive computation, licensed solvers, laboratory work, and outside expert engagements require a separate proposal and approval.

## Competing explanations and inference boundaries

Maintain separate tests for:

1. **NIST's specific proposed fire-to-failure sequence.** A developed account to test, not a premise to accept.
2. **Other fire-triggered structural pathways.** Failure of NIST's exact sequence would not automatically falsify this broader family. Each useful alternative needs its own specified initiating and propagation mechanism.
3. **Deliberate support removal.** Distinguish conventional explosive, thermal/chemical, mechanical, and mixed proposals where evidence or a testable mechanism justifies the distinction. Do not invent operational device specifications or treat an unconstrained ability to remove arbitrary members as a validated explanation.
4. **Other or mixed mechanisms and underdetermination.** An open category for specified, evidence-grounded alternatives, not an explanation that receives credit merely because it is unconstrained.

These categories are not necessarily mutually exclusive. Separate **initiation**, **support loss**, **propagation**, **observed motion**, and **intent**. A calculation that reproduces motion after prescribed support loss does not independently identify what caused that loss, whether it was deliberate, or who was responsible.

Maintain two assessments: (a) physical compatibility with independently checked observations, and (b) the overall evidentiary comparison, explicitly including conditional weight assigned to published models and documentary evidence. Keep likelihood assumptions and prior/contextual judgments visible. Do not translate historical rarity, institutional reputation, motive, absence of a matched precedent, or public confidence into an unstated numerical prior. A failure to rank is not a 50–50 finding.

## Questions the investigation must address

| ID | Question | Required discriminator or limiting result |
|---|---|---|
| Q01 | What fire is actually visible, where, and when? | Visibility-qualified façade/floor/time observations; distinguish no visible flame, obscured area, and unobserved interior. |
| Q02 | Are modeled fire duration, spread, fuel, ventilation, and temperature histories consistent with independent evidence? | Source-pinned input audit and plausible alternatives; quantify downstream effects where inputs permit, otherwise identify the missing dependency. |
| Q03 | What moved first, and how did movement propagate? | Calibrated, uncertainty-aware multi-point tracks and cross-camera timing; penthouse, roof, façade, and other observable features, not one chosen point. |
| Q04 | How long and where was acceleration compatible with gravity, and what resistance does that constrain? | Reproducible fits, interval sensitivity, projection/deformation limitations, and an explicit force/mass boundary. A roofline point is not automatically the building's center of mass. |
| Q05 | How symmetric, vertical, or footprint-contained was the collapse? | Define measurable spatial and temporal quantities; compare views and known geometry, retaining out-of-plane and obscuration uncertainty rather than adopting verbal descriptions as measurements. |
| Q06 | Can a localized initiating failure plausibly produce the observed interior/exterior sequence and rapid widespread support loss? | Explicit load paths, connection behavior, loss of bracing, buckling, redistribution, contact, and time/energy accounting. Distinguish a physically possible story from a demonstrated building-specific chain. |
| Q07 | What do recorded sounds, flashes, warnings, and early reports establish? | Source-chain and recording-quality analysis, synchronization and propagation uncertainty, detection limits, and alternatives to each interpretation. |
| Q08 | Which features distinguish documented fire outcomes from documented demolition methods? | Independently grounded comparator labels, declared inclusion criteria, matched characteristics, and specificity limits. |
| Q09 | Do physical or documentary records affirmatively discriminate an intervention or evidence-handling explanation? | Building-specific attribution, custody, chronology, independently corroborated records, and an explicit bridge from an act to mechanism or intent. |
| Q10 | Which conclusions depend on unavailable records, discretionary modeling choices, or inadequate tools? | A dependency map, sensitivity results where feasible, and exact records/tests needed to resolve each material uncertainty. |

## Scientific controls

- **Preserve before interpreting.** Record source location, retrieval date, acquired-byte hash, edition, custody/authenticity status, and derivation lineage. A hash establishes integrity relative to captured bytes, not historical authenticity. Preserve originals and failed or superseded analyses.
- **Do not count copies as corroboration.** Group footage, syndication, excerpts, testimony repetitions, and analyses by underlying origin. Independent cameras can independently constrain motion without independently authenticating every claim in a compilation.
- **Separate evidence layers.** Every material claim states whether it is observed, derived, model-dependent, inferred, hypothesized, or speculative; its exact source/time/page pin; assumptions; reproduction status; strongest alternative; falsifier; and strength grade with reasons. Use existing SRC/EXH references where applicable without minting formal case facts.
- **Declare bias-sensitive choices before the next analysis.** Version inclusion rules, time sampling, track selection, fitting intervals, comparator selection, parameter ranges, and evaluation metrics. Prior familiarity with WTC 7 is acknowledged: this is not a retroactive preregistration. Label exploration and protocol changes; preserve their reasons and earlier outputs.
- **Hold out genuinely unused evidence.** Identify what was used for construction/tuning versus evaluation. Alternate clips of the same event are not independent event-level training/test samples. If no clean holdout exists, label the evaluation retrospective rather than independent validation.
- **Carry uncertainty through the chain.** Keep source, clock, geometry, annotation, parameter, and model-discrepancy uncertainties distinct. Report ranges and sensitivity; do not hide disagreement behind one best-fit line or one animation.
- **Test alternatives fairly, not identically.** Apply the same observational constraints and claim standards; account for different model complexity and tuning freedom. Do not grant an unspecified mechanism unlimited adjustable failures. Actively seek evidence against whichever explanation currently appears strongest.
- **No synthetic evidence.** AI may help search, transcribe, annotate, or fit validated measurements. Generated frames, interpolated imagery, reconstructed audio, or simulated failures must remain labeled derivatives/simulations and cannot supply missing historical observations. Human spot-checks and synthetic ground-truth tests must precede consequential automated measurement.
- **Negative evidence requires an opportunity to detect.** A missing sound, residue, document, or visible event has weight only to the extent that acquisition, preservation, sampling, and instrument coverage could reasonably have detected it. Report unsearched and destroyed/unavailable portions separately.
- **No automatic legal conclusion.** An engineering mismatch does not establish intentional falsification, a particular actor, or an invalid withholding. Preserve relevant technical results for separately reviewed legal analysis; do not amend pleadings or the factual record through this goal.

## Work packages and acceptance gates

### WP0 — Reproducible setup and evidence map

Start with the existing public-source research map, acquired media manifests, and the Collapse Reconstruction Workbench (CRW). Treat prior memos as leads to underlying evidence, not additional witnesses. Inventory available originals/access copies, duplicates, source families, inaccessible originals, models, analysis scripts, and current capability gaps.

Record Sherlock/CRW code hashes or an actual source-control revision, runtime and dependency versions, and commands. Recheck the current software rather than treating an earlier passing test suite as a permanent certification. Keep synthetic pilot output separate from real case state.

**Exit:** Every selected initial input has a located artifact or explicit unavailable status, provenance and sensitivity classification, a source-family assignment or documented uncertainty, and a mapped question. The local analysis route is auditable; no generic charter or software approval flag is represented as actual user review.

### WP1 — Independent fire-observation map

Declare a coverage plan for all available façades, floors, and time intervals. Record camera position/view, clock uncertainty, resolution, smoke, reflections, obstructions, and windows/floor assignments. Annotate visible flame/smoke and observation quality against the area actually observable. Examine contrary images and preserve disputed annotations; independently re-annotate a declared sample including borderline cases.

Compare this map to the source-pinned NIST fire inputs and reported mismatches, including floor-to-floor substitutions and prescribed ventilation/ignition choices where documented. Do not infer steel temperature or an interior heat field from exterior flame appearance alone. Use thermal calculations only with stated, defensible boundary conditions and sensitivity bounds.

**Exit:** A reproducible visibility/observation timeline, disagreement and uncertainty record, and input-by-input agreement/mismatch table. For each apparent overestimate or underestimate, distinguish demonstrated observation mismatch from its unmeasured structural consequence.

### WP2 — Multi-angle motion and acoustic constraints

Preserve presentation timestamps, frame-rate changes, duplicate/dropped frames, edits, stabilization transforms, and original audio/video alignment. Calibrate scale and perspective where possible; track multiple features with positional uncertainty. Define apparent symmetry, onset ordering, verticality, and debris/footprint extent operationally before comparing them.

Fit position histories before drawing acceleration conclusions. Compare reasonable fitting windows, change points, smoothing choices, and deformation assumptions; retain residuals and raw annotations. Align cameras from identifiable shared events with uncertainty, not by shifting clips until a desired sequence appears. Separate directly timed within-camera events from inferred cross-camera ordering.

For sound candidates, record microphone/location uncertainty, clipping, automatic gain, compression, bandwidth, noise, possible re-dubbing, and sound-travel delay. Compare only after quality and detectability assessment; amplitude in separately processed recordings is not a direct sound-pressure comparison. Do not equate a loud transient with an explosive charge or nondetection with exclusion.

**Exit:** Reproducible tracks, timing maps, candidate audio-event table, calibration/quality reports, and bounded kinematic/force constraints. A second analysis must reproduce material measurements within declared tolerances, or disagreements remain explicit. Insufficient footage quality produces a stated limit, not a fabricated track.

### WP3 — Structural and model audit

Map the causal chain from exposure through temperatures, thermal expansion/weakening, floor and connection behavior, loss of lateral restraint, column instability, redistribution, and global motion. Audit initiation separately from post-initiation replay. Identify simulated processes versus imposed damage, member removal, or transferred solver state.

Begin with dimensional checks and reproducible bounded calculations for dynamic floor impact, energy absorption, bracing length/buckling, load redistribution, and propagation times. A toy model is a constraint or sensitivity illustration, not a WTC 7 validation. Do not infer an exact number of failed floors from load ratios alone.

For available NIST and alternative analyses, map geometry, drawings, materials, connections, boundary/contact conditions, failure criteria, solver versions, temperature fields, handoff procedures, and output/render provenance to primary records. Attempt only genuinely available reproductions. Where feasible, test documented alternative inputs and report collapse and non-collapse runs, reaction forces, energy balance, residual support, failure sequence, and numerical warnings. Do not recreate withheld choices by guessing and call the result a reproduction.

**Exit:** An assumption/dependency ledger and common-observable comparison, with sensitivity results for executable tests. Separate numerical verification, physical validation, calibration, and historical identification. Every infeasible material test identifies the missing file/input/expertise and the result that would change the assessment. Building-specific engineering conclusions remain qualified pending competent expert review.

### WP4 — Comparator study

Build a search log and selection matrix covering documented fire-exposed buildings that survived, partially collapsed, or totally collapsed, and documented explosive implosions, mechanical/pull-down/top-down demolitions, and other removal methods where reliable examples exist. Record exclusions and failed searches. Include unlike cases for narrow mechanism questions without representing them as closely matched precedents.

Match or explicitly stratify structural system, geometry, height, floor system, loading, damage, protection, fire duration/exposure, suppression, deliberate pre-weakening, and recording conditions. Establish cause/method labels independently of the footage being classified; a collapse publicly attributed to fire is not automatically a validated fire control. A hand-picked video library is not a population from which to calculate historical base rates.

**Exit:** A documented comparator inventory and feature-specific comparison with confounders and counterexamples. No classifier-derived causal verdict or numerical probability without defensible independent labels, event-level holdouts, calibration, and an appropriate sampling model. Start with measurement and comparison, not AI training.

### WP5 — Physical provenance and documentary tests

Use the existing operational-evidence plan as a lead register, rechecking underlying public sources. Review building/sample attribution, collection/transfer/testing records, debris disposition, warning/report source chains, and any specific, evidence-grounded authorization/access/procurement/logistics lead. Look for affirmative corroboration and ordinary explanations; distinguish genuine independent origins from a common report repeated through multiple channels.

For alleged concealment, identify the record, chronology, preservation duty or practice, decision/instruction, responsible role/person where reliably documented, and competing administrative or emergency explanations. Lost evidence, document withholding, access, opportunity, or later benefit does not alone establish a deliberate operation or suppression of its evidence. No private-person fishing expedition or accusation from association.

**Exit:** A public-source lead disposition table: corroborated within a stated ceiling, contradicted, unresolved, exhausted within documented search coverage, or awaiting a precisely described record. No outreach, witness contact, new FOIA submission, or fee commitment without approval.

### WP6 — Adversarial review and synthesis

Give separate analytical reviewers the strongest fire-based and intervention-based cases, the same observation set, and the common test criteria. They must identify what would falsify their own favored explanation. Computational agent review is not equivalent to an independent licensed structural/forensic expert; state reviewer independence and qualifications accurately.

Produce an updated evidence matrix and explanations of any ranking change. Separate fit to terminal motion from explanation of initiation and evidence of intent. Report ties/partial orderings or non-identifiability when justified; provide no unsupported percentages. For model-fidelity results, identify affected record categories and capability limits without silently turning technical uncertainty into a legal holding.

**Exit:** Reproducible material outputs, critical-review issues answered or prominently unresolved, all contrary results retained, and a final assessment stating what changed, why, what did not change, and the highest-value next discriminating records or tests.

## Sherlock operating boundary and improvement loop

Sherlock is the provenance/claim/action/report layer. CRW is a separate media provenance and derivative tool. Neither currently supplies a validated full collapse inverse solver. Add narrowly justified capabilities only through documented tests; do not mistake a roadmap feature or a successful synthetic pilot for a working forensic method.

Use only actual agent privileges. Do not supply a fictitious reviewer/publisher identity, activate a high-stakes theory as if a human reviewed it, accept findings on the user's behalf, or create publication/promotion authorization. Keep agent proposals distinct from accepted findings. Disable publication and canonical promotion operationally for this research pilot until the relevant controls and actual approvals are established.

The present CLI creates a charter with a generic scope and empty constraints. Until full-scope charter creation/versioning is supported and tested, this document remains the controlling research charter; do not silently replace it with those defaults or hand-edit an immutable Sherlock ledger. Public-source inventory and method preparation can proceed independently.

Maintain actionable notes in [SHERLOCK-FEEDBACK.md](SHERLOCK-FEEDBACK.md). When an actual pain point or improvement need arises:

1. Deduplicate it against existing notes and record the observed behavior, desired behavior, investigation impact, priority, smallest non-sensitive reproduction, and measurable acceptance test.
2. Send the sanitized technical note to the existing Sherlock task **“Define Phase 0 invariants”** (`01a074ee-3dc0-7821-9125-aa8d9ffc2f8c`; project `SHERLOCK`). Ask it to record/triage notes, not to treat them as blanket authorization for implementation or case access.
3. Record the delivery/acknowledgment and any destination issue ID. A sent message is not a fixed or independently verified feature.
4. Retest any claimed fix with synthetic or approved data and record code version, result, and residual limitation before depending on it. Batch related small notes; send evidence-integrity or blocking issues promptly.

The feedback loop is part of active investigation work, not a new scheduled monitor. Software capability feedback may be sent under the user's request only when non-sensitive. Do not transmit case documents, private paths containing personal information, confidential metadata, litigation strategy, protected-source information, credentials, or sensitive security details. When sensitivity is uncertain, retain the note locally and obtain exact-payload/destination approval before sending. Technical feedback authorization is not authority for unrelated project changes.

## Completion, pauses, and resumption

This goal is **not complete when the charter is saved, Sherlock runs, or a preferred explanation is selected**. Completion of this first full evidence cycle requires:

- Every work package has completed its feasible, declared tests and documented coverage; material accessible leads have not been abandoned merely because they are inconvenient.
- Every material conclusion is traceable to preserved inputs and transformations, with independent reproduction or an explicit, consequential reproduction limitation.
- Competing predictions, failed analyses, disconfirming observations, dependency, and uncertainty remain visible.
- Critical review is addressed; missing records and specialist prerequisites are identified specifically, with their impact on the permitted conclusion.
- The synthesis and its methods/results can be checked by another investigator, while no claim exceeds the evidence or the investigators' competence.
- Sherlock pain points encountered have been logged and safely routed, with sent, acknowledged, fixed, and verified states kept distinct.

An unavailable record can bound a conclusion after documented retrieval attempts; it cannot supply the missing result. A software gap first calls for a safe alternative or a bounded capability request. When a necessary next step requires new authority, spending, private access, or expert engagement, report the precise need and ask the user; continue independent authorized work where useful. Do not expand indefinitely into unrelated events or declare scientific closure because a resource is unavailable.

Future materially new evidence starts a versioned follow-up cycle with an explicit changed-evidence list. Do not rewrite the earlier record of what was known.

## Initial state and next milestone

On adoption, the active app goal is established, but no real Sherlock case has yet been initialized for this charter. Existing synthetic demonstrations remain synthetic. No causal ranking is changed by goal creation.

**First milestone:** WP0 source/capability manifest and test protocols for the existing public media corpus and the reported fire-input discrepancies. Reconcile current source hashes and dependencies; specify the first bounded independently reproducible measurement. Record the full-charter creation gap in the Sherlock feedback channel. Do not begin training a cause classifier or choose a collapse mechanism as a label.

Existing entry points (not new corroboration):

- [Current collapse synthesis](../wtc7-collapse-evaluation-synthesis.md)
- [Video comparison and acquisition records](../wtc7-video-comparison/README.md)
- [CRW implemented scope and roadmap](../collapse-reconstruction-workbench/README.md)
- [NIST claim-strain audit](../nist-claim-strain-audit.md)
- [Operational-evidence leads](../wtc7-operational-evidence-plan.md)

The existing research map remains the navigation authority; this charter does not replace source records, prior results, or separate legal analysis.
