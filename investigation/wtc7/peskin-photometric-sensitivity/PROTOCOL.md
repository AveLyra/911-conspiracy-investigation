# Peskin figure photometric and visibility sensitivity

Research-only continuation under Q01/Q02 and the unchanged [charter](../CHARTER.md).
This declaration precedes this unit's historical calculations. The preceding
correspondence results and images are known: this is retrospective sensitivity,
not a fresh exposure-identification experiment or independent source family.

## Question and scope

Does a simple global monotone gray-level adjustment, fitted on foreground
buildings, transfer to the already defined background and bright-feature
regions? Which differences persist under candidate, sampling and tone-curve
choices? A failed transfer does not identify selective alteration: different
exposures, camera response, haze, blur, geometry and intermediate generations
remain alternatives. Success is compatibility, not identification of NIST's
processing method. No inference of interior fire extent, duration, heat flux,
steel temperature, structural failure or cause is authorized by this test.

Use exactly the 12 native candidate/target pairs from the prior global
shortlist in [primary-summary.json](../peskin-figure-correspondence/primary-summary.json),
SHA256 `c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3`.
Verify each native image against its pinned completed-run receipt and both
targets against the prior core's fixed hashes. Preserve all prior outputs.
No new acquisition, video decoding, image generation, enhancement for viewing,
archive access, model execution, transmission or canonical promotion.

## Fixed geometry, sampling and masks

Retain each candidate's best **previous** foreground geometry without refitting.
Compare four processing branches: 180x120 and 360x240 gray grids, each using
Pillow BILINEAR and BOX resizing. Convert to L before resizing. Scale the prior
integer canvas/raster dimensions and offsets by 1 or 2 to keep its numerical
geometry, not a new optimized geometry. Apply tone adjustment **after** these
resampling operations. This is not linear-light/colorimetric calibration or
physically correct aspect reconstruction. The 180/BILINEAR branch must exactly
reconstruct the old working image and valid mask.

Use both original foreground rectangles and all W1–W4/W1–W2 and D1–D4 boxes
from [check_regions.py](../peskin-figure-correspondence/check_regions.py),
SHA256 `6990064d77887e245b6843c0580679c5e5c9b5e5a262e1f5e8287fb7411a196b`.
Apply its 21 exclusions with four target-pixel expansion and outer-three-pixel
guard to foreground as well as evaluation masks. Pixel centers map into the
720x478 target coordinate system. These remain approximate scene neighborhoods,
not authenticated member/floor labels or pure-flame masks. Missing source
padding is invalid, never black scene evidence. Remove the union of every W/D
evaluation mask from the **new photometric** foreground mask: independent
pre-run review found that the old T149 foreground rectangle overlaps part of
W1. The preceding geometric fit remains unchanged; its old mask is not claimed
to be disjoint. Test the new fit/evaluation disjointness at both resolutions.

Split the foreground into alternating 8x8 baseline-grid tiles by parity of
floor(x/8)+floor(y/8). Use the same spatial tile layout at 2x resolution.
Fit on fold 0 and evaluate fold 1, then reverse. Geometry/shortlist already used
these scenes; this is only a within-image photometric fit/evaluation split.
W/D masks never train a curve. Keep both folds, all curves and all regions.

## Models and measurements

Keep the unadjusted baseline. For each fold and gamma in
`[0.5, 0.75, 1, 1.25, 1.5, 2, 3]`, fit ordinary least squares
`target/255 = a*(source/255)^gamma + b` on training pixels only. Require a>0.
Clip predictions to [0,1] for evaluation, preserving the fraction that the
unclipped prediction places outside that range. OLS is performed before
clipping; do not call it the optimum of a clipped-loss problem. Do not select
a curve on W/D performance or assign an empirical equivalence threshold.

Require >=32 observed pixels and >=85% coverage for any error/fit row. Constant
regions may have descriptive error but not rank information. Raw encoded-gray
population variance must exceed 1e-8 for rank/fit information; powered normalized
training-source variance must exceed 1e-14 for regression. Report nulls/reasons.
No historical error cutoff is a scientific pass/fail criterion.

For every valid region, baseline and fitted curve report signed bias, MAE and
RMSE in encoded 0–255 gray units (bias is prediction/source minus target);
fractions with absolute residual >25.5 and
>51; prediction/target fractions <=5 and >=250; exact endpoint fractions; and
threshold-support intersection-over-union (IoU) at levels 64,128,192,224.
Keep both selected fractions and union counts; both-empty IoU is null, not 1.
Threshold support is bright-pixel support, **not flame area**.

On unadjusted aligned arrays also report Spearman correlation with average
tie ranks and upper-quantile support IoU at q=0.1,0.2,0.3. Use linear quantile
interpolation and >= the resulting threshold; report realized fractions and
ties. Constant fields return null rank/quantile diagnostics. A strictly
monotone non-clipped tone map preserves ordering; do not count this invariance
as new corroboration from each gamma.

For each fold/region report source fractions outside the training minimum–
maximum and 1st–99th percentile interval. Bright-feature fits may extrapolate
far outside the available foreground range. Endpoint counts are encoded-image
diagnostics, not proof that a historical camera sensor saturated.

## Controls and verification gates

Before historical runs, test identity; all seven recoverable synthetic gamma
curves; quantization (separate <=2 gray-unit MAE control, not a historical
tolerance); monotone-rank invariance and clipping-induced ties; constant/tied
arrays; empty threshold unions; unchanged foreground with displaced/altered
bright evaluation patches; exact pixel-center masks; invalid padding/coverage;
and known extrapolation fractions. Noiseless recoverable normalized errors
must be <=1e-10. Preserve failed controls and version corrections.

Independent review checks the full protocol and implementation before the
historical run. Run twice into fresh create-only directories, compare all
scientific output and saved numerical arrays, and independently recompute
material metrics. Report shared libraries and actual independence. Synthetic
tests verify arithmetic behavior; they do not validate a historical account.

Bound this unit to these 12 pairs, four sampling branches, two folds and seven
gammas (672 fit attempts), with <=100 MiB total local derivatives and <=300 s
per invocation. No parameter search expansion merely because transfer fails.
Final artifact: linked research report, claim ledger, complete machine results,
source/code/version pins, reproduction and critical-review disposition.
Record useful generic workflow lessons under existing local Sherlock feedback;
the archived-destination routing decision remains pending.
