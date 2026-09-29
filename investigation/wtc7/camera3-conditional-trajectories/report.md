# Conditional Camera 3 roofline trajectories

The saved public analysis contains a substantive kinematic result: under
its assigned scale and nominal clock, the image-right roof-corner track
has late-window downward acceleration close to gravity. That result is
not uniform across the two tracked locations, fitting windows or calibration
assumptions. It supports taking the rapid-descent observation seriously;
it does not establish whole-building free fall, simultaneous removal of all
supports, or what initiated the collapse.

For example, over nominal seconds 11.0–13.4, the right-corner quadratic fit
gives **9.874 assigned m/s²**, compared with the conventional gravity
reference 9.80665 m/s². The second upper-rim track gives **8.559 assigned m/s²**
over the same window. These are calculated coefficients, not calibrated
confidence intervals or a finding that either value equals a physical
acceleration to three decimals. All declared windows—not only this example—
are retained.[^1]

This reconstruction tests the public project's saved coordinates using new,
explicit polynomial fits. It does **not** reproduce the author's historical
velocity/acceleration estimator or NIST's different source/analysis chain.
The original runtime, physical calibration and human-review requirements
remain unresolved. The investigation's cause ranking is not changed by this
unit alone.

## Source and feature correspondence

Two separate PointMass arrays contain 71 positions each, at frame indices
138,141,…348. A numeric-only export retains their exact x/y literals and
ordinal identities, excluding private path fields, arbitrary names and
comments. Tagged software source describes these fields as saved position
coordinates, not measured velocities or forces.[^2]

Both visual reviewers inspected eight prospectively chosen native frames
and their separately marked query displays before interpreting fitted
accelerations. The observations agree on the important distinction:

- **track01:** a relatively distinctive image-right outer top/side corner
  of the broad facade. Its association is plausible in all eight samples,
  including the last small visible corner above foreground obstruction.
- **track02:** a less distinctive location on the main upper rim, initially
  beside the raised left rooftop structure's base. It does not track that
  structure's top. At the final sample the query is smoke-softened and
  adjacent to foreground overlap; its exact target association is ambiguous.

The raised rooftop silhouette changes before the broad facade's conspicuous
descent, but these two arrays do not measure that raised structure's separate
trajectory. Eight checks per track are not verification of all 71 positions
or an unchanged material point. A moving silhouette intersection can differ
from a material landmark. No cardinal corner label, center-of-mass identity,
rigidity or whole-building symmetry is assigned.[^3]

An exploratory follow-up checked the saved keyFrames field because the
early curves are very smooth. All 71 positions in each array are also listed
as keyframes. That rebuts the narrow suggestion that this saved state labels
some of these positions as interpolation gaps. The software's keyframe
category includes manual **and automatic** marks, however, and can be populated
on loading older data. It does not authenticate manual annotation, original
exposures, independent errors or the prior editing history. The initial
serialized-list format rejection and subsequent bounded adaptation are
preserved in the [keyframe addendum](KEYFRAME-ADDENDUM.md).

## Position histories and all-window comparison

The nominal saved-analysis clock is `t=(frame−138)/15` seconds. Its zero is
an assigned analysis origin, not identified collapse onset. At all 71 saved
indices, the current WMV's relative encoded times agree **exactly** with this
nominal grid. Consequently the two clock scenarios produce redundant
calculations here; they are not independent clock authentication or a test
of an unknown historical timing distortion.[^4]

The baseline converts native x/y into assigned downward displacement using
the saved 0.7240787° angle and 3.3366688 pixels per assigned metre. Both curves
have little early net displacement, then much larger descent late in the
record. Their final assigned downward displacements are 58.313 m and 56.802 m.
The frame 348 identity/occlusion qualification remains especially important
for the second value. Similar terminal displacement does not imply identical
acceleration histories.

![Saved position histories and all declared sliding-window accelerations, conditional on the nominal clock and saved calibration](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-conditional-trajectories/figure01/trajectories-and-window-sensitivity.png)

The upper panel shows the saved coordinates transformed to assigned metres.
The lower panels show **window-wise quadratic coefficients**, located at
each window's center—not independently measured instantaneous accelerations.
Every sliding window of 5, 9, 13 and 21 points is shown. Full-span fits remain
in the data but are omitted from the window plot. Source arrays for the
figure are retained in [plotted-series.json](figure01/plotted-series.json).

