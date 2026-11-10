> **Historical research:** This document reports a past, bounded computational audit, not a new reproduction or current instruction. Missing image, media and receipt links are marked as unavailable in this package; see the [publication note](README.md).

# A/V correspondence audit validation

Research-only validation for the declared [protocol](PROTOCOL.md), [refinement](REFINEMENT.md) and [report](report.md). Integrity checks do not establish original media authenticity, calibrated motion, sound attribution, human review or a collapse cause.

## Execution and actual coverage

The initial extraction was completed in fresh `run01` and `run02` directories. Each first ran six declared synthetic assertions on two lossless fixtures with zero and five-second starts, then preserved 322 compilation and 12 comparator frames. Each historical selected index, PTS and dimension was checked against a separate full-frame probe and decoder `showinfo`. The code decodes from the beginning, disables autorotation and requested resampling, and explicitly converts to RGB without claiming color calibration.

The one declared refinement completed in `refine01` and `refine02`, with 90 compilation and 30 comparator frames each. Root inspected all initial 334 and refined 120 thumbnail presentations: 400 unique compilation and 38 unique comparator encoded indices after 16 overlaps. This is coverage of selected stored frames, not independent camera exposures, the full compilation, or all visible structural detail.

Root's additional full-raster viewing (1280 × 720, no new crop/interpolation) was:

- `run01/compilation/frame-` **0030, 0031, 0236, 0237, 0283, 0289, 0291** `.png` (seven).
- `refine01/compilation/frame-` **0023, 0024, 0031, 0039, 0045, 0051, 0061, 0076, 0090** `.png` (nine).
- `run01/comparator/frame-` **0001, 0002, 0003, 0004** `.png` (four).
- `refine01/comparator/frame-` **0001, 0009, 0030** `.png` (three).

These are 23 full-raster presentations / 22 unique source indices, because compilation 602 s appears in both runs. The initial root overview covered eleven compilation sheets and one comparator sheet; refinement covered three compilation sheets and one comparator sheet. This list records actual inspection, not an automated visual-certification claim. The separate review records its own 334 + 120 thumbnail views, 25 + nine native rasters and exact file hashes. Both are computational analyses of the same evidence, not licensed expert or genuine human spot-checks.

## Reproduction and independent checks

[verify_outputs.py](verify_outputs.py) completed with **1,101 passing checks** in [verification.json](verification.json). Its scope includes 1,062 fresh product hash/size checks across the four visual runs, source-before/after receipt consistency, command exit states, pair comparisons, 16 overlapping frame identity checks, unchanged audio derivatives, audio equality and three output-overwrite guards. The number of checks is not a confidence score.

- Initial runs: **399 of 401 product pairs byte-identical**. Only `synthetic-0.mkv` and `synthetic-5.mkv` differ. Their full probed timestamp maps, selected synthetic RGB images and all historical PNGs/overview sheets agree. The container-byte difference is preserved and its container-level cause is not diagnosed; do not claim complete byte-for-byte reproduction of every initial product.
- Refined runs: **130 of 130 product pairs byte-identical**. The refinement receipts do not freshly record runtime/library versions or FFmpeg/FFprobe binary pins. The initial runtime capture is not automatically contemporaneous refinement evidence. Output equality supports the recorded products, not a fully pinned repeat environment.
- Overwrite tests: invoking each of `extract_frames.py run01`, `refine_frames.py refine01` and `audio_crosswalk.py audio01` again failed with the expected `FileExistsError`; all existing files in those target directories remained byte-identical. These expected failures were part of testing, not failed scientific runs.
- The separate [fixture checker](reviewer-check/check_synthetic.py), without importing root extraction code, passed 86 checks on 72 source PTS values and all pixels of 40 selected synthetic frames. It compared the complete timestamp schedule against `offset + index/12` within half a container tick. Root read its implementation and result; root did not claim an additional fresh execution of that independent checker.

