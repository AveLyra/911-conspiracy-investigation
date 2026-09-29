# Localized gaps and variable fireproofing: source/applicability audit

2026-09-27. Working research; no structural or historical-cause finding.

## Scope declared before source acquisition and calculation

The preceding Testwell locator turn completed its finite search and identified
specific studies cited in NIST FAQ23. It was progress, not a verified wait.
This unit tests the scope of those cited results: NCSTAR1-6 Chapter2 and
NCSTAR1-6A Chapter5. The [Testwell follow-up](testwell-original-record-followup-2026-09-27.md)
and [earlier protection crosswalk](protection-assumption-crosswalk-2026-09-27.md)
provide context, not independent corroboration of these studies.

Search existing public research locators/reviews first and retrieve official
report copies only if needed. Preserve originals unchanged with actual URL,
date, byte/hash and edition identities. Initial PDF parsing is limited to
metadata and physical pages1-20 for title/contents/figure locators; no broad
PDF search. Record the exact narrative/result-page allowlist before further
parsing or rendering. Model schematics in these public reports are in scope;
original structural drawing sheets and unrelated appendices are not.

Compare physical geometry, fireproofing properties/thickness, gap width/location,
spatial variability and assumed distribution, heat exposure, boundary conditions,
temperature locations/averages, performance metric, sensitivity cases and
claimed applicability. Distinguish a computational plate idealization from a
physical experiment and a tower truss from a WTC7 beam or connection. Identify
what source conditions support the author's conclusion and where extrapolation
would require new evidence. Preserve adverse cases as well as favorable ones.

Acceptance: whole-page source reading of decisive definitions/results, exact
page pins, source/copy integrity checks, an explicit applicability/claim ledger,
and independent critical source review. Do not call report reading an independent
thermal reproduction or infer historical missing-coating geometry from the1997
survey's generic descriptions. No graph digitization or solver execution in
this unit. No historical ranking change without an identified discriminating
result; a new limitation alone does not identify an alternative cause.

Root owns this research note, page derivatives and navigation. A separate
locator checks prior work; a separate source reader will inspect declared
decisive pages. Main charter, record-preservation, drawing/privacy and actual-
human gates remain controlling. No legal promotion, outreach, fees, publication,
new requests, protected-source access, commit or push.

## Source locators and page selection

The official NCSTAR1-6A legacy PDF was acquired first. Metadata/title locator
identifies the September2005 report, later digitized in2015; digitization is
not the report date. Physical8's contents place Chapter5 at printed51, §5.2 at57,
§5.3 at60 and Chapter6 at63. Physical12's figure list identifies the plate-gap
and variability figures. These are text locators, not a completed reading.

Before mapping body pages, extend the front-matter locator for each report to
physical21-40, solely to establish the first printed Arabic page and offset.
This is an exact early-page allowlist, not a header/footer filter applied to the
whole report. Do not inspect unrelated later pages or appendices. Once offset
is confirmed, record the specific body selection before its extraction/rendering.

PDF page-label metadata maps NCSTAR1-6A printed1 to physical53, and NCSTAR1-6
printed1 to physical85. Before reading the body, select **1-6A physical103-114 /
printed51-62 (entire Chapter5)** and **1-6 physical109-114 / printed25-30
(§2.4 through the summary and adjacent start of properties)**. Also render
1-6A physical3 and1-6 physical5 for complete title/date verification. Confirm
printed footers in the images, not just metadata. No pages41-52/41-84 are added
by implication; the page-label metadata avoided another front-matter crawl.
These are public report discussion, model diagrams, charts and a published
condition photograph, not original drawing-sheet inspection.

## Result: a material applicability gap, not a cause finding

The inspected chapters support a **conditional sensitivity result**, not a
demonstration of FAQ23's two assertions: that small damaged areas would not
have affected WTC7 framing response, and that occasional gaps did not
significantly alter member thermal response. They report faster local steel
heating as thickness variability or missing
length increases. A separate equivalent-thickness calculation matches the
elongation of an idealized tower-truss bar, not local connection failure or a
building's collapse sequence. The two reports describe the same studies;
their agreement is not independent replication.

FAQ23's plate-study characterization is not established by the inspected
sections it cites. That is an identifiable citation/applicability weakness,
not proof the WTC7 model's overall result is wrong, that missing coating caused
collapse, or that its authors acted improperly. Local thermal differences
could coexist with a small change in a chosen whole-member metric; the cited
plate study does not supply a quantitative insignificance criterion for that
claim. A WTC7-specific response test could support the FAQ despite this gap.

