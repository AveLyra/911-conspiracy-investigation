# Calibration verification record

2026-09-15. Local research only. This verifies preserved inputs, finite
bookkeeping and stated review scope, not image-perception accuracy.

## Executed checks

- Root and the bookkeeping author each ran `test_summarize.py`: **31 tests
  passed**, including the ten protocol scenarios as subtests. Tests include
  threshold touching, category-neutral membership, unknown/excluded precedence,
  zero in-frame extent, native span boundaries, semantic conflict, invalid
  enums/intervals/booleans/non-finite values, duplicate/missing IDs, changed
  source hashes, metadata representation, reproduction and overwrite refusal.
- Each annotator answered all ten disclosed text scenarios before saving
  historical labels. These are rule-comprehension checks. Root had previously
  seen imagery/old labels; the fresh reviewer answered before opening geometry
  or viewing images. Both control files remain frozen.
- Root produced `summary01.json` and `summary02.json` in two successful fresh
  executions. `cmp summary01.json summary02.json` returned zero.
- The independent checker passed **16 synthetic checks**, then rederived all
  **78 rows** (2 reviewers × 13 units × 3 thresholds) and **12 groups**
  (2 reviewers × 2 images × 3 thresholds) for both summaries. It checks frozen
  source pins, raw-document equality, memberships, preliminary/final states,
  conflicts, spans and all six field-difference lists. It does not import the
  producer or independently decode images. Generated reason text is not a
  separately validated scientific inference; original reasons are preserved.
- Root read the complete checker, reran its 16 controls and the full summary01
  check. `independent-root01.json` is byte-identical to the agent's receipt01.
  Receipt02 differs because its verified summary input path is summary02;
  both summary bytes are identical. No arithmetic disagreement occurred.
- Independent visual cross-review confirmed the one identity, five opportunity,
  five appearance differences and equal-total/different-location example.
  It required qualifying “purely semantic” to category-priority disagreement
  and reserving substantive evaluability uncertainty for the other regions.
  Those wording corrections were applied without changing labels.
- Main strict record validation passed its headers, issue/fact links and
  citation-tag scope. Worktree `git diff --check` passed; neither validates
  physical claims. Main was clean when checked. No source/record files edited.

Runtime for root tests and summaries: bundled Python **3.12.14**, Pillow
**12.3.0**. No packages installed. No browser/UI change or browser testing
applies to this offline unit. No new video decoding, image resampling,
temperature inference, solver execution or external transmission occurred.

## Reproduction commands

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/fire-visibility-calibration/`.
Use fresh output names; do not overwrite the preserved runs.

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_summarize.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B summarize.py --labels main.json reviewer.json --out summary-new.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py --selftest
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py --summary summary-new.json --out independent-new.json
cmp summary01.json summary-new.json
```

The source paths are read-only dependencies in the main repository. Writes to
this separate worktree require the environment's scoped permission review.
The independent agent's initial receipt write was denied after comparisons;
the same operation succeeded with scoped escalation. No scientific output was
discarded or input changed to make the check pass. Its deliberate repeat to an
occupied receipt path was correctly rejected.

Before first historical production, root noticed that the fresh reviewer's
independence metadata was a structured object while the producer expected a
string. The protocol requires identifying metadata but specifies no such type
restriction. Producer validation was expanded and synthetically tested to
preserve a nonempty string or object, with non-finite values rejected. Both
frozen label files and all scientific rules remained unchanged.

## Frozen pins

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5` |
| main.json | `a770538e31081ab46e40dc9c26e78bf660128bc419c1491d3357839190f9c3ba` |
| reviewer.json | `ea8547d0eed74751074637dcb4f3b8d9c7108723b4f3230ff98e787eefa3dc2b` |
| summarize.py | `bfdf1c875c24d104a9aec2b76306c4445060778676ad43c0c4e60c6bc302b9f8` |
| test_summarize.py | `4ef40ad0c2c32ed40016ffb9cecc3db2c03e49effae21ed7507b0c58eae07d4a` |
| summary01.json and summary02.json | `87d762e2d25709f30397b312502d2c60b6d2bb47ff9b61656bfc637dc06ea9fd` |
| independent_check.py | `0a7849db4a943bf3d5240485f26a97b33b0bc2679dfc45e94321c3dd04a85cfd` |
| independent-receipt01.json and independent-root01.json | `b4a6a3c0838f688d6cc979f01f50899cbdd4fe60390dacbf269e67605e225aba` |
| independent-receipt02.json | `82254ea6ad3fe307fed2959f2be79494c557587a243c0758ff0146d63c938738` |

The protocol pins geometry and both JPEGs; the [method audit](method-audit.md)
pins untouched v1 records. Reviewer controls/note pins are in
[reviewer-note.md](reviewer-note.md). The producer checks actual JPEG dimensions
and verification, and rehashes inputs before returning the report. The fresh
annotator separately checked native dimensions; a hash is integrity of the
captured derivative, not historical authenticity.

The producer's geometry validation is in-bounds/interval validation on an
exactly pinned geometry file, not a general polygon-topology certification.
The independent checker is a frozen-input arithmetic oracle, not a complete
adversarial validator for arbitrary new files. Neither program measures real
optical opportunity, opacity, flame area, or observer accuracy.

Final root document/integrity pass: all 3 Python files parse as AST, all 9 JSON
files parse, and all 15 local links in the 6 Markdown files resolve. Both sets
of 10 text-control answers match the frozen scenario contract. All 4 pinned
old v1 files remain unchanged. Summary and root-receipt byte comparisons pass
again. These are integrity/navigation checks, not added scientific validation.
