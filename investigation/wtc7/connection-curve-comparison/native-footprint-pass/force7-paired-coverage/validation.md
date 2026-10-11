# F7 coverage-follow-up execution record

October 8, 2026. Research-only. This file records actual execution as it
occurs; source annotation, historical comparison and independent review are
not complete merely because preparation checks pass.

All commands below use the bundled Python executable
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(P for brevity), with `-B`. P is notation, not an assumed shell variable.
Files belong to the existing research worktree, not main. Original graphs,
readings, admission results and the live human packet remain preserved.

## Decision and pre-extraction review

Root inspected the current authority/status, parent admission decision, F7
readings, field contracts and unchanged complete Im1/Im2/Im3/page76 images.
The page display was resized to 1376×1780 from 1700×2200; no native coordinate
was taken from it. The separate method reviewer independently inspected the
three native strips, not a new composed-page view. Its recommendation is one
fixed [220,0,330,88] Im2 target and no automatic later-descent extension.

The initial protocol incorrectly attributed a new composed-page view to that
reviewer. This was corrected **before extraction or annotation**; no target,
criterion or source was changed. Initial protocol SHA256 was
`6c24c020c0c58fb91ff902cf2a46de1fef1f3b406d17877e223d8a79aec0db37`;
the actual frozen protocol used for all saves is
`aae8d37e8f0cda59f4c226e05c386f0dd73ace7b6954c7cd7ea81142f252ab19`.
READERS.md is `d62c0390fbb19bc507cb49a8da3d04802f1ad39e39784eb88ae27cc909424417`.

The context adapter was mechanically derived from force6-im3/read_context.py,
changing fixed source, geometry, labels and pins. Root and reviewer read the
adapter; it introduces no color selection. `P -B read_context.py controls`
passed all 17 controls initially (5a3307), separately (c99be7), and after the
protocol-attribution correction (18da58). These cover exact-white retention,
lossless display, bounds/row order, representation and exclusive-write behavior.

`P -B read_context.py save01` and `save02` created separate outputs exclusively
under scoped worktree-write approval (d247b5), both exit 0. Each is 1,233,648
bytes, SHA256 `ff9f1f0e47b443994c6ba5325a1f2347c2522f48f2a79012b3c6d285bcb6874f`.
Each contains 10,032 context cells and nine pinned dependencies. Current
adapter SHA256 is `826e1bc24904d631b0b613ceea73b6ddc14b228438e77db751f291a60c717599`.

## Independent source/display checks

The separate context checker imports neither producer nor display module.
It compares both complete contexts with native Im2, checks types/order and
the complete required pin map, and decodes the producer CLI display as a
black box with its own strict parser. All 20,064 repeated records / 10,032
distinct cells and all 114 displayed columns match. There are 8,737 nonwhite
cells and 1,295 exact-white omitted cells. Shared Pillow is explicitly not
an independent JPEG decoder or evidence of perceptual ownership.

`P -B context_check.py --controls`: 15 controls pass (separate b9be0b;
root 506f89). Verification passed 13f083. Exclusive receipt save first
failed on sandbox write permission (4f3530), then succeeded with scoped
approval (75c2d8). No failed or existing output was overwritten.

`P -B context_check.py | cmp - context-check.json`, with shell pipefail:
root exact-byte replay passed (506f89, exit 0); separate replay b0ae9c also
passed. Receipt 6,210 bytes, SHA256
`85445cc886a9e4e1bf9d6019d454a5b7c8450d56b182b84124fa16af411d70ad`.
Checker SHA256 `41fc7d84f84372ee9f89f880c8a6e05f8ea0fdda53a67d34672a7a2f70a9fc8a`.
Readers were released to inspect new raw context only after these checks.

## Consumer preparation checks

The new region ID is preserved. A documented copy-only compatibility alias
avoids the older validator's two-token region parser; source, pair, geometry,
roles, memberships and original fields are checked before aliasing. Originals
are checked unchanged afterward. This is not relaxation of an eligibility rule.

