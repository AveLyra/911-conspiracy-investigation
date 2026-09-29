# Independent capacity-table and arithmetic verification

Research derivative, 2026-09-12. Numerical comparison PASS within the scope below.
This is independent source transcription and arithmetic by a separate agent,
not an independent engineering laboratory, professional certification, or a
validation of WTC 7 collapse physics.

## Source and independence

The controlling source is the preserved [NCSTAR 1-9 PDF](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf),
SHA-256 30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f,
797 physical pages. Full-page views at 120 dpi covered physical pages 529–538
(printed 463–472), including all page headings, equations, explanatory text,
figures and table continuations. PDF text extraction was an auxiliary
transcription aid, not a replacement for the page-image review.

The independent transcription contains all 55 data rows: Table 11-2 has 22
(16 on physical page 536 and six on 537), Table 11-3 has 13 on 537, and Table
11-4 has 20 on 538. All nine printed average/minimum/maximum summary values
were included. No row was selected because its quotient looked discrepant.
Every failure load is printed as an integer; the one-decimal design load
73.4 kip is retained as such, and every printed ratio has one decimal place.
Member-name capitalization, engineering failure modes, region labels and
source page are preserved in the independent JSON.

This is exploratory follow-up: the table choice followed an observation that
some displayed divisions appeared discrepant. It is not preregistered anomaly
discovery. Nevertheless, the independent source transcription was frozen and
its hash sent to the parent before viewing any root transcription, arithmetic
results or implementation. The independent arithmetic implementation and first
successful result were also frozen before reading root values. The later
schema adapter was necessarily written after viewing the root output structure.
No root calculation function was imported or copied.

Frozen pins:

| Artifact | SHA-256 |
|---|---|
| [Source transcription](capacity-independent.json) | 8a0f3c8bece01776289265d5db5b316032321c7eae70bf7ad8e80d045e4d4b00 |
| [Independent arithmetic code](verify_capacity.py) | 59f3da69a009c98c8fdd1d5e8f6fdef2ff3e3ec1bdd36afa9c22bf155b38b5da |
| [Independent arithmetic receipt](capacity-independent-results01.json) | 2aa98dff2474c38d7b0ed674999df7be1886437a65c2294ee6e3a23d7394b165 |
| [Arithmetic protocol](ARITHMETIC-PROTOCOL.md) | 32b68c94b0a5c60edcc4e3689f1b742aca1666d086b3bffdad3fff5384524e3b |
| [Unit protocol](PROTOCOL.md) | 7bf240b13ff1141ce9d69381d1dcc1ac17cb2c917b4f7e11800f01ba70d28247 |
| [Post-schema comparison code](compare_capacity.py) | 3041ee0e2f77351eb357ae8968e89433da5b146a1be9476671daba495e2cf51d |
| [Final comparison receipt](capacity-comparison02.json) | 97636eda01c2e100d04c1480249282391f66ceda7852f68e548557647f80df77 |

## Exact arithmetic result

Calculations use rational numbers parsed from the displayed decimal strings.
For each positive failure-load interval and design-load interval, the quotient
minimum uses the lower numerator and upper denominator; the maximum reverses
those choices. The interval intersection test is exact, with closed endpoints
and endpoint-only matches explicitly retained.

There are 16 displayed-load quotients outside the printed ratio's closed
plus/minus 0.05 interval: nine in Table 11-2, four in 11-3, and three in 11-4.
The same 16 differ under the separate nearest-one-decimal, half-up diagnostic.
Rows are:

- 11-2: 2, 8, 9, 12, 14, 15, 16, 18, 22.
- 11-3: 1, 2, 9, 11.
- 11-4: 1, 10, 11.

Under the declared display-rounding possibility (integer load plus/minus 0.5,
one-decimal load plus/minus 0.05, one-decimal ratio plus/minus 0.05), **all 55
rows have nonempty quotient/printed-ratio interval intersections**. None of
those intersections is endpoint-only. This result disproves the narrow claim
that these row discrepancies cannot be accommodated by those display boxes.
It does not identify the actual unrounded numbers, authenticate NIST's rounding
discipline, or prove that rounding actually produced the discrepancies.

All summaries below are unweighted across table rows; no connection-population,
load, floor-count or other weighting is inferred.

