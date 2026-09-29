# Scene-correspondence declaration after the eight-frame screen

2026-09-19, before candidate extraction or numerical image comparison. Root has
viewed exactly the predeclared native Tilted frames 0,67,135,203,271,339,407,475.
The first five show the upper facade/raised roof features amid changing smoke;
339 shows a changed/lowered upper outline; 407 a substantially lower visible
upper facade; 475 a dust-obscured area with the former roof no longer visible.
These are sampled appearances, not physical onset times or acceleration.

The entire foreground/background arrangement, left image border and upper
building form strongly resemble the previously reviewed Camera2 images.
The held Tilted raster is 720x480 with SAR131:144; Camera2 is 640x480. This is
a concrete pixel-geometry difference, not an authenticated source relationship.

## Fixed candidate corpus and processing

Use every Camera2 decoded frame **6500 through 7200 inclusive (701 frames)**,
covering a margin around the older 6593–7104 declared event region. Root selected
this interval from prior source coverage, not from new similarity scores. Reuse
the preserved native-Y extraction helper, original all-frame hash map and exact
PTS; stream from the file start and verify all 8,042 decoded frame hashes.
No source seeking, clock normalization, temporal interpolation or automatic
rotation/scaling is allowed. Save 701 native PNGs; this is extraction/numerical
coverage, not a claim to have viewed all 701.

Comparison queries are exactly the eight already declared Tilted frames.
Use three **diagnostic**, non-physical resampling branches, each resizing only
the 720-pixel image width to 640 with unchanged 480-pixel height: Pillow NEAREST,
BILINEAR and BOX. No rotation, translation optimization, warp or fitted tone
correction. This tests an obvious raster relationship, not an architectural
calibration. Retain each branch; do not pick one by agreement with acceleration.

Compare native Camera2 and resampled query Y values on an every-fourth-pixel
grid starting at native (0,0), with half-open rectangles in Camera2 coordinates:

- full scene: [32,16,632,464)
- left foreground geometry: [40,270,300,460)
- right background geometry: [500,160,630,320)
- target/smoke: [280,70,480,320)

The two geometry regions are selected for nominally stationary buildings, but
late smoke/dust may obscure them. They are not an independently validated static
mask or camera calibration. Regions intentionally serve different descriptive
roles and can overlap the full scene; they are not train/test event holdouts.

For every query/candidate/branch/region compute raw mean absolute Y difference
and mean-centered normalized correlation. Undefined constant-image correlation
stays null; it must not count as a perfect match. No geometric or tonal parameter
is fitted. Keep all scores and all source hashes/PTS, not only the minimum.
Select the minimum-full-scene-MAE candidate within each branch (tie: lowest
source index; report exact ties). Record the runner-up and MAE gap, but do not
turn a gap into a statistical confidence level or unique exposure finding.

Before historical scoring, synthetic tests must cover exact copies, signed/
constant brightness changes, changed localized content, constant-frame undefined
correlation, repeated identical candidates/ties, and the stated resampling/grid
and mask membership. Reproduce material score arithmetic independently.

## Subsequent visual coverage and inference

After scoring, root may view the complete native Camera2 frames in the union
of the three branches' selected minimum-MAE candidates for all eight queries,
at most 24 distinct frames. Record actual viewed indices and query/branch joins.
No unviewed runner-up or additional historical image may be described as visually
reviewed. Rendered point overlays and motion tracking remain outside this unit.

Report actual matches/mismatches, boundary minima, reversed/nonmonotone index
sequences, weakly distinguished neighbors, and failure of the proposed raster
relationship. A low residual and related smoke/roof configuration across the
series can support common recorded content; it cannot authenticate the native
camera, a unique original exposure, unedited timing, a source-to-paper project
link or physical calibration. Do not infer a time offset by forcing the paper's
reported onset labels or a gravity curve to match.
