# Released-input curve dependency search

September 13, 2026. Prospective for this search, following the completed
Case A/spring audit. That audit's missing LCD602/LCD803 references and prior
June thermal-source inventories are known, not blind discoveries. The
investigation charter controls. This is a bounded WP3/Q10 source test, not
a solver run or a new causal ranking.

## Question and source coverage

Can other already released numeric inputs supply the actual definitions of
the two selected LS-DYNA spring references? Distinguish an explicit curve or
table definition from a same-number ANSYS material/node, an arbitrary literal,
an executable generator, and an authenticated input/run relationship.

Scan the three APDL files selected by the preserved June-production manifest
and every non-directory, non-PNG member of its thermal ZIP. Scan the remaining
September inputs SRC116, SRC117 and SRC118 in full. The earlier independent
SRC119–121 curve/family results remain fixed read-only dependencies; do not
rerun their completed scientific calculations. Together these cover the
already inventoried June numeric package and all six September keyword
inputs, not every agency record or every file on the computer.

The June manifest is
`/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv`,
SHA256 `30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`.
Its source root is the preserved `ResponsiveFiles for DOC-NIST-2024-000233 -
Interi20250605122539` directory. Thermal ZIP SHA256 is
`2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181`.
Use manifest byte/hash pins for the three APDL files and archive members;
keep original ordinal and name hash without emitting embedded paths. Prior
census: 25,639 archive entries, five directories, 272 PNG bodies excluded,
25,362 non-PNG bodies and three APDL files. This is a coverage expectation,
not permission to omit an unexpected entry or force an observed count.

September compressed pins, in SRC order:

- SRC116: 5,331 bytes, SHA256
  `982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da`.
- SRC117: 103,872 bytes, SHA256
  `aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273`.
- SRC118: 2,702,040 bytes, SHA256
  `51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447`.

Prior selected spring result `../c79-casea-spring-audit/casea-root01.json`
SHA256 `27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2`;
independent full family inventory
`../c79-casea-spring-audit/independent-definition-presence01.json`, SHA256
`7377187b71fe0fc10a5483ed80424499555270708d02a61d2d2a991c14a939c7`.
The underlying three-stream gap is already independently verified; this
extension must not be counted as independent historical evidence.

## Detection and interpretation

Read every selected body to EOF and retain its byte count, SHA256, physical
line count, NUL/non-ASCII counts and ZIP CRC result. Search case-insensitively
for the literal family stems `*DEFINE_CURVE`, `*DEFINE_TABLE` and
`*DEFINE_FUNCTION` anywhere in every body, including comments/quoted text;
separately count candidate line-leading keyword positions. Preserve locator,
family, match position and base-versus-suffix status, not raw source text.
Check ASCII/UTF-8 literal bytes and UTF-16LE/BE encoded stems separately.
An initial UTF-8 BOM may be removed only for line-leading classification;
it remains in byte/hash coverage. A textual hit is not a supplied typed
definition until its full syntax and reference fields are separately reviewed.

The raw-literal pass is intentionally broader than a semantic keyword parser:
comments and quoted/generated strings can be false positives. If a candidate
definition appears, freeze the presence result and declare its exact source-
card extraction before evaluating points. Preserve duplicates, conflicting
definitions, unsupported variants and unresolved include/run links. Use the
prior arithmetic protocol only after actual tables and provenance are resolved.
Do not construct replacement curves from similar ANSYS coefficients.

A zero result excludes these explicit literal definition families only within
the covered bytes/encodings. It does not prove absence of dynamically generated,
encoded, binary, external or historical definitions. NUL-containing bodies
remain separate; an all-NUL body can be identified bytewise but cannot be
interpreted as a working source program. PNG pixels, PDFs/correspondence,
unprovided files and the held packet remain outside this numeric scan. Prior
APDL command-role results may narrow generator leads, but cannot certify a
general runtime evaluation that was never performed.

## Safety and verification

No raw export, embedded instruction execution, solver, include-path traversal,
network retrieval, legal edit, source promotion, commit, push or transmission.
Output only allowlisted engineering-family names, aliases, ordinals, numeric
locators, byte counts and hashes. Unknown strings/comments/titles and personal
metadata remain suppressed. Stop an uncertain sensitive output before emitting
it. Preserve failed attempts and sanitized failure codes.

Bounds: 30,000 ZIP entries, 4 MiB/member, 512 MiB total June input, 512 MiB per
September stream, 16 KiB/physical line, 10,000 retained marker occurrences per
body, 300 seconds and 768 MiB measured peak RSS. Do not extract ZIP members to
their embedded paths. Check duplicate names, size/CRC/hash, EOF, changed inputs
and create-only receipt destinations. No incomplete scan may support absence.

Synthetic tests precede historical scanning and cover mixed case, leading
whitespace/BOM, variants, quoted/commented/embedded hits, repeated hits, both
UTF-16 orders, NUL-only/mixed and non-ASCII data, no-final-newline, exact family
versus unrelated substrings, line/byte caps, duplicate ZIP names, CRC corruption,
pin refusal and output refusal. Separate source readers freeze before sharing
new results/code. Reconcile all common per-body identities, byte/hash/line
coverage, exclusions, encoding flags and marker locators, not only zero totals.
Root repeats its result; independent comparisons retain any disagreement.

Deliver source coverage and a scoped dependency disposition, with exact next
record/test and claim limits. A negative explicit-definition search can close
this finite local search, not the whole investigation or a historical cause.
