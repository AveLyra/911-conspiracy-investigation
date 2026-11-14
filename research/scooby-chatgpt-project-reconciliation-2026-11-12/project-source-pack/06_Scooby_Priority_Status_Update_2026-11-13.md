# Scooby priority status update — 13 November 2026

This update supersedes the R21 zero-match status in files 04 and 05 for the bounded raw-to-export computation. Those earlier files remain historical snapshots. This is a status update, not an independent re-audit of all six topics.

## R21 — Flight 77 raw words to engineering export

The latest R21 report is preserved as a PDF and reproducibility ZIP under `priority-followups-2026-11-13/result-files/R21/raw-word-reconciliation/`; the 55.5 MB source package is preserved under `result-files/R21/source-inputs/`. The corresponding rendered chat turn is archived in `chat-captures/6af7d5c1-0fc0-83ea-88a0-9cfe949d3650-turn-01.md`.

The report verifies the source archive and three member hashes against actual opened bytes. It reports 56/56 selected engineering values matching exactly across four predefined frames, plus 4/4 frame-counter joins. The 56 values are 16 pressure-altitude, 32 computed/true-airspeed, and 8 barometer values, supported by 76 qualified decoded words. Boeing conversion rules match all sampled values; a literal database-printout pressure-altitude alternative differs in 14/16 samples. The bounded sync/order gate covers 1,298 complete unique frames. The report also records 19/19 independent absolute-baseline matches and 17/17 periodic duplicate-baseline matches.

**Updated decision:** GO for the sampled raw-to-export comparison and the bounded final-segment decoder/order checks. The conclusion is limited to these validated inputs, segment, four frames and selected fields. Whole-capture or full-CSV equivalence, earlier segments, the partial terminal frame, Hamming/parity certification, historical RAPS behavior, aircraft-specific installation/wiring, radio-height calibration, independent timing/trajectory and suppression remain unestablished. A successful reconstruction does not prove which decoder or configuration was historically run by NTSB.

The 55,468,480-byte source ZIP was subsequently downloaded from its Personal Library item, hashes to `528cdb88a2010a66af9fd6f30ddfb6b048a49b0b1da15f2c754e079ffa5fc442`, passes the ZIP integrity check, and contains the three members whose hashes are reported in the R21 PDF. This confirms local archive identity with the named Library package; it is not agency-side authentication.

## Current six-topic queue

The following status is carried forward from the user's 13 November update. Apart from R21, this file does not independently re-open the cited source records.

| Topic | Remaining work |
|---|---|
| R01 — SEC trading | Complete the 704-page packet index; reconcile cancellations, account allocations, portfolio context and referral responses. |
| R08 — Heated connections | Obtain native NIST workbooks and instrumentation drawings; extract time series and channel definitions; decide whether inputs support a numerical benchmark. No benchmark has run. |
| R13 — Iron-rich spheres | Published-method and source-location work complete; obtain four original USGS TIFFs with specimen/run linkage, May 2003 Volume III, and applicable classifications, denominators and uncertainty data. |
| R03 — Flight 93 calls | Documentary comparison complete; obtain two playable original MP3s and P200055 flights.zip for audio–memorandum and native call-key/caller-attribution analysis. |
| R25 — KBR | Verify/index Army compilation pages 36–117; obtain final indirect-rate agreements for task orders 1–4, remittances and closeout vouchers. |
| R21 — Flight 77 | Extend sampled reconciliation to whole-capture equivalence; resolve historical RAPS behavior/configuration, aircraft-specific installation/calibration and independent timing/trajectory checks. |

## Next batch recommendation

1. **R01 packet index.** First confirm the exact 704-page PDF version and bytes, then inventory each document boundary/page and stable locator. Keep transaction arithmetic and attribution gated on original cancellation, allocation, referral and price records.
2. **R08 workbook recovery.** In parallel where convenient, retrieve and hash the native NIST workbooks and instrumentation drawings. Inventory sheets, units, calibration, channel labels and missingness before deciding whether a numerical benchmark is supported.
3. Keep R13 and R03 at their original-file gates until the specified binaries are available. Continue R25 only after obtaining the unverified compilation pages and final payment/indirect-rate records. Extend R21 only with a declared full-capture acceptance test; sampled exact matches do not imply whole-capture equivalence.

## Provenance

- R21 report Library item: https://chatgpt.com/library?file_id=libfile_b872a0a8154c81919fa49ecc038e4370&account_id=personal
- R21 source package Library item: https://chatgpt.com/library?file_id=libfile_9afb870a0e8c81919153b878881eb102&account_id=personal
- R21 chat: https://chatgpt.com/g/g-p-6aed53a21aec8191b9aab8307b9c8e49-scooby/c/6af7d5c1-0fc0-83ea-88a0-9cfe949d3650
- The reports in 04 and 05 are retained unchanged as historical records. No local sources or chats were deleted.

