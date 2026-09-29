# Conditional saved-point / native-raster method review

2026-09-24. Independent computational method review, frozen before this
reviewer sees any new native image, point overlay or observation result from
this unit. Research working material under the main investigation charter;
not historical measurement, expert approval, physical validation or a legal
finding. The [protocol](PROTOCOL.md) controls the selected 50 frames / 83 rows.
The reviewer owns only this file.

**Current unit status:** the final read-only file inventory contains only
`PROTOCOL.md` and this method review. No new-unit implementation, extraction,
overlay, observation or verification-result files exist in that inspected
directory. The tests below remain a contract, not completed verification.

## Decision and scope

**H0 is a source-supported, reasonable first mapping to inspect, but is not
proved:** use saved PointMass image-space `(x,y)` directly in the current
720 x 480 native Tilted raster, with x right and y down, without a world-axis
rotation, zoom multiplication, sample-aspect correction or fitted adjustment.

There is affirmative support beyond the absence of filters: the exact saved
TrackerPanel declares image dimensions **720.0 x 480.0**, matching the current
decode, and saves its magnification separately. The held source code also
separates image positions from world coordinates and UI zoom. No contradiction
between those saved dimensions and the current raster was found. This does
not reproduce the historical engine's pixel construction or certify the
identity of the media used when each row was marked.

Reading a fixed source-derived point on its own image is a useful next test
after the prior independent observations have been frozen. It must be labeled
source-guided, not independent feature selection. It can proceed without a
new acceleration experiment or full recovery of the paper's editing history.
The charter's human/specialist and consequential-measurement gates remain
unmet; this review supplies neither.

## Direct support and the precise remaining gap

1. **Saved point namespace.** Held `tracker-6.1.2-PointMass.java`, lines
   511-530, declares `createStep(n,x,y)` coordinates to be image-space values.
   Lines 3355-3393 serialize/restore the position's x/y. Lines 2908-2934
   restore rows at their original frame indices, not compacted row ordinals.
   Lines 1411-1415 separately obtain world coordinates, while 1464-1465
   retain `p.x,p.y` as pixel columns. Thus an image overlay must not first
   convert the saved x/y into assigned metres or rotate them by the saved
   world-axis angle.
2. **Saved dimensions and zoom.** In the byte-pinned nested TRK, root
   `width=720.0`, `height=480.0`, and `magnification=1.7817974362806785`
   occur at `/*[1]/*[2]`, `/*[1]/*[3]`, and `/*[1]/*[4]` respectively.
   They are also in `project01.json`, `settings_objects[0].fields`.
   Held `TrackerPanel.java` lines 1667-1704 call width/height image units;
   1616-1646 turn magnification into preferred UI dimensions; 3789-3803
   load image dimensions and magnification separately; 4092-4097 save them
   separately. The saved zoom is therefore not a multiplier to apply to the
   saved coordinates when using native images. Missing `VideoPanel`/`TPoint`
   leaf implementations limit a complete runtime proof, not this observed
   separation in the held caller code.
3. **Draw/filter contract.** Held `osp-6.1.2-VideoAdapter.java` lines 88-90
   distinguish raw-image dimensions and filtered displayed dimensions.
   Lines 140-175 draw the image with the panel transform and, in image-space
   drawing, without the world-coordinate transform. Lines 1265-1284 save a
   nonempty filter stack; 1316-1327 restore saved filters. A fresh in-memory
   inspection of the exact TRK found zero `filters` properties. This supports
   testing an unfiltered mapping; it is not proof of no earlier baked resize,
   historical runtime filter, replacement media or engine-side transformation.
4. **Current native media.** The retained probe records 720 x 480 YUV420P,
   476 frames, sample aspect 131:144, display aspect 131:96 and time base
   1/60000. The declared probe requested stream rotation/display-matrix side
   data; none is present in its saved stream result. The existing extraction
   command explicitly used `-noautorotate`, `-noautoscale` and passthrough
   timestamps. These describe the preserved present-day asset/decode, not
   the historical Xuggle engine's raster. A correctly aspect-presented movie
   and an uncorrected native raster can look different without either file
   having changed. H0 concerns native raster coordinates, not physical aspect.

