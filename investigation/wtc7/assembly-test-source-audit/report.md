# Original connection experiments and the later NIST comparison

Working research. This audit concerns Thompson's 2009 shear-tab experiments and
the comparison in NIST TN1749 (July2012, corrected February2013). It is not a
reproduction of WTC7, a validation of its collapse cause, or a legal-record
finding. Numerical reproduction and independent review are recorded separately
in [validation.md](validation.md). The [source/inference review](final-inference-review.md)
is incorporated, including its publication-date and hydraulic-hose corrections.

## Assessment

The original study supplies real experimental support for connection bending,
tensile load transfer after large displacement, differing failure mechanisms,
and residual load carrying after some initial failures. It strengthens the
empirical foundation behind the later comparison: that foundation is more than
agreement between two numerical models. It does **not** establish the behavior
of WTC7's heated, composite floors or its global collapse sequence.[^1]

The numerical comparison is informative but narrower than a claim of validated
failure physics. NIST reports that both models predict bolt-shear failure,
whereas the experiments also produced tab tension and block-shear failures.
It reports two experimental peaks at a secondary failure, whereas model peaks
occur at the initial failure. Initial gaps and the unloading rule were assessed
against these experimental responses, so the displayed agreement is not wholly
an unused prediction.[^2]

The original-to-NIST data bridge remains incomplete. The thesis's tables refer
to different physical events; its printed rotation equation conflicts with its
variable definitions; and the exact load-channel normalization and later
experimental-series selection have not been authenticated. These are concrete
reproducibility issues, not proof of invented experiments or deliberate tuning
of the historical WTC7 model. The original expressly identifies separately
available experimental data through its university library.[^1]

## What was tested, and what was not

Nine bare two-span assembly tests were conducted, with eighteen connection specimens
in three-, four- and five-bolt configurations. The same beams and other
apparatus were reused. Doubler plates suppressed selected beam-web deformation;
exterior pin supports and a rigid test frame supplied restraint. There was no
steel deck or concrete slab in the assemblies. A hydraulic system slowly pulled
down the initially unsupported central column.[^1][^2]

The original methods say the pump was manually operated and could not maintain
a steady force or automatically impose predetermined load/displacement steps.
The operator chose increments using a live plot. This was not a physical test
of suddenly removing a loaded support. No numerical thermal-exposure history
or measured specimen temperature is supplied by the reviewed methods; these
tests must not be described as elevated-temperature validation.[^1]

The original reports two load cells, two displacement transducers and eight
strain gauges, with instrument checks. Axial forces and moments were derived
from strain using elastic-section assumptions, not directly measured by
independent axial-force cells. Two faulty strain channels were excluded.
Reported instrument checks are positive evidence of experimental care, but
are not independently obtained calibration certificates or a complete error
budget.[^1]

Several particulars affect interpretation:

- Test3ST1's misaligned hole was manually reamed, producing uneven bearing.
  Its bolt-shear failure differed from other three-bolt failures. The proposed
  causal link is the original author's interpretation, not a controlled
  single-variable experiment.
- In5ST1 the hydraulic hoses were reversed, limiting capacity. Testing stopped,
  the hydraulic hose connections were corrected, and recording restarted near maximum
  flexural capacity. Early data were neglected. The experiment still has
  later failure observations; it is not wholly missing.
- Data for the left side3STL3 had unexplained spikes and failed the original
  statics comparison. That side was not evaluated in later original sections;
  the controlling failure was on the right. This does not automatically
  invalidate every quantity from the entire3ST3 assembly.
- Snug-tight installation is not a measured zero bolt preload. NIST's zero
  initial bolt tension and representative material curves are disclosed model
  assumptions; specimen-specific tensile tests were not supplied to its later
  comparison.[^1][^2]

## The event definitions cannot be pooled

