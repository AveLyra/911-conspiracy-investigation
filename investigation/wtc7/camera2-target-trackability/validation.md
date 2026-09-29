# Validation and review record

This closes the bounded Camera 2 appearance-trackability unit, not WP2 or the
full investigation. [Report](report.md) SHA-256
`47986942425df03f36a1ac5cd71ac8c56a08956d6b42658a41e1e913b4932932`
is the reviewed scientific interpretation. Sources and frozen annotations
remain preserved; no conclusion is promoted to the legal record.

## Observation and display coverage

Before their annotation files were released, root and the separate annotator
each viewed all **17 full native images and 17 unmarked coordinate panels**.
Their [root notes](root-annotations.md), [separate notes](annotator-annotations.md)
and [release record](annotation-release.json) preserve exact coverage, source
pins and the stated no-other-new-coordinates-before-save boundary. Shared
definitions, familiar imagery and computational-AI review limit independence.
These are 17 shared source frames, not 68 independent observations of history.
Root also checked the baseline native image and marked proposal when accepting
the definitions. No extra images were opened in the historical calculations
or post-release conceptual review.

The presentation procedure is unchanged at SHA-256
`a4b3ca69b2d8704b9f799bd009136fdac91bd32c5c9227c07a4c906a02f3df5c`.
The two presentation runs have **22 listed products plus a receipt** each,
all 23 corresponding files byte-identical. The saved
[independent presentation check](verification-presentation02.json) reconstructs
all 17 first-copy panels pixel by pixel and verifies the repeated copy.
The two synthetic displays check exact source crop, threefold pixel-cell
replication and all 21 x / 30 y ticks. Ticks indicate cell origins; enlarged
cell centers differ by one display pixel. Neither enlargement nor labels add
historical resolution.

The inherited “no point overlay” footer on the separate **marked baseline
proposal** is inaccurate and remains qualified in [selection](selection.json).
It was not used as an unmarked evaluation panel. The artifact was preserved,
not silently replaced.

## Calculation and independent reproduction

All new runs were made in the [dedicated worktree](WORKTREE-CONTINUATION.md).
Its initial two-package population comprised 252 files that matched the
original checkout byte for byte. Existing absolute source pins remain
read-only dependencies; this is not a portable standalone archive.

| Check | Actual result and scope |
|---|---|
| Producer controls, old `calc-controls01` / `02` | Both preserve 14 passing checks. The first predates the release/snapshot amendment; the second pins the current code at the old location. Neither is relabeled as a new-worktree run. |
| [Current worktree controls03](calc-controls03/receipt.json) | Observed exit 0; 14 checks. Procedure, protocol, contract and executable pins bind this location. |
| [Independent subject02](independent-controls-subject02.json) | Observed exit 0; 18 synthetic checks of current producer functions against independent expectations, before historical annotation inspection by the resumed reviewer. |
| [Independent oracle03](independent-controls-oracle03.json) | 13 no-subject geometry checks and four full-oracle/comparator checks, including five rejected mutations. No historical producer import. |
| [Historical run01](run01/receipt.json), [run02](run02/receipt.json) | Each observed exit 0 after the current-code clearance. Twelve listed products plus a receipt per run; all 13 corresponding files byte-identical. |
| [Independent historical02](verification-historical02.json) | Observed exit 0; all 68 raw rows, 34 analyst comparisons, 34 target-pair rows, 408 map attempts and four first-selected summaries independently reconstructed. |
| [Root independent rerun](verification-root01.json) | Observed exit 0 using the fully read frozen verifier. Repeats four oracle controls and the complete historical arithmetic/128-pin audit. |

Producer SHA-256:
`ac495eecb98845cf5a11cd6d27161cd051ea367cc7cb6a9e186b57329ef10ed6`.
Final verifier SHA-256:
`76a7aa25df5eb86384ef542fddd4ab1fe29e430d6a7fb57a016308aea335a69a`.
The two historical receipts share SHA-256
`1ae4d3bbfc2c8c1d70849a769ed057ea6705bba2c62720322f6c51b90f546d5b`.

The [independent method review](method-review.md) documents exact-rational
subtraction, closed-form two-by-two inverse maps of every corner, analytic
matrix conditioning and a separate supporting-edge hull construction. Status,
row order, annotation and field comparisons are exact; floating arithmetic
uses absolute tolerance 1e-8 and relative tolerance 1e-10. These tolerances
are not observational or physical uncertainty. All 128 combined source,
input, procedure and product pins are rechecked; all 426 saved reference-map
keys are covered without re-fitting. The checker verifies hashes and native
luma geometry, not new visual judgments.

