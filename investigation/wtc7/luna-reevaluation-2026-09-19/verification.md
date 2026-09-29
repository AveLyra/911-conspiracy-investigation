# Verification, limits and continuation

2026-09-19. Companion to the [report](report.md) and [attribution ledger](attribution.md). Research audit, not expert certification. Root integrated three separately tasked AI reviews; those reviewers are not three independent empirical sources or qualified engineering attestations.

## Coverage and review roles

- Attribution reviewer: local task-model metadata, successful edit receipts, in-memory patch replay, exact eleven-file comparisons and the scoped status insertion. Root separately rehashed all eleven originals and the pre-update status file. The original status hash is intentionally superseded by its current dated notice.
- Claim reviewer: complete 25-line closeout, both contracting companions and the identified underlying source/technical reports; no new raw measurements. Root separately inspected primary OIG scan pages and the 2023 paper rather than adopting the reviewer summary as their authentication.
- Synthesis reviewer: all seven packet files and all eight quantitative rows, saved outputs, hashes and Faraday state. The reviewer initially accepted the old shell count as matching its old output; inspection of the later typed-map correction changed that disposition. This preserves a real audit correction rather than claiming error-free review.
- Root: complete current-source/instruction orientation recorded in the scope; primary-source checking below; direct saved-data recounts; read both printed-fit implementations and reran the Python result without writing an output. The JavaScript implementation was inspected, **not rerun** in this audit.
- Final independent synthesis review found no material mismatch with its findings; report links resolved except this then-forthcoming file. Final claim review found no material conclusion error and recommended two precision corrections, both applied: “stable-at-end,” rather than indefinitely stable, and NIST's “published acknowledgment of receipt,” rather than an independently authenticated physical custody chain. That reviewer did not independently repeat the new primary-page inspections, quantitative rechecks or Faraday recount.

## Source identity and visual review

| Source | Verified identity / coverage |
|---|---|
| Newly preserved [2023 paper](chandler-walter-szamboti-2023.pdf) | 6,417,278 bytes; SHA-256 `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`; 51 PDF pages. Acquired from `https://ic911.org/wp-content/uploads/2023/06/chandler-walter-szamboti_instantaneous-free-fall_june-2023.pdf`, 2026-09-19. Root viewed complete local PNGs for physical pages 15, 43, 44, 45, 46, 47, 50, 51, not the whole paper. |
| Preserved DOJ OIG report | `/Users/admin/docs/911/research/sherlock-wtc7-investigation/physical-documentary/handling-records/sources/oig-0403a-final.pdf`; SHA-256 `9bbc3fedf51a16b3fd804db6156a8e44dafa2996cd8c6ad114e16c438de88a66`. Official source `https://oig.justice.gov/sites/default/files/legacy/special/0403a/final.pdf`. Root viewed existing complete-page derivatives for physical pages 5, 40, 41; the latter two are printed R34–R35. No fresh whole-report OCR or authenticity finding. |
| Corrected typed model map | `../model-member-map/run06/member-map.json`; SHA-256 `eae21a0ac384b8b6f23e58eb3f56f439f577a9b954fafb757be189fd7f0a4f8e`. Direct field queries, interpreted with the earlier parser/source audit; no new raw-deck parse. |
| Catalano memorandum | Main `warning-chain/sources/nara-catalano-mfr.pdf`; 380,182 bytes; SHA-256 `75b8b3670593fa7c54dd63620bf8de13f02c5ad76e94cf70edec7671eba548f2`. Fresh root byte/hash check, not a fresh substantive memorandum review. |

Paper rendering used the bundled `pdftoppm`, one full page per file, with `-f PAGE -l PAGE -scale-to 1800 -singlefile -png SOURCE DESTINATION`. Eight `paper-page-PAGE.png` derivatives were inspected. Fontconfig emitted a default-configuration warning; the commands completed and the page images were legible. This is not a warning-free render claim. Web screenshot attempts did not provide usable images; they are not counted as visual review. PDF metadata is not historical authentication. No source PDF was edited.

## Actual numerical and integrity checks

