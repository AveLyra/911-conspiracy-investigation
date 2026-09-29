# Material-definition parser: code and privacy review

2026-09-28. Working research; AI method/code review, not a licensed engineering
review, native model reproduction or independent historical evidence. Main
AGENTS, WORKFLOW, START-HERE and investigation CHARTER control. The reviewer
may inspect protocol/code/tests and perform synthetic-only checks. No native
source, manifest body, include dependency or historical parser result is in
this review's scope. This note is the reviewer's only write target.

## Protocol prereview — before producer code exists

The complete prospective protocol was read at SHA256
`2fd0a97c96a385e9fb689ee0d28879a476a7ac8dc86e858ad9076f4a177f0ea5`.
The existing main controls were reread earlier in this review sequence; fresh
hash checks identify AGENTS `d069c3ca120cd3b2d97e3ddde4ff6fb28df9a869930889e25de2a204c8e66476`,
WORKFLOW `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`,
START-HERE `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72`,
and CHARTER `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
Evidence-audit and source-preservation skills separate captured bytes,
lexical definitions and active historical state; development-verification
requires actual focused checks before a code/privacy disposition.

The one-candidate, seven-command scope and minimized output policy are suitable
for the stated finite test. No substantive protocol blocker was identified.
This is not execution clearance: the producer and independent implementations,
their synthetic tests and safe source/output guards still require review.

Implementation acceptance points communicated to root before code review:

- Unknown labels, expressions, coded-database UNBL forms, malformed quotes and
  extra nonblank fields must prevent whole-row fully-decoded status. Partial
  recognized fields must not hide unresolved structure. Blank fields and
  explicit numeric zero remain distinct; no default resolution is permitted.
- Standard field positions must match the protocol's documented modern
  reference basis. A legacy syntax/version claim does not follow from lexical
  recognition. ET textual names remain unresolved; numeric library codes alone
  do not establish an element's historical use or role.
- A mechanical-only result can characterize decoded literal definitions.
  Unresolved rows, format records, unknown commands and unexamined control/I/O
  behavior must remain visible and limit any broader negative inference.
- Source resolution must verify allowed identity, confinement and symlink
  refusal before source opening, with before/after pin checks. Code must not
  execute commands, evaluate expressions or follow includes.
- Success and failure output must remain create-only and confined, without
  source paths, filenames, free strings or exception text. Imports and tests
  must not trigger historical access.

Actual checks so far: full protocol and relevant skill reads; current control
and protocol hashes; unit file listing. At this checkpoint only PROTOCOL.md
existed in the unit. No parser, synthetic test or historical run was executed.

**Disposition: protocol prereview complete; code/privacy clearance pending.**

Later review findings must be appended below without replacing this prereview.

## Initial producer review — before historical execution

The full clarified protocol, producer and its22 tests were read. Reviewed pins:

- Protocol: `f1e3ce9d2fb1da5d0742e2de3a78008083f8ae6b9af6cc33268b4473c668b153`.
- Producer: `91c481dc2df14264fbc4b659d5953d4b4877b921c8be2e11ae8e3a8d74b41458`.
- Producer tests: `8b8acaf793fc8bb368957769e5515dd0ac3f11f61649793262475bf4dd4c0829`.

Actual command, from the unit directory:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -q test_parse_material
```

Result:22 tests, PASS. The reviewer also ran a stdout-only synthetic Python
script importing the producer and pinned lexer without invoking historical
entry points. AST inspection of the lexer confirmed definitions/constants and
a guarded main entry; the synthetic checks did not call its source readers.

Twelve additional assertions produced11 passes and one failure. Passing checks
covered privacy suppression for quoted labels/comments/expressions, all seven
complete schema shapes, numeric lexeme preservation including signed zero and
D exponents, MPDATA/ET field offsets, TB unused/function blanks, UNBL rejection
without fields, no filesystem access during scan, fixed-code failure-receipt
sanitization and create-only failure output. The first test-harness attempt
stopped because the temporary output directory lacked its synthetic protocol
fixture; that was a reviewer fixture error, not a producer finding. A corrected
rerun supplied the fixture and produced the stated12-check result. No native
input was opened. Temporary synthetic fixtures were automatically removed.

