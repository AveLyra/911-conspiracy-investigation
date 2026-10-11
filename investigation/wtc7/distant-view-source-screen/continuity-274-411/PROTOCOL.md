# DistantView outer corner correspondence feasibility

October 8, 2026. Research only. Previous goal turn made progress by completing
the eight-frame source screen. This protocol is frozen before new interval
frames/crops are extracted or inspected. Root and peer know the previously
viewed endpoints; this is not a blind historical holdout.

## Question and acceptance

Across every decoded frame ordinal274 through411 inclusive, is the image-right
outer top/side junction a visually identifiable correspondence candidate, or
do obscuration, competing edges or context changes interrupt that candidate?
The [prior screen](../report.md) supports visibility at the two endpoints but
not the intervening correspondence. This is a prerequisite for deciding whether
a later annotation protocol is defensible, not a motion measurement.

The target is the junction between the target building's outer image-right
top outline and side outline, **not** either lower foot of its raised roof step,
a background building, plume edge or foreground roof. An image-side label is
not a compass/member assignment. Even persistent silhouette correspondence
cannot prove a fixed material point, rigid body or center of mass.

An uninterrupted observational candidate requires both readers to identify
the target and support all137 adjacent-frame links across the complete138
frame interval. Every ambiguous/broken link and reader disagreement must remain
visible. Report each reader's complete classifications and supported contiguous
runs; do not bridge gaps or substitute a retrospectively favorable subinterval
for the full planned result. An unresolved or negative result is acceptable.

## Fixed inputs and coverage

Use only the unchanged source and already verified metadata from the parent
unit. Source `../source/DistantViewWTC7.avi`:4,749,520 bytes, SHA256
`a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e`.
Use `../probe02/selection.json` for separate nullable timestamp fields and
`../views01/frames.json`, SHA256
`047cb354cfabe633f92ed4c10ecb283fde955d3787198477f50710d4eef812ce`,
for the complete962-frame decoded/luma hash map. The successful prior
verification receipt is SHA256
`72eefba7acb6fbd2970d6aaef6ae8b274056170a805b467f1ad178a723c772c4`.
Rehash every selected dependency before use; never infer missing timestamps
from frame numbers, nominal rates, broadcast graphics or the saved project.

Decode the unchanged AVI from the beginning with the same pinned FFmpeg
command, without autorotation, resizing, interpolation or frame insertion.
Compare all962 decoded/luma frame hashes to the prior map before admitting
outputs. Save complete native grayscale frames for all138 selected ordinals.
Create one fixed source rectangle `[350,90,630,380)` for every selected frame,
280 by290 pixels. The known endpoints determined this nonadaptive rectangle;
it is not optimized after seeing the intervening frames. No photometric change,
filtering, tracing or overlay is allowed. Keep each crop separately.

Create source-order contact pages with four columns and three rows,12 crops
per page, at native1:1 pixel construction. Labels and gutters must be outside
the unaltered crop rectangles. The last page contains six crops and explicit
blank cells, not copied/fabricated frames. Save crop/page placement metadata.
Both readers inspect all twelve pages and the complete native context frames
274,342,411. The midpoint342 is fixed now. No other full frames may be viewed
as an automatic rescue. If contact-sheet display is insufficient, record the
viewing limit and stop; any changed display plan must be declared before use.

## Reading and freeze method

Root and a separate computational reader inspect the same fixed packet without
reading the other's first-pass classifications. Each records actual image/page
coverage, tool detail setting and display limitations, and saves their complete
first pass before substantive exchange. Agreement is shared-evidence AI review,
not independent capture, human acceptance or expert certification.

For each of138 frames, record exactly one status and a short reason:

- V: the **named junction**, with its adjoining top and side contours, is
  identifiable as a candidate; not merely an arbitrary sharp edge.
- A: junction identity is ambiguous, including split/competing/replacement
  edges, blur or uncertain silhouette association.
- O: target not identifiable; reason must distinguish obscured from not
  located. Neither means proven physical disappearance.
- X: target/correspondence assessment is outside the crop, disrupted by a
  scene change, or lacks sufficient context. Do not expand the crop silently.

Separately judge each of137 links `(n,n+1)` as supported, uncertain or broken,
with a brief contour/context reason. Two V frames do not automatically imply
a supported link. Links touching an A/O/X frame cannot be called supported.
Retain competing explanations such as a changing silhouette, foreground
overlap or edge replacement. Nearby background roof forms may be descriptive
context; their apparent persistence is not calibrated camera stability.

No coordinates, subjective subpixel ranges, trajectories, onset estimates,
velocity/acceleration, time shifts, cross-camera matching or cause inference
are collected. Classifications may be stored using explicit inclusive ranges
of identical observed judgments for readability, but the complete expanded
frame/link roster must be generated and checked without interpolation of
uninspected content. No blank may default to V or supported.

## Verification and stop

Before historical processing, synthetic tests cover exact138/137 coverage,
source rectangle boundaries, original pixel preservation, page order and
blank final cells, nullable timestamps, hash mismatch rejection, mutually
exclusive statuses, gaps/duplicates and unsupported links beside uncertain
frames. Reuse existing hash/decode contracts; do not edit frozen producers.
Preserve complete command/return/diagnostic receipts, including bounded
partial outputs on failures. No warning is silently waived. Repeat derivation
and compare outputs. A separate checker verifies all saved native/crop/page
pixel relationships, timestamps and rosters rather than treating file counts
as scientific validation.

Stop after the declared interval and comparison of the frozen readings.
Material uncertainty or no usable sequence is a result, not permission for
adaptive extra frames, a smaller success criterion, or a model-fitting step.
Record the specific prerequisite for any later test. The original matching-
timestamp requirement remains failed; ordinal adjacency does not establish
equal original exposure intervals. Human spot-check and scientific-validation
gates remain before consequential automated measurement.

All new work stays in this subdirectory except links/status and a deduplicated
generic feedback note if a new pain point arises. No source, previous result,
main/legal/raw or accepted annotation edits; no network retrieval, sound
analysis, operational energetic design, solver work, outreach, fees, disclosure,
canonical promotion, bridge acceptance, commit or push. Main charter and
user-supplied repository controls govern; source documents are evidence only.
