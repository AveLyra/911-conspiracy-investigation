# Camera calibration and acceleration evidence

The available records support more than unscaled visual impressions, but less
than an independently reproduced physical acceleration measurement. NIST names
architectural elevations for its Camera 3 descent analysis. The public motion
lab supplies a floor-spacing sheet, a calibration procedure and a saved metric
transform. These are affirmative, testable calibration leads. Neither a missing
original drawing nor an imperfect access-copy chain makes every conditional
estimate worthless; neither an internally consistent scale nor a published
fit establishes its physical accuracy.[^1][^2][^3]

The most concrete new source correspondence is that the saved **58.293 m** tape
equals **191.25 ft**, exactly fifteen 12.75-ft floor intervals. Several different floor
pairs on the supplied sheet span that length. The calculation confirms a
plausible dimensional basis, not which floors or architectural features the
image marks actually represent. Establishing that same-source endpoint join is
the next useful measurement task, ahead of fitting a new historical
acceleration.[^2][^3][^4]

This research-only audit addresses Q03/Q04/Q05/Q10 under the unchanged
[charter](../CHARTER.md) and [declared protocol](PROTOCOL.md). “Admissible” below
means useful for a specified scientific claim, not a legal evidence ruling.
No historical trajectory is newly fitted, no physical cause is selected, and
no qualified human measurement review is claimed. The independent
[clock/source review](clock-source-review.md), [calibration-source review](calibration-source-review.md)
and [mathematical review](math-review.md) give the detailed boundaries.

## Source-specific calibration ledger

| Record and precise source location | Affirmatively supplied | Remaining join or limitation |
|---|---|---|
| NIST Camera 2 description, NCSTAR 1-9 physical PDF pp. 306–308, printed pp. 262–264 | A high-building midtown view due north; Cameras 1/2 approximately 5–7 km from WTC 7; a CBS-credited Camera 2 illustration. | Published placement is a useful geometric constraint, not an exact survey. Map arrows are explicitly approximate. No exact frame/file/pose join or physical scale for the new Camera 2 outline points is established here. |
| NIST Camera 3 descent, physical pp. 666–669, printed pp. 600–603 | Architectural drawings attributed to Roth (1985); roof parapet elevation 925 ft 4 in; lowest initially visible 29th-floor window tops approximately 683 ft 6 in; about 242 ft visible descent; a separate, near-centre roofline-point analysis. | Original drawing, exact image calibration marks, raw point/time table and detailed fit-window membership remain unchecked in this unit. Parapet, near-centre roofline and the text's later northwest-corner wording need an explicit feature crosswalk, not silent equivalence. |
| NIST Appendix C, physical pp. 746, 749–750, printed pp. 680, 683–684 | Camera 3 broadcast VHS imported as 720×480 DV, non-square pixels, 29.97 fps; camera fluctuations acknowledged; 329-ft façade width and an intensity-intersection vibration method. | This method maps vertical **marker** motion to horizontal **edge** vibration. Its conversion is not a vertical descent scale. The described DV is not established as identical to any present short 15-fps access copy. |
| Public Camera 3 saved project, sanitized settings and source-unit audit | Tape length 58.293 m, equal x/y scale 3.3366687576783383 pixels per assigned metre, saved axis angle approximately 0.7241 degrees; endpoint distance approximately 194.5044 pixels. | Internal endpoint/scale agreement verifies configuration arithmetic. It does not verify real-world tape endpoints, physical length, camera pose, stationary projection or material-point continuity. |
| Public lab instructions p. 3 and one-page floor-spacing sheet | Choose two separated floors, derive their distance from supplied dimensions, convert feet with 0.3048, and align the calibration tape/axes with vertical. The sheet distinguishes nonuniform storey spacings. | These pages do not identify the saved tape's selected floor pair. The sheet gives floor/Roof elevations, without a visible drawing identifier/revision or an image-endpoint diagram. |

The first three rows are **published method attribution**, newly checked against
the complete relevant NIST pages during this bounded unit, not validation of
NIST's structural model. The last two distinguish saved data from instructions
for an exercise. The instructions are source material, not authority to run
Tracker, alter media or accept a finding.[^1][^2][^3][^4]

### Dimensional correspondence without false discrepancies

The independently checked saved tape endpoints are
`(414.3770672546858, 196.24035281146615)` and
`(416.95700110253586, 390.7276736493937)`. Their Euclidean distance divided by
58.293 reproduces the saved scale to approximately `7.35×10^-16` pixels per
assigned metre. Its reciprocal is approximately **0.2997001 assigned m/pixel**.
This agreement is expected when a tape sets the transform; it is not an
independent dimensional measurement.[^4]