The reviewer also recomputed the report's numerical summaries directly from
its independent reconstructed results. It confirmed the 229/41/138 map
outcomes, hull counts, displacement/correction ranges, zero-inclusive
between-target intervals and all 24 conditional first-selected variants.
Root's separate read-only summary of the producer results agreed to the stated
precision. Software agreement does not establish material identity or a cause.

## Preserved failures and review corrections

- [Presentation01 review failure](verification-presentation01.json): the
  checker incorrectly expected an earlier control's protocol snapshot to equal
  the later amended protocol. Both known versions and their actual recorded
  pins are now checked; no source or presentation was changed.
- The separate annotation comparison's first inline command failed parsing
  before calculating anything; the corrected read-only command succeeded.
  Its [review](annotation-comparison-review.md) records that history.
- [Historical01 review failure](verification-historical01.json): the checker
  initially required an absolute control-receipt key, but the producer retains
  the actual relative CLI spelling. Only the two exact legitimate spellings
  were admitted; no producer, annotation or result changed.
- [Duplicate-run negative](verification-duplicate-run-negative01.json): actual
  historical entry with the same directory twice returned exit 1, as expected,
  before historical reads. It cannot count as two executions.
- The previously recorded frame-7021 small-patch affine cutoff-rounding
  rejection remains rejected in both eligible T1 mapping attempts. No threshold
  tuning or source-map correction was made.
- Worktree initialization and LFS status issues are preserved in the
  [continuation note](WORKTREE-CONTINUATION.md). Adding the navigation file
  initially used an unsupported `sparse-checkout add --no-cone` option; it
  exited 129 without adding that file. The supported `add` syntax succeeded.

A separate read-only conceptual review challenged the initial report's
asymmetric “validates NIST” / “positive evidence” wording and the inclusion of
two necessarily zero baselines among 15 differential rows. Both were corrected:
the same validation/exclusion standard now applies to the mechanisms; 13
later-sample comparisons are distinguished; zero-containing intervals are
explicitly **not proof of equal displacement or symmetry**. The reviewer
confirmed adoption at the final report hash above. It read the report,
protocol/contract and complete annotation comparison, all raw/comparison
summaries and differential rows, all 24 map groups and the T1/frame-6946
admission rows; it opened no images and did not claim independent numerical
reproduction. The follow-up checked the revised report only.

## Commands and remaining limits

From `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, the commands
actually used were the following; output directories/receipts must be **new**
for any future rerun. Existing outputs are never overwritten.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-target-trackability/analyze.py controls --out research/sherlock-wtc7-investigation/camera2-target-trackability/calc-controls03
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-target-trackability/analyze.py analyze --controls research/sherlock-wtc7-investigation/camera2-target-trackability/calc-controls03 --out research/sherlock-wtc7-investigation/camera2-target-trackability/run01
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-target-trackability/analyze.py analyze --controls research/sherlock-wtc7-investigation/camera2-target-trackability/calc-controls03 --out research/sherlock-wtc7-investigation/camera2-target-trackability/run02
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera2-target-trackability/verify_target.py --historical run01 run02 --calculation-controls calc-controls03 --source-root /Users/admin/docs/911 --out research/sherlock-wtc7-investigation/camera2-target-trackability/verification-root01.json
```

Python was 3.13.7, NumPy 2.3.4 and Pillow 12.0.0. No new native decode,
interpolation, target matcher, acceleration fit, simulation, online search,
source acquisition, agency-payload inspection or bridge invocation occurred.
The observations and sparse subjective envelopes remain computational and
appearance-defined; qualified human review, material identity, scale,
projection and source-clock authentication remain unestablished. The full
goal is active. Generic software lessons are deduplicated under the existing
SFB-002/SFB-004 items and retained locally; delivery is not claimed.

## Final local checks

Root checked **eight** touched Markdown documents and **172 local link targets**:
no unresolved targets, trailing whitespace or conflict markers were found.
Because this is a sparse checkout, **104** targets were verified to exist in
the original read-only checkout rather than being populated here. This does
not claim that all navigation links are self-contained in the sparse tree.
The three current Python scripts parsed successfully. Root's and the numerical
reviewer's final verification JSONs are identical after removing their distinct
command fields. Scoped `git diff --check` passed, including the final tracked
edits; the direct Markdown checks also included new/untracked documents.

The original checkout remained at `e8d83d7`; a read-only Git comparison found
no tracked changes in either original Camera 2 package. All new research
changes are confined to the investigation worktree. The canonical record
validator was not rerun in this sparse science checkout, which intentionally
omits the case spines; no canonical-record validation or legal-draft clearance
is claimed. No original source or frozen annotation was changed.
