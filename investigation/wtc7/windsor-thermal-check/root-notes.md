# Root source and calculation freeze

2026-09-20 UTC, before independent observer findings/code were read. Source
SHA25630de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007.
Prior-informed AI reading, not blind review or engineering certification.

## Actual coverage

Viewed all13 complete held100dpi PNGs exactly once:10–13 first, then1–5,
then6–9 after the explicit SCOPE-EXPANSION amendment. No failed display,
crop, enhancement or unreadable passage observed. Every page carries the
October19,2007 workshop-draft header; no separate printed page numeral was
visible. All locators here are physical PDF pages. Root matched source and
all13PNG hashes to the held comparator validation receipt. Independent
integrity replay reports all13 byte/pixel matches with no render diagnostics;
its source-interpretation role is excluded and no observer findings received.

## Source transcription/context

- P11 Figure4 has logarithmic axes: time in seconds10–10000, penetration
  depth in mm1–100. Visible increasing straight plotted line and annotation
  assigning50.3mm to1hour. This is a printed calculation claim, not measured
  historical penetration or a curve we digitized.
- P12: density2400kg/m³, conductivity1.2W/(m K), specific heat880J/(kg K),
  diffusivity0.57×10^-6m²/s. Concrete material properties are assumptions,
  not independent specimen measurements here. P12 says main burning phases
  of order1hour uncertain, referring to source10; about50mm penetration.
- P12:230mm-deep modeled beam/slab assembly, default5nodes/shell element,
  spacing58mm, traversed in about1400s. P12 also says Fig4 suggests at
  least10mm resolution for the first100s. We have no native shell settings
  or temperature interpolation scheme; their terminology is not independently
  validated ABAQUS behavior.
- P11 states insufficient nodes tend to exaggerate heating, affecting the
  mechanical modeling. No numerical convergence series or actual mesh-error
  estimate is shown. P12 restates early under-resolution, not a completed
  fully validated failure simulation.
- No explicit penetration equation, threshold temperature/fraction or boundary
  condition tied to Fig4 was located anywhere in the13pages. The earlier
  sections describe alternative imposed temperatures, gas/flux histories,
  spatially varying CFD and quasi-steady/transient approaches; they do not
  specify which defines this illustrative penetration calculation.
- P12 juxtaposes roughly50mm with reported500°C damage contours exceeding
  200mm in small regions, offering side heating of narrow waffle ribs as a
  possible explanation. These are different quantities and geometries; do
  not call that a measured fourfold model error or directly equate the graph's
  undefined penetration to a500°C isotherm.
- P9 approximates clay+concrete cover as concrete, a fixed core attachment
  and pinned perimeter attachment; p6 warns beam simplification precludes
  much3D redistribution; p7 considers upper floors taking tension after
  lower support loss. P10 further2D/multifloor/3D work is future. P4's observed
  buckled ninth-floor steel with retained structure is positive survival
  context, not a computed reserve margin. P8 lists possible failures, not
  uniquely established actual sequence.
- P13 reference3 is INTEMAC2005; reference10 is Kono's2005 Japanese report.
  Neither is newly inspected for this unit. The existing source assessment
  already qualifies the post-fire temperature 'confirmation' on p11 as an
  assumption-dependent reconstruction. This is not new historical thermometry.

## Root calculations, frozen conditional meanings

`calculate.py` (SHA25661c28ab16f55a2c9ba1003ea57ccc089f8c6f3bf5c26ed5fc26403fa58c6dbf7)
uses50-digit Decimal arithmetic. Nine controls passed; calculation02.json
SHA256f27147daca48b0b99c69d6cf025d9eb670925f1d9c15911b5d8277b7fb25e8f8.

1. k/(rho c)=5.681818…×10^-7m²/s,0.32% below the printed rounded value
   when the difference is expressed relative to the calculated value.
   The properties' internal arithmetic is sound to the printed precision.
2. Five equally spaced endpoint nodes over230mm give four gaps57.5mm,
   consistent with rounded58mm. Equal endpoint spacing is an assumption,
   not an authenticated software model.
3. Same-curve monotonicity:1400s<3600s but58mm>50.3mm. Those central
   points cannot belong to one nondecreasing depth curve with the same
   definition/time origin. This conclusion does not require fitting a power
   law. It does require that the source's adjacent prose and figure refer
   to the same depth; the paper provides no distinct definitions reconciling
   them. Cooling can move an isotherm back, but the shown increasing curve
   and this explanatory calculation do not supply such a case.
4. **Conditional**, not a recovered author formula: assuming d proportional
   to sqrt(t), normalized to50.3mm at3600s, d(1400)=31.36756mm,
   d(100)=8.38333mm. Reaching58mm takes4786.549s (79.78min), or57.5mm
   takes4704.378s.10mm corresponds142.287s. This does not recover exact
   Figure4 data or justify a required count of temperature nodes.
5. Hypothetical convention d=2sqrt(alpha t), using printed alpha, gives
  58mm at1475.439s; using57.5mm gives1450.110s. Thus the prose's about
  1400s could plausibly reflect a different multiplier/convention. But this
   same convention gives90.598mm at1hour, not50.3mm. It is a candidate
   ordinary explanation, not an attributed author equation or correction.
   Calculated alpha changes the58mm time only to1480.16s; property rounding
   cannot bridge the factor-of-about3.4 time difference between these curves.

The first code edition hard-coded the elementary ordering conclusion and
misnamed its field 'assumption_free'; root corrected this before freezing.
Original code and calculation01 remain preserved. The final function computes
ordering from inputs and tests increasing/decreasing/constant/duplicate-time
controls; it expressly retains the same-definition assumption. Scientific
numerical values did not change. Passing bookkeeping tests does not validate
the paper's model or the historical event.

## Assessment and falsifier

An internal, unreconciled figure/prose numerical inconsistency exists under
the paper's presented common monotonic-depth interpretation. The exact
formula is under-specified, so we cannot identify which number is erroneous
or assert that its executable model used either. A documented different
definition, time origin, corrected figure/edition or original calculation
could resolve it. No deception/fraud inference.

The general concern that steep thermal gradients require adequate resolution
survives; this passage does not quantify sign/magnitude of its model's actual
heating/strength error or establish10mm as converged. The1400s adequacy
benchmark must not be reused as verified. Concrete thermal analysis here
does not directly test NIST's WTC7 steel-temperature histories, its fire
mechanism or a demolition alternative. No cause ranking follows. Missing
thermal worksheet/definition, actual shell temperature mapping and convergence
outputs are more discriminating than further speculation over this draft.
