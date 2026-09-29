# Independent five-field follow-up review

2026-09-28. Working research record, not expert engineering review, solver
execution, historical authentication or a causal finding.

## Pre-native implementation freeze

Scope is the additive [FOLLOWUP-PROTOCOL.md](FOLLOWUP-PROTOCOL.md): exactly
APDL01 ET ENAME at physical lines 27, 2453 and 2654, and MP DENS C0 at lines
46 and 281; all segment 1. The old material-audit protocol, parser, receipts and
review remain unchanged. No native source or manifest body was read while
implementing or testing this follow-up. No parent producer code or result was
read. Earlier audit command counts and the five unresolved locators/hashes were
already known; this is not blinded discovery or independent historical evidence.

Main AGENTS.md, WORKFLOW.md, START-HERE.md and CHARTER.md were read; the
development-verification, evidence-falsification-auditor and
source-of-truth-guardian skills governed this bounded implementation. No legal
record, source authority, disclosure permission or causal ranking changed.

Frozen inputs/code before native access:

| Item | SHA256 |
|---|---|
| Follow-up protocol | `5cced3d7159405e035c2c4c0c0eca4995b2052371992977735c618a90ae54fd5` |
| Fixed targets | `e29a710e92720686d6be306c45fa5d9562f3f5dc47b1d585638d8f74b1324dae` |
| Public element-name allowlist | `423426c4f3579e241eddff94f603556debc3380edf95f5812b41b425ac122b9d` |
| Reused own helper | `4faf95f175ccd8d17947cc29f777e8bcb714727a034be72cc99c937578524d62` |
| New independent_followup.py, 21,538 bytes | `a9443bed6460d4de33c4caf5e97d611648891800aad21fb197f738d02418596e` |
| Prior protocol, preserved | `88aa92198fd2c754db0301c0cd8b1d679caa70cd338cf9debe7113b75691e670` |

The full current protocol, targets, allowlist JSON and own helper were read.
The 139-name list is an input supplied from root's primary-documentation
transcription; I did not independently retrieve or authenticate its web source.
Synthetic tests use both thermal and structural names and deliberate nonmatches,
not guesses at the withheld five field contents. No target hashes were inverted.

## Implementation boundary

[independent_followup.py](independent_followup.py) independently implements the
specified density grammar and element membership check. It imports only its
own exact pinned helper bytes, calls only `read_guarded`, `manifest_candidate`
and `_split` from that helper, and never invokes its complete-source scanner,
classifier, CLI, tests or historical entry point. The guarded reader and selector
are deliberately shared with this investigator's prior audit; their bugs would
not be independently tested by a second use of the same helper.

New code performs its own no-follow bootstrap and output handling. Native mode
checks all control pins before source access; validates the exact five targets
and their original segment/field hashes, commands, argument counts, ID and DENS
label; emits five rows in fixed target order; and checks source, manifest and all
controls again before create-only output. Complete source bytes are needed for
hashing. NUL and length checks cover all LF records as integrity safeguards, but
only five selected records are split into command/field content. No token, value,
arbitrary identifier, comment or native filename is emitted. A matching ET name
may be emitted only from the frozen finite public set. Density emits a category
only. Source/manifest reads retain their prior separate byte caps. Line cap uses
`len(raw LF record)+1 <= 16384`, including a final record without an LF byte.

Operational native HOLD remains in force pending the parent's explicit code/
privacy clearance; the existence of a historical CLI mode is not permission to
run it. Two deterministic native receipts and their later comparison are pending.

## Actual synthetic verification

