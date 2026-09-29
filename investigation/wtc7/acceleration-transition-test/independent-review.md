# Independent acceleration-transition certificate review

September 20, 2026. Reviewer: `next_discriminator`. This initial theorem/code
record is frozen before reading any producer implementation or numerical
result. Main controls, the full charter, the complete current protocol and
its four linked prior method/clock reports were read in this investigation
context. Evidence/source preservation and development-verification skills
govern the work. No new source viewing, media, network, optimizer, structural
solver, main/legal/accepted-engine change or causal ranking is involved.

## Independently derived basis and optimality proof

Let `s=t-tau`, `x=t-6.4`. The verifier uses the piecewise twice-integrated
unit acceleration ramp, rather than the producer's positive-part expression:

```text
D = 0:  G = 0 for s <= 0, otherwise s²/2.
D > 0:  G = 0 for s <= 0;
             s³/(6D) for 0 < s < D;
             s²/2 - Ds/2 + D²/6 for s >= D.
```

The value at D is D²/6 from both sides; the first derivative is D/2 from
both sides; the second derivative is 1 from both sides. At zero the ramp's
value/first derivative/acceleration are zero. These facts follow by integrating
acceleration 0, then s/D, then 1, with continuous position and velocity.
The step case has continuous position/velocity and a discontinuous acceleration.

For each of the 16 observations the independent constraint rows are
`[1,x,G,-1] z <= y` and `[-1,-x,-G,-1] z <= -y`, where
`z=(b,v,a,R)`. Add `[0,0,1,0] z <= 0` and `[0,0,0,-1] z <= 0`.
Thus there are 34 inequalities, with both nonpositive acceleration and
nonnegative residual allowance explicitly enforced.

For any feasible z and nonnegative lambda satisfying
`B^T lambda = -(0,0,0,1)`, multiplying and summing the inequalities gives
`-R <= h^T lambda`, or **`R >= -h^T lambda`**. A feasible saved primal whose
R equals that exact lower bound is globally optimal for this fixed tau,D
linear program. This proof requires no optimizer success flag, floating
tolerance, active-basis correctness, uniqueness assumption or appeal to a
strong-duality theorem. It does not prove optimality between grid onsets.

## Clock-certificate transformation

Use `t'=6.4+alpha*(t-6.4)`, the same transform for tau, and `D'=alpha*D`.
Then `G'=alpha² G`, with `b'=b`, `v'=v/alpha`, `a'=a/alpha²`, `R'=R`.
The residual-row dual multipliers and the `-R<=0` multiplier stay unchanged.
**The multiplier of the normalized final constraint `a'<=0` must instead be
`lambda_a' = alpha² * lambda_a`.** This cancels the alpha² factor in the
residual rows' acceleration column. Its right-hand side is zero, so the dual
objective and all residuals remain unchanged. All three declared factors are
verified by reconstructing the transformed full primal/dual problem.

This multiplier rule was independently sent to root before any producer
results were read. Root subsequently reported that its initial synthetic run
failed at the upward-case clock certificate after 13 completed fits, preserved
that partial output and original code, corrected its multiplier transform,
and reran synthetic controls before historical fits. At this initial freeze
that execution history is **root-reported**, not independently inspected.
The correction changes a coordinate-covariance certificate check, not the
declared fit family, source selection or tolerance.

## Verifier implementation and pre-result checks

`independent_verify.py` uses only standard-library exact `Fraction` arithmetic;
it imports neither producer code nor any optimizer. It reconstructs expected
synthetic values, common historical membership, every inequality, predicted
residual, phase count, extra allowance, grid minimum/tie, boundary flag and
zero-acceleration-witness flag. It checks complete lists of 178 synthetic and
656 historical fits, not a sample. It also independently retains transformed
parameters for every winning onset under all three declared clocks.

The synthetic result schema was clarified by messages before inspection:
`label` values known/line/all_post/outlier/upward/offgrid_step; top-level
`summary` is singular. Historical records have matching label/target keys.
Activity thresholds are not inferred from fitted values: the verifier
permits only the protocol's **three** activity thresholds 1e-7, 1e-6, 1e-5.
Phase boundaries use a partition: for D=0 the single boundary counts only as
at_start, with at_end=0. Summary grid_boundary means a winner at 6.4 or 8.4;
zero_acceleration_winner means at least one saved winning witness has a=0.

Actual pre-result command:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent_verify.py --self-test
```

Exit 0: piecewise boundary/interior/post-ramp and step checks passed; negative
D, missing/duplicate/non-increasing times and inadequate observations rejected;
mutated primal and dual rejected; an exactly singular four-row basis rejected.
An analytic exact-line certificate and a separately constructed certificate
for the protocol's upward synthetic case passed, including all three clock
maps. The upward certificate has a nonzero acceleration-bound multiplier,
so this test exercises the nontrivial dual transformation rather than only
zero-multiplier cases. No historical optimization or new synthetic sweep was
performed. These self-tests do not yet verify producer outputs.

A separate read-only source check confirmed the full common position
intersection is exactly source rows **38–53**, 16 nominal times 6.4–9.4,
and 64 selected position values. Every selected literal time and position
matches the separately frozen root transcription. Expected fit inputs are
constructed from the **independent** transcription. All three source pins
below were freshly rehashed; the PDF was not reopened as pages.

- Independent table SHA-256:
  `fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8`.
- Root table SHA-256:
  `a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc`.
- Published PDF SHA-256:
  `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
