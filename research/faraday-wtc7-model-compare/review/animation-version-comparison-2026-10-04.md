# WTC 7 animation-copy comparison (exploratory)

**Status:** local copy and file-structure comparisons completed; source identity
and rendered-content equivalence remain unresolved. The frame-similarity check
below is exploratory and non-confirmatory. It does not identify an original,
replacement, alteration, or cause of collapse.

## Question and result in brief

Are there other copies or versions of the AVI
`CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`? A bounded search across the local
911 repositories found three copies, all with the same SHA-256. They are
byte-identical duplicates, not independent versions. No matching FLV source
files named by the archived NIST Flash wrappers were present in that search.

There are also two archived capture dates for each of two NIST-named SWF
player files, plus a Commons Ogg derivative that its description says
concatenates two clips. The SWFs are materially different binaries and their
wrapper metadata/tag structures differ, but the local captures do not contain
the referenced FLV video payloads. Consequently, whether the SWF changes
changed the animation shown is unknown.

The later part of the Ogg looks broadly similar to the AVI's whole-building
render. An exploratory resampled SSIM check produced a higher score at one
candidate offset than at zero offset, but the offset was not prospectively
registered and the cut point is not authenticated. This is a lead for a
properly designed comparison, not evidence that the Ogg and AVI are the same
source or that either is an original.

## Inputs and byte identity

The same AVI bytes were found at:

- Faraday worktree: `media/nist-simulations/CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`
- Another local Faraday research checkout: its corresponding nested
  `media/nist-simulations/CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`
- Public-repository copy: `research/faraday-wtc7-model-compare/media/nist-simulations/CaseB-Temp-4.0hr_Dmg_NorthWestView.avi`

All three SHA-256 digests were
`f74f653134c8016d858840334919bfedba96fb36dec1db29eff47cb3a0dd5744`.
This establishes byte identity among these local copies only; it does not
establish independent acquisition, authorship, or a match to a NIST master.
An exact-name search did not find `CU animation.flv` or
`whole building animation.flv` in the searched 911 repositories. That bounded
search is not proof that no other copy exists elsewhere.

## Captured NIST SWF files

The local provenance record links the following Internet Archive identity
replays to two SWF paths on NIST's historical video page. Hashes identify the
captured replay bytes, not an independently acquired NIST master.

| NIST path / capture | SWF version | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `CU animation.swf`, 2008-08-29 10:02:16 UTC | 9 | 84,654 | `e067773201621de8dcc0851eeada92a61a02ec8490302af99fe676274c145f44` |
| `whole building animation.swf`, 2008-08-29 10:00:49 UTC | 9 | 84,678 | `9acbef93ef59f0103071b8ce580cee3beb8cdb6139a2ac16f15d864013c84f44` |
| `CU animation.swf`, 2008-09-07 01:30:11 UTC | 8 | 52,070 | `c3a00150f07f449d5a642879f2c294a186b3314cb2672134d708ecff85db8508` |
| `whole building animation.swf`, 2008-09-07 01:30:06 UTC | 8 | 52,079 | `1926c25114092d4c61a170ed8d1a2a04aa223f758421f75b35fdf6185e793074` |

Read-only parsing found that the August captures are version-9 SWFs with a
12-fps wrapper header, one `ShowFrame`, 25 `DefineSprite` tags, and an
ActionScript `DoABC` tag. The September captures are version-8 SWFs with a
30-fps wrapper header, one `ShowFrame`, 41 `DefineSprite` tags, 16
`DoInitAction` tags, and two `DefineVideoStream` tags; no `VideoFrame` tags
were present in those parsed tag lists. The CU wrappers contain the string
`CU animation.flv`; the whole-building wrappers contain
`whole building animation.flv`.

These observations establish that the captured SWF bytes and player-wrapper
structures differ between capture dates. They do **not** establish what
changed in any separately served FLV, the content of the rendered animation,
or whether a model or simulation run changed. FFmpeg's SWF demuxer does not
render these wrappers reliably: it produced a meaningless 45x45 frame for the
August captures and unknown/zero-dimension streams for the September captures.
The existing archive audit reports that the available 2011 Wayback replays of
the named FLV URLs returned NIST error-page HTML rather than FLV video.

NIST's archived August 2008 index page listed the two SWFs under separate
captions. The Commons page describes its Ogg as two concatenated clips and
attributes them to named NIST videos, but the exact-byte chain from those
historical FLVs to the Ogg is not verified. See the source links below and
`media/derivatives/README.md` for the underlying retrieval record.

