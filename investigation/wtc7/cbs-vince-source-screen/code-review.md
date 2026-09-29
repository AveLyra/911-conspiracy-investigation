# Nine-target preparation adapter: author check and handoff

2026-09-28. Research-only implementation record. This is the adapter author's
code/self-check, not independent code review, historical execution, image
inspection, model validation or human/scientific acceptance. **Historical use
remains on hold pending root's complete code/test reading, independent review
and the protocol's existing-sampler synthetic-control gate.**

## Authority and scope

Current main AGENTS.md, WORKFLOW.md, START-HERE.md and complete investigation
CHARTER control. The new [protocol](PROTOCOL.md) was read completely, including
its SAR/interlace and immutable reference-landmark clarifications. Its reviewed
SHA-256 is `5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc`.
The existing sampler and its tests were read completely before implementation.
Repository intake returned branch `research/sherlock-wtc7-investigation`,
183 existing working-tree entries, exit0 (chunk381063). No WIP was reverted.

Owned authored files only: [adapter](prepare_samples.py),
[synthetic tests](test_prepare_samples.py), and this note. Generated synthetic
fixtures/receipts stay in new `adapter-controls01` and `adapter-controls02`.
Old code, source media, reference JPEGs, root acquisition records and protected
main/raw/legal material were not changed. No historical file or image was
opened, probed, decoded or viewed by this adapter author.

## Minimal contract

The input is an explicitly declared, hash-pinned JSON object with exactly
`schema`, `stage`, and `sources`. Schema is `cbs-vince-input-v1`. Stages1–4
respectively require clip pairs1–2,3–4,5–6,7–8 in ascending order. Each of the
two source objects has exactly `id`, `clip_number`, `path`, `sha256`, and
`bytes`. IDs are safe lower-case sampler identifiers; paths are absolute,
non-traversing, regular non-symlink files. The path and source identities must
come from actual acquisition records, not guessed filenames or placeholder
hashes. No historical manifest was created during this implementation.

The adapter does not download, validate provider identity or establish camera
custody. Root must join this declaration to the fixed eight catalogue IDs and
acquisition receipts. Operational sampler IDs are not provider IDs. Equal
content or a shared source family is not independent corroboration.

For each stage it:

1. Creates a new output directory, verifies and saves immutable snapshots of
   the caller-pinned manifest and protocol, and pins its code, the reviewed
   helper, Python executable and probe executable.
2. Uses the unchanged helper's command/status recorder for the FFprobe7.1.1
   version check, a complete container/stream metadata probe, and a selected
   `v:0` complete frame inventory. Commands, raw stdout/stderr and numeric or
   launch-failure status are preserved. Any probe stderr byte is a refusal;
   no diagnostic vocabulary was extended.
3. Refuses unknown container/selected-codec lanes before the frame probe.
   The preflight recognizes only the existing AVI DV/yuv411p and synthetic
   AVI FFV1/bgr0 lanes. This preliminary format check does not certify that
   the eventual strict decode diagnostic grammar will accept every message.
4. Requires nonempty strictly increasing integer PTS, constant positive native
   geometry, a positive rational time base, consistent stream identity/pixel
   format/SAR and explicit valid interlace flags. Reported header/read counts,
   when present and not `N/A`, must equal the full frame-inventory count.
   Missing/`N/A` header counts remain unknown; the inventory determines count.
   Full probe output retains any other color/container metadata without
   inventing missing values or applying a transform.
5. Computes `p0 + j*(pL-p0)/8` using `Fraction`, for all nine `j=0..8`.
   Each target selects the first PTS at or after it. The target table retains
   every target, its exact rational PTS/seconds, chosen index and chosen PTS/
   seconds; the extraction index list is the sorted distinct set. A one-frame
   clip thus has nine target rows but only one extraction/observation index.
6. Checks source identity before/after each clip and again before issuing the
   full-stage manifest; checks declaration/code/environment pins after the
   stage. Failed clip receipts persist, including successful earlier clip
   preparation, but a partly refused stage gets no sampling manifest.
