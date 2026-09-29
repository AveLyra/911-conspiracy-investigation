# Column 79 contact geometry and restraint dependencies

Working research; the declared numerical unit is complete, with remaining
physical and evidentiary limits below. This does not identify the collapse
cause or establish the adequacy of Column 79's remaining support.

The released inputs contain inspectable geometric and contact information
that a shared-node-only graph cannot represent. Two independently written
readers reproduce the selected source coordinates, supplied thicknesses,
master faces and common part references exactly. This narrows the claim that
the relevant model is wholly unavailable, but does not establish initialized
contact pairs, force transfer or historical execution. A subsequent geometric
classification failed exact independent replication because of floating-point
boundary handling. A separately declared exact-arithmetic calculation now
reproduces across two implementations and two precisions. The failed floating
calculation remains preserved; it is not an anomaly in the building or evidence
of model manipulation.[^1][^2][^6]

## Physical question and scope

The physical question is whether the reported remaining seats and attachments
could have supplied enough directional restraint to affect Column 79's
instability. A connection's presence, local connector failure, continued
bearing/contact, loss of bracing and column instability are distinct events.
None can be inferred merely by counting shared mesh nodes or looking at a
schematic of a connection. The preceding [restraint audit](../c79-restraint-audit/report.md)
located reported north-seat and west-attachment qualifications and the source
contact definitions. This unit follows their geometry and input dependencies,
not their unknown run-state force history.

The 742 selected master records were inherited from that prior audit: 710
from segment set1 for contact1 and 32 from segment set3 for contact2. Selection
was by intersection with the earlier seed region, not by proximity tuning.
The entire respective slave populations were then reconstructed; they cover
far more than the immediate Column 79 region. Global population totals below
must not be called counts of nearby connections or supporting members.[^1]

## Independently reproduced input geometry

| Input population | Unique nodes | Nodes without shell incidence | Nodes with differing incident corner thickness | Supplied corner-thickness extrema |
|---|---:|---:|---:|---|
| Contact1 slave node set1 | 152,977 | 4 | 11,187 | 0.004763–0.127 |
| Contact2 slave segment set2 vertices | 131,740 | 0 | 0 | 0.01803–0.1692 |

Values remain in the supplied coordinate/thickness convention; no physical
unit or floor label is assigned here. The four no-shell nodes each have one
beam endpoint incidence. They are not unsupported nodes, and absence of a
shell is not a license to assign zero effective contact thickness. Differing
incident corner values likewise are source data, not necessarily an error.

All 742 selected master records have one unordered four-node shell alias.
Of these, 442 match the same order and 300 use a different order. Every actual
master and alias has four distinct vertices, so the two readers' set-versus-
multiset normalizations are equivalent for this data, not in general. Their
783 distinct vertices all resolve to coordinates. Segment set1's aliases
include 700 records from effective part179 and ten from part1179; segment
set3's 32 aliases are in part179. Repeated face records are retained rather
than treated as independent physical interfaces.

The selected-node union contains 285,500 nodes. All 11 common numeric arrays,
742 master metadata records and 119 common part references match exactly
between implementations. The root's two array archives are byte-identical;
the fresh comparison-consumer replay agrees. This is parsed-input numerical
verification, not historical authentication or physical validation. Full
section-property cards and several implementation-specific extras remain
outside dual verification as listed in the [independent review](independent-review.md).

## Actual controls and their limits

The global control block is present, not generically unavailable. Separate
extractions agree on its source, two numeric card locations and all sixteen
numeric fields. Its explicit values include SLSFAC=.1, PENOPT=1, ISLCHK=1,
ORIEN=1 and TIEDPRJ=0. Six contact blocks are preserved; the declared lexical
scan found no PART_CONTACT block in the three complete geometry streams.
These are source-input findings, not effective-state findings.[^3]

The selected definitions are tied-shell-edge-to-surface OFFSET and tied-
surface-to-surface OFFSET. The contemporary Version 971 manual describes
penalty-based attachment and a thickness/diagonal-dependent closeness test.
Its option qualifications matter: the local IGNORE=1 description concerns
automatic contacts, so that field does not demonstrate ignored penetration
or skipped projection in these plain ties. Likewise, numeric zero in a
contact card does not by itself establish zero stiffness, zero thickness or
an inactive contact. Explicit orientation of segment faces must be retained;
the global ORIEN=1 description covers automatic part input, not demonstrated
reorientation of these explicit segment records.[^4]

