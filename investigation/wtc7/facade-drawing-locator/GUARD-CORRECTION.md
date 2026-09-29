# Prospective archive-guard correction

2026-09-24. Independent synthetic testing found that the original locator
checked legacy ZIP64 sentinel fields, but not the preceding ZIP64 locator.
Python's ZipFile can use that locator even when legacy fields are ordinary,
and then use a different, over-cap directory size. The original general
ZIP64/cap enforcement claim was therefore false. This is our local tool defect,
not an agency-record anomaly or a historical-data finding.

Preserve `run01`, `run02`, `identifiers01` and their original receipts.
`source-v1/` preserves the exact original implementation bytes; these snapshots
are historical source, not runnable alternatives with their own data roots.
Original locator SHA256:
`eff900720a56dbf026df8f9dcc60571803b7ece70f04ff1d8a4918279f64aa8d`.
Original identifier wrapper SHA256:
`e77b6eff0b58ecb66e1b8914735abd8e4217978ddc92853766356ceffeccd116`.

The revised producer reads at most20 bytes immediately before the absolute
EOCD offset and rejects the ZIP64 locator signature before opening ZipFile.
Reading relative to the file offset, rather than just the bounded tail,
also handles a maximum-length EOCD comment. Existing sentinel/count/size/
multi-disk/ambiguity and pending-packet guards remain. No payload is extracted.

The explicit *unopened* other-container suffix set additionally includes
`.iso`, `.zst`, `.lz4`, `.cab`. This does not identify every container format,
extensionless object or misleading suffix. `rg` does not follow directory
symlinks and omits file symlinks; the direct symlink guard is not a symlink census.

Before relying on the revised code, rerun the independent guard/predicate
fixtures, including the nonsentinel ZIP64 case and a long-comment boundary.
Use create-only `run03/run04` and `identifiers02/identifiers03` for revised
production repeats. Compare source identities, paths, metadata, name matches
and output bytes with their preserved predecessors. Do not silently rehash
old receipts or call old runs corrected. The independently written metadata
reader had already excluded preceding ZIP64 locators before its first freeze;
its historical-input comparison is a separate check, not a universal proof
that every possible archive is handled safely.

Residual implementation limits are explicit: the entry-count precheck uses
EOCD declarations, while a malformed central-directory count is rejected only
after ZipFile parses it. This is not a hardened hostile-archive service. The
finite current inputs also receive independent actual count/size checks.
Integrity hashing reads compressed source bytes; the legacy status string
`members_listed_no_payload_read` means no member payload was decoded,
extracted or interpreted, not that compressed bytes were never read.
Identifier predicates are permissive locators, not exact entity authentication;
prefix/suffix false positives require review, and no observed match is silently
joined to the named drawing set.
