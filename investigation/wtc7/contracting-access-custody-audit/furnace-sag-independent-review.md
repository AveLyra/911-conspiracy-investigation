# Furnace-sag claim: separately authored source review

2026-09-28. Research only. Source observations frozen before reading root's
new synthesis. This is an AI source-critical review, not a blinded experiment,
licensed engineering opinion, new measurement, or independent model execution.
The reviewer shares the declared scope and earlier investigation context and
received root's render-ready message. Only this working review note is edited.

## Scope and actual inspection

Read main AGENTS.md, WORKFLOW.md, START-HERE.md and the investigation CHARTER,
the evidence-falsification and source-of-truth skills and their referenced
checklists, the PDF skill, and the complete prospective
[scope note](furnace-sag-claim-trace-2026-09-28.md). These controls keep reported
observations, author assertions, model outputs and historical inferences apart.

After root confirmed renderer completion, visually inspected all four complete
pages in furnace-sag-render01, including headings, figure legend/caption,
paragraph continuations and page numbers:

| PDF and physical/printed page | PNG SHA256 |
|---|---|
| NCSTAR 1-6 v1, 138/54 | `6fe6d3c33249d720d7cfb3600b59593f0cefdcfab362166450ac81a10098a43a` |
| NCSTAR 1-6 v1, 139/55 | `6927ba8a617094ea649d468d7d8154f5101dd857cdb303f958c3e2694d7b372d` |
| NCSTAR 1-6 v2, 148/330 | `dff603a870b05a879b8d28b7df11606bb73171f480390082c86eaf3b6e269942` |
| NCSTAR 1-6 v2, 149/331 | `20d0e2956bbf3a10b1ea182303bf7b34ca580b19e639598de21b36b834cc419b` |

`view_image` requested original detail. Actual displays were resized from
1559x2139 to 1344x1843, 1559x2125 to 1344x1831, 1575x2131 to 1344x1818,
and 1575x2125 to 1375x1856, respectively. Text and page boundaries remained
readable; no graph coordinates, pixels or curve values were measured.

Fresh `shasum -a 256` checks of the four PNGs and receipt matched the receipt
entries. Receipt SHA256:
`9df8ffc838b3115c99121fd67b797a4bff607166a89e34300b4b3321a250d3b7`.
Read receipt source/page fields with `jq`; it records complete pages, 200 dpi,
and matching before/after input pins. Its source pins are v1, 23,824,565 bytes,
`9874df97f3ce7bffb048fa9390823599f733cfed5549ca14b934a126f62240d4`,
and v2, 19,845,494 bytes,
`cfc847c22beebfc87ff5e15af5c604f945f2ff1b6d9e62c16b381e10ae8a4f43`.
This reviewer did not reopen PDF bodies or rerun rendering. Root reports
terminal exit 0 and no render/parser warnings after an initial sandbox mkdir
failure; that execution account is root's, not an independently repeated run.

Opened the two authorized official HTML URLs directly, with no search queries,
and read complete answers in their question context: supplement Q7/Q8/Q14 and
current towers FAQ Q14/Q17/Q26. Tool-returned neighboring content was not used
to expand the review. Neither HTML page was downloaded by this reviewer or
assigned an invented acquired-byte hash. No cited underlying volume was opened
beyond the four authorized images. Initial concatenated tool displays were
truncated; required control text and receipt fields were reread in bounded
outputs. No selected page or FAQ answer remained unreadable.

## Frozen source observations

### The original claim is about magnitude, not merely the existence of sag

NCSTAR 1-6 v2 printed331, section10.3.1 Finding7, states:

> The magnitude of the sagging observed in the tests was consistent with that computed from finite element structural analyses.

That expressly compares an observed quantity with a calculated quantity. It
must not be weakened to only a statement that both tests and calculations
showed some sag. Nevertheless, the sentence supplies no sag value, common
time/channel, specific calculation identifier, error bound or acceptance
criterion. In these pages it is a qualitative report of magnitude agreement,
not a displayed quantitative fit or a demonstrated independent prediction.
The word "computed" supplies no pre-test prediction or tuning chronology.

