# Independent TN1749 transcription and arithmetic review

Research-only derivative, 2026-09-12. TN1749 arithmetic and post-freeze root
comparison are complete. The separately authorized native-unit original-stage
diagnostic and its post-freeze root comparison are also complete. No total-load
or angular conversion has been performed. The source-transcription and pause
discussion below record earlier phases; the final sections record the resumed
bounded calculations and their exact verification limits.

## Source coverage and independence

The preserved July2012, corrected February2013 TN1749 PDF has SHA-256
5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf.
It has113 physical pages. Full-page views at130dpi covered PDF41–47 /
printed23–29, including complete text, tables, figure axes/captions and
footnotes. PDF text extraction was an auxiliary aid only.

Both Tables3-3 and3-4 are complete on PDF46 / printed28. They have three
connection-size rows each, for3/4/5 bolts. No table continuation appears on
the neighboring pages. The six rows contain both detailed and reduced model
values, their signed percentage deviations, experimental means and COVs:
36 printed numerical values excluding connection-size identifiers. Model and
mean load values have one decimal in kN; rotation values have three decimals
in rad; deviations and COVs have one decimal in percent. Display precision
and signs, including0.120 and positive deviations, are preserved as strings.

[Independent source transcription](tn1749-independent.json) was frozen with
SHA-256638b66018eb46fc2ed1ea07949b053a68964ce29a6a1fbc07b696b3267a05dbe
before arithmetic or root transcription/result access. No root parser,
calculation or table values have been consulted at this phase. This is
independent transcription of one retrospective report, not an independent
experimental data collection.

## Counts and definitions that must survive the calculation

- PDF41 and43 / printed23 and25 report three test executions for each
  connection size, nine total. PDF41 and44 say the same beams were reused.
  Nine executions must not be described as nine fully independent new
  assemblies.
- Figure3-21 on PDF45 / printed27 shows test labels1/2/3 for the3-bolt and
  4-bolt series, and2/3 for the5-bolt series. PDF43 says measurements for
  5-bolt test1 were not presented because initial data were missing owing to
  a setup problem.
- Neither table explicitly declares the constituent test IDs or n used for
  its mean/COV. The frozen transcription therefore records conducted n=3
  separately from sample_n_stated_in_table=null. Missing initial data do not
  by themselves prove that an ultimate observation was wholly unavailable;
  figure omission is not automatically summary exclusion.
- The footnotes define deviation relative to the experimental mean and COV
  as standard deviation divided by mean. They do not identify sample versus
  population standard deviation. The selected tables do not supply individual
  experimental values from which to recalculate either mean or COV.
- PDF44 / printed26 says NIST rotations use1.89m between bolt centerlines,
  whereas Thompson used1.99m from the exterior pin to the center-column face.
  It describes NIST rotations as about5percent larger. Preserve both source
  definitions; no conversion or new discrepancy has been computed at this
  phase.

## Model comparison is not a clean unused-data test

PDF42 / printed24 states that specimen-specific tensile-test data were not
provided; representative calibrated material curves were used. Zero initial
bolt tension is a model assumption on that page, not an independently
verified experimental pretension measurement. Initial gaps in the reduced
model were selected with attention to agreement.

PDF44–45 / printed26–27 identify axial-restraint/gap sensitivity and describe
choosing quadratic unloading over linear unloading because it gave better
experimental agreement. Thus the comparison is not wholly unused prediction
evidence for every modeling choice. This observation does not establish that
every parameter was fitted to these experiments.

PDF44 reports an additional comparison boundary: both models predict bolt
shear in all cases, but experimental failure modes also include shear-tab
tensile rupture and block shear. The model peak is at initial failure,
whereas4-bolt test1 and5-bolt test3 reportedly peak at a secondary failure.
An eventual peak-load percentage must not silently be described as agreement
on the same failure mechanism or stage.

Concentrated loading of a center column that is already unsupported, described
on PDF41, is not by itself a sudden dynamic column-removal experiment.
Neither this transcription nor the forthcoming arithmetic establishes a
fire-exposed WTC7-specific connection test.

