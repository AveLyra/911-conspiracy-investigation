# Stage A verification record

September 20, 2026 UTC. These are scoped provenance/record checks, not
independent historical-clock or physical-model validation.

## Executed checks

Root's fresh read-only standard-library check returned exit 0 and PASS for:

- Six pinned inputs: three primary PDFs, Camera 2 MOV, full frames.json and
  the earlier refine01 receipt. All source pins remained unchanged.
- Original root/observer freezes and completed observer-followup hashes.
- All four initial warned PNGs equal their clean-rendered counterparts byte
  for byte. Both warned and clean copies remain preserved; this equality does
  not make a warning-free process out of the initial run.
- Sixteen unique clean page renders exist (13 in source-pages-verified, three
  in observer-geometry-pages); hashes are recorded below.
- Three selected held media PNG sizes/hashes and their indexed PTS rows:
  indices 6593/6624/6924, PTS 659301/662402/692402. No new decode is claimed.
- Then-current unit Markdown trailing-whitespace and conflict-marker scan.

Root viewed all 16 unique complete pages; the observer viewed 12. Root viewed
three unique held media frames; the observer one. Reopening the baseline for
context does not add an independent sample. Text-locator coverage is distinct
from visual reading. The subsequent critical review's actual viewing belongs
to its own record, not these counts.

Initial render calls returned 0 with a Fontconfig configuration diagnostic;
clean rerenders returned 0 without output after the local fonts.conf was set.
The initial diagnostic is preserved in the tool transcript and written stage
records, not a saved raw stderr file. Source PNGs remain unchanged. The clean
4-page rerender was executed, not merely inferred from byte equality. Later
selected renders and locators also terminated successfully; no process remains
pending from Stage A. No glyph/layout issue was apparent on full-page viewing.

## Frozen record pins

| Record | SHA-256 |
| --- | --- |
| root-definitions.md | bc5909b8b62ce8761f66022c4798d356f09202a73f63831293a18f72d65c10b7 |
| observer-definitions.md | a72438dac7b124babf336b9c460760e8006d33d4cea24fc50530ed36138d9969 |
| observer-followup.md | 293328f537b8c8d1a57dfbca1ca1a8b609a7bfa33585ae2ae5967f4abf28a2e6 |
| root-followup.md | 66e862fa0b0688533f4eb9aef1bde8c1c376bcf4a88ff8e45d0cf7110f87d0fa |
| PROTOCOL.md | 448ff4d2d62561df8d29bea85c21bfb307103578d77b10eb44865d977f2b4a30 |
| REFERENCE-SCOPE-02.md | df5d99120981dd2cdb9a77c1991f761fc918202f55be757106df95256b0b2c6e |
| MEDIA-SCOPE-02.md | 531a2338a528ef82a4be931080e6f9f114b468a778cd50612bae573c90ac50b7 |
| fonts.conf | 4d5f52e474d0b79398751b839703f34a45fffd91076ed81543a6ab57d2f0f85d |

The original Stage A report was hashed before review as
`15c3adc21979c484a76c62c3b03003ca26ca7d559cc137daa0b14dd2d7a97104`.
Subsequent review clarified a last-visible/first-below-parapet bracket rather
than assigning an exact disappearance time to the last visible frame. The
original observational freezes were not changed. A new prospective STAGE-B.md
declaration is distinct from the Stage A protocol; its existence is not proof
of extraction or measurement.

## Clean complete-page derivative pins

Paths below are under source-pages-verified except the last three, under
observer-geometry-pages. These pin derived images, not original photo custody.