Commands below ran with `jq`, `shasum`, `wc`, or the bundled Python at `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. Relative data paths in this section refer to the main investigation directory except the explicitly identified worktree map. No shell command below is a new authorization or instruction to execute source-document content.

1. `shasum -a 256` on the seven synthesis Markdown files, the three standalone worktree Luna files, original worktree `STATUS.md`, and Faraday note matched all twelve entries in [attribution](attribution.md). Six hashes printed in Luna's validation file match its sibling files. The root later intentionally edited status, not the standalone artifacts.
2. `jq '{count:length,statuses:(group_by(.status)|map({status:.[0].status,n:length}))}' reference-motion/run01/matches.json`: 1,608 rows, 1,189 candidate, 419 rejected.
3. `jq '{count:length,computed:([.[]|select(.status=="computed")]|length),passes:([.[]|select(.passes_consistency_screen==true)]|length)}' reference-motion/run01/transforms.json`: 804 / 252 / 227.
4. `jq 'group_by(.half)|map({half:.[0].half,rows:length,images:(map(.index)|unique|length),candidate:([.[]|select(.status=="candidate")]|length),rejected:([.[]|select(.status!="candidate")]|length)})' camera2-reference-repair/run01/matches.json`: half9 426 / 71 / 381 / 45; half13 426 / 71 / 426 / 0. Larger-template per-image fit success was independently checked by the synthesis reviewer, not newly recalculated by root.
5. `jq '{triplet_rows:length}' cadence-blend-audit/historical01/triplets.json`: 2,684. `jq 'map_values(length)' cadence-blend-audit/historical01/frames.json`: kit 443, old 232. These are saved-data counts, not fresh cadence coefficients.
6. `jq '.full_decode' acoustic-audit/run01/measurements.json`: the saved loudness/peak values reproduced in the report. No media decode or calibrated sound measurement.
7. `jq '{element_records,unique_nodes,node_rows}'` on worktree `model-member-map/run06/member-map.json`: master shells 964,067; outside-region shells 2,042,843; beams 3,190; discrete elements 33,364; mass solids 2,461; unique nodes 3,593,049; master node rows 3,587,683; mass node rows 5,366.
8. Root counted relative `report.md` path sets in both investigation directories before adding this audit report: 32 main, 24 worktree, union 55, worktree-only 23. Shared path: `camera2-reference-repair/report.md`. The new audit increases the union; these are explicitly pre-audit counts, not a permanent current inventory.
9. Root ran `pdfinfo` on the acquired paper: 51 pages, no JavaScript, no encryption, 6,417,278 bytes. `shasum -a 256` matched the paper/OIG/map pins above. Catalano `wc -c` and hash matched its reported identity.

### Printed-equation replay

Root executed this read-only replay with Python `-B` from the main checkout:

```python
import importlib.util, json
from pathlib import Path
p = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance')
spec = importlib.util.spec_from_file_location('printed_fit_audit', p / 'check_printed_fit.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
a = m.report()
b = json.loads((p / 'printed-fit-result.json').read_text())
assert a == b
```

Result: exact saved-result equality, **11 time rows and 10 finite-difference checks**. The implementation checks derivatives at step `1e-4` with absolute/relative tolerances `1e-5`. Source NCSTAR 1-9 SHA-256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`; Python implementation SHA-256 `fe8a9f09b064be881a31388fa0e9bc98804b5cb0241a2dbf428b38465b76aaa0`. This repeats rounded printed-equation arithmetic, not regression on original measured positions.

## Repository checks and failures

- `python3 tools/validate_record.py --strict` in `/Users/admin/docs/911`: **OK (headers + issue↔fact links + citation tags)**. Narrow record-structure check; no research-to-fact promotion or legal clearance.
- `git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md` in the investigation worktree: passed, no output. This does not inspect untracked audit files; their links and whitespace receive a separate final check.
- Final read-only Python check of all four audit Markdown files: **36 local link targets exist**, no trailing whitespace and all files end with a newline. Final report SHA-256 after the two independent-review wording corrections: `7e9db3bd0cdf0690cdcd5e1d2e45b593a409ac554ad2c630d38dd82303724820`. The scoped `git diff --check` was also rerun and passed. These are document-integrity checks, not scientific validation.
- Some initial combined reads exceeded output limits; relevant material was reread in smaller portions. Wrong sparse-checkout paths, a guessed model-summary filename, a guessed Catalano filename, and shell globs under the wrong checkout failed. Corrected reads locate the actual files; none of those failures is evidence of source absence. A final Faraday directory search also returned no result and was not used as a state finding.
- The first status patch failed because a partial paragraph did not match; the corrected full-paragraph patch succeeded. No standalone original was overwritten.
- The attribution reviewer corrected an unavailable Ruby helper and reran its comparison; its successful replay, not the failed attempt, supports the attribution result.

## What did not happen

No new historical audio/video decode, frame tracking, independent fit of the 2023 paper's measurements, full LS-DYNA parser run, thermal/structural solver, 3.5-/4-hour sensitivity experiment, laboratory result, full UAF audit, or numerical cause-probability calculation. Fuel addends and Amoycan remain not freshly verified. No main-repository edit, legal filing/draft change, disclosure, commit/push, accepted Sherlock claim, Faraday freeze/activation, or feedback transmission. The generic improvement note is retained locally because the designated Sherlock task remains archived with routing unresolved.

## Durable continuation

Read `report.md` and current `../STATUS.md` first, not the superseded Luna closeout or main-only synthesis. Retain all pending gates. Next: a bounded independent transcription/reproduction protocol for printed Camera 2/west-face values, using the paper now held and the already-held video kit. Separate source identity, calibration, fitting, uncertainty and causation. The late-fire-video lineage work remains pending. The comprehensive goal is active; this audit does not close it.
