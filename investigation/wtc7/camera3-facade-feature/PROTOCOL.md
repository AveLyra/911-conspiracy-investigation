# Camera 3 distinctive facade-corner test

Exploratory declaration, 2026-09-12. The charter controls scope. Prior dense
roofline results and images are known; this is not a historical holdout.
Root newly inspected only the existing baseline288 native/crop before this
declaration. No new coordinate table or fit has been produced for C.

## Observable and sampling fixed before coordinates

**C** is the lower-right corner of the prominent dark rectangular band below
the broad facade's upper rim: the intersection of its right termination and
its lower sloping edge. It is not the overall building corner A, the upper
right corner of the band, or a fixed image column. Follow this local contrast
junction in x and y only while that same junction remains recognizable.
Its architectural identity and physical material correspondence are open.

Use all 22 existing native/crop pairs in `../camera3-late-reannotation/views01`:
258 and 288 through348 in steps of3. The existing receipt SHA-256 is
`8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161`.
Check image hashes before relying on them. Reuse these verified derivatives;
no new decode, interpolation, crop or synthetic enhancement is needed.
The target crop [295,125,535,375) repeats native pixels3x with external rulers.

Root and a separate computational observer view all selected native/crop
pairs. Before comparison, each freezes integer x,y and inclusive subjective
x/y localization bounds, plus a feature-identity/visibility note for every
frame. Bounds encompass plausible placement of the visible edge junction,
not a calibrated confidence interval. Choose bounds on image legibility,
not closeness to another track or a desired acceleration. When uncertain
between different features or obscured, return null and the reason; do not
extrapolate or continue a predicted trajectory. Preserve disagreements.

The separate observer must not consult root C annotations, any C fit or the
earlier A/B coordinate arrays before freezing C. The identical input images
are shared evidence, not independent cameras or human/expert measurement.
Previous frozen A placements will be reused explicitly, not called new data.

## Declared calculations after both tables freeze

Report coverage and per-frame overlap of both C boxes. Compare same-frame
image separation A-C in x and y with each observer's own earlier A boxes.
Keep central differences and their full box extrema, no interval averaging.

Test whether one constant image separation can meet every available box
simultaneously: intersect per-frame [A_low-C_high,A_high-C_low] independently
for x and y. Test each observer and both together (intersect both observers'
A boxes and C boxes at mutually readable samples). Do so for all22 selected
and late21 only. Preserve the omitted frame lists and empty intersections.
A feasible vector supplies an explicit per-frame box witness; an infeasible
vector supplies the conflicting extremal frames and minimum uniform box
widening needed to restore this purely geometric feasibility. Widen each
individual coordinate box by the same delta>=0; no frozen box is changed.
This is sensitivity, not an inferred actual error or confidence level.

If C has sufficient coverage, fit native y against nominal t=(frame-138)/15
for all predeclared 9,13,21-point sliding late windows, retaining failures,
position residuals and linear acceleration weights. Fit A-C similarly and
propagate placement boxes as a Cartesian product. Report native units first;
no new metric calibration or preferred gravity-matching window is selected.
Use independent arithmetic for material derived outputs and synthetic
constant/curved/translated/ambiguous/missing cases before historical results.

These tests concern image correspondence and relative motion, not physical
rigidity, all supports, force, footprint or causal identification. Constant
image separation is not necessary for a physically rigid body under a moving
or perspective camera. No mechanism gets credit just from fitting a terminal
trajectory. A local source/drawing check will independently examine whether
architectural geometry can be established; failure remains a result.

## Preservation and boundaries

All new files stay in this investigation worktree. Preserve source images,
old annotations/results and raw/canonical/legal material. No case promotion,
model execution, held-packet inspection, transmission, task rerouting,
commit/push, Faraday call or change to a cause ranking is authorized by this
unit. Human/physical-calibration gates remain. Report reviewer independence
accurately and leave the comprehensive investigation active.
