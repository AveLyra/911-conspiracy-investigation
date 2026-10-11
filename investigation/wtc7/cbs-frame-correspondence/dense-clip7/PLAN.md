# Full Clip 7 comparison execution schedule

2026-10-04 UTC. Complete the remaining full-source paired search under the
unchanged [CBS correspondence protocol](../PROTOCOL.md) and
[fixed regions](../regions.json). The main-repository investigation charter
controls; this is descriptive source retrieval, not consequential physical
measurement. Clip 3's completed results, all failed products and every original
annotation remain unchanged. No new historical image or score was examined to
choose this schedule. Existing pilot results and reference familiarity are
disclosed; these are not clean holdouts.

## Inputs and unchanged method

Use only the held Clip 7 source, 140334936 bytes, SHA-256
`a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b`,
at `../../cbs-vince-source-screen/stage4/raw/clip7-attempt1.avi` relative to this
directory. The manifest selects every index **0–1127**, with no exclusions.
The source has 1128 inventoried frames, native 720×480, SAR 8:9, yuv411p and
bottom-field-first metadata; encoded time base 333673/10000000 is not an event
clock. Verify the actual source/inventory again, not merely this declaration.

The paired target is the unchanged full Figure 5-142 JPEG, 706×457, SHA-256
`68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a`.
Use its existing disjoint static/dynamic masks from regions.json. Reuse the
pinned pilot numerical preparation, `comparisons` and `summarize` functions,
and original correlation core. No mask, scale, translation, field representation,
coverage, count, variance or tie rule changes. Full/even/odd candidate arms,
180×120 grid, 13 scales, 51×51 translations and the existing two-stage banner
exclusion remain exact. Dynamic ranking is at each frame's **best static** fit,
not optimized independently or over both retained alternatives.

Use `../dense-clip3/v2/sample_v2.py` unchanged, SHA-256
`62603c9ca8a8c5979b8faa00aacfe97a5361e289ae621f9b2c974c13d93084e4`.
Its parent remains `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d`.
This retains the reviewed zero-or-one ASCII-space progress-field grammar and
all warning, unknown-line, cardinality, PTS and native-product refusals. No
generic normalization, altered decoder command, newly admitted old failure or
additional grammar change is allowed. Identify the actual sampler in receipts.

## Finite serial execution

Create only these new historical products below this directory:

1. `extract01`, then `extract02`, each containing all 1128 indices.
2. `score-a-01` through `score-a-18`, then `score-b-01` through `score-b-18`.
   For chunk k, indices run from 63(k−1) to min(63k−1,1127). The first seventeen
   chunks each have 63 frames/189 comparisons. Chunk 18 is **1071–1127**, with
   57 frames/**171 comparisons**. A uses extract01; B uses extract02.
3. One `aggregate-a`, after all 36 scoring jobs succeed. Reconcile every one of
   the **3384 comparisons per pass**, every saved score/coverage array, all masks,
   all 1128 repeated PNG/RGB/PTS rows, and the nine earlier Clip 7 pilot frames
   at 0,141,282,423,564,705,846,987,1127 plus their 27 paired Figure 5-142 records.

Run **serially**, with no extraction/score/aggregate overlap. A finite batch may
invoke these exact names in order, requiring each child and wrapper's success
before starting the next. No automatic retry, skipped failed job, overwritten
output or deletion. Reentry must use a newly authorized version if an existing
attempt failed; ordinary continuation may start the next unrun declared job only
after inspecting authoritative completed receipts. An observation timeout does
not authorize restarting a live job. Preserve raw subprocess streams.

Do not inspect partial chunk rankings or choose images while scoring continues.
Only the single complete aggregate may form global groups and shortlists.

## Bounded implementation changes

Create a Clip 7-specific adapter derived from the existing dense Clip 3 adapter,
not a new numerical framework. Replace only source/target paths and IDs, count,
the declared chunk population, pilot indices, output lane, explicit limits and
truthful code/test/control identities. Parameter constants are preferable to
scattered literal substitutions. Preserve every applicable verification check,
including complete native metadata, diagnostic reparse, source before/end pins,
repeat disagreement and pilot reconciliation. Pin both new code and inherited
parents; do not label changed execution as an unchanged Clip 3 adapter.

One declared execution-only optimization is permitted for aggregation: collect
the repeated chunk input path/hash maps, reject **any conflicting hash for the
same resolved path**, then hash every unique dependency before accepting those
inputs and again at final recheck. Do not silently discard a conflict, trust an
unverified saved pin, omit a chunk's source identity, or skip final verification.
All numerical surfaces, exact result joins and repeat/pilot comparisons remain.
The reason is explicit: the old collector otherwise performs approximately
81216 repeated PNG dependency hashes across 36 chunks. Test the optimization
with matching duplicates, conflicts and changed underlying bytes. This changes
verification orchestration, not historical or numerical content.

A narrowly parameterized derivative of `../dense-clip3/guard.py` may supply
explicit lane-cap, lane-reserve and free-floor keywords to the same monitor and
receipt. Preserve its original defaults and cleanup semantics so the inherited
16 controls still exercise them. Add tests for the new Clip 7 limits and receipt
truthfulness. No concurrent scheduler is needed. A local runner must enumerate
only the 39 declared jobs, bind the frozen plan/manifest and control pins, and
reject undeclared/traversing names. Freeze code/tests after review and before
historical use. No original code file is modified.

## Resource limits

The **entire new dense-clip7 directory** has an inclusive **3584 MiB** limit,
with **128 MiB reserved**: stop at **3456 MiB**. Count controls, logs, derivatives,
failed attempts and later versions cumulatively; do not reset the budget by
creating another version directory. Earlier Clip 3/source files remain outside
this new lane, preserved, and already consume filesystem space. Keep at least
**4096 MiB free** before and throughout every generated-write job.

| Job | Time ceiling | Output ceiling | Included reserve / stop threshold |
| --- | ---: | ---: | ---: |
| Each extraction | 240 s | 1280 MiB | 64 MiB / 1216 MiB |
| Each scoring chunk | 240 s | 256 MiB | 32 MiB / 224 MiB |
| Single aggregation | 240 s | 64 MiB | 2 MiB / 62 MiB |

Retain 0.1-second monitoring and one-second termination grace. These monitored
ceilings are not hard OS quotas; report actual duration/bytes and any overshoot,
shutdown uncertainty or missing receipt. Stop on a resource or admission refusal;
no enlargement is authorized by this plan. Before controls and generated writes,
check lane/free-space limits. Synthetic temporary fixtures may be cleaned by
their tests, but retain logs and disclose cleanup. Do not remove evidence to fit.

Planning estimates use existing file sizes only, not new image/score inspection.
Nine retained Clip 7 PNGs average 775230 bytes; extrapolating yields about
1.749 GB for two full sets. Scaling Clip 3's complete score-job bytes yields
about 1.497 GB for the two Clip 7 scoring passes, plus aggregation/provenance.
This is plausible within the cap but **depends on compression** and is not a
worst-case guarantee. Raw RGB and uncompressed score/coverage payloads alone
would total roughly 6.00 GB. Actual cap/floor checks control; extrapolating the
nine samples' maximum is not a full-population upper bound. At planning, about
9.27 GB was free; unrelated concurrent disk use can reduce that.

## Controls and observable acceptance

Before historical decoding/scoring, obtain separate method and implementation
review, fresh configured sampler controls, pilot controls and supervisor
controls, plus Clip 7-specific tests. Root independently reruns the material
new suite. Preserve inherited source/function identities and explicitly disclose
any child test that still imports a different module. Retain the optimized
sampler refusal check for the actual V2 wrapper. The final expected test-group
population and code hashes must be frozen before historical execution; passing
zero or skipped tests is not acceptance.

Tests must cover complete 1128-index manifests, all 18 chunk ranges including
the last 57 frames, exact 3384/6768 populations, wrong source/target/PTS/field/
PNG/RGB/missing/duplicate cases, complete 36-chunk reconciliation, late winners,
cross-boundary ties, all-null dynamic groups, nine pilot frames and 27 pilot
comparisons, conflicting/changed dependency pins, stale controls, create-only
outputs and each changed resource boundary. Port applicable dense negative
controls rather than falsely reporting unchanged Clip 3 tests as Clip 7 coverage.
Mocked population wiring is not numerical or historical validation.

After the complete aggregate, independently audit all saved populations,
rankings, masks, coverage decisions, repeat/pilot equalities, source and execution
identities. Root or a separate checker must directly recalculate the retained
scores at all selected transforms with the declared 1e-9 numerical tolerance,
retaining null/coverage decisions. State shared dependencies; saved-array sorting
is not full independent correlation recomputation. Preserve all raw surfaces.

## Interpretation and delivery

Retain all six groups and eighteen 0.005/0.01/0.02 near-best sets; do not pool
arms or count repeats as independent historical observations. After full
aggregation and artifact checks, root may view exactly the union of top-two
static and top-two dynamic indices per arm, **at most twelve** native images,
once each in ascending index order, plus the unchanged full reference once.
No additional neighbors, crops, enhancement, field rendering, audio or newly
selected scoring cues. Record actual views and visibility failures.

Deliver complete results, receipts, source/derivative pins, observations,
separate synthesis critique and a bounded report. Then the declared 1317-frame
paired population will be computationally covered only if both Clip 3 and this
lane actually pass; missing scores remain missing, not excluded exposures.
Candidate retrieval is not exact exposure, original-field identification,
absolute time, physical glazing, fire severity, steel temperature, mechanism
or intent. Unknown report processing, interlacing, obscuration, prior-informed
regions and multiple-search opportunities remain explicit alternatives/limits.

The actual-human consequential-measurement gate and matrix-save permission are
unchanged. Preserve the full charter and other work packages. No new acquisition,
publication, disclosure, main/legal edit, engine acceptance, stage, commit or push.
