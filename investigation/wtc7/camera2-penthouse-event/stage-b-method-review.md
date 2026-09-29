# Stage B producer implementation and synthetic control record

September 20, 2026 UTC. This is the implementer's method record, **not an
independent review of the implementer's own code**. Root source/code review,
separate artifact verification, historical execution and observation remain
separate. No historical media was decoded or visually annotated in this task.

## Implemented, tested, not historically executed

The implementer read `STAGE-B.md` completely and followed the current charter,
source-preservation and development-verification controls. Added only:

- `stage_b_extract.py`, a Camera 2-only driver over the pinned unchanged
  historical `inputs`, `decode` and `sheets` functions;
- `test_stage_b_extract.py`, bounded synthetic orchestration controls;
- this record, plus the fresh control-output directories described below.

The new driver does not invoke the old two-camera CLI, old declaration writer
or fixed-output verifier. It imports the original helper only after checking
its pinned bytes, with bytecode writing disabled during import. The CLI has
only `--out`; there is no camera switch, arbitrary source or interval override.
Outputs must be previously absent descendants of this investigation unit,
without a symlink route. Outside-unit and main-repository targets fail before
creation. Existing source/code/output files are not overwritten.

Selection is exact rational [220,234] with adjacent stored bounds: 419 interior
and 421 total rows, indices 6593-7013 inclusive. The driver rederives the plan,
checks metadata, and admits only the fixed count/range. It calls the inherited
full-source 8042-frame decoder, not a seeking or 421-frame-only decode.
Every saved selected row receives its pinned metadata duration, as integer
source ticks and exact rational encoded seconds. No PTS or pixel is retimed.

The inherited diagnostic classifier remains unchanged. The new driver adds
**exactly one** known PCM stereo-layout-guess line, checking both the reported
classification and actual raw log. Zero, two, or an unknown line fail. Native
PNG dimensions, mode, map fields, filename, byte hash and decoded Y-plane hash
are rechecked; the existing sheet renderer is retained. A passing receipt does
not establish feature identity, original exposure timing or event onset.

## Current pins

| Artifact | SHA-256 |
|---|---|
| New producer, 11388 bytes | `08932e04ff5e18d22f56c9e98f52311e43c7de3941e16841ac8c2e4640584a9a` |
| Final new tests, 15131 bytes | `38354b7bf258c057ac71745ad88267d7bb9801d84d67661c2eb066739552f072` |
| Stage B declaration | `24738fd6c695f450972b663cb55836b3d935b8c91487630c1aeca763d21d3da3` |
| Unchanged imported producer | `df245c5fcf2790a45643c1fddf481bd38c63aed3592a4b0c9ad32819c23dc64c` |
| Unchanged inherited tests | `3898f4baaf721df3637d89fdbb2a959b1e36485c89e2be997461d156ff6f67b4` |

The declaration and inherited producer/protocol have expected hashes enforced
by the new code. Each actual execution also snapshots its own producer, the
declaration and inherited implementation/protocol separately, with current
Python, Pillow, FFmpeg and ffprobe identities/versions. These are finite local
runtime pins, not a hermetic build or all-library attestation.

## Actual control executions