The result does **not** establish a new historical-cause ranking. It
narrows what can be claimed as independently supported about this modeling
assumption. Lost coating could increase fire vulnerability; it is not evidence
against fire by default. Neither study tests deliberate support removal.

## Sources, identity and reading coverage

Both official PDFs were acquired September27,2026, with HTTP200,
`application/pdf`, unchanged final URL and completed download before parsing.
Titles identify September2005 reports. Their2015 Internet Archive creation/
digitization metadata are not report dates. The official1-6 publication landing
lists December1,2005; that difference is retained without inventing an edition
relationship. Alternate official download links and a draft were located,
not acquired or treated as independent evidence.

| Source and preserved copy | Bytes / SHA-256 | Complete image reading |
|---|---|---|
| [NCSTAR1-6A, Passive Fire Protection](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6a.pdf), [local PDF](ncstar-1-6a-source01.pdf) | 22,813,796 / `75b910620ee9c9f202256acd898f01f28a0df23546132c2108a2a1735cb021b3` | Physical3 title;103–114 = printed51–62, entireChapter5 including blank62 |
| [NCSTAR1-6, Structural Fire Response and Probable Collapse Sequence of the World Trade Center Towers, Chapters1–6](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-6v1.pdf), [local PDF](ncstar-1-6v1-source01.pdf) | 23,824,565 / `9874df97f3ce7bffb048fa9390823599f733cfed5549ca14b934a126f62240d4` | Physical5 title;109–114 = printed25–30, §2.4/§2.5 and start of§2.6 |
| [NIST WTC7 FAQ23](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation), [held HTML](nist-wtc7-faq-source01.html) | 142,624 / `d3b6dc382b699819c4d220df8dd6fdfd28791445b6c0e6cf5124f142d2236c15` | Exact HTML lines954–968, not a fresh full-page web audit |

The source locations above identify published claims, not independently
verified historical coating conditions. Root read all20 selected full-page
images. Rendering/display and separate review boundaries are recorded in the
[verification receipt](gap-study-render01/verification.md). The initial
front-matter text-locator coverage was physical1–20 and21–40 in each PDF;
those are not represented as full-page visual reviews. No appendices, original
drawing sheets or other body pages were inspected in this unit.

### What each calculation actually did

| Feature | Plate sensitivity:1-6A pp51–57;1-6 pp25–27 | Equivalent thickness:1-6A pp57–61;1-6 pp27–29 |
|---|---|---|
| Object | Numerical 1in-thick,60in-long steel plate; coating on both faces | Numerical 1in-diameter,60in-long bar,100 length elements |
| Heating | Uniform radiative exposure representing1100°C fire, initial300K; up to2h | Radiation representing1100°C fire; calculated temperature histories |
| Coating variation | Mean0–2in in0.25in steps; SD0,0.25,0.5,0.75,1in; pseudorandom thickness | Lognormal target mean/SD0.75/0.3in original and2.5/0.6in upgraded;3 realizations each |
| Missing coating | Missing length0–30in in6in steps; illustrated12in central gap in otherwise2in coating | Not a demonstrated isolated bare-gap equivalence study |
| Spatial treatment | Coating mesh0.125in by0.6in; layer twice mean thickness; ineffective cells assigned low heat capacity/high conductivity | Original-case rough and five-point-smoothed profiles; upgrade analysis smooth profiles only; profile means/SDs approximately retained |
| Reported metric | Local temperatures at6,18,30,42,54in from one end at30,60,90,120min; Fig5-6 focuses on point2 | Unrestrained axial length change with12500psi tensile stress; not connection force, buckling or failure |
| Main result | More variation or larger gaps can accelerate local heating, including adjacent protected steel | Approximate elongation equivalence to0.6in uniform coating for original case and2.2in for upgrade |

These temperatures, dimensions and outcomes are source-reported model inputs/
outputs. No model was executed here. The1100°C input is not evidence that
WTC7's actual steel, gas or fire reached that temperature. A schematic caption's
use of “physical model” does not turn this into a laboratory experiment.

### Decisive observations and qualifications

1. **Local effect is explicit.**1-6A printed52 reports that0.5in uniform
   coating takes about60min to reach600°C at point1, whereas the SD1in example
   requires a mean near1.75in for similar protection. This is an illustrative
   extreme-variability case, not a WTC7 estimate. Printed55–56 discuss a central
   bare region heating quickly and conducting heat into protected steel. The
   point2 response depends on whether the gap reaches that location;24/30in
   gaps expose it. No graph was digitized to create additional numerical claims.