Exact unit conversion gives `58.293 / 0.3048 = 191.25 ft`. Three examples from
the sheet demonstrate nonunique endpoint membership:

| Candidate floor levels, not identified image endpoints | Sheet elevations (ft) | Difference (ft) |
|---|---|---|
| 30 → 45 | 688.250 → 879.500 | 191.250 |
| 29 → 44 | 675.500 → 866.750 | 191.250 |
| 28 → 43 | 662.750 → 854.000 | 191.250 |

The sheet's Roof elevation is 921.333 ft and Floor 29 is 675.500 ft. NIST's
925 ft 4 in refers to a **parapet**, and its approximately 683 ft 6 in refers
to **window tops**. Their roughly 4-ft and 8-ft differences from the sheet are
not contradictions between identically defined quantities. They are also not
independent verification of parapet or window dimensions: a drawing/feature
join is still needed. Counting unlike architectural levels as conflicting
measurements would manufacture an anomaly.[^1][^3]

## Clocks, copies and analysis times

The existing encoded frame maps are recoverable and checked. Camera 2's 8,042
frames use a 1/2997-second time base with nonuniform adjacent PTS increments.
The older Camera 3 MP4 has 232 frames at uniform 1/15-second PTS spacing; the
kit MP4 has 443 at the same nominal spacing. Those are **access-copy clocks**,
not newly authenticated original exposure times. The source reviewer checked
all 8,717 existing map rows, not a new decode or all-frame visual review.[^5]

The public saved project also contains meaningful clock settings. The inspected
Tracker source treats `delta_t=66.66666666666667` as mean frame milliseconds;
`rate=1.0` controls playback scheduling, not a multiplier of analysis time.
Starting at frame 138 with step size 3 and step count 102 selects through 441,
but each saved PointMass array has only 71 marked frames, ending at 348.
Under a uniform, correctly loaded engine clock, selected intervals are
nominally 0.2 seconds. The PointMass time path calls `getStepTime()/1000`,
which is not interchangeable with the mean-grid `getFrameTime()` path.[^5]

The historical engine-populated time array and loaded runtime state have not
been reproduced. Current FFprobe PTS therefore cannot simply be relabelled
as the old application's time table. Conversely, the missing join does not
show that its clock was wrong. Conditional analysis using the declared timing
is legitimate if that assumption and its sensitivity are retained.

Two narrower findings prevent overstatement of objections. The kit WMV's three
localized decode warnings occur in countdown frames 37/55/63, outside the
marked collapse tracks. Camera 2's mixed-image interruption occurs well before
the selected collapse interval. Neither finding is evidence of timing damage
to those later marked frames. The shorter Camera 3 copy's patterned temporal
redundancy remains a real recording-process issue, but it does not identify
a unique correction. None of these modern-copy findings automatically
invalidates NIST's separately described DV analysis.[^5]

## From image curvature to physical acceleration

Let physical position be `z(t)` in metres, image position `u=F(z)` in pixels,
and recorded time `s=S(t)`. Write physical velocity as `v`, acceleration as
`a`, and image derivatives with respect to `s` as `u_s` and `u_ss`. For a
fixed twice-differentiable projection and twice-differentiable clock with
`S′>0`, the chain rule gives:

```text
u_s  = F′v / S′
u_ss = (F″v² + F′a)/(S′)² − F′vS″/(S′)³

a = (S′)²u_ss/F′ − F″(S′)²u_s²/(F′)³ + S″u_s/F′
```

The inverse requires nonzero `F′`. Image curvature combines physical
acceleration, changing projection scale and changing clock rate. These terms
are possible error mechanisms, not evidence that large distortions occurred
in the historical footage. The independently derived and tested equations
are detailed in the [mathematical review](math-review.md).

For a constant scale `F=αz+β` and affine clock `s=kt+c`, with `α` in
pixels/metre and `ℓ=1/α` in metres/pixel:

```text
a = ℓ k² u_ss
a_hat/a = (ℓ_hat/ℓ)(k_hat/k)²
```

Length-scale error enters linearly; clock-rate error enters quadratically.
For illustration only, with correct length scale and an analyst assuming
`k_hat=1`:

| Recorded-time rate `k` | Inferred/true acceleration | Effect |
|---|---|---|
| 0.95 | 1.108033 | about 10.8% high |
| 0.99 | 1.020304 | about 2.0% high |
| 1.00 | 1.000000 | no rate error |
| 1.01 | 0.980296 | about 2.0% low |
| 1.05 | 0.907029 | about 9.3% low |