The surrounding findings matter. All four tests sagged without failure;
the unrestrained specimen had two 0.875-inch bolts and did not sag enough to
bear on them. The three restrained specimens had welded ends. No knuckle
failure was observed. Findings6/8 report damage/buckling and continued load
support, respectively. Findings10-14 distinguish fire ratings from ability
to carry load, and identify concrete behavior, overspray and specimen size
as important to differences between ratings. Thus survival, sag, local damage
and rating are not interchangeable outcomes.

Printed330 supplies the four-test setup: two 35-foot, 0.75-inch-SFRM cases
(restrained and unrestrained), and approximately17-foot cases with0.5- and
0.75-inch protection. Earlier findings on that page report insulation
selection, measured/equivalent thickness and adhesion; these are context, not
identification of the specific structural calculation used in Finding7.

NCSTAR 1-6 v1 printed54 section3.6.5 reports standard-fire ratings, loading,
scale and restraint differences. Figure3-18 compares measured bottom-chord
average temperatures for Tests1-3; its legend does not contain a structural
model-prediction series. Printed55 section3.7 reports considerable sagging
without collapse, local damage/buckling and no observed knuckle failures.
It specifically flags limit-state measurement, scale, restraint stiffness,
connections, exposure/loading, repeatability and cross-furnace reproducibility
for further study. These cautions are favorable evidence for an explicitly
limited interpretation, not evidence that the tests themselves were ignored.

Printed54 calls the load-support duration approximately two hours and gives
a minimum of116minutes; Finding8 on printed331 says two hours for all four.
Retain the more precise qualification when needed. This wording difference
alone is not a demonstrated mechanical contradiction or evidence of deception.

### FAQ answers clarify purpose and applicability, not the sag comparison