The current hashes of the three Java files match the prior source-semantics
receipt. They are held source versions attributed by that receipt to 6.1.2,
not authenticated historical executables. The saved project also says 6.1.2.
No new engine, Java application or Internet retrieval was used here.

## Source-grounded alternatives, not fitting freedoms

The following distinctions prevent an apparent overlay mismatch from becoming
an excuse to try arbitrary transforms:

- **UI zoom / viewport:** the saved magnification and panel source show a
  display transformation. A comparison to a saved screenshot would require
  its origin/viewport/zoom, but this is not an alternative transform for H0's
  native raster. Do not multiply by the saved magnification here.
- **Sample-aspect presentation:** the current non-square sample-aspect field
  is a real reason to question historical display handling. If primary
  evidence later shows that marks were stored in an aspect-resized raster,
  its actual dimension/origin/resize convention would define an inverse
  mapping. The ratio alone does not establish that premise, resampling
  convention or pixel-center offset. Do not silently try a horizontal
  correction and select whichever places a point on a desired feature.
- **Saved world coordinates:** the reviewed ImageCoordSystem inverse is the
  correct conditional route from saved image x/y to assigned world X/Y.
  It is not a competing pixel-to-pixel transform. Applying its axis angle
  again to the raw image-coordinate marks would mix namespaces.
- **Different media / baked processing / runtime filter:** these remain
  unresolved provenance possibilities. A located alternative saved version,
  dimensions, filter parameters or documented processing chain could define
  a new mapping. Mere mismatch does not supply those parameters. The prior
  Camera2 scene-resize/scoring branches and approximate frame joins do not
  authorize a 640-pixel-width transformation or time shift in this audit.

No fully specified alternative native-pixel mapping, supported strongly enough
to replace H0, was established in the held inputs inspected here. That is a
bounded source-review conclusion, not an assertion that none existed.

## What a point-to-image result can discriminate

H0 predicts where a stored coordinate will be displayed under the declared
mapping. **It does not predict that the analyst selected a real material point,
that a visible corner persists, or that every saved position was directly
observed.** A point displayed on smoke or a straight edge could reflect a bad
mark, occlusion, a geometric construction, generated/imported values, changed
feature identity or a wrong raster association. An isolated disappointing
overlay therefore does not uniquely falsify H0, much less establish fabrication.

Conversely, good-looking placement at all rows would support compatibility of
the saved marks with this representation, not independently prove the mapping,
physical scale, historical marking process or publication-version identity.
Numerical table correspondence shares these dependencies. The lower-feature
report's disappearing step appearances are a motivation for the audit, not
ground truth against which every later point must fail.

Preserve PM05's 35 nonkeys and eight keys and PM08's 40 keys. A consistent
later roof-edge construction is a meaningful possible outcome; it must not
inherit the earlier step-foot or a material-particle interpretation silently.
The protocol's host/feature/relation categories and reasons can express this
without a newly tuned pixel-distance threshold. Systematic mismatches justify
a specifically bounded mapping/provenance check, not free transform fitting.

## Minimal synthetic representation contract

The protocol's nearest-cell display is adequate for a qualitative reading aid
if the following software properties pass before historical presentation:

1. **Native-frame lineage:** retain original indices, exact rational PTS,
   mode/geometry and luma hashes. Verify every decoded frame against the
   existing 476-frame record; produce exactly 50 chosen frames and 83 point
   rows. Wrong index/hash, duplicate or missing required rows, unsupported
   geometry and unexpected diagnostics must fail explicitly. Existing
   decoder controls may be reused only when their code/runtime relevance is
   documented; changed adapters need their own bounded checks.
2. **Unmodified image regions:** a known coordinate-pattern synthetic image
   must reproduce every full-scene pixel and each valid source crop pixel.
   The 60 x 60 half-open crop must become exactly 180 x 180 by 3 x 3 cell
   replication. No tone adjustment, smoothing, SAR resize, axis rotation or
   feature fitting is permitted. Padding has a separate validity mask; it
   must not be confused with observed black/white pixels.
