# CBS pilot execution and verification record

2026-10-04 UTC. Working directory for commands below:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
The executable abbreviated as `python3` is exactly
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0. No package installation, browser,
new download, media decoder invocation, external disclosure or legal edit.

## Preparation and fixed versions

The earlier completed eight-item screen supplied two scene leads. Main charter,
source controls, the new protocol, both reference images and the reused kernel
were inspected. The [preparation record](METHOD-NOTES.md) preserves two
pre-score method clarifications, the pre-test ceiling-index correction and
fresh arithmetic checks. The [method critique](method-review.md) conditionally
accepted the pilot before historical scoring. Regions did not change after
their freeze; protocol did not change after critique or score inspection.

| Dependency | SHA-256 |
| --- | --- |
| PROTOCOL.md | 4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa |
| regions.json | 5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694 |
| pilot.py | b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8 |
| test_pilot.py | cffa4d160de892439ef9e1e02ec0994d536812ae46ed6826111b7afad86522ab |
| verify_selected_scores.py | 60f9e76c0f469baa6751407226cc5d7baf4350a298fd6c0f6f42d748cdbe59b7 |
| method-review.md | 6d8c734f5bd3c68599cc4db07100c73841c415e047b980b4cb055b14ad3d293d |
| artifact-review.md | 40b83b2a3637e62af5101c9168311c43bd026642a1c7ae0d60a825d6e5fde642 |

The adapter author ran its 25 synthetic tests in `adapter-controls01`; root
read the complete adapter and tests and separately ran:

```text
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/test_pilot.py --output research/sherlock-wtc7-investigation/cbs-frame-correspondence/adapter-controls-root01
```

Root's session 23385 ended with exit zero (chunk `d5b530`), 25/25 in 1.620 s,
no failures, errors or skips. The author's session 68160 ended with exit zero
(reported chunk `ec1337`), 25/25 in 1.705 s. Root did not poll or restart the
author's session. Both receipts pin the same code and tests. The 39 exclusion
cases, mask/parity handling, strict variance convention, corrected sample
indices, source/product integrity refusals, ties and group separation passed.
The synthetic 108-comparison wiring test deliberately mocks the score producer;
actual historical scoring is the separate run below. Inherited checks were
11/11, 16/16 and 73/73 as recorded in METHOD-NOTES and their saved receipts.

## Historical executions

The following two commands were launched in parallel, sharing read-only inputs
and writing separate create-only directories. Each rechecked source hashes,
stored frame and PTS joins, PNG/RGB identities, controls, protocol and regions
before any score. Inputs were checked again before completion.

```text
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/pilot.py --run pilot01 --controls research/sherlock-wtc7-investigation/cbs-frame-correspondence/adapter-controls-root01/summary.json --protocol-sha256 4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa --regions-sha256 5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/pilot.py --run pilot02 --controls research/sherlock-wtc7-investigation/cbs-frame-correspondence/adapter-controls-root01/summary.json --protocol-sha256 4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa --regions-sha256 5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694
```

| Run | Session and terminal output | Result | Recorded elapsed | Total saved bytes including receipt |
| --- | --- | --- | ---: | ---: |
| pilot01 | 89689; `f887f3` | Completed, exit 0 | 41.552414 s | 21531968 |
| pilot02 | 23404; `1ce9b4` | Completed, exit 0 | 41.864041 s | 21531967 |

No retry or historical failure occurred. Both fit their 240-second and
256-MiB per-run limits. The timer is a signal plus between-operation checks;
the receipts disclose that native calls can delay signal handling. Recorded
elapsed values are not independently calibrated timing measurements.

## Independent checks and actual viewing

The [artifact audit](artifact-review.md) independently reconstructed all 216
retained transform rankings from 108 complete score surfaces, 24 metric groups,
72 near-best sets, validity masks and eight-image shortlist. It rehashed all
39 input pins and found 112 material products byte-identical across repeats.
Its read-only assertion calls exited zero (`6311cc`, `fc1467`). The auditor did
not open image content or recompute historical correlations. Root read that
review and performed a separate check without importing the matcher:

```text
python3 -B research/sherlock-wtc7-investigation/cbs-frame-correspondence/verify_selected_scores.py
```

Exit zero, chunk `91398f`: all 216 retained transforms checked, 347 finite
scores and 85 null decisions reproduced, maximum observed score difference
`6.485922909860165e-13`, below the check's `1e-9` tolerance. This tolerance is a
numerical verification criterion, not a photographic matching threshold. The
checker independently uses direct sums and mask indexing but shares Pillow/
NumPy; it does not independently decode the original video or re-evaluate all
3,651,804 static score cells.

Root also preserved [native observations](root-observations.md) of all eight
shortlisted images, each displayed once at original resolution in clip/index
order. No candidate was omitted, no display failed, and no additional candidate
or transformed image was viewed. Scores were known before those views; this is
not a blind confirmation. Two earlier native reference views were part of
region preparation; the method reviewer separately viewed those two references.
No new human acceptance, camera-original authentication or causal result follows.

## Corrections and completion boundary

The index-rounding and interpolation-exclusion issues were found before scoring,
not repaired by changing the results. One source-path inspection command used
an incorrect `jq` variable scope and exited 5; it produced no evidence output
and was replaced with a plain frame/path listing. An initial documentation patch
contained a nonexistent context line and failed; the corrected patch applied.
Neither changed the frozen protocol, source data, calculations or observations.

The separate synthesis critique required a narrow table-label clarification:
dynamic ranking uses each frame's **best static transform**, not the maximum
over both retained transforms. Root added that wording without changing any
value or leader. This matters because a runner-up static transform can have a
higher dynamic score. The [synthesis critique](synthesis-review.md) retains the
review disposition and exact scope.

After the corrected report's reviewed readback, root also adopted the reviewer's
optional caveat: static leader 188 uses about 87.3 percent static overlap, while
the other three 0.005-near-best frames use effectively full overlap. The saved
result row supplies that value. This is an explicit limit on comparing scores
over different content, not a new computation or changed matching rule.

Final read-only documentation QA exited zero (chunk `400084`): ten fixed pins,
eight authored Markdown documents, fourteen local links, all three Python
files' syntax/whitespace, both navigation entries and both completed receipts
checked. `git diff --check` also exited zero (`7cd8ca`). Final report SHA-256:
`2401308b5d975abaa35ad91b1e8f6337ae078ea2caf4542085d8c4e3afd8c685`.
This report hash includes the expressly recorded post-review optional caveat
and review link; it is not falsely presented as the earlier reviewed hash.

This finishes the bounded pilot, not the full-frame search or full charter.
The next task is a finite extraction/runtime/storage plan for dense comparison,
retaining the existing method and documenting any separately proposed change.
All authored changes stay in the investigation worktree; this work did not
modify main or previous source/observation records. Previous WIP is preserved.
No stage, commit, push, accepted Sherlock/Faraday finding, matrix
save, publication, court-facing promotion or human approval was performed.
