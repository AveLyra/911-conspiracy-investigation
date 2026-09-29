# Independent bounded interpretation review

2026-09-12. WP3 working research. Review of the member-map report against the frozen source-method work and authorized run05 numeric output/receipt. This is an adversarial interpretation and selected output-consistency check, not an independent reconstruction of the complete historical mesh, a solver run, physical validation, expert structural opinion, or causal ranking.

## Disposition and exact scope

Two material overstatements were identified in the first reviewed report and corrected by the producer. The revised report keeps the selected model-region, supplied-coefficient, cross-family-candidate, and incomplete-properties boundaries explicit. No remaining material interpretation correction is required within the reviewed scope, subject to the independent numerical comparison being completed and documented separately.

The reviewer read the report, selected run05 receipt fields and output records, the previously frozen primary-method work, and the narrowly relevant producer-code paths. Selected checks covered counts, thermal duplicates/envelopes, named column-region joins, the two high-TS exceptions, candidate-list memberships/geometry, and unresolved material references. No compressed source payload was reopened, no historical mesh was recalculated, and no independent-verifier artifact or result comparison was opened. Reading the producer's JSON is an internal-consistency check, not independent corroboration of its raw-input parse.

The sole new file written by this reviewer in this pass is this review. The producer made its own report corrections. Preserved sources, main checkout, frozen method files, run05 output/receipt, canonical records, and outgoing communications were not changed by this reviewer.

## Pins and review history

All investigation paths below are relative to `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/model-member-map/`.

| Artifact / reviewed stage | SHA-256 |
|---|---|
| Initial `report.md`, before the two corrections | `2d78fe5f87228cab1a20346308f590e55d3f118763d9e8aa761d57206504320d` |
| Revised `report.md`, rechecked after the corrections | `ddfafe30680ac25e040f413a4507ec1fb5999c9dbc83154039477312ffbcd40f` |
| `run05/member-map.json` | `92c9e4115b11c6e3b9bd73b59a79ee1cfa467d5cd4a31b24cf3b7c823d2af038` |
| `run05/receipt.json` | `1e78f866dac0f7af24e272b15b85bbb8a409ced5356bdfae87d7e759479ae388` |
| Run05 producer, `map_members.py`, matching receipt and independently retested here | `a4bf444a915bdc088c2735180532ac5d1fd909a1f40eb0daf67b756c8525be35` |
| `method-source-review.md`, unchanged original freeze | `cbea5556de774752fefc82ff5c49ed299bb73ea3fb65af0fcafc7c0e7f24fe5f` |
| `method-followup.md`, unchanged through this review | `b9644b5d489ca315d0535e97bdcb21068dd9f845ba2b44f736b567419577daf0` |

The output hash independently computed in this review matches `receipt.result_sha256`. The receipt records completion, 16 controls with zero failures/errors, and EOF plus successful final source pins for all six inputs. This pass checked those receipts, not a fresh independent hash of all six compressed source files. The run05 output, receipt, and producer hashes remained unchanged across the review.

## Findings raised and closed

### IR-01: a classification counter did not prove four distinct shell vertices

Original report lines 45–46 asserted that all shell records had four distinct vertex IDs. The run05 producer's `element()` diagnostic selects triangle versus quad solely by whether N3 equals N4. An N3-not-equal-N4 count therefore does not establish that N1, N2, N3, and N4 are pairwise distinct.

This was demonstrated against the exact run05 producer hash above using a purely synthetic shell, with nodes 1, 2, and 3 predefined:

```text
*ELEMENT_SHELL_THICKNESS
10,2,1,1,2,3
0.1,0.1,0.1,0.1
*END
```

The shell has only three distinct vertex IDs but the producer reports `quad_shells: 1`. This test establishes a limitation of the diagnostic, not the presence of such a degeneracy in the historical inputs. No actual historical shell defect is inferred.

**Closed by wording correction:** the revised report says no shell uses the recognized N3=N4 pattern and expressly notes that this does not by itself prove four distinct IDs. The aggregate element count remains supported by the typed-record output; the counter was not used as evidence of geometric validity.

### IR-02: low coefficients were bridged to a published initiation premise

Original report lines 101–103 described low selected coefficients as compatible with the published premise that direct severe heating of initiating columns was not the trigger. Even though surrounding text denied historical-temperature proof, that bridge was stronger than this input-only unit supports: duplicate-card resolution, curve/reference/unit conventions, complete physical-member coverage, and the physical trigger are unresolved. A model's selected input values are also not independent evidence for the mechanism that model was constructed to examine.

**Closed by wording correction:** the revised report calls this an input-consistency observation and explicitly denies independent support for published column temperatures or the initiating mechanism. The useful finding survives: supplied coefficients on the selected model-attributed regions are numerically low, while no historical temperature or causal conclusion is promoted.

## Selected report-to-output checks

These checks reproduce comparisons and small aggregations from run05 JSON, not the complete source-to-output calculation.