Method review identified pre-save metadata guard weaknesses: mere truthy views
could omit the actual source/page, and explicit truncated-block metadata could
escape the inherited standard-schema check. Local guards and synthetic tests
now reject those cases. Prior-knowledge strings and any explicit counterpart-
access flag are checked, but the program cannot independently witness reading.
The prior independent receipt's additional dependency map is now also verified
before and after calculation. No new historical result preceded these repairs.

Actual root test commands/results, each in its named directory:

- Here: `P -B -m unittest -v test_assess.py`: initial 17 pass (15e24f), then
  18 pass after metadata controls (4d5053).
- `../../historical-applicability/admission-2026-10-08`:
  `P -B -m unittest -v test_assess.py`: 20 pass (704912).
- `../../historical-applicability/conditional-envelopes-2026-10-08`:
  `P -B -m unittest -v test_calculate.py`: 12 pass (561a5b).
- `../../historical-applicability/approach34-extension-2026-10-08`:
  `P -B -m unittest -v test_extend.py`: 8 pass (4ccfe2).
- `../force56-remainder`: `P -B -m unittest -v test_compare.py`:
  18 pass (0c883f).

These 76 current/reused unit tests and the context controls test software,
not source identity, physical curve containment or historical calibration.

## Retained inspection failures

Root's initial guessed `native-strips01/manifest.json` path was absent; the
actual `receipt.json` was located by file inventory and inspected. An accidental
read command for `completion-does-not-exist` failed without mutation; it has no
evidentiary meaning. A guessed `admission.py` filename was corrected to the
existing `assess.py` via inventory. Overlong combined output was truncated;
required protocol/contract and code sections were reread in bounded calls.
No failed read is treated as source unavailability or completed inspection.

## State at the initial preparation checkpoint

The two source readers are inspecting/recording their separate originals.
Their freezes, literal replay, historical coverage calculation, independent
arithmetic and final claim review remain to be recorded below. No consequential
graph comparison, human acceptance, physical/cause finding or goal completion
is claimed by this preparation checkpoint.

## Continuation verification and incomplete peer

Root checked current file hashes (7876ce). Frozen primary script:
`eb88429fabb627c72cdca859574daadd6f31d2fae68b44c3cd81961a6f65ca3b`;
JSON `4a3c323f83b25b93a88dd8db1b31fdcc77935e90b1494e3b3dc8f7eb40f8b734`;
notes `85e77c860c9fc701f76daa44d846ed7101f6b7ea0de5726bafa0540549963f28`.
The designated reader's read-only replay (4bc5d8, exit 0) produced two exact
builds matching the saved 151,073-byte JSON, with all 21 declared pins stable.
It checked counterpart/output presence only, not the peer's selections.

The partial peer script remains
`3d4bf1e066755d0242f287ef02b48a40fc6f27a28941953471e089214c00d98b`.
Root inspected its false completion flag, empty input pins and saved raw-block
list ending at 297. The peer reported two provenance-save rejections; the
second specifically disputed cited chunk visibility/completeness. Its reported
smaller rereads were not accepted as a completed inspection record. No peer
JSON/notes or historical result/independent receipt exists (4bc5d8).
The original false flag and partial file were left unchanged. This is an
unresolved verification boundary, not a demonstration of missing source data.

Root ran `P -B -m unittest -v test_assess.py test_independent_check.py`
in this directory: 44 tests passed, exit 0 (9baffb). Current independent checker
SHA `b95e64271eab6c2bb6c9f981ddbda39bfa8159204ddfd81304f828b231f54304`;
its tests `4a644deada7fe66838757e319929e8711cab40b127f54ed5def18c891c0e8f18`.
Current producer `e8a4af86fcaea4b34c8b86ea837fa6ec7d78455d6d576c89946818e5c0ca949a`;
tests `a3945b67fd16e0f205360b0ac411a3dd086935a22a1bf73a52123c428528a36d`.
These 18 producer and 26 independent-checker controls use synthetic fixtures.
They do not supply the absent historical paired run or certify reading.

The [current report](report.md) records the precise unresolved prerequisite.
No incomplete annotation was promoted, and no historical arithmetic was run.
