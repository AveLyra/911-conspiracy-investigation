# Native red and green terminal curve annotations

October 7, 2026. Research-only recovery of the two fixed terminal regions in
NCSTAR 1-9A Figure 3-5, not a measured model discrepancy or a collapse finding.
For each region, the reader records attest that root and a separate
prior-informed AI reader inspected the complete source strip and page, then
every raw context column before freezing separate annotations. The
readings agree more closely on the darker stroke cells than on pale edges or
dash-body attribution. Neither reader supplies calibrated original-curve
bounds or actual human acceptance.

## Coverage and preservation

The [protocol](PROTOCOL.md) and [all-pair region roster](REGIONS.json) were
frozen before this pass. Root was designated the primary version before
comparison. These visually informed terminal regions are not random or
representative samples of the whole curves. Source Im8 is 745 by 92 pixels,
with SHA-256 `0c49df5f6117d3f0e9b206d7c3352edf57849e4ac00ef9764b857b1445947d83`.
The composed-page legend identifies solid Spring, dashed Shell, red six bolts
and green seven bolts; local line style, not height alone, supports the route
labels. No identity is extended through an earlier same-color contact.

| Region | Target box in native cell edges | Context cells read by each reader | Entries per reader |
|---|---|---:|---:|
| E6 red | [515,57,690,85] | 5,728 | 350 |
| E7 green | [580,14,690,30] | 2,280 | 220 |

Boxes mean x0,y0,x1,y1 with half-open upper edges. Each entry is one column
for one local route, with explicit core and tentative fringe rows, status,
boundary flags and local fragment attribution. All 1,140 reader entries
remain in the four original JSON files. The two complete raw context saves
are byte-identical; a separate check compared all 8,008 cells to the native
source and losslessly reconstructed the sparse display, which omits only
exact white. This uses the same Pillow decoder, not independent codec validation.

Preserved readings: [E6 root](reader-E6-root.json),
[E6 separate reader](reader-E6-independent.json),
[E7 root](reader-E7-root.json), and
[E7 separate reader](reader-E7-independent.json).
The [context check](context-independent-check.json) records its complete
coverage and limits. The [E6](E6-reconciliation01.json) and
[E7](E7-reconciliation01.json) comparisons retain every entry and difference.

The root E7 reading was resumed and reread after context recovery before it
froze. Neither reader inspected the other's new annotations before its own
freeze. Both had prior source knowledge; agreement is not independent historical
corroboration, blinding, human inspection or an engineering qualification.
The composed-page display was resized; all recorded coordinates came from
unchanged native RGB, not pixels in that displayed page.

## Reader disagreement

An outer set is that reader's core union fringe. A classification difference
means either the core set or fringe set differs. Counts concern annotations,
not physical displacement, statistical error, model disagreement or accuracy.

| Region | Paired entries | Different outer sets | Different core or fringe sets | Different status labels |
|---|---:|---:|---:|---:|
| E6 red | 350 | 81 | 96 | 37 |
| E7 green | 220 | 131 | 132 | 38 |

For E7, both readers assign row 24 to the dark solid stroke in every column.
Root also retains pale row 26 as tentative fringe; the other reader leaves it
unassigned. That single systematic edge choice accounts for all 110 solid-route
outer-set differences. The dashed route differs in one core column and 21
outer sets. These totals must not be summarized as 131 independently misplaced
curves or as a physical model discrepancy.

For E6, the two solid readings differ in 18 columns, including how the upper
stroke occupies adjacent rows. Dash annotations differ more in pale intervals:
root retains candidate fringe in every such interval; the other reader assigns
no cells in 30 columns and retains narrower ambiguous fringe elsewhere. Empty
attribution is not proof of a true gap, missing curve or zero physical support.
The original choices, including differing dash endpoints, remain unchanged.

The readers' status vocabulary also differs: E7's separate reader uses
`fringe_only` for uncertain cells without a unique body, while root uses
`identity_conflict`. Both are allowed by the frozen protocol. The comparison
preserves those original labels and separately reports unknown attribution;
it does not convert a naming difference into recovered identity. Reader-local
fragment IDs are not equated merely because their labels look alike.

