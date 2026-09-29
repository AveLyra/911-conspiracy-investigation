# Local screening helper review

2026-09-16. Research working code only. Controlling protocol SHA256:
`f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486`.
No historical source was decoded or viewed during this helper task. Work stopped
after the bounded implementation and synthetic verification when root redirected
the active task to the supplementary-production folder.

## Invocation and selection contract

Use the bundled Python with Pillow already installed:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B screen_local.py --selection /absolute/selection.json --protocol /absolute/PROTOCOL.md --run /absolute/fresh-run
```

An optional repeated `--source-id ID` selects existing declared IDs without
changing the selection document. Every run records the original selection hash,
its total source count, the actual requested IDs, and a byte-identical snapshot.
It is therefore possible to process or reproduce one declared file without
silently restarting the other files. The caller must reconcile all eight IDs
before claiming coverage of the declared set.

Selection is an object containing `sources`, a list of one to eight objects with
`id`, absolute `path`, lowercase `sha256`, integer `bytes`, and integer
`step_seconds` (2 or 15). Descriptive extra fields are preserved. IDs, resolved
paths and encoded-object hashes must be distinct. Optional top-level
`protocol_sha256`, when supplied, must match the hard-coded protocol pin. The
one-source option permits synthetic controls and separately attributable subset
runs; it does not amend the eight-file protocol.

## Implementation and evidence boundaries

The implementation elaborates the declared full-decode method into two passes.
First, ffprobe fully decodes the selected video stream from file start and writes
an allowlisted integer-PTS and stored-raster geometry inventory. Exact rational
arithmetic chooses the first frame in each occupied source-PTS bin and records
every occupied bin's frame count plus internal empty bins. There is no inferred
coverage before the first or after the last observed frame. Duplicate or
decreasing PTS, malformed/missing PTS, and changing stored dimensions stop the
run for review.

Second, ffmpeg fully decodes from file start, selects the planned source frame
indexes, and saves RGB PNGs without seeking, autorotation, audio, crop,
stabilization, temporal interpolation or enhancement. Every selected showinfo
PTS and dimension is reconciled against the first-pass plan; stream/filter time
bases must agree. PNG dimensions, mode, sequence and counts are checked before
overview creation. Overview sheets are fixed 3-by-4 grids with at most 320-by-240
LANCZOS thumbnails, source ID, sample index, bin, PTS and exact source seconds.
The native PNGs keep stored geometry; no sample-aspect-ratio correction is
applied. Probe metadata retain sample/display aspect and declared color fields.

The first synthetic run stopped on the platform's exact swscaler warning that
accelerated yuv420p-to-rgb24 conversion was unavailable. That message states
software fallback, not a failed decode. The only accepted warning is now that
exact component/message combination, counted in `diagnostic_summary`; every
other warning/error/fatal/panic message stops the run. Raw diagnostics stay
local and are preserved. This review does not establish color calibration.

The source is hashed before and after each source run and again at the outer-run
boundary. Tools are hashed and versioned; controls are hashed/snapshotted and
checked again at completion. Source receipts list exact commands, frame data,
gap counts, source identities, and native/overview/diagnostic product hashes.
Destinations must be new. A failed run retains partial outputs, local traceback,
sanitized category, and attempted post-failure source identities. The CLI emits
sanitized source IDs, counts, receipt hashes and failure categories only.

## Verification actually performed

Final command: bundled Python `-B test_screen_local.py`. Result: **16 tests passed,
zero failures/errors**, including a generated 64-by-48 FFV1 fixture with source
PTS starting at 3 seconds, a missing 2-second bin, and SAR 2:1. Two complete
synthetic helper runs produced identical native and overview hashes. Frame count
(12), selected PTS (3000 and 6000 at 1/1000), source indexes (0 and 4), source
pins, dimensions, gap list, SAR metadata and product hashes were reconciled.
Additional synthetic controls cover rational boundaries, negative/nonzero PTS,
malformed/duplicate/out-of-order timestamps, selected-frame order/count/time
base, dimension/mode failures, protocol/subset rejection, unchanged input pins,
simulated post-decode identity change, unknown-warning refusal, and overwrite
refusal. The simulated hash change does not alter the fixture itself.

Passing receipt (all generated controls and intentional failures retained):
`/var/folders/tr/qmsqldfn59591rbflj14mc4r0000gn/T/late-fire-screen-tests-8x6g9s1z/test-receipt.json`.

- Helper SHA256: `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c`.
- Test SHA256: `5988d73bfb93e24546f015983c0070f7e767c831f8330973b03f962731337b74`.
- Python 3 runtime and Pillow version are recorded by each run; no dependencies
  were added or global settings changed.

First failed attempt is preserved under
`/var/folders/tr/qmsqldfn59591rbflj14mc4r0000gn/T/late-fire-screen-tests-vs4dqek9/`.
It ran 14 tests with one error, zero assertion failures; the error was the
software-conversion notice above. Its run contains the old complete helper
snapshot (SHA256 `e654ac82bb97ca83f634f8692b5ebbdfee661684f828f474822587de2618021e`),
partial PNGs, diagnostics and failure receipts. It was not reused or deleted.
These temporary directories are retained now but are not a durable archive;
promote only the desired control artifacts locally before temp cleanup if needed.

## Remaining review and limits

Historical extraction, independent receipt review, overview inspection, candidate
reconciliation and material historical-derivative reproduction remain undone.
No browser was used; no UI behavior was changed. The two passes and repeated
synthetic runs use the same FFmpeg decoder family. They check processing
consistency, not independent historical authenticity, visual correspondence,
clock time, pulse duration, original cadence, physical cause, or archival
completeness. Strict diagnostic/PTS/geometry checks can reject an otherwise
viewable source; such a failure requires a documented follow-up, not a silent
retry or relaxed check. Large-source runtime and historical-format compatibility
have not been measured. Selection and known source holdings remain root-owned.
