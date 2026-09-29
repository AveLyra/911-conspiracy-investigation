# Independent first-stage geometry review

September 13, 2026. Research-only, numeric source extraction. The parent
[protocol](PROTOCOL.md) and [independent plan](INDEPENDENT-STAGE-PLAN.md)
control. No proximity threshold or physical contact-pair claim is introduced.

## Independence and prospective scope

The independent implementation reuses its author's frozen
`c79-restraint-audit/verify_restraint.py` typed numeric reader, SHA
`5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a`.
It does not import the root producer or `map_members.py`. The 710/32 selected
master records and their seed selection are prior knowledge, reused from the
frozen independent contact result; they are not newly independent physical
evidence. Complete slave NSET1 and SEG2 membership, selected coordinates,
element incidence and master-shell aliases are freshly extracted from all
three admitted geometry streams. No new root geometry code/output was read
before this implementation and its source pass were frozen.

The first source-pass code was frozen as
`a1e60b3625d00f266e3f31c983ffcbe4b3843a1c38087ccf3924e9f006ec8a06`.
The independent plan hash is
`4b616ea1a57727c7b0ac034cdc55bdb25fc656d355ef805907407bcc11cf506f`;
the parent protocol hash is
`b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea`.

## What is retained and what is not inferred

The numeric-only NPZ design retains every selected membership occurrence,
source/line/row/slot, coordinate with source locator, and the union of slave
nodes and every selected master vertex. It does not dump all global node
coordinates. Integer IDs remain integer arrays. Float blank slots remain
explicit masks/NaN, distinct from supplied numeric zero. Consumers use
`allow_pickle=False`; each array has a registered shape, dtype, columns and
C-order byte hash in JSON.

Node incidence counts each physical element once per node. Repeated shell
corners remain separate corner-slot records with their corresponding THIC
field. THIC1–4 extrema and the fifth BETA/MCID field remain distinct; none is
chosen as effective solver contact thickness. Whole-incident-shell THIC
extrema are distinct from the local corner's supplied values. Beam N3 is an
orientation reference, not an endpoint; discrete ground zero is not a node.

Every master-shell alias is retained. Exact ordered four-node equality is
reported separately from equality of the sorted four-slot multiset; repeated
vertices are not collapsed into a set. Multiple or missing aliases are not
silently reduced to one. Supplied element, PART, SECTION and material-ID
associations remain input references, not proof of physical member identity,
mechanical response, contact activation or surviving restraint.

The three-source include graph is freshly reconstructed and checked against
the frozen earlier graph, including all transform cards and source locators.
This gate precedes the physical-element pass. Source120 namespace shifts are
PID/MID/SECID/HGID +1000, with unchanged NID/EID/set IDs. FCTLEN1 and TRANID0
support coordinate identity. The numeric FCTTEM1 character-flag caveat remains;
it is not interpreted as a temperature multiplier. The thermal include is
recorded as an edge and is not followed in this three-source task.

Numeric CONTROL_CONTACT cards are independently retained. Any PART_CONTACT
presence receives only a hash/locator until an admitted schema is established;
the reused geometry reader rejects unsupported PART variants. This review
does not certify default selection, optional-control applicability, historical
executable behavior, contact pairing, units/floors, capacities or collapse cause.

## Controls and execution status

Before any new historical source pass, 27 synthetic controls passed. These
exercise selected-header/member separation, membership and corner repetition,
numeric zero/blank attributes and controls, unsupported/missing set headers,
END coverage, duplicate sets/nodes, unique-element incidence, local versus
whole-shell thickness, fifth-field exclusion, orientation and ground-node
exclusion, zero-shell nodes, ordered/unordered/missing/multiple aliases,
namespace/missing material reference, missing element nodes, actual reused
shell continuation parsing, missing continuation rejection, nonnumeric-array
rejection, output-scope and existing-output guards, a digest-mismatch gate,
and numeric-only NPZ round-trip. The digest control is a synthetic gate test,
not a deliberate mutation of historical inputs.

