# Independent spring-law manual review

September 13, 2026. Research-only, primary-document interpretation; no solver
execution, physical-capacity finding, or historical-run authentication.

## Source, scope and independence

The controlling [protocol](PROTOCOL.md) was read completely and verified at SHA256
`b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41`.
Current main AGENTS/WORKFLOW, START-HERE, the investigation charter, and the PDF,
evidence-falsification and source-of-truth skills were read. This derivative stays
in the isolated investigation worktree; no canonical record is changed.

The sole semantic authority consulted was the admitted LSTC *LS-DYNA Keyword
User's Manual*, May 2007, Version 971, in the preserved 2,206-page PDF:
[/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf](/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf).
SHA256 `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`
was checked before reading and by the render helper before/after each render run.
The cover was read and visually inspected. This is not an assertion that this
edition/build was the historical executable. No modern held documentation, raw
model cards, spring extraction output, court packet, or external source was read
for this review. Prior general model/parser knowledge and the protocol's named
dependencies are acknowledged. Schema findings were sent to the parent while
its independent source readers worked; this is independent manual interpretation,
not a blind physical experiment or an external expert's opinion.

Physical PDF page numbers below are one-based; printed page labels are separate.
Every page in the main rows below was read in full and visually inspected, not
just searched for the relevant term. Blank cells and rows matter.

| Subject | Physical PDF pages | Printed pages | Local full-page renders |
|---|---|---|---|
| Input blocks, IDs, order and free format | 46-47 | GS.2-GS.3 | `manual-renders/p46.png`, `p47.png` |
| ELEMENT_DISCRETE, complete entry | 758-759 | 14.14-14.15 | `manual-renders/p758.png`, `p759.png` |
| PART, complete base/options entry, with preceding index | 1027-1036 | 25.1-25.10 | `manual-renders/p1027.png` through `p1036.png` |
| SECTION_DISCRETE, complete entry including examples | 1100-1102 | 29.16-29.18 | `manual-renders/p1100.png` through `p1102.png` |
| MAT_SPRING_NONLINEAR_ELASTIC, complete entry | 2175 | 783 (MAT) | `manual-renders/p2175.png` |
| DEFINE_CURVE, complete base entry | 674-676 | 11.36-11.38 | `manual-renders/p674.png` through `p676.png` |
| DEFINE_SD_ORIENTATION, complete entry | 705-706 | 11.67-11.68 | `manual-renders/p705.png`, `p706.png` |
| INCLUDE_TRANSFORM cards and ID/conversion definitions | 859, 861-862 | 17.5, 17.7-17.8 | `manual-renders/p859.png`, `p861.png`, `p862.png` |
| Explicit contrast: MAT_SPRING_GENERAL_NONLINEAR | 2177-2178 | 785-786 (MAT) | `manual-renders/p2177.png`, `p2178.png` |
| Material reference tables (context only) | 1404, 1408 | 12, 16 (MAT) | `manual-renders/p1404.png`, `p1408.png` |