Runtime was bundled Python 3.12.14 with `-B`. First stdout-only command:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit/independent_followup.py selftest
```

Terminal exit 0, `PASS SYNTHETIC 93` (tool chunk `842610`). A second run used
the same command with final argument `followup-independent-synthetic01.json`,
under scoped worktree-write approval: exit 0, 93 passed (chunk `37df16`). Saved
[synthetic receipt](followup-independent-synthetic01.json) SHA256:
`0274c466e3ba328bd3d5de1fcdd37004c71ec31991c6e4c1e6508a38dc13db49`.

Repeating that receipt-writing command returned exit 2, exactly
`REFUSED OUTPUT_EXISTS` (chunk `17f4a1`); the existing receipt was not overwritten.
The receipt hash was then checked with `shasum -a 256` (chunk `ffbc28`). This was
an intended negative check, not a successful historical run or failed source.

The 93 controls include all categories; exact 64-character number/32-character
identifier, 128-token and 16-parenthesis-depth boundaries; precedence-free
unary/binary shapes, zero-division shape without evaluation; Unicode and other
unsupported input; quote-aware commas, dollars, comments and doubled quotes;
exact five-row order and target/hash/schema mismatch stops; byte/NUL/all-line
limits; private synthetic sentinel non-disclosure; bad control pins before
source access; duplicate/invalid allowlist rejection; path traversal, existing
output and sanitized arbitrary CLI error checks. Synthetic test labels and
counts are not native field tokens/counts.

No actual native classification, element-role interpretation, helper source
selection replay or parent-output comparison has occurred at this freeze.

## Inferential ceiling and disconfirmation

A successful result can establish only that the selected pinned fields have
the prescribed literal/name/shape classification. An official-name match cannot
establish historical library availability/defaults, assignments, active degrees
of freedom, loading, execution or physical fidelity. The list's incomplete
historical coverage makes a nonmatch unresolved, not an invalid historical
element. A numeric-looking or identifier-arithmetic density cannot establish a
value, unit, defined arithmetic, parameter binding or active material state.
Both implementations could agree because they share the wrong source selection,
protocol or transcription. The fixed source/target checks and independent new
classifier reduce specified implementation risks, not these historical risks.
Any pin/target mismatch must stop; disagreement must remain visible without
widening the list or reading more fields to obtain agreement.

## Cleared five-field runs — post-readiness supplement

2026-09-28. The preceding 6,612-byte readiness prefix is preserved, SHA256
`02cac08471d8c909ada58c11b5e0c28cca788d537e503c2acc057b0dc69a936d`.
Root expressly cleared the exact code/protocol/list/target route after a separate
reviewer reported 93 replayed selftests plus 10 reviewer checks. Those additional
reviewer checks and root's public-list transcription verification are not my
own checks. Native access was then confined to the prescribed guarded route.

Actual commands, both with scoped worktree-write approval and bundled Python
`-B`:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit/independent_followup.py historical 5cced3d7159405e035c2c4c0c0eca4995b2052371992977735c618a90ae54fd5 e29a710e92720686d6be306c45fa5d9562f3f5dc47b1d585638d8f74b1324dae 423426c4f3579e241eddff94f603556debc3380edf95f5812b41b425ac122b9d a9443bed6460d4de33c4caf5e97d611648891800aad21fb197f738d02418596e followup-independent-run01.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit/independent_followup.py historical 5cced3d7159405e035c2c4c0c0eca4995b2052371992977735c618a90ae54fd5 e29a710e92720686d6be306c45fa5d9562f3f5dc47b1d585638d8f74b1324dae 423426c4f3579e241eddff94f603556debc3380edf95f5812b41b425ac122b9d a9443bed6460d4de33c4caf5e97d611648891800aad21fb197f738d02418596e followup-independent-run02.json
```

Both commands terminated exit 0 with exactly `PASS FIVE_FIELDS`: chunks
`0a9205` and `f40dbf`, reported command wall times approximately 0.048 and
0.024 seconds respectively (not total tool/approval latency). There was no
historical failure/retry and no source text in stdout/stderr. The code's
before/after source, manifest, protocol, targets, list, helper and new-code
checks passed; every original target segment/field hash and typed locator
check passed. This is pin consistency, not historical authentication.

[Run 01](followup-independent-run01.json) and
[run 02](followup-independent-run02.json) are each 2,995 bytes, both SHA256
`62b58c30326c78fe6f72aaf5163a26495c97e446f9f85a1ac7bbcda0bfd5ca68`.
`shasum -a 256`, `wc -c`, and `cmp` on those two explicit paths completed exit 0
(chunk `37d0f6`); `cmp` emitted nothing. Both receipts and their hashes were
reported to root before any parent result access. I subsequently read only my
own minimized run01 receipt (chunk `17e555`), not native text.

