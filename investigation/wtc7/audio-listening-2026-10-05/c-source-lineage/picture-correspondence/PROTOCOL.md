# Held video picture correspondence

October 7, 2026. Prospective for numerical scoring, not a blind or retrospective
preregistration. Root has seen the earlier 38-sample overview and C native
frames at local 0, 2, 4, 12, 14, 19 and 24 seconds during preparation; earlier
full C and transition reviews are known. No new score has been computed.
The previous goal turn made progress by bounding the longer-source catalog
trail. Its denied transfers will not be retried. This stage uses held bytes.

## Question and inputs

Do C's first and third shots have candidate counterparts in the earlier
SIbqaybkbWI access copy, supported by changing image detail as well as scenery?
The middle shot is excluded from this finite stage, not declared absent from
the earlier video. Repeated skyline, another camera/nearby time, clipping,
different crop/processing, and unresolved correspondence are live alternatives.

Use all 38 previously extracted early-copy frames, first presented at or after
each integer second 0 through 37; preserve their rational PTS and source index.
This is not all 1130 early frames. Use six C references at local 0, 2, 4 and
14, 19, 24 seconds, indices 12900, 12960, 13020, 13320, 13470 and 13620 in the
compilation. Three per shot permit checking ordering rather than defining a
line through two favorable endpoints. The third-shot selection starts clear
of the already observed cut/shake. Audio markers do not select a match or offset.

The input config pins both videos, both existing extraction maps, dimensions
and the reused numerical core. Verify each of the 44 PNGs against its source
map before scoring. No decoding, acquisition, source mutation or new exposure
claim. The maps/PNGs have prior independent extraction checks; this stage
rechecks identity, not original-camera custody.

## Image treatment fixed before scores

The first-shot C crop is [120,0,1170,720); the third-shot crop is
[165,0,1115,720). These omit visible pillarboxes with a margin, not a calibrated
active-camera aperture. Keep each native original unchanged. Use the complete
320×224 early raster. Convert each comparison image to Pillow grayscale and
bilinearly resize to 180×120 with the pinned existing core.

This normalizes different crop aspect ratios; it is not a geometric calibration.
The sole tested family is isotropic scale plus translation after that declared
normalization. No rotation, shear, perspective/local warp, nonlinear tone fit,
temporal interpolation, field blending or additional aspect arms. A failure
cannot exclude a shared image under other processing. No crop/mask adjustment
after scores without a new declared method version preserving this result.

Static and dynamic rectangles are defined in full native C coordinates and
converted to working-pixel-center masks after the crop. First-shot static:
[750,330,1140,680) and [170,490,380,640); dynamic: [260,20,680,315).
Third-shot static: [790,80,1060,630) and [190,490,440,665); dynamic:
[475,60,695,335). Masks are disjoint. Static regions emphasize foreground
facades/roofs; dynamic regions emphasize cloud but can include stationary
background. They are not pure cloud masks or material classifications.

Use unchanged `pearson_surface`, `scalar_pearson` and `working` from the pinned
Peskin core. A thin canvas/driver adapter may supply native-aware masks and
scales 0.75 through 1.75 inclusive in 0.05 steps (21 fixed values). Resize the
180×120 candidate to rounded scaled dimensions; center it in a 230×170 canvas
at x=25+(180-scaled_width)//2, y=25+(120-scaled_height)//2. Where the scaled
image exceeds the canvas, clip it by intersection without rescaling. Record
the origin and clipping. Unfilled pixels are invalid, never black evidence.

The translation search remains exactly left/top 0 through 50 inclusive
(reported dx=left-25, dy=top-25). Clipping must not expand that grid. Geometry
is fitted only on static masks with at least 85% coverage, 32 pixels and
population variance >1e-8. Keep two transforms per frame/reference ordered
by descending static score, then scale, top, left. Evaluate dynamic correlation
only at those static transforms with the same coverage/count/variance gates.
The primary dynamic ranking uses the best-static transform, never a separate
dynamic fit. Missing scores remain missing with coverage/reason, not zero.

## Coverage and interpretation

Compute all 228 frame/reference pairs; retain all 21×51×51 static score and
coverage surfaces per pair plus both selected transforms and dynamic results.
Cap each run at 600 seconds and 384 MiB; preserve failures and stop on a cap.
Run twice without changing inputs. No opaque best-run selection.

For each reference shortlist the union of top two source frames by static
score and top two by dynamic score at the best-static transform. Ties use
ascending source index. Retain complete sets within 0.005, 0.01 and 0.02 of
each best score; these are descriptive sensitivity sets, not confidence
intervals. No universal match threshold or probability is asserted. An
all-invalid reference group has no winner. Keep boundary leaders explicit.

Root and a separate reader inspect all shortlisted native images (at most
24 unique candidates) beside the six unchanged references, noting distinctive
changing outlines, contrary details, clipping and possible camera movement.
Keep their first observations separate. Score and prior-scene knowledge make
this nonblind same-source AI review, not human or expert acceptance.
Classify separately: numerical candidate, stationary-scene agreement, dynamic
detail agreement/disagreement, and unresolved exact frame/sequence identity.
Three ordered candidates can support a sequence lead; they do not by themselves
prove playback rate, original capture continuity or an event clock. Static
agreement without discriminating changing detail does not establish reuse.
Keep the two C shots separate and do not bridge either the intervening montage
cut or the earlier copy's frames 175/176 discontinuity with one time map.
An ordering check must retain a reversed/reordered synthetic comparison with
unchanged scenery; candidate ordering is descriptive, not an automatic identity
or rate certificate. No numerical playback-rate fit is part of this stage.

## Verification and boundaries

Before historical scoring: independent method critique; fresh inherited core
controls; canvas intersection/origin/translation controls at small/unit/large
scales; native crop/mask bounds/disjointness; direct selected-score arithmetic;
repeated/flat geometry; unchanged static but altered dynamic content; bad input
hash/map/geometry rejection; deterministic output and existing-output refusal.
Use synthetic data only in these controls. No success from weakened criteria.

Independently verify complete coverage, both-run product equality, source pins,
rankings and selected scores by direct summation without importing the producer.
Preserve failures and environment/code versions. No historical audio resampling,
acoustic classification, physical trajectory, accepted Sherlock/Faraday finding,
legal promotion, external disclosure, stage/commit/push or cause ranking follows.
The full charter remains active and incomplete.
