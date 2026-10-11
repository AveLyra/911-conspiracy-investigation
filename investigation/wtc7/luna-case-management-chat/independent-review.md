# Independent substantive review: Map FOIA case-management needs

2026-09-24. Working research review, frozen before reading root's integrated
report. This is a prior-informed AI review, not counsel or an expert panel's
endorsement. Scope is the three retrieved completed turns in task
`01a0b5ff-cdd4-7092-aacb-989d7d271428`, not all Luna output.

## Coverage, controls and attribution limits

Read the full unit PROTOCOL (SHA256
`f04b935bc5a8f3ecb4c471656e796e1b87e8c2c38230ac472b01d83fdb7268aa`),
main AGENTS, WORKFLOW and START-HERE, the repository-owned faculty-review
skill, personal no-pigeonhole skill, and the standing discovery complaint.
Applied the evidence/source-of-truth and orchestration skills. Read Case OS's
public README, engine README, starter README, PLAN, and the complete older
repo-coherence plan identified in the handoff. Inspected the viewer and pointer
validator implementation, and located test names; did not run the application
or tests. The private registry/pages, correspondence, confidential packet and
amendment contents were not inspected for this review.

The app returned three completed turns, no next cursor, and all eight visible
assistant messages. The retrieved response was filtered to user/agent message
objects for substantive review; no reasoning content is copied or relied on in
this note. Each final was shorter than the requested 20,000-character limit.
The first attempted call with30,000 was rejected and supplied no thread data.
An initial combined output was display-truncated; the stored response was then
filtered and every visible user/assistant message printed and read completely.

| Turn | User message ID | Assistant message IDs read, in order |
|---|---|---|
| 01a0b5ff-d0ce-7151-835d-cfff54f83254 | 01a0b5ff-da3b-7822-90c1-834fcb3534c9 | msg_04ea2942fcf6efb8016aad9168071c87d1bc07f3e4a66a9103; msg_04ea2942fcf6efb8016aad91a1999887d1b4a2ce7f02b1385b; msg_04ea2942fcf6efb8016aad92128b1c87d19a2632d3004a7125; msg_04ea2942fcf6efb8016aad9349644c87d1bace639d4154af43 (final) |
| 01a0b608-caf3-7101-afac-0a89d3e026c1 | 01a0b608-cb6c-7020-a0b7-46a8ecaa24b3 | msg_04ea2942fcf6efb8016aad93c4c03087d1b25b23aa99312302 (final) |
| 01a0b60a-a54a-7db3-a250-af660b384c93 | 01a0b60a-a5b7-7440-9b70-e011e283fdfc | msg_04ea2942fcf6efb8016aad942cc49887d18364a85ed5554880; msg_04ea2942fcf6efb8016aad94a5b0b487d1a1d9343432d82155; msg_04ea2942fcf6efb8016aad94f13e8487d1826782985e87b015 (final) |

Below, F1/F2/F3 refer to those three final messages. Root reports per-turn
rollout metadata as gpt-5.6-luna/max, not low effort. This reviewer did not
independently open the rollout or verify model metadata; the separate
attribution audit must establish that claim. The app-visible authorship labels
alone are not model proof.

## Overall disposition

F1 is substantially responsive to the initial read-only request: FOIA-first
product strategy, a metamap, normalized document comparison, professional-tool
patterns, and free-tier sponsorship are addressed. It preserves important
record/interpretation boundaries. It is a proposal, not a demonstrated product.

The strongest substantive issue is F3's unconfirmed substitution of a future
Advocates implementation roadmap for the requested breakdown of changes after
the user raised committing/pushing everything. The most consequential design
gaps are preservation of unique review decisions outside a disposable index
and the private-file boundary in the proposed Copilot handoff. Neither is
evidence that data were actually lost or disclosed.

## Findings and counterreadings

### R1. Commit-handoff scope was silently narrowed