The full render directory is
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/c79-casea-spring-audit/manual-renders/`.
The cover is `p1.png`. Other full text pages read to establish section boundaries
or reject false search hits were 860, 1037, 2172-2174, 2176, and 677-679. These
are not separate visual-review claims or independent evidence. A whole-manual
text search for curve/interpolation and spring/failure/extrapolation terms was
used as navigation, not an exhaustive semantic proof of absence. Hits in other
material and loading types were not imported into S04.

## Field map and parser implications

### ELEMENT_DISCRETE

PDF758 gives the explicit fixed-card format `(5I8,E16.0,I8,E16.0)`, not eight
uniform ten-character fields. Ordered fields are:

| Field | Meaning and relevant default/condition |
|---|---|
| EID | Unique element ID; visualization null beams are generated. The manual warns against sharing this ID with ELEMENT_BEAM or ELEMENT_SEATBELT. This does not by itself settle deletion semantics for a beam-set numeric coincidence. |
| PID | PART reference. |
| N1 | First physical node. |
| N2 | Second physical node; zero means N1-to-ground, not a node whose coordinates should be looked up. |
| VID | Optional orientation reference, default zero. Zero acts along N1-to-N2; nonzero refers to DEFINE_SD_ORIENTATION, not a third physical endpoint. |
| S | Force scale factor, default 1. The page does not declare explicit zero equivalent to blank; preserve those inputs separately. |
| PF | Print flag, default zero: 0 prints forces in DEFORC; 1 suppresses that print. It is not a physical activation/failure switch. |
| OFFSET | Initial displacement or rotation, default zero. A positive translational offset can create tensile force at time zero; it is not automatically a geometric coordinate translation. |

PDF758 states that rotations are in radians. It also warns that these elements
affect the time step, that connected nodal masses must be defined, and that
unrealistically high stiffness/damping must be avoided. A finite curve or
successful parse cannot establish numerical stability. Its recommendation of
beam type 6, especially for orientation, is not permission to replace a supplied
ELEMENT_DISCRETE with another formulation in this audit.

For nonzero VID, PDF705-706 supplies one card:
`VID IOP XT YT ZT NID1 NID2` (I,I,F,F,F,I,I). The table gives zero defaults.
IOP0 uses the supplied fixed-space vector; IOP1 uses the spring-node axis
projected into its normal plane. IOP2 uses a direction defined by two referenced
nodes; IOP3 projects the spring-node axis into the plane normal to that moving
direction. XT/YT/ZT are used for IOP0/1 and NID1/NID2 for IOP2/3. The latter
nodes are dependencies, not extra spring endpoints. Node-defined orientation can
change during motion; the manual warns that nodes passing each other can reverse
the direction and cause instability. VID therefore cannot be treated as a generic
coordinate-system ID or reduced to the initial N1-to-N2 line in every case.

### PART

PDF1029 defines a heading card followed by
`PID SECID MID EOSID HGID GRAV ADPOPT TMID`.
PID/GRAV/ADPOPT are integer fields; SECID/MID/EOSID/HGID/TMID are printed A8
identifiers. A numeric-only parser must reject or separately classify unsupported
labels rather than coercing them to zero. Preserve the heading's existence even
when its text is suppressed. Defaults for PID/SECID/MID are unspecified/required;
EOSID/HGID/GRAV/ADPOPT/TMID have printed zero defaults.

PDF1032-1033 makes SECID the SECTION reference and MID the MAT reference. EOSID
is for solid-element equations of state; HGID zero takes default hourglass/bulk
viscosity values. GRAV is an overburden/hydrostatic initialization option for
brick elements with LOAD_DENSITY_DEPTH, not a universal gravity on/off switch.
ADPOPT zero means no adaptation; negative values reference a size-vs-time curve
for 2-D r-adaptivity, and 1/2 identify documented h-/r-adaptive cases. TMID is a
thermal-material reference and zero defaults to MID. The page says beams/discrete
elements are not considered in thermal analyses in this context; it does not
prove an arbitrary structural spring can never be affected by imposed state,
changing surrounding elements, or another modeling mechanism.

The complete base entry includes option-dependent cards; do not flatten them
into the eight core fields:

- INERTIA: `XC YC ZC TM IRCS NODEID`; `IXX IXY IXZ IYY IYZ IZZ`;
  `VTX VTY VTZ VRX VRY VRZ`; and, for IRCS1,
  `XL YL ZL XLIP YLIP ZLIP CID`. These are rigid-body mass, inertia,
  initial-velocity and reference-frame definitions. A nonzero CID replaces the
  six vector entries. NODEID can replace the center-of-mass coordinates.
- REPOSITION: `CMSN MDEP MOVOPT`, for the documented external rigid-component
  repositioning context, not a spring-axis definition.
- CONTACT: `FS FD DC VC OPTT SFT SSF`; these are contact friction/thickness/
  penalty definitions with the contact-type and activation qualifications in
  PDF1031/1034-1035. In particular this FD is friction, not spring failure FD.
- PRINT: `PRBF`, rigid-body ASCII output selection; ATTACHMENT_NODES: `ANSID`,
  rigid-body updating subset with the explicit contact/load-membership cautions.

PDF1028 permits keyword option names in any order. No option is assumed present
in the actual selected cards here. If encountered, preserve it and audit its
payload/dependencies before claiming complete PART interpretation.

### SECTION_DISCRETE

PDF1100 defines first card `SECID DRO KD V0 CL FD`, then second card `CDL TDL`.
SECID is A8, DRO integer, and the other fields floating point. SECID is referenced
by PART; DRO0 is translational and DRO1 torsional. These must agree with the
material's intended element class. PDF1101 expressly makes KD through TDL
optional; its table supplies no blanket numerical default row. Retain blank,
absent and explicit zero distinctly before any implementation-specific claim.

- KD/V0: if KD is nonzero, the displayed law is
  `F_dynamic = (1 + KD * V / V0) * F_static`, where V is the absolute relative
  velocity and V0 the test velocity. It is a separate scale mechanism from
  element S and material LCR. Zero/invalid V0 under nonzero KD is a dependency
  problem, not a reason to invent a finite amplification.
- CL: a compressive displacement before the material force-displacement law
  begins. Nonzero clearance makes the spring compression-only per the manual.
- FD: failure deflection (twist for DRO1), negative for compression and positive
  for tension. It is a separate field from curve endpoints. The entry does not
  supply a detailed post-failure deletion/contact algorithm or an explicit
  FD=0/default truth table. Do not infer historical failure from field presence.
- CDL/TDL: compression/tension deflection limits. PDF1101 describes momentum
  conservation and a common acceleration at the limit, not the same operation
  as FD failure. Applicability is restricted to deformable bodies and at most
  one limited spring per node. Rigid-body nodes cause error termination, and
  NODE/BOUNDARY_SPC constraints must not be used on these limited-spring nodes.
  PDF1102's worked limit example supplies positive 12.5 for both CDL and TDL;
  do not apply FD's signed convention indiscriminately to both limit fields.

The examples' kg/mm/ms/kN units are explicitly examples, not the WTC7 model's
authenticated unit system. The first example leaves dynamic effects and limits
unset; it supports the optional nature of those entries, not a universal claim
that every explicit zero equals an omitted field for all solver builds.

### MAT_SPRING_NONLINEAR_ELASTIC (S04)

The complete entry is one page, PDF2175/printed783. Its only card is
`MID LCD LCR` (A8,I,I). It describes a nonlinear-elastic translational or
rotational spring, with one connected degree of freedom between two nodes.
LCD references force-versus-displacement or moment-versus-rotation. LCR is an
optional scale-factor curve versus relative translational/rotational velocity.

Important layout qualification: the underlined requirement about negative and
positive quadrants and passing through (0,0) is printed in the **LCR description
row**. It is not printed under LCD. Treat this as the literal source attribution
and a possible editorial ambiguity, not an authorization to move the condition
to LCD or invent a velocity-scale convention. This review has not compared any
selected curve with that condition or adjudicated its validity.

No distinct unloading-curve ID, yield/hardening field or failure field appears on
S04's card. The nonlinear-elastic description supports a distinction from an
explicit plastic/hysteretic law, but the page does not spell out a complete
load-reversal algorithm. In contrast, S06 on PDF2177-2178 explicitly has
LCDL/LCDU, BETA, TYI/CYI, loading/unloading curves and history rules. Those S06
rules, including its curve ordering/sign/softening rules, must not be imported
into S04. The reference-table S04 row (PDF1408) marks SRATE and TENS, with FAIL,
THERM and DAM blank; this is context consistent with the card, not a proof that
an assembly using S04 cannot lose support by other mechanisms.

### DEFINE_CURVE

PDF674 defines header `LCID SIDR SFA SFO OFFA OFFO DATTYP`; I,I,F,F,F,F,I,
with defaults none,0,1,1,0,0,0. Each subsequent card contains one `(A,O)` pair
in explicit `2E20.0` format, continuing until the next keyword. Preserve all
points/source order and blank slots; do not stop at an apparent final plateau.
The base entry also documents suffixes 3858 and 5434a for older discretization
choices. An unsupported suffix is not a harmless spelling alias.

PDF675 supplies these rules:

- LCID shares an ID space with DEFINE_TABLE, and table/curve references can be
  interchangeable. A missing curve should not be silently substituted from an
  unrelated MAT/PART ID; an encountered table dependency requires its own review.
- SIDR0 is transient/other applications; 1 is initialization but not transient;
  2 is both. This metadata alone does not authenticate what a historical run used.
- Explicit zero SFA or SFO defaults to 1, unlike blindly multiplying by zero.
- Offsets are applied **before** scaling:
  `x = SFA * (A + OFFA)`, `y = SFO * (O + OFFO)`.
- DATTYP1 denotes general nonmonotonically increasing xy data; DATTYP0 is the
  ordinary time/force-displacement/stress-strain case. It is not a documented
  S04 unloading selector.

PDF676 adds that positive abscissa offsets with DATTYP0 generate additional
zero-valued points at time zero and .999*OFFA; DATTYP1 does not generate them,
and negative abscissa offsets simply shift the values. Do not ignore this branch
in a nonzero-offset calculation or guess how a later solver resamples it.

For constitutive models, the manual describes internal equal-abscissa
discretization, warns against poorly spaced/near-infinite points and physically
meaningless extrapolation, and states extrapolation occurs off the supplied
abscissa domain. This differs from applied-load curves, which are set to zero
off scale. Redefined restart curves ignore offsets/scales per the cited restart
qualification. PDF674 explicitly acknowledges that changes in discretization
altered results in previously validated models.

Neither the complete base DEFINE_CURVE entry nor S04's entry specifies the exact
S04 interpolation or endpoint-extrapolation formula. The manual contains linear
interpolation statements for other loading contexts; those are not enough to
prove a solver-exact S04 implementation. Therefore transformed point extrema,
adjacent secant slopes, sign/domain/order and supplied-origin checks may be
reported as arithmetic properties of the supplied table after a separate
protocol. They are not automatically instantaneous tangent stiffness, a terminal
capacity, the entire solver curve, an unloading path, or a failure criterion.

## Namespace and remaining dependency guardrails

PDF859/861/862 defines INCLUDE_TRANSFORM offsets distinctly: node IDNOFF,
element IDEOFF, part/nodal-rigid-body/constrained-nodal-set IDPOFF,
material/EOS IDMOFF, set IDSOFF, function/table IDFOFF, DEFINE IDs except
FUNCTION IDDOFF, and section/hourglass IDROFF. Mass/time/length conversions
are FCTMAS/FCTTIM/FCTLEN; FCTTEM is a four-character temperature conversion
flag, not a generic scalar multiplier. TRANID zero means no specified geometric
transformation. No source transformation card was re-extracted in this arm.
The protocol's +1000 PART/MAT/SECTION and unchanged node/element/curve identity
therefore remain source-check obligations of the extraction arms, not numbers
proved by reading the manual. A source FCTTEM numeric convention must retain its
previously documented edition caveat.

The dependency closure for a later source audit is:

1. Exact ELEMENT_DISCRETE -> effective PART -> effective SECTION/MAT, with all
   fields, duplicates and namespace transforms retained.
2. Nonzero VID -> SD_ORIENTATION -> vector or referenced-node definitions as
   appropriate, without substituting one orientation option for another.
3. LCD and optional LCR -> actual curve/table headers and complete point/member
   data in the correct namespace, including suffix/initialization/scale/offset.
4. Optional section failure/clearance/limits and any triggered PART option ->
   their actual inputs and applicable constraints, not guessed defaults.
5. Historical build, initialization/restart state, selected input execution and
   D3HSP curve-usage/error output -> unresolved until separately authenticated.

## Claim-strength and falsification ceiling

| Claim | Type/strength | Decisive limit or falsifier |
|---|---|---|
| This edition defines S04 using MID/LCD/LCR and one connected DOF. | Primary text, A within this edition | Different applicable edition/build or an actual different keyword would change the interpretation. |
| S04 card alone does not prescribe a distinct failure or hysteretic unloading branch. | B, bounded card-level interpretation | A linked section/failure mechanism or documented build-specific rule could supply it; absence from this card is not assembly-wide absence. |
| The last table point need not be terminal failure. | B, supported by constitutive extrapolation text | An authenticated applicable failure/limit or different actual curve consumer can change the endpoint behavior. |
| Supplied-point transforms and secants can be independently checked. | Proposed derived calculation, not yet performed | Unsupported headers, duplicate abscissae, generated-point rules, or changing dependencies must be retained, not patched silently. |
| These cards establish real surviving restraint, capacity, collapse timing or cause. | D/E if asserted from this review | Requires physical units/member attribution, validated constitutive calibration, connected-system state, loads, executable-version behavior and historical evidence not supplied by this manual read. |

The strongest disconfirming details against a simplistic curve-only account are
the separate failure/limit fields, optional velocity/orientation mechanisms,
explicit constitutive extrapolation, and admitted version-sensitive
discretization. Conversely none of those uncertainties establishes intentional
manipulation, actual activation, or physical failure. No causal ranking changes.

## Actual review execution

`render_spring_manual.py` uses the admitted hash-pinned PDF and bundled Poppler,
preserves the input, and refuses an existing page-image output. All 31 selected
full-page images were inspected after generation. The bundled executable was
used because plain `pdftoppm` was not on PATH. A preliminary fitz import was
unavailable; no PDF data were altered and pypdf plus Poppler completed the read.
Poppler emitted Fontconfig default-configuration warnings, but completed each
run; the resulting full-page images were legible with tables/footers intact.
No PDF was authored or re-exported. No raw model source was executed or displayed.

Rendering used the bundled Python executable with `-B`, the local helper, and
these page groups: `758 759 1027 1028 1029 1032 1033 1100 1101 1102 2175 674
675 676`; `705 706 1030 1031 1034 1035 1036 2177 2178 859 861 47`;
`1 46 862`; `1404 1408`. This is human-visible agent document review, not a
numerical solver test or independent physical validation.
