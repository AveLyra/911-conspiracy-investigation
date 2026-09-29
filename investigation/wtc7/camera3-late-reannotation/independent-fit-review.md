# Independent dense-annotation fit verification

2026-09-12. Research-only arithmetic and inference-boundary review, not human
image annotation, source authentication, expert engineering review, or a
causal finding. The charter and the frozen PROTOCOL.md control scope.
The evidence-falsification-auditor, source-of-truth-guardian and
development-verification skills informed the separation of verified
arithmetic from observation and physical interpretation.

## Outcome

The independent implementation reproduced every declared fit/comparison
record within prospective tolerances. No numerical discrepancy was found.
The 20 uncomputed windows are genuine retained missing-localization cases,
not failed verification and not interpolated observations.

- [Verifier](verify_fits.py), SHA-256
  `467d2817d51be45c5c6955be687807781c1043ba9658ad4463878745ae69c5cd`.
- [Executed verification receipt](independent-fit-verification01.json), SHA-256
  `b833d877d87eabc302122e7fd8f0b8018fc9d6517fc8bdddcabe459648d72ae6`.
- Producer inputs and all three output products match
  [analysis01/receipt.json](analysis01/receipt.json); full byte counts and hashes
  are recorded in the independent receipt and were unchanged after checking.
- Both annotation JSON and Markdown pins, the protocol, image-preparation
  receipt and saved numeric-only points derivative match the frozen pins.
  The producer code is hash-checked against its receipt, not imported.

