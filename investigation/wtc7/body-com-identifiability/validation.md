# Verification, review and continuation

2026-09-24. Research-only mathematical/dependency audit. No historical force
or body/COM bound was measured. The preceding turn is progress: it supplied
the independently checked finite-interval constraint that this unit tests.

## Reproducible synthetic calculation

Actual producer commands, from the investigation worktree, both exit 0:

```text
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/body-com-identifiability/calculate.py --out run01
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/body-com-identifiability/calculate.py --out run02
```

Each produces eight hidden-mass cases, eight rigid-body cases and two envelope
cases. Controls include24 proper-pose recoveries,144 pair-distance checks,
six affine-removal controls, all sixteen envelope vertices,128 fixed-positive-
mass corner mixtures, and five invalid-input rejections. The producer is
exact rational arithmetic using only Python's standard library. Its create-
only run directories refuse overwrite; the commands above are execution
records, not instructions to replace saved output.

The independent implementation and its two executions are documented in
[independent-review.md](independent-review.md). It froze its derivation and
outputs before seeing producer code/results, then checked450 exact equalities
across all eighteen cases, and independently enumerated the producer's larger
mass-mixture grid. The independent frozen grid and producer grid have different
control coverage; the review preserves that difference. No independent
historical experiment or human engineering review is implied.

Root fully read both implementations and ran a read-only
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B -` replay, loading each script
with `runpy.run_path(..., run_name='verify_only')`. Calling producer `build()`
and oracle `fixtures()`, followed by their respective serialization functions,
exactly reproduced both saved JSON results, including control results.
Root separately compared284 fields or nested structures across the eight
hidden, eight rigid and two envelope cases. It checked exact byte identity
for both products across each implementation's two runs, plus the producer's
four unchanged dependency pins. Observed exit 0:

```json
{"read_only_replay_both":"PASS","matched_fields_or_nested_structures":284,"hidden_cases":8,"rigid_cases":8,"envelopes":2,"repeated_products_identical":4,"producer_inputs_unchanged":4,"oracle_controls":{"assertion_checks":648,"envelope_cases":2,"expected_value_errors":29,"hidden_cases":8,"rigid_cases":8}}
```

No numerical failure was observed in the producer runs, independent runs or
root replay. The proper-pose routines test exact synthetic known geometry;
they are not noisy-image pose estimators. No browser/UI, solver, new media
decode, library installation or network call was needed.

## Pins and review dispositions

| Artifact | SHA256 |
|---|---|
| Prospective protocol, including fixture declaration | `56acfc527feb2ac817d64ba582d46edddec7b853411eaed00d7b3322434d9553` |
| Producer code | `93d38d3ef5527893515d809551f85e276d3b04482bb5a6c75613c6380b9e5ee7` |
| Producer results, both runs | `1e210ed55cfbaa265fc621b1977ec54b6b04b3db217a8f6ce6669f74103de7f2` |
| Producer receipt | `86c97efe9d07b42d36aadf04e879436a085ce90bdd2bcd8ef2df07845c624055` |
| Independent code | `c39ef5492438accfae8ff99f3c1d5dee322cff92d9b92e08238dbdd4eae758b2` |
| Independent results, both runs | `dd23348b694b5a4d2625a5c82fcdc7c525cdddc6d0a75af8f5b97f8354333934` |
| Final reviewed report | `b36ca1f664b97a4b6a0127d2b67a24e3c26d9896df86dfb31938a0292ad017f1` |
| Bounded source review | `7b6d827bda977119e95d011c3c36cd1ac7a8c06bcc1e8914478b42fb16a67860` |
| Completed independent mathematical review | `efc787af4df245b96525d8ccac425b635b8c49202cdbc211972302c159a7c4fb` |

The mathematical reviewer requested two substantive precision edits: the
examples are not **demonstrations** of physically feasible histories (rather
than proven infeasible histories), and passing a loose envelope means **not
excluded**, not structurally possible. The source reviewer additionally
qualified B/eta as departure from an affine baseline, not absolute separation.
All are incorporated; the mathematical reviewer reread the final assembled
report at the hash above, with no remaining blocking issue within its scope.
It also corrected its own baseline/clearance wording. No result changed.

The separate source reader rechecked both saved documents against its bounded
prior reading. It confirmed Camera2/Camera3 separation, static-versus-dynamic
geometry, located-versus-unexported mass cards, and valid attached-body
accounting. It did not independently verify root's additional Camera3 endpoint
and conditional-trajectory source findings. Its inspected report version
preceded the three minor final qualifications; the final math reader covers
the assembled wording, not a new primary-source read.

## Current-source checks and preservation

Root repeated numeric-field queries on the existing member-map and material-
crosswalk derivatives and checked their hashes against the source review.
An inline `python3 -B -` verification recomputed all392 static bounds' union,
four mass-part solid counts and PART lines, four SRC-119 MAT keyword lines,
and absence of those four IDs from the **selected numeric export** only.
Observed exit 0:

```json
{"existing_derivative_hashes_match":2,"parts_with_static_bounds":392,"four_mass_parts_and_definition_lines":"PASS","numeric_mass_cards_unexported_in_selected_materials":true,"phase_resolved_envelope_inferred":false}
```

This is not a raw-deck replay. The source-review file preserves exact queried
fields and upstream provenance. No new PDF pages, actual video frames or raw
model cards were inspected. Main AGENTS, WORKFLOW, START-HERE and charter
SHA256 values matched the start-of-turn pins on a fresh final check.
No main/raw/legal/canonical or accepted Sherlock/Faraday record was changed.

## State and smallest next independent task

Branch `research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`, existing dedicated worktree.
Intentional research WIP remains uncommitted, unmerged and unpublished.
The full investigation remains active. This bounded dependency audit is
completed with a missing historical geometry/COM join, not a cause result.

Next full-reasoning task: a bounded **local drawing/attachment locator** for
the original north elevation and lower-west louver-bank detail already named
in the Camera3 source review. Read that review's exact prior search coverage
first; inspect current source/drawing inventories and relevant held primary
descriptions without replaying exhausted routes. Declare roots, terms and
archive/representation coverage before searching. Acceptance is an exact
drawing/sheet/revision/feature locator or a documented bounded non-location,
not global absence. If located, check whether it actually identifies visible
material, depth, attachment and assembly extent; a similar elevation picture
alone is not the join. Preserve camera/time/calibration limits and user-only
human/expert review. Do not treat extracting a static mass total as recovering
dynamic COM motion. No outreach, fees, new FOIA request or publication.