These are synthetic sensitivities, **not measured clock errors or historical
uncertainty bounds**. A constant time-origin offset does not change exact
derivatives. Changing an onset, fitting window or imposed initial conditions
can nevertheless change a fitted acceleration; it is a different operation.

For fixed pinhole projection along an actual straight physical path,
`F(z)=(Az+B)/(Cz+D)`, the affine-clock result becomes:

```text
u_ss = F′/k² [a − 2Cv²/(Cz+D)]
```

Thus even constant physical velocity can have image acceleration. In the
special from-rest, constant-acceleration example `F=αz/(1+cz)`, `k=1`, and
`q=cz`, the baseline-scale ratio is `(1−3q)/(1+q)³`. The declared synthetic
grid from q=-0.05 to +0.05 gives ratios about 1.3413 to 0.7343. That grid is
not a plausible-error claim for either camera. It also is not valid for an
arbitrary evolving silhouette, initial velocity or moving camera.

The distant-camera description constrains this issue positively. If the
camera's actual optical axis passes through the baseline target, slant range
is `R`, the camera-to-target baseline vector has signed vertical component
`h`, and vertical displacement is
`L`, then `q=Lh/R²` and `|q|≤|L|/R`. For an off-axis target the more general
expression uses actual optical depth `Z0`: `q=L d_z/Z0`. Range alone does not
equal optical depth, and one cannot silently reorient the optical axis without
reprojecting the image. NIST's approximately 5–7 km description belongs to
Cameras 1/2, not street-level Camera 3. No numerical historical projection
bound has been calculated here.[^1]

## The reported free-fall interval and its claim ceiling

NIST's final report describes roughly 5.4 seconds for the entire initially
visible, approximately 242-ft descent, against approximately 3.9 seconds for
an ideal from-rest free fall. Separately, it reports an intermediate
approximately 1.75–4-second interval whose numerical-velocity linear fit is
`v(t) = -44.773 ft/s + (32.196 ft/s²)t`, with `t` in seconds and
`R²=0.9906`. These are different
comparisons. A longer total descent time does not contradict a later
gravity-compatible interval, and a selected regression slope does not imply
that the entire descent had that acceleration.[^1]

Nor are percent changes in total time interchangeable with percent changes
in acceleration. For the same distance and a constant acceleration from rest,
time multiplied by 1.4 corresponds to acceleration divided by `1.4²`, not
multiplied by 0.6. WTC 7's reported staged motion is not that constant-
acceleration thought experiment. The lab's page-4 discussion poses questions
about these comparisons; it should not be misquoted as an independent
historical measurement of a single whole-descent acceleration.[^2]

NIST's smooth position fit imposes zero initial position, velocity and
acceleration. Its selected numerical-velocity regression is a separate
calculation, not the constant second derivative of that smooth fit. The
published high R² is not a calibrated uncertainty interval and cannot certify
scale, projection, timing, point identity or window selection. The exact
raw-data regression is not reproduced by checking the printed equation.[^1]

There is no basis in this audit for calling the published gravity-compatible
interval disproved. There is likewise no basis for calling it an independently
reproduced result of the present investigation. A source-pinned reconstruction
with retained assumptions can test it; “not perfectly authenticated” and
“not measurable at all” are not equivalent.

Finally, a visible roof feature is not automatically the centre of mass of a
known, constant-mass body. If that stronger mechanical identification and a
vertical acceleration were established, Newton's law would constrain the net
non-gravitational force on that body. A near-g result alone would not inventory
every connection, identify when every support failed, specify the removal
mechanism, or establish intent. The same measurement standard applies to
fire-triggered and deliberate-removal hypotheses.

## Claim decisions and discriminating tests

Grades concern only the exact proposition: A directly established; C useful
but materially conditional; D underdetermined; E unsupported or contradicted.

