# Local transcription of the spoken excerpt

October 5, 2026. Research only. The cached Whisper large-v3-turbo model
produced a candidate transcript of excerpt A. Two GPU runs returned identical
full JSON, text and SRT. A preceding CPU attempt timed out without a transcript
and remains preserved. This demonstrates a local speech-recognition route,
not root perceptual access, event authentication or blast detection.

## Unedited machine words

Times below are native estimated segment positions in the 18-second excerpt,
not calibrated timing bounds, word onsets or times of the described event.

| Local interval | Machine text |
|---|---|
| 0–3 s | We believe it was seven world trade. |
| 3–7 s | We had just been told that they were fearful that that building was compromised. |
| 7–11 s | All of a sudden a loud, incredibly loud explosion. |
| 11–15 s | And we have the video to show you now what happened. |
| 15–18 s | Just before we say it again, what you're seeing are high figures. |

Unchanged outputs: [text](run02-gpu/repeat1/spoken.txt),
[SRT](run02-gpu/repeat1/spoken.srt), [full JSON](run02-gpu/repeat1/spoken.json).
No output was repaired or selected from differing runs. Displayed segment
boundaries happen to be whole seconds; extra decimal places do not add accuracy.

## Comparison with the human transcript

The [user's rough transcript](../human-spoken-transcript-2026-10-05.md) and
machine version agree on the substance of the speaker's account: an anticipated
building problem followed by a described loud explosion. These are readings of
one recording, not independent witnesses or corroboration that the event occurred.

Differences are preserved, not adjudicated:

- Human `7` and machine `seven` agree in ordinary numerical meaning.
- The machine omits human `there was` and `an` in the explosion sentence.
- It repeats `that` before `building` and uses singular `video` rather than
  the human `videos`.
- Human `see it again` differs from machine `say it again`. The model adds
  `Just` and `figures`, while the human version preserves `wa—` / `—s` and ends
  at `high`. That ending is unverified, not an accepted correction or a
  demonstrated hallucination.

No word-error percentage is computed against the rough, incomplete human
reference. Rough speech markers versus machine segment starts do not establish
timing error. Actual listening could resolve particular wording; no repeat is
required merely to force agreement.

## Method and actual failures

The [protocol](PROTOCOL.md) pins source, model, executable identities and
decoding choices. Model: existing `ggml-large-v3-turbo-q5_0.bin`; runtime:
whisper.cpp 1.9.2. The Pataphor wrapper and vocabulary prompt were not used.
Neither the human transcript nor event vocabulary was fed to the model.
No upload, credentials, download, install or Pataphor transcript access was
invoked by the adapter. This is not a network-traffic audit or OS-isolation proof.

The first launch was sandbox-denied before directory creation (tool completion
`802f63`). The same command then ran with approved filesystem access. Help
took 98.35 seconds, including about 96 seconds of Metal library compilation;
conversion succeeded. CPU inference timed out after 600 seconds with no
transcript. The [CPU receipt](run01/receipt.json) preserves this failure.
A general process diagnostic was sandbox-denied; an approved Whisper-only
diagnostic showed CPU use. No hang or missing dependency was established.

The separately declared [GPU addendum](GPU-ADDENDUM.md) preceded any machine
transcript. It changed hardware and time cap, not speech settings or output
acceptance, and preserved the CPU protocol/runner. Both GPU executions exited
zero after 7.85 and 5.01 seconds. Logs identify `use gpu = 1` and the MTL0
backend. Exact commands, outputs, environment and hashes are in the
[GPU receipt](run02-gpu/receipt.json). No CPU/GPU output equivalence is claimed.

The separately preserved mono derivative is equal-channel averaged and
resampled: PCM16, 16000 Hz, 288000 frames, SHA-256
`84bf174495fbc380861a314a73295ba58754778615f26c0b4833c420d2788943`.
It loses stereo separation and is not a calibrated pressure signal. The source,
model and executable pins matched before and after both runners. Runtime
libraries were identified by installed versions/logs, not transitively pinned.

## Verification and evidentiary limit

Before inference, runner syntax and one valid/four invalid invented output
checks passed. A separate reader reviewed both runners. Both successful
outputs passed segment structure, ordering and [0,18000]-millisecond bounds.
Their complete transcription objects and JSON/TXT/SRT bytes match exactly.
Repeatability is not accuracy: both use the same weights, code and source.

The separate reader independently checked all ten GPU product hashes/sizes,
fresh input pins, runner/protocol/addendum/CPU-receipt identities, derivative
format, command equivalence apart from output paths, identical repeats and
both actual GPU logs. That read-only Python/hashlib/json/wave check exited zero.
The reader independently identified the same wording disagreements. This is
an AI technical review with shared source access, not a second human listener
or an independent recording; no new inference was run for that review.

Human/machine agreement supports the transcription of the speaker's explosion
account. It does not identify an explosion audible at 7 seconds. No nonspeech
event, reliable nondetection, speaker identity, original synchrony, sound
pressure, device mechanism or collapse cause is established. B/C/D remain
outside this ASR trial. An outstanding question asks whether the user noticed
any abrupt sound separate from speech; no answer is inferred.

This new capability can aid further speech passages. Acoustic-event work
still needs actual sound observations and source/detection analysis. No
cause ranking, accepted Sherlock finding, legal promotion, commit or push
changes. The generic cached-route/prompt-isolation lesson is queued locally
under existing SFB-002/SFB-005; archived feedback routing remains unresolved.
