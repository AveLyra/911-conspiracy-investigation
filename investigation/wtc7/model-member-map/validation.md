# Member-map verification record

2026-09-12. Research-only numerical/input verification. No solver, browser
application, human expert assessment, physical validation or legal finding.

## Root calculations actually executed

The system Python lacked NumPy. No package was installed; the already bundled
runtime was located and used. All root producer commands ran from
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation` with
`PYTHONDONTWRITEBYTECODE=1`. The exact launcher was:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/model-member-map/map_members.py --controls
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/model-member-map/map_members.py --output research/sherlock-wtc7-investigation/model-member-map/run06
```

Each historical run used its own new child directory, with local-worktree
write approval; sources and prior run directories were not overwritten.
The final17 synthetic controls pass. They exercise fixed/CSV cards and
required blanks, two-row shell/triangle handling, orientation exclusion,
offsets, shared nodes, duplicates/missing nodes, inactive comments, short or
unsupported records, fractional IDs, unknown-keyword suppression, repeated
set rejection, END boundaries, unequal thermal coefficients, the primary
Type124 material ID schema, separate discrete numeric candidates and
non-mutating aggregate bounds. Choose a new child directory for another
historical rerun; the commands above identify the executions already made.

| Run | Actual terminal result | Retained evidence |
|---|---|---|
| run01 | Exit1: first repeated thermal node, source line53,531 | [Receipt](run01/receipt.json); the original one-value-per-node admission rule was too narrow. |
| run02 | Exit1: unequal repeated TS, after thermal EOF | [Receipt](run02/receipt.json); prompted the declared coefficient-envelope addendum, not scalar resolution. |
| run03 | Exit1: unallowlisted material keyword at master line1,429 | [Receipt](run03/receipt.json); full thermal/list results retained. Primary-manual vocabulary subsequently confirmed Type124. |
| run04 | Exit0, but later independent geometry verification failed;15 controls | [Receipt](run04/receipt.json), [map](run04/member-map.json). |
| run05 | Exit0, but later independent geometry verification failed;16 controls | [Receipt](run05/receipt.json), [map](run05/member-map.json). |
| run06 | Exit0: corrected aggregate ownership;17 controls | [Receipt](run06/receipt.json), [map](run06/member-map.json). |

The earlier failed producer source versions were **not separately archived as
runnable files**. Their receipts retain code hashes and error sites; current
adversarial controls reproduce the relevant failure classes. Do not claim
exact executable replay of every earlier revision from those hashes alone.
Final source and successful result bytes are present and pinned below.

