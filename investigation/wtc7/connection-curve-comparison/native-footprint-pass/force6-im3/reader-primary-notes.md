# Primary F6-Im3 original: reading, coverage, and limitations

Reader: `force6_im3_primary`, serialized `primary`. This is a same-source AI
reading, not human acceptance, independent historical corroboration, a
calibrated uncertainty interval, or physical/causal support. The output keeps
`human_accepted: false` and `physical_support: null`.

## Scope and method

Only F6 in unchanged `../../native-strips01/Im3.jpg` was annotated. The target
is half-open `[145,0,440,88]`; the context is `[143,0,442,88]`. Every context
column 143 through 441 and row 0 through 87 was actually read. Each of the
295 target columns has one solid and one dash record, including inspected
columns with no attributable cells. Empty records are not claims of physical
absence. Context-only columns are not promoted to target selections.

The complete native 741 by 88 strip and complete composed page
`../../render01/page-076.png` were viewed through `view_image` with original
detail before raw-display receipt `f047d2`. The page tool displayed the entire
1700 by 2200 page resized to 1376 by 1780; this was orientation, not a claim
of native-resolution page inspection. The page identifies the red 6-bolt
series and solid/dashed styles. It does not establish physical model validity.

Selections in `reader-primary.py` are manually chosen literal inclusive row
ranges. `build()` only expands them, assembles schema fields, and checks pins.
No RGB threshold, classifier, smoothing, interpolated continuation, curve fit,
or centerline chose cells. The raw context displays omit only exact
`RGB(255,255,255)`. `gN` is exact grayscale and equal-RGB row runs are inclusive;
near-white and mixed-color cells remain displayed. All 14 blocks below were
untruncated. No recovery reread was needed.

## Actual raw-display coverage

Every command used the bundled Python at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(`P` below), from this directory:
`P -B read_context.py show --first FIRST --last LAST`.

| Inclusive context columns | Actual shell-output receipt |
| --- | --- |
| 143–152 | `f047d2` |
| 153–168 | `3e7334` |
| 169–188 | `42b35e` |
| 189–208 | `0c670f` |
| 209–228 | `d43738` |
| 229–258 | `205b21` |
| 259–298 | `8ce306` |
| 299–328 | `85fce8` |
| 329–348 | `4a0e37` |
| 349–368 | `6dcd34` |
| 369–388 | `de6a83` |
| 389–408 | `84463a` |
| 409–428 | `c483da` |
| 429–441 | `dad394` |

Coverage is 299 columns times 88 rows = 26,312 cells, exactly once in this
block accounting. No uncompleted context remains. These receipts document
actual observation rather than an automatically filled claim of inspection.

## Local choices and unresolved ownership

Distinct visible dash bodies retain local fragment IDs, including disjoint
bodies in the same column. The descent and irregular shoulder are retained;
there is no monotone repair. Core and tentative fringe are distinct, with
explicit top/bottom/right contact flags only for selected cells actually
touching those target edges. Shared red-style contacts and mixed-color/pale
ownership remain separate unresolved bands with reciprocal route references.

Examples of retained uncertainties include the rising solid's green/purple/
blue contacts, the source-top transition, red solid/dash contacts around
columns 361–366 and 384–385, the solid descent's purple contact near the
source bottom, and the dashed shoulder's blue/green/purple/cyan contacts and
right-edge terminal fragments. A band containing competing colors does not
assert that a hidden red stroke exists beneath them. Candidate ownership is
an explicitly unresolved local reading, not recovery of occluded pixels.

Counts are accounting facts, not quality scores:

| Output | Solid | Dash |
| --- | ---: | ---: |
| Route records | 295 | 295 |
| Core cells | 176 | 279 |
| Fringe cells | 111 | 190 |
| Boundary-truncated records | 3 | 13 |
| Identified-local-fragment records | 50 | 83 |
| Fringe-only records | 0 | 7 |
| Identity-conflict records | 35 | 27 |
| No-attributable-cells records | 207 | 165 |

There are 68 unresolved band records containing 346 cells. None of those
cells is also in an attributed route, and same-column bands are disjoint.
Core/fringe boundaries and route attribution remain fallible manual judgments.
The strongest countercheck is that mixed colors, compression artifacts, or
an apparently separate fragment could defeat this reader's ownership choice;
exact replay and complete display coverage cannot resolve that objection.

## Actual checks and saved original

Before historical cell selection, `P -B read_context.py controls` completed
with all 17 controls true in receipt `f047d2`: boolean boundary rejection,
clipped margin, context count, representation, coverage, exact grayscale,
no-gap-bridge display, display round trip, losslessness, near-white retention,
out-of-window display rejection, overwrite refusal, row-major order,
exact-white-only omission, and wrong height/mode/width rejection.

Read-only inline Python verification in receipt `f66a56` independently checked
all 26,312 unique current context coordinates against `Image.getpixel` on the
unchanged native RGB source and found exact equality. Both context files were
byte-identical with SHA256
`8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024`.
That check also confirmed route bounds, class disjointness, membership counts,
boundary flags, and unassigned-versus-attributed disjointness. The coordinator's
older-overlap check is not represented as a check performed by this reader.

The final read-only inline Python check in receipt `426034` called `build()`
twice and verified equality; exact 590 route-row coverage; allowed statuses;
sorted, unique, bounded, disjoint class sets; exact per-class membership unions;
outer fragment IDs; nonempty reasons; empty/conflict status consistency;
boundary flags and ordering; candidate-route lists; reciprocal same-column
band references; absence of band/route, band/band, and solid/dash cell overlap;
exact once-only context-block coverage; both complete context input maps; all
17 current input pins; script pin; source RGB mode/size; and the false/null
acceptance/support fields. It passed.

`P -B reader-primary.py` first failed at exclusive creation with a sandbox
permission error (`a06d9b`); no JSON was created by that attempt. The same
narrowly scoped command then succeeded with the worktree-write escalation
(`35ca21`). It used mode `x`, not overwrite. The subsequent read-only replay
in receipt `865971` verified saved JSON equals `build()` exactly, all 17 pins
remain current, and another exclusive-open attempt raised `FileExistsError`
while leaving the original bytes unchanged.

Frozen original JSON: 341,477 bytes, SHA256
`d53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9`.
Literal script: 17,734 bytes, SHA256
`c39fafafc7fdc807b91c841eca12684a49e12dfb452f7a5323232fbbefb850e3`.
The coordinator receives the separate hash for this note. After reported
freeze, corrections require preserved new versions, not edits to originals.

## Prior knowledge and authority separation

The current batch/parent protocols, field contract, main repository authority
instructions, and investigation charter were read. Their used dependencies,
both contexts' complete declared input maps, source/page, and literal script
are pinned. Extra authority files and skills are authority/context dependencies,
not scientific evidence. The evidence-falsification and source-of-truth skills
required the explicit distinction between reproducibility and acceptance,
and between source observations and interpretation used here.

The reader knew this batch overlaps a previously inspected F5 context; no
prior F5 annotation or counterpart annotation was read. Whole-page/strip
orientation means this is not blind selection. Shared metadata clarification
from the coordinator changed `candidate_routes` serialization to lists; it
did not supply annotation cells. No counterpart exchange preceded this freeze.
Only this reader's three assigned files were written. No legal text, other
investigation, source bytes, comparison, physical metric, or activation changed.
