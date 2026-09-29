# Released material / run-state crosswalk

2026-09-12. Research only; the [charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
controls. This is a bounded follow-up to the [member map](../model-member-map/report.md),
not a collapse simulation, expert certification or amendment to the legal record.

## Result

The supplementary release permits a more specific finding than “the connection
properties are missing.” **23 used master-region parts reference 19 material IDs
without definitions in the three inspected geometry/material inputs. They contain
16,324 shell-element records. All 19 original material numbers also have definitions
in the transformed include, but there their effective IDs are 1000 higher.**
Those are supplied numerical counterparts, not definitions of the master-region
references. Neither copying them over nor ignoring the +1000 transformation is
an authenticated repair.

The six explicit beam candidates from the separate Case B damage list are different:
they reference part 98, section 98 and **supplied material 50**. We can identify its
numeric law and section fields subject to manual-version limits. We cannot establish
that these beams failed, were deleted in a historical run, or had those exact
properties in the real building.

These results sharpen reproducibility questions. They do not establish exaggerated
fire temperatures, false connection capacities, intentional withholding misconduct,
or a different collapse-cause ranking.

## Scope and reproduction

[Protocol](PROTOCOL.md), [producer](map_materials.py), [run 1](run01.json),
[run 2](run02.json), [report arithmetic](crosswalk-summary01.json),
[arithmetic code](summarize_materials.py), [validation](validation.md),
[independent extraction](independent01.json), [independent review](independent-review.md),
[method sources](method-source-review.md), [inference review](inference-review.md).

The four pinned inputs are SRC-116 and SRC-119–121. Full decompressed streams total
567,432,650 bytes / 11,294,760 physical lines. Both root passes reached EOF with
matching compressed and uncompressed hashes. The two result trees are identical
except elapsed time. Raw comments, arbitrary headings and unknown keyword strings
were not exported; titles are hashes. Source content was not executed.

Inventory: 459 part definitions, 459 section definitions, 379 material definitions,
59 curve blocks, and 392 element-referenced parts. Mesh record counts reproduce the
previous corrected map: 3,006,910 shells, 3,190 beams, 33,364 discrete elements and
2,461 solids. A shell thickness row is not another element.

SRC-121's include-transform begins at physical line 5,520,133; numeric rows are
5,520,136 / 138 / 140 / 142. The established interpretation adds 1000 to SRC-120's
part, material and section IDs, not node, element or curve IDs. The thermal-only
SRC-118 dependency was checked in the preceding units, not rescanned here. This
reader is not a general include or solver interpreter: unknown control blocks
remain uninterpreted, and the documented numeric temperature-conversion-flag
caveat remains. Consequently the claim is about these inspected, pinned inputs
under the explicit assembly interpretation—not every possible solver input.

## Exact missing-reference map

All rows below are SRC-121 PART data-card lines. Each section exists, has the same
effective ID as its part, and is a `*SECTION_SHELL`. Complete numeric section cards
and their line pins are in the retained outputs. Zero here means no match in the
**separate, unused** SRC-116 shell list; it does not mean zero physical force.

| Part ID | Missing material ID | Shell records | Set-2 shell matches | PART card line |
|---:|---:|---:|---:|---:|
| 25 | 25 | 11,368 | 0 | 2315 |
| 33 | 33 | 1,478 | 0 | 2432 |
| 711 | 711 | 644 | 0 | 4084 |
| 712 | 712 | 84 | 3 | 4092 |
| 713 | 713 | 140 | 0 | 4100 |
| 722 | 712 | 42 | 0 | 4116 |
| 723 | 723 | 56 | 0 | 4124 |
| 731 | 731 | 616 | 38 | 4132 |
| 733 | 733 | 112 | 0 | 4148 |
| 741 | 741 | 70 | 0 | 4156 |
| 742 | 742 | 84 | 2 | 4164 |
| 743 | 743 | 28 | 0 | 4172 |
| 751 | 751 | 168 | 42 | 4180 |
| 752 | 742 | 248 | 0 | 4188 |
| 753 | 743 | 28 | 0 | 4196 |
| 761 | 761 | 672 | 105 | 4204 |
| 762 | 762 | 206 | 0 | 4212 |
| 763 | 763 | 28 | 0 | 4220 |
| 772 | 772 | 84 | 7 | 4228 |
| 773 | 773 | 28 | 0 | 4236 |
| 782 | 772 | 56 | 0 | 4252 |
| 802 | 802 | 42 | 0 | 4284 |
| 803 | 803 | 42 | 9 | 4292 |

Thus 206 of 1,543 shell-list matches intersect seven missing-material parts.
The other matches are in parts 11 and 27, which have definitions. There are also
355 numerically corresponding discrete elements in the beam-number list; none
belongs to these missing-material parts. Cross-family matching remains distinct
from the applicable deletion semantics. No active DELETE_ELEMENT card was found
in the inspected streams, and this unit did not activate any damage list.

The numerical pattern does not identify actual connection type, floor, fabrication
detail or calibrated strength. Those joins require the component mapping and
source calculations; a material number is not a column number or a physical label.

## What the transformed counterparts add—and do not add

SRC-120 contains MAT024 definitions with effective IDs 1025, 1033, 1711, 1712,
1713, 1723, 1731, 1733, 1741, 1742, 1743, 1751, 1761, 1762, 1763, 1772,
1773, 1802 and 1803. Their full supplied numeric cards are preserved.

There is a same-original-part-ID counterpart for each of the 23 master parts.
Nineteen original PART data cards are numerically identical across the two files,
before the transform. Four are not: master parts 722, 752, 753 and 782 share
materials 712, 742, 743 and 772 respectively, whereas their included counterparts
reference their own original material numbers. Twenty-one title hashes match;
those for parts 25 and 33 do not. Neither a shared title hash nor matching raw
numbers proves equal geometry, constitutive behavior, temperature dependence or
historical use. The four different material references are a concrete reason not
to equate same-number parts mechanically.

This is positive evidence of supplied property information in another namespace.
It defeats blanket absence claims, but does not close the missing master-region
property/run join. This unit has not established which definition was removed,
when, why, or whether an alternative version supplied it.

## Six explicit beams: supplied fields, bounded meaning

The same-family beam IDs are 42620, 42627, 42778, 42785, 42936 and 42943;
SRC-121 lines 5,522,780 / 787 / 938 / 945 / 5,523,096 / 103. All belong to
part 98's 1,106 beam records. PART line 2109 references section 98 and material
50. Material 50's four numeric cards are lines 1759–1762; section cards are
2104 and 2106. The prior map's endpoint coordinates remain a separate result;
this unit reproduces IDs/connectivity without rebuilding the coordinate array.

Under the May 2007 Version 971 manual, MAT024's positive FAIL field is a plastic
strain criterion, not a clock time. MID50 supplies FAIL=0.084, E=205,000,000,000,
PR=0.288 and density-field RO=12,260.85. It supplies eight strain/stress pairs;
the first is (0, 259,000,000). The pairs supersede the zero SIGY/ETAN fields;
LCSS=0 therefore does **not** mean that no stress–strain law is supplied.
TDEL=0 is a separate minimum-time-step deletion field, not a scheduled collapse
time. These are card interpretations, not proof of actual failure or a faithful
physical capacity. [Manual, MAT110–112 / PDF1502–1504](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf).

Section98 specifies ELFORM=1 and CST=1. In the same manual, the selected formulation
is an integrated beam and TS1/TS2=0.2175 occupy outer-diameter fields, with
TT1/TT2=0 as inner diameters—not an area of 0.2175. The calculation's units,
surrogate/member correspondence and historical run still need authentication.
[Manual, SECTION29.2–29.5 / PDF1086–1089](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf).

NIST describes simplified connection geometry, grouped capacity calculations,
calibrated shell-tab behavior/failure strain and additional discrete vertical
support. It also describes density scaling to allocate total load. These provide
reasons to examine calibration and mass allocation, not replace missing cards
with ordinary steel or label a density field erroneous in isolation.
[NCSTAR1-9A, printed8,22–24,53 / PDF59,73–75,104](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612).
Its ANSYS break-element account is a different implementation; USER102–105 and
their post-failure stiffness do not identify these LS-DYNA material numbers.
[NCSTAR1-9, printed473–474 / PDF539–540](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611).

## Claim strength and next discriminating evidence

| Claim | Layer / grade | Limit, alternative and falsifier |
|---|---|---|
| The selected used parts have unresolved MID references in the inspected material-definition inventory. | Derived, A for the stated files/namespace | A correctly linked definition in a dependency or documented different assembly could close the gap. Not a finding that the building had no connection strength. |
| The transformed file supplies all 19 same-original-MID definitions under different effective IDs. | Observed/derived, A | Not an applicable substitution. An authenticated region-specific property mapping could establish intended equivalence or a difference. |
| The six listed explicit beams have supplied section and MAT024 cards. | Observed/derived, A; manual interpretation version-conditional | A differing executable interpretation, historical input or restart could change run behavior. No forces, failed integration points or deletion output were reproduced. |
| These gaps establish manipulated fire physics or deliberate collapse. | Hypothesis, E as a conclusion from this unit | No discriminating causal/intent evidence was generated. Authentic definitions plus matched collapse/non-collapse runs, or independent physical/operational evidence, would be needed to test those propositions. |

Highest-value existing records/tests are: the master-region definitions with
version/assembly mapping; the connection spreadsheet linking actual locations,
groups and capacities to parts/materials; the calibration inputs, force–deflection
outputs and failure thresholds; and the actual executable/input echo, continuation
or restart, diagnostics and matched damage/no-damage outputs. The supplied
counterparts make a **specific comparison** possible if the missing mapping is
obtained; they do not justify filling it by assumption.

The next feasible scientific source task is to trace the reported connection
calibration back to its spring/component calculations and any independent tests.
Agreement between two calibrated numerical models must remain distinct from
experimental validation. No fresh generic search for “missing model” is needed.
