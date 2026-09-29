# Synthetic curve arithmetic: bounded implementation record

2026-09-24; frozen after 14:33:28 UTC. Owner `/root/curve_method`.
Research only. **No historical ordinates, image processing, calibration-fidelity
result or human approval is supplied by this unit.**

## Result and authority

Implemented `curve_math.py` and `test_curve_math.py` under the frozen main
CHARTER, unit PROTOCOL, HUMAN-REVIEW-GATE, pre-measurement method review and
Stage 1 NUMERICAL-PROTOCOL. The last contract was read after the original
method-review freeze; it identifies source axis/legend meanings, but no
historical graph, ordinate, fitted curve or numerical historical result was
read by this implementation agent. Source-specific ranges are not hardcoded
in the arithmetic core. Skills used: repository orchestration, evidence
falsification, source-of-truth and development verification.

Only the two new code/test files and this report were changed for this job.
The earlier method-review freeze was not edited. No new source acquisition,
solver, bridge, engine state, raw evidence, main/legal record, publication or
commit/push was involved. No browser/UI behavior changed or was tested.

The final **27 synthetic unit tests passed twice**, with exact hand-expected
values. The initial smaller 25-test version also passed; two controls and
own-domain/support/endpoint outputs were added during contract alignment.
There were no failed unit-test runs. A preliminary read of the then-absent
NUMERICAL-PROTOCOL returned a file-not-found error; the created file was later
read completely. That was a preparation lookup, not a measurement or test
result.

The core is implemented and narrowly verified against these controls, **not
independently accepted**. The parent reviewer will inspect the code and perform
an independently authored oracle check. Same-agent test expectations and
repeat execution do not satisfy that independent-implementation requirement.
Actual human source/mapping spot-check remains unmet. This cannot be used to
strengthen or weaken the historical calibration claim at this stage.

## Exact behavior implemented

- `SupportedBranch(name, support_tag, points)` requires an explicit supported-
  monotone tag, unique nonblank branch names within a curve, at least two
  points and strictly increasing displacement. Input numbers must be exact
  integers or `Fraction` instances. Booleans, all floats including NaN/infinity,
  strings and nulls are rejected; there is no implicit rounding.
- Multiple branches must already be ordered and strictly disjoint. Touching
  branches are deliberately refused as ambiguous by this narrow interface;
  contiguous, genuinely continuous data must be explicitly represented as one
  branch. No automatic join or sorting of a backtracking trace occurs.
- `compare_curves(reference, candidate, x_axis=..., y_axis=...)` intersects
  supported intervals, splits at both curves' knots and exact interior
  difference-zero crossings, and integrates each resulting linear piece.
  Differences are candidate minus reference. Gap intervals contribute nothing
  and remain listed as missing through support/coverage output, not filled.
- Outputs include signed/absolute/squared-difference integrals and means,
  axis-range-normalized means, maximum absolute difference and all maximizing
  points/plateaus, each curve's own/common supported peak and locations, both
  own supports, the joint support, and common/separate terminal ordinates.
  Areas for both curves use exactly the same joint domain. Squared mean is
  supplied exactly; an inexact square root/RMS display is not implemented.
- Coverage is joint interval length divided separately by the nominal overlap
  envelope and the full declared displacement-axis range. The former can be
  one when only a small fraction of the plot is covered; the latter preserves
  that distinction. Empty/endpoint-only overlap is rejected, not agreement.
- Axes require strictly positive ranges and all declared points must lie within
  them. No clipping/extrapolation or model-specific axis warp is performed.
  The generic core accepts its caller's declared axes; source-verified frozen
  historical axis constants still require an outer source-registration guard.
- `ordered_area(..., order_tag=...)` separately preserves point sequence,
  backward displacement and vertical/repeated vertices. It returns a signed
  geometric line integral. A purely vertical path contributes zero area but
  cannot be admitted as a positive-length function domain by the comparison.
- `mn_m_to_nm` multiplies an exact value by exactly `1,000,000`. It is a unit
  conversion, not identification of the quantity as dissipated energy.
- `conditional_pure_dissipation_residual` refuses unknown identities and only
  calculates `E-W` under the explicitly stipulated toy identity. A declaration
  token cannot verify the truth of physical assumptions. The elastic control
  demonstrates that a caller who falsely stipulates that identity receives a
  nonzero conditional residual, not a finding of physical inconsistency.

