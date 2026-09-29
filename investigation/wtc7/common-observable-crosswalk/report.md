# NIST and UAF: what can actually be compared?

2026-09-20. Research only. This completes the five-observable source crosswalk
specified after the [post-Luna reassessment](../luna-reevaluation-2026-09-19/follow-through-2026-09-20.md),
not an executed model comparison or the investigation charter.

## Result

The published comparisons have testable content, but they do not yet supply a
common, independently reproduced five-feature test. NIST's damaged-building
case has an explicit west-penthouse timing discrepancy. UAF reports a close
terminal-motion match, but prescribes core/exterior failure timing, leaves the
acceleration function's exact input/output role unresolved here, and admits
not reproducing the roof kink. Neither study's alignment choices, selected
views or favorable self-appraisal can count as independent validation.

This strengthens a specific criticism of claims that either model already
reproduces the entire collapse. It does **not** establish that every NIST
downstream failure was imposed, that every UAF motion was imposed, that fire
was impossible, or that deliberate intervention was demonstrated. No strict
causal ordering or numerical probability is newly justified; that is not an
assertion of equal odds.

## Sources, independence and terminology

Root read twenty complete, previously rendered pages; separate readers read
the ten NIST and ten UAF pages. All three saved notes before exchanging
findings. This is prior-informed independent interpretation of shared sources,
not independent historical evidence, blinded selection or engineering approval.
No video was newly decoded, track measured, model run, time shift fitted or
tolerance selected. See [protocol](PROTOCOL.md), [root notes](root-notes.md),
[NIST notes](nist-notes.md), [UAF notes](uaf-notes.md) and
[verification/review record](validation.md).

Source keys below use **printed pages**, with physical PDF pages in parentheses:

- **N1:** NCSTAR 1A, pp. 43–44 (85–86), Table 3-1 and §§3.5–3.6.
- **N2:** NCSTAR 1-9A, pp. 96–97 (147–148), Figures 4-41–4-43.
- **N3:** NCSTAR 1-9, pp. 275–280 (319–324), Figures 5-201–5-206.
- **U:** Hulsey, Quan and Xiao, March 2020 final report, pp. 92–95 and
  105–110 (105–108 and 118–123), §§4.1–4.3 and 4.6–4.7, Figures 4.1 and 4.16–4.21.

Source/derivative hashes are recorded in the notes and validation. A
**reported observation** is an author's observation, not our new measurement.
A **computed response** is conditional on its inputs, not automatically an
unfitted prediction. A **prescribed failure** does not identify its physical
cause. An **alignment event** supplies a clock origin, not a predictive win.

## The fixed five-observable crosswalk

