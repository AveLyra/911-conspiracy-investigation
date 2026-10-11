# Plasco Chapter 3 root source reading

2026-10-04. Research-only documentary assessment, frozen before exchange with
the separate Chapter3 reader. This is not a solver reproduction or structural
expert certification. The [protocol](PROTOCOL.md) controls the fixed source,
scope and exclusions; [execution](execution.md) records commands and deviations.

## Coverage and independence

Read every printed page77-117, physical92-132, as complete source-order text
from the pinned PDF, then viewed all41 complete run02 pages in the same order.
Finally viewed the two declared complete300dpi supplements, physical117 then120,
for small graph legends. Thus41 unique chapter pages and43 full-page views;
no crop, digitization, source video, solver or measured trajectory. All selected
text was read, including historical discussion, negative outcomes and conclusions.

Source SHA256: `0d76577bbf898dfa2d1587d02f1cc51378d531e3b59983fc0d4db8665fd575b4`.
Run02 receipt: `d2c203d1bb9cf243e1cbdfc68a204c3996df358b65528d8df171fe0ec645524c`.
Supplement receipt: `304438b81f95bd532fe453cd8d9ae217a1bebd13d026129220e6c96e54c32693`.
Printed/physical locators below refer to this single source family. The source
contains the author's model outputs and interpretations, not observations newly
measured in this audit.

Prior Chapter6/7 work was known. Root also accidentally reread the prior Chapter7
report during resumed orientation before this freeze; the execution log retains
that ordering deviation. No other reader's new Chapter3 conclusions were received.
This is separately recorded interpretation, not a blind or historically independent
experiment. The later joint synthesis must not hide that limitation.

## Answer from this chapter alone

The chapter reports heating-induced member deformation, buckling and load
shedding. It does not describe starting its principal cases by deleting a
column or floor. Calling these cases merely imposed support removal would
misdescribe the published method. But no connection rupture law, falling-floor
contact/impact sequence or complete global-collapse computation is demonstrated
here. The reported heated structures also retain alternative support, including
explicit stable cases. Local buckling is not equivalent to elimination of every
supporting load path.

Crucially, Table7 calls the thermal analysis **Transient**, using **Newmark**;
only the preceding gravity analysis is Static/LoadControl. It would be wrong
to import a later chapter's static scope into this chapter. Conversely, that
integrator label alone does not establish resolved rapid-collapse dynamics.
Mass, damping, integration parameters, convergence/energy histories and a
contact/rupture implementation are not furnished in this chapter's published
description. Their absence here is not a claim that they are absent everywhere.

## Shared assumptions and implementation boundaries

| Item | Source statement and what it permits |
|---|---|
| Question and heating | 77-79/92-94 explicitly say these fire scenarios do not accurately reproduce the historical fire. ISO834 section heat transfer tests selected components/areas; time-domain application is for practical convenience. 92/107 sends realistic CFD discussion to Chapters4-5. No historical temperature field or independently predicted incident clock follows. |
| Extent and geometry | 77,91,93/92,106,108: top six storeys of a tower described as17floors. Nine floor segments, core/perimeter columns, long truss/Vierendeel beams. Figure3.2 visually shows the truncated model. Bottom-model boundary detail and original geometry files are needed before replication. |
| Elements/materials | 77/92: displacementBeamColumnThermal and ShellNLDKGQThermal; steel thermal degradation attributed literally to Eurocode1, layered plane-stress concrete/CDP and biaxial rebar/J2. 93-94/108-109: fiber thermal sections with15 or25 temperature points. These are simulated section assignments, not sensors. Do not silently replace the stated code designation with another code. |
| Gravity/load choice | 94/109: estimated7.5kPa dead load, comprising6.2 slab/joinery plus1.3 partitions; prescribed5.0kPa live versus estimated historical minimum6.0. 99/114 gives DL+1.5LL for load-ratio assessment. Exact live load used in each FE case versus capacity calculation is insufficiently specified for a fresh reproduction. |
| Solver/time/mesh | 95/110: dead load10increments; nominal3600s thermal history/100steps; UmfPack, Plain constraints/numberer, NormDispIncr; ModifiedNewton/Static for dead load, KrylovNewton/Newmark/Transient for thermal.71,000nodes,105,000elements. Mesh prose includes an unclear column-length phrase; no native mesh or refinement/convergence study supplied here. Do not infer a collapse time from an analysis-step number. |
| Connections/welds | 98/113 and112/127 explicitly exclude modeled connection failures. Aged weld performance is uncertain and not represented; effective cross-section treated as full at99-100/114-115. This retains coupling which may redistribute load or transmit inward forces, but cannot predict actual separation timing. No verified rigid-joint law is substituted merely from another chapter. |
| Composite action | 87,91,115/102,106,130 acknowledge unverified shear studs/actual composite behavior; Chapter3 calls its model composite. Full/no-composite comparison is assigned to later thesis parts, not demonstrated as a complete sensitivity pair here. Need actual tie/slip/rebar definitions. |
| Protection | Thin members are described as unprotected; false ceilings and masonry may shield selected members. Core protection is qualified at101/116; Figure3.8 at102/117 is explicitly the neighboring surviving five-storey building, not direct coverage measurement of the tower's core. Edge beams are deliberately unheated in the final multi-floor case at112/127. |

