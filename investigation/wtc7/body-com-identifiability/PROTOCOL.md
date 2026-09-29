# Body/center-of-mass identification test

2026-09-24. Research-only Q04/Q05/Q06/Q10 under the main-repository charter.
Previous turn is progress: the debris-source correction and independently
reproduced finite-interval force bound changed the next scientific dependency.
Do not repeat those calculations or substitute source-review counts for a
historical force result. This unit tests that dependency, not a new cause model.

## Scope and acceptance

Determine whether currently held, already-reviewed motion and model records
identify a fixed material set whose three-sample COM curvature can be bounded
tightly enough to use the preceding force test. Separate three candidate
systems: the original building material, a specified upper material region,
and the visible north facade or a specified component subset. An attached
subset is a valid material system; its attachment forces are external to it.
Mass crossing a spatial boundary is a different, open-system problem.

Deliver a source-linked dependency table, explicit mathematical nonidentification
examples, sufficient-condition bounds, independently checked synthetic controls,
and a concise conclusion stating which actual records would discriminate.
Do not require a numerical total mass merely to compute a force/weight ratio;
do not require a detailed mass model where a verified full-body geometric
envelope supplies a valid bound. Conversely, matching two image features cannot
be silently upgraded to a rigid body or hidden-mass history.

Root reads the existing metric-motion, lateral-geometry, Camera3 endpoint,
conditional-trajectory and facade-feature reports, multipoint-table report,
Camera2 paper/frame join and target-trackability report. A separate source
reviewer reads the existing model-member-map and material-run-crosswalk plus
directly necessary ledgers and the current facade/paper-join reports. These
are verified or qualified research derivatives, not new primary-source
inspection. Their source/page/file links remain the upstream provenance;
hash selected derivatives and any actual numeric dependencies. No claim of
exhaustive repository search or unseen full-deck/PDF inspection.

An independent mathematical reviewer starts from the prior force protocol,
without reading root's new construction/results before freezing its own
derivation. Root and reviewer may exchange scope corrections, with that
exposure declared. Reviewers are AI analyses, not human engineering opinions.

## Prospective mathematical controls

Use synthetic arbitrary length/time units, never WTC7 dimensions or an assumed
historical motion history. No new image measurement, fit, clock choice, model
execution, acquisition, optimization or cause probabilities.

1. Fixed-mass decomposition: show explicitly how changing unobserved component
   motion can change COM while preserving selected visible-point histories.
   Preserve fixed positive weights and distinguish absence of an observation
   constraint from mechanical admissibility in an actual building.
2. Rigid-body geometry: test whether collinear perfectly known 3D markers fix
   the body's pose/COM. Construct a proper rotation about their line and check
   identical marker coordinates, changed off-line COM and distance preservation.
   Then add a known off-line marker as a positive discrimination control.
   The held four roof labels have not been proved collinear material markers;
   the construction applies to that reduced ideal observation set, not every
   pixel of the actual videos.
3. Sufficient bounds: derive COM intervals from full-material vertical
   envelopes and, where supplied, positive fixed mass fractions. Propagate
   interval endpoints through the three-sample second difference; demonstrate
   both loose and discriminating synthetic cases. Unknown dependence across
   times may make box bounds conservative, never a guarantee of realizability.
4. Clarify the preceding B parameter as deviation from an affine trend in
   roof-point/COM separation, not a direct peak-to-peak separation change.
   Verify its exact minimum for three equally spaced samples. State sufficient
   rigidity/pose/COM-geometric prerequisites rather than assuming them.

After both derivations are frozen, compare algebra and implement a small exact-
rational control set with separate verification. Pin code/protocol/input reports
and runtime; create-only products; one deterministic repeat. Select all finite
synthetic cases before numerical evaluation. No toy case may be represented as
a mechanically realizable WTC7 reconstruction or evidence favoring a cause.

## Boundaries and stop rule

Close this particular dependency audit when the held-record join and exact
mathematics have been critically checked, either with an actual justified
historical bound or with a specific account of what remains unidentified.
Missing calibration is not evidence that the published motion is wrong;
missing hidden-mass motion is not license to assert unlimited real deformation.
No numerical historical B will be invented. A complete image sequence could
exclude a toy construction even if a reduced point set cannot.

Work only in this investigation worktree. Preserve main/raw/legal/accepted
Sherlock/Faraday state and previous derivatives. No outreach, paid software,
new bridge call, disclosure, publication, commit or push. Log a new software
fixture only if this exposes a genuinely additional, deduplicated need.
Leave the full goal active; closing this audit is not completing WP2/WP3.

## Exact synthetic fixture declaration, before either implementation runs

After the mathematical reviewer froze its derivation by message, root selected
the following minimal finite cases and sent the same specification for a
separate implementation. No numerical results or implementation were exchanged.
All units below are arbitrary synthetic units; g_ref=10 and visible p(t)=5t^2.
Samples are t=-h,0,h; these are not event-onset windows or historical dimensions.

- Hidden component: eta in {1/4,1/2}, h in {1,2}, B in {1/10,1/2}, all eight
  combinations. Visible COM=p; baseline hidden COM=p+4; alternative hidden
  COM=p+4-(B/eta)*(2*(t/h)^2-1). Fixed mass fractions 1-eta and eta. Verify
  identical visible trajectories, changed combined COM, curvature difference,
  and exact three-sample affine-removal residual. No feasibility claim about
  connections, clearance, energy or an actual building.
- Rigid component: h in {1,2}, L in {1,3}, endpoint (cos,sin) in
  {(4/5,3/5),(3/5,4/5)}, all eight combinations. Rotation is about local x;
  middle is identity and both endpoints use the same positive angle, admitting
  theta(t)=theta_endpoint*(t/h)^2. Translation is p(t) in downward z. Local
  roof markers are (-1,0,0),(0,0,0),(1,0,0); an off-axis marker is (0,0,1),
  and local COM=(0,0,L). Compare with constant identity orientation; check
  proper rotations, distance preservation, invariant roof markers, changed
  off-axis marker/COM, and exact B*. Recover the known proper pose with the
  noncollinear marker and reject the collinear-only construction as rank deficient.
- Full-body envelope: h=1, relative vertical offset q=z-p is in [0,2] at all
  three samples, or [9/10,11/10] at all three. Enumerate all eight endpoint
  combinations, and verify a fixed positive two-mass mixture (weights1/3,2/3)
  remains inside the corresponding convex bounds. Compare resulting net-force
  intervals with the illustrative lower fraction1/4. These are a loose-bound
  and a discriminating-bound control, not historical uncertainty proposals.
- Affine-removal control: show B*=|r_--2r0+r_+|/4 for equally spaced samples
  using the cases above plus zero/linear/quadratic synthetic triples, preserve
  the residual witness and reject nonpositive half-spans and invalid envelopes.

The exact algebra is independently derived. Root and reviewer use distinct
implementations and freeze outputs before numerical comparison. One repeat
per implementation establishes determinism, not scientific validation.