Two concrete pre-native issues were sent to root:

1. **Quoted comma shifts partial field roles.** At this producer version,
   `parse_row` uses plain comma splitting. For synthetic
   `MP,'PRIVATE,A',1,42`, the row correctly remains unresolved and suppresses
   the unknown text, but its decoded numeric fields incorrectly assign
   `c0=1,c1=42`. A quote-aware field split should retain a single unknown label,
   `material=1,c0=42`; alternatively the row must emit no misleading partial
   fields. Whole-row unresolved status does not make incorrect field positions
   faithful observations. Include doubled-quote and quoted-comma tests.
2. **CLI failure leaks supplied argument text.** A separate captured subprocess
   test passed wholly synthetic unrecognized command-line arguments. It exited2
   before historical access but argparse echoed the sentinel in stderr, rather
   than the protocol's fixed-code error output. Handle parser errors within the
   sanitized failure route. The captured sentinel itself was not printed.

The static source/output design otherwise uses fixed candidate name/content/
size pins, manifest checks, direct-child confinement, final-component symlink
refusal, capped candidate reading, after-read pin checks and exclusive output
creation. This is not adversarial filesystem-race hardening or an active-solver
semantic audit. Recognized numeric fields retain unit/default ambiguity, and
no include path or expression is executed.

**Disposition at these pins: historical execution not cleared.** Correct the
two findings and rerun relevant producer/reviewer checks before reconsidering.

## Targeted correction review — producer code/privacy clearance

The complete amended protocol, producer and test file were read. The two
blockers above remain part of the preserved review history; they are resolved
at these newly reviewed pins:

- Protocol: `88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670`.
- Producer: `16f87f8e123a2f8a702f68985ce206660282c942479a662d9ca70c8b77e7f12a`.
- Producer tests: `d940dc553d52412452d1a9506625d907041d9eb430498c1f5fab656981a7bb5e`.

The producer now separates comma fields while retaining single/double quotes
and doubled quotes. The quoted unknown label remains hashed/unresolved and no
longer changes the roles of subsequent numeric fields. Its SafeParser raises
a fixed refusal handled inside main; unknown or incomplete CLI arguments do
not print supplied argument text. The post-read candidate check now reads at
most CAP+1 bytes and checks both size and content hash.

Actual verification repeated the same bundled-Python command recorded above:
`-B -m unittest -q test_parse_material` returned25 tests, PASS. A separate
stdout-only reviewer script returned19 passes and zero failures:

- Four single/double/doubled-quote comma cases retained material=1,c0=42,
  blank c1 and unresolved quoted label, without the synthetic private token.
- Seven-schema recognition, signed-zero/D-exponent lexemes, MPDATA and full ET
  field offsets, and TB final blanks remained correct.
- Both UNBL variants emitted no decoded fields. Comments, unknown labels,
  expressions, element names and include arguments remained suppressed.
- A patched filesystem-denial check confirmed scan itself did not open files
  or follow source includes.
- Three captured invalid CLI subprocesses returned only the fixed refusal JSON
  with exit2 and empty stderr; none reached the historical route.
- A synthetic failing loader produced a sanitized failure receipt; a second
  output attempt refused without replacing its bytes.
- Two synthetic run-path checks substituted a mock candidate/manifest and
  temporary protocol. Both requested exactly CAP+1 post-read bytes: unchanged
  bytes passed, while a grown candidate failed with source_pin_after.

All fixtures were synthetic and temporary. The run-path tests replaced the
candidate reader; no actual manifest, native APDL body, historical result or
other source dependency was opened. The reviewer did not execute a solver,
evaluate source expressions, follow includes or run the historical parser.
Only this review note was changed persistently.

**Disposition: PASS for the producer's declared one-candidate lexical field
audit and minimized-output route at the pins above.** The prior two producer
code/privacy holds are lifted for this narrow scope. This does not clear an
unreviewed independent parser, authorize broader source selection, authenticate
a historical run, certify solver-version semantics, prove material assignment
or validate any physical conclusion. Root retains responsibility for separate
independent-parser review, frozen result comparison, source pins, all existing
authority gates and appropriately bounded interpretation. Unresolved fields,
control/format behavior and defaults continue to limit negative inferences.

## Post-result source and inference review — independent comparison pending

