# Independent facade-feature arithmetic verification

2026-09-12. Research-only computational review. All declared material
numeric outputs reproduce within the prospective 1e−8 absolute tolerance.
Joint box calculations and original-box witness memberships agree exactly.
This is not image authentication, architectural identification, human
annotation, physical calibration or an engineering cause determination.

The main checkout's current AGENTS.md, WORKFLOW.md and START-HERE.md and the
complete new PROTOCOL.md were read. The evidence-falsification-auditor,
source-of-truth-guardian and development-verification skills informed the
separation of numerical reproduction from observation and inference. The
investigation charter remains controlling; no authority boundary changed.

## Independence and execution

The mathematical core of verify.py was implemented and its 22 independent
synthetic groups run successfully **before** reading analyze.py or any
facade-feature producer output. Its frozen prefix, through the marked
END_INDEPENDENT_MATH line, has SHA-256:

`6ac5ade0e3cfae57519099531e8fd966a8b9fb2aab2f1f465fdac485e46f37ff`.

Output-schema adapters were subsequently appended without changing this
prefix; the executed verifier checks that prefix hash. No producer code is
imported or executed. The earlier independent equal-grid derivation was
reused as a method, not a producer least-squares implementation. I read
frozen C annotation notes and files, not images or a new source decode.

Final [verify.py](verify.py) SHA-256:
`a8210c081bb490bccfa4b0280cf12215c1150ddfdddad0bfef49da57db2d4f64`.

First executed historical verification [receipt](verification01.json):
`c34b25e967756243118e444939a3500152d7e74c099e2f49578275230b141308`.

