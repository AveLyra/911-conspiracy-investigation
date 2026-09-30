# Crucial Findings: WTC 7

**Status:** Research summary, updated September 29, 2026. This is not an expert
report or a final determination of the collapse cause. Read the linked reports,
protocols, and source records for the full methods and limits.

## Summary

There is substantive reason to test the robustness of NIST's specific
fire-triggered collapse sequence and to seek a more complete record of its
model inputs and outputs. Independent work also proposes other technically
possible pathways, including another fire-driven pathway. The material reviewed
here does **not** establish that NIST falsified records, that demolition
occurred, or that competing causes have equal probability.

NIST's account is a physically motivated, building-specific model. Its key
historical links—from actual fire exposure, through timed loss of structural
capacity, to the observed global collapse—have not been independently
reproduced from the public record reviewed in this project. That is a
reproducibility and validation gap, not proof that the account is false.

## Findings that put pressure on NIST's specific account

### 1. The critical sequence depends on model choices that need testing

NIST combined a detailed fire and structural-damage analysis with a separate
global-collapse analysis. Its published comparison reports a 3.5-hour damage
state that did not initiate global collapse and a 4.0-hour state that did.
The repository's review finds no public run series demonstrating how robust
that transition is to intermediate fire histories, damage transfer, connection
behavior, and failure criteria. A threshold in a model is not inherently
suspicious; its sensitivity matters because it carries a major causal step.

NIST acknowledges that after global collapse begins, its analysis predicts
large inward deformation of the upper exterior walls that is not visible in
the video. NIST also reports sharply increased uncertainty during breakup and
says its analysis omitted nonstructural components that contribute stiffness
and strength. This is a direct model-to-observation mismatch in the late-stage
exterior response. NIST's explanation accounts for why it expects divergence;
it does not validate the predicted wall motion. The late-stage animation
therefore cannot serve as visual confirmation of that response, and treating
it as such is methodologically dubious. See [Exhibit A: NIST's methodologically
dubious late-stage exterior-motion validation](research/wtc7-video-comparison/nist-simulation-footage-crosscheck-2026-09-30.md).
This finding concerns late-stage exterior behavior; the Stage 2 near-free-fall
interval constrains motion but does not identify what initiated collapse.

### 2. Released input data contain a specific unresolved anomaly

In the released thermal input, the repository audit found 63 nodes in the
modeled Column 79 region with two unequal temperature coefficients each. Those
nodes connect to only one modeled part, so sharing between parts does not
explain these repeated rows. The audit could not determine how the solver
processed them or which temperature was effective. This is a concrete
provenance and processing question—not evidence, by itself, of wrong
temperatures or deliberate manipulation.

NIST's public materials also do not include all detailed inputs and results
for its collapse models. NIST says it withheld specified files under a
public-safety provision. Their absence limits independent reproduction; it
does not establish that the withheld material would contradict NIST.

### 3. Other analyses challenge uniqueness, with important qualifications

- The University of Alaska Fairbanks (UAF) team's 2020 report concludes that
  fire did not cause the collapse. UAF identifies Architects & Engineers for
  9/11 Truth as the project's funder. The repository audit finds that the
  report's best-matching global-motion scenario prescribes broad core and
  exterior column failures; it therefore does not identify what historically
  caused those failures. The audit also notes that the report excludes P-delta
  effects from its described global analysis and does not reproduce the roof
  kink. These points limit the report's force as proof that progressive
  collapse was impossible; they do not erase it as a competing analysis.
- Orabi, Jiang, Usmani, and Torero's 2022 *Fire Technology* paper models a
  possible hydrocarbon fire in a mechanical space damaging the transfer
  structure and removing core-column support. It challenges the idea that
  NIST's exact sequence is the only possible fire pathway. The paper's model
  shows feasibility under its assumptions, not that this event actually
  occurred. NIST says it considered diesel fires and rejected their role based
  on its evidence and analysis.

## What these findings do not establish

- Near-free-fall motion does not, by itself, prove simultaneous removal of all
  supports or identify the initiating cause.
- A simulated deletion or removal of model elements describes a modeling
  operation; it is not direct evidence that physical members were cut or
  removed.
- Missing, withheld, repeated, or mismatched records do not alone establish
  fraud, concealment, explosives, thermite, or a coordinated operation.
- A weakness in NIST's exact pathway does not rule out every fire-driven
  mechanism. A competing model also needs authenticated inputs and tests
  against independent observations.
- The current record does not support a defensible numerical probability
  ranking of fire, deliberate support removal, or other causes. Unresolved
  does not mean equally likely.

## Best next tests

The highest-value work is to map each published result to the exact source
files, model version, solver inputs, transfer steps, run history, and output;
resolve the repeated thermal assignments; and test the 3.5-to-4.0-hour
transition across justified intermediate and perturbed cases. Compare model
outputs with video features and timing that were not used to choose or tune the
run. For every proposed alternative, identify a specified physical mechanism
and evidence that can distinguish it from ordinary fire and structural-failure
pathways.

## Source map

- Project overview and calibrated summary: [README](README.md)
- Current assessment: [causal-chain synthesis](investigation/wtc7/causal-chain-synthesis/report.md)
- NIST-specific proposition audit: [claim-strain audit](research/nist-claim-strain-audit.md)
- Late-stage simulation/footage mismatch: [Exhibit A](research/wtc7-video-comparison/nist-simulation-footage-crosscheck-2026-09-30.md)
- Thermal input anomaly: [thermal-assignment trace](investigation/wtc7/thermal-assignment-trace/report.md)
- UAF method and limits: [UAF final-report audit](investigation/wtc7/uaf-final-method-audit/report.md)
- Alternative fire path: [Orabi et al. research note](research/orabi-2022-alternative-fire-records-lead.md)
- Primary sources: [NIST NCSTAR 1-9](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf), [NIST WTC 7 FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation), [UAF project page and final report](https://ine.uaf.edu/wtc7), and [Orabi et al. paper record](https://discovery.ucl.ac.uk/id/eprint/10146056/).
