# Independent pre-execution harness review

October 5, 2026. Reviewer: Codex source-audit subagent, separate from the harness
author and root executor. This is source inspection, not an executed guard test,
human review, security certification or scientific validation.

## Disposition and exact reviewed inputs

**Suitable for the declared bounded synthetic trial, subject to the protocol's
runtime gates. No blocking source defect or additional correction was identified
in the final version below.** Root retains responsibility for the exact launch,
observed guard controls, stopping on safety failures, preservation and final
outcome review. This disposition provides no broader execution authority.

| Input | SHA-256 |
|---|---|
| `verify_bridge.py` — final reviewed 445 lines | `5747e97e9f08220c1f09ef49701464b152c9e1910c94dc9ae6caada0e772d3fd` |
| `PROTOCOL.md` — preserved original | `d6b9a077c97dc2b207a587739f7e697f1b94c055bedee1f7a536c022da2569da` |
| `PROTOCOL-ERRATUM.md` | `727bc53e3ee790cfc560630f237297f1ce25ace83596ba293793d4b98096acf8` |

Read both protocol files in full and the entire harness, including the final
pinning changes. The initial 440-line draft, SHA-256
`a55cb7694eb48f609f2122bc39503effe921bc37864f4b8b89ff580a4ca0b4f3`, still had a
placeholder protocol pin and lacked the erratum pin. That version was reported
as not ready; no trial was approved from it. The final version checks both
document hashes and retains both documents inside each run directory.

The corrected schema pin is
`10400ded1ce9cb771197c4e63eb56d8b122798af9f6c6c6dfb020c24c2b9f662`.
The original protocol's shorter transcription is preserved and superseded only
by the separate erratum. This correction does not alter test scoring or engine
bytes.

Used the earlier [source audit](source-review.md), and reread relevant CLI and
service dispatch for workspace audit, synthesis and ledger verification. Read
and hashed the final harness and documents with shell `sed`, `rg`, `wc` and
`shasum`. No harness import, AST parse, target-code import, application command,
pytest execution or fixture calculation was performed by this reviewer. The
author's reported AST-only check is not an independently repeated result here.
No protocol, harness, engine or historical record was changed. This review file
is the only write in this review task.

## Guard and isolation assessment

The harness checks an exact isolated, bytecode-disabled Darwin Python 3.13.7
executable and a narrowly cleared environment before installing its audit hook.
It requires a fresh, nonsymlinked immediate child of the declared temporary
parent. The guard is installed before creation of that run root and before
Faraday or pytest import. It rejects a pre-imported Faraday module and rechecks
that installed Faraday add-on entry points are empty before target execution.
No external add-on path survives the permitted environment keys, and no custom
CLI call supplies `--addon-path`.

For the inspected code path, the audit hook addresses writable opens, directory
creation, removals, renames, hard links, symbolic links, metadata mutations,
truncation, directory changes and temporary-file destinations. It checks both
rename/link endpoints and both the symlink destination and resolved target.
Descriptor-based path lookup uses Darwin F_GETPATH; an unresolved mutation
target is denied. The guard rejects audited socket/process operations and
foreign-call access via the listed ctypes events.

The self-controls require successful in-root writes, temporary-file replacement
and an in-root symlink write, followed by refused outside write, escaping
symlink, socket creation and subprocess attempts. Expected denials are labeled
separately from any target-time denial. `BoundaryViolation` derives from
`BaseException`, so the application's ordinary ValueError handling cannot turn
the denial into a normal acceptable refusal. An unexpected denial invalidates
the receipt. Custom commands unwind immediately; native pytest also refuses
subsequent test setup if a denial has been recorded.

This is appropriate bounded instrumentation for these inspected local fixtures.
It does not inspect all possible Python audit events, constrain reads generally,
prove protection against native extension calls or inherited descriptors, solve
concurrent path replacement, or cover interpreter/stdlib initialization before
hook installation. The harness and protocol disclose the lack of an OS security
sandbox. Do not convert an absence of recorded unexpected denials into a claim
of universal network/write isolation. Runtime self-control outcomes remain
unobserved at this review stage.

## Native test invocation

Native mode invokes the unchanged exact
`/Users/admin/dev/faraday/tests/test_sherlock_bridge.py` with installed pytest.
The run has an in-root empty pytest config, `--noconftest`, importlib import
mode, a fresh in-root base temporary directory, no cache provider, and disabled
third-party plugin autoload. A small reporting plugin records collected items
and per-phase reports without changing the tests. The harness requires exactly
nine collected and nine passed cases, zero reported failures/skips, and pytest
exit zero. Source/test/schema pins are checked before and after execution.

