# Independent bounded method review

Research working note. October 4, 2026 America/New_York / October 5 UTC.
This reviews the declared metadata method, not historical PDF content,
archive authenticity or completeness. Only this note is reviewer-owned.

## Authority, scope and pre-request review

Main AGENTS, WORKFLOW, START-HERE and the main investigation CHARTER control.
Evidence-falsification, source-of-truth and development-verification skills
were read, including the evidence/source reference checklists. Their material
effect is to keep a successful parser test separate from validated historical
input, preserve failed runs, and prohibit silent schema repairs or promotion.
No legal, main-repository, original-source or frozen-note edits are authorized.

Complete skill read: af091d exit 0. Initial combined control output was
truncated; complete recovery reads were 2b96bd and b36df5, both exit 0.
Protocol/query read and pins: 18038c, 7cce97, e34cbe. The final compound
command exited 1 only because its trailing scoped `rg --files -g AGENTS.md`
found no nested research AGENTS; the protocol/query reads and hashes completed.

- Protocol: `4d80c5e158fb35be8bd569ecd6ea4824bd860275bd54c36b1332353b4e4ff37d`.
- Query map: `4304b2197346f6bfb6d8b7daefc855ee9e1833b097e62813cbba323f96e3ada0`.

No pre-request blocker found. All ten query strings match the declaration;
count 50, metadata-only properties, source restriction, no pagination or
post-result enlargement, preserved failures and raw bytes, access boundaries,
independent extraction freeze, and claim ceilings are explicit. The selection
is an informed keyword screen, not an exhaustive search of all seven corrective
items. Quoted/hyphenated/punctuated forms, OCR and tokenizer behavior remain
unvalidated. A complete-query flag means only that the saved response satisfies
the declared server-termination checks; it cannot establish complete archive
or document-body coverage. The known-record control has the same narrow limit.

## Strict adapter and synthetic verification

Complete adapter/tests read and scoped read-only status: b406be, ed409b,
7e6bf5, terminal exit 0; the unit is untracked working material. Imported
dependency read/hash plus test run: 234765 to 977672, exit 0.

- Adapter `check_metadata.py`: `6f51bfda7c4cf6508ab0095240bbbba3b935d8f23f0bae957bc36f42f8986b72`.
- Tests `test_metadata.py`: `cefeec65be44795043c7ed04eda86730fb4005b993af8eeb9e4d3f7ad91d8479`.
- Imported `../test-acceptance-locator/check_metadata.py`: `d561ee20e778bd0111103b3352f251396f618f2be2a23ad172ad96efb7ac6d7a`.
- Bundled Python 3.12.14 confirmed by 7e11a1 to f25253, exit 0.

