# CBS Clips 5 and 6 execution record

2026-10-03 America/New_York; acquisition starts2026-10-04 UTC. Research only.
This is stage3 of the unchanged eight-candidate scene-identification protocol.
The preceding goal turn made progress: it acquired and screened Clips3–4,
recovering a bounded5-143 scene lead and partial5-141 correspondence.
These outcomes do not change sampling, landmarks or acceptance thresholds.

## Before acquisition and views

State: research/sherlock-wtc7-investigation at ca1c2233; stage2 and existing
navigation/feedback WIP are preserved. Main controls and charter hashes match
the completely read versions; current state and repository intake rechecked.
No main/legal/raw edits. Approximately10GiB disk space was available.

Protocol remains SHA-256
5dbaca2b2329db7bc85f67fc0995adf5fd15b8fe3fd0c4b0e50f445179dd35bc.
Both frozen reference descriptions and all four implementation/test hashes
remain unchanged from the preceding stage. Root and the same separate
replacement reader reuse those descriptions; no reference reread or retuning
is intended. The separate reader remains dependent on the original observer's
textual freeze, not a new independent inspection of reference pixels.

The next pair is exactly Clips5–6, followed by still-required7–8. Fresh
metadata IDs/titles/MIME/sizes match the catalogue and all-eight refresh.
Normalized omission of requested checksums/descriptions/video metadata is
not proof of provider absence; access_not_verified remains explicit.
The two declared files total90,497,248bytes. Limits remain55seconds/attempt,
at most two separately preserved attempts/item, catalogue size plus1MiB:
66,930,316bytes for5 and25,664,084bytes for6. Bearer URLs must not be stored.

Use fresh synthetic controls, fixed nine exact rational targets per admitted
clip, two native extractions, source/product reconciliation before views,
and complete Clip5 observation freeze before Clip6. Both readers must freeze
before exchanging judgments. Acceptance is a bounded scene/view association
or explicit sampled non-recovery. No source-clock, glazing, heat, motion or
cause finding follows; no physical measurement is being performed.

## Actual execution

At the initial save no acquisition, historical decode or view had occurred.
The completed calls below supersede that preparation state, not the protocol.

The exact outer script invocations and terminal outcomes are preserved in
[commands.json](commands.json). Fresh parent14 controls completed exit0
(c2bc39); fresh adapter25 controls completed exit0 (e85290). The Python/Pillow
runtime remains3.12.14/12.3.0, ffmpeg/ffprobe7.1.1; version commands and
runtime pins are retained in preparation/extraction receipts. No code or
diagnostic acceptance grammar changed.

## Acquisition and retained failure

Fresh exact metadata and raw-fetch results retain source ID/title/MIME/size
joins in [metadata-refresh.json](metadata-refresh.json) and
[acquisition.json](acquisition.json). The raw-fetch calls use original stored
file bytes, download_raw_file=true, include_base64=false. Only top-level
authenticated file references were consumed. The temporary URL was supplied
through curl's non-echoing stdin, not command arguments or saved logs.

| File attempt | Terminal result | Received bytes | Reported elapsed seconds |
|---|---|---:|---:|
| Clip5 attempt1 | exit0, HTTP200, empty stderr; selected | 65881740 | 2.438420 |
| Clip6 attempt1 | exit28, HTTP200; excluded partial | 2686193 | 71.150559 |
| Clip6 attempt2 | exit0, HTTP200, empty stderr; selected | 24615508 | 2.720973 |

The first Clip6 attempt was confirmed terminal (a5dd0b) before a refreshed
file reference and the single permitted retry. Its original bytes and100-byte
stderr remain preserved. The latter says it timed out after71150ms with
2686193 out of24615508bytes received. **This exceeds the requested55second
limit.** The command included --max-time 55; that requested setting did not
guarantee the observed duration. The overrun's cause is unresolved. It is not
silently reclassified as compliant, nor a reason to admit partial bytes.
No threshold was increased and no third attempt occurred. The retry completed
at b2769a. No live session was restarted merely because observation yielded.

Every materialization command checked that its exact output path did not
exist, disabled terminal echo, then invoked /usr/bin/curl with --config -,
--proto '=https', --proto-redir '=https', --location, --fail, --silent,
--show-error, --max-time 55, --connect-timeout 15 and the declared max-filesize.
Each had its own output and stderr path beneath stage3/raw. The write-out
was restricted to http_code,size_download,time_total,content_type. All
requested limits, received hashes and terminal chunks are in the receipt;
source hashes establish integrity, not historical authentication.

## Selection and extraction

Preparation completed exit0 (226a3b), with both clips admitted for metadata
selection and unchanged pins. All frame probes retained empty diagnostic
stderr; these probes decode internally but do not display images.
Clip5:529frames, indices0,66,132,198,264,330,396,462,528.
Clip6:197frames, indices0,25,49,74,98,123,147,172,196.
Both time bases are333673/10000000seconds; encoded clocks are not exposure
authentication. selection-targets.json was frozen before extraction with
SHA-256 d2bbb409fc90d86e65b186dfaa06443f9c95bf72680adda61f8bb56b4409ea26.

Two new extraction directories completed exit0 (6a95f5,1071d8), both
descriptive_candidates_only, with unchanged strict diagnostics. The full
inner commands/stdout/stderr/status and frame manifests are retained. A
stdout-only root check rehashed36 PNG/RGB products and verified18 equal
repeat frame records plus four clean source receipts before image release
(e9038b,exit0). This was not an image display or independent-decoder test.

