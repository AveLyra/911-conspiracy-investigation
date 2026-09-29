# Native descriptive sample plan

Declared 2026-09-19 after file acquisition/probing and before local video-frame
derivatives. Governing PROTOCOL.md SHA-256:
`7d0fb79d2a1a5cdfc92a7062221e75cd2a2a5caf5f85919c48d3d58bbabb0e2b`.
Root already saw a paused public Drive preview of Dub5 15 and had inspected the
two report references in the preceding unit. This is not a root-blind screen.
A separate AI observer freezes reference anchors before seeing our new samples.

## Exact inputs and intended sampling

| Local source | SHA-256 | bytes | Probe count |
|---|---|---:|---:|
| sources/cbs-net-dub5-15.avi | 8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781 | 60183924 | 475 |
| sources/cbs-net-dub6-44.avi | c3a19c895f5bcacdb473745641dbbd500982219a6de57726920125477a12f90c | 104308572 | 824 |

Select zero-based decoded frame indices 0, every 60 frames, and the final frame:
Dub5 15 = 0,60,120,180,240,300,360,420,474 (9);
Dub6 44 = 0,60,120,180,240,300,360,420,480,540,600,660,720,780,823 (15).
These are descriptive sparse samples, not a continuous-event or no-event test.
At approximately 30 fps the spacing is approximately two seconds, but exact
source PTS and rational time base, not nominal FPS, label each frame. A later
dense inspection requires a separate declaration before inspecting it.

Full ffprobe frame JSON is retained. Reject missing/non-integer or
non-increasing PTS, a frame count unequal to the predeclared count, changing
native dimensions, or source hash/size mismatch. This does not independently
validate a historical camera clock or decoder correctness. Distinguish PTS from
event, broadcast and wall-clock time.

FFmpeg 7.1.1, ffprobe 7.1.1 and bundled Python/Pillow produce native-size RGB PNGs
with no autorotation, scaling, deinterlacing, interpolation, frame-rate change,
audio analysis or enhancement. Color conversion to RGB is a display derivative,
not calibrated photometry. Both inputs are 720×480 DV; sample aspect ratio and
interlace flags are retained as metadata, not corrected by resampling. There
are no thumbnails or montages in this first pass; all 24 images can be inspected
at native raster resolution. Do not quantify distances from uncorrected aspect.

Decode video stream 0 only with `-map 0:v:0 -an -sn -dn`. Use FFmpeg's documented
input option `-guess_layout_max 0` to disable guessing missing audio channel
layouts; this does not repair audio or validate it. Reference:
https://www.ffmpeg.org/ffmpeg.html (input/per-stream guess_layout_max option).
This declared choice is limited to this new video-only unit; it does not
retroactively admit either previously refused source or suppress arbitrary
decoder warnings. Keep all stdout/stderr and exact command arguments. Review
every warning/error; unexpected decode warnings leave the derivative provisional.

## Controls and acceptance

A tiny local helper orchestrates these commands, checks source identity, frame
indices, rational timestamps, native PNG dimensions and pixel hashes, and
retains its own code/plan hashes. It does not decide visual correspondence.
First run a synthetic 125-frame lossless FFV1 AVI at 30 fps, 96×64, with a
predeclared three-color sequence (red frames0–59; green60–119; blue120–124),
SAR4:3, and stereo PCM audio whose AVI layout is unspecified. Require selection
0,60,120,124 and expected exact RGB pixels, unchanged PTS, count and dimensions.
Compare selected video pixels/timestamps with guessing enabled and disabled.
This tests selection and the limited option effect on this control, not all DV
decoding, source truth, calibrated color or pulse timing. Unit negative controls
must reject wrong input hash/count and an existing output destination.

Then process the two historical clips in two separate new output directories.
Require matching per-frame indices, PTS, dimensions and decoded RGB-pixel hashes,
plus identical source hashes before/after. Full logs/command receipts remain
even on failure. Independent review will verify metadata/source assertions and
selected claims. Actual human spot-check and scientifically consequential
measurement remain pending; passing this descriptive check does not satisfy
the charter's human-review gate or establish a causal hypothesis.

Evaluate Figure5-157 and Figure5-158 separately using persistent facade,
neighbor, enclosure, upright and parapet relationships. A strong scene match
is weaker than an exact pixel/frame match. Two CBS dubs may repeat one camera
view and cannot be counted as independent cameras. Visible orange forms must
be distinguished from claims about their mechanism; neither severity, duration,
temperature nor ignition/collapse cause is inferred in this unit.
