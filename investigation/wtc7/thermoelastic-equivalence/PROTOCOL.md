# Loaded elongation versus restrained force: method test

September27,2026. Research-only elementary mechanics; no historical simulation.
The previous turn completed the declared primary-source restraint audit:
progress. Main CHARTER and preservation/privacy/human gates remain controlling.

## Question and limits fixed before execution

Does matching axial elongation at one fixed tensile load require matching
axial force under a prescribed-length boundary condition? Distinguish this
logical question from whether a specific NIST temperature/coating pair actually
violates equivalence. No native cases, heat-transfer solver, graph tracing,
material calibration or WTC7 geometry is supplied or reconstructed here.

Derive from a stated one-dimensional small-strain linear thermoelastic law,
axial equilibrium and compatibility. Piecewise temperatures/moduli may vary
along a series bar. Same reference geometry/material law for both candidates;
no lateral instability, bending, plasticity, creep, contact or failure law.
Axial guide constraints are idealized and cannot predict buckling survival.
No claim these temperatures result from historical coating or fire conditions.

The mathematical issue is already suspected from the preceding source audit;
fixtures are deliberately constructed, not blind samples or probability data.
Exact arithmetic verifies implications/counterexamples within the assumptions,
not physical or historical validation. Preserve failures and revisions.

## Reference and boundary conventions

Stress-free reference temperature T0 is common. Let dimensionless temperature
rise theta=(T−T0)/Tscale, with arbitrary positive Tscale. Length is normalized
by L0 and force by A*E0; both bars have the same constant area A, common
reference modulus E0, reference length L0 and no initial thermal strain.
Choose thermal free strain theta/1000 and E(theta)/E0=1/(1+beta*theta^2),
beta>=0. This is a synthetic constitutive law, not a fit to steel data.
Three equal reference-length segments unless a named refinement control says
otherwise. Positive force/displacement denotes tension/elongation.

Fix reference tensile preload p=1/1000 and second probing load p2=1/500.
The common cold compliance is1 in normalized units and the cold loaded
elongation is p. Report total hot elongation from stress-free length. For
each probing load n in {0,p,p2}, report both explicitly labeled increments:
delta_hot(n)−n (its own cold load-controlled baseline) and delta_hot(n)−p
(the common reference preloaded length). The preloaded clamp always uses p,
not p2. This clarification was added before execution after both independent
reviewers identified the original increment-label ambiguity; no prior result
or fixture is discarded.

Compare two distinct clamp experiments without mixing conventions:

1. Cold stress-free clamp: total length remains L0, normalized elongation0.
   Report total reaction force (negative means compression).
2. Cold preloaded clamp: first apply p at T0, then lock the ends at L0*(1+p)
   and heat. Replace the load-controlled end by the clamp; do not also retain
   an independently prescribed end traction p. Report total force and its
   change from p. Both candidates share this same initial state.

## Fixed fixtures, outputs and discriminators

- Variable modulus beta=1: uniform hot theta=[1,1,1] versus spatially variable
  theta=[0,0,2]. Compare loaded total/incremental elongation at p and p2,
  stress-free thermal elongation, effective axial compliance, both clamp
  forces and preloaded-clamp force increments. Exact equality/inequality,
  not a fitted tolerance. All cases reported; no favorable selection.
- Zero heating, identical profiles, and segment subdivision/reordering are
  controls. At cold/preloaded clamp the force must remain p; cold/unloaded
  clamp must remain0. Subdivision preserves geometry and state, not inputs
  silently changed to obtain a pass.
- Constant-modulus beta=0: [1,1,1] and [0,0,3] have equal mean thermal strain.
  Determine whether both clamp responses then agree. This is a positive
  control, not an alternative historical material model.
- Two-load identification: at fixed temperature state, evaluate elongation
  at0,p,p2. Derive which thermal/compliance quantities two distinct loads
  identify. Test coincident-load rejection. This load-independent-temperature
  linear law is essential; nonlinear/damage-dependent behavior is excluded.
- Full-trajectory objection: derive, without a thermal PDE, whether the
  same logical issue can persist along a continuous monotonic heating path.
  Uniform theta=s; variable theta=[0,0,q(s)], with q>=0 defined by
  q^2+q=3*(s^2+s),0<=s<=1. Verify the algebraic identity and endpoint(s)
  exactly; do not sample floats and label that proof. This is a constructed
  admissible constitutive-state path, not a physically solved heat field.

Acceptance requires a derivation, exact fixture output with retained units/
conventions, conditions under which transfer does hold, independent mechanics
derivation/calculation, synthetic positive/negative controls and repeated
deterministic runs. Independent checker must not import root functions or
read root results before freezing its own. No numerical probability, collapse
prediction, model-falsification or causal ranking follows.

Root owns this protocol, `calculate.py`, root result files, report and status.
A separate reviewer owns `independent-review.md` and optionally `oracle.py`
and oracle outputs, using this protocol but not root implementation/results
until its freeze. A third reviewer may critique the derivation and final
inferential ceiling. Inputs/program hashes accompany saved runs; outputs
are create-only. Use standard-library exact rationals; no dependency install
or external solver. No browser UI change or browser testing is needed.

## Work boundary

Only this research directory and existing navigation/feedback notes may change.
No main/legal/raw source/accepted engine edits, original drawing access,
outreach, fees, publication, sensitive transfer, stage, commit or push.
The prior [source audit](../contracting-access-custody-audit/restraint-followthrough-2026-09-27.md)
is motivation, not proof of the synthetic result. Completion here is only
this inference check, never completion of the comprehensive investigation.
