# Camera 2 reference repair: supported image constraint, not physical calibration

2026-09-11. **Bounded result:** replacing our confirmed misplaced reference allows the unchanged six-reference method to admit Camera 2 image maps. The larger templates pass in all 71 selected images; the smaller templates retain substantial reference ambiguity. This corrects a limitation of our earlier configuration, not an anomaly in the collapse. No target trajectory, acceleration or causal ranking is produced.

Research-only under the [charter](../CHARTER.md). The [original diagnostic](../reference-motion/report.md), mistaken annotation and failed fits remain preserved. This exploratory follow-up uses already-seen footage, not a clean holdout. [Protocol](PROTOCOL.md), [validation](validation.md), [independent review](independent-review.md) and complete [summary](summary01.json) control the detailed scope below.

## What changed, and what did not

The original C2-R3 coordinate was associated with the wrong low-texture region. Only that reference was replaced, by C2-R7 at native (333,413): a small bright patch/cap on a lower-central foreground roof edge. The annotator proposed one candidate from baseline f6593. Root separately checked the native image, marker and both template crops before baseline numerical scoring. Both baseline gates passed and the selected configuration was frozen before later-frame scoring. A baseline self-match does not establish subsequent correspondence.

All five other references, their order, both template sides (19 and 27 pixels), fixed ±24-pixel searches, texture/correlation/competitor/tie/boundary gates, all-six admission, translation/proper-similarity/affine models and two-pixel training/leave-one-out screens remain unchanged. The [selection](preflight01/selection.json) and [preflight receipt](preflight01/receipt.json) preserve the exact objects and parent identities. No candidate was silently moved after scoring; no threshold was relaxed or failing reference dropped.

Coverage is the same 71 native-Y Camera 2 selections f6593–f7104, using exact source-copy times from `219767/999` to `710404/2997` seconds. These are selected frames, not every intervening frame. The converted CBS/DV access copy and earlier pixel/PTS maps remain the inputs; their hashes are integrity checks, not independent authentication of original exposure times. No new decode, Camera 4 rerun, interpolation or stabilization was performed.

## Computed results

Each size has 426 reference/frame rows and 71 potential fits per model. “Pass” means the fixed numerical consistency screen, not a probability, surveyed accuracy or physical-model validation.

| Template | Accepted reference rows | All-six admitted images | Translation passes | Similarity passes | Affine passes |
|---|---:|---:|---:|---:|---:|
| 19×19 | 381/426 | 26/71 | 26 | 26 | 25 |
| 27×27 | 426/426 | 71/71 | 71 | 71 | 71 |

All 142 R7 candidates pass and return (333,413). All 45 remaining rejected match rows belong to the unchanged C2-R6 smaller patch: its distant-competitor margin is insufficient. Those failures are distributed through the sampled interval, not one contiguous late segment. Every affected all-six fit remains uncomputed: 135 model-status rows in total. All 291 admitted models and their 1,746 omitted-reference predictions are retained, including the single exact-cutoff failure discussed below.

The larger patches give identical integer positions for five references; R1 varies by up to one vertical pixel. The fitted translation is therefore x=0 and y between −1/6 and 0 pixels. This is a descriptive image-space result, not a calibrated upper bound on camera movement. Subpixel changes, shared errors, reference depth and changing image appearance remain unresolved. Similarity/affine offset parameters cannot be read as pure translations independently of their fitted matrices and coordinate origin.

The template sizes disagree in candidate coordinate or acceptance status for 61 reference/frame pairs: eight R1 pairs and 53 R6 pairs. Sixteen of those pairs pass both sizes despite different integer candidates. Thus accepted correspondence is still scale-sensitive; two overlapping template sizes are not two independent historical witnesses. Larger-patch success does not make the smaller-patch failures disappear.

### The one fit rejection is a numerical boundary effect

At f7021 with 19×19 templates, five matched positions equal their baseline positions and R6 is two pixels left. Omitting R6 leaves five identical source/target pairs, including three noncollinear points. Their unique identity map predicts an R6 error of exactly (−2,0), norm 2, for each model.

