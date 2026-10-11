# F5/F6 integrated without changing earlier readings

October 8, 2026. Research-only conditional calculation. The four completed
F5/F6 source readings add 159 local graphical windows and 581 explicit
exclusions under the existing rule. All 38 earlier conditional reading objects
remain exactly unchanged. The combined inventory contains 21 local regions,
42 original readings and 13,240 route records across all fourteen pairs:
4,658 conditional windows and 8,582 exclusions.

Use [version 2](run-v2-01.json) and its [identical repeat](run-v2-02.json).
Version 1 is preserved; version 2 restores two earlier inventory qualifications
without changing a number, original reading or exclusion. The [fixed protocol](PROTOCOL.md)
and [wording-only correction](PROTOCOL-V2.md) control this unit.

## New readings and reproducible results

| Original reading | Solid windows | Dash windows | Excluded records | All records |
|---|---:|---:|---:|---:|
| F5 Im3 primary | 53 | 11 | 166 | 230 |
| F5 Im3 peer | 54 | 9 | 167 | 230 |
| F6 Im1 primary | 0 | 16 | 124 | 140 |
| F6 Im1 peer | 0 | 16 | 124 | 140 |

These are reader-route column counts, not independent observations, shared
displacement support or model-agreement rates. The F6 solid zeros mean no
conditional solid window in this target, not zero force or absence of the
solid model. Its separately read solid crest is in Im2; there is no automatic
join to the Im1 broken crest.

The [source batch](../../native-footprint-pass/force56-remainder/report.md)
supplies unchanged F5 Im3 target [310,0,425,88] and F6 Im1 target
[270,55,340,88]. This integration reads no new image pixels. It validates each
original with the frozen source validator, uses the prior copy-only membership
adapter with height 88, and runs the unchanged coordinate calculator with each
strip's own PDF transform. The serialized `force56_peer` identity remains in
both peer originals; it maps only to the previously assigned peer role.

All four new originals, including 50 uncertainty-band records, remain in
`new_source_originals`. The earlier extension's four embedded originals remain
in `prior_source_originals`. Bands are not allocated to a model or erased.
All twelve non-F5/F6 inventory pair objects remain exactly unchanged; F5/F6
append the new regions and narrowly update their residual work descriptions.

Each new conditional window retains two axis-registration alternatives,
yielding 318 coordinate hulls. The 215 base rectangle conversions include
records subsequently excluded by further rules; they are not 215 admitted
windows. Registration variables remain shared across the panel, not independent
per-point errors or calibrated confidence intervals.

## Disagreements and assumptions remain consequential limits

The calculation still assumes Hidentity (reader-local attribution is right),
Hsupport (the generating curve spans the full native column), and Hink0
(its ordinate stays within the selected outer cell edges). Source reading and
arithmetic do not establish these assumptions. No curve is interpolated through
a dash cap, contact, unassigned band, crop boundary or strip seam.

The specifically reviewed disagreements remain visible:

- F5 dash columns 391/403 have primary band references but different peer
  attribution; both readers' rows are excluded, for different reasons.
- F6 dash columns 288/320 have equal selected outer cells but different
  core/status classification. Both are excluded by the local neighbor rule;
  equal outer pixels have not been relabeled complete agreement.
- F6 dash column 325 retains the primary band and peer allocation difference;
  neither becomes an admitted window here.
- F5 solid column 375 retains primary-only bottom clipping. Both readings are
  excluded; the narrower peer fringe is not selected to manufacture admission.

Thus those illustrative disagreements do not change the final inclusion flag
at those exact columns. They still have different recorded reasons and must
not be erased or generalized into evidence that all reader differences are
numerically immaterial. Equal F6 window totals likewise do not prove equal
curves or coordinates.

The strongest objection to treating these results as calibration validation
is decisive: faithfully converting selected raster ink does not verify its
model attribution, pre-raster enclosure, full support, native solver inputs
or physical connection behavior. These are conditional graphical preparations,
not a shell-versus-spring discrepancy finding or a historical-collapse test.

