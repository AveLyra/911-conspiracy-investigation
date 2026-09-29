# Camera 2 replacement-reference selection: baseline only

2026-09-11. One candidate is proposed for the separately declared [repair protocol](PROTOCOL.md): **C2-R7 at (333,413)**. Root visual acceptance and numerical baseline preflight are still pending. This is a working research annotation, not a verified stationary material point or an accepted camera registration. The first diagnostic and its erroneous C2-R3 annotation remain frozen.

## Authority and selection boundary

Read `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, the complete [investigation charter](../CHARTER.md), the [v1 protocol](../reference-motion/PROTOCOL.md), current [v1 report](../reference-motion/report.md), and the new repair protocol. The source-of-truth and evidence-audit skills require an additive, explicitly exploratory proposal and preserved contrary history. No research result is promoted into the canonical case record.

The known reason for this repair is the confirmed description-to-coordinate error: v1's (288,400) was not on its described cap. Earlier visual familiarity with the event frames and review of v1 results cannot be undone; this is not a clean holdout, independent human review or retroactive preregistration. **This selection revisited only f6593 and derivatives of f6593.** No later frame or new replacement-reference matching output was viewed to choose the candidate, and no later-frame performance claim informs the choice.

## Preserved baseline and actual visual coverage

Source: [Camera 2 f6593 native Y-plane PNG](../multiview-onset-review/refine01/camera2/f006593.png), `VID-WTC7-001`, source-copy time `219767/999` seconds, mode L, 640×480. SHA-256: `39bcb70c16ccc468133edf92b3a9dc9ea43edbc5692d82d8adcfc08cc22903a8`. This pins the existing derivative's bytes; it does not authenticate the original camera or assign a physical clock.

Actual selection coverage: **one distinct full native frame, one exact native-resolution crop, one labeled coordinate-grid derivative and one labeled nearest-neighbor anchor crop**. No Camera 4 or later Camera 2 image was viewed for this selection. Each derivative and its hash are listed in [candidate-seeds.json](candidate-seeds.json).

- [Native central crop](baseline-central-native-crop.png): exact source rectangle `[240,270,410,440)`, 170×170 mode-L pixels, no resizing or contrast change.
- [Labeled coordinate grid](baseline-central-grid.png): that crop, RGB only for red grid/labels and an external explanatory area. Grid lines every ten native pixels; labels use original coordinates.
- [Labeled R7 anchor check](baseline-r7-anchor-check.png): source rectangle `[310,390,355,433)`, enlarged fivefold with nearest-neighbor for inspection. Red brackets surround but do not cover the proposed source pixel (333,413). This adds no detail and is not evidence independent of the baseline.

These aids were generated with the explicitly selected Python 3.13.7 interpreter and Pillow 12.0.0, as reported by the actual generating command. No source PNG was changed. The enlarged crop is solely a coordinate-reading aid, not a resolution enhancement or new historical observation.

## Ordered candidate — one only

| ID / order | Integer center | Subjective baseline envelope | Appearance and coordinate association |
|---|---|---|---|
| C2-R7 / 1 | (333,413) | ±3 pixels in x and y | Center of the small bright, roughly rectangular roof-edge patch/cap on the lower central foreground building, immediately left of the taller gridded foreground block. The marked source pixel falls within the visible bright patch in the baseline and labeled anchor crop. |

Both requested square templates fit the stored image. Their inclusive bounds are 19×19: x324–342/y404–422; 27×27: x320–346/y400–426. This is only an in-bounds check, not a texture, uniqueness or tracking test. The named anchor is the visible patch center, not an asserted surveyed corner or hidden structural member. Unlike the old R3 center, its marker is associated with the described bright patch rather than the dark area well to its left.

The region appears to belong to a neighboring foreground building, not the WTC7 target, smoke, a person or a vehicle. Exact building/component identity, material-point continuity and depth are unverified. A highlight or changing brightness, blur/compression, similar rooftop texture, background inclusion and different-depth overlap remain alternatives. The visual envelope is a subjective localization allowance, not a probability interval or a physical measurement-error bound. Physical stationarity is an assumption requiring later checks; the static baseline cannot establish it.

No R8 or R9 is proposed. This bounded choice contains one visually defined candidate rather than an open-ended list. Root must independently inspect the native baseline, center marker and both template-size crops, then apply the unchanged v1 baseline gates to both sizes. If C2-R7 fails either the visual association review or either size's numerical baseline gates, retain the failure and stop this selection; do not silently move the point or add further candidates after seeing scores. A passing self-match on the construction image would still not establish later correspondence.

## Claim limits and next gate

The image-appearance claim is narrow: (333,413) lies on the named visible bright patch in this retained baseline. A contrary native-pixel/marker inspection would reject that proposal. The claims that this is a fixed material point, remains visible in later frames, or permits a valid camera map are **not established** by this selection. No later-frame coordinate, acceleration, cause, corrected image or target trajectory is supplied.

Root owns the separate visual acceptance/preflight record and may freeze the new six-reference configuration only after the declared checks. The remaining five reference seeds, model choices, thresholds and all-six admission rule stay unchanged. Until root releases the frozen seed, this annotator will not annotate later frames or inspect replacement-reference results. No source/code/configuration change, production or held-packet inspection, bridge, network, outreach, canonical promotion or commit occurred.
