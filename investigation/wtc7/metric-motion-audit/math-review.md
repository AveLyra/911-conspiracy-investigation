# Independent mathematical review: pixels, clocks and acceleration

Research-only mathematical review, September 12, 2026, under the
[charter](../CHARTER.md) and [protocol](PROTOCOL.md), protocol SHA-256
`2ef59293a4e7994929964878ace70cef3569b4b689008e7ef85c66dc1e00e800`.
The evidence-audit, source-of-truth and development-verification skills guide
this review. All examples are synthetic; this reviewer has not inspected
historical point data or new source payloads for this mathematical pass.
Original source material and prior target-study artifacts remain unchanged.

## Variables and the actual identifiable quantity

Let `t` be physical time, `z(t)` a physical path coordinate in metres, `u`
an image coordinate in pixels, and `s=S(t)` the recording/presentation time.
Assume a twice-differentiable, fixed projection `u=F(z)`, a locally monotone
clock with `S′>0`, and `F′≠0` where inversion is intended. Denote physical
velocity by `v=dz/dt` and acceleration by `a=d²z/dt²`. Image y increasing
downward does not authenticate the world direction; orientation is part of
the geometric calibration.

The chain rule gives

```text
du/ds     = F′ v / S′
d²u/ds²   = (F″ v² + F′ a)/(S′)² − F′ v S″/(S′)³

a = (S′)² u_ss/F′ − F″(S′)² u_s²/(F′)³ + S″ u_s/F′.
```

Here `F′` has units pixels/metre and `F″` pixels/metre². If both clocks use
seconds, `S′` is a dimensionless rate ratio and `S″` has units 1/second.
Every term in `u_ss` has units pixels/recorded-second²; every term in the
inverse equation has units metres/physical-second². Signs are retained.

The recorded curvature is therefore a combination of physical acceleration,
projection curvature acting on squared velocity, and clock curvature acting
on velocity. Unknown functions are not evidence of historical distortion.
Conversely, source pixel positions and encoded PTS alone do not determine
those physical transformations. Independently justified bounds can support
conditional estimates; perfect forensic knowledge is not a prerequisite to
every useful estimate.

## Affine scale and affine clock

For `F(z)=αz+β`, with `α` in pixels/metre, and `s=kt+c`, with `k>0`,

```text
u_ss = α a/k²
a = k² u_ss/α = ℓ k² u_ss, where ℓ=1/α is metres/pixel.

a_hat/a = (α/α_hat)(k_hat/k)² = (ℓ_hat/ℓ)(k_hat/k)².
```

Thus a length-per-pixel scale error enters linearly and a clock-rate error
quadratically, with the stated direction. Stretching recorded time (`k>1`)
reduces the apparent image acceleration by `1/k²`. Treating that stretched
clock as physical time underestimates physical acceleration, if scale is
otherwise correct. A declared frame rate and an actual exposure rate are
different variables; one must specify which was changed before describing
the error's sign. If `s=n/r` and `t=n/f`, then `k=f/r`.

A constant spatial offset `β` or time offset `c` does not change exact
derivatives. This is **not** a blanket claim that reselecting an onset leaves
a fitted result unchanged: moving an event window can select different
samples, and imposing zero initial velocity or other onset constraints can
change a fitted acceleration. Offset, interval selection and clock-rate
assumptions must not be conflated.

## Fixed projective mapping

For a scalar projective map along a fixed straight spatial line,

```text
F(z) = (Az+B)/(Cz+D), Δ=AD−BC, Cz+D ≠ 0
F′ = Δ/(Cz+D)²
F″ = −2CΔ/(Cz+D)³.
```

The coordinate must actually parameterize that physical line for this model
to apply. Fixed-camera pinhole projection does not turn an evolving
silhouette or arbitrary three-dimensional deformation into a material-point
track. Lens distortion and moving-camera effects also are not included in
this fixed scalar model.

