# Independent late-fire screening helper review

2026-09-19. Research-only code/controls review under the unchanged main
investigation charter and this unit's protocol. The evidence-audit and
development-verification skills informed the distinction between an executable
sampling method, verified synthetic behavior and historical/physical claims.
No helper, test, protocol, selection, historical source or prior result changed.
The only new repository file from this lane is this review.

## Result and operational disposition

**The unchanged existing suite passes all 16 tests. No unconditional code
blocker was found for a bounded first historical attempt under the frozen
protocol.** This is not a finding that any of the eight historical files will
decode without refusal, that all eight have been covered, or that a figure-like
scene or continuous pulse has been found. Historical media and report reference
images were not decoded or displayed in this lane, and no source was acquired.

There is one concrete foreseeable compatibility stop. The already preserved
Camera2 candidate-extraction selection records one audio-layout-guess notice;
this helper accepts only the exact reviewed swscaler software-conversion
warning. If the same notice is emitted here with warning severity, the helper
will refuse the decode as designed. The prior receipt is
`../tilted-camera-source-join/candidates01/selection.json`, SHA-256
`360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552`,
with `audio_layout_guess_stereo_lines=1`. This is an existing diagnostic
receipt, not a new historical decode or proof of the warning's severity in this
different command. Root was informed before historical execution. Preserve
any actual refusal and review its exact local diagnostic before deciding on a
documented follow-up; do not silently broaden the warning allowlist or reuse
the failed destination.

## Exact reviewed inputs

Read all of `PROTOCOL.md`, `helper-review.md`, `screen_local.py` (360 lines),
`test_screen_local.py` (244 lines), and the eight-source `selection.json`.
The relevant main controls and full investigation charter were already read
in this continuing lane. No nested research instruction file was found.

| File | SHA-256 |
|---|---|
| `PROTOCOL.md` | `f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486` |
| `helper-review.md` | `2b88d413221b27a3c9bea05ea8bb15b3c1dc584f5c198694899239692338c43d` |
| `selection.json` | `e5abd641738cbbb7656f2c4d0f70336725247787d8955637082a44401047fdc0` |
| `screen_local.py`, 20,080 bytes | `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c` |
| `test_screen_local.py`, 13,040 bytes | `5988d73bfb93e24546f015983c0070f7e767c831f8330973b03f962731337b74` |

These match the earlier helper review's producer/test pins. The selection has
eight distinct declared IDs, paths and encoded-object hashes: the three NIST
camera files and Camera3 kit MP4 use two-second bins; CNN, BBC, 27Angles and
complete Peskin use fifteen-second bins. This review read the selection as
configuration, not as proof that each current media file still matches its pin.
The helper checks actual source bytes before it begins and after it finishes.

## Code findings by evidence boundary

**Finite coverage.** `read_selection` permits one through eight entries for
synthetic/subset use, with distinct IDs, resolved paths and hashes. The CLI's
optional `--source-id` retains the original selection snapshot, original source
count and requested IDs. `frame_plan` bins exact rational `PTS*time_base` by
floor division and selects the first decoded frame in each occupied bin,
including negative/nonzero starts. Its coverage records all observed-frame
counts and internal empty bins, and explicitly makes no inference outside the
observed endpoints. A complete subset receipt is not complete eight-file
coverage. Root must reconcile the declared eight IDs across completed, failed
and unattempted subsets before a set-wide sampling statement. Even all eight
completed cadences do not establish every-frame or every-holding coverage;
15-second sampling can miss the report's approximately six-second episode.

**Integer timestamp and raster preservation.** The probe inventory retains
integer `pts`, width and height for every decoded frame. It refuses malformed,
missing, duplicate or decreasing timestamps and geometry changes. The second
pass starts at the file beginning, selects the planned decoded frame indices,
and uses `-copyts`, `-noautorotate`, `-noautoscale`, passthrough frame output and
demuxer encoder time base, with no seeking, audio, crop, stabilization or
time interpolation. Selected showinfo sequence/PTS/time base/dimensions are
checked against the first pass; rounded `pts_time` is only a consistency check,
not the binning authority. PNG names, counts, RGB mode and native dimensions
are checked before overview generation. Sample/display aspect metadata are
retained; RGB conversion and LANCZOS thumbnails remain display derivatives
without SAR correction or color/area calibration. This proves preservation
relative to the current decoder's source timing and raster, not native camera
exposure or the media's earlier editing history.

**Diagnostic refusal.** Nonzero subprocess exits fail. Any nonempty warning-
level probe/inventory stderr fails. The decode classifier, with FFmpeg's
`level+info` logging, accepts only the exact component/message combination for
the previously reviewed yuv420p-to-rgb24 software fallback. Every other labeled
warning/error/fatal/panic causes refusal. Raw logs remain local; the CLI emits
fixed categories and sanitized IDs/counts. This strictness can reject otherwise
viewable media and must not be interpreted as proof that its image content is
false or unusable. The real historical codec/container/diagnostic combinations
are still untested by this lane.

