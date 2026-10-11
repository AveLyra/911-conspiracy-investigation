# Version 2: independent implementation review

2026-10-04 UTC. Reviewer `/root/one_pixel_check`.

**No material blocking implementation defect found in the pinned wrappers.**
The code is adequate for the declared bounded schedule, conditional on the
root's independent fresh control rerun and its normal preflight checks. That
rerun was not yet present when this review was written. This is implementation
review, not media admission, scientific acceptance or permission to widen the
schedule. No historical decoder, image view or score was run by this reviewer.

## What was independently checked

- Read the complete frozen plan, all four wrapper/test files, inherited dense
  implementation and relevant sampler, pilot, numerical-core and guard code.
  The plan hash is
  `e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe`.
- A read-only Python import/assertion check compared configured and original
  modules: all **17 sampler function bodies** and all **16 dense function
  bodies other than the declared gate/method-pins replacements** are unchanged.
  The sampler grammar differs in exactly the one permitted final-summary
  `fps= ?` fragment; the number grammar and other expressions remain unchanged.
  Original sampler/dense files still match their frozen parent hashes.
- Configured sampler receipts identify `sample_v2.py` as code and the original
  sampler as parent. Dense receipts/method pins identify `dense_v2.py`, its
  parent dense code, wrapper tests and inherited dependencies. Retained old
  schema names describe serialization, not a claim of unchanged execution.
- Dense `BASE` still resolves to the unchanged correspondence method, while
  `DENSE` resolves to this version's directory. The original source manifest
  remains hash-fixed. Both new extraction paths are mandatory before scoring;
  old refusal receipts lack the required admission/products and carry different
  code/plan pins. No version-1 products were retroactively admitted or inspected.
- All **nine** declared job specifications point to create-only version-2
  outputs, but the supervisor receives the **parent dense-clip3 directory** for
  cumulative accounting. Four independently supplied undeclared/traversing
  names were refused. Extraction/scoring and aggregation limits match the plan.
- The saved author control run contains **70 passed tests**: sampler 14,
  dense 22, pilot 25 and version-specific 9; no failures, errors, skips or
  changed dependencies. Verified all four group summaries against their logs,
  all **15 dependency hashes**, and the configured synthetic receipt identity.
  The inherited optimized child still uses the old sampler; that limitation is
  expressly disclosed and a separate optimized version-2 refusal is tested.
- Independently called the actual runtime gate on the saved controls: **21
  input pins** passed. Five in-memory negative cases were each refused: stale
  code identity, changed wrapper dependency, stale test identity, wrong test
  population and a failed group. No saved control was changed. The gate also
  requires the fresh, hash-matched 16-test supervisor summary.

## Actual checks and frozen identities

Local reads used `cat`, `sed`, `rg`, and `shasum -a 256`. Two stdout-only
scripts used the bundled Python 3.12 runtime with `-B -`: configuration check
`02098d` and gate/log/hash check `96f204`, both exit **0**. These imported and
inspected code and saved synthetic records only; neither called a historical
execution function. A preliminary `rg` referenced a nonexistent numerical-core
path; the correct path was then taken directly from `pilot.py` and read. This
was a lookup error, not an implementation or verification failure.

| File | SHA-256 |
| --- | --- |
| sample_v2.py | `62603c9ca8a8c5979b8faa00aacfe97a5361e289ae621f9b2c974c13d93084e4` |
| dense_v2.py | `f4c01b825bfd82d41869d9f988f4b10b36af76f1f8ba7c0246d4525883b4783b` |
| run.py | `95ecb9a493486f003881123ffd13d4083ff1b75ec6a0769f37561b8c0e0ebac0` |
| test_v2.py | `2bd62459905821c5a42c090ad5a608ec6634d4cd50096170a7370aa5cf0e83cd` |
| controls01/summary.json | `4dacfe3b7cdee2aa471ef914a4d08e7b877c0a6879227bb452bde49686b474d2` |

## Limits and execution conditions

Use the reviewed `run.py` route, not direct invocation of the sampler bypassing
the wrapper's preflight. Serial order and stopping after a refusal remain
operator responsibilities; the wrapper is not a concurrent-job scheduler.
The strongest residual resource risk remains overshoot between monitor polls
and during shutdown: reserves are not hard disk quotas. Missing receipts or
unresolved cleanup require a stop, as in the prior supervisor review.

The saved 70-test run was audited here, not independently rerun here. Mocked
dense population wiring is not validation of numerical or historical results.
The unchanged first-attempt failure remains separate and refused. A later
successful supervisor or extraction does not establish source authenticity,
fire conditions, causal mechanism, intent or human acceptance.

At root's request, also read the new `verify_scores.py` and its pinned direct-
sum helper. No adapter arithmetic/mask/field-slicing discrepancy was found.
That supplementary verifier checks retained transforms, not whole surfaces,
and shares Pillow/NumPy. Its checks use Python assertions: it must run with
assertions enabled, or explicitly refuse optimized execution, to avoid a false
pass. This condition was sent to root; this review does not claim a historical
verifier run or extend the four-file execution-control pin set above.

Only this review file was authored. No parent implementation, failed record,
annotation, media or control result was edited.

## Addendum: root rerun and optimized-verifier safeguard

2026-10-04 UTC, subsequent to the review above. Its original temporal wording
is retained. **The independent fresh-control-rerun condition is now satisfied.**
Root ran `test_v2.py --output controls-root01` and reported terminal exit 0
(`d573e1`). This reviewer independently checked the saved root records: all
**70 tests** again passed (14 sampler, 22 dense, 25 pilot, 9 version), with no
failures, errors, skips or changed dependencies. All four group summaries and
log hashes match, all 15 frozen dependency hashes still match, and the actual
runtime gate accepts the root controls with 21 input pins. The synthetic
sampler receipt again identifies the wrapper and its correct parent.

The read-only root-record check was tool chunk `9c59a7`, exit 0. Root summary
SHA-256: `1f8e7edea24b1764851c5117ef6189b6c6690d29eb18bd57971da26313e4647d`.
No new control suite or historical job was executed by this reviewer.

The supplementary verifier now has an explicit `if sys.flags.optimize` refusal
before the pinned helper import and all assertions. A separate optimized-mode
**import-only negative check** (`1f6108`, exit 0 for the expected refusal)
confirmed the exact RuntimeError and that neither the helper nor the verifier's
`main` was defined. No historical file, image or score was opened by that check.
The reviewed verifier SHA-256 is
`d3bf3a4ef52063344824bea381d5fb41777546d2846f136f13bffd54dd0325a4`.

These checks clear the stated implementation conditions only. Historical
extraction admission, complete A/B score reconciliation, resource receipts,
independent artifact review and scientific interpretation remain later gates.
