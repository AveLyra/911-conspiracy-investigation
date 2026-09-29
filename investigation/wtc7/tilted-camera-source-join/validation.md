# Verification and handoff receipt

2026-09-19. This bounded source/data correspondence unit made **progress** under
the active investigation goal. It did not complete WP2, all Luna reevaluation,
the comprehensive investigation, an expert review or any legal/send gate.

## Implemented, verified and not accepted

Implemented: safe preservation of one exact nested public clip; complete
allowlisted saved-project export; fixed scene and position-table comparisons;
two independently written arithmetic checks; source-method and critical
reviews. Existing source files, prior outputs and legal records were not edited.

Verified: the exact scopes below. Accepted/activated: **no** new Sherlock or
Faraday result, bridge workflow, physical calibration, source-clock
authentication, expert measurement, cause finding or legal fact. Synthetic
controls and deterministic repeats are not physical experiments.

## Actual commands and results

Commands below are relative to this unit unless an absolute path is shown.
Root/export/scene/table runtime was Python 3.12.14 at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
with NumPy 2.3.5 and Pillow 12.3.0. The independent source/table reviewer used
Python 3.13.7 for its Fraction/determinant calculation. FFmpeg/FFprobe were
7.1.1 at `/opt/homebrew/bin/`. No new packages were installed.

| Check actually executed | Outcome and ceiling |
|---|---|
| `prepare_media.py test` | Seven synthetic controls passed before media processing and again in root's final check. |
| `prepare_media.py preserve` followed by the declared probe/decode stages | Exact parent/member/duplicate-media pins matched. 476 frames decoded without warnings. `views01` and `views02` independently decode the same complete stream and retain the same eight selected PNGs. |
| Main `multiview-onset-review/test_extract.py --out …/extractor-controls01` | Eight controls passed, including the actual synthetic irregular/nonzero clock decode and expected failure conditions. |
| `prepare_candidates.py --out candidates01` | All 8,042 Camera2 decoded frame hashes checked against the held map. 701 declared candidates retained. One previously classified audio-layout diagnostic; zero unclassified diagnostics. No claim that all candidates were visually reviewed. |
| `project-export-tests.py` | Seventeen synthetic tests passed, including null/duplicate/invalid/security/locator conditions; root reran them successfully. |
| `project-export.py --out project01.json` and `--out project02.json` | Fresh outputs byte-identical. Same-agent independent direct-XML oracle checked 1,469 locators, 742 lexical values and all 668 x/y scalars; passed. This is not an outside independent review. |
| Source-method synthetic program and pin checks retained in `source-semantics-pins.json` | Twelve inverse/round-trip cases, sparse indices and irregular-clock caller distinction checked. Twenty source pins rechecked. Historical Tracker executable and missing leaf call were not run. |
| `compare_scenes.py --test`, then `--out scene01` / `--out scene02` | Seven synthetic controls passed before scoring and again afterward. Both full 67,296-pair outputs reproduce byte-for-byte. |
| `scene-independent-check.py --controls-only`, then `--output …scene-independent01.json` / `…02.json` | Twelve synthetic controls pass; complete independent score outputs are byte-identical. All 67,296 MAEs and correlations, 96 entire rankings and 24 selected summaries checked against root; no disagreement beyond the declared numerical bound. Root reran the controls, not this entire independent historical computation. |
| `project-table-controls.py`, then `compare_project_table.py --out table01` / `--out table02` | Thirteen synthetic controls pass before each calculation and on root's final rerun. All 334 rows/48 pairings retained. All four output files reproduce byte-for-byte. |
| `table-independent-check.py --controls-only`, then `--out table-independent01.json` / `…02.json` | Twelve independent control groups pass; distinct determinant/Fraction computation precedes inspection of peer results; outputs byte-identical. |
| `table-independent-check.py --compare-existing` | Independent reviewer and exporter each ran the final read-only verifier: 62,910 field/decision checks, zero disagreements. Root read both reviews and rechecked source/output pins and reported discrete counts, not all 62,910 comparisons afresh. |
| `verify_unit.py` | Root read-only integrated check passes: **20 file pairs** byte-identical, **753** distinct pinned paths checked and rechecked, row counts/flags/failure indices verified. Full details remain in the individual receipts. |
| `python3 /Users/admin/docs/911/tools/validate_record.py --strict` | Exit0: headers, issue↔fact links and citation tags OK. This is record-structure verification, not legal or scientific approval. |

Final local integration checks also passed: all **12** unit Markdown documents
were checked for conflict markers/trailing whitespace and all **24** detected
local Markdown links resolved directly, with no missing target or main-path
fallback. All **10** unit Python files parsed successfully with `ast.parse`.
The scoped `git diff --check` for the four tracked research navigation/control
documents exited0. These are syntax/navigation checks, not execution of all
scripts or verification of every linked document's claims. Untracked unit
documents were checked directly rather than falsely included in the tracked
diff check. Final report hash matches the critical review's resolved version:
`c1851faca025c31edc6ac6d660f5edf2fa97ff569a750f3846b18d783890ce38`.

