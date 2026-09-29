# Independent method review of comparison design v1

2026-09-26. Working AI scientific-method review, not an engineering/expert
opinion, human acceptance, source authentication or execution approval.

## Disposition

**The comparison can be frozen as a design after the five bounded clarifications
below are incorporated or explicitly retained as unresolved execution gates.**
Do not label this reviewed snapshot an execution-ready scoring specification.
The execution annex appropriately remains gated on exact native cases,
observation/calibration contracts, adapters, numerical validity, resources and
actual required human checks. No reason to demand generic power/sample-size,
randomization or statistical-significance fields for this deterministic design.

The structure is substantively sound: native reproduction and modified cases
are separate; conditional motion is not confused with initiation; imposed
losses and calibration reuse remain visible; family vectors replace a causal
winner score; unsuccessful and missing cases remain in coverage; and a finite
schedule prevents a search until a favored answer wins. It explicitly permits
non-identifiability without asserting equal odds. These controls should remain.

The most consequential remaining risk is **apparently compatible marginal
scores that cannot be satisfied by one whole run and one common calibration**.
The draft already prohibits feature-specific time shifts, but its subsequent
interval/aggregation contract must preserve that prohibition mathematically.

## Review scope and pins

Read the complete design, existing five-observable report, draft-alignment
note and crosswalk protocol. Main AGENTS, WORKFLOW, START-HERE and the complete
investigation charter had been read in the immediately preceding task; their
current hashes were rechecked unchanged. Applied the fully read
evidence-falsification-auditor and source-of-truth-guardian skills. This review
adds only this exploratory note, with no authority-layer promotion.

| Reviewed record | SHA-256 |
| --- | --- |
| `comparison-design-v1.md` (19,934 bytes) | `5e62a5fa38b73afd75559a7c6addcd7e7a0c0a4b047b75cfa8c1190cb17ff2c2` |
| `report.md` | `952628e3fbb405f2a9f05af09546f876a567a5c9975da21442de7a74c26e6024` |
| `draft-alignment.md` | `c852c2d4c9fc1d476c9eeae18bd59b00969ec70e3332cccb8161427e3a058438` |
| `PROTOCOL.md` | `36cf535ca6080cd69955735d818f000c30cb4b510a18da372f5703efa48e9be2` |
| Main `AGENTS.md` | `01e3fbd03120a2085520818cea0a843a8c6748b4c7bb8ef0e68547c634a963cc` |
| Main `WORKFLOW.md` | `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a` |
| Main `START-HERE.md` | `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72` |
| Main `research/sherlock-wtc7-investigation/CHARTER.md` | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |

This is independent review of the draft's logic, not independent historical
evidence. I am a reused AI with prior source/render/annotation implementation
and reader roles. I did not author this design. I did not inspect new images,
native solver cases, primary historical sources, other new review conclusions,
engine state or private correspondence. Root owns the separate source review.
No external research, solver, acquisition, model fitting or source edit occurred.

## Findings and minimal corrections

Severity describes scientific consequence, not a claim of misconduct:
**High** can give a misleading agreement/comparison; **Moderate** can distort
coverage or overstate robustness. These are implementation/design ambiguities,
not findings that a bad calculation has already occurred.

### 1. High — preserve joint calibration through interval scoring

Draft language: “propagate the **same** shift to all features,” followed by
“For event intervals use the analogous gap” and separate feature aggregation.

The common-shift requirement is correct. But independently enlarging every
model/observation interval by that shift, scoring interval overlap, and then
combining those gaps could give zero everywhere using mutually inconsistent
shifts. The same issue applies to a shared camera projection, scale or
registration parameter. Pointwise or per-view envelopes can conceal it even
when the underlying raw predictions were generated from a single run.