## Complete reported case and outcome table

Cases below distinguish calculations described in the chapter from historical
reconstruction and hypothetical consequences. Numerical values are author's
reported outputs, not rerun or independently validated values.

| Case and locators | Thermal/structural input | Reported response and retained support | What is not computed or established |
|---|---|---|---|
| Ambient gravity and load ratios;95-100/110-115, Figs3.4-3.5, Table8 | Truncated structural model; load assessment also describes ground and upper levels | All tabulated column load ratios below1. Fig3.5 and conclusion116/131 assign44% to four core columns,19% to eight secondary-main columns,37% to30others. | Exact mapping from six-storey model reactions to whole-tower ground ratios and capacities requires input files; differing counts/percentages in prose retained below. |
| Southeast core column heated;100-103/115-118, Fig3.9 | Thermal load on SE core; author describes heating until failure | Initial restrained expansion increases SE reaction and reduces SW; later SE sheds load. Text says after gas temperature550°C reaction begins decreasing; SW increase35%, NE4-5%, perimeter much smaller. Figure3.9 shows SE retaining nonzero normalized reaction through plotted step35 and other members taking load. | No explicit deletion, connection rupture, global free fall, or complete global-collapse trace. Exact strength/buckling criterion and reason curve ends at35 rather than nominal100 not disclosed.550°C is identified as gas temperature, not a measured column temperature. |
| One primary beam area heated;104-106/119-121, Figs3.12-3.13 | 3×10m area includes beam, secondary trusses and slab, all receiving ISO834 heat-transfer histories | Large floor deflection extends beyond heated area; text150-200mm, about200m² affected by deformation. Slab bottom about900°C/top about85°C are calculated, not flame-derived measurements. One-beam displacement curve levels substantially. |30m² heated area must not be confused with200m² response area. No demonstrated slab/connection fracture or detached floor. A primary beam losing stiffness is not automatically deleted. |
| Two primary beams on one face;105-108/120-123 | 8×10m heated edge zone on same floor, including two beams | Larger, mainly one-way deformation across three floor segments; source says nearly3times one-beam case. Fig3.12 plots finite displacements through step100. Catenary pull/local detachment are conditional alternatives. | Both heated area and affected member count change. This is not an isolated one-variable test of beam count alone. No resolved global collapse or measured rapid timing. Exterior fire photo motivates a scenario, not its exact boundary conditions. |
| Single-storey secondary-main column case;108,117/123,132 | Secondary-main column/heating initially confined to one storey; exact standalone settings not tabulated | Load successfully redistributed; conclusion says no collapse-causing conditions predicted for single-floor case. This result motivated expanding heating to two storeys. | No separate complete histories/paired case archive. Do not omit the negative case because the next case deforms more. |
| Two-storey secondary-main column plus connecting primary beams;108-110/123-125, Figs3.15-3.16 | Heated column length extends over two storeys with connecting beams | Column buckling reported at step23 and column temperature500°C; floor displacement340mm. Text explicitly says global stability not affected unless connections fail. Adjacent-column reactions rise to2.0 and2.37times initial. |500°C is author-assigned column temperature, unlike preceding550°C gas value. No modeled joint rupture/impact follows. Higher demand alone does not establish exceeding adjacent capacity. Figure3.16 retains a nonzero heated-column reaction; failed does not mean completely removed. |
| Effective-length capacity sensitivity;111/126, Table9 | Adjacent-column effective-length factors0.5,1,1.25,1.5,2; representing different retained restraints | Reported load/capacity ratios0.40,0.46,0.60,0.66,1.00; reduced restraint can exhaust reserve capacity. | These are conditional capacity calculations, not a simulated history that destroys the required restraints. Actual section, axis, end restraint and code implementation are needed for reproduction. |
| Wider multi-floor edge-compartment fire;112-113/127-128, Figs3.18-3.19 | Heating across multiple floors/edge compartments; edge beams deliberately unheated because of assumed masonry shielding | Selected perimeter columns buckle; floor displacement520mm; adjacent reactions2.72times initial. Buckled columns said to carry≤10% of total gravity load. Adjacent overloaded columns did not buckle because cooler parts still provided lateral support; edge beams/corner columns resist inward pull, permitting temporary stability. | Exact heated floor/member list absent. Hypothesized lateral progression is not the reported result. No modeled connection failure or verification that the assumed cool load paths disappeared historically. |
| Historical NW floor cascade and final sequence;79-85,108,115-117/94-100,123,130-132 | Literature, stills and retrospective interpretation, not another executed Chapter3 case | Reported NW local floor loss followed by about30min broader stability; later damaged members associated with final failure. | No independent video timing/custody, impact-energy model or simulation of floor-to-floor collisions. Debris buckling/weld photographs cannot independently date damage to initiation. |

