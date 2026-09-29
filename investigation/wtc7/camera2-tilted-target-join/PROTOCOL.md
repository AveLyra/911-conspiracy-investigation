# Point-independent Camera2 / Tilted target correspondence

2026-09-24. Prospective local diagnostic for Q07/Q10. Prior-informed analysts;
not an event-level holdout, expert authentication, physical measurement or
actual-human acceptance. Previous turn: progress, completing the finite source
locator and resolving the two-file PNG integrity discrepancy.

## Question and scope

Can scene content outside the left foreground narrow the counterpart candidates
for Camera2 indices **6924, 6925, 6926, 6969, 6970, 6971**, within the already-held
Tilted clip's complete **0–475** decoded frame domain? No fixed offset is assumed.
Unknown processing ancestry limits the result to cross-representation content
correspondence; neither capture independence nor original exposure identity is
established by different encodings or an image-similarity minimum.

Authority: current main AGENTS/WORKFLOW/START-HERE and investigation CHARTER.
Only this dedicated research worktree is writable for this task. Existing raw,
source, prior outputs and legal records remain unchanged. New code/derivatives
and this note are working research. No network, new source acquisition, engine
acceptance, contact, publication, commit or push. Full goal remains active.

## Inputs and preservation

Use `../tilted-camera-source-join/`'s held Tilted MP4, `probe01` records,
`views01/frames.json` and receipt, and the six native Camera2 PNGs in
`candidates01`, admitted against their complete selection/receipt chain.
Tilted media SHA-256:
`393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f`.
Camera2 geometry is 640×480; Tilted is 720×480. Existing aspect/processing
uncertainty persists. Native decoded grayscale/Y is not calibrated brightness.

Reuse the existing Tilted extraction command/clock parser under exact code and
input pins; no seek, rotate, frame-rate conversion, interpolation or scale.
Before scoring, re-decode all 476 native Y420 frames and require every full-frame
and luma hash and clock row to agree with the stored records. Native PNG output
must round-trip to its luma bytes. Preserve exact warnings/errors and reject
unreviewed diagnostics, missing/extra frames, wrong geometry or failed pins.
Fresh output names, bounded local computation and before/after input checks;
never repair an old receipt to accommodate a mismatch. Independent input
admission and arithmetic review precede reliance on resulting scores.

## Mask sanity check before scoring

Existing descriptions place both points on a thin upright above the **left**
foreground roof, well left of the main target. No reliable numeric location was
supplied by the user. Fix the masks below now, before viewing/scoring. Root may
display only the two already-held complete native Camera2 frames 6925 and 6970
at original detail to check that the described upright lies comfortably left
of the 320-pixel midpoint. This is a coarse region check, not a new coordinate
annotation or physical interpretation. Verify each PNG's own receipt first.
If either appearance cannot confidently be excluded by that broad boundary,
stop: do not tune masks using match scores. Record any changed declaration
separately. No alternate image or light comparison is authorized by this check.

## Fixed metric, branches and retained alternatives

Resize only Tilted's width from 720 to640 using separately retained Pillow
NEAREST and BILINEAR branches; keep height480. BOX is omitted because the prior
four-pixel grid showed it redundant with NEAREST, not because of target results.
No fitted translation, warp, contrast, time shift or learned model. Sample the
global grid x=0,4,…636 and y=0,4,…476 with half-open rectangles:

| Region | Rectangle in Camera2 pixels | Role |
|---|---|---|
| right_half | [320,16,632,464) | Primary scene diagnostic, excluding left foreground |
| target_right | [320,64,480,320) | Sensitivity to changing main-target/cloud region |
| right_background | [500,160,630,320) | Background sensitivity; may be temporally uninformative |

The x boundary is far from the excluded left foreground and allows a resampling
footprint margin; synthetic controls must verify excluded-region perturbations
cannot affect sampled scores. Masks overlap; they are not independent samples.
Static structures, cloud changes and shared-source artifacts can dominate.

For every six-query ×476-candidate ×two-branch ×three-region combination retain
integer absolute-difference sums, sample count, raw mean absolute difference
and mean-centered correlation (null for constant data). Raw difference ranks
candidates within a branch/region; correlation is diagnostic, not an alternate
winner selector. Keep all scores. Report minima, exact ties, runner-up gaps,
boundary minima and order reversals/repeated winners across adjacent queries.
An argmin is not a unique exposure or a calibrated confidence statement.

For a finite **review shortlist**, retain the first five ranks **including all
ties at the fifth score**, plus each retained frame's immediate neighbors where
in0–475, unioned across both branches and all three regions for each query.
This rank-based shortlist is not a confidence interval or an exhaustive set of
possible original exposures. Report disagreement without choosing a preferred
branch after seeing it. No offset interpolation and no forced one-to-one or
monotonic assignment. If broad or contradictory, retain ambiguity.

## Controls, outputs and stopping rule

Before historical scoring: known copies, positive/negative brightness shifts,
localized changes, constant images, signed subtraction, exact/rank-cut ties,
missing/duplicate/invalid input, boundary and nonmonotone/repeated selections,
global grid membership, width-only sampling, excluded-left perturbation under
both resize branches, deliberately ambiguous neighboring frames and fresh-output
refusal. Verify each historical PNG identity and native array before sampling.
Independent arithmetic must reproduce all material scores/selections or preserve
the disagreement. Repeated runs establish computation, not history.

Deliver code/tests, source and run receipts, all scores/shortlists, independent
check and a bounded report. Do **not** inspect any shortlisted Tilted frame for
the bright points until scores and selection are frozen and reviewed. A later
paired qualitative-view declaration must address all relevant alternatives and
representation limits; that viewing is not part of this numeric diagnostic.

No radiometry, emitted-flash finding, physical duration, synchronization, failure
timing or causal ranking follows. Actual-human gates remain unmet. The strongest
objection is a shared or ambiguous processed exposure producing similar pixels;
unique numerical rank cannot resolve it. A failed representation contract or
non-discriminating scene is an informative limit, not permission to weaken the
acceptance criteria. Generic software lessons are deduplicated in existing
Sherlock feedback; archived-destination routing remains separate.