The source pass completed **PASS**, exit 0, with 27 controls, nine complete
source/phase EOF receipts, unchanged compressed/decompressed and dependency
pins, 90.1216262918897 seconds, and peak 294,649,856 bytes. Each of SRC119–121
was read through EOF for selection/control scanning, metadata/nodes, and
physical elements. Source byte/line counts were respectively 508,372/7,905;
232,959,541/4,088,491; and 333,947,423/7,196,443 on each pass. No source-pass
failure occurred in this unit. These are parser runs, not source-program or
solver executions.

Frozen [independent-stage01.json](independent-stage01.json) SHA:
`ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd`.
Frozen numeric [independent-stage01.npz](independent-stage01.npz) SHA:
`fcab10b2081c7fe3e1c0f9f4cdf92344d55e88e12c408fd7b70ebaeb0bcc0ad5`.
The NPZ contains 35 registered numeric arrays, 10,603,554 compressed bytes;
the saved arrays were reopened with pickle disabled and checked exactly
against their in-memory arrays, including matching NaN positions.

All 3,593,049 node records and 3,045,925 physical element records were parsed.
The element total comprises 2,461 SRC119 solids; 2,042,843 SRC120 shells;
and 964,067 shells, 3,190 beams, and 33,364 discrete elements from SRC121.
Only the selected 285,500-node union is retained, with every selected
coordinate resolved. The retained incidence tables contain 207,820 shells,
33,059 non-shell elements/orientation-reference records, 614,635 shell corner
occurrences, and 318,601 unique node/part/family aggregate rows.

| Population | Unique nodes | No shell incidence | Differing local supplied corner thickness | Physical node-element incidences |
| --- | ---: | ---: | ---: | --- |
| Slave NSET1 | 152,977 | 4 | 11,187 | 249,651 shell; 5 beam; 33,054 discrete; 0 solid |
| Slave SEG2 vertices | 131,740 | 0 | 0 | 361,536 shell; 0 other families |
| Selected master vertices | 783 | 0 | 546 | 3,448 shell; 0 other families |

These incidence totals count a node-element relationship, not distinct
elements across an entire population. All three populations have zero beam
orientation-reference incidences. NSET1 has 152,977 occurrences with no
repeated member ID. SEG2 has 90,384 rows and 90,336 distinct ordered four-node
tuples, hence 48 extra ordered-node occurrences. Attributes remain separate
and were not silently included in that uniqueness definition.

All 742 selected master records have exactly one unordered four-slot shell
alias: 442 also match the full order and 300 do not. None has a missing or
multiple unordered alias. These are record aliases, not 742 unique physical
surfaces, contact pairs or necessarily 742 different shell elements.

One CONTROL_CONTACT block was found in SRC121, keyword line 4, with two
supplied numeric cards on lines 5–6. The preserved values include both numeric
zero and nonzero fields. No PART_CONTACT keyword was found in the three full
streams. Neither observation establishes effective defaults or contact state.

## Post-freeze comparison plan

After the independent source output froze, the parent released both root
stages and its code. Root reports its first implementation was completed
before receiving these independent new result summaries; those summaries
arrived while its first source run was pending, without code adaptation.
The root first synthetic attempt had failed the N2=0 discrete-ground fixture
before historical source reads. Its preserved preflight/code and primary
method addendum describe that correction. That is a producer test failure,
not a historical model finding. This review has read the complete current
root producer, but does not upgrade primary-method or physical claims by
doing so.

The comparison adapter was written after both extractions froze. It will
compare all 11 root NPZ arrays exactly, all 742 master records/aliases, common
PART/SECTION/material references, include transformations, global counts,
and complete stream receipts. No tolerance is allowed for parsed coordinates
or supplied thicknesses. Root numeric JSON integer/integral-float differences
are permitted only as exact equal numbers, never equal to booleans. Floating
array NaN positions must match. Root repeats may differ only in elapsed time
and the declared NPZ archive filename.

The adapter reconstructs NSET rows from positive independent member
occurrences and their exact source lines/row/slot numbers. Omitted slots are
normalized to root's zero-padding representation; this does not independently
recover the original blank-versus-zero lexical distinction for those slots.
Root SEG1/SEG3 master role columns are reconstructed separately from the
independent frozen master records. Node/part/family rows are reordered by the
explicit source IDs and field meanings, not by proximity or matching counts.

