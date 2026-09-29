# Matching expansion does not, by itself, establish matching restrained force

September 27, 2026. Completed synthetic method test; research only.

Two bars can expand by exactly the same amount under a specified tensile load
and nevertheless develop different axial forces when their ends are held at
the same length. The declared examples retain this difference even while
matching the entire loaded-expansion history. Conversely, matching expansion
**and axial compliance** does ensure matching restrained force in this linear
model. The negative and positive results are both independently checked.

This establishes a limit on a proposed inference, not an error in a specific
NIST calculation. No historical thermal field, steel calibration, coating
profile, connection, buckling response or collapse was reconstructed. No cause
ranking changes. The useful consequence is a sharper validation requirement:
equivalence in one response must not be silently promoted to equivalence in
another response or in structural failure.

## What was tested

The [frozen protocol](PROTOCOL.md) specifies a small-strain, one-dimensional
series bar with common reference geometry, constant cross-section and a common
stress-free reference temperature. Temperatures are prescribed independently
of force. There is no bending, instability, plasticity, creep, contact, damage
or failure criterion. Axial guiding is an idealization, not proof of stability.

Length changes are normalized by reference length L0; axial forces by A E0.
Positive values mean extension and tension. The dimensionless temperature
theta uses an arbitrary positive temperature scale, not an assigned steel
temperature. The deliberately synthetic material law is

    thermal strain = theta/1000
    E(theta)/E0 = 1/(1 + beta*theta^2), beta >= 0.

Each comparison uses three equal-length segments unless explicitly testing
refinement. The preload is p=1/1000; a second probing load is p2=1/500.
The two clamp experiments hold total normalized elongation at D=0 (cold
stress-free length) or D=p (cold preloaded length). The clamp replaces the end
traction; it does not independently prescribe both force and displacement.

Here, "unrestrained under a tensile load" means the ends can extend under that
load. It does **not** mean an unloaded bar. Total hot elongation and increments
from the cold length at either the probing load or the reference preload are
kept separately labeled in every output.

## The reason: two independent state quantities

With no distributed axial load, all segments carry one common axial force n.
Equilibrium, the constitutive law and length compatibility give

    H = sum(w_i * theta_i/1000)
    C = sum(w_i * (1 + beta*theta_i^2)) > 0
    d(n) = H + n*C
    n_D = (D - H)/C.

H is normalized free thermal elongation; C is normalized axial compliance
(physical compliance divided by L0/(A E0)). One loaded elongation constrains
one combination of these two quantities. A larger mechanical extension can
offset a smaller thermal extension, concealing a difference in restrained
response.

If two candidates satisfy d*=H_A+p*C_A=H_B+p*C_B, then exactly

    n_D,A - n_D,B = (D - d*) * (1/C_A - 1/C_B).

Thus equal reactions follow if and only if their compliance is equal or the
chosen clamp happens to hold the common hot extension D=d*. The latter special
boundary is not generally either cold clamp. Matching one loaded response
does not **always** yield different forces; it simply does not guarantee equal
forces. The identity also expresses materiality: a small compliance difference
or a clamp close to d* can make the force difference small. No historical size
or practical consequence has been measured here.

## Exact counterexample and positive controls

At beta=1, compare a uniform state [1,1,1] with a nonuniform state [0,0,2].
All quantities below are normalized, not measured dimensions or temperatures.

| Quantity | Uniform | Nonuniform |
|---|---:|---:|
| Free thermal elongation H | 1/1000 | 1/1500 |
| Axial compliance C | 2 | 7/3 |
| Total elongation at p | 3/1000 | 3/1000 |
| Elongation increment from cold preload | 1/500 | 1/500 |
| Total elongation at p2 | 1/200 | 2/375 |
| Force at stress-free clamp D=0 | -1/2000 | -1/3500 |
| Force at preloaded clamp D=p | 0 | 1/7000 |
| Force change from preload p | -1/1000 | -3/3500 |

The preloaded nonuniform bar still has a positive tensile force despite a
negative change from its original force. A reduction in tension must not be
called compression. All zero-load and second-load increments, including both
cold-reference conventions, remain in [root output](run01.json) and
[independent output](oracle-run01.json); no unfavorable case was discarded.

With constant modulus (beta=0), [1,1,1] and [0,0,3] instead have equal H=1/1000
and C=1. Their loaded elongations and both restrained reactions agree. Cold,
identical-profile, reordered-profile and segment-refinement controls also pass.
Reordering invariance concerns global response under these assumptions, not
identity of local strain fields or invariance of a real connection structure.

