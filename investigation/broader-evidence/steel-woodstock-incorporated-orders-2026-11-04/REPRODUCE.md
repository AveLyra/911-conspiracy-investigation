# Reproduce the representation checks

Use Python 3 with pypdf and the unchanged captured entities identified in SOURCE-PINS.json. The July ledger is the prior published IDENTIFIER-ROWS.json at commit35bd9f3190f2126d0aa7ab7307f4b53e3c928240; the agreement and meeting are the previously captured versions. Resolve operational media through the repository's guarded media_path.py; stop if the verified store is unavailable. Do not overwrite existing sources.

```sh
python3 verify_sources.py --december PATH_TO_7075_PDF --july PATH_TO_7076_PDF --meeting PATH_TO_PRESERVED_MEETING_HTML --agreement PATH_TO_7077_PDF --prior-ledger PATH_TO_PRIOR_LEDGER_JSON
```

The source verifier checks only captured bytes, extents and explicitly extractable locators. Manual full-face reading at 144dpi supports the separately labelled scanned wording/date/catalog observations. Rendering was read-only using Poppler. There was no OCR substitution, newly executed full-list census, native signature validation, source-copy equivalence test, physical examination or scientific experiment. A fresh download with different bytes is a separate version, not permission to replace a preserved copy.