Root requested this separately bounded follow-up after the producer result and
draft existed. The reviewer read the complete draft at SHA256
`db7ef8bb75bdf01192e92c670482e0e23815320f810fba17fd16bcad4232e341`
and the minimized producer result at SHA256
`289ad8ed8518179df34c11eec9242dda3507a205917deadb1f7fab45cd7aed14`.
This is prior-informed result interpretation, not a blind independent source
parser or another historical observation. No native body or include was read.

Actual checks used jq for the receipt/schema and selected safe fields, plus a
stdout-only bundled-Python `-B -` script with json/collections to aggregate all
233 rows, field kinds, label/material groups, segment ordinals and locators.
The result was compared with every numerical/locator assertion in the draft:

- 233 selected rows: 228 literal-field rows and five unresolved-field rows.
- Command counts: MP 2, MPDATA 93, MPTEMP 63, TB 5, TBTEMP 49, TBDATA 18 and ET 3.
- MP/MPDATA labels: DENS 2, EX 31, PRXY 31, CTEX 31; all selected label fields
  are recognized. TB labels: MISO 3 and CREEP 2, at the stated material IDs/lines.
- All nine MPDATA label/material groups match the printed consecutive line
  ranges and 11/11/9 counts per label. All 233 selected segments are 1.
- The five unresolved fields are ET library fields at 27/2453/2654 and MP DENS
  first-value fields at 46/281. ET local IDs are 1/2/5; density material IDs 1/2.
  The two stripped unknown density field hashes are identical; no numeric
  value or shared effective runtime value is inferred from that identity.
- All 1,578 field kinds reconcile: 1,008 blank, 195 integer, 270 number, 100
  label, five unresolved. Unknown-token buckets sum to 2,587 occurrences in
  26 hashes; 12 noncommand segments, 36 DO commands, five IF commands and
  265 TBPT commands agree. The saved lexical-flag dictionary is empty.
- Receipt protocol/producer/lexer/manifest hashes match the reviewed pins.

No count or locator discrepancy was found. These are checks of the producer's
minimized derivative, not a fresh confirmation that its rows exhaust all
semantically meaningful native definitions. The draft correctly retained the
pending independent comparison at this checkpoint. This reviewer did not
inspect run02 or independently establish the draft's byte-identical-run claim.

### Primary-document vocabulary check

The exact official2024R2
[MP reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_MP.html)
was opened, particularly its label table. It supports the distinct meanings
assigned to EX, PRXY, CTEX, DENS, C, ENTH and conductivity labels in the draft.
The density label is not uniquely structural; thermal expansion is not heat
storage. Neither vocabulary observation establishes active input state.

The exact official2024R2
[TB reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_TB.html)
was opened and its header/label table and PLASTIC, THERM and USER portions
located. MISO appears as a modern PLASTIC option, and the thermal options are
separately described. The draft correctly does not treat the native lexical
MISO-in-label-position observation as invalid merely because modern syntax
differs. These are targeted public HTML checks, not a full historical-version
manual review or a preserved-byte publication pin. No native data was sent to
the documentation service.

### Inference ceiling and next-test value

The draft's positive mechanical/expansion-role evidence is supported. Its
selected-grammar negative finding is also faithful: all retained MP/MPDATA
labels are recognized and none is a direct specific-heat, enthalpy or
conductivity label. That does not classify every unknown command, execute
control flow, resolve parameter state or identify an upstream thermal model.
Definitions can be inactive, overwritten or combined with other state; material
IDs are not physical insulation/member identities. The manuscript retains
those important limits and does not infer omitted heat storage, wrong heating,
intent or cause from this candidate.

One next-step wording correction was requested: replace a promise to
"resolve the three ET name fields" with a test of whether the three unresolved
ET library fields match a predeclared official engineering-name allowlist,
retaining nonmatches unresolved. Their current hashes do not establish that
they are literal names or that the proposed test will resolve them.

