# Column 79 drawing/member-to-restraint crosswalk

2026-09-13. Research-only, retrospective source/identity audit under
[PROTOCOL](PROTOCOL.md). This closes the bounded crosswalk, not the structural
validation or the comprehensive investigation. See [validation](validation.md)
for actual inspection and review coverage.

## Result

The supplementary files yield real, reproducible column-label/part bridges;
they are not merely filenames. Published engineering sources also identify
specific connection behavior and drawing leads. **The join from each selected
floor's installed detail to its exact released seat/attachment elements is
still unresolved.** We have not measured those connections' surviving capacity.

This narrows the missing evidence. It does not show that NIST removed every
restraint, that the remaining restraints were adequate, or that the released
model reproduces the historical calculation. The [interim causal assessment](../causal-chain-synthesis/report.md)
stands: conditional mechanistic weight, but no independently established strict
probability ordering, equal odds, or intervention finding.

## 1. Which drawing is evidence of what?

NIST distinguishes Cantor design plans, Frankel erection plans and fabrication
shop details. It reports about 2,500 shop drawings used for connection modeling;
the shop set was not PE-sealed, contained 1985/1986 revisions and agreed with
renovation photographs from 1989-1990 on several floors. That is favorable
reported corroboration worth pursuing, not independent verification of the
specific seats here. An unsealed shop drawing is not thereby false.[^design]

The STC subsection additionally attributes the north-C79 connection type to
shop drawings and construction photographic evidence. We have not independently
matched those photographs to the selected floors.[^connection]

NCSTAR 1-9 Figure 2-20 and Figure 11-15 are explicitly schematic/analytical
derivatives. NCSTAR 1-9A Figure 3-22 reproduces a reduced S-8 plan fragment next
to a model plan, without a complete original title/revision block. The report
also describes floor-dependent member changes and automatic length adjustments
during TrueGrid generation. A typical-plan match does not settle every floor's
connection identity.[^plans]

The independent [drawing-source review](drawing-source-review.md) completed six
queries and six linked-resource attempts. It identifies concrete public-release
and member/detail leads but authenticates no complete original construction
sheet. The UAF 2017 presentation's page 39 attributes a section to Frankel 9114
and girder A2001; it is an inspectable technical depiction, not the complete
original sheet or proof that its detail applies to all selected floors.[^uaf]

NIST acknowledges Floor 10 modifications involving added studs, plates and
connection reinforcement that were not incorporated in its 16-story model,
citing incomplete revised load/connection information. Their applicability and
effect require a floor-specific check. [NIST FAQ, item 27](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation).

## 2. Version-aware dimensions and distinct physical roles

| Item | Preserved 2008 statement | June 2012 corrected attribution |
|---|---|---|
| Axial walk-off, printed p.482 | 6.25 in. | 5.5 in. |
| Lateral walk-off, printed p.482 | 5.5 in. | 6.25 in. |
| Seat width, printed p.527 | 11 in. | 12 in., citing Frankel 1091 |

The errata calls these typographical errors and says the correct dimensions
were used in the analyses. That is NIST's historical-use assertion, not a
solver-card audit performed here. April 2012 also changes the Chapter 8 plan
attribution from E12/13 to S-8. Preserve all three distinctions: original text,
corrected text, and the inputs actually used.[^errata]

The older [contact source-crosswalk note](../c79-contact-geometry/source-crosswalk-review.md)
correctly records the original p.482 but must not supply current corrected
dimensions without this qualification. Its earlier reading remains unchanged.

| Feature | What the inspected sources depict/model | What cannot be substituted for it |
|---|---|---|
| Column-side seat and plate | Bearing below the girder; shell seat/clip tied to column in the described LS-DYNA representation | Not the girder's own web stiffeners and not a measured post-damage capacity |
| Girder-web stiffeners | Partial-height plates on the girder depicted in UAF page 39's attributed detail | The column-side plate in a NIST schematic does not demonstrate that these different plates were included or omitted in every model |
| Top clip, seat bolts, weld and hole clearance | ANSYS explicitly separates bolt shear, slip, clip/weld failure, contact and walk-off; top holes are slotted, seat holes standard | Bolt failure is not itself loss of bearing; nor must every bolt and weld fail in every alternative failure path |
| Slab and shear studs | Separate slab/beam interaction; NIST describes continuing gravity contact after stud shear | A stud omission question is not resolved by showing unrelated bolts or a seat plate |
| Local connection axes | Figure 11-15 local x along the member away from the column, local z upward | Neither local axis is automatically the released model's global axis |

