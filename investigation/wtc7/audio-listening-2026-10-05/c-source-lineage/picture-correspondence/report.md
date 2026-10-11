# Held recordings picture correspondence

October 7, 2026. Research only under the full investigation charter.

**C's first shot has a stronger shared-picture-material lead; its later shot
remains unresolved.** The first shot's changing cloud outlines have close
counterparts in the earlier access copy, beyond the already recognized skyline.
Nearby alternatives prevent an exact frame assignment. The later shot contains
related buildings and cloud movement but does not recover an equally clear
changing-detail counterpart within this bounded comparison. Neither result
authenticates a camera original, soundtrack or historical clock.

This distinction matters for the user's approximate bang marker: it falls in
the later shot, not the first. The first-shot correspondence cannot authenticate
that sound by association. No cause ranking changes, and the full investigation
remains active and incomplete.

## The observed correspondence and ambiguity

Six reference frames were fixed before scoring: local C seconds 0, 2, 4 and
14, 19, 24. Each was compared against all 38 earlier one-second samples, not
the full 1,130-frame video. Geometry was fitted only to foreground buildings;
a separate cloud-containing region was scored without refitting. The complete
[rankings and alternatives](picture01/rankings.json), not just leaders, remain
available. All times below are file coordinates, not historical times.

| C local second | Leading earlier sample for changing detail | Correlation at the best stationary fit | Other samples within 0.005 of that score |
|---:|---:|---:|---|
| 0 | 13.013 s, frame 390 | 0.984897 | Frames 360 and 420 |
| 2 | 14.014 s, frame 420 | 0.995074 | None in this sample grid |
| 4 | 15.015 s, frame 450 | 0.957754 | Frame 480 |
| 14 | 24.024 s, frame 720 | 0.424094 | None in this sample grid |
| 19 | 32.032 s, frame 960 | 0.721522 | None in this sample grid |
| 24 | 37.003633 s, frame 1109 | 0.804522 | None in this sample grid |

These are descriptive scores under different shot-specific masks, not match
probabilities, uncertainty intervals or a calibrated first-versus-third-shot
test. A unique coarse-grid leader can still have better unsampled counterparts.
The last row selects the final coarse sample, so its apparent separation does
not establish that the desired passage ends there.

The same earlier frame, 360, leads stationary-geometry scoring for both C0 and
C2, despite their different cloud detail. That directly illustrates why a
skyline fit does not identify time. For C0, seven stationary candidates lie
within 0.005 of the best score. The separate cloud comparison is more selective,
but C0's near-best set still includes C2's leader. An ordered sequence of three
winning indices is not a unique temporal correspondence.

Root inspected all 16 unique shortlisted native early images against the six
native references. The [frozen observations](root-observations.json) identify
consistent evolving dark and light cloud edges in the first-shot candidates,
particularly C2/frame420. They also retain contrary detail: C4's advancing lower
roll is more developed than frame450's and has another candidate around480;
that conspicuous lower region is not wholly inside the frozen upper cloud mask.
This is evidence for a related/reused passage, not an exact exposure certificate.

The later shot has tighter/downward framing and different facade proportions,
tone and clipping. Broad advancing cloud in the same apparent corridor can
explain candidate similarity without establishing the same recorded exposure.
The declared crop/aspect normalization and scale/translation family cannot
resolve every possible processing difference. Failure here is not exclusion
of shared footage, proof of a different camera, or evidence of manipulation.
Separate visual-review disposition is recorded in the final review section.

## Fixed method and reproducibility

The [protocol](PROTOCOL.md), [configuration](config.json) and
[pre-score review](preparation-review.json) define the source pins, prior image
familiarity, six reference times, crops and disjoint stationary/cloud masks.
The complete earlier 320×224 images and prescribed C crops are converted to
grayscale and resized to 180×120. This is a comparison normalization, not
perspective or physical geometry calibration. The cloud masks include some
background; native changing-detail review remains necessary.