The five-field follow-up has limited but genuine discriminatory value. Verified
thermal/coupled element vocabulary could challenge a simple structural-role
interpretation; verified structural-only vocabulary could strengthen this
candidate's role classification. Neither result establishes use, full element
assignment or the missing upstream heat-storage law. Classifying a density
token as a parameter/expression also cannot recover its value, unit or property
law. Recommend a strict five-field stop rule, no evaluation/identifier tracing
without a further declaration, and explicit treatment as candidate-role
closure rather than a replacement for locating the version/run-linked thermal
material setup. The latter remains the more discriminating implementation
dependency. No new native test is authorized by this review.

**Disposition: no substantive count/locator or inference defect found in the
reviewed draft; narrow next-step wording/value clarification requested.** Final
historical reproduction status remains pending the independent comparison and
root's resulting verification update. This review does not assert that those
later checks have passed.

## Final bounded integration review

The reviewer subsequently read the complete final unit report, the causal
synthesis paragraph beginning "The subsequent APDL01" and footnote27, the final
APDL01 SCOPE section, causal validation's top APDL01 section, STATUS's first
section and research README lines21–30. Only these additions were critiqued;
older causal units were not restudied. The unit validation's reviewed-execution
section and minimized independent receipt headers were also inspected.

The requested correction is integrated: the proposed next test conditionally
checks three unresolved ET library fields against a predeclared engineering
allowlist, retains nonmatches, limits density work to non-evaluative token
classification and stops after five fields. It explicitly cannot replace the
upstream version/run-linked thermal setup. No new source access is granted by
that wording or this review.

The causal paragraph, footnote, scope and navigation faithfully preserve the
positive structural/expansion vocabulary, selected-grammar negative finding,
five unresolved fields, activation/version limits and absence of a new causal
finding. No substantive inference correction is required in those additions.
The final unit report also distinguishes the differently defined auxiliary
unknown-token counters instead of falsely claiming all counters agree.

Actual read-only `shasum -a 256` checks confirm producer01 and producer02 share
`289ad8ed8518179df34c11eec9242dda3507a205917deadb1f7fab45cd7aed14`;
independent03, independent04 and root05 share
`57c1edcfaa1848a03ef0270a0a35952e644de7ee6bc3194be449624676b93652`.
Selective jq header checks show successful historical-lexical-only receipts,
the reviewed protocol pin and independent code
`4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62`.
This reviewer did not rerun the independent parser or root's comparison code;
the233-row/1,578-field cross-parser agreement remains attributed to root's
recorded source-free comparison. This review adds receipt-identity and
integration-text checks, not another native reproduction.

One execution-document continuity issue was sent to root: at inspection the
unit validation ended at the earlier independent6e27e0d4/73-control clearance.
It should retain that stage and append the manifest-cap failures, repaired
4faf95f1/76-control review, successful reads, root replay and comparison
chronology. The causal validation addition is substantively accurate but is not
a substitute for that detailed unit execution record. No source/body recheck
is needed to repair the documentation.

**Disposition: PASS for the named final inference/integration additions and
requested wording correction; append the final unit execution chronology.**
No native body, source command, include or model was accessed/executed in this
integration review. Earlier review stages and failures remain unchanged.

### Execution-chronology closure

The complete new validation section, "Manifest-cap failure, corrected
independent reads and comparison," was subsequently read. Validation SHA256 at
this check is `3285ab4e8685ac665b359bae8cf38319968577b8f627b5c797f46a81b938d62a`;
the unit report is `04e378d792213bcd750e319fdcc40998b7af8622a0577184bc36331fc9434ffe`.
The addition retains the earlier stage and explicitly records both failed
receipts, the manifest-only size/hash repair, final code pin,76-control replay,
pre-read re-clearance, successful frozen receipts, actual root replay command,
selected-field comparison and ten in-memory mismatch checks. It distinguishes
different auxiliary counters, root's confirmatory replay and the two separately
implemented readers. The adopted next-test correction and unsuccessful patch
attempt are preserved without turning either into new scientific evidence.

The chronology is consistent with the checked receipt hashes/headers and the
bounded final report. The reported76-control and ten-perturbation runs remain
attributed to their recorded root execution; this reviewer did not rerun them.
No further native or historical-result body reading was performed.

**Final disposition: PASS within the named code/privacy, result-inference and
integration-review scopes. The execution-document continuity concern is
resolved; no further correction is required by this bounded review.** This is
not full language interpretation, solver execution, physical validation,
historical model authentication or an expert engineering certification.
