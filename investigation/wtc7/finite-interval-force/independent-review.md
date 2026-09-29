# Independent exact-arithmetic and mechanical review

2026-09-24. Research-only review under [the prospective protocol](PROTOCOL.md).
The evidence-falsification and development-verification skills guided claim
boundaries and the exact checks. This is computational review, not a qualified
structural-engineering opinion or independent historical measurement.

## Independence and frozen products

The reviewer derived and implemented the calculation without reading or
importing root's `calculate.py` or its products. The complete first result
and control hashes were sent to root before any producer comparison. Both
implementations necessarily use the same previously reconciled source table;
agreement does not add a new camera or independent calibration evidence.

Frozen code SHA256:
`f0d5b88c8aa56b87f4f69e64bc18951b929ccb758c57fc0658f66625b5b18520`.
First [exact results](oracle01/run01/results.json):
`e3902f6b5bf8eada0c5fa33efb54ab192e70a34668425e714118288f56b6314d`.
First [controls](oracle01/run01/controls.json):
`eed728b93f5f91b729461d45f59adb9f2468ac781bcf19fa0a873b3a929381d1`.
[Receipt](oracle01/run01/receipt.json):
`e3d2253128433f8669b15fbed3832e0226caf82ef346ce2710fdedd0f551c0e7`.

The receipt pins the table, held PDF, protocol, code, and CPython 3.14.0
runtime. Source hashes were actually checked in both executions. This verifies
captured bytes, not original tracking accuracy or source authenticity.

## Independent derivation

Use actual physical time for the identity, downward physical vertical position
`p`, and samples at `tc-h,tc,tc+h`, where `h>0`. Integrating twice, separately on
each side of the midpoint, gives

```text
q[p] = p(tc-h) - 2*p(tc) + p(tc+h)
A[p] = q[p]/h^2
     = integral_{-h}^{h} [(h-|s|)/h^2] * p''(tc+s) ds.
```

The triangular weight is nonnegative and integrates to one. Constant position
and velocity cancel. The quantity is a weighted mean acceleration, not a
pointwise second derivative, unweighted mean acceleration, or instantaneous
force. The identity permits nonconstant acceleration; a global quadratic fit
is unnecessary. Piecewise smooth motion with the usual integral interpretation
is sufficient.

Define a fixed set of material particles with constant total mass `M`, center
of mass `z`, constant gravity `g`, downward non-gravity external force `D`, and
upward external force `U`. Then `M*z''=M*g+D-U`. For `R=U-D`,

```text
weighted_mean[R]/(M*g) = 1 - A[z]/g.
```

Internal forces cancel only within that specified material set. An open
spatial control volume gaining mass requires momentum-flux accounting. A
tracked roof point is not automatically the COM; neither a visible facade nor
a component name defines the requisite mass system.

Write `p=z+r`. Suppose an independently justified offset constraint is
`|r(ti)-(alpha+beta*ti)|<=B` at the three selected times. Unknown affine offset
and relative velocity cancel. The three coefficients `(1,-2,1)` give
`|q[r]|<=4B`, hence `|A[p]-A[z]|<=4B/h^2`. Rotation and deformation must be
included in `r`; they are not ruled out by this calculation. A geometric bound
may later constrain them, but none is supplied here.

If `A[p]` is bounded by `[a_low,a_high]`, the resulting signed net-force interval is

```text
1-(a_high+4B/h^2)/g <= weighted_mean[R]/(M*g)
                          <= 1-(a_low-4B/h^2)/g.
```

To accommodate a proposed **lower bound** `weighted_mean[R]/(M*g)>=rho`, its
upper feasible limit must reach `rho`. Equivalently,

```text
B >= max(0, [q_point_low - h^2*g*(1-rho)]/4).
```

The oracle computes this last, displacement-first form independently. It also
checks exact equality to the protocol's acceleration-first hinge. The named
`rho` values are illustrative lower bounds on signed net upward force divided
by weight. They are not exact forces, probabilities, historical assignments,
or percentages of surviving columns. In particular `rho=0` means nonnegative
weighted net upward force, not exactly zero force.

## Sharpness and the inverse's scope

