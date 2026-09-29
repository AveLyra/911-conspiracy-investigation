# Tilted Camera saved-coordinate and clock source review

2026-09-19. Separate computational source-method review under the [protocol](PROTOCOL.md) and [charter](../CHARTER.md). Research only. This review owns this note and [source-semantics-pins.json](source-semantics-pins.json); it changes no source evidence or case authority.

## Result and permitted calculation

The exact Tilted project supplies an explicit fixed image-to-assigned-world transform and an assigned analysis clock. The held tagged sources are sufficient to specify a conditional reconstruction of its saved image coordinates. Neither the saved settings nor this code audit authenticates the historical analysis engine, the publication's original inputs, physical scale, material-point identity, or exposure clock.

Use the Tilted settings below directly. The Camera3 settings and earlier extraction assumptions are not transferable. No Tilted coordinate values, transformed trajectories, published numerical tables, or fit results were inspected in this lane. Frame indices/keyframe membership and allowlisted non-PointMass configuration were inspected as metadata. No new video image or PDF page was viewed; there are consequently no new claims about the paper's method pages or visible calibration endpoints.

## Source identity and actual coverage

The primary input was the named nested archive in the preserved public ZIP. Current independent SHA-256 checks matched:

| Input | Bytes | SHA-256 |
|---|---:|---|
| Parent `WTC-911-Motion-Lab.zip` | 172774879 | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| `The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz` | 15608229 | `7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552` |
| Nested TRK, zero-based ordinal 4 | 161200 | `babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da` |

The original bytes were read in memory, with DTD/entity rejection and numeric/structural allowlists. No archive member path was used as an extraction destination; no author paths or arbitrary source names were emitted. No Tracker project was launched.

Eight held Java files were read at the precise ranges in the pin receipt. Their current hashes match the prior retrieval receipt, which attributes the OSP sources to commit `6835186f28e1a1c55c2dcb4395b579ddbc2a2eb5` and the Tracker sources to `86f756a731f425a0a37d8171ead24d35446d9705`, both associated there with 6.1.2. This is inspection of those source bytes, not a revalidation of the tags or identity of the historical executable/dependency bundle. The saved project's semantic-version field is `6.1.2`.

The prior clock/source review was fully read; the prior Camera3 extraction script was fully read without execution; its report was searched for source leads and read only at lines 26–37 and 210–220. They directed source lookup and supply no independent Tilted measurement evidence. Early batched tool output was truncated; the relied-on texts and code ranges were subsequently retrieved in bounded outputs. The receipt distinguishes reading from hash-only coverage.

## Coordinate formula, signs, units and fixed state

Let saved image coordinates be `(x,y)`, image-space world origin `(xo,yo)`, saved angle `A` in degrees, `theta=A*pi/180`, `c=cos(theta)`, `s=sin(theta)`, and scales `sx,sy` in image units per assigned world unit. For this project's image coordinates, image y runs downward. Set `u=x−xo`, `v=y−yo`.

The literal `ImageCoordSystem` world-to-image matrix is:

```
x = xo + sx*c*X − sx*s*Y
y = yo − sy*s*X − sy*c*Y
```

Its inverse is:

```
X =  c*u/sx − s*v/sy
Y = −s*u/sx − c*v/sy
```

The source sets the first matrix and calls `createInverse()` for the second (`ImageCoordSystem` 1136–1147); `imageToWorldX/Y` apply that inverse (813–846). The serializer writes angles in degrees (1186–1207), and the loader multiplies by `pi/180` (1080–1099). The scale getters explicitly define image units per world unit (277–296). A positive zero-angle downward pixel displacement produces negative world Y. With unequal scales, divide each image component by its own scale **before** combining it with the rotation; a common denominator is valid here only because the literal saved scales are equal.

| Saved Tilted field | Literal value | Meaning |
|---|---|---|
| `xorigin`, `yorigin` | `470.25`, `349.0` | World-origin position in the project image space |
| `angle` | `-2.5913472025433153` | Degrees; not radians or a video-filter instruction |
| `xscale`, `yscale` | both `1.4841091539439202` | Pixels per assigned world unit |
| `length_unit` | `m` | Assigned length label; independent physical validation remains separate |
| `fixedorigin`, `fixedangle`, `fixedscale` | all `true` | One unchanged configured transform across frames |

The exact TRK has one coordinate framedata object and no `referenceframe` property. The fixed-state setters propagate the saved values to all frames; the serializer reduces fully fixed coordinates to one frame record (`ImageCoordSystem` 150–275, 449–455, 550–556, 653–659, 1040–1058). `TrackerPanel` normally loads the coordinate system before tracks (3941–3967) and can subsequently load a moving reference frame (4006–4011); none is declared here. Fixed flags do not establish a physically fixed camera or depth-invariant calibration.

`PointMass.createStep` defines x/y as image-space coordinates (511–530), the FrameData serializer writes those position values (3355–3393), and the data refresh obtains world positions through `TPoint.getWorldPosition(panel)` (1411–1415). Its pixel columns retain `p.x,p.y` (1464–1465). The held source inventory lacks the `TPoint`/`PositionStep` leaf implementations, so that leaf call was not independently stepped through or executed. The inverse above is directly established for the inspected `ImageCoordSystem`; a claim to have reproduced every runtime call would exceed this audit.

