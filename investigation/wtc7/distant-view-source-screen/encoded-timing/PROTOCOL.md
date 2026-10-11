# DistantView encoded timing audit

October 8, 2026. Research only. This is a new metadata test, independent of
the pending human localization pilot. It does not amend that pilot or the
earlier failed matching-timestamp requirement.

## Question and prior knowledge

Do the missing FFprobe frame PTS values follow coded picture type and packet
reordering, and what timing does FFprobe/FFmpeg produce under its explicit
`genpts` option? The existing screen reports 329 missing frame PTS out of 962
frames and one missing best-effort value. Inspection of its first few rows
already showed missing I/P-frame values and present B-frame values. This
motivates the test; it is not a blinded prediction or independent holdout.
The old `stored_pts` field is an alias for FFprobe's decoded-frame `pts`,
not proof of a literal timestamp stored in the AVI or camera original.

## Fixed inputs and outputs

Use only the held `../source/DistantViewWTC7.avi`, 4,749,520 bytes, SHA256
`a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e`,
and the two previous raw probes `../probe02-diagnostics/probe-stdout.json`
and `../probe03-diagnostics/probe-stdout.json`, each SHA256
`c0c7ce905e0f3e96a4ce9fedbc8b4309d9c9a13c43d5f86afbe0d176e2e5ac84`.
Pin this protocol, code and the canonical FFprobe7.1.1 binary at
`/opt/homebrew/Cellar/ffmpeg/7.1.1_3/bin/ffprobe`, SHA256
`fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`.
Record runtime/library version output; the binary pin is not a complete
dynamic-library environment lock.

Generate two independent fresh output directories. Each contains one default
probe and one probe differing only by input `-fflags +genpts`. Request only
video stream geometry/codec/time-base/rate/count, packet stream/PTS/DTS/
duration/position/size/flags/SHA256-data-hash, and decoded-frame stream/PTS/DTS/best-effort/
duration/packet-position/key/picture-type/geometry fields. Preserve complete
raw stdout and stderr, argv and exit/timeout status before parsing. A probe
may internally decode video; no image/audio is emitted or inspected. Do not
seek, remux, re-encode, add frames, extract pixels, or overwrite old probes.
Use a 60-second timeout per process and a 16 MiB post-capture output limit;
oversized/failed/timeout output is retained and excluded from analysis.
Output directories must be new, within this unit, and refuse overwrite.

## Analysis fixed before execution

For all frames and separately ordinals274–411, tabulate picture types,
missing/present PTS and best-effort values, and exact known timestamp
increments. Preserve null values and each known pair's two ordinals,
ordinal gap and timestamp difference; distinguish adjacent pairs from pairs
spanning missing values. Compare all old requested fields to the
new default frame records and compare the two fresh runs byte-for-byte.
Report differences, do not make equality a condition for preserving results.

Record packet count, nulls, DTS increments and packet-position uniqueness.
Check each reported packet byte range against file bounds and its reported
data hash against the same source-byte slice, retaining mismatches. This is
payload accounting, not parsing the packet into pictures or authenticating
exposures; packed/multiple-VOP semantics remain untested in this unit.
Join frame `pkt_pos` to packet `pos` only where exactly one packet matches;
retain zero/multiple-match dispositions. A positional join is FFprobe's
association, not independent proof that one packet contains one exposure.
Enumerate every default/genpts field change and check whether picture type,
geometry, duration and position associations remain identical. Metadata equality does not prove
decoded-pixel or picture-order identity, nor an independent correspondence
from packets to displayed pictures. Do not fill
the original table with generated values. Report ordinal-to-time regularity
only as a property of each specified FFprobe output, not historical cadence.

Read primary FFmpeg documentation and narrowly relevant AVI demux, timestamp
handling and best-effort selection source. Prefer exact tag `n7.1.1` in the
official FFmpeg repository; permitted source files are
`libavformat/avidec.c`, `libavformat/demux.c`, `libavcodec/decode.c`.
One bounded acquisition per file plus one transient retry is allowed. Preserve
retrieved bytes/URL/status/hash; no substitute version if unavailable.
The already opened official7.1 Doxygen pages are orientation, not proof of
the exact installed build's executed branch. No instrumented or rebuilt
decoder is authorized. Code inspection can support an explanation, not prove
every branch executed. No raw MPEG4 VOL/VOP parser in this unit.

## Verification and interpretation

Before historical execution test null versus zero, malformed timestamps,
picture-type cross-tabs, nonmonotone/irregular intervals, absent/duplicate
packet positions, changed default/genpts identity fields, changed baseline,
output refusal and failed/timeout diagnostic retention using synthetic data.
A separately implemented checker must reconstruct material counts, joins,
differences and regularity from the raw JSON without importing the producer.
Repeat source/code/input hashes before and after; retain failures. A separate
reviewer audits source interpretation and strongest alternatives.

Evidence favoring a codec/metadata explanation would include systematic
picture-type association and a reproducible generated-timestamp sequence
consistent with documented behavior. Anomalous association, changed ordering,
nonregular increments or failed joins weakens a simple account and remains
unresolved. Either result can change the timing dependency's wording, but
cannot establish the absence/presence of historical dropped exposures, edits,
speed changes, manipulation or an original capture clock. Uniformly generated
timestamps can label nonuniformly acquired or edited images.

Stop after this finite test, independent check and research report. No
historical coordinate, trajectory, physical calibration, acceleration,
cross-camera lag, cause ranking or repair of source data; no automatic human
acceptance, solver, main/raw/legal edits, case transfer, outreach, fees,
publication, commit or push. Human review and all other charter dependencies
remain separate.
