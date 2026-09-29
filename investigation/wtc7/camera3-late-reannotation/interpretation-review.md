# Independent interpretation review of the frozen late-window results

2026-09-12. Working research review by the separate computational image
observer after both annotation tables were frozen. This review approves the
limited image-coordinate conclusions below; it does not approve a physical
acceleration, gravity comparison, mechanism ranking or causal finding.

## Review scope and checks

Read both frozen annotation tables and their notes, all comparison entries,
the complete fit data by read-only parsing, the analysis receipt, the
reference-method review and root-reference-verification01.json. Subsequently
read the complete report.md draft at the hash recorded below. My initial
labels remain unchanged. No new source retrieval, image alteration, feature
annotation, reference scoring, calibration or model fitting occurred here.

The four frozen observation-file hashes still match their freeze pins. The
analysis receipt has eight identical before/after input pins, and all three
listed analysis products match their byte counts and hashes. I independently
recounted every comparison and fit status. Reapplying the stored acceleration
weights to all computed input arrays differed from the recorded coefficients
by at most 2.88e-13 px/s². Reapplying the signed-weight interval extrema differed
by at most 4.27e-14 px/s². Reconstructing all stored residuals from the stored
coefficients differed by at most 5.69e-14 pixels. These are consistency checks
of saved arithmetic, not a fresh independent least-squares solver or a proof
that the subjective placement envelopes cover physical error.

## Supported conclusions and necessary qualifications

1. **The recognizable right corner reproduces the earlier image-coordinate
   trace at the stated precision.** Every saved A y value lies inside each
   observer's subjective envelope: 22/22 for root and 22/22 for independent.
   Both observers' A envelopes overlap in all 22 frames; their central y
   selections differ by at most 2 pixels. This supports annotation agreement
   for this operational corner. It neither makes the older decimal coordinates
   subpixel measurements nor independently authenticates the video.

2. **Late downward image curvature survives independent annotation.** Both
   observers produce all 23 declared A windows; all 23 A acceleration-placement
   envelopes per observer lie above zero under the nominal clock. The full
   21-mark quadratic coefficients are approximately 31.657 px/s² (root) and
   31.746 px/s² (independent), versus 31.524 px/s² from the saved A coordinates.
   Their full-window placement envelopes are approximately 28.889–34.425 and
   29.119–34.613 px/s², respectively. These are rounded displays, not new
   outward-rounded bounds. They characterize quadratic image fits over
   nominal 10–14 seconds; they do not establish a constant physical acceleration
   throughout that interval. Perspective, deformation, material correspondence,
   the conditional clock and source limitations remain outside these envelopes.

3. **The B comparison is silhouette proximity with an unresolved identity
   problem.** Saved B y values fall inside root's envelopes in 16/21 localized
   frames, and inside the independent envelopes in 19/19 localized frames.
   These denominators include the frame258 comparison and differ because of
   missing annotations. Root's five outside cases are frames300,309,312,315,318;
   their location before severe late smoke shows that the discrepancy cannot
   be described solely as a late-occlusion problem. Both observers' B intervals
   overlap in all 19 jointly localized frames, with central y differences of
   at most 2 pixels. The saved moving-column query ranges from x≈321.299 to
   x≈323.846 over the selected marks, whereas new B always uses x322. No
   distinctive persistent material marker was identified at B. Proximity of
   saved y values to these outlines cannot establish common material identity.

4. **Retain the localization disagreement, not a combined track.** Root
   localized B342 and B345 with broad envelopes; I judged them unlocalizable
   because the direct rim blended with smoke. Both observers judged B348
   unlocalizable. My B339 value remains low-confidence and broadly bracketed.
   Neither observer's choice is ground truth. Null records indicate an
   observation limit, not disappearance of the building or a zero displacement.
   Agreement with a saved coordinate must not be used to fill these positions.

