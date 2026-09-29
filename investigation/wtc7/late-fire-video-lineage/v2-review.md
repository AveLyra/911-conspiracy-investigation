# Version 2 inventory grammar: implementation and controls

2026-09-19. Local research helper revision under GRAMMAR-FOLLOWUP.md, SHA-256
`8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723`.
Original helper/tests/protocol/selection and all previous runs remain preserved.

## Frozen implementation scope before tests

This separately named full copy changes only recognition/counting of one
terminal empty compact-inventory token, plus run revision/declaration metadata,
a declaration snapshot and its final identity check. Existing exact field set,
unique keys, integer values, fixed dimensions, increasing PTS, decoder commands,
diagnostic classifier, sampling and RGB/overview processing are unchanged.

The original sixteen test methods are copied unchanged and import v2. Ten
additional targeted methods cover old/trailed/mixed grammar, field order,
malformed empty tokens, unknown payload, duplicate/missing/noninteger fields,
PTS/raster refusal, Late-SEI refusal, revision/snapshot metadata and declaration
integrity gates. Tests may generate/decode only tiny synthetic fixtures.

Declared exclusive synthetic output directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/v2-controls01`.
The test suite writes all successes and intentional failures there; it cannot
overwrite an existing destination. No historical decoder invocation is
authorized for this agent. Saved Camera2/kit inventory text may be replayed
for metadata planning only.

Root must review the complete v1/v2 diff and completed controls before its
separate historical execution. Only VID-WTC7-001 and CAMERA3-KIT-MP4 may enter
the declaration's new v2-run destinations; source 006 remains refused. This
helper revision is not a scientific finding, image acceptance, clock
authentication, physical calibration, causal ranking or a general allowance
for unknown fields/diagnostics.

## Results

**Implemented and verified on synthetic controls; historical execution remains
for root after its full-diff review.** The 26-test suite passed with zero
failures/errors. The 16 original test methods and every original test class,
fixture/helper function and dispatch definition are AST-identical; only the
import selects `screen_local_v2`. The ten new methods are additional controls.

The complete helper diff was inspected. Only `frame_plan` and `run` change,
plus three revision/declaration constants. `frame_plan` recognizes one terminal
empty token only if exactly three nonempty tokens precede it, then applies the
unchanged remaining schema/numeric/geometry/order checks. Its coverage adds
`recognized_terminal_delimiter_records`. `run` adds the revision identifier,
checks the declaration's fixed hash, preserves `grammar-followup.snapshot.md`,
and includes declaration identity in the final control check. The generic
`screen_local.snapshot.py` filename now contains the actual v2 producer bytes
in each new v2 run, with the recorded producer hash and revision identifying it.
The source-level command construction, diagnostic classifier, showinfo/PNG
checks and all other helper functions are unchanged. No Late-SEI allowance,
new codec path, timestamp repair, resampling or source selection was added.

### Exact implementation and control artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `screen_local_v2.py` | 20997 | `890963c2104f53813593b4e09da9b3c5892d2461a2a6a415f06f84842b31d8f9` |
| `test_screen_local_v2.py` | 19522 | `61fee5f4bd23a6ce3b6abd372c3f40d6d9e0d3ea9ab3d71ebe745c239c731c83` |
| `v2-controls01/test-receipt.json` | 724 | `5c8fefe8a36164bce3d359b7d69c50edf2c6c45848f26b09a984d0f0944d344a` |
| `v2-controls01/unittest-local.txt` | 3265 | `49b586c758daaa00d89f0c910c8eaec3149b9738f594d8a15c8d6f441e555393` |

Originals rechecked unchanged after testing:

- `screen_local.py`: `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c`.
- `test_screen_local.py`: `5988d73bfb93e24546f015983c0070f7e767c831f8330973b03f962731337b74`.
- `PROTOCOL.md`: `f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486`.
- `selection.json`: `e5abd641738cbbb7656f2c4d0f70336725247787d8955637082a44401047fdc0`.
- `GRAMMAR-FOLLOWUP.md`: `8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723`.

### Actual commands and results

From `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`:

```sh
diff -u research/sherlock-wtc7-investigation/late-fire-video-lineage/screen_local.py research/sherlock-wtc7-investigation/late-fire-video-lineage/screen_local_v2.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/late-fire-video-lineage/test_screen_local_v2.py --artifacts /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/v2-controls01
```

The diff command returned 1 because it reported the intended differences; it
was not a test failure. The suite returned zero: 26 tests in 1.647 seconds,
Python 3.12.14/Pillow 12.3.0, using the same pinned FFmpeg 7.1.1 family as the
earlier controls. No dependencies or global settings were changed. The existing
unittest loader runs the original real-decoder fixture before the new revision-
receipt integration checks; the latter deliberately inspect that suite's saved
run01 and reuse its synthetic source. This is a full-suite control harness,
not a promise that each receipt test can run without its fixture independently.

Read-only AST checks confirmed all original test definitions unchanged and
exactly the two named helper functions changed. Separate post-run receipt
checks rehashed **70 product-hash references** across both successful outer
and source receipts; all match. The two native PNGs and one overview are
byte-identical between the two successful synthetic runs. Revision, helper and
declaration identities/snapshots match their current pinned files. Entire
receipt byte identity is not claimed because paths/diagnostics are run-specific.

All intentional failures remain under `v2-controls01`, including the inherited
negative controls and new `bad-v2-declaration` (`grammar_declaration_pin_mismatch`,
preflight) and `changed-v2-declaration-simulation` (`control_changed`, final_pins).
The latter simulates an identity change without modifying declaration bytes.
These expected negative outcomes are passed tests, not accepted historical runs.
No development or synthetic invocation failed in this v2 implementation lane.
No browser check applies to this non-UI helper.

### Saved-inventory planning check, with no historical decoding

An additional bundled-Python `-B` read-only program imported v2 and each failed
run's frozen v1 snapshot, rechecked inventory/snapshot hashes, and replayed only
the saved integer inventory text. It compared v2's complete plan and all old
coverage fields against v1 applied to the independently diagnosed removal of
exactly the known terminal token. No source media was read or decoder launched,
and no historical plan/image file was written.

| Saved source inventory | Records | Recognized terminal delimiters | Candidate samples | Hypothetical plan bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| Camera2 `run01-VID-WTC7-001` | 8042 | 8042 | 135 | 33523 | `d89223e0196065177cef188b0daabbfea7a569668926733f975b1397803e17ce` |
| Kit `run01-CAMERA3-KIT-MP4` | 443 | 1 | 15 | 3541 | `625b8a75c91869ca910a39d353c0736ec97213bb45db9513f2b928e124b310e2` |

The Camera2 plan exactly matches the independently declared pre-implementation
candidate hash. The kit's 442 untrailed records retain their previous grammar;
one first-record delimiter is recognized. Serialization uses the frozen
helper's `json.dump(..., indent=2, sort_keys=True)` plus final newline. Original
inventory hashes remain `1402a823c8139f18c81b5d866fc0d8e54a5c037e35bb7c58b02d0200714f67d0`
and `61a54dc649d4a3cb7e7cd9d562a5ad173729534896de5d20fb0892ef8497ceb6`.
These are candidate-plan equalities, not completed historical screening or
independent pixel validation. The existing failure products were not rewritten.

### Remaining boundary

The declaration's two historical source IDs and exclusive `v2-run01-ID` /
`v2-run02-ID` destinations remain the caller's operational scope; the helper's
existing generic subset interface was preserved rather than expanded or
silently treated as permission for other sources. Source 006 remains refused,
and the new explicit Late-SEI test confirms the unchanged warning gate.
Root must inspect the complete diff and these receipts before its separate
historical invocation. Fresh unknown diagnostics remain refusals. Successful
grammar parsing alone does not establish RGB fidelity, full source coverage,
figure correspondence, pulse duration, original timing, calibration or cause.
