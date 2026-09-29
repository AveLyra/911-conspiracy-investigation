# Independent pre-measurement method review

2026-09-24, frozen after 14:21:37 UTC. Reviewer `/root/curve_method`.
Research only. This is an AI mathematical/methodological review, not an actual
human spot-check, professional structural certification, primary-page reading,
historical curve measurement, solver reproduction or causal finding.

## Scope, independence and present disposition

Read the main CHARTER, current main and worktree instructions, the new unit
PROTOCOL and HUMAN-REVIEW-GATE, the prior `connection-calibration-audit/
nist-validation-review.md`, and the completion audit's `structural-review.md`.
The two prior reviews are derivative source leads, not new evidence. I have not
viewed the selected figures or read the root/source reader's forthcoming
readings, extracted historical ordinates or historical numerical results.
I own only this file; earlier studies, source files and legal records are
unchanged. Evidence-falsification, source-of-truth and repository-orchestration
skills were read and applied to prevent a calibration comparison from becoming
an unsupported physical-validation claim.

The all-seven-pair comparison is methodologically useful if it distinguishes:

1. recovery of published graphical information;
2. reproduction of a selected calibration target;
3. physical validity under relevant loads and temperatures; and
4. historical explanatory sufficiency.

Only the first two are candidates for this unit. Even those require source
identity, graph support, uncertainty and the actual human gate. A plot-level
result used to strengthen or weaken the calibration claim is consequential;
calling it provisional does not exempt it from the charter. The gate is
currently unmet. Source inventory, this method design and synthetic checks may
proceed; no historical automated discrepancy is accepted by this review.

Observable acceptance for the method is an explicit row for every 3–9-bolt
spring/shell pair in both panels, with either a source-supported comparison or
a named unresolved state, independently reproduced arithmetic, preserved
uncertainties/failures and no force-work/energy identity assumed without its
required definitions. An unreadable row satisfies transparent disposition,
not successful measurement of that pair.

## Freeze the source-to-series contract first

- Pin source bytes, complete-page renders, page boxes, axis labels/ticks,
  plot rectangles, units, legend entries, figure IDs and transformations.
  Source readers must confirm meanings; OCR alone does not register axes.
- Fix model identity from the actual legend and line style, and bolt count
  from the legend's color/style association. Do not infer identity from the
  expected capacity order or whichever assignment gives a closer match.
- Preserve every candidate graphic path or raster region, including legend,
  axes, text, grid and unresolved candidates. Give each selected component a
  direct source-object/region reference and its inclusion/exclusion reason.
- Determine whether the graph is vector, raster or mixed before choosing a
  recovery algorithm. A raster placed inside a vector PDF is still a raster.
  Source-vector coordinates are drawing instructions, not raw solver output,
  recovered solver sampling frequency, precision of a physical law, or proof
  of a historical run. They may already embody downsampling or smoothing.
- With vector paths, preserve path order, move/line/curve operations, stroke
  width, dash definition and phase, graphics-state transformations, clipping
  and drawing order. A dash style applied to one continuous path differs from
  independently drawn fragments. Curve flattening needs a fixed source-unit
  tolerance and a refinement check. A hidden path's existence is documentary
  information, not direct visible support for a guessed series identity.
- With rasters, freeze colors/antialiasing tolerances and axis registration
  before tracing. Use independent manual source-to-series checks. Do not
  treat every similar-colored pixel as data: legends, text and crossings can
  share colors. Multiple readers share the same representation limitation.
- Freeze separate statuses for `identified`, `overprinted`, `clipped`,
  `ambiguous identity`, `missing support` and `not work-comparable`. Record
  dependencies instead of deleting a hard-to-read bolt pair.

No fitted axis warp, model-specific horizontal shift, amplitude rescaling or
retiming may improve a match. Axis conversion from source tick locations is
calibration of the graph, not a free parameter fitted to the curves. Any
symmetry/normalization factor must come from the source, not curve agreement.

## Support, crossings and displacement reversal

For each identified model/bolt pair, retain its own source-supported domain.
For pointwise comparison, use the intersection of the two reliably identified,
unclipped, single-valued domains. Retain this as a union of intervals, not an
automatically filled interval from the earliest to the latest point. Report
coverage both against the nominal overlapping displacement range and against
the full displayed axis range. An aggregate over surviving intervals cannot
represent unobserved gaps or the whole response.

