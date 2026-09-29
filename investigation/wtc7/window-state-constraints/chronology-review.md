# Independent interval and window-state chronology check

2026-09-24; frozen after 14:48:34 UTC. Reviewer `/root/curve_method`.
Research only: exact conditional arithmetic, not a new image observation,
camera-clock calibration, historical opening measurement or solver input.

## Scope and independence

Read this unit's PROTOCOL and rechecked the main CHARTER hash against the
complete charter read earlier in this turn sequence. Repository/source-of-truth
and evidence-falsification controls remain applicable. The only authored file
for this job is this review. No historical image, source page, native model,
root's contemporaneous calculation or other reader's new observations were
read. No source acquisition, solver, automated optical measurement or canonical
promotion occurred.

The supplied source-attributed inputs are:

- Exposure **A**, Figure 5-127: 15:12:50 ±5 minutes.
- Exposure **B**, Figure 5-126: somewhere in 15:11:15–15:16:51.
- The source additionally infers A before B from a claimed glass-present to
  open difference. That is an image-state-derived order, not an independent
  camera timestamp.
- The supplied source account allows an opening to coexist with some retained
  glass. This review checks the logical implication; it does not independently
  verify that either photographed target exhibits that state.

Intervals below treat the written endpoints literally as inclusive, continuous
time bounds on the same date/time convention. This is conditional modeling of
the report's assigned windows, not proof that the quoted uncertainties are
hard calibrated bounds, confidence intervals, independent errors or uniform
distributions. Further clock error or a source-specific joint timing constraint
could change them. Integer-second labels do not restrict possible exposure
times to an integer-second lattice.

## Results

| Quantity | Exact interval under the stated constraints |
|---|---|
| A's assigned window | `[15:07:50, 15:17:50]` |
| B's assigned window | `[15:11:15, 15:16:51]` |
| Unconditioned B−A | `[-395, 541]` seconds = `[-6 min 35 s, +9 min 1 s]` |
| B−A after imposing strict A<B | `(0, 541]` seconds |
| Union of possible transition times τ, given A<τ≤B | `(15:07:50, 15:16:51]` |

Square brackets include an endpoint; parentheses exclude it. No strictly
positive minimum separation is established. The infimum is zero, unattained
when A<B is strict. The maximum 541 seconds is attained by the earliest
admissible A and latest admissible B. The union of possible transition times
is not a best estimate, probability distribution, guaranteed duration, or a
transition observed throughout that entire interval.

The assigned windows overlap, so they do not independently establish A<B.
Without the source's additional order inference, B may be earlier, simultaneous
or later within these assigned windows. Conditioning on that inference removes
the nonpositive separations but does not turn the inferred order into new
clock evidence.

## Derivation and endpoint checks

Measure time in seconds after midnight. Then

```text
A ∈ [54,470, 55,070]
B ∈ [54,675, 55,011]
min(B−A) = 54,675 − 55,070 = −395
max(B−A) = 55,011 − 54,470 =  541
```

Both difference extrema are attainable under the literal interval constraints.
The continuous interval of differences is therefore closed before ordering.
Strict A<B intersects it with positive differences, giving `(0,541]`.
Arbitrarily close admissible A and B can be chosen within the overlapping
windows; there is no one-second or other minimum imposed by the printed labels.

For any admissible transition, `A<τ≤B` implies
`54,470<τ≤55,011`. Conversely, every τ in that interval is feasible under the
stated constraints: choose `A=54,470` and `B=max(54,675,τ)`.
Those exposures lie in their assigned windows and satisfy `A<τ≤B`.
Thus the union is exactly `(54,470,55,011]`, not merely a loose subset bound.
This construction does not claim those particular assignments occurred.

The lower endpoint is excluded because τ must be strictly later than A and no
A is earlier than 15:07:50. The upper endpoint is included because τ is allowed
to equal B and B may equal 15:16:51. If the physical observation only warranted
strict τ<B, an interval of exposure rather than an instantaneous sample, or
non-inclusive source limits, the endpoint convention would need revision;
none of those alternatives is silently substituted here.

## What “open” does not establish

Given the supplied source meaning, **apparently open and partial retained glass
are compatible states**. An opening need not imply full-pane loss. Conversely,
glass being present somewhere in an opening does not establish that it was
fully closed beforehand. The categories “glass present” and “open” are not
automatically mutually exclusive.

To interpret τ as a physical loss-of-glass event, additional premises are
needed: the same window and comparable viewed portion were identified;
the earlier state really lacked the later opening; the later feature is an
opening rather than darkness/reflection/occlusion; and the relevant change is
monotone within the observation interval. Misidentification, an already partial
opening, a changing view or re-glazing would invalidate that inference. Those
premises belong to the source/pixel review, not this arithmetic.

Accordingly, this calculation supplies no opening fraction, total pane-loss
finding, thermal exposure, ventilation rate, fire duration, temperature or
actual modeled removal schedule. Even a verified state change would constrain
a model only after matching its window geometry, state definition, clock and
native input representation. A report-inferred order is not an independently
verified input contradiction.

## Actual verification

Executed the following read-only arithmetic in this unit's directory; Python
3.14.0, exit 0, all assertions passed. It writes no files:

```sh
python3 -B -c 'import json; ac=15*3600+12*60+50; a=(ac-300,ac+300); b=(15*3600+11*60+15,15*3600+16*60+51); delta=(b[0]-a[1],b[1]-a[0]); assert a==(54470,55070); assert b==(54675,55011); assert delta==(-395,541); assert max(a[0],b[0])<min(a[1],b[1]); print(json.dumps({"input_kind":"literal_report_assigned_bounds_not_independent_clocks","A_seconds_after_midnight":a,"B_seconds_after_midnight":b,"unconditioned_B_minus_A_seconds_closed":delta,"conditional_A_before_B_delta":{"lower_seconds":0,"lower_included":False,"upper_seconds":delta[1],"upper_included":True},"conditional_transition_union_seconds_after_midnight":{"lower":a[0],"lower_included":False,"upper":b[1],"upper_included":True},"minimum_positive_separation_exists":False},sort_keys=True))'
```

The open/closed endpoint flags and absence of a minimum are mathematical
conclusions justified above, not results established by the printed boolean
flags themselves. No sampling program substitutes for the interval proof.
Other commands actually run: bounded `sed` of PROTOCOL; `shasum -a 256` of
PROTOCOL and the main CHARTER; scoped `git status`; `python3 --version`.

| Control document | SHA-256 at review |
|---|---|
| This unit PROTOCOL.md | `b503e6055fbc7ece3910e3af143959d2f76b98fd40a0ca09a92606f3980bbced` |
| Main CHARTER.md | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |

The strongest limitation is semantic and evidentiary, not arithmetic: source-
assigned windows and a claimed image-state change may not be independent or
sufficiently resolved. The bounds are exact only for the literal constraints
supplied. A primary clock calibration, a different joint timing relation, or a
well-supported contrary state/identity reading would change the permitted
historical inference without contradicting this conditional calculation.
