# Fire-image contrast and correspondence sensitivity

Simple global gray-level adjustments account for much of the difference between
NIST Figures 5-148/149 and the retained Peskin access-copy candidates. Adjustments
fitted without the fire-test pixels reduce error in every declared background
and dynamic-region comparison. Fine-detail disagreement remains, particularly
in the small, faint Figure 5-148 feature. This supports a limited processing-
compatibility explanation, not exact exposure identity or a validated fire
history. It supplies no affirmative indication that these two illustrations
inflated fire extent, but it is not a test that excludes all local alteration.[^1]

This is research under Q01/Q02. The complete investigation, including the
thermal/structural and intervention hypotheses, remains open. No collapse
ranking changes from this test alone.

## Evidence and comparison

The targets are two 720x478 JPEG codestreams extracted from NCSTAR 1-9, printed
page 234 / physical page 278. Their captions disclose intensity adjustment and
added labels. The comparison frames are twelve saved 1620x1080 PNGs from an
admitted joined access copy, not authenticated camera originals. The preceding
959-frame study selected seven candidates for Figure 5-148 and five for
Figure 5-149. Those choices and the prior geometry were retained; this unit
did not search for a more favorable frame or count copies as independent
corroboration.[^2]

Four numerical sampling branches use 180x120 or 360x240 grids with bilinear or
box resizing. At each fixed geometry, alternating spatial tiles of a nominal
foreground mask train positive-slope affine transformations of gray values
raised to each of seven fixed powers. The other tiles and all W/D regions
evaluate transfer. The unadjusted baseline, both training folds and every
curve remain in the results: 48 image-pair branches and 672 fitted curves.[^3]

The masks describe image neighborhoods, not certified pure physical planes.
Independent pre-run review found that the old Figure 5-149 fitting rectangle
overlapped W1. The new photometric fitting mask excludes every W/D evaluation
pixel and passes explicit disjointness checks. The prior geometric fit still
used its original mask; it is not retroactively independent of those pixels.
This correction separates the present curve fitting from its evaluation,
without establishing a new event-level holdout.[^4]

## Measured results

Mean unadjusted access-copy gray levels are higher than the target levels in
all 344 W/D patch instances. For Figure 5-148 the regional mean differences
span 22.45–28.82 gray units; for Figure 5-149, 38.86–56.86, on an encoded 0–255
scale. These are means over selected masks, not a statement that every source
pixel is brighter, a radiometric ratio or a measurement of fire intensity.

Every one of the seven curve families reduces regional mean absolute error
(MAE) relative to its matching unadjusted baseline in all 688 fold/region
comparisons: 448 for Figure 5-148 and 240 for Figure 5-149. The full 4,816
comparisons remain available, with no curve selected using fire-region error.
These repeated choices share images and are not independent trials or a
significance calculation.[^1]

The following ranges cover **all** retained candidates, both resolutions,
both resampling methods, and both folds where applicable. The affine column
uses the predeclared gamma=1 case, not a post-hoc best curve. D1–D3 are the
prior bright-feature neighborhoods; they contain background pixels too.

| Target / region | Raw MAE | Affine-adjusted MAE | Unadjusted spatial-rank correlation |
|---|---:|---:|---:|
| 5-148 D1, isolated upper patch | 24.52–27.55 | 2.45–5.19 | 0.615–0.902 |
| 5-148 D2, lower cluster | 23.37–25.49 | 3.30–7.24 | 0.439–0.865 |
| 5-148 D3, faint lower patch | 23.92–25.84 | 1.45–3.51 | 0.289–0.647 |
| 5-149 D1, left occlusion-edge feature | 41.97–48.72 | 7.14–20.66 | 0.745–0.979 |
| 5-149 D2, central group | 53.65–55.25 | 7.65–12.78 | 0.776–0.951 |
| 5-149 D3, right group | 55.14–56.00 | 7.00–10.62 | 0.730–0.931 |

For the prior 5-148 leading candidate at source PTS 2521.133 s in the original
180/bilinear branch, D1–D3 raw MAEs of 26.79, 24.25 and 25.63 become respectively
2.45–2.51, 3.30–3.39 and 2.02–2.13 across the two affine fits. The prior 5-149
leader at 2524.203 s changes from 43.98, 54.02 and 55.91 to 7.14–7.24,
7.65–7.79 and 7.33–7.49. These are disclosed illustrative candidates chosen by
the preceding correspondence study, not new photometric winners. Complete
background, haze and foreground results remain in the machine record.[^1]

## Contrary results and sensitivity limits

Small residual magnitude is not exact shape identity. Figure 5-148 D3 has
relatively weak rank agreement across some choices, and its top-10%-brightness
support IoU ranges from 0.227 to 0.667. The 5-149 left feature's affine MAE
reaches 20.66 in the tested alternatives. Different resolutions and kernels
preserve nonzero discrepancies; they do not produce a uniquely identified
original exposure. No measured error threshold was calibrated as historical
equivalence.