Synthetic counterexample, not WTC7 data: two modeled event times are 0 and 2;
both observations are exactly 1; one common shift may lie in [−1,1]. Separate
envelopes are [−1,1] and [1,3], each overlapping 1 with gap zero. No common
shift gives both matches: required shifts are +1 and −1. Over all allowed
shifts the minimum maximum absolute gap is 1, since the shifted modeled times
remain separated by 2. This is not a stochastic-confidence objection.

**Correction:** state that admissible calibration/clock nuisance values form
one shared joint set per whole run. Compute family vectors at jointly
consistent values, retaining their dependence; marginal envelope overlaps are
descriptive only and cannot establish joint compatibility. If reporting a
best admissible fit, disclose the common value and predeclared selection rule;
do not optimize each family separately. Carry any shared annotation/systematic
error similarly rather than treating every time point as independently movable.
Freeze the concrete nuisance representation and numerical procedure in the
execution annex. This is a narrow completion of the existing rule, not a request
for a generic covariance/stochastic framework.

Related limit: the draft appropriately separates model-discrepancy uncertainty.
Make explicit that an unspecified model-discrepancy allowance cannot be added
to observation intervals until a failed prediction becomes compatible. Report
raw mismatch; only externally justified, predeclared discrepancy allowances
can have a stated conditional role.

### 2. High — dimensional and feature/view aggregation remains underspecified

Draft language: “Aggregate first within each physical feature and then equally
across declared features within each family,” and “Without defensible scales,
report units separately and **do not compute a cross-family score**.”

The prohibition is too narrow: a single family can contain displacement in
pixels/metres and onset gaps in seconds, or pixel tracks from different camera
scales. Raw equal averaging within that family is not meaningful. It is also
unclear whether equal weighting averages per-feature RMS values or pools their
squared gaps, and whether several views give one physical feature extra weight.
The existing instruction to retain per-view results does not resolve this.

**Correction:** keep quantity/unit/view sub-vectors within families unless
predeclared defensible scales or a common physical projection support a stated
dimensionless combination. For any permitted combination, the annex must fix
one formula, feature list and view treatment before output inspection. Do not
average heterogeneous units anywhere, not merely across the five families.
One feature's extra views are correlated constraints, not automatic extra
weight. Splitting a roof into more named points must not silently change its
importance. The small default is to retain these sub-vectors rather than add
an aggregate that is not needed for the comparison question.

“Full signed residuals” also needs a modest definition: an observation interval
does not alone supply a uniquely meaningful central estimate. For a scalar
interval, a signed outside-gap can be `y-hi` above the interval, `y-lo` below,
and zero inside; call it a signed gap, not error against a known true midpoint.
Point-estimate residuals may additionally be reported only where that estimate
and its role were declared. Two-dimensional joint bounds need an explicit
coordinate/joint-distance rule, not an implicit rectangle if correlations
exclude parts of that rectangle. These details may stay in the gated annex.

### 3. Moderate — Lane C needs a complete starting-state contract

Draft language: “shared geometry, mass/gravity, material laws,
connection/contact descriptions and observation projection wherever physically
applicable,” and “given each declared starting state and support history.”

Shared parameters do not by themselves establish a matched dynamic contrast.
An inherited thermal/deformation/damage state can also carry stress, plastic
strain, displacement, velocity, contact status and stored/kinetic energy.
Resetting one model to a gravity-equilibrated undeformed state while retaining
another's heated/deformed state can change the subsequent motion independently
of the stated varied factor. Conversely, forcing those states equal may remove
the very fire-history effect a test is meant to examine.

**Correction:** for every Lane C contrast declare the common comparison stage,
complete state/handoff variables and constraints, how each is mapped and
verified, and what history-dependent differences are deliberately retained.
Either create a physically consistent common starting state for a genuinely
matched conditional-mechanics question, or label the starting-state difference
as part of the tested package rather than an isolated factor. Verify balance
and mapping on the component/state-transfer benchmark before whole-building
use. Unavailable state mapping gates the affected contrast; it is not grounds
to invent equivalence or disfavor either model.