3. **Rounding and marker:** independently check `floor(x+0.5)` on integer,
   fractional and exact-half fixtures, including negative values. The selected
   source cell is crop index (30,30), whose replicated central display pixel
   is (91,91). Verify the marker/gap footprint independently and keep the
   unmarked crop alongside it. Preserve exact saved coordinates and rounding
   residuals. This is the declared display convention, not recovery of
   Tracker's subpixel sampling convention or a localization error bound.
4. **Boundary distinctions:** evaluate the original coordinate's membership
   in the declared continuous native domain separately from its rounded
   display cell and crop coverage. For example, x=-0.4 rounds to 0 but remains
   out of frame; x=719.8 lies in [0,720) but rounds to 720 and needs explicitly
   marked padding. Never clip a source coordinate into a valid-looking point.
   Cover all four edges/corners, entirely outside crops, nonfinite/boolean
   inputs and missing-track counterparts without inventing zeros.
5. **Independent verification:** use a separately written crop/round/marker
   oracle, not the producer's own drawing routine as its expected result.
   Check all historical native/unmarked crop pixels, the exact row-to-frame
   association and all marker locations. Two same-code repeats check
   determinism, not independent correctness. Keep exclusive output creation,
   input/output hashes and retained failures.

No synthetic acceleration, classifier or collapse simulation is required for
this display audit. Such tests would not resolve raster identity. If new
automated historical localization, motion or force inference is later added,
the relevant synthetic ground truth, actual human spot-check, physical
calibration, uncertainty and independent-reproduction gates must be met
separately; this note does not authorize that expansion.

## Evidence receipt, exposure and verification

Read current main AGENTS, WORKFLOW, START-HERE and the complete charter;
read the current lower-feature report, this protocol, the prior
project-export review and source-semantics review/receipt. The lower-feature
report was read only after its independent observations were frozen. No new
historical image, marked overlay or new-unit observation has been viewed.
Earlier metadata work exposed first/last saved point values; that exposure
does not constitute a blind point-selection record and is not concealed.

Primary-source checks actually performed, read-only and stdout-only:

- `sed -n` / `rg -n` over the exact Java ranges cited above; `shasum -a 256`
  confirmed PointMass, TrackerPanel and VideoAdapter against the prior receipt.
- Ruby JSON queries read only saved root dimensions/zoom, current probe
  geometry and source identities; the project hash matched its existing pin.
- A `python3 -B` in-memory ZIP/XML query rehashed the exact parent ZIP, named
  TRZ and zero-based TRK entry 4, rejected DTD/entity declarations, then read
  only direct root width/height/magnification and counted filter properties.
  Actual result: 720.0, 480.0, 1.7817974362806785, zero filters. No XML, media
  or new measurements were written.

Source pins: project01 `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`;
TRK `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da`;
probe JSON `778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de`.
Protocol read at `50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d`;
lower-feature report read at `6cb016644a05c6d901bc0b0829419a3cc5ac87c2bd427d09aa9b27f664847702`.
Main charter remains `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.

Preserved execution limitations: an initial combined read was truncated; the
relied-on charter/source sections were reread in bounded output. Default
file discovery omitted ignored new units; the corrected `--hidden --no-ignore`
listing located them. A guessed `probe01/receipt.json` did not exist; the
actual `probe01/execution.json` was read. One metadata hash-summary command
failed with a Ruby syntax error; its corrected read-only form succeeded.
No failed result was adopted. No synthetic tests or historical decoder were
executed by this reviewer; the controls above are proposed acceptance checks,
not claimed passes.

The evidence-falsification and source-of-truth skills shaped the conditional
claim, competing provenance explanations and separation of display validation
from physical evidence. Only this working review is added; no authority is
promoted, no preserved input changed, and no external disclosure, legal work,
solver/bridge activation, commit or push occurred.
