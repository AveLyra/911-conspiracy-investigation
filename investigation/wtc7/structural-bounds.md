> **Historical research:** This record presents idealized mechanics and computational checks, not a building-specific reconstruction or causal determination. Filesystem output paths are omitted where indicated. See [provenance](structural-bounds-PROVENANCE.json).

# Elementary structural bounds: what physics does and does not settle

2026-09-08 · WP3 first-pass constraints · Research only · No causal ranking change

## Result in plain terms

There is no universal answer to “how much weight breaks through eight floors.”
The missing quantity is not simply a floor's static load rating: it is its
force-versus-deformation behavior, the moving mass and velocity, impact geometry,
and what remains connected. This calculation supplies conditional constraints,
not the missing WTC 7 measurements.

In the idealized model, a floor can stop a falling mass despite a substantial
impact, or fail to stop it despite an upward resisting force exceeding the
mass's weight. Both outcomes occur in the retained grids. An abrupt stop in one
segment cannot be skipped by adding up favorable energy over later segments.
Losing bracing can greatly reduce an ideal column's buckling load without first
adding weight to that column. Neither fact demonstrates that the proposed
building-specific failure sequence happened.

## Status and authority

The [charter](CHARTER.md) controls scope. [Protocol v1](structural-bounds/PROTOCOL.md)
was written before this module's first run. This is a declared, finite illustrative
grid, not an inverse reconstruction, finite-element model, experiment, or expert
opinion. It uses no WTC 7 floor masses, member capacities, temperatures, calibrated
video measurements, or assigned cause labels. Numerical output is an exploratory
derivative, not canonical case evidence.

[Code](structural-bounds/bounds.py), [15 unit tests](structural-bounds/test_bounds.py),
and [run manifest](structural-bounds/run-v1/manifest.json) are available. Two runs
produced byte-identical six-table outputs and manifests under Python 3.12.14.
No failed numerical run occurred in this first pass. Same-author reproduction
and tests verify these equations' implementation; they do not validate a real
floor, column, or collapse. Independent main-agent mathematical review and any
later competent engineering review must be recorded separately. The [main-agent mathematical review](structural-bounds/main-review.md) has now passed fifteen tests, reproduced all six tables/manifest, and independently matched 42 idealized cases using a velocity recurrence. Its [receipt](structural-bounds/main-review.json) is a computational check, not a physical validation.

## 1. Falling mass versus floor resistance

Take downward translation z as positive. During this part of the calculation,
the translating mass M is fixed. Let R(z) be the **total upward force on that mass**
from the modeled load path, not a static floor rating. Let T0 be its translational
kinetic energy on first contact. The work-energy balance is

```
T(z) = T0 + M g z - integral[0..z] R(s) ds.
```

