# DistantView index integration execution record

October 8, 2026. Research-only preservation and reference work. Commands below
ran from `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation` unless
otherwise stated. This record does not attest to human review, historical
authenticity or a new physical measurement.

## Baseline and protocol

Root inspected current main-repository AGENTS, WORKFLOW, START-HERE, charter
and isolation instructions; current worktree status; all four DistantView
reports; the existing index, validator, tests and relevant structured records.
The branch is `research/sherlock-wtc7-investigation`, at
`ca1c223335c20905d6608eb15c676f88cbfac734`. Existing unrelated work is preserved.

`shasum -a 256` confirmed that the current index and the old reviewed
`integration-2026-10-08/candidate-index.json` both have SHA256
`6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1`.
The old validator remains SHA256
`97c4cba63dd29ddc0667262a9038bfb86670ee1ddee8e27175e53626c9aaee96`.

Before candidate preparation, root saved the [protocol](PROTOCOL.md), SHA256
`ea61050d5d95fa2978bb33a093331a9e1e44ad11fe3af7241c4366f5685f58aa`.
A separate mechanical reviewer read it and found no material mismatch with
the intended preservation contract. Its clarification requires before/after
integrity checks to encompass the entire wrapper, including the old checker.

## Prechange checks

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest discover -s research/sherlock-wtc7-investigation/synthesis-packet/integration-2026-10-08 -p test_validate_index.py -v
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/synthesis-packet/integration-2026-10-08/validate_index.py --index /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/synthesis-packet/material-claim-index.json
```

The41 synthetic tests passed (root receipts `b48421`, completion `63dda0`).
The unchanged actual index passed all207 selected artifact pins and existing
reference/coverage checks (`854a38`):58 links,19 families and23 transforms.
These checks establish the declared structural/byte properties, not scientific
truth or completion. No historical decoder or simulator was run.

## Implementation and review boundary

The semantic author owns the finite extension, not the current index. A second
agent owns the preservation wrapper/tests and does not choose scientific claim
wording. Root reviews both before freezing the extension and generating any
candidate. A separate mechanical reviewer will inspect the actual candidate.
These roles are separate AI work, not independent scientists or human acceptance.

The intervening acoustic answer supplied a sourced inference clarification,
not a new investigation measurement. The existing Q07 status already retains
the user's reported sounds and hypothesis-specific detection limits; no
blanket absence-of-sounds claim is introduced or restored here.

## Extension freeze

Root read the451-line preparation implementation and its semantic records,
all four underlying reports, the299-line wrapper and350-line test file.
Concrete source locations were checked against saved roster/receipt fields,
report headings and timing tables. The semantic author corrected a source
locator to `streams[0].time_base`; root requested specific WP contribution
labels instead of generic process/substantive labels. Neither correction
changed observations or claim strength.

The initial preparation preview was SHA256
`ff32b646dc5329f3657b48e059b81144084613a90efba69f585eaf85e5760773`;
the locator-corrected saved draft was
`129149d749835abe48f7b10636e39aadfd2f7b20525b73ab9e2dd55fccbd15be`.
Neither was frozen or used to build a candidate. The final role-specific
[extension](extension.json),62631 bytes, is frozen at
`41046974bccc6694b8fe9114a738511a7b8858f784892b8705d7a34f7651cc61`.
Root's `prepare_extension.py --check-saved` returned0 and matched that exact
saved payload (`71c9ce`). This preparation command deliberately requires the
pre-adoption version2 current index; later candidate reproduction uses
`extend_index.py` and the preserved snapshot, not the preparation helper.

Root installed that literal extension hash in the wrapper before candidate
generation. The earlier placeholder prevented production use. The preparation
helper is SHA256
`bfee1837a8603d331b520de4cd7db98f56fab9f0c9958e570ba875876f3d2876`.
Its65 added artifacts are selected entry points, with I01 reused; this is not
a fresh660-file dependency audit or an independent scientific replication.

Root ran23 new synthetic tests, all passing (`fb4a63`). Their legacy-dispatch
tests intentionally mock the old checker; they do not replace the separate
41-test run or the required actual candidate validation. A separate reader
reviewed the wrapper before the literal-hash change and found no material
flaw. Its implementation check and the later candidate review have different
scopes; neither is human or forensic acceptance.

## Candidate execution and adoption

Root's final23-test run after the hash-literal change passed (`74525c`). Final
wrapper SHA256 is
`64129bd9df191e23e4258395d7332c91d0a2c86cc3064d50c78e8edb9c7cd10f`;
test file SHA256 is
`19baab315245d71488abe5fedd19f1b075f50a2f96d3b43767500c6845e65b1b`.
The reviewer independently confirmed that only the literal extension pin
changed from the previously reviewed wrapper (`f26c72`). Its own23-test run
before that pin change also passed (`ca9da3`).

Actual root commands:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/test_extend_index.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/extend_index.py build --out candidate01.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/extend_index.py build --out candidate02.json
cmp research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/candidate01.json research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/candidate02.json
```

