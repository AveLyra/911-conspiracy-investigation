# Root source reading freeze

October 8, 2026. Frozen before reading the other observer's scientific notes.
Prior-informed AI reading, not blind adjudication, licensed engineering review
or replication of the author's numerical models. Original PDF SHA256
`4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543`.

## Actual coverage

I inspected every complete full-page110dpi image in the original61-page
roster and the single16-page expansion: physical1,11–15,33–34,81–94,
114–154,161–162,166–171,197–202. Total77. Printed body pages are physical
minus26; labels, headings, tables and figures were visually checked, including
the intentionally blank pages82 and154. Text extraction assisted front matter
and publication-table reading; visual pages controlled interpretation. No
graph digitization or solver execution. Render generation alone was not
counted as inspection. This is not a whole-thesis reading.

## Six comparison fields

1. **Depth quantity and threshold.** Printed58 and62 mention penetration as
   an objective/available output, without an equation or specified temperature
   threshold. None of the77 inspected pages defines the earlier draft's
  50.3mm/3600s versus58mm/~1400s penetration benchmark. The literal50.3 match
   is reinforcement area in mm² (Table5.1, printed93), not depth; the1400
   locator is within a plot's14000-second axis tick (Figure6.5, printed143),
   not a1400-second penetration claim. No explicit correction of the draft's
   pair was found within this coverage. Disposition: unresolved original
   definition; different/noncomparable later thermal analysis, not proven
   reconciliation or correction.
2. **Time origin and thermal boundary.** Printed61 uses an ISO-based heating
   curve and one-hour linear cooling; printed103–104 applies relative top/bottom
   onset delays, including bottom-only, rather than the old undefined thermal
   wave calculation. Printed100 applies external temperatures through radiative
   and convective films at shell top/bottom. Printed103 states100-hour heat
   transfer analyses to include cooling. Printed105 and140 warn about duration
   scaling during thermal-to-stress transfer. Printed135 uses one-hour heating
   plus one-hour cooling for the later model. These are model prescriptions,
   not recovered historical thermometry.
3. **Materials.** Printed88–89 uses Eurocode-derived temperature-dependent
   properties, calcareous concrete in most early sensitivity runs, and CDP
   without damage evolution. Actual properties are referred to AppendixA;
   this selected PDF/page review does not supply a native materials deck.
   Printed108–110 specifies1.5% moisture for subsequent work and upper-bound
   conductivity; spalling is excluded. Printed118–126 later changes CDP,
   tensile treatment and expansion definitions. Printed135 uses siliceous
   concrete and full live load. Do not transfer the earlier constant-property
   diffusivity calculation into these different assumptions.
4. **Geometry and exposure.** Printed90–92 simplifies a230mm-deep,
  100mm-wide waffle rib with5.2m span into a simply-supported beam-like shell
   strip, omitting the structural contribution of inter-rib screed. Clay sides
   are omitted and bottom clay represented as concrete. Printed93–100 introduces
   a fixed-ended floor variant and then explains the one-dimensional heating
   approximation, excluding shell-edge heat inflow; Figure5.28 is a schematic
   rationale, not a measured/quantified1D-versus2D validation. Printed67–68
   explicitly frames a selected Windsor-like section, not a totally forensic
   whole-building reconstruction.
5. **Mesh and temperature mapping.** Printed92 states S4R shells can have up
   to19 depth temperature points; this is a capability statement, not a
   through-thickness refinement experiment. Printed100 says DS4 thermal and
   S4R stress models share nodes and depth temperature-point counts. Table5.7
   (printed111) compares20,40,160,480 elements with named heat/stress files.
   It does not report a series refining the earlier five depth nodes, a depth
   threshold, or an early-heating temperature-error norm. Do not conflate
   element-count sensitivity with resolving the draft's depth benchmark.
