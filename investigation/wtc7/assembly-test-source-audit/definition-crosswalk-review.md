# Original-to-retrospective load and rotation definitions

Research-only independent source-definition review, frozen September 13, 2026
UTC. This is a bounded follow-up to `original-inference-review.md`, not a revision
of it, an independent experiment, professional engineering certification, or a
reproduction of raw measurements. No root/other-agent numerical arrays, candidate
statistics or numerical results were read. No original candidate calculations,
digitization, solver execution, outreach or new-production inspection was done.

## Result and interpretation ceiling

TN1749 explicitly defines a **total center load** and a **beam-chord rotation**.
The original thesis explicitly locates its load cells and rotation reference
lengths, but the selected original methodology does **not** authenticate a
factor-of-two conversion from its printed `V_app` to TN1749's `P`. Indeed, the
literal original statics prose compares the **sum** of the two beam reactions
with `V_app`; this favors an assembly-total reading, not an express half-load
definition. It must remain beside any subsequently proposed numerical
reconciliation, not be discarded because another interpretation fits a mean.

A change from column-face distance to bolt-center chord is source-supported.
An exact implemented angular conversion is not established: the original's
printed arctangent ratio is inverted relative to its stated variables and
rotation-from-horizontal interpretation. The separately held experimental data
are explicitly identified by the original's Appendix G. These are specific
definition/provenance gaps, not affirmative evidence of fabricated measurements
or a historical WTC7 cause.

## Controls, pins and independence

Read current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, the complete unit
protocols and the prior owned inference review. Evidence-falsification,
source-of-truth, PDF source-review and repo-orchestrator safeguards were applied.
The report is working research; no authority tier, legal position or canonical
fact was changed. Read-only repository intake confirmed the assigned
`research/sherlock-wtc7-investigation` branch; unrelated intake output was
suppressed. The assigned note and temporary renders are the only write targets.

| Preserved input | SHA-256 |
|---|---|
| `PROTOCOL.md` | `a06f1bc8f7e4283dbca0c9f54337eba0123045538ca47b411eb3aa8c260d637d` |
| `ARITHMETIC-PROTOCOL.md` | `88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e` |
| `sources/MSST_Thompson_2009-sirsi.pdf` | `b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78` |
| `../connection-calibration-audit/retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf` | `5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf` |
| Unchanged `original-inference-review.md` | `56867304c2be06f148dcc05c8486566412bb26a5afe1d4a4f95c8754a07f903d` |

Original references below are physical PDF pages and matching printed pages.
TN1749 physical41-47 are printed23-29. The later source is the preserved
July2012 report corrected February2013, not evidence of what the 2008 WTC7
investigation had already validated.

Full-page views in this resumed pass: original4-6,12-16,68-80,105-111,145,
160-161,179-182; TN1749 physical41-47. Previously frozen original103-104 and
95-107 readings supply table/event context; the new load/rotation conclusions
rest on the freshly viewed methods and definitions, not another agent's
transcription. The new view set contains 35 original pages and 7 TN pages.
Captions, axes, footnotes, continuation text and notation were included.

Original PDF183, the approval/signature page, was not rendered, displayed,
text-searched or used. Lexical discovery was restricted to original1-182 and
returned page numbers/allowlisted term matches. An additional load-cell/reduction
term co-occurrence search covered59-182 only; it is a discovery aid, not proof
that no definition could exist elsewhere. No protection marking was observed
on selected technical pages; that is not blanket clearance of other material.

Renders: `/private/tmp/thompson-definitions.15hHF2/`, plus reused full-page
renders in `/private/tmp/thompson-inference.FTRSDo/` and
`/private/tmp/retrospective-tn1749.JTkzd4/`. Read/render tools were bundled
Python3.12.14, pypdf6.10.0 and Poppler26.05.0. No plot-derived coordinates or
values were produced. Physical quantities below are source transcriptions or
explicitly labeled symbolic deductions, not recomputed original statistics.

## 1. Total load, reaction components and the unresolved table channel

### What the original actually establishes

Original68, Figure3.9, places two load cells in the hydraulic-cylinder reaction
frame, one on each threaded support rod under a common upper plate. The cylinder
acts centrally. These are **not** depicted as separate instruments at the two
beam shear connections. Original69-70 traces the threaded ram connection to the
central column. Original70-71 says the cylinder supplies applied vertical shear
load and that two load cells measure applied force. Original145, AppendixC.3.1,
describes the upper plate's centered point load and its two rod supports in a
design calculation. That confirms the load-path geometry, not an experimental
channel-processing recipe or measured load history.

