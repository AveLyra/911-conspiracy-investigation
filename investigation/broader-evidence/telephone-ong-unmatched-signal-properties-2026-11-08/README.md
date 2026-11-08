# Ong court-resource suffix: low energy, mostly nonzero, no exact earlier repetition

November 8, 2026. AUD016-A1 / TC05-B105 / TC06-B110 / TEL02. New bounded numerical inspection of one court-presentation representation. This completes the specified suffix energy/exact-repetition test; it does not complete the telephone original-record track or any of the five-track goal's eighteen original requirements.

## New observation and its practical limit

The previously unexamined **51,800-sample suffix** has RMS **0.00021009043497643182**, versus **0.20718791958619895** for the immediately preceding equal-length segment: a ratio of **0.0010140090956848732**, about one-thousandth. **51,290 samples are nonzero; 510 are numeric zero**, or about **0.98456%** zero. The longest exact-zero run is **456 samples**. These are properties of the specified derived mono8,000Hz float32 view, not a classification of what someone would hear.

The complete suffix and each of seven predefined blocks have **zero byte-identical, sample-aligned occurrences earlier in that same event analysis view**. All eight searches completed without reaching their cap. This rules out the narrowly specified all-zero suffix and exact earlier full-suffix duplication hypotheses in this representation. It does not exclude approximately repeated audio, re-encoding or gain differences.

**Do not treat the extra nominal 6.475seconds as established omitted speech, or call it silence, an encoding artifact, deceptive editing or added content.** No listening, semantic classification, source master, edit/export project or actual Flash playback test was performed. Low signal energy does not determine intelligibility. The origin and cause of the coverage difference remain unresolved.

## Source and transformation chain