The small adapter reuses the unchanged, hash-pinned correlation core. Its
21 scales range from 0.75 to 1.75; the translation grid stays ±25 pixels on the
working grid. Larger scaled images are clipped at a defined canvas intersection;
empty padding is invalid. At least 85% mask coverage, 32 pixels and nonconstant
intensity are required. Cloud scores are evaluated at the two best stationary
fits; the primary cloud ranking uses only the best stationary fit. No dynamic
refit, audio input, rate fitting or time map across either recording's cuts occurs.

Both complete runs tested all 228 pairs, saving all scale/translation stationary
score and coverage surfaces. Each produced 231 pinned products totaling
83,561,021 bytes, excluding its start/final receipts, in about 76–77 seconds.
All 231 products match byte-for-byte between runs. The six pairings with the
black early frame have no admitted stationary transform. Of the other 222
primary fits, 35 have unavailable cloud scores. Across both retained transforms,
70 cloud null decisions remain explicit, rather than being encoded as zero.

Nine adapter tests and 11 inherited numerical controls passed before historical
execution. A pre-run review found that reversing ranked rows did not test
changing-image order. The earlier test source and its receipts remain preserved;
a three-image synthetic sequence was added. It recovers ordered/reordered cloud
assignments while unchanged scenery alone remains ambiguous. Root reran the
complete repaired suite before starting both historical runs.

The [separate numerical check](independent-check.json) imports neither producer
nor numerical core. Ten synthetic checks preceded its historical run. It
verified all 228 pair memberships, 44 input images, full saved-surface top-two
selection, all six ranking groups, both-run byte equality and all 444 retained
transforms by direct arithmetic. Maximum score difference was 1.89×10⁻¹⁵
against the fixed 10⁻⁹ tolerance; coverage difference was 4.44×10⁻¹⁶ against 10⁻¹².
It reproduces the 70 cloud null decisions. It does not independently recompute
every search-surface cell or authenticate historical sources; Pillow resizing
and underlying records are shared. Root read the checker and reran it, agreeing.

The [execution record](execution.json) preserves actual commands, runtime
versions, the synthetic corrections and failures. Historical runs used Python
3.13.7, NumPy 2.3.4 and Pillow 12.0.0. An end-to-end existing-output refusal returned
the expected error and left all 233 files of the first run unchanged. No source
bytes, earlier observations, legal records or accepted Sherlock/Faraday state
were changed; no new media, commit, push or transmission occurred.

## Final review and next discriminating test

The [separate visual reading](independent-visual-review.json) inspected all
16 shortlisted early images and six C references, freezing its interpretation
before opening root's current observations. It agrees on the stronger first-shot
changing-detail lead and unresolved later-shot correspondence, particularly
C14. Its strongest alternative is that nearby times or a nearby camera can
share scenery and broadly evolving cloud without an exact exposure match.
No material disagreement emerged from the subsequent comparison. Both readings
are nonblind, same-source AI assessments, not independent historical evidence,
human acceptance or expert certification. A separate report audit found no
material numerical/provenance correction.

Claim grades: A for the reproduced calculations under the stated procedure;
C for the first-shot reuse/sequence inference because exact exposure and
processing remain unresolved; D for exact later-shot identity and original
sound attribution. These grades state inferential limits, not probabilities.

The first-shot lead justifies a separately declared dense image comparison
around the early 12-to-16-second passage, retaining neighboring alternatives and
the existing geometry/cloud distinction. Its acceptance criterion should be
discriminating changing-detail agreement at more than two moments with explicit
source-frame and crop uncertainty, not merely high correlation or a convenient
ordered triple. Even a reliable relationship between these derivative file
coordinates would not establish original capture speed or camera sound.

The later shot needs a better source/processing relationship before using it
to time the bang. Do not lower the completed audio threshold, choose an audio
offset to match a desired structural event, or bridge montage cuts. A future
audio test would need a separately justified picture-time relationship and its
own declared processing model. Thermal, conventional-blast and fire pathways
receive no new support or exclusion from this picture-source result alone.

Work is intentionally uncommitted in the dedicated investigation worktree,
branch `research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. The existing
status and research map point here; raw sources and earlier results remain
unchanged. A full-reasoning follow-up should freeze the dense test and its
coverage/storage schedule before execution, reusing the verified numerical
components and extraction controls. No new human acceptance or access is
implied by this proposed next test.
