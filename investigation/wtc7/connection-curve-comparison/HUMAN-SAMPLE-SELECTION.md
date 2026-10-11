# Prospective selection of human curve samples

Version 1, October 5, 2026. Research-only preparation, declared before historical
tracing or discrepancy results. This fills the sample-selection gap in
[NUMERICAL-PROTOCOL](NUMERICAL-PROTOCOL.md); it does not replace its arithmetic,
support rules, uncertainty requirements or [human gate](HUMAN-REVIEW-GATE.md).

## Purpose and boundaries

The existing six-anchor/legend packet remains the next human action. It does
not accept curve samples. Historical linewidth/color characterization, visible
support declarations and eligible tracing remain separate prerequisites.
Nothing here clears them, supplies coordinates or authorizes a historical
metric now. The existing registration/uncertainty code and frozen records are
unchanged. No new viewer, source acquisition, image view or tracing is needed
to declare this rule.

The eventual sample is a deterministic coverage check, not a random sample,
confidence interval, whole-curve accuracy certificate or new engineering
acceptance threshold. Three positions are a prospective practical choice to
cover early/middle/late supported displacement, not a calibrated sample size.

## Selection rule before looking at discrepancies

1. Keep all seven bolt counts 3–9 in both force and energy panels. For each
   panel/bolt pair retain both spring and shell identities and each curve's
   full supported/unsupported inventory under the existing rules.
2. Designate the primary tracing/registration version before historical
   extraction, not after comparing fits. After the prerequisite human
   axes/legend check and source-native uncertainty/support work, freeze that
   inventory and its code/source hashes before any spring-versus-shell
   discrepancy calculation. Independent sample recovery remains required;
   disagreement must not be resolved by choosing the more favorable trace.
3. Use the numerical protocol's union D of common supported displacement
   intervals for that pair. Require valid identities and a validated list of
   finite, ordered, disjoint, positive-length intervals within 0–1.6 m.
   Invalid inputs are errors, not empty support. Do not fill dash gaps,
   crossings, clipping or hidden spans to obtain a useful sample.
4. Let L be the sum of the interval lengths. Select displacement at cumulative
   supported-length fractions 1/4, 1/2 and 3/4. Traverse intervals in increasing
   displacement. For qL, choose the first interval whose cumulative ending
   length is at least qL, then add the remaining length to its left endpoint.
   Use existing exact arithmetic where available; preserve the unrounded
   target and never select by graph discrepancy, peak or visual convenience.
5. An exact cumulative-boundary tie selects the preceding interval's right
   endpoint. Record that boundary explicitly. Do not jump across a gap or
   nudge to a clearer stroke. If its complete source-coordinate/uncertainty
   footprint cannot be admitted under existing support rules, mark it
   unresolved. The same rule applies at strip seams and identity conflicts.
6. If L=0, retain all three intended slots as unavailable, with each model's
   support and the reason. An absent or inadmissible series is unavailable,
   not a zero curve. If targets map to the same native cell/footprint, retain
   all slot IDs and flag the duplicate coverage; do not count them as
   independent checks or substitute other points.

This yields **42 paired slots**: 2 panels × 7 bolt counts × 3 fractions.
Each paired slot retains two model-specific coordinate/identity responses,
for 84 intended model entries, including unavailable or duplicate ones.
Order is force then energy, bolt count ascending, fraction ascending; within
each slot spring then shell. IDs use F/E, bolt count and Q1/Q2/Q3, for example
F3Q1-spring. D's coverage and omissions must remain visible; sampling only
supported spans does not validate missing spans or the declared support itself.

## Concrete response record and acceptance

For each paired slot preserve:

- Slot ID, panel, bolt count, quantile, unrounded selected displacement,
  cumulative interval, and boundary/duplicate flags.
- Source PDF/page/image hashes, primary trace/support inventory hash and
  registration/uncertainty version. Preserve every intersected native strip
  and its transform; a rendered-page pixel is not a native graph pixel.
- For each model: declared identity/style, proposed source/native-coordinate
  region and uncertainty, composed-page locator, support/ambiguity status,
  and selection failure reason where applicable. A hidden stroke stays unknown.
- Attributable human response: which entries were actually inspected,
  agreement/correction/unreadable/unresolved, the observed cue or identity
  concern, and any corrected location/range with its coordinate convention.
  Leave uninspected entries uninspected; a displayed marker is not acceptance.
- Independently recovered sample mapping and disagreement disposition,
  retaining the original proposal and human response separately.

Present the complete source page plus locators. Group the two model entries
at each paired position to reduce navigation, without merging their identities
or uncertainty. Do not show a preferred-cause label or discrepancy score as
a reason to accept a point. This is prior-informed inspection, not blinding.
One human response may explicitly cover multiple coincident slots, but every
slot retains its own status. Unavailable entries are not requests to invent
a coordinate.

The selected supported entries need actual inspection and an interpretable
mapping response before they can support consequential comparison. A failed,
ambiguous or uninspected entry is not passed by majority vote or by the other
model's successful entry. Apply the existing per-claim uncertainty/missing-
support rules; do not infer whole-pair validity from a passed subset. Conversely,
an unavailable slot does not turn independently established support elsewhere
into zero or prove a model wrong. Any later acceptance decision must explain
which proposed metric its validated support actually covers.

If inspection contradicts registration, identity or support, preserve the
failed packet and withhold affected metrics. Correct the source interpretation,
freeze a new full inventory, and regenerate **all** targets using this same rule
under a documented version change; do not replace only troublesome samples.
No favorable outcome authorizes erasing the earlier failed targets.

## Reproducibility examples and stopping point

These are invented interval examples, not historical graph measurements:

| D in metres | L | Q1, Q2, Q3 |
|---|---:|---|
| [0, 8/5] | 8/5 | 2/5, 4/5, 6/5 |
| [0, 1/5] union [4/5, 1] | 2/5 | 1/10, 1/5, 9/10 |
| [0, 1/10] union [2/5, 1/2] union [1, 6/5] | 2/5 | 1/10, 1/2, 11/10 |
| Empty | 0 | unavailable, unavailable, unavailable |

The second and third rows intentionally exercise gap-boundary ties. Their
selection does not decide whether a native uncertainty footprint is readable.
Small intervals can map several targets to one source cell; that is retained
resolution loss, not three independent confirmations.

Acceptance of this preparation means a separate reviewer can reproduce the
same selected targets from the same frozen support inventory without seeing
discrepancy results, and that all 42/84 intended slots are accounted for. The
filled historical packet remains **not created** until its dependencies exist.
No historical extraction, comparison, human acceptance, solver run, engine
admission, matrix save, transmission or legal promotion occurs in this unit.
Stop after this declaration, bounded method review and exact synthetic
selection checks; do not create another general curve framework.
