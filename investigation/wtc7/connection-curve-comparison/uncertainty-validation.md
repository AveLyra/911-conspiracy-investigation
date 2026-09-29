# Local uncertainty: verification and inference limits

2026-09-27. Synthetic mathematical work under the existing main CHARTER.
No historical curve reading, human acceptance, native solver reproduction,
case finding, or accepted Sherlock/Faraday state change.

## Before-outcome declaration and independent expectations

Read the complete PROTOCOL, NUMERICAL-PROTOCOL, HUMAN-REVIEW-GATE,
technical-preparation, REGISTRATION-STAGE and registration-comparison, plus
the full frozen `curve_math.py` and tests. The narrow missing dependency is
local ordinate uncertainty with horizontal-location and shared-calibration
dependence, not another run of the completed raster grid.

An independent method critic reviewed [UNCERTAINTY-STAGE.md](UNCERTAINTY-STAGE.md)
before execution. No blocking mathematical defect was found. Requested
clarifications were incorporated before outcomes: units and vertical orientation,
one uniform hull over a nonzero-width query, exact versus uncertain knots,
unequal per-curve radii rather than one-sided errors, and malformed-input
validation even when another input has unknown identity. The initial stage
hash was `0c9bb4a217830b29572f4a0e0c0476721d553b8c83c867785a1e0c63e3604fbc`;
the execution version is
`38d075e25e6c8352a4f3229736accdf12f40c09e54b6d833036052e92790e34a`.
The change clarifies the model; no result motivated it.

Root authored [32 analytical expectations](uncertainty_oracle.py) without
reading the new producer implementation or its outputs. It imports neither
producer nor original interpolation/optimization code. Hash frozen:
`da9b90eef453975eeddb0c803e64ea9395813a1b54afe2102558b96af0b097b6`.
Twelve local-envelope and twenty pair examples include twenty-five numeric
answers and seven unresolved support/identity answers. A separate reviewer
checked every affine/tent derivation and strict-sign label; all agreed.
The producer was instructed not to read these expectations before freezing
its implementation/tests. Shared contracts and earlier method discussion mean
this is not blinded study design; the examples are synthetic, not evidence.

The prior arithmetic baseline was rerun with the bundled Python3.12.14:
`python3 -B -m unittest -q test_curve_math`, all27 tests passed. Its core and
test hashes remain the previously recorded `7b5a1a3dc4cd822d0e948bdcb6ec5d2793a23bad0744f56dcfcc47980a1300e1`
and `f3692c3a27ab101154ea25efb5553f7b2dceea0617f3b1f34e970dd175fbf79d`.

## Mathematical scope

The shared-t feasibility construction is justified by pairwise intersection
of three closed intervals on the real line. Each segment pair has an affine
objective over its bounded feasible polygon, so extrema occur at vertices,
including degenerate line/point cases. A positive shared ordinate gain is
independent within the stipulated rectangular parameter box, making the
final signed interval product exact for that box. A source-derived feasible
calibration set may be nonrectangular; no historical box is established here.

Precise calculation cannot fix incorrect feature identity or omitted support.
If uncertainty reaches a gap/tail, the contract deliberately returns no
uniform numeric conclusion rather than narrowing the query after seeing it.
An unresolved strict sign includes genuine equality and sign-changing ranges;
it is not a finding of equality. These checks do not validate a joint error
distribution, uncertain knot geometry, integral uncertainty or physical models.

## Execution record

The adapter and [producer record](uncertainty-producer-validation.md) are
complete within this declared synthetic scope. All 32 fixed analytical cases
match: eight numeric and four unresolved local envelopes; seventeen numeric
and three unresolved pair comparisons. All returned strict signs agree.
Unresolved cases are retained outcomes, not failed tests removed from the set.

Examples from the fixed inputs (dimensionless toy coordinates, not case data):

| Question | Exact result under the stipulated model |
|---|---|
| Parallel lines one unit apart, common horizontal shift | Difference [1,1] |
| Same lines with separate local x radii 1 and 2 | Difference [-2,4]; no strict sign |
| A narrow interior peak with both query endpoints at zero | Range [0,7], not [0,0] |
| Query or local radius reaches an unsupported gap/tail | No numeric bound |
| Common vertical offset in [-100,100] | Cancels from the difference |

The producer froze code/tests before executing them or reading the root
oracle. Its first and second focused runs passed all26 tests. Root read the
complete final implementation/tests after the independent oracle freeze.
A separate mathematical/code reviewer checked every-segment-pair vertex
enumeration, degeneracies, common-t witnesses, support refusal, ordinate
expansion and strict signs; no substantive defect was found. That reviewer
also ran26 tests under Python3.14.0, but a concurrent comment-only edit means
its test-file before/after hash was not stable. Do not report that run as a
stable final-edition receipt. Root's final bundled-runtime run is stable.

The sole producer change after initial tests was the wording of a comment:
separately subtracting marginal envelopes is valid but can be non-tight, not
mathematically wrong. No expectation, allowance, threshold or calculation
changed. The initial/final test hashes are preserved in the producer note.

Commands actually run from this unit, using
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(Python3.12.14), abbreviated below as `python3`:

