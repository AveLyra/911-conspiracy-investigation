# Full Clip 7 prospective method review

2026-10-04 05:06 UTC. Separate agent review by the continuing stage-2 visual/method reviewer. This is a review of the saved prospective schedule, not an independent historical source, expert certification, implementation approval or claim that tests have run.

## Disposition

**Conditionally acceptable as written. No material plan correction required.** The plan is logically executable with the declared bounded adapter and supervisor changes. Historical use remains conditional on the plan's implementation review, frozen actual code/test identities, fresh configured controls and independent reruns. The reviewer did not run those controls, decode media, inspect scores, or open any image in this review.

Reviewed pins:

- `PLAN.md`: `0404e0a819e7d8392ad3a320a4cb018ecef02c4d9d3f72337d4b3d1d131f6d70`.
- `manifest.json`: `ece7d7fbae14d3ec043c16eb845d74af617a06854c267b1e686e7b33d4e6e3ad`.
- Parent `PROTOCOL.md`: `4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa`.
- `regions.json`: `5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694`.
- `pilot.py`: `b561aaae16cb1d68f1252f7ca496c6de2fe0407f79219fa096bdd437cd00cee8`.
- Reused V2 sampler: `62603c9ca8a8c5979b8faa00aacfe97a5361e289ae621f9b2c974c13d93084e4`.

## Decisive checks and limitations

1. **Population and source identity are consistent.** A read-only `jq` check returned `indices_exact: true` for the manifest against `[range(0;1128)]`, with one source, count/selection length 1128 and the same source path, SHA and byte count as the unchanged protocol. This checks the declared population, not a fresh decoder inventory. Seventeen 63-frame chunks plus one 57-frame chunk total 1128; chunk 18 is 1071–1127. Three arms yield 3384 comparisons per pass, 6768 across repeats. Two extractions, 36 scoring jobs and one aggregation give 39 serial jobs.

2. **The numerical method is preserved.** Figure 142's native dimensions and masks, representation arms, validity exclusions, transforms, coverage/variance gates and best-static-transform dynamic ranking remain unchanged. Global-only selection after full repeat/pilot reconciliation prevents selecting a preferred chunk winner. Six metric/arm groups and eighteen near-best sets remain descriptive, not confidence intervals. Null groups cannot be silently omitted.

3. **The deduplication is a permissible execution change, not permission to skip verification.** It must merge the complete dependency maps across both passes, canonicalize paths, reject conflicting expected hashes, check each unique dependency before accepting the inputs, and recheck it at the end. Tests must include conflicts between different chunks/passes and changed underlying bytes, not merely duplicate strings. The plan already requires these protections. Actual implementation and receipts must demonstrate them.

4. **Resource feasibility is plausible, not assured.** Serial execution avoids a second scheduler and concurrent owned-process shutdown problem. The 1280 MiB extraction ceiling leaves room above approximately 1115.33 MiB of raw RGB per extraction. Reusing the earlier metadata-only extrapolation with the now-declared 64 MiB aggregation allowance gives approximately 3159–3273 MiB before additional controls/logs/failures, leaving roughly 183–297 MiB to the 3456 MiB lane stop. The sampled maximum is not a population bound. Compression, monitoring overhead and unrelated disk activity can defeat this estimate. The inclusive lane accounting, continuing free-space floor, explicit overshoot reporting and no automatic retry/enlargement are therefore substantive acceptance conditions.

5. **Verification scope must not shrink to the image shortlist.** Direct arithmetic verification means the retained transforms for the full admitted comparison population, not only the at-most-twelve images chosen for viewing. Recalculation of one pass can be described alongside independently established exact repeat equality; neither repeated arrays nor shared Pillow/NumPy dependencies constitute independent historical corroboration. The inherited hard-coded Clip 3 counts, source/target IDs, final-chunk assumptions and resource defaults require configured Clip 7 tests as the plan specifies.

6. **The strongest false-match alternative remains available.** Stable facade/sign geometry and background inside a dynamic mask can correlate across nearby moments. Different object depths, interlacing, unknown report processing and selective visibility can leave a high-scoring candidate without identifying the original exposure. A larger searched population also offers more opportunities for a high maximum. Complete computational coverage cannot establish physical glass state, fire severity, temperatures or collapse cause, and does not satisfy the actual-human consequential-measurement gate.

## Review record and authority

Read the exact plan and manifest, unchanged correspondence protocol and regions, controlling charter, inherited dense adapter, V2 adapter/runner and external guard. Current main AGENTS/WORKFLOW/START-HERE pins match the controls previously read in this continuing review; main and worktree charter both hash to `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`. Repository intake confirmed the investigation branch and existing uncommitted work. Hash checks and the manifest query succeeded. One initial implementation lookup used a wrong subdirectory and failed; the actual parent `dense_clip3.py` was subsequently located and read completely.

The evidence-audit and source-of-truth skills informed the distinction between prospective acceptance, verified execution and historical inference. Prior reference/pilot familiarity and the earlier replacement-reader limitation remain; this is not blind validation. Only this review file was authored. Original code, sources, failures, observations and legal/main records remain untouched by this review.
