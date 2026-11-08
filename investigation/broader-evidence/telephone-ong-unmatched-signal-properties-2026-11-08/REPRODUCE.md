# Reproduce the bounded numerical result

Use Python3 with NumPy and installed local FFmpeg/ffprobe. The recorded run used Python3.13.7, NumPy2.3.4 and FFmpeg/ffprobe7.1.1. No SciPy, speech service, browser/Flash runtime, playback or media output is required.

Obtain the unchanged [court archive](https://coop.vaed.uscourts.gov/moussaoui/flights.zip) and the exact [previously published helper](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/reproduce_resources.py). Their SHA256 values must match SOURCE-PINS.json. Follow applicable local media/storage rules; the source archive is large media. Keep original bytes unchanged. No network access is performed by the analysis program.

```sh
python3 inspect_suffix.py --controls-only
python3 inspect_suffix.py /absolute/path/to/court-flights.zip --helper /absolute/path/to/reproduce_resources.py --ffmpeg /absolute/path/to/ffmpeg --ffprobe /absolute/path/to/ffprobe > result.json
```

The first command runs synthetic checks only. The second reads one member, gates source/native/view hashes before using the old fitted range, and prints aggregate JSON. It saves no audio, arrays or source media. With the recorded software and exact script, result.json SHA256 was **19476cfdc2bc6c19ac97194d394bfbb204ad67b1365d4376c9c213b65a363d65** in both executions. Different software may change numeric formatting or metrics; a source/native/view gate failure stops the old-region measurement and must be preserved, not corrected by modifying input.

No global alignment fit, prior28-window search, streaming decode, source seeking, actual player behavior, semantic content, caller/custody/clock authentication or AA77-specific call join is tested. Read PROTOCOL.md and README.md before interpreting results. Passing controls or equal output hashes do not authenticate a recording or establish a historical cause.
