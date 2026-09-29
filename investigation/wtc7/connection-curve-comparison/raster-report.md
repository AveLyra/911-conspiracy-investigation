# Synthetic raster reading: uncertainty and missing support

2026-09-27. Working research. Ready within the reviewed synthetic scope;
historical curve measurement is **not** ready or accepted. This completes the
fixed [raster test stage](RASTER-UNCERTAINTY-STAGE.md), not WP3 or the full goal.

## Result

The fixed known-color reader fails to locate one unambiguous stroke in many
of the deliberately degraded synthetic cases. Enlarging a coordinate envelope
can cover a shifted single stroke; it cannot supply missing support or resolve
multiple disconnected candidates. Three separately constructed scene pairs
also have identical visible pixels despite different latent content/identity.

These are method results, not observations about the historical connection
plots. No historical pixels or curve ordinates were read in this stage.
Neither a NIST/UAF discrepancy nor a collapse-cause ranking follows. The
earlier source/axis observations and human-review requirement remain unchanged.

## Full fixed grid, including unfavorable outcomes

The112 base fixtures span all seven declared artificial colors, two vertical
stroke widths, two slopes, two subpixel phases and solid/dashed styles. Five
encodings give560 cases, with128 tested source columns each. All71,680 column
records are preserved:53,760 with true visible support and17,920 true gaps.
They are related synthetic pixel columns, not independent statistical trials,
historical building samples or measured physical force/energy values.

Each table row contains10,752 true-support columns. Enclosure failures count
only single-run results; missing and ambiguous columns remain unresolved at
every allowance and must be included when assessing usable coverage.

| Encoding | Missing | Ambiguous | Single run | Enclosure failures at extra allowance0 /1 /2 /4px |
|---|---:|---:|---:|---|
| Lossless PNG |0|0|10,752|0 /0 /0 /0|
| JPEG95, subsampling0 |0|0|10,752|0 /0 /0 /0|
| JPEG75, subsampling0 |16|40|10,696|64 /0 /0 /0|
| JPEG75, subsampling2 |2,213|1,409|7,130|2,259 /540 /0 /0|
| JPEG50, subsampling2 |2,610|2,386|5,756|2,081 /433 /0 /0|

All four allowances were declared before outcomes. The favorable2px/4px
enclosure counts do **not** select2px as historical accuracy: bounds become
wider, unavailable columns remain unavailable, and neither the fixture grid
nor the supplied color predicate models the full historical imaging process.
No candidate was found in this grid's17,920 true gap columns. That finite
negative result does not authorize bridging actual dashes or declaring that
unknown historical gaps contain no line.

The [run01 summary](synthetic-run01/summary.json) contains per-case summaries.
Complete column records and interval widths are in the per-case files pinned
by its [manifest](synthetic-run01/manifest.json). The independently repeated
[run02 manifest](synthetic-run02/manifest.json) is identical. No failed case,
ambiguous component or less favorable radius was dropped.

## Identity limits tested constructively

The two sides of each pair were specified and rendered separately:

1. A dashed line and a solid line covered by white at the dash gaps.
2. Same-color crossing lines whose latent identity assignments either continue
   straight or switch branches after the crossing.
3. No line versus a line fully hidden by an opaque white layer.

Each pair has identical base RGB arrays, encoded files and decoded pixels
under all five encodings. The independent checker regenerated all six scenes.
The codec repetitions preserve three ambiguities; they are not15 independent
findings. Additional source labels, known masks or justified continuity
constraints can reduce ambiguity. These examples neither establish that a
specific historical trace is ambiguous nor demonstrate hidden historical data.

## Verification and independent review

The [producer record](raster-producer-validation.md) preserves exact commands,
settings, dependency pins, the14 focused controls and initial sandbox failures.
Both approved complete runs exited0. Each contains1,158 products plus its
manifest; all1,159 relative filenames and file bytes match between the runs.
The six instruction/code input identities remained unchanged.

The [separate review](raster-independent-review.md) and
[receipt](raster-independent-check01.json) reproduce35 predeclared cases:
all seven colors, thin/sloped/half-phase/dashed, across the five encodings.
All4,480 column records agree, including complete components, intervals,
widths, statuses and four allowance outcomes. Seven base RGB arrays and the
three ambiguity constructions also reproduce.31 independent-checker controls
pass;107 consumed run files stayed unchanged. This is a separate implementation
with prior discussion and producer-code access, not a blinded source study;
both implementations share Pillow/JPEG codecs.