7. Emits `sampling-manifest.json` in the unchanged sampler's
   `late-fire-sequence-v1` schema and a separate `selection-targets.json`.
   The only successful status is `prepared_not_executed`. Every receipt
   retains `scientific_or_human_acceptance:false`.

An existing output directory is refused without writing into it. An import-time
helper-pin mismatch likewise refuses before execution. After an output directory
is created, ordinary caught preparation/probe failures preserve its receipt and
available raw command records. This is not a guarantee against process killing,
disk failure or concurrent filesystem interference. The existing command helper
has no added subprocess timeout; do not restart a still-running command merely
because a caller's polling window expires.

## Existing extraction route and limits

No new extraction implementation or historical executor call was added. After
the required reviews, root can pass the generated manifest and its hash plus
the fixed protocol/hash to the unchanged `late-fire-sequence/sample_sequence.py`
executor twice, using two fresh output directories. Its preexisting strict
probe/decode diagnostics, native RGB outputs, exact PTS/geometry/SAR/interlace
joins and PNG/pixel checks remain in force. Any refusal requires diagnosis;
this adapter does not relax it. The source's SAR/interlace may limit visual
inference even when the stored raster and encoded PTS are faithfully preserved.

This author did not rerun the older sampler's test module: it includes separate
saved-log and actual synthetic-video controls whose fresh execution is root's
declared prerequisite. The new adapter tests below use only generated fake file
bytes and mocked FFprobe responses. Passing them verifies preparation logic,
not actual codec compatibility, optical fidelity or historical scene identity.

## Actual synthetic checks

Both commands used the bundled Python3.12 runtime, `-B`, and scoped permission
to create only new synthetic-output directories in this worktree. No server,
network, historical probe/decode or source image display was started.

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_prepare_samples.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/adapter-controls01
```

Exit0, chunkd06d36:23 tests,0 failures,0 errors. The first passing adapter/test
pins remain in that directory's `test-results.json`; no output was overwritten.
Before any historical use, a stricter known-format preflight and two tests were
added to refuse unsupported container/codec formats before the frame probe and
retain the existing synthetic FFV1 lane.

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B test_prepare_samples.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/cbs-vince-source-screen/adapter-controls02
```

Exit0, chunk929db9:25 tests,0 failures,0 errors. Coverage includes irregular
and exact-hit rational targets; short/one-frame and negative-PTS clips;
deduplicated indices with nine retained targets; duplicate/nonmonotonic/
missing/bad PTS; geometry, time-base, native metadata and count failures;
invalid stages/order/IDs/paths/size/hash/schema; duplicate/nonfinite JSON;
existing-executor manifest compatibility; wrong source hashes/sizes; any
probe diagnostic byte; nonzero and launch failures; malformed raw inventory;
source mutation both during and after its own probe; existing-output refusal;
manifest/protocol/helper pins; version and partial-stage refusal; and a changed
declaration during probing. Failure-path fixture receipts and streams are kept.

Final code/test pins, also recorded by the final test run:

- Adapter: `5992d2a95be2dd8587a13980a7c05b363bd9760d24dc9768c345a3733049bb87`.
- Tests: `484d1f391b3d4e0bf0116fa35e6f2f20bd264c0098b255a1b59dff0d27e74c55`.
- Unchanged helper: `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d`.
- Unchanged old tests: `cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43`.

No historical clearance, human acceptance or cause ranking is implied. Root's
complete reading/repetition and the separate review remain outstanding at this
handoff; the latest coordinate-only request does not authorize beginning the
new historical stage.

## Freeze coordination update

After the author checks above, root reported reading the complete final adapter,
tests and unchanged parent implementation/tests, finding no blocking defect.
Root also reported14 parent controls passed in `controls-parent01`; this author
did not rerun or independently inspect that receipt. Root's fresh repetition of
the final25 adapter controls is next. No code changed after the `5992d2a9...` /
`484d1f39...` freeze. This update supersedes only the earlier pending-root-reading
status, not any historical-execution or human/scientific acceptance boundary.
