> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../README.md).

# Equipment follow-up: validation and review disposition

2026-09-11. Research-only closeout of this bounded source follow-up, not completion of the investigation. [Selection](SELECTION.md) and [acquisition log](acquisition-log.md) preserve source identity, navigation limits and failures.

## Source and reading coverage

- Root read the equipment cover separately, then all text and complete images of 30 selected NCSTAR 1-1J pages: 3–5, 9, 33–35, 45–47, 51–52, 55–56, 59–61, 65–66, 69–70, 75–83. The complete 84-page text extraction was a locator, not an 84-page reading attestation.
- The inventory reviewer read its separately selected 30 equipment pages and eight preserved N9/1A comparison pages. Root read its final report and arithmetic helper, not every additional comparison page again.
- Root and the errata reviewer each inspected both complete errata pages, including struck-out and inserted text. The combined critical reviewer additionally read 13 equipment pages and three N9 pages. These are computational-agent readings of the same source family, not independent historical corroboration.
- Root's fresh N9 reading in this follow-up covered extracted text on physical pages 435, 438 and 440; root's complete visual N9 inspection belongs to the preserved parent audit. Do not conflate the two.

## Reproduction actually completed

The equipment receipt (historical local reference `root-reproduction/receipt.json`; not included here) records 30 fresh PNGs identical to the root reading derivatives, all 1,700 × 2,200, and 30 identical fresh page-text extractions. Both render sets had zero captured stderr bytes. The errata receipt (historical local reference `root-reproduction/errata-receipt.json`; not included here) records two root rerenders identical to the reviewer's PNGs, both 1,701 × 2,200, with zero captured stderr. Source hashes remained unchanged. Repeated rendering verifies a transformation, not the source's physical claims.

Environment: bundled Python 3.12.14, pypdf 6.10.0, Pillow 12.3 and Poppler 26.05. Rendering used `-scale-to 2200 -png`, the existing `fire-coverage-extension/fonts.conf`, and explicit `FONTCONFIG_FILE` and `FONTCONFIG_PATH`. The inventory renderer (historical local reference `inventory-review/render_review.py`; not included here) and errata renderer (historical local reference `errata-review/render_review.py`; not included here) preserve the exact source/command forms. Use fresh output directories for reproduction; these reviewer scripts write their own receipt paths and must not be rerun in place to overwrite historical attestations. The first unconfigured cover render produced warnings and an incomplete locally preserved stderr record; it is excluded from accepted fidelity checks. That failure is retained in the acquisition log.

The [root arithmetic receipt](root-reproduction/inventory-arithmetic-receipt.json) independently checks the reviewer's Decimal results with integer-tenths addition and exact rational arithmetic. Table inputs, in printed order, were:

```text
Salomon, tenths of a gallon:
120000,225,1461,349,199
Base including tenant systems, tenths of a gallon:
240000,317,220,500,10,576,2750,21,262,2750,21,109,60000,116,169,2750,12,21
```

Sum each list and divide by 10: 12,223.4 and 31,060.4 gallons, totaling 43,283.8. For conversions use exact liters-per-gallon fractions 3785411784/1000000000 and 454609/100000. Multiply by 70/60 for L/s, or by 12, 23 and 1 for the stated cubic-meter checks. Eight outputs matched the reviewer within 10^-25, allowing finite Decimal rounding of recurring fractions. This reuses the same visually transcribed source inputs; it does not authenticate stock, pumping or model values. All 39 entries in the inventory reviewer's final artifact manifest were also freshly hash/size checked without mismatch.

## Review disposition

1. Combined reviewer: no material overclaim in its tested control/thermal chain. Added direct physical-page pins and selection link to EC07 and its report paragraph. The negative finding remains confined to reviewed sections; later closure of a 2005 gap is not ruled out.
2. Inventory reviewer: incorporated the two memberships yielding three tanks/600 gallons and the declared gallon-convention arithmetic. Preserved the distinction between a compatible numerical pattern and actual historical/model inputs. Root additionally qualifies the reviewer's characterization of the earlier parent report: the parent flagged reconciliation, not a uniquely proved tank membership.
3. Rejected reviewer error: original page 60 says 6,000, not 6,600 gallons. Reinspection corrected the preliminary messages; no source discrepancy or rated-versus-usable theory is adopted.
4. Structural propagation: appended a dated correction to SC01 in the earlier structural audit. The historical 11-inch/5.5-inch quotation is explicitly superseded by the published 12-inch seat/6.25-inch lateral correction, distinct from 5.5-inch axial travel. NIST's claim that models already used corrected values remains an assertion awaiting input verification. Original source/derivative/reviewer attestations were preserved.

The combined review's earlier report/ledger hashes attest to the pre-integration snapshot. They are not relabeled as a review of later text. No solver, equipment transient, fire experiment or physical reconstruction was executed. No bridge, disclosure, legal promotion, commit or push occurred.

Final scoped integrity checks passed for 16 Markdown documents and 137 local link targets, with no missing targets, trailing whitespace or conflict markers. Seven preserved source/review pins and 62 root equipment/errata image hashes matched. The generated `root-reproduction/final-integrity-receipt.json` records those checks. Scoped tracked `git diff --check` and `python3 tools/validate_record.py --strict` passed; the latter checks record headers, issue/fact links and citation tags, not scientific validity. This paragraph records the check outcome without changing link targets. Unrelated working-tree changes were not reviewed or cleared.
