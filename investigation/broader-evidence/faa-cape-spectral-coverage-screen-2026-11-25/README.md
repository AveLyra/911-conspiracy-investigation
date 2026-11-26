# Cape audio: preselected spectral coverage screen

2026-11-25. A wider sample of file offsets did not reproduce the approximately **2349.2–2349.3-second** candidate shift reported for five adjacent windows in the [prior spectral test](https://github.com/AveLyra/911-conspiracy-investigation/blob/9c8b0a2472ef7bdda6a04fd3ef53a877e3daea37/investigation/broader-evidence/faa-cape-spectral-control-2026-11-25/README.md). The previous finding remains a **local candidate correspondence**; neither result establishes whole-file coverage, a UTC alignment or absence of audio.

## Method and observations

The [screen script](spectral_screen.py) uses the predecessor's 2-kHz mono, log-spectral discrete-cosine features and normalized search over the entire K90-30 MP3. Before running, it selected 16 ten-second windows at the K90-39 file offsets below. All best peaks, including weak peaks, are reported; there was no acceptance threshold:

| K90-39 offset s | Best K90-30 offset s | Difference s | Score |
|---:|---:|---:|---:|
|100|2951.6|2851.6|0.199218|
|400|1498.5|1098.5|0.168619|
|700|4067.4|3367.4|0.231907|
|1000|1279.2|279.2|0.153749|
|1200|2026.3|826.3|0.184571|
|1400|899.9|-500.1|0.121504|
|1600|1499.0|-101.0|0.192587|
|1800|1696.4|-103.6|0.159365|
|2100|3529.1|1429.1|0.130948|
|2500|2920.1|420.1|0.143293|
|3000|4051.0|1051.0|0.403204|
|3500|3574.9|74.9|0.490520|
|4000|932.2|-3067.8|0.328461|
|4500|3730.5|-769.5|0.348283|
|5000|1650.7|-3349.3|0.136663|
|5500|3797.5|-1702.5|0.199765|

The earlier five adjacent queries at **1453–1493** seconds yielded the approximately **2349.2–2349.3** shift. This screen's nearby **1400** and **1600** samples yielded different best peaks and low scores. The gap between the sampled windows was not tested. Results may reflect non-overlapping source material, quiet or repetitive audio, changes in content or speed, recording/encoding differences, or limitations of the method; those possibilities remain untested. The screen supplies no calibrated negative distribution or threshold, and a best peak is not automatically a match. The 16 searches and the earlier five are not independent evidence of historical events.

The approximately 1253 UTC attribution still rests on an unverified automated speech-recognition/transcript candidate; it is not a calibrated clock. The screen cannot determine whether **1315–1345 UTC** exists in K90-39, whether silence was cut, or whether the **1538–1540** DAT gap is covered. Human listening, independent timing anchors, original source tapes, item-level custody and controls with known matching/nonmatching material remain TODOs. The FAA corrected answer and administrative disposition remain separate outstanding work.

## Reproducibility and provenance

NARA [K90-30, NAID 7598879](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/b-Voice-Recordings/5-K90-30-Sup-Console-1229-1253-UTC%3B-Flight-Data-1229-1253-UTC%3B-High-AR-1247-1259-UTC.mp3), SHA-256 `9095c0b717eb3820df1f509329ffdad0fc7a42b05a8d7a04ae2bf939b986a20c`; [K90-39, NAID 7598886](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/b-Voice-Recordings/5-K90-39-High-AR-1230-1400-UTC.mp3), SHA-256 `6c8c16d52e09fea2877dd798dbbffd6823e626f09f58cadf022d05b7425a9b37`; both retrieved 2026-11-25 and retained in the verified media store. Script SHA-256 `14d1bf480a833fc34ef1d051b3de76b386ea0d161048dbe8a11594bff6ca3a0d`. Set `CAPE_AUDIO_ROOT` to a directory containing the filenames shown in the script; use FFmpeg 7.1.1, NumPy 2.3.4 and SciPy 1.16.2. The result table is the output of one run; the predecessor's five-window and internal control results remain unchanged. No audio, transcript or feature output received human listening verification.
