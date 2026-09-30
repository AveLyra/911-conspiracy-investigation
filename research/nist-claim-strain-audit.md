# NIST WTC 7 claim-strain audit

**Prepared:** 2026-09-04  
**Status:** Working technical research; not an expert report, factual finding, or pleading text  
**Question:** Which observations, model results, and evidentiary limitations genuinely strain propositions NIST makes about WTC 7, and what files would resolve each issue?

## Scope rule

This is not a general demolition comparison and does not attempt to disprove claims that NIST never made. It tests only source-pinned NIST propositions. A finding of strain means that a proposition needs further testing, qualification, or a fuller record; it does **not** establish a competing cause, fraud, or intentional intervention.

The distinction is essential:

- **Direct mismatch:** NIST’s stated output conflicts with a measured observation.
- **Validation gap:** the public material does not permit independent testing of a stated correspondence.
- **Sensitivity risk:** a result materially depends on a choice whose reasonable alternatives have not been shown.
- **Evidence limitation:** a missing source constrains all relevant hypotheses and is not affirmative evidence for one.

## NIST propositions and the current audit

| NIST proposition | Source pin | What presently strains it | Classification / current strength | File or test that would resolve it |
|---|---|---|---|---|
| The visible global descent followed an earlier, staged internal failure: floor failures around Column 79, Column 79 buckling, wider core failure, then north-façade descent. | `authority/nist/wtc7/ncstar-1a.pdf`, Table 3-1, pp. 42–43; `ncstar-1-9.pdf`, §5.7.6. | The public video records precursor motion, but its principal views obscure the lower/interior support-loss zone. The sequence is therefore not directly observed end-to-end. | **Validation gap — B.** The visible chronology is a useful constraint, not direct confirmation of every hidden failure step. | Original camera files; time-aligned model member histories; synthetic-camera outputs from the exact baseline run. |
| The 4.0-hour fire/damage state is the relevant collapse-producing state, while the 3.5-hour state did not initiate global collapse. | `ncstar-1a.pdf`, pp. 41–42; `ncstar-1-9a.pdf`, §4.4. | The narrow reported threshold is consequential where fire history, connection behavior, and damage transfer are uncertain. Public material does not supply an ensemble demonstrating robustness around the transition. | **Sensitivity risk — C.** A threshold is physically possible; its existence alone is not suspicious. | Complete 3.5–4.0-hour inputs/results; intermediate and perturbed runs; stated parameter ranges and failure criteria. |
| Global collapse analysis used imposed debris damage, temperature ramping, and transferred ANSYS fire damage to initialize the LS-DYNA run. | `ncstar-1a.pdf`, pp. 38–39. | NIST describes instantaneous application of some accumulated damage for numerical initialization. Public material does not establish whether gradual or alternate handoffs yield the same onset, timing, and motion. | **Sensitivity risk — C.** This is a model-transfer question, not a claim that NIST said real-world damage occurred instantaneously. | Handoff scripts/files, keyword decks, include trees, solver versions, and pre-specified gradual-handoff sensitivity runs. |
| The best-fit model’s timing and visible progression are consistent with observed collapse behavior. | `ncstar-1a.pdf`, Table 3-1, pp. 42–43; `ncstar-1-9.pdf`, §5.7; NIST WTC 7 FAQ, question 25. | NIST acknowledges that its predicted inward deformation of the upper exterior walls after global collapse is absent from video. It also reports sharply increased breakup uncertainty and omitted nonstructural stiffness/strength. Those facts make late-stage exterior-motion validation methodologically dubious; NIST's explanation accounts for the divergence but does not turn it into visual corroboration. | **Direct mismatch after global onset — C; late-stage visual-validation weakness — C.** See [Exhibit A](wtc7-video-comparison/nist-simulation-footage-crosscheck-2026-09-30.md). | Full output histories; model-to-camera mappings; the pre-existing validation criteria; sensitivity runs for omitted components; comparison against camera measurements not used to select the run. |
| The north façade’s measured Stage 2 near-free-fall descent is consistent with the collapse sequence. | `ncstar-1a.pdf`, §3.6, pp. 44–46. | The public account measures the façade motion, but does not provide a released baseline roofline acceleration/resisting-force history showing the global model independently reproduces the same interval. | **Validation gap — C.** Near-free fall requires negligible net upward resistance on the tracked path; it does not identify why that condition existed. | Native source-frame measurements, calibration/uncertainty record, LS-DYNA nodal displacement/velocity/acceleration and contact/force histories. |
| Fire-induced thermal expansion and resulting connection/floor failures initiated the Column 79 pathway. | `ncstar-1-9a.pdf`, initiation analysis; NIST WTC 7 FAQ. | The connection geometry and failure sequence are technically contested, including by UAF. That disagreement is not itself contrary evidence, and UAF’s prescribed broad failures do not establish a cause. The decisive question is whether the NIST geometry, contact, restraint, and failure rules are reproducible and robust. | **Contested model input / sensitivity risk — D pending source-level audit.** | Construction drawings, connection schedules, ANSYS model inputs, contact definitions, material/failure cards, run logs, and independent reruns. |
| The event was not caused by explosives. | NIST WTC 7 FAQ; `ncstar-1-9.pdf` audio/video analysis. | No direct mismatch in the presently reviewed material. The existing audio is distant, obstructed, and incomplete, which limits the force of NIST’s negative acoustic conclusion; it does not reverse it. | **Qualified negative evidence — C against conventional high-explosive demolition.** | Native, continuous audio with microphone/camera metadata; propagation-corrected synchronized analysis; method-specific physical evidence with custody. |
| The investigation can reconstruct WTC 7 without identifiable recovered WTC 7 steel. | NIST WTC 7 FAQ, questions 21–22. | NIST acknowledges that WTC 7 steel could not later be clearly identified. This prevents direct examination of the critical members for heat deformation, overload fracture, cutting, or explosive effects. | **Evidence limitation — B.** It weakens forensic discrimination across mechanisms; it is not evidence of a concealed cause. | Debris-removal and custody records; any contemporaneous tagged photographs, manifests, laboratory records, or recoverable samples. |

