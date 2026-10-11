# F6 Im3 execution and verification record

October 8, 2026. Research-only. This record distinguishes infrastructure checks
from source-reading completion and later interpretation. No human acceptance,
physical-model validation or cause inference follows from software checks.

## Environment and prospective controls

Worktree `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, base `ca1c2233`; intentional existing WIP.
The main repository's charter controls scope; its legal files remain untouched.
Repo intake receipt `2138d5`; protocol/reader contract inspected at `95024f`
and their unchanged hashes checked at `666827` before implementation.

Commands below run in this directory unless otherwise noted. `P` abbreviates
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Context metadata records Python 3.12.14 and Pillow 12.3.0.

- `P -B read_context.py controls`: receipt `375e4f`, exit 0, all 17 controls
  true. Covers exact-white omission/near-white retention, lossless display,
  row-major geometry, out-of-range rejection, exclusive creation, clipped
  two-cell margin and correct/wrong width, height and mode. These are synthetic.
- `P -B read_context.py save01` and `... save02`: scoped worktree-write
  approval, receipt `1b11b6`, exit 0. Each has 26,312 cells, 3,232,288 bytes,
  SHA256 `8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024`.
- Separate inline Pillow check, receipt `0be854`, exit 0: read both files,
  required byte equality and the exact ordered coordinate roster
  `[(x,y) for y in range(88) for x in range(143,442)]`; compared every stored
  RGB tuple to the unchanged Im3 source directly, checked all nine input pins,
  and compared all 10,472 prior F5 context cells by exact coordinate/RGB.
  No producer extraction or comparison function was imported for this check.
- `P -B -m unittest -v test_compare.py`: receipt `6012db`, exit 0, 19 tests
  passed before historical comparison. These cover complete/partial coverage,
  source/role identity, bounds, memberships, duplicate ink, band references,
  class arithmetic, recursive pin changes and all four cross-series reader
  pairings. Empty synthetic annotations do not represent historical readings.

Initial infrastructure hashes, receipt `a7c541`:

- `read_context.py`: `f37c9f55ccdc69d6a3d83d01015cbe5eff7b1f2f8aea4febe6c40863812ae5ec`
- `compare.py`: `60685e35d7c27e305e0778788d77a37815a1461b0fbd456736027013ba3878f5`
- `test_compare.py`: `cac6f86d7d2d3d61381eb7854316a4f94adbf71177e32cdec42fa28d77cb9b65`

At this initial infrastructure stage, two separately designated source readers were executing the frozen reading
contract. Their own notes and receipts must establish actual source coverage;
the checks above do not witness their perception. Root is coordinator, not a
third annotator. The independent arithmetic checker is being prepared without
producer comparison imports. Historical results and independent verification
are not yet claimed in this initial record.

## Pre-comparison review adjustments

These occurred before any historical comparison output, without changing a
source reading or selection rule:

- Made `input_pins` explicitly list all four material originals (two new F6,
  two preserved F5), in addition to their recursive dependency entries.
  Nineteen producer tests passed again, receipt `c5eb67`.
- Made the exact-white diagnostic order explicitly solid/dash/unassigned,
  rather than depending on JSON object ordering. Nineteen tests passed again,
  receipt `7f966b`. Current producer SHA256:
  `188e84b03d1931b16fd7105d1831be594149d22c608f978efd58659f05758cbc`.
- Root read both prior F5 literal scripts, receipt `14fab2`, and identified
  two preserved supplemental band fields before executing the new checker:
  `other_possible_origins` and `continuity_claim`. The checker now validates
  those exact legacy fields without stripping them, rejects unknown metadata
  and false-like numeric continuity flags, and keeps complete originals.
  Root read the independent implementation and tests (`c5eb67`, `c3cba5`,
  `7f966b`, `bf1610`, `85b051`); all 14 independent unit tests passed in root
  replay at `85b051`. This is code/schema review, not a source-reading revision.
- Clarified the reader contract's shorthand: `candidate_routes` serializes
  as a list of `solid` and/or `dash`, not the string `both`. Both readers were
  told this metadata clarification, with no counterpart cell information.
- A file-existence check at `bf1610` returned exit 1 because the readers had
  not saved their JSON/notes yet. That was unfinished work, not a failed
  historical comparison. No annotation was repaired or fabricated.

## Frozen readings and pre-comparison compatibility

Both originals froze before any counterpart exchange. Primary's actual whole
strip/page views and fourteen full raw blocks, and peer's views/sixteen blocks
plus three rereads, are enumerated in their respective notes. Those source
coverage attestations are not independently witnessed perception by the checker.
The page displays were resized; source-strip coordinates remain native.

| Original | Bytes | SHA256 |
|---|---:|---|
| `reader-primary.json` | 341477 | `d53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9` |
| `reader-peer.json` | 365573 | `ab84ccc41a395414982489c8ef4e9d874908a4e79c6b08a84a6d3c651ba32f42` |

- Primary checks: controls `f047d2`, direct source-cell check `f66a56`,
  record/reference check `426034`, frozen literal replay `25895c`. Default
  sandbox save failed `a06d9b`; exclusive scoped save succeeded `35ca21`.
  Actual overwrite refusal `865971`. Read-only confirmation `2b0e77` left
  script, original and notes unchanged.
- Peer pre-save validation `c46ff8` rejected two route-specific bands at x413
  with the same generated ID. No JSON yet existed. Route-qualified identifiers
  corrected this without changing cells; corrected validation `90ecd4`.
  Default sandbox save failed `18c790`; exclusive scoped save succeeded
  `ece539`. Replays `1c3d70` / `a2b0ab` and actual overwrite refusal `176122`.
- Root read complete primary literal/notes at `6c9a4e` / `0fd983` and peer
  literal/notes at `e80952`. These are audit reads after freezes, not a third
  source annotation.
- The unchanged `CONSUMER-COMPATIBILITY.md` has SHA256
  `6faa9f91d73199e10c76c5e0a522310510c85ee446a3184b8f70a55238741e5a`.
  It records exact row-key aliases, the fixed primary's missing outgoing-band
  reference field and preserved old F5 metadata before comparison. Reciprocal
  route references, strict types and unknown-field rejection remain required.
- Primary used the worktree charter path. Root checked its entire bytes and
  SHA against the controlling main charter at `77f45d`: both
  `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
  Root had read main itself. Both exact paths are pinned and equality required;
  no claim is made that the primary read the main path. Unknown outside paths
  remain prohibited. This bounded path mistake is not silently relabeled.