The positional bound is sharp: offset errors `(B,-B,B)` attain `q[r]=4B`;
the opposite signs attain `-4B`. The quadratic
`r(tc+s)=B*(2*s^2/h^2-1)` supplies a continuous witness bounded by `B` throughout
the interval. Independently varying printing cells attain the point interval
endpoints. Therefore the hinge is the exact minimum in this relaxed,
three-position feasible problem. If it is positive, using any smaller `B`
cannot reach the force lower bound. At its boundary a witness reaches that
bound; when the hinge clips to zero, the force lower bound can already be met
with affine point-COM offset. The controls check both situations.

This is only a necessary condition for a building-specific physical history.
Actual geometry, additional samples, admissible deformation, mass membership,
projection, and force restrictions can further shrink the feasible set. The
quadratic witness is an algebraic sharpness construction, not evidence that
the structure followed it. No joint physical reconstruction of all four points
or intervening source rows is claimed.

Bounded displacement does not bound instantaneous acceleration. For example,
`r(t)=B*cos(omega*(t-tc))` remains between `-B` and `B`, while
`r''(tc)=-B*omega^2` is unbounded as frequency increases. Therefore these
calculations do not bound peak force, individual connections, restoring
stiffness, or hidden failure times. They also do not separate upward resistance
from an additional downward force that might offset it.

## Exact source slots and sign

All positions below are the preserved **upward-positive source tokens**; the
oracle negates each once. Array indices are zero-based and source rows are
one-based. The source page is 47 throughout. No nulls occurred in the twelve
selected slots; nulls and missing values are rejected rather than filled.

| Point / column | Times | Array indices | Source rows | Raw upward positions |
|---|---|---|---|---|
| NE / ne_y | 8.0,8.6,9.2 | 45,48,51 | 46,49,52 | 127.98,125.51,119.77 |
| EC / ec_y | 8.2,9.4,10.6 | 46,52,58 | 47,53,59 | 127.25,117.06,92.59 |
| WC / wc_y | 8.2,9.4,10.6 | 46,52,58 | 47,53,59 | 128.40,119.66,95.47 |
| NW / nw_y | 8.2,9.4,10.6 | 46,52,58 | 47,53,59 | 129.68,120.61,96.85 |

NE spans 1.2 nominal seconds; the other triples span 2.4 nominal seconds.
They must not be described as simultaneous whole-facade force measurements.
Every result remains conditional on assigned metric scale, the specified
uniform clock scenario, and eventual material/physical coordinate identification.

## Numerical result inventory

The [exact results](oracle01/run01/results.json) preserve all twelve input
slots, twelve clock/point cases, acceleration intervals, continuous hinge
coefficients, and **all 72 exact threshold values**. Each nearest-hundredth
printing cell has half-width `1/200`; its second-difference half-width is
`1/(50*h^2)`. These are printing allowances, not historical measurement errors.

Nominal-clock results, in assigned metres and seconds:

| Point | h | A | Printing half-width | Hinge intercept | Hinge slope |
|---|---:|---:|---:|---:|---:|
| NE | 3/5 | 109/12 | 1/18 | -44/625 | 8829/10000 |
| EC | 6/5 | 119/12 | 1/72 | 167/5000 | 8829/2500 |
| WC | 6/5 | 515/48 | 1/72 | 3259/10000 | 8829/2500 |
| NW | 6/5 | 1469/144 | 1/72 | 1359/10000 | 8829/2500 |

For each clock multiplier `k` in `1,1001/1000,1000/999`, the complete exact
transformation is `h=k*h_nominal`, `A=A_nominal/k^2`, printing half-width
`e=e_nominal/k^2`, slope `s=s_nominal*k^2`, and intercept
`i=(q_center-1/50)/4-s`. Thus each continuous function is
`B_min(rho)=max(0,i+s*rho)`; all transformed coefficients are explicitly saved.
No historical clock is selected by the result.

Positive thresholds at `rho=0` for EC/WC/NW are a consequence of this assigned
scale/clock three-position curvature exceeding `g=9.81`, even after printing
allowance. They are not a new historical supergravity or downward-force claim.
They expose the additional geometric/calibration dependencies of converting
these point data into a nonnegative net-resistance statement. No physical `B`
is supplied, and no mechanism is ranked.

## Actual verification

Observed commands, both with exit 0:

```text
python3 -B research/sherlock-wtc7-investigation/finite-interval-force/oracle.py --out oracle01/run01
python3 -B research/sherlock-wtc7-investigation/finite-interval-force/oracle.py --out oracle01/run02
diff -rq research/sherlock-wtc7-investigation/finite-interval-force/oracle01/run01 research/sherlock-wtc7-investigation/finite-interval-force/oracle01/run02
```

The repeated directories' three files are byte-identical. Each execution passed
81 exact polynomial/integral identities (powers zero through eight, three
centers, three half-durations); 48 error vertices covering all eight signs at
each of two radii and three half-durations; 144 affine-offset invariance checks;
54 inverse/boundary/witness cases; and 13 malformed/null/missing/duplicate-time,
missing-position or nonpositive-duration rejection checks. Four analytic
oscillatory examples retain the instantaneous-force limitation. All explicit
checks use exact rational arithmetic; no optimizer or structural solver runs.

No numerical failure occurred in these two independent runs. Arithmetic
verification and source-byte integrity do not establish source accuracy,
physical calibration, COM identification, expert approval, or a collapse cause.

## Producer comparison after independent freeze

After sending the independent hashes, the reviewer read root's complete
`calculate.py` and its frozen `run01/results.json`, SHA256
`c3a79c48dff5ce9c04a25158aaf55085c76a2c6b25eabc6212eec146c6dec5c3`.
No producer code was imported. Root's source negation, interval construction,
clock scaling, and lower-bound hinge implement the stated equations correctly.
Root's saved controls cover 15 polynomial/affine cases, all eight signs at
each of two half-spans, and five invalid-input cases. The independent controls
above additionally test off-center polynomial identities, printing-error
vertices, inverse infeasibility below the threshold, and oscillatory limits.

The reviewer then ran a read-only inline `python3 -B -` checker, using only
`hashlib`, `json`, `fractions.Fraction`, and `pathlib`. It first asserted both
frozen result hashes, indexed producer cases by point and exact clock factor,
then checked every source token/row/time/sign, equal half-span, acceleration,
both printing endpoints, printing half-width, displacement second difference,
hinge coefficient, and scenario value against the independent result. It also
verified each producer decimal against its stored exact fraction. Observed
exit 0 and exact stdout:

```json
{"all_assertions_passed": true, "exact_case_agreements": 12, "exact_threshold_agreements": 72, "producer_decimal_consistency_checks": 132, "source_slots_checked": 12}
```

This establishes exact arithmetic agreement for the frozen twelve-case,
seventy-two-threshold calculation, including input membership. It does not
validate the historical inputs or expand the physical claim. No blocking
arithmetic or mechanical-formula issue was found in the inspected producer
code/results. Subsequent prose/derivation review is separate from these
frozen numerical comparisons.

## Report wording review

The reviewer read the complete report at SHA256
`11d07b76419608ecbc7a30fcd138aae78d47f21ce12b476d1bad380d3d189cfc`.
Its body boundary, signed external-force definition, affine-offset bound,
inequality direction, assigned-versus-physical units, rounding-only allowance,
and distinction from earlier all-sample regression are correct. The report
appropriately limits positive `B_min(0)` and does not infer actual downward
pull, simultaneous failure, or a collapse mechanism.

Four precision edits were requested from root: write the inverse step as
`weighted_mean(R)/(Mg)>=rho`; label the two example columns `B_min(0.25)` and
`B_min(0.50)` because rho names the lower bound; explicitly qualify the NW
example as a triangular-weighted average; and replace the stale statement
that an independent check remains required with the completed exact agreement.
For rigorous integration conditions, the reviewer also recommended requiring
absolutely continuous velocity (which includes twice continuously
differentiable trajectories). These do not change any numerical result.
After root applied those five edits, the reviewer reread the complete assembled
report and checked its SHA256:
`bd8b2d39f2229d8453fb1ea71dd0c8da8b45b58ca4b1fdc7037ecf542e09a44c`.
All five corrections are present. The physical-versus-assigned units,
lower-bound rho convention, rounding-only allowance, three-position statistic,
and instantaneous-force limitations remain explicit and consistent. No blocking
formula, body-boundary, inequality, or claim-scope issue remains in that checked
report version. This is completed computational/methodological and wording
review, not historical measurement validation or qualified engineering approval.
No new calculation or source reread was performed in this final text check.
