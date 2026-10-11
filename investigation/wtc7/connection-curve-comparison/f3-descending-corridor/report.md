# F3 descending corridor recovery

October 7, 2026. Research-only graphical annotation. The published black
three-bolt curve pair now has complete column-wise annotation of its selected
descending corridor: two frozen readings, each covering 90 columns for both
local routes. The readers disagree on outer pixel membership in 26 of 180
entries and on core/fringe classification in 56. This materially expands
source coverage; it does not yet establish physical ordinates, a calibrated
original-line error bound or a spring-versus-shell discrepancy.

## Source coverage and reading method

The [protocol](PROTOCOL.md) fixes native Im4 columns 270–359 and all rows
0–87, with raw context extending to columns 268–361. All 8,272 context RGB
triples are preserved in [raw-context.json](raw-context.json). Both readers
viewed the full unchanged native strip and complete composed page, and read
every context column in declared, untruncated blocks. The larger page display
was resized and was not used to infer native pixel precision.

The sparse textual display omits only exact white cells, retaining every
other coordinate and RGB triple. It is a lossless reading aid, not a darkness
classifier. Independent reconstruction checked 2,925 explicit nonwhite cells
and 5,347 omitted pure-white cells against all 8,272 source cells.

[Root annotations](reader-root.json) and [separate annotations](reader-independent.json)
were frozen before exchange. Core means a confidently attributed local dark
raster stroke; fringe means tentative edge or compression attribution. These
are subjective readings, not guaranteed bounds. The source legend and local
continuous/broken patterns motivate provisional spring/shell identities;
relative height or left/right ordering alone does not. Colored strokes remain
separate from the neutral black descent. Each reader preserves reader-local
dash names and multiple pieces sharing a column without joining their gaps.

This is prior-informed, same-source AI review. Both readers knew the earlier
small-fragment work; neither supplies independent historical corroboration or
actual human acceptance. The [method review](method-review.json) required
lossless display checks and overlap comparisons restricted to previously
inspected rows. Literal dash names are not equated across readers.

## Retained differences

| Route | Entries | Different core sets | Different fringe sets | Different outer sets | Different classifications | Both outer sets empty |
|---|---:|---:|---:|---:|---:|---:|
| Continuous black descent | 90 | 20 | 25 | 11 | 25 | 20 |
| Broken black descent | 90 | 24 | 31 | 15 | 31 | 26 |
| Total | 180 | 44 | 56 | 26 | 56 | 46 |

An outer set combines core and fringe. Thirty entries have equal outer sets
but different classifications. The root reading selects 289 core and 547
total cells; the separate reading selects 341 core and 573 total cells. These
are finite annotation counts, not accuracy estimates. Counting the 46 jointly
empty entries as successful stroke identification would overstate agreement.

[The reconciliation](run01.json) retains every original record, exact set
operations and per-reader statuses. Empty entries mean no cells attributed to
that route in that inspected column—not a verified gap, absence of a curve or
zero load. Selected cells meeting the strip top/bottom remain truncated;
neither physical endpoints nor continuity into the neighboring strip is inferred.

Both readers reproduce their own earlier fourteen entries exactly **within
the old row boxes**. New dash cells at columns 300 and 307 lie outside the old
row range and are reported separately, not as contradictions or previously
observed background. This consistency is prior-informed, not fresh validation.

## Reproduction and verification

All producer commands used
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B` from this directory,
with Python 3.13.7 and Pillow 12.0.0 for image decoding:

- `read_context.py save` preserved the declared 8,272 cells.
- `reader-root.py` expanded literal manual row runs without selecting pixels
  algorithmically; the separate reader preserved its own manual annotation.
- `reconcile.py controls` passed 21 synthetic checks before reconciliation,
  including malformed membership, holes, disjoint sets, different partitions
  with equal outer sets, boundary and fragment consistency, old/new row limits,
  changed source/protocol pins and overwrite refusal.
- `reconcile.py run01` and `reconcile.py run02` both exited zero. Complete
  outputs are byte-identical, SHA-256
  `3d075839476f5be66f0bffaa910fb8a9a0d78a1cd52fafabde920ad0f4b57d84`.
- Root checked all ten recorded input pins, three Python syntax trees, counts
  and old/new row comparisons. Requesting the existing output again returned
  the expected exit 1 with `FileExistsError`; all eleven then-existing files
  in this stage were unchanged. No producer repair was needed.

The [independent verification](independent-check.json) passed: all 8,272 source
cells and the lossless display, 360 verbatim reader records, 2,700 set
operations, status summaries, 28 old/new common-region records, input pins
and both output bytes. Its separate checker did not import the producer;
both image paths still share Pillow, so this is not an independent decoder
test. These checks establish faithful recording and arithmetic, not correct
stroke identity or physical-model validity. The finite corridor stage is
complete within that limit.

## Interpretation and remaining work

The corridor yields useful local stroke attribution while exposing materially
different edge interpretations. The strongest limitation remains shared error:
both readers could miss the same true edge or misidentify a stroke. Their union
does not necessarily enclose the original pre-raster line. Larger coverage
does not turn agreement into a calibrated one-pixel confidence interval.

Leave this corridor's frozen readings unchanged. The remaining F3 initial
rise, crest, strip seams and tail require
their own finite source-recovery work and explicit identity conflicts. All
fourteen force/energy pairs, defensible uncertainty/support treatment and the
42 paired review slots remain required. No physical ordinate, source-array
recovery, support domain, cause ranking, solver result, engine acceptance or
legal-record promotion is claimed. No source image or prior experiment was
overwritten; work remains local and uncommitted.
