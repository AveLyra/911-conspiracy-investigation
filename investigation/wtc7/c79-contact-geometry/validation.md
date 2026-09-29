# Column 79 contact-geometry validation record

September 13, 2026. Working record: input extraction, failed floating
reproduction, exact arithmetic and its cross-implementation checks are
complete. The contact-to-damage join, independent comparison and fresh root
consumer also pass. Final report review is complete; version-specific
artifact/guard coverage is recorded below and in its separate receipts.
No overall investigation or physical validation is claimed.

## Authority and state

Worktree `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. Raw/main/legal/canonical inputs are
read-only dependencies. This unit and earlier work are intentionally
uncommitted; no merge, commit or push has occurred. The main checkout has
unrelated legal changes, left untouched.

Current AGENTS/WORKFLOW/START-HERE and the research charter control. The
source-of-truth, evidence-audit, repository orchestration, development-
verification, PDF and context-handoff skills govern their respective tasks.
This is a Markdown research artifact, not a PDF-authoring operation. No UI
behavior changed and no browser validation was applicable. The separate
public-source PDF reviews used complete rendered pages, not text hits alone.

## Source pins and coverage

The three admitted compressed geometry inputs remain at their original
supplementary-production paths. Their stream totals and individual pins
are in [control-method-review.md](control-method-review.md), the two first-
stage receipts and independent extraction. A hash establishes integrity
relative to those bytes, not original-run or 2010-release authentication.

| Source | Compressed SHA-256 | Complete decompressed byte count |
|---|---|---:|
| SRC119 | 2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7 | 508,372 |
| SRC120 | c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59 | 232,959,541 |
| SRC121 | f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d | 333,947,423 |

Each root first-stage run made two full passes over all three streams. The
independent stage made three full passes over all three. The separately
written control reader made one additional full pass over each. All saved
EOF, size, line-count and decompressed-hash receipts match their declared
pins. Later comparisons and geometric calculations consume frozen outputs;
they are not new raw-source reconstructions. No thermal stream was decoded
for the first-stage geometry extraction, and no deletion or solver code ran.

## First-stage extraction and exact comparison

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea |
| INDEPENDENT-STAGE-PLAN.md | 4b616ea1a57727c7b0ac034cdc55bdb25fc656d355ef805907407bcc11cf506f |
| extract_geometry.py | 67c0074e4f873f3b4fb50df77ee740d6c5773b31f0ab23a0c750bb4a0ec1f525 |
| verify_geometry.py | a1e60b3625d00f266e3f31c983ffcbe4b3843a1c38087ccf3924e9f006ec8a06 |
| stage-root01.json | deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963 |
| stage-root02.json | 0a9ff75f944ffa9238c56e01fc234e199f1ca65faccfbed98217c4bd53152a33 |
| stage-root01.npz and stage-root02.npz | 2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf |
| independent-stage01.json | ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd |
| independent-stage01.npz | fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5 |
| compare_geometry.py | 93d751c87eeae5e1e93609f2d8e4719af1de830a84a82f833d66048ac40efc2a |
| comparison01.json | 3aea77662c5eb6587694e56296809394e9fae666ce4c435f540b10275f682028 |
| comparison-root01.json | 9cfe8c0873dc1b79e5279b19ea2a91107204af060aac09ba570c66123ee8c269 |

Root and independent implementations reused their own distinct prior numeric
readers; neither reuse is an independent physical witness. Root code was
fixed before receiving the new independent result summaries, which arrived
while root's first pass was live. No adaptation followed those summaries.
The independent arrays froze before root code/result access. Exact comparison
then used an explicitly documented normalization adapter.

All 11 common arrays, 742 master records and 119 common part references match.
The 15,083,434 numeric-array-slot count includes both root repeats and an
internal corner-count check; it is not that many independent observations.
Matching NaN positions are required. All 27 independent and 11 root extraction
controls reran, as did 17 comparison mutation controls. Root's fresh consumer
completed PASS; differences from the first comparison receipt are only its
command paths/output name, elapsed time and peak memory. Source/dependency
pins, controls and substantive results match.

Excluded from dual verification: full root SECTION_SHELL property cards
beyond the first ID/source locator; heading hashes; the root-only global
ground-reference counter; and several independently retained full element
and orientation arrays beyond the common schema. The independent control
block later received a separate bounded 16-field/source-line comparison in
[proximity-implementation-review.md](proximity-implementation-review.md).

### Preserved ground-reference preflight failure

The initial root controls failed on a synthetic discrete spring/damper N2=0
ground reference before the historical geometry pass. The preserved
`extract_geometry-before-ground-review.py` has SHA-256
`bea73d76a92ac138a88ab2dd7f712df5a2c35145a057f2fce7439c4c1da18305`.
The [failure note](preflight-failed01.json) is an authored record of observed
tool results, not an original machine receipt. The
[ground addendum](GROUND-REFERENCE-ADDENDUM.md) records the primary-manual
rule and corrected exclusion of ground zero from physical node geometry.
Actual streams had zero such ground records in the root counter. This was
our parser preflight failure, not a source-model defect.

## Floating geometric diagnostic

The final prospective geometric method and implementation clarification are
pinned to `73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e`
and `ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd`.
Their definitions and exact-arithmetic mathematical review remain unchanged.

| Artifact | SHA-256 |
|---|---|
| proximity.py | 111f5e99646e05096838997d9aa4cddc0574d9767f784b860cb04dbcf52f0bb2 |
| proximity-root01.json | d2201fcd1f0c36f3240a32813b01ec1c8b90f44d019ac0cbb93ce54a99e5f6cc |
| proximity-root02.json | 962f378986ad225276c1d1d8f796218b3ce729d1079ce65de5cb3664f615601b |
| proximity-root01.npz and proximity-root02.npz | b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca |
| verify_proximity.py | cd3559d84e332ea7a3877a15fe8ef0e7ec8717b9cc2c73746d610e3364a31d9e |
| independent-proximity01.json | cc50ea1607ee4875610fdd7cdae62e22dc5e423eb776842849f1e6199217543c |
| independent-proximity01.npz | 26a9c9421e37c38e96e7568bb0521763b0cd0e621a12e7e101f8a9b411a2bef5 |
| compare_proximity.py | c5bf5392d85c3abb9d05ee499e97f58d2b4dbce94a401096d35b61ff595c10e2 |
| proximity-comparison01.json | 17c43652a02a8685d12e9ff0f49d9548678989a5a8157ca2f2fc39202e21221a |
| proximity-comparison-root01.json | 3ae497db581bf158d24b3e2a26498eb8180017ec5bf5ab52db0cea043c677e88 |
| summarize_proximity.py | 4009b0c5c87bdc4ddf585b956814fd39ff828551519b408b9402b729bfac7f70 |
| proximity-summary01.json | b722afe6144e27a6b74ada24c2922f24deb8f8b79d7e0a9cc751580e8bcc3d8f |

The two root runs completed with 15 controls each in approximately 16.88
and 16.97 seconds; their complete NPZ archives are byte-identical. The
independent implementation used a Voronoi-region triangle-distance method
rather than root's plane/edge method, passed 35 controls and completed in
approximately 17.43 seconds. Each completed run produced 11,292 admitted
rows and retained complete masks for all 338,488,050 combinations. These
are completed computations, not a statement that their classes agree.

Both complete comparisons return **FAIL_EXACT_REPRODUCTION**, expected exit1,
with all discrepancies retained. This is a completed failing comparison,
not an interrupted computation. All 26 root arrays are mapped; numerical
fields agree within the declared unit-scaled comparison tolerances. Exact
IDs, masks, common part joins and geometry warning flags agree. However,
518 class differences and 77 projection-flag differences remain. In
particular, 46 class1/class2 differences change the class2/3 union, so it
cannot be represented as a reproduced candidate set.

All root class2 rows are small floating inversions; none affirmatively
measures thickness sensitivity. The saved unknown category contains four
nodes repeated across every contact1 master/setting. A zero empty-master
count is therefore vacuous for that interface. The descriptive summary
preserves these results but cannot resolve their failed replication. Its
derived geometric/class claims must be read under that failure ceiling.

The root read all comparison code before the fresh consumer replay. The
comparison runs reran 35/15 producer controls and 12 comparison controls.
The separate implementation reviewer read the complete frozen producer and
checked all saved array hashes/representations, but did not independently
recompute distances. Its before-load mutation test rejected an altered
synthetic method fixture with no source/array load; exact setup and temp-file
pins are preserved in its review. Existing-output guard scope is narrower
than a guarantee of a retained receipt for every possible refusal.

## Primary-source and mathematical reviews

- [Source crosswalk](source-crosswalk-review.md): independent full-page
  coverage of 16 NIST pages, including 12 initially declared leads and four
  immediate context extensions. Root separately viewed complete NCSTAR1-9
  physical542/548/549/550. This does not claim root personally viewed all16.
- [Control-method review](control-method-review.md): independent full-stream
  numeric extraction plus 13 additional complete manual-page views and four
  repeat views; exact primary coverage and prior47-page dependencies are
  listed there. Root viewed complete physical395/402/403 for the geometric
  formula, with earlier full views of the selected global/local controls
  preserved in context and prior review. Ground758/759 are root's separate
  primary-rule check, not the control reviewer's page coverage.
- [Mathematical review](geometry-method-review.md): independent derivation
  of bilinear/triangle distance enclosure and conservative AABB containment;
  no source/run/implementation certification. It expressly distinguishes
  numerical tolerance from certified arithmetic and physical uncertainty.
- [Implementation review](proximity-implementation-review.md): fixed-input
  algorithm and stored-representation review, with unknown/inversion,
  multiplicity and control-application qualifications preserved.

No admitted PDF was edited or re-exported. No held source or marked packet
was used. A source's published model description is not independent evidence
that its state occurred in the building.

## Exact arithmetic and independent reproduction

The [exact follow-up](EXACT-ARITHMETIC-ADDENDUM.md) is prospective after the
failed floating result, not a change hidden inside the frozen calculation.
Two reviewers independently identified a missing +epsilon in its initial
broad-phase wording before historical evaluation. The appended correction
preserves the original text and restores the original boundary buffer.
Current addendum SHA-256 is
`b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89`.
Both implementations have now completed the fixed 80/120-bit evaluation,
and all exact cross-implementation comparisons pass. They reuse separately
extracted frozen numeric geometry, not independent physical measurements.
Root read the full reference producer before its earlier 80-bit replay and
the full current comparison adapter/helper before the new consumer replays.

| Artifact | SHA-256 |
|---|---|
| exact_proximity.py | 032804acb5862b6202d7037b864b2421c10b0f8383b0f2382a856810423dc25f |
| exact-proximity80.json | 25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324 |
| exact-proximity120.json | ec72208fb65f7a849efebae77af5c834c4eb17e1180dddca2f1a17fb525d0711 |
| exact-proximity80-root01.json | 60e12bb8f70944cb0c8996e7a1e8387c3405de7e5b341e5d6bfd2c84e08843f3 |
| All three reference NPZ products | 79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628 |
| exact-proximity80-proofs.json and root repeat | 53757ba19edeeacf7ec64222786344977cb02eef5d54d7da2cbae0445e4bd2e6 |
| exact-proximity120-proofs.json | f653b0d0d4e69bfd42a79bb1321e540c4a18a92bdaa99efd3540bccc13fe80e7 |
| verify_exact_proximity.py | c850bdb2e02843e4cbdf2c3cb08b309e25d47708d9fa7b1e41bc4dbe9d044e2f |
| independent-exact80-02.json | df8246830906ba20a814835d69f45c0196301ab76179e84b227c447d0352b11e |
| independent-exact120-01.json | ecbde1063f26bbc520fdbae40209c88c5e433542eee97c6e92b212dc08ffab62 |
| Both independent NPZ products | 6c4bf3e3bdfeb00c14ef859407c7d685c950123a415a49452e4058e0aecbd8a4 |
| compare_exact_proximity.py | 9854b4d2df68ae14b03a834539c79163a66961407c0cee193ace2361f9edd7e3 |
| compare_exact_reference.py, current adapter | d3f0640a73f95001ce8a0ec8115243fd3362cae16c879de86b77cf66bbc06dcc |
| independent-exact-reference80-root01.json | 4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8 |
| independent-exact-reference120-root01.json | 5535deca74b1eed2c187a58a77c892e7b34ad206ec6b92ca82aea8015a91b4ef |
| independent-exact-precision-root01.json | cd7ff215a3b8bd1f0e1dfb44600dcff4840bfe6c507e3b5db61a1890e0f0a238 |

The reference uses exact oriented-cross projection plus closed edges; the
independent implementation uses a rational Gram-system projection plus
closed edges. Both convert frozen binary64 values through integer ratios,
compute extended corners rationally and enclose roots on fixed dyadic grids.
Their actual all-population search masks agree; rational squared distances,
intervals and projection flags reproduce. All 14 reference arrays, 11,292
pair certificates and 2,226 geometry certificates match at each precision,
without a numerical tolerance. Schema normalization and the separately
recomputed diagonal/slab-counter views are explicitly post-freeze checks,
not a third blind discovery. See [independent review](independent-review.md).

Reference runs passed 12 control groups each; independent runs passed 32.
The independent precision consumer passes 14 controls, all 12 of its numeric
arrays and 95,880 pair interval-nesting checks. The reference author's own
[precision checker](exact-precision-comparison01.json) is separate internal
validation, not independent geometric corroboration. Root's new comparison
consumers passed 12/12/14 controls in 6.881/6.971/6.170 seconds respectively,
at measured peaks 618,561,536 / 639,991,808 / 590,069,760 bytes. All three
calls are terminal, exit0; there is no pending root comparison process.

Both exact implementations retain class totals [8,520,84,0,2,688] and all
338,488,050 population memberships across settings. No class2 remains under
these arithmetic/scenario definitions. This is not a finding that effective
physical thickness, contact pairing or restraint is certain. Float views
of the rational results are ordinary conversions, not certified outward
floating endpoints.

### Exact follow-up history: retain the actual failures

Reference preflight [exact-controls01.json](exact-controls01.json), SHA
`afc1efff1a55e7c4ec63dfc9cccb74b7b3545a216098d0b1fc243fbaca9e731d`,
**passed**. A schema-only check then identified a four-column independent
master-identity representation versus three reference columns. The adapter
was corrected before historical evaluation; the old
[preflight code](exact_proximity_preflight01.py) is preserved. Added boundary
and nesting controls also [passed](exact-controls02.json), SHA
`1bb12933db25b40f7c3190cc366b55866c8ab8e9e516381b9afb4817eb744148`.
There was no failed reference exact calculation. The reference records
memory peaks but has no enforced RSS cap; its producer replay's measured
745,848,832 bytes must not be called a passed memory-rejection test.

The independent arm's initial old-method-pin refusal occurred before tests
or geometry evaluation. Its first historical 80-bit run subsequently failed
the 768-MiB memory gate after the geometry loop but before saving a complete
result/NPZ: peak 985,808,896 bytes. Both failure receipts and exact code
versions remain preserved in the [independent review](independent-review.md).
Changing only the packed-mask comparison to avoid simultaneous full bit
expansion yielded the completed 80/120 results; geometry and classifications
were not tuned. The original floating comparison remains FAIL, not retroactively
PASS because the later arithmetic works.

## Contact-to-damage join

The [contact-to-damage protocol](CONTACT-DAMAGE-JOIN-PROTOCOL.md), SHA-256
`36443e2edb37ae596f93b66c58792bceb83b4cd2f902dc4aee1ec13f7ab22cd7`,
declares an exact typed/coordinate-checked join against 1,543 shell, six beam
and 355 discrete candidates using already preserved derivative geometry.
Root's frozen `contact_damage_join.py`, SHA
`537f8b025a851572e17fc3dfb654838efde28e1aa54c50edcd48b39ae870d965`,
passed 10 synthetic controls before each completed historical join. It
requires a hash-pinned PASS exact comparison receipt before loading the
candidate geometry. This invocation uses the actual fresh root 80-bit
comparison consumer, not a manually authored approval flag.

| Artifact | SHA-256 |
|---|---|
| contact-damage01.json | e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479 |
| contact-damage02.json | e9b33a59006cf60f722388ad3299a80a50bc5be75233c0a29b9faa98685bdce9 |

All 1,904 typed element records reconcile across the two frozen derivative
sources; all 54 setting/CID/class/family groups, 78 positive match rows and
zero master-alias matches are retained. The complete repeat JSON differs
only in its output command argument and elapsed time. Per setting, the
positive CID1/class3 groups contain nine shells/12 matched nodes/36
node–master–element relations and 17 discrete numeric beam-list matches/
17 nodes/20 relations. All other groups are zero. These are static typed
incidences, not deletion semantics or activation. The CaseA contact-mediated
expansion is separately unperformed.

The independently written endpoint-index join froze its code/results before
root producer or result access. It passed 23 controls, reconciled all 1,904
typed records, and checked all 571 node IDs shared by those elements and
the frozen stage: 1,713 coordinate scalars, not only eventual positive hits.
It retains 11,208 selected candidate rows/406 unique nodes and all 742
master-alias negative results. Its separate post-freeze comparison adapter
covers every root result field, all 54 groups (48 zero), 78 element-group
records and 168 node–master–element relations across settings. It reruns
14 adapter controls and both producers' 23/10 controls. Root read the
complete independent producer and adapter, then completed its own adapter
replay, PASS exit0.

| Artifact | SHA-256 |
|---|---|
| verify_contact_damage.py | c49436fbe3be336ee936a68bc685d2921261fbac95b148e468821fa51d11b511 |
| independent-contact-damage01.json | dfc169a0c824f0a0981aea60d0e01a5fac0e4de9af4e26e580bc702b177430de |
| independent-contact-damage02.json | 60fb501873e30815b74fafa766fcd2b0dd129e4fca2e2978b7df2116569a1a5a |
| compare_contact_damage_independent.py | 7a684b8ee7506609d66ad432d61561d2c077ce1ce99b5f30d9a63e35d6f0c7a4 |
| independent-contact-damage-comparison01.json | 9e746e77c3258e5a34ca9c316e79c2c07598be3354e207ecf21cd517cfe86de7 |
| independent-contact-damage-comparison-root01.json | d55867f6a86b09750d721775a982f2f342c995ffe7be33798484333cd26be875 |

The full adapter replay differs only in command paths/output name, elapsed
time, peak bytes and one producer unittest stderr hash. The latter includes
test elapsed time; old raw stderr bodies are not retained and are not claimed
byte-identical. All substantive comparison fields, input pins and parsed
control results match. The original independent review's earlier pending
parent-consumer wording is superseded here by these actual completed receipts.

### Candidate/part descriptive summary

`summarize_exact_parts.py`, SHA
`95f78eb2b6abe8496e2d882e599480617c2f18ea4b9d7d420367dd6219d941d1`,
passes 12 synthetic groups before source-array loading. The post-result
summary uses all frozen exact candidates, not a new selection rule, and
reconciles stage versus exact-output incidence arrays. All 18 setting/CID/
class groups, 14 typed-part entries per group including zeros, 406 node
records and pairwise CID/class overlaps remain available. The absence/type
of material definitions is inherited from the previously verified registry,
not a fresh search for every historical include or full property law.

[exact-parts01.json](exact-parts01.json), SHA
`fe62487947a64dd4816c398cc92124073c4253a1d04f40c5401aa18b2e893e1e`,
and root's [replay](exact-parts-root01.json), SHA
`4358020def13b035b5579e89424de5f3f3bfda28e39609183107c7b13c2c958c`,
agree on every field except output path and elapsed time. Root read the full
code before replay and the completed [part-summary review](exact-parts-review.md).
The full [independent join review](contact-damage-independent-review.md) was
also read; its pending-parent language is historical, superseded by the
actual comparison-consumer receipt above. This is same-code reproduction of
descriptive grouping, not a third independent extraction or an independent
mechanical validation.

## Final report review and version boundary

The [completed review](completed-report-review.md), SHA
`3d8a130872f11d20ca417d2e9d6c406b5981311eba485cc5bee4699aa5ff345d`,
finds no remaining material issue in report SHA
`897985a48592f4ea13394e9a4b4514ada1857d769e679dd967f55113e4d97ee8`.
Root read that complete review. Two wording corrections explicitly distinguish
excluded class1 summary groups from retained overlap reconciliation, and
completed part summaries from still-needed material-law details. Reversing
exactly those changes reproduces the original reviewed report hash; no
result, source, method or physical conclusion changed.

That reviewer read validation version
`8a4be5036ad64d2bddbe67bf4362728f1cd52965824b792fa4cdbbd3b7d3e374`.
Subsequent additions here record completed subreview reading, actual artifact
checks and the final disposition; they are root-authored closeout, not
silently included in the earlier independent review. The same reviewer
opened and compared the actual fresh consumer receipts, including the
documented exact80 adapter-version additions. Scope is computational/source-
provenance review, not licensed engineering or external expert endorsement.

## Artifact and guard checks

[verify_unit_artifacts.py](verify_unit_artifacts.py), SHA
`36d903c8a399659bec0af7bde7b664fa59b4c4032cbdc5cedd4d147bd1544a39`,
checks file integrity, Python syntax, strict JSON parsing, local Markdown
link existence, text whitespace, expected retained PASS/FAIL statuses and
complete receipt differences against narrow exclusions. It does not validate
link fragments, engineering methods, historical authenticity or every
unretained diagnostic. No synthetic fixture alters a source/result file.

The actual join entrypoint rejects a changed verification hash before data
loading and refuses an existing output without changing its bytes. A
temporary synthetic dependency also passes the production pin function,
then fails after its contents change. These checks supplement the producer's
weaker pin-predicate unit test; they do not cover every possible refusal.

[artifact-check01.json](artifact-check01.json), SHA
`c4d3dd8498037614c41e00c326a1e6aa78b2a157c7b168e94f16c043e825fa14`,
passed with 23 Python ASTs, 40 JSONs, 107 local links and 40 text-whitespace
checks. That inventory pins the report's pre-final-review version
`2794e40962c350b2d66b2441626b2957836844e261f41921cb2976875924f45a`;
later report/validation changes require a fresh final artifact receipt.
Read-only `validate_record.py --strict` and scoped tracked-file
`git diff --check` also pass. The record validator checks headers,
issue/fact links and citation tags, not science or disclosure authorization.
The final post-review inventory is saved separately as `artifact-check02.json`;
its actual status and pinned versions, rather than this planned filename,
control that check's disposition. It excludes artifact-check receipts from
its own file inventory to avoid self-referential hashing.

## Runtime, commands and boundaries

Bundled Python3.12.14 / NumPy2.3.5, dependency bundle26.905.11957. Executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Commands ran in this unit directory with `-B`; fresh output names are required:

```text
python3 -B compare_geometry.py --output comparison-root01.json
python3 -B proximity.py --output proximity-root01
python3 -B proximity.py --output proximity-root02
python3 -B summarize_proximity.py
python3 -B compare_proximity.py --output proximity-comparison-root01.json
python3 -B exact_proximity.py --bits 80 --output exact-proximity80-root01
python3 -B compare_exact_reference.py --bits 80 --output independent-exact-reference80-root01.json
python3 -B compare_exact_reference.py --bits 120 --output independent-exact-reference120-root01.json
python3 -B compare_exact_proximity.py --output independent-exact-precision-root01.json
python3 -B contact_damage_join.py --output contact-damage01.json --verification independent-exact-reference80-root01.json --verification-sha 4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8
python3 -B contact_damage_join.py --output contact-damage02.json --verification independent-exact-reference80-root01.json --verification-sha 4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8
python3 -B compare_contact_damage_independent.py --out independent-contact-damage-comparison-root01.json
python3 -B summarize_exact_parts.py --output /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/c79-contact-geometry/exact-parts-root01.json
```

The floating `compare_proximity.py` command retains its completed failed
comparison; the subsequent exact and join commands completed PASS. Source
products remain unchanged. There is no live root calculation session
awaiting a poll for these commands. All three bounded review agents have
returned terminal results; earlier pending-results sentences are historical.

No solver, activation, assumed missing material, source transmission,
canonical promotion, outreach, legal drafting, commit or push. The generic
precision/decision-reproducibility workflow note was deduplicated locally
under SFB-004/SFB-005; the designated archived feedback task remains
unresolved, with no send, acknowledgment or fix claimed. No operational
Sherlock–Faraday bridge or accepted scientific finding was created.