## AVI versus Commons Ogg: exploratory image comparison

The AVI stream is 996x724, 5 fps, 82 frames, 16.4 s, Microsoft Video 1
(`CRAM`). Its AVI main header separately says 998x725, and `file` calls it
“uncompressed”; those conflicting reports are preserved in
[`avi-container-stream-header-audit-2026-10-04.md`](avi-container-stream-header-audit-2026-10-04.md)
and are not reconciled here. FFmpeg prints AVI metadata strings
`\uFFFD NDW Ltd. 2008` and `JPGVideo`; the replacement character reflects
FFmpeg's displayed output, not a verified decoding of the underlying metadata
bytes. Embedded strings alone do not authenticate the creator or source chain.

The Commons Ogg is 464x338, Theora, 25 fps, 24.88 s. Its page says two clips
were concatenated and currently lists several generated transcodes. Those
transcodes are alternate encodings of the Commons derivative, not independent
source copies.

An exploratory contact-sheet review found the Ogg's later full-building
render broadly resembles the AVI render. The arithmetic difference between
the total Ogg duration and AVI duration is 8.48 s; using that as a candidate
offset, I resampled the Ogg to 5 fps, scaled both sources to 996x724, and
compared 82 frame pairs with FFmpeg's SSIM filter. The per-frame mean of the
`All` SSIM values was 0.88237 at that candidate offset and 0.70494 at zero
offset. A zero offset compares the AVI with the Ogg's opening segment as well
as part of its later segment, so it is not a matched-content control. FFmpeg
also warned during Ogg decoding: `Broken file, keyframe not correctly marked.`
A scene-detection filter produced a high score at Ogg time 8.76 s, but it did
not establish an exact clip boundary.

**Protocol limitation:** the existing collection plan says the synchronization
method and observable must be specified before further synchronized frame
comparison and that the offset must not be tuned after viewing. This SSIM check
was exploratory and was run before checking that gate; it is not a protocol-
compliant or confirmatory result. The 8.48-s candidate is not established as
the cut time, and no adjustment to maximize similarity was made. Do not use
these SSIM values to identify a source, authenticate a version, or resolve the
AVI metadata discrepancy.

## Observations, inferences, and unresolved questions

**Observed:** three local AVI copies have identical bytes; four archived SWF
captures have distinct hashes; the same NIST-named SWF paths have different
captured wrapper binaries/metadata across dates; the local SWFs reference
separate FLV filenames; a Commons derivative contains two clips; and the
exploratory resampled-frame calculation yielded the values above.

**Limited inference:** the later Ogg segment is a plausible visual relative
of the AVI's whole-building render. This rests on a derivative, unverified
clip boundary, and non-prospective comparison and therefore has low evidentiary
weight for exact file identity.

**Unknown:** whether the archived SWF releases displayed different video
content; whether either FLV is the AVI or the source of the Ogg; whether the
AVI is a native NIST export; whether any copy was replaced or altered; and
whether any difference affects interpretation of the simulation.

## Sources and reproduction

- [NIST current WTC archive](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) — confirms the public repository has a “Computer Simulations” category; it does not identify this exact AVI.
- [Commons Ogg file record](https://commons.wikimedia.org/wiki/File:NIST_WTC_7_collapse_model_with_debris_impact_damage.ogv) — derivative metadata, concatenation description, file history, and transcoding status.
- [2008 NIST index capture](https://web.archive.org/web/20080823230025id_/http://www.nist.gov/public_affairs/releases/wtc_videos/wtc_videos.html).
- [August 29 whole-building SWF capture](https://web.archive.org/web/20080829100049id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.swf); [September 7 capture](https://web.archive.org/web/20080907013006id_/http://www.nist.gov/public_affairs/releases/wtc_videos/whole%20building%20animation.swf).
- [August 29 CU SWF capture](https://web.archive.org/web/20080829100216id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.swf); [September 7 capture](https://web.archive.org/web/20080907013011id_/http://www.nist.gov/public_affairs/releases/wtc_videos/CU%20animation.swf).
- Local replay/source manifest and decoder limitations: `media/derivatives/README.md`.

Reproduced read-only with SHA-256, `file`, FFmpeg/ffprobe stream probes,
SWF decompression/tag parsing, FFmpeg contact sheets, SSIM at the stated
fixed candidate and zero offsets, and an FFmpeg scene-detection pass. Temporary
contact sheets and SSIM logs were written under `/private/tmp`; source video
files were not modified. These checks establish only the listed file and
comparison observations.