| Table / row count | Printed average / min / max | From printed ratios: mean / min / max | From displayed-load divisions: mean / min / max |
|---|---|---|---|
| 11-2 / 22 | 4.4 / 2.3 / 6.7 | 4.4 / 2.3 / 6.7 | 4.4211571462 / 2.2615803815 / 6.6666666667 |
| 11-3 / 13 | 3.2 / 1.9 / 5.1 | 3.1538461538 / 1.9 / 5.1 | 3.1552774993 / 1.9 / 4.9375 |
| 11-4 / 20 | 3.3 / 2.2 / 7.2 | 3.33 / 2.2 / 7.2 | 3.3484620060 / 2.17 / 7.2333333333 |

All nine statistics computed from printed row ratios round to the corresponding
printed summaries under the declared half-up diagnostic. Eight of the nine
statistics from displayed-load quotients do so. The exception is Table 11-3's
maximum: displayed 79/16 gives 4.9375, not the printed 5.1. That source row
is nevertheless interval-compatible when both displayed loads are allowed
their declared rounding boxes. A summary mismatch is not silently erased by
that compatibility result.

Five surrounding arithmetic statements were independently reproduced:

| Source physical page | Displayed expression | Exact result | Printed result | Assessment of displayed arithmetic |
|---|---|---|---|---|
| 531 | 60 / 0.8 | 75 ksi | 75 ksi | Exact |
| 531 | 75 / 0.8 | 93.75 ksi | 93.75 ksi | Exact |
| 531 | 0.601 × 75 | 45.075 kip | 45 kip | Agrees at printed integer precision |
| 534 | 0.68 × 1.0 × 1.0 × 0.44 × 65 | 19.448 kip | 19.5 kip | Would round to 19.4 at one decimal under half-up |
| 535 | (21.5 + 17.2) / 2 | 19.35 kip | 19.4 kip | Exact half-step, consistent with half-up |

The shear-stud formula differs by 0.052 kip from the printed result; the exact
displayed product is 0.002 kip below the lower boundary of a closed rounding
interval for 19.5. This is a limited printed-arithmetic discrepancy, not a
demonstrated error in the underlying physical strength. Engineering parameters
were not assigned the table-load rounding boxes, and no alternative unprinted
area or parameter was substituted to make the expression agree.

## Direct source-method implications

- **Calculated failure loads, not measured specimen capacities.** Physical page
  529 / printed 463 says these capacities use AISC LRFD provisions with
  resistance factors set to 1.0. Page 535 / printed 469 says the connection
  evaluations here use room-temperature material properties. Reproducing the
  capacity/design-load ratios does not reproduce high-temperature, dynamic,
  coupled-connection or full-building performance.
- **Bolt-stress adjustment is an assumption-dependent analytical step.** Page
  531 / printed 465 raises the A325 nominal shear stress from 60 to 75 ksi by
  dividing by 0.8, and applies the analogous adjustment to A490. The text bases
  this on asserted even load distribution among shear-connection bolts, in
  contrast to a splice-connection reduction. It also assumes threads are
  excluded from the shear plane and calls that conservative. This review
  records those claims; neither the label “conservative” nor correct arithmetic
  independently validates their applicability to the modeled connections.
- **Stud strength includes averaging and directional transfer.** Pages 534–535 /
  printed 468–469 distinguish strong and weak positions, describe conditional
  geometry/placement factors, and cite an external prediction and AISC values.
  The report averages 21.5 and 17.2 kip because a stud could be placed on either
  side of a rib, then chooses 19.5 kip for both parallel and perpendicular
  loading to deck ribs. The page-534 claim about agreement with published
  experiments is a source attribution; this bounded check has not inspected
  those experiments, their specimen counts, residuals or holdout status.
- **The three tables are not an all-connections validation set.** Page 535 says
  the STC/STP seated connections at Columns 79 and 81 were evaluated only for
  horizontal failure because their vertical seat capacities exceeded the
  reported vertical loads. Page 536 distinguishes horizontal failure modes
  from vertical ratios and says a horizontal design-load comparison was not
  available. Thus these fin/header/knife vertical ratios do not by themselves
  test the proposed horizontal initiation mechanism or the seated-connection
  capacity at Column 79.
- **The modeling handoff still needs its own evidence.** These Chapter 11
  calculations do not authenticate a particular released LS-DYNA material ID,
  transfer spreadsheet, spring law, calibrated failure energy or historical
  run. Numerical agreement here cannot fill those prior record gaps.

Strongest supported conclusions are the source transcription (observed report
content) and the exact arithmetic conditional on it (derived, independently
reproduced). The assertion that rounding actually explains the source values
remains underdetermined; the assertion that this verifies real connection
failure or identifies a collapse cause is unsupported by this test. The useful
next records are the original precision-preserving capacity calculations and
their connection/location mapping, plus actual test/calibration provenance
with geometry, loading, temperature and independent evaluation conditions.

