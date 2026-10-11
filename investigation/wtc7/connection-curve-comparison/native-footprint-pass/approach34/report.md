# E3/E4 approach annotations: complete fixed batch, unresolved attribution

October 8, 2026. Research only. The declared source-annotation batch is
complete; it is not complete recovery of either curve, physical validation,
human acceptance, or a finding about collapse cause.

## Scope and method

The [frozen protocol](PROTOCOL.md) and [reader assignments](READERS.md)
preceded new column-level readings. E3 black and E4 gold each have two
separately frozen, prior-informed computational readers. Each inspected the
unchanged strip and composed page, followed by every raw context cell in
finite, untruncated blocks. Receipt references and prior knowledge are retained
in each export and its notes. These are not blind readers, independent
historical observations, professional review, or human curve acceptance.

| Pair | Native target, half-open | Native context, half-open | Context entries per copy | Route records per reader |
|---|---|---|---:|---:|
| E3 | [195,35,365,92] | [193,33,367,92] | 10,266 | 340 |
| E4 | [195,0,440,92] | [193,0,442,92] | 22,908 | 490 |

Both use unchanged [Im10](../../native-strips01/Im10.jpg), 745 by 92 RGB,
SHA256 `fe8c069f4bb7a19f6eb996b42b266c55552a110f8e9cbc6e9cc0d7269547cdd3`,
and [page 76](../../render01/page-076.png), 1700 by 2200,
SHA256 `0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6`.
The E3 context lies inside E4's: 33,174 region-cell entries represent
22,908 unique cells per copy, not 33,174 independent observations. The old
E3 terminal context shares 116 cells; target interiors do not overlap. No
identity transfer or seam join is inferred.

The [context reader](read_context.py) reuses the pinned parent helper.
Its lossless display omits only exact white, abbreviates identical RGB runs
and grayscale triples reversibly, and checks each displayed round trip.
It does not classify ink, interpolate, or threshold faint pixels. Eleven
controls passed before the two exclusive-create context saves; their bytes
match. Manual local selections were expanded mechanically, not selected by
an image classifier. Core/fringe labels are reader judgments, not calibrated
confidence intervals.

## Preserved readings and disagreements

| Original | Route records | Unassigned bands | Notes |
|---|---:|---:|---|
| [E3 primary](reader-E3-primary.json) | 340 | 54 | [Prior knowledge and limits](reader-E3-primary-notes.md) |
| [E3 peer](reader-E3-peer.json) | 340 | 51 | [Coverage and decisions](reader-E3-peer-notes.md) |
| [E4 primary](reader-E4-primary.json) | 490 | 73 | [Coverage and decisions](reader-E4-primary-notes.md) |
| [E4 peer](reader-E4-peer.json) | 490 | 50 | [Coverage and decisions](reader-E4-peer-notes.md) |

E3 primary leaves selected upper-neighborhood ink in columns 219–262
unassigned. That is this reader's attribution limitation, not proof that
every cell is intrinsically inseparable. The peer identifies local solid
pieces at 224–232 and 234–237. Later separately attributed pieces exist,
but neither reader resolves all ownership or continuation. The primary
retains fifteen local dash-body IDs; pale adjoining tips do not establish
full-column support. Shared ink near contact remains one-copy uncertainty,
not two recovered model trajectories.

E4 selections meet the top source edge. Selected edge pixels, later empty
records and a narrow residual band establish neither physical termination
nor continuation into Im9. Unassigned material may include neighboring-curve
or compression contributions; no decomposition into those causes is proven.
Five E4-primary columns, 275–279, contain two disjoint uncertainty bands with
different route candidates. All bands and reciprocal route-specific references
are preserved separately. A dictionary keyed only by column would lose data.

The [comparator](compare.py) validates the recorded data through a copy-only
adapter to the existing comparison helpers, preserving all originals. It maps
field names and normalizes the
internal status of unassigned material without changing original statuses,
membership, notes, or band lists. Original route and band dictionaries appear
in the output. No voting, averaging, forced band merger or common-domain
construction occurs.