## Preserved read limitation and next gate

An initial image lookup used two-digit rather than Poppler's three-digit
page suffix. It returned a missing-file error, produced no evidence, and was
resolved by inventorying the actual render names before viewing all seven
full pages. No PDF or transcription was modified to resolve it.

The numerical protocol was subsequently read and the TN-only calculation
completed, as recorded below. Original Thompson-source inclusion, sample
count and rotation mapping remain distinct work, not assumed facts.

## Completed TN arithmetic and pause handoff

The arithmetic protocol was frozen before calculation, SHA-256
88954a1929e80b32fd49f061f426be594997532ade2e59528a87c6bbb4bde78e.
The independent calculation uses exact rational values of
100*(model-experimental_mean)/experimental_mean and tests the declared
last-place display-rounding intervals. It does not treat COV as an error bar
or derive missing observations from a summary.

[Independent code](verify_tn1749.py), SHA-256
f6955dcda59cb1bb09b911c8aa90f3579ffd41619c79a81faac1ee25d3d1c24f,
ran successfully after the protocol freeze. [Result01](tn1749-independent-results01.json),
SHA-25618970dbeff47ea2fe562fc8765997bb63544f45130c57ad4a71ec800a1e8010b,
preserves all12 comparisons and nine passing synthetic control groups.
Source PDF, transcription, protocols and code hashes were unchanged across
the run. The exact command and Python version are in that receipt.

Nine point deviations lie outside the printed deviation's plus/minus
0.05percentage-point interval. All12 model/mean rounding intervals intersect
their respective printed-deviation intervals; none is an endpoint-only
intersection. This is a rounding-possibility result, not an authenticated
account of NIST's unprinted values or a physical-validation result.
No original means, standard deviations or COVs were calculated at this stage.

The original thesis was then independently transcribed, without root
transcription or output access. [Original-source transcription](thompson-independent.json),
SHA-2567f1ff93025f499e62498a5ec2c21700c0a2b3d58213cb72363dd7757b2c153b9,
pins the original PDF at
b8eff9830bcc87940c4eadc9c64b80e7381ab43c96f52b528ef773b3b0332e78.
Complete page views covered75–78,95–97,103–107. Physical and printed page
numbers agree on those pages. Approval/signature page183 was excluded from
display and use. This is an independently verified source transcription,
not a rerun of original measurements.

The original transcription retains all rows of Tables4.1–4.4:

- Table4.1:18 specimen rows at sampled approximate maximum moment, not
  automatically ultimate vertical load.
- Table4.2:nine initial-failure rows, preserving controlling specimens,
  units/precision, failure modes and footnotes.
- Table4.3:nine secondary-stage rows, including four measured stage records
  and five null stages with explicit source reasons. Null does not mean zero.
- Table4.4:18 left/right row representations for a statics sample, including
  two null5ST1 side rows. Its merged test-error cell is duplicated only for
  row-location clarity; the two sides do not become two independent errors.

Two specific source issues require explicit treatment before calculation:

1. Equation34 on original PDF78 is printed as atan(x_f/Delta), with
   x_f=78.375in; it is not printed atan(Delta/x_f). The bolt-line distance is
   74.625in and the strain-gage distance36.875in. A corrected-geometry
   conversion cannot be called a literal reproduction of that equation.
2. Table4.3 assigns its initial-tension-rupture footnote to3ST1, while
   Table4.2 calls3ST1's initial failure bolt shear. Both entries remain
   preserved. No label was silently corrected.

The parent initially instructed a pause after the user's new-production
reminder; no additional calculation ran during that pause. The parent later
authorized the TN/root comparison and a separate native-unit stage protocol,
as recorded below. No original-to-TN rotation or total-load conversion has
been performed. In particular, P=2V has not been inferred from a table heading.