## Visual reading freezes

Root viewed18 native images once each, with no crop, transformation, reference
image reread, audio or extra frame. Clip5 was saved/hashed before any Clip6
view. Original reference descriptions were reused unchanged. Both readers'
new judgments remain separate until both complete records have frozen.
The last Clip6 image displayed successfully but its content is visibly
impaired; successful display/decoding is not reliable fine-detail evidence.

Root Clip5 SHA-256:
d26774a3cf65eda6e3dcf76b908f322fdee2f955dc2b88198426438fb9c30066.
Root Clip6 SHA-256:
7f6c27b52a562fef3a6a47a1effcb5416ebec75a5318693fd48fb4d3fe86f1d2.

The second reader also viewed exactly 18 samples once, saved Clip 5 before
any Clip 6 view, and froze both complete files before reading root's records.
Its Clip 5 hash is
e64fde7c761bdd85f89909ab489f52693100e06bd8635bf530165596528a6e97;
Clip 6 hash is
0d0f31f0b29327812a0627473facc14036237c75a6977519f9b0afe8f119345f.
The second reader reported its completed freeze check at 01:39:50 UTC.
Root's later hash check (717b3d, exit 0) confirmed all four files unchanged.
No observations were edited after the exchange. Both report unresolved
reference-specific associations, with different fine discriminators for
Clip 6 preserved in the synthesis.

## Independent audit and continuation

The artifact reviewer saved [artifact-review.md](artifact-review.md), SHA-256
168cd8761f9184adbb682ffd9a99d9dc4f4a619795cc9de373a869f2a10c15eb.
Its read-only checker directly adapts the pinned stage 1 checker, not a
chain through stage 2. Root read the full base checker and adaptation, then
ran the exact command printed in that review from /Users/admin/docs/911
with bundled Python 3.12.14. Result: exit 0, chunk e211f9, artifact_result PASS
and transfer_time_cap_result NOT_MET_RETAINED_DEVIATION. It reconciled three
attempts, one excluded partial, one time overrun, 18 targets, 726 preparation
and 1,452 repeat inventory records, 36 PNG/RGB records, 18 repeat pairs,
17 statuses and four decode logs. This rerun displayed no images, decoded
no historical video and wrote no files. Test receipts were checked, not
rerun during this final audit.

The intervening user reply repeated the comparator coordinates. That turn
freshly checked the existing transcription and arithmetic without advancing
this source screen. On goal continuation, current state and controls were
rechecked and stage 3 synthesis resumed; no acquisition or view was restarted.
The report is a new source-screen result, not another coordinate recheck.

The artifact reader separately checked commands.json against the control,
preparation and extraction receipts (b0ea1f, exit 0), with no receipt-backed
mismatch. All five recorded outer invocations reconcile on paths, pins,
output locations and result states. Outer invocation/exit records and terminal
chunk IDs are transcript-derived; inner receipts do not independently prove
the literal shell invocation, view ordering or freeze chronology. Its wording
corrections were applied: spaced curl options and plural raw-fetch calls
instead of the ambiguous count of two fetches. Two initial exact-text patch
attempts failed without changes; the corrected patch applied all three edits.

## Synthesis critique and documentation checks

The separate visual reader's [synthesis critique](synthesis-review.md), SHA-256
d1c2cedd36341ebfc06dee562cba7f9335fd8e9cfab7147ba69a9964eef7b129,
found no material scientific correction. Root read the entire saved critique.
It reviewed report hash
7d89aecbeece3cbb52288cefd4125020640a5f548e5e35d537f82ed4aa2c1012
and execution hash
aeed676f5e278031b9b8c0b5f3f844bb1fdf5debf57525af91eaf6576c294ba5.
The only subsequent report change replaces its prospective critique sentence
with the actual no-correction result and bounded stage-completion statement;
no observation, disposition, evidence grade or threshold changed. Later
execution additions record this closure and QA, not new historical results.
The reviewer retained its rejected first save separately in the critique.

Preliminary stdout-only documentation QA (25221c, exit 1) passed all 12 pinned
protocol/reference/history/observation/audit/command identities and whitespace
checks across seven authored stage documents, but found the then-pending
synthesis-review.md link missing. That was not a completed QA pass. The review
is now saved; final link/whitespace/navigation verification follows below.
The working diff was inspected (07d9f1); preceding stage 2 changes are preserved.
Main control/charter hashes and branch/HEAD were freshly checked unchanged
(72648d). No source images, code, prior reports or frozen readings were changed
during closure. No broader human gate, original-source authentication,
scientific-engine acceptance or legal promotion is implied.

Final stdout-only Python documentation check (65d36c, exit 0) passed 13 fixed
protocol/reference/history/observation/review/command pins, all eight authored
stage Markdown files, 26 local links, two current navigation entries and
whitespace checks. `git diff --check` also exited 0 (e704f3). This checked
saved text/link integrity, not rendered layout or source authenticity. The
final report SHA-256 is
88e88224c06e3bcc87e0a4782b3409f0173d32e8ab419d03989d1bd1de2ea4a8.
The earlier missing-link failure is retained above, not removed or counted as
a pass. This closure paragraph adds no new links or scientific assertions.

Scope completed: the fixed two-clip scene screen and critique, with transfer
noncompliance retained. Scope still open: Clips 7–8, later source/field tests,
other work packages and the full charter. No staging, commit, push, external
feedback delivery, accepted Sherlock/Faraday finding or legal-record edit.
