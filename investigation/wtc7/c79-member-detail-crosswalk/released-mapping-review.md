# Released mappings for the selected column/member crosswalk

2026-09-13. Independent bounded review under [PROTOCOL](PROTOCOL.md) and the
[charter](../CHARTER.md). Research only; no raw-source rescan, solver, new law,
physical restraint finding, coordinate-floor transform or cause inference.

## Result

The frozen derivatives provide explicit **Column44 → PSID144 → PID144,
Column76 → PSID176 → PID176, and Column79 → PSID179 → PID179** diagnostic
joins. These are normalized source-author labels linked through actual part
sets, not a guess that a part number names an architectural column. Parts,
section/material references and aggregate coordinate envelopes are supplied.

The north seats at Floors8–12/14 and the Floor14 west attachment are **not yet
identified as specific released parts/elements** by these derivatives. The
selected Column79 region has full seed-node/element provenance and contact
candidates. Column44/76 mostly have aggregate part geometry, plus one specifically
traced Column76-region node. The selected contact-stage population has zero
node–part-incidence rows to144/176; this is a limited coverage result, not
evidence of physical disconnection or absence of inter-column girders.

No physical units, signed geographic frame, origin, floor-to-Z table,
as-built identity, initialized tie or surviving restraint capacity is supplied
by those labels or numerical relationships. Regular spacing is not a floor ID.

## Actual coverage and checks

Read current main AGENTS.md/WORKFLOW.md/START-HERE.md; complete worktree charter,
current synthesis and latest handoff; the present protocol and the member-map,
thermal trace, residual/contact extension/candidate join, contact geometry and
material/run protocols. Read the complete member-map, thermal-trace, residual-
restraint and contact-geometry reports and the prior contact source-crosswalk
review. The job card governed initial inspection before this protocol existed;
the completed protocol was read before saving this note.

Inspected only safe numeric/typed and hashed-label/locator fields in the eight
numeric derivatives M/T/R/C/S/A/P/V below, plus receipt MR. No raw title/comment,
private metadata, original payload, PDF/drawing, media or force history was
opened. No new primary visual coverage is claimed. The source/evidence skills
keep this note exploratory and preserve the record-content/physical-inference
boundary. All main/raw/prior-result files remained unchanged.

