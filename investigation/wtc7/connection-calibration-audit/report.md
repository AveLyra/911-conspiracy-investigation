# Connection calibration: physical basis, fit and remaining validation

Research only, September 12, 2026 local / September 13 UTC. A bounded WP3/Q06/Q10
unit under the [charter](../CHARTER.md); not an expert report, model execution,
legal conclusion or completed investigation. The supplementary production stays
incorporated through the [material/run crosswalk](../material-run-crosswalk/report.md).
This unit audits published methods, not another raw-file intake.

## Result

NIST's connection work has an engineering and partly experimental basis, but
**calibration against another model, agreement between solvers, and independent
experimental validation are different claims**. The selected WTC 7 pages
establish the first two; they do not independently demonstrate the accuracy of
every connection's failure and residual-resistance history under the building's
actual thermal/loading conditions. This is a narrower, stronger criticism than
calling the simulation an animation or saying its supports had no resistance.

The most useful new evidence is a later NIST study with explicit experimental
comparisons, fit choices and failure-mode disagreements. It supports taking
post-ultimate connection behavior and restraint sensitivity seriously, while
not authenticating the 2008 WTC 7 implementation. A separate arithmetic audit
does **not** substantiate suspected table-ratio errors once display rounding
is allowed. Neither result identifies deliberate intervention or changes the
collapse-cause ranking by itself.

## Dependency map: do not collapse these branches

| Branch and source pin (physical PDF / printed page) | What it supplies | Unfinished link |
|---|---|---|
| NCSTAR 1-9A, 54–58 / 3–7 | Reported steel tensile data; converted/extrapolated material curves, iteratively adjusted to reproduce test behavior | Raw tests, independent holdouts and transfer from the earlier WTC steel program to particular WTC 7 connections |
| NCSTAR 1-9A, 73–76 / 22–25 | Sadek 2008 fin-spring output → fitted shell behavior/failure strain; grouping by geometry; added vertical discrete resistance | Exact original paper/tests, target arrays, group spreadsheet/outliers and location-specific calibrated input mapping |
| NCSTAR 1-9A, 77 / 26 | Reported selected LS-DYNA-versus-ANSYS agreement | Comparison identities, load histories, common inputs, numerical errors and acceptance criteria |
| NCSTAR 1-9, 529–538 / 463–472 | Code-formula ultimate capacities, bolt/stud assumptions and printed vertical-capacity ratios; a distinct ANSYS branch | Original unrounded worksheets, actual connection conditions and applicability under combined thermal/mechanical loads |
| TN 1749, 33–35 and 41–45 / 15–17 and 23–27, July 2012 / corrected February 2013 | Later component and assembly comparisons; explicit Sadek 2008 spring-law attribution; both agreement and nonmatches | Original experimental reports, untuned prediction checks and a demonstrated bridge to the WTC 7 historical inputs |

Primary reports: [NCSTAR 1-9A](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612),
[NCSTAR 1-9](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611), and
[TN 1749](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1749.pdf).
Source hashes, exact coverage and retrieval failures are in [validation](validation.md),
the [independent NIST review](nist-validation-review.md), and the
[retrospective source ledger](retrospective-context.md). Repeated publications
from the same program are not independent experiments.

## 1. What the WTC 7 calibration does and does not show

NCSTAR 1-9A describes a 6–12 inch target mesh that could not explicitly resolve
fine connection details. Fin tab material behavior and failure strain were
adjusted to match a spring model attributed to Sadek, El-Tawil and Lew (2008).
Header and knife connections were developed similarly. The source documents
normalization by weld/plate thickness, group averaging, an approximate 20-group
construction and a coefficient-of-variation guideline of 0.3, with outliers
handled separately. That guideline is not an experimental uncertainty interval
or a guaranteed error bound for every connection. (PDF73–75.)

Figures 3-4/3-5 (PDF76) compare **spring and shell models**, not ANSYS or measured
experiments. All seven 3–9-bolt pairs are present. Terminal dissipated energies
visually agree more closely than the full force-displacement shapes: the
7-bolt shell curve, for example, sustains appreciable resistance farther along
the displacement axis than its spring target. Similar accumulated energy does
not require equal force at each displacement. Different local histories could
matter to propagation, but the plots alone do not quantify a global effect.
The horizontal axis is displacement, not seconds; no failure-time difference
has been measured. No curves were digitized into replacement properties.

Two important counterweights remain:

- PDF75 explicitly adds a discrete element to supply vertical capacity missing
  from the calibrated shell representation. PDF77 includes bearing plates,
  sliding contact and discrete bolts for seated-top-plate connections. Thus
  **all residual or secondary support was omitted** is not supported by these
  pages. Which paths survive each actual failure still requires specific checks.