Executed from the isolated investigation worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-late-reannotation/verify_fits.py
```

Python 3.13.7; standard library only. First executed verification run ended
with exit 0. One earlier tool-call construction had a JavaScript syntax
error before invoking the file patch, so it wrote nothing and ran no fit.
There was no failed numeric run and no result-driven code adjustment.
The verifier refuses an existing receipt filename; a separate root rerun
can use `--output independent-fit-root01.json`.

## Independence and method

I read the charter, protocol, repository controls and relevant skills;
the frozen observation notes/tables and producer output schema supplied the
inputs. I did **not** read or import analyze.py before implementing and
freezing the independent checker and obtaining its first passing receipt.
Only afterward did I inspect narrowly selected producer rejection and
missing-data gates, identified below. This is an independent implementation
on shared inputs, not independent evidence or a blind historical holdout.
I did not inspect images or reproduce image decoding/correlation here.

For each equal grid, use exact rational
`t=(frame−138)/15`, midpoint `c`, halfspan `h`,
and `u=(t−c)/h`. Writing
`S2=Σu²`, `S4=Σu⁴`, `Y=Σy`, and `U2Y=Σu²y`:

- Linear coefficients: `b0=Y/n`, `b1=Σuy/S2`.
- Quadratic: `b2=(n U2Y−S2 Y)/(n S4−S2²)`,
  `b0=(Y−S2 b2)/n`, with the same `b1`.
- Acceleration coefficient in native px/s²: `2b2/h²`.
- Its weight for point i:
  `wi=2(n ui²−S2)/(h²(n S4−S2²))`.

These symmetry equations are solved using Fraction, not a producer solver
or NumPy. The checker verifies residual orthogonality exactly and confirms
`Σw=0`, `Σwt=0`, and `Σwt²=2`.
Condition numbers are independently reconstructed from the analytic
eigenvalues of the linear/quadratic Gram matrices; only the square roots
and final comparisons use floating arithmetic.

A linear functional on an independent Cartesian product of closed placement
intervals reaches its extrema at sign-selected endpoints. Positive weights
select lower/upper bounds respectively; negative weights reverse them.
The checker calculates these endpoints exactly and checks every retained
interval. A−B uses `[A_low−B_high, A_high−B_low]`, not subtraction of two
lower bounds. Saved-track intervals remain null: unknown, not zero error.

The declared 1e−8 absolute tolerance applies to coefficients, each residual,
weights, conditions, time, acceleration and interval endpoints. The separate
1e−7 SSE tolerance was declared before execution because SSE accumulates
floating residual operations. Actual errors were far smaller; the checker
did not loosen tolerances after seeing results. These tolerances say nothing
about camera clock accuracy, physical scale, or image-localization error.

## Exact coverage and maximum discrepancies

| Covered item | Result |
|---|---:|
| Window records: 3 datasets × 3 series × 23 windows | 207 |
| Computed windows | 187 |
| Uncomputed missing-localization windows | 20 |
| Linear/quadratic coefficient scalars | 935 |
| Individual fitted residual scalars | 4,070 |
| Quadratic acceleration weights | 2,035 |
| Fitted input y scalars | 2,035 |
| Propagated placement-envelope endpoints | 236 |
| Direct A−B versus fitted A minus fitted B exact checks | 59 |
| Frame/feature comparison rows | 44 |
| Localized / unlocalizable observer comparison entries | 84 / 4 |
| Saved x/y decimal-text versus numeric-value checks | 284 |
| Producer control fit objects reproduced in full | 8 |
| Producer interval-control vertices reproduced | 32 |
| Additional independent synthetic control groups | 20 |

There are 23 successful A windows per dataset. Root B and A−B each have
20 successful/3 uncomputed windows; independent B and A−B each have
16 successful/7 uncomputed windows. Saved A/B/A−B each have 23 successful
windows, with no source localization envelopes assumed.

| Quantity | Maximum absolute difference |
|---|---:|
| Coefficients | 1.180e−12 |
| Individual residuals | 9.589e−13 |
| SSE | 2.624e−12 |
| Acceleration, px/s² | 3.257e−12 |
| Acceleration interval endpoints, px/s² | 3.207e−12 |
| Weights | 1.380e−13 |
| Condition numbers | 1.560e−14 |

Displayed maxima above are rounded upward. The receipt retains full
calculated values, all coverage counters, zero verification failures and all
20 uncomputed windows.

Independent synthetic checks include constant, linear and quadratic paths
at 5/9/13/21 points; every impulse weight; position/time-origin shifts;
all 32 vertices of a separately chosen asymmetric five-point interval
example; and rejection of an internal missing value, duplicate time and
nonfinite value. The checker reproduces the producer's full numeric
constant/linear/quadratic, time/position translation, signed-interval and
common-translation differential controls.

## Preserved limitations and small comparison omission

The producer's seventh control group saves only rejection names and reasons,
not attempted arrays. After the independent code and result were frozen,
I inspected analyze.py lines 19–25, 84–111 and 148–180. The recorded source
defines:

- Duplicate-time attempt: t=[0,0,1], y=[1,2,3], intervals=null; the positive
  time-difference gate rejects it as `clock_order`.
- Nonfinite attempt: t=[0,1,2], y=[1,NaN,3], intervals=null; the finite-array
  gate rejects it as `shape_or_finite`. NaN here denotes the source's
  nonfinite test value, not a numeric JSON output.

The source plus producer execution record supports what was attempted;
the two reason strings alone are not complete fixtures. This reviewer
did not import/rerun the producer rejection routine. Independent analogous
rejection checks passed, and the actual 20 missing-data windows were checked
against the frozen annotations, including absence of partial-fit fields.
No frozen producer output was rewritten.

For localized B comparisons, all retained x differences are correctly
`322−saved_track02_x`. The four unlocalizable B observer entries omit x/dx
along with y, although the fixed sample column remains defined. This is a
small traceability omission, not a fit error; the missing y must remain
missing. The known x comparisons are supplied here directly from the pinned
source decimal fields, without filling any y:

| Frame | Unlocalizable observer entries | Saved track02 x | 322−saved x, native px |
|---|---|---:|---:|
| 342 | independent | 323.5313423039055 | −1.5313423039055 |
| 345 | independent | 323.3738103052183 | −1.3738103052183 |
| 348 | root and independent | 323.84640630127996 | −1.84640630127996 |

The source x values were read from the same hash-pinned numeric-only points
derivative used above. The supplement does not make fixed-column B and the
saved moving-x point material-identical.

## Inference audit

The arithmetic reproduction is grade **A** for the stated operations on the
frozen numeric inputs. A physical claim of a uniform building-wide
acceleration or a specific initiating cause remains **D — underdetermined**
by this work alone.

All 41 comparison rows with two numeric y envelopes have overlapping
envelopes; three rows have an unavailable overlap because B is unlocalizable
for at least one observer. These are subjective placement intervals, not
independent probability distributions or evidence of identical true tracks.

As a post-result illustration, the 303–339 interval yields root A−B
2.72228 px/s² with placement envelope approximately [−12.96204,18.40659],
and independent A−B 3.84615 with [−13.43656,21.12887].
Both include zero under the declared Cartesian-product placement model.
The saved difference is 4.35647 with **unknown** placement bounds.
Thus nonzero central coefficients alone do not establish distinct physical
accelerations of material points. Equally, an envelope spanning zero does
not prove rigid motion, common material acceleration or literal free fall.

Common same-frame vertical translation cancels exactly from A−B. The
checker verifies that identity using independently chosen non-polynomial
common shifts in each successful differential window. This rules out pure
common translation as an explanation of the *numeric difference itself*,
not rotation, perspective/depth, changing silhouette, annotation error or
unmeasured camera effects. No stationary-reference result is certified by
this fit audit.

The source and annotation limitations are decisive: B is an Eulerian
outline sample, not a confirmed persistent material point; A is an apparent
geometric corner with unresolved physical calibration. The nominal clock
is conditional. Independent numerical agreement cannot upgrade these
assumptions, supply hidden support forces, authenticate the historical clip,
or identify fire versus deliberate support removal.

Only the verifier, its new receipt, and this review were written in the
isolated research worktree. Preserved sources, earlier protocols/results,
legal records and canonical registries were untouched. No external transfer,
commit/push, accepted Sherlock finding or Faraday execution occurred.
