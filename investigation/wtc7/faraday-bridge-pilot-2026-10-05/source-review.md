# Independent Faraday bridge source review

Date: October 5, 2026. Reviewer: Codex source-audit subagent. This is an
independent reading of source and tests, separate from the parent task's harness
implementation and execution. It is not independent human review, scientific
validation, security certification, or a WTC 7 finding.

Controlling pilot protocol: [PROTOCOL.md](PROTOCOL.md), read in full before saving
this report; SHA-256
`d6b9a077c97dc2b207a587739f7e697f1b94c055bedee1f7a536c022da2569da`.

## Scope, authority and work performed

The bounded question is whether the local evidence-export implementation can be
tested on explicitly synthetic fixtures while accurately preserving its limits.
Acceptance requires distinguishing unchanged scientific records, an appended
audit event, and newly written export files; typed destination options from
verified Sherlock records; and source predictions from observed runtime results.

Read the entire 666-line `/Users/admin/dev/faraday/AGENTS.md`, main 911
`AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, and the investigation `CHARTER.md`.
Applied the development-verification, evidence-falsification-auditor and
source-of-truth-guardian skills. Their relevant effects were to retain the
scientific claim ceiling, keep research separate from case authority, and avoid
describing unexecuted tests as passed.

Read the entire bridge module, native bridge-test file, bridge-link schema,
`pyproject.toml`, integration README, and add-on registry. Read relevant portions
of the main README, CLI, application service, policies, evidence-admission
validator, filesystem repository, domain models and bundled general-science
add-on. The targeted service reads cover export, dataset classification, evidence
admission, hypothesis staging, inquiry validation, evidence-status reads and
event append. This was not an exhaustive review of the engine or all transitive
imports.

No Faraday code was imported or executed by this reviewer. No pytest invocation,
fixture execution, provider call, network request, live workspace access,
Sherlock import, outreach, commit or push was performed. Shell diagnostics only
read files, listed filenames, queried Git state and computed hashes. Research
filenames were enumerated while locating the charter; no real case-store
contents or credentials were opened. No engine, historical evidence, main 911
file, protocol, harness or canonical store was changed. This report is the only
authorized write by this reviewer.

## Code identity and verification record

Read-only commands actually run in `/Users/admin/dev/faraday` included:

```text
git rev-parse HEAD
git status --short
wc -l AGENTS.md
shasum -a 256 src/research_machine/application/sherlock_bridge.py src/research_machine/application/service.py src/research_machine/interfaces/cli.py src/research_machine/application/policies.py src/research_machine/adapters/filesystem.py src/research_machine/addons/registry.py tests/test_sherlock_bridge.py schemas/sherlock-bridge-link.schema.json
```

`cat`, `sed -n`, `nl -ba`, `rg -n` and `rg --files` supplied the source reads and
navigation. No application verification command is claimed here.

Initial and pre-report rechecks both returned commit
`26ab7c96228b3c7ddcec0539f187d104ba49b47b` and empty `git status --short` output.
`wc -l AGENTS.md` returned 666. Rechecked source pins matched the initial reads:

| File relative to Faraday | SHA-256 |
|---|---|
| `src/research_machine/application/sherlock_bridge.py` | `18a9bba79cbde0df917bdceea592d59c8513a53fcac07ec9571c95e8df5eac79` |
| `src/research_machine/application/service.py` | `e739b18f1ca97814d1c6f001435e38280948f66480a9be5310ba520f9c20c933` |
| `src/research_machine/interfaces/cli.py` | `5fdfed7b4bd63ac9d51df1b6701a1775314daa91d6918ba396a9cf0a9aec67aa` |
| `src/research_machine/application/policies.py` | `a5f8490d9e2e19555d40fe3bf8ea76372852fef10ced546796438958dd143ba2` |
| `src/research_machine/adapters/filesystem.py` | `5b9f428f5f281e517de801f90b46bb14b27d834a05de306f3a77c4bad77bfde4` |
| `src/research_machine/addons/registry.py` | `e99e60426bd75c40f4642bd1e8a6312d76d3581c60d92234d093dbae354bc5fb` |
| `tests/test_sherlock_bridge.py` | `6787df5978a7f273c6df153dd0e0951141182400867ad2d7418bc6a81e17ccbe` |
| `schemas/sherlock-bridge-link.schema.json` | `10400ded1ce9cb771197c4e63eb56d8b122798af9f6c6c6dfb020c24c2b9f662` |

The parent task reports installed Python 3.13.7, pytest 8.4.2, jsonschema 4.25.1,
empty installed `research_machine.addons` entry points, no pytest in the bundled
Python, and no Faraday `.venv`. These are parent-reported environment checks,
not runtime observations independently repeated by this source reviewer.

## Findings

### 1. Native fixtures have a typed synthetic-classification omission

`tests/test_sherlock_bridge.py:123` and `:241` register datasets named
`Synthetic fixture source` without `--synthetic` or a manifest supplying it.
CLI dispatch at `interfaces/cli.py:3272` defaults that field to `False`.
`application/service.py:2660` derives the final value only as
`command.synthetic or any(source.synthetic for source in sources)`.
Neither the dataset name nor surrounding prose changes classification.

Source-supported prediction: these two native fixture datasets are serialized
with `synthetic: false`. This is not a claim that they become scientific
evidence: their dataset-only exploratory records have no run, so
`service.py:7493` derives `scientific_evidence_eligible: false`. The omission is
still consequential for truthful fixture metadata. Preserve native tests
unchanged and describe the limitation; do not reproduce it in the custom pilot.

An honest existing-contract route is available: explicitly register
`--synthetic --role exploratory`, stage a complete toy hypothesis only as
`pending_review` with an agent identity and truthful rationale, and record
inconclusive/contradicting dataset-only exploratory `source_assessment` records.
`policies.py:516` permits exploratory evidence for pending hypotheses;
`:834` allows dataset-only source assessment. `service.py:2198` leaves
`activated_at=None` during staging. No fabricated human identity, engine patch,
manual canonical JSON edit or activation is needed. The parent must observe and
assert these fields at runtime before claiming propagation was verified.

### 2. Export preserves scientific projections but appends an audit event

`service.py:7538` resolves the inquiry, runs its integrity checks, finds the
requested evidence and related records, builds the summary and receipt, writes
the two export files, and then calls `_event` with
`command=sherlock.evidence.export`. `_event` delegates to
`adapters/filesystem.py:547`, which appends and fsyncs a hash-chained ledger row.
That event includes output paths, output hashes, supplied Sherlock identifiers
and authority-boundary fields.

The export method does not save or mutate a scientific record. Its Boolean
`canonical_state_mutated_by_export: false` and receipt equivalent must therefore
be explained with the narrower scientific-record meaning. They do not prove
that no workspace bytes changed. The declared before/after snapshot test should
measure actual projections and ledger differences separately.

### 3. The summary is a full local projection, not a privacy-filtered export

`sherlock_bridge.py:89` and `:103` serialize full inquiry, evidence, claim,
hypothesis, dataset, protocol and run records via `to_dict`. The latest status
event, when present, is also serialized in full (`:50`). There is no redaction
pass in this path. CLI file registration retains an absolute resolved artifact
locator (`interfaces/cli.py:1381`). Dataset metadata, run metadata and status
review roots/locators may therefore appear in a real export.

The output contains records and locators, not an automatic copy of the dataset
file bytes. Nevertheless, record prose and metadata can themselves be sensitive.
The authority flags do not review or authorize disclosure. Keep this pilot
strictly synthetic and local; do not infer safe public export or permission to
copy a real case workspace from successful fixture behavior.

### 4. Destination validation is syntax, not Sherlock endpoint validation

`sherlock_bridge.py:187` requires nonempty trimmed strings, one of six allowed
reference kinds, and an optional 64-character lowercase hexadecimal digest.
An omitted destination ID becomes `pending-<evidence-id>`.
`policies.py:376` adds no identifier grammar, maximum length or interior-control
character check beyond nonempty canonical text.

The bridge does not open Sherlock state, resolve case/reference existence,
compare the declared kind with a destination record, retrieve artifact bytes,
or recompute the supplied Sherlock digest. A well-formed nonexistent reference
and unverified digest are expected to survive as caller declarations. The
published JSON schema describes shape and false authority flags; it does not
establish the truth of the reference. Runtime export does not invoke that
schema validator. No successful receipt establishes import, acceptance,
promotion or two-way integration.

### 5. No provider call is visible in export; CLI startup has extension hooks

The inspected bridge implementation uses JSON, hashing and local filesystem
operations. The service export and repository event paths contain no provider
or network invocation. This supports a bounded source claim only.

Before command selection, `interfaces/cli.py:2363` unconditionally loads a
registry. `addons/registry.py:258` discovers installed
`research_machine.addons` entry points, imports them and calls callable
factories. `:276` executes Python from explicit local add-on paths, including
`RESEARCH_ADDON_PATH`. These hooks can run extension code even for export.

The protocol's isolated environment, cleared add-on configuration, entry-point
recheck and pre-import network/process/write guard address this pilot's path.
Guard review and runtime observations belong to the parent and harness reviewer.
This source audit does not establish comprehensive network isolation or exclude
uninstrumented native operations. Direct service tests would avoid CLI registry
dispatch, but would need to be labeled service tests rather than CLI coverage.

### 6. The read scope is larger than one selected evidence record

`service.py:7542` calls `show_inquiry` before option validation and selection.
`show_inquiry` validates the inquiry's claims, hypotheses, datasets, protocols,
runs, evidence, status events, recommendations and cross-lane lessons. Some
branches replay local custody, review or run artifacts. This makes an actual
workspace inappropriate for a supposedly isolated single-record pilot. The
fresh toy workspace bounds those reads and avoids unrelated state.

For an exploratory synthetic dataset without protected custody requirements,
the inspected inquiry-read path validates its sealed manifest but does not
re-hash the raw source file. A changed or missing raw fixture may therefore be
exported with the registered old digest and locator. That is a source-supported
prediction for the declared stale-source probes, not an observed result or a
new fail-closed guarantee the exploratory contract promises.

### 7. Write-once behavior is bounded and not an atomic export transaction

`service.py:7618` resolves and expands the caller's output path without confining
it to a trusted root. `sherlock_bridge.py:210` rejects an existing output
directory, creates parent directories and writes two files sequentially.
Each file uses exclusive creation of a process-specific temporary name, flush,
fsync and replace (`:35`). Exception cleanup attempts to remove the two final
files and the final directory; created parent directories may remain.

The ledger append happens after file publication. If it fails, export files can
remain without their export event. No combined filesystem/ledger transaction,
hostile-concurrency proof, symlink-safe path boundary, or filesystem immutability
mechanism is supplied. The hashes can detect changed bytes when compared with
an independently retained trusted value; the word `immutable` does not prevent
someone from modifying a file. The declared existing-directory test establishes
ordinary non-overwrite behavior only.

### 8. Status and hashes retain narrower meanings

With no evidence-status events, `sherlock_bridge.py:55` emits
`status=active, source=implicit_no_status_event`. This is record-status history,
not an active hypothesis, human acceptance or scientific evidence eligibility.
Inspect the explicit hypothesis and evidence fields separately.

`evidence_payload_sha256` excludes `admission_checks` by design. The summary hash
covers the serialized summary bytes, including those checks when present.
Neither hash authenticates historical chronology, reviewer identity, truth,
Sherlock custody or scientific conclusions. The tests should assert their
precise byte relationships without assigning those stronger meanings.

## Coverage limits and proposed interpretation

The native file defines nine parametrized cases by source count: example schema,
four forbidden-authority-field schema cases, integration ignore rules, charter
hash binding, ordinary CLI export and existing-directory refusal. Actual
collection/pass/fail/skip counts remain to be measured. In particular, the
native assertions compare hashes and authority labels, but do not independently
prove unchanged scientific projections, redaction, endpoint resolution,
explicit synthetic propagation or atomic ledger/output publication.

High confidence applies to the explicit data flow and validation omissions in
the pinned source. Runtime behavior remains unobserved by this reviewer.
The strongest objection to a broad safety conclusion is that the full record
projection retains local metadata and CLI extensions execute before dispatch;
a passing isolated fixture cannot clear those properties for real data.

The parent protocol's synthetic matrix can demonstrate export preservation,
ordinary refusal behavior, explicit synthetic classification and actual mutation
boundaries within its guarded test conditions. It cannot validate a scientific
claim, authorize real-data export, prove an operational Sherlock endpoint or
complete WP0/the investigation. Preserve contrary results and product limits;
make no engine repair in this pilot.
