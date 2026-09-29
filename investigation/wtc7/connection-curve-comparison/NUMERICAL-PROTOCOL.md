# Quantitative contract, before historical curve measurements

2026-09-24. Stage 1 mathematical contract, **not execution clearance**.
Root has seen the complete published plots and qualitative differences;
this is prospective for numerical extraction only, not a blind preregistration.
Read PROTOCOL.md and HUMAN-REVIEW-GATE.md. The two source readings are frozen.
All seven 3–9-bolt pairs in both panels remain the fixed scope. No selected
misfit alone can stand for the complete comparison.

## Confirmed source semantics and unresolved mapping

Figure3-4: x is vertical component displacement, 0–1.6m; y is applied vertical
load, 0–1.0MN. Figure3-5: x 0–1.6m; y dissipated energy, 0–800,000N-m.
Both: solid=spring model; dashed=shell model; 3black,4gold,5blue,6red,7green,
8cyan,9purple. Caption shear-model terminology is not a third trace.
The benchmark's displacement is not automatically individual bolt slip.
The source's grouping normalization and symmetry boundary do not authorize
an analyst-chosen multiplier, per-bolt division or fitted axis adjustment.

Representation inspection identifies raster strips, not native curve paths.
Before the historical stage, a separate source-registration record must pin
all raster objects/placements, plot/legend/axis regions, tick-coordinate
intervals, line/antialiasing tolerance, overlay masks, and every source-to-model
curve identity. Freeze it before tracing. Use native-source pixel uncertainty,
not the apparent extra pixels in a higher-resolution page render.

No historical ordinate extraction is authorized by this mathematical contract
alone. Source-mapping human spot-check, synthetic raster identity/uncertainty
controls and independent registration must be completed first. If a continuous
solid/dashed assignment cannot be established, keep a missing/ambiguous interval;
do not interpolate it merely to complete seven rows. The admissible dash-gap
rule must be stated and tested separately from occlusion/crossing gaps.

## Fixed arithmetic, independent of raster recovery

Input is a set of explicitly identified, supported, single-valued monotone-x
piecewise-linear branches for each model in one panel. Preserve disjoint valid
intervals rather than filling between the first and last point. Reject
nonfinite, boolean, inconsistent-identity, contradictory-overlap and zero-length
inputs. No sorting of backtracking paths into a monotone curve.

For a pair, D is the union of supported common intervals, length L. List each
model's own support and D; report L/1.6 and the supported fraction of nominal
overlap. L=0 yields no comparison, not agreement. A small observed fraction
cannot become a whole-curve result.

At exact source breakpoints and valid intersections, compute shell−spring:

1. Signed integral and signed mean over D.
2. Integral and mean of the absolute difference, splitting sign changes.
3. Integral and mean of squared difference (RMS optional and explicitly rounded).
4. Maximum absolute difference and all maximizing locations/intervals.
5. Each curve's supported peak and locations on own and common domains.
6. Each curve's integral over exactly D, with gap/partial-domain labeling.

Normalize force differences only by the fixed 1MN axis span, and energy
differences only by 800,000N-m. Retain absolute units. No division by a small
reference ordinate or epsilon denominator, fitted offset, scale or horizontal
shift. No combined seven-pair score, statistical p-value or invented engineering
good/bad cutoff. Graphical distinguishability is not engineering consequence.

Displacement uncertainty must enter with ordinate uncertainty: construct local
envelopes over the admissible x interval then expand y. Systematic axis error
stays correlated; interval extrema are allowed to be conservative rather than
pretending independent normal errors. For shell envelope[Slo,Shi] and spring
[Rlo,Rhi], difference is[Slo−Rhi,Shi−Rlo]. Report robust signs only when zero
is excluded throughout the stated interval. Unknown identity is not repaired
by increasing a numeric error bar. These graphical bounds do not estimate
uncertainty in actual historical connection capacity.

Terminal comparisons use the last commonly supported coordinate plus each
curve's separate endpoint. Merging into an axis, disappearing behind another
line or ending at a plot boundary is not a demonstrated physical zero or
complete failure. Preserve clipped/hidden maxima as limits. No conversion
from displacement to failure time without a source-supported time history.

## Work/energy definitions

For an explicitly ordered path, force-displacement line area is the sum of
trapezoids with signed displacement increments. Vertical segments contribute
zero work but remain as discontinuities. Backtracking is not sorted away.
Convert MN*m to N-m by exactly10^6, without treating unit conversion as a
proof of physical work conjugacy.

The plotted dissipated-energy panel is compared internally, spring versus
shell. An integral of that panel against displacement has units N-m² and is
only a shape metric, not a second absorbed-energy estimate. Do not assert
equality with integrated force. The selected source pages do not establish
reaction/energy sets, symmetry factor, baseline, storage/kinetic/numerical
terms or exact work-conjugate coordinate. Cross-panel equality/error claims
remain **not admitted** pending those definitions. No adjustable bookkeeping
term may be fitted to manufacture agreement.

## Verification and acceptance

Implement the narrow arithmetic on exact rational synthetic polylines first.
Controls must include identical curves with unequal sampling, cancelling signed
area with nonzero absolute error, zero reference, a narrow spike, repeated
vertices, disjoint support, missing tails, reversed displacement, a vertical
drop, unit conversion and rejection of an unspecified energy identity.
An independent implementation/oracle checks those results without importing
producer interpolation/integration. This validates arithmetic only.

Historical acceptance separately requires source/raster-identity controls,
actual human mapping checks, before/after source/code hashes, two deterministic
runs, independently recovered sample mappings and independent arithmetic over
all admitted pairs. Unresolved pairs remain explicit; no generic all-seven
pass is possible when one is missing. No replacement constitutive law, native
solver recovery, physical validation or cause conclusion follows from passing
this graph-level contract.

Current stage: mathematical method frozen; raster registration, graphical
uncertainty calibration, human spot-check and all historical metrics pending.
