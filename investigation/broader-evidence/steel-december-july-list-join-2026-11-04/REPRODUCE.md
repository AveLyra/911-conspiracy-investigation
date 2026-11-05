# Reproduce the exact-label comparison

Use Python3/pypdf, the unchanged December ledger in this bundle, the published July IDENTIFIER-ROWS.json at commit35bd9f3190f2126d0aa7ab7307f4b53e3c928240, and the three captured PDFs identified by their exact hashes in SOURCE-PINS.json. The July ledger's actual source is the533-page Clearwater packet; the11-page WoodstockJuly PDF is only the separately checked paired-row counterpart. Do not substitute one PDF's hash for the other's source role.

```sh
python3 verify_compare.py --december-ledger DECEMBER-IDENTIFIER-ROWS.json --july-ledger PATH_TO_PRIOR_JULY_LEDGER --december-source PATH_TO_DECEMBER7075_PDF --july-ledger-source PATH_TO_CLEARWATER_AGENDA_PDF --july-paired-counterpart PATH_TO_JULY7076_PDF
```

The command reads inputs and prints JSON; it writes no source or ledger. Resolve operational PDFs/media with guarded media_path.py; stop if the verified store is unavailable. Keep any changed response as a separately named source version.

manual_ledger.py preserves the literal source-cell transcription and row-assembly method. Its exclusive-write generator is for a fresh directory only; do not rerun it over existing files. OCR navigation was localTesseract5.5.2/PSM6 on the seven specifically frozen Decemberlistfaces. Every accepted cell was read against its full144dpi image; images/rawOCR/PDFs stay in native research storage and are excluded from this public bundle. The arithmetic check does not prove manual reading, scientific validity or physical custody. A second reader/native table could change a reading and its downstream counts; preserve any correction separately with a diff.