The builds used normally approved scoped worktree writes, each returned0
(`3ca4ad`, `dad956`) and each passed all272 selected pins and references.
Root's `cmp` returned0 (`897e5e`). Both are444380 bytes, SHA256
`e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8`.
No candidate or old snapshot was overwritten.

The independent Ruby comparison checked complete protected objects, all58 old
links, the ordered18-addition prefix, exact5/4/2/65 additions, four-unit coverage,
all272 size/hash pins (364405242 bytes),272 unique paths and13 unchanged control
files (`9d6105`, exit0). Its first run's final string guard failed because
`JSON.parse` changed a buffer's encoding label, not file bytes (`e67f09`).
Immediate SHA/binary equality checks showed unchanged files (`07be25`); the
corrected diagnostic parsed a duplicate and used binary equality. No data or
acceptance criterion was weakened. Its actual wrapper check of candidate01
also passed (`4389da`). Unit reachability overlaps are not source-independence
counts. The durable independent review preserves this pre-adoption scope.

The separate content reviewer read the final extension at its frozen hash,
all four reports and selected exact structured fields (`caa336`, `f5662d`).
No material correction was identified. An initially stale message about
pending WP-label refinement was expressly corrected: the reviewer confirmed
the on-disk frozen version already contained the specific labels. The reader
authored the wrapper and several underlying producers; its review is separate
from the semantic manifest author, not independent scientific acquisition.

Only after both reviews passed, root rechecked the old-current and candidate
hashes, generated their exact unified difference and applied it with
`apply_patch`. Post-adoption current/candidate `cmp` returned0 (`2d54c9`).
The final read-only command was:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08/extend_index.py check --index /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/synthesis-packet/material-claim-index.json
```

It returned0 (`6c9278`). Its unmodified JSON stdout is saved in
[validation-receipt.json](validation-receipt.json):63 links,23 additions beyond
the original40,272 artifacts,21 families,27 transforms,12 WP rows,9 dependencies,
8 causal ordinals and the unchanged3 old traversals. These are structural
and selected-byte checks, not fresh inherited scientific reruns or acceptance.

For continuation accounting, the preceding conversational clarification did
not execute a new goal measurement or update research state. This turn
revalidated that state and completed the finite WP0/WP6 integration deliverable.
The full charter goal remains active and incomplete; no model or cause change
is implied by completing this unit.

## Final documentation checks

`git diff --check` returned0 (`5c2447`). A separate trailing-whitespace scan
first failed because the installed Ruby lacks `Enumerator#filter_map`
(`416bf0`); no whitespace result was claimed from that failure. The same scan
using `each`/`with_index` passed for all12 new-unit files (`2f176f`). A local
Markdown-target check passed for all11 then-present report/execution links
(`e67380`); the later independent-review link is checked in the final pass.
An editorial multi-file patch initially failed its exact context check; readback
confirmed no partial edit before the corrected patch. These are documentation
diagnostics, not failures or repairs of the historical scientific methods.

The [independent review](independent-review.md) and its
[verbatim Ruby command](independent-review-command.rb) were archived after
adoption without another execution. That original command retains its
pre-adoption current-index hash, intentionally failing against the now-adopted
version3 if replayed unchanged. Do not replace the live index to satisfy it.
Use the current read-only wrapper for present-state validation; retain the
archived independent command as the exact method of the prior review.

Final readback included the archived independent review and complete Ruby
command; the historical command was not executed against version 3. After
the editorial changes, `git diff --check` passed (`9489a3`), the same whitespace
scan passed all 12 files (`fb78d7`), and the local-target check passed all 15
links across report, execution and independent review (`6e2185`). The current
read-only wrapper passed again (`338aee`), retaining the adopted SHA256 and
all 272 selected pins. No additional scientific or human review is implied.