Root uses unordered node sets whereas the independent extractor uses sorted
four-slot multisets. The adapter will require every actual selected master
and alias to have four distinct vertices before declaring equivalence here.
Its repeated-slot negative control demonstrates why that equivalence cannot
be generalized to arbitrary shell cards. All independent extra element
records beyond root's retained master aliases, full root SECTION_SHELL
property cards beyond the first ID/locator, and root heading hashes remain
outside dual verification. Root's global ground-discrete counter likewise
lacks independent global endpoint retention in this unit.

Seventeen adapter controls passed before the comparison: exact/NaN identity;
tiny coordinate, NaN/zero, shape, dtype, nonnumeric array, node order,
namespace, line, attribute, alias count, metadata-key and boolean mutations;
set-versus-multiset/repeated-slot distinction; and strictly scoped root-repeat
exclusions including rejection of a changed numeric result.

## Actual comparison disposition

The exact comparison completed **PASS**, exit 0, in 0.9781459589721635 seconds,
peak 354,975,744 bytes. No discrepancy or failed comparison attempt occurred.
All 27 independent and 11 root extraction controls were actually rerun as
consumers and passed; these were synthetic control runs, not new full source
passes. Compressed historical sources and frozen dependencies were freshly
hash-checked before/after the comparison, with identical pins. Both root NPZ
archives have the same byte hash.

Frozen [compare_geometry.py](compare_geometry.py) SHA:
`93d751c87eeae5e1e93609f2d8e4719af1de830a84a82f833d66048ac40efc2a`.
Frozen [comparison01.json](comparison01.json) SHA:
`3aea77662c5eb6587694e56296809394e9fae666ce4c435f540b10275f682028`.
Root stage JSON pins are
`deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963`
and `0a9ff75f944ffa9238c56e01fc234e199f1ca65faccfbed98217c4bd53152a33`;
the common root NPZ hash is
`2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf`.

All 11 root arrays matched the explicitly normalized independent arrays for
both stages: 7,398,967 array slots per root result. The comparison counter of
15,083,434 includes both roots plus an internal 285,500-slot independent
corner-count consistency check, for 23 array comparisons. Sixteen compared
slots were matching NaNs. These are repeated verification operations, not
15 million independent scientific observations. Metadata counters (85,055
numeric, 2,638 boolean, 2,618 null and 945 string comparisons) likewise include
root repetition, checksums and repeated records rather than unique evidence.
Maximum difference on compared finite numeric data is exactly zero; no
tolerance, approximate match or rounding repair was used.

Every selected master record's set ID, line, ordered nodes, attributes,
coordinates, aliases, alias source/line/EID/original/effective PID,
connectivity order, full supplied thickness card and thickness source line
matched. All 742 actual masters and their aliases have four distinct node
slots, satisfying the set-versus-multiset equivalence gate for this data.
All 119 common part references matched, including the correct transformed
material/section namespaces and missing-definition states. Header rows,
global node/element counts, numeric include transformations and source EOF
receipts matched. Root01/root02 entire JSON objects matched after removing
only elapsed seconds and the explicitly different NPZ archive filename.

The two slave population bounds, in supplied coordinate values without a
physical-unit/floor assignment, are:

| Slave population | X range | Y range | Z range | Local supplied corner thickness range |
| --- | --- | --- | --- | --- |
| NSET1 | −65.96434 to 32.83676 | −26.9367 to 16.29029 | −94.869 to 90.44146 | 0.004763 to 0.127 |
| SEG2 vertices | −66.11758 to 32.92211 | −26.8913 to 16.26348 | −87.4268 to 86.8172 | 0.01803 to 0.1692 |

The four NSET1 no-shell nodes are IDs 912586, 912618, 912650 and 912682,
SRC121 node lines 916882, 916914, 916946 and 916978 respectively. Each has
one beam endpoint incidence and no shell/discrete/solid incidence. All four
have supplied Z −94.869. The comparison receipt retains their exact XYZ
values. Absence of shell incidence is not absence of all element incidence,
zero stiffness or proof of any solver's selected thickness rule.