5. **No computed new A−B window excludes zero within its placement envelope.**
   There are 20 computed root differential windows and 16 independent ones;
   all their envelopes include zero. Root has 12 nine-mark and 8 thirteen-mark
   computed differential windows; independent has 10 and 6. Neither observer
   has a complete 21-mark B or A−B fit. All 20 missing-localization rows remain
   in the 207-row output (187 computed), including corresponding B and A−B
   failures. Thus the defensible statement concerns every *computed* window,
   not a full late-interval differential measurement. These independent
   per-point Cartesian envelopes are not calibrated confidence intervals.
   Zero inclusion does not prove equality, a constant separation, absence of
   deformation, or a probability of equal acceleration. The overlapping
   windows are not independent experiments. Separate zero inclusion in each
   window also does not demonstrate that one jointly feasible point sequence
   makes every window's quadratic coefficient zero simultaneously.

The saved full-window A−B coefficient remains numerically about 3.888 px/s².
This review does not erase that calculation. Fresh placement alternatives,
uncertain B identity and explicit missing late labels prevent upgrading the
old difference into demonstrated different physical accelerations. Nor does
the current test prove that placement error alone explains the old difference.

## What common-translation cancellation actually establishes

If the same vertical additive image displacement v(t) affects both selected
coordinates, it cancels algebraically in their same-frame difference. This
statement does not depend on a stationary-reference fit. It removes one
specific shared term, not all camera effects.

B is fixed in image x, so horizontal translation can change which part of a
sloping outline it samples. For a silhouette y=f(x,t), common horizontal and
vertical translations h(t),v(t) give B=f(322−h(t),t)+v(t). A tracked corner has
y=A_body(t)+v(t) in this simple model, so A−B=A_body(t)−f(322−h(t),t). The v term
cancels, while the h-dependent outline-sampling term remains. Rotation,
perspective/depth changes, shape evolution and uncertain correspondence remain
as well. Do not label A−B generally camera-motion-free or a same-body-coordinate
acceleration difference. No numerical size for the remaining effect was
measured here.

## Exact draft-report review and corrections

The report draft at SHA-256
`dcd1fc9ea36a186da399c7010dc32f5c60d7243bb64c3157370fe5d5a615e03b`
already says a purely common vertical shift cancels and immediately explains
the fixed-image-column horizontal-sampling problem. That paragraph correctly
states the important limit; I do not find a substantive cancellation error
in this draft. Its zero-inclusion paragraph also expressly denies equality
and complete physical coverage. The 303–339 example coefficients, intervals,
RMSE figures and divisions by the stated assigned scalar scale all agree
with the stored values to displayed precision. Checking that division does
not validate the scale or historical clock. The claimed earlier saved-angle
value and the underlying calibration were not independently reviewed here.

Two concrete corrections should be made before calling the report final:

- The phrase “All20 computed root A−B envelopes and all16 computed
  separate-observer A−B envelopes contain zero, across the complete declared
  window set” is numerically correct but can be read as an affirmative test
  over the complete late interval. Add immediately: “Neither observer supplies
  a complete 21-mark B or A−B fit because the final rim is unlocalizable.
  Root has three and the separate observer seven uncomputed differential
  windows.” This makes the consequential coverage limit visible at the result.
- The claim-table row “The two original arrays prove different physical
  accelerations” is graded D/underdetermined. A proposition that they *prove*
  this is unsupported; the unresolved question is whether the physical
  accelerations differ. Replace the row claim with “The two locations had
  different physical accelerations.” Keep D/underdetermined and the stated
  material-identity/placement limitations. Alternatively retain “prove” and
  grade the proof claim as unsupported. Do not conflate uncertainty about
  physical equality with uncertainty about whether these arrays prove it.

One additional useful precision sentence after the equality disclaimer is:
“Separate zero inclusion in overlapping windows does not show that one
jointly feasible trajectory has zero differential curvature in every window.”
The present disclaimer is already directionally correct; this addition
prevents a stronger simultaneous-equality reading not tested by the method.

The reference paragraph preserves my R3/21 rejection and the distinct 31-pixel
alternative appropriately. The next-candidate language keeps the dark facade
band as a lead, not an accepted material marker. The pending arithmetic-review
paragraph must be updated only to the checks actually completed by the other
reviewer; this interpretation check does not substitute for that reproduction.

