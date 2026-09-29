# Original Thompson measurements: independent inference review

Research only; independent agent source/inference review, not a professional
engineering certification, raw-data replication or historical WTC7 validation.
Only this research note and temporary page renders were authored. No source
PDF, model input, other review, main/legal file or canonical record was changed.

## Independent extraction freeze

Frozen September 13, 2026 UTC, before reading the other source agent's new
review, root's original-table statistics or messages giving specific new
findings. The assignment supplied the priority pages and general warning that
there were problematic tests and formulas, not a blind anomaly search. Earlier
TN1749 reading is known context and is not claimed as new independent evidence.
No group statistics, numeric model deviations, digitized curves or replacement
historical laws have been calculated in this review.

Controls read in full: current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`;
unit `PROTOCOL.md` SHA-256
`a06f1bc8f7e4283dbca0c9f54337eba0123045538ca47b411eb3aa8c260d637d`;
`ARITHMETIC-PROTOCOL.md` SHA-256
`88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e`.
Evidence-falsification, source-of-truth and PDF-review skills apply.

Original technical source: acquired Thompson2009 thesis,
`sources/MSST_Thompson_2009-sirsi.pdf`, SHA-256
`b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78`.
Full-page views in this pass: physical PDF68,70-78,95-107, with the same printed
page numbers on these pages (23 pages). Captions, notes and tables included.
PDF183, the approval/signature page, was neither rendered, displayed, searched
nor used. Bounded auxiliary discovery searched only technical PDF50-75 for
instrument/load terminology. No protection marking was observed on the selected
technical pages; that is not blanket clearance of other pages or attachments.

New full-page renders are `/private/tmp/thompson-inference.FTRSDo/p<page>.png`.
TN1749 PDF46 / printed28 was also freshly rendered and viewed in full as
`/private/tmp/thompson-inference.FTRSDo/tn1749-p46.png`, supplementing previously
viewed TN1749 PDF41-45. TN1749 source SHA-256 remains
`5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf`.
No original-data claim in this note is based on TN1749 alone when the selected
thesis pages give the original evidence.

## Central finding: the tables estimate different quantities

The thesis supplies physically informative original measurements and failure
observations. But “original experiment,” “original printed table” and “raw
time history” are not synonyms. It explicitly derives and averages quantities
before tabulation. A reproducible average of the wrong observable would not
verify TN1749's ultimate-load comparison.

| Source table | Actual field/selection meaning | Valid comparison ceiling |
|---|---|---|
| Thompson Table4.1, PDF103 | Approximate maximum **moment**, with corresponding applied shear, axial force and beam-end rotation. Values are sampled averages between extremes in moment, using a range selected from the controlling connection and applied to the opposing connection. Eighteen L/R specimen rows represent nine test executions. | Do not treat these as nine or eighteen instantaneous ultimate vertical-load records. Associated shear and rotation are at the moment-selected averaging interval, not necessarily at maximum vertical load. |
| Thompson Table4.2, PDF104 | Initial failure: one controlling connection specimen per test, with shear, moment, axial force, rotation and failure mechanism. Nine rows. | A candidate first-failure dataset. It is not automatically the maximum load over the entire test. |
| Thompson Table4.3, PDF105 | Secondary failure quantities. Nine test rows are retained, but only four have numeric secondary-failure results; other rows have different stated reasons for absence. | Must not fill absent secondary events with zero, infer that each test was loaded until total loss, or average only recorded secondary events as though this were the full group. |
| TN1749 Table3-3, PDF46 | Mean ultimate **vertical load** of a two-span assembly; detailed/reduced model predictions, deviations and experimental COV. Three connection-size rows. | Requires a declared assembly-load definition, event/peak selector, inclusion set and variability convention. It is not labeled mean maximum moment or mean first-failure load. |
| TN1749 Table3-4, PDF46 | Mean rotation **at ultimate load**, in radians, with both model predictions and COV. | Requires the same peak-event selection as the load and a reconciled rotation geometry. Rotation at maximum moment or at first failure is not automatically interchangeable. |

The strongest permissible comparison using Tables4.2/4.3 is a named diagnostic
that selects the larger **tabulated** first/secondary shear where both exist,
keeps first-failure values where no later value was recorded, and retains each
missing-event reason. That would test compatibility of candidate summaries,
not establish NIST's actual peak selection or recover unobserved later peaks.
Table4.1 should remain a separately labeled maximum-moment comparison and should
not be substituted because it happens to give closer numerical agreement.

## Measurement and estimator chain

### Instrument observations versus derived forces

PDF70-73 describes two load cells measuring applied force, two draw-wire
transducers on the interior-column flanges, and eight beam strain gauges.
Load cells were reportedly checked against a separate laboratory apparatus
within100 lb /0.1% of rated capacity; DWTs within0.01in; the strain gauges were
checked for120-ohm resistance. These are positive reported instrumentation
checks, but resistance continuity is not by itself a full strain-channel
calibration, and rated-capacity accuracy is not a constant relative error at
every test load. The actual calibration records are not reproduced here.

PDF75-78 derives axial force and moment from strain-gauge data using assumed
linear-elastic stress conversion, cross-sectional area10.3in², second moment
510in⁴ and equal-distance gauges on opposite sides of the neutral axis. It
reports erroneous left gauge1/right gauge6 data and instead uses left2/3 and
right5/8. The final expressions use stress differences for moment and the
sum for axial force. Moment is then extrapolated to the bolt line with a
triangular moment distribution and the outer true pin as zero moment.

Thus the plotted “measured” moment and axial forces are experimentally based
but analytically derived. They depend on gauge health, elastic stress/section
assumptions, geometry and the zero-moment boundary. They are not direct bolt
force transducers. The source's “flexural force” in kip-inches is a moment,
not a force to be numerically compared with a kN vertical load.

PDF103 adds a second estimator: sampled averaging between moment extremes.
The selected interval for the controlling side is applied to the opposing side.
The two rows in a test therefore share a time-window selection and assembly,
not two independent experimental executions. The duplicate applied-shear values
in those rows are not independent observations to be counted twice.

### Applied shear versus total assembly load remains a mapping question

PDF68/71 describes two load cells in a common hydraulic-cylinder reaction
assembly. PDF106 says the sum of the two beams' vertical reactions is compared
with measured applied vertical shear. Table4.4 on PDF107 nevertheless gives a
repeated applied-load entry on its left/right rows and one error per test.
The selected pages do not explicitly spell out whether the Tables4.1-4.3
“applied shear” is a per-side share, an averaged cell reading or a total
assembly load using another normalization.

It is mechanically necessary to distinguish per-beam shear from the total
load applied to the common central column; TN1749 labels its ordinate as the
assembly load. A factor-of-two reconciliation may be a useful candidate test
if supported by the measured channel combination and symmetry convention.
It must not be chosen solely because it reproduces TN1749's means. The
load-cell reduction, original histories or a precise definition are the
stronger bridge. Static equilibrium also includes axial force resolved along
the deformed beam, so moment divided by a nominal length is not a complete
substitute for the applied vertical load in the catenary stage.

### Rotation definition and printed equations

PDF78 supplies three different geometric distances:36.875in to the strain
gauge,74.625in to the bolt line, and78.375in to the column-flange face. It says
beam-end rotation is derived from the DWT vertical displacement and the
flange-face distance. TN1749 instead describes its chord convention between
bolt centers. Changing length definition is not a material ductility change.

Equation34 as printed is `theta = arctan(x_f / Delta)`, while the text defines
`x_f` as horizontal distance and `Delta` as vertical deflection. That ratio
approaches a right angle rather than zero for an initially horizontal beam as
deflection approaches zero; it conflicts with the plotted small rotations
starting near zero. The ordinary rotation-from-horizontal expression has the
opposite ratio. This is a genuine **printed formula/definition inconsistency**;
it does not prove the actual data-processing program used the printed ratio.
An exact source-to-source angular conversion cannot be authenticated without
resolving the implemented convention. A simple nominal-length multiplier is
at most a separately identified approximation, not an exact arctangent identity.

Equation23 on PDF75 also uses unusual microstrain notation, labeling the
measured quantity with a negative-six exponent while printing a positive-six
multiplier. If the input is a numerical value in microstrain, the usual
micro-to-unit-strain conversion must be made in the opposite direction.
The raw-number/unit encoding is not supplied here; preserve the notation and
request the actual reduction implementation before asserting a gross scaling
error in the published force histories.

## Problems and missing records: separate their consequences

1. **5ST1, PDF95-97.** The original explicitly reports reversed hydraulic
   couplings limiting pump output, interruption, corrected hoses and restarting
   data collection near the maximum flexural-capacity region. Data before
   approximately0.06rad were neglected. Later failure observations and values
   are still recorded. This is not a wholly nonexistent test, but its history
   is not exchangeable with uninterrupted tests without qualification. TN1749's
   omission of its initial curve has an original-source explanation, not
   affirmative evidence of concealment. Inclusion in a later summary still
   needs its own explicit membership check.
2. **3STL3, PDF106-107.** The thesis reports severe unexplained spikes and a
   27.50% statics-verification error for test3ST3. It questions left-specimen
   data and excludes that specimen from later thesis evaluation, while noting
   that the controlling failure was isolated to right specimen3STR3. That is
   not an instruction to discard the entire test or all its load data, nor
   permission to average both axial channels without checking their quality.
3. **Gauge substitutions, PDF76.** Specific channels were replaced because
   their collected data were erroneous. This disclosed filtering needs raw
   channel and reduction provenance; its disclosure is contrary evidence to
   a blanket claim that problems were hidden.
4. **Secondary-event absence, Table4.3.** A secondary failure was not attained
   in several rows;4ST2 specifically was not loaded to a secondary failure.
   No later recorded load is therefore not proof that no later capacity was
   physically possible. The generic footnote for three-bolt rows cites initial
   tension rupture, although Table4.2 labels3ST1 bolt-shear rupture. Preserve
   that local labeling inconsistency rather than silently overwriting the
   explicit initial-failure classification.
5. **Statics-check ceiling, PDF105-107.** The report conducts the check in a
   selected linear force-rotation state. Most tabulated errors are below4%,
   but5ST1 is not evaluated and3ST3 is the reported exception. This is useful
   partial instrumentation/model consistency evidence, not validation of the
   complete nonlinear history, every failure event or all nine tests.

No percentage above was recomputed here; these are source statements/table
transcriptions with their conditions. Raw histories remain distinct from the
thesis's selected and processed curves and tables.

## Physical meaning, strongest counterevidence and transfer limit

The original photographs, described failure mechanisms and load histories are
stronger evidence than a solver-to-solver comparison alone. PDF95-105 documents
localized block shear, tension rupture and bolt-shear rupture, with some
connections continuing to transfer load after initial damage. In several
four/five-bolt cases, additional catenary action and later failure allow
continued or recovered load carrying. Other cases fail without an attained
secondary stage. These observations support taking residual resistance,
failure mode and load-path transition seriously rather than using a universal
single abrupt deletion law without testing it.

They also contradict the converse universal premise that a bolted connection
must always retain enough support to prevent rapid failure: the experiments
include sharp force drops and ultimate connection loss. Neither observation
quantifies the support-loss coordination or speed in an entire building.
Reported broad similarities and experimental variability must remain alongside
TN1749's mismatch of particular failure modes and peak-event ordering.

PDF74 says loading was slow, manually incremented at the operator's discretion;
the pump could not hold a steady force or impose automatic preset increments.
The failure endpoint was a force drop with visual confirmation. This is not
a demonstrated sudden-column-removal dynamic experiment. The selected technical
pages do not report a physical test temperature. No temperature is inferred
from indoor photographs, and TN1749's numerical bolt cooling remains a separate
preload device, not a fire exposure.

This thesis can strengthen the physical provenance of the later comparison and
expose concrete estimator/selection issues. It does not by itself authenticate
NIST's 2008 fin law, map a released WTC7 material card, establish performance
under combined thermal/dynamic loading or decide between historical collapse
causes. A useful next discriminating record is the original load-cell/DWT/strain
history with channel/reduction definitions and TN1749's exact table membership
and peak selectors. Agreement or disagreement of rounded summaries cannot
recover those records by itself.

## Pause / integrity closeout

The independent extraction above is complete for the assigned selected pages.
The parent then instructed a pause following the user's notice of additional
supplementary-response files. No further inquiry was opened: the other source
agent's new review and root's numerical outputs remain unread here, no original
statistics were calculated, and the newly flagged production was not inspected
by this reviewer. The final local edits only clarified wording in this owned
note. Original-source and protocol hashes were checked again at closeout; the
source PDF and excluded PDF183 remain unchanged and outside any further use.