6. **Convergence and error evidence.** Printed110–113 reports a real numerical
   sensitivity series under15-minute upward spread, calcareous concrete and
  1.5% moisture; Figures5.36–37 compare reinforcement strain and displacement.
   Table5.7 reports the160/480-element runs did not complete, stopping after
  24.7/23.3hours, with unknown cause. Prose says their endpoints were comparable
   to coarser runs at similar times and variation generally minor, then concludes
   mesh effects negligible. This is positive evidence of an attempted and
   partially completed sensitivity study, not demonstrated full-duration mesh
   convergence or a quantified heat-gradient error bound. No precise graph
   differences have been measured in this review.

## Material qualifications and favorable evidence

Printed107–108 reports an Abaqus6.7-1 heat-transfer error producing excessive
internal temperatures. Only the selected15-minute case was rerun with6.8-1;
the earlier fire-spread sweep was retained as more severe. This is the thesis's
reported software/case issue, not our independently verified diagnosis, and
not an identified cause of the2007 penetration-number inconsistency. Figures
5.30 and5.33 visibly present different thermal histories with the source's
version labels; no exact temperature reductions are inferred from the plots.

Printed118–119 reports initial CDP parameters may have been unphysical and
provides a changed-parameter comparison (Tables5.11–12); earlier sensitivity
models were not all rerun. Printed120–122 reports failure to converge using
nonductile tensile behavior and a retained ductile idealization with a
temperature-dependent tensile floor. These are numerical accommodations,
not evidence that real concrete follows that idealization.

Printed122–126 identifies incorrectly formatted thermal-expansion inputs and
tabulates corrected coefficients and response changes. Table5.20 reports
calcareous beam deflection changing from−0.3655m to−0.301m; Table5.22 reports
siliceous floor deflection changing from−0.127m to−0.09814m. These are quoted
model results, not newly reproduced calculations. Printed125 says correction
allowed a previously unstable siliceous beam to complete. Printed126 expressly
declines to rerun prior delay/moisture/mesh/duration sweeps with corrected
expansion values, and identifies remaining low-temperature expansion issues.
That limits transfer of the early mesh conclusion to the final material setup.
The text's candor and positive corrections count against dismissing this as
merely an animation or claiming that no sensitivity work was done.

Printed142–144 supplies a separate, useful two-step-size steel-temperature
comparison: large increments300s before ignition,60s during first5min,300s
thereafter versus5s/1s/1s. Reported differences are+1.1% to−1.8% for insulated
steel and−21.3% to+8.9% for uninsulated steel; smaller increments were selected
for the latter. This is reported time-step sensitivity of a different steel
calculation, not validation of concrete depth resolution or historical use.
No underlying time series was acquired or recomputed. Printed145 gives a
double-UPN100 simplification applied to larger sections. Printed136 begins a
Standard/Explicit comparison whose remaining results are outside the roster;
I make no conclusion about that full comparison.

Printed171–176 reiterates model-based failure/survival conclusions but also
acknowledges that a fully forensic reconstruction is impractical and that the
actual upper support condition is unclear. Additional tensile/damage/3D and
localized-fire work is proposed. These qualifications limit historical
identification; a proposed future check cannot be counted as completed.

## Scope disposition and next evidence

The later thesis supplies materially more method and sensitivity evidence than
the2007 draft. It does not resolve that draft's ambiguous depth calculation
within this77-page review. Completed model execution, solver convergence,
mesh sensitivity, discretization convergence and physical/historical validation
remain distinct. Four published mesh counts with two incomplete runs cannot
justify a blanket claim of numerical inaccuracy either; the actual error
remains unquantified.

Most discriminating missing artifacts are the original penetration worksheet
and boundary/threshold definition; the named Table5.7 native case pairs and
logs/output histories; and a matched refinement series using the final
corrected properties and explicitly varied depth temperature resolution.
The source names files but their presence/executability is not established.
No WTC7 temperature, cause, actor or probability is inferred. No independent
new historical witness is supplied by another publication from this author
and research lineage. Original prior studies remain unchanged.

An incidental printed steel-strength/unit issue on printed92 is outside this
bounded benchmark audit; no model-error finding is made from that prose alone.
AppendixA, complete native inputs and the remainder of the thesis have not
been inspected. They are limitations, not silently reconstructed parameters.
