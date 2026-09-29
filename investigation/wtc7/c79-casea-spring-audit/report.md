# Case A contact incidence and missing spring-curve dependencies

Two independently implemented source readers reproduce a negative Case A
contact-incidence result, while a separate spring audit identifies two
specific missing constitutive dependencies in the supplied file set. These
findings narrow what can be tested; they neither establish the collapse
mechanism nor validate the historical simulation.

This is working scientific research under the investigation charter, not an
expert report, a procedural fact promotion or an assessment of anyone's intent.
The full protocols, source pins, failed attempts and verification limits are
preserved in [validation](validation.md).

## Case A: the expanded contact test remains negative

The supplied Case A shell list, SRC-117, contains 45,152 nonzero membership
occurrences and 45,152 unique identifiers, with no duplicates. All 45,152
resolve to shell elements in the complete SRC-119 through SRC-121 streams.
The readers preserve every membership row, its position and source line,
ordered shell connectivity and original/effective part identity. The list's
316,064 unused fields are blank, not explicit zero. There are no unmatched
requested shell identifiers.[1]

The test uses the preceding audit's fixed contact-candidate selection rather
than deriving a new selection from these results. It checks three geometric
extension settings, two contact IDs and three retained classes: unknown
thickness, unresolved classification and geometrically admitted. All 18
groups have zero Case A shell-to-candidate-node intersections. The 742
selected master shell aliases are also absent from the Case A list.[1][2]

| Check | Reproduced result | Limit |
|---|---:|---|
| Complete Case A shell membership | 45,152 matches; zero unmatched | List membership, not an executed deletion command |
| Retained contact groups | 18 groups; zero relations in every group | Fixed candidate map, not every possible load path |
| Selected candidate/master-node coordinates | 1,189 nodes; 3,567 coordinate scalars agree | Same preserved model version, not measured building geometry |
| Master aliases | 742 absent from list; fresh connectivity/version checks pass | Static shell identity, not initialized contact or surviving force |
| Cross-family numeric coincidences | 498 beam and 3,461 discrete records; zero solids | Equal numbers do not merge element namespaces or establish deletion semantics |

The master-shell follow-up independently re-extracted all 742 shell records
and checked their source, line, original/effective part, ordered nodes,
paired thickness data and face-order relationship. It passes 7,420 declared
field checks. This closes a real limitation of the first independent Case A
pass, which had used the frozen master metadata for unlisted aliases. The
supplement was implemented after that gap was identified, not presented as
part of the original blind extraction.[2]

The conclusion is deliberately narrower than “Case A cannot affect Column
79.” A failure elsewhere could change forces, geometry, contact or stability
through relationships outside this selected map. Likewise a supplied list is
not evidence that it was applied at a particular time. These static negative
joins do not reconstruct any actual collapse sequence.

## Spring cards are present, but their referenced curves are not

The preceding Case B study identified 17 discrete-element numeric matches
to a beam list near the eligible contact nodes. They remain cross-family
candidates, not confirmed deletion actions. This unit follows those exact
17 source identities through their actual PART, SECTION_DISCRETE and
MAT_SPRING_NONLINEAR_ELASTIC cards.[3]

| Effective part / section / material | Selected elements | Whole part's discrete elements | Referenced force-displacement curve, LCD | Selected element force scale, S |
|---|---:|---:|---:|---:|
| 820 / 820 / 820 | 7 | 991 | 602 | 1 |
| 821 / 821 / 821 | 7 | 991 | 602 | 1 |
| 859 / 859 / 859 | 3 | 84 | 803 | 0.5 |

All nine definition blocks are supplied. Their twelve numeric cards and all
17 complete discrete-element cards agree between separate source readers.
Each material card has LCR=0; each selected element has VID=0, PF=0 and
OFFSET=0. The section cards have DRO=0 and explicit zeros in KD, V0, CL, FD,
CDL and TDL. Blanks remain distinct from those zeros.[3]

The decisive missing entries are **curves 602 and 803**. Both readers locate
59 DEFINE_CURVE blocks, but neither referenced identifier is among them.
Separate complete-stream checks find no DEFINE_TABLE or DEFINE_FUNCTION
family blocks and no curve-family variants in SRC-119 through SRC-121.
The subsequent full comparison also reconciles all 59 curve headers and
968 point rows as an inventory check. Those other curves are not replacements
for the two missing references.[3][4]

This is a scoped file-content finding. It does not establish that the curves
never existed, that they are absent from every agency record, or that a
historical solver necessarily ran with unresolved references. A separate
input, include, restart or different historical package could change the
dependency finding. Such a record must be located and authenticated; it
cannot be assumed into the calculation. Curve ID803 is also a different
namespace from shell material ID803 discussed in the previous audit.

## What the contemporaneous manual does and does not establish

