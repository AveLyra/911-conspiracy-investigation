# Root source reading and independent geometry outline

2026-09-20 UTC. Frozen before receiving the second reader's interpretations.
Prior-informed computational reading, not blind/expert review or a fresh
historical-video measurement. Protocol/source pins in render01. Eight complete
pages viewed once each:53/307/308,320/321/322,323/324. No failed/repeated display;
all headers, footers, prose, captions and figure panels readable. Physical322
is a landscape page, correctly rendered as such. Physical323 is low-resolution
historical difference imagery, not unreadable page text. Extracted text for324
was consulted in addition to the full-page view. Zero saved render warnings.

## Source ledger

| Physical / printed | Supplied material | Boundary |
|---|---|---|
|53 /9|Plan described as trapezoidal, approximately329ft longer side,247ft shorter side,140ft width,610ft height; general building/location text.|No corner-coordinate table or uncertainty for these approximate dimensions on this page. Do not silently turn them into exact surveyed coordinates or identify every dimension's compass direction from this paragraph alone.|
|307 /263|Fig5-183 nine-camera location sketch,305m scale bar; Camera3 on West Street, Camera4 by West Broadway/Leonard. Cameras1/2 distant direction arrows, approximately5–7km.|A mapped location is usable context, not numeric camera extrinsics, lens settings, survey accuracy or independent camera authentication. No map digitization done.|
|308 /264|Figs5-184–186 camera1/2/3 views, captions and attributed intensity adjustment/floor-number overlays.|Camera3 is oblique with north facade and a side visible. No new pixel tracking or scale extraction.|
|320 /276|Fig5-202 plus explanation of Camera4 hand motion/zoom and transfer of pre-collapse NE-edge/reference lines using two fixed foreground buildings.|Explicit correction method exists; it is not an untouched raw view. No transformation matrices, control-point coordinates, residuals or error budget supplied here.|
|321 /277|First five Camera4 views reportedly align old/current NE edges within resolution after about10stories descent; interpretation permits straight-down, toward-camera or away-camera motion. Later frame10.6s is reported sharply westward. Camera3 differencing reports tilting edges, NE continuing and NW returning near original line.|The source itself states a line-of-sight ambiguity. Different NE/NW behavior contradicts assuming a rigid translating facade as an unexamined premise. Reported image relationships are not our new raw-image measurements.|
|322 /278|Fig5-204: eight Camera4 annotated views6.7,7.7,8.8,9.7,10.1,10.6,10.9,11.4s.|10.3s is not one of these displayed times. The target figure uses10.3s, between last displayed near-alignment and the later visible tilt; do not silently assert a simultaneous Camera4 measured residual.|
|323 /279|Fig5-205: nine difference images7.3 through11.3s, white old/current-edge overlays. At10.3s both sides visible with different shapes/relative edge relationships.|This is processed illustrative material; edge identity, registration and uncertainty need checking before metric use. Printed images qualitatively support changed edge relationships, not a newly measured displacement.|
|324 /280|Fig5-206, explicitly a heavily processed Camera3 difference frame at10.3s. Right red lines described as west roofline/SWedge; left red line parallel to west roofline through descending NEcorner. Paragraph says calculation uses line angle, building dimensions, camera distance and viewing angles of NE/SWcorners, yielding11m±3m. Combining Camera4 yields primarily due north.|No explicit calculation/equation, numeric camera distance/azimuths or uncertainty propagation supplied in the paragraph. Graphic has labels60 and“91,-54degrees”; only the angular unit is explicit. Pixel-length identities/reference endpoints are not defined in these pages. Do not guess their units or treat them as complete raw measurements.|

The phrase “angle between these two lines” has a potential referent ambiguity:
one right pair comprises an oblique and vertical line; the separately mentioned
left oblique is described as parallel to the roofline. It would be premature
to call the prose self-contradictory merely because the two obliques are parallel.
An annotated construction worksheet would resolve the intended pair/angle.

## Independently derived geometric constraint (symbolic only)

Let the pre-motion tracked vertical edge have fixed horizontal location
`(x0,y0)`; choose `x`east,`y`north,`z`up. For a pinhole camera with horizontal
position `(cx,cy)`, the plane through its center and that vertical line has a
horizontal normal proportional to `(-(y0-cy), x0-cx, 0)`. Every point descending
purely vertically at `(x0,y0)` remains in this plane and projects onto the
original edge's image line, independently of its changed height. This statement
does **not** require a rigid facade, but does require correct feature identity,+a fixed or correctly registered camera, and the original vertical-edge reference.

In homogeneous-image form, if `p ~ P X` and the original image line is `l`,
then `l^T P X=0` on that plane. Off-line image residual is related to this
quantity divided by projective depth; pixel distance alone is not metres.
For horizontal displacement `d=(dx,dy)`, a normalized plane residual is
`n_x dx+n_y dy=q`. Two cameras give a two-row system `N d=q`; if their plan
normals are independent, calibrated residuals identify horizontal displacement.
This is a geometry derivation, not the unpublished NIST formula.

Consequences conditional on reliable source observations:

- Genuine nonzero Camera3 displacement **from the original projected vertical
  edge at the new height**, together with Camera4 near-alignment, is positive
  evidence for horizontal movement approximately along Camera4's plan line of
  sight. Pure vertical descent alone cannot produce that off-edge residual in
  a correctly registered ideal pinhole view.
- Zero horizontal motion cannot satisfy an exact nonzero plane residual. But
  the source does not supply our needed numerical residuals/error intervals.
  We have not demonstrated that registration/placement uncertainty excludes
  zero in the historical data. Lack of an error budget is not proof that zero
  actually fits the images.
- Camera4 near-alignment constrains the transverse component, not distance
  along that sightline. Camera3's oblique view can constrain the remaining
  component **after** calibration; it does not do so merely by existing.
- A report-level qualitative comparison therefore can have real directional
  weight while leaving11m and±3m unreproduced. Calling all image evidence
  worthless would be as unwarranted as treating the published interval as a
  newly independently verified measurement.

## Required next arithmetic declaration / limits

No numerical sweep or image measurements done in this note. A useful bounded
next calculation is to implement the two-plane inverse, uncertainty intervals
and ill-conditioning tests using explicitly synthetic, nonhistorical fixtures.
Then state the actual missing data needed to apply it: image-line/point placements,
camera transformations/calibration, covariance/bounds, and cross-camera temporal
join (in particular the10.3s construction versus displayed10.1/10.6s brackets).
No arbitrary pixel-to-metre factor or convenient map coordinates should be
chosen to force11m. Testing this mathematical constraint is not reproducing
NIST's original geometric worksheet or reconstructing camera motion.

No cause ranking changes. The source supports an attributed deformation claim
and a testable geometric method; the precise interval and uncertainty require
more information or independently calibrated measurement. Even a confirmed
corner displacement would not measure a final debris footprint or distinguish
fire from deliberate initiation by itself.