## Frame index, selected step and analysis time

The literal settings are `startframe=0`, `stepsize=6`, `stepcount=80`, `video_framecount=476`, `starttime=-2020.0`, `delta_t=33.36666666666667`, `rate=1.0`, `frame=258`, and `playallsteps=true`.

`VideoClip.stepToFrame(k)` returns `max(0,startframe+k*stepsize)`; the clip tests membership against its selected-frame array. `frameToStep(n)` casts `(n-startframe)/stepsize` to an integer; for the selected nonnegative frames here this is exactly `k=n/6` (`VideoClip` 446–480, 576–581). The configured selection is therefore frames `0,6,...,474`, steps `0,...,79`. It does not claim every selected frame has a saved position.

`video_framecount=476` is the loaded-video count recorded by the serializer, not the number of annotations. In the normal successful load, `setStepCount(80)` also sets the video's selected end frame to `0+(80−1)*6=474` (`VideoClip` 276–302, 648–669, 867–888). A calculation using engine timestamps to reconstruct the controller stretch should therefore use the actual loaded endpoints; it must not substitute frame 475 merely because it is the full video's last frame.

`delta_t` stores mean frame duration in **milliseconds**, while `starttime` is the assigned clip start time in milliseconds (`ClipControl` 340–345, 379–381; `StepperClipControl` 241–287; `VideoPlayer` 513–523). `rate` changes playback scheduling, with division by rate in the timer delay, and is absent from the analysis-time formula (`StepperClipControl` 225–238, 385–396). `frame=258` saves/restores the current playhead (step 43), not a clip start or time offset (`ClipControl` 349, 386–390).

For a valid finite video, let `p[n]` be the historical engine's millisecond frame-time array, `a,b` its loaded start/end frames, `d=33.36666666666667 ms`, and `T0=−2020 ms`. The inspected normal controller path is:

```
S = d*(b−a)/(p[b]−p[a])
n = 0 + 6*k
t_seconds(k) = (T0 + S*(p[n]−p[a]))/1000
```

Here `a=0,b=474` is the expected successfully loaded configuration, not an observed historical runtime state. `VideoAdapter.getFrameTime` returns its `startTimes[n]`, and `getStartTime` returns the current start frame's time (978–1018). `StepperClipControl` computes the stretch and relative step time (266–287, 334–352); `VideoPlayer` adds the assigned origin and rejects out-of-range steps (520–523); `PointMass` uses that step-time method divided by 1000 (1383–1404). The alternative `VideoPlayer.getFrameTime(n)` uses mean-duration arithmetic (533–535), so substituting that caller silently assumes the result agrees on an irregular engine clock.

Under the expressly named **uniform engine-clock hypothesis**, or the controller's no-valid-video fallback with the same assigned duration, this reduces to:

```
t_seconds(n) = −2.020 + n*33.36666666666667/1000
t_seconds(k) = −2.020 + 0.2002*k    (to displayed decimal precision)
```

Do not round selected spacing to 0.2 s, drop the −2.020 s origin, or shift time to force a printed match. A DataTrack time source can override assigned duration/origin (`ClipControl` 235–250); the exact saved track classes are CoordAxes, TapeMeasure and eight ordinary PointMass objects, with no DataTrack class or saved moving-reference declaration. This is affirmative configuration evidence against those particular saved overrides, not a certification of every possible later runtime state. Current FFprobe timestamps are not automatically the historical Xuggle `startTimes` array. Neither clock uncertainty nor a configured offset is evidence that the actual exposure clock was distorted.

## Sparse saved rows and keyframe provenance

Preserve a row's video frame index, selected-step membership, literal numeric presence/finite-value status, and keyframe membership separately. The independently inspected metadata contains the following saved frame objects; this lane did not inspect their x/y values:

| PointMass ordinal | Saved frame objects | First–last frame | Saved keys | Keyframe relation |
|---|---:|---|---:|---|
| PM01 | 75 | 0–444 | 75 | Same indices |
| PM02 | 80 | 0–474 | 80 | Same indices |
| PM03 | 16 | 18–108 | 16 | Same indices |
| PM04 | 30 | 144–318 | 30 | Same indices |
| PM05 | 43 | 150–402 | 8 | Keys 360–402; 35 earlier frame objects are not keys |
| PM06 | 16 | 252–342 | 16 | Same indices |
| PM07 | 34 | 150–348 | 34 | Same indices |
| PM08 | 40 | 210–444 | 40 | Same indices |

The serializer allocates framedata at the step-array length and leaves null entries for absent steps; it saves keys separately (2847–2865). The loader restores null slots and creates the supplied image-space positions at their **frame indices**, then loads the keyframe array; for older files with no nonempty keys it treats all present steps as keys (2908–2954). A null or absent row must not become `(0,0)`, an invented observation, or a compacted time index. Actual PointMass data refresh skips null and clip-excluded entries (1383–1392); it does not itself fill missing positions.

