# Root preflight before historical processing

2026-09-19. Read the entire prior helper and frame plan, the new helper and
test suite, including the final hardening changes. New-source acquisition,
container probe and fixed selection precede any historical PNG processing.
This is code/method review, not a human/scientific gate approval.

Pinned final code: sample_sequence.py SHA-256
`c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d`;
test_sample_sequence.py SHA-256
`cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43`.
Manifest21d9595609115deb0ea35a9cd81d8d01c38d92c06716eeb9dc1aa0285acc1867;
plan4c2870ab8775dd4a8b33fdbd59d32fafc2940fb14d7cee6cc19df829ad476297.

The versioned helper uses explicit exceptions rather than bypassable asserts;
validates source identity, exact index order/range and pinned manifest/plan
snapshots; records launch/nonzero status and all streams; treats any probe
stderr byte as a refusal; uses a closed decode-info grammar with semantic
PTS/geometry/SAR/interlace/final-count checks; rehashes sources after success
or refusal where possible; and distinguishes descriptive candidates from
scientific/human acceptance. Unknown messages are not silently discarded.
It preserves failed output rather than overwriting or relabeling old runs.

Root independently ran, from this unit directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_sample_sequence.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-sequence/root-control01
```

Exit0,14 grouped tests passed in0.824seconds. Actual coverage includes exact
synthetic RGB pixels/PTS/SAR and repeat products; malformed indices and source
identity/count; missing/duplicate/boolean PTS and geometry; explicit severity,
probe-only stderr, unknown/info-injected diagnostic and control-character
refusals; showinfo/final-count/path consistency; refusal of existing output;
retained nonzero statuses; optimized-Python negative; pinned execution and
wrong-plan refusal. A grouped test may contain multiple cases:14 is not a count
of independent scientific experiments. The suite uses real synthetic decoding
and mocked failure paths plus retained historical logs, not new historical
decoding. The producer's earlier control01/02 remain untouched.

Limits: the grammar intentionally supports this pinned FFmpeg7.1.1 DV/FFV1-to-PNG
lane, not all media; legitimate new messages will stop for review. Synthetic
FFV1/control and same-build repeats do not validate DV source authenticity or
rule out deterministic errors. Strict structure/diagnostics do not identify
fire extent, temperature, original camera timing or continuity. Root's separate
read-only acquisition check reconciled six catalog identity fields, both local
source hashes/sizes and all64 declared indices. A format-tag-only container
probe for14returned no tags; no inference about editing history follows.

Observable historical acceptance now requires empty probe diagnostics,
declared decoder messages only, correct structural/pixel receipts and repeated
products for each source separately. Any refusal remains excluded until a
separately justified tested change; it cannot be cleared by similarity to a
desired scene. No actual person has approved consequential measurements.
