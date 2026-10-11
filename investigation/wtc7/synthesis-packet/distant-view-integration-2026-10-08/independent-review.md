# Independent mechanical review — pre-adoption

October 8, 2026. Reviewer: `/root/envelope_arithmetic`. This records the completed
pre-adoption check, not a new post-adoption run. The parent subsequently reported
adoption; this reviewer has not rerun the archived command after adoption.

Scope: exact preservation of the reviewed v2 objects plus the frozen DistantView
extension, candidate identity, declared-reference reachability and selected
artifact bytes. No source acquisition, media interpretation, scientific rerun,
repository-data alteration or acceptance promotion was performed in that review.

## Successful command and pins

The successful inline command was `ruby -rjson -rdigest -rpathname` with a
`RUBY` heredoc. Its complete body is archived verbatim in
[independent-review-command.rb](independent-review-command.rb): 9,932 bytes,
SHA256 `b632bee6365c883d5d7425b876a54ee4afd0aa956c0a3ef8315fa05f51fc1fad`.
The body was preserved without adding imports, changing paths or adapting the
then-current-index expectation. Archive readback matched the archival payload
exactly (`df3b16`); byte/hash check: `143df4`.

Equivalent file invocation, not executed after adoption:

```sh
cd /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/synthesis-packet/distant-view-integration-2026-10-08
ruby -rjson -rdigest -rpathname independent-review-command.rb
```

The script contains all 13 control pins, including these principal pins:

| Artifact | SHA256 |
|---|---|
| Preserved v2 snapshot and then-current index | `6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1` |
| Frozen extension | `41046974bccc6694b8fe9114a738511a7b8858f784892b8705d7a34f7651cc61` |
| Both candidates | `e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8` |
| Wrapper | `64129bd9df191e23e4258395d7332c91d0a2c86cc3064d50c78e8edb9c7cd10f` |
| Wrapper tests | `19baab315245d71488abe5fedd19f1b075f50a2f96d3b43767500c6845e65b1b` |
| Protocol | `ea61050d5d95fa2978bb33a093331a9e1e44ad11fe3af7241c4366f5685f58aa` |

## Observed results

Receipt `9d6105`, exit 0, Ruby 2.6.10p210: pass. The independent implementation
used type-sensitive recursive equality and five parser/type controls. It
preserved all 58 old links, the ordered 18-addition prefix, critical review,
statuses, source joins, old registries and three traversals. It verified the
exact extension and revision, with counts:

| Registry | Old | Added | Final |
|---|---:|---:|---:|
| Artifacts | 207 | 65 | 272 |
| Families | 19 | 2 | 21 |
| Transforms | 23 | 4 | 27 |
| Claim links | 58 | 5 | 63 |
| Additional claims | 18 | 5 | 23 |

The original 40 claims remain. Both candidates were byte-identical at 444,380
bytes. All 272 selected artifact size/SHA256 pins matched, totaling 364,405,242
bytes at 272 unique resolved paths; all 13 controls remained unchanged. All
65 new artifacts were reachable through the new claims or their transforms.
Per-unit reachable/new-artifact counts were source-screen 21/20, correspondence
17/17, localization 15/15 and timing 22/22. These overlapping counts are not
independent-source counts.

The actual wrapper was also run before adoption from the same directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B extend_index.py check --index candidate01.json
```

Receipt `4389da` reported pass: 272 artifacts, 63 links, 23 additional claims,
21 families, 27 transforms, 12 WP components, nine dependencies, eight causal
links and three mechanically reachable traversals. The following hash check
still showed the reviewed candidates and the old v2 current index unchanged.
A separate read-only literal-reversal check (`f26c72`, exit 0) reproduced the
previous wrapper SHA256 `2f7a6cebf7c76ff181b8c1eb8c208fab0db25da962d6f2ce0032833fc757e938`,
confirming its sole change was replacement of the extension-hash placeholder.

## Retained diagnostic failure and correction

The first inline diagnostic (`e67f09`, exit 1) reached its final guard and
reported `changed control baseline`. This was a diagnostic error, not evidence
of changed repository bytes: Ruby `JSON.parse` changed the input buffer's
encoding label from ASCII-8BIT to UTF-8. Ordinary string equality was false;
binary-string equality was true, and all immediately rechecked hashes were
unchanged (`07be25`). The successful command parses a duplicate and uses binary
comparison at the final guard. No repository data were repaired. The original
failure is retained here rather than presented as a clean first attempt.

## Replay boundary and checking ceiling

This historical command deliberately pins `../material-claim-index.json` to
v2 and asserts that it equals the old snapshot. It is not replayable unchanged
against the now-adopted v3 current index. Faithful replay requires the
pre-adoption filesystem state at that expected path, with the other pinned
paths available. Do not overwrite the current index merely to replay it; a
separately authorized reconstruction or a separately identified post-adoption
check would be different work. No such reconstruction or adapted run occurred
here.

Passing establishes mechanical preservation, selected bytes and explicit graph
references only. It does not establish locator accuracy, semantic support,
inherited calculation reproduction, source authenticity or independence,
human/expert acceptance, historical timing or cause ranking. Development-
verification and source-of-truth safeguards kept those levels separate.
