# Full Clip 3 version 2: independent artifact audit

2026-10-04 UTC. Reviewer `/root/one_pixel_check`.

**Passed the declared artifact-consistency audit.** Both complete passes,
all saved static surfaces, retained-transform ordering, global summaries,
source joins, repeat/pilot comparisons and nine supervisor/end records passed.
This does not establish exact exposure, historical authenticity, physical fire
conditions, collapse mechanism, intent or actual-human acceptance.

## Scope and actual execution

The helper refused access to chunk/aggregate score files until aggregate,
supervisor and wrapper terminal records all reported successful completion.
No chunk scores or rankings were inspected during preparation. After root
reported complete aggregation, the reviewer ran:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B audit_artifacts.py
```

Working directory: this `v2` directory. First complete audit: session **86444**,
terminal chunk **`e0ce73`**, exit **0**. The final helper's prior synthetic-only
run (`--self-test`, chunk **`1a6ec7`**, exit 0) passed nine checks without opening
historical files. The helper has 368 lines, SHA-256
`3bcc92ea0f6b73d6b7253cbe7733d24b0fb1ff0313d63d05d6854ea1d160cb2b`.

The audit read metadata/logs, hashed file bytes and loaded saved numeric arrays.
It did not launch an extractor, matcher, image decoder or viewer. It did not
recompute Pearson correlations from historical images. Source/diagnostic
contracts reuse the configured, pinned implementation; saved-surface sorting,
mask/coverage construction and global ranking/epsilon sets were separately
computed. This is not an independently implemented end-to-end scientific model.

## Verified population and joins

| Check | Verified count |
| --- | ---: |
| Complete source indices per extraction | 189 (0–188) |
| Comparisons per pass | 567 (189 × 3 representations) |
| Saved static score cells across both passes | 38,343,942 |
| Finite cells across both passes | 29,573,586 |
| Retained transforms checked across both passes | 2,268 |
| Null dynamic scores at those transforms | 824 |
| Per-arm/metric global groups | 6 |
| Near-best sets, separately preserved | 18 |
| Identical repeated frame records | 189 |
| Prior pilot frame joins / paired score joins | 9 / 27 |
| Input files hash-checked and rechecked | 1,674 |

All 1,134 surface files have the declared 13 × 51 × 51 score/coverage shape.
Independent sorting over every finite saved cell reproduced both retained
transforms, including the scale/top/left tie rule. The full per-frame results
agree materially across A/B, and their score/coverage arrays agree exactly
(including NaN positions). All six chunk mask sets agree with separately
constructed fixed masks and with the relevant pilot masks. The 27 paired pilot
records and arrays agree with the corresponding full-source results.

Source bytes, declaration copies, wrapper/parent pins, exact commands and
statuses, PTS/metadata joins and configured diagnostic reparsing passed.
Native PNGs were checked by file hashes only. Reliance on saved RGB identities
is explicitly bound to both frame manifests' hash and the separately completed
[extraction pixel audit](extraction-review.md), not described as a new RGB decode.
That review records 387 PNG/RGB checks, including the nine pilot files.

The independently reconstructed global shortlist is exactly **127, 128, 135,
156, 186, 187**. Each representation has 189 finite static frame scores; dynamic
scores at the best static transform are available for 121 even, 121 full and
119 odd frames. Missing values were retained, not replaced by zero. Static
near-best sets within 0.005 contain 46, 53 and 62 frames respectively, showing
that a high static score alone is not unique exposure identification. These
sets are descriptive, not confidence intervals; the three representations
and repeat passes are not independent historical evidence.

## Resource receipts and preserved refusal

All nine supervisor records report completion/return code 0, no unresolved
shutdown/snapshot errors, correct commands and parent-lane accounting. End
checks report no changed dependencies. Measured job-directory sizes match
their receipts.

- Extractions: 131,095,110 bytes each; 4.5681 and 4.6465 seconds.
- Six score jobs: 41,745,865–41,836,731 bytes each; 58.2518–62.3149 seconds.
- Aggregation: 2,211,201 bytes; 9.9839 seconds.
- At audit time the parent lane held **649,972,967 bytes** and free space was
  **10,274,828,288 bytes**. Stored before/after values and all job limits passed.

These are checks of preserved receipts, directory sizes and the reviewed
monitor—not an independent history of every resource poll or a hard quota.
Version 1's refusal receipts and diagnostic log retain their original hashes;
its 189 filenames, 130,737,499 PNG bytes and 131,007,165 total extraction bytes
remain, with no retrofitted `frames.json`. Its PNG contents were not newly
decoded or admitted. No failed run was deleted or rewritten.

## Audit correction disclosed

Before the first historical audit or ranking read, the second reviewer found
that the draft checker wrongly required exact equality between FFT-derived
coverage and direct integer-count fractions. A synthetic probe found 7,676
unequal cells from roundoff, maximum error 3.33e-16. The checker was corrected
before use: absolute tolerance **1e-10**, zero relative tolerance, while retained
`static_overlap` must equal its saved surface cell exactly. Finite-score count
eligibility retains the numerical core's explicit **1e-7 count tolerance**.
Nine synthetic checks then passed. This corrected the audit, not the frozen
method, historical results, thresholds or ranking rules. The first complete
historical artifact-audit invocation passed; no failed historical audit was
discarded.

Root's separately saved [direct verification](direct-verification.json) reports
recomputed scores at all 1,134 retained transforms: 1,856 finite and 412 null
checks, maximum absolute error 6.294964549624638e-14 against 1e-9. That is a
separate root execution, not a second calculation by this reviewer or a
full-surface numerical recomputation.

## Selected pins and remaining boundary

| Artifact | SHA-256 |
| --- | --- |
| aggregate-a/summary.json | `d899cbc6052c8d4fce092cebaaf5adc75f61e4e93005acd0a30b09ea9c122c1f` |
| aggregate-a/results.json | `bbb3c3599f4d4a9a9156b920c91e9c0cf681bc78e40923d19ea7d21a176d9da2` |
| aggregate-a/repeat-results.json | `ac57a7878bd990be43474556570c6bb55d9945f7d8c007b8ab0e0e196b3cedff` |
| aggregate-a/receipt.json | `5562322b7b7682326f06d5f74f5ccdfa888a919bec6c18bc4537f0cf6b7c2008` |
| extraction-review.md | `301a8f00a05ce6dd817fd8ca9fe91dc6a696e34fea4af7e60d958c69394fd206` |
| direct-verification.json | `522cdcf62d91a6a2d92bc90de1b081b735b40b48c5cbe7a6c6b9672182af63f9` |

The artifact gate supports the already declared limited native-image review;
it does not enlarge the permitted shortlist or authorize a physical measurement.
Only Clip 3's 189 frames were completed here. Clip 7, other source-processing
possibilities, consequential human review and the larger investigation remain
open. The frozen representations, geometry, masks and score gates are material
limitations. A bounded candidate retrieval result cannot settle causal rankings.

This reviewer authored only the local audit helper and this review for this
stage. No scientific output, frozen implementation, source, annotation or
earlier record was changed, and nothing was transmitted, staged or committed.