- Protocol: 9,639 bytes, SHA-256
  `3d9e0929ae092ac6c167c9e5e01bde4aa0bf2d830230fed79d6fd4547b2c614b`.
- Frozen verifier: 17,854 bytes, SHA-256
  `ec65077b2918b38163f74daed3c5884495d844af211e2535e2f33db3fd77af70`.

## Limits and initial exchange status

Acceptance will establish exact fixed-grid minimax optimality for supplied,
independently checked table values and the declared families, not authenticity
of the source measurements, calibration, physical uncertainty, a unique
acceleration history, instantaneous support loss or cause. Printing allowance
is not total measurement error. Multiple clocks are coordinate transforms
of the same observations. Multiple targets share source/camera dependencies.

A saved optimal parameter vector need not be the only optimal vector. The
minimum R and all tied **grid onsets** can be checked exactly without claiming
unique b/v/a or a confidence interval for tau/D. Positive finite ramps that
fit as well do not prove gradual real-world onset; worse ramp fits do not
exclude other gradual histories. Missing historical calibration cannot be
supplied by a valid LP certificate.

No producer result has been read at this freeze. Later execution, any verifier
failures or schema corrections, result comparison and conclusions must be
added explicitly after this initial record rather than silently rewriting it.

## Post-freeze execution and disposition

This section was appended after exchange. The preceding 7,449 bytes were
frozen with SHA-256
`fbe651a69b6bf5d8597d74e5c621ff3c7ee2f5c76e8dd8284c6400a13820b69c`;
the initial theorem and chronology are not retrospectively rewritten.

**Scoped pass:** the independent checker verifies all 178 corrected synthetic
fits and all 656 historical fits, their exact grid summaries and ties, and
2,502 reconstructed clock-coordinate certificates. The supplemental check
also validates all 834 saved active bases. These are algebraic/record checks
for the declared printed inputs and finite model grid, not validation of the
historical measurements or a determination of physical cause.

### Actual failure, narrow repair, and commands

All commands below ran from this unit under Python 3.13.7, without producer
or optimizer imports. The first post-freeze command was:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent_verify.py --controls controls02.json
```

It exited 1 on the first fit with `ValueError: fraction fields must be strings`.
The producer's `activity_threshold` diagnostic is a JSON number, contrary to
root's earlier overbroad schema description. No historical fit was checked or
output created by that failed invocation. With root's explicit authorization,
the complete initial checker was preserved as `independent_verify-initial.py`;
`cmp` confirmed an exact copy before the live checker changed. The sole repair
was:

```text
fraction(fit['activity_threshold'])
    -> Fraction(str(fit['activity_threshold']))
```

The three-value diagnostic membership guard remains. Every mathematical
input/certificate field still requires a rational string. No source value,
model, inequality, certificate test or acceptance bound changed. Current
checker SHA-256 is
`901ed517cb221e5168397d3c6779e6359785fe9b6b7503bed9c1763224ba9b88`;
the archived initial checker retains the original frozen hash above.

Fresh `--self-test` and then the controls-only command both exited 0. A
separate read-only metadata inspection briefly attempted to subscript
`clock_certificates`, causing `TypeError: 'int' object is not subscriptable`.
The field is the integer count 3, not a stored list. Correcting that inspection
did not change the checker, evidence or mathematical calculations. The checker
independently reconstructs each transformed certificate; it does not accept
that count as proof.

The complete output-producing command was:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent_verify.py --controls controls02.json --historical run01.json --output verification01.json
```

With scoped worktree write authorization, session 87894 reached terminal
exit 0: 178 controls and 656 historical fits verified. The exclusive output
is 73,636 bytes, SHA-256
`a97c87608ba2ecab84f5a3b8b591f09143e6d754b86e0a5c87b16327713d5711`.
Its synthetic and historical clock counts are respectively 534 and 1,968.
No optimization was run by this reviewer.