The geometric diagnostic uses an unextended baseline of 1 and manual-
motivated search extensions of 1.006 and 1.025. It treats these as declared sensitivity
settings, not authenticated historical defaults. Supplied corner-thickness
minima/maxima are also scenarios, not proven bounds on the solver's effective
nodal thickness. Actual aggregation, projection, competing-face selection,
initialization and state histories remain necessary before interpreting a
geometrically close node as a force-carrying interface.

## Geometric test and failed floating replication

The [declared method](GEOMETRIC-METHOD.md) evaluates every slave–selected-
master combination at each setting, retaining every broad-phase mask and
all admitted rows. It evaluates both quad triangulations and bounds their
distance from the bilinear patch using the mixed-corner term. The
[independent mathematical review](geometry-method-review.md) verifies that
bound in exact arithmetic; it does not certify floating-point evaluation or
solver applicability. No normal, same-ID, same-part or nearest-neighbor
filter selects a preferred connection.

Each setting examines 108,613,670 contact1 combinations and 4,215,680 contact2
combinations: 338,488,050 across three settings. Both implementations retain
identical masks: 3,156 contact1 rows and 608 contact2 rows per setting.
The total 11,292 includes 8,520 deliberately retained unknown-thickness
rows, because the same four beam-connected nodes are carried through every
contact1 master and setting. These row counts are repeated computations,
not numbers of physical connections.

The complete comparison is **FAIL_EXACT_REPRODUCTION**, with 518 class
disagreements and 77 plane-projection-flag disagreements. Distances agree
within the predeclared numerical comparison thresholds, but that is not
enough to pass exact classification. All class disagreements accompany a
change in whether the computed distance enclosure is slightly inverted.
Of them, 472 exchange inside and unresolved status; 46 exchange outside
and unresolved status. Therefore even the floating inside-or-unresolved
membership is not independently reproduced.[^2]

All 325 root unresolved rows are tiny numerical inversions, not observed
thickness-sensitive connections. The root's maximum inversion is
2.7755575615628914e-17; the independent calculation's is approximately
1.83e-15. The declared safeguard retained these rows instead of silently
clamping the bounds. Apparent extension-dependent changes in those class
counts must not be interpreted as real changes in candidate connections.
The original code and outputs remain frozen.

## Exact-arithmetic resolution

The [prospective follow-up](EXACT-ARITHMETIC-ADDENDUM.md) holds the frozen
parsed numeric inputs and geometric rules fixed while replacing approximate
evaluation with binary-rational arithmetic and outward square-root intervals.
Two implementations use different triangle-distance constructions and
recompute the complete-population broad phase. Their classes, projection
flags, masks and rational certificates match exactly at both fixed precisions,
80 and 120 bits. The primary calculation's repeat is byte-identical for its
array and proof products; fresh comparison-consumer replays also pass.[^6]

| Contact | Unknown-thickness rows | Outside-high rows | Unresolved rows | Inside-low rows | Unique inside-low nodes |
|---|---:|---:|---:|---:|---:|
| 1, each setting | 2,840 | 28 | 0 | 288 | 122 |
| 2, each setting | 0 | 0 | 0 | 608 | 280 |

These are node–master rows, not unique connections. The same node can be
inside one master and outside another. Unknown-thickness rows deliberately
retain four nodes regardless of distance; they are not certified close
pairs. All exact broad-phase masks match both frozen floating masks. The
corrected classes show no change across the three declared extensions and
no known-thickness interval ambiguity in this evaluation. This resolves the
specific numerical disagreement; it does not establish the historical
effective thickness or eliminate physical uncertainty.

Exactness applies to the stored binary numbers and declared surrogate, not
unrounded source decimals, physical measurement accuracy or LS-DYNA's actual
contact initialization. The independent certificate comparisons cover all
11,292 admitted pair proofs and 2,226 master/setting geometry proofs, not a
sample. Their large array-slot counts include packed coverage and repeated
computations, not independent observations.

## Contact candidates and supplied damage-list membership

The [prospective typed join](CONTACT-DAMAGE-JOIN-PROTOCOL.md) expands the
earlier exact shared-node question to geometrically eligible slave nodes.
It reconciles all 1,904 supplied candidate element records between two
frozen derivatives: 1,543 shells, six explicit beams and 355 discrete
elements whose numeric IDs occur in the beam list. Physical node IDs,
source locations, effective/original parts and requested/actual element
families must agree. Every matched node's coordinate must equal the frozen
stage coordinate. Beam orientation references are not endpoints.[^7]

The independently written joins agree on the following at every declared
extension. The complete comparison and fresh root consumer cover all result
fields, not only matching totals; both producers' repeats also agree.