Each track/clock has 241 declared windows: 67+63+59+51 sliding windows and one
full 71-point window. Each window has linear, quadratic and cubic position
fits, including all residuals. Thus 964 window records contain 5,784 scalar
polynomial fits across two coordinates. Overlap, repeated clocks, transformed
copies and shared media are not independent replications.

The following examples expose the main window dependence. They were chosen
for concise display after the complete run, not preregistered as physical
onset boundaries or selected as the closest matches to gravity. The complete
[fit arrays](fit01/fits.json) preserve every declared alternative.

| Nominal window / frames | Points / duration | track01 downward coefficient | track02 downward coefficient |
|---|---|---:|---:|
| 6.0–10.0 / 228–288 | 21 / 4.0 s | 0.007 | 0.014 |
| 8.0–12.0 / 258–318 | 21 / 4.0 s | 2.605 | 2.932 |
| 10.0–14.0 / 288–348 | 21 / 4.0 s | 9.457 | 8.283 |
| 10.0–12.4 / 288–324 | 13 / 2.4 s | 9.379 | 8.385 |
| 11.0–13.4 / 303–339 | 13 / 2.4 s | 9.874 | 8.559 |
| 11.6–14.0 / 312–348 | 13 / 2.4 s | 8.504 | 7.225 |

Units are **assigned m/s²**, using the saved angle/15-interval scale. The
full 0–14 s quadratic coefficients are approximately 1.028 and 1.038 m/s²; those
long windows include the nearly stationary portion and must not be used as
an argument against a later gravity-like segment. Conversely, the late
near-gravity coefficient cannot characterize the entire 14-second record.

Across all 0.8-second windows, the maximum coefficients are 12.475 and 11.360
assigned m/s². Across 2.4-second windows, maxima are 10.469 and 9.353. Those
maxima describe retained calculations, not estimated physical peaks or a
search yielding the preferred mechanism. Short-window excursions above the
reference do not prove an additional downward force: annotation, tracking,
projection, deformation and changing local curvature remain alternatives.

## Fit quality and sensitivity

For the 11.0–13.4 s example, native-y RMSE is 8.175 pixels for a line, 0.352 for
a quadratic and 0.188 for a cubic on track01. The corresponding track02
values are 7.099, 0.431 and 0.157 pixels. The strong departure from a straight
position line is affirmative curvature evidence in the saved data. A cubic's
smaller in-sample residual is expected from its additional freedom and does
not establish its physical correctness. Residuals do not include calibration,
clock or material-correspondence errors.

The assumed physical span remains consequential:

| Assumed equal 12.75-ft intervals | Span | track01, 11.0–13.4 s | track02, same window |
|---|---:|---:|---:|
| 14 | 54.4068 m | 9.215 | 7.988 |
| 15, saved assignment | 58.2930 m | 9.874 | 8.559 |
| 16 | 62.1792 m | 10.532 | 9.129 |

These are dimensional scenarios, **not a measured uncertainty range**. The
preceding image study found affirmative support for approximately fifteen
repetition cycles but did not identify both physical endpoints. Nothing in
this table establishes equal probabilities for 14, 15 or 16. With 15 intervals,
removing the saved axis rotation changes the example to 9.862 and 8.556 m/s²:
small in this example, but not a measured bound on camera perspective.[^5]

Short-window derivative sensitivity is independently testable. Under the
baseline transform, a one-pixel change to one native y coordinate has the
maximum-response magnitudes below, depending on where the point lies in the
window. Values are rounded for display; use the retained full-precision
weights for a strict numerical bound:

| Window duration | Largest one-point response | Bound if every y value may independently shift by at most one pixel |
|---|---:|---:|
| 0.8 s / 5 points | 2.141 | 8.562 |
| 1.6 s / 9 points | 0.454 | 2.270 |
| 2.4 s / 13 points | 0.165 | 1.048 |
| 4.0 s / 21 points | 0.042 | 0.394 |

Units are assigned m/s² per stated perturbation. These are operator
sensitivities, not evidence that errors of that size occurred or statistical
error bars. They hold x fixed and omit other error sources. The weights and
their signs are retained for each fit. For an actual clock that is a factor
r longer per nominal second, with all else fixed, physical acceleration
would scale by 1/r². No value or historical range for r is established here.

## What the result changes

