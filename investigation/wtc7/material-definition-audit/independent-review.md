# Independent typed material/element audit

## September 28, 2026: pre-native implementation and synthetic freeze

Working research under the main AGENTS, WORKFLOW, START-HERE and investigation CHARTER, and this unit's [PROTOCOL](PROTOCOL.md). Those controls and the preceding thermal-transfer protocol were read completely. Applied development-verification, evidence-falsification-auditor, source-of-truth-guardian and repo-orchestrator skills; repository intake reported branch `research/sherlock-wtc7-investigation`, existing intentional WIP and HEAD `2fab1389`. Its displayed inventory was truncated, so no claim of reviewing every working-tree change follows. Only this unit's assigned independent files are edited.

This is separately implemented code under a shared declared grammar, not independent historical evidence, a blind test or expert engineering review. Earlier command counts and the finite candidate identity are prior knowledge. The producer implementation, existing lexer implementation and producer results were not read or imported before this freeze. `scan_transfer.py` lines 1–38 were read only to recover constants/path-route metadata; this unnecessarily displayed its technical ZIP basename, but no APDL source filename, native body or source comment. That minimization shortcoming is preserved rather than claiming perfect output minimization. Only the manifest header's six column names was read at this stage, not its native file entries or APDL payload. No other source body, archive, model or include was opened.

### Implementation contract

[independent_parse.py](independent_parse.py) independently implements quote-aware comments, dollar slots, comma fields, doubled quotes, format records, typed schemas, unresolved hashes, fixed error codes, source/pin/path guards and create-only output. It imports neither the producer nor the old lexer/scanner. Numeric lexemes are not evaluated; labels are emitted only from the protocol allowlists. Blanks are distinct from zero, omitted trailing positions remain distinguishable through `argument_count`, and unsupported/quoted/UNBL/extra-field forms cannot silently become fully decoded rows.

Pre-native clarifications from root fixed TB's seven current-reference positions with the last two blank-only, MPTEMP's documented empty reset, all-dollar-slot ordinals, latin1 stripped-segment hashes, UTF8 stripped unresolved-field hashes, and first-of-three APDL manifest selection. These were shared schema decisions before native outcomes, not independent validation of historical solver syntax. The later pre-native review also fixed malformed known-command forms such as `MP EX,1,2` as selected unresolved rows and reserved one LF byte in the line cap (`len(raw_record)+1 <= 16384`, even for a final unterminated line). An unmatched quote anywhere on a line marks its selected rows unresolved; its individual unknown tokens remain hashed. Expected format records are retained with explicit statuses and bound any absence inference.

Source selection will use the unique declared source SHA and filename hash, additionally asserting that it is the first of three `.apdl` manifest rows. The implementation opens directory chains with no-follow flags, checks regular-file type, byte cap, expected size and digest, and rechecks source/manifest/protocol/code pins after parsing. Output existence is checked before any historical read, with exclusive create again at writing. No source path, native filename, unrecognized label, comment or free argument is emitted in results. Runtime gate parameters must match the declared protocol and implementation bytes. This is a safety/reproducibility mechanism, not authorization by itself.

### Actual synthetic verification and preserved failures