| Contact/class and element family | Matching typed elements | Unique matched nodes | Node–master–element relations |
|---|---:|---:|---:|
| Contact1, inside-low, shell | 9 | 12 | 36 |
| Contact1, inside-low, discrete numeric beam-list candidates | 17 | 17 | 20 |
| Contact1, inside-low, explicit beam | 0 | 0 | 0 |
| Contact2, inside-low, each of the three families | 0 | 0 | 0 |
| Either contact, unresolved or unknown-thickness, each family | 0 | 0 | 0 |

All 54 setting/contact/class/family groups are retained, including zeros.
The 78 match rows across settings repeat the same 26 typed elements; they
are not 78 distinct damaged elements. No selected master shell alias itself
appears in these typed lists. The nine matching shells belong to effective
part803; the discrete matches belong to parts820, 821 and 859. These are
numeric/source joins, not identifications of particular seats, floors or
physical supporting members. Counts across families can share node IDs and
must not be added as unique nodes.

This positive geometric expansion does not contradict the older direct-graph
zero: the earlier question expressly excluded contacts between distinct node
IDs. It does prevent extending that zero to all possible contact-mediated
relationships. Conversely, none of the 17 discrete matches establishes that
a beam-list keyword would delete a discrete element; requested and actual
families remain separate. The supplied list is static input, not proof of
activation, removal, support loss or a historical event. The separate CaseA
contact-mediated expansion remains unperformed.

## Candidate part and material dependencies

A post-result descriptive summary retains all 18 setting/contact/class
groups and every selected typed-part entry, including zero entries. It
maps 406 distinct candidate nodes to 14 typed parts. Four of those nodes
are the unknown-thickness beam-connected nodes; 402 are inside-low nodes
in the two contacts. Class1 rows are excluded from the summary's selected
groups; selected nodes with outside-class1 relationships are explicitly
reconciled, and the complete exact output retains those rows. The summary
uses the independently checked
frozen incidence/reference data; it is not a fresh raw-source reconstruction.[^8]

Two candidate shell parts reference material definitions absent from the
frozen registry: part773/material773 has 21 inside-low nodes, and
part803/material803 has 28. Part803 is also the part containing all nine
matching listed shells above. This connects a previously identified
missing-property dependency to the newly calculated candidate geometry;
it does not establish that those shell elements represent a particular
seat, floor or historical failure. Part and section definitions are present
for all 14 selected typed parts. A supplied part or section alone does not
replace an absent material law.

The three matched discrete parts820/821/859 reference supplied
`MAT_SPRING_NONLINEAR_ELASTIC` definitions. That type identification neither
supplies their full force–displacement curves in this summary nor verifies
units, failure/release semantics or state. The frozen reference schema
retains material presence/type but not material-definition source lines;
those locators and dependent curves require the separate material/source
records. Present definitions must not be described as withheld simply
because this summary does not expand their cards. Conversely, a transformed
same-number material elsewhere is not automatically a substitute for the
missing effective reference.

## Connection drawings and coordinate attribution

NIST's published C79/C81 seated-connection description separates top-clip,
bolt and weld failure from subsequent walk-off and loss of vertical support.
It represents slip and later beam-to-column contact with an initial gap.
Figure11-15 identifies local member and vertical axes; its published travel
assumptions are not proximity tolerances for the released global deck.
Similarly, the shear-stud model distinguishes shear failure from continuing
slab-to-beam gravity contact.[^5]

Figure11-9 supports eastward X and northward Y for the illustrated ANSYS
plan. Section11.2.7 explicitly identifies global z as vertical in that
ANSYS model. These are positive source mappings, not an authenticated
transfer to released LS-DYNA IDs, absolute elevations or units. The bounded
16-page source review found no floor-to-Z or physical-member-to-PID179
crosswalk in its selection. It does not establish that such a mapping is
absent from every report, drawing or production. The ANSYS local-initiation
model's stated simplifications must not be misattributed to the entire
LS-DYNA global model.[^5]

## Claim ledger and remaining discriminator

