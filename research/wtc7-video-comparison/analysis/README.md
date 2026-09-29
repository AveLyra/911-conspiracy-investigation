# Audio-analysis derivatives

This directory contains reproducible screening derivatives. None is a preserved source object or a calibrated acoustic measurement.

## Files

- `audio_window_plot.py` decodes a requested source interval to temporary 44.1 kHz, mono, 32-bit floating-point PCM; calculates a 2 ms peak envelope; and plots a 2,048-sample Hann-window spectrogram with 1,792-sample overlap.
- `figures/27-angles-spoken-explosion-reference.png` covers compilation time 00:58-01:16.
- `figures/27-angles-msnbc-segment.png` covers 09:38-10:16.
- `figures/27-angles-peskin-segment.png` covers 07:10-07:35.
- `figures/hertz-confirmed-implosion-control.png` covers 00:08-00:25 of the comparator.
- `transcripts/27-angles-whisper-base-en.json` is an uncorrected Whisper `base.en` transcript used only to navigate the compilation. It contains recognition errors and is not filing-ready.

The waveform scale is digital full scale, not sound-pressure level. The spectral scale is referenced to decoded full scale and is useful for within-file morphology, not for reconstructing physical loudness at the camera.

## Reproduction example

```sh
MPLCONFIGDIR=/private/tmp/wtc7-mpl python3 analysis/audio_window_plot.py \
  "media/compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f140.m4a" \
  analysis/figures/example.png \
  --start 58 --end 76 \
  --title "27 Angles audio window" \
  --marker "66.000=spoken phrase begins"
```

Run the example from the package root. Requirements are `ffmpeg`, Python 3, NumPy, SciPy, and Matplotlib.

The 2026-09-02 derivatives were produced with FFmpeg 7.1.1, Python 3.13.7, NumPy 2.3.4, SciPy 1.16.2, and Matplotlib 3.10.7. Integrated loudness and true peak were screened with FFmpeg's `ebur128=peak=true` filter.

## Integrity

The source hashes are in [`../media/SHA256SUMS`](../media/SHA256SUMS). Derivative hashes are in [`SHA256SUMS`](SHA256SUMS). Regeneration may change PNG bytes across library versions even when plotted data are substantively the same.
