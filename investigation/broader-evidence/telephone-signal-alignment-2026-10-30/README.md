# Court audio representations: strong overlap correlation, incomplete coverage

October 30, 2026. AUD016-A1 / TC05-B105 / TC06-B110 / TEL02. New local same-decoder signal test. **Local reviewed candidate; no public push is claimed.** The original-record plan, all five tracks and eighteen substantive criteria remain open.

## What the test found

The previously identified event-resource and root-stream MP3 bytes differ in both files. **Their decoded comparison signals nevertheless show strong correlation over a fitted overlap:** about **0.958 for Lyles.swf** and **0.916 for Ong.swf**. All 28 tested ten-second windows favored zero additional local shift within the predefined local search. This supports related signal structure across those overlaps. It does not establish identical words, full recordings, speaker identity, authentic source provenance or what the presentation actually played.

The Ong event resource also has an unmatched tail of **51,800 samples in the derived 8,000-Hz view**, nominally **6.475 seconds**, after the fitted overlap. Its content was not listened to or classified. Do not call it silence, removed speech, fabrication or an export artifact. Both the strong matching structure and the coverage difference must be retained.

This weakens an interpretation that the earlier byte nonmatches alone demonstrated unrelated audible content. It does not resolve why the representations differ. Re-encoding, latency/padding, content selection and other preparation differences remain hypotheses, not adopted explanations.

## Original inputs and actual scope

Only two archive members, **Lyles.swf** and **Ong.swf**, were read from the held [official court ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip), SHA-256 **3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801**. Member names are source labels, not identities authenticated here. The long root DefineSound1 resource and concatenated root MP3 streaming payloads were reconstructed with the existing bounded tag walker, and verified against the exact hashes in the [preceding static comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/39b64108cf112760b162bd176a6d4c80a86c55ca/investigation/broader-evidence/telephone-sound-controls-2026-10-30/README.md).

No source audio or SWF was overwritten, trimmed, corrected or selected as the true record. Each MP3 sequence was decoded to original-rate/channel signed16 PCM in memory; its sample count and hash were retained. Separately, FFmpeg generated a **derived mono 8,000-Hz float32 analysis view** for comparison. This resampling is a disclosed transformation for the test, not replacement evidence or a corrected duration. All original fields and source byte differences remain preserved.

SWF SeekSamples, root-frame delays, envelope/button/action behavior and per-block player seeking were **not applied**. Concatenated stream decoding is not an actual Flash playback reconstruction. No audio was played, listened to, transcribed, uploaded or saved as a new media file. No voice/caller, carrier-event, operational clock, source-custody or historical-cause authentication was performed. Recorder/materials-owner technical work was not duplicated.

## Predefined method and controls

The protocol and polarity clarification were saved before decoding. The search used overlap-local Pearson correlation, nominal lags within **±30 seconds** of the derived view, at least **80% of the shorter view** and at least **30 seconds** overlap. It retained greatest signed and greatest absolute coefficients with polarity, using the latter for indexing. Lag convention: **event[k + lag] aligns with stream[k]**. The strongest alternative outside ±0.25 seconds of the peak was recorded as an ambiguity diagnostic, not a probability.

Consecutive full **ten-second windows** covered the overlap; each had a local ±one-second search with at least 90% overlap. The leftover partial window was explicitly reported, not silently counted as a full-window test. Pearson centering is part of the comparison statistic; it does not change stored originals. Numerical values are descriptive, not confidence levels or percentages of identical content, conversation coverage or proof.

Before source data, deterministic cropped/gain/DC and inverted-polarity controls recovered the expected **+137-sample lag**, with signed correlations near **+1 / −1**. The unrelated-noise control's maximum absolute correlation was **0.0185523**, below the predefined 0.1 bound. Selected FFT coefficients agreed with direct overlap Pearson calculations within the fixed **1e−9** tolerance. These control algorithm indexing/numerics, not recording provenance or the likelihood that a real unrelated recording would match.

Actual invocation versions: **Python 3.12.14, NumPy 2.3.5, FFmpeg/ffprobe 7.1.1**. SciPy was not installed or used. This is one decoder family; it is **not independent decoder validation**. The helper is reused code, not an independent parser implementation. Earlier software-version and independence qualifications remain preserved.

## Results — all units and nonmatches retained

