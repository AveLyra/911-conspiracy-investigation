# Final mathematical and inferential review

Disposition: **qualified pass, with three precision edits recommended; no
blocking mathematical, numerical or fairness defect found** in the report
reviewed below. This is computational mathematical review, not a qualified
human measurement review, independent primary-source interpretation or cause
finding. The evidence-audit and source-of-truth skills guide its scope.

## Exact reviewed version and actual coverage

The complete 268-line [report](report.md) was read at SHA-256
`e1244985880135a062bdb34534bb25c4b5e420bf6b3960cf58fc2e0e04e51a4e`;
the hash was unchanged after review. The reviewer did not edit it. This
disposition applies to that exact version, not automatically to later edits.

The complete 126-line [source checker](verify_sources.py) was read at SHA-256
`75cb3e2a60ee542b4d56f1d568fa1a1306abe4883224c8406553245e04c1e4e7`.
The status and configuration results in [source-check-root01.json](source-check-root01.json),
SHA-256 `b3cb0bf523c5a267b2f3541de410b82f5c4c7f14dbe2a22c1bddb44c267bd1bd`,
were inspected; its recorded 65 hash checks all report matches. This final
review did **not** rerun those source-file hashes or reopen the underlying
PDFs, Java source, saved project or images. Source descriptions in the report
remain attributed to the named source-review passes, not newly certified by
this mathematical review.

The prior separate exact Taylor-series reconstruction of all 26 synthetic
examples remains documented in [math-review.md](math-review.md) and
[independent-runs01.json](independent-runs01.json). In this final pass, the
reviewer directly parsed both complete independent receipts and checked that
[independent-root01.json](independent-root01.json) equals its own receipt in
every field except `command`. It did not import the producer, rerun a
historical fit, inspect media, alter source data, or transfer anything outside
the research worktree.

## Independent numerical cross-checks

Using only the decimal endpoint/length/scale numbers quoted in the report,
a fresh 60-digit Decimal calculation gives:

- Pixel separation: `194.504431891343417342258839469908744494702613773706018568811`.
- Separation divided by 58.293 assigned metres:
  `3.33666875767833903457119790489267569853503188673950591955828` pixels/assigned metre.
- Difference from the quoted saved scale:
  `7.3457119790489267569853503188673950591955828e-16` pixels/assigned metre.
- Reciprocal saved scale:
  `0.299700111885185232246292661999755300959474710222535151149453` assigned metres/pixel.

These agree with the report and source-check receipt to their stated precision.
This verifies arithmetic on the reported configuration, not the endpoint
identities, source transcription, dimensional survey or true metric scale.

Exact Fraction calculations independently confirm `58.293/0.3048=765/4 ft`,
equal to 191.25 ft and `15×12.75 ft`. All three quoted floor-pair differences
equal 765/4 ft. Multiple compatible pairs therefore do not identify which
architectural levels the tape actually joins. The report properly avoids
turning floor, window-top and parapet labels into identical measurements.

The timing arithmetic also is consistent: `8042+232+443=8717`,
`138+3×(102−1)=441`, `138+3×(71−1)=348`, and `3/15=0.2 seconds` under the
expressly stated uniform 15-fps clock. These arithmetic identities do not
independently validate the engine's historical loaded clock or point marks.

For a fixed distance and constant acceleration from rest,
`a2/a1=(t1/t2)²`; a factor 1.4 in duration therefore gives exactly `25/49`
(approximately 0.5102) of the original acceleration, not 0.6. This thought
experiment is correctly separated from the reported staged motion. The
quoted regression slope converts as `32.196×0.3048=9.8133408 m/s²`; that is
a unit conversion of published output, not a newly measured acceleration or
an uncertainty interval.

## Equations and interpretation

The chain-rule expressions, inverse acceleration formula, linear length-scale
factor and quadratic clock-rate factor are correct on their stated local
invertibility domain. The projective velocity-squared term and the specific
from-rest ratio `(1−3q)/(1+q)³` agree with the independently verified synthetic
examples. The report does not transfer that special ratio to arbitrary
initial velocity, evolving silhouettes or moving cameras.

