# Independent counted-window and calibration-document review

2026-09-19. Research-only computational review by
`/root/camera2_calibration_observer`; not human or architectural certification.
This follows `SOURCE-ADDENDUM.md`. The earlier `observer-note.md` and
`observer-pins.json` remain byte-for-byte unchanged. Neither root's endpoint
note nor its new document conclusions was read to prepare this review.

## Result

The newly inspected source image supplies a genuine, previously uninspected
**author-annotated floor-labeling lead**: red graphic points named `Floor47`
and `Floor29`, with a `Floor35` object also listed in its algebra sidebar.
That materially improves the available source context beyond an unlabeled
façade. It does **not** identify either exact saved Tilted calibration query or
provide a demonstrated mapping between its drawing coordinates and the
720×480 Tilted raster. The assigned length `58.293` is not stated in the
inspected illustration or selected PDF pages.

The image and floor-sheet duplicates are exact copies, not independent
architectural corroboration. The shared illustration's archive placement in
both Dan Rather and Tilted folders does not identify its source camera, frame,
or registration to both videos.

## Actual source coverage and provenance checks

I inspected exactly four complete visual assets:

1. The unchanged `source-docs01/counted-windows.png`, 1010×846 RGB.
2. The existing complete floor-spacing page 1, 935×1210 RGB.
3. The existing complete lab-instructions page 2, 935×1210 RGB.
4. The existing complete lab-instructions page 3, 935×1210 RGB.

All four were legible as complete images. No crop, overlay, new rendering,
registration, enlargement, other video frame or additional PDF page was used.
The PDF skill prompted complete-page coverage; evidence/source-of-truth skills
kept the annotations separate from architectural fact and preserved the frozen
first pass. The earlier calibration review was used as a source-path/pin
locator; its Camera3-specific interpretations were not transferred to Camera2.
The existing `reading-products.json` was read in full for derivative lineage.

Using bundled Python 3.12.14, Pillow 12.3.0 and pypdf 6.10.0, I independently
read the five exact declared archive member bodies by verified zero-based
index and member name. All five hashes and byte lengths matched. The three
floor PDFs at indices 38/47/53 are byte-identical; the two counted-window PNGs
at 46/49 are byte-identical and equal the retained local PNG. The held parent
archive hash, source receipt, two existing PDFs, three page PNGs and counted
image pixel hash also matched their declared values. pypdf confirmed one
floor-sheet page and five lab pages, without expanding visual coverage.

These were read-only checks. No new file was extracted or modified by this
review. An initial directory listing looked for `lab-pages` under the review
directory and reported those two directories absent; the review's explicit
`camera3-provenance` source root resolved that locator error before any image
inspection. No source pin, body-duplicate or pixel check failed. Exact pins and
actual visual coverage are in `document-pins.json`.

## What the annotated image actually shows

The complete source is a screenshot of a graphical geometry application with
window title `Window Counter.ggb`, toolbar, algebra sidebar and a photographic
background. It is not an original architectural elevation. A black diagonal
line crosses the visible façade, with blue points along it and two red labeled
points. The upper red point is labeled `Floor47`; it lies below the roof
silhouette, not at the top of the central raised roof structure. The lower red
point, `Floor29`, is farther down/right, beside the image region containing
bright foreground rooftop fixtures. `Floor35` is named in the sidebar, although
it is not separately labeled on the photographic graphic in this screenshot.

The picture shows a broad banded façade, a stepped/raised roof silhouette,
a bright right vertical boundary and foreground rooftop structures/fixtures.
Those features are qualitatively compatible with the general view in the
three frozen native-frame observations. This supports the relevance of the
illustration as a scene/feature lead; it is not a quantitative image match or
proof of a particular frame or camera origin. The photographic background is
colored and enlarged inside an application screenshot, unlike the native
Y-plane raster already inspected.

