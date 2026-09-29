# Independent Windsor draft source/arithmetic reading

2026-09-20. Frozen before reading root notes/code or receiving root numerical
findings. Prior-informed AI reading, not blind, a historical witness, or expert
certification. Research only; no solver, network, new source, or canonical change.

## Scope, provenance and actual coverage

Read PROTOCOL.md completely, then the prospective SCOPE-EXPANSION.md before
viewing any added pages. Original scope was physical pp10–13; these four pages
were inspected first, in order, once each. The explicit amendment then admitted
pp1–9 to check for an earlier definition; these were inspected in order, once
each. **13 complete pages, 13 displays, zero repeated or failed displays.**
No note was frozen at the four-page stage. No page beyond this 13-page draft
and no later edition or cited reference was opened. No text extraction was used.

The document is *Model-based analysis of a concrete building subjected to fire*,
with the recurring header identifying a draft for the Santander workshop,
19 October 2007. No printed page number is visible on these pages; all page
references below are physical PDF positions. All thermal quantities, Figure 4
axes/annotation, conclusions and references are legible. Page 10 has a crowded
inline ventilation-rate expression; I do not claim exact symbol transcription
or use it in any calculation. The thermal-penetration result does not depend on
that expression. No other material clipping/illegibility was observed. Existing
images were read, not repaired or regenerated; visual reading is not a claim of
a clean original rendering environment or independent-engine fidelity.