| Observable | NIST result and role | UAF result and role | Present comparability |
|---|---|---|---|
| **1. East-penthouse onset** | N1 Table 3-1 sets observed and both Case B simulation onsets to zero **by definition**. Hidden C79 buckling is separately computed at −1.3 s with debris or −1.4 s without; no observed value is given. Visible below-roof passage is another event, observed at 2.0 s. | U p. 92 reports onset about 6.9 s before north-roof descent, drawing on video review and NIST/FEMA. U pp. 94–95 separates the penthouse analyses and explicitly labels its column-removal height tests linear static. Those tests do not predict an elapsed onset time. | A shared visible event can anchor future alignment, but matching zero is not evidence for an initiating cause. The UAF target is not independently reproduced here or established as unused validation data. Hidden failure, first visible movement and roofline disappearance remain distinct. |
| **2. West-penthouse passage below a roofline** | N1: observed 9.3 s after east-penthouse onset; damaged case 6.9/7.3 s; undamaged case 10.6/10.9 s. The two modeled values use different viewpoints. N3 warns that near-camera parapet occlusion occurs before complete sinking through the roof. | U p. 92 reports west-penthouse/screenwall collapse **beginning** 0.5–1 s before north-roof descent. U pp. 95/105 prescribe all-core loss followed 1.3 s later by all-exterior loss. The selected pages give no separate computed roofline-passage time. | NIST's published discrepancy is real at the level of its table, subject to unresolved exact view/threshold correspondence. UAF's onset interval cannot be substituted for that passage endpoint, nor can its hidden 1.3 s removal delay. No numerical NIST-versus-UAF passage residual is available. |
| **3. North-façade onset and trajectory** | N1's feature is the **eastern section** of the north roofline: observed 6.9 s, damaged 6.3 s, undamaged 9.8 s after penthouse onset. N3 reports visible upper façade moving as a unit by 9.0 s. The selected N1 page introduces, but does not supply, a complete velocity/acceleration calculation. | U pp. 106–108/Figs. 4.18–4.20 reports close agreement of simulated **northwest roof-corner** velocity/acceleration with Chandler, including about 2.5 s of free fall. Failure sequence is prescribed; the resistance/acceleration function's derivation and calibration remain unresolved. Two removal-height bands reportedly give the same corner history. | Eastern onset and northwest velocity are not the same observable. A plot overlay is positive reported agreement, not our reproduced residual or a unique inverse solution. Need a common physical feature, projection and clock; neither visible skin nor one corner is the building's center of mass or all hidden supports. |
| **4. Lateral deformation** | N3 describes view-dependent lateral/rotational motion and derives NE roof-corner displacement of 11 ± 3 m, primarily north, at 10.3 s. N2's early model X/Y contours at 1.1(17.1) s and inward east-wall motion concern another stage/component. N1 qualifies reliability after global breakup/kink. | U pp. 92–93 criticizes NIST's exterior distortion; p. 105/Fig. 4.16 reports southeast tipping for a hypothetical C76–81-removal case. Displacements are expressly amplified. The later core/exterior case supplies no calibrated lateral trace in this selection. | Direction and morphology are genuine possible tests, but early contours, amplified tilt and late corner displacement are not one residual. “Straight down” cannot mean zero lateral motion of every feature or final debris containment. NIST's metric estimate remains unreproduced; missing calibration does not erase qualitative contrary observations. |
| **5. North-roof kink appearance** | N3 p. 276 describes an emerging kink near perimeter C47 in the 9.0 s view. N1 p. 44 describes a kink near the core's C76, visible at 9.3 s, and says simulations form it without supplying case-specific timing/shape error here. | U p. 95 expressly reports inability to simulate the kink and attributes this to time-dependent buckling/numerical limitations. No quantitative kink onset or shape trace is supplied. | This is an unreplicated UAF target and a claimed NIST qualitative success, not a complete timed NIST validation. Column namespaces and “emerging” versus “visible” thresholds must be resolved; the 9.0/9.3 labels alone do not establish an internal contradiction. |

### Preserve the discrepancy without manufacturing another

Table 3-1's west-penthouse numbers give damaged-case differences of **−2.4 and
−2.0 s**, and undamaged-case differences of **+1.3 and +1.6 s**, relative to
the reported 9.3 s observation. Its eastern north-roof onset differences are
**−0.6 and +2.9 s**. These are exact subtractions of attributed rounded values,
not measurement-error estimates, confidence intervals or a new rejection test.
Two cases bracketing an observation are not one accurate prediction, and they
have different buckling patterns (N1 p. 44).

Conversely, N3 p. 275 says the last relevant Camera 3 section **was seen** at
8.0 ± 0.1 s; the 8.1 ± 0.1 s comparison shows the west penthouse no longer
visible there while Camera 2 still shows it. That is not an exact measured
disappearance at 8.0 s, nor a contradiction of a later whole-component
roofline crossing. A setback structure vanishing behind a foreground parapet
and a structure sinking through its own roof are different events.

### Preserve the difference between model purposes

NIST describes computed load redistribution and subsequent buckling given
its applied damage/thermal conditions. These pages do not show that each
downstream column failure was prescribed. UAF's best-match scenario explicitly
prescribes broad core/exterior losses separated by 1.3 s. Its reported
acceleration function needs native inspection before determining which parts
of the plotted trajectory are emergent, parameterized or fitted. It is
incorrect either to credit the entire trace as an independent prediction or
to dismiss the entire trace as directly imposed based on these pages alone.

UAF's low-column-failure/tilt and NIST exterior-distortion objections remain
concrete challenges. But the linear-static height-band tests do not by
themselves reproduce dynamic loss, impact and propagation. The
[earlier UAF method audit](../uaf-final-method-audit/report.md) separately pins
the report's P-delta exclusion within stated result scope; it does not verify
every later native case's settings or quantify the omitted effect.

## What could falsify the specified cases?

The comparison is not immune to testing merely because some inputs are missing.
Each test below requires uncertainty from actual footage/model precision—not
a generous tolerance chosen after seeing disagreement.