Root compared run04 and run05 after removing only the two declared added
fields (discrete candidates and each diagnostic's high-TS examples): **all
common results are identical**. Both full runs validate all six source
compressed pins and EOF; total streamed uncompressed bytes per complete
six-file read are602,566,715. Source line/size counts and uncompressed hashes
are retained in each receipt. No full coordinate table was written.

That agreement did not catch a shared-array bug. The independent comparison
found three wrong coordinate extrema in diagnostic101's member bounds;
the ordinary part101 bounds and all thermal values were correct. Aggregating
the All Columns set had mutated its first source part's cached array. Run06
uses a copied array and adds a non-mutation control. Root's complete recursive
run05/run06 comparison finds **exactly those three scalar changes** and no
other result differences. The sources were unchanged. Successful execution
of runs04/05 is therefore not successful independent verification.

## Independent verification and source review

The [independent review](verification-review.md) controls its actual coverage,
pre-result core freezes, failed attempts, supplemental checks and final
comparison disposition. Its independent checkpoint was saved before any
producer-result read: [independent-checkpoint01.json](independent-checkpoint01.json),
SHA85e2649cdc2ccc2974f4959e5f19bb8d01f8533e16326bb2647c092252bcbd2e.
The complete independent historical calculation used28 synthetic controls,
two-pass input/mesh handling and181.22s; recorded peak RSS764.125MiB was below
its768MiB gate. It is independent code, not a second physical observation.

Three earlier independent failures are retained in independent-failed01–03:
comma heading parsing, numeric conversion-row admission and an unresolved
material-reference gate. The first receipt is partly reconstructed, with
that limitation documented; later failure receipts were automatic. A later
static review identified incorrect active-delete keyword spellings in the
checkpoint's status guard. That old empty field alone does not independently
prove inactivity; a separate correctly spelled source check is required.
Neither failure nor a fixed reader is evidence of source falsification.

The [primary-method review](method-source-review.md) was frozen before new
map outputs. Its code audit then independently reproduced and checked fixes
for short CSV solids/empty elements, repeated-set overwrite, fractional-PSID
truncation, unallowlisted keyword output and active-graph/END boundaries.
The first correction retest at producer SHA010cc49ac61c2053ee0f7fa10baa236f8df6a22769549d5a172f227fd0260cf0
covered14 controls and those adversarial fixtures; it does not certify all
later source revisions. Later thermal/cross-family rules have their own
controls and independent real-data comparison.

The reviewer, not root, rendered and visually checked the public manual pages
listed in the source reviews. Root read those reviews completely. Manual
semantics and their historical-version limits are distinct from the complete
numeric joins and from a solver implementation test.

## Run05 pins (superseded by the corrective run06)

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | d2c2b77d9801236c0a7d940349412a3b3cc50cc977997b67114ac2aff9afac7c |
| THERMAL-DUPLICATE-ADDENDUM.md | 7433fb5d5b4e151eb70df22b1c40825939d3868842af0ee0ff816c830f236b94 |
| CROSS-FAMILY-ADDENDUM.md | 412641464272c746ac632f5e16e3c9b7b1556b06c02a4598aac67428c39d377f |
| map_members.py | a4bf444a915bdc088c2735180532ac5d1fd909a1f40eb0daf67b756c8525be35 |
| run05/member-map.json | 92c9e4115b11c6e3b9bd73b59a79ee1cfa467d5cd4a31b24cf3b7c823d2af038 |
| run05/receipt.json | 1e78f866dac0f7af24e272b15b85bbb8a409ced5356bdfae87d7e759479ae388 |

## Corrective run06 pins

| Artifact | SHA-256 |
|---|---|
| map_members.py | f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b |
| run06/member-map.json | eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e |
| run06/receipt.json | 4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d |

Before the subsequent alias fix, root rechecked the run05 producer/result hashes against their receipt and
parsed both current Python files with `ast.parse`. The record validator ran
read-only on main:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_record.py --strict
```

It passed headers, issue↔fact linkage and citation tags. That does not validate
engineering, grant disclosure authority or promote research into case facts.
The targeted JSON field `centroid` is the arithmetic mean of unique endpoint/
vertex coordinates, not a section or mass centroid. `quad_shells` only records
N3≠N4, not pairwise uniqueness of all four vertex IDs; the report was narrowed
following the [interpretation review](interpretation-review.md). Low selected
TS coefficients likewise remain input consistency, not independent support
for an initiating mechanism.

Root reran the independent reader's28 controls with `--selftest`: PASS.
Reusing the exact existing run05 output directory was rejected before source
reading or output writes with exit2 / `output_must_be_new_child`; both existing
result/receipt hashes remained unchanged. Narrow tracked-navigation
`git diff --check` passed. Final comparison checks are recorded below.
No commit, push or external transfer.

## Completed final comparison

The independent consumer and root's separate rerun both pass for corrected
run06:42,492 exact integer scalars and46,286 floating scalars (88,778 numeric
values), maximum absolute difference0.0 under the declared1e-8 tolerance.
They cover392 element-bearing parts against459 definitions,83 diagnostics,
85part sets,1,543 shell/6explicit-beam/355discrete candidate geometries,
45,152CaseA matches and43part bounds, and4high-TS example occurrences at
2unique nodes. Both also performed fresh, bounded header scans reaching EOF
on all6sources, checking heading-hash recipes, active/commented delete cards
and compressed/uncompressed source pins. The original independent checkpoint
and supplemental result remain unchanged; the consumer did not borrow root
coordinates to fill missing independent fields.

Root's actual rerun command was:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/model-member-map/verify_member_map.py --verify --run run06 --output verification-root01.json
```

It exited0. The two verification receipts differ **only in their command
field**, not results, pins or coverage. The earlier failed comparison remains
separate; it is not overwritten by the corrected result.

| Artifact | SHA-256 |
|---|---|
| verify_member_map.py, final consumer | de7ee2aa5f4a2aedd4a9446561322aa5e14e688d1c72a57aa96e593df1f148cc |
| independent-supplement01.json | 7803e6b2d82b852d37c656e44bbf0c04b4d109f1a1ac03fb97a87ab8816a8fc8 |
| comparison-failed01.json | 64e2a35832164173c5130e15975d726cc74a58df89648b893e03eaf51ad46107 |
| verification01.json | 3d4f810181abc5e7aa3ea6b2e60b6b54c330d85a8a12bfd851e1280a7a4c348c |
| verification-root01.json | c1d3fd6e24e1303da8b77bbfa4cc5da3546fab9bfc3c47af049beff4b85ad9a8 |

The final17 root controls,28 independent control groups and complete numeric
comparison are different checks, not confidence percentages or additional event
observations. The prior interpretation review examined the earlier report
and selected run05 values; its two wording corrections remain incorporated.
The later report revision adds the alias-failure/correction history and links
run06, whose only numeric changes from run05 are the three independently
identified diagnostic101 bounds. Physical, solver-policy and historical
identification limits are not closed by this numerical agreement.

Final integration checks:9Markdown files /29local links, all targets present;
no unexpected trailing whitespace;2current Python AST parses; final producer,
result and verifier hashes match the successful receipts. Narrow tracked
navigation diff checks pass. The independent final report review is terminal
with no material correction (review SHAa17a8ea385d22e7e2d998bf17edd9fcf9fcdbdda8044004b02acf7e4d1872dd1).
Root inspected verifier entry/import interfaces and ran its controls/consumer;
no complete root line-by-line audit of the independent verifier is claimed.
All calculation sessions and bounded reviews are terminal. The comprehensive
investigation goal remains active, and all research changes are uncommitted.
