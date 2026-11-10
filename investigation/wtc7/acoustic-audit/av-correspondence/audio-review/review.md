> **Historical research:** This document reports a past, bounded computational audit, not a new reproduction or current instruction. Missing image, media and receipt links are marked as unavailable in this package; see the [publication note](../README.md).

# Independent numeric audio crosswalk review

2026-09-11. Separate computational-agent review of the declared audio windows only. Research-only; no acoustic specialist, human listening, visual-transition validation or historical-source authentication is claimed.

## Result

All **66 declared windows** reproduce: three supplied visual-edit coordinates, each with the immediately preceding/following 0.1-second windows and twenty contiguous 0.02-second bins spanning ±0.2 seconds. Each channel's RMS, absolute peak, RMS dBFS and peak dBFS agrees with the root measurement. Exact rational sample boundaries agree without rounding.

The separate implementation made **870 scalar comparisons**:

- 528 level comparisons: 492 finite floating-point values and 36 exact `null` dB values for zero-valued windows;
- 330 exact per-window boundary/count/source-time checks (five per window);
- 12 exact per-edit coordinate/source/origin checks (four per edit).

All passed. Floating values used absolute tolerance **1×10⁻¹⁰**, declared in the saved code before execution; maximum absolute error was **4.263256414560601×10⁻¹⁴**. Integer boundaries, frame counts, rational coordinate strings, source labels and `null` values were compared exactly. This verifies calculations on shared retained derivatives, not independence of microphones or observations. Overlapping before/after and 0.02-second windows are not independent evidence samples.

## Method and preserved inputs

I read current repository instructions, the full investigation charter, [PROTOCOL.md](../PROTOCOL.md), [REFINEMENT.md](../REFINEMENT.md), the complete [root audio code](../audio_crosswalk.py), and the relevant root result. The evidence-falsification and development-verification skills required that the physical claim ceiling remain separate from passing numerical checks; source-of-truth and repository-orchestration controls confined edits to this new research-review directory. The repository intake reported branch `main`; unrelated working changes were preserved.

The [separate script](recompute.py) imports neither root code nor NumPy/SciPy. It parses the retained RIFF/WAVE bytes using Python's `struct` module, requiring 44.1 kHz, two channels, IEEE float32, an eight-byte sample-frame stride, one data chunk and a consistent RIFF byte count. It reads the retained PCM samples rather than running any new audio decoder. RMS uses scalar `math.fsum(value × value)`, followed by square root; absolute peak uses scalar `max`; dB uses `20 × math.log10`. Zero RMS/peak is represented by `null`, matching the declared root representation rather than a finite dB value. RMS is uncentered and includes any DC component; it is not a calibrated measure of audible power.

Before any historical sample calculation, nine independent synthetic checks passed: parsing across an unknown odd-length padded RIFF chunk; known before/after half-open RMS/peak/counts; known dB; zero-to-null behavior; and rejection of a nonintegral sample coordinate, empty interval, negative interval and truncated RIFF object. These are bounded software checks, not a comprehensive container-fuzzing suite or an event detector calibration.

Both retained WAV hashes, sizes, format contracts and frame counts matched their expected pins and the root result. Both source hashes and the root result bytes were rechecked unchanged after calculation:

| Retained derivative | Source-time origin | Sample frames | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| `edited-stereo.wav` | 430 s | 1,102,500 | 8,820,058 | `b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd` |
| `msnbc-stereo.wav` | 578 s | 1,675,800 | 13,406,458 | `b9758e82432a354fc584b22529b03c84aefc7b192d8579d5b8f95de3b715b292` |

They remain derived float WAVs from the parent full decode, not native camera audio. This pass did not reacquire or re-decode the original AAC streams, rerun the parent acoustic audit, inspect images, listen, inspect a transcript, or authenticate the three visual edit coordinates.

## Exact tested sample boundaries

All indices below are zero-based, relative to the specified retained WAV, and use half-open `[first, end)` ranges. Each 0.1-second interval contains 4,410 sample frames; each of the twenty 0.02-second bins contains 882 frames. The script independently generated every bin boundary using rational arithmetic and compared every one with the root output.