At that pause, the proposed next task was to resume with the frozen source
JSONs and protocols and confirm original applied-shear versus total-load
definitions, declare any initial-only versus maximum-reported-stage candidate
and any conditional geometry diagnostic, then calculate both sample and
population variability with explicit n and missing-stage coverage. Preserve
all reported-test and figure-subset candidates; do not choose a convention
because its output happens to agree. Root comparison is a later, post-freeze
adapter. The later native-unit protocol below authorized stage summaries
without resolving or adopting a load/angle conversion. This judgment-sensitive
source mapping merits full-reasoning review,
not an unchecked mechanical data merge.

No source rewrite, new-production-folder inspection, main/legal mutation,
solver, raw-history synthesis, transmission, commit or push was performed by
this reviewer. All new artifacts remain intentional uncommitted research
work in the isolated investigation checkout.

## Completed post-freeze TN and stage-source comparison

[Comparison code](compare_tn1749.py), SHA-256
f8c0f1c5ab9e70c78ab2d47a1b8748d149778dff30a9053ea163876dabddd430,
uses the independent implementation for all arithmetic truth. The separate
root numerical module was read completely and imported only for its
synthetic-control execution/review, after the independent sources and
arithmetic outputs had already frozen.

[TN comparison01](tn1749-comparison01.json) passes, SHA-256
ae7e2b540ad7db1c26d75e29d675c443796aa90cfa9f11bb31ea68605d23de7d.
Coverage: six TN source rows/36 displayed numerical values; all12 model
comparisons; 96 exact-rational comparisons,96 decimal-render checks and459
metadata/value/disposition equalities. There are zero numerical disagreements
or failed comparisons. The largest40-significant-digit root decimal-render
error is about4.89881e-39; each rendering was checked against half its own
last displayed decimal place. Fractions were required to agree exactly.
The original plus signs on the two positive source deviations are preserved;
root omits their optional leading plus. That normalization is explicitly
recorded, including its repeated appearance in source and result fields.

The original-stage comparison independently matches all nine initial records
and all nine secondary slots: four populated secondary records and five
null stages. All26 common shear/rotation values, their source precision,
controlling specimen identities, failure labels and footnote codes agree.
Moment/axial fields and Tables4.1/4.4 have no root counterpart and are not
described as doubly transcribed or numerically reproduced. Footnote prose
was reviewed for equivalent meaning, not claimed to be verbatim-identical.

The root TN source and output pins checked by this comparison are:

- TN source JSON:2a9ed1412e592f053c4f75c6fdc001858afb55557d69d3720f04ed1bbf0d4aca.
- Original-stage root JSON:3265861472770daee4fe35df339d91a419c175a9bb793c73f225a5cd3adb07ac.
- Root code:d4ab1e687c201da7004c14314d060d0b4add6be63319b2a8e75c675a226e4e5b.
- Root result01:57c68de1adc72eba267b6138338d1113963de90c4ecb967ac12ebe486526cb9f.

All source, source-transcription, protocol and code hashes were unchanged
before/after comparison. Nine independent controls and14 root controls
were actually executed and passed. This is not full branch-coverage proof:
the root endpoint-only assertion exercises a separate local interval
classifier, not its production calculate() function. Its separately computed
1.50/1.00/50.5 fixture returns overlap and asserts only the point value50.
Likewise the independent endpoint control calls its interval helper; none
of the12 real rows yields endpoint-only overlap. Both software-control
ceilings remain explicit. Root also admits a model-box lower endpoint equal
to zero whereas the independent helper requires it positive; every actual
TN input box is positive, so that admission difference has no effect here.

## Native-unit reported-stage diagnostic, independently frozen

The parent next froze [STAGE-DIAGNOSTIC-PROTOCOL.md](STAGE-DIAGNOSTIC-PROTOCOL.md),
SHA-2567f1c6ddb2425891869c369e115c8f66eb77836cfdd2bcddbb034bc4ddfee46c4,
before systematic original-stage calculation. It explicitly permits
initial-only versus maximum-reported-stage selection, associated rotation,
all tests versus the figure subset without5ST1, sample/population variability
and secondary-minus-initial contrasts, all in the source's native units.