The native omission of `--synthetic` is explicitly retained in the native
receipt; the tests are not altered to conceal it. Native success can establish
only their actual assertions. Per-phase failure/skip counters are not a separate
collection-error counter; if collection fails, use the pytest exit status and
retained full stdout/stderr rather than summarizing only those counters.

The local pytest configuration and disabled third-party hooks mean this is the
complete selected native test file under the declared isolation setup, not the
entire repository's CI campaign. The protocol does not ask for a broader run.

## Custom fixtures and coverage

The fixture case uses an explicit `codex-synthetic-fixture` actor, a toy
proposition with prediction, alternatives and falsification, and agent staging
to `pending_review`. Its rationale expressly keeps human review pending.
The dataset uses both `--synthetic` and `--role exploratory`. Inconclusive and
contradicting source-assessment labels are explicit software fixtures, not
independently derived scientific evaluations. Neither human activation nor
confirmatory evidence is requested.

The success checks compare complete exported inquiry, claim, hypothesis,
dataset and evidence payloads against the returned fixture records. They check
synthetic/exploratory/non-scientific status, pending review, direction,
uncertainty, claim ceiling, both file hashes, receipt-to-summary binding,
evidence commitment, false authority flags and published schema conformance.
The exported locator and metadata are retained for disclosure-limit inspection.
Schema checking uses a date-time format checker in addition to structural
validation.

The fixed cases cover ordinary export; existing output refusal; missing
Faraday evidence; unsupported reference kind; malformed destination hash;
nonexistent destination plus well-formed unverified hash; omitted ID; the
contradicting record; and separate changed/missing raw-source probes.
The unknown-destination and stale-source probes use `expected=None`, preserving
acceptance or refusal instead of inventing a product requirement. The explicit
unsupported-kind case is a CLI parser refusal; it does not establish a separate
service-level bypass test.

The original generated raw CSV is retained before the declared mutation. The
changed CSV is recoverably renamed inside the run root for the missing-source
probe. Canonical dataset records and historical inputs are not manually edited.
There is no post-result adjustment of fixture classification or acceptance
thresholds.

## Mutation snapshots and final audit/synthesis

Every custom CLI call records argv, stdout/stderr, exit or exception, complete
workspace file hashes and parsed ledger content before and after. Each export
requires unchanged non-ledger workspace bytes. A successful export must retain
the old ledger prefix and add exactly one `sherlock.evidence.export` event;
a refusal must retain all workspace and pre-existing output bytes and leave no
new output. The native mode separately retains its generated file inventory.

These are file-byte and ledger-content checks; they do not prove unchanged
filesystem permissions, directory-only state, external reads or all operating
system activity. For the fresh inspected fixture workspace, they answer the
protocol's scientific-projection versus export-event question. Root must still
inspect the actual event payloads and saved outputs when interpreting results.

The later `workspace audit` invocation uses the engine's existing default
`fail_on=never`. The harness marks command completion, while retaining the full
audit response, including warnings or errors. Exit zero must not be reported as
scientific-rigor clearance. The trial's `passed` flag is a software-check result.

`synthesis build` intentionally writes `current-synthesis.md`, updates
`inquiry.current_synthesis_path`, and appends a `synthesis.build` event
(`service.py:7863`). These changes occur after the export cases and are captured
in their own command snapshots. Therefore “exports left scientific projections
unchanged” must be supported by those export snapshots; “the entire completed
matrix left the workspace unchanged” would be false. Synthesis text and its
limitations are retained. Final ledger verification checks the ledger after
those permitted changes; ledger validity does not validate scientific content.

## Remaining execution and reporting work

The harness performs one selected mode per invocation. Root must run the native
mode and the two separately named fresh custom matrices, preserve every attempt,
and compare the two matrices' declared outcomes and semantic fields. The harness
retains a normalized semantic-result structure but does not itself launch or
compare the two matrices. Root must also perform the protocol's engine Git
cleanliness/revision recheck and retained-output review. These are existing
protocol tasks, not missing authority for additional testing.

No software trial has passed by virtue of this review. A pin mismatch,
unexpected guard denial, failure of a guard self-control or actual boundary
escape stops the trial under the preserved protocol. Do not broaden the allowed
paths or change the engine to make a trial pass. Other harness defects, if
observed, remain subject to the single documented harness-only repair allowance.

The strongest limitation on a favorable interpretation remains that this is a
synthetic export test: it does not check a real Sherlock destination, admit a
record there, establish privacy-safe export of real data, authenticate history,
validate a scientific inference, or change a WTC 7 hypothesis ranking.