## Independent comparison and preserved failures

The final adapter checks all 55 rows and their 165 displayed load/ratio
strings, source pages, row IDs, engineering member/connection identities,
displayed precision, nine printed summaries, 18 mean/min/max calculations,
and five formulas. It checks each quotient, signed difference (with the
root/independent sign convention explicitly reversed), quotient-box endpoints,
printed-ratio endpoints, overlap endpoints and dispositions.

Result: **468 exact-rational comparisons, 806 metadata/value/disposition
equalities, and 468 fixed-16-decimal rendering checks pass; no numerical
disagreement.** The largest root decimal-render error is exactly
3/60500000000000000, about 4.95868e-17, below the declared 5e-17 bound.
The exact-rational comparisons use no floating tolerance.

The root source transcription hash is
476051df3c2c58689b8dccc20a8a6a6f3ba9d246cca1445ca1d0a40596eebcf4.
Root results 01 and 02 are byte-identical, both
02fe6a43dab1f66d4994c855ae69d3620748aeff15fd1e8a8dbff00675246a6b.
All compared input, source-PDF and implementation hashes were checked before
and after the final comparison. The comparison re-executed all ten independent
arithmetic control groups and regenerated the independent result object for
exact equality. It checked the root's recorded count of 14 control groups,
but did not execute or independently inspect those root control definitions.

Source-label differences are not concealed as exact text agreement:

- Root normalizes uppercase X, abbreviates some floor labels, inserts “Core”
  in some group aliases, and changes punctuation/case in the 40-inch girder
  label. All are explicitly recorded in the comparison receipt.
- Four root rows in Table 11-4 add “Beams” to the printed South/North Floor
  labels. That addition is not supported by the source, whose table title
  identifies core floor girders. It does not alter the matched numerical
  rows. The frozen root files are retained, not silently corrected.
- Failure-mode labels are independently transcribed from the source but are
  absent from the root schema, so they cannot receive a two-transcription
  agreement claim.

Two failed execution stages remain visible:

1. The first arithmetic execution finished computation/hash checks but failed
   at receipt creation because the shell sandbox did not permit writing this
   isolated worktree. [Failure receipt](capacity-independent-failed01.json)
   records the actual traceback stage and its provenance limit. The same
   command/code succeeded with scoped worktree-write authorization. No output
   from the failed attempt was represented as a saved numerical receipt.
2. [Comparison 01](capacity-comparison01.json), SHA
   ef14e2099949c397a42c2a9bad549fa716c3bd2fa9e00e2af81d271587bbc007,
   failed 21 equality checks because the adapter had not yet accounted for
   the added “Core” aliases and 40-inch girder punctuation/capitalization.
   All 468 rational and 468 decimal checks already agreed. Its field
   “exact_rational_disagreements” was also incorrectly named: it counted all
   nondecimal failures, including these aliases, not 21 rational disagreements.
   The [exact earlier adapter](compare_capacity-before-alias-review.py) is
   preserved at SHA
   e34491f8f87ad1cde091bf1d631119de8316687819359ccd29920fa5ddc002cd.
   Only alias handling and the failure-counter distinction changed before
   comparison 02. Neither transcription nor the arithmetic core changed.

Two initial tool invocations to author the adapter/review had JavaScript
quoting syntax errors before any file operation ran; no candidate code or
result was produced by those invocations. They did not affect the data or math.

## Reproduction

From the isolated worktree, use the actual bundled Python:

~~~sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/verify_capacity.py --output capacity-independent-root01.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/compare_capacity.py --output capacity-comparison-root01.json
~~~

Both commands create only a new named receipt and reject existing output
basenames. The parent has been given these commands for consumer reruns;
completion of those reruns is not yet asserted here. No browser test applies
to this command-line exact-arithmetic check. AST parsing passed for the
independent arithmetic implementation. Original PDFs, legal/canonical records,
prior research units and source files were left unchanged; no solver,
property replacement, publication, transmission, commit or push was performed.

### Subsequent root consumer execution

Root subsequently read both complete implementations and ran the independent
arithmetic as `capacity-independent-root-replay02.json` and the final adapter
as `capacity-comparison-root01.json`. Both returned PASS. Direct comparison
shows exact equality of their result/comparison objects with the independent
initial/final receipts; only command/output-name fields differ. See
[validation.md](validation.md) for the exact receipt hashes. This closes the
pending parent-replay item above, not physical validation or additional blind
transcription. The earlier reviewed version's hash remains historical.