| Original record | Measurement event | Invalid shortcut |
|---|---|---|
| Table4.1, p.103 | Sampled averages around approximate maximum **moment**, with a window selected from the controlling connection and applied to both sides | Treat its shear entries as global peak vertical loads, or the two sides as independent assembly tests |
| Table4.2, p.104 | Initial failure and its controlling connection | Assume initial failure always means ultimate load or complete support loss |
| Table4.3, p.105 | Secondary failure when reached | Replace blanks with zero reserve capacity or assume later failure always has the higher load |
| Table4.4, p.107 | Instrument/strain-derived statics consistency at a selected response state | Treat it as validation of the later numerical model |

The source itself preserves important exceptions.4ST2 was not loaded to a
secondary failure. Table4.3's generic three-bolt footnote describes initial
tension rupture, although Table4.2 and the individual narrative describe3ST1's
initial failure as bolt shear. The inconsistency is retained, not silently
corrected.[^1]

### Recomputed native-unit stage sensitivity

The declared diagnostic compares initial failure with the larger **reported
shear value** among the initial and secondary stages, retaining the rotation
from the same selected stage. It does not reconstruct the maximum of an
unavailable raw history. All nine tests and all missing secondary stages are
retained. A second cohort omits5ST1 solely as a sensitivity to the displayed
NIST-figure membership, not as an inference about NIST's table membership.
See the [prospective diagnostic](STAGE-DIAGNOSTIC-PROTOCOL.md) and
[full results](root-stage-results01.json).[^3]

| Cohort / bolts | Stage rule | n | Mean printed shear, kip | Mean rotation, rad | Sample COV shear / rotation, % |
|---|---|---:|---:|---:|---:|
| All /3 | Initial or larger reported stage |3|6.200000|0.132667|11.351 /3.399|
| All /4 | Initial |3|7.326667|0.094000|15.976 /1.843|
| All /4 | Larger reported stage |3|8.296667|0.106000|21.897 /18.844|
| All /5 | Initial |3|10.833333|0.076333|7.058 /8.004|
| All /5 | Larger reported stage |3|10.890000|0.083000|6.428 /9.639|
| Without5ST1 /5 | Initial |2|10.955000|0.077000|9.488 /11.020|
| Without5ST1 /5 | Larger reported stage |2|11.040000|0.087000|8.326 /6.502|

Unchanged three-/four-bolt cohorts are not repeated in this presentation; all
twelve cohort/size/rule scenarios and both sample and population statistics
remain in the results. Extra decimal places describe arithmetic on printed
inputs, not experimental precision. These COVs are descriptive and are not
confidence intervals.[^3]

At the printed stages,4ST1's later shear value is41.453% higher than its initial
value;5ST3's is1.663% higher. The later values for5ST1 and5ST2 are22.946% and
18.820% lower. These contrasts demonstrate the cost of substituting one event
definition for another. The small5ST3 difference is not assigned statistical
significance without measurement uncertainty. No force or angle conversion to
NIST's series has been applied.[^3]

## NIST's displayed arithmetic and physical agreement

All six table rows and both models were independently transcribed. The audit
recomputes `100*(model - experimental mean)/experimental mean` exactly and tests
the declared possibility that each printed value was rounded by half its last
shown unit. Nine of twelve direct quotients fall outside the printed deviation's
own rounding interval, but **all twelve are compatible once the displayed
model and mean precision are also allowed for**. This is evidence against
calling those small arithmetic differences established numerical errors. It
does not recover hidden digits or verify the experimental means.[^2][^3]

| Quantity / bolts | Experiment mean | Reported COV | Detailed model | Reduced model | Reported deviations, detailed / reduced |
|---|---:|---:|---:|---:|---:|
| Ultimate vertical load /3 |55.1 kN|11.3%|47.1 kN|43.4 kN|−14.6% /−21.3%|
| Ultimate vertical load /4 |73.5 kN|19.5%|65.7 kN|74.8 kN|−10.6% /+1.8%|
| Ultimate vertical load /5 |96.4 kN|7.1%|90.7 kN|106.6 kN|−5.8% /+10.6%|
| Rotation at ultimate load /3 |0.139 rad|3.4%|0.120 rad|0.103 rad|−13.8% /−26.1%|
| Rotation at ultimate load /4 |0.111 rad|18.8%|0.087 rad|0.093 rad|−21.5% /−16.6%|
| Rotation at ultimate load /5 |0.087 rad|9.6%|0.066 rad|0.082 rad|−24.3% /−5.6%|

