# Elementary structural constraints — protocol v1

Declared 2026-09-08 before executing this module. Research-only; not a building model.

The finite first pass contains only analytical mechanics and explicitly hypothetical
parameter sweeps. It ingests no WTC 7 masses, strengths, geometry, temperature
histories, media coordinates, or collapse labels. Prior familiarity with the event
is acknowledged; this is not a blinded historical-cause study.

1. A translating fixed mass crosses a piecewise-constant upward resistance law.
   Integrate gravity and resistance work until the first stop; never continue through
   a negative-kinetic-energy region. Compare a constant plateau and an early-barrier
   counterexample. A stop is not a guarantee of permanent arrest if support later
   degrades or stored elastic energy causes rebound.
2. Show a one-dimensional collision of a moving mass and an initially stationary,
   externally unrestrained mass for mass ratios 0.25, 1, 4 and restitution 0, 0.5, 1.
   Check momentum and total kinetic-energy loss. Attached floors do not generally
   satisfy the negligible-external-impulse assumption.
3. Hypothetical eight-target chain: initial mass m0, identical target mass m0,
   gap h before each encounter, target crush stroke delta/h in {0.05, 0.1, 0.5},
   upward plateau R/(m0 g) in {0, 2, 5, 10, 20, 50}. Compare fixed translating mass
   without target pickup against perfectly inelastic mass pickup followed by
   separately specified structural resistance. Both are limiting toy models,
   not upper/lower rigorous bounds on a real building. Stop at the first arrest.
   The eight targets respond to the user's eight-floor question; the number and
   toy parameters are not inferred from actual floor properties.
4. Ideal elastic Euler load ratio: E/E0 in {1, 0.7, 0.4}; I/I0 = 1;
   effective-length ratio (K L)/(K0 L0) in {1, 2, 4, 8}. No temperature mapping.
5. Gravity-only translation: hypothetical distances 0.1, 1, 4, 10, 30 m and
   starting downward speeds 0, 5 m/s with g = 9.80665 m/s², an explicitly chosen
   conventional illustration value, not a measured local value. Compare eight
   rest-start 4 m drops to one uninterrupted 32 m drop; neither is an event clock.

Validation: unit, dimensional-rescaling, endpoint/arrest, momentum/energy, invalid
input, monotonicity, and deterministic-output checks. Preserve failed runs and
superseded outputs if any. Write each result set to a fresh output directory;
record source/protocol/test hashes and interpreter version. No fitting or grid
tuning to obtain a chosen outcome. A different parameter set requires a versioned
protocol and result directory.

Acceptance ceiling: correctness of these stated idealizations, not fire causation,
actual floor failure counts, actual column 79 capacity, or propagation chronology.
Main-agent review is computational review, not licensed engineering review.