| Claim | Evidence layer and grade | Best countercheck or limit |
|---|---|---|
| Selected source geometry and common references reproduce | Parsed-input calculation, A within declared coverage | Source rehash failure, independently inconsistent values or unverified historical release identity |
| The four no-shell nodes have beam connections | Parsed element incidence, A | Does not establish stiffness, effective thickness or support adequacy |
| The sources define candidate attachment mechanisms beyond shared nodes | Source-input observation and manual interpretation, B | Actual initialization, direction, material law and surviving force remain unobserved |
| Floating geometric classifications reproduce exactly | Contradicted, E | 518 retained class disagreements; tolerance-level distance agreement is insufficient |
| Unresolved floating rows demonstrate physical thickness sensitivity | Unsupported, E | All root unresolved rows arise from arithmetic inversion |
| Fixed-input exact geometric classes and certificates reproduce | Derived calculation, A within the surrogate | Both precisions and implementations agree; effective historical contact algorithm remains unverified |
| Candidate contact nodes overlap supplied set2 elements | Independently reproduced static join, A within declared coverage | Nine shells and 17 discrete numeric beam-list candidates; no activation or complete-support-loss conclusion |
| Candidate shell parts773/803 lack referenced material definitions in the frozen registry | Source-dependent derived association, A within that inventory | An authenticated matching effective material definition or resolved include/run dependency would close the gap; this is not evidence of deliberate omission |
| Connector failure necessarily removes all bearing/contact immediately | Not supported by the examined published connection model | The published model distinguishes failure, slip, contact and walk-off; this is not proof of historical survival |
| Remaining contact was sufficient, or insufficient, to prevent buckling | Underdetermined, D | Requires authenticated member mapping, initialized contact and run-specific force/state/material histories |

The exact arithmetic has resolved the computational ambiguity and the typed
join now has an independently reproduced positive result.
The analogous CaseA contact-mediated test remains separate and unperformed;
the older direct-node zero does not answer it. Remaining material-law details
and the specific member/floor/run mappings are necessary before
interpreting these candidate relationships mechanically.

Even a positive static join would not show that the listed elements were
deleted in the historical run or that deletion removed an entire restraint.
The decisive physical bridge remains a traceable member/floor-to-model
mapping, effective initialization and deformation/contact-force histories,
together with the relevant surviving material/connection properties. No
collapse-cause ranking, actor attribution or legal conclusion follows from
the current unit.

## Sources and reproducible artifacts

[^1]: Preserved SRC119–121 geometry sources and their full-stream receipts in
  [stage-root01.json](stage-root01.json), [stage-root02.json](stage-root02.json)
  and [independent-stage01.json](independent-stage01.json); exact comparison
  and consumer in [comparison01.json](comparison01.json) and
  [comparison-root01.json](comparison-root01.json). The canonical intake
  remains in the original repository; this unit does not create source IDs.
[^2]: Frozen [root proximity receipt](proximity-root01.json),
  [independent proximity receipt](independent-proximity01.json),
  [complete failed comparison](proximity-comparison01.json), and
  [pre-comparison implementation review](proximity-implementation-review.md).
  Its earlier "reproducible candidate-to-incidence map" characterization is
  superseded for class-dependent floating maps by the failed comparison above.
[^3]: [Control extraction](control-extraction01.json),
  [primary-method review](control-method-review.md), and the later common-field
  comparison in [implementation review](proximity-implementation-review.md).
[^4]: Livermore Software Technology Corporation, *LS-DYNA Keyword User's
  Manual*, Version971, May2007, physical363–375/394 (OFFSET, defaults and
  penalty qualifications), 395/402–403 (search and closeness),
  397/399 (option qualifications), 472–476 (global controls). Admitted copy
  SHA-256 `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`;
  [official distribution](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf).
  The URL directory date does not change the manual's edition.
[^5]: NIST, *NCSTAR1-9*, 2008, physical542/548–550, printed476/482–484,
  Figures11-9/11-15/11-16 and section11.2.7, in the
  [preserved PDF](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf).
  Complete selected-page coverage, limitations and source hashes are in the
  [independent source crosswalk](source-crosswalk-review.md).
[^6]: [Exact 80-bit result](exact-proximity80.json),
  [120-bit result](exact-proximity120.json),
  [80-bit repeat](exact-proximity80-root01.json),
  [independent implementation and comparison review](independent-review.md),
  and fresh [80-bit](independent-exact-reference80-root01.json) /
  [120-bit](independent-exact-reference120-root01.json) comparison consumers.
  [Validation](validation.md) records methods, failures and independence scope.
[^7]: [Root typed join](contact-damage01.json) and
  [repeat](contact-damage02.json), [independent join](independent-contact-damage01.json),
  and [fresh complete comparison](independent-contact-damage-comparison-root01.json),
  using source-pinned derivatives from the
  [member map](../model-member-map/report.md) and
  [prior typed-list audit](../c79-restraint-audit/report.md).
[^8]: [Post-result candidate/part summary](exact-parts01.json),
  [replay](exact-parts-root01.json), [summary code](summarize_exact_parts.py), and the preserved
  [material/run crosswalk](../material-run-crosswalk/report.md). The numeric
  registry is a derivative of the selected source inputs, not a complete
  historical property or contact-force archive.
