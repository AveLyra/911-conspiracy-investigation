# Remaining audio transcript drafts for review

October 5, 2026. **Machine drafts, not human-verified quotations or acoustic
event detections.** Two unchanged GPU runs per excerpt produced identical
JSON, text and SRT. These drafts reduce manual transcription work; they do
not complete the investigation's sound-event review.

## Files and coverage

| Excerpt | Original stereo audio | Machine draft | Timed draft | Emitted segments |
|---|---|---|---|---:|
| B, 38 seconds | [Listen](/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/msnbc-stereo.wav) | [Text](run03-bcd/B/repeat1/msnbc.txt) | [SRT](run03-bcd/B/repeat1/msnbc.srt) | 12 |
| C, 25 seconds | [Listen](/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/edited-stereo.wav) | [Text](run03-bcd/C/repeat1/edited.txt) | [SRT](run03-bcd/C/repeat1/edited.srt) | 5, including 3 ellipses |
| D, 17 seconds, another building | [Listen](/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/comparator-stereo.wav) | [Text](run03-bcd/D/repeat1/comparator.txt) | [SRT](run03-bcd/D/repeat1/comparator.srt) | 4 |

B and C are excerpts of the same compilation, not independent sources. D is
the Capital One/Hertz demolition comparator, not WTC7. All times below are
ASR segment estimates relative to each excerpt. Their apparent decimal
precision is not a calibrated uncertainty interval or physical event clock.

## Material wording to check

**B, 6.22–11.64 seconds:** The model emits:

> Well, at first we had thought, Brian, that we'd heard another explosion,
> but I think it's just another truck that's heading down to the south.

The qualification is important to preserve alongside the initial description.
If verified by listening, it supplies a speaker's alternative interpretation
of a sound. It would not establish that a truck caused the sound or identify
the sound's actual source. The draft alone cannot adjudicate either account.
Names elsewhere in this draft also remain unverified and are not witness IDs.

**B, 24.60–38 seconds:** The model emits reactions and reassurance, including
`Look behind us`, repeated `Oh, my God`, and `We're okay`. These are candidate
words, not measurements of collapse onset, sound-arrival time or foreknowledge.

**C, 0–18 seconds:** Three segments contain only `...`, at 0–5, 5–14 and
14–18 seconds. They are not transcribed speech and must not be recoded as
silence, no blast, or a specific sound. At 18–22 seconds the draft says
`Looks like seven World Trade Center just collapsed`; at 22–25 seconds it says
`Look at this. Unbelievable.` Both require actual listening verification.

**D, 0–6 and 12–17 seconds:** The model emits `Here we go!` twice, then
`Oh! Yay!` and `Wow!`. It emits no segment for 6–12 seconds. That gap says
nothing about whether an audible demolition sound occurs there. The unrelated
building's known comparator role does not validate any model-generated word.

## How to review without reproducing all the typing

Use the original stereo clips above at comfortable volume. A first listen
without reading the draft can reduce suggestion; prior exposure is already
present, so this is not a blinded trial. Correct only what you can actually
hear and mark unclear passages as unclear. Distinguish spoken descriptions
from separate audible sounds. Approximate local times or untimed descriptions
are sufficient when precise timing is unavailable. Report actual coverage and
any playback failure; there is no need to agree with the drafts or a cause.

No human response for B/C/D is recorded yet. Excerpt A has the separately
preserved human rough transcript, but its distinct-sound question remains open.

## Method and verification

The [batch protocol](BCD-PROTOCOL.md) preceded processing. It uses the same
pinned cached model, direct GPU runtime and unprompted decoding settings as A.
The originals remain unchanged. Separate mono PCM16 derivatives use equal
channel averaging and 16 kHz resampling, with 608000, 400000 and 272000 frames
for B, C and D. No normalization, denoising or content-driven tuning was used.
All commands, identities, logs and repeat outputs are in the
[execution receipt](run03-bcd/receipt.json).

The initial Python 3.9 launch failed before inference because a hashing helper
requires a newer interpreter. Its empty directory was preserved under
`run03-bcd-launch01-empty`; the [launch note](BCD-LAUNCH-NOTE.md) records the
correction to installed Python 3.13.7. The runner and speech settings were
unchanged. The corrected self-test passed three valid and ten invalid invented
cases and matched decoding arguments to the successful A receipt.

All nine conversion/inference commands exited zero. The six inference durations
were B: 3.35/2.76 seconds, C: 1.16/1.21 seconds, D: 1.21/1.20 seconds. Both
outputs for each clip are byte-identical; no favorite result was selected.

A separate Ruby read-only check (`496a2a`, exit 0) verified all 39 product hashes
and sizes, three source hashes, recorded before/after runtime/source identity,
three PCM WAV headers/frame counts, every segment's finite ordered in-range
times, complete JSON and TXT/SRT repeat equality, nine zero exit codes and six
logs identifying actual GPU use. This is separate verification code by the
same analyst, not independent human review or proof of transcription accuracy.

Repeated model output can repeat the same error. No cause ranking, acoustic
event inventory, actual human acceptance, source authenticity, calibrated
loudness, legal fact or accepted Sherlock finding follows from these drafts.
The full investigation remains active and incomplete.
