# Clip 7 implementation review

2026-10-04. Independent reviewer: `one_pixel_check`. Research-only,
prehistorical implementation/control review; not acceptance of historical
results, image correspondence, physical measurements or a collapse explanation.

## Disposition and scope

The final version below is adequate for the bounded, serial execution declared
in [PLAN.md](PLAN.md), SHA-256
`0404e0a819e7d8392ad3a320a4cb018ecef02c4d9d3f72337d4b3d1d131f6d70`.
Both corrected author and independent root suites have actually completed.
The reviewer found no remaining blocking implementation defect within this
scope. This does not authorize new parameters, retries, parallel jobs, larger
limits, partial-rank inspection, image viewing or scientific promotion.

Read the complete implementation, tests, plan and method review, relevant
parent implementation/tests, and the direct-score checker. No historical job,
decoder, matcher or image viewer was executed by this reviewer. No implementation,
source, legal/main file or previous record was changed. This review is the
reviewer's only new file in this unit.

## Implementation findings

- The source population is exactly indices 0–1127: seventeen 63-frame chunks
  and a final 57-frame chunk, each in full/even/odd modes. This gives 3384
  comparisons per pass and 6768 across both passes; all nine pilot frames and
  27 paired pilot comparisons remain required. The 6768-call wiring control
  mocks numerical registration; it is not a historical numerical validation.
- The sampler uses the already reviewed V2 configuration. A read-only comparison
  found all 17 sampler function code objects unchanged from the parent. No new
  parser relaxation or normalization of old refused logs was introduced. The
  numerical matcher, masks, search lattice, tie rules, scoring and pilot/core
  dependencies remain pinned; changing the population/paired reference is not
  represented as an independent numerical implementation.
- Each chunk must include the canonical fresh required-input map, including the
  source and fixed Figure 142 reference. Every supplied map is canonicalized and
  conflict-checked before merging. Both passes share one dependency map. Every
  unique input is checked before acceptance and again at the end; deduplication
  does not remove the required per-chunk provenance check.
- `run.py` admits exactly 39 jobs in the declared order, requires completed
  predecessor receipts and unchanged control/code pins, and refuses already
  attempted current/future jobs. Outputs and supervisor records are create-only.
  Only this runner is the authorized historical entry point; the inherited
  standalone supervisor CLI is not a substitute.
- The supervisor retains the parent's process-group cleanup, live-descendant
  detection, bounded permission-error handling and truthful failure receipts.
  AST comparisons found its size/save/group-existence/stop-group functions
  unchanged. The extension parameterizes the lane limits without weakening
  cleanup. Every job has a 240-second deadline. Job caps/reserves are extraction
  1280/64 MiB, scoring 256/32 MiB and aggregation 64/2 MiB; the inclusive lane
  cap/reserve is 3584/128 MiB with a continuing 4096 MiB free-space floor.
- The supplementary direct checker rejects optimized Python before relying on
  assertions, requires a completed aggregate, preserves input/end checks, and
  checks declared retained transforms with direct sums. It does not independently
  recompute every saved surface cell. Its historical main was not run here.

## Issues found and preserved history

Before historical execution, the review required actual aggregate-orchestration
controls for a cross-pass dependency conflict and a mutation rejected at the
final recheck. These were added without changing numerical registration.

Author then identified, and this reviewer confirmed, that merging supplied maps
alone did not reject an omitted required source entry. The narrowly approved
repair requires the fresh map in every chunk, explicitly pins reference 142,
and tests missing source and missing reference separately. The earlier
`controls-author01` 110-pass record remains preserved; it is not a pass for the
corrected version and now fails its stale-control gate.