Do not bridge a crossing, obscuration, clipping boundary or missing component
by assumed curve order. Native continuous path instructions may explicitly
encode continuation through printed dashes; report that distinction. In a
raster-only dashed curve, interpolation across an intentional dash gap must
be preregistered, bounded by verified dash geometry and independently checked;
it cannot also license interpolating an occluded or ambiguous segment.

A force-versus-displacement curve need not be a single-valued function if
unloading/backtracking occurs. Never sort recovered points by displacement,
discard duplicate abscissae, or take an outer envelope and call the result
the original force history. First establish whether plotting-path order is
loading order; that identity is not automatic. If loading order is known,
ordered work for a polyline is

`W = sum[ (F[j] + F[j+1]) / 2 * (d[j+1] - d[j]) ]`.

The displacement increment is signed. A vertical segment contributes zero
to this line integral but remains meaningful as a multivalued force limit.
If loading order is unknown, a multibranch plot can support graphical branch
descriptions but not a recovered physical work history. Any branchwise
point-comparison must be semantically matched, not assigned by resemblance.

## Graphical uncertainty, not invented physical error bars

Keep four uncertainty classes distinct: axis registration, visible stroke/
pixel localization, identity/support, and unknown source-to-solver fidelity.
The first two can have graphical bounds. The latter two are not solved by
increasing render resolution or supplying extra decimal places.

For vector recovery, retain exact centerline drawing coordinates separately
from a presentation-resolution envelope. A defensible graphical envelope
includes half the transformed stroke width, source-coordinate quantization
and bounded registration error. For raster recovery, additionally include
pixel localization/antialiasing uncertainty measured in the actual source
raster, not fictitious subpixels from an enlarged rendering. A fixed nominal
one-source-pixel localization allowance can be a declared starting rule, not
a universal guarantee; controls and independent annotation must show whether
it contains errors. If they do not, fail/refine the method before historical
comparison and preserve the earlier failure.

Propagate horizontal uncertainty as well as vertical error, especially near
steep drops. One conservative construction at displacement `d` is to take
the range of curve ordinates reachable over `d ± e_d`, then expand vertically
by `e_F`. Do not silently replace that rectangle with an error only in force.
Near endpoints shrink the assured comparison domain; do not extrapolate.
Use interval or explicit parameter-set propagation for systematic axis error;
root-sum-square combination requires a justified statistical error model.
Line-width bands are graphical distinguishability bounds, not 95% confidence
intervals and not uncertainties in historical connection capacity.

Given force envelopes `S=[S_low,S_high]` for shell and
`R=[R_low,R_high]` for spring, the difference lies within

`[S_low - R_high, S_high - R_low]`.

The lower absolute difference is zero when this interval includes zero;
otherwise it is the smaller absolute endpoint. The upper absolute difference
is the larger absolute endpoint. Integrating these bounds gives conservative
graphical discrepancy bounds, potentially loose because shared registration
errors are correlated. A robust positive/negative difference requires exclusion
of zero after these allowances. That is a statement about these graphics,
not the historical building.

## Fixed comparisons that remain defined near zero

Use a nonzero plotted-axis scale `F_scale = F_axis_max - F_axis_min`, and
analogous `E_scale`, confirmed separately for each panel. They are fixed from
the source axes before measuring discrepancies. Retain physical units as well
as normalized results; state what the denominator is. Reference-force division
at every point, MAPE and arbitrary epsilon denominators are disallowed.

For common valid single-valued domain `D`, length `L > 0`, and
`DeltaF(d) = F_shell(d) - F_spring(d)`, report:

- signed local differences and their sign-changing intervals;
- signed mean difference `integral_D DeltaF / L` and its division by `F_scale`;
- mean absolute difference `integral_D abs(DeltaF) / L`, normalized likewise;
- maximum absolute difference on `D`, with location/uncertainty;
- optional RMS difference `sqrt(integral_D DeltaF^2 / L)`, normalized likewise;
- each curve's force-area and their difference on exactly the same `D`, with
  the explicit label **partial-domain force–displacement area** if gaps remain.

Calculate absolute difference after splitting at all valid line intersections;
the absolute value of the signed integral is not an absolute-discrepancy metric.
For piecewise linear input, exact segment integration is preferable to a grid
that can miss a narrow spike or zero crossing. Repeated raster/path points are
not independent observations. Do not report a statistical p-value from them.

Apply corresponding pointwise/mean/maximum difference metrics to the plotted
energy panel, on its own supported common displacement domain. An integral of
energy against displacement has units energy-times-length; it is not itself
an absorbed energy. Do not combine the force and energy panels into one score
or average seven bolt pairs into an apparent independent sample of buildings.
All seven rows, including stronger and weaker shell responses, remain visible.