| PNG | SHA-256 |
| --- | --- |
| ncstar1-9-306.png | ec72fddf038142c605799cabcface75478fa7690069659ec759e82c196a4bb11 |
| ncstar1-9-307.png | ef6213ce9da86b21642fdc5bd91cc079023913466264f56193fa86a1ca086ad0 |
| ncstar1-9-308.png | 9cc51f2c899c678f289cc4edf269a591a0d82a9218b6771dad8cba843f1c6a54 |
| ncstar1-9-319.png | 36de16f3b8e41259a9d1deee5ebe356cf2e7fdd8ebc12719fd96ef658008530f |
| ncstar1-9-320.png | fb6518785bcd110fdd58d54dae461ef98b03bb02dda4df95d260b406367f5db1 |
| ncstar1-9-321.png | f5db37f5abacd1071c4b05e96b5f5c9e3a75c21fd0b8d328a0424a5bdb56677c |
| ncstar1-9-323.png | a78e37732f279dac99a2f8f6f5a387cd721f64a1a9ce2fec58e8fca6129bc218 |
| ncstar1-9-325.png | 2316d0c49a5d91988ea212a059ec81fbe3933b4d693faf594391b225130877df |
| ncstar1-9-326.png | 106250ffe8a32d58b2658adf1963f813772862be0840f6fded38c080a8c9a993 |
| ncstar1-9a-147.png | aa27688a12c3a4d81bf3b5d91812d12a7c6e8ed247b541ac0c8b5c7b7f29439e |
| ncstar1-9a-148.png | 76a76f60aabe388ad2e6f15ff17b88d04b2c11bb28f0a7f4d5a4506aa22ec7f8 |
| ncstar1a-085.png | d2b8cb5a7f3e5129e601bc872f028eb5d142d864677d8e86bab5a4926d6ba3d6 |
| ncstar1a-086.png | 4903d1f0f9bad3d98f14cd00767c796692c8349532450ac2f57f1ab7591c9965 |
| ncstar1-9-134.png | 6e8a6d7ed1ee069cd5b2408a59b693c17c397f27d2b94f7a3bf2b569ba216a49 |
| ncstar1-9-135.png | 864eb3b0737bdf6d980e52b99430c40eb6949143e52a0613d7bff04467757139 |
| ncstar1-9-143.png | 85f737a2311eb171b2077acb714d2f9df8fa6265f36770ce2b6296ed5cec76f4 |

No Stage B tests, extraction, endpoint annotation or interval result is
claimed in this Stage A verification record. Later execution must retain its
own actual command outcomes and reproducibility checks.

## Independent review and repository checks

The completed independent-review.md is 9,447 bytes with recorded SHA-256
`059361d82dd74b465225813cc570297fd066ae8f12dc393d70dc7c5dea839780`.
Root read it in full. Its eight-page primary check found no remaining material
Stage A inconsistency after the event-bracket clarification. It explicitly did
not inspect video frames or verify new extraction/counts. Its prospective
Stage B method review is not implementation or execution approval. Report
navigation was subsequently updated to name the now-declared stage, without
changing source observations or claiming new results.

After the navigation/feedback update, root executed:

- `python3 /Users/admin/docs/911/tools/validate_record.py --strict` in main:
  exit 0, `OK (headers + issue↔fact links + citation tags)`.
- `git diff --check` in the investigation worktree: exit 0, no output.

These checks concern record structure and tracked whitespace, not scientific
validity or the contents of every unrelated working-tree change. Untracked
unit files receive their own scoped checks; tests for the later extractor must
remain separately reported. Nothing was committed, pushed, sent or promoted.

## Final integration checkpoint

Stage B's subsequent extraction/verification is fully recorded in
[stage-b-execution.md](stage-b-execution.md), not retrospectively attributed to
Stage A. Root's final scoped check passed 20 Markdown files across this unit and
the copy-locator unit, 17 local link targets, four Python parses and whitespace/
conflict checks. It rechecked all 971 listed fingerprints in the root driver-
control receipt and all 46 in the root checker-control receipt, respecting their
separate symlink-fixture contracts. These are artifact instances, not independent
scientific tests or evidence samples. Both initial observation-freeze hashes
remain unchanged.

After the report/navigation changes, `validate_record.py --strict` again
returned 0/OK, and worktree `git diff --check` returned 0 with no output.
The report at this checkpoint is SHA-256
`002ccddcfcdf59cb8ef2aee0c25a3f895366ce163bf64a239904487fd3a4485d`;
the Stage B execution note is
`205d6f0fd04c313ed0f775cc0f7e1c3b552ddd8bb345c55d7e96cc34d3639b23`.
No Stage B visual endpoint work is claimed. All tool processes and subordinate
review tasks completed; the active goal and stated scientific next task remain
incomplete. No legal/raw-source/accepted-engine state or publication changed.