A read-only inline command using
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`
and hashlib/json/pathlib/NumPy completed exit0. It checked M/T/R/S/A file hashes
before and after, loaded A with `allow_pickle=False`, and verified every array
against S's shape/dtype/SHA-256 of `tobytes()`. Results:

| Actual check | Result |
|---|---:|
|Pinned inputs before/after|5/5|
|Stage array shape/dtype/byte-hash matches|11/11|
|Identical thermal/graph seed-ID population|873|
|Thermal strings converted to binary64 equal graph XYZ|873/873 nodes|
|Common stage/seed exact XYZ and `[121, NODE line]` matches|774/774 nodes|
|Stage incidence rows / unique nodes for PID144|0 /0|
|Stage incidence rows / unique nodes for PID176|0 /0|
|Stage incidence rows / unique nodes for PID179|774 /774|
|Stage incidence rows / unique nodes for PID1179|18 /18|

This is consistency checking of frozen derivatives, not independently repeated
raw extraction or physical validation. Other locators below were read directly
from freshly hashed JSON fields. No new proximity/transform arithmetic or
historical parser/synthetic-suite rerun is claimed. No standalone code/receipt
artifact was saved for this small read-only check; the table records its actual
terminal outcome, not a producer-generated historical receipt.

## Diagnostic → part → section/material

All lines in this table are in the previously decompressed SRC121 master.
`column_diagnostics[].line` locates the diagnostic keyword and `partset.line`
the part-set keyword. PART keyword/card locators are independently retained
in V, not guessed from line spacing.

|Diagnostic|Diagnostic / set keyword|Effective PID / SECID / MID|PART keyword / numeric card|Region / incident thermal IDs|
|---|---|---|---|---|
|Column44|369 /366|144 /144 /100|3070 /3072|624 shells /700 IDs|
|Column76|593 /590|176 /176 /99|3486 /3488|944 shells /864 IDs|
|Column79|614 /611|179 /179 /99|3525 /3527|952 shells /873 IDs|

Pointers: M `column_diagnostics[]` selected by `column_number`, M `parts[]`
by PID, and V `all_part_references[]` by effective PID. The numeric PART cards
are `[144,144,100,0,144,0,0,0]`, `[176,176,99,0,176,0,0,0]` and
`[179,179,99,0,179,0,0,0]`. Original/effective IDs coincide for these master
definitions. These are ordinal source values, not new physical-property claims.

All three sections are marked defined. V `material_id_index[]` locates
MID99 at SRC121 keyword2486 and MID100 at2496, both
`MAT_ELASTIC_VISCOPLASTIC_THERMAL`. Their full bodies are not among V's selected
material exports. **Definition present** is not **full body reviewed here**;
this is not a missing-law finding for99/100.

S retains SEC179's SECTION_SHELL keyword3522/cards3523–3524:
`[179,2,1,4,0,0,0,null]` and `[0,0,0,0,0,0,null,null]`. It does not retain
selected section bodies144/176. That limited schema omission does not negate
M's positive section-presence flags. No new field semantics, stiffness or
section capacity is assigned.

### Exact retained part envelopes

These are model-coordinate minima/maxima, not surveyed centers or elevations:

|PID|X|Y|Z|
|---|---|---|---|
|144|17.13738…17.68602|15.85341…16.30299|−70.50379…−43.6118|
|176|−0.22733…0.22733|−0.28448…0.28448|−71.1708…−43.6118|
|179|13.13262…13.77258|2.408667…3.077733|−71.1708…−43.6118|

The three retained Z envelopes overlap on −70.50379…−43.6118;176/179 have
identical aggregate Z limits. This simple interval intersection is not proof
of coincident material, matching floors or physical connection at either end.

M's diagnostic `member_geometry_bounds` and corresponding part `geometry_bounds`
agree. Its declared scope is the entire referenced part set, not only the
cutting-plane intersection. The diagnostic plane cards cannot be relabeled as
floor coordinates or a verified force-selection intersection. These regions
are not necessarily complete physical columns.

## Element, node and region bridges

R retains all952 selected PID179 shells with family/EID, ordered physical
nodes, original/effective PID and source line, plus873 seed nodes. Example:
SRC121 shell769990 at line5505690 has nodes
`[843090,843091,843095,843094]`. Direct neighbor SRC120 shell769987 at3981182
has `[843080,843083,843091,843090]`, sharing843090/843091.

All20 direct neighbors are outside-region shells, effectivePID1179;18 seed
nodes are shared. There are zero direct beam/discrete/solid neighbors and891
retained coordinate records over seed+neighbors. The18 shared seed nodes lie
on exact supplied Z−71.1708 and−43.6118, without story assignments. Exact
same-node incidence is not adequate restraint or complete coupling coverage.

The admitted SRC120 transform adds1000 to part/section/material IDs, not
nodes/elements/coordinates. Its originalPID/SECID/MID179 becomes1179.
V retains its PART keyword4087367/card4087369 and raw numeric values
`[179,179,179,0,179,0,0,0]`; effectiveMID1179 is
`MAT_PIECEWISE_LINEAR_PLASTICITY`, keyword4087357, not masterMID99. S retains
SECTION_SHELL keyword4087364/cards4087365–4087366. Matching original integers
does not make regions or materials interchangeable. WholePID1179 geometry is
broader than the20 direct neighbors and is not their neighbor-only extent.

T supplies NODE source lines for every regional seed node. Node921518 is
SRC121 line925814 at `[13.65127,2.408667,-67.2846]`, with four PID179 shell
incidences. SRC118 lines512465/512527 carry TS50.57/46.97, TB0/LCID2.
These are coefficients in source order, not historical time steps or effective
temperature. Seven nine-node repeated-coefficient Z groups do not name floors.

T also supplies the specifically selected node842747: SRC121 line847043 at
`[0,0,-71.1708]`, with two PID176 shells, two effective1176 shells and one
beam each in73/74. Its nine assignment rows remain in T. This is partial
Column76-part coverage, not a Floor14 attachment identification or a complete
Column76 graph. No analogous full Column44 node export is present in these
selected derivatives.

## Contact and candidate-part bridges

C preserves these SRC121 definition/selector locators:

|CID / variant|Keyword / heading / first numeric card|Slave → master|Seed-related selection|
|---|---|---|---|
|1, TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET|6426410 /6426411 /6426412|node set1 → segment set1|710 master records|
|2, TIED_SURFACE_TO_SURFACE_ID_OFFSET|6532025 /6532026 /6532027|segment set2 → segment set3|32 master records|
|3, AUTOMATIC_SINGLE_SURFACE_ID|6532071 /6532072 /6532073|part set1; master not applicable|set includes179|

Node set1 is keyword5523384/header5523385; master segment set1 is5542509.
Slave segment set2 is6426421/header6426422; master set3 is6516807.
Part set1 is6532036/header6532037, with seed membership at6532049.
Neither node set contains seed nodes; the seed's master-side role still exists.
These selections are relative to PID179, not all columns/floors/components.

S supplies742 ordered master records, complete vertices/XYZ and shell aliases
with typed EID/PID, source connectivity/thickness lines. Example: segment-set1
record SRC121 line5632324 is `[843083,843080,843090,843091]`; its unordered
shell alias is outside769987 above, thickness continuation3981183. Its order
differs from the shell. It is not an initialized pair or an automatically
corrected orientation.

For a candidate node, the usable chain is P `result.node_registry[node_id]`
→ NODE source line + typed incident PID → `part_reference_registry[effective_pid]`.
Group `relations` carry node/master-index joins; that index resolves to
S `result.master_segments`, with ordered faces and alias locators. These
bracket expressions mean selection by the named field, not JSON array indexing
by node/part ID. A supplies XYZ and numeric incidence joined by actual NID.
Its schema gives node/kind/effective-part/count columns, with shell0/beam1/
discrete2/solid3. Array positions are not node identifiers.

P retains406 unique nodes across14 typed parts in selected classes0/2/3.
At each extension it has122 class3 CID1 nodes,280 class3 CID2 nodes and4
unknown-thickness CID1 nodes, no shared-CID nodes and zero class2 nodes.
These are surrogate candidate memberships, not406 realized connections.
Unknown-thickness nodes have beam incidence, not an absence of connectivity.

The typed candidate universe is shells11/12/773/803/1034/1783/1803,
beam66 and discrete806/820/821/852/855/859. Parts773/803 have present PART/
SECTION definitions but absent materials in that frozen registry;21/28 class3
nodes respectively are listed, not automatically disjoint physical supports.
Their PART card lines are4236/4292; section card lines4232–4233/4288–4289.
Spring-type definitions820/821/859 are positively present in P; the later
spring audit controls their full consumer/curve-dependency result, not this
limited presence schema. No PID is promoted to a seat/clip/bolt/floor label.

The array check's zero144/176 incidence applies only to this selected-stage
population. It does not exclude contact-mediated paths through these other
parts, other sets or other column regions. The old contact report's statement
that its CaseA follow-up was unperformed is superseded by the completed
CaseA/spring audit and current synthesis; this review does not revive it or
rerun any damage join.

## Physical join still needed

The prior source review supplies a published ANSYS plan orientation and local
C79 connection axes; earlier global-result prose names north/south Y roles.
Neither authenticates the released coordinate frame. No new geographic or
floor assignment is made here. The root's source arm controls2008-versus-2012
seat/travel corrections; old values in prior notes are not adopted as current
dimensions or contact tolerances by this arm.

|Physical target|Positive existing bridge|Unresolved bridge|
|---|---|---|
|C44–C79 north seats, Floors8–12/14|44/79 diagnostic-part envelopes; full selected179 graph; typed contacts/candidates|Floor/elevation and exact girder/seat/clip/bolt part/EID/end-node identity, drawing revision and surviving state|
|C79–C76 Floor14 west attachment|79/76 diagnostic-part envelopes; one traced176 node; full179 contacts|Floor14 and member/end/attachment identity; 'west attachment' is not a one-sided or bilateral law|
|Floor13 comparison|Same column-label and selected179 data|No floor13 assignment from repeated Z groups or presumption of identical retained-floor connections|

The smallest useful independent check is a version-identified drawing/model
crosswalk for one C44–C79 seat and the Floor14 C79–C76 attachment, naming the
member/detail, floor, effective part/element and end-node IDs. It must state
units/origin/signed axes and model/release transform, or give sufficient
independent labeled control points to test a declared transform against an
additional unused point. Numerical fit alone is not historical authentication.
Then compare its ordered end/face nodes against these frozen records. If the
identified nodes lie outside coverage, a new targeted source-extraction
protocol—not speculative whole-mesh remapping—is the next numerical step.

A successful geometry join would still require initialization/engagement,
gap/slip, failed versus surviving connector/bearing state and displacement/
directional-force histories for the relevant run. No stiffness, adequacy,
buckling sufficiency or physical cause follows from this static bridge.

## Identity pins

Fresh SHA-256 values; original sources were not newly rehashed. MR records
the earlier complete EOF=true and pre/post compressed/uncompressed identities.

|ID|Derivative|SHA-256|
|---|---|---|
|M|[Member map](../model-member-map/run06/member-map.json)|`eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e`|
|MR|[Map receipt](../model-member-map/run06/receipt.json)|`4ed99830a61606e18ac0720102354c3450ecffc61fc7743d35f9b62b9750529d`|
|T|[Thermal trace](../thermal-assignment-trace/run01.json)|`54f20f57b06948f95a1ad8d384fd5f8a1778c0a6c0d2d8966efa139addac13ae`|
|R|[Residual graph](../c79-restraint-audit/root01.json)|`f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef`|
|C|[Contacts](../c79-restraint-audit/contacts-root01.json)|`04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859`|
|S|[Stage metadata](../c79-contact-geometry/stage-root01.json)|`deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963`|
|A|[Stage arrays](../c79-contact-geometry/stage-root01.npz)|`2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf`|
|P|[Exact parts](../c79-contact-geometry/exact-parts01.json)|`fe62487947a64dd4816c398cc92124073c4253a1d04f40c5401aa18b2e893e1e`|
|V|[Property references](../material-run-crosswalk/run01.json)|`b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594`|

Inherited decompressed source hashes: SRC118
`fa721837357cf7b7fd43e49d2a9d171973663e12399c503163ef56c3464b060d`;
SRC119 `8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601`;
SRC120 `7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda`;
SRC121 `8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf`.
MR retains matching compressed pins/counts. Source integers and line locators
refer to those captured streams, not authenticated historical execution.

Reviewed prose: member report `68a1978db06ba10461c39e4c0074480fc4fef440f8bbda9d866113e2d5a8e4e5`;
thermal report `bd8e9162b10eb5ce59d671cce0cbe8a8b8febaa6ac1d1d484c5a21ef1b8ea08c`;
restraint report `6b57c44b9e6b194b019a8a362cb5242ab1f3b69ec679907389382e5593d59fda`;
contact report `897985a48592f4ea13394e9a4b4514ada1857d769e679dd967f55113e4d97ee8`;
contact source review `ecd223c11a23daa1ef1dc3bbd9c228a3489fe5fe7596fa20144d9bbb7f259c34`;
current synthesis `3ab4479ab789d204ebd1760aac97191b5ac90fbf69756cb66e76c9657a947269`;
current protocol `f2a2dc599e2cb06c828aed9fea6965fbc8f1d9387dca779b554641f084e299bb`.

The first save attempt timed out at automatic permission review; no file was
created. This note is the permitted single retry, with no separate numeric
receipt. No unrelated file, main/canonical record, raw source, or previous
output was edited; no transfer, outreach, commit, push or expert certification.
