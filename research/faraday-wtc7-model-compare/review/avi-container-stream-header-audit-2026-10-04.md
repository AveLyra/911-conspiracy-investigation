# Open discrepancy record: AVI container and video-stream metadata

**Status:** discrepancy preserved; no explanation selected. Local artifact
integrity check only; source provenance unresolved. This is not evidence of
historical cause or intentional alteration.

## Artifact

- Faraday worktree path: `media/nist-simulations/CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`
- Matching copy in this repository: `research/faraday-wtc7-model-compare/media/nist-simulations/CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`
- SHA-256 of each local copy: `f74f653134c8016d858840334919bfedba96fb36dec1db29eff47cb3a0dd5744`
- The existing local collection-plan entry calls the file 998 × 725, 5 fps, and “uncompressed”; it does not identify an acquisition URL or authenticate this as a NIST master.

## Observations

On 2026-10-04, the first 512 bytes of the AVI header were inspected read-only.
The `avih` main-header fields encode sequence dimensions 998 × 725. The
video-stream `strf`/BITMAPINFOHEADER fields encode 996 × 724, 16 bits per
pixel, and compression FOURCC `CRAM`. FFmpeg 7.1.1 reports the video stream
as Microsoft Video 1 (`msvideo1`), RGB555LE, 996 × 724, 82 frames at 5 fps,
16.4 seconds, and 22,598,144 bytes. `file` reports 998 × 725 and
“uncompressed.” These are the observed, conflicting reports and fields.

Microsoft’s AVI RIFF reference describes `avih` as the main header and
`strh`/`strf` as per-stream headers; for video, `strf` carries a BITMAPINFO
structure. That supplies the field definitions, not a finding about why these
values differ. Whether the difference reflects header disagreement, padding,
cropping, export behavior, a parser convention, or another cause remains
unresolved. Do not treat any of those possibilities as the explanation.

## Interpretation and limits

**Directly observed in the inspected local bytes:** the `avih` dimensions are
998 × 725; the video `strf` dimensions are 996 × 724 and its compression
FOURCC is `CRAM`. FFmpeg and `file` report different stream/container
properties as listed above. The same SHA-256 in both checkouts pins the
audited bytes, not their creator, acquisition chain, or relationship to any
NIST master. The source of the discrepancy has not been resolved.

**Not established:** which header or tool output should govern a particular
measurement; whether the file is corrupt; whether its content was altered;
whether it is a NIST-authored or native simulation export; or whether the
discrepancy affects any collapse-mechanics inference. Padding, cropping,
export behavior, parser conventions, and header error are untested competing
possibilities. The AVI name alone does not establish that it is the source
animation used in any NIST report or presentation.

## Open hypotheses about the discrepancy (not findings)

One possibility raised for investigation is that this file could be a
replacement or non-original copy whose container metadata was not updated.
That is logically compatible with conflicting metadata, but the mismatch does
not distinguish that possibility from routine export/transcoding behavior,
container-versus-stream dimension conventions, padding/cropping, a malformed
header, or a tool's interpretation. The inspected bytes do not establish that
the file was swapped, is fake, or was intentionally altered. Keep each of
these as an open hypothesis; do not resolve the discrepancy by choosing one.

Evidence that could discriminate among these possibilities would include an
authenticated source copy or archival acquisition record; matching hashes
from independent, documented copies; original export/encoding records; a
frame-by-frame comparison against a source-authenticated NIST animation; and
chain-of-custody records identifying when and how this local file entered the
collection. None of those comparisons has been completed here. Even a proven
replacement would not by itself establish who replaced it, why, or whether the
replacement changed substantive image content.

## Reproduction and source

Read-only checks used `shasum -a 256`, `file`, `xxd -g1 -l 512`, `ffprobe`, and
one decoded frame through FFmpeg 7.1.1. The source URL for this AVI is not
recorded in the reviewed Faraday collection-plan materials; locating and
hash-comparing an authenticated public acquisition source remains necessary
for provenance.

Primary format reference: [Microsoft AVI RIFF File Reference](https://learn.microsoft.com/en-us/windows/win32/directshow/avi-riff-file-reference),
accessed 2026-10-04. It describes the `avih` global header and the required
per-stream `strh`/`strf` chunks, with video stream format represented by
BITMAPINFO. That format documentation explains field roles; it does not
validate this particular AVI or explain its mismatched values.
