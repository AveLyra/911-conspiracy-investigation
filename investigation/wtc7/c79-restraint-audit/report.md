# Column 79 residual restraint in the published account and released inputs

The accessible records support a more specific question than whether Column 79
was simply connected or disconnected. NIST's published account retains some
direction-dependent support at its calculated buckling initiation. The released
geometry separately identifies shared-node connections and tied-contact
definitions involving the mesh region labeled Column 79. These are positive,
checkable findings about the account and inputs. They do not establish the
remaining restraint's strength, its state during a historical simulation, or
the actual building's stability.[^1][^2][^3]

This research-only audit addresses Q06 and Q10 under the
[investigation charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md).
It distinguishes published model states, released input definitions, derived
topology and physical inference. It does not execute a solver, supply missing
properties, or identify a collapse cause. The [validation record](validation.md)
documents reproduction, failures and the limits of computational review.

## Published support state

At the reported Column 79 buckling initiation, NIST says the north girders
between Columns 44 and 79 remained seated at Floors 8–12 and 14, although their
erection bolts had failed. The prose describes possible resistance to northward
Column 79 movement, but not east, west or south movement from those girders.
At Floor 14, a separate girder between Columns 79 and 76 remained attached on
the west. Its location and reported restraint do not specify a one-sided
westward-only force law.[^1][^2]

| Floors in the Column 79 diagram | Published support classification | Qualification that must survive interpretation |
|---|---|---|
| 2–3 | Full | No numerical directional stiffness or capacity is supplied. |
| 4–5 | Partial | Not a statement of half capacity; direction and mechanism are unresolved here. |
| 6–7 | No support | A diagram classification, not independently verified reaction or stiffness data. |
| 8–12 | No-support color, with explicit north-only lateral-restraint and vertical-support annotation | The north seats are retained; prose says they possibly resist northward movement. |
| 13 | No support | Not in the retained north-girder list. |
| 14 | Partial | Retained north girder plus attached west girder; neither contribution is quantified. |
| 15–18 | Full | Qualitative upper support class, not an authenticated boundary condition for a new calculation. |

The table summarizes NCSTAR 1-9 Figure 12-44 and the Column 79 panel of
NCSTAR 1-9A Figure 4-17. The complete [source matrix](source-review.md) preserves
each floor, direction and qualification. In particular, the red legend, the
affirmative north-only annotation and the prose's possible resistance are not
silently reconciled into zero stiffness or an intact bilateral connection.[^1][^2]

The reported initiation time is −1.3 (14.7) seconds: collapse-reference time
followed by calculation-reference time. NIST aligns the east-penthouse kink
with calculation time 16.0 seconds. This does not independently observe an
interior column failure 1.3 seconds before that kink. Figure 12-43's cutaway
instead depicts −0.5 (15.5) seconds; Figure 4-17's three columns are each shown
at their own initiation times. They must not be combined into one simultaneous
support census. Some framing was hidden for display, not thereby deleted from
the simulation, and resultant-displacement colors do not supply motion sign.[^1][^2]

There is an affirmative reason to distinguish bolt failure from all support
loss: NIST describes the north-side seat/stiffener/clip arrangement as shell
plates tied to the column, with separate discrete bolt elements. Damage to a
seated connection is described as removal of specified failed-bolt elements
and application of seat/clip damage. A failed bolt and a lost bearing/contact
surface are therefore different modeled events, not synonyms. This description
does not identify the corresponding released element IDs or their state.[^2]

The published 3.5-hour damage case reportedly did not buckle the interior
columns, unlike the 4.0-hour case under otherwise similar loading. That is
relevant counterevidence to treating every modeled damage state as inevitably
unstable. It is not a reproduced no-collapse run or proof that either input
state describes the historical exposure.[^1]

## What the released geometry identifies

The source-input path is a normalized diagnostic label → part-set reference →
listed part → elements → nodes. Master-source lines 614–617 define the diagnostic
associated with Column 79 and part set 179; the set at lines 611–613 lists
effective part 179. This is an author-attributed model association, not a guess
that part 79 is Column 79 and not an original-drawing identification of the
whole architectural column.[^3]

