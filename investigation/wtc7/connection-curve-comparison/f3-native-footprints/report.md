# First F3 native stroke recovery

October 7, 2026. Research-only source annotation. The first two local F3
fragments now have explicit native-pixel membership from two separately
frozen AI readings, rather than only rectangular locators. Their outer sets
differ in seven of fourteen fragment-column entries. These are recoverable
raster observations with retained disagreement, not accepted physical
ordinates or a calibrated uncertainty bound on the original plotted curves.

## Coverage and method

The [frozen protocol](PROTOCOL.md) selects the existing Im4 solid proposal
at columns 300–305, rows 32–48, and single-dash proposal at columns 300–307,
rows 4–14, inclusive and zero-based. These are fourteen fragment-column
entries but only eight distinct x coordinates. Every one of the 660 RGB
cells in columns 298–309, rows 0–54 is preserved in [raw context](raw-context.json).
No threshold classifier, image filter, interpolation or hole filling was used.

Both readers inspected the unchanged native strip and composed page. The
large page display was resized; native coordinates and raw cell values
control the annotations. Each reader classified a local dark-stroke core
and tentative fringe, preserving empty sets, separated cells, boundary
warnings and explanatory text. Both records were frozen before exchange:
[root reading](reader-root.json) and [separate reading](reader-independent.json).
This is prior-informed, same-source AI work—not blind review, independent
historical evidence or actual human acceptance.

The [prospective method review](method-review.json) required keys to include
both fragment and column, and required different core/fringe assignments to
remain visible even where the outer sets agree. Both conditions were tested
and implemented. All original readings remain unchanged.

## Results and disagreements

| Comparison | Entries that disagree out of 14 |
|---|---:|
| Core row membership | 8 |
| Fringe row membership | 9 |
| Combined core and fringe membership | 7 |
| Core or fringe classification | 9 |

These counts describe this selected finite set, not an error rate or a
probability. Status wording differs in six entries; differing wording is not
automatically a conflicting physical judgment. [Both reconciliations](run01.json)
retain every original row and all intersections, unions and differences.
The frozen machine summary keys ending in `_equal` contain **disagreement
counts**, as their accompanying limit states; they are not agreement counts.

The root reading assigns 25 core cells and 52 total cells; the separate
reading assigns 36 core cells and 61 total cells. Agreement about an outer
set need not imply agreement about its interpretation. For example, at solid
column 302 both outer sets contain rows 35–40, but the core is rows 37–38
in one reading and 36–39 in the other. Dash column 302 likewise has equal
outer sets but different classifications. At solid column 300 the separate
reading retains tentative row 38 without filling row 37. Collapsing that set
to a bounding rectangle would invent membership.

The continuing solid stroke is cut by the selected left and right boundaries;
those are not physical endpoints. Empty core at a dash edge does not establish
zero load or a validated gap. The black solid/single-dash assignments remain
local, provisional identities based on source style and context. They are not
propagated through crossings, strip seams or uninspected portions.

## Reproduction and checks

The runtime was Python 3.13.7 with Pillow 12.0.0. The pinned Python executable
is `/Users/admin/.pyenv/versions/3.13.7/bin/python3`. From this directory the
actual producer commands were `python3 -B read_context.py`,
`python3 -B reconcile.py controls`, `python3 -B reconcile.py run01`, and
`python3 -B reconcile.py run02`, using that full executable path.

- Raw context extraction completed with all 660 cells. Each retained triple
  has equal red, green and blue values; all three channels remain stored.
- Seventeen [synthetic controls](controls.json) passed, including malformed
  rows, shared columns across fragments, empty/disjoint sets, holes, equal
  outer sets with unequal classifications, changed pins and overwrite refusal.
- Both historical reconciliations exited zero and are byte-identical:
  SHA-256 `7f379defca5b1b00fa17391d6882bc607a4b5061411d21b24e2e1359cebf64b3`.
- The [separate verification](independent-check.json), without importing the
  producer, checked all 660 RGB triples, 210 set operations, 28 verbatim reader
  records, status comparisons and both output bytes. It passed with no
  arithmetic failure. Both implementations use Pillow, so this is not an
  independent JPEG decoder test.
- Root rechecked all thirteen pinned files from that receipt. An actual
  repeat request for the existing `run01.json` returned the expected
  `FileExistsError` and exit 1; all eleven then-existing files in this stage
  remained byte-identical. This was a preservation test, not a failed analysis.

The source Im4 SHA-256 remains
`53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd`.
The protocol SHA-256 is
`407c8f18f4202047aa01e573ceee2f5c1350ece9f9fb7961a3042881ea5e1fea`.
The independent receipt retains all remaining source, code and result pins.

## Scientific limit and next measurement

The strongest objection to treating these sets as uncertainty bounds is that
both readers could miss the same faint edge or misidentify the same stroke.
A union encloses these two annotations, not necessarily the original line.
JPEG edge structure, original line placement and model identity remain
distinct uncertainties. Agreement or a successful replay cannot calibrate a
one-pixel allowance or recover the pre-raster centerline.

This finite annotation stage is complete. Continue the remaining F3 route
through a separately declared selection, including the other descending
fragments and explicit crest, rise, seam and tail conflicts. Do not retune the
failed color predicate or repeatedly validate only these convenient fragments.
All fourteen force/energy bolt-count pairs and the eventual 42 paired review
slots remain required by the parent protocols. No displacement support,
centerline, force/energy difference, human acceptance, causal ranking, engine
activation or legal promotion follows from this stage.
