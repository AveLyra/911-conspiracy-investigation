# What the Plasco robustness analysis establishes

2026-10-04. Working scientific research under the full WTC7 investigation
charter. Separate readings compared and scientific synthesis reviewed.

Chapter3 of the held Domada thesis is a **heating, buckling and load-redistribution
study**, not simply a replay after arbitrary support deletion. It also does
**not demonstrate the complete transition from fire to total collapse**.
Connection failures are not modeled, historical fire conditions are expressly
not reconstructed, and several damaged configurations retain support through
neighboring members. Those qualifications constrain both a dismissal of the
fire mechanism and a claim that the whole collapse has been reproduced.

Source: Domada Veera Venkata Ramakanth, *Multidisciplinary forensic investigation
of buildings in fire: the case of the Plasco Tower*, institutional edition2025,
Chapter3, printed77-117 / physical92-132, in the
[preserved thesis](/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/plasco-thesis/sources/domada-2025-plasco-thesis-8358.pdf).
The source is one research family, not multiple independent confirmations.
Below, locators are **printed / physical**. Reported numerical results remain
the author's model outputs, not calculations rerun or physically validated here.

## Generated local failure is not imposed removal

The chapter heats selected columns and floor regions using ISO834-derived
section temperatures. It reports thermally driven column buckling and resulting
load shedding. The principal cases do not describe a member-deletion step.
That supports treating their local response as a reported thermomechanical
prediction, conditional on model inputs, rather than labeling all support
loss arbitrary. Exact failure commands, capacity criteria and logs are still
needed to verify the implementation. **77-79,92-95,100-112 / 92-94,107-110,115-127.**

The modeled structure contains the top six storeys, not the complete tower.
The chapter explicitly excludes connection-failure modeling and acknowledges
uncertain weld performance and composite action. It therefore cannot determine
when actual joints detach, what falling floors strike, or whether those impacts
destroy the remaining support. Neither a dramatic deformation image nor the
word “failure” supplies those missing steps. **91,93,98-100,112 / 106,108,113-115,127.**

One important methodological correction: **Table7 specifies Transient/Newmark
for the thermal analysis**, while gravity loading is Static/LoadControl.
Calling this chapter entirely static would be incorrect. Nevertheless, the
listed integrator does not by itself verify rapid-collapse dynamics: mass,
damping, integration settings, contact/rupture behavior, energy histories and
time-step sensitivity are not supplied here. The nominal3600s/100steps and
analysis-step plots are not an authenticated incident clock. **78,95 / 93,110.**

## Cases that failed locally or retained support

The [complete root case table](root-reading.md) retains every reported case,
including the ambient calculation, effective-length sensitivity and historical
interpretations. The central contrasts are:

| Heating case | Published result | What remains unresolved |
|---|---|---|
| Southeast core column | Reaction initially rises, then falls; other core/perimeter columns take load. SW reaction rises35% from its initial value. Fig3.9 still shows nonzero SE reaction over its displayed interval. **100-104 / 115-119.** | No complete global-collapse trace; exact failure criterion and why the plot stops at step35 are not given. The stated550°C threshold concerns gas temperature. |
| One versus two primary beams | Heated zones expand from3×10m to8×10m; larger affected floor regions deform, with more deformation for the two-beam case. **104-108 / 119-123.** | Both exposed area and member count change; not a one-variable beam-count test. Finite floor displacement is not demonstrated detachment or impact. |
| One-storey secondary-main column case | Load is successfully redistributed; the author reports no collapse-causing conditions and then expands the study to two storeys. **108,117 / 123,132.** | No complete standalone input/output archive for this stable control. It must not be dropped from the comparison. |
| Two-storey column and connecting beams | Buckling reported at step23, column temperature500°C;340mm floor displacement. Neighbor reactions rise to2.0 and2.37times initial. Global stability is described as unaffected unless connections fail. **108-110 / 123-125.** | Actual connection failures are not modeled. Increased force does not establish that remaining capacity is exceeded. |
| Wider multi-floor edge heating | Selected columns buckle; reported520mm floor displacement and2.72times neighboring reactions. Cooler structure still braces adjacent columns, which do not buckle; edge beams/corner columns can maintain temporary stability. **112-113,117 / 127-128,132.** | Edge beams are deliberately unheated on a masonry-protection assumption. The subsequent destruction of these retained load paths is not generated here. |

These results make the “coupling” issue concrete. Connectivity can redistribute
load and prevent immediate collapse; it can also transmit forces that threaten
other members. The outcome depends on their remaining capacity, temperature,
restraint and connection behavior. It is not established merely by asserting
that the building is interconnected. Here, several reported cases preserve
support despite localized buckling.

The source's Table9 varies effective length and reports adjacent-column
load/capacity ratios rising from0.40 to1.00. That is a conditional capacity
sensitivity, not a computation that removes the required bracing in the actual
event. The section, axis, restraint assumptions and formula implementation
remain necessary for reproduction. **111 / 126.**

The protected-primary-beam discussion is a qualitative counterfactual about
retained edge support and two-way slab action, not another separately documented
numerical run. **103,105-107 / 118,120-122.**