Executed from the isolated investigation worktree, Python 3.13.7:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-facade-feature/verify.py
```

The first full run exited 0 with no discrepancies. No failing result was
repaired or overwritten. The output filename must be new; root may reproduce
with `--output verification-root01.json`. Synthetic core tests run before
historical output checking. All four frozen annotation hashes, protocol and
existing image-receipt pin agree. Producer inputs/code/output hashes match
its receipt, and controlling annotations, producer outputs and code remain
unchanged after verification.

Producer code pin:
`03860226937d78233a64dd185aac30989271fe562b0772804603b61b4515c860`.
Results pin:
`9ccc92e7116249c2afd8c632a184fa7b6259989e8c2e0c2d3f0d2a3bc76842bf`.
Controls pin:
`e0fa756ecc96f717746841abc0612932054fbad0a750a747ccb1fcc883e6f56f`.

## Exact derivations

The linear and quadratic fits use exact Fraction arithmetic on the
conditional equal grid t=(frame−138)/15. With midpoint c, halfspan h and
z=(t−c)/h, odd power sums vanish. Set S2=Σz², S4=Σz⁴, Y=Σy:

- b1=Σzy/S2 for both fits.
- Linear b0=Y/n.
- Quadratic b2=(nΣz²y−S2Y)/(nS4−S2²) and b0=(Y−S2b2)/n.
- Acceleration is 2b2/h², with per-point weight
  2(nz_i²−S2)/(h²(nS4−S2²)).

Residual orthogonality, zero response to constant/linear motion, and exact
response 2 to t² are checked. Signed linear interval extrema select lower
or upper placement endpoints according to each weight's sign.
A−C bounds are [A_low−C_high,A_high−C_low]; direct fits agree exactly with
the acceleration difference from separate A/C fits. Missing C is never
converted into a zero or interpolated value.

Joint calculation starts from the **original** A/C boxes, joined by source
observer and frame, not from producer-summarized intersections. For each
axis, intersect observer boxes separately for A and C. A common separation
must lie in every [A_low−C_high,A_high−C_low] interval.

Uniformly widening each original box by δ changes a joined lower endpoint
to L−δ and upper to U+δ. Thus a local observer-intersection gap g requires
δ≥g/2. Every separation interval expands by 2δ at each endpoint, so a
global separation-intersection gap g requires δ≥g/4. The largest nonnegative
requirement across local conflicts and both coordinate axes is necessary
and sufficient for this Cartesian-box problem. It is not a measured error.

The verifier independently checks all per-frame joins, extrema and their
attaining frames, original feasibility and minimum δ. It then checks the
producer's actual witness coordinates exactly against **every original box**
with that δ, rather than requiring the producer to choose the verifier's
preferred in-box placement. The x and y witnesses must each have the one
stated constant separation. This validates a mathematical witness, not a
historical trajectory or physical dynamics.

## Coverage and results

| Item independently checked | Count |
|---|---:|
| Comparison frames | 22 |
| Localized / missing C observer comparisons | 40 / 4 |
| Declared fit dispositions | 92 |
| Computed / missing fit windows | 72 / 20 |
| Linear/quadratic coefficient scalars | 360 |
| Individual residual scalars | 1,520 |
| Acceleration weights | 760 |
| Placement-interval endpoints | 144 |
| Exact A−C fit-linearity checks | 36 |
| Historical joint scenarios / axes | 6 / 12 |
| Historical joined/witness rows | 117 |
| Historical original-axis-box memberships | 624 |
| Producer fit-control results | 4 |
| Producer joint-control fixtures | 4 |
| Joint-control witness rows / box memberships | 7 / 32 |
| Independent mathematical control groups | 22 |

Each of root/independent C and A−C has 18 computed and five missing windows.
The five missing windows per series comprise two 9-point windows, two
13-point windows and the sole 21-point window, all involving 345 or 348.
Their exact dispositions are retained; no full late C trajectory is inferred.

Maximum absolute discrepancies, across case and control arithmetic:
coefficients 1.252e−12, residuals 9.751e−13, SSE 1.991e−12,
acceleration 3.411e−12, acceleration bounds 3.287e−12 and weights 1.509e−14.
These displayed upper descriptions are rounded upward; the receipt retains
full values. Joint interval/extremum/delta comparisons have zero discrepancy;
witness memberships use exact rational inequalities, not the float tolerance.

All six original-box scenarios are feasible without widening:

| Observer / coverage | Included / selected | Constant x interval | Constant y interval | δ |
|---|---:|---|---|---:|
| Root / all | 20 / 22 | [92,97] | [−47,−44] | 0 |
| Root / late | 19 / 21 | [92,97] | [−48,−44] | 0 |
| Separate / all | 20 / 22 | [92,96] | [−47,−43] | 0 |
| Separate / late | 19 / 21 | [92,97] | [−48,−43] | 0 |
| Combined / all | 20 / 22 | [92,95] | [−47,−44] | 0 |
| Combined / late | 19 / 21 | [92,95] | [−48,−44] | 0 |

Every scenario omits 345 and348. Unlike the earlier B comparison, the
root/separate/combined scenarios share coverage within each all/late choice.
Combined witnesses use (x,y) separation (93.5,−45.5) for all and
(93.5,−46) for late. A constant vector can fit the supplied boxes on covered
samples; neither equality of central placements nor rigid physical motion
has been established.

The 22 self-test groups include 12 constant/linear/curved fits over
5/9/13/21 points, each with an actual position/time-origin transformation;
all32 vertices of an asymmetric interval case; missing, ambiguous,
nonfinite and duplicate-clock rejection; global-gap, local-gap, touching and
two-axis maximum-δ cases with actual shared per-frame coordinate shifts;
and explicit empty-coverage refusal. Positive δ cases are also checked for
infeasibility immediately below their exact threshold. No fictitious
infeasible historical scenario is reported.

## Narrow producer-control caveat

Only after the independent passing run, I inspected analyze.py lines27–38
and111–146. Its missing-data gate and the retained missing fixture agree
with the observed dispositions. Full source inputs for the four joint
fixtures and their expected δ values are retained and reproduced.

The producer group named translated_pair_difference is generated directly
as nine constant values of10. It verifies a constant-difference fit, not a
construction transforming two separate trajectories. It should not be
described as a second independently performed pair-translation experiment.
This is a control-label/scope limitation, not an arithmetic error in the
retained constant fixture. The independent frozen controls actually shift
both A/C coordinate boxes per frame and verify invariant joint intervals;
the two types of checks should remain distinguished.

## Interpretation ceiling

The numerical reproduction is grade A for the stated operations on pinned
inputs. Historical physical interpretations remain materially conditional.
For example, every one of the18 computed A−C acceleration envelopes per
observer contains zero; the joint test now supplies the stronger simultaneous
constant-vector alternative within original boxes. Neither result establishes
that the actual motion was rigid, the boxes are probability-calibrated, or
the witness is physically realizable.

C is a more explicitly defined contrast junction than fixed-column B, but
its architectural/material identification is not supplied by this verifier.
Perspective/camera rotation can change image separation for a rigid object;
apparent contrast boundaries can also change without tracking a fixed
load-bearing point. Two shared-image annotation passes are not two cameras.
Neither existence nor failure of a constant-vector image model alone would
identify fire, deliberate support removal, force, hidden support timing or
intent.

Only verify.py, verification01.json and this review were written by this
subtask, all in the isolated investigation worktree. Frozen inputs, prior
results, preserved media, main and canonical/legal records were untouched.
No transmission, accepted finding, Faraday call, commit or push occurred.
Final report-to-evidence review, when supplied, will be recorded below without
changing the frozen calculation or receipt.

## Final report-to-evidence review

I read the complete report at SHA-256
`d72505841cb0901ad6c5e6c3e4c61d736363e9e91c2b9de5ccc0a6de4ca14ec9`
and the complete source-geometry-review.md at
`e2af9e7d546e2f35b122bded6f69b467c810c79894b37b970bb0f06f02aa86d9`.
This follow-up checks the report against the already reproduced numeric
artifacts and the separately authored architectural review. It is not a
second direct PDF/image inspection or another numerical replication.

The root rerun, verification-root01.json, has SHA-256
`e5ab77395d09db9938d120a0a8eca1f9749f0384897abf55a993cfa90b7cf115`.
It equals verification01.json except for the command field, reflecting its
different output argument. The report correctly identifies that rerun, the
independent mathematical implementation, and their shared source inputs.

Checked report summaries agree:

- All20 readable C-box pairs overlap in both axes. Maximum central
  observer disagreement is2px horizontally and1px vertically.
- All/late denominators are20/22 and19/21, with345/348 omitted in every
  scenario. The combined all vector (93.5,−45.5) is the retained witness
  within original boxes; the late witness has y difference−46. No full
  late21 trajectory or gap interpolation is implied.
- The six scenario intervals and zero widening, 92/72/20 fit counts,
  18computed/5missing per series, 360coefficients,1,520residuals,760weights,
  144interval endpoints,117witness rows and624box memberships match the
  reproduced outputs. Counts reuse observations rather than multiplying
  source independence.
- The303–339 table and line/quadratic RMSE values match the saved fits at
  the stated display rounding. The report keeps those numbers in native
  conditional units and warns that displayed interval limits are not
  outward-rounded bounds.
- C's central acceleration ranges are16.0173160173–39.5562770563 for root
  and17.6948051948–38.6363636364 for the separate observer. The reported
  positive exclusion of zero in18/18 root and16/18 separate C envelopes,
  versus zero inclusion in all18 A−C envelopes per observer, is correct.
- The maximum verification discrepancy including controls is3.411e−12.
  The report preserves the limited meaning of the producer's
  constant-difference fixture label and does not invent a performed
  pair-translation construction.

The geometric review supports the architectural-region attribution in the
report: apparent lower-west corner of the north-face Floors46/47 louver
bank, not a verified trim/steel node or a newly surveyed metric point.
The report distinguishes this source-informed identification from original
drawings, exact elevation/depth/attachment and NIST's different east-edge
parapet reference. This reviewer checks fidelity to that separate source
review, not independently authenticating its underlying published report.

The report makes the important causal limits explicit: a constant image
vector is compatible with the supplied boxes, not proof of exact physical
rigidity, equal physical acceleration, whole-building symmetry/free fall
or either initiating mechanism. It gives no probability to the witness and
does not require constant projected separation of a physically rigid body.
This is a properly bounded mathematical compatibility result. The new
region identification strengthens the basis for investigating C without
turning it into an independently identified material point.

One wording correction was requested in the reviewed version:

> The definition and all sampling and calculation choices were declared
> before the new coordinates.

The phrase “all ... calculation choices” is broader than what is explicitly
specified in the protocol, which does not predeclare every numerical
control fixture or display choice. Suggested replacement:

> The feature definition, selected images, window families, and
> constant-separation/widening tests were declared before the new coordinates.

This preserves the supported prospective commitments without claiming an
exhaustively prespecified numerical workflow or historical holdout.
No numerical correction or causal-interpretation correction was required.
The next subsection, if added, records the disposition of this wording
request against the exact final report hash. No producer output or frozen
annotation was edited during report review.

### Final wording disposition

The requested clarification is applied in final report.md, SHA-256
`3327432747dba2b3f705406e31c28710b21da3f4d10064b6dcfe8db988957539`.
I inspected its actual line wrapping and verified that replacing exactly
that new sentence with the previously reviewed sentence recovers the prior
report hash
`d72505841cb0901ad6c5e6c3e4c61d736363e9e91c2b9de5ccc0a6de4ca14ec9`.
Thus the sentence and its wrapping are the only report changes: numerical
and source text are unchanged. An initial read-only replacement check used
a different assumed line wrap and found no match; after inspecting the
actual lines, the exact reverse-hash check passed. No file was changed by
either check.

The clarification resolves this review's sole requested correction. The
final report is cleared within the report-to-evidence review scope stated
above; unresolved image/material/physical calibration and causal limits
remain substantive limits, not certification failures that were waived.
Validation.md is now present as the parent's separate closeout record; its
creation does not alter this numerical or source-review scope. This
disposition edited only the review, not code, calculation receipts or the
final report.
