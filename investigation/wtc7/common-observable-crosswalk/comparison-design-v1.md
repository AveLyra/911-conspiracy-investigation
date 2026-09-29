# Prospective NIST/UAF comparison design — version 1

2026-09-26. **Working research; reviewed design, not an execution-ready
protocol. No simulation authorized by this document and no new simulation
performed.** Review disposition and final design hash are recorded in
[design validation](comparison-design-validation.md). This extends the existing
[five-observable crosswalk](report.md) and its [Faraday draft alignment](draft-alignment.md),
not a second investigation framework or an accepted Faraday protocol. The
[main charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
controls scope, resources, human review and inference. Source records outrank
our summaries. This design does not change the legal record or cause ranking.

## Authorization, deliverable and acceptance

The user's current instruction adopts documented defaults: compare NIST's
publicly reproducible pathway and UAF's published support-loss pathway;
use common geometry/material assumptions where possible; isolate causal
factors; measure initiation, roof/penthouse motion and failure sequence;
use independently timed trajectories with uncertainty; predefine scores;
preserve missing inputs; and infer robustness, not historical intent.

The deliverable now is a reviewed, locally hash-frozen **design**, an explicit
missing-input gate and a finite execution-annex specification. Design freeze
is not executable-protocol freeze. No default can manufacture an unavailable
deck, validate a substituted connection law, or supply human acceptance.
The user need not choose every parameter: investigators choose and document
defensible settings under the rules below; new cost, disclosure, expert
engagement and execution authorities remain governed by the charter.

Acceptance for this design: all requested factors/outcomes have a defined role;
native reproduction is separated from modified common-assumption tests;
motion fit is separated from initiation; score and inclusion rules precede
new runs; material unresolved inputs remain gates; independent critical review
is answered or prominently unresolved. No claim that protocol compliance alone
makes a result scientifically valid. Numerical verification, measurement
validity and physical validation remain separate requirements.

This is prospective only for future work. Prior findings and published curves
are already known. It is not blind preregistration or an unused-data validation.

## 1. The comparison question and its strongest limitation

Which **specified implementation** reproduces the independently checked common
observations across defensible parameter ranges, with less dependence on
unverified choices? Report a partial ordering or non-identifiability when
appropriate. Do not assign historical probabilities from simulation success
fractions or imply that failing one implementation eliminates its whole family.

There are two distinct comparisons:

1. **Conditional mechanics:** given each declared starting state and support
   history, what subsequent motion emerges? A prescribed-loss model can be a
   useful comparator here without explaining what produced its loss.
2. **Initiation and causal-chain adequacy:** what exposure or other physical
   process actually generates that state and loss, with what evidence? Missing
   initiation evidence stays missing even if terminal motion fits well.

Strongest objection: an inverse fit to the one historical collapse may remain
non-unique, especially if support removals or timing were selected using that
same motion. A better terminal fit need not imply a more probable historical
cause. Conversely, a more mechanistic narrative receives no credit for an
unverified link merely because its equations are plausible.

## 2. Reproduction and matched modification are separate lanes

**Lane N — native documented cases.** Attempt each nominated published case
with its actual geometry, settings, inputs, solver/build and case history.
Reproduce author-reported output before changing assumptions. Preserve failed,
non-collapse and numerically invalid attempts. A syntax check, gravity-only
initialization or visually similar animation is not a collapse reproduction.

**Lane C — common-assumption comparisons.** Only after a source-linked mapping,
create named research variants with shared geometry, mass/gravity, material
laws, connection/contact descriptions and observation projection wherever
physically applicable. Map node/member/architectural identities explicitly.
Different discretizations may be acceptable; undocumented equivalence is not.
Record every departure from each native case. These are modified research
models, not exact reproductions of either institution's published result.

Match the complete initial state as well as labels: equilibrium, mass and
gravity loads, temperature/history, residual stress/strain, deformation,
velocity, contact state, pre-damage and surviving restraint. A solver handoff
must account for transferred and omitted state, including stored and kinetic
energy. Define the common comparison stage and any history-dependent
differences deliberately retained. A mismatch in any of these
is a declared contrast/confounder, not silently a test of the nominal factor.
Check state transfer and balance in the component benchmark. If a physically
consistent common state is unavailable, gate that contrast; native reproduction
remains separately reportable and the unequal-state comparison is a package
comparison, not an isolated causal factor.

Do not force equivalence between static and dynamic analyses, incompatible
contact/failure formulations, or different solver abstractions. An unmatched
subsystem makes the relevant comparison unmatched, not automatically inferior.
Use a small common component benchmark to check a proposed mapping before
whole-building use; a successful benchmark alone does not validate the building.

## 3. Current dependency gate — not an assertion of permanent unavailability

The existing [native UAF locator](../uaf-native-case-locator/report.md),
[released-member audit](../model-member-map/report.md), and primary-source pins
in the completed crosswalk control these inherited limitations. They must be
rechecked against materially new files before execution, not silently treated
as current global availability findings.

- **NIST:** a released global-input subset exists. The earlier content audit's
  shell-row overcount is corrected in the member audit; use that correction.
  The supplied active deck's gravity-stage termination, commented later damage
  hooks, missing/native restart choices, specialized connection behavior,
  unresolved references/thermal assignment rules and input-to-output case
  linkage do not yet establish a reproduced full fire-to-collapse chain.
  The [thermal trace](../thermal-assignment-trace/report.md) locates NIST's
  reported build (mpp971dR4 beta, revision 41161, double precision); the actual
  executable and its use with these bytes remain unauthenticated. Do not
  regress to claiming that no build was reported.
  Do not activate comments or choose a missing handoff file and call that the
  historical run. Preserve the named 3.5-hour non-collapse control as a desired
  paired case; absence is not a modeled collapse or non-collapse result.
- **UAF:** the held selected ZIP was a README wrapper, not the native final
  case. Exact final-report case/member identity, removal schedule and the
  acceleration/resistance function's implementation **and calibration history**
  remain unresolved in the bounded locator. The advertised larger archive may
  contain useful inputs; that possibility is not a recovered case or authority
  to retry an unsafe route or download hundreds of gigabytes.
- **Observation:** the five families have a source crosswalk, not a completed
  independently calibrated common trajectory set. The user's report that the
  R1 viewer cannot show reliable pixel coordinates is not a human location
  check. Existing human spot-check gates stay unmet unless actually completed;
  defaults do not replace them. R1 is a different-building comparator and does
  not supply WTC7 coordinates, source independence or a WTC7 error model.
- **Execution:** no source-pinned complete pair, solver/build/license audit,
  finite resource budget, verified adapter and numerical acceptance envelope
  is established by this design. Do not launch a solver to discover whether
  undocumented inputs happen to give an appealing collapse.

Thus “NIST's publicly reproducible pathway” is a target to test, not a premise
already established. Neither side gains scientific weight from relative ease
of acquisition. Missing dependencies block only the affected calculation;
documentary criticism and useful independent observation work can continue.

## 4. Fixed observational contracts

Reuse the five families in the crosswalk. The execution annex must identify
actual member/feature IDs, footage hashes and exact evaluation domains before
new model output is inspected. Do not silently substitute near-camera occlusion
for a structure passing through its own roof, an eastern onset for northwest
motion, or roof motion for the building's center of mass.

| Family | Primary quantity | Non-interchangeable / secondary quantities |
|---|---|---|
| East penthouse | Same visible feature's projected position and onset interval | Hidden column instability and disappearance are separate events. If onset sets alignment, its timing gets no predictive score. |
| West penthouse | Defined first/final roofline-passage interval, view and moving/reference roof specified | Track partial occlusion/reappearance. Generic onset cannot substitute for complete passage. |
| North roof/façade | Named roof-feature projected position history and onset interval | Velocity and acceleration are correlated derivatives, not extra independent wins. No assumption of rigid-body or whole-COM motion. |
| Lateral deformation | Named component's projected lateral displacement/shape at matched stages | Unseen depth is unknown, not zero. A corner trajectory does not measure final debris containment. |
| North-roof kink | Bend location/shape and appearance interval on a defined roof segment | Distinguish physical member namespace, visible threshold and alleged initiating failure. |

Failure-sequence scoring uses the ordered/bracketed **visible events** above.
Separately log simulated internal initiations and failures as model outputs;
do not score hidden support losses against invented video observations.

### Video and timing defaults

Preserve native frames, PTS/time base, interlace/blend/duplicate diagnostics,
camera motion and provenance. Independent annotation means a separate
measurement process, not another file copy or another AI counted as a witness.
Record prior exposure and common-source ancestry. A genuine held-out view,
feature or interval must have been unused in calibration; otherwise mark the
test retrospective. Another view of this collapse is not a second event.

Use source-linked physical feature identity and camera projection. Native-pixel
position comparisons are permissible when common projection is authenticated;
metre estimates require defensible scale/depth calibration. Keep annotation,
registration, clock, projection and model-discrepancy uncertainties distinct.
Retain raw reader disagreement. Obscured or unidentifiable points are missing,
not stationary. Overlapping copies do not gain additional statistical weight.

Before evaluating model runs, freeze each usable source's frame window and
sampling rule, calibration inputs, onset threshold/persistence rule, visibility
rules, uncertainty construction and any displacement-fit/differentiation method.
Set these from source quality, controls and declared resolution needs, not
the size of a NIST/UAF discrepancy. Test the measurement pipeline against
known synthetic trajectories and obtain the required actual-human spot checks.
An unmeasurable required family makes the overall comparison incomplete.

Use at most one model-to-observation time alignment per full case, with a
declared anchor and uncertainty; no per-feature realignment or unrestricted
time warping. If anchor uncertainty varies, propagate the **same** shift to
all features. Observation-to-observation camera synchronization comes from
identifiable shared events/clocks, not matching a model's predicted sequence.
No absolute initiation-time claim when only relative time is available.

## 5. Controlled factor plan and range-selection defaults

Do not call an arbitrary percentage perturbation “standard” or “conservative.”
A choice conservative for one failure mode can favor another. Use reported
case values first, then independently supported measurement/material bounds.
Record source, physical role, units and rationale for each bound. Unknown
bounds remain unknown; broad exploratory ranges are not historical priors.

Start with nominated native baselines and a verified common baseline where
possible. One-factor-at-a-time (OFAT) runs diagnose local influence; they are
not sufficient to establish global robustness. The execution annex fixes all
levels and resulting run IDs in advance, with a numerical run/resource cap.

| Factor | Isolated contrast and safeguard |
|---|---|
| Fire exposure / resulting thermal field | Vary one documented exposure or thermal-state dimension at a time; maintain its causal dependencies. Do not vary ambient fire and assign an inconsistent steel field simultaneously. |
| Support-loss history | Use exact published member identities/schedules and declared nearby timing/location alternatives where justified. This is a mechanical prescription, not a demolition-device model or proof of an initiating process. |
| Debris damage | Separate initial impact/damage state from later falling-structure contact. Label source/pattern uncertainty; no silent arbitrary cuts. |
| Connection behavior | Source-linked constitutive/failure law or independently justified bounds; carry geometric/material consistency and temperature dependence. Substitution is explicit. |
| Deletion/erosion rules | Separate prescribed historical handoff from numerical failure/erosion. Track removed mass, momentum, energy and surviving load paths; avoid making vanished elements silently erase resistance. |

After OFAT, test these predeclared interactions wherever applicable and
implementable: thermal state × connection behavior; connection behavior ×
failure/deletion rule; initial debris damage × thermal state; support-loss
schedule × connection/contact behavior. For each applicable pair, run the
four low/high combinations within the source-supported levels, retaining
the baseline. Deduplicate identical input states by hash. If a pair is
inapplicable, explain physically; if it is unavailable, say not tested.
Changing more than one setting defines an interaction run, not an OFAT run.
Define the physically feasible joint parameter domain before selecting the
grid: incompatible endpoint combinations stay labeled infeasible with reasons,
not executed as physical candidates. Categorical alternatives use their actual
named laws/states and a finite declared combination table, not artificial
numeric low/high ordering.

Pairwise tests do not establish robustness over all higher-order interactions.
Endpoint tests also miss nonmonotonic interior behavior. Include each
independently documented interior level in the annex's fixed one-factor grid;
where a continuous range has only justified endpoints, predeclare a midpoint
diagnostic as an analyst-selected level, not a historically probable value.
For an applicable two-factor grid, include the center and edge-midpoint
diagnostics before execution, alongside its four corners. For categorical
laws with no meaningful interpolation, use named alternatives, not an
invented midpoint law. A finite grid still establishes only tested-point
behavior. No assertion of an entire stable parameter interval without an
additional justified bound or declared refinement test. Report coverage
explicitly. Do not fit parameters using the test residuals.
Any later search/optimization gets a new exploratory version and cannot turn
the original result into a prospective success. If stochasticity is involved,
freeze the seed list and repetitions before runs; deterministic repeatability
is not physical validity.

## 6. Predetermined comparison and reporting rules

Primary reporting is a **vector by observable family**, not a visually chosen
winner, aggregate probability or count of screenshots resembling the footage.
Use the same assessable features/windows for each matched contrast. Also
publish full per-model coverage so intersection-only scoring cannot hide a
missing or unfavorable feature.

Define observational support without looking at whether a model predicts it.
A solver/output-export failure is a technical failure or missing output;
a verified physical failure to produce an observed feature is a model
discrepancy. Neither silently removes that observed feature from scoring.
Retain the common observational support, classify the reason, and mark the
overall comparison incomplete where the required prediction is unavailable.
Do not treat model-specific missingness as a favorable low residual.

For a scalar observation with a defensible bounded interval O=[lo,hi] and a
projected modeled value y, report distance to the interval:
`d = max(lo-y, 0, y-hi)` in physical or native-image units. An interval overlap
has zero incompatibility distance; it is **not** confirmation or equal accuracy.
For event intervals use the analogous gap
`d = max(observed_lo-model_hi, model_lo-observed_hi, 0)`.
Intervals must include their actual declared uncertainty and censoring limits,
not be widened after seeing a mismatch. Two-dimensional tracks retain both
coordinates/joint bounds; do not ignore an inconvenient component.

Pointwise interval distances are descriptive diagnostics, not a joint-fit
test. Shared alignment, calibration and camera parameters must have a single
jointly feasible assignment for the complete run across all features/times.
Freeze their admissible set from external calibration. Show the metric vector
across that set (or a declared verified enclosure); separately favorable
pointwise minima do not establish one feasible matched trajectory. If a
nuisance parameter is fitted, disclose the calibration evidence used and
evaluate on separately declared observations where available. Do not tune
nuisance bounds using the very discrepancy under examination.
Do not add an unspecified model-discrepancy allowance to observation bounds
to absorb a failed prediction. Retain raw gaps; any externally justified
predeclared discrepancy allowance has a separate, explicitly conditional role.

Per feature and measured quantity, retain full signed gaps, interval
gaps, maximum gap and time-weighted RMS gap over the frozen observed domain.
For a scalar interval, the signed outside-gap is `y-hi` above, `y-lo` below
and zero inside; a point-estimate residual additionally requires a declared
point estimator. Do not treat an interval's midpoint as known truth.
Event times, positions, shape metrics, velocities and accelerations stay
separate even within a family. The default is to keep feature/quantity/view
sub-vectors, with no automatic family average. Any optional summary must
combine only commensurate quantities under an annex-frozen formula and feature
list; it must not give one feature extra weight merely for extra views or
post-hoc subdivision into more points. Retain per-view results and shared-origin identifiers.
Do not average native pixels from differently scaled views; use each view's
own output or a verified common physical scale. Dense duplicate frames must
not dominate. Normalize only by a pre-run justified resolution/tolerance
scale, never by a value fitted to favor a model. Without defensible scales,
report units separately and **do not compute a cross-family score**.
Freeze the time-weight/integration and interpolation rule, joint-coordinate
distance rule, missing-segment treatment and covered-duration reporting in the
annex. No interpolation across an unobserved gap to enlarge coverage. Censored
passages retain their censoring, not fabricated finite event times.
No p-values or confidence levels from these deterministic gaps without an
additional justified stochastic/error model. No independence multiplication
of position, velocity, acceleration or copied footage.

The five family results, visible event order and quality flags stay separate.
Call a case **incompatible with an observed feature** only when a repeatable
discrepancy survives the frozen measurement/calibration bounds and numerical
resolution checks. A solver-invalid case is numerically invalid, not physical
counterevidence. A case that matches some observed families but misses another
is a partial match; do not replace it with its best sibling run for each feature.

Parameter robustness: show each scheduled run, each family's metric range,
coverage and the number of valid/invalid/missing runs. Any success fraction is
a property of this declared design grid, not a probability of historical cause
or a volume fraction under an unstated parameter distribution. Evaluate one
**whole run** across all families; never splice a virtual best-case building.

“Fewer special assumptions” is an inspectable ledger, not an invented penalty:
list free/fitted parameters, externally imposed losses, undocumented choices,
calibration evidence reused, and independent constraints. A shared uncertain
assumption remains uncertain. Do not trade a missing causal link against a
small improvement in an animation score or announce a winner by subjective
weighting after results.

## 7. Numerical validity, evidence preservation and finite stopping

Before consequential runs, freeze units, gravity equilibrium acceptance,
mesh/time-step convergence contrasts and tolerances, energy/mass/momentum
accounting, contact/penetration checks, hourglass/artificial-energy limits,
failure/erosion diagnostics, solver warnings and abort criteria appropriate
to the actual solver/formulation. Do not invent universal numerical thresholds
without the solver/component benchmark. Preserve full logs and all runs.
Mesh/time refinement that materially changes a key finding defeats a robust
interpretation at the tested resolution. Fixing a bug requires a new version
and rerunning all affected contrasts, not only the unfavorable one.

Execution annex must bind: input/output hashes and native case/version mapping;
parameter values/units/ranges; exact run table and dependencies; physical
feature/event definitions; camera/time/calibration/uncertainty contract;
measurement and solver code/environment; numeric validity tolerances;
finite compute/storage budget; stop/abort rules; resource authorization; and
separate review dispositions. Its hash must precede new runs. A Faraday draft
is not accepted/frozen engine state, and an AI reviewer is not a human expert.

Stop at the finite schedule or a declared failed prerequisite. Do not extend
the search until a favorite model wins. Incomplete comparisons yield explicit
limits and the smallest missing input/test. No new solver launch, license,
large download, outreach, transmission, filing, fact promotion or engine
approval follows from this design. Report implemented, verified, accepted
and activated separately.

## 8. Next bounded action

Review and hash-freeze this design after corrections. Build the execution
dependency table from existing inventories and the newly considered files,
without rerunning closed existence searches or attempting the same blocked
archive route. Prioritize (a) exact NIST staged case/connection/result linkage,
(b) UAF final-case/function/removal mapping, and (c) the five observation
contracts' measured-versus-missing status. A small authenticated member/case
manifest is more useful than blind bulk acquisition. If neither native chain
can be reconstructed, preserve that as the reproduction limit and proceed
only with clearly labeled, separately declared component tests or observations.

The previous 32-image light review is a separate qualitative unit and supplies
neither structural parameters nor a new initiating-mechanism observation.
The broader Luna audit and investigation remain incomplete. Generic workflow
feedback stays locally queued while the designated Sherlock task is archived;
do not reopen it or disclose case content by implication.
