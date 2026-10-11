# Full Clip 3 correspondence schedule

2026-10-04 UTC. Prospective execution schedule under the unchanged
[CBS correspondence protocol](../PROTOCOL.md). This lane tests every indexed
Clip 3 frame against Figure 5-143. It is source-candidate retrieval, not an
exact-exposure determination, a physical fire measurement, or a cause ranking.
Clip 7 remains in the declared population; this schedule does not authorize
its dense extraction or claim completion of all 1317 frames.

## Fixed method and inputs

The protocol SHA-256 is
`4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa`;
the region file is
`5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694`.
Reuse the unchanged pilot functions, including masks, validity guards, thirteen
scales, translations, three representations, strict coverage/variance gates,
top-two static transforms, and dynamic scores at those static transforms.
The pilot implementation is
`b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8`.
Do not change these choices from dense results.

Clip 3 is the complete held `stage2/raw/clip3-attempt1.avi` in the CBS source
screen, 23,621,148 bytes, SHA-256
`ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d`.
The source manifest contains exactly all integer indices 0 through 188 in
ascending order. The source-index/PTS join must be one-to-one, with PTS equal
to index and time base 333673/10000000. Native geometry is 720 by 480, SAR 8:9,
interlaced, bottom field first. These are encoded metadata, not a certified
camera clock or acquisition history. The reference remains the pinned native
705 by 480 JPEG in the parent protocol.

## Extraction and bounded execution

Use unchanged `../../late-fire-sequence/sample_sequence.py`, SHA-256
`c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d`,
with its exact `late-fire-sequence-v1` manifest and strict diagnostic grammar.
Do not broaden that grammar. Run all 189 selections twice into create-only
`extract01` and `extract02`. Check fresh 14 sampler controls before extraction.
Preserve exact commands, source identity before/after, full probe inventory,
decode diagnostics, PNG and RGB hashes, receipts and failures. Compare every
frame across both extractions, and compare all nine prior pilot selections
against the fresh products. Identical received pixels do not authenticate
historical origin. No download, audio analysis or image viewing occurs here.

The sampler lacks a subprocess timeout. A separately tested external process-
group supervisor therefore watches each extraction or scoring invocation.
It records requested limits and actual elapsed time separately. At a limit
breach it terminates the child process group, waits at most one second, then
kills remaining group members. Polling and shutdown can exceed a requested
threshold; report that deviation, never an exact hard ceiling. Keep interrupted
logs and products, even if the sampler could not finish its own receipt.
The sampler buffers subprocess output in memory; a forced termination may lose
those buffered diagnostics. Mark such an extraction incomplete/refused, never
reconstruct or claim a clean diagnostic record.

| Bound | Declared limit |
| --- | --- |
| Each extraction or scoring invocation | 240 seconds |
| Each extraction or scoring output directory | 256 MiB |
| All new files under this lane, including controls and logs | 1536 MiB |
| Minimum free space before and during an invocation | 4096 MiB |
| Resource polling interval | 0.1 second |
| Automatic retries | None |

Each create-only aggregation invocation has a 60-second and 16-MiB output
limit, with 1 MiB reserved for shutdown/receipts. It remains subject to the
whole-lane 1536-MiB limit, 32-MiB lane reserve and 4096-MiB free-space floor.

Reserve 32 MiB below both byte ceilings for polling/shutdown overshoot and
terminal records; crossing the reserved threshold stops a run. Check whole-lane
size/free space before and during every child run. Extraction/scoring runs are
serial, preventing competing cap monitors from multiplying the allowance.
Before controls or other generated writes check the same lane budget. Controls
and aggregation are small, but their bytes count in the lane total.
No evidence deletion or cap increase is authorized by this schedule.

Estimated conservative storage is about 392 MB for two uncompressed RGB frame
sets plus about 614 MB for uncompressed score/coverage arrays across both
passes, leaving room within 1536 MiB for manifests, tests, logs and reporting.
Actual compressed sizes must be recorded. This is a capacity estimate, not
a promise that every operation fits. A refusal remains a result.

## Scoring and completeness

Before historical scoring, review the adapter, pass fresh parent adapter and
dense-specific controls, verify all input/source/PTS/hash joins, and freeze
code/test pins. The inherited arithmetic controls remain available and pinned;
do not describe them as freshly rerun unless actually rerun in this lane.
Tests cover missing/duplicate/out-of-range indices, false PTS and source/hash
joins, mismatching repeated products, incomplete aggregation, cross-chunk ties,
all-null groups, repeat disagreement, finite caps, and complete population wiring. Mocked wiring checks are
not numerical or historical validation.

| Chunk | Source indices inclusive | Paired comparisons per pass |
| --- | --- | ---: |
| 01 | 0 to 62 | 189 |
| 02 | 63 to 125 | 189 |
| 03 | 126 to 188 | 189 |

Pass A consumes extract01; pass B consumes extract02. Each frame has full,
even-row and odd-row representations against Figure 5-143 only. There are
567 paired comparisons per complete pass, not 567 independent observations.
Retain every score and coverage surface and both selected transforms. Recheck
inputs at use and at completion. Pilot cross-view controls remain preserved
and reported; they are not newly recomputed for all dense frames.

Do not shortlist or report chunk winners as clip-wide winners. Aggregate only
after all three chunks have exact expected keys and completed receipts. Compare
both passes' material score/mask/results products; distinguish run-specific
paths, commands, elapsed time and logs from scientific-product identity.
Reconcile all 27 paired pilot comparison records with their dense counterparts.
Global ranking uses each frame's best static transform, separately by arm and
metric. Preserve all invalid scores, coverage differences, and all three
epsilon sets (0.005, 0.01, 0.02), which are descriptive tolerances, not CIs.

## Review and reporting

Only after complete aggregation and artifact checks, shortlist the union of
top two static and top two dynamic frames for each arm: at most twelve unique
native images. Read that fixed union once in ascending source-index order.
Root may reopen the unchanged complete reference once alongside that review;
record the actual displays, obscured details and contradictory evidence. Do
not crop, enhance, view extra neighbors, inspect chunk winners early, or treat
correlated field-arm agreement as independent corroboration. A second reviewer
checks the synthesis and strongest alternative reading; a separate artifact
audit checks joins, coverage, ranking and reproduction without new image views.

Deliver this frozen schedule, manifest, bounded implementation and controls,
complete extraction/scoring receipts, all results including failures, actual
view record and a reviewed limited report. A dense retrieval success still
does not clear human consequential-measurement, historical source identity,
window-material, event-clock, causal-model, matrix-save or legal-promotion
gates. Original annotations and all previous protocols/results stay unchanged.
No external disclosure, accepted Sherlock/Faraday finding, staging, commit or
push. The full investigation goal remains active and incomplete.
