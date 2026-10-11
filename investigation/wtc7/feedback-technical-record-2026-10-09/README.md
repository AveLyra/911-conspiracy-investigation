# Sherlock feedback technical record

This packet preserves the technical requirements in the frozen October 9,
2026 feedback log, including acceptance cases, negative controls, conditions
and limitations that a 27-topic digest can compress. It is a requirements
record, not a finding about a collapse, a product implementation, or a new
scientific result.

Read [the detailed requirements](REQUIREMENTS.md). The editable source is
[record.json](record.json); the Markdown view is generated from it. Stable
source-line IDs map each unit to the frozen source and to the earlier digest
topics. [Review and verification](REVIEW.md) records the completeness and
publication checks and their limits.

## Scope and authority

The selected source is the local `SHERLOCK-FEEDBACK.md` snapshot with SHA-256
`e1c718bb928ba846deb0d527f69cda7ea00a8d888c2247a864b1d666b4204133`,
containing 2,468 lines. Its source log and underlying evidence remain preserved
unchanged. This packet neither replaces raw evidence nor changes the meaning
or approval status of source records. It does not claim to inventory every
requirement in Sherlock's codebase, every investigation file, or future notes.

“Requirement complete” here means that every technical obligation, example,
limitation and acceptance condition identified in that finite source has a
reviewed technical representation; every source line has an explicit
disposition. Line coverage alone cannot prove semantic completeness. A missed
condition would require an additive correction and a new packet version, not
rewriting the preserved source or asserting that its meaning never changed.

Chronological recurrences remain separate where their examples or constraints
differ. Shared digest and SFB mappings group related requirements without
discarding refinements. Source-ordered repetition is intentional: this is a
traceable technical transcription, not another condensed roadmap. Historical
claims about local checks are attributed claims, not newly executed tests.
Acceptance lists restate the source conditions in checkable form; they are not
new product tests or an instruction to implement them all in one change.

## Publication transformations

The same technical packet is intended for `AveLyra/911-conspiracy-investigation`
(public) and `roryscot/911` (private). Publication includes this packet only,
not original case files, private product code, litigation correspondence or
the original feedback log. Administrative routing details, personal or local
identifiers, and private source links are omitted or generalized explicitly
in each unit's publication-transformation field. Substantive conditions must
remain; sanitization is not permission to weaken an acceptance criterion.

Source-span hashes permit comparison against the authorized local original.
They contain no plaintext source text, but are not a privacy guarantee:
candidate text can be checked against a hash. They do not prove historical
authenticity or let a reader lacking the original independently check
transcription fidelity.
The public packet remains inspectable without private files: its requirements,
coverage map, checker, controls and review are included. Original-source
comparison requires separately authorized access to the matching snapshot.

## Status distinctions

The earlier 27-item batch was delivered and acknowledged. That does not prove
that its recipient log retained every detailed requirement. In particular,
classifying digest items 15, 16 and 27 as “already covered” did not verify
implementation or preservation of every refinement. This packet supplies the
detailed record; repository publication alone is not a new recipient
acknowledgment, implementation assignment or product fix.

SFB-001's later local adoption verification supersedes its early unresolved
status; the historical note is retained without reopening the resolved issue.
SFB-002 through SFB-005 include workflow requests and observations from local
methods, not generally source-inspected Sherlock defects. Proposed acceptance
tests remain proposed unless a specifically attributed test record says otherwise.

The last source-log bridge note describes an earlier schema-only inspection.
A later, separately recorded synthetic export pilot executed two matrices
with 136 checks each and nine existing native tests. It preserved exploratory
flags, but also accepted unresolved destinations and unchanged registered
metadata despite changed or missing raw files, and retained local locators.
These are exporter-boundary observations, not automatically contract defects.
The later pilot does not establish two-way Sherlock admission, source
authenticity, scientific-method validity or human acceptance. The earlier
digest's item 25 already reflects this later status; no real-data bridge is
authorized by this packet.
This publication-time status context is supplemental source SUP-01,
`CONTROL-RETRY-RESULT-2026-10-07.md`, SHA-256
`170e97cdc0ea352254270546655ad7f17443e44fa19ca531a720627c680202ce`.
It is not a statement contained in every older feedback span and is not
included as raw source text in this publication. The unit qualifications and
JSON supplemental-source record identify that attribution separately.

## Reproduce the record checks

From this packet directory, using Python 3 with its standard library:

```sh
python3 -B verify_record.py --manifest
python3 -B -m unittest -v test_verify_record.py
```

With separately authorized access to the exact local source snapshot:

```sh
python3 -B verify_record.py --source /authorized/path/SHERLOCK-FEEDBACK.md --manifest
```

The source path above is a placeholder, not an acquisition instruction.
`--render` regenerates `REQUIREMENTS.md` after an intentional JSON edit; this
changes a released artifact and requires renewed review and manifest versioning.
The checker enforces complete ordered spans, source pins when supplied,
required fields, mappings, generated-view equality and exact packet file hashes.
Its negative controls test structural failures. Neither those checks nor a
passing unit suite independently establish semantic completeness, privacy,
Sherlock feature coverage or scientific validity.

## Further corrections

Use the stable technical unit ID, the missed source condition, and the exact
proposed correction. Retain the old packet and original feedback. A fresh
implementation task should select relevant requirements and run their actual
product acceptance checks; do not mark every requirement implemented merely
because this record is complete or published.