The source comments describe keys as manually **or auto-marked** steps (1188–1189, 1225). Key membership therefore does not establish human marking or independent observations. The program also has a between-key interpolation pathway (1271–1315), using `x_i=x_L+(x_R−x_L)*(k_i−k_L)/(k_R−k_L)`, and the equivalent y formula. Whether that pathway operates depends on a global enable flag and the track autofill flag (1030–1045). No direct `autofill`, `isAutofill`, `dependent`, `isDependent` or `timeSource` properties were found in these eight saved PointMass objects; property absence is not proof of the entire editing history.

For PM05 specifically, all 35 nonkey frame objects precede its first surviving key. They cannot be reproduced as **between-current-key** interpolation using the surviving keys alone. Possible earlier marking, import, editing, changed keys or other history remains unresolved; this review does not choose one. Keep those rows, mark their status, and do not describe 43 independent manual measurements or 35 confirmed interpolations. The later numerical comparison can test narrower arithmetic hypotheses without changing that provenance ceiling.

## Image space, filters and physical calibration

There are zero `filters` properties anywhere in the exact saved TRK, not merely an empty sanitized summary. `VideoAdapter` saves a nonempty filter collection, restores filters in collection order, and displays an enabled filtered image when present (1265–1284, 1316–1327, 134–175, 1079–1103). Thus this project declares no saved filter or static filter rotation to invert. Its coordinate-axis angle acts through the matrix above; rotating the measured coordinates once more would apply an extra transformation.

In the general filtered case, image-space marks refer to the image presented for marking and require the declared filter/display chain before they can be compared with unfiltered pixels. This lane has not audited the absent FilterStack/rotation-filter implementations. It also has not examined encoded video rotation metadata, sample-aspect handling by the historical engine, crops/resizing baked into the MP4, or camera motion. Root's media lane handles current decode geometry. A native-to-display resize or aspect correction requires a declared join: do not combine coordinates from one raster with the literal scale/origin of another.

An assigned metre remains useful for a conditional calculation. Physical interpretation needs visible endpoint/feature identity in the actual source raster, an independent dimensional reference, perspective/depth and pixel-aspect treatment, and their uncertainties. The strongest alternative to a direct physical interpretation is an internally consistent saved calibration applied to a different projected length or processing geometry. Internal tape/scale agreement alone would not exclude it.

## Verification, claim strength and next records

Actual checks used Python 3.13.7, `rg`, `sed`/`nl`, SHA-256 hashing, inert nested-ZIP/XML reads and a synthetic arithmetic program retained in the pin receipt. Twelve transform cases covered zero angle, a quarter-turn and the saved Tilted angle with **unequal** synthetic scales; the explicit inverse agreed with an independent two-by-two inverse and round-tripped with maximum error `8.881784197001252e-16` (<`1e-12`). A synthetic sparse example retained frame/step pairs `(3,0),(7,2)`, excluding an off-grid record and a null slot. A synthetic irregular clock produced 0.010 s from the step-time path and 0.030 s from the mean-only frame-time path, demonstrating the substitution risk. These are arithmetic controls, not execution of Tracker or tests of historical measurements; printed rounding tests belong to the separate comparison addendum.

An initial index-metadata parser assumed keyFrames used individual integer child elements and stopped with an assertion. Structural inspection showed a `[I` array represented by one brace-delimited numeric string. A revised strictly numeric parser succeeded. No source strings were emitted by the failure, no failed result was accepted, and no coordinate values were inspected. All input identities and the exact inspected code ranges are in the receipt.

Post-write verification rehashed 20 pinned local files, all matching, and replayed the retained synthetic program. Its first combined harness reused a variable name from the synthetic program and failed in the subsequent coverage loop; isolated replay and the coverage check then completed. One requested display range ended at line 3400 past PointMass's actual EOF at 3397; the receipt records actual coverage through 3397. These bookkeeping corrections did not change the formulas or results.

The narrow saved-field/code claims are grade A for the inspected bytes; applying the formula to the saved numeric export is a reproducible conditional calculation. Historical engine/export identity and independently physical calibration remain grade C/D, depending on the specific proposition. A source hash, version label, matching table, or correct algebra cannot by itself establish those missing links. Conversely, unresolved provenance does not show that the saved measurement is wrong.

The smallest discriminating additions are: a permitted original exported point/time table with exact media/executable/engine identity and loaded endpoints; the `TPoint` leaf source at the pinned OSP revision if complete call-chain review is required; source-raster calibration endpoints linked to an independent dimension with aspect/projection treatment; and measurement/editing history resolving PM05's nonkey prefix and any claimed publication correspondence. This unit authorizes none of the outreach, project launch, fitting, or promotion that might be involved in obtaining those records.

The evidence-audit skill supplied the competing explanations and falsifiers; the source-of-truth skill kept preserved configuration, direct code semantics, derived arithmetic and historical claims separate. No facts/timeline/Sherlock acceptance, legal position, publication, or source artifact was changed.