## Independent checking and preserved correction

Two complete version-1 executions agree byte-for-byte. Independent review
caught a narrative omission: the new F5 inventory failed to carry forward the
older Im2/Im4 warning about generic same-column peer references flagging an
unrelated route. Version 2 explicitly restores that warning and F6's earlier
warning that repeated fragment IDs across unknown spans do not prove continuity.
The old annotations and conservative exclusions are unchanged. Both earlier
outputs and their incomplete current-inventory wording remain preserved.

The version-2 copies each contain 7,689,225 bytes, SHA256
`3b9e96e03a0daa37a0c30e8b9e4eb540b0b350a1b3ae832eeb3acc161815dd07`.
All 173 input pins remain unchanged. A separate preservation review verifies
the exact allowed wording/metadata changes and all older objects.

The [independent checker](independent_check.py) and [saved receipt](independent-check.json)
reconstruct every new decision, 215 rectangle conversions and 318 coordinate
hulls using pinned independent helpers, without importing the producer,
its adapter/classifier or mapping functions. It checks all 50 bands and the
complete required dependency union, including 46 source-closure files and
14 JSON nodes. Its 222 controls comprise 49 arithmetic/schema/preservation
controls and 173 individual missing-pin rejection checks—not 222 independent
scientific validations. Root read the implementation and reproduced the entire
saved receipt exactly. The 12,500 old decisions are checked for preservation,
not recalculated in this unit. Earlier source-reading attestations are records,
not independently witnessed human perception.

The producer's 11 integration tests, four version-2 tests, twelve unchanged
calculator tests, twelve reused adapter/wrapper tests and eighteen source
validator tests pass. [Validation](validation.md) records actual commands,
failed preflights, the sandbox-denied initial save, repair scope and receipts.
Tests establish only their stated computational scope.

## Claims and remaining work

| Claim | Evidence layer / limit | What would change it |
|---|---|---|
| The new readings add 159 conditional windows under the declared rule. | Reproduced calculation; directly established within the pinned files and assumptions. | A failed independent decision/coordinate check, altered input or justified protocol revision. |
| Earlier readings and unrelated pairs were preserved. | Exact object, byte-pin and whitelist comparisons; directly established within this version. | A differing earlier object, unpermitted field change or missing dependency. |
| The published graph's full support or physical model is validated. | Not established; readable local fragments do not settle identity, enclosure, continuity or solver applicability. | Source-specific support/identity evidence, selected human checks and separately justified physical validation. |
| These additions favor one collapse mechanism. | Unsupported by this unit. | A validated connection-to-building causal test with competing predictions and historical inputs. |

The current full inventory is `inventory` in the version-2 result. F5 still
has out-of-target Im3, broader Im4, remaining Im2, Im5 origin/tail and join
obligations. F6 still has out-of-target Im1/seam, Im3 irregular shoulder and
rise/descent, Im4 rise/descent, Im5 origin/tail, remaining Im2 and joins. Every
other pair's residual obligations remain unchanged. Qualitative descriptions
are not exact complementary pixel masks and unknown support is not zero.

Next independent task: source-specific recovery or limiting disposition of
the inventoried F6 Im3 shoulder/rise/descent. Read the full remaining-route
inventories/reconciliation, the current versioned inventory and existing Im3
targets/contexts first. Inspect the original source to define a finite target
before new annotation; do not silently expand into completed F5 material.
Use separately frozen readings and independently checked coverage, or report
precisely why the source cannot resolve a portion. This is one next task,
not permission to drop the broader fourteen-pair scope.

All 42 paired human-review slots remain unselected/unaccepted; confirmed axes
and legends stand. No common-domain comparison, physical-model validation,
causal ranking change, accepted Sherlock finding, Faraday activation, legal
promotion, external disclosure, commit or push. The investigation remains
active and incomplete on its dedicated worktree, branch
`research/sherlock-wtc7-investigation`, base `ca1c2233`, with intentional WIP.
