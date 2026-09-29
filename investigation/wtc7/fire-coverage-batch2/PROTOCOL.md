# Fire-observation coverage batch 2: separate observation axes

2026-09-15. Research-only continuation of WP1 under the unchanged investigation
charter. Declared after the v2 calibration result and before this batch's new
structured observations. Prior source screening is known; this is not a
retrospective claim of preregistration or fully blind physical validation.

## Scope and source boundary

Review every remaining photographic asset in the existing 28-asset extraction,
not a result-selected subset. There are 25 photographic assets, 12 already
paired in batch 1, and three geometry graphics. The independent inventory must
confirm exact membership before summary; a mismatch stops counting and is
retained, not silently reconciled by changing this sample.

Read-only source directory:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/`.
The `assets/run-01/reviewed-provenance-key.json` SHA-256 is
`c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3`.
It maps report-native JPEGs, page placements and prior figure associations.
The prior main image-level record SHA-256 is
`d7673cc50ebca454ea30a0d2c45e44041e9d06de9f586e32dd27a65818f535ce`;
the separate prior reviewer record SHA-256 is
`03c671cfb383e939509e0008101a81e4954141c8c8f680596bbecde573f128f0`.
All remain unchanged. Source report NCSTAR 1-9 is pinned by the extraction key,
not treated as independent authentication of its assertions.

Declared new image IDs, in observation order:

1. A-873f87e7149b
2. A-e1b0c06ad11d
3. A-9e7b4935c8aa
4. A-0b722775db93
5. A-fa6f410444bb
6. A-ffe3726a0312
7. A-0e60b82a1a4c
8. A-6902e91e39ee
9. A-671f312eade8
10. A-69d899e75343
11. A-8bc36f05fe38
12. A-7b61385d1373
13. A-f1e2fa01e344

Image files are `assets/run-01/images/<asset_id>.jpg`. Use original dimensions
and bytes from the pinned key; inspect every complete native image, not a
thumbnail/contact sheet alone. No new crop, resampling, enhancement, erased
labels, generated/interpolated pixels or automated flame classifier. Bounding
rectangles are approximate locators on the original raster, not segmentations,
surveyed apertures, areas burning or counts of windows.

This completes only the declared extraction's photographic observation coverage
when checked. It does not complete the full report, all publicly available
imagery, the day's chronology, or WP1. Separate source-family and clock limits
prevent treating each figure as an independent fire event.

## Independence and staged source review

Root knows earlier research and sees the inventory's figure/page associations.
A fresh context-limited AI reviewer receives this protocol, anonymous JPEG IDs,
hashes/dimensions and native images, not captions, other labels or model inputs.
Visible numerals/credits and general knowledge compromise blindness. Neither
reviewer is a qualified human forensic expert. Do not claim such expertise.

A separate source reviewer reads complete existing page renders and surrounding
source text to record report-attributed facade/floor/time/credit/processing and
limitations. That reviewer does not supply visual labels to the two annotators.
Freeze both image-observation records before opening source attributions or
cross-reviewing each other. Preserve exact disagreements; no averaging or
relabeling to obtain consensus. Then visually check relevant complete source
pages before relating labels to the model-input questions.

## Versioned observation schema

The v2 pilot showed that smoke and no-discernible-flame descriptions can both
be true. This batch therefore separates these axes instead of forcing one
exclusive primary class. Old records are not migrated or overwritten.

Top-level JSON: `reviewer`, `independence` (nonempty string or structured
object), `protocol_sha256`, `provenance_key_sha256`, and `assets` (all 13).
Each asset contains exactly:

- `asset_id`, `image_sha256`, `dimensions` `[width,height]`,
  `complete_native_image_inspected` true.
- `target_rect`: `[x0,y0,x1,y1]` or null. This locates the candidate target
  frontage in the image, not independently authenticated WTC 7 architecture.
- `target_evaluability`: `partial_detail`, `limited_detail`, or
  `unresolved_target`. Partial means useful localized detail with retained
  occlusions; limited means predominantly obscured, small, dark or blurred;
  unresolved means even candidate localization is not secure. These are
  qualitative descriptions, not ordered numerical exposure/detection scores.
- `target_reason`: actual framing/appearance basis and uncertainty. If target
  is unresolved, use null target rectangle. Do not extrapolate hidden edges.
- `luminous_features`: zero or more `{rect, appearance, target_relation,
  reason, alternatives}`. Appearance is `flame_like` or `ambiguous_glow`;
  target relation is `on_candidate_facade` or `uncertain`. Flame-like means
  resolved irregular luminous/tongue-like morphology consistent with flame,
  not verified emitting gas or measured temperature. Saturation, reflection,
  illuminated material and projected depth remain explicit alternatives.
  An empty list means no such feature identified in this review, not no fire.
- `smoke`: `{status, regions, reason}`. Status is `visible`, `uncertain`, or
  `not_identified`; regions is a list of rectangles. A visible veil can be
  described while its underlying facade is unevaluable. Its source is never
  assigned merely from overlap or proximity. Visible requires at least one
  locator; uncertain may have none; not_identified has none.
- `nondetection_regions`: zero or more `{rect, reason}` describing only the
  actually visible region in which no flame form was identified. Include the
  opportunity limit in each reason; this is not a calibrated optical detection
  limit. Leave empty where target identity/detail cannot support even that
  bounded description. Never turn opacity or an unseen room into a negative.
- `visibility_limits`: nonempty list of strings describing actual obstruction,
  resolution, exposure, glazing, depth or processing limits.
- `overlay_regions`: list of rectangles for visible source-added labels/credits
  relevant to interpretation. They are not flame observations. This is not an
  exhaustive overlay segmentation or authentication of what the marks assert.

Coordinates are native pixels, origin upper left, rectangles half-open and
within `[0,width]×[0,height]`. Do not imply precision better than a few pixels;
if localization is not defensible, retain absence/uncertainty in the relevant
field rather than inventing a small rectangle. Overlapping bounding boxes are
permitted and do not imply double-countable phenomena. A broad box can contain
unlit or occluded portions: it never means its full area is flame or smoke.

## Rule controls and deterministic verification

Before viewing this batch, each annotator records answers to six disclosed
text scenarios (controls, not visual-detection tests):

1. A veil crosses a dark framed region without identified flame: smoke may be
   visible and a qualified nondetection region may coexist; no interior absence.
2. Target cannot be localized behind foreground: unresolved/null target and an
   empty luminous list do not mean no fire.
3. Smooth orange illumination lacks resolved morphology: ambiguous glow,
   with reflection/material alternatives; no temperature estimate.
4. A bright red printed numeral: overlay, not luminous fire evidence.
5. Two bounding boxes overlap: no area sum or window/fire count follows.
6. Two figures repeat the same camera/view: retain source-family dependency;
   different filenames do not establish independent corroboration or clocks.

Validate every source/record hash, exact sample membership, no duplicate JSON
keys, field structure/enums, finite non-boolean coordinates, positive dimensions,
in-bounds nondegenerate rectangles, substantive reasons and the smoke/target
consistency rules. Check rules with synthetic records before historical summary.
Verify no inputs change during calculation and refuse occupied output paths.
Emit original records and explicit per-asset agreements/differences, not a
confidence-weighted or numerical fire-extent score. Two runs must reproduce
the deterministic products, and an independent check must reproduce material
inventory/comparison results or leave the discrepancy unresolved.

## Allowed comparison and continuation

After labels freeze, map source-attributed facade/floor/time separately and
identify what new visibility coverage is added. Check against prior observation
and source-input tables without treating report prose as a physical premise.
Source processing, ambiguous targets, clocks and reused exposures remain
limitations, not evidence of manipulation. Any actual incompatibility must
specify the same region, time, quantity and observational opportunity.

No interior heating, extinction time, model-error magnitude, structural result,
causal ranking or intent follows from qualitative image labels alone. Do not
discard obscured/negative views or promote apparent agreement with imagery used
to construct the model into independent validation. Report available new
constraints and the precise native-video/input dependency for unresolved tests.
