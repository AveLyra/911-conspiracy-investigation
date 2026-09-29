# Verification and durable handoff

2026-09-19. This unit completes declared printed-table arithmetic and the separately declared clock diagnostic. It does not complete WP2 or the investigation. [Report](report.md) states the evidence ceiling; [protocol](PROTOCOL.md) and [clock addendum](CLOCK-ADDENDUM.md) preserve analysis choices and their timing.

## Inputs, implementation and independent review

- Source PDF SHA-256 `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`; [prior acquisition record](../luna-reevaluation-2026-09-19/verification.md). Root viewed complete pages 15,43–50; pages 43–47/50 were existing derivatives,15/48/49 were complete derivatives from the method reviewer's new render. Root did not newly view every page of the paper. Separate method reviewer covered10–16 and 37–50; separate transcription reviewer checked all selected cells at full-page and section scale.
- Root and independent transcriptions were frozen before comparison. [Root freeze](transcription-root/source-review.md), [independent source review](transcription-independent/source-review.md), [reconciliation](reconciliation.json) SHA-256 `2aba8ca61b1ef8461654cfcab4b4cd86847660259576a9038aa6015e4ccc0fe6`:791 numerical tokens/229 nulls, no differences. Shared source and extraction-library dependencies remain; this is not independent camera evidence.
- Main protocol pre-result SHA-256 `85c1570d523fa8514e9596ecc36e85bc1299586f0a70b0211c38f3725eb59aac`. Root `calculate.py` SHA-256 `d7bdeee43b7524f5b97edbff23e9636f5f74d2ed91aba31cc186b64a3b1863f2`; tests `4c6f92dd1b0dc106481ceeaf3b7d2ce80981e7616e13a3062280d5a9088be911`. Python 3.12.14, NumPy 2.3.5. [Root receipt](run01/receipt.json).
- Independent rational implementation was separately frozen before seeing root's output: [freeze](oracle/implementation-freeze.md), [review](independent-numeric-review.md). It used Python 3.14.0 and `Fraction`, no NumPy fit. These are independently written arithmetic methods, not independent engineering experts or source observations.
- Final source/inference reviewer requested three precision corrections, applied: signed western difference−0.28; no assumption that the unknown author fit mask differs; clock row-wise compatibility rather than identification of a historical explanation. Its gravity-scale wording suggestion was also made explicit. No original numeric output was changed.

## Actual executed checks

