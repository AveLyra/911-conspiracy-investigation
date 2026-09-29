# Validation and continuation record

2026-09-19. Research-only; the comprehensive goal remains active/incomplete.

## State and durable decisions

Investigation checkout: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`,
branch `research/sherlock-wtc7-investigation`, HEAD `e8d83d7`. Existing substantial
uncommitted research is intentional and preserved. This unit adds
`camera2-paper-frame-join/` and updates existing worktree navigation/feedback;
it does not commit, push, edit main records, or activate any Sherlock/Faraday
finding. Main source files are read-only dependencies.

The source-derived labels and candidate image features remain separate from
authenticated material points. Old T2 is the upper step corner; it is not the
paper's lower WC point. Neither source download identity nor table-arithmetic
agreement supplies scale, time zero or original track identity. The root
file-freeze rule failed before coordinate comparison; that independence limit
is retained, not repaired by numerical agreement. Original annotations and
initial settings-review coverage stay frozen.

## Executed verification

Root used Python 3.12.14, Pillow 12.3.0 and pypdf 6.10.0 from the bundled runtime.
From the investigation checkout, these commands ran:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/camera2-paper-frame-join/verify_join.py --self-test
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/camera2-paper-frame-join/verify_join.py --output research/sherlock-wtc7-investigation/camera2-paper-frame-join/verification01.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B research/sherlock-wtc7-investigation/camera2-paper-frame-join/verify_join.py --output research/sherlock-wtc7-investigation/camera2-paper-frame-join/verification02.json
cmp research/sherlock-wtc7-investigation/camera2-paper-frame-join/verification01.json research/sherlock-wtc7-investigation/camera2-paper-frame-join/verification02.json
git diff --check
```

The seven synthetic test methods passed before historical verification and
again after the PDF-lookup correction. They test signed differences, complete
membership, duplicate/missing rows, reversed/out-of-frame/non-integer bounds,
out-of-bounds centers, ambiguity regions remaining unmeasured, and overlap
versus touching/disjoint boxes. Both historical runs exited 0; `cmp` exited 0.
They confirm source PDF/MOV hashes, the page's embedded Figure 4 bytes,
selection metadata, both native PNG/luma identities/geometry/PTS, all eight
record pairs, and the recorded independence limitation. This verifies record
and arithmetic integrity, not visual or physical validity.

Initial historical attempt exited 1 before writing output: pypdf's page image
lookup requires an XObject key, not the exported filename; using `Image76.jpg`
as that key raised `KeyError`. A read-only inspection showed `/Image76` as key
and `Image76.jpg` as exported name. The corrected code selects the unique page
image by its exported name and verifies its bytes. No source image was changed;
the failure does not indicate missing Figure 4 or corrupt historical evidence.

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `bbd5301cbb912b073fe166d42d59a18900b269a71ea55967a178a4782b27e807` |
| ADDENDUM-01.md | `5cb6e8c9dd32f244a0f98ea35dcefdc226976cf22b76d84d20bb34da1c1dec79` |
| root-feature-proposal.json | `64691f300a697a459cc35af2417e46ed2fc76759567bec586892c49876e5a687` |
| independent-feature-proposal.json | `b2ff33b771893a124f0ed6ce2f77bfb605d6c29c098d761e1c8b192db5612c8a` |
| settings-review.md | `ec4956a7b0f3c41f36da691cd626bd95a7f546caa93fc29694682576a52d111d` |
| verify_join.py | `71724ddfbd397f38dda8e0a45c7defe017993fe91614211c21d5f27dfebe52c0` |
| verification01.json and verification02.json | `bd69d3e98ae6a8aa924208456fe44d02721d67a20a0f35d8fff16ad9a0119a6d` |

`python3 tools/validate_record.py --strict` also ran read-only from main:
exit 0, headers + issue/fact links + citation tags OK. This narrow schema check
does not validate factual/legal claims or authorize case-record promotion.
The worktree's `git diff --check` exited 0; it does not cover untracked files
by itself. An initial unit-specific check separately covered 8 Markdown files,
24 local links, 15 text files for whitespace and 6 JSON parses, with no errors.
The final check after reviewer integration is recorded below.

## Alias and comparison review completion