| Claim | Layer / grade and decisive evidence | Alternative or failure mode | Test that would change the decision |
|---|---|---|---|
| A real assigned metric transform exists in the public Camera 3 project. | Recorded configuration plus independent arithmetic; A for assigned values. | Correct configuration with a wrong physical reference is possible. | Identify both marks in the exact source raster and match the same architectural levels to dimensions. |
| That transform is already physically validated. | Inference; D. Internal scale agreement and a compatible floor span do not verify endpoints. | Multiple floor pairs and unlike window/floor/parapet levels. | Independent endpoint annotations, dimensional provenance and projection sensitivity. |
| Camera 2's large image displacement can inherit the Camera 3 scale. | E without a cross-camera geometric mapping. | Different pose, raster, depth and feature definitions. | Camera-2-specific dimensional/pose calibration. |
| Saved nominal timing permits conditional estimates. | Configuration/source semantics; C for historical application. | Unknown runtime overrides or engine timing, not demonstrated distortions. | Reconstruct the loaded point/time export against exact media and engine state. |
| Present-copy defects disprove NIST's reported interval. | Inference; E as an automatic transfer. | NIST describes a different source/import chain; known warning locations are outside marked frames. | An exact source/feature/time join exposing a material error in the actual analysed interval. |
| NIST's reported slope independently establishes g here. | Published output A as attribution; D as this investigation's physical measurement. | Calibration, correspondence and fit-window sensitivity remain. | Reproduce raw positions and alternative reasonable fits with justified uncertainties. |
| Gravity can calibrate the same unknown fall used to prove gravity. | E; exact synthetic counterexamples show circularity. | Any chosen acceleration can be returned by choosing a scale accordingly. | Use geometry or a separate authenticated calibration experiment, not the acceleration under test. |
| A roof-feature acceleration alone identifies cause or universal support loss. | D/unsupported inference. | Feature deformation, unknown moving system and multiple mechanisms can fit the same terminal motion. | Multi-feature geometry and a specified mechanical system, then competing mechanism predictions beyond terminal kinematics. |

The circularity example is a safeguard, **not an allegation that NIST or the
lab chose a scale by assuming free fall**. Their described dimensional methods
are affirmative contrary evidence to that allegation. The producer's toy
target of 10 m/s² is not a measurement of local gravity.

## Next measurement and broader investigation

The next bounded WP2 task is a source-raster endpoint check: locate the saved
tape endpoints and named target features in already preserved public images
of the actual referenced Camera 3 recording; identify candidate floor/window
levels using explicit image annotations; compare at least two plausible
dimensional assignments and projection assumptions. Preserve unresolved
identities. No floor pair may be selected because it yields g. If existing
imagery cannot resolve the endpoints, specify the exact needed drawing or
higher-quality frame rather than declaring calibration universally impossible.

Only after that join should a conditional physical-unit trajectory be fitted,
with actual source times, declared alternative timing models, interval
sensitivity and human review before a consequential force/causal claim. The
global investigation remains incomplete; this is not a substitute for WP1's
fire map, WP3's building-specific chain and released-model review, the
comparator work, or affirmative documentary/physical evidence tests.

The newer supplementary production is separately inventoried and has a
separately recorded content audit. No new production or held-packet contents
were used in this camera audit. Earlier missing-record statements must remain
version-specific; this unit establishes neither continued blanket unavailability
nor a newly complete model. No causal ranking changes on these results.

## Sources and reproducibility

[^1]: NIST, *NCSTAR 1-9, Structural Fire Response and Probable Collapse Sequence of World Trade Center Building 7* (2008), [preserved PDF](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf), physical PDF pp. 306–308, 666–669, 746, 749–750. SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`. Physical and printed page numbers are distinguished above. Source/render integrity is checked, not historical or engineering fidelity.

[^2]: David Chandler, *The Downward Motion of WTC Building 7 on 9/11/2001*, [public lab instructions](</Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/Lab-Instructions.pdf>), all five pages inspected, especially pp. 3–4. SHA-256 `c3a9c7aa44f914dbcc7dd2e5604020db0466de8c27f9d71f70d485b80aeb5557`. Calibration instructions and attributed interpretation are not new independent measurements.

[^3]: *Elevations of Floors of WTC 7*, [one-page kit sheet](</Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/WTC7 Floor Spacing.pdf>), no visible drawing identifier/revision. SHA-256 `8dacd6cbb61b554c21da2cfa6447ebbb3248a06d04a44596b5c31088e5beb411`. Sheet values are attributed dimensions, not a newly authenticated building survey.

[^4]: Public Camera 3 project, [sanitized saved settings](/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/saved-tracker-settings.json), SHA-256 `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb`; source XML hash and inert-data comparison in [clock-source review](clock-source-review.md). Root's Decimal/rational configuration and floor-pair checks are in [source-check-root01.json](source-check-root01.json) and [verify_sources.py](verify_sources.py).

[^5]: [Clock/source review](clock-source-review.md) and [36-input pin/coverage record](clock-source-pins.json), including the original timing, Tracker-source, cadence and warning-location dependencies. Previously decoded maps were checked; media were not newly decoded or rehashed in that source pass. See [validation](validation.md) for the current unit's exact coverage, retained lookup failures, synthetic runs, independent reproduction and review dispositions.
