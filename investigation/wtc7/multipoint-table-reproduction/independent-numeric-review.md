# Independent numerical review of printed multipoint tables

Status: independent rational implementation, two deterministic historical
runs and producer cross-comparison passed on 2026-09-19. Research only;
this is arithmetic verification, not independent historical measurement
validation or a new source of case facts.

## Independence and acceptance

I read [PROTOCOL.md](PROTOCOL.md), the investigation charter, repository
controls, and the development-verification and evidence-falsification-auditor
skills. I independently implemented exact rational normal equations without
reading or importing the producer's calculation code/results. Inputs were the
separately source-reviewed [page 47](transcription-independent/table47.json)
and [page 50](transcription-independent/table50.json) transcriptions. Historical
calculation waited for root's reconciliation release and the synthetic pass.
See [implementation freeze](oracle/implementation-freeze.md).

Acceptance requires all 45 fixed windows plus four whole-post-onset contrasts,
both fit families on identical inclusive times, exact memberships and exact
decimal comparison classifications. Producer/oracle coefficient and residual
agreement must be within the unchanged `1e-8` tolerance. Agreement with an
author-reported acceleration is not an acceptance condition.

This independence concerns implementation and arithmetic. Both calculations
share the source tables, declared choices and units; neither independently
authenticates the underlying measurements. I did not re-transcribe the PDF or
inspect original video. The separate source-review receipts supply the table
transcription provenance.

## Method and preserved outputs

[exact_oracle.py](oracle/exact_oracle.py) forms the normal equations using
Python standard-library `Fraction` values, centers time at its exact mean,
and solves with independently implemented Gauss-Jordan elimination. The
acceleration is minus the linear velocity coefficient or minus twice the
quadratic position coefficient. A separate linear-functional solve provides
each observation's acceleration weight; its dot product with the inputs must
exactly equal the fitted acceleration. The conditional display half-width is
exactly `0.005 * sum(abs(weight))`.

Every fit retains its time/source-row membership, values, centered and original
time-basis coefficients, predictions, observed-minus-fit residuals, descriptive
SSE/MSE/R², acceleration, input weights, display interval and overlap result.
Fraction strings control comparison; floating displays and RMSE are presentation
aids. The historical output contains 98 fits, 162 printed-velocity entries
(161 testable centered derivatives and one unsupported endpoint), 75 western
subtractions, both complete offset comparisons, 25 displacement rows and 75
pairwise displacement differences. Scale/clock factors are analytic scenarios.

[run01 results](oracle/run01/results.json) and
[run02 results](oracle/run02/results.json) are byte-identical, SHA-256
`a703e5a5c2ffb5b572b8bb3339a02194b69f7c1da53a383b7be5a8fa9db3c091`.
Both receipts are byte-identical, SHA-256
`d5d7284374455254176ef98e937c473d21082446b42e3a8756a6809d2439848e`;
they bind source, both inputs, protocol, code, tests, reconciliation and results.
New output directories/files use exclusive creation. The initial filesystem
sandbox failure is retained in [failed-run01-sandbox.md](oracle/failed-run01-sandbox.md);
the code remained unchanged for successful runs.

## Independently calculated results

Primary windows are NE 8.0–9.2 s and EC/WC/NW 8.2–10.6 s. The protocol retains
10.8 s in sensitivity but does not label it co-primary. All numbers below are
downward acceleration in the printed assigned units of m/s²; ± bounds concern
independent nearest-hundredth input display rounding only.

| Point | Reported target | Primary velocity fit ± display half-width | Primary position fit ± display half-width |
|---|---:|---:|---:|
| NE | 9.30 | 9.307143 ± 0.010714 | 9.267857 ± 0.059524 |
| EC | 9.79 | 9.780769 ± 0.005769 | 9.929820 ± 0.017483 |
| WC | 9.81 | 10.319780 ± 0.005769 | 10.601149 ± 0.017483 |
| NW | 9.92 | 9.957143 ± 0.005769 | 9.956793 ± 0.017483 |

Comparing these intervals with each printed reported target's own ±0.005
interval, primary velocity fits overlap for NE and EC; primary position fits
overlap only for NE. Other primary differences exceed the stated display
rounding allowance. These facts concern the declared reconstruction windows;
they do not establish the authors' original membership or falsify every
alternative fit method.