| Topic | Check and permitted interpretation |
|---|---|
| Mesh records | Output matches 964,067 master shells, 2,042,843 outside-region shells, 3,006,910 total shells, 3,190 explicit beams, 33,364 discrete elements, 2,461 solids, and 3,593,049 unique defined nodes. The prior shell-count overstatement is correctly attributed to the earlier inspector's data-line counter, not an agency discrepancy. |
| Thermal cardinality | Receipt matches 870,201 rows, 628,127 unique node IDs, 242,074 extra rows beyond one per ID, 235,010 repeated-ID nodes, and 170,491 unequal-TS nodes. Every recorded row uses TB=0 and LCID=2. The six threshold figures in the report match the minimum/maximum-per-node summaries. |
| Thermal incidence | Output reports zero thermal IDs without geometry or mesh incidence, 50,023 multi-part thermal nodes, and 683,397 part incidences. The report correctly distinguishes row, unique-node, and shared-part-incidence counts. |
| Column79 model association | Diagnostic keyword line 614, PSID 179, set keyword line 611, listed PID 179, and part-definition line 3527/MID 99/SECID 179 agree with output. Its 952 shells, 873 incident thermal IDs, 63 unequal-TS nodes, coefficient maximum 116.45, and quoted coordinate envelope match. This remains a model-authored region, not drawing authentication or an entire physical-column temperature. |
| Neighboring selected regions | Model labels Column80/81 match PIDs 180/181, each with 873 incident thermal IDs and 63 unequal-TS nodes; maxima 91.30 and 135.62 agree. The table describes supplied thermal assignments, not a completed temperature field for all physical-member nodes. |
| High-TS exceptions | The model-named All Columns set has two per-node maximum coefficients above 300. Node 842747 has supplied extrema 25–574.45 and node 842833 has 25–397.93, each in nine rows. Their diagnostic IDs are 176 and 177, whose normalized model column labels are 76 and 77 respectively. The report correctly retains these exceptions and denies both a unique coefficient and a physical-claim falsification. The set-wide largest per-node minimum is 178.05. |
| Shell candidates | All 1,543 set2 shell IDs are represented in output; the nine quoted part counts match. All 45,152 CaseA shell IDs match across 43 parts, with an empty set2-shell intersection. Their candidate/unused status and unknown CaseA purpose remain explicit. |
| Beam/discrete candidates | Output contains six explicit BEAM matches in PID 98 and 355 distinct candidate IDs matching DISCRETE but not explicit BEAM records, across 19 parts. The candidate EID set exactly equals the set2 IDs unmatched in explicit BEAM records. No exclusivity against every other element family is inferred. These are typed/numeric counterparts, not demonstrated restart deletion semantics. |
| Six explicit beam geometries | The quoted three elevations and paired endpoint ranges agree with targeted output. Orientation node 757586 is a separate field, excluded from endpoint geometry. The report does not convert these locations into historical deletion timing or real structural failure. |
| Properties | All 392 used parts have definitions and a reported section reference. Exactly 23 used parts have no material keyword lookup, covering the 19 MIDs listed in the report. The report's limiting phrase “in the parsed assembly” matters: this is not proof that no definition exists in another historical deck or that any withholding was justified. No substituted constitutive law is inferred. |
| Active assembly | The receipt/output list the expected three active includes, identity coordinate placement for the inspected transform, and no active delete cards. Those are input-configuration facts, not proof of solver execution or reconstruction validity. |

Two optional wording refinements would improve readability without changing the disposition: distinguish “diagnostic ID 176 (model label Column76)” and “diagnostic ID 177 (model label Column77)” in the exception paragraph; and prefer “numeric counterparts” over “meaningful counterparts” in the summary so that ID correspondence is not mistaken for an authenticated cross-family deletion relationship. Similarly, retain the table's incident-thermal-node wording: unassigned mesh nodes are not established to be ambient by this join.

## Code-test history: what was and was not independently retested

| Producer hash / stage | Actual reviewer action and result |
|---|---|
| `d5af076df038fd9020a98f62c913444046a38c8750c2492a09e751c252e99cea` | Earlier bounded audit reproduced silent two-card CSV-solid misinterpretation, repeated deletion-set overwrite, fractional-PSID truncation, and unallowlisted material-keyword retention. These were communicated before accepted historical geometry output. This hash identifies that historical review stage, not the current producer. |
| `010cc49ac61c2053ee0f7fa10baa236f8df6a22769549d5a172f227fd0260cf0` | Earlier corrective retest independently ran 14 controls with zero failures/errors; the original adversarial fixtures rejected safely. Missing/duplicate/extra include graphs and active-deletion status were tested through extracted current guard statements. Identical thermal repeats retained row versus unique-node statistics. Unequal thermal TS was rejected at that stage; the subsequent declared envelope addendum intentionally changed that admission rule, so this earlier rejection is not presented as current behavior. |
| `a4bf444a915bdc088c2735180532ac5d1fd909a1f40eb0daf67b756c8525be35` | In this interpretation pass, independently loaded the exact run05 producer without invoking its historical run, executed its 16 synthetic controls with zero failures/errors, and reproduced the three-distinct-vertex counterexample above. Code hash was unchanged during the test. No whole-mesh rerun or full adversarial re-audit of every later code change is claimed. |

Tests used bundled Python with `PYTHONDONTWRITEBYTECODE=1`; the source was compiled into a non-main namespace, so importing it did not run the production workflow or write an output directory. The quad fixture and control suite were wholly synthetic. The parent's separate existing-output-directory refusal test was reported to this reviewer but was not rerun here and is not counted as this reviewer's test.

## Remaining verification and inference boundary

This reviewer did not compare run04 with run05 or inspect the independent reader's final result, supplemental source pass, or comparison. The report's claims about those stages require their own completed validation records; this interpretation review cannot substitute for them. In particular, two reads by one producer and re-reading its JSON do not constitute an independent source reconstruction.

Within the revised report, the strongest supported claims remain typed input counts, reproduced coefficient multiplicity/envelopes, source-labeled part-region joins, explicitly qualified candidate-ID correspondences, and unresolved references in the parsed assembly. These do not resolve duplicate-card execution, original-drawing correspondence, complete physical-column heating, spring/null-beam deletion behavior, material/run lineage, physical response, or cause. The explicit no-causal-ranking conclusion is appropriate. Main/source preservation and the original method freezes remain intact.