Native reproduction should remain independently reportable even if a common
state cannot be built. The current text already permits separately declared
component/observation work when native chains cannot be reconstructed; retain
that fallback without calling it either full reproduction or a fair whole-case
NIST/UAF experiment.

### 4. Moderate — distinguish observed missingness from missing predictions

Draft language: “time-weighted RMS gap over the frozen valid domain” and “Use
the same assessable features/windows for each matched contrast.”

These are useful safeguards, but “valid” can be misread as whatever coordinates
a model happens to retain. Predicted deletion, visibility loss, destruction of
a feature, run termination and a source-obscured observation are different
states. Dropping a model's difficult tail from its denominator can improve RMS
without improving its match. Conversely, automatically assigning an infinite
coordinate error to a physically destroyed feature is not justified either.

**Correction:** freeze observation-side time support separately from model
output availability. For each predicted disappearance/destruction, apply the
predeclared observable/event definition or mark a specific prediction gap; do
not silently shorten the scored observation domain. Solver abort/invalidity
remains numerical invalidity, not physical refutation. Keep censored event
bounds as censored, not fabricated finite passage times. Define time weights,
gap handling and interpolation in the annex; do not interpolate across an
unobserved interval merely to increase scored duration. Report covered duration
and missing segments alongside the fixed-domain metric. Existing intersection
coverage reporting should stay and include these distinctions.

### 5. Moderate — endpoint interactions are screens, not range bounds

Draft language: “run the four low/high combinations within the source-supported
levels, retaining the baseline” and “Pairwise tests do not establish robustness
over all higher-order interactions.”

The higher-order caveat is good, but another limit exists even with just two
factors: nonlinear/threshold behavior at an interior setting need not appear
at the four corners or native baseline. A support-loss location, contact rule
or connection-law alternative may be categorical, so a generic “low/high” has
no physical order. Coupled parameters can also make some Cartesian corners
physically impossible. None of this requires a vast all-factor search.

**Correction:** call these predeclared endpoint interaction screens. Specify
named categorical alternatives instead of artificial low/high labels; define
the physically feasible joint settings and preserve omitted/infeasible reasons.
Do not infer interior-range robustness from corner agreement. If component
physics/source information flags a consequential interior regime, predeclare
a small justified intermediate contrast before full-case results, or state it
as untested. A later adaptive search needs the already required exploratory
version and finite budget, not retrospective promotion of the original grid.

## Bias, falsifiability and authority assessment

No default numerical prior, percentage perturbation, fitted-removal complexity
penalty or simulation success fraction is treated as historical probability.
That is appropriate. Common uncertain assumptions must remain uncertain;
choosing one institution's native settings as the shared default would still
need an independently supported rationale or explicitly paired alternatives.
The existing source/range and assumption-ledger rules can handle this without
an additional framework.

The intended falsifiers are observable mismatches surviving declared source,
calibration and numerical bounds. They can reject a specified implementation,
not an entire fire or intervention family. The principal disconfirming concern
for a claimed terminal-motion win is calibration reuse/underdetermination;
the principal concern for a claimed mechanistic-chain win is an unverified
link. The draft treats both explicitly. No demand to prove an actor or intent
before comparing physical outputs was found.

The design's no-launch language is clear, as are the incomplete native-input
and human-check gates. “Hash-frozen design” must remain a versioned planning
artifact only; root's disposition of these issues and a changed hash are not
solver authorization, accepted engine state, physical validity or actual human
review. Do not silently update this review's reviewed-source hash after edits:
record a separate response/re-review against any changed version.

## Actual checks and limits

Read-only `sed -n` calls read the entire 303-line design in two chunks and the
complete records listed above; `shasum -a 256` checked their pins. The main
controls retained the recorded hashes. No closed historical study was rerun.