## Observations that should not be counted as strain

- “Perfectly into its own footprint”: NIST’s own video analysis records lateral displacement, rotation, and later breakup; this is not a NIST claim to refute.
- “All columns failed simultaneously”: NIST proposed a staged sequence. Façade coherence alone cannot replace its stated internal timeline with a straw version.
- “Steel had to melt”: NIST’s stated mechanism centers on thermal expansion, connection/floor failure, and instability, not melting steel.
- “NIST never considered explosives”: NIST did address blast and thermite claims. The audit question is adequacy and evidence quality, not whether a response exists.
- Premature news reports or generic collapse warnings: these may warrant separate source-chain preservation, but they do not test NIST’s structural mechanism without a connection to a specific model prediction.

## 2026-09-11 LS-DYNA input check

The September 11 keyword decks and the June APDL/thermal/letter sweep instantiate two strain rows without converting them into fraud or a competing cause. IDs: [DISC-001](sherlock-wtc7-investigation/released-file-discrepancy-index/discrepancy-index.csv)–[DISC-028](sherlock-wtc7-investigation/released-file-discrepancy-index/index.md). Case/investigation split: [discrepancy implications](sherlock-wtc7-investigation/lsdyna-supplement-content-audit/discrepancy-implications.md).

- **Handoff sensitivity (row 3):** the live global deck has no residual-stress import. The unused damage hook is commented `*DELETE_ELEMENT_SHELL/BEAM` of set 2. The 4.0-hour companion lists 1,543 shells and 361 beams, including six labeled penthouse-decoupling beams. Instantaneous deletion is now a countable input, not only report prose.
- **4.0 / 3.5-hour threshold (row 2):** a 4.0-hour list is now local; the 3.5-hour control is not. The master comments a **4.1-hour** filename that was not produced. The threshold is more specific and still one-sided.
- **Connection-input gap (row 6):** `no-conn-matl` coexists with bolt/seat part names and a “Connection Shell/Beam” deletion list. Geometry is more inspectable; specialized connection-failure materials remain the withheld residue, if any.
- **Fire-history substitutions (synthesis, not a new strain row):** the Case B 4:00 p.m. nodal field is now inspectable. Floors 11/13 exist in the June zip as Core/SLAB-only trees, and Case B adds a live `SLNo` class. That does not, by itself, quantify the Floor 11/13 substitutions or contradict column-temperature prose.

