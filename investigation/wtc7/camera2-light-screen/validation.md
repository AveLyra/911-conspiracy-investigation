# Execution record: Camera2 qualitative light-change screen

2026-09-24. All work is exploratory research in the dedicated investigation
worktree. Main charter, source preservation and actual-human review boundaries
control. Input/presentation checks do not establish a historical light event.

## Preparation and actual commands

Main read the complete protocol, source/method checks, producer and tests,
including the final test-only changes. The initial name implying a post-change
test was corrected; a separate runtime-pin-change refusal test was added.
Protocol was fixed before current historical views. Skills used:
repo-orchestrator, evidence-falsification-auditor, source-of-truth-guardian and
development-verification; they require source integrity, explicit uncertainty,
scoped changes and actual verification rather than accepting an AI narrative.

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
Runtime in every command below:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(Python3.12.14, Pillow12.3.0).

```text
python3 -B research/sherlock-wtc7-investigation/camera2-light-screen/test_present.py --out controls02
python3 -B research/sherlock-wtc7-investigation/camera2-light-screen/present.py --out run01 --expect-code-sha256 71074fe186b99f99c1cf8ccd4f7c980e0ed4abb8f76f389f8cc6f2f1798c38b1 --expect-protocol-sha256 8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25
python3 -B research/sherlock-wtc7-investigation/camera2-light-screen/present.py --out run02 --expect-code-sha256 71074fe186b99f99c1cf8ccd4f7c980e0ed4abb8f76f389f8cc6f2f1798c38b1 --expect-protocol-sha256 8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25
```

Here `python3` denotes the exact bundled executable above, not PATH selection.
Root controls02: **12 tests passed**, exit0, 10.185s. Author controls01:
12 passed, exit0, 10.140s. The author's first default-sandbox output-directory
attempt was denied before output creation; scoped approval allowed the run.
No acceptance criterion was removed. The test outputs and receipts preserve
their actual commands. Fixture images are synthetic, not historical evidence.

Controls exercise complete schedule and adjacent pairs, pixel-preserving
rectangles, labels, exact clocks/receipt joins, wrong/missing/reordered inputs,
tamper and multiframe rejection, existing-output/symlink refusal, retained
render warning/failure, runtime-change refusal and two complete synthetic runs.
This tests representation, not salience thresholds or flash-detection accuracy.

Root displayed controls02/synthetic-page-00.png once using original detail.
All six synthetic patterned cells and external labels were readable, in the
declared layout. This is a display-route check, not human/forensic validation.

Historical runs01/02 each exited0 with 84 pages, 421 unique source frames and
504 display slots. No historical image had yet been viewed at this point.
The source's one recorded stereo-layout diagnostic remains; no new presentation
warning was recorded. No fresh video decode took place.