Actual supplied-suite command, from this unit:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_metadata
```

All 20 supplied tests passed. They cover exact request/echo, JSON/property/ID
duplicates, scalar cardinality, source restriction, cross-query consistency,
membership, absent/empty results, pagination, estimates and termination causes.

A separate stdout-only Python `-B` heredoc ran 22 additional synthetic cases
(af2fc4 to 10c6a9, exit 0). It imported the fixture and adapter, mutated only
in-memory objects, and mocked `prior.read` for the full-calculation control:

- Rejected boolean estimates, numeric paging flags, 51 results, malformed IDs,
  mismatched titles, zero/fractional pages, negative/fractional/NaN bytes,
  boolean numeric scalars, two scalar kinds, a missing property, nonempty user
  context, and absent results with a next-page flag: 16 cases.
- Marked empty, mixed and null termination evidence, plus absent zero results
  with a previous-page flag, incomplete: four cases.
- Rejected a missing known-record control through a mocked full calculation.
- The negative guard probe `python3 -B -O check_metadata.py` stopped with
  `Assertions are required` before data reading; no historical calculation
  was run with assertions disabled.

No historical response was consumed in these tests. The adapter does not call
the imported dependency's historical calculation. Exact query literals remain
a frozen-input/protocol responsibility: the adapter validates label order and
echo agreement and emits input pins, rather than hard-coding every query string.
Imported optimized use is outside the supported non-optimized execution route.

No blocker found in the strict adapter for its declared contract. This means
malformed data can stop analysis; it does not mean real inputs satisfy it.

## Subsequent real-input failure and diagnostic boundary

After the above tests, root reported actual parser receipt 24f118, exit 1:
at least one ten-property result omitted `folder_name`. Root reported no
validated strict output or freeze. This paragraph attributes that execution
to root; the reviewer has not independently parsed the historical responses.
The strict failure must remain a failure of the fixed eleven-property contract.

A separately labeled diagnostic wrapper may classify strict-valid occurrences
and quarantine exceptions without changing the strict checker, prior sources,
or acceptance criteria. Required limits for that diagnostic are:

1. Retain every occurrence by query and result ordinal, its actual property
   objects/ID where readable, missing/extra/duplicate property names, and exact
   failure class/message. Preserve malformed entries instead of dropping them.
2. Leave absent `folder_name` absent. Do not invent empty, null, inferred or
   neighboring labels and present them as returned source fields.
3. Keep query-envelope validity/coverage separate from record-schema validity.
   Quarantine and returned counts must reconcile; the strict-valid subset is
   not the whole response and is not archive coverage.
4. Preserve duplicate/conflicting ID occurrences, including cross-query
   conflicts, rather than deduplicating them into an apparently valid record.
5. Label the unit as qualified and not a full fixed-contract pass. Diagnostic
   success cannot erase the original failure or establish historical truth.

The diagnostic implementation and its own tests have not yet been reviewed.
No new requests, PDF acquisition or reading, image views, wider investigation,
Git mutation, cross-project messages or non-note writes were performed here.

## Diagnostic continuation reviewed after root freeze

The pending-review statement above records the earlier checkpoint. Root then
declared the continuation, implemented the separate wrapper, and froze its
diagnostic output before this review. Complete declaration/code/test reads and
hash checks were 6c9ca3, b299aa, f0b4fe, terminal exit 0:

- `DIAGNOSTIC-CONTINUATION.md`: `4d3a9fe762050b37b8a4d1880d6ae69e3ed0d9120943765997451d4aa273d17c`.
- `diagnose_metadata.py`: `98b7a748aa7abe4c8dd1b25c9cbe930a98f6cfc42e59fd373344a82e766540a2`.
- `test_diagnostics.py`: `c159ca2ee7592498f24b20a39120eeff95e0badf5c6edd9cf90e3e2a15fe98c6`.
- Frozen `root-diagnostic.json`: `c6a80ecc100e77cc3d387e17fa032e8c4032e4e13cb761d20bffd6eaed51e7d8`.
- Strict adapter still `6f51bfda7c4cf6508ab0095240bbbba3b935d8f23f0bae957bc36f42f8986b72`.

The wrapper permits only the expressly observed missing-folder exception;
other missing/extra/duplicate properties or bad identifying/count fields stop
execution. It separately validates the query envelope, retains raw quarantined
result objects and one-based ordinals, counts every returned record, and rejects
within-query duplicates or cross-query conflicts. Missing `folder_name` is
not filled in. Its status explicitly retains the full-contract failure.

Actual supplied diagnostic-suite command, in this unit:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_diagnostics.DiagnosticTests
```

All eight supplied diagnostic tests passed. A subsequent stdout-only Python
`-B` heredoc ran nine additional in-memory diagnostic cases. The combined
execution was 8d6aa8, df18d5, 85b950, terminal exit 0:

- Five stop cases: missing folder plus missing source; missing folder plus an
  extra property; duplicate missing-folder IDs; request-echo mismatch despite
  quarantine; and estimate below returned count despite quarantine.
- Previous-page and missing-termination cases remained incomplete even when
  their sole row was quarantined.
- A mixed two-row case reconciled one valid and one quarantined occurrence,
  retained the quarantine's exact raw object and ordinal 2, and left its folder
  field absent.
- A mocked full calculation rejected the same ID appearing as valid in one
  query and missing-folder in another as a cross-query conflict.

After these synthetic checks, the reviewer consumed the saved historical
metadata through the diagnostic code, not through PDF content or new requests.
`diagnose_metadata.calculate()` serialized with indent 2, sorted keys,
`allow_nan=False` and a final newline matched the complete frozen diagnostic
bytes exactly, at the hash above. This is an independent execution of root's
implementation, not an independent extraction algorithm or blind reading.

Counts reconcile: 142 occurrences = 134 strict-valid + 8 quarantined;
97 unique IDs = 89 strict-valid + 8 quarantined. All eight quarantines have
exactly ten actually supplied property names, missing only `folder_name`,
without a synthesized replacement. These are metadata counts, not physical
pages read, historical document independence or archive completeness.
The same check called unchanged `check_metadata.calculate()` and confirmed it
still raises `AssertionError`; no strict-output pass is claimed.

No blocker found in this bounded diagnostic continuation. The original fixed
eleven-property extraction remains failed; unknown schema exceptions, any
later conflict, unsearched query variants, capped results and source-body/OCR
coverage remain outside a claim of complete validation. A successful method
check neither chooses the next historical packet nor authorizes its reading.