The three geometry streams were read completely. The outside-region include
has its explicit +1000 part/material/section transformation; node, element and
set IDs remain unchanged under the admitted include transformation. The thermal
include is recognized but not reinterpreted here. Candidate damage lists are
not activated. The [first protocol](PROTOCOL.md) separates direct node incidence
from every stronger assertion about transfer or restraint.

| Selected input feature | Independently reproduced result |
|---|---:|
| Part 179 seed shells | 952 |
| Distinct seed nodes | 873 |
| Outside-seed elements sharing seed nodes | 20 shells, all outside-include effective part 1179 |
| Distinct seed nodes shared with those neighbors | 18 |
| Unique coordinate points retained for seed and neighbors | 891 |
| Direct beam, discrete or solid neighbors | 0 |

The 18 shared seed nodes occur at exactly two supplied Z values: nine at
−71.1708 and nine at −43.6118, also the seed region's minimum and maximum Z.
These are model-coordinate end planes, not authenticated story elevations or
effective bracing lengths. The seed bounds are X 13.13262…13.77258,
Y 2.408667…3.077733 and Z −71.1708…−43.6118. No length unit or architectural
floor label is assigned by this audit. The relevant section/material references
resolve to SEC179/MID99 for part 179 and SEC1179/MID1179 for part 1179; locating
definitions does not validate their physical capacities.[^3]

The zero direct beam/discrete-neighbor count does **not** establish absence of
floor or bolt connections. Different node identifiers can be connected through
contact or other coupling definitions. Even shared node incidence alone does
not establish adequate restraint. Those limitations prompted the separately
declared [typed-contact extension](CONTACT-TRACE-PROTOCOL.md).

## Contact definitions omitted by a shared-node-only graph

The released master contains 85 part sets, two node sets and six segment sets.
All 93 sets were retained in the comparison, including 88 without intersection
with the selected seed. Three part sets contain part 179; two segment sets
contain selected seed nodes. Neither node set contains a seed node. The last
fact is not absence of tied contact: the seed appears on the **master** side
of the two relevant tied-contact definitions.[^3]

| Contact ID and variant | Slave selector | Master selector | Relationship to selected Column 79 seed |
|---|---|---|---|
| 1 — tied shell-edge to surface, ID/OFFSET | Node set 1 | Segment set 1 | 710 master segment records intersect seed nodes. |
| 2 — tied surface to surface, ID/OFFSET | Segment set 2 | Segment set 3 | 32 master segment records intersect seed nodes. |
| 3 — automatic single surface, ID | Part set 1 | Not applicable | Part set includes part 179. |
| 4 — tied surface to surface, ID/OFFSET | Segment set 4 | Segment set 5 | No seed intersection. |
| 5 — tied shell-edge to surface, ID/OFFSET | Node set 2 | Segment set 6 | No seed intersection. |
| 9 — automatic single surface, ID | Part set 2 | Not applicable | No seed intersection. |

These are six input definitions, not six demonstrated connections to Column 79.
The 12 selector records comprise ten resolved typed-set references and two
not-applicable single-surface master fields. Contact IDs need not be consecutive.
All 36 numeric cards after the six ID headings are retained, with their blank
positions; no omitted option is silently filled with a physical assumption.

The selected segment counts also need a definition. They count membership
records intersecting any seed node, not distinct initialized contact pairs:

| Segment set | All records | Unique ordered four-node tuples | Distinct seed nodes in selected records | Selected records | Exact ordered seed-shell matches | Same unordered node-set matches |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 883,899 | 883,881 | 702 | 710 | 420 | 700 |
| 3 | 15,216 | 15,212 | 96 | 32 | 16 | 32 |

All 742 selected records preserve ordered vertices, attributes, source lines
and seed intersections. An unordered match is not an orientation-equivalent
contact face; those match counts are not pooled or upgraded into pair counts.
Set 2 also has 48 extra ordered-node tuples beyond unique tuples; set 1 has
18 and set 3 has four. These are duplicate ordered-node records, not demonstrated
duplicate forces, errors, or full attribute-row duplication. The other three
segment sets have no such ordered-tuple duplicates.[^3]

