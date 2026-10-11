# Separate thesis reader: initial frozen notes

October 8, 2026. Research-only reading under the current protocol and its one
prospective expansion. Reader: the `admission_method_review` AI subagent.
These notes were composed before reading root's notes or exchanging scientific
findings. Root reported freezing its own notes while this reading remained in
progress; that notification contained no scientific findings.

This is a separate, prior-informed interpretation of a shared source, not a
blind review, human review, qualified engineering assessment, independent
historical witness, native-model reproduction or physical validation. The
earlier Windsor draft audit and its open question were known beforehand.

## Source and actual inspection

Original: Ian A. Fletcher, *Tall Concrete Buildings Subjected to Vertically
Moving Fires: A Case Study Approach*, title page dated May 2009. The title page
identifies a University of Edinburgh PhD thesis. Physical page 34, printed 8,
lists the Santander workshop paper, FiB 2007 paper and SiF 2008 paper separately.
This establishes the author's stated publication relationship, not identical
texts or an explicit correction of the held 2007 draft. The catalogue's
`subject` versus the PDF title's `Subjected` remains a bibliographic variation.
I did not independently authenticate authorship beyond this source attribution
or repeat the institutional acquisition.

I inspected **all 77 complete frozen pages**, including headings, body text,
equations, tables, plots, captions, footers and intentionally blank pages:

| Physical PDF pages, one-based | Printed labels | Coverage |
| --- | --- | --- |
| 1 | Title | Complete page |
| 11–15 | xi–xv | Complete contents |
| 33–34 | 7–8 | Contributions and publications |
| 81–94 | 55–68 | Complete research-method chapter |
| 114–138 | 88–112 | Structural/material/thermal setup and sensitivities through mesh |
| 139–152 | 113–126 | Sole prospective expansion: remaining Chapter 5 sensitivities |
| 153–154 | 127–128 | Chapter 5 conclusions, including blank page |
| 161–162 | 135–136 | Sole expansion: full-scale material choices and relation setup |
| 166–171 | 140–145 | Full-scale heat-transfer section |
| 197–202 | 171–176 | Conclusions and further work |

Full-page 110dpi PNGs were actually displayed with `view_image`, not merely
generated. The first 28 inspected pages (1, 11–15, 33–34, 81–94, 114–119) were
viewed from `/private/tmp/windsor-thesis.mXK0Gu/`; the remaining pages were
viewed from this directory's `render/`. An attempted grouped display of
120–124 was truncated by the tool's context limit and was **not** counted;
120–124 were subsequently reopened in successful smaller calls. All temporary
and preserved PNG pairs were then byte-compared successfully. Printed body
pagination on the inspected pages agrees with physical position minus 26.

No additional PDF pages, root notes, new source acquisition, model execution,
graph digitization or numerical reconstruction were used. The page-selection
document's extracted-text locators assisted orientation; full-page visuals
controlled interpretation. The old draft report was reread as the preserved
comparison claim, not substituted for the new source. No supplied equation
needed numerical recomputation to decide this bounded question, so none was
performed.

## Six protocol fields

### 1. Depth quantity and threshold

The inspected thesis sections do **not** supply a defining temperature
threshold, penetration equation or matched-case correction connecting the
draft's 50.3mm at 3600s and approximately 58mm at 1400s. General discussion of
penetration on printed 58 and 62 (physical 84 and 88) establishes a modelling
aim, not a quantitative criterion.

The literal 50.3 located on physical 119 is **50.3mm² of top reinforcement
area**, Table 5.1, printed 93. It is not a thermal depth. The physical 169
locator for `1400` falls on a plot whose time-axis labels include 14000s; the
page concerns steel timestep sensitivity, not a 58mm concrete penetration
event. These numerical substring matches provide no reconciliation.

The scope-bounded outcome is **unresolved depth definition / different
analysis**, not a proved correction and not a newly reproduced comparable
contradiction in the thesis. The earlier draft's conditional same-depth
ordering problem remains attached to that source only. An uninspected
appendix, original worksheet or explicit author clarification could still
change the disposition; this is not a thesis-wide absence claim.

### 2. Time origin and thermal boundary

