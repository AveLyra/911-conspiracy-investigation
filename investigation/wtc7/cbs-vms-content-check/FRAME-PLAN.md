# Native-image selection and diagnostic disposition

Declared before producing/viewing this candidate's PNGs. The source is
8,717,690bytes, SHA256
bae07b52bc85c735c72b227b55a327da3a49c6bf6a0798ccc9d85602dae185ad.
Select v:0, which is container stream1, WMV1/yuv420p,320x240. Probe supplies
4531 strictly increasing integer PTS at timebase1/1000,33→302602. Missing,
duplicate or decreasing PTS would refuse this selection; none occurs.

Grid origin is first decoded PTS33, not zero or a real-event timestamp. Take
the earliest frame at or after each target33+4000*k through the last PTS;
include first/last frame and deduplicate sorted indices. Four seconds is the
first positive multiple of two yielding at most80 images (77). No nearest-
frame rounding, interpolation or nominal-FPS resampling. Exact indices:

0,60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1019,
1079,1139,1199,1259,1319,1379,1439,1499,1559,1619,1679,1739,1799,1859,
1919,1979,2038,2098,2158,2218,2278,2338,2398,2458,2518,2578,2638,2698,
2758,2818,2878,2938,2997,3057,3117,3177,3237,3297,3357,3417,3477,3537,
3597,3657,3717,3777,3837,3897,3957,4016,4076,4136,4196,4256,4312,4372,
4432,4492,4530.

Native dimensions are retained; RGB conversion is a display derivative, not
photometric calibration. SAR is absent, not authenticated1:1. All decoded
frames report progressive, not evidence of the original camera scan mode.
Timestamp gaps at source indices4302/4303 are267/133ms; retain them as encoded
gaps without imputing lost camera frames. Last video frame starts302.602s,
while container duration303.102s includes other timing metadata. Do not use
the latter as the last visible frame time.

The upstream FFmpeg n7.1.1 yuv2rgb.c source was acquired (46,246bytes,
SHA256f0a61e340defcbb193f51d9f8c7faed727cc89987d2786551f6a966458f8f29b).
Lines561–578 log the observed missing-accelerated-converter warning; the
non-YUV422P branch at622–638 returns yuv2rgb_c_24_rgb for RGB24. Thus this exact
warning is a software-fallback notice, not itself a corrupt-frame report.
This version-tag source is not a byte-for-byte attestation of the installed
binary. Two additional native-yuv420p full decodes have empty warning-level
stderr. Both native runs and both original RGB runs have4531 matching PTS rows
and identical within-format checksum sequences. Pixel format byte sizes match.
Only this exact swscaler warning is allowed after review; any other diagnostic
or nonzero subprocess status refuses image admission. Original warned runs
remain labeled as such, not retrospectively clean.

Before historical extraction, test the selection path on the preserved
125-frame synthetic FFV1 fixture (source SHA256
03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6), indices
0,60,120,124, expected solid red/green/blue/blue,96x64. This checks a bounded
selection path, not WMV decoding or unique identity within same-color spans.
Each historical PNG must independently match the corresponding full-stream
RGB framemd5 row, dimensions and selected index. Repeat into a new directory;
compare decoded pixels and image-file hashes. This does not authenticate the
original camera's color, cadence, chronology or scene identity.

Root and observer inspect all77 admitted images at native resolution and
save standalone descriptions before receiving each other's findings. Use
sample-order plus source-index/PTS pins. Then compare a separately named prior
Dub5 15 anchor; do not promote resemblance to exact source identity. Sparse
screening cannot rule out short intervening fire views. Declare additional
coverage before attempting a whole-file content absence finding.
