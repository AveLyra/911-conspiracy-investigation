# Later thermal-response paper: validation-role audit

2026-09-28. Working research only. Main repository AGENTS, WORKFLOW,
START-HERE and the main investigation CHARTER control. Their hashes were
rechecked against the already-read versions this turn and remain unchanged.

## Prospective scope

The preceding user-response turn reverified an existing coordinate record;
it did not advance the goal. This unit resumes the specific open lead in
[the completed floor-model audit](floor-model-validation-followup-2026-09-27.md):
NIST pub_id927871, *Thermal response of a composite floor system to the
standard fire exposure*. Prior search snippets exposed portions of the paper,
so this is not a blind or previously unseen-source protocol.

Question: which physical specimen and channels are compared, which inputs
are measured, assumed or fitted, and does this publication supply a paired
structural sag prediction/test comparison or only a thermal comparison?
A later fitted thermal response is not a contemporaneous 2005 structural
prediction or validation of a WTC7 collapse sequence.

Boundaries, fixed before retrieval/body review:

- At most two official-domain metadata locator queries, then direct official
  metadata/PDF opens; at most one new target PDF. No new general search.
- Preserve the PDF create-only, with URL, acquisition time, byte count,
  SHA-256, page count and edition identifiers. Existing files stay unchanged.
- Inspect frontmatter first. If the paper is at most 30 physical pages,
  review all pages; otherwise declare selected sections before body review.
- A separate reader freezes source findings before seeing root's synthesis.
  Record actual prior exposure; no claim of expert or event-level independence.
- Distinguish measured traces from simulations; calibration from held-out
  evaluation; reported agreement from reproduced errors; thermal from
  structural response; specimen validity from historical transfer.
- Retain favorable validation evidence, discrepancies, temperature-dependent
  assumptions, sensor/termination limitations and any reported error metrics.
- No graph digitization, invented histories, solver execution, original
  drawing access, physical experiment, legal promotion, disclosure, commit
  or push. No earlier frozen notes or source annotations are rewritten.

Deliverables: this source-linked disposition, separate critical source review,
and a source/render integrity check; update the existing audit index and active
status. A causal-synthesis change is warranted only if the source materially
changes its current claim. Acceptance requires actual page coverage, explicit
limits and the exact next missing records, not a predetermined finding.

## Execution and disposition