A published distant-camera description is a positive geometric constraint,
not something nullified by missing survey precision. Under the additional
assumption that the camera's actual optical axis points through the baseline
target, let `R` be their slant range and `h` the signed vertical component of
the camera-to-target baseline vector. A physical vertical displacement `L`
then changes optical depth by `Lh/R`, and its fractional depth change is
`q=Lh/R²`, up to the declared vertical sign. Therefore `|q|≤|L|/R`, with a
tighter bound when `h` is independently bounded. Without that axis assumption,
the general expression is `q=L d_z/Z0`, where `d_z` is the vertical component
of the optical-axis unit vector and `Z0` the baseline optical depth. Slant
range alone does not equal `Z0` for an off-axis target. One cannot simply
rename the axis through the target without accounting for image reprojection.
This review validates these conditional formulas, not a numerical historical
pose/range/displacement bound or a transfer between differently placed cameras.

With an affine clock, the measured curvature is

```text
u_ss = F′/k² [a − 2C v²/(Cz+D)].
```

Consequently constant physical velocity can produce nonzero image
acceleration, and constant physical acceleration need not produce a quadratic
image curve. For the particular synthetic map `F(z)=αz/(1+cz)`, constant
acceleration from rest at `z=0`, and `k=1`, `v²=2az` gives

```text
u_ss/(αa) = (1−3q)/(1+q)³, q=cz.
```

This last expression uses the **baseline** scale `α`, not the varying local
slope `F′`, and it requires the stated from-rest trajectory. Arbitrary initial
velocity or position requires the general formula. The finite illustrative
grid `q∈{-0.05,-0.02,0,0.02,0.05}` is a sensitivity demonstration, not an
empirical bound on WTC 7 camera geometry or depth change.

If projection varies explicitly with time, the numerator of the first term
instead becomes `F_z a+F_zz v²+2F_zt v+F_tt`; the clock-curvature term uses
`F_z v+F_t`. A translation-only reference correction cannot silently remove
all these terms or establish transfer across unknown depths.

## Circular gravity calibration is not a test of gravity

An image curve `u(s)=10s²` has curvature 20 pixels/recorded-second². With
`α=4 pixels/metre` and `k=1`, it comes from physical acceleration 5 m/s².
Choosing `α_hat=20/g` using assumed `g=9.81 m/s²` necessarily returns
`a_hat=20/α_hat=g`. This would falsely “confirm” gravity even in the explicitly
constructed 5 m/s² example. It is a calibration identity, not independent
validation.

The same image curve also admits `α=4`, `k=2`, `a=20`, illustrating a distinct
clock-scale ambiguity. These are synthetic alternative parameterizations,
not allegations about actual footage. Independent geometric/clock records
could exclude those parameterizations. One may use known gravity for a
separate calibration experiment, but not use the very acceleration under
test to calibrate itself and then count the result as corroboration.

Even an independently calibrated image acceleration compatible with `g`
does not by itself identify the moving mass, centre of mass, net non-gravity
force, support-removal mechanism or intent. Those are additional physical
and evidentiary questions, not algebraic consequences of a roof feature.

## Initial disposition and next check

The formulas above were sent to the producer before its synthetic results
were reviewed. The independent implementation will use exact rational
second-order Taylor algebra and local clock inversion, not import the
producer as an oracle. Finite controls include known affine rates/scales,
constant offsets, nonlinear projective witnesses, monotone nonlinear clocks,
and the gravity-circularity counterexample. Producer-result verification and
an exact code/result receipt will be additive.

The material historical discriminator is independently justified scale,
projection and original-exposure timing for the **same source, feature,
direction and interval**, accompanied by a defensible correspondence and
fitting model. A useful next source check can bound these rather than assume
they are exact or unknowable. This mathematical review does not itself
perform that source check or rank collapse mechanisms.

## Completed synthetic verification

