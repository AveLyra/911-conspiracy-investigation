# Dense first shot picture comparison

October 7, 2026. Research only; no human acceptance, historical authentication
or legal-record promotion.

The dense comparison sustains the first-shot shared-picture lead, but does
not identify unique matching frames. It supplies later candidates whose lower
cloud more closely resembles C's fourth-second picture than the previous
coarse leader did. Numerous close alternatives remain, including separated
score bands not inspected visually. The higher maxima alone are not stronger
independent evidence: this is a selected refinement of the same recordings.

Nothing here authenticates C's soundtrack. The user's approximate bang at
local 13 seconds occurs in a different shot, beyond two montage cuts. It
cannot inherit a first-shot picture relationship. No collapse explanation
or acoustic-silence finding gains weight from this result.

## Scope and numerical result

The [reviewed protocol](PROTOCOL.md) retains the parent crop, masks, scale and
translation search, score gates and selection rules. It compares every
earlier-copy frame in PTS [10,18), source indices 300–539, with the unchanged
C references at local seconds 0, 2 and 4. These are file presentation times,
not historical event times. All 720 pairs and complete score/coverage surfaces
are retained in each run. [Configuration](config.json) pins dependencies;
[input map](screen01/input-map.json) pins all 243 selected images.

The following dynamic scores are evaluated at each candidate's best
stationary-scene transform, not fitted independently on the cloud. A score
is a correlation, not a probability of identity.

| C local second | Earlier-copy leader index | Earlier file second | Dynamic score | Frames within 0.005 | Separate contiguous bands |
|---|---:|---:|---:|---:|---:|
| 0 | 369 | 12.3123 | 0.991827 | 21 | 11 |
| 2 | 421 | 14.0474 | 0.995178 | 31 | 11 |
| 4 | 489 | 16.3163 | 0.975013 | 6 | 5 |

The exact rational timestamps, complete ranked alternatives and 0.005, 0.01
and 0.02 descriptive score bands are in [rankings](screen01/rankings.json)
and the input map. They are not confidence intervals. Dense adjacent pictures
are correlated; a singleton numerical maximum is not a unique original
exposure. The corresponding counts within 0.01 are 63, 68 and 14, and within
0.02 are 117, 133 and 44.

Stationary-only leaders are indices 349, 341 and 491: their non-chronological
order reinforces that foreground agreement cannot establish the sequence.
None of the six score leaders lies at a tested time endpoint. The three
dynamic leaders use scale 1.05 and translations (0,-1), (-1,-3), (-1,-10);
none hits the scale or translation boundary. This is an aspect-normalized
image fit, not physical camera calibration or evidence of a playback rate.

All pairs have valid stationary transforms. Dynamic coverage/variance gates
leave 98 primary scores and 196 scores across both retained transforms
missing. They remain explicitly null, not zero or silently excluded pairs.

## Native picture review

Both computational readers inspected the same rule-selected 12 unique native
earlier pictures and all three C references. Their first accounts were saved
separately in [root observations](root-observations.json) and
[separate visual review](independent-visual-review.json). These are nonblind,
same-source AI readings, not independent historical sources or expert/human
acceptance. The other 228 dense frames were not visually inspected in this
stage; neither were all other close-score bands.

The foreground building layout persists across the candidates. More usefully,
the dark upper cloud, its brighter sloping edge and changing central billows
show related configurations across the three moments. Root found the C2
changing detail more consistent with E420/421 than with its stationary-only
candidates. C4's lower advancing roll is conspicuous in its later dense
candidates, narrowing the coarse comparison's mismatch without proving an
exact exposure. That lower detail lies partly outside the scored upper-cloud
region and does not receive a second, independently calibrated score.
The comparison with the old coarse concern uses its preserved observations;
the old coarse image was not reopened for a new paired visual test here.

The earlier raster is only 320×224, has a dark lower strip and differs from C
in framing and image processing. Close candidates can look alike while
vertical framing changes substantially. Nearby time/camera, repeated or
interpolated pictures, a common derivative ancestor and unresolved fine
contours remain alternatives. Neither an ordered set of leaders nor the
preserved scores authorize a fitted time map across shots.

## Reproduction and checks