Printed 61 (physical 87) describes an ISO-based heating curve followed by one
hour of linear cooling. Printed 103–105 (129–131), Table 5.5 and Figure 5.30,
specify delayed application to the beam's top and bottom: for example, the
15-minute upward case applies the bottom fire at zero and the top at 15min.
The heat-transfer analyses use a 100-hour duration to allow core cooling.
Printed 100 (126) describes external temperature inputs, represented by both
radiative and convective films on the shell's top and bottom, rather than
directly imposed external heat-flux histories. The exact film coefficients
are not established by this bounded reading.

Printed 113 (139), Tables 5.8–5.9, distinguishes a baseline total fire duration
of 120min and peak temperature of 945°C from ±10% duration/temperature cases.
These are model scenarios, not measured histories establishing a draft
penetration time origin. Printed 127 and 135 (153 and 161) retain the
one-hour heating plus one-hour cooling scenario and explain its selection.

Printed 140 (166) supplies explicit full-scale sequence origins: in the
30-minute downward case, the fire on top of floor 16 begins at zero, while
that beneath floor 5 begins at 21600s. Nodal thermal output is automatically
scaled to the stress-analysis duration, whereas manually supplied steel
temperature histories require matching the Explicit time-scaling manually
(printed 145 / physical 171). Printed 105 warns of stretched/compressed
thermal histories if Standard thermal and stress durations differ. These are
important mapping conventions; none identifies the draft's missing depth
definition.

### 3. Material properties

Printed 88–92 (114–118) explains uncertain historical material details,
Eurocode temperature-dependent properties and idealizations. Most initial
sensitivities use calcareous concrete despite post-fire indications favouring
siliceous aggregate. Final multiple-floor models use siliceous concrete as
the closer stated analogue (printed 122 and 135 / physical 148 and 161).
Printed 108–110 (134–136) varies moisture between 0%, 1.5% and 3%, chooses
1.5%, and specifies the upper Eurocode conductivity bound. Moisture acts
through effective heat capacity; spalling is expressly not modelled.

The mesh comparison is specifically stated to use calcareous concrete, 1.5%
moisture and 15-minute upward fire spread (printed 110 / physical 136). It
must not be silently relabelled as a final siliceous full-structure validation.
The inspected thesis does not give a matched reuse or explicit correction of
the draft's constant conductivity/density/heat-capacity penetration arithmetic.

Material/implementation caveats are substantive, not incidental:

- Printed 118–119 (144–145), Tables 5.11–5.13: initial CDP values may have
  been unphysical; recommended values were adopted, with a tabulated response
  comparison, but prior sensitivities were not all rerun.
- Printed 119–122 (145–148): initial concrete tensile capacity is constant
  1.5N/mm² with ductile post-yield behaviour. More realistic descending tensile
  models did not converge; later siliceous floor modelling retains a
  0.9N/mm² floor because greater reductions caused numerical instability.
- Printed 122–126 (148–152): expansion coefficients had been supplied in the
  wrong form. Corrected values produce changed tabulated responses and allow
  a previously unsuccessful siliceous beam run to complete. Earlier mesh,
  moisture, delay and duration sensitivities were not rerun. The author also
  identifies artificially low corrected coefficients at 20°C and resulting
  20–100°C expansion error as further work.

These observations do not prove the executable results are false. They limit
transfer of an earlier mesh-sensitivity result across changed constitutive
inputs and show why solver completion is not itself physical validation.

### 4. Section and exposure geometry

Printed 90–92 (116–118), Figures 5.20–5.22: a 5.2m span, 100mm-wide,
230mm-deep rectangular rib representation includes a 30mm screed directly
above the rib; the rib is not treated as a full T-section. Bottom and top
reinforcement and cover are specified, with top cover less certain. Clay
formwork is simplified: side insulation is omitted and bottom material is
treated as concrete. The initial simply supported beam is distinct from the
restrained floor model. Printed 94–96 (120–122) combines three ribs into a
0.3m-wide representation and scales loads; lateral slab redistribution is
not fully represented.

Printed 99–100 (125–126), Figure 5.28, argues that cover plus side clay
insulation makes one-dimensional through-depth heat transfer adequate for
reinforcement temperature. The schematic is an explanatory comparison, not a
reported numerical 1D-versus-2D error test. The shell formulation cannot admit
edge heat transfer in this setup; full 3D heat transfer would require a
different element representation. That distinguishes it from a fully resolved
multisided concrete temperature field.