Independence clarification: this reviewer also briefly considered rough
mental load/2V comparisons while interpreting the original source, before
its JSON freeze. Those unverified ideas were not implemented or adopted.
The frozen JSON's broad phrase “before original-data calculation” therefore
means before systematic/code calculation, not absence of all mental numerical
exploration. The source transcription did precede root-array access, and the
stage implementation/result freeze precedes root-stage code/result access.
Neither this work nor the protocol is represented as blind historical discovery.

[Stage verifier](verify_stages.py), SHA-256
56a2b2b0552cd447c2658e6cdbb9638d008d0085445d704dd2fb4c8966c1650f,
produced [independent-stage-results01.json](independent-stage-results01.json),
SHA-25663f51024d9571d769256b567b774d8e4ee887d8020d249a72b956c377a568bbd.
The run passed10 synthetic control groups and retained12 scenarios/24
quantity summaries, plus all nine contrast records with four populated and
five missing secondary stages. All pinned inputs and code were unchanged
across the run. Mean, squared-deviation sum and both variances use exact
rationals; SD and percent COV use80-significant-digit Decimal calculations.
Source precision remains preserved in selected row records.

The maximum-reported-stage rule selects the secondary record only for4ST1
and5ST3. It retains the rotation from that selected stage, never an
independently maximized rotation. Missing secondary records remain null and
their reason codes remain attached. Absence of a reported later failure is
not proof of absence of later load reserve.

All-test versus figure-subset mean summaries are shown below in native units;
these are conditional table-endpoint summaries, not NIST global peak loads.
Sample/population variances, SDs and COVs for every row below and both
quantities are retained in the complete JSON.

| Cohort / bolts / n | Initial mean shear, kip | Maximum-reported-stage mean shear, kip | Initial mean rotation, rad | Same-stage rotation mean, rad |
|---|---:|---:|---:|---:|
| All /3 /3 | 6.2 | 6.2 | 0.1326666667 | 0.1326666667 |
| All /4 /3 | 7.3266666667 | 8.2966666667 | 0.094 | 0.106 |
| All /5 /3 | 10.8333333333 | 10.89 | 0.0763333333 | 0.083 |
| Figure subset /3 /3 | 6.2 | 6.2 | 0.1326666667 | 0.1326666667 |
| Figure subset /4 /3 | 7.3266666667 | 8.2966666667 | 0.094 | 0.106 |
| Figure subset /5 /2 | 10.955 | 11.04 | 0.077 | 0.087 |

Secondary-minus-initial changes for every populated secondary record:

| Test | Shear change, kip | Percent change from initial shear | Rotation change, rad |
|---|---:|---:|---:|
| 4ST1 | +2.91 | +41.45299145 | +0.036 |
| 5ST1 | -2.43 | -22.94617564 | +0.012 |
| 5ST2 | -2.20 | -18.81950385 | +0.014 |
| 5ST3 | +0.17 | +1.66340509 | +0.020 |

Repeated unchanged cohort rows are not independent evidence. The calculation
does not establish that NIST used the figure subset, that either stage rule
matches its underlying experimental histories, or that one rule is the
correct historical validation target. No total-load factor, unit conversion,
angle correction, Table4.1/4.4 pooling or NIST mean/COV cross-comparison was
performed by this stage implementation.

Before reading root-stage outputs, the independent comparison criterion was
declared: exact rational/source-selection equality and absolute1e-30
tolerance for high-precision SD/COV values, with maximum errors retained.
The completed comparison below applies those unchanged criteria. Existing
frozen data/results were not overwritten.

## Completed post-freeze native-unit stage comparison

[Stage comparison code](compare_stages.py), SHA-256
3ddf6349aff19cad6a0ded35c6ed6b1113eed4b4dcd0a911fa28f614d07d35bc,
was authored after the independent stage source, implementation and results
had frozen. It uses the independent implementation for numerical truth;
root's stage code was read completely and imported only to execute/review
its synthetic controls. A mistyped root-source pin in the adapter draft was
corrected before its first execution; no failed result was generated for
that textual draft. No extraction or calculation core was changed.