Read-only source root:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/`

| Input | SHA-256 |
| --- | --- |
| windsor/sources/fletcher-santander-2007-draft.pdf (195,207 bytes) | `30de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007` |
| validation-receipt.json | `022d706460953f551eee7ef8e4634dd56bf074a3b144c13a9550051c352fa0f9` |
| This unit's PROTOCOL.md | `d02efad11d2008aa65536547510d78110daae974693d4291d6c07c359573db05` |
| This unit's SCOPE-EXPANSION.md | `063d4c02ca135382ebab6c71ce3b005f29ba946acd5f16f59d2d7b85bae6f147` |

Actual admission checks used `shasum -a 256`, source `stat -f '%N %z bytes'`,
and Ruby JSON/Digest comparison of exact `path`/`sha256` entries in the central
receipt. First the PDF and pp10–13 matched (5/5); before expanded admission,
pp1–9 matched (9/9). After all reading, the PDF and all 13 PNGs matched again
(14/14). These commands exited 0. Image paths are
`windsor/rendered/fletcher-01.png` through `fletcher-13.png`; their exact baseline
hashes are retained in the pinned central receipt. Main AGENTS, WORKFLOW,
START-HERE and full CHARTER hashes matched the previously fully read controls.
Evidence-falsification, PDF and source-of-truth skills were read and applied.

## What the source states

| Page | Source claim/definition and status |
| --- | --- |
| 2,5–7 | Thermal exposure can be represented by surface temperature, gas temperature or incident flux; transient and steady-state approaches and model-resolution limits are discussed. These alternatives are not an explicit mathematical definition of the later penetration depth. Concrete/rebar properties are temperature-dependent in the general discussion. |
| 8–10 | Initial structural idealization treats the slab as beams; bottom cover includes 10 mm clay plus 10 mm concrete, idealized as concrete. P9 gives a 0.23 m deep, 0.1 m wide beam at 0.6 m centers, with assumed fixed/pinned structural end conditions. P10 selects narrow deep shell elements to allow depth-dependent temperature input. Those mechanical supports do not define the thermal boundary condition of Figure 4. |
| 10–11 | Fire-model results depend on ventilation assumptions. P10 reports peak computed gas temperature above 1100 C and concrete surface temperature about 200 C lower. P11 attributes surface temperatures above 800 C to post-fire analysis [3]. Neither claim is independently validated here. Independent thermal models provide temperatures to shell layers/rebar; insufficient nodes are said to exaggerate heating and affect mechanical predictions. |
| 11, Figure 4 | Title: thermal penetration depth for concrete. Logarithmic horizontal axis: time in seconds, labeled 10,100,1000,10000. Logarithmic vertical axis: penetration depth in mm, labeled 1,10,100. A visibly increasing straight plotted trend is annotated **one hour = 50.3 mm**. I did not digitize that curve or assign precise values to unlabeled points. |
| 12, first paragraph | Assuming normal-weight siliceous-aggregate concrete: density **2400 kg/m3**, conductivity **1.2 W/m/K**, specific heat **880 J/kg/K**, reported diffusivity **0.57 x 10^-6 m2/s**. Specified strengths: 24.5 MPa columns/walls, 29.4 MPa deep beams, 17.2 MPa floor slabs, with variations acknowledged. |
| 12, first paragraph | Fire duration is uncertain; evidence [10] is said to support a main burning phase on the order of one hour, leading to penetration about 50 mm. Post-fire studies [3] reportedly found small ceiling regions with a **500 C isotherm** beyond 200 mm; side heating of 100 x 200 mm waffle beams, excluding the top slab, is offered as a possible explanation. This separately specified damage/isotherm depth is not stated to define Figure 4's penetration convention. |
| 12, second paragraph | Five default nodes per shell element in a 230 mm-deep beam/slab assembly give **58 mm spacing**, said to be traversed in **about 1400 s**. Before that time thermal response is said to be unresolved. Figure 4 is invoked for a required resolution of at least 10 mm for the first 100 s. No convergence runs or error magnitudes accompany these claims. |
| 12–13 | The conclusion describes an approach being undertaken and models developed to examine possible mechanisms, not a completed validated reconstruction. References include the 2005 INTEMAC study [3] and Kono's 2005 investigation [10]; those sources were not followed in this unit. |

After reading all 13 pages, I found **no explicit penetration-depth equation,
temperature-rise threshold, prefactor, or specified initial/surface-temperature
history for Figure 4's simple calculation**. Its use of thermal-wave language
does not define a literal sharp front or first-arrival temperature criterion.
Different exposure/threshold conventions could yield different depths, but the
draft does not identify such a change between the two adjacent numerical claims.

## Independent arithmetic

Chosen implementation: Ruby 2.6.10p210, standard `Rational` arithmetic for
material properties, squared ratios and inverses; `Math.sqrt` only for displayed
square roots. No root code was read or imported. Computation ran once, exited 0,
and all **seven deterministic arithmetic assertions passed**. This validates
the local arithmetic, not the author's unspecified calculation or historical
thermal response.

Material diffusivity uses the dimensional relation conductivity divided by
volumetric heat capacity: `(W/(m K))/((kg/m3)(J/(kg K))) = m2/s`.
The spacing check assumes five uniformly spaced endpoint-inclusive nodes, which
is the simple geometry consistent with the printed 58 mm; it is not an ABAQUS
element-definition validation.

| Quantity | Independent result | Meaning |
| --- | --- | --- |
| 1.2/(2400 x 880) | 5.68181818182 x 10^-7 m2/s = 0.568181818182 mm2/s | Rounds to the source's 0.57 x 10^-6; rounded value is 0.32% higher. Material-property arithmetic reproduces. |
| 230/(5-1) | 57.5 mm | Rounds to 58 mm. Spacing arithmetic is consistent under the stated geometric interpretation. |
| (50.3 mm)^2/3600 s | 0.702802777778 mm2/s | A descriptive squared-depth/time ratio, not an attributed author formula. |
| (58 mm)^2/1400 s | 2.40285714286 mm2/s | 3.41896363935 times the preceding ratio. Ordinary rounding of diffusivity cannot make the two the same fixed squared-depth/time relation. |
| Depth/sqrt(alpha x time), figure pair | 1.11217484637 | Dimensionless diagnostic computed from that pair and the property-derived alpha, not a chosen physical penetration threshold. |
| Depth/sqrt(alpha x time), node pair | 2.05646020419 | Different diagnostic coefficient; the paper does not supply the definition required to select either one as physically correct. |
| **Conditional** fixed squared-depth/time scaling anchored only at 50.3 mm/3600 s | 31.3675610925 mm at 1400 s; 58 mm at 4786.54909509 s; 57.5 mm at 4704.37810513 s | Algebraic consistency checks, **not** reproduction of an expressly stated heat-transfer equation or established corrections to the paper. |
| Same conditional figure scaling | 8.38333333333 mm at 100 s; 10 mm at 142.28742851 s | Does not validate that 10 mm nodal spacing adequately resolves the first 100 s. Resolution wording is not a convergence result. |
| Conditional fixed squared-depth/time scaling anchored at 58 mm/1400 s | 93.0069121855 mm at 3600 s | Illustrates the incompatible normalization; not an actual temperature/depth prediction. |

No heat-transfer equation has been imported to fill the missing definition.
The conditional rows merely ask whether a single fixed squared-depth/time
ratio could reproduce both printed pairs; they do not identify that ratio as
the author's law. The visibly straight log-log trend motivates examining
scaling but was not fitted, digitized, or assigned an exact slope.

Reproducible arithmetic command body (executed with `ruby -e`):

```ruby
puts RUBY_DESCRIPTION
alpha = Rational(12,10) / (2400 * 880)
alpha_mm = alpha * 1_000_000
spacing = Rational(230,4)
fig_x = Rational(503,10)
fig_t = 3600
node_x = 58
node_t = 1400
fig_rate = fig_x**2 / fig_t
node_rate = Rational(node_x**2,node_t)
q = {
  alpha_m2_s: alpha,
  alpha_mm2_s: alpha_mm,
  alpha_rounded_relative_difference: (Rational(57,100)-alpha_mm)/alpha_mm,
  five_endpoint_node_spacing_mm: spacing,
  figure_squared_depth_per_time_mm2_s: fig_rate,
  node_squared_depth_per_time_mm2_s: node_rate,
  node_to_figure_squared_rate_ratio: node_rate/fig_rate,
  figure_dimensionless_squared_depth: fig_rate/alpha_mm,
  node_dimensionless_squared_depth: node_rate/alpha_mm,
  figure_depth_over_sqrt_alpha_t: fig_x.to_f/Math.sqrt((alpha_mm*fig_t).to_f),
  node_depth_over_sqrt_alpha_t: node_x/Math.sqrt((alpha_mm*node_t).to_f),
  conditional_figure_scaled_depth_at_1400_mm: Math.sqrt((fig_rate*node_t).to_f),
  conditional_figure_scaled_depth_at_100_mm: Math.sqrt((fig_rate*100).to_f),
  conditional_figure_scaled_time_to_58_s: node_x**2/fig_rate,
  conditional_figure_scaled_time_to_57_5_s: spacing**2/fig_rate,
  conditional_figure_scaled_time_to_10_s: 100/fig_rate,
  conditional_node_scaled_depth_at_3600_mm: Math.sqrt((node_rate*fig_t).to_f),
  conditional_node_scaled_depth_at_100_mm: Math.sqrt((node_rate*100).to_f)
}
q.each { |key,value| puts "%s = %.12g" % [key,value.to_f] }
checks = 0
check = ->(condition) { abort "Assertion #{checks + 1} failed" unless condition; checks += 1 }
check.call(alpha == Rational(1,1_760_000))
check.call(alpha_mm.round(2) == 0.57)
check.call(spacing == Rational(115,2))
check.call((node_x**2/fig_rate)*fig_rate == node_x**2)
check.call(fig_rate*(4*fig_t) == (2*fig_x)**2)
check.call(node_t < fig_t && node_x > fig_x)
check.call(node_rate > fig_rate)
puts "#{checks} arithmetic assertions passed; conditional scaling is not an attributed author formula"
```

## Bounded assessment and what could change it

The strongest inconsistency test needs **no assumed square-root law**:
**1400 s is earlier than 3600 s, but 58 mm (also the unrounded 57.5 mm) is
greater than 50.3 mm.** They cannot both describe the same increasing
penetration-depth function plotted in Figure 4. Thus the adjacent prose and
figure annotation are internally inconsistent **under the same-depth reading**.
No single material-property rounding correction resolves that ordering. The
exact author's intended convention and which printed value should change remain
undetermined; this is not a full reproduction of the thermal calculation.

The strongest ordinary explanation is a drafting/label/transcription error,
or an unstated change in penetration criterion or calculation assumptions.
An original calculation defining separate depth criteria could make both
numbers meaningful. A corrected annotation or time could instead remove the
conflict. The admitted draft supplies neither, so the two values should not be
treated as jointly reproduced. Numerical disagreement is not evidence of fraud.

The general concern about resolving steep temperature gradients with enough
through-depth nodes survives this check as a modelling concern; the specific
1400 s resolution threshold is not verified by the displayed curve. Under the
explicitly conditional figure-anchored scaling it would be later, around
4.7–4.8 ks, but that is not a proven corrected threshold. No magnitude or even
universal sign of actual FEM temperature/mechanical error is established by
this arithmetic. The author's assertion of exaggerated heating would require
the actual discretization, imposed thermal profiles and convergence comparisons
to test in this case. It is not enough to compare one spacing with one heuristic
depth or to infer adequate resolution immediately after one nominal crossing.

Historical exposure remains uncertain; the local 500 C damage isotherm and
multi-sided heating discussion cannot be silently substituted for Figure 4's
undefined criterion. No actual Windsor residual capacity, exact collapse
sequence, or WTC7 causal conclusion follows. The next exact dependency is the
draft's underlying penetration calculation/definition and, for model-error
claims, actual thermal inputs and a controlled mesh-convergence comparison.
This note does not authorize retrieval, later-edition substitution or a solver.