Root separately used a read-only Python stdlib check, importing no producer,
to rehash every receipt product and compare both product dictionaries:
**93 identical substantive products per run**. It also checked all84 ordered
six-index arrays, 504 slots, exact421-index membership and all420 adjacent
pairs. Both input and runtime before/after dictionaries matched. Receipts
themselves differ in their recorded output command and are not counted as
identical substantive products. Complete pixel/label verification is separately
recorded in source-check.md before admission to image viewing.

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25` |
| present.py | `71074fe186b99f99c1cf8ccd4f7c980e0ed4abb8f76f389f8cc6f2f1798c38b1` |
| test_present.py | `51d59a2157b2a0898096fccebe5f0597dbd8967cd277596c2ae5495f43582010` |
| controls02/receipt.json | `7a75b53458acc0dbbbd3b5d8ae8f076ebb1befec86d32a155da757be47b7b2ae` |
| run01/receipt.json | `bafcb0d149a7e6867ec02b8d106aa573c973391bcb94bfa3370a809f360bd473` |
| run02/receipt.json | `8a5d32bb0cd481939222e6f13da48764d840e5597a70e4b80527d68b27c5148d` |
| run01/manifest.json | `58e9ae14cfc47c4fddd1caf883675c9387aafc28daac65f10c0bd42f68d5869d` |

## Separate human-coordinate review

The user's reply that their viewer cannot show reliable pixel coordinates is
not approval or an observation. The R1 human gate remains pending. The existing
read-only viewer's execsession18331 was checked as still running; sandboxed
curl failed to connect, while the narrowly approved loopback GET returned
HTTP200 at http://127.0.0.1:49761/. No second server was started and no human
review was simulated. The existing R1 HUMAN-REVIEW.md remains the guide.

## Historical reading and synthesis

The primary reading completed all84 pages: root0–27, A28–55 and B56–83.
The fixed independent reader completed its15 prescribed pages. All four
records report one successful original-detail display per page, explicit
per-frame dispositions saved before the next page, and no failed display,
retry or extra historical image. Reader C disclosed a context compaction
between viewing page54 and saving it, before its next page; no redisplay.
The records froze before substantive exchange. These are observer logs,
not a claim that a later parser independently verified every screen exposure.

| Frozen record | SHA-256 |
|---|---|
| root-observations.md | `951680468bfc3ffd57609a22b4b7ef5857069a5c99abb1a2484d9901fa4f536c` |
| reader-a-observations.md | `0ce25e6f7979d0a6edfabe5d15bedfe7a1e2a1318cf19eda54b350583bbfd0fd` |
| reader-b-observations.md | `3492a60102235ac78e6a5639d36e9b02ab3b628322e1be4ee881b0e4a592231c` |
| reader-c-observations.md | `40df160cb1947c24274b3767a5cc150be01e4afcb6e15f7187b2e00bad71ad91` |
| source-check.md, after presentation appendix | `a3600bb82f369b342e5bd585c33a4d775ba9630d963b3e98a1e5bb33b1244113` |
| comparison-review.md | `4086f52511992b622c8fb51d808a53baa0398462215270a6e17e4b04d0a3f6ff` |

Root's initial own-row parser failed because it also counted a prose repetition
of an index/code. It was corrected to parse the bold disposition row only;
the frozen record was not changed. Root then used an independent Python3.12.14
stdlib regex parser on all four files, checking each six-index page against
the fixed formula. It reproduced504 primary rows/421 unique indices,90 fixed
rows, every candidate location and all90 pair categories from the separate
Ruby check in comparison-review.md. The Ruby check initially used unavailable
Array#tally, then an explicit counter; that failure is preserved there.
No historical light measurement or confidence estimate was calculated.

Pair categories (primary/C): U/U1, N/U11, C/U3, N/N59, C/C1, C/N15.
The14 differing context-only rows are separate from15 C/N differences.
The three primary U entries are block-start context limits, not unreadable
images. Both cross-reader boundary pairs remain unchanged. The continuing
roof-edge C run includes a distinct point description at6970; the candidate
ledger preserves it instead of collapsing it away.

## Declared result-selected follow-up

FOLLOWUP.md was written and hashed after all freezes and before additional
views: `1dd6858ef245eebb61d6bf336bd1d86f0e3f6ccb8178437703d0c66d2772a797`.
C viewed pages27/28, A66/75, root72/78/83. Each saved before the next page;
all7 displays succeeded at original detail, zero retries or extra images.
These are42 further display slots, not42 independent exposures. Together
the first pass/sample/follow-up comprise106 page presentations of the same
421 underlying held images. No crop, enhancement, new decode or measurement.

| Follow-up | SHA-256 |
|---|---|
| followup-c.md | `066a6792f9f94471c0a315ab5d37329c7cb3da7bbf13f1db8ff48fae9107509d` |
| followup-a.md | `e71b1e06d7923e7d1e444c10ca9339463d50597287ffc69ecb87d4bfe3a66c24` |
| followup-root.md | `c36c9a7afd1aad078689cecd5b8d9d558587170763a4229ebff0b8c202bd5d08` |

Root read complete comparison/follow-up records before synthesizing report.md.
The two late bright-point descriptions and notch continuation have contextual
corroboration, not physical-source authentication. The late pale-rim labels
retain their disagreement and unpaired portions remain first-reader-only.
No final7013 continuation, flash absence or causal ranking was invented.

## Repository and release boundaries

Branch `research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`; intentional investigation WIP
remains uncommitted. No staging, commit, push, outside retrieval or transfer.
Main showed the same seven preexisting changed paths on final inspection;
this unit made no main/raw/legal/accepted-engine edits. Main AGENTS, WORKFLOW,
START-HERE and CHARTER hashes matched their initial pins. No actual human
review, Sherlock/Faraday acceptance or all-Luna clearance is claimed.

Generic sequential-page/context/parser lessons were deduplicated into existing
SFB-002 locally. The final comparison added the generic distinction between a
new candidate, its continuation and no additional candidate, including nested
candidate preservation. Nothing was sent to the archived Sherlock task.

## Final critical review and closeout

The separately tasked critical reviewer read the assembled records, checked all
504 primary/90 paired rows and requested two report corrections. First, a
processing artifact can explain a visible point without refuting its appearance.
Second, the point-directed page 75 follow-up also supplied pale-margin context,
without adjudicating rim coding. Both corrections were made in the mutable
report; no frozen record changed. The reviewer read the full revised report
and found no remaining material blocker to closing this fixed qualitative
screen on its stated terms. Its prior source-check/Reader B role and common
AI/source limits are explicit, not described as wholly independent evidence.

Root read the complete [critical review](critical-review.md), including its
revised-draft disposition. Pins:

- Critical review: `8e7f4a77cf7ad762bae816417cd4267a16f8729ecfa064379b06706120fd43f6`.
- Reviewed revised report: `f1c53d3d039fe3d6dc69e0a19747e74ba14f6ca93110fc0e382e0c5720bbcfcd`.
- Final report, only the pending-review header replaced with the review link:
  `b81f2e3a287804891b32552ee89c4c04d14e299524205f219a1ffdb972b3a2de`.

A separate read-only Node v22.16.0 parser checked all 17 reported artifact pins,
all disposition schedules, 83 boundary repeats and all 15 six-pair comparison
table rows (90 paired indices). Exit 0; counts match those above, with 81
unchanged repeats and the two disclosed context-boundary differences. Its
12-link check applies to the earlier report hash
`16db68b953b20eaef57c205ad9437050a964394239ca5682da9c47cbea0deae1`
and validation hash
`7d4bf1cbe41aef3bebaa92fcec87b9f296dd30aa1fddeeb83c45b5273e6cba4a`,
not later documentation edits. All 19 files read remained unchanged during
that check. It viewed no images and did not rerun the producer or tests.

Root's stdout-only `node - <<'JS'` link check then verified all 13 local links
in the corrected report and the new navigation sections' four links. The
final stdout-only Node check passed all 20 local links across report (14),
validation (1), current STATUS section (3) and new research-map section (2),
and verified the final report/critical-review pins above. No images were opened.
`git diff --check` exited 0 for tracked changes. `git branch --show-current` and `git rev-parse HEAD`
confirmed the branch and HEAD above. A fresh main `git status --short` still
listed only its seven preexisting changed paths; `shasum -a 256` confirmed the
same AGENTS, WORKFLOW, START-HERE and CHARTER pins. No broader dirty-worktree
content or unrelated WIP is certified by these checks.

The context-distiller skill kept the existing STATUS and research map current:
bounded screen complete, broader goal active, precise source/scene follow-up,
unchanged human gates and intentional uncommitted state. This is not acceptance
of a physical light source, detector accuracy, a cause ranking or all Luna work.