[Stage comparison01](stage-comparison01.json), SHA-256
1bc82e39c8d35919ae03997225e14745be1c36da24dd43be25cbb60d62f53ca4,
passes with zero failures. It checks all 12 scenarios, 24 quantity summaries,
34 selected-row instances and nine contrast records (four populated, five
null). The retained comparisons comprise:

- 84 exact rational equalities and 84 root decimal-render checks;
- 96 SD/COV comparisons, using the prospectively declared absolute 1e-30
  tolerance;
- 48 exact implied-SSE consistency checks and 268 metadata equalities.

The largest SD/COV absolute difference is approximately 8.89056510e-39.
The largest rational decimal-render error is approximately 3.62606232e-39;
each rendering was also checked against half its own last displayed place.
The root's 40-digit decimal output and independent 80-digit output thus
agree well within the declared comparison tolerance. Fractions agree exactly.
Source/protocol/code pins are unchanged before and after the comparison.
Root stage results01 and02 are byte-identical, SHA-256
aa3c5b87b1794a427d65f0ed511e35c1dcac9a5b926b8f8128f58179c18262df;
root stage code is pinned at
50faa90dfa33c74fb7de95415fd15dcd3995702769e44d6bf967ca3aaea4719f.

Schema differences are explicit: two cohort-name aliases, two quantity-name
aliases and the secondary-footnote field name. No source value, unit or
angle transformation is part of the adapter. Root group selections omit
the retained specimen/failure/source-locator detail; the common original
source fields were separately checked in the TN source comparison. Root
does not store SSE, so the 48 SSE checks derive it from each exact variance
and denominator; they are consistency checks, not comparisons against an
independently retained root SSE field. Repeated row instances are not new
experiments.

Ten independent synthetic groups and all 17 recorded root controls were
actually rerun and passed. Root controls exercise the production selection
and statistics functions, including associated rotation, tie/null handling,
sample/population distinction and rejection cases. Root contrast arithmetic
is inline in its main function and has no separate synthetic contrast test.
The four actual populated contrasts and five null cases agree independently;
the independent implementation also has a signed synthetic contrast fixture.
These checks are not exhaustive software verification, physical measurement
validation, or evidence identifying NIST's actual summary cohort.

## Independent-consumer replay receipts and current handoff

The parent executed the frozen independent TN scripts as a separate consumer.
This reviewer read the saved receipts, verified their hashes, and compared
their complete objects with the original independent runs. Each differs
only in its command/output filename:

- [TN independent consumer](tn1749-independent-root01.json), PASS, SHA-256
  097ee6c0528d9c3f160a17e7fdc88b6715c26ad55a5ab835f8339b827ff3f2df.
- [TN comparison consumer](tn1749-comparison-root01.json), PASS, SHA-256
  28bc06d4de5aa0c9790aa44c69b43cccd13b9323d5d206f77040a9a0038433c4.

The four independent Python scripts parse successfully with Python's AST
parser. The parent subsequently completed both stage independent-consumer
commands. This reviewer checked the actual saved receipts on September 13,
2026, including each complete object against its corresponding original;
each differs only in command/output filename:

- [Stage independent consumer](independent-stage-root01.json), PASS, SHA-256
  b70ed5d77dbb2467005bb13445b89dcd4ba36043ab66de36f1b19aa88d9f34f1.
- [Stage comparison consumer](stage-comparison-root01.json), PASS, SHA-256
  8197f2c0bdee1c92529f9867582e029ed5d074619345004a1d935875c82c39a4.

The two root TN outputs are byte-identical to each other, and the two root
stage outputs are byte-identical to each other; this reviewer independently
checked both pairs. These replay checks verify deterministic execution of
the frozen programs, not an additional independent source transcription.

