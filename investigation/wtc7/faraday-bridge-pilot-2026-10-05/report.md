# Faraday bridge trial remains incomplete

October 5, 2026. Research software capability result, not historical evidence.

**No evidence export was exercised.** The native test runner failed before
collecting a test, and the separate custom matrix failed during fixture setup.
Both failures are in our harness, not demonstrated Faraday export failures.
The single permitted harness repair was already consumed by an earlier
environment-preflight failure. No further repair or repetition is performed
under this protocol. The bridge is not cleared for real investigation use.

## Actual execution and failure attribution

| Attempt | Observed outcome | What it establishes |
|---|---|---|
| First native launch | Environment assertion, exit 1, before target import or run-root creation | Cleared-environment assumption was incomplete on this host |
| Native retry after the one repair | Pytest internal error, exit 3; runner exit 1; 0 collected, passed, failed or skipped | Our output wrapper lacks the `isatty` interface required by pytest; no native assertions ran |
| First custom matrix | Seven successful setup commands, then invalid `contradicts` direction rejected with exit 2; runner exit 1 | The harness used an unsupported enum value; no export case ran |
| Second custom matrix | Not run | Repeating the unchanged failed setup would not test the bridge |

The first failure and exact invocation are preserved in
[native-launch01-failure.json](native-launch01-failure.json). The original
harness remains [separately preserved](verify_bridge-before-repair.py).
The correction removes only the macOS-injected `__CF_USER_TEXT_ENCODING` key
before the otherwise unchanged strict environment check. The initial schema
pin typo is separately preserved and corrected by the pre-execution
[erratum](PROTOCOL-ERRATUM.md).

The native retry's [receipt](captured-runs/native-run02/receipt.json) and
[full log](captured-runs/native-run02/stdout.log) retain the internal error.
Zero reported failures is not a pass: collection never occurred. The complete
selected file's nine required cases remain unverified.

The custom matrix's [receipt](captured-runs/matrix-run01/receipt.json) and
[full log](captured-runs/matrix-run01/stdout.log) preserve the fixture commands
and failure. Faraday's actual direction vocabulary is `supports`, `weakens`,
`refutes`, `inconclusive` (CLI choices derived from `EvidenceDirection`).
Our descriptive intent to include contrary evidence did not justify inventing
the literal `contradicts`. A later repair would need an explicit mapping to the
actual contract, not silently rename a historical result.

Running the unchanged custom mode after the native failure did not bypass a
safety gate: the native failure concerned pytest's terminal interface, the
guard self-controls passed, and the protocol did not require native success
before the independent custom fixtures. Both root and a separate reviewer
checked that reading. The native obligation nevertheless remains unmet.

## Limited results that were actually observed

In both created run roots, the guard allowed its intended local operations
and rejected its four declared outside-write, escaping-symlink, network and
subprocess probes. Neither receipt records an unexpected denial. These are
bounded Python instrumentation results, not an operating-system security proof.

The custom setup created a synthetic exploratory dataset, an agent-staged
`pending_review` hypothesis with `activated_at: null`, and one inconclusive
exploratory evidence record with `scientific_evidence_eligible: false`.
These fields are visible in the saved responses and toy workspace. They were
**not verified through an export**. No human reviewer or acceptance is invented.

The eight recorded commands comprise seven successes and the refused eighth
command. The failed command's complete before/after file hashes and ledger
content agree. Six earlier setup ledger events remain; none is an export event.
The generated raw fixture was neither changed nor removed, because those
declared probes were never reached. Final workspace audit, synthesis and ledger
verification were also not reached. No scientific-rigor or ledger-validity pass
is claimed from this trial.

## Source findings remain source findings

The [independent source review](source-review.md) identifies these implementation
limits: destination references and hashes receive syntax checks rather than
Sherlock endpoint resolution; summaries retain complete record metadata,
including artifact locators; an export appends an audit event while projecting
scientific records; and exploratory raw-file changes may not be rechecked.
It also identifies native fixture descriptions that omit the typed synthetic
flag. **The failed runtime trial does not upgrade any of those predictions
to observed export behavior.**

No native bridge test, successful export, write-once refusal, missing-evidence
export, unsupported export-kind test, destination-digest probe, placeholder
test, contrary-evidence export, stale-source probe, second-run comparison or
two-way integration is verified here. A plausible source-level capability is
not a validated operational bridge.

## Preservation and review limits

The two full generated run trees were copied locally without rewriting their
contents. Root verified all 57 entries: 25 regular-file byte/size/hash matches,
two matching symlink targets and 30 directories. Absolute scratch locators and
symlink targets remain as captured; this is an exact preservation copy, not
a relocated portable workspace. Scratch originals remain retained.

Faraday remains clean at `26ab7c96228b3c7ddcec0539f187d104ba49b47b`.
An external read-only check after both attempts matches all 13 pinned files.
The failed matrix did not reach its own post-run source-pin/import-inventory
assignments; the external check does not retroactively fill those absent
receipt fields or prove a complete transitive runtime inventory.

Both prior source reviews, the harness author and root missed ordinary
execution-contract defects. Their favorable source-readiness opinions were
therefore insufficient. Preserve those reviews, not revised histories implying
that these errors were caught in advance. The final critical review must
evaluate the failed outputs and this narrower conclusion separately.

## Investigation consequence and next work

There is **no change to the collapse-cause assessment**. No real WTC 7 records
entered Faraday, no Sherlock record was imported or accepted, and no historical
measurement, legal record, source byte or human-review gate changed.

The bounded software trial stops incomplete. A future capability retry requires
a separately declared repair scope addressing the output-stream interface and
the actual enum, with synthetic checks before target execution; it is not an
automatic next task or permission to weaken this protocol.

The next independent investigation task is the already identified source/claim
reconciliation: reuse the October 4 fourteen-input comparison and eleven newer
completed reports to reconcile Q01–Q10, the eight causal links and D1–D9.
Trace the selected material claims to their source receipts; preserve source
families, adverse results, completed searches and null audio events. This is
evidence integration, not a substitute for unfinished physical tests or
permission to save the separately held NIST/UAF observation matrix.

Generic software feedback remains deduplicated and local while the existing
archived-task routing question is unresolved. No engine patch, installation,
fee, outreach, sensitive transfer, canonical promotion, publication, staging,
commit or push occurred. The comprehensive investigation remains active and
incomplete.
