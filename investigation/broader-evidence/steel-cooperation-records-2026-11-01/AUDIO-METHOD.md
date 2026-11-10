# A01 audio: recovered outputs do not authenticate the words

The verified Intel store became available again. Existing files were inspected **without rerunning inference**. Source, model, derived WAV and executable hashes matched the saved launch. The earlier file-open failure and unmounted-share observations remain preserved; their exact cause, onset and relationship are unknown.

The prior FAA package review preserves two aircraft descriptions, B767 and B757. Neither is selected here. [Earlier report, D04/D08](https://github.com/AveLyra/911-conspiracy-investigation/blob/ca224c35d97a1aac5d885e8a85bc76fc3d08a037/investigation/broader-evidence/faa-package-version-review-2026-10-27/README.md); [official A01 source](https://catalog.archives.gov/id/7595603).

| Machine-output observation | Baseline | Text-context control |
| --- | ---: | ---: |
| Segments | 119 | 84 |
| Segments labeled exactly `(music playing)` | 40 | 0 |
| Segments over 500 characters | 0 | 1 |
| Zero-length model intervals | 0 | 1 |
| Matches to the declared aircraft-word pattern | 0 | 0 |

These are statistics about machine output. They do not measure word accuracy, establish music or silence in the source, prove an aircraft word absent, identify a speaker, or calibrate a historical clock. Repetitive strings and unverified non-speech labels were retained. Different machine text from the same bytes is not evidence the source recording changed.

The baseline subprocess returned 0. The control wrapper returned 1 while hashing its outputs and never wrote the intended receipt. Its internal inference exit code remains unavailable. Five control artifacts now exist, its JSON parses, and its log contains saving/timing messages; those observations do not substitute for the missing exit-code receipt. No successful control exit is asserted.

Both passes used the same full-file 16 kHz signed16-bit mono derivative, local whisper.cpp 1.9.2, pinned base.en weights, English, four CPU threads, temperature 0, no temperature fallback, no initial prompt, grammar, VAD, denoising or target-word hints. The second pass changed maximum text context to 0. Inference used a process sandbox denying network access. No source audio was transmitted.

The original stereo-channel diagnostic also found unequal full-stream processed channel hashes and RMS values. It did not identify which channel carried speech, code or another signal, select a preferred channel, or decode a time signal. No further ASR tuning or channel-specific transcription was performed in this recovery.

Sources A01/MODEL/WAV/TOOL/RUN119/RUN84 and the exact locator pattern are pinned in [SOURCES.json](SOURCES.json). Raw audio, transcripts, output logs, weights and machine-attributed speaker names remain outside this publication. Direct listening/independent checking and custody/clock joins remain necessary. This methodological result supplies no missing FAA corrected QFR, signed personnel decision or recorder/materials acceptance criterion.

A matching command specification (replace path placeholders with the pinned inputs) is:

```text
ffmpeg -v error -nostdin -n -i SOURCE -map 0:a:0 -ar 16000 -ac 1 -c:a pcm_s16le WAV
whisper-cli -ng -m MODEL -f WAV -l en -t 4 -p 1 -tp 0 -nf -ojf -otxt -osrt -of BASELINE_OUTPUT
```

The control uses the same inference command with `-mc 0` and a different output prefix. The actual inference commands were wrapped in the recorded network-denying process sandbox. Remaining tool defaults included five beams/best-of-five. These commands document the performed local method; this publication's verifier does not download or run inference. Hardware/library differences and unverified source speech limit any exact-text reproduction claim.