Two distinct loads at the **same load-independent thermal state** supply the
missing information:

    C = (d(n2) - d(n1))/(n2 - n1)
    H = d(n1) - n1*C, with n1 != n2.

Matching both responses therefore matches all prescribed-length reactions in
this model. Coincident loads cannot identify both quantities and are rejected.
This is not a two-test certification rule for nonlinear or damaged structures.

## Matching a whole history does not remove the ambiguity

The continuous comparison uses uniform temperature s in each segment and
nonuniform temperatures [0,0,q], with 0<=s<=1 and

    q = (-1 + sqrt(1 + 12*s^2 + 12*s))/2
    q^2 + q = 3*(s^2 + s).

Both loaded elongations equal p*(1+s+s^2) at every s. The path is continuous
and nondecreasing in temperature; two nonuniform segments remain cold. For
s>0, q<3s, so C_nonuniform-C_uniform=s-q/3>0. The common loaded elongation
exceeds p. The reaction identity therefore gives a smaller uniform-bar force
at both cold clamp lengths for every s>0; the cold states coincide.

This is an algebraic proof over the interval, supported by exact polynomial
checks and endpoint controls—not a conclusion from a few numerical samples.
It is a constructed path through constitutive states, **not a solved heat-flow
history**. The [independent derivation](independent-review.md) gives the full
monotonicity and sign proof, including the favorable transfer conditions.

## Application to the investigation

The preceding [primary-source follow-through](../contracting-access-custody-audit/restraint-followthrough-2026-09-27.md)
reports that the selected June 2004 progress pages show elongation comparisons
under tension and describe restrained-bar work as ongoing. The selected later
summary reports use of the equivalent thicknesses but does not supply the
exact restrained-bar comparison. That is a bounded source finding, not a
whole-literature absence finding. Separate restrained physical floor tests
were reported and cannot be erased by the narrower bar-output gap.

The present calculation explains why the response-metric distinction matters.
It does not demonstrate that the published pairs have different compliance,
that their approximation is practically inadequate, or that it changes a
WTC7 connection failure. The strongest objection is that the actual cases may
constrain compliance and temperature distributions, compare additional
responses, or lie in a regime of negligible force difference. The synthetic
counterexample cannot resolve those empirical questions.

The discriminating records/tests are the original and equivalent-profile
thermal histories, applicable material laws, initial and restrained boundary
conditions, and paired reaction/stress histories with a declared tolerance.
For this linear-bar question, H and C or a second load response at the same
thermal state are sufficient. WTC7 transfer additionally requires relevant
geometry, connection/restraint behavior, gradients, failure response and
sensitivity; the bar test cannot supply those by analogy.

## Claim and verification boundary

| Claim | Type and support | Strength / possible defeat |
|---|---|---|
| A one-load match is not generally sufficient for a clamp-force match. | Exact derived relation and explicit counterexample, independently calculated. | A within the declared model; an algebra/implementation error would defeat the result. |
| A one-load match plus equal compliance, or matches at two distinct loads, transfers the response. | Exact derived positive conditions, with controls. | A within the linear, load-independent-temperature assumptions; nonlinear coupling falls outside them. |
| Whole-history matching at one load can retain the ambiguity. | Constructed continuous-path proof and polynomial checks. | A for this state path; no assertion of historical thermal realizability. |
| NIST's particular approximation is materially wrong. | Not demonstrated by these inputs or tests. | D/unresolved; actual paired histories, calibration and relevant tolerances are required. |
| A collapse cause or intentional modeling choice follows. | No case-specific causal or intent evidence added. | E as a conclusion from this test alone. |

The [verification record](validation.md) preserves protocol revision, program
and output pins, actual commands, independent roles and limitations. Root's
12 tests and the independent calculator's 125 checks pass. Two runs of each
calculator are byte-identical. Post-freeze comparison matches 125 exact fields
across five common cases: 35 are prescribed inputs and 90 are derived values,
not independent observations. All nine oracle states and its complete run
payload also replay. Continuous-path records are checked separately, not
counted among those 125 cross-compared fields.

Computational independence reduces arithmetic and interpretation risk; it is
not licensed engineering review, another experiment or historical validation.
The bounded method test is complete; the comprehensive investigation is not.