| Point | Fixed-grid velocity range | Velocity target overlaps | Fixed-grid position range | Position target overlaps |
|---|---:|---:|---:|---:|
| NE | 8.907143–9.590000 | 2/9 | 9.053571–9.785714 | 3/9 |
| EC | 8.904835–9.881993 | 1/12 | 9.482486–10.178904 | 2/12 |
| WC | 9.723750–10.602727 | 1/12 | 9.907624–10.853521 | 0/12 |
| NW | 9.316923–10.094056 | 1/12 | 9.486951–10.086913 | 2/12 |

All fixed-grid results are retained, including nonmatches. Selecting the one
overlapping WC velocity window would not recover its historical fit mask.
The full-post-onset EC/WC/NW contrasts, which deliberately include later
curvature, yield velocity accelerations 8.474191, 7.285919 and 7.447134; their
same-time position fits yield 9.039391, 7.468761 and 7.726341. The NE contrast
duplicates its primary interval and is retained separately. Window choice and
fit family have consequences much larger than display rounding for several
tracks. These differences do not provide a physical uncertainty distribution.

Of 161 testable centered derivatives, 150 lie within ±0.030 m/s and 11 exceed
it. Exact excess cases are:

| Point | Time (s) | Printed velocity minus centered derivative (m/s) |
|---|---:|---:|
| EC | 10.2 | +0.045 |
| WC | 9.8 | +0.035 |
| WC | 10.8 | +0.045 |
| WC | 11.8 | +0.045 |
| WC | 12.4 | +0.045 |
| WC | 12.6 | +0.040 |
| NW | 11.0 | +0.040 |
| NW | 11.2 | +0.040 |
| NW | 12.0 | +0.040 |
| NW | 12.4 | +0.035 |
| NW | 12.6 | +0.045 |

The first NW printed velocity at −1.0 s lacks a printed preceding position
and is not tested. The 11 failures reject this exact nominal-grid
centered-difference formula plus the stated printing-error model as a
sufficient explanation for those displayed rows. They do not identify the actual software derivative,
underlying timebase, preprocessing, or explanation for the mismatch. The
passing rows establish only row-by-row compatibility, not one feasible
hidden-precision series for the entire table.

All 11 failures have positive residuals while velocities are negative: the
printed descent speeds are slightly smaller in magnitude than this nominal
0.4-second stencil gives. A systematic timebase or processing difference is
a possible explanation for that sign pattern, but no alternative denominator
or processing method was fitted or tested in this review. Any follow-up clock
variant must preserve these original results and its prospective declaration;
even a full compatibility pass would not authenticate the camera clock.

All 75 western raw-minus-reference comparisons fall within ±0.015 in the
assigned position units. The common-offset intersections are [4.32, 4.33]
for center and [8.23, 8.24] for SW; both are nonempty at this pairwise
comparison level. The largest absolute difference between displacements
from each point's own 8.20 s value is exactly 0.28 at 8.60 s, with center
minus SW equal to −0.28. This is a comparison of printed coordinates, not
an uncertainty-qualified rejection of rigidity, a metric perspective
correction, or an independent onset estimate. No western acceleration was
calculated.

## Comparison against the separately frozen producer

Root froze its two historical result files before I inspected them, at
SHA-256 `c78146f9bb596a5c0c8241ae918d43f700c35596131e62af53912f75fd5a5dfd`.
Its implementation was identified as `calculate.py`, SHA-256
`d7bdeee43b7524f5b97edbff23e9636f5f74d2ed91aba31cc186b64a3b1863f2`.
I then wrote [compare_frozen_outputs.py](oracle/compare_frozen_outputs.py),
which reads the frozen JSON outputs and imports neither calculation program.
The comparison script requires both frozen output hashes before proceeding.

[comparison01.json](oracle/comparison01.json) records a pass for 1,959 exact
and 5,088 numerical comparisons. All 98 fit identities, inclusive source-row
memberships, sample values/times, primary labels, and display-overlap flags
match. Maximum absolute differences are:

| Quantity | Maximum difference |
|---|---:|
| Centered coefficients | 2.203 × 10⁻¹³ |
| Observed-minus-fit residuals | 2.118 × 10⁻¹³ |
| Downward acceleration | 4.405 × 10⁻¹³ |
| Acceleration input weights | 9.592 × 10⁻¹⁴ |
| Display-rounding half-width | 1.554 × 10⁻¹⁵ |

