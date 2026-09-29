# Released-input curve search validation

Working research. The [protocol](PROTOCOL.md) and later, still pre-scan
[byte conventions](SCAN-CONVENTIONS.md) define the new source test. The
[report](report.md) states its scientific interpretation. Independent full
common-field comparison and root replay pass; the completed checks below
are not broader engineering or whole-goal completion.

## Executed source and coverage checks

Root's separately written `search_definitions.py` imports no earlier source
reader. It retains the already established paths/pins and writes only bounded
numeric/hash derivatives. Both full source passes run its 14 synthetic test
groups first. Root01 and root02 reached EOF on all 25,368 selected bodies;
their complete result objects are exactly equal, not just summary counts.

Root01 took 19.773271 seconds, peak RSS75,546,624 bytes; root02 took18.681283
seconds, peak78,577,664 bytes. These are run-specific measurements, not general
benchmarks. Time/RSS checks are checkpointed observations, not hard operating-
system interruption guarantees. All read bounds and source pins are unchanged.

The independent `independent_scan.py` is a separate standard-library reader,
with no imported root scanner. Its code and 17-fixture/13-check control receipt
froze before source processing; its full result froze before root code/results
were released to that reviewer. It reads whole bounded bodies rather than
root's line stream, computes its own CRC, and independently checks the three
September uncompressed hashes/counts against earlier integrity pins. It took
6.807774 seconds, peak301,563,904 bytes. It reports the same body/byte/line
totals and zero searched markers. The separate complete common-field
comparison below establishes more than agreement of totals.

The readers have disclosed guard differences. Root rejects duplicate ZIP
names; the independent reader records duplicate ordinal groups and opens
each entry by its `ZipInfo` object. The pinned archive has none. Root caps an
APDL body at4MiB; the independent APDL read uses the remaining512MiB June
budget. All three pinned APDL bodies are below4MiB. Both bound ZIP members
to4MiB, September streams to512MiB and physical lines to16KiB. Those differing
guard implementations do not change this actual input coverage.

The independently designed reader retains LF-byte counts, maximum line sizes,
additional BOM fields and per-encoding/family zero counters beyond root's
schema. Such fields are not automatically dual-verified merely because
common bytes agree. Per-body aliases and archive ordinal bases differ and
must be explicitly normalized in the comparison adapter; source identity
cannot be established by a filename substring or count alone.

The frozen `independent_compare.py` compares all 25,645 records (25,368 bodies
and 277 exclusions), totaling 407,801 record leaves with zero mismatches. All
ten summary/pin comparisons pass. The full root-result repeat separately
compares 407,824 leaves and 76,387 containers without a mismatch. All 17
cross-reader byte fixtures, 29 comparator mutations and create-only refusal
pass. The [independent receipt](independent-comparison01.json) and
[fresh root replay](independent-comparison-root01.json) have exactly equal
result and control objects and unchanged matching input/code pins.

Both adapter runs used bundled Python3.12.14. Independent comparison took
1.909118 seconds, peak RSS347,471,872 bytes; root replay took1.789158 seconds,
peak379,813,888 bytes. The adapter imports both frozen readers only for
preserved synthetic fixtures; it never reruns their historical source paths.
The [independent review](independent-review.md) preserves the initial freeze
record and appends its later comparison and bounded report review. It does
not claim review of later document edits or root's subsequent replay.

Root used the host's Python3.14.0; the independent source reader used bundled
Python3.12.14. Both scanners use only the standard library. Runtime/build
strings are retained in the receipts; no interpreter or dependency installation
was performed. Cross-runtime agreement is numerical/source verification,
not independent historical evidence.

`verify_saved_coverage.py` passes seven synthetic comparison tests and
reconciles every one of25,365 June body aliases/name hashes and byte/hash/
line/NUL records with the previous frozen full-source audit (six comparison
fields per body). It separately verifies all three September uncompressed
byte/line/hash pins, complete root-result repeat, EOF and the328-byte all-NUL
exception. This is coverage reproduction against prior data, not a third
independent implementation of the new marker search.

## Method review and retained failures

A separate bounded AI method reviewer read the complete root scanner and both
prospective documents without inspecting historical scan results or the new
independent scanner. The reviewer reran all14 built-in controls and reports
866 additional in-memory synthetic oracle cases with no locator/encoding/
suffix/leading-flag discrepancy, plus line/byte/marker-cap and ZIP EOF/hash/
CRC checks. No raw-source pass or external engineering review is claimed.
The866-case review harness was not saved as a new artifact; its reported
outcome is supporting method review, not a separately replayable receipt.
Root's14 controls and the independent reader's fixtures are retained in code
and/or receipts for replay.

