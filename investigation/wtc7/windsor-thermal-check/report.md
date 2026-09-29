# Windsor draft: an unreconciled thermal-depth benchmark

2026-09-20 UTC. Research only, charter WP4. [Protocol](PROTOCOL.md),
[declared source expansion](SCOPE-EXPANSION.md), [root freeze](root-notes.md),
[independent freeze](observer-notes.md), [calculation](calculation02.json),
[source integrity](integrity-review.md), [independent arithmetic](arithmetic-review.md),
[execution and limits](execution.md).

## Finding

The held **2007 Fletcher workshop draft contains a numerical inconsistency
under its apparent same-depth interpretation**: Figure4 assigns50.3mm of
thermal penetration to one hour, while adjacent prose says the thermal wave
traverses58mm in about1400seconds. An earlier time cannot have a greater depth
on the same increasing curve. Both source readers independently confirmed
the values and found no definition change reconciling them in the full13pages.

This is a real source-level problem, not proof that the authors' executable
model was wrong. The paper does not give the penetration equation, threshold
or boundary history needed to determine which number should change. An
unstated convention switch or drafting error is a plausible ordinary
explanation. A later corrected edition or original calculation could resolve
it; neither was inspected here. No fabrication or misconduct inference follows.

## Source and reproducible checks

Source: *Model-based analysis of a concrete building subjected to fire*,
Fletcher et al., draft for the October19,2007 Santander workshop. The held
[PDF](/Users/admin/docs/911/research/sherlock-wtc7-investigation/comparator-expansion/windsor/sources/fletcher-santander-2007-draft.pdf)
is195207bytes, SHA25630de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007.
This is not the later2008 proceedings version. Page locators below are physical
PDF positions; no separate printed page numbers are visible.

Two prior-informed AI readers each inspected all13 complete pages and froze
source/arithmetic notes before exchange. The initial four-page scope expanded
explicitly because the mathematical definition was missing there. Independent
Poppler replay matches all13 held images byte-for-byte and pixel-for-pixel,
without render diagnostics; the font-cache location changed to preserve main
read-only. Root rechecked23 pinned inputs, every image pair and the preserved
receipts. These are preservation/reading checks, not historical thermometry.

| Test | Independently checked result | Evidentiary meaning |
| --- | --- | --- |
| Material properties, p12 | 1.2/(2400×880)=5.681818…×10^-7m²/s, rounding to0.57×10^-6 | Internal diffusivity arithmetic is sound. The properties remain assumed values. |
| Five nodes across230mm, p12 | Four equal endpoint-inclusive gaps give57.5mm, approximately58mm | Geometric consistency under that node-placement interpretation; not validation of the actual ABAQUS configuration. |
| Figure/prose ordering, pp11–12 |1400<3600seconds, but58>50.3mm | Incompatible with the same increasing depth curve/time origin, independently of a chosen square-root formula. |
| Conditional square-root scaling anchored to the figure's50.3mm/3600s |31.37mm at1400s;58mm at4786.55s;57.5mm at4704.38s | A diagnostic consistency calculation, **not** recovered author input data or a proven corrected threshold. |
| Same conditional scaling at100s |8.38mm;10mm reached at142.29s | Does not establish that10mm node spacing is sufficient for accurate early heating. |

The source's increasing log-log plot motivates the conditional scaling test;
we did not digitize its line, fit an exact slope, or invent underlying samples.
The incompatible ordering alone is the stronger finding. Ordinary rounding
of the diffusivity, only0.32% relative to the calculated value, cannot explain
the roughly3.42 ratio between the two squared-depth/time normalizations.

As a **post-hoc algebraic diagnostic**, the hypothetical expression
`d = 2 sqrt(alpha t)` gives58mm at about1475s, or57.5mm at1450s, using the
printed diffusivity. This makes a different multiplier a plausible explanation
for the prose's approximate1400s. But the same expression gives90.60mm at
one hour, not50.3mm. It is not attributed to the authors and is not independent
evidence that this was their method. We cannot select a physical penetration
criterion from these numbers alone.

## What this changes scientifically

The **1400second mesh-resolution benchmark must not be treated as reproduced
or validated by Figure4**. The draft's general concern about unresolved steep
temperature gradients remains sensible, but this passage does not establish
the size or universal direction of actual FEM heating error, or that a mesh
becomes adequate when one spacing equals one penetration depth. Testing those
claims requires the actual temperature profile, shell temperature mapping,
interpolation and a controlled convergence comparison.

Do not substitute the p12 report of local500°C damage contours beyond200mm
for the figure's undefined penetration measure. The paper itself discusses
multi-sided heating of narrow waffle ribs; geometry, temperature criterion
and post-fire inference differ. A heat-diffusion penetration convention is
also not a measured first-arrival front or direct steel-failure temperature.

The full read retains the draft's legitimate scope: it discusses computed
thermal quantities and simplified structural modeling, while more extensive
multifloor/3D work is prospective. It also acknowledges beam idealization
limits on redistribution. This check neither demonstrates the actual Windsor
failure sequence nor negates its observed partial-collapse/survival outcome.
It does not test NIST's WTC7 temperature fields or establish fire or deliberate
support removal as more probable.

## Claim strengths and next discriminator

- **A, source observation:** the printed numerical claims and absence of an
  explicit defining equation in this13-page version; both full readings agree.
- **A, bounded calculation:** property arithmetic, geometric spacing and
  central-value ordering conflict, with their stated assumptions.
- **C, conditional diagnostic:** the square-root-scaled times/depths; they
  cannot be promoted to the authors' actual calculation.
- **D, unresolved model claim:** actual mesh error and corrected adequacy
  time. No convergence run or native model was inspected/executed.
- **E, unsupported extension:** concluding deception, actual collapse cause,
  or a WTC7 hypothesis ranking from this discrepancy.

The precise missing items are the Figure4 worksheet/equation and boundary
conditions, the node/section-temperature definition, imposed thermal profiles,
and a mesh-convergence series holding other inputs fixed. A source defining
two different penetration criteria could remove the apparent contradiction;
a corrected numerical value could instead identify a drafting error. The
later edition remains an unreviewed source lead, not proof of correction.

This is a substantive follow-through on the comparator limits retained in the
[Luna reevaluation](../luna-reevaluation-2026-09-19/report.md), not a newly
discovered claim that Luna personally calculated these values. Original notes,
sources, failed checks and both reading freezes remain preserved. No main/legal
or accepted Sherlock/Faraday state, request, publication, commit or push changed.