## Verification and limits

Thirteen synthetic tests passed before the historical comparisons. They cover
coverage/order, strict row types, holes, disjoint classes, boundary flags,
fragment unions, uncertainty statuses, dependency pins, repeated output and
overwrite refusal. Root review identified missing schema adapters and pin
checks in the first implementation; these were repaired before any historical
comparison. None of the frozen annotations was edited to obtain a pass.

Each historical comparison was run twice with input pins checked before and
after. E6's repeated output SHA-256 is
`54a34943a6b08aaee0b36fa0e4e0c5bd48c3d81307d3ff143b0e306f8f488fd1`;
E7's is `1ee237c9f84858e6c9489b5630dd751b2dce1840d0492e30d691834fcf3c28b9`.
Every output retains both literal reader entries and the core, fringe and
outer intersections, unions, one-reader-only sets and symmetric differences.
The [independent implementation](independent_reconcile_check.py) reproduces
all 1,140 literal annotation memberships/statuses/IDs/boundary flags and all
8,550 set operations, checks raw-entry retention and source/dependency pins,
and confirms both repeat pairs. It extracts literal instructions without
importing or executing the reader scripts and uses an ordered-merge algorithm
instead of the producer's set operators. Fourteen synthetic controls passed.
Its [saved result](independent-reconciliation-check.json) has SHA-256
`7ce9af1495facf6808d429cbb514f9fcaaf8a15b5d022b2a3f1c6d88c76aa64d`.
The checker author also supplied the E7 separate reading; implementation
independence is not reader, source or historical independence. The pinned
8,008-cell context check was reused explicitly, not claimed as a new traversal.

Executed commands used Python 3.13.7 at
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`, with `-B`, from this directory.
Root ran `-m unittest -v test_validate_reconcile.py` (13 passed, receipt
`56d5f9`), then the following comparison command for each pair E6/E7 and each
run 01/02:

```text
validate_reconcile.py --root reader-PAIR-root.json --peer reader-PAIR-independent.json --pair PAIR --output PAIR-reconciliationRUN.json
```

All four comparison commands exited zero: E6 receipts `e2025c`/`d39ec7`, E7
`926406`/`d49f6f`. A hash check followed (`707e69`). The placeholders above
describe those four literal invocations; they are not additional executions.
Replays must use fresh output names because existing outputs are protected.
The count review (`6d7e7f`) used a separate traversal but was performed by the
comparison-code author, so it is not a separately implemented verification.
The independent command was `independent_reconcile_check.py check`: agent
receipt `8fdc37`, then root replay `97f080`, both exit zero. The latter reran
all 14 controls and the complete historical check. All reader/source inputs
remained unchanged. The [verification record](verification.json) pins the
final code, original readings and completed check.

The strongest limitation is that two readers can agree while missing the same
pale pixels or misidentifying the same source feature. Conversely, their union
is not automatically a valid bound and their intersection is not an accurate
centerline. This result establishes a reproducible annotation record, not
pre-raster containment, admitted physical ordinates, complete support or a
consequential model-fidelity result.

## Next declared source work

This fixed two-region batch is complete. Continue the roster's
next batch: E3 in Im10 [365,30,690,60], E4 in Im9 [440,72,690,92], and E5 in Im9
[395,18,690,47]. The context rule remains two native cells, clipped to source
dimensions. Preserve unknown two-series membership where only one band is
visible; do not duplicate it into apparent agreement. New context outputs need
the same lossless checks and separately frozen readings. Full-reasoning readers
are appropriate for these identity judgments.

This completes neither all fourteen pairs nor the full supported-domain
inventory. E6/E7's earlier approach/contact, F3's remainder, and the roster's
other targets retain their existing pending or unresolved dispositions. Bounds,
identity and physical support require separate decisions before the unchanged
42-slot human sample rule. The main charter's other workstreams remain open.
No cause ranking, Sherlock/Faraday acceptance, legal promotion, disclosure,
commit or push follows. Work remains in the investigation worktree on
`research/sherlock-wtc7-investigation`, base HEAD `ca1c2233`, intentionally dirty.
