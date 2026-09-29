# Independent mathematical and synthetic-control review

2026-09-24. Research-only review by `/root/body_com_math`, a separate AI
analysis, not a licensed engineer's opinion or an independently authenticated
historical observation. Mathematical derivation, independent synthetic
arithmetic and the assembled-text review recorded below are complete within
their stated scopes.

## Independence and actual exposure

The reviewer read the current main AGENTS, WORKFLOW, START-HERE and charter,
the evidence-falsification-auditor skill/reference, and the earlier
finite-interval-force protocol/report. The reviewer derived and sent the
hidden-mass construction, roofline-axis rotation construction, convex-envelope
bounds, rigid-pose bound and exact minimum affine residual before reading any
root body-COM implementation or output. Scope corrections were exchanged:
attachments need not vanish before a material subset can be analyzed; total
mass magnitude cancels from a force/weight ratio; entire-body geometric bounds
can sometimes replace a detailed mass distribution. Thus this is not an
isolated double-blind review of the problem definition.

Root then selected and appended the same exact finite fixture specification
to [PROTOCOL.md](PROTOCOL.md) before either implementation ran. The reviewer
implemented [oracle.py](oracle.py) without reading root code/results. Both
oracle runs and their hashes were frozen and reported before permission to
read root [calculate.py](calculate.py) and [run01/results.json](run01/results.json).
No actual historical coordinates, source video, model deck or new primary
source were read for this mathematical subtask. The earlier force report is
pinned as method context, not supplied as synthetic input data.

## Derivation independently checked

Let `A[f]=(f_- - 2*f_0 + f_+)/h^2`, with downward position positive and `h>0`.

1. **Hidden component.** For visible COM `zV=p+c`, hidden COM `zH=zV+s` and
   fixed hidden mass fraction `eta`, the combined COM is `z=p+c+eta*s`.
   Replace affine `s0` by `s=s0-(B/eta)*(2*(t/h)^2-1)` on `[-h,h]`.
   The entire visible motion is unchanged, the hidden group's departure from
   the affine relative-motion baseline s0 is at most `B/eta`, and `A[z]`
   changes by `-4*B/h^2`. These are fixed positive
   masses, not mass accretion or a different body at each sample.
2. **Roofline-axis ambiguity.** A rigid transform `Rx(theta(t)) + p(t)*ez`
   leaves local roof markers `(xj,0,0)` unchanged while a local COM `(0,0,L)`
   follows `z=p+L*cos(theta)`. Middle angle zero and equal endpoint angle
   theta produce `A[z]-A[p]=-2*L*(1-cos(theta))/h^2`. A smooth witness is
   `theta(t)=theta_endpoint*(t/h)^2`; no abrupt rotation is required for
   this kinematic example. All rigid distances are preserved. An off-axis
   marker distinguishes the histories.
3. **Exact affine residual.** For a relative-position triple `r`, let
   `d=r_- - 2*r_0 + r_+`. Any affine subtraction with residual magnitude at
   most B requires `|d|<=4B`. Residuals `(d/4,-d/4,d/4)` attain equality and
   leave a zero-curvature affine trend. Thus `B*=|d|/4` exactly. This is a
   three-sample minimax residual, not a peak-to-peak displacement or an
   all-times bound. The declared smooth quadratic/cosine witnesses also
   provide an all-times bound within their particular synthetic constructions.
4. **Full-body envelopes.** If every particle of the fixed material set has
   offset from p within `[Lj,Uj]` at sample j, positive fixed mass weighting
   puts its COM in that interval. Consequently `A[z]-A[p]` lies between
   `(L_- - 2*U0 + L_+)/h^2` and `(U_- - 2*L0 + U_+)/h^2`. The condition is
   an entire-material-set envelope, not the outline of what happens to be
   visible. Temporal and structural dependencies can tighten this box bound.
5. **Sufficient mass/geometry constraints.** Bounds `BV` on non-affine
   point/visible-COM separation and `BH` on hidden/visible-COM separation,
   with fixed `eta<=eta_max`, yield `B<=BV+eta_max*BH`. This upper bound
   can be compared with the previous force test's necessary lower `B_min`.
   Unknown hidden motion does not license unlimited historically admissible
   deformation; a verified bound H on departure from s0 would constrain the
   specific first construction to `B<=eta*H`. An actual clearance constraint
   must also account for the baseline position/motion and body geometry.
6. **Rigid positive control.** For known pose `Rj`, local marker a and local
   COM c, `A[p]-A[z]=ez^T*(R_- - 2*R0 + R_+)*(a-c)/h^2`.
   Known constant 3D orientation makes this correction zero without knowing
   total mass or exact c. If `|a-c|<=L`, its magnitude is at most
   `L*||(R_- - 2*R0 + R_+)^T*ez||/h^2`; a known convex COM region can
   tighten it by optimizing that linear functional. Three noncollinear,
   known-geometry, same-body **3D** markers fix a proper rigid pose. Projected
   2D markers are not automatically those 3D observations, and a fit of a few
   markers is not proof that the entire facade remains rigid.

## Mechanical and historical limits

These examples establish a many-to-one observation map for a specified
reduced observation set. They do **not** supply connection forces, energy,
contact/collision feasibility, materials, loading, access, or any actual
building's motion. A complete image sequence could rule out a construction
that identical selected roof points cannot. The actual four published roof
labels have not been established here as collinear material points; the
roofline example must not be presented as a proved ambiguity of every
available WTC7 pixel.