Official metadata locator used two NIST-domain queries once each:
`"927871" "Thermal response"` (empty), then
`"Thermal response of a composite floor system to the standard fire exposure"`.
The [official catalog](https://www.nist.gov/publications/thermal-response-composite-floor-system-standard-fire-exposure)
identifies Dilip K. Banerjee, *Fire Safety Journal*, December 1, 2019,
DOI `10.1016/j.firesaf.2019.102930`; catalog updated December 10, 2019.
Root and locator agent opened that metadata independently; the agent did not
open the PDF body. Search snippets are not body-review evidence.

Source URL: <https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=927871>.
Root's public web open exposed extracted pages 1–6 and reported 27 pages.
The first local urllib request returned HTTP403 before creating a file;
a standard curl GET of the same URL succeeded, terminal exit0, without
credentials or an alternate source. Preserved create-only as
[thermal-response-927871-source01.pdf](thermal-response-927871-source01.pdf).
Acquired September28 UTC; checked at `2026-09-28T05:12:02.201493+00:00`:
1,241,013 bytes, 27 pages, unencrypted, SHA-256
`953b493d550eda3f8a00f67e4c05817e6112f4baedeb48e542f84a313de5b432`.
PDF creation/modification metadata: December10,2019, Word for Office365.
That metadata is not an independent publication/authenticity certificate.

**Body scope now fixed:** all physical pages1–27 under the predeclared
short-paper rule, full-page renders at200dpi. Printed/page identity will be
checked visually. No other PDF body is added by this scope. Root read only
local page1 text before this declaration. No new source conclusion yet.

Root has now viewed all27 complete page images in order, with matching printed
numbers. Pages1–8 were displayed resized to1376×1780;9–27 at native1700×2200.
No crop, enhancement, graph tracing or curve measurement. Fine embedded
drawing labels on p5 are not certified as fully legible. The decisive text,
tables and curve legends were readable. The separate completed source reading
and post-freeze critique are recorded below. During correction review, root
reread p19's text and p20's complete image (displayed1376×1780), plus the
earlier physical-test audit's termination table; no new PDF body was added.

**Source-informed arithmetic check, declared before execution:** Table4 p18
appears to contain a threshold/text discrepancy. Check all four reported
statistics against both printed critical values (eight comparisons), not just
the apparent exception. Separately check every populated Table5 p20 percentage
against `100*(predicted_C-measured_C)/(measured_C+273.15)`, the ordinary
measured-value relative-error interpretation of its absolute-scale heading.
Flag differences exceeding0.25 percentage point as a screening tolerance for
printed/rounded values, not a scientific acceptance threshold. Preserve
missing cells; this cannot recover raw data, the author's unprinted formula,
sampling covariance or the actual FE run. No p-value/model-accuracy inference
or reconstructed time series is authorized by this arithmetic check.

## Source findings — root reading with completed independent critique

Page citations below are both printed and one-based physical pages. This is
a complete reading of this particular27-page paper, not of its cited sources.

### What this source adds, and what it does not

**This paper contains thermal measured-versus-model comparisons, not structural
sag validation.** Its abstract, pp3–4,10 and23–24 consistently describe heat
transfer as the subject and structural analysis as a subsequent use. No paired
deflection, reaction-force, connection-failure or collapse-sequence validation
is presented in its body or appendix. This closes the present paper as a
candidate location for the missing sag comparison; it does not establish that
such a comparison is absent elsewhere.

The experiment-to-model lineage is real, not merely an animation: pp4–9 and
Figs1–6 describe the35ft UL Canada restrained Test1 and unrestrained Test2,
with sprayed protection, measured furnace/slab/steel temperatures and sensor
locations. Reference8 identifies NCSTAR1-6B; reference9 identifies the2012
NIST TN1771 thermal study. These are tower-floor test specimens, not WTC7.
Test1/2 are not all four assemblies from the earlier physical-test audit.
The catalog's2019 publication and the later cited software/literature do not
authenticate a2005 prediction or a model used for WTC7.

### Comparison design and conditioning

| Layer | Source-pinned content | Consequence for inference |
|---|---|---|
| Geometry and temperatures | pp11–16: one main truss without end supports, half-width slab; no bridging trusses/angles, explicit metal deck or protruding knuckles; thermal solid/link/surface elements. | A simplified thermal subassembly, not a structurally complete floor or collapse solver. Omitted thermal mass is offered as one possible explanation for a location-specific mismatch. |
| Exposure inputs | pp14–16: ASTM E119 reference-node heating, unit view factors; initially25°C, adiabatic unspecified boundaries. | Prescribed exposure, not a CFD reconstruction or independently predicted furnace gas field. |
| Measured boundary input | p15: time-varying measured mean temperatures on unexposed slab segments are imposed as boundary conditions; this is the stated thermal-model difference between Tests1/2. | Legitimate conditioning on observations, but those same boundary temperatures cannot count as independently predicted validation channels. Interior steel comparisons retain empirical value; using measured boundaries does not make every comparison circular. |
| Material/boundary choices | pp13–16,26–27: uniform protection/slab approximation,19mm slab overspray assumption, perfect steel/slab contact, convection15W/m²/K, steel/slab emissivity0.7/0.6; temperature-dependent material tables. | Published choices and rationale improve inspectability. They are not all shown fitted to these tests. Uniformity, contact and constant exchange coefficients are expressly acknowledged limitations. |
| Response extraction | pp16–18: averages over model cross-sections interpolated to A,C,E,I; measured lower/upper chord and mid-web channels. Some south-truss readings added for comparison; erroneous sensors excluded by cited logs. | Node/sensor mapping, inclusion masks and valid-time histories are necessary to reproduce the comparison. A sectional average is not automatically a pointwise prediction. |
| Intact-protection evaluation | pp18–21, Figs10–12/Table5: much lower-chord/mid-web agreement, plus early/local disagreement and substantial later upper-chord underprediction at several plotted locations. | Affirmative but heterogeneous evidence. Good channels and failed channels must both remain; no blanket never-validated or uniformly accurate conclusion. |
| Inferred protection loss | pp21–23: restart/removal times tied to reported sounds; lengths2–3ft, removal depths selected by trial and error. Test1 removal at3800s (A0.5in; I/E0.75in), then4500s (C0.75in). | An explicitly data-informed inverse/calibration exercise, not blind prediction of spalling time/amount. Improved agreement supports plausibility under the assumptions, not unique identification of that mechanism. |

Figure14 retains significant imperfect agreement: the modified model remains
too cool at late A and too hot at late E; I differs before the jump. These are
qualitative curve comparisons, not digitized residuals. The trial-and-error
history, other tried cases, objective function and held-out channels are not
provided. No unused validation set is established in this paper. This does
not prove every baseline parameter was tuned, or make calibration improper.

### Checkable reporting and reproduction questions

1. **Table4 contradicts an unqualified two-level agreement statement.**
   Section4.1 excludes the initial transient and describes agreement at both
   1% and0.5% levels. Seven of eight printed statistic/critical-value
   inequalities support that description, but Test2/A3 is67.54, exceeding
   the printed1% critical value64.94 while remaining below the0.5% value68.04.
   The other three rows are below both thresholds. This is a reported-number
   inconsistency, not a rerun of the statistic. The paper does not supply a
   recoverable statistic formula/error covariance, exact included times or
   adjustment history sufficient to independently verify its statistical
   interpretation. Failure to exceed a critical value is not a model-accuracy
   probability or proof of equivalence.
2. **Percentage arithmetic is mostly reproducible, with one conspicuous
   exception under the stated interpretation.** Table5's heading says
   differences use the absolute temperature scale. Root transcribed all48
   location/time/member cells;37 have printed percentages, nine lack measured
   values, and two retain measured/predicted values but no percentage.
   Of37 comparisons,36 agree within the predeclared0.25percentage-point
   screening tolerance. Mid-web A at90min lists792°C measured,820°C modeled,
   and3.5%; the declared Kelvin-denominator calculation gives2.6287%, while
   a Celsius denominator gives3.5354%. That is consistent with a denominator
   or editorial inconsistency, not proof of its cause or an FE error. Top-A
   at90/120min has no printed percentage; the tabulated pairs imply−15.8742%
   and−26.6777% under the same interpretation. These are retained missing
   source cells, not silently inserted source values. Kelvin-relative error
   is not fractional error in thermal expansion, stiffness or collapse risk.
3. **Model-version and channel identity need reconciliation.** Figures12/14
   do not display the same intact upper-chord trajectory at all locations;
   Figure14 identifies individual thermocouples whereas the earlier plots
   are described using averages. The paper's conclusions say the model
   overpredicts the upper chord, while the intact curves underpredict several
   late measured traces and the modified curves have mixed error signs.
   Do not harmonize these by selecting one favorable plot. Different channels,
   case versions or editorial shorthand are possible explanations; exact
   run/output mappings would distinguish them. No figure pixels were traced.
4. **Published material tables are not an executable native package.**
   AppendixA pp26–27 gives useful thermal properties, but steel tables end
   at702°C while the presented responses extend higher. SFRM conductivity
   is printed0.0 at25°C with only one decimal place, and its listed density
   rises after600°C. Concrete's room-temperature density is2101.7kg/m³,
   whereas p4 gives a1601.85kg/m³ design target and Table2 gives differing
   wet specimen weights. Temperature, moisture, rounding, material identity,
   extrapolation and source-version conventions must be established before
   using these entries. None alone proves an incorrect actual input.
5. **Test attribution is internally inconsistent.** Page19 attributes a
   comparison to Test2 while referring to Table5, which is explicitly captioned
   Test1 on p20. The source's label is preserved in the arithmetic derivative;
   no second table or corrected attribution is invented. Original case/channel
   mappings or an author correction could resolve this reporting issue.
6. **Late Test1 timing needs reconciliation.** The paper uses120min Test1
   comparisons, whereas the earlier
   [physical-test audit](physical-floor-test-followup-2026-09-27.md) records
   Assembly1's116min furnace stop. This specific cross-source question requires
   the original clocks, heating/shutoff histories and valid-channel records.
   Furnace shutoff does not instantly end meaningful temperature measurement;
   post-shutoff data or timing conventions may explain the difference. The
   mismatch alone establishes neither invalid late data nor manipulation.

The reproducible printed-table derivative is
[thermal-response-table-check01.json](thermal-response-table-check01.json).
It preserves all48 cells, nulls, the four Table4 rows, assumptions, formula and
calculated endpoints. Root used a stdout-only JavaScript calculation followed
by create-only addition of that JSON; no solver or graph digitization ran.
The separate arithmetic reader independently transcribed the fullpage images
18/20 before reading root's JSON. Its first freeze reproduced all37 populated
percentage comparisons, the sole tolerance flag and all eight Table4 decisions.
After freeze it compared all48 input cells, nulls and computed fields with the
JSON and checked the two additional Top-A derived values: no disagreement.
Its original37-cell scope had left those two source-percentage blanks
uncomputed; the post-freeze extension did not turn them into printed values.
This independent arithmetic is not another experiment or source.

### Claim-strength disposition and strongest alternatives

| Proposition | Type and grade | Reason / what would change it |
|---|---|---|
| The paper presents real specimen-linked temperature comparisons | Source observation A; physical predictive adequacy C | Complete paper supports the comparison's existence. Original sensor data, input/output files and valid-channel masks are still needed for reproduction. |
| The paper validates structural sag or WTC7 collapse | E as a characterization of this paper | Its modeled/reported response is thermal; structural use is prospective. A separate case-linked structural comparison could supply missing evidence, but is not in this paper. |
| Fitted protection-loss responses independently prove the actual loss history | D | Trial-and-error conditioning and remaining mismatches do not establish uniqueness. Independent protection-loss observations and held-out thermal predictions would strengthen the inference. |
| The reporting discrepancies prove intentional falsification or no value in the model | E | Arithmetic/editorial/model-version alternatives remain, alongside genuine agreement and openly stated assumptions. No act, intent or WTC7 historical cause is established. |

The strongest counterpoint to a dismissive reading is that meaningful steel
temperature agreement survives without replacing every measured output by an
input, and the author openly reports simplifications and discrepancies.
The strongest objection to broad validation is that temperature agreement
conditioned on test observations, with fitted loss events, cannot validate a
different structural response or identify a historical causal sequence.
No WTC7 causal grade or comparative ordering changes from this paper alone.

## Verification and next discriminating work

The [independent source review](thermal-response-independent-review.md) read
all27 complete page images and their full text derivatives before reading
root's synthesis or the separate arithmetic result. It is prior-informed AI
review, not blinded, licensed engineering review or model replication. Its
original18,406-byte source freeze has SHA-256
`333561d438f264184ef7cac6b3afc4c3f7acb087651cb8556d6e312c4c51838b`.
The post-freeze critique reviewed this entire source note, the dated causal
subsection/footnote22 and corresponding SCOPE addition. It requested the
explicit test-label and116/120min issues now preserved above and found no
other material scientific overclaim in that scope. Root read the complete
review. Its acquisition, whole-table arithmetic and artifact checks remain
separately attributed, not certified by that scientific critique.

The reader subsequently checked both corrections, the review attribution,
STATUS opening and dated causal-validation summary; no material scope/role
error was found in those passages. Root read that appended check. Completed
review:22,632bytes, SHA-256
`d0b9f6d04a101558d39e64c79e5d334ea0577686f925d0d698f10a72dbf3ff45`.
The original source freeze remains unchanged; no new source was added by
the correction check.

Renderer invocation: bundled Python3.12.14 `-B -`, loading the existing
`render_condition_pages.py`, overriding only its in-memory source tuple with
this PDF/hash/27pages/physical1–27, and calling
`render('thermal-response-render01')`. Terminal exit0:27 fullpage derivatives,
no per-page renderer stderr, no parser log or captured warnings. Receipt SHA:
`22720bbc011a580fea398bb420e3f39dbd0cb9b27f289212a82da44e47434e2a`.
[Independent artifact verification](thermal-response-artifact-verification.md)
checked116 products,27 decoded pixel hashes and geometry, and an unchanged
118-file before/after interval. Root read that complete note. Version-banner
stderr is not empty; seven non-source dependency pins were not freshly checked
by the artifact verifier. These checks do not verify the science.

Final root documentation/arithmetic check used bundled Python3.12.14 `-B -`,
an inline read-only stdout program retained in the task tool history, terminal
exit0 (chunk`ddab70`). It parsed/recomputed all48Table5 cells (37printed
percentages,9missing measurements,2paired percentage blanks,1screening flag)
with absolute arithmetic tolerance1e-12, preserved nulls and checked all eight
Table4 inequalities. Ten touched Markdown files passed newline/trailing-space/
conflict-marker checks;51local targets existed across this note, the two
separate reviews and causal report/validation;22causal footnotes were unique
and all references defined. The source PDF, render receipt and artifact-note
pins matched, as did the original18,406-byte source-review prefix and four
main-control hashes. The check also recorded the completed review pin above.
`git diff --check` exited0. External URL reachability, fragment resolution,
source authenticity, scientific validity and model execution are outside
these checks. This is not a saved independent verification program or a
physical experiment.

Needed for a thermal reproduction: original channel/time/validity arrays;
segmented slab-boundary inputs; exact geometry/property functions including
high-temperature extrapolation; solver case versions and APDL extraction;
removal restart/history and all candidate fits; statistic formula, units,
covariance and sample masks, including the explicit Test1/Test2 attribution
and116/120min timing reconciliations. Needed for the outstanding sag claim: the
distinct contemporaneous structural model/case IDs, matched load/restraint
histories, measured sag channels and prediction/calibration chronology.

Next bounded source lead is reference9, *NIST TN1771* (2012), explicitly cited
for thermal data and properties. First check existing repository coverage,
then its official metadata/frontmatter; inspect only the sections needed to
resolve channel/property/run-version provenance. It is not assumed to contain
a sag comparison, and a thermal-only disposition cannot close that separate
dependency. No repeat of this paper acquisition or the exhausted two queries
is needed. Broader investigation and all existing privacy/human-review gates
remain active; no main/legal record changes or external transfer occurred.

**Subsequent source follow-through:** The
[complete TN1771 audit](tn1771-provenance-followup-2026-09-28.md) now completes
the then-next lead above. It supplies separate Test2 comparisons and positive
graph evidence for a rounding explanation of the printed zero. Exact Table2/
Table5 numeric identity establishes shared published values, not native-run
identity. It leaves the internal116/120min clock question, property conventions
and output-channel/version mapping unresolved. The original audit and its
review history remain preserved; no new sag validation or causal ranking is
inferred from the follow-through.
