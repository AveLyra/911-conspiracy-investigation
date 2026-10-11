# CBS comparison preparation record

2026-10-04 UTC. Research method preparation, not a historical result.

The existing Peskin masked-Pearson kernel is reusable; its hard-coded historical
runner and 720 by 478 target masks are not. Main CRW provides provenance and
derivatives, not an exact-frame registration engine. A separate read-only
inventory found these distinctions; no existing source code was changed.

Root reopened the two complete native reference JPEGs once each after writing
the prospective protocol, then saved `regions.json` before new candidate views
or any historical score. This is a new, disclosed viewing, not a silent change
to the earlier eight-clip screen's frozen descriptions. The region file's
initial SHA-256 is
`5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694`.

## Preexecution validity correction

The initial protocol (SHA-256
`38df9ee7cd401a343b9940f1fa93ef812f0427ab46298333c841809b843f8b22`)
said: “Use nearest sampling for binary validity and bilinear sampling for image
values.” Root and the adapter author independently noted that this can allow
excluded banner pixels to contribute through interpolation near the boundary.
Before any historical scoring, root added a two-working-row guard at initial
normalization and a two-row guard above the scaled validity boundary, plus an
explicit synthetic invariance test over all declared parities and scales.
The initial wording alone is not a sufficient no-contamination guarantee.
No result was tuned, no region changed and no old experiment was rewritten.

## Fresh arithmetic controls

Using the bundled Python 3.12.14 runtime, root ran:

```text
python3 -B research/sherlock-wtc7-investigation/peskin-figure-correspondence/direct_oracle.py --controls --output research/sherlock-wtc7-investigation/cbs-frame-correspondence/direct-controls01.json
python3 -B research/sherlock-wtc7-investigation/peskin-figure-correspondence/fixtures/compare_producer01.py --output research/sherlock-wtc7-investigation/cbs-frame-correspondence/core-comparison01.json
```

Here `python3` is
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`;
working directory is the investigation worktree. Both commands exited zero.
The independent direct oracle passed 16 controls and 3030 random offsets.
The producer comparison passed 73 checks over 71 surfaces and 1593 offsets;
maximum observed score difference was about 1.14e-13. The saved receipts retain
code pins and exact invocation arguments. These results do not verify new
mask mapping, field handling, interpolation exclusion or historical matching.
Root also imported the pinned kernel without its historical runner and called
`controls(out)` with the fresh `core-controls01` directory. Its eleven controls
passed (exit zero); `core-controls01/summary.json` has SHA-256
`175019b3d873ea8632ea14dd4cec1fd4dc35b6c3f9557dab7503491d4e7ffcc7`.

The direct oracle accepts a positive variance equal to its chosen floor; the
historical producer rejects equality. The new protocol explicitly keeps the
producer's strict greater-than rule. The tested integer-valued synthetic core
comparisons do not erase that boundary distinction. Adapter controls and a
separate preexecution method critique remain required.

The preexecution reviewer also requested explicit ranking groups. Before
scoring, root clarified paired-only visual shortlists and separate near-best
sets for each target, source clip, representation and metric. All-invalid
groups must retain an empty set and reason. No scores were pooled or inspected
to make that choice. Protocol after these two corrections: SHA-256
`4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa`.

The separate [pre-score critique](method-review.md) conditionally accepted this
bounded candidate-only pilot; it did not accept an implementation or historical
result. Its SHA-256 is
`6d8c734f5bd3c68599cc4db07100c73841c415e047b980b4cb055b14ad3d293d`.

## Implementation review before execution

Root read the initial 391-line adapter completely and caught an incorrect
nearest-rounding formula in its expected sample-index check. The inherited
sampling contract requires the first PTS at or after each rational target.
For Clip 7, the incorrect formula would demand 704, 845 and 986 instead of the
preserved 705, 846 and 987. This was identified before any historical scoring
and would have caused refusal, not a valid new frame selection. Root requested
the ceiling rule plus explicit regression tests against both frozen nine-frame
lists. There is no historical failed run or score to claim for this code-review
finding. Passing the old controls alone would not validate this new adapter.
The adapter author reported independently finding the same defect while
inspecting the source schema. Root's subsequent read confirms the ceiling
expression is now present. The prior source receipts do not supply a separate
probe-output hash; the adapter therefore records a fresh probe dependency hash
and checks its semantic joins to pinned manifests. That is not retroactive
authentication of the old probe bytes.
