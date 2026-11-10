> **Preservation note:** This is a public derivative of a dated working research document. Source-access and verification statements below are historical reports; they were not independently rerun for this package. No source media, full-text papers, images or rendered pages are included. Missing linked items are identified in the text; local filesystem paths, if any, are withheld. The companion [provenance record](PROVENANCE.json) records the changes and original hashes.

# Comparator validation and boundaries

Checks completed 2026-09-09; research-only. The receipt (supporting item not included in this public package) preserves the checked source hashes/page counts and Windsor derivative hashes. This verifies attribution/integrity to the stated extent, not historical authenticity, structural causation or expert competence.

## Actual checks

- Root rehashed all **nine admitted source PDFs** against the acquisition baselines: four survival reports, two Plasco manuscripts, two Windsor documents and one HBI capability statement. All matched. Each opened with pypdf and returned a page count. The held, uninspected HBI PDF was excluded entirely.
- Root rerendered both Windsor PDFs into the fresh directory `[local filesystem path withheld]` using the same bundled Poppler, 100 dpi and explicit local font environment. All **53 pages (40+13)** matched the initial PNGs byte-for-byte. Both rendering processes exited zero without emitted diagnostics. This is a same-renderer reproducibility check, not an independent image-decoding implementation.
- An initial aggregate assertion expected54 pages and failed after every individual page pair matched. Independent PDF page counts and file enumeration established53. The incorrect count in the Windsor prose was corrected; the failed expectation is preserved in its acquisition log and receipt. No page pin or source conclusion changed.
- Root visually inspected27 complete INTEMAC pages, six complete Fletcher pages, the two decisive DERT pages, four survival-source pages and three Plasco pages. The case agents' broader reading and the separate review's distinct scope are recorded in their logs. No collective coverage is described as each reviewer independently reading every page.
- The [independent source review](independent-review.md) requested one clarification: explicit missing loading/prior-state/media fields in the central matrix. The final matrix addresses it. No further substantive draft correction was requested. The reviewer authored HBI, so it receives no independent-review credit from that reviewer; root separately read its two decisive primary PDF pages. Capital One's prior primary audit is carried forward, not newly performed.

No fire/thermal/structural model, laboratory result, original-camera timing, footage acceleration, acoustic signature, building footprint or causal probability was reproduced by these checks. The new papers' proposed future stages and unacquired versions remain unverified.

Final local checks: all 62 hash rows in the receipt reverified; 43 relative file links across 13 comparator Markdown files resolved; a separate 729-line scan found no trailing whitespace in those new Markdown files. `tools/validate_record.py --strict` passed its headers, issue/fact linkage and citation-tag checks. Scoped `git diff --check` passed, but the comparator directory is untracked, so this Git check alone does not inspect its new-file contents. These checks do not test scientific truth.

## Recheck the preserved receipt

This read-only standard-library check can be run from the repository root. It checks the saved bytes, not the correctness of the provenance assertions:

```python
from pathlib import Path
import hashlib, json
base = Path('research/sherlock-wtc7-investigation/comparator-expansion')
r = json.loads((base / 'validation-receipt.json').read_text())
for row in r['sources'] + r['windsor_page_pairs']:
    p = base / row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256'], row['path']
```

Windsor's acquisition log provides the exact rendering command shape and runtime paths. Reproduce into a fresh directory, then compare all source-named PNGs; do not overwrite the preserved originals. Temporary directories are convenience locations, not permanent evidence backups.

## Record and privacy boundary

All additions remain in the research layer. No source/exhibit/fact/timeline spine, filing, witness message or public publication was created. Source versions, failed access and the excluded held download remain explicit. The current dirty worktree contains unrelated changes that were not altered by this batch. No commit or push was performed.

The minimized Sherlock supplement encountered an archived destination and was not delivered. SHERLOCK-FEEDBACK.md (supporting item not included in this public package) records the pending requirements and routing question; earlier acknowledgment is not a fix and does not imply receipt of this new note. Existing local Sherlock0.1.2 adoption is separately documented; no evidence/report intake or finding acceptance was performed by this comparator batch.
