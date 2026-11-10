> **Historical research:** This is an arithmetic check of NIST’s printed fit, not a measurement of actual motion or an independently replicated regression. The NIST PDF is not included here. The unmodified Python script expects the pinned source at `authority/nist/wtc7/ncstar-1-9.pdf` under the repository root; a source hash match is required. See [provenance](printed-fit-PROVENANCE.json).

# What NIST's printed smooth curve does and does not establish

2026-09-08. Research-only derived arithmetic, not new historical measurement. [Protocol](printed-fit-protocol.md), [Python calculation](check_printed_fit.py), [numerical output](printed-fit-result.json), [separate JavaScript chain-rule check](check_printed_fit.mjs), and [independent arithmetic receipt](printed-fit-independent.json).

## Result

The smooth function printed in NCSTAR 1-9 Figure 12-76 necessarily starts with zero acceleration for its published exponent. Its calculated acceleration then varies substantially, including through the interval labeled Stage 2. Its downward velocity peaks near 4.897 s and decreases afterward. These are properties of the selected curve family and fitted constants; they are **not independently observed evidence** of a gradual physical onset or late upward net force.

This does not contradict the mere fact that NIST reported a separate approximately gravitational regression slope. Figure 12-77 and its accompanying text distinguish numerical velocities computed from displacement differences from the derivative of the smooth curve. NIST's reported 32.196 ft/s² slope belongs to a straight-line fit of selected numerical velocity points. Recomputing that regression requires the underlying displacement/time pairs and selection details, which this audit has not recovered. See [the source-method audit](../nist-camera-method-audit.md).

The useful criticism is precise: a close position fit and a visually smooth velocity curve do not, by themselves, validate acceleration history or distinguish instantaneous from gradual onset. Conversely, showing that the smooth curve has varying acceleration does not refute the separately calculated gravity-compatible interval. Both claims must be tested against the raw measurements, with timing, scale, point identity and correlated errors accounted for.

## Calculation

Main visually inspected all of NCSTAR 1-9 physical pp. 666-669 (printed pp. 600-603), including the equations, footnotes and graph legends, in the preserved source [NIST PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf). With A=379.62 ft, b=0.18562 s^-1 and k=3.5126:

`z(t) = A [1-exp(-(bt)^k)]`

`v(t) = A k b (bt)^(k-1) exp(-(bt)^k)`

`a(t) = A k b² (bt)^(k-2) exp(-(bt)^k) [(k-1)-k(bt)^k]`

The finite zero-time limits are z=v=a=0 because k>2. The general family does not have zero initial acceleration for every possible exponent; this statement uses the published k. The derivative coefficient A k b is 247.5155852 ft/s, consistent with the separately printed 247.52 after rounding. No parameters were refitted.

Selected values from the complete, predeclared eleven-time grid:

| Time after NIST's roofline-zero (s) | Smooth-fit displacement (ft) | Smooth-fit velocity (ft/s) | Smooth-fit acceleration / report's g=32.2 ft/s² |
|---|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1.75 | 7.242 | 14.396 | 0.625 |
| 2.5 | 24.750 | 33.615 | 0.950 |
| 3.0 | 45.580 | 50.028 | 1.069 |
| 4.0 | 112.473 | 82.430 | 0.818 |
| 5.0 | 203.752 | 95.065 | -0.112 |
| 5.4 | 241.116 | 90.840 | -0.538 |

These are sampled values, not an optimization-derived acceleration range. A negative value here means the **smooth curve's** downward speed is decreasing. It is not a claim that the actual building decelerated at that value. The velocity maximum follows analytically at t=[(k-1)/k]^(1/k)/b=4.89724 s, v=95.2501 ft/s. The late numerical points in the source graph do not track the smooth decline; exact residual magnitudes and significance require the original data, not visual estimates.

The fit's stage distances are approximately 7.242 ft, 105.231 ft and 128.643 ft over 0-1.75, 1.75-4.0 and 4.0-5.4 s. Their broad agreement with the report's approximate 7/105/130-ft descriptions is retained as a cross-check, not hidden because this is a critical audit. The source's separate stage-3 switch in landmark wording remains unresolved. The straight regression line is also evaluated in the raw output outside its fitted interval solely to keep arithmetic explicit; its negative early velocity or continued late increase must not be interpreted as a published prediction there.

## Verification and claim ceiling

Python analytical derivatives agreed with symmetric finite differences at all ten positive sample times under the declared 1e-5 absolute/relative tolerances. A separate JavaScript implementation uses u=(bt)^k and the chain rule rather than the factored acceleration expression; all eleven z/v/a rows agree within 1e-10 absolute units. A fresh Python run reproduced the complete output byte-for-byte. Source SHA-256 is checked by the script. This verifies rounded-equation arithmetic, not least-squares parameter estimation, historic data quality, original software or structural causation.

**Next discriminator:** recover the raw displacement/time pairs and exact selected interval; reproduce the published midpoint-velocity regression, then compare preregistered abrupt-onset and gradual-onset position models with camera/geometry and correlated-error uncertainty. The current curve alone cannot choose between those physical histories. Neither NIST's structural mechanism nor deliberate intervention receives a new causal ranking from this check.