`D` empty or `L=0` means no interval comparison. A small surviving domain is
reported as small, not a whole-curve pass. There is no source-supported good/
bad engineering tolerance identified by the prior reviews; graphical
distinguishability and effect size must not be relabeled engineering failure.

## Peak, terminal and zero-resistance conventions

Report observed maximum force separately on each own supported domain and on
the common domain. Retain all near-maximum locations/plateaus permitted by the
graphical band. A maximum clipped by the graph boundary is only a lower bound
on the unknown source maximum. A greatest visible point is not automatically
the true global peak; an unobserved interval may contain more.

Use the last shared supported displacement for a common-endpoint comparison,
and separately list each plotted domain endpoint and terminal ordinate. Label
the former a common-domain endpoint, not ultimate failure displacement. A curve
stopping, merging into an axis, entering an overlap or leaving the plot is not
proof of zero force. A reported zero tail needs its own series/support evidence.
Do not convert displacement differences to elapsed failure times. No velocity
history is supplied by a displacement abscissa alone.

## Force area and dissipated energy: conditional, not an identity

The prior review describes Figure 3-4 as applied vertical load in MN versus
vertical displacement in m, and Figure 3-5 as dissipated energy in N-m. Root's
independent primary-page reading must verify these labels and meanings.
The unit conversion would be `1 MN*m = 10^6 N-m`; conversion does not establish
that the two plotted quantities should be equal.

Mechanical work is the integral of a force along its work-conjugate
displacement (relative deformation for an internal spring), or the sum of
such products over relevant degrees of freedom.
The pictured vertical quantity supports a work interpretation only after
identifying its point/component, sign, imposed motion and system boundary.
A schematic mechanical balance for a stated system is

`W_vertical + W_other = DeltaK + DeltaU_recoverable + D + R`,

where `R` explicitly collects separately defined other energy/storage/transfer
terms not yet accounted for. It is an unresolved bookkeeping quantity, not a
free correction fitted to erase disagreement. Model-specific numerical energy,
contact, damping, thermal work, gravity, symmetry factors and deleted-element
accounting may need separate treatment. Their existence or magnitude must be
established from the actual source/output definitions, not assumed here.

The identity `D(d) = integral F_vertical dd + constant` requires the same system,
normalization, loading path, displacement coordinate and energy baseline, with
the non-dissipative/other terms appropriately zero or already removed. It is
not guaranteed by a caption saying dissipated energy, monotonic displacement,
similar terminal values, or a quasi-static intention. With zero initial stored
energy and no other input, and nonnegative remaining storage/kinetic/other loss
terms, one can conditionally bound `D <= W_vertical`; preloading, energy release,
other input or different accounting can invalidate even that inequality.

A simple counterexample is a unit linear elastic spring loaded from `d=0` to
`d=1`: `F=d`, work `1/2`, recoverable energy `1/2`, dissipation `0`. The nonzero
work–dissipation gap is correct physics. A purely dissipative constant force
`F=2` over the same monotonic coordinate gives work and dissipation `2d` under
its deliberately restricted assumptions. Neither toy case identifies how NIST
defined its plotted quantity.

Accordingly:

- Compare spring against shell within the force panel and independently within
  the energy panel even if cross-panel accounting is unresolved.
- Integrate supported force paths only with the stated path/work qualification.
- Compute a cross-panel residual only as an explicitly conditional diagnostic
  with source-verified coordinate, unit and normalization correspondence.
  If dissipated-energy semantics remain unknown, retain that dependency instead
  of declaring a conservation violation or a successful energy validation.
- Do not differentiate a raster energy trace to reconstruct a force law; that
  adds numerical noise while making the same unproved identity assumption.

Equal force-area totals need not imply equal local force: on `[0,1]`, spring
`F=1` and shell `F=2d` each have area `1`, while the signed difference integrates
to `0`, absolute difference integrates to `1/2`, and mean squared difference is
`1/3`. Thus a local-shape mismatch can be real while a scalar total matches.
Its global structural importance is still an untested downstream question.

## Required synthetic controls and independent oracle

Before accepting automated historical output, the harness should include:

| Control | Required behavior |
|---|---|
| Identical polylines with different point sampling | Zero difference; same area without grid/sampling bias. |
| `F_spring=1`, `F_shell=2d`, `[0,1]` | Signed area 0; absolute area 1/2; mean squared difference 1/3. |
| Zero reference and nonzero constant comparator | Finite absolute/full-scale metrics; no division by the reference. |
| Narrow triangular spike, exact crossing, duplicate vertices | Recover known area/extremum; split difference at crossings. |
| Ordered elastic out-and-back `(0,0),(1,1),(0,0)` | Ordered work 0; never sort by displacement to get 1/2. |
| Vertical segment `(0,0),(1,1),(1,0),(2,0)` | Work 1/2; vertical drop retained, not averaged into a ramp. |
| Disjoint valid intervals, missing tail, hidden peak | Missing sections not interpolated; coverage and peak limit retained. |
| Known stroke width, antialiasing, axis error, steep drop | Declared interval envelopes contain known drawing coordinates. |
| Legend colors shared with non-data objects; crossings/overprints | Correct identity or explicit refusal, not convenient reassignment. |
| Native dash, fragmented dash, clipping, transformed/cubic paths | Distinguish actual path support; transformation/refinement bounds hold. |
| Force in MN, displacement in m, energy in N-m | Exact factor 10^6, without fitted normalization. |
| Elastic work/dissipation counterexample | Do not flag physically valid stored energy as an energy error. |
| Unknown baseline, symmetry factor or energy definition | Cross-panel claim refused/conditional; no hidden offset/factor fit. |
| Mutated source/mapping/code, stale output or missing pair | Fail with preserved receipt; no stale or incomplete all-seven success. |

The arithmetic oracle should be implemented separately, without importing the
producer's parser, interpolation, integration, support or identity functions.
Use hand-specified rational polylines and analytical antiderivatives for
synthetic truth, then independent recovery of selected source mappings for the
historical stage after the human gate. Merely rerunning identical code checks
determinism, not independence. At least one independent render/overlay check
must verify source-to-curve assignment; a second arithmetic engine reading a
misidentified trace would otherwise reproduce the same wrong quantity.

An oracle's exact rational answer validates arithmetic on its specified toy
inputs. It neither resolves graphical uncertainty nor experimentally validates
the connection model. No completed implementation/control coverage is claimed
by this list.

## Narrow claims, falsifiers and verification

| Claim | Type / support | Strength and strongest limitation |
|---|---|---|
| Signed-area agreement can conceal local mismatch | Mathematical derivation; exact constant-versus-ramp counterexample | A for the constructed functions, not a measured historical result. |
| Vertical force-area need not equal dissipated energy | Mechanical bookkeeping plus elastic counterexample | A as a counterexample to universal equality; the actual plotted energy definition remains unverified here. |
| All-seven graphical comparison could refine the calibration critique | Proposed method | C until identity, uncertainty, controls and actual human checks succeed; inseparable curves could limit it. |
| Published fit proves the building-specific fire-collapse chain | Historical/physical inference | Unsupported by this proposed graph test; relevant validation, actual histories and global sensitivity are missing. |

Commands actually run: repository intake; complete bounded instruction/review
reads via `sed`; scoped `rg --files`; SHA-256 checks; `cmp` of main/worktree
AGENTS (different, as expected from the older worktree); and a read-only Python
`fractions.Fraction` check of the sign-cancellation, elastic, ordered-reversal,
vertical-segment and unit-conversion toy values above. All toy assertions
passed. This is not the proposed full synthetic test suite. One combined read
truncated; affected WORKFLOW, START-HERE and CHARTER were reread completely.
No PDF/figure was inspected and no historical number was extracted by this
reviewer. Main instructions control where the older checkout differs.

| Read input | SHA-256 |
|---|---|
| Main CHARTER.md | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| This unit PROTOCOL.md | `1ec6fedc9110f9ef2001f69fd1e13ad3a316a904f057345af26a0118d3216e19` |
| HUMAN-REVIEW-GATE.md | `2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee` |
| Prior nist-validation-review.md | `7391cceb80134aff4981208d4e433d6c77a54b6acb3ecf5548d1a1d12f98a92a` |
| Completion structural-review.md | `a4c7233c340da8b24ce563221ec1fda9cdf4f1e6ed0e80031297b208c418717a` |

Next executable steps are source registration/identity and synthetic known-truth
verification, followed by the actual human spot-check gate. If primary-source
energy semantics cannot be resolved in the admitted pages, record the exact
definition dependency before widening the source scope. The unavailable native
arrays are a separate fidelity limitation, not permission to label the printed
graphics raw solver results. Any post-measurement revision to this review must
be a dated addendum preserving this pre-measurement record.
