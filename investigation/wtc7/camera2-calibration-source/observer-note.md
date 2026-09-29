# Independent descriptive pass: saved Camera2 calibration queries

2026-09-19. Research-only computational observer
`/root/camera2_calibration_observer`. First pass frozen before reading root's
new endpoint observations or sharing substantive observations with root.

## Scope, independence and authority

I read main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, the investigation
`CHARTER.md`, and this unit's `PROTOCOL.md` completely. The
evidence-falsification-auditor and source-of-truth-guardian skills and their
referenced checklists were applied. Preserved sources control; this note is a
working descriptive interpretation, not a canonical fact, accepted finding,
human review, scale calibration, or expert report. No source or main-repository
file was edited.

I received inherited textual context about earlier scene/source work, including
the saved calibration queries and limitations. I did not read the root's new
endpoint descriptions, another observer's first pass, or Camera3 endpoint
narratives. I am a computational agent, not an independent human observer or
licensed specialist; sharing source material, task framing and model context
limits independence. These are previously used event images, not an unused
holdout.

Actual visual coverage is exactly three complete native 720×480 Y-plane PNGs
at clip indices **0, 67, 135**, followed by their three unmarked 300×540
nearest-neighbor enlargements of rectangle **[390,130,490,310)**. The native
100×180 crop files were read for pixel verification, not separately displayed.
No other image, alternate frame, overlay, deblurred image, new crop, drawing or
physical-dimensional source was viewed for this pass.

The two existing queries, not newly annotated points, are:

- Q1: `(444.9122807017544, 185.82456140350877)`.
- Q2: `(441.3701657458563, 272.2651933701657)`.

I checked those literals in the already-pinned `project01.json` TapeMeasure
array, along with its assigned world length `58.293`. Reading that assignment
does not validate its architectural meaning or physical size. No coordinate
was moved to a band, edge, window, corner, or preferred floor level.

## Descriptive observations

| Frame | Q1 neighborhood | Q2 neighborhood | Identity ceiling |
|---|---|---|---|
| 0 | Within the large target façade's interior, below the roof silhouette and away from its bright right boundary. Faint repeated horizontal light/dark banding is visible. The query is not a uniquely recognizable corner or isolated architectural marker in this view. | Within the lower visible portion of the same façade. Faint horizontal banding and broad contrast variation are present. Foreground rooftop structures are visible lower/left in the complete frame and crop, but no definite foreground object covers the query neighborhood itself. | Façade association is visually supported; an exact floor, sill/spandrel edge, or other unique architectural identity is not established. |
| 67 | Same broad façade-interior association; repeated horizontal texture remains visible but blurred and low contrast. No newly unambiguous marker identifies the exact query phase within the repeated banding. | Same broad façade association. The neighborhood is not definitely hidden by a discrete foreground obstruction; its weak local contrast does not identify a unique floor boundary. | No exact architectural identity is established. |
| 135 | Façade and horizontal banding remain visible at the saved query. Changes elsewhere in the roof/smoke context do not supply a unique identity for this interior query. | Façade texture remains visible. The saved query is above the main foreground roof obstruction in the complete-frame context, but the specific horizontal phase/feature remains ambiguous. | No exact architectural identity is established. |

These descriptions refer to neighborhoods of the saved numerical queries, not
new subpixel measurements. The many decimal places in the saved coordinates
are software-record precision, not demonstrated visual localization accuracy.
The enlargements preserve and repeat existing pixels; they do not resolve
details absent from the native images.

The strongest positive observation is that neither query is obviously in sky,
outside the target façade, at its roof edge, or on a clearly separate foreground
building. This is not enough to identify two architectural endpoints or their
physical separation. In particular, I did not count bands, assign floor
numbers, fit a scale, test physical perspective, trace motion, or infer a
collapse mechanism.

## Claim limits and contrary considerations

- **Source fact, directly checked in a derivative:** the pinned project export
  saves the stated two query coordinates and assigned length. This checks the
  existing export, not a new independent raw-XML parse or historical software
  execution.
- **Descriptive inference, moderately supported:** both query neighborhoods
  appear associated with the visible target façade in all three viewed frames,
  rather than an obvious separate obstruction. Limited resolution, contrast,
  haze and repeated image texture constrain finer identification.
- **Unresolved:** exact architectural feature/floor identities and the physical
  separation represented by `58.293`. No dimensional source was inspected in
  this subtask. This pass neither confirms nor falsifies that assigned length.

The strongest objection to overstating the uncertainty is that real horizontal
façade banding and whole-building roof context are visible. A qualified reviewer
using better-preserved imagery and a specifically identified architectural
elevation might establish identities that this limited pass cannot. Conversely,
repeated dark/light bands in low-resolution processed footage should not be
automatically equated one-for-one with structural floor boundaries. Ambiguity
here is not evidence that the project author deliberately chose wrong points.

The next useful discriminator is an independently source-pinned architectural
mapping of the *same* visible features, supported by an original project
annotation or appropriate façade/elevation record and adequate imagery. No
numbered floor assignment from a different camera should be transferred without
establishing the view-specific correspondence.

## Verification actually performed

1. `shasum -a 256` checked the four main authority files, this protocol and the
   held public parent archive. Values are recorded in `observer-pins.json`.
2. Bundled Python 3.12.14 with Pillow 12.3.0 checked the three native PNG byte
   hashes, file sizes, 720×480 geometry, mode L, and decoded-luma hashes against
   `views01/receipt.json` and `views01/frames.json`. All three passed. It also
   hashed the held project export and preserved MP4; both matched declared pins.
3. A separate direct in-memory crop and nearest-neighbor resize of each of
   those three native images was compared byte-for-byte with both root-supplied
   context products. All six output PNG/luma pins, geometries and reconstructed
   pixel identities passed. This verification did not read root's crop-helper
   implementation. No new image was written or displayed by the verification.
4. Exactly the six displays listed above were inspected. Root reported five
   synthetic crop/origin/bounds/scale controls passed before derivation; I did
   not rerun those controls and do not represent that report as my execution.

No observed failure occurred in these verification checks. Hash matches prove
integrity relative to the retained files, not historical authenticity or
correctness of a physical calibration. No acceleration, cause ranking, legal
conclusion, human approval, or canonical-promotion status changes follow.