**Partial results and overwrite refusal.** A destination must be new. Source-
and run-level failures preserve phase/category, local traceback, commands that
returned, partial products and attempted post-failure source identities.
Inventory output survives a planning failure; a simulated late integrity failure
retains already generated `frames.json` without marking the source complete.
An outer failure retains earlier completed sources and the full requested-ID
list. A failure before a subprocess launches may have no completed-command
receipt entry; the source snapshot and local traceback remain the reconstruction
route for that attempted operation. The caller still needs to distinguish the
failed current source from later unattempted IDs. Existing run refusal leaves
the original destination intact instead of adding a failure file into it.

**Repeated products and independence.** The suite creates a real synthetic
FFV1 file and runs the helper twice through ffprobe and ffmpeg. It compares
the two native RGB PNGs and one overview by exact bytes, and checks receipt
product hashes. An independent read-only reconciliation here checked all 68
listed product-hash references across both outer and source receipts, plus
source/snapshot identities, integer frame/PTS/bin membership, dimensions and
source aspect metadata. The three generated image products are byte-identical
between runs. Receipts contain run-specific paths and diagnostics; no claim is
made that whole run directories or every receipt are byte-identical. Both
passes and both repeats share FFmpeg libraries. This is independent receipt/
code review and same-family processing consistency, not an independent decoder,
historical source, visual corroboration or human forensic examination.

## Actual execution and retained controls

Command run from the investigation worktree:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/late-fire-video-lineage/test_screen_local.py
```

It exited zero: **16 tests, zero assertion failures, zero errors**, runtime
1.687 seconds in the local test log. Python 3.12.14, Pillow 12.3.0. No dependency
installation or global setting change occurred. FFmpeg and FFprobe report
version 7.1.1; executable hashes are respectively
`7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`
and `fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`.

The suite preserved all generated material under
`/var/folders/tr/qmsqldfn59591rbflj14mc4r0000gn/T/late-fire-screen-tests-6v0ee8n1/`.
This is retained temporary evidence, not a permanent archive; nothing was
deleted or promoted to a new repository artifact by this review.

| Current control artifact | Bytes | SHA-256 |
|---|---:|---|
| `test-receipt.json` | 670 | `8a2143f2d98624f4f4410d8b40c1eab9a1b5625bb367f353bd97a2c076c2d613` |
| `unittest-local.txt` | 1,927 | `f8311bef3c27eba0696ba917723e4c64e2e381920c5eb96b056bf68d27434ea0` |
| `tiny-fixture/nonzero-gap.mkv` | 11,893 | `1045ddb60d9cb37c17148b34751371e7910acf59a08d48dd3d234c00375841c9` |

The synthetic media has 12 decoded frames; the selected pairs are source index
0 / PTS 3000 / bin 1 and index 4 / PTS 6000 / bin 3, time base 1/1000. Bin 2
is empty. Native images are 64×48 RGB and source SAR is 2:1; the overview is
960×1120. The successful decode records 13 exact reviewed software-fallback
notices and zero unreviewed warnings/errors. Test failure artifacts preserve
`source_pin_mismatch`, `source_subset_invalid`,
`selection_protocol_pin_mismatch` and the simulated `source_changed` outcome;
those are expected passing negative controls, not failed historical runs.
The fixture bytes did not change during the simulated identity-change test.

The sixteen tests include exact/rational boundaries, negative and nonzero
starts, gaps, duplicate/out-of-order and malformed PTS, time-base rejection,
selected PTS/order/count/dimensions, display-time rounding, native dimensions/
mode, exact-warning allowance/refusal, real decode/repeat, overwrite refusal,
bad pins, subset/protocol rejection and late source-change rejection. They do
not exercise a multi-source failure midway through eight real codecs, encoded
rotation metadata, all possible decoder warnings or historical-format/runtime
limits. Those remain execution observations, not presumed passes.

No test invocation failed in this lane. An initial instruction-file search
also named a nonexistent `tools` directory in this older worktree and returned
an error; the actual research instruction search was then completed. A no-match
`rg` exit during inventory is not a test failure or an instruction-source read.
Earlier producer-revision failures documented in `helper-review.md` remain
preserved and are not rewritten as passes by this fresh run.

## Acceptance ceiling and next required observations

The narrow supported claim is that the current helper implements the declared
finite coarse-sampling contract and passes its available synthetic controls,
with independently reconciled synthetic receipt/products. The strongest
objection to broader readiness is that one small generated FFV1 file shares
the decoder family and does not exercise historical codec, timestamp, edit,
warning or corruption behavior. A mismatch/refusal in an actual source would
change the compatibility assessment while preserving the utility of the
synthetic findings.

For historical results, independently reconcile every admitted source receipt,
actual requested/completed coverage, plan-to-frame integer PTS and dimensions,
and material repeated derivatives before interpretation. Independent overview
screening notes must be frozen before root candidate decisions are disclosed
to that visual lane, as the protocol requires. No figure correspondence,
continuous-event duration, historical absence, time of day, physical mechanism,
global inventory completeness, cause ranking or legal/Sherlock acceptance is
established by this code review.