## Supplied deletion candidates and this exact mesh region

The candidate lists do not select the 952 seed shells or their 20 direct
same-node neighbors. The set 2 list's 1,543 shell candidates, six explicit
beam candidates and 355 discrete-element numeric counterparts have no shared
seed nodes either. The last pool remains a cross-family numeric match to a
beam list, not established discrete-deletion semantics. The separately read
Case A list has 45,152 unique shell IDs, none in the complete seed/direct-neighbor
graph.[^5]

The set 2 test reuses the prior independently verified member-map records;
the Case A extension freshly reads the small candidate list and joins typed
IDs to the complete frozen graph. Case A's zero shared-node-incidence result
is conditional on that graph's verified coverage, not a fresh reconstruction
of all Case A geometry. Explicit zero results are retained. There were no
actual matching coordinates to compare in this join; that positive branch
has synthetic tests only.

This does not establish that the candidate damage has no effect on Column 79.
It excludes only the specified direct selection and shared-node relationships
to the selected region. Contact-mediated connections, other architectural
regions, load redistribution, damage transfer and historical activation are
not tested by this zero intersection. Nor does a filename or supplied list
establish that a collapse run applied it. The [candidate protocol](CANDIDATE-JOIN-PROTOCOL.md)
and [Case A extension](CASEA-ID-EXTENSION.md) preserve these distinctions.

## Mechanical interpretation and the remaining gap

The contemporary Version 971 manual describes plain OFFSET tied contacts as
penalty-based transfer, distinct from direct identical-node connections and
from other offset formulations. It also distinguishes translational and
rotational behavior; the presence of a tied surface does not justify assuming
an arbitrary moment restraint. Conversely, multiple translational force paths
can have an assembled rotational effect even without a direct rotational
constraint. Contact syntax permits option reordering, while
the placement of ID and ordinary data cards remains specified.[^4]

Successful tying is a separate geometric and initialization question. The
manual describes proximity criteria depending on thickness and master-segment
geometry, overrides and warnings for nodes left untied. Input set membership
is therefore insufficient to establish a realized pair, its gap/projection,
its transferred force, or continued restraint after deformation and damage.
The applicable executable/build and control settings also matter. No actual
pairing, distance threshold or penalty stiffness was computed here.[^4]

The independent [manual-method review](contact-method-review.md) identifies
specific thickness, spatial-filter, projection, stiffness, timing and output
dependencies. Its rules are not silently generalized to every contact variant.

This yields a specific testable bridge, rather than a generic invocation of
"coupling":

| Evidence layer | Present result | Still needed for the next inference |
|---|---|---|
| Published description | Retained north seats and Floor 14 west attachment | Release-specific floor/member/coordinate mapping. |
| Direct geometry | Seed, 20 same-node neighbors, exact coordinates | Identification of architectural extent and connected member roles. |
| Typed contact selection | Two tied master sets and one automatic-contact part selection involve the seed | Candidate slave geometry, orientation, thickness and applicable initialization/control rules. |
| Realized and surviving restraint | Not reconstructed | Initialized-pair/warning records; seat/clip/bolt state and deletion/failure times; directional force-displacement response. |
| Column stability and propagation | Not independently calculated here | Full section/splice/imperfection, axial load and changing restraint state; verified subsequent load paths and dynamics. |

Published global-model prose gives +Y as north, −Y as south, and X as east–west.
It does not, in the inspected selection, establish the positive X sign, origin,
floor-to-Z table or exact transformation to this released region. Unfollowed
source-page leads are listed in the [source review](source-review.md); this is
not a claim that such information exists nowhere.[^2]

The next available local test is to locate the slave-side geometry selected by
contacts 1 and 2 relative to the selected master records, then join candidate
seat/clip/member parts to their section/material and separately typed damage
records. Selection rules for proximity, projection, normals and duplicate
records must be declared before new calculations. Candidate geometry must
remain distinct from actual initialized pairs. No guessed spring law or
activated deletion can replace the historical state dependency.