Both authors initially made an incorrect synthetic expectation that an
UTF16LE example would yield only one encoded-pattern match. Under the declared
any-byte-alignment search, shifted UTF16BE matches must also be retained.
The scanning algorithms already did so; test expectations were corrected
before any historical source processing. Root's exact failed-control code
is `search_definitions_before_encoding_control_fix.py`, SHA
`6d647d452270ea018c4ebe94df65906d52d5f8bdd07309e5b407c5969b51deac`.
The independent failed fixture receipt and exact earlier code remain in this
unit as `independent-controls-failed01.json`, SHA
`719e04b7bb427dcace85986f17b0dba1ec52ddfa5105bafbb1dab948b12ba24b`,
and `independent_scan_before_control_expectation_fix.py`, SHA
`d3d36bf19c3d7994fb8c977605341f62db5e2cde0b1e86e90c291d8cd29d8d78`.
No historical output was patched to eliminate encoding ambiguity.

The first final-artifact check failed before writing a receipt: its harness
incorrectly expected the earlier failure note to use the source scanner's
`FAIL`/body-list schema. That note actually records
`SYNTHETIC_CONTROL_FAILURE` and `historical_bodies_opened: 0`. The exact failed
checker remains in `verify_artifacts_before_failure_status_fix.py`, SHA
`d54ec8d72c4813c4789f05f0dc86c2afcfd718f0e5544a70b1c4ddbc18239932`.
Only the checker expectation was corrected; no preserved result, failure note
or source changed. This was a harness-schema error, not a scan disagreement.

A first attempt to launch root02 used a mistyped working-directory argument.
Process creation failed before a handle or output existed. Correcting that
path produced the actual root02 receipt. It was not a resumed scan or a
scientific disagreement. Source01 and source02 are terminal; no source process
remains live. Local raw data, main, canonical facts and legal files are unchanged.
The main repository's `tools/validate_record.py` passes its header, issue/fact
link and citation-tag checks. This is record consistency, not engineering
validation. `verify_artifacts.py` checks saved pins, receipt agreement, syntax
and report links; its separately saved receipt records the final documents.

## Frozen pins and replay

| Artifact | SHA256 |
|---|---|
| PROTOCOL.md | dfc4ecbf348066574c6d38b5b087272120f006d35bfb72a1920ff79c14189865 |
| SCAN-CONVENTIONS.md | 06d9f8921be5dd2994dcca74c56ca5104b3aa88be85048a34c1b476ea82c85be |
| search_definitions.py | 3bdbefb2c324671293991070aa5991033a163f6ff13359ab1f276b115c72968a |
| root-01.json | b85f806373294697eb1dc15b2673c5d8d34f81890658c0a76937fec9a55f9b06 |
| root-02.json | e5eea54090c3215534e6c5f4ae776680b673769353fa12240ba2699368f91a49 |
| independent_scan.py | 8c5aee84f2b4b96d4149cd8469902531a31f8d47c59cb2f4f7037657eddfe3ff |
| independent-controls01.json | 3c1797ca32ae37c40361d08ffc3a6c9e9c8e673fa38c2fdf94f8faa0e385ae0a |
| independent-scan01.json | 76a43ff38376979140608c5d368a93ae40bd7c9d55b33a3ec1e87069a6ce5bc7 |
| verify_saved_coverage.py | aa229f6e83cba5b2a214844ad744264beb9f936590299431a8cdc579187ca2ec |
| coverage-check01.json | a71466540ea58ba15e0309ccb2ca7e1cdf1179fc34b153d8c15cf6b50ccd9d5a |
| independent_compare.py | ea10f1aa8193779ba1badc2a691cac150deb55390fa1ccb5b79f99fce768ec74 |
| independent-comparison01.json | d45d1adb5eba7a03f6bf6d0278fd1d94bbfbc5138100176cb3ae0633bce4aa1a |
| independent-comparison-root01.json | 6e3531eb4ac4e2c73c79b1e8d64edb49f3e918d77160122e0343c436328048ef |
| independent-review.md | cbb4cdbf5167b54b329c073aa051d18d92ac48a47b044bc47c8470d0cd41c81f |

Commands below are examples for new, unused output destinations from the
investigation worktree. They are not claims that those future outputs exist.
The source readers enforce their saved input pins and never run source code.

```text
python3 -B research/sherlock-wtc7-investigation/curve-release-search/search_definitions.py --controls
python3 -B research/sherlock-wtc7-investigation/curve-release-search/search_definitions.py --output root-03.json
python3 -B research/sherlock-wtc7-investigation/curve-release-search/independent_scan.py --out independent-scan02.json
python3 -B research/sherlock-wtc7-investigation/curve-release-search/verify_saved_coverage.py --output coverage-check02.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/curve-release-search/independent_compare.py --out independent-comparison-root02.json
```

The coverage verifier reads pinned root01/root02 and the earlier June receipt;
changing its output name does not compare newly generated root03. Such a
comparison requires a separately declared/pinned input update. Saved scientific
results, controls and failed attempts must not be overwritten to obtain a pass.
The independent adapter likewise reads its fixed pinned source/comparison
inputs regardless of the chosen output name. Its replay is a saved-result
and synthetic-control comparison, not a new raw-source scan.
