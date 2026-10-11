# Gold and blue force-curve readings

October 8, 2026. All three fixed F4/F5 regions now have two separately frozen
AI readings. Their six annotation exports and three comparisons reproduce
exactly, including a separately implemented computational audit. Crossings,
faint edges and fragment boundaries retain real attribution disagreements.
These are annotations of a published connection-model graph, not observations
of the building, accepted physical measurements or a collapse-model finding.

## Scope and source coverage

The [protocol](PROTOCOL.md) declared this finite batch before its new pixel
readings, using the existing [region roster](../REGIONS.json). Both source
JPEGs remain 741 by 88 RGB cells. Full-strip and composed-page views supplied
context; coordinates came from native RGB records, not resized overview images.
Finite, untruncated raw-reading blocks omitted only exact white, explicitly.

| Region | Target box, upper edges excluded | Context records | Route records per reader |
|---|---|---:|---:|
| F4 gold, Im4 | [330,0,425,88] | 8,712 | 190 |
| F5 blue, Im4 | [375,0,475,88] | 9,152 | 200 |
| F5 blue, Im2 | [225,50,350,88] | 5,160 | 250 |

The 23,024 context records include overlapping source positions. They are not
23,024 independent observations. For F5-Im4 the peer reused its own earlier
reading of 4,752 overlapping cells, after checking exact source/context equality,
and newly read the remaining 4,400. That reuse is documented coverage, not
independent corroboration or a claim to have reread the overlap.

Root was prospectively designated primary for F4; a separate AI reader was
primary for both F5 regions. A third AI reader supplied all three peer readings.
Matching-region substantive exchange followed both freezes. Prior knowledge,
shared source and shared conventions can correlate errors; these are not
blind human observations. Coverage records are internally checked, not
independently witnessed perceptions.

Solid/Spring and broken/Shell assignments require local style plus the confirmed
legend, not vertical order. Literal manual runs expand mechanically. Core and
tentative fringe remain separate; unresolved material is recorded once rather
than copied into both models. Multiple pieces keep explicit memberships.
There are 1,280 route records and 640 explicit unassigned-band records across
the six readings. Empty bands, missing bands and unknown support are not zero
physical force. The two F5 sources remain separate: no seam join or cross-strip
coordinate union was performed.

## Reader differences

An outer set is core plus fringe. These counts compare readers, not Spring
against Shell. Even a single tentative edge cell makes a column different;
the counts are neither model-error scores nor statistical confidence intervals.

| Comparison | F4-Im4 | F5-Im4 | F5-Im2 |
|---|---:|---:|---:|
| Route entries compared | 190 | 200 | 250 |
| Different outer sets | 62 | 52 | 32 |
| Different core/fringe classifications | 68 | 55 | 34 |
| Different status labels | 8 | 16 | 22 |
| All-selected-ink columns compared | 95 | 100 | 125 |
| Different all-ink outer sets | 52 | 57 | 32 |
| Different all-ink classifications | 57 | 60 | 42 |

The complete [F4-Im4](comparison-F4-Im4-01.json),
[F5-Im4](comparison-F5-Im4-01.json) and
[F5-Im2](comparison-F5-Im2-01.json) comparisons retain original records and
every set operation. All corresponding second saves match exactly.

For F4, local continuous and broken gold strokes can be distinguished, but
some pale edges and dash-body boundaries remain disputed. In particular,
primary fragment d02 spans columns 362–368; the peer separates 362–364 and
365–368. Agreement on a union of pixels would not establish agreement about
fragment topology. Original identifiers are retained, not harmonized by name.

For F5-Im4, both readers leave the blue/red overlap at columns 446–455
unassigned. The peer's core cells there mean confidently visible mixed ink,
not confident blue-model membership; the primary uses fringe-only unassigned
material. Other differences chiefly concern faint edges and class assignment,
not demonstrably displaced physical trajectories.

For F5-Im2, the primary assigns rows 72–75 at column 225 to solid, while the
peer leaves contact material unassigned. The mixed cell (225,74), RGB
[84,49,131], does not independently identify each contributing original curve.
At columns 286 and 292, the primary retains a broader unresolved contact;
the peer separates two local pieces with an unassigned middle. The narrower
peer interpretation is plausible, but no calibrated source bound resolves
the disagreement. Locally identifiable pieces away from contacts do not
justify bridging them or joining Im2 to Im4.