- Final producer tests: `P -B -m unittest -v test_compare.py`, receipt
  `5d05b0`, exit 0, **21 passed** after compatibility controls. Reused prior
  helper's 18 tests passed at `bc2b3a` without modifying the old helper.

## Historical comparisons and independent reproduction

Both historical commands below completed at `6308fd`, exit 0, using scoped
exclusive worktree writes (replace `NN` with `01`, then `02`):

```sh
P -B compare.py --primary-sha d53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9 --peer-sha ab84ccc41a395414982489c8ef4e9d874908a4e79c6b08a84a6d3c651ba32f42 --run NN
```

Each run freshly executes `build()` for both new and both frozen old F5
readings, checks equality and every declared input pin, and preserves originals.
Both comparison files are 2,720,586 bytes with SHA256
`e6b1202512e0615e7f35bb4d7e843edfd9e73127278e12916c6ad11944103a02`.
No averaging, threshold adjustment, additional crop or physical-coordinate
conversion occurred. Cross-pair totals/interpretation were inspected at
`161e85`, concrete route cases at `ad31d6`.

Final implementation hashes:

| File | SHA256 |
|---|---|
| `compare.py` | `63dae6eb1e69ac974f4a065650440ac13f5fbb5f4cbfdd41b7bddad8f2076ce7` |
| `test_compare.py` | `ab75d37cffb1ab63171e4efe79e110e6bf9ae06856519ce332116a9fc63062ac` |
| `independent_check.py` | `d0eb3c11e38c135a51e6012d1ab549287ee9a9c245cd186cf8478e3eb5a2571b` |
| `test_independent_check.py` | `c7c3cbb1c271c98d123f6a034f5352e543db76ec6670d11aad33701ff69f6d95` |

