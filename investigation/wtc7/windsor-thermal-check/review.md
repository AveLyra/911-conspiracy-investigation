# Independent final report wording/source review

2026-09-20. Research-only review under the evidence-falsification and
source-of-truth controls. Only this file is written; both reading freezes,
code, outputs, source and prior derivatives remain unchanged.

## Actual scope and reviewed versions

Read the complete report, both frozen notes and calculation02.json. Used my
previously recorded 13-page complete visual reading and independent Ruby
calculation; no new page display, text extraction, acquisition, network or
solver. This is a source/wording review, not a fresh rendering-integrity audit,
historical reconstruction, software certification or whole-investigation pass.

| Artifact | SHA-256 |
| --- | --- |
| report.md | `851d44df525eecd12b65c8aa8acc0fe3446484c2c908b10f18eb532005c82ddd` |
| observer-notes.md | `703d1ca458bb86f8112cdf9e1367da3a5302712f2aeec4b23a647fa17f73dccb` |
| root-notes.md | `d85fc9a3767a009abf1642205fe6cad5a921bfd5273ecc976fd44560db7d32b1` |
| calculate.py | `61c28ab16f55a2c9ba1003ea57ccc089f8c6f3bf5c26ed5fc26403fa58c6dbf7` |
| calculation02.json | `f27147daca48b0b99c69d6cf025d9eb670925f1d9c15911b5d8277b7fb25e8f8` |
| PROTOCOL.md | `d02efad11d2008aa65536547510d78110daae974693d4291d6c07c359573db05` |
| SCOPE-EXPANSION.md | `063d4c02ca135382ebab6c71ce3b005f29ba946acd5f16f59d2d7b85bae6f147` |

Actual checks: complete `sed` reads and `shasum -a 256` checks exited 0.
A fresh Ruby Rational calculation gave
`(58^2/1400)/(50.3^2/3600) = 3.41896363935`; one bounding assertion passed,
exit 0. This ratio compares the two printed depth/time pairs, not the time
ratio between the figure-normalized curve and the hypothetical multiplier-2
curve. It agrees with the frozen independent arithmetic.

The earlier post-freeze comparison (not repeated as a new test here) inspected
the entire current code/output, reran
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 calculate.py --test` with
9 tests OK, and independently checked the hypothetical multiplier-2 results
with Ruby. The current code/output hashes still match that comparison.
Integrity replay and the report's 23-input receipt claim belong to the separate
integrity/root verification; this wording review does not independently
reperform or enlarge those checks.

## Result: no material correction required

- **Definition boundary:** The opening explicitly conditions the inconsistency
  on the same-depth interpretation, and the table adds the same time origin.
  It does not assume that two definitions were actually used. Missing criteria
  and a possible convention switch remain an unresolved explanation, not a
  recovered author method. The ordering argument is kept separate from the
  conditional square-root diagnostic.
- **Numerical boundary:** The report's 4786.55 s and 4704.38 s reproduce the
  frozen calculations and are expressly not proven corrected thresholds.
  The hypothetical 1475/1450 s convention is labeled post hoc and is checked
  against its incompatible 90.60 mm one-hour result. The roughly 3.42 ratio is
  now attached to the correct two printed squared-depth/time normalizations;
  it does not perpetuate the frozen root note's ambiguous curve-comparison
  phrase. No freeze should be rewritten to conceal that clarification.
- **Geometry/page boundary:** Five endpoint-inclusive nodes/four gaps are
  identified as an interpretation, not native ABAQUS settings. P12 supplies
  the 230 mm assembly, node count and spacing. The report does not repeat
  root's minor cover locator error: the clay-plus-concrete cover idealization
  is on p8, whereas beam dimensions and fixed/pinned end assumptions are on
  p9. Mechanical support assumptions do not establish Figure 4's thermal
  boundary conditions. No extra cover or geometry claim is needed here.
- **Observed/modelled boundary:** Figure 4's depth is not substituted for the
  separately specified local 500 C damage isotherm. The report retains the
  geometry/multi-sided-heating and post-fire-inference qualifications. It does
  not assign a literal thermal first-arrival front or steel-failure threshold.
- **Error/cause boundary:** The general resolution concern is not promoted to
  measured error, a universal error sign, convergence at 10 mm, or adequacy
  after a nominal crossing. Actual profiles, mapping/interpolation and
  convergence comparisons remain necessary. Neither Windsor's failure
  sequence nor a WTC7 hypothesis ranking is inferred.
- **Grades and preservation:** A is limited to source observations and bounded
  arithmetic under stated assumptions; C to conditional diagnostics; D to
  unresolved model claims; E to unsupported misconduct/causal extensions.
  These are appropriately proposition-specific, not author-guilt grades.
  The report preserves the scope expansion, prior-informed independence,
  original failures and frozen records. My p10 crowded-expression qualification
  remains in the observer freeze; the report makes no fresh exact-transcription
  claim about that unrelated expression.

## Narrow next source option, not performed

Before extending this finding from the 2007 draft to the later publication,
an authenticated **2008 edition equivalence check** is the next bounded source
test: verify title/authors/version provenance, then inspect the complete pages
corresponding to Figure 4 and the adjacent material-property, spacing and
1400-second passages, together with any relocated definition/correction.
Record whether numbers/definitions persist, change, or are absent. A changed
criterion/value could resolve the draft discrepancy; unchanged text would
extend only the same limited textual finding, not establish executable model
error. No URL, DOI, contents, correction, or availability of that edition has
been independently verified in this review, and no acquisition is authorized
or performed by this note. The current report already correctly keeps that
edition an unreviewed lead.

## Completion version check

The report gained its execution-and-limits link during review completion.
Read the resulting complete report as well, SHA-256
`1a124e0c41ea2a1b53c214fd07dc1173b8fae42c6b6dcb44d274cd5a1192395c`.
The scientific wording is unchanged and the same no-material-correction result
applies. The frozen-note and code/output hashes above remained unchanged.