The admitted May2007 Version971 manual defines the selected S04 material as
a nonlinear-elastic spring joining one degree of freedom. Its LCD references
force versus displacement for a translational spring, or moment versus
rotation for a torsional one; LCR is an optional velocity-dependent scale
curve. SECTION_DISCRETE supplies a separate failure-deflection field, FD,
and separate compression/tension deflection limits, CDL/TDL.[5]

This matters because neither the material name nor a curve endpoint supplies
a demonstrated failure history. The manual states that constitutive curves
are extrapolated outside their supplied abscissa domain; it does not specify
the exact S04 extrapolation or load-reversal algorithm on these pages.
CDL/TDL are also not simply alternate names for FD: their documented limiting
behavior involves momentum conservation and a common acceleration.[5]

The selected explicit FD=0 is preserved. The reviewed pages do not supply a
complete zero/default truth table, so this audit does not infer either
immediate failure or a verified disabled-failure rule from that value.
Similarly, it does not turn LCR=0 into an independently verified runtime
scale. The source's underlined origin/quadrants sentence is printed under
LCR, not LCD; that layout ambiguity is not silently repaired into a finding
against the absent LCD curves.[5]

The separately declared point-transformation and secant calculations were
prepared and synthetically tested, but **zero historical spring-curve
evaluations were possible**. Root and independently implemented dependency
checks record unresolved references. No missing points, stiffness values,
capacity, unloading path or force history were invented.[6]

## Effect on the investigation

The Case A result excludes this particular static list/contact intersection;
it is useful negative evidence within that declared test. The spring result
adds a specific obstacle to evaluating the local force-response chain from
the supplied files. It corrects any inference that merely locating a spring
material card completed that dependency audit.

Neither result distinguishes a fire-triggered historical failure from
deliberate support removal. Neither supplies an initiating mechanism, timed
loss of resistance, historical member displacement or operational evidence.
Consequently this unit does not change the collapse-cause ranking. The result
is increased specificity about model testability, not a probability estimate
or an inference of concealment.

The next discriminating records/tests are concrete:

1. Locate the actual definitions and source/version provenance of LCD602 and
   LCD803 in other already accessible released material, if present. Search
   by typed consumer/reference identity, not by filename or an untyped803
   match. Preserve a negative search's exact file coverage.
2. Establish which complete input/include/restart set and executable build
   produced the relevant run. The selected deck and manual edition do not
   authenticate that history.
3. Obtain or locate the run's D3HSP curve-usage/input diagnostics and relevant
   discrete-force, displacement, contact and damage histories. The manual
   specifically points to D3HSP's curve-usage table; PF0 alone is not proof
   that a DEFORC output was requested, generated or retained.[5]
4. With those dependencies resolved, evaluate and independently reproduce
   the declared point diagnostics; then relate forces to validated physical
   member geometry, calibration and state. A supplied curve would still not
   itself establish a historical failure sequence.

No source files, pleading, case facts or filed records were changed. All
work remains local research in the dedicated worktree. Solver execution,
external expert engagement, legal promotion and disclosure remain separate
questions, not automatic consequences of these findings.

## Sources

1. Preserved SRC-117 and SRC-119 through SRC-121; complete source hashes and
   source/card locators in [root source result](casea-root01.json),
   [repeat](casea-root02.json), [independent source result](independent-casea01.json)
   and [exhaustive comparison replay](casea-comparison-root01.json).
2. Frozen preceding [contact-geometry result](../c79-contact-geometry/report.md)
   and [fresh independent master-shell supplement](independent-master-aliases-root01.json).
3. [Independent spring source extraction](independent-springs01.json),
   [original extraction review](spring-extraction-review.md), root source
   result above, and [full common-field comparison](spring-comparison-root01.json).
   The original review predates the completed alternative-definition check;
   source4 resolves that particular pending question without rewriting it.
4. [Root family-presence result](definition-presence01.json) and
   [independent complete definition supplement](independent-definition-presence01.json).
5. LSTC, *LS-DYNA Keyword User's Manual*, May2007, Version971, admitted PDF
   SHA `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
   Physical PDF674-676 / printed11.36-38 (curves),758-759 /14.14-15
   (discrete elements),1100-1102 /29.16-18 (sections),2175 /783MAT (S04),
   705-706 /11.67-68 (orientation),1027-1033 /25.1-7 (PART).
   [Full manual review and local source link](spring-manual-review.md).
   Published copy: [official Ansys-hosted manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf).
   Hosting-path date does not change the manual's stated edition.
6. [Arithmetic protocol](ARITHMETIC-PROTOCOL.md),
   [root dependency limitation](spring-arithmetic01.json),
   [repeat](spring-arithmetic02.json), and
   [independent chain/dependency check](independent-spring-arithmetic01.json).