Working directory for all commands:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Commands used `PYTHONDONTWRITEBYTECODE=1` and
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`.

| Fresh scope | Command suffix after the runtime | Observed result |
|---|---|---|
| `driver-controls01` | `research/sherlock-wtc7-investigation/camera2-penthouse-event/test_stage_b_extract.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/driver-controls01` | 16 tests, zero failures/errors, terminal exit 0; session 34459 |
| `inherited-controls01` | `/Users/admin/docs/911/research/sherlock-wtc7-investigation/multiview-onset-review/test_extract.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/inherited-controls01` | 8 tests, zero failures/errors, completed exit 0 |
| `driver-controls02` | `research/sherlock-wtc7-investigation/camera2-penthouse-event/test_stage_b_extract.py --out /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/driver-controls02` | 17 tests, zero failures/errors, terminal exit 0; session 16158 |

The producer bytes were identical across both new-driver control runs. The
second test version adds a synthetic wrong-byte fixture that exercises the
**actual inherited input-pin guard**, with its media path temporarily directed
only to that synthetic fixture. The first test snapshot remains preserved:
SHA-256 `eccf16bfa89d2097322902d0bfd2f9847f251c8c3d4815948537bc0c32b49d2d`.
There was no failed control suite or post-failure criterion relaxation.

Current driver controls cover rational exact/on-either-side boundaries,
adjoining frames, empty/missing-bound cases, strict index/clock input,
fixed-map selection without pixel decoding, output/symlink/collision guards,
dependency-before-source ordering, source-before-decoder ordering, invalid
duration rejection, a complete synthetic Camera 2-only run, exact warning
count/grammar, wrong decoded count, post-source change rejection, and CLI
help, dispatch, unsupported camera argument and outside-output rejection.
The inherited eight controls freshly test known lossless synthetic planes,
irregular timestamps and its existing decoding/map/stream/diagnostic guards.

The complete synthetic driver adapter writes flat synthetic luma, never
historical pixels, and labels its result `synthetic-adapter-control`. The
top-level test receipt labels the suite `synthetic-controls-no-historical-decode`.
Such a receipt must never satisfy historical-source acceptance. The one
fixed-map control reads the held timing CSV and checks its pin/selection; it
does not decode, view or infer an event from the historical source.

Eight deliberately rejected synthetic driver scopes remain in the final
control tree, each with `failure.json` and no accepted `receipt.json`:
dependency, source, metadata-duration, decoded-count and post-source failures,
plus zero/multiple/unknown diagnostic cases. Their expected rejection is a
passing guard test, not a failed historical extraction or hidden discarded
scientific result. Output-collision/escape guards reject before creating a
new output scope; they therefore intentionally create no failure file outside
the permitted directory. A symlink escape fixture remains local and is explicitly
listed in the control receipt rather than followed into other directories.

Receipt pins:

- `driver-controls01/receipt.json`:
  `59338458fee8fd2be9fbfdfcd0f1bc9a73cde230dd116388465dadf6a91f7f7c`.
- `driver-controls02/receipt.json`:
  `15c0f3cefb2b0fd43739d5fcdf855d9faab7b37f4406488f0740affd0fcdbdee`.
- `inherited-controls01/receipt.json`:
  `f01c825d0150eda2388fbe93a3d2d0c41ee64f7b60897ad9d6d63cafff6eaa8d`.

The new test receipts record Python 3.13.7 and Pillow 12.0.0. The older test
runner's receipt omits those runtime fields; its actual launch command and
current runtime are recorded here without silently adding fields to that
preserved receipt. Root separately reported its own fresh eight-control run
under `stage-b-inherited-root01`; this implementer neither overwrote nor claims
to have independently checked that root-owned output.

## Actual output/receipt contract for root and separate verifier

A successful driver scope contains:

- `driver-snapshot.py`, `stage-b-snapshot.md`,
  `inherited-extract-snapshot.py`, `inherited-protocol-snapshot.md`;
- `initial.json`: actual code/declaration/dependency/binary pins and versions;
- `selection-plan.json`: exact fixed membership/rule/counts;
- `source-pins-before.json`, `source-pins-after.json`;
- `camera2/`: 421 native PNGs, 27 navigation sheets,
  `decoder.local-only.log`, `selection.json`;
- `receipt.json`: status, execution kind, only Camera 2 counts, complete product
  fingerprints excluding the receipt itself, and runtime pins before/after.

`camera2/selection.json` retains the inherited full-stream digest, decoded
count/geometry, exact command, diagnostics, source-map rows, selected PNG/luma
pins and sheet list. It adds source ID, explicit execution kind, duration fields,
and input pins before/after (plus the compatible `input_pins` field). Both source
and runtime before/after values must match, rather than simply being stored.

A failed execution after a valid fresh output is created preserves its partial
files and a failed receipt with phase/type/message. It has no success receipt.
No error-handling code promotes partial images or auto-restarts a decode.
The inherited 55-second watchdog is unchanged; a future real workload failure
must be retained and reviewed, not silently patched away.

## Verification ceiling and remaining work

Root must finish actual source/code review and rerun controls before historical
execution under its retained authority. The separate verifier author received
the schema and code pins, not endpoint candidates. Its tests and review are not
claimed here. Pairwise real-run reproduction, independent artifact checking,
viewing coverage, endpoint uncertainty, human/specialist review and scientific
comparison remain undone by this implementer.

No browser UI was changed or tested; browser verification is inapplicable.
Direct whitespace/conflict-marker scans of both new code files found no
matches. Fresh hashes confirm the inherited producer/tests remain unchanged.
No commit, push, source alteration, historical decode, additional PDF/media
view, accepted-engine transition or legal-record change occurred in this task.

## Later root-reported execution status

After this implementer froze the code and control record, root reported full
review of the producer/tests, fresh passing inherited eight and driver seventeen
controls, and two historical runs that each completed with exit 0. Root reported
421 native images and 27 overview images per run, agreement across the paired
products, 458 inventoried products per receipt, exactly one admitted warning
per run, and passing raw-stream, map, duration and luma checks in its own
read-only traversal. These are **attributed coordination reports**, not checks
performed or independently verified by this implementer. This implementer did
not open either historical output or annotate any endpoint. Root retained the
separate-verifier review and later visual-admission gates. The earlier remaining-
work paragraph records the handoff state before this later report; this
postscript does not promote an artifact or scientific conclusion.
