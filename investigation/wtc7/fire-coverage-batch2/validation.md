# Batch-2 validation and preservation record

2026-09-16. Local research. Checks establish declared coverage, byte integrity
and descriptive comparison reproducibility, not physical interpretation.

## Actual execution and review

- Both annotators saved six disclosed text-scenario answers before this batch,
  then viewed all 13 complete native JPEGs. These controls test rules, not
  optical detection. Records froze before root opened new source attributions
  or the other review. Old annotation versions remain unchanged.
- The producer author passed **27 synthetic tests** before reading historical
  labels. Root ran all 27 successfully before its historical summaries. Tests
  cover separate axes, raw-record retention, malformed schema/coordinates,
  source pins, changed inputs, exclusive creation and repeat production. See
  [synthetic-test-receipt.md](synthetic-test-receipt.md) for coverage and limits.
- The inventory author freshly rehashed the report, all 28 JPEGs and both
  stream forms, and all 23 page PNG/text/fragment sets. Exact counts,
  protocol/key/prior-review hashes and declared 13-ID subtraction passed.
  Root read the full `inventory.py` and replayed `--check`; the entire rebuilt
  inventory matched `inventory01.json`. This does not rerun the old independent
  extraction parser or authenticate historical camera files.
- Root ran the producer twice to fresh comparison01/02 files. Both are
  **177,385 bytes** and byte-identical under `cmp`. Source and record pins
  remained unchanged across calculation.
- A separate checker froze its own validator/comparator before reading new
  labels or producer output, without reading/importing/running the producer
  algorithm. **35 synthetic controls** passed. It then computed and froze its
  own historical result before inspecting the producer JSON layout. The first
  control receipt embeds the complete initial implementation.
- Only then did the checker add a product-schema adapter and **eight adapter
  controls**. All 43 passed. Product verification confirms unchanged ASTs for
  all 14 original non-main functions, then compares both outputs against its
  independent result: **65 axes, 65 unforced region pairs, 39 description pairs,
  both complete raw documents and the complete source-hash block per output**.
  No material discrepancy was found. Scope prose/schema-version metadata are
  not independently certified by those equality checks.
- Root read the complete checker, ran all 43 controls, recomputed its raw
  result and verified both products to three fresh receipts. Product/control
  receipts equal the agent's final receipts except `argv` (different output
  names). Root's raw result equals the initial result except `argv`, the
  current checker hash and 43-versus-35 control-count metadata. All descriptive
  fields match exactly; these receipts are not called byte-identical.
- Root viewed all ten new complete source pages after observation freeze,
  plus four supplemental text pages. The source reviewer viewed all 23
  preserved page PNGs and documented other text-only coverage. Their scopes
  are separate from the native-image observation pass.
- The visual cross-review requested four wording corrections: unmeasured
  severity, provisional glare, unequal region scope and complete localization
  disagreement. The source review corrected estimated interval versus exact
  time for 5-116, photograph terminology for 5-126, and prior/current observer
  coverage. Root applied all seven; both reviewers verified their localized
  corrections. See [cross-review.md](cross-review.md) and
  [source-review.md](source-review.md), which preserve earlier critiques.

Main `tools/validate_record.py --strict` passed its headers, issue/fact links
and citation-tag scope. That is not scientific or legal merits review.
No packages were installed. The producer runtime was Python 3.12.14/Pillow
12.3.0. These offline scripts require no browser/UI testing.

## Limits and preserved failures

Reason strings receive nonblank/schema checks, not semantic certification.
The producer does not automatically certify every relation between target
evaluability, nondetection and luminous-feature depth. Actual visual/source
review remains necessary; no raw record was repaired into agreement.

The independent checker is a frozen-input audit, not a general hostile-input
validator or proof of schema equivalence. It accepts a string for alternatives
although the actual records/producer use lists; `math.isfinite` may raise
`OverflowError` on an enormous integer. Neither occurs in these pinned inputs.
The initial code remains preserved. Its synthetic mutation check compares
digests, not a concurrent attack; actual sources were hashed before/after.

Some inventory family strings retain full credits while others use shorter
keys. Do not derive independent-source counts from unique strings. Explicit
origin links and credit equivalences are retained in the source review.

The inventory author's first exclusive creation was denied by the worktree
permission boundary after checks; no output was created. The same scoped
operation succeeded with escalation and replayed successfully. Root's
`pdftotext` attempt failed because the executable was unavailable; read-only
`pypdf` extraction then succeeded on physical pages 238/254/264/284. Reads
attempted before two agent notes existed returned missing-file errors; both
completed notes were subsequently read. A documentation patch failed its
STATUS context match without changing files and was reapplied with exact
context. No scientific failure/input was erased or altered.

These checks do not measure optical opportunity, aperture identity, smoke
opacity, temperatures, clocks or causes. No model was executed, no new image
render/enhancement or network acquisition occurred, and no material was
transmitted or promoted to canonical fact, legal position, accepted Sherlock
finding or Faraday certification. Prior/main/source files remain protected.

## Reproduction and pins

From this directory, use fresh output names:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_summarize.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B inventory.py --check
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B summarize.py --labels main.json reviewer.json --out comparison-new.json
cmp comparison01.json comparison-new.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py controls --output independent-controls-new.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py run --output independent-raw-new.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B independent_check.py products --output independent-products-new.json
```

Product mode verifies pinned comparison01/02, not a new command-line comparison
filename. `cmp` separately verifies the fresh producer output. Never overwrite
frozen products to obtain a passing replay. Source paths deliberately resolve
to the main repository; writes stay in the isolated investigation checkout.

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | `8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff` |
| main.json | `63100450901d2358ee14f253a95b154f038091a88e0d3cf1c81e56126a0c2c2b` |
| reviewer.json | `2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7` |
| inventory01.json | `8d16768c37ccf00a81c9fb1441427360d00d2cc679b8c9e38fefc1e7caacbda9` |
| comparison01.json / comparison02.json | `f6934003b585a3d2f43e5ae5c7965b9a5b687247c0c5fa590117e7ddcf8e3cfb` |
| independent_check.py with adapter | `cb8725cc75cf2f99ef5900c5541ff01ce334f61ba7b152a3c21a89c0e60c8b44` |
| independent-root-controls01.json | `2fc7ff39b5b4c51a784f1ef30e465c116d846224cbbf89f2d29afc0d5927a6ab` |
| independent-root-raw01.json | `e321e98ffdd2ea12e9f7674310b9813397551f88999510eef2f302ec063cbf8e` |
| independent-root-products01.json | `789d0a4e57a17c999764c50670cbf6a1d887d710688fc3f8e290add81f554dc4` |

The [independent review](independent-check-review.md) pins both checker versions
and its controls/results. Producer/code pins are in the synthetic receipt;
source PDF/key/prior-review and all object/page pins are in inventory/source
review. Root/reviewer control answers remain separate and are not evidence of
historical fire conditions.

Final root integration pass: all **4 Python files** parsed as AST; all **15
JSON files** parsed with duplicate-key/nonfinite-constant rejection; all **8
Markdown files** and **22 local links** passed the scoped text/target checks.
Nine frozen code/source/report pins matched, including the final report hash
verified in both correction dispositions. New navigation links resolve.
Worktree `git diff --check` passed; main `git status --short` was empty.
These checks include this unit's untracked files rather than relying only on
the tracked diff. No unrelated WIP was reset, staged or committed.