Negative controls were actual invocations, not descriptions of intended tests:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent_verify.py --controls controls01.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent_verify.py --controls controls02.json --historical run01.json --output verification01.json
```

The first exited 1 with `all 178 synthetic fits required`; the second exited 1
with `FileExistsError`. The existing verification output's hash was unchanged.
Thus neither incomplete controls nor overwriting an existing receipt was
accepted. Expected rejection is not a passing historical fit.

### Supplementary independent record and basis checks

A read-only standard-library inline pass, importing only this independent
checker, exited 0. Its reproducible method was:

1. Read corrected controls and historical JSON, reconstruct each fit's 34
   rows with the independent piecewise basis and exact fractions, and require
   four distinct integer `basis_indices` within 0–33. Apply exact row
   elimination to those four coefficient rows, require rank four, require
   equality of all four constraints at the saved primal, and require every
   nonzero dual entry to have its index in that basis. All **834** pass.
2. Rehash each stored producer input path and compare with both before/after
   pins. Require exactly the three declared clock factors, per-fit clock
   count 3 and nonnegative integer iteration diagnostics. This checks saved
   diagnostic structure, not independently reproduced optimizer iteration
   counts or complete dependency binaries.
3. Compare all historical `source_data` literal and rational times/positions
   and row IDs with the independent transcription: **16 rows, 64 positions,
   rows 38–53**, all matching. Confirm full fit order/membership and all
   recomputed summary fields in the saved independent verification.
4. Read initial controls without accepting them as a full run. Require
   incomplete status, exactly 13 fits, and equality to the first 13 fits of
   corrected controls. Rehash archived `calculate-initial.py` and compare
   to the initial recorded `calculate.py` pin; require initial recorded
   before/after pins to match. All pass.
5. Rehash the nine monitored protocol/code/control/result artifacts before
   and after that read-only pass. All are unchanged.

The initial producer failure is therefore now independently inspected, not
merely root-reported. `controls01.json` is 26,022 bytes with SHA-256
`7754956547fb932decada3add158eee9b24f80124b0c39b0cc7ce4eca5aea133`.
Its traceback reaches the upward synthetic fit's transformed-clock assertion.
The preserved initial source is 12,789 bytes, SHA-256
`a416f9386895638779c5d419333c7277ea58c9fc181ec6a2dec272d9a9af3eae`.
`diff -u calculate-initial.py calculate.py` returned the expected exit 1 for
differences: the acceleration-bound dual multiplier scaling and explicit
boundary velocity/acceleration control checks/counter. No model, source,
grid or tolerance change appeared in that diff.

The corrected source is 13,056 bytes, SHA-256
`94e53d45b979765526b6ff12bcf6a5064f0ebb96b04ec462d401fd5eadd2042b`.
Corrected controls are 376,830 bytes, SHA-256
`262c9433261a8dea030825a1ca304797ec743a2fe4fb9eccf440e1ed1e1e677b`.
Historical `run01.json` is 1,385,468 bytes, SHA-256
`879700371bc35bdb302ef98dbe8db35fdab8efa358633e702331ea99fb1f1d62`.

After root reported the second optimizer run, this reviewer independently ran
`shasum -a 256 run01.json run02.json` and `cmp run01.json run02.json`.
Both hashes equal the historical hash above; `cmp` exited 0. This confirms
identical saved output, not this reviewer's witnessing or rerunning the
optimization. Root's separate read-only replay of the independent checker
is recorded in execution.md and remains root-attributed here.

### Findings and final text review

All 16 target/duration grid minima exceed the printing allowance 1/200;
therefore no one of the 656 declared historical candidates is
printing-compatible. This rejects only a rounding-only fit within this
restricted model/grid. It neither estimates total error nor attributes the
misfit to tracking, deformation, processing, calibration or any mechanism.

NE, WC and NW favor the step on this grid; EC favors the longest tested
ramp. Each minimum has one grid onset, away from the onset-grid endpoints.
Those facts do not establish unique nuisance parameters or an optimum over
continuous onset/duration. In the known abrupt off-grid synthetic case, the
0.2 and 0.4 ramps both outperform the sampled step grid. For example, exact
step R is 353/11100 and 0.2-ramp R is 705311/24546600. This is a verified
grid-identifiability counterexample, not evidence that the historical
transition was gradual.

I read report.md and execution.md completely after the output checks. Text
review pins were respectively
`26409562c2f99ac478284f8854f676c17029a113af4f7bcd889c14953cb30788`
and `8a953d1a20681c947995f51e6b37e98804ae87aee65f438256fb42e46d50fbf8`.
A fresh read-only numerical inspection checked all 16 displayed minima and
extra allowances, the stated best onsets, the short-ramp phase counts, and
the approximate -7.9 to -12.0 assigned acceleration range. They agree with
the already independently certified saved fits. The report appropriately
labels units as author-assigned, printing precision as distinct from
measurement uncertainty, four points as source-dependent, and clock maps as
coordinate checks. It does not promote a curve fit to a cause ranking or
claim continuous-onset optimality. No material overclaim was found within
that reviewed text version.

The strongest relevant objection to a stronger abruptness inference is that
the small step/short-ramp central-value differences lack a demonstrated
stability result over even the printing intervals, let alone independently
grounded measurement uncertainty. Conversely, these calculations do not
disprove abruptness: three pointwise grid minima favor it and the model
families are deliberately narrow. No new image annotation, physical support
history, event authenticity, statistical probability or all-charter
completion follows from this scoped pass.
