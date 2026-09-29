# Camera 2 all-frame extraction: read-only reuse assessment

September 20, 2026 UTC. Proposed Stage B method, not execution or acceptance.
No historical images were extracted/viewed and no endpoints annotated in this
review. The exact source/view work and subsequent Stage B declaration control
scientific scope; old screening protocols do not grant a new measurement pass.

## Smallest complete reuse path

Use a small **Camera 2-only driver in this unit** that imports the pinned
read-only main-repository `multiview-onset-review/extract.py` functions:
`inputs`, `decode`, `sheets`, `fingerprint`, `write_json` and the Camera 2 spec.
Preserve their full ordered raw-hash, native-plane, diagnostic and output checks.
The new driver should own a strict fixed-interval selector, exclusive fresh
output creation, current protocol/code/runtime snapshots, before/after pins,
failure record and complete artifact receipt. This avoids recreating the decoder
or broadening the task to Camera 4. It is a proposal, not implemented code.

Do not copy the old script into a new directory and assume its constants still
resolve correctly: `ROOT` is derived from the script's filesystem location.
Import the explicit pinned original path as a read-only dependency, or make any
intentionally changed input-root resolution explicit and tested. Do not silently
modify main's source, historical selections or receipts.

The existing top-level extraction CLI is **not directly Camera 2-only**:

```text
extract.py --out FRESH_DIRECTORY [--refinement JSON_PATH]
```

`run()` loops over both entries of `SPECS` unconditionally. An empty Camera 4
list still opens and fully decodes Camera 4; omitting the key fails. The
refinement JSON accepts per-camera index arrays and silently collapses duplicate
indices through a dict. Its additional metadata is copied but is not a semantic
selector validation. Without `--refinement` it uses its old one-second sampler.
Its stored protocol snapshot is the old screening protocol, not this new stage.

## Exact fixed selection, computed without media decoding

For the **closed encoded-time interval [220,234] seconds**, exact-rational CSV
selection gives **419 interior stored frames**, indices 6594 through 7012.
Adding the immediately preceding and following stored frames gives **421 total**,
indices 6593 through 7013 inclusive. These are extraction boundaries, not
candidate event locations or measured onset times.

| Role | Source index | PTS at 1/2997 | Exact encoded seconds |
|---|---:|---:|---|
| Preceding bound | 6593 | 659301 | 219767/999 |
| First inside | 6594 | 659400 | 219800/999 |
| Last inside | 7012 | 701204 | 701204/2997 |
| Following bound | 7013 | 701303 | 701303/2997 |

Compute membership from rational PTS, not nominal FPS times 14 seconds. Require
the interior to be nonempty, both adjoining frames to exist, strict ordering,
unique integer (not boolean) indices, exact membership and explicit distinct
selection reasons for interior and each bound. No arbitrary imported index
list should stand in for verification against the declared interval.

The existing decoder checks **all 8042 frames** from the full Camera 2 source
and saves only selected frames. Reuse that contract; input-side seeking would
change decoder state and remove its complete ordered source-map cross-check.
421 native PNGs would require 27 of its existing 4-by-4 overview sheets.
Sheets remain screening aids, not native-resolution endpoint evidence.

## Source and implementation pins

Main base is `/Users/admin/docs/911/research/sherlock-wtc7-investigation/`.
The reviewed implementation, tests, old protocols and verifier were fully read.
Fresh script hashes match the earlier accepted controls/receipts where stated:

| Dependency | SHA-256 |
|---|---|
| `multiview-onset-review/extract.py` | `df245c5fcf2790a45643c1fddf481bd38c63aed3592a4b0c9ad32819c23dc64c` |
| `multiview-onset-review/test_extract.py` | `3898f4baaf721df3637d89fdbb2a959b1e36485c89e2be997461d156ff6f67b4` |
| `multiview-onset-review/PROTOCOL.md` | `1dfdabe397ff64fba08b712f2999242380aa1cd5733f74152392064aec8794a5` |
| `multiview-onset-review/declare_refinement.py` | `c96fe520438e30bbc3f6d3150f4c9ac3494b9df1a6cbee2c60d897b1419a1bb0` |
| `multiview-onset-review/verify.py` | `56b54d5c00370a4fa68bd35a4621037297f73ef9cf0fcf8e1f4441f57b7a6269` |

