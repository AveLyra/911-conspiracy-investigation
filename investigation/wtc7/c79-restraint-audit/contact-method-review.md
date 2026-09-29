# Version-971 contact and set semantics: independent methods review

Research only; September 13, 2026. This primary-manual review is not a solver
run, historical-run certification, structural-capacity calculation, licensed
engineering opinion, or causal ranking. It does not interpret the root's
numeric arrays or independently count the supplied model cards.

## Scope, source and inspection receipt

The delegated scope supplied two occurrences each of
`CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET`,
`CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET`, and
`CONTACT_AUTOMATIC_SINGLE_SURFACE_ID`, plus two `SET_NODE_LIST` and six
`SET_SEGMENT` cards. These counts are task context, not this review's findings.
The purpose is to establish typed schema and the inferential ceiling before
a separately declared source-membership scan.

Primary source: *LS-DYNA Keyword User's Manual*, Volume I, May 2007, Version
971, LSTC. Local admitted copy:
`/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf`.
The cover and 2,206-page count were checked. SHA-256:
`f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
This identifies the manual edition, not the exact executable, build,
platform, input deck, restart state or output used historically.

All relied-upon pages were inspected as complete page images, including
tables, continued paragraphs and qualifications. The 47 viewed physical
pages are: 1; 362–376; 394–395; 400–407; 472–476; 856–863; 1161–1164;
1171–1174. Page 377 was additionally rendered but is not relied upon.
CONTACT pages use printed 7.x numbering (physical page minus 360);
CONTROL_CONTACT 472–476 are printed 8.24–8.28; INCLUDE 856–863 are printed
17.2–17.9; SET_NODE 1161–1164 are printed 31.11–31.14; SET_SEGMENT
1171–1174 are printed 31.21–31.24. Selection expanded locally from the
keyword/schema locators to directly relevant continuation and global-control
pages; it was not a prospective survey of all solver features.

Renders: `/private/tmp/c79-contact-manual.NF6ibK/p<physical-page>.png`.
Poppler `pdftoppm` 26.05.0 rendered with `-f P -l P -scale-to 1700 -png
-singlefile SOURCE OUTPUT_PREFIX`. Executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`.
Font configuration:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf`.
Python 3.12.14/pypdf 6.10.0 served bounded PDF location/metadata; Python also
dispatched rendering. No source input file was executed. No solver, new
network request, held modern help, private source, outreach, main/legal edit,
Faraday run, commit or push was used.

Main AGENTS, WORKFLOW, START-HERE and the unit protocol were read. The PDF,
evidence-falsification, source-of-truth and repository-orchestration skills
governed full-page inspection, source/interpretation separation and the
limited worktree write. Unit protocol SHA-256 before this note:
`b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d`.
The first scoped write was rejected when the approval service disconnected;
read-only checks found no partial target and unchanged manual/protocol pins
before retrying the same bounded operation.

## 1. Keyword options must be parsed before the numeric cards

Physical 363 / 7.3 defines `ID`: the first card supplies an interface ID and
heading. Physical 364 / 7.4, Remark 1, allows options 1–4 in any keyword
order while requiring their data in the specified order. Therefore
`..._ID_OFFSET` has the ID heading card even though the keyword does not end
in `_ID`. An `endswith('_ID')` discriminator alone is inadequate.

Physical 366 / 7.6 gives this sequence: ID/heading if specified; MPP card if
specified; mandatory contact Cards 1–3; applicable type-specific data;
thermal data if specified; optional contact cards in prescribed order.
Later optional cards can require earlier blank placeholders. Discarding a
placeholder or unknown extra card can shift all positional meanings.
Physical 368–369 also document MPP controls and a special `&`-prefixed
optional card. This review does not claim those forms occur in this deck.

Physical 367 / 7.7 specifies integer `CID` followed by 70-character
`HEADING`, not eight integer selectors. CID is unique contact-interface
identity, not a slave/master set, part, element or node ID. The manual gives
it a role in full-deck restart initialization; the card alone does not prove
the actual restart state. Arbitrary heading text need not be emitted to
recover the schema.

## 2. Resolve side selectors in typed namespaces

Physical 370 / 7.10 gives mandatory Card 1:

| Field | Relevant source meaning |
| --- | --- |
| SSID | Slave selector; namespace depends on SSTYP. |
| MSID | Master selector; namespace depends on MSTYP and contact class. |
| SSTYP | 0 segment set (surface-to-surface); 1 shell-element set (surface-to-surface); 2 part set; 3 part; 4 node set (node-to-surface); 5 all-inclusive single-surface definition; 6 part-set exclusion form. |
| MSTYP | 0 segment set; 1 shell-element set; 2 part set; 3 part. No master node-set type 4 is listed. |
| SBOXID / MBOXID | Optional spatial restrictions; sign/type qualifications on physical 371. |
| SPR / MPR | Side force-output flags, not mechanical constraints. |

Preserve the source's contact-class qualifications. This is typed vocabulary,
not certification of every arbitrary keyword/type/value combination in every
Version-971 implementation. Retain literal fields and mark an unresolved
compatibility issue instead of silently substituting a different class.

Physical 370–371 limits the `SSID=0` all-parts convention to single-surface
contact; 371 says MSID is not defined for single-surface contact. Thus its
zero master field must not become a missing node/segment set. Nor may that
zero convention be generalized to the two-sided ties. The table says
"none" for the first four defaults; an absent field is not authorization
to silently supply type zero.

Physical 371 describes positive DEFINE_BOX restrictions for associated set
types 2 or 3, and negative IDs referring to contact volumes. Without applying
a nonzero relevant spatial restriction, a membership scan is a pre-filter
candidate scan. Single-surface inclusion does not mean every included node
is attached to every other included node.

## 3. Include ID offsets and contact OFFSET are different operations

Physical 859 / 17.5 gives INCLUDE_TRANSFORM Card 2 as `IDNOFF, IDEOFF,
IDPOFF, IDMOFF, IDSOFF, IDFOFF, IDDOFF`; Card 3 contains IDROFF.
Physical 861 / 17.7 defines the namespaces:

| Offset | Identifier category |
| --- | --- |
| IDNOFF | Nodes |
| IDEOFF | Elements |
| IDPOFF | Parts, nodal rigid bodies, constrained nodal sets |
| IDMOFF | Materials and equations of state |
| IDSOFF | Sets |
| IDFOFF | Functions or tables |
| IDDOFF | IDs defined through DEFINE, except FUNCTION |
| IDROFF | Sections and hourglass definitions |

An included ordinary node/segment set SID therefore uses the set namespace;
its listed NIDs use the node namespace. Contact references follow resolved
entity type, not one global integer-offset shortcut. The constrained-nodal-
set exception under IDPOFF is not ordinary SET_NODE_LIST. These pages do not
explicitly assign contact CID an offset category; no such mapping is invented
here. Physical 857 and 859–862 distinguish ID changes from coordinate,
constitutive and unit-factor transformations and TRANID. Actual include
context remains necessary. A renamed-ID match does not prove historical
reading of that include or the intended architectural location.

## 4. Node and segment sets supply candidates, not element connections

Physical 1161 / 31.11: SET_NODE_LIST (and blank-option form) header is `SID,
DA1, DA2, DA3, DA4`; list cards then hold eight NIDs until the next keyword.
Header attributes are not additional NIDs. COLUMN, LIST_GENERATE and GENERAL
use different schemas (1162–1164). LIST_GENERATE selects defined nodes within
inclusive bounds after input is read; numbering gaps are allowed. GENERAL
NODE/PART/BOX additions and removals are operation/order dependent. A
list-only parser must not treat these alternatives as literal lists.
Physical 1162 calls for unique node-set SIDs; duplicates must be flagged,
not silently overwritten.

Physical 1171 / 31.21: plain SET_SEGMENT has the SID/default-attribute header
then `N1, N2, N3, N4, A1, A2, A3, A4` per segment. The first four fields are
ordered face-node IDs, not an element ID followed by three nodes. Physical
1174 defines triangles by N4=N3. Preserve tuple order and attributes even
when deriving a deduplicated node-membership diagnostic; the triangular
repetition is not another independent restraint. Physical 1172 calls for
unique segment-set SIDs.

GENERAL (1172–1174) uses operation-dependent string/integer/real fields.
BOX/PART can generate exterior solid faces or one face per shell; IO forms
can include internal solid faces. DBOX/DPART/DSEG remove prior selections;
SEG adds node-defined faces. A plain-only parser must label GENERAL
unsupported, not manufacture faces from positional integers.

Attributes are context-dependent (1164, 1174). Normal/shear failure examples
concern named TIEBREAK variants. They do not establish a fracture-capacity
law for the supplied plain tied OFFSET contacts.

## 5. Ties, offset springs and ordinary contact are not interchangeable

Physical 363–364 distinguishes baseline tied projection/constraint behavior
from OFFSET's penalty formulation: discrete springs transfer forces and,
where applicable, moments between slave nodes and master segments. OFFSET
permits rigid bodies, unlike the stated baseline constraint restriction.
Thus lack of shared node IDs can coexist with intended tied interaction.
That affirmatively establishes why direct shared-node incidence is incomplete,
not that all candidate ties actually formed.

Physical 364 says tied node-to-surface and tied surface-to-surface OFFSET do
not affect rotational degrees of freedom. BEAM_OFFSET is a distinct option,
available for tied shell-edge contact, whose beam-like springs transfer
force and moment. Do not relabel plain OFFSET as BEAM_OFFSET or infer a
six-degree-of-freedom clamp from the word "tied." Its rotational-node
instability warning is a formulation limitation, not a finding in this case.
Multiple translational force paths can have an assembled rotational effect;
no directly constrained rotation does not prove zero rotational restraint.

AUTOMATIC_SINGLE_SURFACE is separately listed as type 13 (406). Its selected
population defines contact candidates, not the declared attachment of a tie.
Friction/sliding depends on contact state and the applicable law. Main Card
2 FS/FD/DC/VC/VDC controls and exceptions are on 372–373. Physical 373 uses
FS/FD as failure stresses only for TIED_SURFACE_TO_SURFACE_FAILURE. None of
the supplied keywords is that variant. Similarly, the TIEBREAK law introduced
on 376 is not evidence of a failure criterion in plain OFFSET.

## 6. Named dependencies between membership and residual restraint

The following are concrete next checks, not generic claims that more data
are needed. A parameter appearing in this manual does not establish that
the corresponding option occurs in this source deck.

1. **Side selection:** complete typed SID-to-node/face/part resolution in
   effective include namespaces, source-line provenance, duplicate/missing
   definitions, actual variants and applicable spatial filters. This is
   the justified next input join.
2. **Initialized tied pairs:** slave positions, ordered master geometry,
   associated thicknesses and overrides, geometric tolerances and untied-
   node warnings. Physical 402–403 / 7.42–7.43 says only sufficiently near
   nodes tie. For its shell-node case: delta1=0.60 times the sum of slave
   and master thicknesses; delta2=0.05 times the smaller master-segment
   diagonal; delta=max(delta1,delta2). It warns about untied nodes and
   excessive tolerance. Negative SST/MST invokes the stated absolute
   delta1 criterion. This transcribes the source, not a calculation on
   this deck or a universal rule independent of option applicability.
3. **Projection/orientation/thickness configuration:** main Card 3
   SST/MST/SFST/SFMT; optional MAXPAR (375, 394–395); global orientation,
   thickness and initialization settings (472–476). Physical 395 lists
   specific MAXPAR defaults for tied shell-edge variants. Physical 476's
   TIEDPRJ paragraph warns bypassed projection can introduce rotational
   constraints through gaps. It names base tied types, not a complete
   OFFSET compatibility matrix. Exact settings and realized initialization
   remain necessary.
4. **Effective force/stiffness law:** local SFS/SFM, global SLSFAC/PENOPT,
   applicable part/set attributes and overrides. CONTROL_CONTACT Card 3
   can override contact-section defaults for named automatic classes
   (472). Optional SOFT/DTSTIF can make stiffness depend on mass and time
   steps (394, 400–401); search depth/frequency also have controls (395,
   475). Finding a contact card neither recovers all effective stiffnesses
   nor physically calibrates them.
5. **Time and surviving state:** BT/DT and dynamic-relaxation treatment
   (374), restart/addition identity (367), actual deformed geometry and
   deletion/retention history. ENMASS describes how some eroded nodes can
   be retained in contact (475). Member-element failure alone does not
   establish all neighboring contact states; a pre-event definition does
   not establish surviving restraint at a later modeled instant.
6. **Release applicability:** Table 7.1 and type mapping (405–407) give
   contact-specific overpenetration behavior involving thickness and
   PENCHK/XPENE/PENMAX. This is not a generic fracture test for all ties.
   Do not assign ordinary-contact release rules to plain OFFSET ties merely
   because both are listed in the CONTACT chapter.
7. **Physical and historical joins:** floor/direction axes, member/connection
   mapping, formulations, surviving material/section/spring state, load
   paths and restraint directions. These convert model interactions into
   effective building stiffness/capacity; the manual supplies no case
   evidence for them. A historical run also needs exact executable/build/
   mode, resolved inputs and state/output provenance. Physical 365's
   limited implicit-supported list illustrates why mode assumptions matter.

## Permissible conclusion and strongest counterchecks

A successful typed membership extension can identify declared interfaces
selecting nodes/faces touching this model region and their candidate other
sides. It can rebut particular missing-shared-node arguments without
recovering every active restraint. Preserve the relation type: shared node,
selected slave, selected face containing a node, candidate counterpart,
realized tie pair and surviving force path are different assertions.

The strongest counterweight to an omitted-coupling claim is the manual's
affirmative capacity for interaction without shared mesh nodes. The strongest
counterweight to an intact-restraint claim is that selection, geometric
tying, penalty stiffness, deformation and survival are distinct and depend
on the actual controls/state above. Neither a graph edge nor a missing graph
edge proves either physical state.

This resolves primary schema for a bounded follow-up. It does not establish
adequate surviving Column 79 restraint, an omission by NIST, reasonable or
contrived inputs, or a changed ranking of collapse explanations. Agreement
between parsers would validate the selected extraction against these inputs,
not the model's physical fidelity or historical use.
