# Black energy curve annotations and a preserved transcription correction

October 7, 2026. Two separately frozen AI readings now cover the complete fixed
E3 terminal region of NCSTAR 1-9A Figure 3-5. Both leave the solid model's
contribution unresolved and identify some later local dash bodies. The visible
band is not duplicated into two model measurements. This is source recovery,
not evidence of model agreement, disagreement, collapse cause or human acceptance.

The comparison also found a real transcription defect: three exactly white
cells appeared in the second reader's tentative fringe. The original is
preserved, and a separate erratum removes only those cells. Passing reproduction
checks did not make the original reading accurate.

## Scope and source observations

The parent [fixed roster](../REGIONS.json), [batch protocol](PROTOCOL.md) and
pre-reading [identity clarification](IDENTITY-CLARIFICATION.md) preserve all
fourteen pairs and the unchanged human-review requirements. E3 uses unchanged
Im10, target [365,30,690,60] and context [363,28,692,62], in half-open native
cell coordinates. Root was designated primary before the readings.

Each reader's coverage record attests that it viewed the complete source strip
and composed page and read all 11,186 context cells. Both retained 650 model-route
records, one per model per target column. The raw display omits exact white
only. No threshold detector, interpolation or fitted centerline selected ink.
The composed page was displayed smaller than its saved resolution; coordinates
came from the native RGB cells, not that resized display.

The initial band is not uniquely separable into solid and dashed contributions.
Root keeps unassigned core through column 485; the other reader through 480.
Later repeated dark bodies support local dashed-style assignments, with 136
root and 151 peer core-bearing dash columns. Neither establishes whether the
solid curve terminated, is hidden underneath, or contributes to shared ink.
Pale body edges have different attribution. These local readings do not locate
physical failure endpoints or establish a mathematically supported domain.

Preserved readings: [root](reader-E3-root.json),
[original separate reader](reader-E3-independent.json), and
[corrected derivative](reader-E3-independent-corrected.json).
The second reader did not inspect root's reading before its own freeze; both
had prior knowledge of the source and locator. They are not blind readers,
independent historical sources, human reviewers or engineering experts.

## Disagreement and the explicit correction

The [original comparison](comparison01.json) retains both complete literal
readings. It distinguishes model-attributed cells from all selected visible
ink, including material whose model identity is unresolved.

| Original reading comparison | Paired entries | Different outer sets | Different core or fringe sets |
|---|---:|---:|---:|
| Model routes | 650 | 56 | 56 |
| All selected ink by column | 325 | 29 | 34 |

There are 64 route-status differences. These counts describe reader choices,
not model error. Both solid routes have empty attributed cell sets because
identity is unresolved; their equality is not evidence of equal physical curves
or zero support. A missing unassigned-band record is retained distinctly from
an explicitly supplied empty one. Reader-local fragment IDs are not equated.

The three invalid selections were unassigned fringe cells (372,46), (373,46)
and (381,45). Direct lookup and the comparator both found exact RGB white.
The reader confirmed that compact manual runs had overgeneralized its intended
selection, not deliberately included white pixels as an uncertainty envelope.
They must not be described as observed ink or calibrated bounds.

The [correction script](correct-E3-independent.py) checks the original hash,
the complete selected-white inventory and the exact intended memberships before
removing these three fringe cells. Before adding correction metadata and
relocating the timestamp, reversing only those changes restores the entire
original annotation object. All model routes are unchanged. The original
freeze time is relocated to source history, not represented as a new independent
reading. Two corrected outputs are byte-identical, SHA256
`d1bc331329ecf5eae6a9ac55708efde3d69653c5b3a6c2f9210301f1a3fc1d53`.
The table above intentionally remains the comparison of the original freezes,
including their defects; it is not silently recalculated on the correction.

## Reproduction and remaining limits

