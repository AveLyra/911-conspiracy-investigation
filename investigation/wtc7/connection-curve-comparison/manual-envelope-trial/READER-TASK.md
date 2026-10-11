# Synthetic stroke reading task

Use only `run01/packet/` and this task description until your response freezes.
Do not read `truth.json`, `truth/`, generator/scorer code, the other response,
or scores. Prior fixture knowledge is disclosed; do not compute expected rows
from it. No historical graph or physical quantities enter this packet.

Inspect the seven contact sheets showing T01 through T28, all four R images,
and each tile's unfiltered column RLE file. Individual images are available
for closer viewing. Contact sheets use nearest-neighbor 3x enlargement;
their labels and layout are not source coordinates. Original images are
160 by 96 except the cropped R04. RLE triples mean inclusive first row,
exclusive end row, RGB; they cover all 96 rows without a color cutoff.

For each T tile, give entries for x=20,23,24,28,32,36, in that order. Core
rows are visually attributable stroke cells; fringe rows are plausible but
uncertain edge cells. Record them as sorted integer lists with no overlap.
Do not add a margin, threshold, fitted centerline, bridge, interpolation or
truth-based correction. Inspect the local image context, not RGB alone.
Choose `identified` only for one attributable contiguous local stroke;
otherwise `unresolved`. Empty or disconnected membership cannot be identified.
Some ambiguous candidate cells may still be recorded with unresolved status.
Include a short observation cue for each entry. Do not call an unassigned
column a proven gap or absence.

For R01 through R04 answer the question in `index.json` as `unresolved` or
`established`, with a reason. The question concerns what pixels alone identify,
not which picture looks most familiar.

Write one JSON file assigned by root, with top-level reader, coverage,
packet_manifest_sha256, tiles and refusals. Under tiles, T01 through T28 each
map to six objects with exactly x, core, fringe, status and cue. Under refusals,
R01 through R04 each map to an object with exactly answer and reason.
Coverage must say which images and raw columns you actually inspected and
any limitations. Freeze with SHA256 and report the actual check/receipt. Do
not inspect results or another reading before freezing; retain all errors.
These are AI annotations, not actual human acceptance or statistical bounds.
