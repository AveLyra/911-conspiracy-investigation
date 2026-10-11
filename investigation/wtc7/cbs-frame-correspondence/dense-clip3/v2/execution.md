# Clip 3 version 2 execution record

2026-10-04 UTC. Research-only, in the isolated investigation checkout on
`research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. The
[prospective plan](PLAN.md), [method review](method-review.md) and
[implementation review](implementation-review.md) precede historical execution.
The original [refused version](../report.md) and all its bytes remain preserved.
This new execution changes only the specified progress-field grammar and the
explicit adapter/control identities; numerical comparison settings are unchanged.

## Source check and controls

The official FFmpeg 7.1.1 `print_report` implementation uses `fps=%3.*f` with
one decimal below 9.95 and integer precision otherwise. A two-digit integer
therefore has one leading ASCII space. Its value is processing throughput,
not a video presentation timestamp. Root and the method reviewer checked the
[tagged primary source](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/fftools/ffmpeg.c#L577-L602).
No public source or media was newly downloaded into this unit. Only `fps= ?`
replaces the corresponding old fragment; warning, unknown-line, malformed-field,
cardinality, source and frame-join refusals remain active. No failed log was edited.

Commands below abbreviate only the executable as `python3`. Actual binary:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Environment: Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0; saved decoder/probe
version checks require FFmpeg 7.1.1. V2 denotes this document's directory.
All generated historical outputs are create-only, with serial operation.

| Actual check | Command and result |
| --- | --- |
| Root fresh supervisor | From checkout root: `python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/test_guard.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-frame-correspondence/dense-clip3/v2/guard-controls01`; 16/16 passed, terminal 40436, exit 0, chunk `c513a2`. |
| Author V2 controls | From V2: `python3 -B test_v2.py --output controls01`; 14 sampler + 22 dense + 25 pilot + 9 version tests passed, terminal 19136, exit 0, chunk `e05219`. |
| Root independent V2 rerun | From V2: `python3 -B test_v2.py --output controls-root01`; the same 70/70 passed, terminal 23728, exit 0, chunk `d573e1`. |
| Independent implementation checks | Read-only configuration, hashes, logs and refusal checks; actual commands/chunks in the implementation review. The root-rerun acceptance condition was independently satisfied before continued scoring. |
| Supplementary arithmetic checker | Import with assertions enabled passed (`d93818`). Reviewer checked its optimized-mode refusal; actual historical arithmetic run is recorded below only after completion. |

No V2 control attempt failed. Synthetic temporary fixtures are cleaned by their
existing tests; their saved logs and summaries remain. The inherited optimized
sampler child still imports the original module, as explicitly disclosed in
both control summaries. A separate V2 optimized refusal check supplements it.
The pilot's prior 11/16/73 numerical-control records are pinned, not described
as freshly rerun here. Mocked dense population tests are not historical results.

## Frozen identities

| Artifact | SHA-256 |
| --- | --- |
| PLAN.md | e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe |
| manifest.json | fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b |
| sample_v2.py | 62603c9ca8a8c5979b8faa00aacfe97a5361e289ae621f9b2c974c13d93084e4 |
| dense_v2.py | f4c01b825bfd82d41869d9f988f4b10b36af76f1f8ba7c0246d4525883b4783b |
| run.py | 95ecb9a493486f003881123ffd13d4083ff1b75ec6a0769f37561b8c0e0ebac0 |
| test_v2.py | 2bd62459905821c5a42c090ad5a608ec6634d4cd50096170a7370aa5cf0e83cd |
| controls01/summary.json | 4dacfe3b7cdee2aa471ef914a4d08e7b877c0a6879227bb452bde49686b474d2 |
| controls-root01/summary.json | 1f8e7edea24b1764851c5117ef6189b6c6690d29eb18bd57971da26313e4647d |
| guard-controls01/summary.json | 0d40bd204977b6fca43ea4e2253750ebe39fe78ec8320cda542545cda2680b94 |
| verify_scores.py | d3bf3a4ef52063344824bea381d5fb41777546d2846f136f13bffd54dd0325a4 |

Every historical wrapper invocation uses the following arguments from V2;
replace JOB only with the exact names in the actual-execution table below:

```text
python3 -B run.py --job JOB --controls controls-root01/summary.json --pilot-controls controls-root01/pilot-controls/summary.json --plan-sha256 e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe --manifest-sha256 fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b
```

Each `guard-JOB/start.json` and `receipt.json` preserves the actual child
argument array and outcome; `wrapper-end-checks.json` records before/end pins.
The parent dense-clip3 directory remains the cumulative budget, including the
failed original run, controls, logs and new outputs. Limits and reserve risks
are unchanged from the plan. A successful supervisor is not scientific acceptance.

## Actual historical execution

All nine declared historical jobs completed. No partial-chunk score or ranking
was inspected before successful full aggregation. Native shortlist review and
final scientific interpretation are recorded separately from execution success.

| Job | Terminal / final chunk | Supervisor seconds | Job bytes | Actual result |
| --- | --- | ---: | ---: | --- |
| extract01 | 53504 / `141041` | 4.568135750 | 131095110 | Exit 0, clean diagnostics, 189 products checked, source before/after matched. |
| extract02 | 60666 / `69f926` | 4.646532000 | 131095110 | Exit 0, clean diagnostics, same 189 frame records. |
| score-a-01 | 60969 / `c06bae` | 59.426812875 | 41745866 | Exit 0, 189 comparisons, unchanged end pins. |
| score-a-02 | 52425 / `1d5b23` | 62.314855292 | 41836731 | Exit 0, 189 comparisons, unchanged end pins. |
| score-a-03 | 31276 / `b75e96` | 58.954730917 | 41814870 | Exit 0, 189 comparisons, unchanged end pins. |
| score-b-01 | 89057 / `548d60` | 58.251769166 | 41745865 | Exit 0, 189 comparisons, unchanged end pins. |
| score-b-02 | 18895 / `03e45c` | 59.827710375 | 41836730 | Exit 0, 189 comparisons, unchanged end pins. |
| score-b-03 | 70851 / `f48a36` | 59.346213791 | 41814870 | Exit 0, 189 comparisons, unchanged end pins. |
| aggregate-a | 45796 / `b0c038` | 9.983867917 | 2211201 | Exit 0, all 567 repeat comparisons and 27 pilot comparisons equal. |

Root's extraction read-only check (`python3 -B -`, `24aa8b`, exit 0) verified
clean second-run diagnostics, checked structures, all 189 equal indexed rows,
successful supervisor/end-check records and matched source identity. It displayed
no images and did not inspect rankings. Root checked the first score receipt
before starting the next job (`058c12`, exit 0). Subsequent receipt checks were
`c3e676`, `4839aa`, `310a38`, `cbc045`, and all six together `e2b8d1`, each exit 0.
These checks read completion/identity records, not partial rankings. The single
aggregate completed before root read the global results (`f0ae37`, exit 0).
That verbose summary display was truncated; a compact six-group read
(`a8eb79`, exit 0) then supplied all group counts, leaders and declared-set sizes.
No missing portion of that first display is treated as read.

The [separate extraction audit](extraction-review.md) is now complete: 378
new PNG/RGB pairs and nine pilot pairs checked, all 189 repeated rows and nine
pilot joins matched, 460 audited dependencies unchanged. It independently
checked the saved diagnostic streams, metadata and actual arguments, without
decoding again, displaying images or accessing partial scores. The two logs
are not byte-identical; exact differences are runtime addresses, output paths
and processing-throughput fields only. Both passed the same versioned parser.
Root read the complete review after a preliminary file lookup occurred before
the reviewer had saved it; that lookup made no changes. No missing review was
represented as read or as a successful check.

At aggregate completion, the saved supervisor record reports 649,960,399 parent-
lane bytes before its terminal receipt and 10,751,176,704 free bytes afterward.
All jobs stayed below their declared monitored time/byte limits and reserves;
this does not turn polling into a hard quota. Reviews and later small documents
also count toward the unchanged parent-lane budget. There was no historical
failure, automatic retry, output overwrite or deletion in version 2.

## Independent selected-score calculation

Root ran `python3 -B verify_scores.py` from V2 (terminal 89156, final `9f42a0`,
exit 0), with assertions enabled and an explicit optimized-mode refusal.
Three synthetic direct-sum checks passed, followed by all 1134 retained
transforms from all 567 comparisons: **1856 finite scores and 412 null decisions**
reproduced, with maximum difference **6.294964549624638e-14**, below tolerance
1e-9. The [saved stdout quantities and provenance](direct-verification.json)
identify this manual durable transcription and exact checker hash.

This calculation reconstructs native full/even/odd raster preparation, masks,
scale, alignment and valid-overlap selection independently of the matcher and
uses explicit direct sums. It shares Pillow/NumPy and a previously pinned
direct-sum helper. It does not recompute every full-surface cell, authenticate
original-camera custody, supply a new image display or clear a human gate.

## Complete artifact audit and native views

The [artifact reviewer](artifact-review.md) independently reconstructed static
top-two ordering and global best-static/dynamic rankings from the saved
surfaces, masks and complete source joins. Its helper had a pre-execution bug:
it initially required exact equality between FFT-derived and integer-count
coverage fractions. A separate reviewer found the floating-point discrepancy
on synthetic masks; the helper was corrected before historical auditing to
use absolute tolerance 1e-10 for that comparison, preserving exact equality to
saved selected cells and the inherited 1e-7 count gate. No scientific setting,
score or historical admission was changed. The final helper's nine controls
include floating roundoff acceptance and material/nonfinite discrepancy refusal.

Author audit `python3 -B audit_artifacts.py` passed (`e0ce73`, exit 0). Root
fully read the final 368-line helper, independently ran its nine self-tests
(`python3 -B audit_artifacts.py --self-test`, `7be64d`, exit 0), then reran the
complete audit (terminal 97987, final `d0b2e7`, exit 0). Both checked 1674 input
hashes, 189 repeated frame records, 27 pilot joins, 38,343,942 saved score cells
across both passes (29,573,586 finite), 2268 retained transforms, six groups
and eighteen epsilon sets. No failed audit execution occurred. The root audit
reported parent-lane bytes 649,979,775 and free bytes 10,273,214,464. The helper
hash is `3bcc92ea0f6b73d6b7253cbe7733d24b0fb1ff0313d63d05d6854ea1d160cb2b`.

This artifact helper hashes PNG bytes and joins saved RGB identities; the
separate extraction audit performed actual RGB decoding. Its sorted-surface
verification is not correlation recomputation. The direct-sum check above
supplies the separate selected-score arithmetic check. Shared dependencies
and the lack of original-camera authentication remain explicit.

Only after these checks, one tool call displayed the original reference and
the six fixed shortlisted native PNGs once each, in reference/127/128/135/156/
186/187 order, all returned and inspected. The [native observation record](root-observations.md)
contains the nonblind descriptions. No extras or transformed images were
displayed. A post-view file/hash join (`aeda2f`, exit 0) matched all six PNGs.

## Synthesis and documentation verification

The [separate synthesis critique](synthesis-review.md) found no material
correction. Root incorporated its optional clarification that the coverage-
checker repair preceded the first historical **artifact audit**, not scoring.
Root also made the review's multiple-search-opportunity caveat explicit: a
higher maximum after more candidates is not calibrated exact-identity evidence.
Review SHA-256: `4c0a52d9cb89ac31a3f16647f1296afb89e082d8ca366877eb6f5d4689e2be9b`.
The review identifies its exact earlier document hashes; this final review/QA
paragraph and completed-state labels were added afterward, not backdated.

Root's read-only documentation assertions passed (`792e5f`, exit 0): 23 fixed
code/input/output/review pins, nine Markdown files, twenty then-present local
links, six Python syntax/whitespace checks, both fresh 70-test suite receipts,
nine historical completions and both navigation entries. Parent storage/free-
space bounds and absence of a retrofitted version-1 manifest also passed.
Tracked `git diff --check` passed (`148b8e`, exit 0); the separate checks cover
the untracked authored files, not just Git's tracked diff. Subsequent completed-
state verification passed (`e456d4`, exit 0): 27 dependency/output/review pins,
nine Markdown files, all 22 local links, six Python source checks, the fresh
runtime gate and both navigation entries. The final tracked whitespace check
also passed (`a0b67d`, exit 0). This paragraph records those actual results;
it does not change any input, output or interpretation.

A later post-record check (`f6d315`, exit 1) inadvertently expanded link
validation to the entire historical STATUS.md and stopped at the absent
`reference-motion/report.md` target. The same link text is present in HEAD
(`a6dd6b`, exit 0), outside the new section; no missing report was recreated or
silently relinked. This is a retained older navigation limitation, not a pass
for every historical status link. The original current-unit acceptance check
was then rerun on the complete execution record and new status section
(`681aaf`, exit 0): eleven links passed, final record edits were well formed,
and the scientific report hash was unchanged. No scientific result or gate
was weakened to resolve the unrelated historical link.

Generic local parser follow-through is recorded under existing SFB-002, not a
new Sherlock defect/fix or delivered payload. The archived-destination routing
question remains open without blocking local research. The full goal remains
active/incomplete. No original annotation, human approval, main/legal record,
engine-accepted finding, matrix save, external disclosure, stage, commit or push
was changed or created.