The parent's fresh [comparison-consumer replay](comparison-root01.json) is
now independently checked **PASS**, SHA
`9cfe8c0873dc1b79e5279b19ea2a91107204af060aac09ba570c66123ee8c269`.
Its receipt differs from the independent comparison receipt only in
`command[0]` (relative script spelling), `command[2]` (output filename),
`elapsed_seconds` (0.9573629170190543) and `peak_bytes` (350,502,912).
All result counts, 17 mutation controls, source/dependency pins, diagnostics,
normalizations, exclusions and 27/11 extraction-control rerun receipts are
identical. The control stdout/stderr hashes also match; no blanket exception
for differing test output was needed. This was a consumer of the same frozen
outputs with fresh source-byte hashes, not another independent source
reconstruction. No producer, extraction code, numeric arrays or frozen
receipts were modified during this verification.

The first-stage numerical review is terminal. It does not certify the
separate primary-method review or an unperformed proximity diagnostic. Any
next numerical geometry method requires its own saved prospective protocol;
none is selected by the successful first-stage reproduction alone.

Passing source arithmetic establishes reproducible input topology and
supplied values, not physical truth or a collapse mechanism.

## Conditional floating-point proximity diagnostic

The separate [geometric method](GEOMETRIC-METHOD.md), SHA
`73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e`,
and its [pre-evaluation implementation clarification](GEOMETRIC-IMPLEMENTATION-ADDENDUM.md),
SHA `ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd`,
were read before implementation/evaluation. Unknown-thickness class0 takes
priority over the small-inversion class2 rule, as clarified before evaluation.
No raw geometry was rescanned. No root proximity code or numerical arrays
were read before the independent code and result froze.

The independent distance implementation uses a Voronoi-region closest-point
triangle algorithm and an orthogonal in-plane basis for the separately saved
projection flags. Root uses edge distances plus plane-projection/cross-sign
tests. Both follow the declared domains, thresholds, AABB admission and
bilinear-image enclosure; neither is a solver initialization implementation.
Thirty-five pre-evaluation controls passed, including full synthetic repeat,
complete mask/row bijection, zero-area planes remaining undefined, reversed
winding, warped and planar non-parallelogram patches, known-zero-distance
patch samples, extension-only admission, conservative broad phase checked
against an unpruned synthetic pass, repeated master records, thickness and
inversion rules, and source-pin/create-only checks.

Frozen [verify_proximity.py](verify_proximity.py) SHA:
`cd3559d84e332ea7a3877a15fe8ef0e7ec8717b9cc2c73746d610e3364a31d9e`.
Frozen [independent-proximity01.json](independent-proximity01.json) SHA:
`cc50ea1607ee4875610fdd7cdae62e22dc5e423eb776842849f1e6199217543c`.
Frozen [independent-proximity01.npz](independent-proximity01.npz) SHA:
`26a9c9421e37c38e96e7568bb0521763b0cd0e621a12e7e101f8a9b411a2bef5`.
The independent evaluation completed with exit 0, 17.426560916937888 seconds,
peak 427,687,936 bytes, 48 registered numeric arrays and unchanged pins.
This execution PASS was not a finding of independent numerical agreement.

All 338,488,050 declared slave/master/setting combinations have retained
packed admission masks. Both implementations admit exactly 3,156 CID1 and
608 CID2 rows at each setting, totaling 11,292 rows; the masks do not change
between the three extension settings. Of these, 8,520 rows are the four
unknown-thickness CID1 nodes repeated across 710 masters and three settings.
Their universal admission is the declared unresolved rule, not evidence of
8,520 physically plausible ties. Both implementations retain zero same-node
ID and same-effective-part overlaps among admitted rows. Master duplicates
were not collapsed or screened out.

### Exact reproduction failed; all disagreements preserved