- `python3 -B -m unittest -v test_curve_uncertainty`:26 tests passed.
- Stdout-only `compare_uncertainty_oracle.run()`: all32 expected bounds,
  applicable signs, query/axis/radius/demand metadata and supported-pair
  extremizer witnesses matched. The witness ordinate check uses a separate
  slope/intercept expression, not the producer's interpolation function.
- `python3 -B compare_uncertainty_oracle.py --out uncertainty-check01.json`
  and the same command with `uncertainty-check02.json`: both exit0. Exact
  scoped filesystem permission was obtained for these create-only outputs.
- A subsequent stdout-only replay exactly matched the entire saved JSON;
  both saved receipts are byte-identical. All eight recorded input/code pins
  match before/after and current files.
- `python3 -B -m unittest -q test_curve_math test_curve_uncertainty`:
  all53 tests passed after the final producer comment edit.

The post-freeze [comparison adapter](compare_uncertainty_oracle.py) is not an
independently authored general optimizer. The independence lies in the
pre-frozen analytical expectations and their separate derivation review.
The comparison checks only those examples, not every possible input. The
mathematical argument, code review and focused malformed-input controls
complement that limited coverage; no formal verification claim is made.

Root's initial comparison-adapter invocation failed to import because of a
missing closing parenthesis. No comparison or saved output was produced in
that attempt. The syntax was corrected and the complete checks above ran;
no expected answer was changed. The adjacent26-test command had succeeded
before that import failure. No browser/UI, historical image, package change,
network retrieval or source-data write was involved.

| Artifact | SHA-256 |
|---|---|
| `curve_uncertainty.py` | `e8a01c17388ec62f7d2b71d7a94fda9f9fce7b2515c12344e180cc750c644042` |
| Final `test_curve_uncertainty.py` | `91f1ff251dfbd43e4781c73ff5368ce5d508e21e3da2828a5ba166d27c25c234` |
| `uncertainty_oracle.py` | `da9b90eef453975eeddb0c803e64ea9395813a1b54afe2102558b96af0b097b6` |
| `compare_uncertainty_oracle.py` | `5ea93cc3b460e406ac6a7d226c5092021ef11acd4f2986885796acff7c6ce802` |
| Each [receipt](uncertainty-check01.json) ([repeat](uncertainty-check02.json)) | `7714e0067c4ac1620e12159534aad3a37d25b1a92581a11e690f6d9240c9a621` |
| Producer note | `736e5ba9a50b3eefc74a3d39a9a8f49061eb6461713aecb385bf7e8abe06b18c` |

The receipts record the exact interpreter path/version and source pins, not
a hermetic hash closure over the interpreter and all standard-library files.
The old arithmetic source, human/source gates and prior observations remain
unchanged. No output is a Sherlock acceptance or a physical-model finding.

A final separate verification used bundled Python3.12.14 and independently
checked all eight stored current/before/after pins, both 85,835-byte receipts
and full replay/serialization equality. It confirmed all32 cases and all seven
expected unresolved outputs. Four in-memory alterations (bounds, sign,
calibration identity and infeasible extremizer) each triggered the comparator's
assertion failure, rather than a false pass. An actual attempt to reuse
`--out uncertainty-check01.json` raised `FileExistsError` and exited1; both
saved receipts stayed byte-for-byte unchanged. That was a deliberate negative
control, not a scientific disagreement. No file was edited in this check.

## Claim disposition and next boundary

| Claim | Evidence and strength | Strongest limitation / falsifier |
|---|---|---|
| The implemented bounds match the32 declared examples | Directly established calculation (A) by exact comparison, repeated receipts and separate expectation review | A changed input/code pin or a missed case mismatch would invalidate this scoped claim |
| The algorithm respects the stipulated shared-axis model | Strongly supported (B) by the interval/vertex argument, code review and controls | A supported counterexample, unhandled degeneracy or wrong calibration model would weaken it; no general second optimizer was built |
| The historical spring/shell curves have a robust measured difference | Not established by this stage | Actual source identity, observed support, native graphical uncertainty and human checks are still missing |

This completes the missing local-envelope arithmetic component, not the
complete source-to-measurement pipeline. Unknown graphical error bounds cannot
be replaced by the synthetic radii, and uncertain knot/path shape cannot be
silently represented as exact centerlines. Historical source-native linewidth/
color and support characterization, actual-human axis/legend review, selected
curve-coordinate checks and independent tracing remain unfinished. Shared
anchor uncertainties must be translated into a justified feasible calibration
set; no box has been chosen for the source plots. Integral/peak-location
uncertainty is also outside this adapter. No historical curve comparison or
causal ranking changes, and the full investigation remains active.

The demonstrated shared-versus-local error and missing-support requirements
were deduplicated into the existing SFB-004/SFB-005 covariance feedback item,
using generic synthetic content only. No new software defect, delivery or fix
is claimed; the prior destination-routing question remains unresolved. Final
root checks passed `git diff --check`, direct whitespace/conflict checks on
all ten unit text/code files, their local Markdown links and new navigation
links. Receipt identities and all eight pinned inputs remained unchanged.
Main's preexisting dirty-file list is unchanged. Work remains intentionally
uncommitted in the investigation branch; no protected record was edited.
