# Local uncertainty producer: freeze and focused verification

September 27, 2026. Reused, prior-informed AI producer `curve_render`.
Synthetic method implementation only; no historical curve extraction,
allowance estimation, solver, accepted engine mutation or human acceptance.

Read complete main CHARTER and unit PROTOCOL, NUMERICAL-PROTOCOL,
HUMAN-REVIEW-GATE, current UNCERTAINTY-STAGE and frozen curve_math.py and
test_curve_math.py. The final stage declaration was read after root's
pre-execution clarifications. Repository authority/evidence boundaries and
development-verification discipline kept code verification separate from
scientific acceptance. No root oracle, root expected-value table or upcoming
comparison output was read before or after this producer's freezes/tests.

## Scope and order

The producer wrote only `curve_uncertainty.py`, `test_curve_uncertainty.py`
and this note. The old core, prior raster outputs, source files, gates,
viewer and main/raw/legal records were unchanged. Parent/root owns the
separate analytical oracle, comparison receipts and final integration.

Root cleared synthetic focused execution after method review. Producer code
and tests were fully saved and their SHA-256 sent to root **before** the
first execution, without reading the root oracle. Initial hashes:

- Producer: `e8a01c17388ec62f7d2b71d7a94fda9f9fce7b2515c12344e180cc750c644042`.
- Initial tests: `3e2bfa45f90e8f3a50dc61f1d81c2ac771f3b00ce6f231c6e22c56f4dd86f2bb`.
- Final stage: `38d075e25e6c8352a4f3229736accdf12f40c09e54b6d833036052e92790e34a`.

## Actual execution and correction

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/test_curve_uncertainty.py
```

Bundled Python 3.12.14: **26 tests passed**, exit 0, reported 0.009 s.
No initial test failed and no calculation was changed after this run.

Root's code review requested one comment correction: separate marginal
subtraction `[-3/2,3/2]` is a valid but non-tight enclosure, not a “wrong”
answer; the declared shared-t model has tighter exact extrema `[-1,1]` in
that control. Only the comment changed. Final test SHA-256:
`91f1ff251dfbd43e4781c73ff5368ce5d508e21e3da2828a5ba166d27c25c234`.
The exact command above was rerun: **26 tests passed**, exit 0, 0.009 s.
Producer code SHA stayed unchanged. No test expectation or criterion was
weakened. No browser, image view, network, package installation or historical
input was used. Comparison with root's independent oracle is not claimed by
this producer-only note.

## Computation and controls

`local_envelope` uses both query endpoints and every intervening exact knot,
then expands the y bounds. The entire closed query must be inside one
declared supported branch; missing identity, gaps and tails are unresolved,
not clipped or replaced with zero.

`compare_uncertain` requires an explicit named `SharedAxis`, validates all
parameters and both curves before an unresolved return, retains calibration,
allowances, demanded domains and failure reasons, and computes one uniform
hull over the full query. Each pair of demanded segment rectangles is
intersected with the exact shared-t feasibility strip. All nonparallel
boundary-pair intersections satisfying every halfplane are evaluated, keeping
line/point degeneracies. Returned extremizers include feasible common-t
witnesses. Shared H cancels; common x error generally does not. Unequal
local radii remain separate set-valued allowances, not random errors.

The 26 focused controls exercise flat/slope/negative/rational local envelopes,
point queries, interior narrow peaks, exact support edges, gap crossing,
missing tails, unknown identity, strict positive/negative and zero-touching
signs, shared vertical-offset cancellation, same/different slopes under
shared x error, independent unequal local x/y radii, signed positive-scale
products, degenerate line/point intersections, and invalid/type-confusable
inputs even when the other curve is unresolved. The existing exact
SupportedBranch validation and interpolation are reused, not reimplemented.

Frozen reused core SHA-256:
`7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1`.
Frozen existing test SHA-256:
`f3692c3a27ab101154ea25efb5553f7b2dceea0617f3b1f34e970dd175fbf79d`.
Both were rehashed unchanged after focused execution. The adapter checks the
core source pin before loading. If already imported from the same path, it
reuses that module to preserve class identity; this is not protection against
arbitrary in-process monkeypatching.

These tests establish only the exercised exact toy calculations. The model
assumes exact knots, declared supported centerlines, separate local-error
sets and a rectangular shared-calibration box. It does not estimate any of
those sets from a raster, authenticate curve identity, characterize a general
nonrectangular calibration set, provide a pointwise band at every x, infer
joint attainability across several x, bound integral/peak-location metrics,
or clear the historical source/human gates.