| Observation | Lyles.swf | Ong.swf |
|---|---:|---:|
| Event PCM samples / decoded rate | 1,987,200 / 44,100 Hz | 2,729,664 / 11,025 Hz |
| Stream PCM samples / decoded rate | 498,240 / 11,025 Hz | 2,658,240 / 11,025 Hz |
| Event analysis-view samples | 360,490 | 1,980,709 |
| Stream analysis-view samples | 361,534 | 1,928,882 |
| Best signed correlation | **0.9578656805** | **0.9163875372** |
| Fitted lag, analysis samples | **−1,185** | **+27** |
| Same lag divided by analysis rate | −0.148125 s | +0.003375 s |
| Overlap, analysis samples | 360,349 | 1,928,882 |
| Event unmatched prefix / suffix | 0 / **141** | **27 / 51,800** |
| Stream unmatched prefix / suffix | **1,185 / 0** | 0 / 0 |
| Full ten-second windows | 4 | 24 |
| Window correlation range at global alignment | 0.9344818–0.9674526 | 0.8729159–0.9452028 |
| Best additional local lag in every full window | 0 samples | 0 samples |
| Partial overlap tail outside full-window test | **40,349 samples** | **8,882 samples** |
| Strongest alternative outside peak's ±0.25 s | −0.0153938 at −21,829 samples | +0.0077227 at +34,378 samples |

Seconds in this table are **nominal analysis-array units**, not a calibrated historical call clock. Only the specified lag range/overlap/window conditions were tested. Stable best local offsets do not exclude brief edits, changed words, low-energy differences or other untested runtime processing. Whole-overlap correlation includes the partial tail, but that tail received no separate ten-second local-lag test.

Event PCM hashes reproduce the prior standalone decoder results. Each stream PCM count equals the previously parsed sum of its root block SampleCount prefixes. Those are positive consistency observations, not proof the entire call is present. The prior Ong **2,880-sample decoded-versus-declared** difference and event/stream seeking and rate fields remain unchanged. We did not subtract metadata values or apply them to force agreement with the fitted lags.

[RESULTS.json](RESULTS.json) retains all 28 window rows, signed/alternative peaks, exact overlap/unmatched ranges, source/PCM/view hashes, amplitudes, controls, versions, options and limits. It omits only decoder stderr diagnostic strings from its comparison projection; each full unmodified run log remains local with its own fingerprint. The first full log is **57,936 bytes**, SHA-256 **d4a83ea2ad412da6a4fb62aeefdeb81ddabe1e0feec2c8ff50cae284c80574f1**. It is a test-output hash, not an original recording hash.

## Interpretation, strongest objection and open questions

**Supported:** within this same-decoder, disclosed-resampling method, the two representations in each file share strongly aligning waveform structure over the reported overlap. The new data should accompany the earlier byte nonmatches when assessing that lead.

**Not established:** semantic identity, complete conversation coverage, innocence or deception, exact export/encoding cause, original speakers, source custody, carrier call records, or historical timing. Pearson correlation can coexist with different words or unmatched material. Related copies and dependent tests are not independent corroboration. The unmatched Ong tail is a specific remaining target, and high correlation does not authorize explaining it away.

The next discriminating inputs are original/received recordings, edit/export/source-member mappings, authoring/runtime documentation, custody/release and exhibit-construction records, and actual carrier/operator/recipient/clock joins. A separately scoped examination of unmatched regions could characterize their signal properties; their content has not been established. [OPEN-TODOS.md](OPEN-TODOS.md) preserves these and the other track dependencies.

## Preservation, reproduction and publication state

[compare_decoded_signals.py](compare_decoded_signals.py) and [REPRODUCE.md](REPRODUCE.md) define the fixed computation. A second run must preserve full logs and compare every non-diagnostic field, exact for bytes/hashes/counts/versions/parameters and within 1e−9 for floating metrics. Only raw decoder stderr, which can include variable memory addresses, is omitted from that explicitly defined comparison projection; it is not erased from the full logs. An actual reproduction receipt is separate from a promised pass.

[SOURCES.json](SOURCES.json), [CHECKLIST.md](CHECKLIST.md), [REVISION.diff](REVISION.diff) and [MANIFEST.json](MANIFEST.json) retain source locators, requirement outcomes, exact additive text/code/results changes and companion hashes. Earlier source reports and discrepancies remain frozen. No public push is claimed: the existing AveLyra SSH identity was not listed by the configured agent in the current read-only check; authentication restoration is a publication TODO, not a reason to alter credentials or use another identity.
