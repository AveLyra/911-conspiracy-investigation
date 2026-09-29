# Independent NIST calibration / validation source review

Research only; not a credentialed engineering verification, physical test, solver
replication, legal finding or cause ranking. Owner: independent source/inference
reviewer `/root/late_reference_diagnostic`.

## Independent extraction freeze

Frozen 2026-09-13 02:02 UTC (September 12 locally), before reading this unit's
`paper-source-review.md`, any new original-paper extraction, or root's final
report. This section records my own reading of NIST's published pages. Any later
cross-check will be an explicitly dated addendum, not a replacement of this
extraction. No curve digitization or discrepancy arithmetic was performed.

Controlling instructions: current main `AGENTS.md`, `WORKFLOW.md`,
`START-HERE.md`, and this unit's `PROTOCOL.md` (SHA-256
`7bf240b13ff1141ce9d69381d1dcc1ac17cb2c917b4f7e11800f01ba70d28247`).
Evidence-falsification, source-of-truth and PDF-review skills govern the review.
The only authored research file is this one. Raw sources, canonical/legal files,
other reviewers' work and model/archive bodies were not changed or executed.

### Primary source and visual coverage

- NIST NCSTAR 1-9A, *Global Structural Analysis of the Response of World Trade
  Center Building 7 to Fires and Debris Impact Damage*, November 2008 with the
  January 2009 change sheet, 173 PDF pages. Local source:
  `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf`.
  SHA-256 before/after selected source extraction:
  `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
- Full-page visual inspection in this review: PDF54-58 / printed3-7;
  PDF61-67 / printed10-16; PDF73-77 / printed22-26; PDF117 / printed66.
  Captions, legends, plotted curves and surrounding text were inspected, not
  merely text-search snippets. Selected text extraction also included PDF59,
  68 and 71 during discovery; those pages were not newly full-page-viewed here.
- New complete-page Poppler renders: PDF54-58 and PDF61-67 in
  `/private/tmp/connection-nist-source.XJeO3Q/p<PDF-page>.png` (1500-pixel maximum
  dimension). PDF73-77 and117 used existing complete-page renders from
  `/private/tmp/material-method-source.rQlqbx/ncstar1-9a-p<PDF-page>.png`, freshly
  viewed here. The latter are reused render artifacts, not independent source
  acquisitions. Text extraction used pypdf in the bundled Python runtime;
  no OCR-derived plotted values were treated as measurements.
- A bounded text search for `residual` across this PDF found vibration-damping
  references, not a direct statement about residual connection capacity.
  This lexical result is not evidence that residual resistance was absent from
  all models or documentation.

## Result: distinguish three different kinds of agreement

The selected connection pages affirmatively document engineering construction
of reduced models and their calibration. They do **not**, standing alone,
document an independent WTC7 connection experiment validating those models under
the temperature, loading and restraint histories of the collapse.

| Published comparison | What is compared | What it supports | What it does not independently establish |
|---|---|---|---|
| PDF73,76; Figures3-4/3-5 | Sadek et al. spring-model output versus the LS-DYNA shell-based fin model calibrated to it | Reduced-model reproduction of selected target force/displacement and energy behavior | Experimental accuracy of the spring target, or independent validation of the fitted fin law |
| PDF77 | Separately developed LS-DYNA and ANSYS connection approaches, for unspecified selected connections | Cross-formulation consistency; a useful possible check on implementation errors | Independence of their physical assumptions, accuracy of common capacities, or validation of every connection/group |
| PDF64-65; Figures2-13/2-14 | Desired analytical average slab law versus a calculated material-specimen response | Constitutive implementation check against its stated target | An experiment on a WTC7 slab, or independent proof of post-cracking/post-crushing capacity |

Calling all three comparisons merely an animation would discard real work.
Calling all three independent physical validation would give that work a stronger
meaning than these sources support. Agreement between different solvers can
increase confidence in implementation **conditional on the physical inputs**;
shared input error or shared omitted behavior can survive that comparison.

## Connection dependency chain: what the pages actually say

1. **Drawings and structural assignment.** PDF73-74 ties connection geometry and
   placement to WTC7 fabrication shop and structural drawings. The six named
   shear types are F, H, K, SWC, STC and STP. Their coverage is not interchangeable:
   fin/header/knife are described for interior framing except seated connections
   at Columns79/81; seated connections cover specified exterior and interior
   locations. Moment connections are also identified. Therefore a fin benchmark
   cannot silently become a benchmark for every connection family.
2. **Reduced geometry.** PDF73 states that the target element size,
   0.15-0.30m / 6-12in, prevented explicit fine-detail connection modeling.
   Simplified geometry and connection-specific materials represented expected
   capacity and ductility. This is an admitted resolution tradeoff, not a hidden
   discovery by this review.
3. **Spring target.** Fin groups depend on beam-web depth, generally determining
   bolt count. PDF73 attributes idealized fin strength, ductility and
   force-deflection output to Sadek et al. (2008). The exact reference on PDF117
   is *Robustness of Composite Floor Systems with Shear Connections: Modeling,
   Simulation, and Evaluation*, ASCE JSE134(11),1717-1725. These pages supply no
   underlying physical-test specimen count, test temperature, load history or
   holdout/fitting partition. That provenance must be established from the exact
   paper and its primary references, not guessed from its title.
4. **Shell calibration.** PDF73 explicitly says tab material behavior and failure
   strain were adjusted to match the spring behavior. Thus Figures3-4/3-5 show
   calibration performance, not an unseen experiment independently predicting
   the calibrated result. Header/knife development is described as analogous,
   not given the same displayed seven-series comparison.
5. **Grouping and restoring geometry.** PDF74-75 describes a spreadsheet of
   locations, connection types, horizontal/vertical capacities and geometry;
   grouping by W12-W36 depth and F/H/K type; normalization by weld/plate thickness;
   group averaging; a coefficient-of-variation guideline of0.3; separate outlier
   handling; and approximately20 groups. Location-specific geometry multiplies
   the group value to recover the non-normalized strength. The guideline is
   neither an experimental error bar nor a guaranteed worst-case error bound.
   These pages do not provide the spreadsheet rows, group residuals, outlier
   selection or full mapping needed to check the claim for each location.
6. **Two-direction construction.** PDF75 says horizontal capacity was calibrated
   first in tension. A discrete elastic-perfectly-plastic element then added
   vertical capacity equal to the stated actual shear capacity minus the shell
   model's shear capacity, with minimal horizontal contribution. This explicitly
   preserves additional vertical resistance; it is contrary evidence to an
   indiscriminate claim that connections were given no secondary support.
   It does not itself validate coupled axial/shear/rotation interaction,
   unloading, reversal, contact after failure or elevated-temperature behavior.
7. **Benchmark restraints.** Figure3-3 labels vertical column movement, a symmetry
   boundary and a fixed point of rotation. Those are specific component-model
   conditions, not evidence that all WTC7 joints shared those constraints.
8. **ANSYS comparison.** PDF77 says ANSYS used beam/break elements and reports good
   agreement for selected connections with the LS-DYNA approach. This page gives
   no selected IDs, number of comparisons, common/different parameter provenance,
   temperature/load paths, comparison plots, acceptance tolerance or errors.
   Absence on this page is a documentation limit, not a conclusion that the
   comparison never happened or that no further description exists elsewhere.

## Figure audit: agreement and visible disagreement

### Fin connections, PDF76

Figure3-4 is **applied vertical load (MN)** versus **vertical displacement (m)**;
Figure3-5 is **dissipated energy (N-m)** versus **vertical displacement (m)**.
Both legends say solid=spring model and dashed=shell model and show all bolt
counts3 through9. Neither figure is labeled an ANSYS curve or an experimental
measurement. The horizontal axis is displacement, not elapsed time; curve
separation cannot be reported as a failure-timing difference in seconds.

The paired force curves broadly preserve capacity ordering with bolt count and
the general increase/softening/decline pattern. But their shapes do not coincide:
the green7-bolt dashed curve builds and maintains appreciable load farther to the
right than the solid curve; several higher-bolt shell curves show jagged or
multi-stage post-peak behavior that differs from the smoother spring target.
This is visible disagreement even though the terminal energy plateaus in
Figure3-5 are substantially closer. Lower-count pairs also retain differences;
none should be declared exact identity from a figure.

The reason both observations can be true is mathematical: a closer accumulated
force-displacement area does not require equal force at every displacement.
Global failure propagation may depend on the order and instantaneous resistance
of particular connections, not only their final dissipated energy. Conversely,
a local force-shape mismatch does not by itself establish a significant global
collapse error. Exact comparison data and sensitivity analysis are needed for
that further claim.

**Quantification gate.** The figures do not provide a table of paired ordinates,
errors or uncertainty, and the source does not state a numerical acceptance
tolerance for good agreement. This review records the printed axes/series and
qualitative differences; it does not manufacture a percent error by pixel
reading, infer an exact failure displacement, or reconstruct a replacement law.
If exact arrays become available, a new arithmetic plan should freeze all
seven pairs, common displacement support, absolute/relative force and energy
differences, peak/end-point conventions and rounding before calculation. A
relative error near a vanishing reference force needs explicit treatment.

### Slab law, PDF61-65

The source starts with construction geometry, separate concrete/reinforcement
responses and a rule-of-mixtures calculation. PDF62 reports specified concrete
compression strength3.5ksi and an age-adjusted estimate4.9ksi citing Lange1994;
these are not two measured strengths of this WTC7 slab. PDF63 supplies component
areas per inch width: concrete4.0in², deck0.062in² in the strong direction only,
wire0.00467in². They are source transcriptions, not independently measured here.

PDF64 states that the selected LS-DYNA formulation could not simultaneously
represent the different tension/compression behaviors and strong/weak
orthotropy; it adopted the average of strong/weak curves for each loading sign.
Figure2-13 visibly retains materially different directional curves, especially
in post-cracking tension. Averaging is a declared simplification, not evidence
that the directional responses were identical.

The source then says a simulated uniaxial specimen reproduced the desired
average material behavior. Figure2-14's early compressive peak and broader
declining shape resemble Figure2-13's average. There is nevertheless a visible
end-of-range difference: Figure2-14 compression falls abruptly to zero before
the0.020 strain axis endpoint, whereas Figure2-13's desired average compression
remains positive through that endpoint. The tensile calculation also includes
initial/transient features absent from a smooth reading of the target curve.
These are model-target differences, not experimental residuals. The figures
alone do not identify which numerical failure setting caused the truncation or
its effect on a whole-floor collapse.

### Steel material fit and coarse failure calibration, PDF54-58,66-67

These earlier pages provide the strongest affirmative physical basis in this
selected NIST account: reported ASTM A370 steel tensile tests and measured
engineering stress-strain curves. Four50ksi tests are described, two
longitudinal and two transverse. The measured curves visibly overlap through
much of the response but show different terminal ductilities. The model uses a
representative curve and selects intermediate ductility. This is genuine
reported experimental constraint, not merely one solver agreeing with another.

However, the report also explicitly describes iterative adjustment of
post-necking extrapolation and failure strain to obtain that agreement. PDF55's
term validation is qualified to reproduction of the response for the test
conditions. In the terminology of this audit, the displayed evidence establishes
a fit/check against reported test data; it does not establish a held-out
prediction for WTC7 connections, fire conditions or multiaxial fracture.

PDF67 reports critical plastic failure strains1.00,0.56 and0.18 for fine,
medium and coarse models, respectively, shifted to match average measured
engineering failure elongation. Those are resolution-dependent parameter
values, not contradictory measurements of one physical failure strain. In
Figure2-17 the coarse shell response continues roughly level/upward where
fine/medium models soften. Matching failure elongation therefore does not also
ensure matching pre-fracture stress history or energy. In this example the
coarse curve is higher late in the response; it does not support a universal
claim that coarsening only weakened the building.

Two source-detail inconsistencies should remain narrow: PDF56 prose calls the
representative tensile curve L1, while Figure2-3 on PDF57 labels TestL2; PDF55
prints the medium mesh length as0.10in with a parenthetical0.254mm. Neither is
resolved here or promoted into a finding about the actual solver inputs.

## Residual resistance: what is and is not established

PDF65 states that elements exceeding their failure criterion were eroded
(deleted), and that the coarse mesh required adjusted failure criteria. A
deleted element cannot continue carrying load through that element. This is a
real modeling choice whose accuracy depends on whether failure criteria and
other retained load paths adequately represent the physical component.

It does **not** follow that all surrounding contact, bearing, catenary support,
remaining bolts or slab resistance were absent. PDF75 explicitly adds vertical
spring support. PDF77 describes STP plates providing vertical constraint and
sliding contact between beams/plates, as well as discrete bolt models. For STP,
the source reports35kip yield,45kip shear failure and0.45in maximum shear failure
displacement per bolt; it describes a component model checked against predicted
behavior, not a measured full connection experiment on that page. These details
prevent a blanket claim of omitted resistance while leaving specific
post-failure and combined-loading adequacy open to audit.

The relevant missing demonstration is narrower: which retained paths remained
after each particular failure, what experimental/analytical evidence constrained
their residual force-displacement behavior under the applicable history, and
how uncertainty in those paths affected propagation? My slab-curve truncation
observation is not a finding that fin/STP residual capacity was omitted, and is
not a quantitative estimate of missing building resistance.

## Claim-strength and next evidence

- **A, directly established as a published method statement:** NIST says it
  calibrated shell fin models to spring output and reports selected cross-solver
  agreement. The source itself makes those distinctions explicit.
- **B, strongly supported within the plotted domain:** paired fin energy totals
  visually agree more closely than the full force-displacement shapes; selected
  slab and steel figures display limits to curve reproduction. Exact error
  magnitude is not established by this non-digitizing review.
- **C, plausible but assumption-dependent:** different formulations agreeing can
  improve confidence in implementation. Strength depends on independence of
  their inputs and a suitably demanding comparison, which these pages do not
  fully disclose.
- **D, underdetermined by these selected pages:** accurate WTC7 connection
  behavior over collapse-relevant temperature, restraint, multiaxial load and
  post-failure histories. Exact experimental lineage remains to be traced.
- **E, unsupported by this review:** no physical evidence informed NIST's models;
  every connection was independently experimentally validated; all support was
  deliberately removed in the model; or this calibration audit identifies a
  historical collapse cause or motive.

The highest-value next materials are the exact Sadek paper and test references;
its actual spring targets and calibration/holdout distinctions; the connection
spreadsheet/group/outlier mappings; fin component input/output arrays; selected
ANSYS comparison identities and results; and explicit residual/coupled-loading
checks. A later test must distinguish target reproduction from independent
experimental validation and must preserve both stronger and weaker numerical
resistance. Missing items justify retrieval/testing, not a presumption of their
contents or a finding of intentional manipulation.