The comparison returns declared-support extrema, not hidden/clipped true peaks
or physical failure points. Branch tags are caller declarations, not source
authentication. Curve names and model/bolt identity cannot be verified without
the separate source-mapping layer.

## Analytical controls and observed results

All entries below are synthetic, with displacement interval `[0,1]` unless
specified. No entry is a measured NIST value.

| Control | Exact expected and observed result |
|---|---|
| Same `F=d`, different point sampling | Both areas `1/2`; all differences zero. |
| Reference `F=1`, candidate `F=2d` | Both areas `1`; signed difference `0`; absolute difference `1/2`; squared integral `1/3`; split at `d=1/2`. |
| Zero reference, constant candidate `1/10^20` | Finite exact absolute/full-scale metrics; no reference-force division. |
| Triangular height-2 spike, base `[499/1000,501/1000]` | Area `1/500`; squared integral `1/375`; peak at `1/2`, not missed by a sampling grid. |
| Candidate everywhere two below reference | Signed area `-2`, absolute area `2`; negative discrepancy retained. |
| Signed-axis ramps on `[-1,1]` | Signed area `0`, absolute area `2`, squared integral `8/3`. |
| Joint support `[0,2/5]` and `[3/5,1]`, difference one | Compared length and difference area `4/5`; gap is not filled; constant peaks remain two intervals. |
| Shifted/disjoint supports within axis `[0,5]` | Joint `[1,2]` and `[3,4]`; nominal coverage `2/3`, plot coverage `2/5`. |
| Reference continues higher after candidate ends at `3/4` | Common reference peak `3/4`, own peak `1`; separate/common endpoints retained. |
| Ordered elastic out-and-back path | Signed area `0`, not the sorted-function value `1/2`. |
| Ordered `(0,0),(1,1),(1,0),(2,0)` | Area `1/2`; vertical drop not converted to a descending ramp. |
| Repeated ordered vertex | Zero contribution from the repeated segment; other area retained. |
| Elastic loading `F=d` with stored energy | Work `1/2`, dissipation `0`; non-pure-dissipation identity refused. |
| Purely dissipative constant-force toy | Stipulated-identity residual zero; unknown identities refused. |
| Doubled ordinate-axis range | Absolute area unchanged, normalized absolute mean halved and normalized squared mean quartered. This exposes why historical axes must be frozen outside the generic core. |
| Invalid support, duplicate identity, nonfinite/boolean/float inputs, zero/reversed axes, out-of-axis points | All declared negative controls raise `ValueError`; no silent clipping, sorting, gap fill or reference-force epsilon. |

The tests also distinguish a zero crossing already present at a knot from a
new interior crossing; both are integrated correctly. Input rejection of a
duplicate vertex in a monotone function does not prevent its explicit use in
an ordered line integral. These are different input contracts, not inconsistent
arithmetic.

## Commands and reproducibility pins