Every tested quantity stays below the unchanged `1e-8` tolerance. All 161
centered-derivative residual fractions and compatibility classifications,
the untestable endpoint, 75 western subtraction residual fractions/flags,
both offset sequences/intersections/flags, 25 displacement rows, 75 pairwise
differences, the maximum pairwise magnitude and analytic scale/clock factors
also agree. The reported differences are numerical-implementation differences,
not measurement errors.

Seven separate in-memory corruptions of the producer output were correctly
rejected: coefficient, residual, input weight, membership, overlap flag,
derivative fraction and western subtraction fraction. Those controls altered
temporary objects only; both saved historical outputs remained unchanged.
No oracle code or numerical output was modified after the independent freeze.

## Actual verification

Executed from `oracle/` with Python 3.14.0:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_exact_oracle
PYTHONDONTWRITEBYTECODE=1 python3 exact_oracle.py --output run01 --reconciliation ../reconciliation.json
PYTHONDONTWRITEBYTECODE=1 python3 exact_oracle.py --output run02 --reconciliation ../reconciliation.json
cmp run01/results.json run02/results.json
cmp run01/receipt.json run02/receipt.json
shasum -a 256 exact_oracle.py test_exact_oracle.py ../PROTOCOL.md ../reconciliation.json
shasum -a 256 run01/results.json run02/results.json run01/receipt.json run02/receipt.json
PYTHONDONTWRITEBYTECODE=1 python3 compare_frozen_outputs.py --producer ../run01/results.json --oracle run01/results.json --output comparison01.json
```

All 15 synthetic tests passed. The two historical commands completed with
98 fits each after scoped filesystem permission; both `cmp` checks returned
exit code 0. Hashes match the pre-calculation implementation freeze and the
saved output receipts. No dependency installation, network activity,
browser/UI check, finite-element solver, canonical record edit or source
modification was part of this review.

The scoped `rg -n '[ \t]+$'` check found no trailing whitespace in the three
oracle Python files, two oracle review notes and this review. An explicit
`test -f` loop confirmed all ten linked local targets exist. The worktree-root
`git diff --check -- research/sherlock-wtc7-investigation/multipoint-table-reproduction`
returned exit code 0; because these new unit files are untracked, that Git
result alone does not check their contents, so the separate text check above
is the relevant whitespace evidence.

## Claim strength and disconfirmation

- **Derived, A within the stated arithmetic model:** the exact rational
  results and two-run identity above. A source-token discrepancy, incorrect
  membership, failed independent comparison, or erroneous sign/weight
  derivation would weaken this conclusion; those are explicit verification
  targets.
- **Model-dependent, B for this finite sensitivity set:** acceleration
  depends materially on interval and fit family for several tracks. This is
  visible in the retained ranges; it is not a calibrated confidence interval.
- **Unsupported by this unit:** recovery of the original fit masks or Tracker
  settings, independent source calibration, instantaneous physical onset,
  whole-building center-of-mass acceleration, removed support force, an
  initiating mechanism, intent, or wrongdoing.

The strongest relevant objection to treating a mismatch as a historical
refutation is that the source does not supply the original fitting mask or
derivative settings. A documented historical mask/settings file and original
track export could explain the differences without changing the printed
numbers. Conversely, arithmetic agreement with one selected mask would not
resolve those provenance and physical-inference limitations.

## Separately declared post-result clock diagnostic

The preceding statements that no alternative denominator was tested describe
the original nominal-grid phase. After that phase's outputs and independent
comparison were frozen, root explicitly declared [CLOCK-ADDENDUM.md](CLOCK-ADDENDUM.md),
SHA-256 `198d31a14ca49368bfc00c64ed3d4827d8fea9d7045a4f2a090e75a5ec6a866f`.
This section records that later test. It does not replace the original
derivative test, alter its failures, or recalculate/rescale any of the 98 fits.

The addendum reports a fresh probe of the preserved Camera 2 access copy and
its agreement with previously retained metadata. I did not independently
probe the video; the numerical tests below use only the three explicitly
declared spans. The six-frame nominal tracking step, twelve-frame derivative
span, and historical use of either listed frame rate remain hypotheses.
The access copy's nonuniform presentation intervals and unverified
video-to-table join prevent identifying these rates as an exposure clock.

I independently wrote [clock_oracle.py](oracle/clock_oracle.py), without
reading or importing root's clock diagnostic code/results, and froze it at
SHA-256 `bba5b6a71a4685fdb3e6fe45e1bec7b87b714809d1d64e19ffdccc2faf77585b`.
[clock_test_oracle.py](oracle/clock_test_oracle.py), SHA-256
`618610c1755ba5a9b8abcb2a0f809ff86d92459991f6283097515e0185a2cc06`, passed
six synthetic tests before historical execution. At every candidate span,
known linear-position histories exactly recovered their velocity; signed
extremal display perturbations attained the exact bound, and perturbations
beyond it failed. Translation, support membership and malformed-input tests
also passed. See [clock implementation freeze](oracle/clock-implementation-freeze.md).

For each supported row, the exact bound is `0.010/span + 0.005` m/s.
All 483 row-candidate results are preserved, including the original failures:

| Hypothesized twelve-frame span (s) | Exact display bound (m/s) | Largest absolute residual (m/s) | Incompatible rows |
|---|---:|---:|---:|
| `12/30 = 2/5` | `3/100 = 0.030000` | `9/200 = 0.045000` | 11/161 |
| `12/(30000/1001) = 1001/2500` | `6001/200200 ≈ 0.029975025` | `39/1540 ≈ 0.025324675` | 0/161 |
| `12/(2997/100) = 400/999` | `1199/40000 = 0.029975` | `1013/40000 = 0.025325` | 0/161 |

The unsupported first NW velocity remains unsupported. Both nearby-rate
candidates provide a concrete row-by-row ordinary numerical explanation of
the discrepancy. Their compatibility does not distinguish between them or
identify historical settings, prove a common hidden-precision series exists,
exclude filtering, or validate the original measurements or a collapse
mechanism. In particular the two candidate rates are so close that these
printing comparisons cannot be treated as a historical choice between them.

[Clock result 01](oracle/clock-results01.json) and
[clock result 02](oracle/clock-results02.json) are byte-identical, SHA-256
`2079a1e96f593b2e3520163df687e59e9f6e1c5e4af8edf2f9b672bc869f21ec`.
Each embeds source, independent table, addendum, implementation and synthetic
test hashes. The original oracle result files still have SHA-256
`a703e5a5c2ffb5b572b8bb3339a02194b69f7c1da53a383b7be5a8fa9db3c091`.

Actual commands, from `oracle/`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v clock_test_oracle
PYTHONDONTWRITEBYTECODE=1 python3 clock_oracle.py --output clock-results01.json
PYTHONDONTWRITEBYTECODE=1 python3 clock_oracle.py --output clock-results02.json
cmp clock-results01.json clock-results02.json
shasum -a 256 clock-results01.json clock-results02.json run01/results.json run02/results.json
```