There is also a metadata caveat: the peer exporter references each selected
unassigned band from both routes in that column. Thus an empty solid route
can carry `identity_conflict` because of material near the dashed route
(for example F5-Im4 column 447). This conservative encoding is not affirmative
evidence that that solid branch is ambiguous. Status-difference counts must
not be treated as measured curve disagreement.

Participating-reader post-exchange source checks found no definite coordinate
transcription defect in the rechecked areas. This was bounded critique, not a
third blind reading or proof that every attribution is correct. No frozen
annotation was edited, averaged or replaced by a preferred consensus.

## Computational verification

The context adapter passed 13 controls before saving identical contexts.
The [separate context check](context-independent-check.json) passed 47 controls
and checked all 23,024 RGB records and all 332 lossless display columns. Its
two saved checks and root replay match. Only exact white is omitted from the
display. Producer Python/Pillow versions are 3.13.7/12.0.0; the separate
checker uses 3.12.14/12.3.0. Both use the Pillow decoder family, so this is not
independent codec validation or historical authentication.

The final comparator passed 31 synthetic tests before the historical saves.
All six reader expansions and all three comparisons were replayed by root;
every result matches the original and repeated bytes. The comparator author
also supplied the F4 primary reading: producer replay is not independent review.

A pre-save code review found that a route could reference a named but empty
unassigned band. The final guard requires real selected same-column material
and a nonempty reason; input JSON is parsed from the bytes actually hashed.
The [pre-review comparator](compare_force45-before-review.py) is a later
reconstruction that matches the previously observed source hash, not a file
archived before review. A synthetic replay demonstrates its acceptance of the
empty-band reference and the final version's rejection. No historical comparison
was saved with that version, and no frozen annotation needed correction.

The [independent annotation/comparison check](independent-comparison-force45-check01.json)
reconstructs every field of all six annotations from inert literal data and
separately authored expansion. It does not import or execute producer readers
or the comparator. It checks all 1,280 route records, 640 band records and
14,400 set operations, rechecks every context RGB record and examines 3,866
selected cell entries across the six readings. Those entries include shared
source positions, not independent samples. Zero selected exact-white cells
were found; nonwhite cells may still be artifacts or have uncertain identity.

Twelve synthetic-only checker tests passed before its historical runs. The
historical audit is not hidden inside that test count. Both audit outputs are
byte-identical; root reran all twelve tests and reproduced every output byte
(`7d93aa`, `04caf9`). All 37 previous E8/E9 artifact pins remain unchanged.
The [verification manifest](verification.json) and
[independent execution receipt](independent-comparison-force45-test-receipt.json)
record commands, pins and attempt outcomes. No historical check failed or
source annotation was repaired in this batch. The demonstrated pre-save guard
defect remains part of the record, not a silently discarded failed control.

These checks establish recording and arithmetic fidelity. They cannot establish
original-curve containment, recover hidden overlapping curves, validate force
values or authenticate the historical collapse. That is the strongest limit
on interpreting a clean computational result as scientific validation.

## Remaining work and boundaries

Continue the [frozen roster](../REGIONS.json) with F6–F9, preserving all six
source-region identities: F6/Im2 [205,0,365,88]; F7/Im1 [220,50,335,88] and
F7/Im2 [330,0,475,88]; F8/Im1 [195,10,370,88]; F9/Im0 [220,55,325,88] and
F9/Im1 [245,0,375,88]. Declare the bounded protocol and two-cell clipped
contexts before new pixel readings. Prior-read reuse needs exact source and
coverage receipts and must not be counted as a new independent observation.

This finite pass does not finish the full fourteen-pair supported-domain
inventory. The [applicability decisions](../../historical-applicability/report.md),
remaining F3 rise/crest/tail, unresolved identities/seams, justified
original-curve bounds and unchanged 42 paired human-review slots remain.
Axes/legend confirmation is complete; curve acceptance is not. Do not repeat
completed energy regions, F3 descending corridor or this F4/F5 batch simply
to reproduce already checked counts.

The [acoustic reassessment](../../../synthesis-packet/acoustic-update-2026-10-07/report.md)
is unchanged. No new cause ranking, simulation, human acceptance, engine
activation, legal promotion, disclosure, commit or push follows. Evidence-audit
and source-preservation controls kept disagreements visible and research
separate from the legal record. Generic source-region, reading-reuse and
empty-band-reference feedback extends existing local Sherlock notes; the
archived delivery destination remains unresolved. No delivery or product fix
is claimed. The full investigation remains active and incomplete.
