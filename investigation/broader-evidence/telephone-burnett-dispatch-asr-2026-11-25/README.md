# Burnett dispatch audio: machine-generated timing lead

**Status: automated speech-recognition output, not human-verified audio or an authenticated dispatch timestamp.** November 25, 2026. This additive test follows the [file acquisition report](https://github.com/AveLyra/911-conspiracy-investigation/blob/a26cd42d3f756cb0d2d82ddfa4bb831a36c93651/investigation/broader-evidence/telephone-burnett-dispatch-acquisition-2026-11-25/README.md). It preserves the earlier observations and does not replace a listening review.

## Reproducible test and observation

Input: the [publisher-linked MP3](https://www.motleyrice.com/sites/default/files/documents/AT_HR/9-11/Deena%20Burnett%20Call%20to%209-1-1.mp3), SHA-256 `53fac6f2677962585b07c845059d76f89c48ec931995146c4e85550b29fef79a`, duration 138.396750 seconds. We used whisper.cpp 1.9.2 on CPU (`-ng -t 4`), English base model [`ggml-base.en.bin`](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin), SHA-256 `a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002`; output JSON SHA-256 `c70379464af4e255a8f57fe3cb534336014460c9ea2ef2d35320dd1ef0570e3b`. The input, model and unreviewed machine output were retained locally; the raw transcript is not republished.

The model output places a possible spoken date/time announcement across its **01:58.160–02:16.400** segments, transcribing a date of **September 11, 2001**, and a possible ending time of **06:33:48**. This is a *candidate produced by software*, not a verified quotation: it can mishear words, times and speaker turns, particularly on telephone audio. The same pass visibly misrecognized other words and a name, demonstrating that its output requires independent checking. Its segment boundaries are generated timestamps, not precise word onsets. No listener has verified what was actually said or whether this is a system announcement, which clock it uses, or which event it marks.

For reproduction, invoke `whisper-cli -ng -t 4 -m MODEL -f AUDIO -oj -of OUTPUT` using the hash-matched files. Program version, model, settings and file hashes are recorded; deterministic equality across platforms is not assumed. This is an automated analysis of a publisher's copy, not independent corroboration of its contents.

## Conflicting and distinct records

- The [publisher's September 2022 article](https://www.motleyrice.com/news/september-11-remembrance-legacy-courage) places a call to a dispatcher at **9:28 a.m. (EST)** and links this audio.
- Its separately linked [typed-account scan](https://www.motleyrice.com/sites/default/files/documents/AT_HR/9-11/Deena%27s%20typed%20notes%20of%20her%20call%20w%20Tom.pdf), page 1, labels a 911 call **6:31**; the earlier visual review found no stated time zone.
- The machine's unverified candidate is an **ending** time of **06:33:48**, not an independently established start time. Do not normalize, reconcile, or treat these labels as measurements of one clock or one event. Both written items appear on the same publisher's page and are not independent corroboration.

## TODO

A qualified listener should check the last 40 seconds against the audio, preserve a timestamped correction, and identify the audible wording without assuming a speaker or time zone. Compare the entire audio with the article only after actual listening. Obtain the original recording, custody/transfer records, dispatcher event log, recorder clock definition and calibration, and any source-to-publication edit history. Until then the candidate is not evidence that the recording is complete, that its time is correct, or that discrepancies reflect alteration or wrongdoing. The original dispatch and carrier records remain open.