| Supplied source coordinate | Retained WAV | Boundary sample | Before 0.1 s | After 0.1 s | All twenty bins span |
|---|---|---:|---|---|---|
| `435` s | edited | 220,500 | [216,090, 220,500) | [220,500, 224,910) | [211,680, 229,320) |
| `13256/30 = 6628/15` s | edited | 523,320 | [518,910, 523,320) | [523,320, 527,730) | [514,500, 532,140) |
| `17423/30` s | msnbc | 122,010 | [117,600, 122,010) | [122,010, 126,420) | [113,190, 130,830) |

The exact source coordinates, all 66 reconstructed windows, channel values and individual comparison results are retained in [result.json](result.json). The third coordinate's preceding 0.1-second window is exactly zero in both channels in this retained derivative, while the following window is nonzero. That is a fact about these PCM samples only: it does not establish scene silence, a contemporaneous acoustic event or original audiovisual alignment.

## Claim ceiling and unresolved tests

| Claim | Type / result | Strongest alternative or limiting test | Grade |
|---|---|---|---|
| These retained WAV bytes and declared sample ranges reproduce the reported digital channel levels | Integrity observation and derived calculation; independently reproduced within stated tolerances | Different source bytes, interval definitions or numerical disagreement would weaken this result; exact pins/ranges are preserved | A within this bounded numeric scope |
| A digital level change at a supplied video coordinate establishes a scene-level sound onset or original A/V synchronization | Interpretation; not tested by this calculation | Editorial audio/video alignment, gain/processing, voiceovers and unrelated sound remain possible; require authenticated source lineage, audiovisual correspondence and human sound annotation | D / underdetermined |
| These RMS/peak windows establish a blast, no blast, or a collapse mechanism | Causal interpretation; no detector or physical calibration was supplied | Need microphone/distance/processing context, calibrated detection opportunity and independently checked sound candidates | E as a demonstrated conclusion of this method |

No correction to the tested root sample indices or numeric outputs is requested. The highest-value next work remains the separately controlled visual/source-lineage and actual sound-review process, with uncertainty and detection limits. More agreement between calculations on the same derivative cannot supply absent historical synchronization or a source identity.

## Verification and immutable pins

- Executed `python3 research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/audio-review/recompute.py` from the repository root using Python 3.13.7; exit 0; nine synthetic checks and all 870 comparisons passed.
- A second invocation was deliberately attempted and refused with `FileExistsError`; the existing result hash did not change. This expected safeguard refusal is not a scientific failure.
- `git diff --check` for the reviewer script passed. No browser check applies to this non-UI calculation.
- Only this review, `recompute.py` and generated `result.json` were written. Root-owned files, parent pinned review/attestations, source WAVs, legal-record spines, held material and bridge configuration were not modified. No network access, sensitive transfer, source acquisition, commit or push was performed.

| Reviewed or produced object | SHA-256 |
|---|---|
| Root `audio01/measurements.json` | `9d36b8b16419307f410508146c31560463110a0415960e985b49a38308fbcb28` |
| Root `audio_crosswalk.py` | `1ac4b5f4830e2d70e4b20805820fb4258306812c4bc1513cb95c48c3b1a9edf3` |
| `PROTOCOL.md` | `fefc783be3428d509d05ced97e98b2e2bd5b456feb0126a26eeb18c8649108c5` |
| `REFINEMENT.md` | `b3bc4f5f64c65e950d57b3824969c414923605bcd22254a4773066a36bcea278` |
| Reviewer `recompute.py` | `d887ab30d583c24c6235752bd6e9fe1c184ab2ca4441da208750f234da220bf0` |
| Reviewer `result.json` | `d9725184f1b578cc11e09098000cd7722b8ba18bb1e358ab1331af1cc99c415c` |

These fingerprints identify this review's tested versions. No root report, future revision, complete visual workstream or overall causal ranking is approved by this numeric review.
