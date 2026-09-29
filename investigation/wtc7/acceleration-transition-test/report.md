# Do the published positions distinguish an abrupt acceleration onset?

2026-09-20 UTC. WP2/Q03–Q04, research only. [Prospective protocol](PROTOCOL.md),
[execution record](execution.md), [full historical result](run01.json),
[synthetic controls](controls02.json), [independent review](independent-review.md),
[exact verification](verification01.json). All declared fits have independently
checked optimality certificates; historical measurement validation remains absent.

## Result

**This test does not establish a zero-duration physical transition.** On the
declared finite grid, an abrupt acceleration change gives a slightly lower
position error for three roof points; a finite ramp gives a lower error for
the fourth. Every tested family/point needs tolerance beyond the table's
printing precision. The unknown tracking/calibration error and restricted
model family prevent turning this numerical ordering into a physical duration
estimate, statistical preference or collapse-cause ranking.

This does not erase the rapid downward curvature already reproduced in the
published data. It tests the sharper proposition that these positions require
an instantaneous acceleration change, not whether substantial acceleration
occurred. Nor does it test when every supporting column failed: these are
apparent roof-point coordinates, not a building center-of-mass or force history.

Claim strength: **A for the derived fixed-grid optima and counterexample**, within
the pinned data/model assumptions and exact verification; **D for a historical
transition duration or causal ordering**, because measurement uncertainty and
the structural connection remain unresolved. A wrong source cell, failed
certificate or mistaken model equation would weaken the numerical result.
Independently calibrated transition-spanning observations could change the
physical assessment. Arithmetic grade A is not physical-validation grade A.

## Data and equal-treatment comparison

Source is the held [Chandler/Walter/Szamboti 2023 paper](../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf),
page47, using the two previously reconciled independent transcriptions. This
unit rechecks the selected values and source hashes, not the original footage.
The [prior source review](../multipoint-table-reproduction/method-review.md)
records 0.2-second sampling and the paper's acknowledgment of limited
measurement resolution. Do not replace that qualification with a claim that
the paper measured mathematical simultaneity at unlimited resolution.

All16 common position rows6.4–9.4 seconds, source rows38–53, are used for each
of NE, east-center, west-center and NW. The earlier proposed9.2 cap was corrected
before calculation because it belonged to velocities. No row within the frozen
common window was discarded, blank filled, reference correction assumed or velocity counted as independent
data. Four points share one camera and measurement chain.

Each candidate has the same free initial position, baseline velocity and
downward acceleration amplitude. Acceleration is initially zero, then either
jumps to its fitted value or ramps linearly to it over0.2,0.4 or0.8 nominal
seconds. Those are four restricted kinematic descriptions, not four initiating
mechanisms. Acceleration is not fixed to gravity. Onset is tested at all41
predeclared values from6.4 through8.4, in0.05-second increments. The grid is
not observation resolution or a proof of the continuous-onset optimum.

For each of656 cases, minimize the largest absolute position residual R across
all16 rows. The additional required allowance beyond printing is
`max(0,R-0.005)` in the authors' assigned metres. It is **not** an estimated
physical error bar. Lower R means only a closer fit within this fixed grid;
no arbitrary statistical threshold or likelihood was assigned.

## All duration minima

Minimum maximum residual R, in **assigned position metres**. Six decimal places
describe arithmetic, not historical measurement accuracy. Exact fractions,
parameters, residuals, onsets and certificates are in the result file.

| Roof point | Abrupt | 0.2-second ramp | 0.4-second ramp | 0.8-second ramp |
|---|---:|---:|---:|---:|
|Northeast|0.050590|0.050954|0.052390|0.091022|
|East-center|0.320104|0.315972|0.304629|0.279555|
|West-center|0.140842|0.141036|0.141623|0.145545|
|Northwest|0.112289|0.112889|0.122933|0.150653|

None is printing-compatible at R<=0.005. Even the best duration per point needs
additional allowance approximately0.045590,0.274555,0.135842 and0.107289,
respectively. This rejects a printing-rounding-only account for these simple
families on this finite grid; it does not identify the source of the discrepancy
or falsify the underlying positions. Tracking error, camera effects,
preprocessing, deformation or more complex motion could contribute.

