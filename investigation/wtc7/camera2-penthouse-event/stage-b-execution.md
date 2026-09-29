# Stage B extraction execution — not endpoint measurement

September 20, 2026 UTC. Implements the separately frozen
[declaration](STAGE-B.md). Root executed two historical extractions after
reviewing the driver/tests and rerunning their controls. **No newly extracted
overview or native frame has yet been visually reviewed in Stage B.** Stage A's
three held context-image views are separate. No timing result is asserted.

## Reviewed implementation and controls

The driver reuses the unchanged, pinned main-repository extractor, adds a
strict one-camera/all-frame selector and source-duration join, pins the new
declaration, confines output to fresh unit subdirectories, preserves failure
records, and requires exactly one previously assessed unmapped-audio warning.
Root read the complete producer and test implementations. Their final pins are:

- stage_b_extract.py: `08932e04ff5e18d22f56c9e98f52311e43c7de3941e16841ac8c2e4640584a9a`.
- test_stage_b_extract.py: `38354b7bf258c057ac71745ad88267d7bb9801d84d67661c2eb066739552f072`.
- STAGE-B.md: `24738fd6c695f450972b663cb55836b3d935b8c91487630c1aeca763d21d3da3`.

Root independently ran the inherited eight tests into
`stage-b-inherited-root01` and the final 17 new tests into
`driver-controls-root01`: both returned exit 0, all tests passed, zero errors/
failures. The latter includes a held-metadata selection check; it does not
decode historical video. Other controls use synthetic images/streams/maps or
failure injection. The earlier implementer's control versions/runs remain
preserved separately; repeated cases must not inflate distinct test coverage.