Eight lossless-reader controls passed before the raw contexts were saved.
Two complete saves are identical, SHA256
`59cef4cee1a54d66dacd4e2846e12a12d7b47c8091285ae8f68d8899bf6f2e48`.
The [separate context check](context-independent-check.json) verified all 26,641
cells across the fixed E3/E4/E5 contexts, their ordering, clipped boxes, input
pins and exact-white display round trips. Ten independent parser controls
passed. Saving and computationally checking E4/E5 cells is not a visual reading
or annotation of those regions. The checker used Python 3.12.14/Pillow 12.3.0;
the producer used Python 3.13.7/Pillow 12.0.0. Both belong to the same decoder
family, so this is not independent codec validation.

Thirteen comparison tests passed before the historical comparisons. They cover
coverage, row types/order, class overlap, holes, boundary flags, shared-band
references, duplicate attribution, missing versus empty records and classification
differences hidden by outer-set equality. The two comparison runs are identical,
SHA256 `5604430b3b161b5b7aac362fccddd391f162d579918e0a49988a6a17ce0a9d03`.
The root expansion also reproduces exactly. The peer's original expansion stores
a live timestamp; its frozen bytes remain pinned, but a rerun is not claimed to
reproduce that timestamp. Numerical reproduction and source accuracy remain
different questions.

The [separate reconciliation check](independent-comparison-check.json) and
its [implementation](independent-comparison-check.py) reproduce all 1,300 route
records, 441 supplied unassigned-band records and 14,625 original set operations.
It extracts literal instructions without executing or importing either reader
or the comparison code, and uses explicit per-row membership instead of the
producer's set algebra. Twelve independent controls passed. Original retention,
dependency pins, repeat bytes and the three flagged white selections were checked.
The peer's timestamp is the sole semantic-replay exclusion; it remains in the
hash-pinned original. Perception claimed in metadata is not independently witnessed.

The checker also verifies the entire corrected derivative, including its
provenance, unchanged routes and exact three removals. Its separate recalculation
of corrected visible-ink selections gives 26 outer-set and 34 classification
differences across 325 columns. These are explicitly new checker calculations,
not substitutions into the original comparison files. Root replayed the complete
check successfully (receipt `9225c6`). The all-context check was separately
replayed by root (receipt `45365d`); selected-cell source values were also freshly
checked during reconciliation. Neither is a new visual source reading.

The comparator is deliberately scoped to these frozen E3 records. Its validation
of `boundary_truncated` requires core cells, so it must not be reused unchanged
for a future fringe-only boundary case. No current E3 record exercises that
limitation. This restriction was not weakened to pass the present inputs.

Executed commands and artifact hashes are in [verification.json](verification.json).
From this directory, root ran `python3 -B -m unittest -v test_compare_e3.py`,
then `python3 -B compare_e3.py --output comparison01.json` and the same command
with `comparison02.json`. The exact Python executable is recorded there.
Read-only independent replay uses the executable and command recorded in
`independent-comparison-check.json`; existing comparison and annotation outputs
are overwrite-protected. No unrun check is implied by these instructions.

The strongest limitation remains common interpretation error: two readers can
agree on ink or style while both misidentifying the underlying mathematical
curve. Neither their union nor intersection provides a calibrated pre-raster
bound. No physical ordinate, spring/shell discrepancy, support interval, human
sample acceptance, solver result or causal ranking is established here.

## Next work

E3 reading, reconciliation and the known three-cell correction are complete
within the stated source-recovery scope. Continue E4 and E5 in the already
frozen boxes with separately frozen readers. Their source
pixels are preserved and checked, but their annotations are not done. Earlier
approaches outside these locators and the rest of the fourteen-pair support
inventory retain their previous dispositions. The 42 paired human slots cannot
be selected by favorable disagreement or by converting unknown support to zero.

Work stays research-only in `research/sherlock-wtc7-investigation`, base HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`, intentionally uncommitted.
No legal record, accepted Sherlock/Faraday finding, disclosure, commit or push
changed. The transcription pain point extends the existing local feedback
fixture; delivery remains pending at the archived Sherlock destination.