These are source/functional distinctions, not newly calculated capacities.
NCSTAR 1-9A p.29 describes a seat with a stiffener plate under the girder,
while Figure 3-12's caption calls the connection unstiffened. Preserve that terminology tension; settle
the actual components from original details, not the caption alone.[^connection]

## 3. Per-path correspondence and unresolved fields

All support states below are **reported model states**, not observations of
hidden connections. The common positive numeric bridge is Column 44 to
PID144, Column 76 to PID176, and Column 79 to PID179 through explicit source
diagnostics and part sets. These are selected shell regions, not necessarily
whole physical columns.[^numeric]

| Selected path | Reported state at C79 buckling | Drawing-specific issue | Exact released member/seat/attachment join |
|---|---|---|---|
| C44-C79, Floor 8 | North girder remains; possible northward resistance after bolt failure | Original floor/member/detail and revision not inspected | Unresolved; column regions identified only |
| C44-C79, Floor 9 | Same reported directional class | Same missing floor-specific chain; no identity inferred from Floor 8 | Unresolved |
| C44-C79, Floor 10 | Same reported directional class | Must reconcile floor modifications, not assume an unchanged typical floor | Unresolved |
| C44-C79, Floor 11 | Same reported directional class | E10/11 is an identified plan lead, not an inspected full sheet | Unresolved |
| C44-C79, Floor 12 | Same reported directional class | E12/13 lead does not prove identical details on both floors | Unresolved |
| C44-C79, Floor 14 | North girder remains; floor classed partial overall | Original floor-specific north detail and its revisions needed | Unresolved |
| C79-C76, Floor 14 | West girder remains attached; constraint from west | Its own member/end details needed, not A2001's north-end illustration | Unresolved; do not assign a knife-connection law by analogy |
| C44-C79, Floor 13 comparison | No support at this location in the initiation schematic | A2001/1091/9114 are specific retrieval leads, not authenticated installed or universal-floor details | No Floor 13-to-Z or member-to-element identity established |

NCSTAR 1-9A p.79 supplies the retained north-girder list and west attachment;
NCSTAR 1-9 p.573 expressly identifies that Floor 14 girder as C79-C76.
Figure 4-17 and NCSTAR 1-9 Figure 12-44 preserve the directional annotation.
Their red symbols at Floors 8-12 must not erase the accompanying north/vertical
support qualification. Floors 2-3 and 15-18 are classed full, 4-5 partial,
6-7 none, and 14 partial in the C79 panel. The three-column figure shows each
column at its own buckling initiation, not one simultaneous state.[^restraint]

The west connection deserves separate identification. NCSTAR 1-9 p.504 names
knife-connection tensile weld failures at C79 on Floors 10-12, attributed to
column motion driven by another floor's expansion. That is a specific modeled
load path, but it neither identifies the Floor 14 attachment's exact drawing
nor independently demonstrates the historical force history.[^west]

## 4. What the released data actually add

| Normalized source diagnostic | PSID / PID / SECID / MID | SRC121 PART numeric line | Shell region |
|---|---|---|---:|
| Column 44 | 144 /144 /144 /100 | 3072 | 624 shells |
| Column 76 | 176 /176 /176 /99 | 3488 | 944 shells |
| Column 79 | 179 /179 /179 /99 | 3527 | 952 shells |

MID99 and MID100 definitions are present at SRC121 keyword lines 2486/2496.
Their complete material bodies were not the selected exports in this review;
**do not call them missing laws**. The independent [numeric review](released-mapping-review.md)
records exact geometry, node/element/section/contact locators and all input pins.
Root separately checked the three diagnostic/set joins, part counts, envelopes,
PART references and material-presence entries in the frozen derivatives.

That review also checks 873 common seed/thermal node coordinates and 774 common
stage coordinates/source lines. These are consistency checks on related
derivatives, not separate historical witnesses. Zero PID144/176 incidence in
the selected contact-stage population does not mean the columns or girders were
disconnected. Candidate contacts are not initialized ties or surviving forces.

The part envelopes are qualitatively compatible with the published plan ordering:
C44's retained X/Y ranges exceed C79's, while C79's exceed C76's. This is a
limited geometric consistency observation, not an authenticated geographic
frame, unit scale, floor origin or coordinate transform. No center fit, floor
assignment, proximity rerun or force/stability calculation was made.

## 5. Claim ledger and discriminating next evidence