For the three points where the abrupt model wins, replacing it with the shortest
ramp increases R by approximately0.365,0.195 and0.599 **assigned millimetres**
(NE, WC, NW). These differences rank the printed central values. Their stability
over the admissible +/-0.005 printing intervals has not been established; no
perturbation test proves either preserved or reversed ordering. They are not
calibrated physical distinctions.
East-center instead favors the longest tested ramp; the0.8-second boundary is
the maximum tested duration, not an estimated optimum over all durations.
Mixed pointwise results are not evidence of four different causal mechanisms.

The best abrupt onsets are7.90,7.90,8.20 and8.05 nominal seconds. The respective
best0.2-second ramps start7.80,7.80,8.10 and7.95: their midpoints coincide with
those step onsets. At the best NE and EC0.2-second candidates, no sample lies
strictly inside the transition; there are observations at its endpoints.
The other two have one interior sample. This is a concrete sampling limitation,
not an assertion that any sub-sample history must fit.

All16 duration/point minima have a single grid onset, away from the onset-search
endpoints; all are saved, including worse candidates. This does not rule out
better off-grid or out-of-range solutions. The fitted final accelerations span
roughly-7.9 to-12.0 assigned m/s² across these minima. Their dependence on point,
window and model is another reason not to identify them with a common
center-of-mass acceleration or infer resistance directly from them.

## Why a good ramp fit is not evidence that the real transition was gradual

The predeclared synthetic control generates a **truly abrupt step** at7.625,
between allowed grid onsets. Its minimum R on the step grid is exactly353/11100
(about0.03180 synthetic position units), while the0.2-second ramp achieves
705311/24546600 (about0.02873). Thus a lower ramp error can occur even when the
generating transition was abrupt. The result was not demanded by the control;
all164 candidate fits are retained. It rules out the shortcut “the best ramp
fit identifies a gradual historical transition.”

There is also an analytic limitation. After a ramp ends,

```text
G(s,D) = 0.5*(s-D/2)^2 + D^2/24.
```

With free intercept and velocity, that is the same post-transition quadratic
family as a shifted step. Synthetic post-transition-only observations fit
every declared duration exactly. Information about shape must come from
observations spanning the transition; later free-fall-like curvature alone
cannot recover its duration. The controls also preserve the a=0 case, where
onset and duration are wholly unidentified.

The strongest objection to dismissing an abrupt transition remains valid:
three pointwise grid minima favor it, and the original dataset has substantial
downward curvature. The strongest objection to declaring it established is
equally material: none of these simplified models fits to printing precision,
measurement uncertainty is not supplied, and onset-grid effects can alter the
relative residual order. This calculation identifies a limitation, not a new
preferred physical history.

## Verification and what would change the conclusion

Floating optimization only proposes a basis. Every saved fit contains exact
rational parameters and nonnegative dual weights: all original residual/sign
constraints hold, and the dual lower bound equals the fitted R. This certifies
the optimum for that specified grid point, not for every possible onset/model.
Root has replayed these certificates for all656 historical and178 synthetic
fits. The clock transformations also preserve every residual, as predicted;
they are coordinate-covariance checks, not additional timing evidence.

The separate checker was frozen before reading producer results, uses the
independent transcription and a piecewise integrated basis, and imports no
optimizer or producer code. It verifies every original inequality, dual lower
bound, residual, grid membership, minimum/tie and clock mapping exactly:
656 historical cases,178 synthetic cases and2,502 clock-coordinate certificates.
The full historical optimization was also repeated with byte-identical output.
Independent proof checking and deterministic repetition are different checks;
neither adds an independent historical recording or engineering expertise.

The first synthetic attempt failed on a clock-certificate weight at the
acceleration-sign boundary. That failure, initial code and13 completed fits
remain preserved. The corrected attempt passed all178 synthetic fits before
the historical run. The checker also preserved a metadata-parser failure and
its one-line correction; no mathematical constraint or source value changed.
See the execution record for commands, pins, review and negative controls. No failed case was discarded
from the final fixed historical grid.

To infer a physical transition duration requires independently grounded
position/clock/calibration uncertainty, measurements resolving the transition,
and model comparisons that handle earlier motion and deformation. A verified
abrupt-only compatibility region under shared uncertainty would strengthen
abruptness; verified finite-transition histories within the same tolerances
would weaken its necessity. More freely adjustable curves without independent
constraints would not by themselves settle the issue.

The [integrated causal assessment](../causal-chain-synthesis/report.md) is
unchanged. This bounded follow-through does not authenticate the published
measurement chain, identify deliberate support removal, validate NIST's
initiating sequence, resolve every Luna artifact or complete the charter.