Training-range extrapolation is limited but not absent. In the 5-149 left
feature, 1.19–8.00% of evaluated source values fall outside the respective
training minimum–maximum. Other bright regions also have occasional small
out-of-range fractions. Those highlights cannot be treated as calibrated by
ordinary training pixels. Clipping, quantile ties, endpoint counts and empty
threshold unions are retained separately. Empty support is uninformative,
not perfect agreement.

Rank stability under a strictly increasing, unclipped tone curve is a
mathematical property, not additional independent evidence from seven curves.
Threshold-selected pixels are not a segmentation of flame, source apertures
or burning interior area. A global brightness difference can coexist with a
local change; reducing average error does not by itself exclude one. Different
exposure, blur, haze, crop, generation and unknown historical processing remain
unseparated alternatives. The experiment cannot recover the camera's response
or determine which processing was historically applied.

## Consequence for the fire inquiry

These two illustrations should not be treated as evidence of exaggerated fire
merely because their contrast differs from the access copy. The observed
spatial correspondence and transferable gray adjustment provide a concrete
ordinary account of much of that difference. This is narrower than certifying
the figures against every alteration hypothesis.

Whether NIST assumed excessive fire duration, spread, ventilation or member
heating remains a different question. That requires floor/time-qualified
observations and actual input histories, not a brightness-to-temperature
conversion. The earlier source-input comparison records specific assumptions
and reported visual/model mismatches that this image experiment does not
resolve.[^5] Deliberate intervention is neither established nor excluded by
the photometric result, and the integrated causal assessment is unchanged.

## Claim ledger

| Claim | Layer / strength | Support and reproduction | Assumption, alternative and falsifier |
|---|---|---|---|
| All declared tone families lower W/D MAE versus their raw baselines | Calculation / A within this experiment | Complete results, byte-identical second run, separate arithmetic audit | Conditional on saved candidates, geometry/masks and encoded grids; a mismatched input, failed independent calculation or omitted adverse row would weaken it. |
| Much of the gray difference is compatible with a global adjustment | Model-dependent inference / B within this family | Disjoint photometric fitting/evaluation and all-candidate transfer | Shared selection/geometry, mixed nominal planes and spatial dependence remain; local differences may coexist. An original-exposure comparison with persistent incompatible content could change the assessment. |
| Exact fine-feature identity is established | Unsupported / E as phrased | Residual and rank/quantile disagreement remain | Neighboring exposures and processing are unresolved; authenticated originals and exact transformations could establish a stronger match. |
| These pixels determine interior heat or validate collapse initiation | Unsupported / E | No calibrated thermal measurement or structural calculation here | Requires independent boundary conditions, material response and building-specific validation; neither a good nor bad gray match supplies them. |

## Reproducibility and next discriminating work

The [verification record](validation.md) separates 28 producer controls,
23 independent controls, exact two-run reproduction and the separately
implemented check of all 672 fits and 6,832 fitted-region rows. Shared image
preprocessing remains explicit. The preserved prior qualitative reviews supply
image-inspection context; this unit adds numerical sensitivity, not a new
blind visual-rating experiment.[^4]

Further tuning of these same two figures is unlikely to identify hidden fire
extent or recover original clocks. The next local WP1 task should repair the
earlier visibility/eligibility rubric with explicit calibration and then expand
the floor/façade/time observation map. Preserve the first annotators' disputed
denominators and distinguish a caution from a decisive exclusion. Exact
camera-original/edit/clock records and native fire-input histories remain
separate source dependencies, not quantities to infer from contrast.[^5]

## Sources

[^1]: [Complete descriptive summary](summary01.json), derived from [run01/results.json](run01/results.json); full arrays and repeated run retained. Source/code/recipe identities are in [validation](validation.md).
[^2]: NIST, *NCSTAR 1-9*, Figures 5-148/149, printed p.234; [target provenance review](../peskin-figure-correspondence/independent-target-review.md). Access-copy lineage and acquisitions: [Peskin source report](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-originals/peskin/report.md). Candidate selection: [completed correspondence report](../peskin-figure-correspondence/report.md). These are linked source records and derivatives, not extra independent witnesses.
[^3]: [Frozen protocol](PROTOCOL.md) and [measurement code](measure.py). All curve/mask/sampling choices precede this unit's historical calculations, with preceding image familiarity disclosed.
[^4]: [Independent pre-result methods review and post-result arithmetic addendum](method-review.md), [checker output](independent-check01.json), and [root replay](independent-root01.json). No licensed-expert or independent-camera validation is claimed.
[^5]: [Existing appearance map and unresolved eligibility problem](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/README.md), [source-input comparison](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation/source-comparison.md), and unchanged [causal-chain synthesis](../causal-chain-synthesis/report.md).
