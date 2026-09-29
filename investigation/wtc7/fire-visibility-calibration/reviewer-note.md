# Fresh AI reviewer calibration note

Research only. All 13 selected units were annotated without reading prior appearance annotations, prior appearance reports or count outcomes, or the root reviewer's new labels. The annotations and controls are frozen before cross-review. This is a context-limited AI calibration, not human forensic expertise, a fully blind trial, or independent camera evidence.

## Inspection and order

I read the main repository `AGENTS.md`, `WORKFLOW.md`, and `START-HERE.md`; the personal evidence-falsification-auditor `SKILL.md` and its claim-ledger template; and this calibration's full `PROTOCOL.md`. I verified that the worktree is on `research/sherlock-wtc7-investigation`. I saw directory/status filenames but did not open the other investigations or appearance products.

I saved and hashed the ten text semantic controls before reading geometry or inspecting images. Their expected outcomes were disclosed by the protocol, so they test rule comprehension only. I then read the complete `geometry-main-v1.json`, including its prior identity suggestions and unselected units, but annotated only the declared 13-unit sample. I inspected the following complete JPEGs with `view_image` at original resolution; no new crop, annotation overlay, enhancement or generated historical frame was made:

- `A-e43e4088a4a2.jpg`, 720 by 478 pixels; SHA-256 `6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469`.
- `A-ad43dfe2413b.jpg`, 705 by 480 pixels; SHA-256 `8a314243feac6b213548048597e20f5e981156a77a291938b93e3b76490958b3`.

The protocol pin is `ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5`; the geometry pin is `d7c593a6d7ccad9f1f403bf0ee8a2bfe5afd6d0c6e5dd446c3602e6a5e590a13`. Native dimensions were independently read using `sips`. All pins and dimensions matched. Native source files were not changed.

The parent provided one label-free method clarification while validation was underway: uncertain obstruction severity should produce null opportunity when no coarse estimate is defensible, and should not by itself make an established identity unresolved. The drafted records already followed those separate axes, and no label was changed in response. R01C03's identity uncertainty concerns unrecoverable lateral candidate boundaries; its null opportunity concerns the absence of a defensible detail interval. Other uncertain material/glazing cases retain a single candidate when exterior framing is visible.

## Epistemic audit

The image observations are relative outlines, repeated framing, dark or luminous surfaces, and cloud-like texture. Candidate identity, opportunity intervals and appearance categories are image-based interpretations of report-embedded derivatives. Opportunity is an ordinal coarse estimate of usable displayed detail in each fixed polygon, not a measured fraction, probability, interior view, or fraction burning.

The best-supported geometric conclusions are that the broad strips span several repeated framed regions and that the right-edge R02C10 is only four native pixels wide. These conclusions support exclusions from this selected candidate-appearance subset, not architectural counts. The more interpretation-sensitive claims are distinctions between irregular flame-like morphology and smooth glow, and between opaque obstruction, dark glazing and unlit depth. Reflection, illuminated or hanging material, low exposure and concealed detail remain plausible alternatives where stated.

No discernible flame describes only the visible portion. Morphology consistent with flame does not establish emitting gas. The source images do not authenticate acquisition time, clock alignment, window IDs, opacity, interior visibility, temperature, duration, model inputs, structural effects or cause. A better authenticated view that resolves framing/material or reproduces alleged morphology would weaken or strengthen these judgments; an additional AI reading of the same derivative is not that evidence.

The explicit decisive-exclusion record is R02C10: the four-pixel edge sliver prevents a useful unit-level appearance assessment. Other cautions were not automatically converted to vetoes. In particular, uncertain opaque-material coverage remains an uncertainty, and localized saturated areas can coexist with a useful localized description. Geometric `not_single` and `clipped` exclusions operate independently of these caution lists.

## Independent finite arithmetic

A standalone local calculation checked exact sample membership, duplicate/missing IDs, exact row fields, enum and interval validity, rejection of booleans/non-finite interval values, reasons, pins and the ten semantic-control outcomes. It recomputed these threshold lists directly from this reviewer's JSON and the pinned geometry, independently of any parent bookkeeping implementation. The lists retain all appearance labels; no percentages or building/floor fractions are calculated.

For `A-e43e4088a4a2`, at every threshold 0.25, 0.5 and 0.75, eligible and unknown lists are empty and excluded is `U02, U04, U05, U06` (0 eligible, 0 unknown, 4 excluded). U02/U04/U06 are `not_single`; U05 is `clipped`. At 0.5, U05 and U06 also have opportunity intervals touching the threshold and retain that unresolved reason under exclusion precedence. At 0.75, U02 and U04 retain that threshold-touching uncertainty, while U05 and U06 additionally have opportunity upper bounds below the threshold.

For `A-ad43dfe2413b`:

| Threshold | Eligible | Unknown | Excluded | Counts eligible / unknown / excluded |
|---|---|---|---|---|
| 0.25 | R01C06, R01C08, R01C10, R01C11, R01C12, R02C05 | R01C03 | R02C10, U02 | 6 / 1 / 2 |
| 0.5 | R01C06, R01C08, R01C11 | R01C03, R01C10, R01C12, R02C05 | R02C10, U02 | 3 / 4 / 2 |
| 0.75 | None | R01C03, R01C06, R01C08, R01C11 | R01C10, R01C12, R02C05, R02C10, U02 | 0 / 4 / 5 |

R01C03 retains both unresolved identity and null opportunity at every threshold. The other unknown results arise from opportunity intervals that reach the threshold at their upper endpoints. R01C10/R01C12/R02C05 are excluded at 0.75 because their upper bounds are below it. R02C10 is excluded at all thresholds for clipped identity, native span below eight pixels, and the explicit reasoned exclusion; its null opportunity and null in-frame fraction remain recorded as unresolved reasons. U02 is excluded for `not_single` at all thresholds, and at 0.75 also retains a threshold-touching opportunity uncertainty. Eligible rows pass on opportunity lower bound with established nominal identity and no decisive exclusion. There is no preliminary-eligible/non-evaluable conflict in these records; the text control explicitly exercises that conflict rule.

## Remaining rubric ambiguities

The protocol leaves a judgment boundary between useful localized appearance and an obstruction/saturation severe enough to prevent unit-level assessment even though a localized positive survives. It supplies no measured opacity or fixed usable-detail proportion for that boundary. I have stated the actual effect and used uncertainty where the image cannot resolve it, rather than inventing a threshold.

Dark surface detail can be sufficient for a displayed-surface description while providing no view through that surface. Opportunity estimates therefore remain dependent on how much edge/texture detail a reviewer finds interpretable at native scale. This calibration may expose that disagreement; it cannot resolve it by arithmetic or by averaging labels. Any persistent ambiguity should be clarified in a versioned protocol before remaining units are reannotated.

## Frozen deliverables

- `reviewer-controls.json`: SHA-256 `13f548120fac17234e4a3e69aaf07fa2dcdafec76dda84c26f8ed6eb1a9136f8`.
- `reviewer.json`: SHA-256 `ea8547d0eed74751074637dcb4f3b8d9c7108723b4f3230ff98e787eefa3dc2b`.

This note's hash is supplied with the handoff after writing it. Cross-review should preserve the frozen files and report separate identity, opportunity, decisive-exclusion and appearance differences. No consensus adjudication or eligibility adjustment is implied.
