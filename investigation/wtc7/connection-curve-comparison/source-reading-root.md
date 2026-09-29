# Root source reading, before exchange

2026-09-24. Prior-informed AI review, not qualified human review. Read the
earlier connection-calibration report/source review before this unit; neither
new independent source reading nor historical numeric extraction was read.
This record is frozen before receiving the other reader's interpretations.

## Source and actual coverage

Held NCSTAR 1-9A SHA-256
cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4.
Viewed all six complete newly rendered pages: physical 73,74,75,76,77,117;
printed 22,23,24,25,26,66. Full 200dpi page files are in render01, with source,
code, text, commands and image pins in its receipt. The image viewer was
requested at original detail but explicitly resized each 1700x2200 file to
1376x1780 in the presentation. No native curve-pixel measurement is claimed
from these views. All page headings, captions, plot legends, context and
references were readable. Pypdf text of the same six pages aided reading;
it did not supply the graph's axes/series labels.

## Page-level meaning

73 / 22: Section 3.3.1 lists six shear connection families and distinguishes
fin/header/knife from seated connections at the specified locations. Target
mesh 0.15–0.30m did not explicitly resolve fine connection details. The
spring model attributed to Sadek et al.2008 provides idealized fin strength,
ductility and force-deflection outputs; tab material behavior and failure
strain were adjusted to match it. The good-agreement statement points to
Figures3-4/3-5. These are fitted model-target comparisons, not experimentally
measured connections in these figures. The curves can nevertheless test how
well the reduced representation reproduces its chosen target.

74 / 23: Figure3-2 shows fin, header and knife schematics; the page attributes
these to fabrication shop drawings. The source describes a spreadsheet with
locations/types, capacities and geometry, sorting/grouping, normalization
by relevant weld/plate thickness and averaging. The figure supplies a
connection concept, not all installed details or an authenticated parameter
mapping for each plotted bolt group.

75 / 24: The 0.3 coefficient-of-variation figure is a grouping guideline;
outliers handled separately and roughly20groups are described. A location's
geometry multiplier restores non-normalized strength. Horizontal tension
capacity was calibrated first, then a discrete elastic-perfectly-plastic
element supplied additional vertical capacity. Figure3-3 labels the column
moving vertically, symmetry boundary, shell connection and fixed rotation
point at the beam end. The displayed benchmark is not an unconstrained
whole-building joint. These pages do not establish that additional resistance
was wholly omitted, nor give a complete combined-loading validation.

76 / 25: Both complete panels and captions were viewed; see the fixed
transcription below. Caption wording uses spring/shear while the overlaid
model legend uses spring/shell. The immediate method text identifies the
shell-based connection model; do not introduce a third measured curve or
ANSYS curve into the figure. Printed ordinate arrays, numerical residuals,
acceptance tolerance, loading rate and energy-channel definition are absent
from the six selected pages as read here.

77 / 26: Figure3-6 expressly identifies both shell and discrete components.
The later LS-DYNA/ANSYS comparison is described separately and no IDs/count,
quantified residual or comparison curves are supplied here. STP bearing,
sliding and bolt models are another connection branch, not validated by all
seven fin pairs. It would be incorrect to read the fin curves as measured
experiments or as the STP curves mentioned later on this page.

117 / 66: The exact Sadek, El-Tawil, Lew2008 article title/journal/volume/pages
match the prior study's lead. The page describes the global gravity/damage/
temperature/propagation sequence and a particular LS-DYNA build. Those global
timings/build statements are not an independently established time history or
energy definition for Figure3-4's displacement-axis benchmark.

## Axis and style transcription, not numerical digitization

| Item | Figure3-4, upper | Figure3-5, lower |
| --- | --- | --- |
| Horizontal quantity | Vertical Displacement (m) | Vertical Displacement (m) |
| Horizontal printed range | 0.0 to1.6, major labels every0.2 | 0.0 to1.6, major labels every0.2 |
| Vertical quantity | Applied Vertical Load (MN) | Dissipated Energy (N-m) |
| Vertical printed scale | 0.0 to1.0, major labels every0.2 | 0 to800×10^3, hundreds marked; preserve displayed multiplier |
| Solid line | Spring Element Model | Spring Element Model |
| Dashed line | Shell Element Model | Shell Element Model |
| Bolt-count colors | 3black,4yellow/orange,5blue,6red,7green,8cyan/lightblue,9purple | same seven legend assignments |

The page supplies seven spring/shell pairs per panel, not seven experiments.
The horizontal axis is not time. Force uses MN while energy uses N-m: a later
work integral would need the factor10^6, not an unlabeled numerical area.

## All-pair qualitative observations and limits

These are visual shape observations, not assigned ordinates, error percentages
or an accepted calibration-fidelity measurement. Line width, overlap and
resizing prevent treating the displayed centerline as exact raw data.

| Bolt group | Force-panel appearance | Energy-panel appearance |
| --- | --- | --- |
| 3 / black | Two rising/falling curves differ in shape; dashed extends above the solid on part of the descending branch. | End plateaus are very close/overlapping at this view; early/middle shapes separate. |
| 4 / yellow-orange | Dashed and solid have different decline shapes; neither is a universal upper bound on the other. | Close/overlapping final level; some separation before flattening. |
| 5 / blue | Dashed peak/decline is displaced relative to the smoother solid, with both sides of the solid represented locally. | Close final level despite middle-branch separation. |
| 6 / red | Dashed jagged/multistage branch crosses the solid and has a visibly different late decline. | Final dashed appears slightly below solid; earlier separation changes along the curve. |
| 7 / green | Dashed curve builds later and retains higher load over a later range than the solid. It is not below it everywhere. | Final dashed appears slightly above solid despite a lower middle branch. |
| 8 / cyan | Dashed jagged branch and late secondary hump differ from the smoother solid; local ordering changes. | Final dashed appears above solid. |
| 9 / purple | Solid and dashed have different early growth, peak shape and late branch; dashed is not uniformly lower. | Final dashed appears below solid. |

A model-target mismatch can occur in either resistance direction. Similar
terminal plotted energy is not identical force shape, and terminal closeness
does not establish pointwise closeness in the energy panel. Conversely, a
force-shape difference alone does not quantify global collapse consequence.
No robust maximum/mean error, complete digitized support, zero-force cutoff,
residual capacity, exact end displacement or failure time is measured here.

## Definitions needing restraint

The selected pages call Figure3-5 dissipated energy/energy capacity but do
not give its extraction formula, model boundary, symmetry normalization,
recoverable/kinetic/damping/hourglass treatment, or explicit equality to
the integral of the applied vertical load over the shown displacement.
Therefore preserve two tests: spring-versus-shell plotted force, and
spring-versus-shell plotted energy. A cross-panel work/energy equality check
would need those missing definitions and work-conjugate loading. Missing
definitions here do not prove that no such documentation exists elsewhere.

The strongest objection to overreading disagreement is that these are reduced
models intentionally calibrated for selected behavior; their global adequacy
depends on sensitivity not provided by a graph. The strongest objection to
overreading agreement is that the target is itself a model and shared/tuned
inputs can preserve physical errors. Neither objection justifies erasing the
actual plotted similarities or differences.

Next: complete independent source comparison and native representation audit,
then obtain actual human source/curve-mapping spot-checks and synthetic
ground-truth controls before any consequential automatic calibration measure.
No source changes, historical solver, exact curve arrays, accepted findings,
cause/intent ranking or human approval is supplied by this reading.