Root commands used the bundled Python at `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, with `-B`, from this unit unless indicated:

```text
python3 -B extract_tables.py --source ../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf --output transcription-root
python3 -B reconcile.py
python3 -B -m unittest -v test_calculate.py
python3 -B calculate.py --output run01
python3 -B calculate.py --output run02
cmp run01/results.json run02/results.json
cmp run01/receipt.json run02/receipt.json
python3 -B -c 'import check_clock; print(check_clock.synthetic_tests())'
python3 -B check_clock.py --output clock-results01.json
python3 -B check_clock.py --output clock-results02.json
cmp clock-results01.json clock-results02.json
```

Results:10 root synthetic tests passed before historical fits;98 fits per run; both result and receipt files byte-identical. Root result SHA-256 `c78146f9bb596a5c0c8241ae918d43f700c35596131e62af53912f75fd5a5dfd`. Independent implementation:15 synthetic tests, two byte-identical historical runs, seven corruption-detection controls. [Comparison](oracle/comparison01.json) checks1,959 exact and 5,088 numeric items; all 98 fit identities/memberships and relevant numeric quantities pass the unchanged1e-8 tolerance. Max acceleration difference4.4054e-13. It also checks all 161 supported nominal derivatives,75 western subtractions, both offset sequences/intersections and 75 pairwise displacement differences. Unsupported NW endpoint remains explicit.

Clock addendum SHA-256 `198d31a14ca49368bfc00c64ed3d4827d8fea9d7045a4f2a090e75a5ec6a866f`; root clock code `975cd047518602771c713d6484f707bc93f1c070fdbd72e0c77c8c7b44bb248d`. Nine root synthetic cases passed before the post-result historical diagnostic. Root clock files byte-identical, SHA-256 `a625dde21e5767adc60147421afb94084d96842fc9ec7e733706555e80297c87`. Independent clock implementation: six synthetic tests, two byte-identical runs and six comparator-corruption controls. [Clock comparison](oracle/clock-comparison01.json) checks3,719 exact items covering all 483 row-candidates and verifies the nominal case still matches the original baseline. Original98-fit output/code hashes were reconfirmed unchanged.

The independent review records the oracle commands and all hashes. Root's validation claim distinguishes delegated execution from its own commands; root did not claim to have rerun every oracle test personally. All post-result variants remain explicitly labeled, not substituted for the original test.

## Camera2 source join and fresh probe

Root read the selected `VID-WTC7-001` row from main's `research/wtc7-video-comparison/media/video-acquisition-manifest.csv` (SHA-256 `5f39f34f6ba978ff8e030c632ab49c54950faaaf2fb3654ccd5cdc14bdfee6dc`). Public file ID `1RGWHdqt_PO_Z-KlWhXza0QBq909BEGmC` matches the paper's page 50 Camera2 URL exactly. The held208,810,910-byte file is `research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov`. Fresh `shasum -a 256` gives `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`, matching the existing acquisition.

Fresh read-only command with `/opt/homebrew/bin/ffprobe` version 7.1.1:

```text
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate,avg_frame_rate,time_base -of json INPUT
```

Result:`30000/1001`, `2997/100`, `1/2997`, respectively, matching the saved stream metadata hash `d54e30ca5e8bece9ba61769e3916741caa14ea3f4b4c0b6dc7757685ec50daa1`. No complete video/audio decoding, tracking or original exposure-clock authentication occurred. The prior [timing audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/timing-audit/README.md) supplies the nonuniform PTS finding; it was reread, not rerun. Acquisition-ID agreement is not proof of current remote byte identity or a table-to-specific-frame mapping.

## Failed attempts and remaining limits

- Final root checks after source/inference corrections and spacing-only narrative formatting: all 10 synthetic tests pass again; exact transcription reconciliation, both result/receipt pairs and both clock results remain unchanged; all 9 clock synthetic cases pass. Frozen source/protocol/code/result pins still match. Report SHA-256 `cfb890026ca160e08509ee4fff69562a6c90f68fc8a6ff0fbfd6c7819ad6f49c`.
- A read-only check of all 11 unit Markdown files found 48 existing local link targets, no trailing whitespace and final newlines throughout. Scoped `git diff --check` on research status/navigation/feedback passed. Main `python3 tools/validate_record.py --strict` returned **OK (headers + issue↔fact links + citation tags)**. The latter checks record structure, not scientific or legal validity. No browser/UI change required testing.
- Initial `pdftotext` path did not exist; used installed `pypdf` extraction instead. No dependency installed or source declared inaccessible.
- Some oversized text/file-search outputs were truncated; selected relevant content was reread. Broad `camera2` searches in per-image JSON were too noisy and were replaced by selected stream-field queries.
- Independent worktree directory/output creation initially hit sandbox permission limits. The transcription reviewer staged its frozen files under `/private/tmp` and installed them after the parent existed; the oracle preserved [its failed run](oracle/failed-run01-sandbox.md), then reran unchanged with scoped permission. Root output creation used scoped worktree permission. No main write was used as a workaround.
- Renderers emitted Fontconfig warnings; the separately recorded complete-page images were legible. No clean-render claim or PDF re-export.
- The nominal derivative hypothesis has11 preserved failures. Two fixed source-motivated clock variants give per-row compatibility only; no global hidden-digit/clock fit was performed. No exact author mask, metric calibration, onset confidence interval or source-video reconstruction is claimed.

## State and next action

Worktree: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch `research/sherlock-wtc7-investigation`, existing HEAD `e8d83d7`. New unit is uncommitted; preserve unrelated dirty work. Update only research status/navigation and a deduplicated local Sherlock note. No source, main, legal record, Faraday state or accepted Sherlock finding changed; no commit/push or outbound message.

Next independent unit: join the paper's Figure4 features/scale/time zero and any saved settings to the already-held Camera2 frames; then independent PTS-pinned annotation and onset/trajectory tests. Read this report, the method review, the current Camera2 target-trackability/reference-repair reports and the source manifest first. Acceptance for the join: an exact held-file/feature/frame locator or explicit unresolved identity for each of the four points; a source-supported or explicitly unverified metric/time origin; no interpolation across known recording defects; and a frozen independent-placement/onset protocol before new historical fitting. Use a full-reasoning driver for the scientific choices and an independent source/annotation reviewer; do not substitute an unreviewed low-cost summary. This does not authorize new tools, costs or sensitive transfers. The separate late-fire-video lineage lane remains active work to finish. Do not treat successful printed-data reproduction as satisfaction of independent measurement requirements. The full goal remains active and incomplete.
