# Verification record

October8,2026. This is a record of actual operations and their limits, not
certification of graph identity, engineering adequacy or historical cause.
All commands ran in this finite-batch directory unless another path is stated.
`P` below is
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

## Source preflight and contexts

- `P -B read_context.py controls`: thirteen checks pass, receipt535059.
  Those controls did not check actual image width.
- `P -B read_context.py save01` and `save02`: both fail before output with
  `Wrong source representation`, receipt320519, combined exit1. These are
  failed attempts, not completed source-context extractions.
- `sips -g pixelWidth -g pixelHeight -g space` on both named sources:
  741 by88 RGB, receipta6d9a0. Original source hashes are in both protocols.
- `P -B read_context_v2.py controls`: fifteen true checks, receiptb17726.
  This includes explicit correct-width acceptance and wrong-width rejection.
- `P -B read_context_v2.py save01` and `save02`: both exit0, receipt00bd74.
  Each JSON is1,606,454bytes, SHA256
  `6289f98ee3ae3c89e894b10b8c5dd512e1b9d4716075ff6fe8a62900028b6ab5`.

## Original readings and main replay

The two readers supply their actual view/read receipts in the four linked
notes. Primary used15 F5 and9 F6 raw blocks; peer used8 and5. Root viewed the
whole source strips and resized composed page for prospective target selection
but did not perform a third raw-cell annotation. Separate AI reading is not
human acceptance or independent historical-source corroboration.

All four originals froze before comparison. Root read the complete four
literal source scripts (7eb17c,94b301) and all four notes (2b0563). Expansion
uses manual cell lists/runs, not an RGB detector. Consumer compatibility was
declared before the first historical comparison, without rewriting originals.

| Original | SHA256 |
|---|---|
| reader-F5-primary.json | 6ce861b44d73e09a88e3d79e754f7f2f41b9458a0baafb1630c22b2de3f2c2b3 |
| reader-F5-peer.json | dbed8ae98651c5fc21a4a11e2d97c6897ed609eac809e20b1638e376246de5f4 |
| reader-F6-primary.json | 4e3dab2e3cf358854da349a987e897fbb1f5915f8ee5c2e67e246cfa06da96be |
| reader-F6-peer.json | b1345970d11e24d552e1bb755279f84f2d251db1232e1d4cedc298b02135310e |

`python3 -B -m unittest -v test_compare.py`: initial16 tests passed57ec44;
final18 tests, including strict role-alias tests, passed6aa49b. These are
synthetic contract checks, not source-annotation accuracy tests.

Root ran `python3 -B compare.py --pair F5 --primary-sha <table hash>
--peer-sha <table hash> --run 01`, then02; repeated for F6. Actual complete
commands are in receipts46f60d andb45e3c, both exit0. Each run checks original
build equality, every record, both context identities, unchanged declared
transitive dependencies, and preserves all differences.

| Repeated output | Bytes each | SHA256, identical in01/02 |
|---|---:|---|
| comparison-F5 | 1,021,829 | d4df145a105099db75d012a38c4b5d7bc5083ab4b75aa965607222dbe5d59205 |
| comparison-F6 | 532,083 | 74aa6e596286ffab22ea44db56a9cf060d573c09f7abd575a67bcd2dd28c086d |

The F5 result pins36 dependencies, F6 pins37. These include methodological
authority/context, not36/37 independent scientific sources. The new role
serialization does not change any selected cell or curve label.

## Independent check and root replay

Context-only checking already verified26,124 records across the two copies,
13,062 distinct source cells, exact RGB, source-aware coordinates and row-major
coverage. Preliminary checker controls passed before full historical outputs.
The completed check then verified all740 route records,50 bands and16,650
operation arrays across four comparison files. Independently collected
required dependency maps are covered by the producer's36/37 entries; all45
checker pins remained unchanged. Thirty-five controls passed, including
deliberate operation corruption and omitted-dependency rejection.

Checker complete run:10be0e; exclusive final receipt save:2e5a38;
same-agent exact nonwriting replay:d7c866. Root read the complete final checker
across7814b6/a4697c and reran `P -B independent_check.py` successfully at
a4697c. The checker SHA256 is
`326cd663a0e5bf8f9eefafb45d1421fa5f81056891a26228ad49168fc28665b0`;
saved receipt SHA256 is
`449bdc39b7eaea29cc67fa81a9fcaa0688928dc79f2743e4f33546f873729076`.
The bundled checker/extraction environment is Python3.12.14/Pillow12.3.0.
Root then invoked `check_all()` without saving and compared the complete
returned object to the preserved JSON: exact equality, receiptc3dc1c, exit0.
That receipt also confirms the system producer/test Python is3.14.0.

The separate methodological reviewer inspected protocols, notes and comparisons,
not new source pixels. Its concrete unresolved examples are retained in the
report; root checked those exact saved rows at0e0051. The final prose review
returned no requested corrections for report SHA256
`3ef885a1f5670f30d3aaea6c67cca95424987883327322fa331d705fafce142d`.
Source interpretations are not validated merely because the bookkeeping passes.

The separate checker imports no producer or reader code for arithmetic and
uses truth-table/bitmask checks. Its decoding shares Pillow with extraction,
so it is not an independent JPEG decoder. It checks reading attestations as
records, not as independently witnessed perception. A source-preserving hash
does not authenticate the underlying historical curve or validate a physical
model.

## Final closeout checks and retained navigation failure

Receipt f2792c reran `python3 -B -m unittest -v test_compare.py` (18 pass),
`P -B read_context_v2.py controls` (15 true) and `git diff --check` (exit0).
A broader Markdown-navigation check then failed at receipt206ae0, exit1,
because `research/README.md` links to the absent
`sherlock-wtc7-investigation/fire-annotation/README.md`. Its later pin and
JSON checks had not run; that command is not recorded as a pass.

A separate read-only reviewer used `git show HEAD:research/README.md` with
an exact `rg` search and `test -e` (receipt171ee9) to confirm that this link
already exists at HEAD line276 and its target is absent. Scoped added-link
inspection with `git diff --unified=0`, `rg` and `test -f` (receipt9a0764)
confirmed all four newly added F5/F6 navigation links resolve. The unrelated
historical link remains unrepaired; no claim that the whole research map
passes navigation checking follows.

Root separately checked all ten Markdown files in this batch for local link
targets, trailing whitespace and conflict markers: all13 local targets exist.
It parsed all11 batch JSON files and independently recomputed byte sizes and
SHA256 for all45 checker input pins: unchanged. Receipt95d9e1, exit0, also
confirms the report hash above. This narrower check does not erase or replace
the failed broad check. A further worktree `git diff --check` passed at2aa8e0;
scoped status at76d6c9 confirms intentionally uncommitted investigation files
on `research/sherlock-wtc7-investigation`. No commit or push was performed.
