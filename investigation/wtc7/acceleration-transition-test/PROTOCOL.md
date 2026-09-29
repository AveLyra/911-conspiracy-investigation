# Published-position acceleration-transition test

2026-09-20 UTC. Prospective specification before new historical fits/code.
Prior turn: **progress**—completed the bounded lateral-geometry source and
synthetic audit, preserving an unreproduced historical magnitude. The full
charter remains active/incomplete. This new Q03/Q04 calculation follows the
Luna audit's table follow-through; it does not clear every Luna contribution.

## Authority, inputs and limits

Main AGENTS/WORKFLOW/START-HERE and full CHARTER read/rechecked; current worktree
branch `research/sherlock-wtc7-investigation`, HEAD `e8d83d7`. All existing WIP
preserved. Work is exploratory research only. Main/raw/accepted engine/legal
state stays untouched; no new media, structural solver, license, outreach,
upload, filing, commit or push. Local numerical optimization is not a collapse
simulation or a claim of engineering validation.

Held published positions: Chandler/Walter/Szamboti 2023 paper, physical/printed
page47. Preserved source PDF SHA256
`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
Previously separately transcribed and reconciled; no new page or video viewing
in this calculation. Parent directory: `../multipoint-table-reproduction/`.

- `transcription-root/table47.json`, SHA256
  `a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc`.
- `transcription-independent/table47.json`, SHA256
  `fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8`.
- `method-review.md`, `report.md`, `CLOCK-ADDENDUM.md` and
  `../multipoint-joint-consistency/report.md` supply prior method/clock limits.

Use all four position columns on their **full common intersection 6.4–9.4**
nominal seconds, inclusive: 16 rows at 0.2-second steps. The initial handoff's
9.2 endpoint was the last common velocity, not position; separate method review
caught this before any calculation. No row selection based on residuals,
blank filling, reference subtraction, smoothing or additional derived-velocity
observations. Verify both transcriptions match every selected literal value.
Preserve their source-row identifiers and all excluded rows as source data.

The coordinates are the authors' assigned metres, not independently calibrated
world distances. Closed +/-0.005 intervals represent nearest-hundredth printing
only, not total measurement uncertainty. Physical error distributions, native
clock, feature identity and preprocessing remain unverified. Four points share
one camera, calibration and source; no four-independent-witness claim.

## Models and fixed search

Let x=t-6.4, s=t-tau, and p+=max(p,0). For each target independently:

```text
y(t) = b + v*x + a*G(s,D),       b,v free; a <= 0
G(s,0) = (s+)^2 / 2
G(s,D) = [(s+)^3 - ((s-D)+)^3] / (6D),  D > 0.
```

Acceleration is zero before tau, jumps to a for D=0, or rises linearly from
zero to a across D and then remains a. These are restricted kinematic families,
not structural support-loss models. Identical free b/v/a for every duration;
no fixing a to gravity or velocity to zero. Baseline is constant velocity, not
an arbitrary earlier acceleration. Failure of either family is permitted.

Fixed nominal onset grid: tau=6.4+0.05*k, k=0..40 (41 choices through8.4).
Fixed durations: D=0,0.2,0.4,0.8 nominal seconds (0,1,2,4 sample intervals).
There are 4 targets x4 durations x41 onsets =656 fixed historical problems.
No post-result refinement/expansion or selection of one fitting window.

This grid does not supply 0.05-second observation resolution or continuous-tau
global optimality. Onset-start bounds are shared; acceleration-midpoint ranges
therefore differ with D. Report all results, all tied best grid onsets, extrema
at search boundaries, and counts of observations before, strictly inside, at
boundaries and after each transition. If a=0, onset/duration are unidentified.

## Objective and numerical proof

Minimize the total uniform residual R >=0 subject to
`abs(y_model[i]-y_printed[i]) <= R` for every selected row, and a<=0.
This is a linear program in (b,v,a,R) for fixed tau,D. Report R and additional
allowance `max(0,R-0.005)` in assigned position units. The allowance is a needed
model/data discrepancy, not an estimated measurement error or confidence band.

Comparison definitions fixed now: printing-compatible iff R<=0.005; all such
models are compatible with printing bounds regardless of finer residual order.
Otherwise compare exact minimum R values on the same finite grid: lower,
equal or higher. Report numeric differences, not a likelihood or an arbitrary
"close enough" threshold. Smaller residual above printing tolerance does not
identify a physical transition duration or causal mechanism.

Write all inequalities B z<=h including a<=0 and -R<=0. Objective
c=(0,0,0,1). Floating SciPy/HiGHS may propose an active basis, but each saved
optimum must have exact rational primal z and nonnegative dual lambda with
`B^T lambda=-c`, `R=-h^T lambda`, and every original inequality satisfied.
The matching lower/upper bounds prove fixed-grid optimality without trusting
the optimizer's success flag. No uncertified result counts as a fit.

Prospective basis reconstruction: use the proposed nonzero dual support and
active constraints; try absolute activity thresholds 1e-7,1e-6,1e-5, retaining
the threshold used. Solve four-row candidates exactly, require full primal/
dual validity and matching objective. Include degenerate zero-dual active
constraints as needed; singular candidate bases reject. If no certificate is
found, retain failure diagnostics and stop/report rather than discard the case,
widen error bounds, change the model or claim the continuous optimum.

## Clock covariance, not repeated evidence

Nominal clock factor alpha=1. The two previously declared alternatives use
alpha=1001/1000 and1000/999 (six frames at the respective near30fps rates).
Map time relative to6.4, onset relative to6.4, and D by the same alpha. Then
`G(alpha*s,alpha*D)=alpha^2 G(s,D)`. Keep b,R fixed; map v/alpha and a/alpha^2.
All position residuals and extra tolerances must be unchanged. Verify every
certificate under all three coordinate mappings; do not call them three
independent fits or select a historical clock. Full time origins are arbitrary
here. Retain the covariance transformation of every best-fit parameter.

## Synthetic tests before historical fits

Use exact same 16 t values6.4..9.4 for synthetic controls; x=t-6.4. Base
b=100,v=1/4,a=-8. All synthetic values are labeled generated, not evidence.

1. For each declared D, generate the model with tau=7.6 and fit at its true
   tau,D. Recover exact R=0 and the parameters; verify basis formula separately
   against the piecewise twice-integrated acceleration and boundary continuity.
2. Fit the exact line100+x/4 at tau7.6 for all four D. Require R=0,a=0 and
   label onset/duration unidentified.
3. Generate the step with tau4.0, so every sample is post-transition, and fit
   all four D at tau4.0. All must fit with R=0 after nuisance adjustment:
   after a ramp, `G(s,D)=0.5*(s-D/2)^2+D^2/24`. This demonstrates a genuine
   observability limitation, not a defect to repair.
4. Add exactly1 to row index3 (zero-based) of the tau7.6,D0 generated series;
   fit that fixed case and require a certified positive residual beyond0.005.
5. Generate a=+8 at tau7.6,D0; fit the downward-only family and preserve the
   certified constrained boundary result (a=0 expected).
6. Generate an off-grid **step**, tau7.625,D0; fit all164 declared grid pairs.
   Preserve all results and duration minima. Do not require the step family to
   win: the example tests whether grid mismatch can favor an apparent ramp.
7. Reject negative D, missing/duplicate/non-increasing selected times and
   inadequate observations; reject singular exact bases. Mutated primal or
   dual certificates must fail. Existing-output guards must refuse overwrite.

Known/model controls account for14 fits plus164 off-grid fits =178 synthetic
optimizations. No historical fits until these controls and their certificate
checks pass; retain failed attempts/code revisions with reasons.

## Independent verification, falsifier and acceptance

A separate computational reviewer should implement a verifier from this
protocol and the independent transcription **before reading producer code or
results**, deriving G piecewise and the optimality inequality independently.
Verify every source membership, constraint, certificate, residual, all onsets/
duration summaries and clock transformation. Root then replays that verification.
This is independent calculation/checking on one published dataset, not a blind
historical study, licensed expert review, or a holdout validation.

The test falsifies printing-only compatibility for a given fixed model/grid if
its exact minimum R exceeds0.005. A finite ramp with no larger required error
than an abrupt step defeats a claim of abrupt-step necessity **within these
families/data/grid**. Worse ramp fits do not exclude all gradual histories;
better ramp fits do not establish that duration in the real building. If every
family needs extra tolerance, report model/data inadequacy explicitly.

Completion requires all656 certified cases or an explicitly consequential
failure; all178 synthetic fits/control outcomes; independently checked full
results, uncertainty/identifiability caveats, and an updated research report/
status. The strongest objection is the unvalidated underlying measurement
chain and restricted model/grid. Do not convert assigned-point curvature into
whole-building acceleration, all-column failure time, intent or cause ranking.
