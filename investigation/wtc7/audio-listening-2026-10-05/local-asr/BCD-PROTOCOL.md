# Remaining excerpt speech drafts

October 5, 2026. Declared before processing B, C or D with the local speech
model. This is review preparation under the resumed investigation goal,
not an accepted sound-event measurement. The preceding A trial is unchanged.

## Fixed inputs and method

| ID | Preserved stereo WAV | Duration | Decoded track interval | Source |
|---|---|---:|---|---|
| B | msnbc-stereo.wav | 38 s | [578,616) s | VID-WTC7-007 |
| C | edited-stereo.wav | 25 s | [430,455) s | VID-WTC7-007 |
| D | comparator-stereo.wav | 17 s | [8,25) s | VID-DEM-002 |

Paths and hashes follow the unchanged [source check](../source-check.md) and
are explicit in the runner. B and C share a compilation; D is the Capital
One/Hertz comparator, not WTC7. The source offsets are not original camera
times. Prior source knowledge means the analysis is not blinded.

Reuse the successful A route: pinned cached large-v3-turbo Q5_0 model,
whisper.cpp 1.9.2, GPU, English, four CPU threads, one processor, temperature
zero, no temperature fallback, beam/best-of five. No prompt, vocabulary,
grammar, translation, VAD, downloads, credentials or uploads. Preserve original
stereo; create equal-channel-average 16 kHz PCM16 derivatives without trimming,
normalization or denoising. Record source/derivative hashes and exact commands.

Process B, C, D in that order, two unchanged runs per clip. Save native JSON,
SRT, text and execution logs for both; compare bytes and complete transcription
objects without selecting a preferred run. Each inference has a 300-second
limit. A failed clip stops its own remaining attempts; other fixed clips may
proceed. Maximum six inference attempts, no tuning or alternative model/device
search. Existing results are never overwritten.

## Acceptance and review boundary

This batch produces machine hypotheses for later listening review, not trusted
quotations or physical event timing. Empty transcription is a valid machine
output here because speech content is not established in advance; it means
the model emitted no text, not that the recording contains silence or no blast.
This differs prospectively from A's known-speech nonempty-output check.
Malformed output, invalid/nonfinite times, reversed/overlapping segments and
out-of-clip times are flagged. Retain raw output even when validation fails.
Gaps in emitted segments do not establish a lack of sound.

Before execution, test the adapted duration/empty-output validator with invented
cases and verify decoding arguments against the successful A receipt. Afterward
use a separate read-only calculation to check hashes, durations, output times
and equality. This is separate code, not an independent human investigator.
No new agent reviewer or licensed acoustic expert is represented.

Write a complete per-clip disposition and a readable, explicitly unreviewed
transcript packet. Preserve potentially implausible words and sound labels
without asserting they were heard. Identical repeats may repeat the same error.
Do not use ASR sound labels such as music, bangs or applause as event detections.
Human checks of uncertain speech and actual sound observations remain necessary
before causal use. The prior unanswered nonspeech question for A remains open.

This unit ends after the three fixed clips and verification. It does not clear
other human gates, change a cause ranking, promote case facts, operate Faraday,
send feedback to an archived task, commit or push.
