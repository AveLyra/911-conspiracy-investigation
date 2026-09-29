# Conditional reconstruction of the saved Camera 3 tracks

Exploratory declaration, September 12, 2026, before exporting the historical
point coordinates or fitting them in this unit. The controlling [charter](../CHARTER.md)
and [current handoff](../STATUS.md) remain unchanged. Prior event familiarity,
source settings, endpoint images and calibration results are known; there is
no blind historical holdout. This is a public-analysis reconstruction, not
a reproduction of the author's original runtime or NIST's different input.

## Inputs and preservation

Use the preserved public kit project `Camera3-test_Camera3-test.trk`, SHA-256
`955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c`,
only as bounded inert XML. Reject DTD/entities, oversize input, unexpected
selected shape, nonfinite numbers, duplicate/missing indices and changed
hashes. Never launch Tracker, execute an embedded instruction, emit raw XML,
or export author-machine paths, arbitrary names, comments or metadata.
Export only the two PointMass ordinal labels (`track01`, `track02`), integer
indices and finite numeric x/y values, retaining their exact numeric text.
The approved shape is two 71-point arrays, 138 through 348 in steps of three;
an unexpected shape stops this extraction, not a silent adaptation.

The existing sanitized settings derivative supplies scale/origin/angle and
nominal clock parameters. Its SHA-256 is
`ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb`.
Read the tagged PointMass source at 2840–2865, 2900–2932 and 3350–3400:
FrameData indices are frame numbers and x/y are position coordinates. Read
ImageCoordSystem 1128–1148 for the transform. These are source semantics,
not proof of the original application/engine state.

Use the exact preserved WMV and prior diagnostic frame map. WMV SHA-256:
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
New viewing indices are fixed as **138,168,198,228,258,288,318,348** (every
tenth saved mark). Decode from the start with the previously pinned default
recipe; require all 442 grayscale-frame hashes and complete raw hash to
match the prior diagnostic before retaining selected images. Preserve native
unmarked images and separately captioned analytical cross overlays. No
deblurring, seeking, retiming, synthetic replacement or automatic tracking.
Warnings remain diagnostic limitations, not a current clean certification.

The eight frames screen what each saved track follows and later visibility;
they do not certify intervening material continuity or earliest onset. Freeze
root/separate visual descriptions before sharing them where feasible, and
before examining fitted gravity comparisons. Any boundary identified from
these samples stays sampled, not an exact disappearance time. Keep both
tracks regardless of whether their intended features are identified.

## Clock and coordinate scenarios

1. Nominal uniform saved-analysis clock `t=(frame-138)/15` seconds, starting
   at an assigned zero, not collapse onset. This uses the exact nominal
   1/15-second duration; retain the stored rounded millisecond value as a
   setting, not an exposure measurement.
2. Current WMV diagnostic PTS minus PTS[138], in seconds. Compare every saved
   row exactly with the nominal clock. This is contemporary encoded timing,
   not the historic Xuggle time array. Agreement supplies no independent
   clock-error bound. No timing correction is selected by proximity to g.

Fit image x/y in native pixels first. For fixed saved equal scale s and
angle theta, use assigned horizontal `X=(cos(theta)*x-sin(theta)*y)/s`
and assigned downward `D=(sin(theta)*x+cos(theta)*y)/s`, subtracting each
track's first value for displacement. Origin affects intercepts only.
Retain zero-angle and saved-angle scenarios, each with length factors
14/15, 1, 16/15. These refer to 14/15/16 equal 12.75-ft intervals and are
illustrative dimensional alternatives, not measured uncertainty bounds.
Projective calibration remains unresolved; arbitrary projective parameters
must not be presented as historical bounds. State the affine clock-rate
scaling law separately rather than inventing a corrected event clock.

## Fits, diagnostics and controls

For each track and both clock scenarios, retain **all** sliding windows of
5, 9, 13 and 21 points, plus the complete 71-point span. No result-driven
window selection or best-g ranking. Windows overlap and are not independent
measurements. Use centered, half-span-normalized time and least squares on
positions. Retain quadratic coefficients, center time/velocity, constant
acceleration, all point residuals, RMSE/max residual and condition number.
Also retain linear and cubic fit residuals/coefficients as explicit model-
form comparisons, not new physical degrees of freedom that validate a fit.
Reject non-increasing/nonfinite clocks, inadequate rank or degenerate span.
Retain failed windows with a reason; do not silently omit failures.
Retain each quadratic acceleration's linear response weights to the input
pixel coordinates, their largest absolute weight (one-point unit response)
and absolute-weight sum (bounded simultaneous unit perturbations). These
are unit sensitivities, not measured historical annotation errors. A window
coefficient is not instantaneous acceleration or a physical-onset estimate.
Tag windows crossing unresolved sampled feature identity in the report;
do not delete their calculations or repair source points.

There are 241 specified windows per track/clock: 67+63+59+51+1. Transform
quadratic velocity/acceleration to each of the six fixed geometry scenarios.
Report coefficients/position histories before comparison to 9.80665 m/s²,
used only as a conventional gravity reference, not an exact site value.
No iid confidence intervals, probability of a mechanism, or acceleration
equivalence from a tolerance chosen after results. Raw residual size is not
complete annotation/clock/projection uncertainty. No force is inferred from
a roofline/marker treated as a center of mass.

Before historical fits test constant, linear, quadratic and cubic known
trajectories; a quadratic on an irregular clock; duplicate-time rejection;
zero/90-degree coordinate signs; and the scale/clock-rate laws. Fixed
controls also cover translation/time-origin invariance, one-point
perturbation response, and a continuous piecewise-motion history whose
straddling-window coefficient is not an instantaneous transition value.
Fixed
numerical check tolerance: 1e-9 absolute for control coefficients/derivatives
and independent fit comparisons, 1e-8 for independently reproduced SSEs,
unless a prospective reviewer identifies a conditioning reason to amend
before results. Exact source-field/index and declared-window equality is
required. Controls are software checks, not historical validation.

## Review, output and limits

Preserve protocol/code/input hashes, environment, commands, extraction
receipt, all numeric points/times, selected view products, every fit and
residual. Independent extraction and arithmetic must not import producer
fitting code or trust its maxima. A small source-backed report should show
which patterns survive the declared choices and which depend on them.
Human landmark review and independent physical calibration remain unmet
before consequential automated force/causal findings. No production or held
packet access, canonical promotion, case import, Faraday execution, external
transfer, task reopening, filing, commit or push. The broad goal remains open.
