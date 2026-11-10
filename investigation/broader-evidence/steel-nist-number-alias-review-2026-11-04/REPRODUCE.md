# Reproduce the qualification and sensitivity arithmetic

Python3 and pypdf are required. Use the exact earlier December ledger at commit9e9940b96d779c882699c9567be5276a51946c07, the unchanged July ledger at commit35bd9f3190f2126d0aa7ab7307f4b53e3c928240, the separate candidate in this bundle, and the two public PDFs pinned in SOURCE-PINS.json.

```sh
python3 verify_review.py --original-ledger PATH_TO_PRIOR_DECEMBER_LEDGER --candidate DECEMBER-QUALIFIED-CANDIDATE.json --july-ledger PATH_TO_PRIOR_JULY_LEDGER --nist-pdf PATH_TO_NIST3B_PDF --court-pdf PATH_TO_COURT7075_PDF
```

The command is read-only and prints JSON. It verifies source hashes/extents, prior/candidate/July hashes, exactly two changed research rows, retained earlier values and both count calculations. It does not inspect source glyphs or prove scanned table semantics. Allother earlier rows are preserved, not independently certified.

Rendering: Poppler fullNISTfaces33/94/95 at144dpi, fullcourtface9 at144and288dpi, completeA5table and courtbottomregion at288dpi. Raw media/PDFs stay outside this public bundle. Ordinary small public technicalPDFsource remains in deliberate localdocument storage; newrasters use the verified Intel store through media_path.py, with no localmedia repopulation or recoveryfallback. Do not alter any source, run hidden macros, infer a missing prefix, or replace a preserved ledger with the candidate. A better copy/independent reading could change the candidate; preserve that as a new version with a diff.