[independent-oracle01.json](independent-oracle01.json), SHA-256
`2f467062f3b13fab9209abee3c4806a8e0cd76f834dfcd408309d6ab6ccb798e`,
passed with observed exit 0 before this reviewer opened the producer's
results. It pins the initial independent implementation
`3441e972a866bc0ec2e94243dce32842893d139daa600acf8dc37648c9df82de`.
Nine finite check groups cover five affine clock rates, three length-scale
factors, explicit offset polynomial expansions at the same physical event,
five nonlinear projective cases, two constant-velocity projective witnesses,
two monotone nonlinear-clock witnesses with inverse recovery, combined
nonlinear terms with reversed image orientation, circular calibration and
same-image alternative parameterizations, and four invalid-domain rejections.
Those groups have multiple cases; they are not nine historical tests.

The producer [calculate.py](calculate.py), SHA-256
`bc59b8a9e6510a0e8a493636dff96907a500c047536c235e7840fb72bb09e3d0`,
and all [inputs.json](inputs.json), SHA-256
`6885b06d38a6ed1b3b55d6188df49c1c91caaa3460fb08b80740ec76dc8fb8f1`,
were then read fully before its output. No blocking mathematical defect was
found. Its six controls include a known positive physical acceleration with
negative projective image curvature, nonlinear clock recovery, and
noninvertible-coordinate/nonincreasing-clock rejections. Its declared
nonlinear clock is `s=t+eta*t²` with `eta=±0.1`, giving rates 0.8 or 1.2 at
t=1. This is distinct from the independent constant-velocity witness's
`s=t+epsilon*t²/2`, `epsilon=±0.1`. Neither supplies historical clock bounds.

[independent-runs01.json](independent-runs01.json), SHA-256
`13977b534d058c81aaa45a71b9e509aa3136b78e255026be301306b4386b0787`,
passes with this reviewer's observed exit 0. It pins the completed
[verify_metric.py](verify_metric.py), SHA-256
`5be3a9c620fe01d362b212e24c58ac91624f00fbd2fa6a8964ae4540702aa8d2`.
It reruns all nine independent check groups, reconstructs all **26** producer
examples (15 affine, five projective, two nonlinear-clock, two offsets and
two circular-calibration rows), and compares every rational/decimal result.
The producer implementation is not imported; there is no historical calculation
in this package. Projection uses exact rational Taylor-series reciprocal
algebra and local clock inversion. Acceleration recovery independently
inverts the projective Taylor series and changes back from recorded time,
rather than calling the producer's derivative or recovery functions.

Both producer runs have exactly **six listed products, seven files including
the receipt**, all corresponding bytes identical. Their common receipt is
`d2839376f40177f8c09875e328f9f66dced562cf5d7135a7d5a7c86c86e22c41`.
The verifier checks current code/input/protocol/runtime identities, preserved
snapshots, initial and final pin sets, all product bytes, complete six-control
receipts and unchanged dependencies after review. Root reported that the two
producer executions printed completion sequentially within one shell command
group whose combined exit was zero; separately captured per-execution exit
statuses are not claimed. The independent review's own exit status was
captured directly. No failed calculation occurred in this review.

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/metric-motion-audit/verify_metric.py --runs run01 run02 --out research/sherlock-wtc7-investigation/metric-motion-audit/independent-runs01.json
```

The bounded numerical illustration is now independently checked. In
particular, the projective q-grid's roughly +34.1% to −26.6% baseline-scale
effects must **not** be recast as historically plausible Camera 2 error bars.
Camera distance, pose, displacement and point identity constrain which
projective parameters are physically available. The producer's circular
example uses an illustrative target of 10 m/s², not an asserted measurement of
local gravity; its known actual accelerations 6 and 12 both return that target
by construction. This review's separate 9.81 example makes the same logical
point with another chosen number.

Passing algebra cannot decide whether the present source/calibration records
support the historical claim. That substantive admissibility decision remains
with the separately source-grounded report, retaining legitimate conditional
inference and each consequential unresolved dependency. Root reread/rerun and
final report review are additional checks, not implied by this receipt.
