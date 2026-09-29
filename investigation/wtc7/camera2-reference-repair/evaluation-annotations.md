# R7 fixed-sample visual annotations

2026-09-11. Completed **five R7 annotations before reviewing new automatic historical outputs**. All five are visually localized at the stated coarse envelopes. This is computational AI review of familiar retrospective images, not human/specialist review or a clean holdout.

## Frozen input and scope

Root released the selected C2-R7 seed at (333,413) after its separate visual review and both baseline gates passed. This annotator checked the released `preflight01/selection.json` SHA-256 `1615cf412019ea9e15d116e20007966890238c3beb68e54abfa5a08666db8fae` and receipt SHA-256 `8fea3c45f64ecf96aefa2c329d0f322a20d03ec42daea80bef9fad49706318b6`. Selection status is `selected_baseline_only_not_validated_track`; old `pending` strings copied inside the candidate metadata preserve its proposal stage and do not replace the completed preflight status.

The baseline proposal, selection, v1 records and other five reference annotations were not edited. Only R7 was localized here, in the already declared native Camera 2 frames 6654, 6751, 6931, 7013 and 7104. The new matching runs may have executed elsewhere in parallel, but no new later-frame scores, candidates, transforms or match overlays were opened for these annotations.

The [machine-readable annotations](evaluation-annotations.json) preserve each original PNG path/hash, raw source PTS, time base and exact rational seconds. These agree with the retained `refine01/camera2/selection.json` entries and actual PNG bytes. Source-copy clocks are not independently authenticated physical camera clocks.

## Actual viewing and localization

Viewed **five full native mode-L 640×480 images and five labeled localization crops**, one of each per evaluation frame. The crop is the same original rectangle `[310,390,355,433)` in each image, enlarged fivefold by nearest-neighbor solely to inspect existing pixels. Axes outside the image label native source coordinates every five pixels. No candidate point or automatic output was drawn on these crops, and no contrast enhancement was applied. Python 3.13.7 and Pillow 12.0.0 were explicitly selected and reported by the generating command. Crop paths, transformations and hashes are in the JSON.

R7 denotes the small bright roughly rectangular patch/cap on the lower central foreground roof edge, immediately left of the taller gridded foreground block. Each frame was examined separately for the recognizable bright patch and its neighboring geometry; coordinates were not obtained from an intensity maximum, thresholded centroid, automatic match or assumed fixed center.

| Frame | Exact source-copy seconds | Visual center (x,y) | Subjective envelope (x,y) | Status |
|---|---|---|---|---|
| 6654 | 665404/2997 | (334,412) | ±3, ±3 px | Localized |
| 6751 | 675100/2997 | (334,412) | ±3, ±3 px | Localized |
| 6931 | 231034/999 | (334,412) | ±3, ±3 px | Localized |
| 7013 | 701303/2997 | (334,412) | ±3, ±3 px | Localized |
| 7104 | 710404/2997 | (334,411) | ±4, ±4 px | Localized |

The first four views retain a recognizable compact bright right-hand patch beside a dimmer horizontal roof-edge strip. Its blurred/rounded edges make any integer center approximate. The final frame still supports appearance identification, but its softer brightness profile and lower-edge merging justify a wider envelope. The nominal one-pixel upward difference in that row is unresolved within the stated envelopes and is not a measured displacement.

The slight nominal difference from baseline (333,413) is likewise within baseline/evaluation localization allowances. Equal rounded coordinates in several rows mean no difference resolved at this visual precision, not zero motion or proof of exact pixel correspondence. The baseline anchor was not moved and no new reference was substituted.

## Identity and inference limits

Appearance identification is narrower than identifying a material point. Exact building/component identity, physical stationarity and depth remain unverified. A rooftop highlight, changing brightness, blur/compression, repeated textures, background inclusion and different-depth overlap can change the apparent center or create a misleading match. The envelopes are subjective rectangles, not statistical intervals, surveyed accuracy or uncertainty propagated through a camera model.

This pass does not revalidate the other five retained references, repair v1 annotations, or measure a target-building trajectory. It cannot establish physical camera motion, calibration, acceleration, support-failure timing or cause. Later comparison to both template sizes must retain these frozen coordinates and distinguish numerical envelope agreement from correct feature/material identity; any post-output disagreement or correction must be additive.

Evidence-audit and source-of-truth controls kept the new annotations separate from accepted scientific claims and earlier records. No raw media decode, new source, agency-production/held-packet contents, bridge, network, code/configuration changes, external transmission, canonical promotion or commit was used. The next step is release of new output paths for the separately scoped comparison; these five annotations are complete and should be preserved unchanged.