Bundled Python command base: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B`, runtime **3.12.14**. The synthetic CLI suffix is `independent_parse.py synthetic independent-run-syntheticNN.json`, using the assigned absolute implementation path.

1. Initial sandboxed synthetic run returned fixed `OUTPUT_IO`, exit 2, while trying to save its receipt. `test -e` confirmed no receipt was created. A stdout-only invocation of the owned `selftest()` then returned **61 passing controls**, `historical_source_opened=false`, exit 0. No native file was opened; this was an output-permission failure, not a parser or source finding.
2. After adding actual symlink-directory refusal, protocol/code gate refusal and sanitized CLI controls, the scoped elevated synthetic run created [synthetic01](independent-run-synthetic01.json): **66 passing controls**, exit 0, plus an actual attempt to overwrite the created receipt correctly refused. SHA-256 `89c8ec8038b01b8e2a3bb4a687562e449007b67b64ae9ee4f968895c7a242e63`.
3. Quoted-comma/doubled-quote field-position and invalid-output-name checks were added before any native read. The next create-only run saved [synthetic02](independent-run-synthetic02.json): **69 passing controls**, exit 0, plus actual create-only refusal. SHA-256 `d72a90d3bd0e335cc44f86c89fb827666922ab07d8813cb7a69160e1d099167e`.
4. The malformed-command, line-wide unmatched-quote and precise line-cap-boundary controls brought [synthetic03](independent-run-synthetic03.json) to **73 passing controls**, exit 0, plus actual create-only refusal. Receipt **5,474 bytes**, SHA-256 `3bcbdf48a83ed3706698f8d9f3476ac3ae0374345e6a92c736902142374574b8`. A separate read of this JSON confirmed 73 actual check records, all true, and the current code hash below. Reusing that exact CLI output name returned fixed `OUTPUT_EXISTS`, exit 2, before running tests; its hash remained unchanged. These expected refusal results are retained, not hidden as successful executions.

Controls cover all seven schemas, blank/zero/omission, E/D numeric spelling, malformed numbers, 64-character bounds, unsigned IDs, unknown/quoted labels, textual element IDs, extra nonblank and trailing blank fields, TB reserved/function slots, both UNBL variants, same-line commands and empty slots, comments, doubled/unclosed quotes, quoted commas, format lines, exact command matching, privacy sentinels, NUL/byte/line/row caps, traversal and `/tmp` symlink refusal, guarded own-code reads, pin/size mismatch, protocol/code gates, manifest-empty selection, sanitized CLI/output failures and exclusive receipt creation. The guard controls use owned code/protocol or synthetic bytes; they do not open the historical source. The final test receipt's byte count happens to equal the source's earlier reported LF count; these are unrelated quantities.

**Frozen implementation:** 26,577 bytes, SHA-256 `6e27e0d40ab211e5db09a224b1ddf31994f43e444216ff47fef38bc3bad5bc5a`.

**Frozen protocol:** SHA-256 `88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670`.

Root separately reported reading this complete final implementation and replaying all 73 controls successfully. That is root's review/replay, not an additional check performed by this reviewer. Root then explicitly cleared the historical gate for exactly APDL01 and these pins, requesting two independent create-only runs followed by a freeze before producer comparison. The following stage, if completed, must be separately recorded below; synthetic success alone establishes no APDL01 content or historical execution finding.

## September 28, 2026: preserved guard failure, repair and successful frozen scans

### Failure and narrowly reviewed repair

The two first authorized CLI attempts (`historical independent-run01.json` and `historical independent-run02.json`, protocol `88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670`, code `6e27e0d40ab211e5db09a224b1ddf31994f43e444216ff47fef38bc3bad5bc5a`) both returned **exit 2 / SOURCE_CAP**. Tool receipts were `3dfbdc` and `8f56ad`. Their create-only [failure01](independent-run01.json) and [failure02](independent-run02.json) are byte-identical, SHA-256 `cf65089cff5c88134ec25709e60f7649e1f3eebbce1a3513f76469b43edf035e`; neither was overwritten or converted into success.

`stat -f '%z'` on the fixed manifest returned **4,698,031 bytes**. The generic reader incorrectly applied the 4 MiB candidate cap to the larger manifest. In the frozen code's execution order, this refuses at the manifest's `fstat` size check, before reading its body or selecting/opening APDL01. The code/protocol guards were checked first; no APDL result or producer content was used to diagnose this failure. This is an implementation-scope mistake, not a source-corruption or missing-record finding.

With explicit narrow approval, introduced a separate `MANIFEST_SIZE = 4698031`, requiring that exact size and the unchanged fixed manifest hash for the two manifest reads. The APDL **4 MiB cap**, source selection, typed grammar and output contents were not relaxed. Three new synthetic checks use a mocked metadata stream larger than 4 MiB: the default candidate cap refuses it, an explicit metadata-only cap admits matching bytes, and the candidate cap is asserted unchanged. No real manifest body or APDL source is read by these controls.

The updated synthetic CLI created [synthetic04](independent-run-synthetic04.json), **76 passing controls plus actual create-only refusal**, exit 0 (`e9a2a0`). Receipt SHA-256 `c87271d1561a4800dc7cb49d00645771068ba759f125278076dfb6fafedd8c59`. Updated implementation SHA-256 **`4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62`**; the protocol pin remained unchanged. Root separately reviewed this exact repair and reported replaying 76 controls successfully, then expressly re-cleared runs 03/04. No producer result was read by this reviewer before the successful independent freeze.

### Actual successful commands and freeze

The following exact historical CLI commands ran with scoped write escalation for the assigned worktree. They read the fixed candidate through the reviewed guards; they do **not** run APDL commands, a solver, includes or any other source body:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit/independent_parse.py historical independent-run03.json 88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670 4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit/independent_parse.py historical independent-run04.json 88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670 4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62
```

Both reached **terminal exit 0**, reporting 233 selected rows (receipts `0767e9`, `c5a8b9`). Each performs before/after source and manifest pin checks, not just one unchecked read. `shasum -a 256` froze [run03](independent-run03.json) and [run04](independent-run04.json) at the same hash **`57c1edcfaa1848a03ef0270a0a35952e644de7ee6bc3194be449624676b93652`**; `cmp -s` returned exit 0. These pins were reported to root before this reviewer accessed either producer result.

Independence timing correction: root clarified that it had read its own already frozen minimized producer result before receiving this reviewer's final code-freeze message, after the shared grammar decisions. It had not read independent historical output or sent historical field values to this reviewer before the independent freeze. The already known source counts, producer digest and total selected-row count were not blinded. Do not claim both analysts remained result-blind, or that root first read its result only after this independent historical freeze. Root's separately reported replay into `independent-run-root05.json` is not this reviewer's run and is not credited as another independent algorithm.