The post-freeze [comparison](proximity-comparison01.json) completed at exit 1
with status `FAIL_EXACT_REPRODUCTION`, SHA
`17c43652a02a8685d12e9ff0f49d9548678989a5a8157ca2f2fc39202e21221a`.
This is a completed comparison with retained disagreements, not an interrupted
or malformed calculation. [compare_proximity.py](compare_proximity.py) SHA:
`c5bf5392d85c3abb9d05ee499e97f58d2b4dbce94a401096d35b61ff595c10e2`.
Twelve comparison controls passed; the 35 independent and 15 root producer
controls were actually rerun and passed. All 26 root array fields were
covered. Both root repeats produce the same comparison; their NPZ bytes are
identical. The full class and projection disagreement records retain exact
pair keys and source locators where relevant. No producer, threshold, epsilon,
face order, inversion or class was changed to obtain agreement.

The exact admission masks, IDs, same-node/same-part flags, part-incidence
joins, source references and geometry warning flags agree. Every finite
numeric field is within its prospectively approved, dimension-specific
comparison tolerance. The original and extended distance-field tolerance is
epsilon = 9.4869e−9. Dimensionless matching tolerance is 1e−10; squared- and
fourth-power length-field tolerances use 1e−10 times the corresponding power
of max(1, longest original edge). The longest original edge is
0.32174000000000547, so those two numerical thresholds are also 1e−10 here.
These are comparison thresholds, not certified error bounds or physical
uncertainty. Zero relative tolerance was used.

Maximum differences are 2.842170943040401e−14 for dA/dB/L/U;
4.760636329592671e−13 for signed plane distance; 3.602673714908633e−14
for geometric lengths; 8.701372955499664e−15 for cross-norm quantities;
1.4953316362920077e−15 for raw Jacobian dot products; and
1.201816424156732e−14 for unit normals. Supplied threshold ranges and original
diagonals agree exactly. Undefined positions match.

Despite those small numeric differences, **518 admitted-row classifications
and 77 projection flags disagree**. The projection disagreements affect 48
distinct setting/master/node rows: 52 flags are independent0/root1, and 25
are independent1/root0. The class differences all accompany a changed
boolean test for L>U. Independent/root positive inversion counts are 311/325;
their largest positive inversions are 1.8318679906315083e−15 and
2.7755575615628914e−17 respectively. All independent class2 rows coincide
with those small inversions in this evaluation.

| Class | Independent rows | Root rows |
| --- | ---: | ---: |
| 0 — unknown thickness | 8,520 | 8,520 |
| 1 — outside high gate | 36 | 76 |
| 2 — unresolved, including inversion rule | 311 | 325 |
| 3 — inside low gate | 2,425 | 2,371 |

Of the 518 class disagreements, 472 are class2/class3 changes and 46 are
class1/class2 changes. Thus even the combined class2-or-class3 membership is
not exactly reproduced. The 582 differing per-master coverage-count cells
follow from these classifications. The class2 label here must not be described
as evidence of physical thickness sensitivity, changing contact, uncertain
restraint, or a robust contact-candidate map. Apparent extension sensitivity
in these discrete classes cannot be separated from the preserved floating
inversion artifact by this run alone.

The parent's [comparison-consumer replay](proximity-comparison-root01.json)
completed at the same expected exit 1, SHA
`3ae497db581bf158d24b3e2a26498eb8180017ec5bf5ab52db0cea043c677e88`.
I compared the complete JSON objects directly. Exactly five leaf values differ:
command[0] (relative executable path), command[2] (output filename), elapsed
seconds (0.532636541989632 versus 0.5583264169981703), peak bytes
(289,210,368 versus 295,075,840), and the root control runner's stderr hash.
All comparison results, input pins, control counts/status/stdout hashes and
retained discrepancies agree exactly. The root control runner is Python
unittest; inspected code and a fresh 15-test PASS confirm that its stderr
contains elapsed test time. The two earlier stderr bodies were not retained,
so their differing hashes are explicitly excluded, not asserted to represent
byte-identical diagnostics. No scientific result was excluded.

The exact-arithmetic follow-up is separate work, not a reason to overwrite
or relabel this completed failed exact-reproduction result. The first-stage
source/topology PASS above remains valid within its own scope.

