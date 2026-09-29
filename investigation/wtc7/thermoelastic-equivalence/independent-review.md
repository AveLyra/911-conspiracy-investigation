# Independent mechanics derivation: frozen before implementation review

September 27, 2026. Synthetic, elementary mechanics only. This is a
prior-informed computational review, not empirical or licensed engineering
validation, a historical simulation, or a cause finding.

## Independence, scope, and protocol identity

I read the main AGENTS, CHARTER, applicable evidence/source skills, and the
complete protocol. `shasum -a 256 PROTOCOL.md` matched
`020decb3dabf5327886961abdf0da5c6a8adafe3127e7446c30a738626ebaa72`.
Before freezing this derivation I did not read root implementation/results,
the other agent's oracle/results, or any new source PDF. Results below are
exact algebraic evaluations, not a claim that an independent script ran.

There is no material well-posedness problem in the two clamp experiments.
The preloaded clamp replaces traction control; it does not impose force and
displacement independently at the same end. Positive force below means the
scalar axial force in tension, not the same global sign at both supports.

One output-reference ambiguity was sent to root before this freeze: at the
second probing load p2, does "increment" mean subtraction of the declared
cold preload extension p, or a separate cold test's extension p2? The main
counterexample does not depend on this choice. Both are labeled below rather
than silently choosing. Any protocol clarification needs a new recorded pin.

Root subsequently clarified both increments for every probing load n in
{0,p,p2}: d(n)-n and d(n)-p, with the clamp preload fixed at p. I re-read
the complete clarified protocol and verified its current SHA-256 as
`d9df71946dd097a4b6154d07fb07c8e0dff8206a91c1393f8251ceac9b817bc0`.
The initial local freeze was 160 lines with SHA-256
`92a4d6e60df5428b2615c753e255ff1b3b5b8ec35c2059c19f784b9a319d25ca`.
The old pin and ambiguity remain above; no algebraic result is discarded.
This clarification does not require reading either implementation or results.

## Derivation from equilibrium and compatibility

Let segment reference-length fractions be w_i > 0 with sum w_i = 1. There
are no distributed axial loads. Axial equilibrium in a series bar therefore
gives one common axial force F. Write f = F/(A E0), d = displacement/L0.
The stated small-strain constitutive law gives each segment's strain as

    epsilon_i = theta_i/1000 + f (1 + beta theta_i^2).

Compatibility is the reference-length-weighted sum of those strains. Define

    h = sum_i w_i theta_i/1000,
    c = sum_i w_i (1 + beta theta_i^2) > 0.

Then the total elongation is d(f) = h + c f. Here h is stress-free thermal
elongation and c is normalized axial compliance. All elongations below are
in units of L0; all forces are in units of A E0. At cold temperature h = 0
and c = 1, so the declared preload state has d = p.

For a prescribed total elongation D, the common axial force is

    f_D = (D - h)/c.

Thus cold stress-free clamping has f_0 = -h/c. Cold preloaded clamping has
f_p = (p - h)/c and force change f_p - p. A negative change from preload
does not necessarily mean the total axial force is compressive.

## One-load non-identification and exact positive conditions

If candidates A and B match loaded elongation at p, let
d_star = h_A + p c_A = h_B + p c_B. For a common clamp elongation D,

    f_D,A - f_D,B = (D - d_star) (1/c_A - 1/c_B).

This proves the exact transfer condition in the stated model: reactions
agree if and only if c_A = c_B or D = d_star. The latter is the degenerate
boundary choice that holds each bar at its common hot extension under p,
not either prescribed cold clamp except when those extensions coincide.

Equal compliance therefore makes a one-load match sufficient. Equal thermal
elongation plus a one-load match at nonzero p also identifies compliance.
Constant modulus, same geometry and area is a useful equal-compliance
positive control. The general negative claim is non-necessity, not that
matching at one load always produces different restrained reactions.

At one fixed, load-independent temperature state, two distinct probing loads
f1 and f2 identify

    c = (d(f2) - d(f1))/(f2 - f1),
    h = d(f1) - f1 c.

Thus matching both elongations between candidates identifies both h and c
and transfers to every D in this linear model. Coincident loads cannot
identify the pair and must be rejected, not assigned an arbitrary slope.