Camera 2's encoded source pin is
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`,
208810910 bytes. Its four read-only input artifacts are the source MOV and
`timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/` files:

- `frame-map.csv`: `ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812`.
- `frames.json`: `424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0`.
- `source-identity.json`: `632c27b1ad4d04bddd991568a7c30206841ae3af5606fac801e61ffff561ca38`.

The old `inputs()` checks source/map hashes, source size, counts, strict rational
time/order, dimensions, YUV420P format and metadata PTS before returning rows.
The new run must execute those checks before and after its own decoding; their
historical receipts do not waive them. This review's selector used the held CSV
but did not freshly rehash the MOV or execute a historical decode.

## Pixel, clock and diagnostic contract

The exact decoder path is `/opt/homebrew/bin/ffmpeg`, video stream `0:v:0`,
with `-copyts -noautorotate`, audio unmapped, `-noautoscale`, YUV420P output,
`-fps_mode passthrough -enc_time_base:v demux`, and a rawvideo pipe. Every
complete 640-by-480 full YUV frame must match its prior decoded SHA-256, in
order; missing, short or extra bytes reject the run. Selected native PNGs retain
unchanged Y-plane byte values in mode L, checked by reopen/roundtrip. No RGB
conversion, intensity adjustment, deinterlacing, interpolation or stabilization
is performed. This does not recover calibrated luminance or color.

The raw pipe carries no PTS. Its timestamp join relies on the **full ordered
raw-frame hash match** to the independently preserved map, not a fresh timestamp
measurement in that pipe. Equal source frames and orderly PTS do not authenticate
the original exposure clock or absence of earlier editing.

The only admitted warning grammar is the existing exact PCM-audio stereo
layout guess, with the source-specific process-address form. Unknown/additional
nonmatching lines reject the run. The old Camera 2 receipt has one admitted
line; the classifier permits zero or multiple matching lines and returns their
count. Do not call it an enforced exactly-one-line check. Preserve any changed
count for review rather than suppressing it. An unrelated warning gate from a
later unit is not automatically this helper's gate.

The old Camera 2 full-stream digest is
`1490b125faceae77a19edbda835682da3876f503c766af04be6cf6e93751b4dc`;
it can be a comparison target, not a replacement for per-frame checking. The
decoder has a 55-second child watchdog. Writing 421 PNGs is a different workload
from prior sparse runs; retain any actual timeout/failure and separately declare
changes rather than letting a tool observation timeout trigger a restart.

## Tests and reproduction: what is reusable

The saved `controls03/receipt.json` reports eight passing tests, zero failures/
errors, with code/test hashes matching the fresh values above. These historical
tests cover known lossless Y/U/V patterns with nonzero irregular PTS, rational
sampling/coalescence, malformed maps, wrong hashes, partial/extra raw streams,
odd geometry/invalid indices, output collision and exact diagnostic grammar.
They remain evidence about those implementations, not this new driver or a
fresh runtime pass. No tests were run in this read-only review.

Before new historical extraction:

1. Rerun the unchanged eight synthetic controls into a fresh directory using
   the selected current runtime and `PYTHONDONTWRITEBYTECODE=1`; do not overwrite
   any old control output. Existing CLI is `test_extract.py --out FRESH_DIRECTORY`.
2. Add focused synthetic tests for the new closed-interval/all-frame selector,
   exact/on-either-side boundary cases, nonempty/available-bound guards,
   duplicate/boolean/unsorted input rejection, and Camera 2-only operation.
   Test new wrapper snapshots, before/after pin checks, output collision and
   failure handling. Old top-level `run()` tests do not cover a new driver.
3. Pin actual driver/dependency/protocol/selector, Python, Pillow, FFmpeg and
   test ffprobe paths/versions. Do not claim that executable hashes alone pin
   every shared library or package byte.
4. After the stage's admission, produce two fresh historical scopes. Compare
   every selected row, PNG pixel/file hash, sheet, inventory and snapshot.
   Retain actual raw diagnostic hashes; allow only the reviewed process-address
   difference between otherwise equivalent matching logs, not arbitrary text.
5. Independently rederive all 421 selected rows and adjoining bounds, validate
   copied PTS/map fields, native pixels/products, inventories and repeated-run
   equality. This verifier must not import the producer's selector. A shared
   decoder/library is still a common dependency, not independent source proof.

Freshly checked binaries still match the older recorded FFmpeg/Python hashes:
FFmpeg `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`;
Python at `/Users/admin/.pyenv/versions/3.13.7/bin/python3`
`7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e`.
Fresh ffprobe hash is
`fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`.
The old receipt reports Python 3.13.7, Pillow 12.0.0 and FFmpeg 7.1.1. Current
package/runtime execution was not retested by these file hashes.

## Do not run the old verifier unchanged

Its CLI requires the output to be **main's existing**
`multiview-onset-review/verification.json` and overwrites that path. Its camera
set, declared interval groups, old snapshots, relative scope root and original
artifact layout are hardcoded. It is not a drop-in validator for the new scope.
Reuse narrowly applicable independent arithmetic/inventory routines in a new
explicitly scoped checker, preserving the old verifier and receipts. Likewise,
the old declaration generator writes the old `refinement.json` and contains
different intervals; do not invoke it for the new selection.

No original script, historical output, case source, legal record or engine
state was changed. Only this proposed-method note was added. The finite
exact-rational CSV selection and fresh hash checks above are the actual checks
performed, not a current extraction/test pass or scientific event measurement.