2. **Missing geometry was a stated limitation.**1-6A printed57 and1-6 printed27
   say that insufficient information on gap frequency/location led to gaps
   being omitted from the towers' thermal modeling. This does not mean NIST
   never studied gaps, nor is it automatically a statement about the separate
   WTC7 model. The photo is of tower bridging-truss protection;1-6A printed55
   warns that its lower-story condition may not represent upper/upgraded areas.
3. **The sampling descriptions conflict.**1-6A printed51 says the plate study
   used a normal distribution;1-6 printed25 calls it lognormal. Both later
   describe the bar-equivalence distribution as lognormal. This is an actual
   text difference, not yet an established execution error. Native inputs,
   distribution/seed records and any correction are needed to reconcile it.
   In particular, the selected plate pages do not specify handling of negative
   sampled thicknesses or values beyond the twice-mean layer. Do not invent
   clipping or infer a coding failure from missing detail.
4. **Equivalence is metric-specific.**The bar's temperature histories feed
   integrated elongation under tension. Comparable elongation does not by
   itself establish comparable local maxima, gradients, restraint forces,
   connection capacity, buckling time or system collapse. Three profile
   realizations per condition are not a validated uncertainty distribution for
   actual buildings. Five-point smoothing changes spatial structure even when
   reported means/SDs remain similar; seeds and native arrays are not supplied
   in the selected pages.
5. **Uniform thickness was not universally just the specified value.**1-6
   printed29 and1-6A printed61 give0.6in for original and2.2in for upgraded
   trusses; other elements use specified thickness, justified by offsetting
   thicker measured averages against reduced effectiveness from variability.
   Table2-2 (1-6 printed29–30) lists specified0.5/1.5in for main-truss original/
   upgraded conditions, distinct from modeled0.6/2.2in. Footnote5 says the
   original one-way bridging-truss condition had no calculated equivalent
   thickness yet used0.6in. Thus a universal calibrated-equivalence claim would
   exceed even the report's own qualifications. These are tower choices, not
   direct WTC7 prescription or error findings.
6. **The table retains empirical gaps.**Its footnotes distinguish unknown
   installed conditions, photo-based estimates and “specified” values inferred
   from correspondence rather than contract documents. We did not verify those
   underlying records here. The start of§2.6 describes material-property testing
   but does not provide the full plate-case functions/boundary implementation
   needed for an independently executable reproduction within these pages.

## Claim and applicability ledger

Grades describe the strength of this bounded result, not the historical cause:
A=direct source-content finding; B=strong scoped inference; C=assumption-
dependent transfer; D=unresolved; E=unsupported in the inspected evidence.

| Proposition | Status and strongest objection | What would change it |
|---|---|---|
| NIST reports numerical gap/variability studies | A: directly described in both reports; same study family, not two replications | Native cases could verify actual execution and outputs |
| Local gaps/variation can substantially change nearby modeled temperature | A for reported cases, not independently reproduced; magnitude/location are conditional | Independent replay with documented conditions and mesh checks |
| The cited plate pages demonstrate negligible thermal effect for occasional gaps in WTC7 | E as a demonstrated claim in this coverage: no WTC7 geometry or quantitative whole-member insignificance test; small average effects could nevertheless coexist with local hotspots | Exact member/gap/exposure cases, complete spatial histories and a prespecified relevant response criterion |
| The bar calculation accounts for some observed tower-truss variability | B within its elongation metric and sampled profiles; source-described equivalence, not independent validation | Native profile/history reproduction and wider sensitivity including different spatial correlation |
| That equivalence establishes unchanged WTC7 connection/system response | D; transfer requires WTC7 geometry, restraints, coating properties and mechanical metrics | Matched WTC7 connection/member cases with defensible input ranges and force/failure histories |
| The normal/lognormal wording proves a wrong or contrived model | E; a summary error is a viable alternative | Original inputs, author correction and consequence analysis distinguishing description from execution |
| These limitations identify deliberate support removal or intent | E; neither calculation addresses those mechanisms, preparations or actors | Independent mechanism-specific evidence and competing predictive tests |

The strongest source-based defense of the FAQ is that specified main-truss
thicknesses0.5/1.5in lie below the modeled equivalent0.6/2.2in: this supports a
conditional rationale that specified uniform thickness can account for some
variability. Also, the plate study's smallest nonzero gap is6in on a60in plate;
its larger-gap/local-temperature cases do not refute insignificance of smaller
defects for a relevant aggregate metric. The FAQ may compress a wider body of
engineering judgment. The strongest criticism remains that the particular
citations inspected do not demonstrate its proposition for WTC7, especially
where a proposed failure depends on a local connection. Resolving that dispute
requires an explicit mapping and response test, not choosing which description
sounds more plausible.

