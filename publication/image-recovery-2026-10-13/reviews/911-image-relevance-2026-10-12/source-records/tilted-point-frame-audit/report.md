# What the saved Tilted Camera points visibly identify

2026-09-24. Research-only source-guided audit, not a new trajectory or cause
test. Main charter and record-preservation controls remain authoritative.

## Result

Under the declared native-raster mapping, the saved PM05/PM08 positions have
substantial visual association with the building's upper outline. Early
positions are near recognizable lower roof-step turns. Later positions mostly
follow a straight roof-edge neighborhood or enter smoke/face overlap, where
the original turn is not separately identifiable. This is a concrete limit
on interpreting those saved positions as an authenticated, continuously
visible material corner; it is not a demonstration of invalid motion data.

Two separately frozen AI readings cover every one of the **83 saved rows on
50 frames**. They agree on all three categorical labels for **63/83 rows**;
all **20 disagreements** remain preserved. Much of the middle-interval
disagreement concerns the width of a "corner neighborhood": both descriptions
often see the marker on the adjoining edge, but one still calls the nearby
turn a candidate and the other calls the local edge a different feature.
There was no preregistered distance threshold to settle that distinction.
Agreement counts therefore measure reproducibility of these descriptions,
not accuracy, independent data, or probabilities of a collapse cause.

**Source-definition qualification:** the paper itself calls EC/WC **roofline
points**, not necessarily persistent material corners. The predefined
lower-step-foot test is our more specific correspondence question; failing
to authenticate that foot is not automatically failure of the paper's actual
observable. The source-method follow-up below matters to any criticism.

The strongest objection to a sweeping criticism is that a moving roof-edge
position or geometrically constructed intersection can be a legitimate
observable even when a particular physical corner disappears. Conversely,
an apparently sensible mark near the roof cannot by itself validate the
original analyst's feature definition, interpolation, exposure clock,
physical scale, projection correction, or published acceleration.

## What was tested

The [prospective protocol](PROTOCOL.md) selected **all**, not favorable,
PM05/PM08 rows from the already-held project. PM05 has 43 rows at frames
150–402 in increments of six: 35 nonkeys followed by eight keys. PM08 has
40 rows at 210–444, all keys. A saved key does not prove human marking;
nonkey status does not by itself identify the generating procedure.

H0 is literal image x/y on the current native 720×480 raster, x right/y down.
Saved panel dimensions and inspected software semantics support testing that
mapping. Its historical engine/aspect behavior and exact publication-version
association remain conditional. Current sample aspect 131:144 was **not**
applied. No rotation, shift, fitted transform, relocated point or retiming
was introduced to improve the pictures.

Every panel contains the untouched full native luma image, plus separate
plain/marked 60×60 crops enlarged 3× by nearest-neighbor replication. Gapped
markers indicate rounded saved pixels, not measured feature centers. Source
coordinates, keys, exact encoded PTS, rounding differences, masks and pixel
hashes remain in [run01/manifest.json](run01/manifest.json). Encoded PTS are
not authenticated exposure times or the analyst's assigned clock.

Both prior-informed AI readers viewed all 50 complete panels, every available
crop pair, in ascending order, before exchanging interpretations. They were
not blind to source labels, saved points, prior footage or the paper's feature
definitions. The [root record](root-observations.md) and
[separate observer record](observer.md) contain all reasons, alternatives and
actual-view hash manifests. Zero panels were skipped or failed. This is not
qualified human acceptance or independently selected tracking.

## Where the readings converge and differ

All intervals below refer only to the saved six-frame grid, not every video
frame or an inferred physical transition time.

| Selected rows | Source-guided description and retained difference |
|---|---|
| PM05, 150–246 (17 rows) | Both call the neighborhood building / corner-or-junction / candidate lower foot. Blur and proximity do not validate exact subpixel placement. |
| PM05, 252–318 (12 rows) | Both reasons describe a nearby step turn and a mark on or beside its adjoining lower edge. Root retains a broad corner candidate through312, then unresolved; observer classifies the local segment as roof-edge / different-feature. No measured displacement error follows. |
| PM05, 324–366 (8 rows) | Both find a roof-edge neighborhood without an identifiable original foot. The first two saved-key rows,360/366, are in this group; keys do not restore a visible corner. |
| PM05, 372–402 (6 rows) | Root still sees a faint edge through384; observer calls those neighborhoods mixed/uncertain. Both call390–402 mixed, with uncertain versus none-resolved at390. Neither identifies the original foot. |
| PM08, 210–324 (20 rows) | Both retain a candidate lower right step foot, with explicit rounding/halo/nearby-edge qualifications. |
| PM08, 330–336 (2 rows) | Observer separates the marked edge from the remaining turn to its left. Root leaves correspondence unresolved, retaining a junction-neighborhood label at330. |
| PM08, 342–432 (16 rows) | Both see a roof edge and leave original-foot correspondence unresolved. A visible contour is not an authenticated material point. |
| PM08, 438–444 (2 rows) | Root retains a soft edge; observer cannot confidently separate haze and face locally. Neither claims a recovered foot. |