The saved right-corner trajectory supplies **positive conditional support
for gravity-scale late descent**. This investigation should not dismiss
that evidence merely because its provenance and calibration are imperfect.
The result also directly discourages treating “uniform free fall of the
whole building” as a measurement already obtained: the two saved locations,
window lengths and calibration scenarios do not yield one common result.
The numerical difference between tracks is real in the exported arrays;
its physical interpretation is not uniquely identified.

Several explanations for that difference remain: different material motion,
deforming silhouettes, perspective/depth differences, annotation differences
or an inadequately identified second feature. These calculations do not
select among them. Nor do they distinguish fire-induced support loss from
deliberate support removal. Such discrimination requires the initiation and
propagation evidence, not only the resulting roofline trajectory.

| Claim | Evidence layer / assessment | What would change the assessment |
|---|---|---|
| The saved arrays produce the reported conditional trajectories. | Derived; A for the specified numerical reconstruction, with complete independent verification and root rerun. This does not grade historical physical accuracy. | A source-field, time-index, transform or fit discrepancy. |
| A late right-corner fit is close to the gravity reference under the saved settings. | A for the computed coefficient; C for a historical gravity-scale interpretation, dependent on clock, scale, projection and tracking. | Independently calibrated geometry/time or re-annotation changing the curvature; all-window/model comparison. |
| Both tracks have one uniform gravity acceleration. | D as a physical equivalence claim; not established by these differing computed histories and unresolved physical uncertainty. This is not proof that no region had gravity-compatible acceleration. | Validated material tracks and physical uncertainty/camera geometry sufficient to reconcile or distinguish them. |
| All supporting structure suddenly disappeared. | E if asserted from these point/outline histories alone; not established. | A defined moving mass system, contact and force/mass accounting plus observable/structural evidence of support loss. |
| These fits identify fire, demolition or intent. | D/underdetermined; no mechanism-specific initiating test is performed here. | Building-specific causal-chain or affirmative operational/material evidence that discriminates the competing accounts. |

## Next discriminating work

The next local motion task is not another generic calibration review. It is
a **dense, independently annotated late-segment check** of the already located
material/outline features, with stationary-reference motion and alternative
visible calibration checked in the same source. Inspect the intervening
marks rather than assuming that eight samples validate them. Preserve
disagreement and determine how much of the track01/track02 difference survives
actual localization/reference/feature alternatives. Any fitted event boundary
must remain distinct from an observed support-failure time.

This remains one WP2 contribution. Cross-camera timing, physical force/mass
limits, source-linked structural/model tests, the other charter workstreams
and expert/human review are not completed by it. The new supplementary
production and its separate audit remain in the source plan; this media unit
does not reopen or characterize those payloads.

## Sources

[^1]: [Declared method](PROTOCOL.md), [all fits](fit01/fits.json), [position histories](fit01/trajectories.json), [summary](fit01/summary.json) and [run receipt](fit01/receipt.json). These are derived research results, not independent source evidence. Reading/verification and execution limits are recorded in [validation](validation.md).

[^2]: Preserved public [Camera3-test_Camera3-test.trk](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/nested/Camera3-test_Camera3-test.trk), SHA-256955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c; no raw XML displayed or copied. [Numeric-only export](extraction01/points.json). Tagged [PointMass source](/Users/admin/docs/911/research/sherlock-wtc7-investigation/tracker-clock-semantics/sources/tracker-6.1.2-PointMass.java), lines2840–2865,2900–2932,3350–3400; source-version context in [clock/source review](../metric-motion-audit/clock-source-review.md).

[^3]: [Frozen root observations](root-observations.md), [separate observations](independent-observations.md) and [view receipt](views01/receipt.json). Source WMV SHA-25648323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722; only eight selected frames were visually inspected. Complete decoded-stream identity is not complete visual review or historical exposure authentication.

[^4]: [Exact clock rows](fit01/clocks.json); prior [clock/source review](../metric-motion-audit/clock-source-review.md) and tagged [clock semantics](/Users/admin/docs/911/research/sherlock-wtc7-investigation/tracker-clock-semantics.md). Current encoded PTS are not substituted for the historical Xuggle time array.

[^5]: [Camera3 endpoint/repetition study](../camera3-calibration-endpoints/report.md) and [calibration source review](../metric-motion-audit/calibration-source-review.md). Those previously inspected primary pages and images are separate prior coverage, not new architectural verification here.