## Where the chapter overreaches or needs clarification

The conclusion at113/128 states that core-column buckling triggers global
collapse, and Table10 at114/129 rates it highly likely with no alternative
load paths. Yet the displayed core-heating case describes redistribution through
other columns, beams and floors. The summary is stronger than that demonstrated
case. A reasonable alternative reading is that Table10 generalizes to more
extensive, multiple-floor exposure, as its heading indicates. That possibility
must be checked against native case definitions; it is not proof that the
displayed case caused global collapse or that it could remain stable indefinitely.

Further precision problems affect reuse, not necessarily the executed model:

- Table8 alternates between10th- and11th-floor labeling; secondary-main and
  secondary upper-level ratios are reversed in later prose. **99,109 / 114,124.**
- Gravity-share prose gives45/20/35% and36secondary columns; Fig3.5 and the
  conclusion give44/19/37% and30secondary columns. Rounding may explain the
  percentages, not the count discrepancy. **96-97,116 / 111-112,131.**
- The photograph used in the core-protection discussion is captioned as the
  surviving **neighboring five-storey building**, not the tower's own core.
  It is an analogy, not direct measurement of that protection. **102 / 117.**
- Fig3.9's absolute reaction contour is labeled Rz(kN); its numerical scale
  and export units need reconciliation before absolute forces are reused.
  The relative reaction ratios above do not depend on adopting that unit label.
  **102 / 117.**

These are documented source limitations, not findings of fabrication or intent.
The thesis's historical photo interpretations, inherited reports and model
outputs also cannot be counted as independent measurements of the same event.

## Comparison with the already audited global collapse chapter

The existing [Chapter7 audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/plasco-thesis/chapter7/report.md)
is context from the same thesis, not a separate source or a new model run.
Its checked hash is
`4466cc654d393c63de0666912790fafb775cb39c8a217effa13d2ff07caaaa8b`.
No material Chapter7 fact used in this comparison is disputed, so no additional
primary-page expansion was needed. The separate reader made this comparison
only after freezing its Chapter3 record; root's earlier reread is disclosed below.

| Dimension | Chapter3 as read here | Chapter7 as previously audited |
|---|---|---|
| Purpose and extent | Idealized vulnerability/redistribution study; upper six storeys | Reconstruction-linked thermal study; upper eight floors |
| Thermal analysis description | Transient/Newmark; nominal3600s/100steps | Static thermal sequence; explicit dynamic limitations |
| Initiating loss | Heating-related member buckling and load shedding reported; no deletion step described | Original thermal response followed by a separate revised model with southeast floor sections removed |
| Connections and propagation | Connection failure omitted; local-to-global branches conditional | Rigid connections; inferred rupture and prescribed damaged geometry do not compute the full detachment/impact bridge |
| Contrary outcomes | Single-storey redistribution and retained cold restraint in multi-floor cases | Stable local deformation and load redistribution before the revised damaged state |

These are different conditional questions, not a demonstrated contradiction.
Chapter3 cannot inherit Chapter7's deletion criticism wholesale; Chapter7
cannot inherit an end-to-end predictive validation from Chapter3's local buckling.

## Implication for the WTC7 investigation

This chapter adds a physically specified example of **reported heating-induced
local buckling with both redistribution and potential propagation pathways**.
It does not supply a closely matched WTC7 fire control, a historical frequency,
or an independently reproduced route to sudden widespread support loss.
It neither validates NIST's particular sequence nor identifies intervention.
No causal ranking or numerical probability changes from this chapter alone.

The most discriminating missing material is the actual six-storey case set:
geometry/supports, loads, member-temperature maps, material/composite/joint
definitions, mass/damping/time integration, any failure/removal commands, and
complete force/displacement/convergence outputs for **stable as well as unstable
cases**. A further scientific test must establish whether independently
constrained joint and restraint behavior actually destroys the surviving load
paths. Guessing those inputs and matching a collapse animation would not
reproduce or independently validate the author's calculation.

## Verification and limits

The [root reading](root-reading.md) and [separate reading](observer-reading.md)
were frozen before findings exchange. Both agree on the material distinctions
and stable outcomes. The [synthesis review](review.md) found no material scientific
correction and requested a missing execution locator, now supplied in the log.
This is a separate analytical check on one source, not independent historical
corroboration or licensed structural-engineering approval.

All 41 chapter text pages and all 41 complete page images were read; two declared
full-page legibility supplements clarified dense legends without digitization.
The [source audit](source-audit.md) independently reproduced all 41 text files,
decoded all 43 PNGs and checked 217 declared products. Root separately rechecked
all 217 product pins, 41 text reproductions and dependency identities. This verifies
the local source transformation, not the structural calculation.

The [execution record](execution.md) preserves the first failed render attempt,
the corrected13-test parser, source/runtime pins and root's early reread of
the already-known Chapter7 report before freezing its Chapter3 reading. That
timing deviation prevents claiming a strictly post-freeze cross-chapter comparison
or blindness. No source images, earlier measurements or human gates changed.
No solver, new acquisition, external transmission, legal promotion, commit or
push occurred. The full investigation remains active and incomplete.