| Claim | Layer / strength | Support and replication | Alternative / falsifier or next discriminator |
|---|---|---|---|
| Source labels bridge to three actual released parts | Derived; A within the pinned streams | Member map supplies diagnostic/set associations; material crosswalk checks PART/property references; root inspected both | A parser/namespace error or changed bytes would weaken this; not an as-built claim |
| NIST reports shop-detail/photo agreement | Published assertion; A for attribution, ungraded for each installed target | Full primary pages; independent source reading | Retrieve location-specific photographs and applicable revisions; conflicts could narrow the reported agreement |
| Corrected dimensions equal historical active inputs | Historical inference; D here | Errata assertion only; no historical input/run reproduction | Inspect actual connection cards, APDL walk-off checks and run/version chain |
| Every selected floor had the same as-built north connection | Unestablished; D | Generic schematics and incomplete specific leads | Applicable erection/fabrication chain and Floor 10 modifications could confirm or disconfirm it |
| All resistance at C79 vanished before buckling | Contradicted as a description of the published model; E | Explicit retained directional/partial support | Actual directional reaction/state histories needed to quantify significance |
| Remaining restraint necessarily prevented, or necessarily permitted, buckling | Physical inference; D here | Static identity and published classifications do not establish capacity | Verified geometry, engagement, constitutive response, demand and dynamic state could discriminate |

**Next source task:** Inspect complete, version-identified original plan/detail
pages for one north seat and the Floor 14 west attachment, including both ends,
member marks, revisions and applicable modifications. The source review records
specific public packet leads and the exact unreviewed-payload boundary; it is
not an absence finding. Minimize acquisition/display to the technical target;
uncertain sensitivity still requires informed approval. Do not substitute a
held packet or retry a denied source through a mirror.

**Next numerical task after an admissible source join:** Establish units,
origin, signed axes and independent labeled control points; test any proposed
transform against unused controls. Match named end/seat nodes to the frozen
ordered mesh/contact records, expanding extraction only for identified missing
nodes. Then seek the actual initialized contacts, damaged connector state,
directional force/displacement histories and relevant material/curve/run
dependencies. A successful geometric match alone cannot decide stability.

The supplementary production remains incorporated, not complete by assumption.
This unit changes mapping precision and version control, not the current causal
ordering. No solver, Faraday audit, accepted Sherlock finding, legal promotion,
outreach, sensitive transmission, commit or push occurred.

[^design]: Preserved [NCSTAR 1-9](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf), physical 59/66/89, printed 15/22/45; sections 2.4/2.4.3/2.7. Reported photographic corroboration was not independently re-inspected here.
[^plans]: NCSTAR 1-9 physical 70/549, printed 26/483; [NCSTAR 1-9A](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf), physical 88-89, printed 37-38, Figure 3-22 and model-construction text. Reduced original-plan text is not a complete legible drawing review.
[^uaf]: Preserved [UAF September 2017 progress presentation](drawing-public-sources/uaf-progress-2017.pdf), physical page 39; full-page root and independent source inspection. Acquisition/pins are in [source README](drawing-public-sources/README.md); calculations were not evaluated by this unit.
[^errata]: Preserved [NIST text changes](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1a-1-9-1-9a-errata-attempt02.pdf), both full pages viewed, June/April 2012 changes on physical page 2. Original p.482 freshly read; original p.527 contrast is the errata's own marked replacement, not a new p.527 inspection.
[^connection]: NCSTAR 1-9 physical 548-549, printed 482-483, Figure 11-15 and adjoining stud description; NCSTAR 1-9A physical 80-81, printed 29-30, Figures 3-12/3-13; UAF page 39. NCSTAR 1-9 Figure 11-9, physical 542/printed 476, separately depicts ANSYS plan axes.
[^numeric]: [Released-mapping review](released-mapping-review.md), diagnostic/part table and identity pins; member map run06 and material-run-crosswalk run01. All line numbers refer to pinned decompressed streams, not PDF pages or execution logs.
[^restraint]: NCSTAR 1-9A physical 130/132, printed 79/81, section 4.3.3 and Figure 4-17; NCSTAR 1-9 physical 639/641, printed 573/575, explicit C79-C76 Floor 14 endpoint text and Figure 12-44. Root freshly viewed all four complete pages.
[^west]: NCSTAR 1-9 physical 570/printed 504, Floors 10-12 subsection. This is an ANSYS account; it is not the selected Floor 14 LS-DYNA attachment's verified property assignment.