| Fixed family | A discriminating outcome | Indispensable prerequisites |
|---|---|---|
| East onset | After one fixed visible-onset alignment, an incompatible relative event sequence or penthouse trajectory rejects that implementation's sequence claim. | Named penthouse feature; first-motion threshold; camera/frame identity; bounded frame timing; authenticated native state/history. Do not use static output as a dynamic clock. |
| West passage | The fixed case's projected last-visible/first-below interval fails to overlap the defensibly bounded observed interval. | Same component, moving roof/parapet reference, view and visibility rule; specify first versus final passage within a fixed window, including possible reappearance; exact native-to-observation time join. Recover these before judging the published 9.3 s endpoint quantitatively. |
| North trajectory | A fixed, identically tracked corner/roof segment systematically disagrees in onset or displacement/velocity history beyond justified uncertainty. | Physical point IDs; camera projection and scale; recording clock; raw tracking and derivative method; native output; provenance of the acceleration function and any calibration. No fresh shift fitted for each feature. |
| Lateral motion | The same feature at the same stage moves in an incompatible projected direction, shape or amplitude. | Native physical scale (remove display amplification), orientation, time and coordinate output; registered views and uncertainty. A directional contradiction may be testable before a precise metre estimate. |
| Kink | The fixed case cannot form the observed segment's bend, or does so in an incompatible location/sequence/time. | Defined roof segment and shape criterion; camera/occlusion limits; case-specific shape history. A post-hoc imposed bend or retuning is not an unused-data prediction. |

These tests can reject a specified case without excluding every fire pathway
or every support-removal pattern. Conversely, rejecting one case does not
make an unconstrained alternative correct. UAF's reported two-height-band
equivalence already warns that the selected terminal corner history alone
cannot uniquely locate the loss, even before asking what caused it.

## Clock and evidence dependencies that must remain explicit

NIST Table 3-1 uses east-penthouse-zero. N2 shows pairs such as 1.1(17.1) s and
5.5(21.5) s and a calculation-reference axis. A 16 s arithmetic offset is
visible, but its definition/native-case linkage is not supplied on these
pages. UAF's Figure 4.17 screenshot has time 1.7 and a model name containing
`Penthouse49`; Figure 4.16's time 5.4 uses a name containing `Penthouse46`.
Both display `ACASE2`; this is not proof of identical cases. Figure 4.20's
plotted clock is not authenticated here to either screenshot or NIST zero.

No held-out validation sample is established in this selection. UAF identifies
video and NIST/FEMA review as sources for its targets and explicitly compares
with Chandler; exact calibration use is unresolved. NIST's observations and
model evaluation concern the same historical record. The five rows are not
five independent experiments. Positive source agreement and input reuse can
coexist; neither should be concealed by a one-word “independent” label.

The [Faraday draft alignment](draft-alignment.md) finds existing vocabulary
adequate. Generic power/sample-size placeholders are not prerequisites for
this documentary comparison. Future quantitative testing needs applicable
contracts, not mechanically completed statistical fields. Nothing was
accepted, frozen or executed in either engine. Existing Sherlock feedback
already covers event identity, shared evidence, input/output roles and case
linkage; no duplicate issue or new transmission is warranted here.

## Next independent task

This source unit is closed; do not reread the same twenty pages as another
model-validation result. The smallest consequential next task is a **bounded,
read-only native-case locator for UAF's Figures 4.17–4.20**: determine whether
already-held manifests/native text can identify the `Penthouse49`/`ACASE2`
case, the two removal-height variants and the acceleration/resistance function.
Identify both its implementation role (such as load input, prescribed
kinematics or computed response) and, separately, its derivation/calibration
history, including any use of the comparison trace. These are not mutually
exclusive categories: an input can be fitted and a computed response can
depend on calibrated inputs. Leave either axis unresolved where evidence is
missing. Local availability of the necessary native records is not yet
verified; non-location would not be evidence against UAF's result.

Start with existing source inventories and the UAF method audit; declare the
selected local package/path set before inspecting members. A filename match
alone is not authentication. Success requires an exact file/version and
definition-to-result link, or a precise missing-file/export dependency with
the coverage stated. No solver, executable/macro, new download, bypass,
retiming or accepted-engine mutation. Stop if a proprietary native format
requires an unavailable safe read-only export; identify that export rather
than inventing its contents. This directly limits how much weight the claimed
motion match deserves. It does not replace the unresolved camera/human/expert
gates needed for a physical comparison.

Recommended driver: full-reasoning Codex for source-to-case interpretation,
with a separate read-only checker for any mechanical inventory. The research
worktree remains on `research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`, with intentional uncommitted WIP.
This handoff does not authorize changes outside the research worktree.