These are NIST's reported COVs, distinct from the native-stage diagnostic above.
They give useful context for observed test variability, not a statistical
equivalence test, a confidence interval for model bias, or authenticated table
membership.[^2]

NIST's displayed comparisons are stronger for some observables than others.
Both model variants underestimate the tabulated rotation at ultimate load.
NIST characterizes these lower capacities as conservative. That can be useful
for a design estimate, but **conservative is not synonymous with historically
accurate**: a reconstruction still needs to establish whether a capacity or
deformation underestimate changes failure onset and propagation.[^2]

The later report describes models capturing slippage, bending, catenary action and steep resistance
loss. It also discloses unmatched failure modes, lower-quality axial-force
agreement, unknown frame-restraint sensitivity and a choice of unloading rule
that improved agreement. Hole gaps have a real geometric rationale; describing
them as arbitrary solely because they improve a fit would also overstate the
criticism. These comparisons support selected mechanical behavior while leaving
model-form, parameter and extrapolation uncertainty. NIST also points to nearby
calculated bolt-shear and plate-bearing capacities and suggests that ordinary
material-strength variation could shift the governing failure mode. That is
relevant counterevidence to treating every mismatch as implausible, but remains
a model-dependent explanation rather than a reproduced specimen-specific
failure prediction.[^2]

## Unresolved load, rotation and sample mapping

NIST defines total center load `P = 2(T sin(theta) + V cos(theta))` for its
symmetric two-span formulation. Local transverse shear alone is not the total
vertical support once axial tension has a vertical component. In an asymmetric
assembly, the two side contributions must be summed separately.[^2]

The thesis's Section4.4 says the **sum** of left and right vertical reactions
is compared with measured applied shear `V_app`. Its Table4.4 repeats a `V_app`
entry on both side rows, and other sections use the shear in a per-connection
analysis. The available text does not explicitly disclose whether the relevant
table values are a cell sum, mean, or later per-side normalization. A factor of
two cannot be chosen simply because it improves agreement with NIST. The
[independent definition review](definition-crosswalk-review.md) preserves both
the literal total-load wording and the competing per-connection context.[^1]

NIST openly explains its approximately5% larger rotations by a shorter reference
length: bolt centerline rather than center-column flange face. The original
provides the corresponding different distances, but Equation34 prints
`atan(horizontal distance / vertical displacement)`. That expression approaches
a right angle, not zero, near the initial horizontal state. The discrepancy is
in the printed equation and variable definitions; no acquired program establishes
what was actually computed. Correcting the formula silently would hide a real
provenance gap, while concluding that all plotted rotations used the literal
misprint would exceed the evidence.[^1][^2]

NIST shows eight experiment traces but says nine tests were conducted;5ST1's
early record problem is the stated reason its trace is omitted. Its tables do
not specify the constituent test IDs or sample/population SD convention. The
omitted figure does not establish an omitted ultimate-load observation. Matching
a rounded mean or COV under one candidate convention would not authenticate
the entire data reduction or the paired load/rotation event.[^2]

## Evidence-weight update and falsification ledger

This is an update to the strength and limitations of a **later connection-model
comparison**, not a new ranking of fire, deliberate support removal or other
WTC7 mechanisms. Thompson's report was published in May2009 and TN1749 in
2012/2013, after the2008 WTC7 report. Publication dates do not establish the
dates of the physical experiments, and no contemporaneous transfer of their
data into the WTC7 investigation is established here. The connection/member/material
crosswalks remain necessary before any transfer to the released WTC7 inputs.

