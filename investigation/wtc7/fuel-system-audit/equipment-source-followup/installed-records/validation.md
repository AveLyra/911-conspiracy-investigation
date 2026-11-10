> **Historical research:** This document reports a prior source review, not a current instruction or new model run. Missing sources and run artifacts are identified; see the [publication note](../../README.md).

# Installed-record follow-up: methods and verification

2026-09-11. This is a research-source and inference-boundary audit, not an equipment test, solver reproduction, legal finding or full-goal completion.

## Scope and actual reading

The [protocol](PROTOCOL.md) declared six exact-record queries and at most twelve primary-source openings. All six queries were used; two primary PDFs were opened and acquired. No original installed-generator/cooling or control drawing was found in the returned results. No broader absence claim follows. [The source log](source-log.md) retains query wording, rejected result categories, successful downloads and failures.

Root read all text and complete rendered images of testimony physical pages 1–12 and briefing physical pages 1, 15–16, 49–51, including full tables, diagrams, footnotes and continuation text. The testimony selection covers its introductory material and appended NCSTAR 1-1 printed pages 175–181. The next intentionally blank printed page and later code appendix were not part of root's visual selection; the original wording anticipating the entire chapter is narrowed to this actual coverage. The briefing selection is six of 106 pages, not a complete briefing review.

Full-page display was resized by the viewing surface, with no crop; source-resolution PNGs remain preserved. Page labels were checked visually: web PDF references use zero-based page indexes, while this report uses one-based physical pages. In particular the named interview footnote is on testimony physical page 11, printed page 180—not physical page 10.

## Reproducible derivative method

The helper (historical local reference `render_selected.py`; not included here) verifies both source hashes and page counts, requires the existing font configuration, and refuses to overwrite a run directory. It preserves selected full-page PNGs, text extracts, per-process local-only stdout/stderr and command/source/runtime receipts. It does not execute PDF attachments, invoke either investigation engine or author a new PDF.

Commands actually completed with exit 0, using the bundled Python executable:

```text
python3 render_selected.py run01
python3 render_selected.py run02
```

The first preflight attempt failed before creating a run directory because the helper initially resolved the font directory one level too high. That index was corrected before successful rendering; it is preserved in the source log rather than reported as a source failure. The bundled renderer uses `-scale-to 2200`, with explicit existing `FONTCONFIG_FILE` and `FONTCONFIG_PATH`; commands and environment/version identifiers are in each receipt.

Verification (historical local reference `verification.json`; not included here) independently compares both runs: all 18 PNGs and 18 text extracts match byte-for-byte, with zero stdout/stderr and exit 0 for all accepted render calls. Portrait pages are 1,700 × 2,200; landscape slides are 2,200 × 1,651. Both source PDFs still match their acquired-byte hashes. Reinvoking `run01` was deliberately tested: it refused with `FileExistsError`, and all existing PNG/text/receipt hashes remained unchanged. The expected refusal is not a successful new render.

The comparison program rehashed every PNG/text in both runs, checked page keys/dimensions and runtime/procedure pins, and rehashed both sources. It did not simply accept the receipt's own success labels. Same-environment image equality verifies the extraction/rendering transformation, not historical authenticity, engineering correctness or a second independent source.

## Review and authority limits

The [independent relevance review](relevance-review/report.md) reads the detailed later-report diesel cases and narrows the generator-shutdown issue to its applicable scenarios and downstream input choices. Its initial page-selection deviation is explicit; supplemental Chapter 13 summaries are not claimed as Chapter 11 source coverage. The root report incorporates the recommendation to preserve case-specific alternative rejection grounds rather than describe shutdown as a universal diesel exclusion.

The [completed testimony/briefing crosscheck](relevance-review/crosscheck-report.md) independently read eight complete pages and checked their 16 PNG/text hashes against the root receipt. It supports the covered soil, interview, fan/rating and briefing interpretations; it explicitly leaves the OEM pump row and search/title context outside its review. Root corrected its sole copy-edit recommendation from “Two” to “Three” configuration rows. The reviewed report hash therefore remains the pre-copy-edit snapshot, not a certificate silently updated to later text.

The initial relevance reviewer independently reproduced 11 existing N9 page images in memory with Poppler after a different renderer produced unequal pixels. Its [coverage record](relevance-review/coverage.md) preserves both methods and the Chapter 13 selection deviation. Root read that report and the additive crosscheck; no fresh root reproduction of those 11 N9 images is claimed here. A source-reading critic is a computational agent, not a licensed engineer, independent historical witness or substitute for original records. Earlier parent reports and source/derivative attestations are preserved. This task performs no thermal, hydraulic, electrical or structural simulation and makes no ranking change.

Final integration checks passed for 13 Markdown documents and 103 local targets, with no missing targets, trailing whitespace or conflict markers. Root freshly rechecked 27 reviewer-cited image/text hashes and the preserved initial relevance-report hash. `final-integrity.json` records these results. Scoped tracked `git diff --check` and `python3 tools/validate_record.py --strict` passed; these do not validate physics or clear unrelated working-tree changes. This outcome paragraph introduces no new link targets. Both root rendering sessions and the bounded review assignment are terminal.

No denied-route bypass, private records, new correspondence, sensitive transfer, bridge execution, canonical facts, filing, commit or push is included. Raw acquisition headers and process logs remain local-only and are not cleared for export or feedback. Scoped link/record checks cannot establish scientific validity or privacy clearance. The investigation stays active; STATUS names the next acoustic-source task instead of repeating this exhausted lookup.