**Evidence:** The initial user requested insight without changing the current
directory. The next user message raised committing/pushing everything,
including WIP; after F2's all-versus-subset question, the user said to break
down the changes into smaller commits, using Copilot if too complex. F3 instead
declares there are no Advocates changes to split and provides future product
commits and a new-app Job1. Its preceding commentary explicitly adopts the
handoff-plan interpretation without confirming that referent.

**Assessment:** There is a material unresolved scope mismatch, not a finding
that the agent was required to push private files immediately. The adjacent
exchange supports the reading that existing work needed inventory and grouped
commits; the answer does not deliver that inventory or grouping. Confidence B
for the mismatch/risk, lower for the user's unexpressed final intended scope.

**Counterreading:** The user could have meant future Advocates work, while
retaining the initial no-edit instruction. That would make a prospective
roadmap useful. It still should be labeled as that interpretation rather than
treated as agreement that existing work is out of scope.

**Correction:** Distinguish existing-WIP organization from future app stages.
Perform or propose a read-only changed-path inventory and coherent commit
groups; retain the exact-payload/destination privacy gate before any push.
Where ambiguity remains material, ask which of those two tasks the user means.
No source records need modification to prepare that inventory.

### R2. Disposable control-plane recovery lacks a source for unique decisions

**Evidence:** F1's proposed rebuildable SQLite/JSON control plane contains
relationships, statuses, deadlines, and human review decisions. It then says
the case should be recoverable after that plane is deleted. The content-plane
list includes originals, Git history, derivatives, and manifests, but does not
specify where independently authored review decisions/approvals are persisted.

**Assessment:** An incomplete recovery contract. Original documents cannot
deterministically regenerate which interpretation a human accepted, which
authority override was selected, or the scope of a prior approval. Confidence
A for the omission; no implemented data-loss defect demonstrated.

**Counterreading:** Versioned manifests could already be intended to contain
those events. If so, make it explicit; the high-level proposal does not resolve
the distinction between durable authored state and regenerable cache.

**Correction:** Store decisions and authority changes as durable versioned
records with source/version hashes, actor, scope, and supersession information;
make the index a projection. Test a rebuild from those records, including
revoked decisions and stale approvals, rather than inferring decisions anew.

### R3. Proposed Copilot context needs its own disclosure boundary

**Evidence:** F3 prohibits real case data and network actions, yet its Copilot
job requires reading absolute main paths for AGENTS, WORKFLOW, START-HERE,
Case OS PLAN, and a case-specific strategy/refactor plan. Some of these contain
case-specific legal positions or strategy, not merely a public engine contract.
Main AGENTS lines203-211 require exact-destination/payload approval for new
potentially sensitive plaintext disclosure.

**Assessment:** A conditional handoff privacy risk, not observed exfiltration.
If the selected Copilot setup transmits file context to a provider, forbidding
network calls in generated application code does not itself prevent that
context transmission. The record does not establish the selected Copilot
processing configuration or clearance of those file contents.

**Counterreading:** The user expressly invited Copilot instructions, and a
particular setup might use only approved/local context. That supports giving
a generic job card, not assuming approval for every case-specific file in its
read-first list. No actual Copilot invocation occurred in the reviewed output.

**Correction:** Supply a synthetic/public-only context packet and public engine
references, or separately identify and approve the exact private content and
destination before use. Do not direct an external agent to recursively index
the live case. Keep the existing synthetic-fixture and no-push safeguards.

### R4. Safety objectives need bounded, testable guarantees

**Evidence:** F1 recommends making external actions impossible without approval.
This appears as an Advocates implication, not a claim that current software
already enforces it. Main AGENTS expressly avoids promising protection against
arbitrary same-user modification; Case OS README says send/privacy/signature
gates stay in case files. The viewed engine is a local pointer viewer, not an
implemented external-action broker or approval system.

**Assessment:** Wording and acceptance-criteria gap in a future requirement,
not a failed present guarantee. A UI confirmation cannot control every host
process, editor, extension, integration, or copied export.

