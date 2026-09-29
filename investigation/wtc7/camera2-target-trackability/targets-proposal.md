# Baseline-only Camera 2 target-point proposal

2026-09-11. Proposed **two** image-outline points, pending root's independent baseline acceptance. No third point is forced, and no evaluation frame has been opened for this selection. This is an exploratory computational AI proposal, not human/specialist review, a clean holdout or material-point authentication.

Read the complete current [charter](../CHARTER.md), [reference-repair report](../camera2-reference-repair/report.md), and new [trackability protocol](PROTOCOL.md). Source-of-truth and evidence-audit controls keep these image-appearance definitions separate from source evidence, physical interpretation and canonical case facts. Hashes of the documents read are recorded in [targets-proposal.json](targets-proposal.json).

## Baseline and actual coverage

Inspected only the existing [native f6593](../multiview-onset-review/refine01/camera2/f006593.png): Camera 2 / `VID-WTC7-001`, source-copy time `219767/999` seconds, mode L, 640×480, SHA-256 `39bcb70c16ccc468133edf92b3a9dc9ea43edbc5692d82d8adcfc08cc22903a8`. This is an integrity pin, not authentication of the original camera or a physical clock.

Actual selection viewing: **one distinct full native frame and three derivatives of that same frame**—one [exact native crop](baseline-upper-outline-native-crop.png), one [coordinate-labeled nearest-neighbor crop](baseline-upper-outline-coordinate-crop.png), and one [separate proposal-marker crop](baseline-target-markers.png). The exact crop is `[280,115,470,200)` (190×85 native pixels). The coordinate display enlarges it fourfold by nearest-neighbor, adds exterior native-coordinate ticks and explicit analytical labels, and applies no contrast change or inferred detail. The marker derivative adds hollow red/blue crosshairs while leaving the selected pixel blocks uncovered. Every path, transformation and SHA-256 is in the JSON.

The generating command explicitly used Python 3.13.7 with Pillow 12.0.0 and reported those actual versions. Original pixels/files were not changed. These are proposal aids only, not independent evidence or enhanced image resolution. They differ from the larger, fixed evaluation presentation specified in the protocol; no evaluation aid was generated here.

## Proposed image points

Coordinates are zero-based native pixels, x right/y down. Envelopes are subjective rectangles, not statistical confidence intervals or calibrated accuracy.

| ID | Coordinate | Subjective envelope | Exact appearance definition |
|---|---|---|---|
| C2-T1 | (454,156) | ±3 px in x/y | Apparent outer upper corner on the target's image-right side: intersection of the lower of its two visible upper-outline segments with the long exterior side boundary. Localize the center of the blurred dark-to-light corner transition, not its bright halo. |
| C2-T2 | (424,144) | ±3 px in x/y | **Upper** endpoint of the short downward step in the target's upper outline: the higher, long upper-outline segment turns into a short near-vertical descending boundary here. This is not the lower junction of that step or an arbitrary horizontal-edge point. |

The labeled markers fall on the intended respective corner transitions in the baseline crop. T1's upper and side boundary segments are visible. T2's upper step endpoint is separable from the lower junction below it. Both are **silhouette/appearance corners**, not surveyed intersections of authenticated material edges. No cardinal direction, floor, roof-component/penthouse identity, structural member, or support function is assigned.

A precise later corner need not be the same feature. If the upper step disappears, the lower junction or a replacement roof outline must not silently become T2. Similarly a later foreground corner or smoke boundary cannot substitute for T1. Each subsequent row must separately record localization and correspondence; localized coordinates may still have uncertain or changed correspondence. Appearance consistency alone is not proof of persistent material identity.

## Why there is no third proposal

The image-left upper transition is smoke-softened, and I cannot identify a separable corner from its adjacent side boundary confidently from this baseline. I also did not select a uniquely defined target-façade landmark to fill a quota. Therefore **no C2-T3 is proposed**. This is a limitation of this baseline-only selection, not proof that no other feature could ever be usable.

The two proposed points are only 30 native pixels apart horizontally and 12 vertically, both near the image-right upper outline. They do not cover the full target width, façade or depth. Their shared local appearance and limited spread constrain later interpretation: agreement cannot establish whole-building rigidity, symmetry, support-loss ordering or tilt.

## Independence and next gate

Later imagery, the collapse sequence and prior work are already familiar. This pass did not reopen later frames or use new numerical scoring to choose these points. Shared seed knowledge also means that the later baseline re-localization is not independent baseline construction; both analysts must nonetheless visually estimate and record their own baseline coordinate/envelope rather than treating the proposal as error-free.

Root must separately check the native baseline and marker aid and freeze accepted definitions before the 17-frame evaluation is released. Rejected proposals remain preserved. This annotator will not open main's new coordinate file, nor begin the evaluation set, until authorized; coordinate files must remain unseen between analysts until both are saved.

No previous source/result artifact, code, shared protocol, case record or commit was changed. No later-image score, trajectory, velocity, acceleration, gravitational comparison, force or causal inference was made. Agency-production/held-packet contents, bridge, network, external acquisition and canonical promotion remain out of scope.