## Source tensions that matter

The chapter's concluding prose at113/128 says core-column buckling triggers
global collapse; Table10 at114/129 rates that collapse highly likely and lists
no alternative load paths. Yet the actual core-heating discussion at101-104/
116-119 and Fig3.9 reports redistribution through other core columns, beams
and composite floors. The qualitative summary is stronger than the published
case demonstration. It may be generalizing to more extensive core exposure
(Table10's header says multiple-floor fire); missing case definitions prevent
equating it with proof that the displayed single-core case globally collapsed.
Neither assume total failure nor assert indefinite stability after the plot ends.

Other source precision limits are retained without alleging model falsification:

-99/114 Table8 upper-level heading says10th floor while prose/caption say11th;
  secondary-main ground ratio0.53 in table versus0.51 in prose.109/124 reverses
  the0.19/0.21 secondary-main/secondary upper-level assignment compared withTable8.
-96/111 says45/20/35 percent and later36secondary columns;97/112 Fig3.5 and
 116/131 give44/19/37 and30secondary columns. The latter count fits4+8+30=42.
  Different rounding may explain percentages, not the unexplained count change.
-80/95 says “Southeastern (SW)”; do not silently use that phrase to resolve
  southeast versus southwest chronology. The heating case itself clearly namesSE.
-Table9's slenderness ratios do not simply scale in direct proportion to the
  stated effective-length factors. Without its actual section/axis formula,
  do not treat the table as a reproduced one-parameter Euler-buckling calculation.
-Fig3.8 is an adjacent-building photograph. Figure3.11 is construction-stage;
  Figure3.6 is post-collapse debris. These are different evidentiary contexts.

The two high-resolution supplements make the requested legends readable but
do not create original plot data. Fig3.9 labels normalized current/initial
load and analysis step, with SE/SW/SES/NE/SEE traces. Fig3.12 distinguishes
one/two-beam cases and depth histories0-120mm; neither graph is a video track.
No plot ordinates, accelerations or uncertainty bands were digitized here.

## Provisional claim limits and next discriminators

Documentary scope claims (thermal cases, Transient/Newmark, omitted connection
failure and stable alternatives) are directly supported by the inspected pages.
The reported buckling and redistribution remain **model-dependent**, unreproduced
results. Their physical/historical force is conditional on exposure, loading,
restraint, composite behavior and untested weld/connection capacities.

This is evidence against describing every Plasco fire model as a pure prescribed
removal replay. It is not a demonstrated fire-to-total-collapse reproduction,
matched WTC7 precedent, proof against intervention or evidence for intervention.
A reliable exact case could strengthen or weaken this assessment in either
direction. In particular, native scripts showing temperature-driven member
instability with retained connections would support the reported local mechanism;
undeclared element deletion or solver termination used as collapse would weaken
its claimed predictive reach. Valid joint laws preserving or destroying the
cool redistribution paths would discriminate the proposed propagation step.

Required records: exact six-storey mesh/supports, member groups and heating
maps; material/section/connection/composite definitions; applied gravity/live
loads; thermal boundary and time arrays; Newmark/mass/damping settings; failure
and removal commands; stepwise reactions/displacements, convergence logs and
energy histories; every stable and unstable case. No missing file is invented.
Photograph captions do not replace authenticated chronology or case inputs.