The [method review](preparation-review.json) required two explicit safeguards
before execution: distinguish duplicate map entries from valid repeated
pictures, and retain visually uninspected near-best bands as unresolved.
Both were incorporated without widening the test or changing numerical rules.

The executed checks used Python 3.13.7 at
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`, with NumPy 2.3.4 and
Pillow 12.0.0. Invocation paths are shortened below to this directory's
filenames; the independent checks were launched from the worktree root:

```text
python3 -B extract_dense.py extract01
python3 -B extract_dense.py extract02
python3 -B dense_screen.py controls --run controls01
python3 -B dense_screen.py screen --run screen01 --controls controls01
python3 -B dense_screen.py screen --run screen02 --controls controls01
python3 -B independent_check.py extraction --first extract01 --second extract02
python3 -B independent_check.py scores --first screen01 --second screen02
```

All completed with exit 0. The actual interpreter path, code/runtime hashes,
parameters and decoder commands are preserved in run and check receipts.

- Both extractions produced 240 native PNGs and eight overview sheets, with
  six synthetic extraction checks per run. The [separate extraction check](extraction-check.json)
  decoded all 1,130 presented frames sequentially and matched all 480 selected
  PNG instances, all exact PTS selections, eight coarse overlaps and 251
  historical products across runs. It shares the installed decoder but does
  not use the producer's selection helper. Synthetic container metadata is
  not required to repeat; historical images/maps/sheets are.
- The full pre-scoring gate passed nine dense-driver tests, nine inherited
  adapter tests and eleven numerical-core controls. This includes changing
  image order with fixed scenery and retention of equal-content pictures at
  distinct valid indices. Standalone developer tests are separate from this
  final dependency-bound gate.
- Both scoring runs completed in approximately 237.55 seconds, each with
  723 products totaling 262,839,646 bytes excluding start/final receipts.
  Both stayed below the unchanged 600-second and 384-MiB output caps.
- The [independent numerical check](independent-check.json) verified all
  pair memberships, all 1,440 retained transforms, null decisions, complete
  saved-surface top-two selections, rankings/bands/ties/endpoints and exact
  equality of all 723 products. Maximum direct score error was
  1.5543122344752192e-15 and coverage error 4.440892098500626e-16, below the
  fixed 1e-9 and 1e-12 limits. It reuses the earlier separate checker's
  arithmetic, never imports the producer/core, and shares Pillow resizing.
  It does not independently recompute every unselected FFT search cell.
- A separate overlap check found all 24 common coarse/dense result rows,
  their NPZ bytes and 48 arrays exactly equal to the preserved parent run.
  This checks reuse of the old method; it is not new corroboration.

Before execution, root found that the independent checker initially expected
a nested receipt where extraction uses a flat pin map. The checker was
corrected to validate both explicit schemas, without changing numerical
criteria; no historical verification had failed. An initial read-only attempt
to inspect the not-yet-written extraction receipt reported a missing file,
not a failed extraction. Earlier protocol hashes remain in the review history.
No source, parent method or prior result was overwritten. Final preservation,
repeat verification and existing-output refusal are recorded separately in
[final verification](final-verification.json).

## What changed and what remains

Directly established computationally: dense score leaders and their many
alternatives, exact extraction and two-run numerical reproduction. Supported
but still interpretation-dependent: a shared/reused first-shot picture-material
lead, with better representation of the later lower-cloud stage. Unresolved:
unique exposure identity, original-camera provenance/clock, and soundtrack
correspondence. This does not rank thermal, explosive or fire mechanisms.

The useful discriminator for the sound-bearing third shot remains its own
source/edit and audio lineage. This first-shot test is finished; no mask
retuning, rate fit or denied-source retry follows. The already authorized
curve-footprint inventory can proceed independently under its separate
uncertainty and human-review gates. The full charter remains active and
incomplete.

Work is uncommitted on `research/sherlock-wtc7-investigation`, HEAD `ca1c2233`.
The evidence-audit and source-preservation skills kept computed similarity
separate from historical or legal claims. Generic repeat-frame/shortlist
safeguards were deduplicated in the existing Sherlock feedback entry; its
archived-destination routing remains unresolved, so nothing was sent.