The [December2007-labeled supplement](https://www.nist.gov/node/442556),
Q7, distinguishes system-scale practical/scaling limits from component/fire
tests, describes calibration to observed impact/fire evolution, and credits
NCSTAR1-5E/1-5B for fire/thermal validation. Q8 gives baseline, factor-comparison
and acceptance-practice purposes for the protected ASTM tests, citing1-6B;
it limits direct inference to9/11 because NIST's impact analysis predicts
dislodged protection. Q14 cites1-6C for modeled sag and load transfer through
surviving connections, studs and struts. These are materially relevant
explanations, but none identifies the furnace specimen/model/time-history pair
behind Finding7. Calibration of impact/fire evolution is not stated calibration
of the furnace-sag comparison. The served page labels itself an archived
12/14/2007 supplement incorporated into a2011 update; its footer shows creation
in2010 and update in2026. This is present-day access to historically labeled
content, not a captured2007 webpage proven unchanged.

The [current towers FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-towers-investigation)
Q14/Q17/Q26 substantially repeat those respective purpose, force-transfer and
system-test explanations. They do not add specimen-specific sag values,
residuals, tolerance, structural input histories or tuning chronology. Q17's
1-6C reference concerns the modeled tower-floor mechanism, not an explicit
join to one of the four furnace cases. Q26's validation statements expressly
concern fire and thermal approaches; they should not be relabeled structural-
sag validation. The header labels creation2011/update2021 and the footer
update2022; question renumbering is disclosed. This same-agency repetition is
not an independent experiment or new corroborating witness.

## Claim-strength and missing-join assessment

| Proposition | Supported ceiling in this review |
|---|---|
| NIST explicitly claimed sag-magnitude consistency | A: directly established as source wording, not proof of the underlying fit |
| Protected specimens could sag substantially while supporting load | B as a primary experimental report; no laboratory replication by this reviewer |
| The selected pages/answers identify an independently reproducible numerical furnace-sag match | Not established here; case/measurement/thermal-history/model-output/tolerance/chronology joins remain unspecified |
| These texts prove the claimed consistency false, or that no comparison exists anywhere | Unsupported; finite source coverage and author-summary form cannot establish global absence |
| Furnace survival validates or falsifies the complete tower initiation sequence, or transfers to WTC7 | Unsupported without the additional condition, system and building-specific joins |

Strongest favorable reading: component testing can support a mechanism without
replicating a complete damaged building, and sag with retained support is not
internally inconsistent with a model whose sagging floor still transfers
horizontal force. The source expressly reports a magnitude comparison and
openly limits the standard-test application. A whole-tower experiment is not
a prerequisite invented by this review.

Strongest contrary reading: magnitude agreement can be materially weak if
restraint, thermal histories, load, specimen scale or comparison timing differ.
The sources themselves identify these sensitivities. Neither a shared
qualitative behavior nor practical barriers to a full-system experiment
supplies the particular furnace-to-calculation mapping. Conversely, absence
of that mapping in the finite reviewed material does not refute the mapping
or determine the adequacy of an uninspected analysis.

What would change this bounded assessment is an existing source that names
the actual furnace case and corresponding structural calculation, identifies
the measured channel and applied history/boundary conditions, supplies aligned
sag results and a stated agreement criterion, and dates model choices relative
to the measurements. Those requirements distinguish magnitude consistency,
calibration and independent prediction; they are not proof that the authors
promised every stronger form. No further acquisition or source expansion is
authorized by this note. Stop this route at the assigned material. No causal
ranking, intent, legal or WTC7 validation conclusion follows.

## Bounded post-synthesis critique

After freezing the source observations above, read the complete updated
furnace-sag-claim-trace-2026-09-28.md and furnace-sag-public-search.md; the causal
synthesis paragraph beginning "The remaining public furnace-sag route" and
footnote29; its matching new SCOPE/validation sections; the new STATUS prefix
through the previous-five-field heading; and the research README furnace
paragraph. No new primary page, query, paper body, model input or other source
was opened. The locator note's June minutes coverage is a separately authored
retrieval account, not an additional direct minutes reading by this reviewer.

The synthesis preserves the decisive distinction: Finding7 asserts agreement
in magnitude, while its source-specific specimen/calculation/history/output
join is not recovered within the declared route. It neither substitutes mere
shared sag for magnitude nor treats unreported tolerances or tuning chronology
as proven falsehood. Favorable physical support, restraint/condition limits,
the prior duration correction and nontransfer to WTC7 remain explicit. The
new dependency is not counted as another independent defect or used to change
causal grades/orderings. Four report pages and six selected answers describe
the source reader's scope; eight queries combine two four-query allocations,
not eight independent experiments or comprehensive coverage.

The new paper lead is correctly limited to metadata and a complete abstract;
the paper body was not read. The minutes discussion is correctly bounded to
the specified sections and credited as pre-test modeling, not demonstrated
comparison with later measurements. Root's chronology is consistent with the
locator note's reported coverage. These derivative checks do not independently
verify the minutes, the publication body or the artifact verifier's numerical
check counts. No whole-synthesis or global-link certification is provided.

One narrow execution-wording correction was requested. The sentence "No old
image or PDF was overwritten; no new code or source command executed" is
ambiguous next to the recorded execution of a derivative renderer. Proposed
replacement: "No old image or PDF was overwritten. No new analysis code was
implemented and no native source commands or solver were executed; the
existing derivative renderer ran as recorded." The existing explanation of
the helper's role makes the intended boundary clear, so this is an execution-
account clarification, not a newly discovered scientific or privacy failure.

**Disposition:** No substantive source/inference objection in these additions;
the one execution-account clarification remains requested at this review
freeze. No broader rewrite or new source work is needed. The actual command
`head -c 10345 furnace-sag-independent-review.md | shasum -a 256` confirmed
the original prefix at
`4a32c7e261f7c1224f811fdd7164e764031e596de2c403eb27b773d96be59dfe`
before this appendix. Earlier observations are not retroactively changed.

### Execution-wording closure

Read back root's saved correction: "No old image or PDF was overwritten; no
native modeling instruction or solver was executed. The renderer/helper are
existing derivative tools, not native simulation code; their four-page source
tuple was overridden as declared." Together with the preceding recorded
renderer run, this resolves the ambiguity without asserting that no tool code
ran. The requested point is closed; bounded disposition is PASS.

Before this closure, the 13,363-byte review prefix was independently rehashed
at `1dcd354ef753658b27b8253259a809512978439dbbaac5a8973ea389f5dcbcd3`.
The original source observations and earlier critique remain intact. No further
source access, computation, global document audit or expanded inference was
undertaken for this readback.