The sidebar contains drawing-point coordinates and a partly clipped line
equation. The image gives no displayed transform from those coordinates to
the native Tilted raster. Neither existing query coordinate is named or
explicitly associated with a labeled point. No calibration tape bearing
`58.293`, numbered drawing citation, source-frame identifier, camera label,
scale legend, survey datum, or author explanation for the floor numbering is
visible. The `.ggb` window title is a project-document lead, not proof that its
underlying editable file is available or that its labels are correct.

## What the selected PDF pages supply

The one-page sheet is headed **Elevations of Floors of WTC 7**. It lists floor
1 through floor 47 and a Roof row, with incremental floor separations and
overall/elevation columns in feet. It is a dimensional table, not a drawing
connecting window bands to slab elevations. It has no visible drawing number,
source citation, explanatory datum, façade diagram or particular calibration
pair. The intervals are not universally uniform: the printed 45→46 and
47→Roof intervals differ from the common 12 ft 9 in entries. No new
floor-pair enumeration or metric arithmetic was performed here.

Lab page 2 describes the `.trz` files as completed examples for comparison
with student work. It distinguishes the Dan Rather video from a similar
tilted-camera view and associates window rows in those views with floors.
It suggests checking a stationary neighboring building for camera movement
and warns that floor spacing varies. Those are the lab author's method and
provenance assertions, not independent verification of the current saved
project or camera stationarity.

Lab page 3 describes rotating the axes to a vertical building edge, selecting
two reasonably separated floors, obtaining their separation from supplied
documents, converting feet to metres using 0.3048, and placing/aligning a
calibration tape at the chosen floors. It does not mandate a particular pair,
name the two saved Tilted queries, or assert that the red endpoints in the
counted-window screenshot are that tape. Its example frame-rate discussion
and instructions to students are not permissions to execute a new analysis.
Interpretive collapse claims elsewhere on these inspected pages are not
adopted as findings by this document review.

## Join to the frozen observations: positive and contrary evidence

| Proposition | What supports it | Limit or strongest contrary evidence |
|---|---|---|
| A source author attempted to label floors in the relevant-looking façade view. | The retained screenshot visibly contains floor-named graphic objects and repeated banding; the lab gives a floor-based calibration procedure. | The labels are assertions. Neither a drawing citation nor their architectural derivation is visible. |
| The annotated illustration is a useful lead for resolving the two saved queries. | Its roof/edge/foreground configuration qualitatively resembles the already inspected scene; identical copies are supplied with both related video folders. | The screenshot does not identify camera/frame or a native-raster transform, and supplies no exact saved-query correspondence. Duplicate placement is not two-camera registration. |
| The existing query neighborhoods are not inherently devoid of usable structure. | Frozen observations identified visible façade banding; the new image shows an explicit attempted numbered interpretation of that banding. | Band/window edges, slab levels, façade details and roof/parapet features are distinct observables. One-to-one equivalence and matching feature phase are not established merely by labels. |
| The exact saved scale is verified or disproved. | A coherent attributed calibration procedure and a dimensional table are now visually checked for this follow-up. | The two saved endpoints remain unjoined to exact architectural features. No physical error, correct scale, or unique pair has been measured. |

This is a real source advance, not a calibration verdict. The strongest reason
not to dismiss the source is that it provides explicit numbered anchors, not
just an unexplained scalar, and could guide a competent architectural/image
review. The strongest reason not to call it validation is the missing bridge
from those author-assigned labels to the exact saved raster queries and to
authenticated architectural levels. Preserving both points avoids turning
uncertainty into either automatic acceptance or an allegation of fabrication.

## Next discriminator and limits

The next discriminating evidence would be a source-linked record identifying
the counted-image camera/frame and image transform, the original editable
window-counter/calibration annotation if it exists, and the architectural
basis for its named levels. A separately declared and controlled geometry
comparison could then test, rather than assume, correspondence to the fixed
Tilted query neighborhoods. Different camera geometry or labels should not be
transferred without that check.

No additional artifact retrieval, pixel registration, point moving, band/floor
count fitting, metric conversion, new trace, acceleration, causal ranking,
canonical promotion or external transfer was performed or authorized by this
review. Duplicate copies remain one underlying image and one floor sheet.