## Reference evidence and preserved preflight disagreement

The reference producer reports all 132 rows passing the frozen numeric gates.
Root's separate raw-moment implementation reproduced 22,308 real scores,
2,366 synthetic scores, selection/gate results and 44 translation groups
within the recorded tolerances. This supports the integer-grid arithmetic.
It is not an independent camera, a human review, or physical stationarity
validation. The method review's reference ruler midpoint defect does not
offset the factor3 target annotation rulers; it remains a documented display
qualification for factor8 reference crops.

My preflight rejected R3's 21-pixel patch because the diffuse pale masonry
lacked a sufficiently distinctive visual association. Root's earlier preflight
accepted it, and it then passed the numeric contrast/correlation screens.
Those results do not retrospectively change my visual judgment. The side21
all-reference diagnostic therefore remains conditional on root's accepted
association, with this observer's disagreement explicit. Do not advertise
unanimous visual clearance of all three small patches.

The side31 alternative stands separately: I provisionally accepted R3 with
the added edge context and accepted R1/R2. Every side31 winning displacement
is (0,0), including frame336 where side21 selected R1's +1 horizontal pixel.
The integer vertical optima are zero at both sizes. This supports no selected
common nonzero integer vertical translation under the tested templates and
±6 search, while leaving subpixel bias, depth, texture evolution and unmodeled
camera effects unresolved. It supplies no sub-half-pixel bound or target-plane
calibration.

## A concrete follow-up candidate and review limits

The existing views visibly contain a large dark rectangular facade band just
below the upper rim. Its image-right corner and adjoining light/dark boundaries
are plausible candidates for a future material-correspondence preflight,
especially before late smoke and foreground overlap. The finite patch could
provide more distinctive local texture than an arbitrary fixed-column rim
intersection. This is a candidate only: its surface/material identity,
deformation, tracking coverage and uncertainty would need a newly declared
study. I have not annotated it or certified it as a persistent landmark.

This review shares the imagery, protocol, tools and general computational
observer limitations with the other analyses. The initial table was independent
of root labels and saved coordinates; this interpretation pass is explicitly
unblinded. It did not independently decode the source, reproduce the complete
reference score grids, recreate fit weights, adjudicate the disputed rim
pixels with a human, or verify an eventual final report after the pinned draft.
Human/expert and consequential-measurement gates remain unmet.

## Reviewed artifact pins

| Artifact | SHA-256 |
|---|---|
| root-observations.json | `20b873f21704b3ccb8ceb75cba3eb09a84ab3431223a0c3f68ef7ce54efa397a` |
| root-observations.md | `42a5f3f4ff373c9b10c1d47f81db2fffbf28831b9e97ea326a062fa44491e027` |
| independent-observations.json | `529db0a68030a3ef26eef26723f0ab8c635fe47d6a743b780014d375ab95808f` |
| independent-observations.md | `d8ca1032081ea033db9f54e66cd9521e65373a88d4ce2e88e24f5ad52815ef72` |
| analysis01/comparison.json | `527417ca1d902de73af59f07796eea34e930faa4b2a2d583f6ab4c745c04a9ef` |
| analysis01/fits.json | `3aca7f5fe9d892ebea056bd3bdf1657f3fb898ed45e6cbe7043a40d78657fe29` |
| analysis01/receipt.json | `ab429f862a20632a260500f4a7c86436c3368ffb68c78cb71a4834f78c5cc01e` |
| reference-method-review.md | `36b00cd280ed7f10763629867b1aa0bbaa64fc186853ec6040435103583b7742` |
| root-reference-verification01.json | `6561d0decd13494171128fc5f4b3cd12e91c884a9b7c46e90479dcb3a892704f` |
| report.md (reviewed draft) | `dcd1fc9ea36a186da399c7010dc32f5c60d7243bb64c3157370fe5d5a615e03b` |

Only this review file was written during this interpretation subtask. Frozen
coordinates, earlier outputs, source records and other worktrees were preserved.
