> **Historical research:** This is a dated computational record, not a new analysis or instruction. Local paths are redacted and omitted dependencies marked; see the [publication note](README.md).

# Additive validation: helper runtime correction

2026-09-11. This records a documentation error found by root after the bounded comparison. No comparison JSON, frozen annotation, plan, baseline configuration or historical product was overwritten to force agreement.

## Preserved failure history

The earlier `independent-comparison-results.md`, SHA-256 `6d089276435a510cb50984f996ed4aba3d99b7ce40ee838b272e8e65be6dd34b`, said: “It was run with Python 3.13.7.” That sentence was incorrect for this annotator's comparison helper. I confused the historical matcher's nested provenance runtime with the helper's own runtime. The note's original comparison-JSON hash was correct; there was no original JSON/hash mismatch.

The original helper commands used bare `python3`. The original and temporary-repeat JSONs both record `3.14.0 (main, Oct  7 2025, 09:34:52) [Clang 17.0.0 (clang-1700.0.13.3)]`. At correction time, bare `python3` reports `/opt/homebrew/opt/python@3.14/bin/python3.14`. The recorded output runtime, not that later path check alone, establishes which version those outputs used. The nested `run_provenance[].initial.python` values instead describe the historical matcher: Python 3.13.7.

| Preserved output | Recorded helper runtime | SHA-256 | Comparison actually checked |
|---|---|---|---|
| [Original](independent-comparison.json) | 3.14.0 | `70f4579bea27fc2f31a31303b22c5e50721b8bd7650f72204532d92bbc872937` | Baseline comparison output. |
| [Agent repeat retained by root](independent-comparison-agent-repeat01.json), originally `[local-path-sha256:82ea5c4092b93c7e3dc4feafbe7f8294731c7544cdeb027e72a7dafba9e612d2]` | 3.14.0 | `70f4579bea27fc2f31a31303b22c5e50721b8bd7650f72204532d92bbc872937` | The temporary file and original were directly compared by `cmp`; correction-time byte equality and recursive structure checks also agree. This is the byte-identical helper rerun. |
| [Root rerun](independent-comparison-root02.json) | 3.13.7 | `83b804897041ca369bfc956e1bf1422ce4347cd8540553beba755202530ee50c` | Recursive comparison finds only `$.python` different. All 120 record objects and all other fields are exactly equal; the full files are not byte-identical. |

The helper source remains SHA-256 `98a430f63db694c027f0be190ac7d1772b8376d2b5843f33bcedae6ae8378636`. The frozen plan, annotations, annotation notes and features hashes were rechecked and remain as previously recorded. Both runtime versions' outputs are retained. No new image viewing, raw decoding, historical matching or additional experimental tests were performed during this correction; only local read-only artifact comparisons and the authorized documentation correction were made.

The claim that all 120 historical match records agree between `run01` and `run02` is distinct from these helper-output comparisons. Re-running a helper that contains this reviewer's visual-coverage statements copies those statements; it does not repeat the visual inspection or provide independent corroboration of it.

Root's retained agent-repeat file was inspected after it was created: it has the hash above and is byte-identical to the still-retained temporary file. The corrected report therefore links a durable repository copy, not just an ephemeral temporary path.

## Root report paragraph review

The manual-comparison paragraphs correctly preserve the 48 nominally localized rows per size, C2-R3's five invalidated feature associations per size, Camera 2 gate counts 23/30 and 25/30, Camera 4's 18 localized accepted and 12 unresolved rejected rows per size, and the prompted/post-output nature of the R3 recheck. Their bounded-sample, non-calibration and non-independent-visual-rerun caveats are warranted. The runtime-only difference should be called a difference between comparison JSON outputs, not evidence of differing historical match results. This review does not independently certify the report's other full-run model statistics or its separate verifier's computations.

The reviewed [root report](report.md), after the terminology correction to “comparison JSON outputs,” has SHA-256 `b5e24f9d6afde46d3157672c056705872406977a7783c3de0b6d95024b95df6c`. The revised runtime paragraph accurately limits reproduction to result fields and explicitly disclaims a repeated or independently validated visual attestation. No further substantive issue was identified in the bounded manual-comparison paragraphs.
