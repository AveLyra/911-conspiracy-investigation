# Reproduce the local same-decoder signal comparison

Requirements: Python3 with NumPy and installed FFmpeg/ffprobe. The recorded run used Python3.12.14, NumPy2.3.5 and FFmpeg/ffprobe7.1.1. No SciPy, playback, external service or media output is required. Input is the unchanged official court flights.zip with its exact pinned hash.

The helper is the previously published [reproduce_resources.py](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/reproduce_resources.py). Its pinned functions are imported without running its main/decoder routine. A full checkout supplies the default sibling path; otherwise pass it explicitly:

```sh
python3 compare_decoded_signals.py /path/to/court-flights.zip --helper /path/to/reproduce_resources.py --ffmpeg ffmpeg --ffprobe ffprobe > result.json
```

The script verifies archive/member/payload/helper hashes, runs sign/gain/DC and unrelated-noise controls, decodes in memory, computes the fixed global and local comparisons and prints numeric/hash metadata. It never runs a SWF, listens, sends data or writes media. It stops on mismatched inputs, failed decoders, nonfinite signals, unsupported channels, >300-second streams or FFT size >2^22. Commands and actual software versions are in the result.

The analysis view is a disclosed resampled copy, not original evidence. Source SeekSamples/player timing are not applied. Use the supplied lag convention; do not interpret array seconds as attack timestamps or correlation as a percentage of proof/words.

Retain full outputs unmodified. The predeclared reproduction comparison excludes only each decoder's stderr strings; compare all other discrete/string/hash fields exactly, and floating values at absolute tolerance1e−9. Variable decoder addresses and floating computation/build details can change full stdout hashes; every full-run fingerprint remains a preservation observation, not a universal expected output. Do not suppress numeric/hash disagreements to obtain a pass. Reproducing this method is not independent decoder/source authentication or a historical cause test.