The synthetic command passed six tests in 0.001 seconds; both historical runs
reported 483 row-candidate calculations and the `cmp` check returned exit code
0. Historical outputs were created exclusively under the authorized scoped
worktree permission. At that independent-output freeze, producer clock-output
cross-comparison was still pending.

After the preceding independent freeze, root supplied its frozen clock outputs
at SHA-256 `a625dde21e5767adc60147421afb94084d96842fc9ec7e733706555e80297c87`.
The subsequent comparison is now complete: [clock-comparison01.json](oracle/clock-comparison01.json)
records **3,719 exact comparisons passed**. All 483 candidate/row identities,
nominal times, tested spans, calculated velocities, signed residuals, revised
bounds and compatibility classifications match. Candidate summaries, maximum
absolute residuals and the unsupported NW endpoint also match. Each of the
161 nominal-30fps rows was additionally compared with the unchanged original
oracle result, including the original residual, bound and classification;
all match exactly.

The standalone [clock comparison script](oracle/clock_compare_frozen.py)
requires both frozen clock-output hashes and the original oracle-output hash.
It imports neither calculation program. Six in-memory corruption checks were
correctly rejected: calculated fraction, residual fraction, bound, span,
membership and compatibility flag. Saved source/results files were unchanged.

Actual comparison command from `oracle/`, exit code 0:

```text
PYTHONDONTWRITEBYTECODE=1 python3 clock_compare_frozen.py --producer ../clock-results01.json --oracle clock-results01.json --baseline run01/results.json --output clock-comparison01.json
```

This verifies arithmetic and the new candidate comparison, not historical
timing. The original nominal-span failures and all original acceleration fits
remain the results of their original declared method.

Scoped trailing-whitespace checks passed for the three new clock Python files,
the clock freeze note and this review. All eight newly linked local targets
exist. These are document/implementation hygiene checks, not source validation.