Actual commands used `PYTHONDONTWRITEBYTECODE=1` and
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`:

```text
/Users/admin/docs/911/research/sherlock-wtc7-investigation/multiview-onset-review/test_extract.py --out <unit>/stage-b-inherited-root01
<unit>/test_stage_b_extract.py --out <unit>/driver-controls-root01
<unit>/stage_b_extract.py --out <unit>/run01
<unit>/stage_b_extract.py --out <unit>/run02
```

Here `<unit>` means the absolute parent of this document, not a shell variable
or authorization to choose another location. These are the command arguments;
exact historical decoder arguments, runtime/source identities and protocol/code
snapshots are preserved in each run. Binaries/package versions are recorded,
not a complete operating-system/shared-library environment lock.

## Two historical executions

Both `run01` and `run02` completed with exit 0. Their tool observation handles
(56059 and 1036) are terminal, not pending processes. Each fully decoded and
matched 8,042 ordered raw YUV frames to the preserved source map, selecting
421 native 640×480 Y-plane PNGs and 27 overview sheets. The source, map and
runtime before/after checks passed. No seeking, retiming, pixel enhancement,
additional camera or audio analysis was used.

Each decode retained exactly one known unmapped PCM stereo-layout-guess line.
These are assessed warnings, not warning-free execution; each raw log remains
preserved. No additional line was admitted. The complete raw-stream digest in
both runs is `1490b125faceae77a19edbda835682da3876f503c766af04be6cf6e93751b4dc`,
matching the prior accepted decode. This checks decoded access-copy identity,
not original exposure cadence or continuous historical recording.

## Root's distinct read-only product verification

After both runs terminated, root executed an independent linear CSV/JSON/Pillow
traversal without importing the producer selector. It returned exit 0/PASS:

- Reconstructed 419 in-window rows plus the two immediate neighbors, exactly
  indices 6593–7013, from rational timestamps.
- Checked all **458 listed products in each run**, with no missing/unlisted
  files beyond the receipt itself and no failed-run marker.
- Checked every selected original map field, metadata duration, native image
  mode/dimensions and decoded luminance hash: 421 rows/images per run.
- Checked each raw diagnostic against the one-line grammar and the full-stream
  digest against the prior pin.
- Compared all **448 PNG pairs**: 421 native +27 overview, byte-identical.
  Complete selection JSONs also agree exactly, as do all four recorded runtime
  before/after pin maps.

That is 421 unique selected source frames, not 842 independent observations.
There are 896 PNG file instances across two runs, including overview derivatives;
neither this count nor 16,084 repeated frame checks creates extra source evidence.
Raw address-bearing diagnostics are preserved separately, not asserted byte-
identical. Root also checked all ten listed products in its inherited-control
receipt, which has SHA-256
`7df1d61d56f93b684c7ff8caeef4a0c8fe83f832c46f1e190f212b3583daf362`.

## Separately implemented checker and root rerun

The independent checker imports no producer code and performs no historical
decode or image display. It independently rehashes the four held inputs,
validates all 8,042 map/metadata rows, reconstructs the fixed selection, checks
every native image and duration, reconstructs overview image reductions with
integer arithmetic, and checks source/runtime pins, product inventories,
diagnostics and repeated-run equality. Pillow text rendering remains shared;
source-to-Y-plane linkage still relies on the pinned producer's observed full
raw-frame matching, not a separate decoder implementation.

Root read the entire checker and final tests, then reran **21 controls** into
`verifier-controls-root01`, exit 0, zero errors/failures. The earlier 20-test
version and implementer's final 21-test run remain preserved; the added case
checks float/nonfinite JSON rejection, and an assertion was moved outside an
expected-exception block so it actually executes. Root's command was announced
as 20 before final reconciliation, but the observed run executed all 21.
The intentionally failed synthetic fixture printed by the suite is a tested
failure path, not a failed suite or historical run.

Both the implementer's actual checker execution (`stage-b-verification01.json`)
and root's fresh execution (`stage-b-verification-root01.json`) returned exit 0
and passed. Their result records agree on every field except the actual output-
path argument. Root additionally invoked the actual CLI with run01 supplied
twice: exit 1 with **distinct-runs-required**, as intended, saved in
`verification-duplicate-run-negative.json`. It prevents counting one run twice;
it is not evidence of a failed historical decode. No historical file was edited.
The root checker handle 17642 is terminal. Actual checker arguments are saved
in each result; the driver hash was supplied explicitly, not selected silently.

| Artifact | SHA-256 |
| --- | --- |
| verify_stage_b.py | 9983608a3da2cac2c28b72b992b8eab6078194cc8bb5e1cd685032d87db4e368 |
| test_verify_stage_b.py | 1c6f6c58c8eab2cc7838a534370bc99a139ffcda0f076235dec36768793aeab9 |
| driver-controls-root01/receipt.json | 6a97f1a214e5f858933e2c2d0f7fb2ac9d89c25acd12cc5c3df75a743a7a7b74 |
| verifier-controls-root01/receipt.json | 884138d4db52cc12edbae400f173782a5376824a19ce9a386a2d807c216a5e7b |
| run01/receipt.json | a5c72edd8f7714c0916c7b66f39f745c2cd7d73c99510f6c8a4be87ed751a114 |
| run02/receipt.json | a85520fbeb1e6b8992d9fd012329d41cf2f56975fddb237678218407069b4b57 |
| stage-b-verification01.json | 59a44cd253063613053c1a290ff7f2edb90c06da7bc365f296edaf0a591d5ee3 |
| stage-b-verification-root01.json | d31a1fa06a28c2ce95fdeb7e89b01f1194940be909cb40ae571a9b495a80442f |
| verification-duplicate-run-negative.json | 8ce432f6cd65ff6cf9826f4ff36e00061e0527aadc1a66aebad1e8361d2a4998 |

Root rechecked all current checker/test/method pins against the implementers'
reported values. The separately maintained
[producer method record](stage-b-method-review.md) distinguishes its author's
own controls from root-reported historical execution; root read it in full.

## Remaining acceptance / next independent task

**Extraction acceptance is satisfied for this declared access-copy scope.**
Visual/endpoint acceptance is not. Next is the paired, separately frozen Stage B
visibility/onset annotation, with smoke/identity/camera censoring and the moving-
parapet rule. Both observers should read STAGE-B.md first, use run01's 27 complete
navigation sheets, and prospectively declare native follow-up indices within
6593–7013 before opening them. Preserve actual viewing lists and do not exchange
endpoint candidates until both records are saved. No new scope or extraction
is needed. Treat a thumbnail as navigation, not endpoint evidence.

Use full-reasoning visual/source review for the ambiguous identities; do not
delegate scientific admission to the test runner. Neither observer has begun
Stage B visual inspection at this checkpoint. Published times/prior-source
knowledge remain disclosed. Original-clock, human/specialist and causal limits
remain. The full goal is active/incomplete; no cause ranking, support-failure
time, legal or accepted-engine state changed. All temporary execution handles
are terminal; there is no hidden pending annotation process.