The root integrated pin-map digest is
`9d4310ebc2c337c8ec59631eeb2207141b0569d99bcf25d7ae53a4de459c8991`.
The map is deterministically reconstructed from the script and underlying
receipts; it is not a claim that 753 independent evidence sources exist.

To rerun the read-only integrated check from the worktree root:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/tilted-camera-source-join/verify_unit.py
```

Original output names use exclusive creation. Existing runs must not be
overwritten merely to reproduce them. Detailed stage arguments and source
pins are preserved in each script's interface and execution/receipt files.
Source-method and agent-local verification commands are retained in the
[export](project-export-review.md), [scene](scene-independent-review.md) and
[table](table-independent-review.md) reviews.

## Material output identities

| Product, with byte-identical separate repeat | SHA-256 |
|---|---|
| Native Tilted `frames.json` | `2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15` |
| Sanitized project JSON | `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8` |
| Root scene scores | `f9dda2fe913ccf39c2caf4794812c7c7fee388f53f0bb0c55c50a808212cdc17` |
| Independent scene scores | `280f247c7561e1625361daab9e1f4c6ea0f9b066c034d9ea7d7cd59fea8c3dd7` |
| Root project/table comparison | `ee49c2628398d5b1009df9c8ef12dc51aa1ec74a4c4a697d894bad38dda3bf19` |
| Independent project/table comparison | `61f2b977e3ceae5c8987744357b6d9a41039d6de5a315272145cb708414f839d` |

Exact arithmetic agreements do not multiply source independence. Both scene
calculators share images, masks and Pillow; NEAREST and BOX lose their filter
differences on this sampled grid. Both table calculators share the exported
positions, source-reviewed transform and the same reconciled printed table.

## Review and preserved failures

The [critical review](report-critical-review.md) found no numerical conflict.
Root tightened “available” to **shared finite** comparisons and separated exact
categorical agreement from numerical tolerance. It also clarified that solving
the paper's historical editing/version chain is not a prerequisite for every
new independent measurement. Such measurements still need their own calibration,
uncertainty and human/specialist gates. Review versions and dispositions remain
in that memo; no reviewer was represented as an outside engineer or human.

The individual reviews preserve these failed attempts, none counted as passes:

- An ambiguous initial archive ordinal selected the duplicate MP4, then failed
  the TRK hash/size guard before parsing or output. Explicit zero-based indexing
  was clarified before the successful export.
- Export/independent-output writes initially hit the worktree sandbox boundary;
  successful retries used scoped permission, not a main-repository workaround.
- An export-summary syntax error, serialized-key-array locator error, initial
  key-array representation assumption, source-check harness variable collision
  and beyond-EOF display range were corrected with their earlier states retained.
- One independent scene control's expected integer sum was mistyped; it failed
  before historical scoring. The corrected fixture passed without a changed
  scoring method. A later uppercase/lowercase schema adapter also failed before
  successful full output comparison.
- A preparatory table inventory referenced an absent receipt path. The actual
  source/probe paths were pinned before historical computation.
- Root's final media-test invocation first used `--test` instead of the actual
  `test` subcommand; it exited2 at argument parsing with no source processing.
  The corrected command passed all seven controls.
- A root image response was context-truncated; the affected candidate images
  were explicitly redisplayed before inspection was counted. A verbose successful
  integrated pin-check display was truncated; compact-output rerun passed with
  unchanged checks. Truncated output is not evidence of full human visual review.

No mismatch was fixed by changing scientific criteria, historical coordinates,
clock settings or a source hash. The coarse-time versus strict-time difference,
three unavailable pairings, absolute-position failures, PM05 nonkey failures
and scene branch/region ambiguities are results, not harness errors to erase.

## Current state and next task

Repository: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD `e8d83d7`. The research worktree
contains substantial intentional pre-existing WIP; this unit and navigation
changes remain uncommitted. No commit/push, main legal edit or source mutation
is claimed. [STATUS](../STATUS.md) remains the existing operational handoff;
raw sources and the main charter retain authority.

The smallest publication-reproduction follow-up is a bounded held-record search
for an exact original point/time export or specifically linked alternative
project version that explains the coordinate/clock/nonkey differences. Declare
the targets and row test before calculation; either an authenticated version
join or a precise retained gap is acceptable. Do not fit offsets away or repeat
this completed arithmetic as new evidence.

In parallel, new independent video measurements may proceed through their own
source-raster point/endpoint, dimensional, aspect/projection and uncertainty
checks; no need to make all of the paper's provenance a prerequisite. The
human/specialist gate before consequential measurement is unchanged. The
late-fire lineage lane and other charter work remain open. Full-reasoning
interpretation is appropriate; bounded byte and row checks can be delegated.

Sherlock feedback remains deduplicated and local pending the archived
destination's routing decision. The context-distiller skill keeps this next
step and the actual verification limits in the established handoff; it does
not authorize accepting a finding or completing the goal.
