# Independent frozen-observation recomputation

2026-09-24. This check was performed only after root confirmed both complete
25-image records were frozen. It closes the historical-comparison and
pair-carry-forward steps left pending in `../technical-review.md`; that earlier
report and all frozen observations, producer code and receipts remain intact.

## Outcome

The independently calculated full 25-image and pair 2-image comparisons match
both respective producer runs exactly, including every saved axis value,
rectangle list and descriptive difference. Each pair of producer runs is
also byte-identical. Both original pair rows for each reviewer are identical
as complete JSON objects in that reviewer's full record. Only the enclosing
pair/full provenance namespace differs, as the declared pair-key note permits.

The checker independently validated all four frozen records, their exact
protocol/key pins, unique membership, per-asset schema, enums, finite
nonboolean coordinates, bounds, reason strings and target/smoke consistency.
All 25 selected JPEG byte hashes and byte counts were rechecked. Their native
dimensions matched both the keys and an independent standard-library JPEG
SOF header parser, without decoding pixels. The two keys have exactly matching
pair entries. All input hashes were checked again after the calculation.

`independent_observation_check.py` imports only the Python standard library.
It imports or executes neither `compare.py` nor the batch 2 implementation.
Those producer files are hashed only, and their reported code pins are
checked. The independent checker deliberately implements the same disclosed
schema and output meaning; implementation independence does not create a new
visual observation or establish the annotators' accuracy.

## Preserved comparisons

Left means the frozen root record; right means the frozen observer record.
The following are counts of saved descriptive comparisons across 25 image
representations, not counts of fires, rooms, windows or independent exposures.

| Axis | Same | Different |
| --- | ---: | ---: |
| Target evaluability | 25 | 0 |
| Flame-like feature identified | 22 | 3 |
| Ambiguous glow identified | 25 | 0 |
| Smoke status | 21 | 4 |
| Bounded nondetection region identified | 23 | 2 |

Flame-like presence differs for `A-c9a2677a3838`, `A-d966352be998` and
`A-e9627d66e7e4`. Smoke status differs for `A-79c9dd7424ec`,
`A-7a19d98a72c7`, `A-c3409ebb7a81` and `A-c9a2677a3838`. Bounded
nondetection-region presence differs for `A-088afe86559c` and
`A-d966352be998`. The pair has one smoke-status difference and no other
presence/evaluability-axis difference.

The root and observer respectively identify flame-like features in 9 and 12
representations, ambiguous glow in 22 and 22, and bounded nondetection regions
in 15 and 15. The equal nondetection totals conceal two different memberships;
the full per-image records preserve that distinction. A false presence flag
means that the reviewer did not identify the specified feature or region; it
does not assert absence of fire or absence of an unobserved interior process.

Matching presence labels do not mean matching geometry or descriptions.
The complete target rectangle differs on 21 images, luminous-feature lists
on 23, nondetection-region lists on 16 and overlay lists on 25. Complete smoke
objects, target reasons and visibility-limit lists differ on all 25. These
are exact saved-JSON differences, without spatial matching, averaging,
consensus edits or an assumption that every wording difference is a material
visual disagreement. `comparisons.json` retains both values for every
observation field and every axis, including nulls and empty lists.

## Actual verification

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/fire-coverage-batch3`.
Python executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

```text
python3 -B -m unittest -v test_independent_observation_check
  7 tests passed. Final run: 0.002 seconds.

python3 -B independent_observation_check.py \
  --full-runs comparison-full01.json comparison-full02.json \
  --pair-runs comparison-pair01.json comparison-pair02.json \
  --out independent-observation-check01
  Exit 0; accepted true; full 25; pair 2;
  both reviewers' pair rows unchanged;
  both full runs and both pair runs byte-identical and independently matched.
```

Synthetic controls cover exact 2/25 membership, duplicate/unknown IDs, source
and schema failures, booleans/nonfinite/out-of-bounds coordinates, empty
reasons, target/null and smoke contradictions, coexistence of all five axes,
unchanged pair rows, duplicate/nonfinite JSON, independent JPEG dimensions,
and rejection of a deliberately altered producer comparison. No historical
failure occurred in this check. The earlier rejected tile geometry remains
rejected and was not retried or relaxed here.

## Receipt pins and remaining limits

| Artifact | SHA-256 |
| --- | --- |
| Independent comparison output | `2b4a91da7eb6467462610c75b375d3e408f0dbd6b9457786c6ffb7966abeabdc` |
| Independent receipt | `d3202ef648e9368e9b3ad0f0a70858b1e7bf97648c3e94ba3139ab79e8ba12d6` |
| Each producer full run | `9c78daeb0f7c81c71b7031095c3cbe2065bea142d369c2f75f76b83bf4664952` |
| Each producer pair run | `f2fae74a01b5abc2f956cbc71b95d2610895dd679f0b88b7c8d42a0d9abf68fa` |

The machine receipt records the exact four frozen observation hashes, both
keys, protocol and addendum hashes, checker/test hashes, all JPEG hashes,
producer-run hashes and the producer code pins. The output directory was
created fresh and both output files were created exclusively. No prior files
were rewritten.

This verifies the recorded computation and preservation, not whether either
observer's image interpretation is correct. Reasons are checked for presence,
not for substantive optical adequacy. No image pixels, captions or source
attributions were viewed here. There is no new severity estimate, inferred
temperature, continuous spread history, causal ranking or validation of
underlying camera authenticity. Figure association, dependent exposures and
clock limits remain matters for the separate source review and coverage join.
