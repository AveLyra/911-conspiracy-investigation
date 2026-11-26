# Cape TRACON recordings: spectral candidate correspondence

2026-11-25. A phase-tolerant spectral comparison found a consistent **candidate common passage** in NARA's K90-39 and K90-30 audio files. This improves on the [earlier inconclusive raw-waveform search](https://github.com/AveLyra/911-conspiracy-investigation/blob/abfb70f079e5cd14c8a8c2ad2079de875538299d/investigation/broader-evidence/faa-cape-audio-waveform-match-2026-11-25/README.md). It does **not** validate the passage's UTC time, establish completeness, or resolve the disputed 1315–1345 interval.

## Procedure and observations

Decoded both archive MP3s to 2-kHz mono samples. The scripts use short-time Fourier magnitudes, log scaling and 16 discrete-cosine coefficients, then search K90-30 using normalized feature correlation at 0.1-second frame spacing. The [single-window script](spectral_test.py) and [five-window script](spectral_multi.py) are preserved. Each of five **adjacent, non-overlapping 10-second K90-39 query windows** was searched across K90-30:

| K90-39 file offset (s) | Best K90-30 offset (s) | Difference (s) | Feature score |
| ---: | ---: | ---: | ---: |
| 1453 | 3802.3 | 2349.3 | 0.763010 |
| 1463 | 3812.3 | 2349.3 | 0.584575 |
| 1473 | 3822.2 | 2349.2 | 0.599943 |
| 1483 | 3832.2 | 2349.2 | 0.789350 |
| 1493 | 3842.2 | 2349.2 | 0.753684 |

The consistency across the approximately 50-second region supports a candidate common signal. The five adjoining windows are dependent observations, not independent recordings or five corroborating witnesses. The 0.1-second quantization and extraction/decoding conventions limit the displayed offset; no clock accuracy or drift is established. An earlier raw waveform search of the 1473-second query instead produced a weak best absolute correlation **0.220343** at K90-30 **3475.715 seconds**. Preserve both methods and results; neither peak is selected as a definitive identity without validation.

A same-file positive control searched an excerpt taken directly from K90-30 and returned **1.0 at 1000.0 seconds**. Excluding a 60-second region centered on that excerpt, its best alternative was **0.321268 at 431.7 seconds**. This is one internal control, not a calibrated false-match distribution, a realistic re-recording control, or proof that every score above it is a match. In particular, filtering, speed changes, repeated sounds and shared background could influence scores. No direct listening, independent audio authentication or source-tape comparison was performed.

## Interpretation and TODOs

The candidate K90-39 passage was previously provisionally associated by imperfect automated speech recognition with an FAA transcript labeled **1253:39–1253:44 UTC**. The new feature comparison does not independently validate that text or timestamp. The two archive files may derive from a common recording, so even a confirmed match would not supply independent evidence of the historical conversation or a verified external clock. The features cannot show that the disputed 1315–1345 interval is present or missing and do not resolve the later tape-change gap.

Listen to the corresponding clips; construct positive controls with known common speech across separate media and multiple unrelated controls; test time-stretch sensitivity and additional intervals; and compare native time codes, original DATs and custody records. Keep source description conflicts intact. The corrected FAA answer and administrative disposition remain separate TODOs.

## Provenance and reproducibility

Sources: [K90-30, NAID 7598879](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/b-Voice-Recordings/5-K90-30-Sup-Console-1229-1253-UTC%3B-Flight-Data-1229-1253-UTC%3B-High-AR-1247-1259-UTC.mp3), SHA-256 `9095c0b717eb3820df1f509329ffdad0fc7a42b05a8d7a04ae2bf939b986a20c`; [K90-39, NAID 7598886](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/b-Voice-Recordings/5-K90-39-High-AR-1230-1400-UTC.mp3), SHA-256 `6c8c16d52e09fea2877dd798dbbffd6823e626f09f58cadf022d05b7425a9b37`. Both were retrieved 2026-11-25 and remain in the verified media store. Run either script with `CAPE_AUDIO_ROOT` pointing to the directory containing the source filenames used in the script; environment: FFmpeg 7.1.1, NumPy 2.3.4, SciPy 1.16.2. Script SHA-256: single `a7dc7f67f3aae9cc50f3c9f9c2ac997935efdd7a70f747e239ca162b28574dc5`; multi `2c98c40534cfda9d74329dd806155f99e910e4c142dcce28fa7693b917ee2f61`. Results are retained locally; no media is republished.
