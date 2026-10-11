# Cyan and purple energy-curve readings

October 8, 2026. The fixed eight- and nine-bolt regions have two separately
frozen readings each. Both show locally distinguishable continuous and broken
strokes, with disputed faint edges and model attribution near close approaches.
The four annotations and two comparisons reproduce exactly. These are readings
of a published model graph, not observations of the building or accepted
physical measurements. Separate source, annotation and comparison checks are
complete for this finite batch; human acceptance and physical support are not.

## Coverage and method

The [protocol](PROTOCOL.md) froze this batch before its new pixel readings.
The unchanged Im7 strip is 745 by 92 pixels. Readers viewed the complete strip
and composed page, then read every raw context cell in finite, untruncated
blocks. The display omitted only exact white. Coordinates came from those
native cells, not the resized overview page. Source-reading receipts and
limitations are retained in each annotation.

| Region | Target box, upper edges excluded | Context records per reader | Model-route records per reader |
|---|---|---:|---:|
| E8 cyan | [535,54,690,86] | 5,724 | 310 |
| E9 purple | [530,30,690,56] | 4,920 | 320 |

The 10,644 context records include overlapping source positions, not 10,644
independent observations. Solid/Spring and dashed/Shell identities use the
confirmed legend and local continuous/broken style, not height alone. Manual
literal runs expand mechanically; RGB is used to diagnose transcription
mistakes, not to select or erase cells. Each dash body keeps a local identifier;
no gap is interpolated or seam automatically joined.

Unassigned material is recorded once rather than attributed to both models.
E8 root supplies 155 explicit band records; the peer supplies one contact-band
record. E9 supplies 160 band records per reader. Empty and missing band records
remain different; neither establishes absent original ink or zero support.
The readers froze before exchanging substantive readings. They are
prior-informed AI readers of the same source, not blind human observations.

## What differs

These counts compare readers, not spring versus shell physics. An outer set
combines confidently selected core and tentative fringe. A one-cell fringe
difference counts as a different column; the table is not a displacement
error, model-accuracy score or statistical confidence interval.

| Comparison | E8 | E9 |
|---|---:|---:|
| Model-route entries compared | 310 | 320 |
| Different outer sets | 129 | 37 |
| Different core or fringe classes | 135 | 38 |
| Different status labels | 53 | 41 |
| All-selected-ink columns compared | 155 | 160 |
| Different all-ink outer sets | 142 | 52 |
| Different all-ink classes | 143 | 54 |

The [E8 comparison](comparison-E8-01.json) and
[E9 comparison](comparison-E9-01.json) retain every original record and set
operation. Both repeated saves are byte-identical. No selected exact-white
cell was found in the four annotations. Nonwhite cells can still be artifacts
or have uncertain curve membership; passing that diagnostic does not resolve
these questions.

For E8, root leaves columns 535–539 unassigned because the strokes are close.
The peer assigns separate pieces and retains cell (535,76) as a shared-edge
uncertainty. The participating peer considers those early assignments less
secure than the well-separated strokes. Root also retains more pale dash-edge
and interbody material, including row 64 alongside much of the later dashed
trace; the peer commonly omits that row. This accounts for many differing
outer sets without establishing a different principal curve trajectory.

For E9, the peer leaves nine interstitial cells unassigned: columns 536–537
at row 49, 547–549 at row 47 and 554–557 at row 46. Root attributes those to
solid fringe. Root records pale material in 35 interbody columns without model
identity. The peer often leaves it unselected, but tentatively attaches some
endpoint cells to a dash body, including (533,52), (542,50) and (618,47).
Neither their tentative assignment nor their nonselection establishes the
original mathematical curve's membership. Some slope and endpoint cells also
differ in core/fringe classification.

Post-exchange critique found no definite transcription defect. It was performed
by the participating readers, not a third blind reading. No original was
edited or averaged into a preferred consensus. The common local identification
does not justify assigning every pale cell, and the pale-cell disputes do not
justify refusing all local curve identity.

## Verification and its limits

The context adapter passed eight controls before saving both identical raw
contexts. The [separate context check](context-independent-check.json) passed
28 fixture controls, compared every context record with freshly decoded source
RGB and recovered every cell from all 323 display columns. Only exact white
was omitted. Its two saves are identical, and root's replay matches exactly
(`883315`, `06e29a`). This checks faithful data/display handling, not perception.
The checker uses Python 3.12.14/Pillow 12.3.0 versus the saved producer's
3.13.7/12.0.0; both use the Pillow decoder family.

Twenty-one comparator tests passed before saving the comparisons and again in
root's run (`4665a5`). Root reran all four reader expansions and both comparisons;
all outputs match their original and repeated bytes (`37bf19`, `224b69`). The
comparator's author also made the peer E8 annotation, so those are producer
checks, not independent verification. Named reader roles now determine
directional differences explicitly; a reversed mapping-order control prevents
accidental role reversal. Previous saved runs used the expected order and are
not shown wrong. The older E4/E5 files remain unchanged: all 34 verification
pins match (`5a8c4a`).

The [separate annotation/comparison audit](independent-comparison-e89-check01.json)
reconstructs all four complete outputs from extracted literal data and its own
expansion, without importing or executing the readers or comparator. It checks
all 1,260 route records, 476 supplied band records and 14,175 list/boolean set
operations; it rechecks every context record against source RGB and all 3,930
selected cells. No selected exact-white defect was found. Both saved audits
are byte-identical, and root's complete replay matches every byte (`0e82fc`).
Nine checker tests pass (`38e41a`); this count includes full historical replay,
not nine wholly synthetic experiments. Thirteen scalar controls are also
exercised. The earlier verification receipt's 45 input paths remain unchanged.
The unsorted but nonoverlapping E8 manual table remains literal source data;
the check validates its expansion without rewriting those choices.

Exact commands, attempt outcomes and pins are recorded in
[verification.json](verification.json) and the
[independent execution receipt](independent-comparison-e89-test-receipt.json).
Faithful replay cannot independently witness the readers' perceptions, prove
historical authenticity or calibrate original-curve containment. Reusing source,
legend and conventions can correlate all readers' errors. A repeated result,
even with separately checked arithmetic, does not validate structural physics.

One root E8 repeat-save permission review timed out before execution. The
permitted single retry succeeded (`0daaca`) and matches the already frozen
original (`3f5ae8`). This is a retained execution failure, not an evidentiary
finding or an altered acceptance criterion.

## Remaining scientific work

Continue the [fixed roster](../REGIONS.json) with F4 and F5:
Im4 [330,0,425,88], Im4
[375,0,475,88] and Im2 [225,50,350,88]. Freeze that adapter/protocol before new
pixel readings; keep F5's two source regions and seam questions separate.
Do not repeat completed energy targets or the F3 descending corridor.

These finite regions do not finish the full supported-domain inventory.
The [fourteen-pair applicability decisions](../../historical-applicability/report.md),
unresolved identities/seams, calibrated original-curve bounds and unchanged
42 paired human-review slots remain. Agreement or reproduced arithmetic
cannot substitute for those requirements. Full reasoning is appropriate for
source interpretation; mechanical checks can reuse pinned, tested components.

The [acoustic reassessment](../../../synthesis-packet/acoustic-update-2026-10-07/report.md)
is unchanged: reported C/D sounds are neither established silence nor
identified mechanisms. No new cause ranking, simulation, human acceptance,
engine activation, legal promotion, disclosure, commit or push follows.
Source-preservation and evidence-audit controls keep disputes visible and
research separate from the legal record. The generic role-order feedback
extends the existing local Sherlock fixture; its archived destination remains
unresolved and no delivery is claimed.