The `M g z` term must not be omitted: gravity continues doing work while the
receiving structure deforms. If the mass fell from rest through a clear distance
h before contact, with no other work, `T0 = M g h`. With initial downward speed
v0 before that drop, `T0 = 0.5 M v0² + M g h`. These are consequences of the
work-energy theorem with both gravity and contact forces included.
[Mechanics basis: OpenStax §7.3](https://openstax.org/books/university-physics-volume-1/pages/7-3-work-energy-theorem).

The one-coordinate model presumes that lateral motion, rotation, debris ejection,
internal deformation kinetic energy, and other work are absent or separately
accounted for. In a deforming real floor assembly, the point-mass translational
formula cannot silently stand in for the full energy balance.

For a constant upward resistance R maintained through a maximum downward stroke
δ, starting with positive T0:

```
stop distance = T0 / (R - M g), provided R > M g.
stop by δ requires R δ >= T0 + M g δ.
for the rest-start clear drop: R/(M g) >= 1 + h/δ.
```

This is a **conditional required average force in the constant-plateau model**,
not a measured WTC 7 capacity or a universal impact amplification factor. A
brief peak force does not determine the work done. At `R = M g`, an already
moving mass does not decelerate in this model. Resistance below weight permits
continued acceleration. Resistance above weight decelerates the mass, but may
act over too little stroke to stop it.

The retained [single-target table](structural-bounds/run-v1/single-target.csv)
gives the following purely hypothetical thresholds:

| Crush stroke δ / prior clear drop h | Constant R / moving weight needed to stop by δ |
|---:|---:|
| 0.05 | 21 |
| 0.10 | 11 |
| 0.50 | 3 |

These numbers are **not floor safety factors**. A force plateau would have to be
provided by the surviving structure over the specified motion. Static strength,
ductility, punching/shear behavior, connection fracture, load distribution and
support settlement are separate inputs. Stored elastic energy can cause rebound;
subsequent loss of support can restart motion. The code reports a **first stop
under the specified sustained/holding resistance**, not permanent building arrest.

### Why the whole resistance path matters

Let the normalized starting kinetic energy and weight both be 1. Suppose
resistance is 25 through the first 0.1 units of travel, then zero through the next
1.9. The unchecked endpoint arithmetic is `1 + 2 - 25*0.1 = 0.5`, apparently
positive. But the mass stops at `1/(25-1) = 0.0416667`, before leaving the first
segment. It cannot obtain the gravitational energy of a later segment without
first reaching it. `transit()` stops at the first zero of kinetic energy. A
unit test protects this counterexample. This is why summing total available
energy alone does not establish an actual progressive path.

## 2. Two collision modes and an eight-target sensitivity check

An impact is not automatically a lossless transfer of `M g h` into breaking the
next floor. For a short one-dimensional collision, initially moving mass M at
speed v, initially stationary target mass μ, and negligible external impulse,
write momentum conservation and define restitution `e = (v_target - v_M)/v`:

```
v_M      = (M - e μ)/(M + μ) * v
v_target = (1 + e) M/(M + μ) * v
loss of kinetic energy = 0.5 * [M μ/(M + μ)] * (1 - e²) * v².
```

For `e=0`, they move together: `v_after=M v/(M+μ)` and the surviving translational
energy fraction is `M/(M+μ)`. For equal masses, speed halves and half the initial
kinetic energy is converted into non-translational forms. For `e=1` and equal
masses, the initially moving mass stops and the target takes its speed; total
kinetic energy is unchanged. The [collision table](structural-bounds/run-v1/collisions.csv)
retains restitution 0, 0.5, 1 and target/moving mass ratios 0.25, 1, 4, including
rebound where applicable. This is standard closed-system collision mechanics,
not an observation of floor collision behavior.
[Mechanics basis: OpenStax §9.4](https://openstax.org/books/university-physics-volume-1/pages/9-4-types-of-collisions).

**Critical limitation:** a still-attached floor can receive a significant impulse
from its supports. The two masses then are not an impulse-isolated system.
Using the free-body collision formula to represent such a floor without checking
support impulse would be unjustified. Momentum is not conserved for an arbitrarily
selected subsystem merely because an impact is fast.

The eight-target illustration compares two distinct idealizations:

- **Fixed moving mass:** a mass crosses a resistance stroke without picking up
  target mass. All modeled losses in that stage are the specified resistance work.
- **Perfectly inelastic pickup:** each initially stationary target mass first
  joins the moving mass in an impulse-isolated collision; a separately specified
  upward structural resistance then acts during the stroke. This assumes target
  pickup/impact loss and subsequent resistance work describe **distinct** processes.
  Counting the same deformation loss in both would double-count dissipation.

Here `m0 = g = h = 1` defines consistent normalized units. Each target has mass
m0 in the pickup mode. There is a clear gap h before each contact and a separate
resistance stroke δ afterward, so the illustrative target-to-target travel is
`h + δ`, **not a claimed story height**. Resistance is specified relative to
the *initial* weight `m0 g`, while gravity work uses the current moving mass.

The [36-case summary](structural-bounds/run-v1/eight-target-summary.csv) and
[full visited-target history](structural-bounds/run-v1/eight-target-detail.csv)
retain all results. At the hypothetical `δ/h=0.1`:

| R / initial weight | Fixed moving mass | Inelastic pickup |
|---:|---|---|
| 0 | Traverses all eight targets | Traverses all eight targets |
| 5 | Traverses all eight targets | Traverses all eight targets |
| 10 | Traverses all eight targets | Stops in first target |
| 20 | Stops in first target | Stops in first target |
| 50 | Stops in first target | Stops in first target |

For the R=10 example, the fixed-mass model has `T=1 + 0.1 - 1 = 0.1` left after
its first target. Pickup initially loses half the unit energy; the mass becomes
2, so it stops after `0.5/(10-2)=0.0625` travel, before the 0.1 stroke ends.
Conversely, in continuing pickup runs, subsequently increased mass also produces
more gravity work. Pickup does not have one universal effect independent of the
rest of the model. Total gravity work equals remaining kinetic energy plus
collision losses plus resistance work, within floating-point rounding.

These are neither rigorous upper/lower bounds on a real structure nor a claim
that one actual floor could defeat eight other actual floors. The generated
grid's stopping cases all stop at the first target because its repeated toy
properties omit floor-to-floor variation. An intermediate stop, strengthening
lower floor, partial floor failure, mass loss, impact eccentricity, changing
connections, or bridging action requires different specified inputs and geometry.

**What this answers:** static load multipliers alone cannot decide the eight-floor
question. **What it does not answer:** how a localized fire would release a whole
floor, whether the released mass hit the required lower-floor area, which supports
survived, or whether a real cascade terminated at a particular level. Those are
unmet building-specific premises, not outputs of this calculation.

## 3. Loss of bracing and ideal Euler buckling

For an ideal straight, slender, linearly elastic, concentrically loaded column,
the pinned-end equation `E I y'' + P y = 0` with zero lateral displacement at
both ends admits a nonzero lowest-mode deflection when `P = π² E I / L²`.
Writing boundary-restraint effects through an effective length `Le=K L` gives

```
Pcr = π² E I / (K L)²
Pcr / Pcr0 = (E/E0) (I/I0) / [(K L)/(K0 L0)]².
```

E is elastic modulus, I the area second moment about the relevant bending axis,
L unbraced length, and K an effective-length factor determined by restraint,
not a parameter that may be chosen to force failure. MIT's mechanics notes
explicitly emphasize `EI/L²` scaling and boundary-condition dependence.
[MIT, David M. Parks, lecture 2, physical pages 11–13](https://ocw.mit.edu/courses/2-002-mechanics-and-materials-ii-spring-2004/bc25a56b5a91ad29ca5c7419616686f7_lec2.pdf).

At unchanged E, I and K, doubling the effective unbraced length reduces this
ideal critical load to 1/4; fourfold length to 1/16; eightfold to 1/64. The
[ratio table](structural-bounds/run-v1/euler-ratios.csv) also shows illustrative
E/E0 values of 0.7 and 0.4. For example, a modulus ratio of 0.7 and a doubled
effective length give `0.7/4=0.175` of the original ideal critical load.

**Why no extra weight is required:** at fixed axial load P and area A, the nominal
axial stress P/A has not increased merely because a brace disappears. Instead,
the instability threshold can decrease below the existing load. Deflection then
introduces bending and second-order effects. “More stress because no bracing”
is therefore an incomplete description; the loss of stability can come first.

**Why this is not a calculation for column 79:** actual restraint continuity,
frame sway, end rotations, partial floor bracing, local buckling, nonuniform
heating, plasticity, residual stress, initial crookedness, load eccentricity and
transient dynamics can materially alter behavior. No actual K, E(T), I, P or
unsupported length is assigned here. Temperature is not inferred from the
illustrative modulus ratios. The Euler result is not a strength check for a
short/yielding column or a model for a heated multistory frame.

The survival or loss of a single column also does not by itself determine global
collapse. Load sharing, connection capacities and alternative paths decide how
its loss affects other members. An unmodeled statement that “the building is
coupled” cannot supply those quantities, the failure order, or the time available.

## 4. Gravity travel scales and hidden versus visible motion

With an explicitly assumed downward initial speed v0 and gravity-only translation
through distance d,

```
d = v0 t + 0.5 g t²
t = 2d / [sqrt(v0² + 2 g d) + v0].
```

The rationalized expression avoids numerical cancellation. The
[time table](structural-bounds/run-v1/gravity-times.csv) uses a chosen illustrative
`g=9.80665 m/s²`, not measured site gravity. A rest-start 4 m travel takes about
0.903 s; with an initial downward speed of 5 m/s it takes about 0.527 s. A 30 m
rest-start travel takes about 2.474 s. None of these distances or velocities is
asserted to describe an observed WTC 7 component.
[Mechanics basis: OpenStax §3.5](https://openstax.org/books/university-physics-volume-1/pages/3-5-free-fall).

Eight separate 4 m rest-start drops sum to about 7.226 s; one uninterrupted
32 m rest-start drop takes about 2.555 s. The first repeatedly resets the speed
to zero, while the second never dissipates energy. These are intentionally
different idealizations, not interchangeable estimates for eight real floor
failures. Resistance, pickup, initial motion and deformation alter the result.
Gravity-only rest-start time is not an unconditional fastest-propagation bound:
an initially moving component or another force changes it, and stress transfer
is not the same process as a mass traversing the full gap.

An interior sequence could precede conspicuous exterior motion **only if the
surviving exterior load paths, connection deformations and geometry permitted
that delay**. Conversely, sufficiently stiff surviving connections could pull
or distort the exterior earlier. Neither possibility follows merely from saying
“interior first” or “coupling.” A hidden sequence has a finite available window:
the measured exterior onset minus the independently established interior onset,
with both timing uncertainties. Sequential steps on a causal path must fit
inside that window; parallel failures do not necessarily add their times.
This module provides no observed onset pair or building-specific propagation
duration, and therefore establishes no such fit.

## Claim/assumption audit and next discriminating inputs

| ID and narrow claim | Layer / present strength | Assumption or strongest alternative | What would defeat application to WTC 7 / next test |
|---|---|---|---|
| SB01: gravity continues adding work during downward floor deformation | Derived, A within the stated translating-mass model; event application D | Other degrees of freedom/work terms may be material | Obtain force-displacement/contact histories, mass and initial velocity; audit full energy balance and first stop |
| SB02: static floor ratings alone do not determine traversal count | Inference from model non-uniqueness, B | A complete dynamic model could constrain the count | Recover actual dynamic capacity/ductility, connected area, impact distribution and mass-loss histories |
| SB03: inelastic pickup dissipates translational energy while adding moving weight | Derived, A for impulse-isolated pickup; event application D | Attached-floor support impulse and fragmentation invalidate simple pickup | Obtain contact duration, support impulse and debris/mass trajectories; compare to no-pickup and partial-pickup models |
| SB04: effective-length growth lowers ideal Euler critical load quadratically | Derived, A under Euler assumptions; event application D | Partial restraint, yielding, sway and nonuniform heating change stability | Verify actual bracing-loss map and restraint stiffness; compare elastic eigenvalue illustration against nonlinear imperfections/material analysis |
| SB05: generic rapid gravity travel does not prove a causal propagation schedule | Derived times A; event sequence D | Initial velocity, resistance and parallelism change time | Independently time multiple visible onsets, specify dependency graph, then test whether member/connection dynamics fit it |
| SB06: one-column failure does not logically imply total failure | Mechanism inference, B; no event outcome assigned | Alternative load paths may arrest or may overload | Recover connection/load-path capacities and run both collapse and non-collapse scenarios with reaction and energy histories |

Grades describe only the specified claim, not the truth of any collapse theory.
No deliberate-intervention mechanism is excluded or established by these toy
results. Showing that a fire account needs these missing inputs is not proof
that the inputs were contrived. Showing an ideal mechanism can run is not proof
that fire supplied the required initiating conditions.

## Reproduction and source-access record

From the repository root, using Python 3.12.14 (standard library only):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/sherlock-wtc7-investigation/structural-bounds -p test_bounds.py -v
PYTHONDONTWRITEBYTECODE=1 python3 research/sherlock-wtc7-investigation/structural-bounds/bounds.py --out [local temporary output path omitted]
```

Choose a fresh exact output directory. Existing output directories are rejected.
The persisted generator manifest includes protocol/code/test SHA-256 values and
all CSV hashes. Six result files plus manifest in `run-v1/` and `reproduce-v1/`
were compared using `diff -r`, exit 0 with no differences. Validation covers
15 named tests: gravity work, exact stop endpoint, early barrier, rest/holding,
segment subdivision, dimensional rescaling, equal-mass inelastic/elastic cases,
collision conservation/restitution, chain conservation, both chain outcomes,
Euler scaling/dimensions, travel time/invariants, invalid inputs, and deterministic
generation/output collision guard. It is not a generic certification of software
or a structural solver.

Primary-source checks on 2026-09-08 were public teaching references only:

- OpenStax §7.3: full search-rendered section; work-energy relation and gravity
  work. An initial mistakenly constructed §7.2 URL returned a nonretryable
  safety/access error; it was not bypassed. A fresh search located the correct
  §7.3 source.
- OpenStax §9.4 and §3.5: direct rendered HTML retrieved; closed-system collision
  assumptions and gravity-only kinematics.
- MIT 2.002, February 9, 2004 lecture: direct PDF text extraction retrieved,
  physical pages 11–13 used only for the stated general scaling/boundary-condition
  proposition. Web screenshot calls returned references without a model-visible
  image; no claim of visual equation/layout verification is made. The equations
  above are explicitly derived here, not transcribed from invisible graphics.

These live web references were not downloaded into the legal source spine and
have no acquired-byte hash in this module. They support elementary mechanics,
not historical claims. No source text or image was altered, and no procedural
fact, exhibit, pleading, correspondence or external publication was changed.