Initial extraction receipts preserve source, script, protocol, reference helper and binary/runtime pins. Refinement receipts preserve source, helper, protocol and selection pins with the runtime limitation above. Raw local process diagnostics were retained; they are not cleared for export or feedback. The preserved parent report and review attestations were not edited.

## Audio crosswalk

[audio_crosswalk.py](audio_crosswalk.py) completed as `audio01` and `audio02`, each after seven synthetic checks. The two measurement JSON files are byte-identical. The three visual cut coordinates map exactly to derivative sample indices 220500, 523320 and 122010; no rounding is needed or permitted. There are 66 windows (three × two 0.1-second windows plus three × twenty 0.02-second bins), each measured separately for two channels. The script tests half-open bounds, a known-amplitude stereo fixture, exact rational indexing and rejection of invalid/empty/nonintegral windows.

The input WAV hashes, shape, rate and float format are checked before use, with hashes checked again afterward. RMS includes DC; peak is sample peak, not reconstructed true peak. Logarithms of zero are represented by null, while the retained linear amplitudes remain exactly zero. No fresh decode, gain transform, automatic event detection or actual listening occurred.

The separate [numeric review](audio-review/review.md) and [implementation](audio-review/recompute.py) now independently reproduce all 66 windows: 870 scalar comparisons, including 492 finite floating-point values, 36 null logarithms and 342 exact boundary/coordinate fields. Maximum absolute numeric disagreement is `4.263256414560601e-14`, below the prospectively declared `1e-10` tolerance. Nine independent synthetic checks passed. The reviewer used a separate RIFF/IEEE-float reader and scalar `math.fsum` arithmetic, without importing root code, NumPy or SciPy. Root read the full code and review and inspected the saved result; it did not freshly rerun this separate script. Shared-WAV numeric agreement does not validate sound identity or original clock alignment.

The visual reviewer also performed a final claim-to-frame consistency pass on root report SHA-256 `17ada7cecff785c525bc40603da149499e9b9c3fbd2aa5c5de602ab656061a69`, with no new material visual inconsistency identified. Its final review is pinned at `3e9b6ea591f43878a450ecc93d85a7e217b23662a2fb98c4969921108b35a53f`. That attestation explicitly excludes audio arithmetic, paired-run reproduction, root viewing-count attestation and this validation document. Numeric-review result SHA-256 is `d9725184f1b578cc11e09098000cd7722b8ba18bb1e358ab1331af1cc99c415c`; the separate review document is `f505aaef4895948c597d0a3bc26f2b2803c30fa9f2607fc11588492c8dc72474`.

## Critical-review dispositions

1. **Initial coverage gap:** the reviewer identified that separate neighborhoods omitted the between-cut passage. The protocol was amended before extraction to include every encoded frame in [434,443). This resolved the declared temporal coverage gap at overview scale, not all full-resolution or visibility limits.
2. **Fixture timestamp schedule:** the separate checker supplies the missing independently constructed full expected schedule; this remains software verification of root-generated fixtures, not an independent historical decoder.
3. **Comparator first-event wording:** the initial native frames show changes before 13 s. The report does not treat [13,14) as earliest-onset coverage. The original selection rationale and outputs are preserved; no extra refinement was introduced to obtain a desired endpoint.
4. **Refinement environment pins:** missing contemporaneous runtime/binary capture remains disclosed, not reconstructed from the initial run or current environment.
5. **Scope of negative observations:** the report says no continuous descent was recognized in the selected screening, not that the building remained motionless. Original chronology, original sound alignment, specialist/human review and detectability remain unresolved.

## Verification ceiling and unfinished scientific work

This package establishes selected access-copy edits and narrows a few timestamp claims. It does not complete WP2: original source lineage, genuinely reviewed candidate sounds, recording geometry/propagation, calibrated multi-feature motion, acceleration uncertainty and physical-force constraints remain separate tasks. The full charter stays active. No held packet, case-sensitive transmission, bridge invocation, new source acquisition, legal-record promotion, commit or push occurred in this work package.