| Paired comparison | Route entries | Different outer sets | Different core/fringe classes | Different statuses | All-visible-ink columns / outer differences |
|---|---:|---:|---:|---:|---:|
| [E3](comparison-E3-01.json) | 340 | 40 | 51 | 16 | 170 / 31 |
| [E4](comparison-E4-01.json) | 490 | 91 | 99 | 28 | 245 / 101 |

Even a single fringe-cell difference counts. These are annotation differences,
not accuracy scores, physical-model error or independent measurements.
All-visible-ink comparisons include every band; they do not assign that ink
to a physical route. No selected cell is exact white. This rules out that
particular transcription defect, not wrong ownership or compression artifacts.

## Verification and retained failures

The [verification manifest](verification.json) records exact hashes,
commands, receipts and outcomes. Both comparison runs match byte for byte;
root's nonwriting producer replay matches both saved copies of each pair.
All four literal annotation builds reproduce their saved bytes.

The separate [checker](independent_check.py) was authored by a reader who did
not annotate this batch. It checks source RGB directly, uses a separate
92-bit implementation of the set operations, and does not import the producer,
context helper or old comparison helpers. It imports each frozen reader
script only for explicitly labeled literal-build replay. Its saved
[receipt](independent-check.json) and root replay agree exactly:

- 66,348 context entries across two copies match the source RGB; overlaps agree.
- All 1,660 original route records and 228 bands satisfy the checked contracts.
- All 37,350 operation arrays across four comparison files reproduce.
- All 27 pinned inputs remain unchanged. Sixteen checker controls pass,
  including RGB corruption, E3/E4 set corruption and reciprocal-reference tests.
- Eleven context controls and fifteen comparator tests also pass.

Repeated copies are not additional evidence. The checker shares the Pillow
decoder with context extraction; this is not independent JPEG decoding.
It validates the coverage attestations' contents, not independently witnessed
reader perception. It does not establish curve identity or physical support.

Earlier integration failures are retained, not silently described as passes:
the old one-band validator rejected reader-local band status (`2ac470`), and
a single coverage-key assumption failed on a peer export (`8a3634`). Before
historical comparison saves, the adapter was corrected to validate each actual
schema and preserve multiple same-column bands; all frozen annotations were
unchanged. The independent checker first encountered missing Pillow in system
Python (`721f30`), then a denied receipt save (`f549df`). Bundled Python and an
exact-command authorized save resolved those environment issues (`e9b2c6`).
No source, annotation or scientific criterion was changed to obtain a pass.

## What this changes and what remains

This replaces a locator-only obligation with explicit source annotations and
retained alternatives. It does not yet extend the earlier conditional-envelope
dataset or establish either curve's full supported domain. The strongest
objection to automatic support is that selected ink remains compatible with
different ownership, hidden continuation and partial-column dash extent.

Next incorporate these saved approaches into a versioned fourteen-pair
inventory. Before conditional conversion, declare and test a copy-only adapter:
these exports use `x` with a list-valued `fragment_membership`; the earlier
envelope normalizer does not directly recognize that combination. Preserve
reader alternatives, exact fragments, disputed contacts and source-edge exits.
Do not rerun source annotation merely to make the readers agree.

The [full reconciliation](../../historical-applicability/footprint-reconciliation-2026-10-08.md)
retains all outside-target obligations, including F5 Im3 descent and F6 lower
Im1. The unchanged 42 paired human-review slots remain unselected pending
full inventory/support disposition. Axes and legend confirmation stands;
curve acceptance remains separate. No midpoint, support union, model-discrepancy
metric, causal ranking, historical solver result, accepted Sherlock finding,
Faraday activation, legal promotion, disclosure, commit or push follows.
Generic multiple-band feedback is recorded locally under existing archived
routing; it was not delivered or verified as an engine defect/fix.
