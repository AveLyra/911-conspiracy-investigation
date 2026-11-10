# Silent-input control failed; court speech was not transcribed

**This is a test of our reading method, not a finding about 9/11.** The installed recognizer produced **“You” from ten seconds of all-zero audio samples**. That failed the predeclared control, so the planned court-audio passes were stopped. No words from the court audio were newly transcribed or authenticated.

## What was actually tested

On November2,2026, a WAV containing160000mono samples at16000Hz/16bits was generated directly from320000zero bytes. A separate file inspection of that saved WAV confirmed every sample byte was zero, the header fields and the10second duration. WAV SHA-256: `ee7bea4232762775f8fce9b3e27e4d3948c8ac6a45a87ca769f703d6eed0b448`.

One local **whisper.cpp1.9.2 /base.en** pass used CPUonly, English,4threads/1processor, temperature0 and no temperature fallback. No initial prompt, desired words, grammar, VAD or translation was supplied. The OS process profile denied network; the permission probe returnedEPERM. Existing installed tools/weights were reused, with no download or source upload. [CONTROL-RESULT.json](CONTROL-RESULT.json) pins the exact engine/model/input/output hashes, command template, timing, options and observed outcome.

Inference exited0, but its text file contained `You` followed by a newline. **Successful execution and a passed control are different outcomes.** The frozen criterion required empty stripped text. The observed nonempty output therefore failed that criterion; it was not erased, excluded, retuned or rerun to obtain a pass.

## What stopped, and what remains unknown

The source court archive was checked before and after the job. The intended Ong event/stream payload extraction and both speech passes were **never reached**. The only new derived audio was the synthetic silent WAV; the only inference directory was the silent-control run. No Flash/ActionScript was executed, no actual call was played or submitted to the recognizer, and no court-word timing, voice or source identity was measured.

The [preceding printed-passage comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/a8b410fc96d29f50f9c134f87acb0822eedc8961/investigation/broader-evidence/telephone-playback-text-comparison-2026-11-02/README.md) preserves the **I'm number five /Our number5**, speaker-label, cockpit-question and **Somebody/nobody** differences, with their agreements and alignment limits. This failed synthetic control supplies **no new reading of any of those passages**, selects neither printed account and changes no historical conclusion.

One false word on synthetic silence does not estimate the recognizer's speech-error rate or show that every transcript it generates is wrong. Conversely, repeating a plausible word is not independent authentication. A different engine/platform/configuration could behave differently; that was not tested. We did not alter this probe's settings, switch models or run additional controls after its failure. The result is a reason to keep machine text provisional, not a cause assigned to the historical source differences.

## Reproduction and scope

[reproduce_control.py](reproduce_control.py) provides the control-only command with exclusive output creation, pinned engine/model checks, an explicit network-denial probe and no source-media input. Supply the matching existing engine and model paths; no automatic downloads or installation. The original full pipeline executed the documented call. This standalone wrapper was syntax-checked and compared to its options, **not rerun** after the frozen stop condition. Its WAV generator was separately checked in memory against the actual input bytes.

The observed engine binary SHA-256 is `40bca494d49af736058eb3f33cbcebaa020eacf6d0087b623f334946e1ab2128`; model SHA-256 `a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002`/147964211bytes. These identify the tested assets; they do not promise identical output on other installations. Public files include selected synthetic results and authored reproducibility material, excluding raw logs, machine transcript files, court audio, model weights and private case data.

The native session/CD/tape/copy/custody/segment records and independent source listening needed to test the printed differences remain missing. Existing FAA correction/disposition, telephone native/release/operator/recipient, recorder configuration/paired-output/clocks, materials specimen/calibration and steel preservation/attribution/review-delivery requirements remain open under their original criteria. [OPEN-TODOS.md](OPEN-TODOS.md) retains all18IDs. Neither this control nor publication completes those requirements.

[CHECKLIST.md](CHECKLIST.md), [REVISION.diff](REVISION.diff) and [VERIFICATION.json](VERIFICATION.json) separate the failed method control from successful preservation checks. The diff adds this methods note after a preserved copy of the preceding report; that report, its sources, all conflicting words and public history remain unchanged. No independent historical audit or main-branch adoption is claimed.