Ran a small inline read-only Python calculation with
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`
to recheck the exact 19,934-byte design hash and the **synthetic-only** event
gap example in finding 1. Actual output: separate interval gaps `[0, 0]`;
common shifts −1, 0, +1 yield gap pairs `[2, 0]`, `[1, 1]`, `[0, 2]`, with
maxima 2, 1, 2. The continuous lower bound of 1 follows from the fixed separation
of 2, not from treating three sampled shifts as exhaustive. No historical
number, uncertainty budget, score, model state or solver result was computed.

Only this review file was authored through `apply_patch`. The draft, main,
raw records, old studies, images and engines were untouched. This review does
not certify source completeness, engineering adequacy or implementability;
it identifies specific conditions under which the planned comparison would
remain interpretable. The finite execution dependency table is the next useful
step, not a solver launch or a broad repeat source hunt.

## Re-review — revised design, 2026-09-26

**Cleared for design freeze only.** No consequential unresolved issue among
the five findings above prevents freezing this revised planning design. This
is not execution readiness, engineering approval, human acceptance or engine
activation. All actual execution-annex, source, measurement, solver, resource
and required human-review gates remain operative.

Reviewed the complete revised `comparison-design-v1.md`, SHA-256
`a5fdb25d10e3610ade6892ee290f6ade026db6599c844240924cfd12138439da`.
The original review and its earlier reviewed-source hash are preserved above.
Before this append, this review file was 15,385 bytes with SHA-256
`4acf94aa4fa4e5d4628d9a485e237c42adbd21fec8341a83a8fd7901efd6ea67`.
This disposition applies only to the separately pinned revised design.

| Original finding | Revised treatment and disposition |
| --- | --- |
| 1. Joint nuisance/calibration feasibility | Section 6 explicitly makes pointwise interval gaps descriptive, requires one jointly feasible assignment across the whole run and all features/times, freezes externally calibrated admissible sets and retains joint metric vectors or verified enclosures. It forbids unspecified model-discrepancy inflation. Addressed at design level; concrete implementation remains an annex gate. |
| 2. Dimensional/view aggregation | Section 6 defaults to feature/quantity/view sub-vectors with no automatic family average; separates event times, positions, shape and derivatives; prevents differently scaled pixel averaging and extra view/subdivision weight. Signed outside-gaps are defined and interval midpoints are not treated as truth. Any optional commensurate summary, joint-coordinate distance and temporal integration must be fixed in the annex. Addressed. |
| 3. Complete matched starting states | Section 2 now names equilibrium, thermal/history state, stress/strain, deformation, velocity, contact, pre-damage/restraint, transferred energy, comparison stage and balance checks. Unequal retained states define a package comparison, not an isolated factor; unavailable common state gates the contrast. Addressed. |
| 4. Observation support versus prediction missingness | Section 6 freezes support independently of model availability, distinguishes technical failure from verified physical discrepancy, prohibits favorable dropping, preserves covered duration and missing segments, and retains censoring without fabricated event times. It forbids interpolation across unseen gaps to enlarge coverage. Addressed. |
| 5. Endpoint/interior/categorical limitations | Section 5 adds feasible-domain and categorical rules, documents nonmonotonic interior risk, specifies predeclared midpoint/interior diagnostics and explicitly limits results to tested points. Analyst-selected midpoint diagnostics are not historical probabilities or whole-range guarantees. Addressed. |

The revised interior diagnostics must still obey the feasible-domain,
applicability and finite-resource rules; this is already supported by the
combined text. They are sampling choices, not a proof of a continuous range's
behavior. No further amendment is required for design freeze on that account.

Read the complete revised file with `sed -n '1,210p'` and
`sed -n '211,430p'`; checked design and pre-append review hashes with
`shasum -a 256`. No images, primary-source reinspection, solver, new scoring,
historical measurement, downloads, engine changes or expansion of review
scope occurred. The newly clarified source/build statement is root's
source-review responsibility; this method re-review does not independently
authenticate it. Only this dated re-review was appended via `apply_patch`.
