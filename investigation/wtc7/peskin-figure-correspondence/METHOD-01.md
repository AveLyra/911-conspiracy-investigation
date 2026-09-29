# Initial registration method declaration

Saved after viewing the two complete report assets and full report page278,
before this unit's candidate-frame comparison. Previous screening familiarity
remains disclosed. This is a bounded candidate finder, not an exposure-identity
certificate. No source score has yet determined these choices.

Use installed NumPy/Pillow. Convert both images to Pillow's grayscale and
resize to180x120 with bilinear sampling for screening. This explicitly maps
each stored raster to a common numerical grid; it is not physical aspect or
angle calibration. Keep original full-resolution images for review.

For each frame compare isotropic working-grid scale factors0.85 through1.15
inclusive at0.025 increments, and integer translations up to25pixels per axis.
Scaling uses rounded raster dimensions and bilinear sampling; preserve the
actual x/y scale implied by rounding. Compute masked Pearson correlation on
the valid overlapping static pixels, with at least85% mask coverage and at
least32pixels. Reject variance below1e-8 rather than divide by zero. Use exact
linear FFT correlations, checked against an independent direct summation on
small synthetic arrays; padding is unobserved, never black evidence.

Static target rectangles, half-open720x478 pixel coordinates:

- Figure148: [5,5,242,435] and [660,5,715,425]. These foreground-building
  features are geometrical registration aids, not WTC7 fire observations.
- Figure149: [5,95,265,435] and [660,5,715,425].

Both masks exclude figure numbering, the bottom copyright text, and the main
WTC7 flame regions. Target149's small glare/foreground changes can still impair
registration; report that limit. Fit image translation/scale only, not member
coordinates. The independent target reviewer may suggest other regions; any
adoption is a separately labeled method version, not a silent replacement.

For each scale/translation, retain its score, overlap and transform. For each
frame retain its best static transform plus runner-up geometry alternatives.
After fitting, evaluate two separately reported dynamic grayscale regions:

- Figure148: [265,130,590,350], including the two small warm-feature bands and
  intervening smoke/windows. This region contains static detail too, so its
score is not an independent pure-flame measurement.
- Figure149: [265,275,590,350], covering the principal flame band. No automatic
  thermal or fire-area classification.

The static-fit ranking generates candidates; dynamic scores never refit the
geometry. Retain per-frame scores for all declared samples, and shortlist the
union of the top four by static score and top four by dynamic score per target
for actual full-frame review. Report sensitivity candidate sets within0.005,
0.01 and0.02 of each best score as descriptive thresholds, not calibrated
confidence intervals. Do not require a preferred time order or three-second
separation. Near-duplicate frames and unstable alignment remain alternatives.

Pre-score clarification from independent method review: the1e-8 variance gate
means population variance (centered sum of squares divided by the actual
overlapping pixel count), not the unnormalized centered sum. Root corrected
that initial implementation before any control or historical result. Complete
registration controls include identity, known integer translation/crop, and
a separately constructed184x123resize then central crop/JPEG quality65 case.
The latter must recover the declared1.025scale and known offset with static
correlation above0.85. These are algorithm controls, not historical tolerances.

First run deterministic synthetic positive/negative controls and the existing
32 one-second samples (bins2502-2533) only. This intermediate screen does not
complete the planned all-frame comparison. Inspect scores/residuals and actual
geometry before declaring any refined dense-pass method; retain initial
failures and the possibility this bounded transform family is inadequate.