## Separate exact-binary-rational follow-up

The [exact follow-up addendum](EXACT-ARITHMETIC-ADDENDUM.md), final prospective
SHA `b02c1e3c08c8ab976cafba990088a4d80b06e7db9fea5d2d927fb7d0a9f8bb89`,
was read in full. I independently flagged the omitted epsilon in its original
broad-phase wording. Its appended correction was saved before historical
exact evaluation: both the global slab radius and the individual AABB radius
retain the original saved epsilon. The explicit norm/4 expression controls
the corrected wording about w. No source population, thickness, extension or
distance gate was changed based on results.

The independent exact implementation uses a rational Gram-system projection
and exact clamped edge distances. It does not import or inspect the separate
exact producer. Every original coordinate, supplied thickness and floating
constant is converted through its binary64 integer ratio, not its displayed
decimal string. The extended corners are recomputed rationally from original
corners. Dyadic square-root endpoints are certified by integer arithmetic.
Sorted coordinate searches use outward-converted slab bounds, exact slab
membership and exact point-to-AABB squared distances with the saved epsilon.
Unknown-thickness nodes remain universally admitted and class0. This is
arithmetic on parsed values, not proof of original-decimal precision, physical
measurement accuracy, effective solver thickness or contact initialization.

### Preserved unsuccessful attempts

The [first preflight receipt](independent-exact-preflight01.json), SHA
`8eff5b1c579457e1135ad22ba1e90c56932f9726c2c8038d8ffbb44964a9c19c`,
records an old method-pin rejection before any control or geometry evaluation.
The protocol was corrected while the independent core was being authored.
[That core](verify_exact_proximity-before-buffer-pin.py), SHA
`8691d11f63cd1d149f46cf6d5ab894dc20ce398844752b968e3aaeea787eb266`,
is preserved; this was not a failed mathematical control.

The [first 80-bit evaluation receipt](independent-exact80-01-failed.json), SHA
`09eb070cccd5a267096ee2f43cb87179358bea3c2f56fada6d81bee024e29313`,
records a memory-gate failure before result/NPZ saving, after the rational
geometry loops completed. Peak usage was 985,808,896 bytes against the
805,306,368-byte cap. The post-loop mask comparison unnecessarily unpacked
two complete bit arrays at once. [The failed version](verify_exact_proximity-before-mask-memory-fix.py),
SHA `1e0dd4d645d610861ac8ffa492754df29fea2bbccc8fbf47d0be215d19ed6cf6`,
is preserved. The correction counts differing bits one packed row at a time;
an added synthetic control compares it with full bit expansion. No rational
geometry or classification rule changed. Both failed receipts retain their
actual scope; the memory failure did not produce a complete frozen result.

### Completed independent results and precision validation

Final independent [verify_exact_proximity.py](verify_exact_proximity.py) SHA:
`c850bdb2e02843e4cbdf2c3cb08b309e25d47708d9fa7b1e41bc4dbe9d044e2f`.
Thirty-two controls passed before each evaluation, including closed triangle
interior/edge/vertex cases, winding reversal, degenerate planes, exact/inexact
square roots, outward conversion, known warped-patch points, extension-only
admission, unpruned synthetic broad-phase comparison, the epsilon boundary
band, unknown priority, interval overlap, duplicate masters and actual
create-only refusal. These are scoped controls, not an exhaustive solver test.

The unchanged code completed both declared fixed precisions:

| Precision | Result | SHA-256 | Seconds | Peak bytes |
| --- | --- | --- | ---: | ---: |
| 80 | [independent-exact80-02.json](independent-exact80-02.json) | `df8246830906ba20a814835d69f45c0196301ab76179e84b227c447d0352b11e` | 11.914289625012316 | 482,639,872 |
| 120 | [independent-exact120-01.json](independent-exact120-01.json) | `ecbde1063f26bbc520fdbae40209c88c5e433542eee97c6e92b212dc08ffab62` | 11.80598608404398 | 492,158,976 |