Working directory for commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison`.

Commands actually executed:

```text
python3 --version
python3 -B -m unittest -v test_curve_math
shasum -a 256 curve_math.py test_curve_math.py NUMERICAL-PROTOCOL.md HUMAN-REVIEW-GATE.md method-review.md
```

Runtime: **Python 3.14.0**, standard library only. Final two unit-suite runs
reported 27 tests, 0 failures/errors, about 0.003s and 0.004s. No bytecode cache
was requested (`-B`). Tests use exact `Fraction` results and no random seed or
external data. A separate read-only `python3 -B -c` call executed the synthetic
constant-versus-ramp comparison twice in the same process and asserted exact
dictionary equality. Its canonical serialized result (sorted keys, compact
JSON, fractions as `str`) had SHA-256
`fdb2140b5133efe65755b19579ab90df8d503f6a1a386033b6433359199e8cb3`.
This repeat is a determinism check, not an independent oracle or two separately
recorded historical runs. The result dictionary was not saved as a historical
artifact.

| Input/code at this freeze | SHA-256 |
|---|---|
| `curve_math.py` | `7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1` |
| `test_curve_math.py` | `f3692c3a27ab101154ea25efb5553f7b2dceea0617f3b1f34e970dd175fbf79d` |
| `NUMERICAL-PROTOCOL.md` | `e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3` |
| `HUMAN-REVIEW-GATE.md` | `2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee` |
| `method-review.md` | `e9ebfb5f000e9c30e04c7e69b57f15164f7baab83e04b06872920cfb7604732e` |

## What is not implemented or accepted

This is **not** completion of the full numerical/historical protocol. Missing:

- Actual human source/mapping spot-check, independent arithmetic oracle and
  independent source registration.
- Raster identity/color/dash/crossing/occlusion extraction, figure registration,
  pixel/stroke/axis uncertainty envelopes and correlated sensitivity bounds.
- Clipped/hidden-support metadata, uncertain extrema intervals and uncertainty-
  qualified terminal comparisons. Exact extrema here belong to the supplied
  toy polylines, not uncertain images.
- Automated proof of model/bolt/source identity and enforcement of a complete
  seven-pair historical batch. This core compares one explicitly supplied pair.
- File/manifest integrity enforcement, mutation/stale-output detection and
  historical run receipts. The pure library reads/writes no source files.
- Actual work-conjugacy or energy-accounting verification; historical cross-
  panel equality remains not admitted. No offsets/factors are fitted.
- Physical validation, a replacement connection law, propagation sensitivity,
  historical-collapse identification or engineering significance thresholds.

The strongest objection to the eventual graph audit remains: exact arithmetic
can faithfully compare the wrong, incompletely recovered or non-comparable
curves. These controls do not answer that objection. The next required check
is an independently authored arithmetic oracle plus actual source-registration
and human review before any historical comparison is accepted. Retain this
record unchanged if a later review finds a defect; document repairs and new
hashes explicitly rather than silently calling this freeze verified.

## Post-freeze addendum: fixed independent oracle integration

2026-09-24, after 14:37:03 UTC. The original code/test hashes and preceding
freeze record remain unchanged. At the parent's subsequent request, added
`compare-math-oracle.py`; this additional adapter file was outside the initial
three-file job but expressly authorized for this follow-up.

Root supplied `math-oracle.rb`, reporting that it had been independently
authored and run before reading the producer implementation/results. The Ruby
oracle uses exact `Rational` linear coefficients and analytical antiderivatives,
not the producer's interpolation or integration functions. I read the complete
frozen oracle after my implementation freeze, did not change it or its expected
cases, and transcribed its existing five cases into this core's explicit-point
API. This adapter is post-freeze integration, not a second independently
authored arithmetic algorithm.

Executed `python3 -B compare-math-oracle.py`: exit 0,
`synthetic_oracle_matches`, **39 exact values matched**. Those are seven values
for each of five comparisons (length, signed/absolute/squared integral, maximum
absolute difference, reference area, candidate area), three ordered-path areas,
and one MN*m-to-N-m conversion. The oracle itself reported 39 passing analytical
assertions. Its elastic-dissipation value is an explicit toy definition, not a
fourth reconstructed ordered-path value or an additional claimed comparison.

The adapter reads only the local pinned code/oracle, launches the frozen Ruby
script with captured stdout/stderr, checks membership and all 39 values, checks
both file hashes before/after, and returns stdout only. It writes no artifacts.
This successful execution had empty child stderr. Negative behavior of the new
adapter's guards was not separately fault-injected; those guards are not claimed
as a tested general mutation-security system.
The queried Ruby runtime was `ruby 2.6.10p210 (2022-04-12 revision 67958)
[universal.arm64e-darwin25]`; the adapter used the Python 3.14.0 runtime above.

This independent check does **not** separately cover peak-location sets,
own-domain peaks, normalized metrics, coverage fractions, all invalid-input
guards, graphical uncertainty or historical source assignment. They retain the
producer control coverage described above, and the human/historical gates
remain unmet. The earlier statement that the oracle was pending describes its
original freeze time; this addendum resolves only the fixed 39-value subset.

| Additional artifact/output | SHA-256 |
|---|---|
| Unchanged independent `math-oracle.rb` | `90afe295b11e179f14ce4286917cd781d1d39700a4916094dafc688915ef9905` |
| New `compare-math-oracle.py` | `c00365822ac899b2c051c6ca0ba1e71d9c2b3f223fb263010a00e9e062472838` |
| Oracle captured stdout in successful adapter execution | `426885fd432a159d3863da4002d40e88cc1924420a5952659d6ca64c27cfd42c` |

Original report freeze SHA-256 before this appended addendum:
`b60a7c2256a756a1af8037dae724b7bd309178314631578f9693c2653305a938`.
