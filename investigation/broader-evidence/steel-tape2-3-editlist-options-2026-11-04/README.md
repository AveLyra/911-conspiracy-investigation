# Same movie bytes, different terminal readouts under MOV edit-list settings

**November4,2026. T23-01; STL02/STL03 context.** A separate end-window test compared three FFprobe7.1.1 input settings on the unchanged steel-recovery movie. Actual returned packet arrays, decoded-window counts, native byte offsets and compressed-payload hashes are preserved below. This is a new software/readout test, not another download, a camera-original authentication or a recovered steel-custody record.

## Actual result and measurement scope

The requested historical read interval was `774%800`: seek toward774seconds, then read to absolute800seconds (beyond this source's end). FFprobe warns that seeking may begin earlier than requested; the actual indices below, rather than an assumed exact one-second clip, define the reading scope. These counts are **only the returned window**, not new complete-file totals.

| Input setting | Returned tail packets | FFmpeg-family decoded window frames | First–last zero-based native sample index |
| --- | ---: | ---: | --- |
| default | 8 | 8 | 11598–11605 |
| advanced-off | 9 | 9 | 11598–11606 |
| ignore-edits | 9 | 9 | 11598–11606 |

Presence of native index11606 in each actual returned tail: `{"advanced-off": true, "default": false, "ignore-edits": true}`. [OBSERVATIONS.json](OBSERVATIONS.json) and the three `source-*-PROJECTION.json` files preserve every returned packet's PTS/DTS/duration, offset, size, flags and SHA256. Their source stream fields remain separate from file-wide annotations. No preferred historical count is selected.

A separate metadata difference is retained: the same packet at native index**11605** (offset**815502668**, payload SHA256**`48771c8659cd00c0c68d9a2c3a86eb92e8537cff75438c767ac65b1a19aa1586`**) has duration**196ticks** in default output and **200ticks** in both alternate outputs, with the same PTS**2321000** and observed time base**1/2997**. The corresponding reported stream durations are **774.506507seconds** versus **774.574575seconds**. These are reader metadata observations, not calibrated camera timestamps or measured clip lengths from this small window. The earlier Apple nominal200tick duration and native movie-clock edit endpoint remain unchanged; this test does not silently equate them.

All returned source packet offsets and sizes matched the prior native map. All offsets common to default and each alternate mode had equal compressed-payload hashes. Separately, direct Python reads of the last **three** mapped source ranges matched the applicable FFprobe payload hashes. The last mapped packet is index**11606**, offset**815560656**, length**57988**, SHA256**`17bab5abb763c11cbc844ee35207dd86f82fdee5f224892dfdfade82c9723952`**; matching modes are `["advanced-off", "ignore-edits"]`. That is a limited compressed-byte correspondence, not a whole-file independent payload test or a pixel/scene identity finding.

## Controls and failed attempts, retained separately

1. The original three-frame control returned3packets/decodedframes under all three full-read settings. The historical full default pass then **timed out at120seconds**. It produced no completed historical count; the other two full historical settings were not attempted. Partial timeout stdout was not preserved by that first harness. This unsuccessful full-source test remains failed, without a new11606/11607total claimed from it.
2. The first tail control expected one final frame, but returned all3frames. Only its first packet was a keyframe. Our one-frame control expectation was unsuitable for that fixture; no historical tail run followed. The failed assertion, source hashes and old control remain. This is a research-method failure, not a discrepancy newly attributed to the historical movie.
3. A separately generated **3182-byte all-keyframe control**, SHA256`ab2dbcfbc3a6d296cebc3e6530f1356f6db8128228b8797f280e77f73d5ac6c5`, kept the same strict expectation: the2%4window must return one packet and one decoded frame atPTS2seconds. All three settings passed. The corrected source test then completed all three end-window cases. The code change and earlier code/results remain preserved; the failed criteria were not relaxed or reclassified as passes.

[FAILED-ATTEMPTS.json](FAILED-ATTEMPTS.json) distinguishes failures, controls and the completed tail test. [TAIL-RUN-STATUS.json](TAIL-RUN-STATUS.json) gives terminal statuses and raw-output hashes. These controls validate the procedure to their stated scope; they are not additional historical evidence.

## Definitions and preserved earlier observations

The installed MOV demuxer help lists `ignore_editlist=false` and `advanced_editlist=true` as defaults. The version-matched [FFmpeg n7.1.1 MOV documentation](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/doc/demuxers.texi#L882) distinguishes ignoring edit atoms from modifying the stream index for their timeline; disabling advanced handling retains only the initial index adjustment. Its [FFprobe interval documentation](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/doc/ffprobe.texi) warns that the actual seek point can differ. Those are implementation definitions, not source-authoring records. Exact native definition hashes, line locators, access dates, installed binary/help hashes and reading limits are in [SOURCE-PINS.json](SOURCE-PINS.json); the executable's source was not audited.

The [previous report](https://github.com/AveLyra/911-conspiracy-investigation/blob/cb8bc2395431a924e8a1eeb740c544eea8ad2aed/investigation/broader-evidence/steel-tape2-3-apple-reader-2026-11-04/README.md) remains unchanged: native size/time/address tables **11607**; nominal edit arithmetic **11605full+1partial+1outside**; prior complete FFprobe **11607reported/11606packets/11606decodedframes**; Apple storage-format **11606samples/11610buffers**, including4zero-sample buffers; Apple source ARGB decode **failed-11833**, with no completed independent decoded count. The earlier failed12planned/11exported-image check is also retained. [PRIOR-COUNTS.json](PRIOR-COUNTS.json) keeps these distinct source/reader layers.

The new observation is limited to option-sensitive terminal readout and the particular compressed-byte joins tested. It does not adjudicate why the stored source, original editor, camera, export pipeline or earlier extraction had these properties. It neither authenticates a camera master nor establishes missing/deleted/substituted footage, altered steel evidence, concealment or historical cause. The movie is one underlying source; reader implementations, tables and hashes are not independent historical witnesses.

## Preservation, reproducibility and unresolved originals

The [publicly linked source](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view) remains **815698448bytes**, SHA256`4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb`. Full hashes before and after each attempted historical-source procedure matched; the guarded Intel source's size/mtime also remained unchanged. No source editing, local movie copy, image/audio/video export, listening, scene interpretation or new historical-media download occurred.

[REPRODUCE.md](REPRODUCE.md) describes the executed settings, native map and generated control. The successful decoder is still FFmpeg-family; compatible independent Cinepak decoding remains a TODO. Actual camera/authoring/source-piece, steel-identity/intake/coupon/transfer/disposition and museum implementation/version records remain unacquired. All eighteen original FAA/telephone/recorder/materials/steel requirements remain open or partial. No source mismatch is silently reconciled, no record target is called acquired, and publication is not substantive completion.

The public files are original research notes/code and selected technical metadata, not historical/control movie bytes, images, reference-document bodies, binaries, private case/correspondence/strategy, donor/contact data or credentials. Ancillary reader tags/dispositions are omitted from clearly labelled public projections; native outputs and their hashes are preserved locally. [REVISION.diff](REVISION.diff) records the exact addition against the immediately preceding preserved media review; the original/source reports remain unchanged. No outreach, new request/fee/filing, mailbox access, deletion, private push, merge or history rewrite occurred.