The stored maximum leave-one-out errors are 2.0 for translation, 1.9999999999997726 for similarity, and 2.000000000000796 for affine. The unchanged exact `<= 2` gate therefore labels only affine false. Independent arithmetic returns an affine maximum of 1.9999999999998863. The exact identity-fold argument and the other folds' smaller errors identify rounding at the cutoff, not demonstrated physical inconsistency. **The original false flag remains unchanged**, with this additive explanation. A future numerical policy would require a separately versioned declaration; no post-result tolerance change is applied here.

## Reproduction and visual checks

The two historical directories each contain 25 receipt-listed products plus their receipt, all 26 pairs byte-identical. Completion is established by complete receipts and independently checked products; the original launcher response was truncated and its exact shell exit statuses were not recovered. No duplicate run was started to replace that observation gap.

The independent reviewer reproduced all 142 new full correlation grids (340,942 scores) by FFT/integral-image arithmetic, maximum difference about 9.43×10⁻¹⁵, with no match-decision disagreements. All 710 retained-reference rows and complete grids equal v1 exactly. The reviewer checked all 426 model rows, all admitted fits/folds, every source/input pin and all 12 overlay images pixel-for-pixel. Root read the verifier and successfully reran it; the two final verification results differ only in their recorded command/output path. Reproduction checks arithmetic and lineage, not physical landmark identity.

Before opening new automatic outputs, the annotator saved [five fixed R7 observations](evaluation-annotations.md). All [ten size-specific comparisons](comparison-report.md) pass the automatic gates and fall inside the frozen subjective envelopes. Automatic-minus-manual coordinates are (−1,+1) for the first four frames and (−1,+2) for the last, for both sizes. Those differences are retained, not corrected away. All ten run02 rows equal run01. Root read and reran the comparison helper; its output is byte-identical to the annotator's two successful outputs, all under recorded Python 3.13.7. The initial helper's incorrect initial/final-pin equivalence assumption and failed attempt remain documented separately.

Root separately viewed all 12 baseline/evaluation overlays (six distinct native frames, both sizes), as did the annotator. The marker remains associated with the small foreground bright patch; no new description-coordinate contradiction was seen. The red R6 markers at f6654/f6751 in the smaller size correctly show rejection, not disappearance. This post-output view is not an independent coordinate measurement or human review; all prior five-reference observations remain unchanged.

Appearance agreement does not authenticate a particular stationary material point: highlights, blur, compression, repeated textures and depth overlap can move an apparent center or mislead a matcher. The visual sample is coarse and retrospective, and does not certify all intervening frames. Root's baseline review and the annotator's before-output evaluation are separate recorded computational reviews, not specialist approval.

## Consequence for the investigation

The v1 inability to admit Camera 2 maps was materially dependent on our invalid reference selection. With that association repaired, the tested larger-patch references support a near-identity image map over the 71 samples. The earlier failure cannot properly be cited as evidence that Camera 2 is intrinsically unusable or that its scene behaves anomalously. Conversely, a consistent reference map does not validate a target-building trajectory or show zero physical camera motion.

The next local motion task is a separately declared, multi-point **target-feature/outline trackability study** on native coordinates: distinguish persistent material features from changing silhouettes and occlusion, preserve source PTS, and quantify selection/scale/reference-model sensitivity before any physical acceleration fit. Do not endlessly replace references until every patch passes. Human spot-checks, scale/projection calibration, origin-clock limits and qualified physical review remain gates before consequential kinematic or force claims.

If inspection is approved, the [new supplementary production](../supplementary-production-2026-09-11.md) takes priority for the already declared model-input/dependency crosswalk. It was not inspected in this unit and does not clear the separately held packet. No claim about model completeness or continued blanket unavailability follows from file names alone.

These results do not change the fire-versus-deliberate-removal ranking. They test measurement prerequisites, not the cause of support loss. The overall goal and work-package exits remain incomplete. No bridge, feedback transmission, case import, canonical promotion, filing, commit or push occurred. Genuine workflow lessons remain deduplicated locally under the existing feedback/privacy gates.