The independent checker uses direct Pillow decoding, native-row truth tables
and integer-bit-mask intersections; it imports no producer, source-display
helper or reader. It adapts the pinned prior independent checker as a method
reference, not a blind implementation or independent JPEG decoder. It checks
saved reading attestations for consistency, not perception. It deliberately
does not execute reader `build()`; the actual producer replay above covers that
separate requirement.

- Independent agent's `P -B -m unittest -v test_independent_check.py` and
  `P -B independent_check.py`: `95260e`, exit 0, 17 tests/full check pass.
- `P -B independent_check.py --save`: initial sandbox denial `3fa2f0`, no
  receipt created; approved exclusive save `550591`, exit 0. Saved receipt
  `independent-check.json`: 22,626 bytes, SHA256
  `22491e6a1e4459941dff884dab4b8d54e389c3731847c5fd1ae8849ca4d8b591`.
- Root read final checker/tests at `461a18`, `9edce2`, `a7bd8b`, `cbd1a5`
  and `911ee1`; inspected exact compatibility/source records separately.
- Root `P -B -m unittest -v test_compare.py test_independent_check.py`:
  `191208` / completion `208ec7`, exit 0, **38 tests pass** (21 + 17).
- Root exact receipt replay: `45ee8e` / completion `017390`, exit 0. Called
  `independent_check.check_all()`, compared the full object to saved JSON and
  its `json.dumps(indent=2,sort_keys=True,allow_nan=False)+newline` bytes to the
  complete saved receipt. Both match; no file was written.
- Root complete comparison/literal replay: `048db7`, exit 0. Called
  `compare.run()` with the two explicit frozen new-reader SHA values, which
  freshly executes all four new/old literal builds. Serialized the full result
  in memory and required byte equality with both saved comparisons. Both match;
  all four originals and 50 dependencies remain exact. No file was written.

The receipt checks 73,568 source records across four copies (26,312 distinct
source cells), four exact 10,472-cell overlaps, 26,910 operation arrays across
the two identical comparison copies, all four originals, 50 required producer
dependencies and 55 unchanged receipt pins. Fourteen embedded controls pass;
these are not seventeen additional unit tests or new historical observations.
All selected exact-white diagnostics are empty. These results establish only
source fidelity, preservation and arithmetic, not semantic correctness,
original-curve enclosure, common support, human acceptance or physical validity.

## Report review and scoped closeout

The independent checker author performed a read-only report/validation audit
against the frozen artifacts: `17f10c` / `27c7ad`, no material issues found.
Counts, cross-pair details, compatibility limits and inferential boundaries
match; frozen scripts, JSON, comparisons, checker/tests and receipt remained
unchanged. This is documentation review, not a new perceptual reading.

Root `git diff --check` passed at `f96d22`. Because that does not cover new
untracked files, a separate bounded check at `b09e03`, exit 0, verified the
exact 21-file batch roster, final newline/no trailing whitespace in batch
Markdown/Python, all 16 local report/validation and new navigation links,
and the unchanged hashes of both original reader notes. This is not a claim
that every older repository link or unrelated WIP file was checked. Root read
the assembled report at `a68439`. Current STATUS, technical preparation and
research navigation now point to this completed finite batch and the required
all-fourteen-pair admission/limitation task. The old conditional dataset remains
unchanged. No commit, push, external message, engine acceptance or legal
promotion was performed.
