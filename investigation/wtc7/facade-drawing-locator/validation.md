# Locator verification and limits

2026-09-24. Verification of a research locator, not geometry, source
authentication, historical force or collapse cause. Main/raw/legal records
were read-only dependencies. The original locator version and failed guard
claim are retained, not silently rewritten.

## Executed producers and integrity checks

Working directory: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Producer runtime: `/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B`.
All seven commands completed with exit0; the CLI output argument selects a
create-only directory within this unit:

| Implementation at execution | Command suffix | Result |
|---|---|---|
| Original locator | `locate.py --out run01`, then `--out run02` | Identical stem-search results. Original guard later found incomplete. |
| Original identifier wrapper/locator | `check_identifiers.py --out identifiers01` | No path/member/inventory match for new identifier predicates. |
| Corrected locator | `locate.py --out run03`, then `--out run04` | Both byte-identical to the original finite-input results. |
| Corrected wrapper/locator | `check_identifiers.py --out identifiers02`, then `--out identifiers03` | Both byte-identical to the original identifier result. |

Stem result, all four copies: 12,362 bytes,
`d7a9c499fe5fda082d905dc3ad4cc4b068a2b4714b722c667b787db25bb10821`.
Identifier result, all three copies: 11,768 bytes,
`1c371828bc33292bd6f824c74fac2299e89556a91bfc9f828d9b508efd4d72d9`.

Root's read-only Ruby/Digest comparison checked seven receipts, their seven
result pins, all31 recorded dependency references and eight distinct current
or historical dependencies. Before/after maps agree; repeated outputs agree
byte-for-byte. For the old code hashes only, the check deliberately resolves
the exact preserved `source-v1/` bytes instead of falsely requiring the revised
file to match an old receipt. `shasum -a256` confirmed both old code snapshots.
The reusable [verifier](verify_artifacts.rb) encodes that explicit rule.

Initial interpreter calls returned live sessions. Each session was polled to
an authoritative exit0; no run was restarted because a poll timed out.
No old output was overwritten. The new locator subtree is excluded from the
search so its own generated notes and snapshots do not become source hits.

## Independent verification

- [Inventory reviewer](independent-inventory-review.md): separate initial CSV/
  reference search, then independently implemented path/archive enumeration
  frozen before opening root outputs. All six root states, path/count/match
  results, fourteen archive byte hashes and member catalogs agree. Its initial
  LF/sorted serialization remains recorded; an explicit later normalization
  matches root's NUL/order recipe. The initial guard already rejected preceding
  ZIP64 locators. It checked the three new predicates independently, with
  twelve positive/negative controls; the parent had disclosed the expected
  zero direction, so this was not an expectation-blinded test.
- [Source reviewer](independent-source-review.md): complete selected prior
  reports and separately read public album/title-item metadata; one later
  metadata request failed. Source interpretation was frozen before root's
  report. Same source family, not independent historical authentication.
- [Code reviewer](code-review.md): independently designed synthetic fixtures
  proved the original nonsentinel-ZIP64 guard bypass. Thirty-two checks ran
  in the original-version review after correcting the reviewer's own fixture
  field-index mistake. The repaired-version replay passed39 assertions,
  including maximum-comment and constructor-not-entered boundaries. This
  reviewer did not inspect real source payloads or clear arbitrary archives.

The [guard correction](GUARD-CORRECTION.md) records source versions, the bounded
repair and residual malformed-header/format/alias/symlink limitations. The
legacy status string does not mean archive payload *bytes* were never read:
byte hashing streams them; no member was decoded, extracted or interpreted.

Root subsequently read the complete saved [synthetic harness](code-review-tests.py)
and replayed both versions with the pinned Python runtime, `-B`, and
`--source-version original` / `--source-version repaired`. Both exited0 and
returned the same32/39 test counts and implementation pins as the reviewer.
The original replay deliberately **demonstrates** the defect; it is not a
guard-clearance pass. Harness SHA256:
`0b92b2d7ce2fe059b82f01c5c2687d068b27a48f85fc5ff80dba0a6664169d26`.
Only freshly created synthetic temporary fixtures were removed on harness
exit; no research/source artifacts were deleted. `ruby -c verify_artifacts.rb`
returned `Syntax OK`. Root also ran the saved integrity/link verifier, not
just the earlier inline comparison. Its initial nine-document check found
20 existing local targets and nine external links deliberately not reopened;
this paragraph adds the harness link, so later totals may differ.

## Text review and retained failures

A separately tasked source reviewer compared the report/search ledger with
its frozen findings, not with new sources. It corrected root's suggestion
that the preceding search had been unspecified: the prior work already named
the architectural family and target detail. The revised report says this
unit narrows that existing lead to a catalog/file/title-item. No source,
original freeze or historical measurement was changed.

The review's original report pin was
`e71a4cb31fac715b1dcdb8ad0e7a605462b79a1dd32abd05d8311b69f72ae3e9`;
the reviewed search ledger was
`8eeea148c7e4c61c3dc03ca62eec4c748a47e74579b62f5046d4b11aa341e3d3`.
The text review did not independently certify root-only metadata pages,
new approval UI state, enumeration or code behavior.

Other retained limitations: an initial header probe exposed an unnecessary
contact field in tool output; the user was told and no such field was copied
here. Later queries allowlist columns and hash names. Some grouped reads were
truncated and relevant passages were reread in smaller portions. A no-op patch
failed to match before the initial protocol addendum was successfully applied.
These are our workflow events, not evidence about the agency or collapse.

No new PDF/image page, structural solver, historical track, calibrated audio,
physical specimen or operational act was examined. The source image approval
is still pending at this handoff. No canonical promotion, accepted-engine
state, external message, commit, push or publication follows from these checks.

## Final scoped handoff checks

After integrating the report, status/navigation and deduplicated local feedback,
`ruby .../facade-drawing-locator/verify_artifacts.rb` again exited0: seven runs,
31 dependency references, eight distinct pinned dependencies, four identical
stem outputs, three identical identifier outputs, nine checked Markdown files,
21 existing local targets and nine external links deliberately not reopened.
The scoped `git diff --check` on research README, STATUS and SHERLOCK-FEEDBACK
returned no errors. Main `git status --short` showed the same seven preexisting
modified files as orientation; this work made no main edits. Main AGENTS,
WORKFLOW, START-HERE and CHARTER hashes matched the previously read controls.

Final report SHA256:
`fb90cea12178a52a67918c4a6275e44349bd917ae2fd00158922a3c5ba5c24f0`.
Independent inventory/source review hashes remain respectively
`0d100be85b633c23a9fcaf6c29e92c4d5fee36da2933f7f8eb16606604a9b03a`
and `465172b21f353bad60660b36d6048ac8b2695d64440b193fa3a6321556f40862`.
Final code review hash:
`a65bcc68b1468cadae2cca6613401e6b0c337926bd80ced7687e742ca53c4146`.
HEAD remains `e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`; intentional
uncommitted research WIP remains. No charter-completion claim is made.
