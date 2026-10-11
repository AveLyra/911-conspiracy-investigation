# Third shot native aspect sensitivity

October 8, 2026. Prospective for the following computation, retrospective and
prior-informed as an investigation. Research only under the full main charter.
The parent coarse screen and dense first-shot results remain unchanged. This
finite test concerns the third shot, which contains the user's approximate bang
marker; it cannot authenticate that shot's soundtrack or locate a sound source.

## Question and scope

Does one fixed correction to the parent's unequal-aspect normalization improve
agreement in separate stationary detail and changing cloud detail, or does
third-shot correspondence remain unsupported under this alternative?

Use precisely C local 14, 19 and 24 seconds, compilation indices 13320, 13470,
13620, against all 38 parent early samples at/after seconds 0 through 37.
These are 114 pairs per arm, 228 total, not all earlier frames or new sources.
Retain black, nonmatching, invalid and endpoint candidates. No finer temporal
search, new acquisition or source edit is part of this unit.

Root has read prior scores and visual observations and reopened all three C
native references plus early frame720 before this declaration. The fixed
rectangles and sample selection are inherited, not selected by new scores.
Their familiarity means the evaluation region is excluded from this fit, not
genuinely previously unseen evidence or an independent camera.

Pin the parent's config, protocol, adapter, tests, both completed receipts,
independent receipt, numerical core and source maps/videos. Validate every
selected PNG, rational PTS and dimensions against the maps before and after.
The parent config is SHA256
`56efd21495ef21b37df9137438f0b53183a120b59b1b43eb0f498b4ac47d65b2`;
adapter `f5d2c75f758da5f3bdf63bd4b8b38d2eba1897aa6a52c37e93f6f91559d44f86`;
core `06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8`.
These reusable methods are not new historical observations.

## Exactly two matched arms

Keep the complete early 320 by 224 raster and C crop [165,0,1115,720],
950 by 720 native pixels. Both retain the parent's grayscale and bilinear
180 by 120 working transformation. This stage does not infer true camera
pixel aspect, calibrated perspective, lens distortion or original apertures.

1. **Normalization baseline:** candidate canvas sizes
   sw=round(180*s), sh=round(120*s), exactly the existing canvas family.
2. **Native relative aspect:** candidate sizes
   sw=round(180*s), sh=round(120*s*133/144).

The factor is fixed analytically, not optimized: native-relative magnifications
without rounding are (950/320)*s horizontally and (720/224)*s*f vertically.
Equality requires f=(950/320)/(720/224)=133/144. After rounding record actual
mx=950*sw/(180*320), my=720*sh/(120*224). The reference normalization itself
remains anisotropic; this arm corrects relative native geometry up to rounding,
not both displayed rasters or historical geometry. Native pixel aspect may
already differ between access copies, so neither arm is presumed correct.

Use the same two-stage resampling in both arms: core.working then candidate
canvas resize. A direct native-to-canvas resize would also alter smoothing
and is excluded. Interpolation and integer-size quantization remain limitations
of interpreting score differences; they are not a pure continuous-geometry test.
No letterbox is inserted in the working images. Canvas padding is invalid.

Keep all 21 parent scales .75 through 1.75 by .05, round sizes with Python's
existing round convention, center in the 230 by 170 canvas at
x=25+(180-sw)//2, y=25+(120-sh)//2, and clip only by canvas intersection.
Keep left/top0 through50 inclusive, dx=left-25, dy=top-25. No expansion at
boundaries, rotation, shear, perspective, local warp, tone fitting or free
aspect parameter. Preserve requested and actual geometry and clipping.

## Fit and evaluation

Convert all rectangles by inherited C native pixel centers after cropping:

- Fit only first former-static rectangle [790,80,1060,630].
- Evaluate second former-static rectangle [190,490,440,665] without refitting.
- Evaluate unchanged dynamic rectangle [475,60,695,335] without refitting.