**Correction:** Define the actions mediated by the app; require tested default
denial and approvals bound to exact destinations and artifact versions for
those actions. Explicitly state out-of-app limits. Hashes/Git history preserve
identity and history when used properly; they do not by themselves make source
files physically immutable or authenticate their historical contents.

### R5. Consequence review is appropriately cautious but needs an authorized baseline

**Favorable evidence:** F1 separates textual change from candidate legal effect,
requires evidence, competing interpretations and human decisions, recognizes
party-versus-joint attribution, and warns against automatic keyword conclusions.
No message adopts declaration-only litigation, substitutes Vaughn papers for
disclosures, or attributes a new concession to Plaintiff.

**Remaining design requirement:** Pairwise latest-version diffs are insufficient
if the previous version already contains an unauthorized concession or a form
transfer silently restores an old answer. The source for review must distinguish
the last expressly authorized position, actual sent/filed packages, and agent
drafts. Current AGENTS lines65-75 now expressly require whole-form comparison;
that September23 clarification is a current requirement, not proof that a
September18 message violated a then-existing verbatim rule.

The short FOIA lifecycle diagram omits explicit discovery/disclosure branches.
That is an incompleteness in a future workflow model, **not itself a discovery
waiver or Plaintiff-attributed legal position**. Likewise, requests/appeal/OGIS
nodes must not silently become universal mandatory sequential gates. No legal
exhaustion determination is made in this product audit.

**Correction:** Carry source-backed authorization and competing party positions
through the graph; test all form answers and assembled attachments against the
authorized baseline. Include fixtures in which similar wording is innocuous,
adverse, already corrected, or genuinely agreed. Preserve separate status axes
for transmission, signature, filing, agreement and currentness; F1 proposed
these well, but F3's generic status-word list does not specify that contract.

### R6. Reuse is a stated aspiration, not an explicit implementation decision

**Evidence:** F1 recognizes pointer-only Case OS; F3 nevertheless starts new
`apps/advocates/` and fixture paths without specifying which existing public
engine/assets/starter components to reuse. The current public engine already
provides configuration, registries, ID lookup, rendering and pointer validation.

**Assessment/counterreading:** No duplication was implemented, and normalized
cross-format documents/semantic review may legitimately require new modules.
This is a bounded design decision left open, not proof of reinvention.

**Correction:** Before implementation, identify reusable components, extension
boundaries, and justified replacements. Do not copy the private instance as an
example. Treat the explicitly stale coherence plan as background; current main
authority controls win wherever its historical path recommendations conflict.

## Retain, qualify and defer

Retain the matter-centered UI, source-backed IDs, derived-index separation,
raw/processed/filed distinctions, independently reviewable synthetic-fixture
jobs, candidate-effect review, and sponsor/content separation as useful design
proposals. Sponsor aggregate metrics still require privacy design; aggregation
alone is not proof of anonymity. The proposed free tier is a product objective,
not a demonstrated funded service.

F2's refusal to treat a blanket push as privacy clearance is consistent with
main AGENTS. That does not settle R1's separate local inventory/scope issue.
The architecture, sponsorship, adapters, semantic diff and enforcement gates
have not been built or validated by these messages. The declaration of no
mutations is a claim for the separate tool-receipt audit, not independently
proven by reading the three finals.

Historical repository counts and named vendor-feature descriptions are not
revalidated here. Root owns those source checks; current counts must not be
silently substituted for the dated snapshot. No product benchmark, security
assurance, comprehensive Luna clearance, cause-of-collapse conclusion, or
legal release/send decision follows from this review.

## Actual work and freeze

Performed read-only app retrieval/filtering, source/skill reads, repository
intake, targeted code/test-name inspection, and source hash checks. One lookup
used nonexistent `tools/test_case_os.py` and `tests/` paths; the actual tests
were then located under `apps/case-os/`. No tests or browser were run, no remote
product research was performed, and no code was executed to change the case.
Only this research note was written. Main/raw/legal sources and other reviewers'
files remain untouched. No implementation, staging, commit, push or transmission
was attempted.