- PDF54–58 report ASTM tensile tests and measured steel curves, including four
  50 ksi tests with differing terminal ductility. These are real reported
  experimental constraints, although curves and failure strains were adjusted
  against those data. The report traces this material program to earlier WTC
  work; these are not demonstrated recovered WTC 7 connection tests.

Other reduced-model comparisons illustrate why acceptance must be observable-
specific. The calculated slab compression curve (PDF65) truncates before the
strain-axis endpoint, while its desired average law (PDF64) remains positive.
The coarse steel curve (PDF67) remains higher late in loading than finer meshes,
despite matching approximate failure elongation. These are model-target
differences, not experimental residuals. They point in different resistance
directions and cannot sustain a blanket claim of systematic weakening.

The [source review](nist-validation-review.md) retains the L1/L2 curve-label
and medium-mesh unit inconsistencies. The initial report also questioned the
42/44ksi descriptions, but critical review located narrowing context:
NCSTAR1-9A PDF59 explicitly supplies an Algoma44W model with44ksi yield and
75ksi ultimate strength, distinct from a few42ksi components. Its footnote
restricts that Algoma model to seats; other connection components use custom
strength models. PDF55's nominal42ksi description remains a textual
inconsistency alongside that explicit44ksi treatment and NCSTAR1-9 PDF527.
It is not evidence that the global model lacked a44ksi representation.
The exact grade-to-location/custom-card mapping still needs its own record.
PDF59 also states that the same strain-failure criterion was used at room and
elevated temperatures; that transfer is a distinct validation question, not
proof that the model ignored temperature-dependent strength.

## 2. Capacity assumptions: strength-enhancing choices also count

NCSTAR1-9 PDF529 sets design resistance factors to 1.0 to estimate ultimate
rather than factored design capacities. PDF531 excludes threads from the bolt
shear plane and raises the stated A325 shear stress from60 to75ksi, citing a
load-distribution adjustment; A490 is similarly raised from75 to93.75ksi.
These changes increase the calculated resistance relative to retaining the
stated reductions. Correctly evaluating them requires actual geometry and load
distribution, not assuming that every discretionary choice encouraged failure.
Code-derived ultimate capacity is nevertheless not a measured failure history.

The stud model uses a stated strong-position formula and adopts19.5kip in both
directions, alongside a19.4kip average of strong/weak tabulated values.
The same pages discuss neglected deck puddle welds and high vertical seat
capacity, and distinguish horizontal from vertical failure. PDF541 confines
detailed ANSYS connection failures to a selected eastern area on Floors8–14,
based on prior single-floor calculations; it says other structural damage was
modeled outside that area. That geographic choice is a sensitivity question
for that branch, not proof that the global LS-DYNA model had the same boundary.
The stud-count scaling example preserves total stated capacity, not necessarily
every spatial failure effect. (PDF534–536,541.)

### Complete printed-table check

The [arithmetic protocol](ARITHMETIC-PROTOCOL.md) includes all55 rows and9
summaries in Tables11-2 through11-4, visually transcribed twice independently
before outputs were compared. All numbers are retained, including disagreements
from direct division. Both implementations use exact rational arithmetic.

| Table | Rows | Printed mean | Mean of printed row ratios | Mean of displayed-load quotients | Point quotients outside printed-ratio rounding interval | Incompatible after declared input rounding |
|---|---:|---:|---:|---:|---:|---:|
| 11-2, tenant floor beams/girders | 22 | 4.4 | 4.400000 | 4.421157 | 9 | 0 |
| 11-3, core floor beams | 13 | 3.2 | 3.153846 | 3.155277 | 4 | 0 |
| 11-4, core floor girders | 20 | 3.3 | 3.330000 | 3.348462 | 3 | 0 |

The rounding test permits half of the last displayed unit for each input and
ratio. All55 ratio intervals have nonzero-width overlap with the quotient
intervals; none requires an endpoint-only tie. This shows **compatibility with
rounding**, not NIST's actual hidden values, weighting or rounding rule.
All three mean comparisons are compatible with displayed summary precision.
The direct quotient maximum for Table11-3 is4.9375, rather than its printed5.1;
this derives from the same79/16 row whose possible input-rounding interval
overlaps5.1. It remains visible, not silently corrected or separately counted
as a second source error. The tables use room-temperature F/H/K capacities,
not the seated-connection vertical capacities at Columns79/81. These static
connection ratios are not a floor-impact
capacity, energy budget, building safety factor or collapse probability.

The five declared formula checks give75,93.75,45.075,19.448 and19.35 in their
respective units. The bolt results and19.35 mean are consistent with the
printed75,93.75,45 and19.4. **19.448 does not round directly to the printed19.5**
at one decimal; the difference is0.052kip. The source's displayed parameters
may be rounded, but their original values were not recovered or replaced.
Unlike the table-ratio test, no parameter-rounding envelope was imposed for
this formula. This is a small retained arithmetic/precision question, not
evidence of consequential capacity error or intentional manipulation.