The distant-camera relation is correct conditionally: when the actual optical
axis points through the baseline target, `q=Lh/R²` and `|q|≤|L|/R`. The
off-axis expression `q=L d_z/Z0` correctly retains optical depth rather than
substituting slant range. The report expressly does not reorient the actual
camera by relabelling coordinates or transfer the distant Cameras 1/2
description to near-field Camera 3. No numerical historical perspective bound
is claimed from the synthetic q-grid. This is an appropriate use of positive
geometric evidence, not arbitrary projection skepticism.

Constant time offsets are correctly distinguished from changing fit-window
membership or imposed onset conditions. Encoded PTS, declared application
settings and original exposure time remain different evidence layers. The
report fairly states that an unresolved clock join is not evidence that the
clock was wrong and does not automatically invalidate a separately described
NIST source/import chain.

A longer total descent and a later gravity-compatible interval can both be
true. The report correctly separates the printed smooth-position function,
its imposed initial conditions, the selected numerical-velocity regression,
and the unreplicated raw-data analysis. High R² does not establish a calibrated
physical uncertainty. Conversely, the report does not call the published
interval disproved merely because this investigation has not reproduced it.

The force ceiling is sound: Newton's law concerns a specified moving system
and its centre-of-mass acceleration, not automatically a visible roof point.
For an identified constant-mass body, downward `a≈g` would constrain its net
vertical non-gravitational force per unit mass; it would not by itself count
connections, establish simultaneous support loss or identify mechanism/intent.
The report does not erase that legitimate conditional mechanical constraint.

The circular-calibration warning is explicitly not an accusation. The report
acknowledges that the described architectural/dimensional methods are contrary
evidence to an allegation that gravity was used to set the same descent's
scale. It preserves legitimate conditional estimates while identifying the
next discriminating endpoint/source/geometry check. No premise of official
truth, deliberate intervention, guilt or innocence is required by this review.

## Recommended exact wording edits

These are precision improvements, not evidence of a different numerical result.

1. Replace **“For a fixed differentiable projection and monotone clock”** with
   **“For a fixed twice-differentiable projection and twice-differentiable clock
   with S′>0”**. The formula uses second derivatives and divides by S′; bare
   monotonicity alone does not ensure the needed nonzero local rate. Keep the
   following inverse requirement `F′≠0`.
2. Replace **“`v=-44.773+32.196t` in feet/seconds”** with
   **“`v(t)=−44.773 ft/s +(32.196 ft/s²)t`, with t in seconds”**. Velocity,
   intercept and slope have distinct units. This does not alter the printed
   coefficients or imply independent reproduction.
3. Replace **“the baseline vertical component is `h`”** with **“the
   camera-to-target baseline vector has signed vertical component `h`”**.
   This fixes the direction and sign convention used in `q=Lh/R²`; `L` uses
   the same vertical orientation.

No additional model fit, media inspection or new synthetic family is needed
to resolve these edits. The broader scientific admissibility decision remains
conditional on the report's identified source/feature/geometry/timing joins.

## Final revised-report disposition

The revised [report](report.md), SHA-256
`cdf5218c9b32ef76c4b7859b5e9c4acfa7405f9ead14fe7330fdc66855941e86`,
implements all three mathematical precision edits and the source reviewer's
replacement of “fifteen 12.75-ft storeys” with “fifteen 12.75-ft floor
intervals.” The reviewer read the changed sentences and verified that these
are **exactly the four changes**: reversing only those four substitutions in
memory reproduces the original reviewed report's complete SHA-256
`e1244985880135a062bdb34534bb25c4b5e420bf6b3960cf58fc2e0e04e51a4e`.
No report file was rewritten by this check.

Final disposition for `cdf5218c…`: **pass within the explicitly bounded
mathematical/numerical/inferential review scope**. The requested wording
corrections are resolved; no remaining meaningful correctness or fairness
issue was found in that exact text. This does not upgrade the separate source
attributions, assigned metric transform, physical calibration, human-review
status, gravitational-acceleration measurement or causal assessment beyond
the report's stated limits.