Root read the full producer, tests, checker and both review records. Actual
additional checks, using bundled Python3.12.14/Pillow12.3.0:

- `python3 -B -m unittest -v test_raster_uncertainty`:14 tests passed.
- A read-only manifest walk checked every product's bytes/hash and exact file
  membership in both runs, then checked all current instruction/code pins.
- A stdout-only full replay called the producer's fixture/render/codec/probe
  functions for all560 cases and all three pairs. Every encoded image,
  decoded hash, all71,680 column records and summaries matched; no warnings.
  This is same-implementation reproduction, not a second independent method.
- A stdout-only `raster_independent_check.audit('synthetic-run01')` replay
  reproduced the entire saved independent receipt exactly, with31 controls,
  35 cases,4,480 columns, three pairs and no mismatches. No files were written.
- Root viewed20 complete synthetic images at original160x96 detail: PNG and
  JPEG50/subsampling2 for each of the seven thin/sloped/half-phase/dashed colors,
  plus both PNG sides of all three ambiguity pairs. No historical image was
  viewed. No UI was changed, so no new browser workflow was tested.

Visual QA showed the expected synthetic layouts and qualitatively weaker/
altered colored strokes under the degraded encoding. Crucially, strokes may
remain visually apparent where this particular numerical predicate fails.
**Detector failure is not proof of universal information loss or human
unreadability.** The exact equal-pixel pairs support the narrower constructive
identity limits independently of that detector's success rate.

Root reproduced a pre-outcome checker defect: memoization before validation
accepted equality-colliding boolean/float tuples after warming with integers.
Moving validation outside the cache corrected it; root rechecked rejection,
and the expanded controls preserve the regression. Thresholds and valid-pixel
calculations were unchanged. This is logged under existing local Sherlock
feedback, not a Sherlock product defect or sent/verified product fix. One
feedback patch initially missed its context and made no change before correction.
Early file locators ran before producer tests existed; missing-file status
was not treated as verification failure or evidence absence.

| Reproducibility artifact | SHA-256 |
|---|---|
| Stage declaration |4adaa3b617a624de9353feda130c1778e0c60d00e133d88754f66baa3298b248|
| Producer |878872fcde4316e2655e156221de970a41f5186351a9525159c7eb7520e8760f|
| Producer tests |eef9c8e5bd97bcb40f6f47f7e32419cff6b0ea5a43539acbb4bf486b7e036188|
| Each complete-run manifest |97ee9afda99a508c1fcbbe6d8b3f27df6674a0f970f43dcb651ba1182c2b60a8|
| Independent checker |6013e91b8f2ffa31daf8cd216d868575407df62a4c627e021b0fa79f575dd559|
| Independent receipt |67bb8f4be03e2cfad99504d36698d264784a17186e28d61a5cd0d844c6baeb66|

## Consequence for the investigation and remaining work

Keep uncertainty envelopes and unresolved identity/support as separate fields.
Do not insert zeros, interpolate an obscured span, use the widest radius to
admit an unidentified trace, or equate a pixel location with a model identity.
The numerical and evidence-audit checks require retaining these distinctions
in any later all-seven-pair comparison; they do not certify its future inputs.

Historical source-native linewidth/color characterization, actual-human
axis/legend and selected source-to-coordinate checks, visible-support
declarations and independently checked tracing remain unfinished. There is no
human reply to the earlier review request. This study does not approve those
steps, R1 review does not transfer, and the pending matrix/drawing/privacy
permissions are unchanged. No dash-gap bridging is admitted.

The mathematical contract also requires local ordinate envelopes over uncertain
x intervals and robust-sign comparison. That missing component was subsequently
declared and [implemented/checked separately](uncertainty-validation.md), using
synthetic curves only and retaining shared-axis dependence and missing support.
The frozen `curve_math.py` remains unchanged; the new adapter is not a graphical
uncertainty estimator or an implementation of all integral-error metrics.
Do not repeat this completed560-case grid or choose a historical allowance
from it. No historical tracing while the human gate remains unmet. Full
investigation active; no source promotion, accepted engine change, external
transfer, commit or push.
