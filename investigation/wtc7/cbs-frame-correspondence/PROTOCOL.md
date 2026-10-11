# CBS frame correspondence protocol

2026-10-04 UTC. Prospective follow-up to the completed
[eight-clip source screen](../cbs-vince-source-screen/stage4/report.md).
The main-repository investigation charter controls. This is a bounded search
for candidate source frames, not a historical exposure certificate or a fire
measurement. Previous knowledge of the references and coarse samples is
disclosed; they are not clean holdouts.

## Question and fixed inputs

Can a fixed image-comparison procedure locate candidate counterparts to report
Figures 5-143 and 5-142 in acquired Clips 3 and 7, respectively? Can changing
image detail distinguish candidate moments after fitting only stationary
geometry? Repetitive facade features, another recording/time, broadcast edits,
and unknown report processing are explicit alternatives.

Use only these complete acquired files, never a partial transfer:

| Input | Relative path | SHA-256 |
| --- | --- | --- |
| Clip 3, 189 inventoried frames | ../cbs-vince-source-screen/stage2/raw/clip3-attempt1.avi | ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d |
| Clip 7, 1128 inventoried frames | ../cbs-vince-source-screen/stage4/raw/clip7-attempt1.avi | a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b |
| Figure 5-143, 705 by 480 | ../fire-coverage-batch3/assets/run01/images/A-60c26b7f3416.jpg | 744b8faff26ea05c8303dfe278d1644f7e949a0f0b3ec02ab13abf9a4af3fb75 |
| Figure 5-142, 706 by 457 | ../fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg | 68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a |

Clips have native 720 by 480 rasters, SAR 8:9, bottom-field-first metadata,
and encoded time base 333673/10000000. The encoded clock is not an authenticated
event clock. The report captions on printed pages 228–229 say intensities were
adjusted; Figure 5-142 additionally has floor/column labels. They do not specify
the complete processing history. Use the held PDF and preserved page text as
attributed source statements, not proof of historical conditions.

## Preparation before historical search

Read the existing Peskin correspondence kernel and its arithmetic review,
plus the existing native-frame sampler and controls. Reuse verified components;
do not repurpose the hard-coded Peskin dense driver or its source-specific
diagnostic rules. Preserve prior code and evidence.

Root may reopen each of the two complete native report JPEGs once, solely to
declare rectangular regions for this new test. Record that new viewing and
save half-open native-coordinate static/dynamic masks before computing any
new candidate score. Static regions must avoid report lettering and visible
flame/smoke as far as the reference permits; dynamic regions must be disjoint
and can contain stationary background. They are not pure flame masks. A
separate method reviewer checks the choices before historical execution. No
candidate-image rereading or tuning from scores during this preparation.

## Fixed comparison and transforms

Use the unmodified numerical functions in
`../peskin-figure-correspondence/match_screen.py` (SHA-256
06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8).
An adapter may supply new targets, native-size-aware masks and frame inputs.
Do not use the old 720 by 478 mask coordinate assumption for these references.
The adapter must also exclude the bottom quarter of each candidate working
raster from valid pixels, before correlation, as a uniform conservative
broadcast-banner guard. Do not count excluded pixels as black evidence. After
the initial working resize, exclude rows 88 through 119: the extra two rows
above the nominal row-90 cutoff protect against bilinear boundary mixing.
Scale this binary mask with nearest sampling alongside the bilinear image;
then exclude the last two otherwise-valid rows immediately above its scaled
bottom boundary as a second guard. Preserve both actual validity masks. This
rule is for these fixed raster sizes and thirteen scales, not a general filter
support theorem. Synthetic tests must show that changing only excluded native
bottom-quarter pixels leaves every declared-valid working and scaled pixel
unchanged in all three arms and all scales. Failure stops historical scoring.
This pre-score choice sacrifices coverage and does not certify that all
overlays elsewhere are removed. Reference masks are fixed in `regions.json`.

The reference arm is its full stored raster. For each candidate test exactly
three representations: full stored raster; rows 0,2,4,...; rows 1,3,5,... .
Parity arms retain measured rows only before the declared working resize;
they are not newly observed frames or proven exposure times. Do not blend
fields, motion-compensate, interpolate new temporal samples or fill missing
historical detail. Other possible reference field treatments remain untested.

Convert each representation with Pillow grayscale and bilinearly resize to
180 by 120. This is a numerical comparison grid, not aspect/perspective
calibration. Target masks select working-pixel centers mapped to the full
native target dimensions. Use the inherited thirteen scale factors 0.85 to
1.15 in 0.025 steps and integer translations -25 to +25 on the working grid.
Preserve rounded raster sizes and actual transform parameters. No rotation,
shear, projective warp, local warp, sharpening, histogram fitting or neural
reconstruction. A failed bounded search cannot exclude correspondence under
untested processing.