The remaining scientific definition gate is unchanged: these native-unit
table-stage summaries do not establish NIST's raw-history peak selection,
table membership, total-load mapping or rotation transformation. No new
conversion or source inspection is authorized by numerical agreement alone.

## Bounded numerical presentation check, September 13, 2026

The parent requested a final presentation check while separate conceptual
review continued. This reviewer read the complete report and validation
documents and checked their numerical presentations against the frozen
source transcriptions and calculation receipts. Reviewed versions:

- [Report](report.md), SHA-256
  6438e8c892a6c316136ac7ce4a77eb353bc3811784dfabbf21784772ea559097.
- [Validation](validation.md), SHA-256
  1eef9a9297a480518c101563cf5d4bfb48f5a5949b1d6f331cf3046ba373eec2.

All seven displayed native-stage table rows agree with the frozen results
at their shown precision. The shared three-bolt row was checked against both
stage rules: eight row/rule comparisons and 40 numerical comparisons covering
n, two means and two sample COVs. The other omitted, unchanged cohort rows
remain in the complete 12-scenario output; the shortened presentation does
not increase the experimental count. The six TN table rows agree on all
30 shown numerical values (excluding bolt-count identifiers), including the
signs of deviations. The four stage shear percentage contrasts round to
41.453%, 1.663%, -22.946% and -18.820% for 4ST1, 5ST3, 5ST1 and 5ST2
respectively. The report's “higher”/“lower” descriptions preserve those signs.
No load conversion, angle correction or new raw-history calculation was used.

Validation's numerical denominators, comparison counts and synthetic-control
counts agree with the saved receipts. All 25 explicitly pinned artifact files
and both pinned PDF files have the stated hashes: 25 unique printed SHA-256
values because each root run pair shares a hash. The 29 distinct local linked
files exist. The original source's stated 9,973,961-byte size also matches.
The listed root-view page ranges contain 17 original pages and eight TN pages;
that is a check of the declared list's cardinality, not a reenactment or
independent attestation of another reviewer's page viewing. Acquisition-query
counts, source-review coverage, render execution, runtime package versions
and physical/source-interpretation claims were not re-audited in this bounded
presentation pass. Reading a narrative here does not expand the numerical
verification scope into source reinterpretation or legal clearance.

No numerical correction was needed in these pinned versions. Parallel
conceptual edits, if any, are outside this exact version disposition and
should not inherit the reviewed hashes automatically. Only this owned review
was updated; no root report, validation, code, frozen array, receipt or source
was modified. Evidence-falsification and source-of-truth controls kept the
reported arithmetic agreement separate from physical validation. The bounded
numerical review and all four independent-consumer receipt checks are complete.

### Final requested numerical delta check

The parent then requested a bounded check of the final presentation edits.
The current numerical disposition now applies to:

- report.md SHA-256
  e0d12644ba8cc3037705c9bc19baa08a78e522e8b44a6e655739aac75a7f68be;
- validation.md SHA-256
  5af6eca422fcc87cb42a3d1a1db8ddf764661abd4489b9daaff08bc4bfb1491e.

All six newly displayed reported COVs match the frozen independent TN source
transcription exactly: load 11.3%, 19.5%, 7.1%; rotation 3.4%, 18.8%, 9.6%,
in three-/four-/five-bolt order. The 30 previously checked numerical values
in that table were checked again in their shifted columns and remain correct.
The new paragraph expressly separates these source-reported COVs from the
native-stage calculation and does not present them as statistical equivalence,
model-bias confidence intervals or authenticated table membership. This is
transcription verification, not a reproduction of NIST's experimental COVs.

Validation's revised opening attributes conceptual review and its two wording
corrections to the separate source/inference review; it does not claim that
review independently certified numerical calculations. The publication-date
and hydraulic-hose changes do not alter the arithmetic checked here. The
previous numerical scope, counts, reproducibility limits and source-mapping
gate remain unchanged. No numerical correction is needed in these final
versions. No source reinterpretation, new calculation candidate or mutation
outside this owned review was performed for this delta check.
