# Independent reading: published fin-connection calibration curves

2026-09-24. Research only. Reader: `/root/curve_source`, a prior-informed AI
reviewer, not an independent historical witness, human reviewer, or qualified
structural engineer. This file is frozen before receiving the root reader's
interpretations or any measured curve ordinates. It is a source reading, not a
digitization, reproduced solver result, or physical validation.

## Scope, authority, and actual inspection

The main investigation CHARTER and this unit's PROTOCOL control this work.
Main/raw evidence, old studies, legal records, and accepted Sherlock state were
read-only. Only this research note was authored by this reader. No new source
was acquired and no solver was run.

- Source: main `authority/nist/wtc7/ncstar-1-9a.pdf`, 173 physical pages,
  SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
  I independently recomputed the source hash before reading it.
- Protocol SHA-256:
  `1ec6fedc9110f9ef2001f69fd1e13ad3a316a904f057345af26a0118d3216e19`.
- Main CHARTER SHA-256:
  `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
- Worktree branch `research/sherlock-wtc7-investigation`, HEAD
  `e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`; existing research WIP was preserved.

I read extracted text from exactly physical pages 73, 74, 75, 76, 77, and 117
with bundled `pypdf`, then actually viewed all six complete 200-dpi Poppler PNG
pages with `view_image(detail="original")`. The visual review included page
headers/footers, captions, legends, schematics, axes, and body text. Printed
pages are respectively 22, 23, 24, 25, 26, and 66. No crop, contrast adjustment,
interpolation, or generated content was used. Text extraction misses the graph
axes and series keys on page 76; their readings below come from the image.

The renderer sent output paths, hashes, and process status only, not its curve
interpretation. I have not read the root source reading or numerical method.
The reader shares prior project context and the same report source, so
separate reading is not source independence or a blinded validation.

Viewed PNG pins, independently recomputed with `shasum -a 256`:

| Physical / printed page | File under `render01/` | SHA-256 |
|---|---|---|
| 73 / 22 | page-073.png | 471745c7181f5edd02d84ad80ea3d396d26571c3441863b5909f8200877dbc4b |
| 74 / 23 | page-074.png | 132859b7a2e3d5abb95f1411c7f111d6ec07c7c751ae2b1cd80954713a155856 |
| 75 / 24 | page-075.png | 60f4b265ff9449de096a091bbea9b0d8350209cee2a388533ee5c11efa802b20 |
| 76 / 25 | page-076.png | 0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6 |
| 77 / 26 | page-077.png | cd0a15b5fa18a352c79d418d439f95c69b29f3713ff1106f0d325f269a9affc6 |
| 117 / 66 | page-117.png | 0f031fc21ba1639185ce134045ef6c6a4fcd8f814c4d0863b7e4e67e4b9f6e3d |

## What the two plots actually label

Both plots occupy physical page 76 / printed 25. Figure 3-4 is the upper force
plot, captioned as spring/shear model force-deflection behavior for fin
connections with different bolt counts. Figure 3-5 is the lower energy plot,
captioned as a comparison of spring/shear model connection energy capacity.

| Item | Figure 3-4 | Figure 3-5 |
|---|---|---|
| Horizontal axis | `Vertical Displacement (m)` | `Vertical Displacement (m)` |
| Visible horizontal range and major ticks | 0.0 to 1.6 m, steps of 0.2 m | 0.0 to 1.6 m, steps of 0.2 m |
| Vertical axis | `Applied Vertical Load (MN)` | `Dissipated Energy (N-m)` |
| Visible vertical range and major ticks | 0.0 to 1.0 MN, steps of 0.2 MN | 0 to 800 x 10^3 N-m; numbered hundred steps with the x10^3 notation at the top |
| Solid-line identity | Spring Element Model | Spring Element Model |
| Dashed-line identity | Shell Element Model | Shell Element Model |

Neither axis is labeled as a dimensionless normalized quantity. The energy
axis scale must not be read as merely 0-800 N-m: its exponent is material.
Dimensional conversion only: MN times m is 10^6 N-m; N-m is joules. These
conversions do not establish what solver output was called dissipated energy.

Each panel's color key lists every integer bolt count from 3 through 9:

| Bolt count | Visible key color | Intended pair in each panel |
|---|---|---|
| 3 | black / dark gray | solid spring; dashed shell |
| 4 | yellow / gold | solid spring; dashed shell |
| 5 | blue | solid spring; dashed shell |
| 6 | red | solid spring; dashed shell |
| 7 | green | solid spring; dashed shell |
| 8 | cyan / light blue | solid spring; dashed shell |
| 9 | purple | solid spring; dashed shell |

Thus there are seven intended model pairs per plot, not just the more visually
separated seven-bolt pair. These are model cases, not seven independently
tested specimens. The captions use “shear model” whereas the explicit plotted
style legend uses “Shell Element Model”; the source context associates these
with the LS-DYNA fin representation. Neither plotted style is labeled as
experimental data. The style legend must control identification, not the
assumption that a stronger or smoother curve belongs to a particular model.

## Context and source claims, page by page

**Physical 73 / printed 22, section 3.3.1.** NIST distinguishes six interior
floor shear-connection types and identifies seated exceptions at Columns 79
and 81. It reports that its target element size, 0.15-0.30 m, prevented explicit
fine-detail connection modeling. Simplified geometry and material behavior
were intended to represent load capacity and ductility, using information
from structural and fabrication drawings. Fin connections were grouped by
beam-web depth, generally related to bolt number. The idealized fin strength
and ductility came from the Sadek et al. (2008) connection spring model, whose
outputs included force-deflection by bolt count. NIST says it calibrated the
LS-DYNA fin model by adjusting tab material behavior and failure strain to
match that spring model, and describes the Figure 3-4 and 3-5 agreement as
good. No numerical acceptance tolerance, error metric, uncertainty band, or
independent test-set definition accompanies that adjective on these pages.

**Physical 74 / printed 23, Figure 3-2.** The fin/header/knife schematics
identify steel plate/angle geometry, fillet welds, coped beams, and 7/8-inch
A325 bolts; their attribution is to fabrication drawings (Frankel 1985).
NIST describes a spreadsheet of locations, types, horizontal and vertical
capacities, weld sizes, and plate thicknesses. Grouping is by member depth
(W12-W36), then connection type. Capacities within a group were normalized
by relevant geometric features and averaged. This is a reported grouping
procedure, not evidence that the two plotted axes are normalized by bolt
count, plate thickness, or an arbitrary scaling constant.

**Physical 75 / printed 24, Figure 3-3.** NIST describes a coefficient of
variation of 0.3 as a grouping guideline, separate handling of outliers, and
about 20 connection groups. A location-specific geometric multiplier was
used to restore non-normalized strength. It reports first calibrating
horizontal capacity by beam tension, then adding a discrete element across
the tab web to supply the difference between target vertical shear capacity
and the shear-model-alone capacity, contributing minimally horizontally.
That element is described as elastic-perfectly plastic. Figure 3-3 labels a
symmetry boundary at the column, vertical column movement, shell connection
elements, and a fixed point of rotation at the remote beam end. Therefore the
plotted vertical displacement should not be silently equated to the local
slip of one bolt or a tab's local deformation. These pages do not fully state
the plotted reaction summation, any symmetry multiplier, sampling/filters,
or energy accounting set. Those definitions are needed before identifying
the graph's force/work with a specific whole-connection or global-model
quantity. Figure 3-3 is a model schematic, not a physical test photograph.

**Physical 76 / printed 25, Figures 3-4 and 3-5.** The axes and all seven
series identities are recorded above. The upper curves have differing
shapes and maxima/decay locations even when lower-panel plateaus appear
similar. The lower plot accumulates to plateaus rather than presenting a
force-like falling branch. Close endpoint energy values alone therefore
cannot be read as matching force at every intermediate displacement.

**Physical 77 / printed 26, Figure 3-6.** The generic shear-connection model
explicitly labels a shell component and a discrete element. NIST separately
reports comparison with an ANSYS approach using beam/break elements, with
good agreement for selected connections. This sentence does not turn either
Figure 3-4 style into an ANSYS curve or say all connection types and all
loading histories were validated. The remainder introduces seated-top-plate
(STP) connections with bearing/sliding/tied contacts and discrete bolt
elements. Its listed bolt capacities/failure displacement and reference to
Figure 3-9 concern that subsequent STP discussion. They are not automatically
the fin curves' parameters. Seated connections must not be replaced with
the fin curves merely because all are floor connections.

**Physical 117 / printed 66, sections 3.6 and 3.7.** NIST reports a global
LS-DYNA model with 3,593,049 nodes and 3,045,925 elements, gravity initialization
over 4.5 simulated seconds, four additional seconds for damage/temperature
initialization, then roughly 16 seconds of propagation. The named solver is
double-precision LS-DYNA mpp971dR4 beta, revision 41161; the text discusses
roundoff concerns. The cited Sadek/El-Tawil/Lew 2008 paper is *Robustness of
Composite Floor Systems with Shear Connections: Modeling, Simulation, and
Evaluation*, J. Struct. Eng. 134(11), 1717-1725. This reference identifies the
upstream model source; this reading has not examined the paper or verified
its experimental basis. The global counts, timings, and version identify
reported computational context, not independently reproduced results or
proof that the local curves encode all global failure processes.

## Qualitative all-pair reading, not measured ordinates

This table records visible shape relationships only. It supplies no numerical
force error, area, peak, cutoff, terminal displacement, or probability. The
source has no plotted error bars. Curve crossings, small dashed segments,
overprinting, and line width can confound local identities; every future
ordinate requires its own identity/support check.

| Pair | Qualitative force-panel observation | Qualitative energy-panel observation |
|---|---|---|
| 3 bolts | The black dashed response is not identical to the solid response: lower around the solid's crest, with later descending support in part of the falloff. | The two late plateaus look close; intermediate paths are separated. |
| 4 bolts | Gold branches separate around and after the crest; neither a complete exact match nor a single constant force-offset description is justified. | Late paths/plateaus look very close, with small intermediate separation. |
| 5 bolts | The dashed blue crest is shifted to greater displacement relative to the solid crest; rising and descending branches are not pointwise equivalent. | The dashed accumulation is visibly behind the solid through part of the rise, with close late plateaus. |
| 6 bolts | Red dashed and solid branches differ in crest location and height; the dashed curve is not everywhere a weaker version of the solid. | Curves separate and converge; final plateaus are close but visibly not a license to infer identical force histories. |
| 7 bolts | The green dashed load persists at substantial levels to greater displacement than the solid in part of the descending range; its crest is also displaced. | Dashed energy is lower through an intermediate interval and slightly higher at the late plateau in this reading. |
| 8 bolts | The cyan dashed curve is visibly more irregular, differs around the crest, and retains a separate late tail/hump. | The late dashed plateau lies above the solid; paths also change relative proximity earlier. |
| 9 bolts | Purple solid/dashed crest and falling branches differ; the dashed curve shows a separate late shoulder/hump. | The late dashed plateau lies below the solid in this reading; intermediate paths are distinct. |

The force-panel near-axis colored traces are not an exact zero-force or exact
complete-failure observation. A cutoff chosen later would require a declared
rule and sensitivity analysis. Dashed rendering gaps are not zero force and
cannot be bridged automatically as if the unprinted path were a measured
sample. Broad recognition of an intended pair does not identify every local
line segment. No conclusion about whether curves are native vector paths or
embedded rasters follows from their rendered appearance; that requires a
separate PDF representation inspection.

## Force, energy, normalization, and validation limits

1. **Quantity distinction.** Applied vertical force and dissipated energy are
   different observables. In a defined conjugate loading coordinate,
   integrating force over displacement gives external work. External work
   need not equal dissipation while recoverable strain energy, kinetic
   energy, other loading components, contact/friction, numerical damping, or
   deleted-element bookkeeping matter. These are possible accounting terms,
   not claims that a particular missing term explains this report's curves.
   The selected pages do not provide the equation/output definition needed
   to assume that Figure 3-5 equals the integral of Figure 3-4 at every point.
2. **Symmetry and scaling.** Physical units are explicit on the graphs, but
   the component schematic has a symmetry boundary and the prose describes
   geometric normalization. Neither fact authorizes inventing a factor of
   two, per-bolt scaling, or thickness factor for a graph comparison. Recover
   native histories, reaction/energy sets, and the plotting transformation
   before interpreting such a factor physically.
3. **Calibration is not independent validation.** NIST explicitly adjusted
   the LS-DYNA representation to the spring-model target. Agreement would
   show fidelity to that target under the depicted component loading, not
   a new independent experimental confirmation of the target itself.
   Upstream experiments may exist; absence from these selected pages is not
   proof that none exist. They need their own specimen/load/temperature/
   failure-mode correspondence audit.
4. **Global applicability is a separate bridge.** A fin-connection calibration
   does not validate seated-connection bearing/walk-off, thermally altered
   combined loading, the transfer of fire states, global redistribution, or
   the historical cause. Mismatch also does not by itself determine whether
   a whole-building prediction changes, or in which direction.
5. **The strongest counterargument to overreading mismatch:** simplified
   connection models may intentionally approximate total capacity/ductility
   rather than match every oscillation. A relevant acceptance criterion
   could allow nonidentical local force histories. That possibility is not
   verification that this approximation was adequate; obtain the declared
   criterion and test its global sensitivity rather than supply one after
   seeing the result.

## Claim/discriminator ledger

| Claim | Type and support | Strength and ceiling | What would weaken or resolve it |
|---|---|---|---|
| NIST describes adjustment of material behavior/failure strain to a spring-model target. | Direct report-text observation, physical 73. | A for what the report says; not independently reproduced calibration. | Native input/optimization history inconsistent with that description, or implementation audit clarifying a different procedure. |
| The plots compare seven 3-9-bolt spring/shell pairs, with vertical-load and dissipated-energy axes. | Direct visual reading, physical 76. | A for legible labels; local curve identities still conditional. | A verified alternate edition or native legend/plot file showing a different association. |
| Close final energy does not establish pointwise force agreement. | Mathematical distinction plus qualitative graph reading. | A for the general distinction; B for visible separations in this rendering. | Quantified identity/line-width audit could reduce or change individual local differences, not the general distinction. |
| Figures 3-4/3-5 themselves show independent experimental validation. | Proposed inference, contradicted by their model labels and calibration context. | E for this narrow claim; no conclusion that upstream experiments are absent. | An independently sourced test series and explicit graph mapping, not merely another model comparison. |
| A observed graph discrepancy makes the historical global collapse wrong or proves deliberate removal. | Causal inference not supplied by these pages. | E if asserted from this evidence alone. | Reproducible global sensitivity under defined alternatives plus independent historical constraints; mechanism/intent require additional affirmative evidence. |

Highest-value missing definitions are the original spring and shell histories
for all seven pairs; the component input/boundary/load prescription and
reaction aggregation; energy-output/channel and element-set definition;
units, symmetry/normalization factors and plotting/filtering script; the
group/location mapping; the target's experimental basis; and predefined
acceptance/sensitivity criteria. Published-graph measurement may still be
useful as a bounded transcription, but must retain unresolved definitions and
must not silently become a replacement constitutive law.

## Completion status of this bounded reading

All six required complete pages were actually inspected, the seven intended
pairs and both axes transcribed, and calibration/validation limits recorded
before interpretation exchange. No numerical extraction, inferred exact
ordinates, or experimental/global acceptance is claimed. The wider
investigation and any quantitative continuation remain incomplete.
