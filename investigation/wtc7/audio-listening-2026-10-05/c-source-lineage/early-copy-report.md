# Earlier video copy preservation and screening

October 7, 2026. Research only.

**An earlier audio-bearing comparison copy is now preserved.** YouTube's
metadata identifies `SIbqaybkbWI` as a public 38-second upload from October 15,
2007, titled [wtc7 collapse (rare video)](https://www.youtube.com/watch?v=SIbqaybkbWI),
by `einsteen`. Its distinctive foreground-building arrangement resembles C's
wide cloud views. This is a useful source-comparison candidate, not yet an
authenticated camera original, a frame-level match or proof that C's reported
bang belongs to this recording.

This extends the [earlier catalog and credit check](report.md); it does not
erase that check's unsuccessful exact-MPG search or its source limitations.
The [prospective protocol and subsequent declared extensions](EARLY-COPY-PROTOCOL.md)
preserve the choices and the acquisition deviation below.

## Source access

The older mirror page returned HTTP 404 on its literal HTTP route. YouTube
oEmbed returned a 403 response for the other named mirror, `O0L5uyqIf0g`;
that restriction was not bypassed or retried using an account. Neither result
establishes why access failed, whether other copies exist or evidence
concealment. The separate reviewer's web-reader attempts and exact searches
also produced no usable source content, a narrower result than global absence.

For the successful ID, oEmbed supplied a title and publisher identity but no
duration or historical camera provenance. The installed 2025.06.09 downloader
failed to extract metadata. The official 2026.08.19 executable, with its
published checksum and the prior preservation record's matching hash, then
succeeded without cookies or account authentication. It ran from a temporary
directory, not a system-wide installation. Its missing-JavaScript-runtime
warning means some available formats may have been omitted. The selected
video was the largest returned direct MP4 format, not a demonstrated highest-
generation or highest-quality source.

The [metadata](sources/SIbqaybkbWI-metadata.json) says part of the collapse is
missing. That is the uploader's statement, not an independently established
reason for any gap. The upload date is platform metadata, not the filming date
or a complete chain of custody. No disclosure of authorship by Peskin or
Rabanne was supplied by the retrieved description.

## Preserved files and the automatic repair deviation

The video and audio were downloaded separately, not merged. Actual byte
identities and stream probes are in the [acquisition receipt](acquisition-receipt.json).

| File role | Bytes | Actual media properties |
|---|---:|---|
| Video format 133 | 758,909 | 320 by 224, square pixels, 30000/1001 fps, 37.704333 seconds |
| First audio download after automatic container repair | 611,449 | Stereo AAC, 44.1 kHz, 37.755646 seconds |
| Audio reacquired with repair disabled | 611,813 | Stereo AAC, 44.1 kHz, 37.755646 seconds |

The first command omitted `--fixup never`, and the tool automatically repaired
the audio container. That violated the declared no-remux preservation plan.
The transformed file remains preserved and explicitly labeled; the correction
obtained a separate copy with repair disabled. This known downloader default
was already recorded in the project feedback, so its recurrence is an execution
lapse, not discovery of a previously unknown risk.

Full-file decoding of both audio copies to native-rate stereo float32 PCM
produced identical hashes and 13,320,192 bytes each, with no decoder error
output. This checks the local container transformation under that decoder.
It neither authenticates historical audio nor establishes correspondence with
the compilation. The unmodified reacquisition is the selected audio input
for future work. No listening or sound-event classification was performed.

The actual video is approximately 29.97 fps, unlike the platform's rounded
30-fps label. All extraction uses recorded presentation timestamps. Differences
between the video and audio durations are not interpreted as physical delay,
tampering or historical synchronization evidence.

## Fixed image screen

The [frozen screen protocol](screen-protocol.json) selected the first presented
frame at or after each integer second from 0 through 37. The source contains
1,130 decoded frames; 38 were selected, preserving full native rasters and
exact rational times. This is not a review of every source frame. Root viewed
both overview sheets and six preselected native frames, then compared the
previously inspected C pictures at track seconds 430, 435 and 443. The
[root notes](root-early-screen-notes.json) were frozen before a second
reviewer's interpretation.

The initial selected frame is black. Samples 1 through 5 show a close facade
view widening to the skyline. Between samples at 5.005 and 6.006 seconds the
scene changes substantially: a broad background facade visible in the first
is no longer resolved in the second, which contains a large cloud. The
one-second sampling cannot determine whether this reflects an edit, time
compression, rapid obscured movement or some combination. Later samples show
cloud advancing among foreground buildings, camera motion and changing
occlusion. No physical collapse time is inferred from these sampled views.

Several stationary features agree qualitatively with C's first and third
segments: a dark double-block facade with a central recess on the right,
pale foreground buildings, a lower banded building and the intervening
street/roof corridor. The resemblance supports further comparison of this
viewpoint. It does not establish the same exact frames, recorder, camera
position or soundtrack. C's middle close-up at track 435 was not established
in these 38 samples; unsampled material prevents a source-wide exclusion.

## Reproduction and limits

The new thin wrapper reuses the existing hash-pinned frame extractor and
synthetic controls. Both runs completed, with all six existing synthetic
assertions passing in each. Root compared actual bytes of all 38 historical
PNGs, two overview sheets and four maps/probe products between runs: all 44
matched their counterpart and recorded hashes. Input/source/binary pins are
preserved in the run receipts. Repeatability does not authenticate the source
or turn a coarse visual screen into an accepted forensic measurement.

A [separate numerical reviewer](independent-early-verification.json) verified
all 93 pinned products in each run, recomputed all 38 selections, and freshly
decoded the full video sequentially. Every selected PNG matched the fresh
RGB pixels exactly. It also independently reproduced the audio PCM byte
equality. The reviewer used separate checking code but the same decoder;
this is not an independent codec implementation or historical corroboration.
The legacy map field `quarter_bin` contains the sampling-bin index; at this
screen's one-sample-per-second rate it is not a quarter-second coordinate.
Exact PTS fields, not that label, control time.

A [separate visual reviewer](independent-early-screen.json) inspected the same
declared images and found no material disagreement after first recording its
own observations. Related or reused edited footage could explain the scene
resemblance without making this copy C's original continuous source. This
same-source, nonblind computational review is not human or expert acceptance.

No historical clock join, audio correspondence score, human acceptance or
causal ranking changed. Source files, failed attempts and the transformed
audio remain preserved; no legal record, accepted Sherlock/Faraday state,
filing, commit or push changed.

## Next discriminating tests

Inspect every source frame around the sampled 5-to-6-second change before
classifying the transition. Separately predefine an image and stereo-audio
correspondence test between this copy and C. Use complete declared intervals,
known-shift controls and explicit uncertainty; do not choose an offset because
it lines up the reported bang with a favored visual event. An exact local
waveform match could establish a shared audio passage between access copies,
but would still not prove original camera sound or the bang's cause.