Across all 83 rows, label agreements are host **78**, feature **64**,
lower-foot relation **69**, and the complete triple **63**. By track, complete
triple agreements are PM05 **27/43** and PM08 **36/40**. The
[all-row comparison](comparison.md) preserves each mismatch and checks both
records against the selected source rows and viewed files. No majority vote,
retroactive recoding, calibrated offset or favorable-frame selection was used.

These observations are not independent corroboration of the preceding
[Camera2 lower-feature review](../camera2-lower-feature-continuity/report.md):
the clips share image ancestry, the representations differ, and current source
coordinates cue where to look. A more positive early classification under
source guidance does not authenticate the historical feature definition.

## What the numerical verification establishes

The [verification report](verification.md) and [execution record](validation.md)
separate software controls from visual interpretation. Two fresh producer
runs agree byte-for-byte on all **357 substantive products**. Both reproduce
the held 476-frame decoded/luma hash and exact-PTS records. Independent code,
without importing the producer, checks the 83 source rows, all 349 PNGs,
full panel pixels, crops, masks, markers and labels. Root repeats that check.

Final producer controls pass13 tests; final verifier controls pass15 tests,
each repeated by root. An earlier inaccurate synthetic-only caption and an
overstrict font-bearing checker both remain in the retained history. Neither
was silently presented as a successful final check. The original image/crop
pixel rules were not relaxed. These are presentation/repeatability passes,
not structural-model, historical-tracking or scientific-causation validation.

The verified source project is SHA256
`4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`;
embedded video
`393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f`.
Root observations froze at
`e31b2f9cbc880872aec69201c155f27c0aa3d3bed9bb5cea8d7748976c853a76`;
observer observations at
`9fe612f5df31b4a37557b57cde83d9f979499a5bf48744c06726ef4873b3b117`.
Integrity hashes establish byte identity, not historical truth.

## Bounded primary-method follow-up

After both visual records were frozen, a separate reader checked the held
paper's method passages and the held motion lab instructions. Root then
independently extracted the complete text of paper pages10,13,44,45 and
lab-instruction page3 with pypdf. This was a text check, not a new visual
figure inspection or layout verification. The
[method follow-up](method-followup.md) records the other reader's wider
bounded scope and precise locators.

Paper page13, section3.1/Figure4, identifies EC as east-center roofline and
WC as west-center roofline. Pages44–45 link the plotted series to those
colored Figure4 labels. Page10 describes an earlier central roofline point
chosen to approximate NIST's point aligned with the east edge of the louvers;
it does not say every later central measurement follows one visible material
corner. The paper's hash is
`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.

The lab's page3 describes generic manual marking/refinement and the alternative
of automatic positioning. It does not specify an EC/WC-specific continuation
or construction rule after obscuration. Its hash is
`c3a9c7aa44f914dbcc7dd2e5604020db0466de8c27f9d71f70d485b80aeb5557`.
Generic instructions do not establish which procedure generated these rows.
The already-exported saved numerical state is also not a complete record of
all descriptive/UI metadata or editing history; uninspected material cannot
be treated as absent. No raw omitted fields were inspected here.

## Consequences and the next discriminator

This narrows a real uncertainty: we now know what all selected saved marks
visibly neighbor under H0, rather than inferring their meaning from a track
name, numerical match, or eight unrelated stills. It does not explain how
the nonkeys were created, why particular saved/publication rows differ, or
what observable the analyst intended after the step became indistinct.

The existing [source/table audit](../tilted-camera-source-join/report.md)
already establishes PM08's conditional displacement correspondence and
PM05's retained all-row differences; it should not be rerun or promoted to
physical validation merely because this visual audit has completed.
No new position, velocity, acceleration, support force, heating estimate,
failure timing or mechanism likelihood was measured here. The integrated
assessment remains **no earned strict ordering**, not equal odds, between
the presently unresolved causal hypotheses. This unit neither validates
NIST's fire-to-failure chain nor supplies affirmative operational evidence
of deliberate intervention.

The useful remaining discriminator is a **specific saved construction/editing
record or better-linked project version**, not another generic viewing of these
same panels or repeat read of the method pages just checked. A bounded next
unit may inventory narrowly allowlisted technical descriptions/track metadata
in the already-held public project, preserving author paths, arbitrary text
and sensitive strings from unnecessary display. First declare that read's
scope and do not execute the project. An unchanged/unspecified method is a
valid result; it is not misconduct. Distinguish direct marking, inferred
intersection, interpolation and an unreported choice; do not substitute a
guessed method. Alternatively, a new independent measurement can explicitly
define a projected roof-edge observable without claiming material-corner
continuity; it still needs preregistered uncertainty, calibration and actual
human review. Better originals or a specifically linked alternative project
may resolve more; merely adding the same frames does not.

The evidence-audit skill required all-row coverage and retained competing
readings; development verification required explicit representation tests;
source-of-truth controls kept the result in research. Main/raw/legal sources
and accepted Sherlock/Faraday engines remain unchanged. No external retrieval,
private-packet access, solver execution, send, filing, promotion, commit or
push occurred. The rounding/domain lesson is queued locally under existing
Sherlock feedback IDs, not sent to the archived destination. Full investigation
and all-Luna attribution coverage remain incomplete.
