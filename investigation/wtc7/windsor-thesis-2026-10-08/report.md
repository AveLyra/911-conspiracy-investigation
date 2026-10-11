# Windsor thesis mesh sensitivity and unresolved thermal benchmark

October 8, 2026. Research-only WP3/WP4 comparison. The 2009 Fletcher thesis
contains substantially more numerical sensitivity work than the 2007 draft.
It **does not resolve the earlier thermal-depth discrepancy within the 77
reviewed pages**, and its reported mesh study does not establish full-duration
convergence under the final corrected inputs. Neither finding identifies
WTC 7's cause or demonstrates that the Windsor model's actual error was large.

## Source and coverage

The [original thesis](fletcher-2009-thesis.pdf) was acquired from the
[University of Edinburgh repository](https://era.ed.ac.uk/items/2ca19958-abdd-42f6-8c03-6775017f9690),
4,425,293 bytes, 207 pages, SHA256
`4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543`.
Its title page identifies Ian A. Fletcher, May 2009. The publication table
(Table 1.3, printed page 8) connects it to the same Windsor research lineage; this is a
distinct later work, not a verified corrected edition or independent historical
witness. The 2008 article's failed access route remains closed.

[Protocol](PROTOCOL.md), [initial roster](PAGE-SELECTION.md) and
[one context expansion](SCOPE-EXPANSION.md) define the 77 complete pages.
Locators below are **printed body pages**; add 26 for physical PDF positions.
This is a bounded method-section review, not a whole-thesis or native-model
audit. [Reading and comparison](review.md), [execution](execution.md) and
[integrity checks](integrity-review.md) distinguish source reading from
reproduction of the author's calculations.

## What the later source changes

| Question | Source evidence | Supported disposition |
|---|---|---|
| Does it reconcile 50.3 mm at 3600 s with 58 mm at about 1400 s? | Penetration is mentioned at 58/62 without a defining threshold or equation in the reviewed sections. The 50.3 locator is rebar area, mm², at 93; 1400 matches part of a 14000-second axis label at 143. | **Unresolved.** No demonstrated correction or common-case reconciliation; a later, differently specified thermal model is not a corrected number. |
| Was mesh sensitivity actually investigated? | At 110–113, Table 5.7 and Figures 5.36–37 compare 20, 40, 160 and 480 elements with named case files, common stated 15-minute upward spread, calcareous concrete and 1.5% moisture. Responses include displacement and reinforcement strain. | **Yes, as published model results.** Saying no sensitivity study exists would be incorrect. |
| Does that establish convergence? | The 160/480-element analyses did not finish; the source reports 24.7/23.3 hours and an unknown cause. The author describes endpoints as comparable at similar times and generally judges the differences small. Displacement varies nonmonotonically; the strain components respond differently. | **Partial sensitivity evidence, not demonstrated full-duration convergence.** Neither reader established a common numerical tolerance. No depth-resolution series or temperature-error norm is supplied here; actual numerical error remains unquantified. |
| Does it test the final corrected configuration? | At 118–126, concrete damaged plasticity (CDP) and thermal-expansion definitions change. Earlier sensitivity sweeps, expressly including mesh at 126, were not rerun with all corrections. | **Transfer remains unverified.** A small mesh effect in one configuration is not automatically a bound for another. |
| Is there other numerical error checking? | At 142–144, two steel-temperature time-step schedules are compared. Reported differences range from −1.8% to +1.1% for insulated steel and −21.3% to +8.9% for uninsulated steel; the finer schedule is selected for the latter. | **Useful, separate time-step sensitivity.** It does not validate concrete through-depth resolution or the old penetration benchmark; neither schedule is an independently established exact solution. |

These are observations of what the source reports, followed by bounded
methodological inferences. No plotted values were digitized, native cases
executed or reported error percentages independently recalculated.

## Qualifications that affect interpretation

The concrete representation is a simplified shell strip, with matching
thermal/stress nodes and depth temperature-point counts, external temperatures
on top/bottom and no shell-edge heat inflow (90–100). A stated capability of up
to 19 temperature points is not evidence of a controlled depth-refinement test.
The 1D-versus-2D illustration is a schematic justification, not a quantified
validation of equivalent heating. The constant-property diffusivity from the
old draft cannot silently substitute for the later temperature-dependent
material assumptions.

At 107–108 the thesis reports excessive internal temperatures from an
Abaqus 6.7-1 heat-transfer error, with the selected 15-minute case rerun in 6.8-1.
It does not report rerunning the full earlier fire-spread sweep. Later sections
report changed concrete-plasticity values, difficulties with tensile softening
and corrected expansion inputs. Tables 5.20 and 5.22 show changed deflections:
−0.3655 m to −0.301 m for the calcareous beam comparison; −0.127 m to −0.09814 m for
the siliceous floor comparison. These are the thesis's model outputs and
diagnoses, not our reproduced solver results. They cannot be attributed as
the cause of the 2007 depth discrepancy without a source/input link.

The strongest favorable reading is that the author openly investigated
sensitivity, disclosed failures and corrected inputs; incomplete finer runs
do not negate all usable comparisons before they stopped. The strongest
objection to the blanket mesh-adequacy conclusion is that neither matched
full-duration refinement under the final properties nor a through-depth
thermal error bound is demonstrated in this material. The honest conclusion
is narrower than either “validated” or “invalid.”

The thesis itself frames a Windsor-like structural model and acknowledges
uncertain historical top support, excluded damage evolution and useful future
3D/material/fire work (68, 171–176). It also claims agreement with ninth-floor
deformation observations (173); that remains the author's claim, not our
independent historical validation. Its failure/survival results cannot be
transferred to WTC 7's different structure or used as an independently verified
fire-only control. The original Windsor observed outcome remains distinct from
the adequacy of this explanatory model.

## Claim strength and next discriminator

- **A, source observations:** the tabulated mesh cases, incomplete runs,
  disclosed corrections and stated rerun limits within the inspected pages.
- **B, methodological inference:** these passages do not demonstrate the
  specific final-configuration/depth-resolution convergence claimed by a
  broader reading. This is not a thesis-wide absence assertion.
- **D, unresolved:** the original depth definition and actual numerical-error
  size; native outputs and executable cases were not admitted.
- **E, unsupported extension:** misconduct, a WTC 7 temperature result, an
  intervention finding or a changed WTC 7 cause ranking from this comparison.

The original Figure 4 worksheet with its boundary conditions and temperature
criterion could reconcile the draft or identify a drafting error. For the
later mesh question, obtain the Table 5.7 heat/stress pairs, completion logs
and matched response histories, followed by a controlled refinement series
using the final material inputs and explicitly varied through-depth temperature
resolution. A stable quantitative series would strengthen adequacy; material
response changes under refinement would weaken that adequacy inference.
This is a concrete future test, not a claim that those
files are publicly available or that another solver run is currently feasible.

The [2007 audit](../windsor-thermal-check/report.md) remains preserved with its
same-depth qualification. No prior source, legal record, accepted engine state,
human-review decision, commit or push changed. The broader investigation
remains active; this bounded source review does not complete it.
