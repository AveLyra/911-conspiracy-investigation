# Local speech transcription protocol

October 5, 2026. Prospective for this new ASR run, after receipt of the human
rough transcript. Research only; neither the analyst nor the source selection
is blinded. This is separate from the original failed root listening trial.

## Scope and acceptance

Transcribe only the held 18-second `spoken-stereo.wav`, using Pataphor's
existing quantized Whisper large-v3-turbo model and whisper.cpp 1.9.2. Do not
run Pataphor's wrapper, read its lexicon, load credentials, install/download,
upload audio, modify Pataphor, or feed the human words as a model prompt.
This is machine speech recognition, not root auditory access or blast detection.

Pins before execution:

- Source SHA-256: `5b12b06ab0f2699539e5621b8483d9c96163364cabdace3768c8b296240de127`.
- Model SHA-256: `394221709cd5ad1f40c46e6031ca61bce88931e6e088c188294c6d5a55ffa7e2`.
- whisper-cli SHA-256: `40bca494d49af736058eb3f33cbcebaa020eacf6d0087b623f334946e1ab2128`.
- ffmpeg SHA-256: `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`.

The Pataphor downloader names Hugging Face `ggerganov/whisper.cpp` revision
`5359861c739e955e79d9a303bcbc70fb988958b1`. This is intended provenance from
local code, not a newly verified remote model digest or historical training audit.

## Preprocessing and decoding

Preserve the stereo source. Make one separately hashed 16 kHz mono PCM16 WAV
using FFmpeg 7.1.1, with explicit equal-channel averaging (0.5 L + 0.5 R), no
normalization, denoising, trimming or speed change. This derivative loses stereo
separation and cannot serve as a calibrated acoustic-pressure measurement.
Require 288000 frames, one channel, 16000 Hz and 16-bit samples before inference.

Call the native local CLI directly: English transcription, CPU, four threads,
one processor, temperature zero, temperature fallback disabled, beam size five,
best-of five, no initial prompt/grammar/translation/diarization/VAD. Save native
full JSON, SRT, text, stdout/stderr and exact command/environment settings.
Untouched CLI defaults remain identified by the pinned binary/help record.

Run twice with identical settings and the same audio, changing only output
directory. Do not select a preferred result or tune settings after reading it.
Compare complete transcription objects and output bytes; preserve disagreement.
Maximum is two inference attempts, each with a 600-second timeout. A failure
stops this route with its receipt; no automatic alternative model or repair loop.

Success means source identity, conversion dimensions, valid output schema,
recorded execution and repeat comparison, not proven word accuracy. Check
segment offsets for ordering and coverage within [0,18000] milliseconds;
flag invalid/unresolved timing rather than accepting it. Model/token scores
and decimal timestamps are not calibrated confidence intervals.

Compare the frozen machine words with the separately preserved human version.
Report agreements and omissions/substitutions. Do not compute an accuracy rate
against this rough, nonverbatim reference. Speech describing an explosion is
not evidence that an explosion is audible at that speech timestamp. Nonspeech
events, speaker identity, source authenticity and physical cause remain separate.

## Verification and limits

Before execution, syntax-check the runner and independently inspect its scope,
pins, commands and output policy. The runner exclusively creates its run
directory and never overwrites an earlier run. Afterward check preserved inputs,
receipt exit codes, model output, time bounds and repeat equality. No real-world
timing calibration or ASR accuracy control is supplied by this single excerpt.
Human listening now supplies a comparison, not a complete acoustic-event review.

No source promotion, accepted Sherlock finding, Faraday export, legal edit,
commit, push or external transmission follows. B/C/D are outside this run.
