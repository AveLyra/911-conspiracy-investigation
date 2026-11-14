# R08 NIST native workbook recovery — 14 November 2026

Start with Scooby_R08_Native_Recovery_Audit_2026-11-14.html. All six original NIST XLSX files are in native/. They total 170,176,394 bytes. Stable acquisition aliases are mapped to exact official filenames and URLs in provenance/native_file_manifest.json. No native workbook was changed.

The source-access gate passes. No structural model ran. A full quantitative thermal/damage benchmark still requires explicit physical channel-validity windows, clock alignment and thermal/material assumptions; see audit/gate_evidence_notes.md.

## Verify without a network

From this extracted directory:

    python3 scripts/verify_bundle.py

SHA256SUMS.txt hashes every delivered member except itself. The independent direct ambient URL retrieval matched the canonical route hash; its duplicate bytes are omitted.

## Repeat the audit without modifying sources

    python3 scripts/inventory_native.py --input native --out rebuilt_inventory
    python3 scripts/audit_primary_time_and_export.py --input native --out rebuilt_inventory
    python3 scripts/finish_inventory.py --input native --out rebuilt_inventory
    python3 scripts/build_channel_crosswalk.py --native-dir native --retrieval-manifest provenance/direct_get_attempts.json --output-dir rebuilt_map

The inventory uses Python standard-library ZIP/XML parsing. Source values, formulas, caches and comments remain separate. A formula follower with empty f text may refer to a shared-formula master; inspect the shared masters ledger. Derived statistics and range/clock/alias interpretations are not native cells.

## Re-fetch original official routes into a NEW directory

    python3 scripts/recover_nist.py --out fresh_http

Compare downloaded bytes with the manifest before treating them as this archived version. This script uses only ordinary official NIST routes and records redirects and HTTP outcomes. It does not use third-party mirrors or bypass access controls.

The matched-pair CSV.gz exports retain source Excel row numbers and original lexical values; cached values in formula cells are accompanied by the source formula ledger. Other three fire workbooks are fully inventoried and included unchanged; no duplicate whole-data CSV is required to recover their values.

The illustration PNGs are optional derived previews of original EMF members (or unchanged embedded PNGs), not digitized measurement plots. Ambient figure B1(d) renders incompletely in Inkscape; consult the untouched embedded original. Rendering, visual-review annotations and assembly scripts preserve the original r08_work staging-path convention and can be adapted without changing sources. The documented CLI commands above are directly portable.

The 13 November prior artifacts are retained for history and are superseded as to file access. The full source/reference/HTTP manifests distinguish successful bytes from tool parser errors and earlier failed routes. No external contact, request, payment, Deep Research, structural model, calibration or holdout run occurred.