For a fixed material set, Newton's law and cancellation of its internal
forces apply even when its components remain attached to outside structure.
Attachment forces cross the boundary and are external. Choosing the facade
changes that boundary: forces from the interior become external to it, not
unexplained terms that can be silently discarded. An open geometric volume
collecting new material additionally requires momentum-flux accounting.
Neither the net-force ratio nor its sign identifies all individual column
forces or the cause of their change. Unknown initial mass distribution and
dynamic membership cannot be cured merely by finding a static mass total.

## Computation and cross-comparison

Actual commands, each exit 0, from the investigation worktree:

```text
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/body-com-identifiability/oracle.py --out research/sherlock-wtc7-investigation/body-com-identifiability/oracle01/run01
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/body-com-identifiability/oracle.py --out research/sherlock-wtc7-investigation/body-com-identifiability/oracle01/run02
diff -rq research/sherlock-wtc7-investigation/body-com-identifiability/oracle01/run01 research/sherlock-wtc7-investigation/body-com-identifiability/oracle01/run02
```

Each oracle run completed 8 hidden-component cases, 8 rigid cases and 2
envelopes, with 648 exact assertions and 29 expected `ValueError` rejections:
24 collinear pose attempts and 5 invalid half-span/envelope inputs. Both
JSON products were byte-identical between runs. The exact pose routine is
purpose-built for rational-basis fixtures; it is not a general noisy camera
pose estimator. No UI/browser test applies to this command-line calculation.

After both implementations were frozen, a read-only inline Python comparison
completed **450 exact equality checks**, exit 0. It mapped every declared case
by `(eta,h,B)`, `(h,L,cos,sin)` or envelope name, not by coincidental list order.
Comparison covered:

- All hidden visible/hidden/combined trajectories, times, COM curvatures,
  normalized net-force fractions, hidden excursions and B* witnesses.
- All rigid rotations, world marker coordinates, recovered poses, COM
  trajectories/curvatures, normalized fractions and B* witnesses.
- Both envelopes' offset/force intervals and quarter-weight predicates.
- Independent enumeration of all 128 two-mass corner mixtures used by root
  (64 per envelope). The frozen oracle itself recorded 16 complementary-pair
  mixtures, plus all 16 single-COM corner triples; these are different check
  scopes, not identical grid coverage.
- All six root affine controls. The frozen oracle instead used three
  representative controls and the 16 case-specific witnesses.

Result: no blocking arithmetic disagreement. Root's loose envelope gives
`A[z]-A[p]` in `[-4,4]` and normalized net force in `[-2/5,2/5]`; the tight
one gives `[-2/5,2/5]` and `[-1/25,1/25]`, respectively. Only the loose
synthetic bound fails to exclude a lower fraction of 1/4. Passing an interval
test is not a proof of structural feasibility. All values are arbitrary
synthetic units, not recovered historical tolerances.

Frozen SHA256 pins:

| Artifact | SHA256 |
|---|---|
| `PROTOCOL.md` | `56acfc527feb2ac817d64ba582d46edddec7b853411eaed00d7b3322434d9553` |
| `oracle.py` | `c39ef5492438accfae8ff99f3c1d5dee322cff92d9b92e08238dbdd4eae758b2` |
| `oracle01/run01/results.json` | `dd23348b694b5a4d2625a5c82fcdc7c525cdddc6d0a75af8f5b97f8354333934` |
| `oracle01/run01/receipt.json` | `1f6567b33cf40787de867459cce27c647bd35aea93f508ab43a39c7e2107b099` |
| Root `run01/results.json` compared | `1e210ed55cfbaa265fc621b1977ec54b6b04b3db217a8f6ce6669f74103de7f2` |

The receipts additionally pin Python executable/version and the prior force
report, with before/after integrity checks. Repetition verifies deterministic
calculation only. No historical B bound, mechanism ordering, independent
engineering validation, legal finding or complete investigation is established.

## Final assembled-text review

The reviewer read the complete root report and source-review, requested two
wording corrections, then read the complete revised report again. Verified
report SHA256:
`b36ca1f664b97a4b6a0127d2b67a24e3c26d9896df86dfb31938a0292ad017f1`.
The source-review read for consistency has SHA256:
`7b6d827bda977119e95d011c3c36cd1ac7a8c06bcc1e8914478b42fb16a67860`.

The final report correctly distinguishes:

- A fixed attached material subset from an open spatial control volume;
  geometric COM bounds from a mandatory detailed mass model or numerical
  tonnage estimate.
- Three-sample B* from peak-to-peak motion and an instantaneous force bound;
  measured 3D rigid pose from assumed rigidity or merely stable projected
  marker geometry.
- Camera3 feature observations from Camera2's published sample triples; the
  source review's joins are attributed rather than treated as newly inspected
  primary evidence by this mathematical reviewer.
- Kinematic counterexamples to reduced observations from demonstrations of
  mechanical or historical feasibility. It neither rejects all available
  full-image information nor asserts actual large hidden deformation.

The earlier phrase “not mechanically feasible WTC7 histories” was replaced by
“not demonstrations of mechanically feasible WTC7 histories,” avoiding an
unsupported infeasibility conclusion. The loose envelope now “does not exclude”
the force fraction instead of suggesting physical permission. Root also added
the common-affine-translation observation: a sufficiently large downward
velocity makes the visible toy trajectory monotone without changing curvature
or relative geometry. That correction removes an irrelevant reversal issue;
it does not prove structural feasibility. The source reviewer's clarification
that `B/eta` bounds departure from s0, not absolute separation, is reflected in
this review as well.

Disposition: no unresolved blocking mathematical or assembled-wording issue
within this review scope. No primary-source verification, historical COM bound,
causal ranking or full-goal completion is claimed. The named historical
body/geometry/time joins remain open scientific dependencies.