## Next discriminating task and stop rules

**Follow-through status:** The finite native-input/clarification search is now
recorded in the [linked follow-up](gap-study-input-followup-2026-09-27.md).
It located primary discussion and methodology slides, not native cases or a
definitive correction. That note preserves actual coverage and the new1-5G/
publication leads; do not repeat the completed queries. The original next-step
scope below is retained as the basis for that completed search.

First perform a **bounded existing-input/primary-locator search** for the
plate and bar studies' native cases or a published clarification. Start with
the exact report identifiers,§5.1/§5.2, the conflicting distribution labels and
the existing public source inventory; inspect titles/manifests before payloads.
Seek the distribution/seed and thickness treatment, raw versus smoothed arrays,
gap geometry, thermal-property functions, radiative/boundary settings and all
five spatial temperature histories. The outcome may be an exact acquired input
set or a coverage-limited unresolved result, not global unavailability.

Do not rerun the completed generic thermal-transfer or Testwell queries.
Do not reconstruct undocumented inputs silently, digitize charts, run a new
solver, open original structural sheets or promote this to court assertions.
Any later synthetic replay needs its own frozen design and must distinguish
method sensitivity from historical WTC7 reconstruction. WTC7 applicability
ultimately needs a same-member/connection comparison with retained uncertainty
and mechanical outcomes, not a similarity between plotted silhouettes.

## Review, failures and verification status

The prior-work navigator found no completed exact-study review in six selected
research documents and five selected indexes; that is not a repository-wide
absence finding. Its initially overbroad JSON search exposed snippets from a
public1-1J text derivative beyond its intended index scope, then stopped. No
substantive result was taken from that derivative. An overbroad identifier
pattern and two guessed directory probes were corrected. Preserve these
failures rather than describe all searches as compliant or successful.

Independent artifact verification passed: both PDF byte/hash pins, selected
page geometry,20 complete PNG decodes and before/after unchanged identities.
This is not historical authentication or scientific reproduction.

The separate source reader inspected the same20 complete images and exact-page
text, freezing findings before opening the FAQ excerpt and root synthesis.
The reader had shared scope and root progress messages; this was not a blinded
experiment or independent empirical replication. The reader independently
confirmed both PDF pins and the FAQ HTML pin. Original-detail display requests
did not prevent resizing; no source-coordinate measurement was attempted.

That review confirmed the plate/bar distinction and distribution discrepancy,
then found an overstatement in the draft: “cannot affect” made the FAQ's
case-specific/significance assertion absolute. It was replaced by the actual
two-level claim. The strongest defense now includes specified versus equivalent
thickness values and the6in minimum nonzero study gap, preventing large-gap
local heating from becoming a refutation of smaller-defect aggregate
insignificance. The profile wording was narrowed to original rough/smooth
versus upgrade smooth-only. Independent documentation review also changed
“NIST performed” to “NIST reports” to preserve execution uncertainty.
The source reviewer then re-read the four corrected passages and confirmed
faithful integration with no remaining substantive discrepancy in that scope.

Root's first `git diff --check` passed. A read-only bundled Python3.12.14
check passed whitespace/conflict checks for six touched Markdown files and
existence checks for seven note/receipt local targets. The separate document
review independently checked those seven targets (zero missing). External
URLs/fragments were not verified by these local-link checks. A final pass after
integration is recorded below. No result is labeled human-approved; all source
readers were computational agents. No commit, push, external feedback delivery
or legal-record change.

Final integrated root verification: the bundled `python3 -B` inline check
passed seven touched Markdown whitespace/conflict checks, all seven note/
receipt local targets, and the exact sizes/SHA-256 of both PDFs and the held
FAQ HTML. It did not parse new PDF content, validate external URLs/fragments
or replay renders. `git diff --check` exited0. `git rev-parse HEAD` and
`git branch --show-current` confirmed branch
`research/sherlock-wtc7-investigation` at
`2fab1389ba8529494dd206a948014cd41cbf97d2`; new source/derivative/note files
remain intentional untracked WIP and existing edits are preserved. Main's
tracked dirty-file listing is unchanged. Scope/next-test handoff is updated in
the existing STATUS, not a new competing authority. Full goal active/incomplete.
