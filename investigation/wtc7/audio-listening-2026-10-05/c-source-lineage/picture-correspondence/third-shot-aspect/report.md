# Third-shot aspect sensitivity: correspondence remains unresolved

October 8, 2026. Research only. **The fixed relative-aspect correction did not
establish a coherent three-moment picture match.** Both computational runs and
the separate arithmetic check passed. Two separately frozen, nonblind AI image
reviews found no unique exposure assignment. This is a completed bounded
processing-sensitivity test, not authentication of the footage or soundtrack,
human acceptance, a finding of manipulation, or a collapse-cause result.

## What was tested

The [frozen protocol](PROTOCOL.md) compares C local14,19,24 seconds with all38
previously held earlier samples:114 pairs per arm,228 total. Both arms fit only
the first stationary building rectangle, then evaluate a separate stationary
rectangle and the changing-cloud rectangle without refitting. The historical
frames and masks were already known; excluded-from-fit is not unseen evidence.

The baseline repeats the working-raster geometry; the alternative multiplies
candidate height by the fixed native-relative factor133/144. That analytically
removes the extra relative anisotropy introduced by normalizing a950x720 crop
and a320x224 image to180x120, up to integer rounding. It does not recover camera
calibration or earlier transfer geometry. Both held encodes report square
pixels, which does not establish how their predecessors were resized. Both
arms retain the same two-stage bilinear processing,21 scales and51x51 positions.

No thresholds, masks, samples or geometry were changed after historical scores.
The old union-static results remain background, not the matched baseline here.

## Results, including contrary and missing results

These are **best dynamic-region correlations across the declared samples**, not
probabilities. Each is evaluated at its frame's best stationary-fit transform;
the two arms can select different frames. They are not paired effect estimates.

| C local seconds | Baseline best score / earlier index | Native-relative best score / earlier index |
| --- | --- | --- |
| 14 | 0.345158 / 540 | 0.286504 / 570 |
| 19 | 0.505529 / 270 | 0.482525 / 240 |
| 24 | 0.667840 / 1049 | 0.610203 / 300 |

For the actual paired comparison, the following uses the **same valid pixel
positions in both arms**, with the original full-mask denominator and unchanged
coverage/variance gates. Delta is alternative minus baseline; positive means
higher correlation, not a better historical explanation. Samples are strongly
dependent, so counts and medians are descriptive, not significance tests.

| C local seconds | Region | Both scores available /38 | Positive / negative deltas | Median delta |
| --- | --- | --- | --- | --- |
| 14 | Separate stationary | 34 | 17 / 17 | +0.002956 |
| 14 | Dynamic | 37 | 14 / 23 | -0.020305 |
| 19 | Separate stationary | 35 | 23 / 12 | +0.018766 |
| 19 | Dynamic | 37 | 5 / 32 | -0.080586 |
| 24 | Separate stationary | 35 | 10 / 25 | -0.050018 |
| 24 | Dynamic | 36 | 8 / 28 | -0.039563 |

Thus the outcome is mixed for separate stationary detail, predominantly lower
for changing detail, and does not rescue the correspondence. All111 available
paired fitting scores also remain in the outputs, including17 improvements
and94 decreases. The22 unequal valid-position sets across228 evaluation
diagnostics demonstrate why raw score differences alone are inadequate.
For C24 stationary detail, common-support evaluation changes the positive/
negative counts from9/26 to10/25. Equal pixel counts need not mean equal pixels.

Missingness is retained: each reference has one early candidate with no fit in
either arm, giving six fitless arm-pairs. Among the remaining common-support
diagnostics, three C14 stationary, two C19 stationary, two C24 stationary and
one C24 dynamic comparisons fail their gates. No missing value became zero.
Full availability transitions and both retained transforms are in
[paired-summary.json](aspect01/paired-summary.json) and
[results.json](aspect01/results.json).

Boundary limitations also remain. Among111 primary transforms per arm,
baseline has19 scale-boundary and36 translation-boundary selections;
alternative has21 and37, respectively (these categories can overlap).
Both C19 dynamic leaders hit the maximum scale; the alternative C14 leader
hits a translation boundary and its C24 leader hits both. No top-two shortlist
entry is a sample endpoint, but1079 is the penultimate sample. The search was
not expanded to resolve any boundary.

## Native-image check and interpretation

[Root observations](root-observations.json) and the
[separate reader's observations](independent-visual-review.json) were frozen
before comparison. Each actually viewed all15 unique shortlisted earlier
images and all three full native C references. Neither is a human/expert
certification or an independent recording; both readers knew prior results.
Their comparison found no material disagreement.

The clearest outside-mask countermatch is C24 versus the alternative's dynamic
leader, early300. C24 has a large rounded cloud front descending beside the
central cupola-bearing roof into the road corridor; that nearer corridor is
comparatively clear in early300. C19 versus early240/270 has a similar lower
cloud disagreement. A favorable local score cannot establish whole-picture
identity. Baseline1049/1079 look more broadly consistent with C24's advanced
cloud development, but they remain neighboring alternatives, not unique matches.

Neither arm's dynamic leaders are chronological across the three C moments:
baseline540,270,1049; alternative570,240,300. This is an ambiguity warning,
**not proof of different footage or a test excluding every common-source map**.
Repeated facade agreement is a poor time discriminator in this setting.

The strongest alternative to this negative identification result is genuinely
shared footage with unmodeled crop, earlier distortion, camera movement or an
unsampled matching exposure. Nearby viewpoints, perspective, compression,
tone and low resolution also limit discrimination. The fixed correction is
only one processing hypothesis. Failure here cannot authenticate or discredit
the approximately13-second sound, locate it, determine original playback rate,
or change fire-versus-deliberate-support-removal rankings.

## Verification and stop

Both runs completed228 arm-pairs with41 PNGs verified before and after;
all233 material products per run are byte-identical. Start/receipt logs contain
different timing and command details and are not claimed byte-identical.
Fresh producer controls passed11 inherited core,9 parent adapter and18 new
tests. The separate checker passed26 synthetic tests; root reran them and the
full historical check, reproducing all substantive receipt fields.

The [independent receipt](independent-check.json) verifies444 retained
transforms,1,305 numeric selected scores,27 selected nulls, all18 ranking
groups,114 paired records and228 common-support records against69 input pins.
Maximum selected-score difference is2.609e-14 (allowed1e-9); coverage difference
4.441e-16 (allowed1e-12). It checks all saved-surface top-two selections, not
every FFT cell by a second algorithm. Pillow resampling remains shared.
An attempted reuse of the existing output path was refused before writing;
all235 files in that run, including logs, stayed unchanged. See the
[execution record](validation.md) for commands and preserved failed attempts.

This unit stops as declared: no further shape search, dense third-shot search,
audio alignment or source acquisition is authorized by these scores. The
specific continuous third-shot source and soundtrack remain missing. A new,
genuinely authorized source route or a separately justified prospective test
would be required to advance that question; not another tuned fit. Other
charter work remains open. The graph human-review packet and incomplete F7
peer reading are separate unchanged prerequisites, not a universal blocker.
No legal promotion, bridge/engine activation, external transfer, commit or push.
