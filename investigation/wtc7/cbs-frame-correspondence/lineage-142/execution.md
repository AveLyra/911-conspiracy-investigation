# Figure 5-142 metadata execution record

2026-10-04. Previous goal turn: progress, not a wait. Current unit is a bounded
lineage follow-up under the full active charter. Worktree
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. All changes remain WIP.

## Commands and actual results

Runtime executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Use `-B` throughout. Collector reports Python3.12.14, Pillow12.3.0,
pypdf6.10.0 and FFmpeg/ffprobe7.1.1. No dependency was installed.
Commands below run from the worktree root; `unit` abbreviates
`research/sherlock-wtc7-investigation/cbs-frame-correspondence/lineage-142`.

1. `python3 -B unit/inspect_metadata.py --test`: initial five controls passed,
   `59d162`, exit0. Covers INFO/padding, skipped movie payload, non-RIFF,
   truncated chunk and missing container type.
2. `python3 -B unit/inspect_metadata.py`: `abfdbd`, exit0, 2.286s reported
   command wall time. Output was too large for the tool capture because the
   index skip list omitted `indx`. Two 32024-byte superindex payloads were
   unnecessarily emitted. The exact available truncated tool response is
   [first-capture-truncated.json](first-capture-truncated.json); it is **not**
   a complete JSON inventory. The original collector remains byte-preserved
   as [inspect_metadata_v1.py](inspect_metadata_v1.py), SHA256
   `0d1e50196b66123de304b122c3eb69b96d6661eab64d386a45c326f838918c3c`.
3. Corrected only `indx` exclusion and added its synthetic control.
   `python3 -B unit/inspect_metadata.py --test`: all six passed, `334ca5`,
   exit0. Separate reviewer reran the same six, `645b66`, exit0.
4. `python3 -B unit/inspect_metadata.py`: `7e514d`, exit0. Exact complete
   stdout saved through apply_patch as [metadata.json](metadata.json), SHA256
   `b2e51a671177c0b5ea0b2784eb1894eaacb38c24208d37a2c20207d5689781fc`.
   It records 24 headers and 866 retained payload bytes; all three input
   hashes agree before/after. No full image/audio output was requested.
5. Root independent inline Python direct read, `0d1022`, exit0: sought
   header offsets140334512/538/564/612/672, compared exact four-byte IDs and
   little-endian payload lengths18/18/40/40/256, hashes and text before NUL.
   Pypdf object2850/0 `/Filter` equals `/DCTDecode`; raw `_data`, `get_data()`
   and held JPEG bytes are exactly equal. This closes the raw-stream gap
   that `get_data()` alone would leave.
6. Separate reviewer direct read, `eff6d3`, exit0: all24 header/parent ranges,
   all866 payload bytes, all3 source hashes and raw PDF/JPEG identity agree.
   No collector rerun, media decoding or image views in that direct check.

The collector's two external commands and their complete stdout/stderr are
embedded in metadata.json: `ffprobe -version` and
`ffprobe -v error -show_format -show_streams -show_chapters -of json <AVI>`.
Each has a30second subprocess timeout; both returned0 with empty stderr.
The byte walker skips movie/JUNK/index payloads. No historical scoring or image
classification was executed.

## Deviations and review corrections

The fixed plan SHA256 is
`f45a46ccd9bb3046c3f297cd63046a41a04ee4401487807ade50b1c50a17e024`.
Final collector SHA256 is
`65bc0e26954ff10b561e34830bb9e707efbc69153a789a1380da0fbd2b155c82`.
The original plan's absolute no-decoding wording was too strong: ffprobe's
ordinary stream analysis may read/decode internally. Reviewer checked installed
help, `c6cec0`, exit0. Root had already run both metadata collections before
this warning, so it is not pre-execution clearance. Preserve that deviation;
do not rerun merely to erase it. No frame/audio derivative, visualization or
physical conclusion resulted. Positive metadata is independently byte-checked.

The generic parser can treat a misplaced essence-named leaf as metadata outside
the movie list; the actual fixed24-record tree has none. Do not reuse this
collector as an arbitrary-file header-only guarantee without hardening and
new controls. This does not invalidate the directly checked current payloads.
The reviewer required a raw-stream rather than only filter-decoded-stream join;
both root and reviewer completed that check without changing the sources.

Initial navigation emitted an overbroad/truncated filename listing and tried a
nonexistent assets/run01/manifest.json path. Neither was taken as an exhaustive
search or evidence of absence. Subsequent checks used the actual attribution,
provenance pointers and named files. No file was deleted or raw byte changed.

## Technical reference lookup

After positive Tdat fields appeared, root checked their meaning using Adobe's
published XMP specification. This is a generic technical-reference lookup,
not a new historical-media acquisition or case-data disclosure. Queries used
format/field names only. Adobe's official page linked its GitHub PDF; the raw
fetch failed unsupported-content-type and a legacy Adobe URL was inaccessible.
A mirrored Adobe-authored2020 PDF provided full extracted text for printed55–56,
section2.3.2.1/Table22. The screenshot request did not yield a complete visual
two-page check. Report links disclose mirror/version/verification limits.
No mirror-to-official byte identity is claimed.

## State

The separate [metadata review](metadata-review.md), SHA256
`dd0641c4c022cef0e0b5be636ebdcd294d2b256dae2a2f18f630dbe564a1d685`,
supports the positive byte findings and requires the retained operational
qualifications. Root read it completely (`52dc7d`, exit0). After that review,
the report gained its review link and explicit untested-limit/timeout scope;
no numerical or source finding changed. Those final qualifications are narrower
than the reviewed report, not an expansion of its conclusions.

Root closure check `6dcb53`, exit0, verified all3 unchanged sources, collector
and plan pins, complete-result hash, preserved original code/truncated capture
and compilation of both Python source versions. Tracked `git diff --check`
also passed. Preliminary link check `4f50e7`, exit0, verified4 Markdown files
and10 resolving local links; it correctly reported the documentary-review link
still pending at that moment. A premature file read likewise returned exit1
(`821bdd`) while the assigned review was unwritten, not because a historical
source was missing. No additional historical run or image view followed.

Documentary review completed at SHA256
`ca32d75ad29f5764085973f3926ec3f17f98deda50bbea82b86558352d3cc6d3`;
root read it fully (`5c670c`, exit0). It preserves the catalogue/page scope and
incorporates the newly recovered embedded lead without claiming a second raw-
byte verification. Final package check `6497d1`, exit0, matched all12
documentary source pins and both review pins, checked5 Markdown files and21
resolving local links, compiled both Python versions and checked both navigation
entries. Tracked whitespace check passed. The earlier pending link is resolved.

Research derivatives only. Original plan/failed capture preserved; no main,
raw, legal, prior score, human acceptance, engine activation, source custody,
matrix-save, commit/push or external feedback-delivery status changed.
Source-identification progress is not a physical-cause finding. The next
independent unit is the bounded tape/timecode-key follow-up described in report.