These cards do not supply results, a 3.5-hour pair, or out-of-sample video validation. They do not raise the “explosives” or “steel melted” straw items below.

## Current conclusion

The strongest NIST-facing issues are **testability**, **model-transfer sensitivity**, **the 3.5/4.0-hour threshold**, and **post-onset model/video divergence**. None presently establishes a contradictory physical mechanism. The public record supports a more limited conclusion than either slogan: NIST has a physically developed, case-specific progressive-fire account, but the released materials do not yet permit an independent analyst to determine how robust its precise causal chain is.

## Released workflow material, withheld models, and the public animation

The released record distinguishes explanatory presentations and selected thermal material from the executable modeling record.  The distinction matters both for technical review and for a precise FOIA description.

| Record status | Material | What it can show | What it cannot establish alone |
|---|---|---|---|
| Released | `WTC 7 Modeling Issues_050609.pptx` | The presentation describes criteria and workflow used in the analyses, including component softening/removal, scripted updates, and restarted analyses. | It does not supply a reproducible baseline model, the complete decision history, or the output histories needed to test sensitivity. |
| Released | `ANSYS Thermal Data.zip` and associated APDL files listed in the interim-production inventory | Some thermal-analysis material and files that may illuminate part of the workflow. | The inventory does not show a complete runnable collapse model, its connection/failure definitions, all scripts, the custom executable, or the LS-DYNA global-collapse decks and results. |
| Withheld as described by NIST | Full ANSYS 16-story inputs and results, break-element source code, ANSYS scripts, custom executable, supporting calculations, and all LS-DYNA 47-story inputs and results | The record categories necessary to identify the actual baseline, transfer, calculation, and output record. | Their titles alone do not show that every file is exempt or that no non-exempt portion is segregable. |

NIST's published physics-based visualization can be compared with video as a visual claim, but a rendering is not itself a substitute for the underlying input decks, result states, frame/timestamp mapping, and camera configuration. A frame-level comparison therefore can identify a claimed correspondence or divergence; it cannot determine whether that difference arose in the model state, an output selection, camera choice, or rendering step without the supporting record.

The references in the released deck to softening or removing components, manual intervention, and restarting an analysis describe numerical modeling choices. They should not be misdescribed as direct observations that physical members simply vanished. The reviewable questions are when the choices were applied, under what stated criterion, whether they were pre-specified, and how outcome-sensitive they were.

### Minimum preservation and inspection fields

Before treating the visualization as technical evidence, preserve the original public asset and source page, retrieval date, file hash, displayed version/date, and any available camera/viewpoint and timing information. For each run or output described in a future index or declaration, seek enough description to distinguish: model family and stage; input, result, source-code, spreadsheet, or render status; filename/type and version/date; scenario/run identifier; connection or failure detail; source dataset for a visualization; and the agency's exemption and segregability rationale.

## Case-use boundary

For the FOIA case, this audit is relevant only as an explanation of why categories such as inputs, scripts, handoff files, result histories, sensitivity runs, and validation materials are meaningful and potentially segregable. It does not support pleading that NIST’s conclusion is false, that any alternative is true, or that a conspiracy occurred. Keep any filed argument on exemption fit, particularity, and segregability.

## Linked research

- [Video/method comparison](wtc7-video-comparison/wtc7-video-demolition-comparison.md)
- [Audio audit](wtc7-video-comparison/27-angles-audio-audit.md)
- [Physics-guided audit blueprint](collapse-reconstruction-workbench/SYSTEM-BLUEPRINT.md)