Full-scale steel calculations are separate: printed 142–145 (168–171)
neglect vertical and cross-sectional temperature variation, use all-side
exposure, assume 50mm Vermiculux with conductivity 0.13W/mK for insulated
members, and apply temperatures calculated for two UPN100 sections to the
larger column sections as a stated simplification. Neither steel timestep
agreement nor these geometry assumptions test the draft's concrete-depth
benchmark.

### 5. Mesh and section-temperature representation

Printed 92 (118) describes shell capability for up to 19 through-depth
temperature definition points. Printed 100 (126) pairs DS4 thermal shells
with S4R stress shells, preserving nodal locations and equal counts of
temperature points by copying the model and changing analysis/element types.
Figures 5.30 and 5.33, printed 105 and 107 (131 and 133), identify bottom,
middle and top temperature outputs. Capability and output labels alone do
not establish the precise depth-node placement used in every source run.

Printed 110–113 (136–139) gives **20, 40, 160 and 480 elements** and named
thermal/stress input files. Those total element-count changes are not an
explicit refinement series of through-thickness section-temperature points.
The source does not establish, in these inspected pages, that the earlier
five-node/230mm depth representation was refined or its penetration error
bounded. No input deck or temperature profile was recovered or executed here.

### 6. Controlled convergence and error evidence

There is genuine **reported performed numerical comparison**, not merely a
mesh-independence assertion. Table 5.7 and Figures 5.36–5.37 (printed
111–112 / physical 137–138) identify four element counts and compare maximum
reinforcement plastic strains and vertical displacement under the stated
common scenario. Ignoring this would unfairly dismiss relevant later evidence.

Its limitations prevent promotion to a demonstrated general convergence
bound:

- The 160- and 480-element analyses stopped after 24.7 and 23.3 hours;
  the stated thermal analysis lasts 100 hours. The author attributes the
  incomplete runs to an unknown numerical instability, not confirmed collapse.
- The prose says final results were comparable to coarser meshes at similar
  times, but supplies no common-time tabulation, exact difference norm,
  tolerance, observed order or extrapolated limit. The displayed maxima are
  not documented as a complete common-duration comparison for all four meshes.
- Deflection varies non-monotonically. Figure 5.36 also shows that the
  response to refinement differs by strain component; describing everything
  as negligible requires an explicit quantity-specific criterion, not merely
  the author's overall judgement. I have not digitized values or invented a
  numerical tolerance.
- This is structural-response mesh sensitivity for one simplified scenario,
  not direct concrete-temperature/depth convergence or independent physical
  error measurement. Later CDP, tensile and expansion choices differ; the
  earlier sensitivity series was not comprehensively repeated under them.

The source concludes mesh effects are negligible on printed 113 and 127
(139 and 153). The bounded disposition is **limited performed mesh
sensitivity, with incomplete refinements and no demonstrated concrete-depth
convergence/error bound**. It would be inaccurate to say the thesis provides
no numerical comparison, and equally inaccurate to treat its conclusion as
validation of the 2007 penetration criterion.

There is also a separate, stronger-in-specificity **steel timestep
sensitivity** comparison. Printed 142–144 (168–170), Table 6.3 and Figures
6.5–6.6, distinguish large steps (300s before ignition, 60s during the first
5min, 300s thereafter) from small steps (5s before ignition, 1s thereafter).
Reported relative variations are +1.1% to −1.8% for insulated steel and
−21.3% to +8.9% for uninsulated steel. Large steps were retained for the
former and small for the latter. These are source-reported comparisons, not
independently reproduced errors. Only two timestep schemes are shown; the
small-step solution is not an independently demonstrated exact solution.
This does not validate concrete shell-depth discretization.

## Contrary evidence, attribution and remaining discriminator

The thesis openly reports an Abaqus v6.7-1 heat-transfer error producing
higher internal temperatures, then reruns the 15-minute upward case with
v6.8-1 (printed 107–108 / physical 133–134; compare Figures 5.30 and 5.33).
Other spread cases were not rerun because the author regarded the earlier
condition as more severe. That disclosure is important contrary evidence to
an account of an unchanged, unquestioned analysis, but it does **not** say
that the draft's two penetration numbers arose from that software problem.
The stress-solver correctness claim is the author's assertion, not independently
tested here. One corrected case cannot establish unchanged ranking of every
unrerun case without an additional justification.

Likewise, printed 102–103 (128–129) compares a proof-of-concept model's
0.036m midpoint displacement with a simple elastic calculation's 0.02m and
accepts the order of magnitude. The author explains the different elastic
assumption. This is a rough reasonableness check, not mesh convergence or a
matched physical validation. Solver convergence language on printed 64,
117–121 and 140 (90, 143–147 and 166) must not be conflated with refinement
convergence.