| Claim | Type / grade | Decisive support | Strongest alternative or weakening test |
|---|---|---|---|
| The later comparison has an identifiable original experimental foundation | Documentary observation /A; physical inference /B | Original apparatus, methods, test narratives and data-quality disclosures | Original lab records could reveal inaccuracies; no physical tests independently repeated here |
| Some tested connections retained load-carrying capacity after initial failure | Reported physical observation /B | Test-specific later failures and measured/derived histories | Check synchronized raw channels, event definitions and uncertainty; do not generalize to every connection or WTC7 |
| Twelve printed model-deviation entries permit ordinary display rounding | Exact conditional calculation /A | Two transcriptions/implementations, all-row interval results | Different hidden rounding rule or source edition; agreement is not raw-data reconstruction |
| Selecting an initial or later reported stage changes summary statistics | Calculation /A within declared inputs | All-row native-unit sensitivity; missing-stage reasons retained | Different original raw peak selector could produce different summaries |
| TN1749 reproduces every experiment's failure mechanism and peak ordering | Contradicted as a universal statement /E | Report itself identifies mechanism and initial/secondary-peak differences | A separately documented model revision could improve this; it is not shown by these comparisons |
| Exact original-to-TN load, angle and sample processing is reproduced | Underdetermined /D | Missing channel recipe, printed-equation issue, unspecified table membership | Acquire synchronized original data and the actual TN comparison selectors/code |
| These tests validate WTC7's heated full-building sequence, or prove deliberate collapse | Unsupported by this unit /E | No WTC7-specific heated/composite/global test or operational evidence | Requires building-specific independent validation or distinct affirmative mechanism/operational evidence |

## Highest-value next evidence

AppendixG of the original does not contain data arrays; it directs readers to
the MSOE campus library for access to the experimental data. This is a specific
retrieval lead, not verified present-day availability. No contact was made.
The useful package would include synchronized load-cell, displacement and
strain channels; units, signs, calibration/tare and channel-combination rules;
the actual rotation calculation; test interruptions, discarded intervals and
failure-event timestamps. NIST's exact comparison inputs, peak selectors,
membership and variance convention are separately needed.[^1]

A future authorized raw-data test should preserve both initial and later peaks,
compare each test before pooling, and retain the actual failure mode and stage
alongside capacity and displacement. A separate test of WTC7 model fidelity
would additionally require a documented material/connection mapping, thermal
conditions, restraint and historical run state. The present study supplies
neither that mapping nor a justified replacement for missing properties.

## Sources

[^1]: Scott L. Thompson, *Axial, Shear and Moment Interaction of Single Plate “Shear Tab” Connections*, MSOE, May2009. [Institutional record](https://msoe.tind.io/record/979), [institutional PDF route](https://milwaukee.ent.sirsi.net/client/en_US/search/asset/901/0), [preserved source](sources/MSST_Thompson_2009-sirsi.pdf). Physical and printed pages coincide: conditions59–78;3ST1 narrative79–81;5ST1 narrative95–97;Tables4.1–4.4 and statics103–107; separately available experimental data182. Administrative/signature page183 excluded. Acquisition details and review coverage: [original-source review](original-source-review.md), [definition review](definition-crosswalk-review.md).
[^2]: Joseph A. Main and Fahim Sadek, *Robustness of Steel Gravity Frame Systems with Single-Plate Shear Connections*, NIST TN1749, July2012, including February2013 corrections. [Official PDF](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1749.pdf), [preserved source](../connection-calibration-audit/retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf). Physical41–47 / printed23–29: setup, calibration/assumptions, response comparisons, tables and equilibrium/rotation definitions; bibliography physical113 / printed95. This is not the2008 WTC7 report or the separately sought2008 Sadek paper.
[^3]: [Arithmetic protocol](ARITHMETIC-PROTOCOL.md), [stage-sensitivity protocol](STAGE-DIAGNOSTIC-PROTOCOL.md), [root table results](root-results01.json), [native-stage results](root-stage-results01.json) and [validation](validation.md). These are research calculations on published printed values, not new experimental measurements.