The unchanged [official court archive](https://coop.vaed.uscourts.gov/moussaoui/flights.zip) was accessed from the identity-verified operational media store. The archive was previously acquired October27,2026; this unit re-read the held bytes, without a new network acquisition. Archive SHA256 **3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801**. Only **Ong.swf**, member SHA256 **8c844a2370852e55597a4aa73ef8b8ff0e6c03e3fec982a9cd98aeb937e5a3ec**, was inspected. Its filename is a distribution label, not authenticated caller identity. The [court item page](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200054.html) labels a combined trial presentation; that label supplies no individual recording custody chain and does not make this an AA77-specific call test.

The long root DefineSound1 tag starts at uncompressed offset **26**. Its MP3 payload has SHA256 **b1340270d0e8f4b159bb4b057ea57ec227cd021fb12dc5fd37a46b7e3e9b78b5**. The already published [pinned resource walker](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/reproduce_resources.py) was reused after code/hash inspection; it is not an independent parser. The member was passively unpacked; SWF scripts and launchers were never executed.

The earlier [signal comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/6dffea2a1a83972f3fad87c2e6ba4d39473099f8/investigation/broader-evidence/telephone-signal-alignment-2026-10-30/README.md) located an event overlap **[27,1,928,909)** against stream **[0,1,928,882)** and an event suffix **[1,928,909,1,980,709)**. Those fitted ranges were reused as qualified locators, not fitted again. No previous global correlation or28-window search was repeated. Array positions are zero-based, half-open, and are not historical clock times.

Both the native decode and derived view reproduced the exact earlier hashes before any suffix metric was accepted. Native output: **2,729,664 samples at11,025Hz**, SHA256 **3f63b0884240c467a8f3e2570314a1c2b6e814d79feb3327aff62ccab7cfc229**. Derived mono8,000Hz float32 view: **1,980,709 samples**, SHA256 **3b9b7033b8ac59b93f8a2d3bba378cf5e7e3cc581b0bf417281759d9b8063990**. Original source fields remain **declared2,726,784 samples, SeekSamples1,669 and rate_code1**; these source and decoded quantities are retained separately, with no cause adjudicated. They were already reported and are not newly discovered mismatches.

No SeekSamples/player delay, stream-block seeking, envelopes or button/action timing was applied. Earlier event/stream byte nonidentity, strong overlap correlation and unequal coverage all remain preserved. This unit decoded only the event object and did not independently revalidate the earlier stream/fit.

## Predeclared measurements and exact locators

The native prospective protocol was frozen before source decoding; its [public derivative](PROTOCOL.md) omits local coordination/status notes and retains every analytical gate, method and acceptance criterion. SOURCE-PINS records both hashes. Metrics are defined in [inspect_suffix.py](inspect_suffix.py#L39); full-pattern byte searches, sample alignment and cap in [line54](inspect_suffix.py#L54); controls in [line76](inspect_suffix.py#L76); source/hash/decode gates from [line114](inspect_suffix.py#L114); suffix/context selection from [line178](inspect_suffix.py#L178); predefined block traversal from [line184](inspect_suffix.py#L184). [RESULTS.json](RESULTS.json) retains every numeric result, command argument, software hash, control and exact sample range. [SOURCE-PINS.json](SOURCE-PINS.json) records the source relationships and reading scope.

The fixed context is event samples **[1,877,109,1,928,909)**. Suffix peak absolute value is **0.007089907303452492**; context peak is **1.187409520149231**. These float-view amplitudes were neither normalized nor converted into an audibility threshold. All sample values are finite. Numeric-zero counting treats +0 and -0 as equal; exact-byte repetition distinguishes their bit patterns.

| Event analysis sample range | Samples | Numeric zeros | RMS | Earlier exact matches |
|---|---:|---:|---:|---:|
| [1,928,909, 1,936,909) | 8000 | 0 | 0.000209113518272 | 0 |
| [1,936,909, 1,944,909) | 8000 | 0 | 0.000153230998574 | 0 |
| [1,944,909, 1,952,909) | 8000 | 0 | 0.000182551506267 | 0 |
| [1,952,909, 1,960,909) | 8000 | 0 | 0.000247336850662 | 0 |
| [1,960,909, 1,968,909) | 8000 | 456 | 0.000254521392782 | 0 |
| [1,968,909, 1,976,909) | 8000 | 0 | 0.000170603132237 | 0 |
| [1,976,909, 1,980,709) | 3800 | 54 | 0.000252140938772 | 0 |

The last block is a **3,800-sample partial block**, not another full second. Each exact search used the complete target bytes in earlier event samples **[0,1,928,909)**, excluded byte-misaligned starts and never compared the suffix with itself. There was no approximate or semantic repetition search.

## Verification actually performed

Seven synthetic checks passed before source decoding: all-zero metrics/run, constant nonzero RMS/mean, known exact-repeat locations, rejection of byte-misaligned matches, seeded random nonrepeat, signed-zero distinction and nonfinite rejection. These check implementation and indexing; they do not authenticate historical evidence.

Two executions produced **byte-identical complete JSON output**, SHA256 **19476cfdc2bc6c19ac97194d394bfbb204ad67b1365d4376c9c213b65a363d65**, with exit0 and empty process stderr. Actual environment: **Python3.13.7, NumPy2.3.4, FFmpeg/ffprobe7.1.1**. Python and NumPy differ from the earlier study's3.12.14/2.3.5; the FFmpeg/ffprobe full version-output hashes and both audio-view hashes match the earlier values. This is same-family reproducibility using reused parsing code, **not independent decoder validation**. No software was installed.

Source audio, PCM and arrays stayed in memory. No audio was played, transcribed, uploaded or saved; no waveform, voice identification or source recording was published. [Reproduction instructions](REPRODUCE.md) state the exact inputs and boundaries. The [text diff](TEXT-CHANGES.diff) compares this new unit with the immediately preceding preserved report; it does not mean that report or its open questions were overwritten.

## Interpretation, contrary possibilities and remaining TODOs

The all-zero hypothesis is contradicted by the nonzero samples. The exact earlier-duplication hypothesis is contradicted within the specified byte-equality search. Neither was an established historical finding in the prior report. This is a narrower result than identifying speech or proving an edit. Low-level recorded content, preparation/encoding behavior, player treatment and other causes remain untested possibilities; no preferred explanation is selected. A source-native master and preparation/runtime records could distinguish them.

Still unperformed: listening/transcription; approximate repetition; independent decoder/parser; actual player reconstruction; the other unmatched prefix/suffix regions; original master/custody/receipt/release/edit/export/source-member joins. The native carrier/operator/recipient records, event definitions, clocks, full Request14 delivery, usage-report attachments and source-to-call/exhibit joins remain necessary. The official Keyton interview already acquired is retained as acquired; its outstanding joins are not relabeled wholly missing. This suffix test cannot resolve AA77 zero-duration semantics or establish a complete call history.

FAA corrected QFR/receipt, signed action/no-action and separate recommendation outcomes remain open. Recorder configuration/custody/clock and materials specimen/run/native-instrument inputs retain their existing technical owners. Steel preservation decisions, inventories/transfers, building-attribution rationale and contractor review/delivery remain open. No core acceptance criterion is closed by this result. The next discriminating evidence is the source recording/preparation/custody chain, followed by the appropriate source-to-call join; a new summary or repeated hash check cannot substitute for it.