An idealized, tare-adjusted static balance of that reaction frame would relate
the **sum** of its two cell reactions to the ram force. Equal reactions would
make their mean one half of that sum. This is a mechanical deduction from the
diagram; the thesis pages do not say which combination was saved as `V_app`,
whether a cell average was subsequently doubled, how tare/self-weight was
handled, or whether a later table applied a per-connection normalization.
Equal frame-cell loads would not by themselves prove equal beam-connection
forces, particularly after asymmetric local damage.

Original105-106, Section4.4 and Figure4.34, independently make the beam-force
balance explicit. The reported expressions are:

```
R_T = M_M / L_SG                         (35)
R_y = R_A sin(theta) + R_T cos(theta)     (36)
```

The text identifies `R_y` as the vertical reaction for one side, then states that
the **summation of left and right vertical reactions** was compared with the
measured applied vertical shear `V_app`. The literal prose therefore supports
`V_app` as the assembly total in that check. Original107, Table4.4, repeats a
`V_app` entry on each L/R row and gives a single error per test; it does not
explicitly explain the repeated-entry normalization. Nomenclature12-16 defines
several force symbols and the side-specific reaction, but does not supply the
missing table/channel reduction formula for `V_app`.

Original108-111 and AppendixE160-161 apply the shear quantity to approximate
individual connection/bolt-force calculations at a selected maximum-moment
state. Their per-connection context is a legitimate reason to investigate a
per-side convention. It is not a replacement for a stated load-cell combination
or a resolution of Section4.4's assembly-sum wording. This review did not use
the printed row magnitudes or percentage errors to select among conventions.

### What TN1749 actually establishes

TN physical41/printed23, Figure3-18, labels a single concentrated force `P` at
the unsupported center column of a two-span assembly. Physical43/printed25,
Section3.3.3, names `P` the vertical load, distinguishes beam axial force `T`,
and says the experimental `T` is the **average** of the measured axial forces
in the two spans. This is an explicit axial-force averaging statement, **not**
a statement that `P` or the original `V_app` was averaged in the same way.
Figure3-21 on physical45 labels `P` in kN, `T` in kN and center displacement
`Delta` in mm. Physical46 Tables3-3/3-4 concern ultimate `P` and rotation at it.

TN physical47/printed29, Section3.4.1, explicitly writes the total applied
vertical load for its two-span model as:

```
P = 2 (T sin(theta) + V cos(theta))       (3.6, concentrated load)
```

For distributed load, the left side is `2wL`; that alternative is not the
concentrated-load experiment. `T` and `V` are axial and shear forces in the
beams at the pin supports. The section assumes connection-concentrated
deformation with effectively rigid beam spans. This is an explicit total-load
definition and equilibrium model; it is not disclosure of Thompson's LabView
reduction or a proof that the experimental halves were exactly symmetric.

### Permissible source-to-source statements

- **Directly established:** TN's `P` is the concentrated total center load;
  local beam shear `V` is a distinct quantity. Thompson's Section4.4 prose
  compares a sum of side reactions with `V_app`.
- **Derived, conditional:** in a symmetric state, a correctly defined global
  vertical side contribution is `P/2`. In a general state the two global
  contributions are added individually. They are not necessarily equal.
- **Not established:** all Thompson Tables4.1-4.3 shear entries equal `P/2`, or
  one cell reading, or the mean of the two cells. A factor-of-two candidate is
  testable, but not an authenticated source conversion in this review.
- **Incorrect shortcut:** double the local transverse shear alone throughout
  the catenary stage. Equation3.6 includes the axial force's vertical component.
  Likewise, `M/L` alone is not the complete assembly vertical load.

Thus a later numeric compatibility calculation should retain the literal
assembly-total reading and any separately declared half-load interpretation,
with the unresolved definition explicitly attached. Agreement cannot select
the historical convention without independent channel or processing evidence.

## 2. Rotation and geometric reference lengths

Original78 defines three different horizontal distances: `x_sg=36.875in` from
outer true pin to strain gauge; `x_b=74.625in` to the tested bolt line; and
`x_f=78.375in` to the center-column flange face. Original12-13 independently
defines the geometric roles. `x_sg` and `x_b` appear in the moment extrapolation
of Equation33. `x_f`, together with the DWT displacement, appears in the
rotation definition. They must not be interchanged because all are lengths.

TN physical41 footnote4 defines beam chord `L` as the **horizontal distance
between bolt centerlines**; ordinary span length, by contrast, is between
column centerlines. Figure3-18 supplies `L=1.89m (6.21ft)` for each half.
Physical44 explicitly says its reported rotations are about5% greater than
Thompson's because it uses the bolt-center length1.89m while Thompson used
1.99m (6.53ft) from exterior pin to center-column face. The paragraph calls
these span lengths, but the locations and the preceding chord footnote remove
the relevant geometric ambiguity. The original's `x_b` and `x_f` identify
those two different locations independently of any fitted numeric comparison.
The rounded metric values do not establish an exact unrounded historical input.

