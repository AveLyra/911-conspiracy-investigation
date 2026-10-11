# Dense transition review and audio correspondence screen

October 7, 2026. Prospective for this new stage; the earlier coarse screen is
known. Research only under the full investigation charter. No new acquisition,
cause ranking, human acceptance, historical clock or original-sound claim.

## Dense images

Use only the pinned early-copy format-133 video (SHA-256
`3f6db089b0e89cdfc030f6aaaf81227931681d26e0bd3c801b98cdcf486ba0d7`,
758,909 bytes). Extract every presented frame with file PTS in [4,7) seconds,
using the existing pinned extractor with no crop, scale, stabilization or
interpolation. Expected source indices 120 through 209 inclusive, 90 frames,
at actual 30000/1001 fps. Retain full native PNGs, all timestamps and readable
overview sheets. Inspect every thumbnail and the native adjacent pairs at
each apparent discontinuity; native pairs are selected by that observation,
not a preselected collapse explanation. Record exact picture changes and
alternatives. A file-coordinate discontinuity is not a measured physical
event gap or a finding about who edited what or why.

Run the existing synthetic tests before historical extraction, reproduce the
extraction in a separate directory, and independently check source bytes,
timestamp selection and actual PNG pixels. Preserve failures. Do not replace
the earlier 38-frame screen or any raw source.

## Audio question and inputs

Ask whether the held early-copy soundtrack contains strongly corresponding
waveform passages to excerpt C. The early input is the repair-disabled AAC
`../media/SIbqaybkbWI.f140.unmodified.m4a`, SHA-256
`0776b39a597f236c85b98b0f1dd3931cb654ab08c967d508d5bfa6fc64f145ef`.
C is main `research/sherlock-wtc7-investigation/acoustic-audit/run01/edited-stereo.wav`,
SHA-256 `b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd`.
It is a 25-second 44,100-Hz stereo float32 derivative of compilation file
coordinates [430,455), not a separately authenticated recording.

No waveform inspection or historical correlation has preceded this protocol.
Root's method proposal received separate review by
`/root/claim_index_critical_review` without historical-waveform inspection.
The corrections below incorporate its requests for precise normalization,
periodic-signal controls, nongrid shifts, inserted edits and timing limits.

Decode each entire input at its native stereo 44,100 Hz to float32 PCM,
without gain, channel mixing, resampling or filtering at decode. Preserve
source pins, exact sample counts, decoder command and output hashes. No
physical synchronization follows from nominal container start times.

## Frozen screening algorithm

1. Convert decoded samples to float64 and resample each entire file to
   6,300 Hz with scipy.signal.resample_poly(up=1, down=7,
   window=('kaiser',5.0), padtype='constant'). Retain separate L/R channels;
   no denoising, mono downmix, gain normalization or speed fitting.
2. Partition C into 25 fixed, nonoverlapping one-second blocks, [0,1) through
   [24,25). Compare each against every completely contained one-second
   window in the entire early copy, at the 6,300-Hz lag grid, for all four
   ordered C/early channel pairs. This is a scale-one screen only.
3. At each lag, use Pearson correlation: each window's own mean is removed,
   and the dot product is divided by both centered norms. Compute sliding
   sums/squared sums independently of the FFT numerator. Undefined or
   numerically unreliable energy is NaN, not a zero score. Reject centered
   energy <= max(1e-18 * sample_count, 64 * float64_epsilon * sum_squares).
4. Save every signed correlation profile locally, plus the best magnitude
   and up to five displayed peaks separated by at least 50 ms. Report sign,
   lag and runner-up structure; five displayed peaks are not exhaustive.
5. Define only a dominant-peak candidate: at least three consecutive C
   blocks, the same channel pair and polarity, |r| >= 0.95 in each, with
   source-minus-C lag range <= 5 ms. Evaluate sequences using each block's
   global maximum among eligible source positions, not a chosen combination
   of peaks. Overlapping qualifying sequences are merged only when the full
   merged range also satisfies the rule. Report all qualifying sequences.
6. Preserve edge scores but exclude C's first/last blocks and source matches
   within 20 ms of either resampled-file edge from candidate qualification.
   This is an explicit padding guard, not a claim to remove all encoding or
   resampling uncertainty. If there is no candidate, say only that this
   dominant-peak scale-one criterion was not met.

The 0.95 score and 5-ms consistency tolerance are stringent exploratory
screening choices, not validated false-positive rates or confidence bounds.
Grid spacing is not timing accuracy. Multiple lags, windows and channel pairs
are dependent searches; mono-like channels are not independent corroboration.
No exclusion of shared audio after time stretching, channel mixing, nonlinear
processing or edits follows from failure. A candidate can reflect reused
soundtrack, repetitive signal or shared material, not original context.

## Controls before historical scores

Verify normalized FFT scores against direct small-array calculations,
including signed lag/index conventions. Use deterministic synthetic signals
with known shifts, unequal gains/DC offsets, polarity reversal and channel
swap. Include a shift not on the 6,300-Hz grid via the full 44,100-to-6,300
pipeline, a deliberately inserted time jump (separate recoverable segments
but no false continuous-lag bridge), constant and near-constant signals,
independent noise and sustained/repeating tones. Show competing tonal peaks;
the sequence rule alone must not be described as uniquely identifying a
recording. Record seed, exact parameters and actual results.

Also run the historical reference reversed in time on the same grid as a
temporal-order sensitivity check, not an independent negative population or
calibration of false positives. Preserve full profiles and report maxima and
candidates even if they undermine the desired interpretation. No tuning of
thresholds/windows after viewing historical results in this stage.

## Acceptance and next step

Passing controls allows exploratory calculation, not scientific acceptance.
Repeat material historical calculations and obtain a separate numerical and
inferential review. A waveform candidate needs image correspondence and
source-lineage assessment; it cannot be aligned to the reported bang by
choosing a convenient offset. Human listening and acoustic-source/detectability
requirements remain independent. Document exact failures or limits and the
next discriminating test, without interpreting anomalies as concealment.
