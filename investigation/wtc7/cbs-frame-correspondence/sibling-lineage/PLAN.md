# Eight clip source metadata and conditional ordering

2026-10-04. Research only. The previous turn made progress by recovering
Clip 7 tape-name/timecode fields. This follow-up includes **all eight already
held complete AVI clips** in the CBS source-screen catalogue, including its
off-target views and selected successful replacements for failed transfers.
It does not select clips according to favorable timing or visual content.

## Question and deliverables

Do the native header fields supply a consistent common-source ordering, and
what would that ordering establish? Deliver a fixed input manifest, tested
header collector and exact output, an eight-row comparison with missing or
conflicting fields retained, independent byte/arithmetic review and a concise
report. This is one source-lineage test within the full charter, not completion
of the fire, motion, structural or documentary workstreams.

Freeze each raw path/size/hash and its acquisition/probe-record dependency
before new header parsing. Reuse the earlier RIFF walk as a versioned bounded
component, addressing its identified misplaced-essence and untested-limit gaps.
Read container headers/native metadata only; do not invoke ffprobe/ffmpeg,
decode DV packs, view media, acquire files or re-run image matching. Whole-file
hashing reads bytes for integrity but does not interpret or decode essence.
All prior collectors, failures, annotations and source bytes remain unchanged.

## Fixed inspection and comparisons

Per file, enumerate headers; skip movie/JUNK/index payloads and recognize
misplaced video/audio essence identifiers rather than treating them as metadata.
Limit metadata payload reads to4MiB, depth12 and10000 records. Test each limit,
parent bounds, odd padding, malformed/truncated headers, multiple RIFF segments,
skipped movie/index/essence, valid metadata and refusal before oversized reads.
The limit is parser accounting, not an OS CPU/memory quota. No frame products
or large output are needed. Preserve exact unknown metadata bytes; use text
before first NUL only as a separately labeled display, not a repaired field.

Report every `tc_O`, `tc_A`, `rn_O`, `rn_A` and `cmnt` occurrence with offsets,
raw hashes and tails retained. Missing or duplicate/conflicting occurrences
remain explicit; do not silently use the first. Decode the fixed AVI video
stream header's scale/rate/start/length and compare to the already saved
container inventory. The header is not an authenticated recording clock.

Original (`tc_O`/`rn_O`) and alternate (`tc_A`/`rn_A`) pairs are separate
comparison lanes; report both even when they agree, without counting them as
independent clocks. Disagreement must not suppress both otherwise usable lanes.

For exactly parsed HH;MM;SS;FF or HH:MM:SS:FF values with nominal30 labels,
show conditional ordering only within an exactly equal nonempty tape-name
group. Consider both30-label non-drop and29.97 drop-frame interpretations;
do not assert the semicolon establishes the latter. For drop-frame mapping,
subtract two frame labels per elapsed minute except every tenth minute; retain
invalid/drop-omitted labels as unconvertible, not zero. Use exact integers and
rationals. The mapping uses the cited FFmpeg7.1 implementation as a
component-arithmetic reference, not a software finding about these files'
historical origin. Uniform-separator parsing and invalid-label rejection are
this collector's declared validation rules, not a claim that FFmpeg's string
parser accepts these native strings or rejects all illegal drop-frame labels.

Report adjacent start-label differences and conditional gap/overlap after the
earlier clip's header frame count under **one-to-one, uninterrupted, same-rate,
same-source mapping**. If that assumption fails, so does the historical meaning
of those differences. Do not bridge edits, resolve24-hour rollover, replace
missing tags, claim historical elapsed time, or assign wall-clock dates.
Non-drop seconds use30fps and drop-frame seconds use30000/1001 only as explicit
interpretation sensitivities; neither replaces the stored container rate.
Do not assign the prior538/539 or127/128 candidate frames a verified tape clock.
Intervals are half-open `[start, start + length)`: gap subtracts the full length,
not length minus one. Equal starts are explicitly ties, not chronology.

All eight rows, all tested interpretations and unavailable comparisons must
be reported before drawing a conclusion. Stored comments remain unattributed
descriptions, not additional witnesses. Common labels/order alone cannot prove
common original camera, continuous footage, absence of edits or faithful NIST
processing. A contradiction may arise from editing/metadata choices as well
as mistaken chronology; preserve those alternatives.

## Verification and boundaries

Synthetic controls and separate method review precede historical parsing.
Match raw hashes before/after, compare Clip7 fields to the prior saved inventory,
and independently seek each positive field's bytes without reusing the parser.
Verify conditional arithmetic with a separate calculation. A useful result is
either a supported metadata ordering or a consequential ambiguity with a
specific next source/edit record. No actual-human gate or physical ranking is
changed by this header-only unit.

Outputs live only in this worktree. No main/legal/fact promotion, raw rewrite,
outreach, new disclosure, engine acceptance, feedback rerouting, commit or push.
Technical-reference reading is permitted; new historical media acquisition is
not needed. Generic feedback remains locally queued at the archived-destination
boundary. Full investigation stays active and incomplete.