TN physical47 gives:

```
theta_N = atan(Delta / L)                (3.7)
```

Original78 Equation34 instead prints `theta_T = atan(x_f / Delta)`, while
identifying `x_f` as horizontal distance and `Delta` as vertical displacement.
That printed ratio approaches a right angle rather than zero as the initial
horizontal configuration is approached. It is inconsistent with the stated
rotation-from-horizontal geometry and displayed small rotations. The defect
is in the **printed equation/definition pair**. No original program, processed
data formula or erratum has been inspected that establishes what was executed.

If, and only if, the actual original rotation used the ordinary horizontal
reference expression `theta_T=atan(Delta/x_f)` for the same displacement and
event, symbolic substitution would give:

```
theta_N = atan((x_f / L) * tan(theta_T))
```

This is a conditional geometric identity derived here, **not** a transcription
of an original-to-TN implementation. Multiplying an angle by a nominal length
ratio is only a small-angle approximation to it. TN's approximate5% description
is not an exact universal angular multiplier. If the two DWT channels capture
different flange motions or are averaged differently, equal event/displacement
also needs verification. No candidate angular values were calculated here.

## 3. What original data and summaries are actually located

The original contents pages4-6 locate experimental acquisition/procedure70-74,
data analysis75-78, individual test narratives/plots79-102, summaries103-104,
statics105 and bolt analysis108. They distinguish appendices for design,
apparatus drawings, bolt-force calculations, limit-state calculations and
experimental data. This is navigation evidence, not a full line-by-line review
of every appendix.

- Original71-72 describes two load-cell channels, two DWTs and eight strain
  gauges acquired with a12-bit DAQ and LabView. Original75-78 works with
  time-indexed strain and displacement measurements and derives forces and
  rotations. These statements establish that channel histories underlie the
  results, not that complete histories are reproduced in the PDF.
- Original103 Table4.1 is the approximate maximum-**moment** sampled summary
  explained in the unchanged prior review. Original104-105 Tables4.2/4.3 are
  initial/secondary failure summaries, not a full sampled load-displacement
  history or an explicit universal ultimate-load selector.
- Original160, AppendixE, says the bolt-force analysis uses data at the
  specimens' approximate maximum moment. Its representative page161 contains
  calculation inputs/outputs, not a raw channel time series. Original179-181,
  AppendixF, supplies approximate limit-state capacity calculations for
  comparison with experiments, not additional raw measurements.
- **Original182, AppendixG, says the experimental data are available upon
  request and directs the reader to the MSOE campus library for access
  information.** The page is a retrieval statement, not the data themselves.
  It does not establish present-day availability, file formats, custodial
  completeness, calibration files or exactly which channel histories would
  be supplied. No request or external contact was made.

A bounded PDF-structure check found no catalog `/EmbeddedFiles` tree and zero
`/FileAttachment` annotations on original pages1-182. No attachment streams
were read or extracted. This supports only the absence of those standard
attachment mechanisms in the inspected scope, not a guarantee that every
possible hidden/linked representation is absent. PDF183 was not used.

The missing experimental bridge is specific: synchronized raw load-cell,
DWT and strain channels; channel-to-quantity names, signs, calibration, tare
and combination formulas; the actual rotation/microstrain reduction; data
selection/repair and event timestamps. The missing retrospective bridge is
the exact source histories supplied to TN1749, selected test membership,
peak/event definition, rotation recomputation, precision/rounding and SD/COV
convention. None is recoverable uniquely from a matching rounded group mean.

Missing portions/events must keep their original distinctions: 5ST1's
interrupted initial record is not a wholly nonexistent experiment; the
questioned 3STL3 channel is not automatically all of test3ST3; an unattempted
secondary failure is not zero remaining capacity. These limits were already
source-frozen in the unchanged original review, not inferred from new results.

## Strongest counterevidence and next discriminating record

The original provides a tangible apparatus, instrumentation checks, visible
failure observations, derived histories and disclosed data problems. TN1749
openly identifies different rotation lengths, experimental variability,
different failure modes, a missing plotted history and peak-order differences.
Those disclosures matter against an unsupported suggestion that every
discrepancy was concealed. Conversely, source disclosure and plausible
mechanics do not close an unexplained numeric/channel mapping or establish
that a later comparison was an unused prediction.

The highest-value source retrieval is the AppendixG experimental dataset with
its acquisition/reduction definitions, paired with TN1749's actual comparison
inputs and selectors. This note records that lead only. It does not authorize
contact, export or new private-source use. No collapse-mechanism ranking or
historical guilt/innocence conclusion follows from this bounded check.