Both [80-bit NPZ](independent-exact80-02.npz) and
[120-bit NPZ](independent-exact120-01.npz) are byte-identical, SHA
`6c4bf3e3bdfeb00c14ef859407c7d685c950123a415a49452e4058e0aecbd8a4`.
Original stage arrays remain the source dependencies, without a new raw mesh
scan. All before/after input and code pins match.

The separate post-freeze [precision/certificate consumer](compare_exact_proximity.py),
SHA `9854b4d2df68ae14b03a834539c79163a66961407c0cee193ace2361f9edd7e3`,
completed [independent-exact-precision01.json](independent-exact-precision01.json),
SHA `1dc00626509d236a01953836120d4422b1bfbacce6939576f0189115a61a2caf`.
Fourteen mutation/boundary controls pass. All 12 numeric arrays and 42,851,509
array slots compare exactly between precisions. Each precision retains 11,292
pair certificates and 2,226 master/setting geometry certificates. Per precision,
the consumer checks 33,876 dyadic square-root certificates, 5,544 supplied
threshold intervals, all classifications, source locators/coordinates,
master thickness ranges, exact corner extensions and exact AABB scalars.
All 95,880 pair interval-nesting checks pass from 80 to 120 bits. Its own peak
was 587,874,304 bytes and elapsed time 5.879603417008184 seconds.

This consumer is an internal certificate/source and precision check; it does
not replace independent triangle-distance reproduction by the separate
implementation. The subsequent cross-implementation check is recorded below.
My exact code and both first completed precision results were frozen before
viewing the separate exact producer or its results.

At both precisions and all three settings, CID1 has 3,156 admitted rows with
class counts [2,840 unknown, 28 outside-high, 0 unresolved, 288 inside-low];
CID2 has 608 admitted rows, all inside-low. Across settings the totals are
[8,520, 84, 0, 2,688]. Exact broad-phase masks match the independent frozen
floating masks, covering all 338,488,050 declared combinations; same-node
and same-effective-part counts remain zero. There is no remaining class2
in this exact evaluation, not evidence that physical uncertainty vanished.
The 8,520 class0 rows remain the deliberately unfiltered four no-shell nodes,
not certified close pairs. Source-inspired thresholds and extension settings
remain declared sensitivity scenarios, not proven effective solver choices.

### Full independent exact comparison passed at both precisions

After the independent results froze and the separate reference froze, I read
all 546 lines of [exact_proximity.py](exact_proximity.py), SHA
`032804acb5862b6202d7037b864b2421c10b0f8383b0f2382a856810423dc25f`.
The reference uses oriented cross-products and three closed-edge distances;
the independent producer uses exact Gram barycentric projection. They share
the declared geometric definitions and fixed dyadic square-root construction,
not a geometric implementation. Their source extraction dependencies were
independently compared in the first stage. The reference's 12 synthetic
groups are source-inspected here; its retained execution and parent repeat
report all 12 passed. They were not a third blind source extraction.

The reference artifacts compared were:

| Precision | Reference receipt SHA-256 | Rational proof SHA-256 |
| --- | --- | --- |
| 80 | [exact-proximity80.json](exact-proximity80.json), `25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324` | [proofs](exact-proximity80-proofs.json), `53757ba19edeeacf7ec64222786344977cb02eef5d54d7da2cbae0445e4bd2e6` |
| 120 | [exact-proximity120.json](exact-proximity120.json), `ec72208fb65f7a849efebae77af5c834c4eb17e1180dddca2f1a17fb525d0711` | [proofs](exact-proximity120-proofs.json), `f653b0d0d4e69bfd42a79bb1321e540c4a18a92bdaa99efd3540bccc13fe80e7` |

Both reference NPZ archives have SHA
`79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628`.
The post-schema [comparison adapter](compare_exact_reference.py), current SHA
`d3f0640a73f95001ce8a0ec8115243fd3362cae16c879de86b77cf66bbc06dcc`,
imports only the pinned independent certificate consumer, never either
geometric producer. Its 12 mutation controls detect changed identity order,
proof keys, canonical fractions, unknown/null coercion, classes, projections,
mask bits, float views and undefined positions. Its initial 80-bit version is
preserved as [compare_exact_reference-before-120-pins.py](compare_exact_reference-before-120-pins.py),
SHA `7a2dc840bad20c748e6056b8d45ba79fdd3cb1320a06577113888417b0ec32be`.
Adding the newly frozen 120-bit pins and the actual 80-bit replay check did
not change the comparison mathematics or frozen producer artifacts.