Fit geometry by masked Pearson correlation using only valid overlapping static
pixels. Require at least 85 percent static coverage, 32 pixels, and population
variance strictly greater than 1e-8 in each image. Padding is unobserved. For
each frame and representation keep the top two static transforms, breaking
ties by scale, top, then left as in the inherited kernel. Keep full score and
coverage surfaces for the pilot (108 comparisons: 18 frames, two references,
three representations). Cap pilot outputs at 256 MiB per run and elapsed
runtime at 240 seconds; preserve failure if either cap is exceeded. Dense
storage is not authorized by this pilot cap.

At each selected static transform evaluate dynamic correlation separately,
with 85 percent dynamic coverage and the same count/variance gates. Dynamic
scores never refit the transform. Neither score is a probability, confidence
interval, glazing classification, temperature, or automatic match certificate.
Linear gain/offset invariance does not establish robustness to unknown nonlinear
intensity adjustments, smoke, clipping or overlays.

## Coverage and review selection

Do not stop at a preferred match. The planned population is all 1317 indexed
frames in the two clips, each tested in all three representations against its
paired target. First test the already declared nine samples per clip as a
bounded implementation pilot. A pilot result is not full-clip coverage. Freeze
the implementation and review controls before that pilot; any subsequent method
change creates a new version and keeps the pilot, failures and stated reasons.

For each paired target and representation shortlist the union of the top two frames
by static score and top two by dynamic score at the best static transform.
Sort score ties by ascending source index. Retain every per-frame result and
report all candidate sets within 0.005, 0.01 and 0.02 of the best score as
descriptive sensitivity sets, not statistical intervals. Compute these sets
separately for every target, source clip, representation and metric, retaining
the distinction between paired and cross-view comparisons. Do not pool scores
across arms or treat these correlated alternatives as independent evidence.
An all-invalid group has no best score and an empty set with an explicit
reason, not a zero score, forced winner or omitted group. Shortlists use paired
comparisons only; the complete cross-view scores remain negative-control data.
Also compare the two
targets against the other clip's same pilot samples as difficult cross-view
controls; these are not authenticated unrelated events. Repeated facade geometry
and a stable scene with altered dynamic content are required synthetic controls.

The pilot may shortlist at most 24 distinct native candidate images total.
Read those in clip/index order, alongside the unchanged native references,
recording actual displays and contradictory or obscured details. Do not infer
exact exposure from a high score or a visually best static fit. Report separate
outcomes: computational candidate; static scene agreement; dynamic agreement
or disagreement; unresolved exact exposure. Field-arm agreement does not prove
which field generated the published image.

## Verification and execution boundaries

Before any historical computation: independent method critique, current source/
code pins, fresh inherited synthetic controls, and adapter controls for native
dimensions, masks, parity extraction, missing/duplicate frames, flat images,
ties, mismatched sources and deterministic reproduction. Use independent direct
summation on small arrays to check the reused correlation core; preserve its
strict variance-boundary convention explicitly. Tests must demonstrate that
matching stationary geometry with changed dynamic content is not source identity.

Pilot uses preserved nine-frame manifests and PNGs; verify their source/index/
PTS/hash joins. No new historical decoding is necessary for that pilot. Dense
execution needs a separate finite extraction/storage schedule, reviewed decoder
diagnostics and complete source-index joins before it starts. This protocol does
not authorize a silently expanded decoder or unbounded output. Preserve failed
runs; do not delete user/source files or weaken checks to obtain a pass.

Human review of the three report-still locations remains as recorded in
`../nist-acoustic-detectability/window-state-human-review-user-2026-09-29.md`.
The pilot is descriptive source-candidate retrieval only. It does not satisfy
the charter's actual-human spot-check requirement for consequential automated
measurement. No physical measurement, exact-source acceptance, event clock,
window-material conclusion, model validation, ranking change or legal promotion
is permitted from its scores. Prepare a concrete human check if downstream use
would rely on those conclusions; do not invent review or replay an old approval.

Deliver this protocol, frozen region choices, bounded adapter/controls,
execution receipts, complete pilot results and a reviewed limited synthesis.
Root owns protocol/regions/results and navigation; a separate reviewer owns
its critique. All work remains in this investigation worktree. No new downloads,
external disclosure, accepted Sherlock/Faraday state, matrix save, stage, commit
or push. The full charter remains active and incomplete.