## 3. Later physical comparisons: useful evidence with explicit limits

The exact Sadek2008 paper is identified, but [the bounded access pass](paper-source-review.md)
did not acquire its full text. A publisher PDF route returned403/zero bytes;
the NIST and author entries did not supply a PDF link. The NIST portal's2017
date does not supersede the publisher's2008 article identity. Unavailable
methods are not nonexistent experiments.

The separately acquired **2012/2013 TN1749** expressly attributes a spring-law
form to that2008 paper (PDF35). It supplies three concrete qualifications:

1. **Experimental endpoints do not validate an unmeasured tail.** In the selected
   Rex/Easterling bolt-bearing comparison, the experimental curve stops at
   12.7mm while the simulated tearout branch continues. TN1749 explicitly
   describes substantial uncertainty in the modeled post-ultimate response.
   Richard's single-shear curve also ends before the modeled final fracture;
   its curve is a best fit to several tests, not one raw trace. (PDF33–34.)
2. **Assembly comparisons contain both agreement and failure.** The Thompson
   comparison describes nine tests, three each for3/4/5-bolt connections, with
   the same beams reused and doublers preventing beam-web bearing deformation.
   Eight histories are shown because one initial record was incomplete. The
   models reproduce broad slip/flexure/catenary stages and abrupt drops, but
   predict bolt-shear fracture throughout while the tests also show tab rupture
   and block shear. Two tests peak at a later failure rather than the first,
   unlike the model histories. (PDF41–45.)
3. **Choice informed by fit is not an untouched prediction.** Initial-gap
   treatment improves agreement, and quadratic unloading is selected because
   it agrees better than linear unloading. Axial-force agreement is weaker and
   more restraint-sensitive than vertical-load agreement. These are legitimate
   development choices to test, not automatically misconduct; the comparison
   is not a demonstrated held-out validation. Numerical bolt cooling in a
   component model imposes preload, not a physical fire experiment. (PDF34,42–45.)

This later source is primary for its own calculations and method choices,
but secondary to the original physical studies, which remain unacquired here.
No reported percentage was independently recalculated in this retrospective
pass. Its spring implementation is not a verified match to the released WTC7
cards. See [the exact conditions and reference ledger](retrospective-context.md).

## 4. Claim strength, contrary evidence and next discriminators

| Claim | Present grade and basis | Strongest qualification / concrete next test |
|---|---|---|
| The displayed WTC7 fin-shell models were calibrated to spring output, not independently measured in Figures3-4/3-5 | A: explicit primary method and correctly labeled plots; two source readers | Supply original spring experimental lineage and genuinely unused validation cases; do not treat fitted agreement as worthless |
| Selected model-target curves differ despite broadly matching energy/failure measures | B: full-page qualitative observations, no digitized error estimate | Exact paired curves and declared observable-specific error/sensitivity analysis could show differences negligible or consequential |
| Table-ratio discrepancies prove bad arithmetic | E as stated: all55 rows compatible with the declared rounding possibility | Unrounded source worksheet could resolve or expose actual inconsistencies; passing interval overlap does not authenticate it |
| Connection behavior was wholly ungrounded experimentally or all support omitted | E as a blanket claim: reported tensile data, later experimental comparisons, springs and bearing/contact are contrary evidence | Audit each actual member/failure path instead; physical transfer and post-failure adequacy remain D/underdetermined |
| Later tests show a particular WTC7 failure law was correct or incorrect | D: later fit/nonmatch evidence with an unverified historical link | Acquire originals, map implementation/version and test relevant geometry, thermal/load history, restraint and post-ultimate response |

Grades describe the stated proposition and scoped evidence, not numerical
probabilities. A=directly established; B=strong within the stated domain;
D=underdetermined; E=unsupported/contradicted in the stated blanket form.
All computational repetitions share their source inputs and are not extra
physical witnesses.

The June2025 manifest contains25,643 rows and no Excel-format extension; it
does contain presentations, archives and other formats. An inventory-only
extension check therefore **does not establish that the capacity spreadsheet
or its data were never released**. The exact location/group/outlier/calibration
mapping is unidentified by this check. Main/raw sources were not modified or
new payloads executed. See [validation](validation.md) for manifest coverage.

The next finite source task is the original Thompson2009 assembly-test record:
resolve its full reference, test protocol, raw/processed histories and failure
labels; compare its reported numerical tables with TN1749's tables under a new
frozen all-row protocol. Rex2003/Richard1980 and the exact2008 spring paper remain
specific separate leads. None authorizes a solver, replacement property law,
paid access, outreach, legal amendment or sensitive transmission.

The current conclusion is **specific limits on validation, plus concrete
experimental leads**, not a demonstrated fire-to-global-collapse chain, proof
against all fire pathways, or affirmative evidence of an intervention. This
unit changes how strongly particular validation claims can be stated; it does
not assign a new causal ranking.