The completed full comparisons are:

| Precision | Comparison receipt | SHA-256 | Seconds | Peak bytes |
| --- | --- | --- | ---: | ---: |
| 80 | [independent-exact-reference80-01.json](independent-exact-reference80-01.json) | `98a4d00dd76241c44345c6b0fab01c0b5ffe710bc17778528cc845708d7e071f` | 6.659480125061236 | 595,181,568 |
| 120 | [independent-exact-reference120-01.json](independent-exact-reference120-01.json) | `d489f6e99ce1ae09b248e84fe534c826a9209974bcdc628b715ed9e7de3d1c95` | 7.102561041945592 | 621,068,288 |

At each precision, all 14 reference arrays and 42,881,618 array slots compare
exactly, including complete-population masks, ordered master nodes, source
identity columns, classes, projection flags, incidence joins and declared
float views. All 11,292 pair proof records and 2,226 geometry proof records
compare exactly as canonical rational numerator/denominator strings.
The squared distances, square-root endpoints, patch enclosure, low/high
thresholds, signed plane intervals and exact AABB scalar are all covered.
There is no numerical tolerance in this comparison. Float arrays match their
declared midpoint/endpoint conversion exactly; these ordinary float views
must not be mistaken for outward-rounded floating certificates.

The recursive comparison counts at each precision are 49,699 numeric leaves,
495,165 strings, 17,040 nulls and four booleans. These count checked fields,
including source pins and repeated rational encodings, not independent
observations. Pair order is normalized by exact setting/master/NID keys;
classes, repeated master records and ordered corner slots are not dropped.
Reference per-CID class totals and unique nodes by class are also reproduced.
In CID1, a node can be outside one master and inside another; the 28 outside
node IDs and 122 inside node IDs are not disjoint populations.

Two extra schema-dependent checks are explicitly post-freeze verification,
not blind discovery. The reference retains both original squared diagonals;
the independent result retained their minimum, so both were recomputed from
the frozen original coordinates. The reference slab counter includes all
population nodes inside the outward floating search bounds; the independent
counter includes known nodes satisfying the exact rational slabs. The adapter
independently applies the reference's counter definition to the complete
frozen coordinates rather than equating different meanings. There are no
actual counter differences here: 3,603 slab memberships, zero box-interval
ambiguities and 1,189 source-node IDs entering the reference coordinate cache
are reproduced. Complete admission masks also match both earlier floating
implementations. None of this verifies an LS-DYNA contact search.

The adapter also compared the parent's actual reference 80-bit repeat,
[exact-proximity80-root01.json](exact-proximity80-root01.json), SHA
`60e12bb8f70944cb0c8996e7a1e8387c3405de7e5b341e5d6bfd2c84e08843f3`.
Only the output-stem command field, NPZ/proof filenames, elapsed seconds
(11.135433416930027 versus 11.31415679201018) and peak bytes
(736,985,088 versus 745,848,832) differ. Every other receipt field matches;
freshly hashed NPZ/proof bytes are identical. The reference records memory
usage but does not implement a memory-cap rejection: these two recorded
peaks are below 768 MiB, which is observed compliance, not an enforced guard.
The independent producer and comparison consumers do enforce their own
768 MiB gates. The parent's separate reruns of this comparison adapter are
pending and are not implied by the verified reference-producer replay.

Disposition: exact arithmetic and cross-implementation reproducibility are
established for this fixed parsed-input surrogate. The earlier floating
comparison remains a preserved failed exact reproduction. Its class2 artifact
has been resolved arithmetically here without tuning a physical input, not
converted into evidence that physical thickness, actual contact pairing,
restraint, connection capacity or collapse cause is known.