That bridge should target the published C44–C79 north seats at Floors 8–12/14
and C79–C76 west attachment at Floor 14, while retaining the lower partial and
upper support classes. A single zero reaction would not establish zero
available stiffness. Conversely, a declared tied-contact surface would not
establish sufficient bracing. Both actual response and possible restoring
response depend on the member, load, deformation and contact state.

## Evidence-weighted disposition

| Claim | Type and strength | Reproduction / assumption | What would weaken it or test the next step |
|---|---|---|---|
| NIST describes residual, direction-dependent support rather than complete disconnection | Source observation A; underlying state remains model-dependent | Independently read complete source pages; source text is not historical measurement | Different governing run/state; actual response inconsistent with the described seat and west attachment. |
| The selected released region has the stated direct topology | Derived input result A within scope | Separate readers agree on IDs, connectivity and parsed coordinates; shared original bytes | A source/layout or namespace mismatch; an architectural crosswalk showing different scope. |
| Contact definitions add modeled transfer routes outside a same-node graph | Source-derived membership A; force inference unresolved | Separately extracted sets and cards agree; method is edition-specific | Applicable build/control or initialization evidence that excludes, changes or leaves candidate pairings under these definitions untied. |
| Remaining support was sufficient, or insufficient, to prevent buckling | Unresolved D | No quantified release-to-run directional restraint or full stability calculation | Authenticated geometry/state/constitutive chain and a verified stability/dynamic test. |
| These inputs establish fire initiation, deliberate intervention, or contrivance | Unsupported by this unit E | Input topology does not identify initiation or intent | Independent historical observations and mechanism-specific evidence, not another prescribed-removal replay. |

The strongest new correction cuts against an oversimplified skeptical argument:
absence of common node numbers does not mean modeled isolation, and NIST did not
describe loss of every support in every direction. The strongest unresolved
challenge to a validation claim remains equally concrete: input membership and
published qualitative support classes do not demonstrate the actual residual
restraint, its failure history or the proposed buckling-to-global-collapse
chain. This audit does not establish that either the fire or intervention
family is more likely. No causal ranking or legal finding is revised.

## Sources

[^1]: NIST, *NCSTAR 1-9, Structural Fire Response and Probable Collapse Sequence of World Trade Center Building 7* (2008), physical pages 638–641 / printed 572–575; preserved [PDF](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf). Hash and full-page inspection coverage: [source review](source-review.md).
[^2]: NIST, *NCSTAR 1-9A, Global Structural Analysis of the Response of World Trade Center Building 7 to Fires and Debris Impact Damage* (2008), physical pages 80, 110, 130, 132, 139 and 147 / printed 29, 59, 79, 81, 88 and 96; preserved [PDF](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf). The source arm additionally inspected physical 158/172; those separate cases are not substituted for the initiation state here.
[^3]: NIST supplementary production, preserved SRC-119–121 geometry files under [the supplied folder](</Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653/>). Exact source and line pins are in [root01.json](root01.json), [contacts-root01.json](contacts-root01.json), the independent outputs and [validation](validation.md). Integrity relative to produced bytes is not authentication of a historical executed deck.
[^4]: Livermore Software Technology Corporation, *LS-DYNA Keyword User's Manual*, Version 971, May 2007, contact/sets sections, especially physical pages 363–367, 370–371, 402–403, 1161, 1171 and 1174; [official-host copy](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf). The URL folder is not the edition date. Exact admitted copy SHA-256: f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d. This manual is not an authenticated historical executable or proof that every option applies unchanged to every variant.
[^5]: Preserved SRC-116/117 candidate lists, prior [run06 member map](../model-member-map/run06/member-map.json) and its verified source receipts, and the frozen direct graph. The [candidate join](candidate-join01.json) and [root replay](candidate-join-root01.json) distinguish retained-data reuse from a new complete SRC-117 list scan. No candidate was activated.