### Independent source-free comparison

Only after the successful independent freeze, inspected the frozen producer JSON schemas—not its implementation or `compare_results.py`—and compared `producer-run01.json`/`producer-run02.json` with own runs 03/04. Producer pair SHA-256 was independently checked as `289ad8ed8518179df34c11eec9242dda3507a205917deadb1f7fab45cd7aed14`. The producer's shape/status vocabulary differs from the independent representation. A first schema-only inspection printed a needlessly repetitive list and was display-truncated; it contained field-key names only, not native text. A compact second schema inspection recovered the complete distinct status/field shapes before comparison; the truncated display was not treated as a full comparison.

The actual comparison was a stdout-only bundled-Python `-B -` here-document (tool receipt `9ea2b5`, exit 0), independently written for these saved JSONs. It normalized these explicit representation differences and did not read or rerun native sources:

- Producer `integer` versus independent `id`, producer numeric `lexeme` versus independent `value`, and producer `literal_fields`/`unresolved_fields` versus independent `decoded`/`unresolved`.
- Field role aliases only: `Lab→label`, `MAT/MATID→material`, `SLOC/STLOC→start`, `TBOPT→option`, `reserved→unused`, `FuncName→function`, `TEMP→temperature`, `ITYPE→local_type`, `ENAME→library_code`; other field names become lowercase.
- Producer extra-trailing-blank count versus independent `max(0, argument_count−schema_field_count)`, after asserting that **no selected independent row contains extra nonblank fields**. Blank states within the schema are compared individually; this normalization does not turn blank into zero or reconstruct an omitted value.

Compared ordered source line/segment/command, stripped segment hash, argument count, normalized status, extra trailing blanks and every normalized field's role/kind/numeric lexeme/allowlisted label/unresolved hash. Source byte count, physical-line count and source/manifest/protocol pins were also compared. Actual results:

| Check | Result |
|---|---|
| Selected rows/locators and row ordering | **233/233 match** |
| Individual typed fields, including blanks and unresolved hashes | **1,578/1,578 match** |
| Argument counts, segment hashes, normalized statuses, extra trailing blanks | Match for all 233 rows |
| Row mismatches | **0** |
| Decoded/unresolved rows | **228 / 5**, matching after status-name normalization |
| Unresolved fields | **5**, matching hashes and positions |
| Source bytes/hash, manifest hash, protocol hash and physical-line count | Match |
| Selected-command totals | Match |
| Shared allowlisted control/I/O command counts | Match within that shared vocabulary |
| Producer 01/02 and independent 03/04 byte equality | Both pairs match |

This is **not whole-schema equality**. The independent scanner deliberately hashes more nonselected tokens because it uses a narrower control/I/O vocabulary and a different token recipe: it retains 3,988 unknown/nonselected segments, while the producer reports 26 distinct unknown-token hash classes. These numbers have different denominators and cannot be called a disagreement count, parser-error rate, or evidence that those native commands are invalid. Root's reported comparison outcome was received before this independently written comparison; the data and algorithms were frozen first, so this was a nonblind reproducibility check, not a holdout test.

### Bounded literal findings and remaining limits

The fixed source has **212,384 bytes**, SHA-256 `e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64`, **5,474 physical LF-split records but 5,473 actual LF bytes**. The earlier protocol's “5,474 LF lines” is an attributed record count, not a verified count of newline characters. This distinction does not alter selected locators.

Matched selected totals: MP 2, MPDATA 93, MPTEMP 63, TB 5, TBTEMP 49, TBDATA 18, ET 3. Recognized labels are **DENS 2, EX 31, PRXY 31, CTEX 31, MISO 3 and CREEP 2**. These literal labels are positive evidence about the candidate's vocabulary; they do not themselves authenticate a historical material table, case assignment, solver version or executed law. DENS alone is not a heat-storage formulation. No recognized C/ENTH or conductivity label appears among the selected recognized labels, but unsupported rows, dynamic expressions/control flow, other files and runtime-supplied definitions remain outside this literal-field inference.

The five unresolved fields, preserved rather than interpreted, are:

- ET `ENAME`: lines **27, 2453, 2654**, all segment 1.
- MP `C0`: lines **46, 281**, both segment 1.

No new names, expressions or values were recovered from those fields. They require any later separately declared review to respect the same privacy, grammar and version boundaries. There were no format records in this candidate's independent result. Known control vocabulary includes loops and conditional commands; no branch, macro, material interpolation, default or solver semantics was evaluated.

Independent agreement establishes deterministic lexical reproduction of the selected minimized field records under the shared protocol. It does not establish model execution, physical validation, active WTC7 heat storage, its temperature domain, a heating bias or a collapse cause. The two parsers can share a specification limitation; agreement does not eliminate the held-out semantics, unresolved fields or surrounding-source dependencies. No further native source or solver access is authorized or implied by this result.