| APDL01 physical line / segment | Fixed field | Classification | Permitted standard name |
|---|---|---|---|
| 27 / 1 | ET ENAME | official_name_match | BEAM188 |
| 46 / 1 | MP DENS C0 | identifier_arithmetic | Not emitted |
| 281 / 1 | MP DENS C0 | identifier_arithmetic | Not emitted |
| 2453 / 1 | ET ENAME | official_name_match | SHELL181 |
| 2654 / 1 | ET ENAME | official_name_match | MPC184 |

All five rows preserve their target dictionary, including old hashes. The two
density fields retain the same old stripped-field hash, but neither expression,
identifier, numeric value, unit nor evaluated result has been displayed or
saved. No more than the five declared fields were classified. No parameter
lookup, include traversal, native body inspection by the analyst or solver
execution occurred. The source bytes were consumed internally by the guarded
hash-and-five-field route exactly as authorized.

This resolves the three ET fields only to public-name membership and the two
density fields only to the fixed identifier-arithmetic shape. It does not resolve
density or historical activation. The new results do not retroactively change
the first audit's numeric-only ET schema or its unresolved-field receipts.
Current element-role documentation remains a separate interpretive step, not
performed by this independent reader. Parent-output comparison is still pending
at this supplement; no agreement with another implementation is claimed here.

## Post-freeze minimized-receipt comparison

2026-09-28. The preceding 10,779-byte source-run supplement is preserved,
SHA256 `36583d9d6908f16e6eff5a06db12b25a8877d25385423650871d3c2f7238543c`.
After my two-receipt freeze, root reported its comparison matched five rows and
detected ten deliberate perturbations; root then authorized my access to its
minimized receipts. Those mutation checks are root's, not mine. The expected
agreement and classifications were therefore already known before my comparison;
this is an independently implemented comparison, not a blind holdout.

I did not read or import root's classifier or comparison script. Filename-only
discovery used `rg --files` restricted to `followup-*-run*.json` in this unit
(chunk `a61dcc`). I then ran this stdout-only code under the same bundled
Python `-B -` invocation (chunk `28f40b`), with no native/manifest access:

```python
from pathlib import Path
import hashlib,json
base=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/material-definition-audit')
names=['followup-independent-run01.json','followup-independent-run02.json','followup-producer-run01.json','followup-producer-run02.json']
blobs=[(base/n).read_bytes() for n in names]
docs=[json.loads(b) for b in blobs]
rows=[d['rows'] for d in docs]
assert all(len(r)==5 for r in rows)
assert blobs[0]==blobs[1] and blobs[2]==blobs[3]
assert all(r==rows[0] for r in rows[1:])
print(json.dumps({'row_count':5,'all_five_row_dictionaries_equal':True,'both_repeat_pairs_byte_equal':True,'receipts':[{'name':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in zip(names,blobs)]},sort_keys=True))
```

Terminal exit 0: all five complete ordered row dictionaries match in all four
receipts, including original target keys/hashes, classifications and permitted
names. Both implementations' repeated pairs are separately byte-identical.
The independent pair remains 2,995 bytes each with the hash recorded above;
the producer pair is 3,087 bytes each, SHA256
`788b5bfebd85653978dac5b568abd54cc958e5b56f7862baa7f11aa549996f67`.
Whole receipt schemas/bytes are not asserted equal across implementations;
their metadata differ. No comparator mutation controls were independently run
by me in this supplement. No disagreements were found within this exact five-row
comparison, and no extra native fields or element documentation were opened.

The bounded task stops here. Agreement supports reproducible lexical
classification under shared pins and protocol; it does not supply any missing
thermal implementation, parameter value, element activation, physical validation
or historical-cause evidence. Old frozen code/protocol/results remain untouched.

## Allowlist authorship correction

2026-09-28. Attribution-only correction supplied after final review: the earlier
description of the 139-name allowlist as supplied from root's transcription was
imprecise. The separate `/root/testwell_public_search` reviewer authored
`element-allowlist.json` and its source note after reading the primary
documentation page. Root then independently transcribed the 139 names and
checked exact agreement before the freeze. This independent classifier consumed
the pinned list; I did not independently read that documentation page. The prior
13,513-byte text, SHA256
`029900cdd52f14662b530aed114c13691860e59d3066cbf5b2a243db6a85a8a5`,
is preserved unchanged. No source read, calculation or classifier result changed.