Printed 171–174 (197–200) states broader fire/structural conclusions and
claims a ninth-floor deformation agreement with observations. These are
retained as source claims, not independently accepted collapse findings.
Printed 175–176 (201–202) expressly says the real structure's matching
behaviour cannot be verified with certainty because the top support condition
is unclear, calls for better tensile/damage modelling and fuller 3D load
redistribution, and identifies further thermal/loading scenarios. Together
with the explicit Windsor-Tower-like scope at printed 68 and 171 (94 and
197), these qualify transfer to historical causation, still more to WTC7.

The finite answer therefore has two parts: the thesis does not resolve the
draft's undefined same-depth benchmark within the inspected scope; it does
add actual, limited numerical sensitivity evidence that must be credited
without being mistaken for the missing thermal-depth convergence test. The
strongest objection to a negative reading is precisely the existence of those
performed mesh and timestep comparisons. The strongest objection to a broad
positive reading is their distinct estimands, incomplete mesh runs and
changed material/implementation choices.

A direct discriminator remains the draft's actual penetration definition,
boundary history and worksheet, or an explicit matched-case correction.
For thermal-mesh adequacy it would be native section-temperature definitions
and common-input, common-time temperature/response refinement results with
declared error criteria, particularly under the final constitutive inputs.
Neither is manufactured here. No misconduct, Windsor/WTC7 cause ranking,
legal promotion or accepted-engine state follows from these notes.

## Pins and performed checks

SHA256 values checked from the working directory containing this note:

| File | SHA256 |
| --- | --- |
| `fletcher-2009-thesis.pdf` | `4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543` |
| `PROTOCOL.md` | `5b786ff3cf50cff9e6b3424deeda49e0aa199e416942da845fd49d6255b67077` |
| `PAGE-SELECTION.md` | `34de8c9f8b7e2dfc78ff9cfcfeec73087bffd27b21876dd8b32f2b6bfa64e25a` |
| `SCOPE-EXPANSION.md` | `50ee750453e44ffd33b7453f814e4fcc4d54d3dcf0440bfb93849c04c815b8d8` |
| `render/render-receipts.json` | `6acb40e9f8e2148dedc0da5d57677f31c8a0048bd254669722e661c36f6373c3` |
| `render/title-render-receipt.json` | `7cd88e6d329228f3ca23ab3c2b42d708e71f6560239c18e8e9de01eac6a7607f` |
| `render/expansion-render-receipts.json` | `9366f737499b0e298b51b7c0be181f37ab9530192d4f185816700591512c784c` |
| `../windsor-thermal-check/report.md` | `7bb811eeecd4281db0015831dde4fed02f0f44f56551980fcba574761d072489` |
| `../windsor-2008-version/execution.md` | `97c6c0357f61ff9239767e7be7c1c461f94a6f7a899802b1031dee385c475cc7` |

Actual read-only shell checks, all completing without assertion failure:

```sh
shasum -a 256 fletcher-2009-thesis.pdf PROTOCOL.md PAGE-SELECTION.md SCOPE-EXPANSION.md render/render-receipts.json
for render_page in render/page-*.png; do cmp "$render_page" "/private/tmp/windsor-thesis.mXK0Gu/${render_page##*/}" || exit 1; done
printf '%s\n' render/page-*.png | wc -l
shasum -a 256 render/page-*.png | shasum -a 256
shasum -a 256 render/title-render-receipt.json render/expansion-render-receipts.json
shasum -a 256 ../windsor-thermal-check/report.md ../windsor-2008-version/execution.md
test ! -e observer-notes.md
```

The image count was 77; the aggregate digest of the relative-path hash lines
from the displayed command was
`559baefe498691663227b334c7157e56e72b18c23cb60954a5deb7713fe13a59`.
`cmp` produced no mismatches. These establish retained byte identity, not an
independent rerender or a guarantee of rendering correctness. Renderer
receipts were read as provenance data; the separate expansion receipts report
zero diagnostics, while the title receipt explicitly limits its diagnostic
capture to combined terminal output. Failed earlier rendering is not erased.

Only this note was created by this reader, using `apply_patch` after the
nonexistence check. No other files were edited. No hypothesis-testing
calculation, model run or external action was performed.