The metadata reviewer repeated the original two-archive inspection and obtained
the same JSON values. Its second, class-specific XPath route checked 50 scalar
fields, two world lengths and two video basenames, plus one parent, two nested
archive and ten contained-file hash/size checks. Root read the exact saved code
in alias-review.md and reran the following read-only check, exit 0 with those
same counts:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /private/tmp/wtc7-camera2-settings-cFee5g/check_alias_fields.py
```

This is root replay of a different code route from the first extraction, not
an independent XML parser or physical measurement. Exact code is embedded in
alias-review.md so loss of the scratch path does not lose the method. No raw
author-path XML was newly preserved or printed. Root also separately checked
both thumbnail hashes/dimensions and viewed both complete 320 x 228 images;
the metadata reviewer did not view them. No video decode occurred.

| Additional artifact | SHA-256 |
|---|---|
| alias-review.md | `fbad9c023e88c7f19dcfac23bd84e0e12b9fd74efb54dc178787bdff67e9bdb1` |
| alias-receipt.json | `30411f78f3ba5d3af0e870bad399fad2d0d7017f7136018d76717a8b6d78012b` |
| thumbnail-receipt.json | `c8b0ea324c7774d8dd7b05a2afae22490169f8e47f4485079d4da8cbf12c69b9` |
| thumbnail-review.md | `dd2191313327f2ddbaab48b9229dd5ead74cb6252be4c115c0cc39e2ba48cbd3` |

The separate feature reviewer recomputed all eight record comparisons from
both original proposal JSONs without reading or running verify_join.py, and
reported exact agreement with both output row arrays. It recommended three
clarifications: normalized candidate/region agreement rather than identical
descriptive status strings, explicit links to both verification runs, and a
direct prior-results link for the later T2 failures. All three were applied.
Its thumbnail assessment is a prose/inference review only; it viewed no new
thumbnail or native image during that cross-check.

The saved result-review.md hash is
`827a0ee13405588673e609535f95a52a923ae6c0b9dcea89f0f91f5a740c437a`.
It identifies its pending-alias report snapshot explicitly; the later integrated
alias paragraph was root-checked against the actual metadata/thumbnail sources,
not represented as part of that earlier independent review. The three requested
changes are adopted in the final report. The reviewer save initially timed out
in automatic permission review and succeeded on its one permitted retry; no
existence or delivery claim preceded successful creation.

Final unit document check: 9 Markdown files, 28 local links, 16 text files for
trailing whitespace and 6 JSON parses; no errors, exit 0. Final worktree
`git diff --check` also exited 0. Final report SHA-256:
`0b54bb43fac1d96bc0fdb9b1be8879cba52812ad012ad64a56a28612b7deddb2`.
No user-interface test was applicable: this is a source/document unit, not a UI
change. No motion fit, solver, video decode, source-master authentication,
independent human review or consequential-measurement gate was run or passed.

**Bounded unit closed with the recorded freeze deviation**, not an all-controls
pass. The prior goal turn and this unit both made substantive progress; neither
is a wait or repeated no-progress state. Actual source records, candidate
identities, checks and the next clip/project test are preserved. The source-
of-truth/evidence-audit skills prevented promoting archive metadata or numerical
agreement into historical/physical findings. Handoff guidance is consolidated
here and in existing STATUS.md rather than a new competing authority file.

The initial attempted `kit-inventory/README.md` and in-progress
`alias-review.md` reads returned absent paths; located source reports and later
completed deliverables are used instead. Truncated combined text outputs were
not used as complete reviews; relevant sections were reread separately.

## Unresolved and next independent task

The exact Figure 4 source frame, author-selected east-penthouse zero, physical
calibration, original pixel track and material-point continuity are not recovered
by this two-frame join. The bounded alias inspection is completed: actual saved
project fields and thumbnails are now inspected at the stated levels, leaving
clip/project/publication correspondence as a live, concrete source lead rather
than an unexamined archive or established absence.

For subsequent WP2 work, read the main charter, this report/deviation, the older
target-trackability failure rows, and the printed-table method/clock limits.
**Smallest next task:** under a new bounded declaration, preserve the exact
embedded `TiltedCameraWTC7Clip.mp4` bytes from the named TRZ and audit its saved
source/filter/timing/track structure against the held Camera2 MOV and the paper.
Start with container/project provenance, then a fixed-sample scene correspondence
test independent of any desired acceleration/onset result. Require exact member
and source hashes, safe fixed output paths, source-native PTS and transformation
records, explicit unique/ambiguous matches and a separate publication-to-project
link. Do not launch Tracker, infer an author-selected clock or transfer scale
merely from similar thumbnails. Actual software semantics need source review.

Subsequent continuity work should freeze lower
roofline feature definitions, source-frame coverage, geometry and onset criteria
before future measurements; retain failure and region-only rows, and do not
choose scale/time to make acceleration equal gravity. Acceptance requires
explicit point identity or unresolved status, pinned source/PTS, a saved
pre-comparison freeze for each reviewer and separate computational-versus-human
review states. Full-reasoning scientific/image review is appropriate; bounded
mechanical hash/link checks can be separately delegated. No new expert outreach,
private-packet access or consequential measurement gate is cleared here.