Root's `controls-root01` was interrupted with exit 1, not a whole-suite pass.
Its three saved completed groups contain 14/25/16 passing tests, and there is
no whole-suite summary. Root's saved [execution record](execution.md) attributes
the failure to a shared-lane directory walk encountering a temporary author02
file during concurrent synthetic cleanup (`FileNotFoundError`, tool `0e971e`).
This reviewer verified the partial records and absent summary, not that terminal
traceback independently. No ignore-missing change or relaxed limit followed.
The unchanged code was subsequently rerun serially as `controls-root02`.

## Actual verification

All commands used the bundled Python 3.12.14 with `-B`; NumPy 2.3.5 and Pillow
12.3.0 are recorded in both accepted summaries. The full-suite invocation was
`test_controls.py --output <absolute path to the named controls directory>`.
The reviewer did not duplicate the full suite; author and root each ran it.

| Saved run | Actual result | Summary SHA-256 |
| --- | --- | --- |
| controls-author02 | 111 passed; terminal 41693, final `db4c2a`, exit 0 | `126c07192b8033508cbdb22aa7295bbcdf954dc328f41f8c93cd20fc0af96ffc` |
| controls-root02 | 111 passed; terminal 8161, final `c3da0d`, exit 0 | `3c656d64ba2d435c86e8db240a2e52b899d94f653d6d75416e6eb9988ce10641` |

Each population is sampler 14, pilot 25, inherited supervisor 16, Clip 7
supervisor 13, dense 33 and version 10, with no failures, errors or skips.
Synthetic sampler decoding and process-supervision tests actually ran; mocked
aggregate wiring and numerical registration are distinguished in the tests.

Reviewer stdout-only `python3 -B -` checks, exit 0:

- `a5f5fc`: code-object/AST reuse, exact chunk population, 39 job specifications,
  dependency identities and then-current loaded suite counts; no tests run.
- `c4cbcb`: author02 summary/group equality, 111 actual passing log entries,
  six log hashes, all 18 dependency hashes, resource samples and current gate
  (34 pins). Prior author01 plus five mutated control variants refused. Eighteen
  synthetic supervisor receipts had no `shutdown_error`.
- `34f4e7`: the same saved-result/hash/resource checks for root02, exactly 111
  passing log entries and 34 accepted gate pins; eighteen synthetic supervisor
  receipts had no `shutdown_error`. Verified root01's partial groups and absent
  final summary. None of the 39 historical product or supervisor directories
  existed at this check.

These checks inspect local records and invoke the control gate, not historical
extraction/scoring. All saved group-boundary samples met the lane/free-space
limits; they are samples, not a continuous resource trace.

## Frozen implementation identities

| File | SHA-256 |
| --- | --- |
| dense.py | `2828059bb3392c335c0d1ea71e7b0727a2e41b9a50db63df260a65a142e8bdb9` |
| test_dense.py | `d55990270cd7a6f4954dde582997ad2479f1c7fd89093eee3a1f707e6b634def` |
| run.py | `dbce88d6a896dd5e3ca5b1c2024f0fac1d52a09286766612463b3a873b1ab95e` |
| guard.py | `1ef728c8ee1827b6ad5d71a2e386b44f501f1fabba9a2ef16bee74fcb68892cc` |
| test_guard.py | `680aef3af6d66f74eaecd914c8033e5ba452b60acb1b803f11de055922334357` |
| test_controls.py | `7983df94692181091b763865d2ee402208f9cf4bb800ad3373a1e9ad38d89dc6` |
| verify_scores.py | `09292f9e1866ba228a83bd47396a3af75949fb15898bb4e7839537d8e136027d` |

## Remaining limits

The strongest operational limitation is that sampled resource supervision is
not an OS-enforced quota: output may grow between polls and during shutdown.
Reserves reduce that risk but do not guarantee no overshoot, and external
termination can prevent a final receipt. Missing, failed or mismatched records
must stop the lane. The concurrent synthetic-run failure also shows why the
shared lane must be used serially, including control runs that create or remove
fixtures. Successful controls establish bounded implementation behavior, not
successful historical execution, source authenticity or scientific causation.
