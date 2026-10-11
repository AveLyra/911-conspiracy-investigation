# DistantView timestamp gaps follow coded picture type

October 8, 2026. Research only. The 329 missing frame PTS values in the held
DistantView copy occur on every I/P picture and on no B picture. FFmpeg's
explicit timestamp-generation option supplies all of them without changing
the checked packet payloads. This supports a codec-processing explanation
for the metadata pattern, not a finding that 329 camera exposures are missing.
The pattern is not affirmative evidence of missing historical exposures.
It does not authenticate the original capture cadence or rule out earlier
editing, duplication or speed conversion.

The [protocol](PROTOCOL.md) was frozen before the new probes. Its review
clarified that generated timestamps belong to the FFmpeg processing chain,
that intervals spanning nulls must retain their ordinal gaps, and that
metadata equality is not decoded-picture identity. Prior inspection of the
old probe's first few rows motivated the picture-type hypothesis; this was
not a blinded prediction. The human localization pilot remains separate.

## Observed metadata and generated values

Each of two fresh runs used the same pinned FFprobe7.1.1 binary and held AVI,
first with ordinary options, then with input `-fflags +genpts`. No source was
modified, remuxed or re-encoded. FFprobe internally decoded frames for metadata;
no historical image or audio was emitted, viewed, annotated or measured here.

| Reported picture type | Frames | Default frame PTS missing | Default best-effort missing | Frame PTS missing with genpts |
|---|---:|---:|---:|---:|
| I | 4 | 4 | 0 | 0 |
| P | 325 | 325 | 1 | 0 |
| B | 633 | 0 | 0 | 0 |
| Total | 962 | 329 | 1 | 0 |

Within the separately fixed localization interval274–411, the 138 frames
contain one I,46 P and91 B pictures. All47 I/P PTS values are absent in the
default result; all138 best-effort values are present. No missing value in
the old records was filled or renamed by this test.

Both arms report962 packets with962 distinct nonnegative positions. Each
reported packet payload's SHA256 matches the corresponding source-byte range;
each frame's reported `pkt_pos` has exactly one matching reported packet
position. These are byte-accounting and FFprobe-association results, not an
independent MPEG4 picture parser or proof of one camera exposure per packet.
Packed/multiple/uncoded-picture semantics remain untested.

Default packet DTS labels run0–961 in unit increments. Every available
default frame PTS and best-effort label equals its zero-based output ordinal
plus one. Default best-effort is absent only on final ordinal961. The genpts
arm reports frame PTS and best-effort labels1–962, all present. The stream's
declared tick is100/2997 seconds; this is an encoded-file time base, not an
independently established camera interval.

The complete arm comparison finds exactly329 changed frame PTS fields,
329 changed packet PTS fields and one changed best-effort field. All are
absent-to-present changes. No reported picture-type, geometry, duration,
packet-position, payload-hash or other requested identity field changes.
Default frame/stream fields agree with both preserved earlier probes on
every originally requested field. This does not certify pixel identity or
historical ordering: no new pixel comparison was made.

## Why the distinction matters

The earlier field called `stored_pts` is an alias for FFprobe's decoded-frame
`pts`; that name does not establish a timestamp literally stored in the AVI.
The exact-tag primary sources show several processing layers:

- The [AVI demuxer](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/libavformat/avidec.c#L675)
  reads scale/rate for its time base; lines1540–1543 assign DTS from a frame
  counter, advanced at1576 through `get_duration`. Regular DTS therefore need
  not be individually stored exposure times.
- [Timestamp handling](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/libavformat/demux.c#L1002)
  distinguishes delayed pictures and can leave PTS absent. The other branch
  at1112–1119 can derive PTS from DTS. Thus even default present PTS can be
  software-derived. Parser output at1232–1249 is another transformation layer.
  The genpts path at1541–1587 uses buffered later timestamps and a conditional
  end-of-file fallback; regular generated labels are not independent clocks.
- [Best-effort selection](https://github.com/FFmpeg/FFmpeg/blob/n7.1.1/libavcodec/decode.c#L289)
  chooses between supplied PTS and DTS using cumulative non-increasing-value
  counts, and is applied at699–701. It neither interpolates missing exposures
  nor guarantees authentic or monotonic acquisition times.

Root and a separate AI reviewer read these relevant routines, including
adjacent conditions, from the locally preserved exact-tag files. The source
explains a plausible processing path; neither reader instrumented the binary
or established every executed branch. The installed binary identifies7.1.1,
but a tag match is not proof of an identical compiled source/build environment.

The strongest contrary interpretation remains possible: orderly timing metadata
can label footage that was edited or cadence-converted before this file was
created. The present evidence supports a narrower statement—**the missingness
is systematically associated with coded picture type and is consistent with
documented FFmpeg handling**—not “the original clock is recovered” or “the copy
is proved unaltered.” Missing PTS alone neither establishes nor excludes edits.

## Verification and preserved failures

[audit.py](audit.py) and [test_audit.py](test_audit.py) implement the finite
test. Root read both completely and ran all21 synthetic tests successfully
before historical execution. The author had first encountered and repaired a
missing-bracket syntax error; that initial failure is not counted as a pass.
The tests cover nullable/zero/type separation, ordinal gaps and irregularity,
positional ambiguity, payload mismatch/bounds, changed fields and baselines,
exclusive output creation, warnings, launch failures, oversized output, and
actual synthetic nonzero-exit/timeout diagnostic retention.

Root separately authored [verify.mjs](verify.mjs) without importing the
producer. Review found two false-confidence risks before its historical use:
trusting a producer-selected baseline field subset, and unchecked JavaScript
integer intermediates. The checker now enforces the complete fixed old field
sets and rejects unsafe deltas/products or invalid time bases. Its16 synthetic
assertion groups pass. These are software controls, not independent scientific
experiments or forensic accuracy estimates.

The separate checker reconstructed both runs' raw frame/packet records,
all/selected type tables, missing-value lists, every consecutive-known pair
with ordinal gap, adjacent/gap partitions, positional joins, source-slice
hashes, baseline comparisons and full arm/identity changes. Packet null counts
and position uniqueness are separately recomputed. Some ancillary producer
summary flags are not independently compared; the underlying checked pairs
and independently computed offsets support the regularity statements above.
The check also does not independently certify every payload status label or
join-reason string; it checks the underlying positions, sizes, digests and
join dispositions. A separate review confirmed these exact coverage limits.
Both [run01](run01-independent.json) and [run02](run02-independent.json)
receipts pass. This is independent arithmetic on shared FFprobe outputs,
not independent decoding or camera evidence.

The raw default outputs, raw genpts outputs, analysis JSON, version output,
empty stderr files and before-pin files repeat byte-for-byte. Elapsed process
times differ and are retained, not required to repeat. Root additionally
verified all10 source/code pins before/after and against current bytes for
each run, plus all11 saved output pins per run. All four historical probes
returned0 with empty stderr; no warning or failed historical result was waived.

Actual commands, from the investigation worktree, were:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/test_audit.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/audit.py --out run01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/audit.py --out run02
node research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/verify.mjs --self-test
node research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/verify.mjs run01
node research/sherlock-wtc7-investigation/distant-view-source-screen/encoded-timing/verify.mjs run02
```

The complete FFprobe argv, version, raw stdout/stderr and execution status are
under each run's `default`, `genpts` and `version` directories. Run receipts
pin the exact inputs and products. They identify Python3.12.14 and the pinned
FFprobe7.1.1 binary/library-version strings; dynamic-library bytes are not a
complete environment lock. The independent checker used Node22.16.0.

The three allowed public C-source downloads initially failed sandbox DNS
resolution. One normally approved retry per file succeeded with HTTP200.
Their original bytes and response headers are preserved alongside this
report; no alternate tag or source was substituted. Local output writes used
normal scoped approval for the investigation worktree. No case data was
uploaded. Receipt references: initial source failures `0f0d4f/a4e425/bafaa6`;
successful downloads `782336/f1801c/80b99e`; root tests `5a673d/dbc630`;
completed runs `2fe698/38dbe7`; independent checks `5fb162/1c7b19`;
repeat and current-pin verification `0b139f`.

A separate AI source reviewer independently aggregated the raw JSON with Ruby
(`420a86`, exit0), confirming picture-type missingness, ordinal offsets, packet
DTS labels, all329/329/1 changes and the old requested-field agreement. Its
endpoint inspection retained the distinction between a frame's reported DTS
and the DTS of its position-associated packet. This reviewer did not rerun
payload hashing or the saved checker; shared raw outputs are not independent
historical origins. Checker review and16-group rerun passed at `ade9b3`.

The final substantive reader inspected this complete report, current status
and the deduplicated feedback clarification and found no material correction
(`437a88`). Its reviewed report hash was
`6df33461c207b5159dea009b4cb7ddbc4a4b18ec10bb8064d721e95c12bd25c9`;
this review-provenance paragraph was added afterward. That is an AI review
of the stated metadata inference, not qualified forensic acceptance.

Key SHA256 pins:

| Artifact | SHA256 |
|---|---|
| Protocol | `85570f004474538ac5cd9e3bf9dfb40e84cafc391671a62103ccca5323d45ba9` |
| Held AVI | `a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e` |
| audit.py | `4998374eed6a13c4bb1e783829b62df1eb0d6e235820d2e7d5e7bd1445f147a4` |
| test_audit.py | `bf20bbaef2bb9c8a03535f5569450571a895be11af9496df9f8116a904415e76` |
| verify.mjs | `c1ab6ec95518c681b6e8fb98028dc2821ca285fcc80afcf8db892014c6b11ce1` |
| Repeated analysis | `af0bc69a8e153f03ad6439cb9de053326bde4366db1f51076b1bd81dbe6c7f46` |
| Default raw output | `b62542e69d8bc16661e9dd43df6011355cce7008fae18dfc6a8fe9e0c3d86408` |
| Genpts raw output | `7de40e08a65aca8dd6baa0085d13084ba3f32892b90d42719861dca124e1eb73` |

The three source-file pins are in each run receipt. Sources were acquired
from `https://raw.githubusercontent.com/FFmpeg/FFmpeg/n7.1.1/` with paths
`libavformat/avidec.c`, `libavformat/demux.c`, and `libavcodec/decode.c`.

## Effect on the investigation and next boundary

The observed type association and checked generated output are directly
established for this file/tool combination (gradeA). Attribution of the whole
pattern to particular internal execution branches remains a supported but
untraced interpretation (gradeC). Authentic original exposure timing remains
undetermined (gradeD). A conflicting bitstream/picture mapping would weaken
the simple processing account; a traceable camera/master chronology would
address historical cadence in a way that generated timestamps cannot.

This narrows the Q03/Q04/Q10 timing dependency: do not characterize these nulls
as missing historical exposures, or describe default PTS as necessarily
stored original timestamps. The original complete-PTS gate remains failed
under its original contract. Any later use of generated labels would require
its own explicit conditional measurement protocol; this test admits none.

The immediate localization prerequisite remains the six actual human responses.
After that, any proposed automated locator still needs the separately frozen
synthetic accuracy/abstention challenge. Physical time, geometry and feature-to-
body interpretation require their own evidence. No trajectory, acceleration,
force bound, cross-camera lag or cause ranking changes here.

This finite encoded-metadata unit is stopped. The source bytes, old nulls,
human packet, main/legal record and accepted Sherlock/Faraday state are
unchanged. The timing-provenance lesson is deduplicated locally under existing
feedback IDs; delivery remains pending the archived-destination decision.
Work is uncommitted on `research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`. The full goal remains active and
incomplete; this result postdates the unchanged material-claim index.
