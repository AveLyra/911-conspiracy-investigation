# Which held records identify the moving material?

2026-09-24. Bounded review of existing research derivatives; no new video,
PDF or raw-model inspection. `/root/body_mass_sources` separately reviewed the
structural/motion joins and returned its findings before reading root's new
synthesis. Root records that review here and independently checked the numeric
inventory fields noted below. Neither reader is a licensed structural expert.

## Positive evidence and the missing joins

| Proposed fixed material set | Affirmatively available | Unresolved bridge to a historical COM bound |
|---|---|---|
| All original building material, retained as the same set even after fragmentation | The released model has extensive geometry, typed element/part definitions and static bounds. | No demonstrated equality between this mesh inventory and all historical constituent mass; no observed or independently validated time-dependent location/envelope for all those particles. Fragmentation does not invalidate the set, but obscured/dispersed material cannot silently be dropped from it. |
| A region defined by original material membership, such as specified stories | Architectural elevation leads, a floor-spacing sheet and model-coordinate bounds. An original-coordinate cut can be a reproducible *model* selection rule. | No authenticated story/datum/member join or independently checked complete time-dependent envelope for such a selected region. A changing spatial “falling block” may exchange mass; that is not the same system. |
| A named facade assembly or component patch | Camera3 A/C supports approximately common apparent motion, and the louver-bank association narrows the target's architectural region. | Exact material identity, extent, depth, attachment and three-dimensional deformation remain unidentified. Its net force would include connections/contact with the rest of the building and would not inventory whole-building supports. |

The [Camera3 facade study](../camera3-facade-feature/report.md) admits one
constant two-dimensional A-C separation inside both observers' original
placement boxes at twenty of twenty-two selected samples. It links C to the
lower-west louver-bank region at Floors46/47 but does not identify an exact
steel node, trim attachment, recess depth or COM. This is **positive image
evidence**, not merely a list of missing records. It is not proof of a rigid
material assembly: two projections can remain compatible for several reasons.

Crucially, the preceding finite-interval numbers use the published **Camera2**
table. The stronger A/C localization concerns **Camera3**. It cannot be imported
as a bound on Camera2's point/COM separation without a same-material, same-time,
geometric correspondence. The [Camera2 join](../camera2-paper-frame-join/report.md)
locates NW and lower-WC candidates in two fixed frames, EC only in the later
frame, and leaves NE smoke-obscured. The older upper-step T2 is not lower WC.
These are precise coverage limits, not proof the published table is wrong.

The later [calibration-endpoint study](../camera3-calibration-endpoints/report.md)
also retains affirmative approximate-scale evidence: a repeated thirteen-pixel
facade period and a roughly fifteen-cycle span. The lower tape endpoint remains
obscured/unidentified. The [conditional trajectories](../camera3-conditional-trajectories/report.md)
and [lateral-geometry audit](../lateral-geometry-audit/report.md) retain actual
curvature and conditional lateral-motion evidence. Their differing sources,
targets, clocks and error models must not be blended into a new physical bound.

## Located mass/geometry fields, not a missing-everything finding

The existing [member map](../model-member-map/run06/member-map.json) contains
3,593,049 unique nodes and geometry bounds for all392 used parts. It distinguishes
3,006,910 shells,3,190 beams,33,364 discrete elements and2,461 mass-component
solids. The union of all used-part bounds is
`[-80,-50,-95.4786]` to `[50,40,98.0948]` in **model coordinates**. This is
static, may include contextual/support components, and has no collapse-phase
time index. It is not an authenticated historical full-body vertical envelope.

Four parts in SRC-119 are indexed as `*MAT_RIGID` mass-component solids:

| PID = MID = SID | Solid records | Model Z bounds | PART data-card line | MAT keyword line |
|---|---:|---|---:|---:|
|1|448|−71.17079926 to −70.86599731|58|2|
|2|448|−71.17079926 to −70.86599731|63|9|
|3|377|82.06739807 to82.37220001|68|16|
|4|1,188|82.06739807 to82.37220001|73|23|

The [material crosswalk](../material-run-crosswalk/run01.json) indexes these
material definitions but does not export their numeric cards in
`selected_materials`; that array covers MID50 and nineteen transformed
counterparts. This is an extraction-scope limit, not evidence that density
or mass information is absent from the preserved source. SRC-119 is the held
`discrete_mass.k.gz`, whose prior receipt reports70,199 compressed bytes,
508,372 uncompressed bytes and7,905 lines; compressed SHA256
`2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7`.
That source was not decompressed or newly authenticated here.

The same crosswalk exports MID50's density field12260.85 at SRC-121 line1759.
It is a solver-assigned value, not measured physical steel density or a
whole-building mass. The prior [primary-method ledger](../material-run-crosswalk/method-source-review.md)
locates NIST's separate equipment weights and density-scaled25%-live-load
description at NCSTAR1-9A physical103–104/printed52–53. It also identifies
connection grouping/calibration at73–75/22–24 and attachment/contact at85/34.
Those are existing report attributions, not a newly reconstructed mass budget.

## Scope, checks, and precise remaining record

The source reviewer read the five initial reports (member-map, material/run
crosswalk, metric-motion, lateral-geometry and finite-interval force), then the
Camera3 facade and Camera2 paper/frame reports and the directly necessary
material-method source ledger. It used bounded `jq` queries on the two numeric
inventories. Root separately read those reports plus Camera3 endpoints and
conditional trajectories, Camera2 target-trackability and the multipoint-table
report. No new raw-deck parsing, video review, PDF page inspection, network
retrieval, solver or accepted-engine change occurred.

Root separately queried part definitions, geometry, typed element counts,
SRC-119 material-index rows and `selected_materials` IDs. Source hashes:

- member map: `eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e`
- material crosswalk: `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594`

The narrowest promising historical target is an identifiable facade assembly.
Its previously named record dependency is an original north-elevation/lower-
west-louver detail establishing trim-to-slab offset, depth and attachments,
joined to same-time calibrated material landmarks. Whether such a drawing is
elsewhere in the holdings is not decided by this bounded review. A complete
geometric envelope can bound COM without a detailed mass distribution; a tighter
mass-weighted analysis would additionally need material membership/load allocation.
The latter's located mass cards can advance a **model** budget but cannot by
themselves recover historical COM motion. No cause ordering follows.