## Exact fixed-fixture values

For beta = 1, p = 1/1000 and p2 = 1/500:

| Quantity | Uniform [1,1,1] | Variable [0,0,2] |
|---|---:|---:|
| h | 1/1000 | 1/1500 |
| c | 2 | 7/3 |
| d(0), also its own-cold increment | 1/1000 | 1/1500 |
| d(0) - p, common reference preload increment | 0 | -1/3000 |
| d(p) | 3/1000 | 3/1000 |
| d(p) - p | 1/500 | 1/500 |
| d(p2) | 1/200 | 2/375 |
| d(p2) - p, same declared preload reference | 1/250 | 13/3000 |
| d(p2) - p2, separate cold probing-load reference | 3/1000 | 1/300 |
| Cold stress-free clamp total force | -1/2000 | -1/3500 |
| Cold preloaded clamp total force | 0 | 1/7000 |
| Cold preloaded clamp force change from p | -1/1000 | -3/3500 |

The increment d(0)-p includes removal of the reference preload. A negative
value there is not a negative stress-free thermal expansion.

At beta = 0, the positive-control pair [1,1,1] and [0,0,3] both give
h = 1/1000, c = 1, d(p) = 1/500, d(p2) = 3/1000, stress-free clamp
force -1/1000 and preloaded clamp force 0, with increment -1/1000.

With zero heating, both laws give h = 0, c = 1, d(p) = p, zero
stress-free-clamp force and preloaded-clamp force p with zero increment.
Identical profiles are identical by construction. Subdividing a segment
while preserving its total reference-length weight and temperature leaves
both sums invariant; reordering segments also leaves these global responses
unchanged. Neither invariance establishes equality of local temperature or
local strain fields, or invariance for models outside these assumptions.

## Full continuous-path proof, not sampled evidence

Take uniform theta_i = s and variable theta = [0,0,q], where

    q = (-1 + sqrt(1 + 12 s^2 + 12 s))/2,
    0 <= s <= 1.

This is the unique nonnegative solution of q^2 + q = 3(s^2 + s).
It is continuous, q(0) = 0, q(1) = 2, and
q'(s) = (6s + 3)/(2q + 1) > 0. Each segment therefore has a nondecreasing
temperature; two variable-profile segments remain cold, not strictly hotter.

For every s, the two total loaded elongations at p are exactly equal:

    d_U(p) = (1 + s + s^2)/1000,
    d_V(p) = (1 + (q + q^2)/3)/1000 = d_U(p).

For s > 0, q < 3s because x^2+x is strictly increasing for x >= 0 and
(3s)^2 + 3s > 3(s^2+s). Hence

    c_V - c_U = q^2/3 - s^2 = s - q/3 > 0.

Also d_star = p(1+s+s^2) > p. For either prescribed clamp D = 0 or
D = p, the reaction-difference identity proves f_D,U < f_D,V at every
s > 0; they coincide at s = 0. At p2 the loaded elongation difference is
(p2-p)(c_V-c_U) > 0. Equality over the entire constructed path at one load
therefore does not supply the missing second independent relation.

This is an algebraic identity and inequality proof over the interval, not
an inference from finitely many floating-point samples. It establishes an
admissible path of the declared constitutive states only; no thermal PDE,
coating profile, diffusion, heat balance or historical fire was solved.

## Strongest objection and inference ceiling

The strongest objection is that the actual application may constrain thermal
fields/compliance more tightly, compare additional responses or loads, or
operate in a regime where compliance differences have negligible effects.
This constructed model does not show that any specific reported NIST pair
violates equivalence or that the needed fields arise from actual coating.
It tests a claimed necessary implication, not the accuracy of a particular
approximation. Equal compliance and two-load identification are explicit
ways in which transfer does hold; these should accompany the counterexample.

The law theta/1000 and E/E0 = 1/(1+beta theta^2) is synthetic. Its normalized
temperature is not a measured steel temperature, and its exact arithmetic
does not validate empirical constitutive behavior, restrained stability,
connection failure, WTC7 response or a collapse cause. The result also does
not extend two-load identification to load-dependent heating, nonlinear
material response, plasticity, creep or damage. No such results were tested.