All three are disjoint. The first includes repetitive facade detail; the second
can differ in depth and occlusion. The cloud rectangle includes background.
These facts can defeat registration or mimic agreement and must remain visible.
Do not switch fit/evaluation masks or add a combined score after seeing results.
The old union-static run is preserved background, not a matched control for
this changed fitting mask; both new arms use exactly the same first-rectangle fit.

Use pinned pearson_surface for fit and scalar_pearson for evaluation. Require
85 percent coverage, at least32 pixels and population variance strictly greater
than1e-8. Missing scores retain reason/count/coverage, not zero. Keep the top two
fit transforms by descending fit score, then scale, top, left. Evaluate both
other masks at those transforms; primary rankings use only the best fit.
Do not optimize transform or source-frame choice with a combined evaluation score.

Save full21x51x51 fit-score and coverage surfaces for every pair/arm, all retained
transforms, complete fit/static-evaluation/dynamic rankings, and near-best sets
within .005,.01,.02 of each best score. These are descriptive sensitivity sets,
not confidence intervals or identity probabilities. For each pair report
alternative-minus-baseline score/coverage differences where both exist and
explicit availability transitions otherwise. Retain scale/translation/sample
boundary leaders. A count of improvements is not an independent-sample test.

Different transforms may admit different pixels even when coverage counts match.
For each evaluated mask at both primary fit transforms, record valid-set equality
and intersection coverage. Add a common-valid-pixel diagnostic: evaluate both
already selected transforms on that same intersection, without any refit, using
the same85-percent-full-mask,32-pixel and variance gates. Retain both scores,
delta or reasons for missingness. This diagnostic does not select/rank frames.
Original unequal-support score differences alone cannot establish improvement;
even common-support changes remain subject to resampling/model limitations.

## Checks before and after historical scoring

Use the parent's Python3.13.7, NumPy2.3.4, Pillow12.0.0 runtime. Run fresh inherited
11 core and nine adapter controls. Add synthetic controls for f=1 exact baseline
equivalence, rational native mapping and rounded size/origin, mask separation,
all translation corners/clipping, known aspect relationship, unchanged fitting
with altered evaluation regions, repeated/flat detail, nulls, ties, exact228-pair
coverage, input pin/PTS failures, stale controls and exclusive output refusal.
No actual-score criterion may be weakened to pass a synthetic test.

Two deterministic historical runs, each limited to600 seconds and384 MiB of
saved output, use the same pinned inputs and fresh successful controls. Preserve
partial failures; do not raise caps or overwrite. Capture runtime/method/source
pins before and after, exact commands, outputs and failed attempts.

Independent checker must import neither this producer nor its numerical core.
It may reuse its own pinned direct-summation methods, with shared Pillow noted.
Check every pair/arm, full saved-surface top-two selection, all rankings/deltas,
both-run product equality and all retained fit/evaluation scores by direct sums.
Tolerances remain1e-9 absolute score and1e-12 coverage. Independent selected-score
checking does not independently recompute every FFT search cell. Synthetic
tests must precede this check's historical evaluation.

For each C reference and each arm, inspect the union of the top two source
frames in each of the three rankings (at most36 unique early candidates total)
alongside all three unchanged C references. Root and a separate AI reader keep
initial observations separate before comparison, noting static agreement,
distinctive cloud outlines, contrary details and ambiguity. Review is nonblind,
shared-source and not human/expert acceptance. No correlations alone establish
reuse; inspect contradictions outside the scoring regions too.

## Result and stop

Report paired processing sensitivity and source-specific interpretation at
all three moments, including failure and mixed outcomes. Improved facade fit
without discriminating cloud agreement is not shared-exposure identification.
Ordered candidates do not establish original speed, continuity or an event clock.
If neither arm supports a defensible common geometry, stop with that limitation;
do not search additional shape families until something fits.

Stop after two runs, independent arithmetic and finite image review regardless
outcome. No automatic dense third-shot search, audio alignment, time-map fitting,
causal ranking, source authentication, engine/bridge activation, human acceptance,
legal promotion, external transfer, commit or push. The specific continuous
source/soundtrack need and all wider charter obligations remain open.
