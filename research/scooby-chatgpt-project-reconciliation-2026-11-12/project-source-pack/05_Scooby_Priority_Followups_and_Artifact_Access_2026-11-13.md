# Scooby priority follow-ups and artifact-access status

**Date:** 13 November 2026  
**Scope:** Six agenda priorities, eight completed chat turns, and retrievable generated outputs.  
**Relationship to the prior pack:** Supplemental to `04_Scooby_Research_Results_and_Next_Stage_2026-11-13.md`; it does not revise the earlier 117-chat inventory or imply that repeated summaries independently corroborate one another.

## Updated status

| Topic | 13 Nov result | What remains |
|---|---|---|
| **R13 — iron-rich spheres** | The Pro source-recovery follow-up identified four USGS Iron-03/04 TIFF paths and an EPA-hosted later RJ Lee methods submission. | No TIFF bytes, specimen-to-run chain, denominator records, or May 2003 Volume III. The result ZIP is named in the chat but is not downloadable in the current view. No specimen-level quantitation. |
| **R03 — Flight 93 audio/assets** | Documentary timing descriptions were compared and an original-media gate report was retrieved. | Original MP3s and P200055 ZIP bytes were not inspected; no audio-derived correction. |
| **R01 — SEC packet** | A bounded audit report was retrieved. The original 704-page packet was not indexed. | The structured transaction ledger card cannot be opened or downloaded; packet-level review still depends on original bytes. |
| **R21 — Flight 77 recorder** | The retrieved report records input hashes and a flash-page envelope probe, but states that no raw word was matched to an engineering CSV cell. | The 55,468,480-byte reproducibility ZIP in personal Library was not accessible through its cited link. No decoder was run in this continuation; no new raw-to-export result. |
| **R08 — heated connections** | A source-gate report and instrument-map CSV were retrieved. The NIST page describes downloadable spreadsheets for the test series. | No NIST XLSX or instrumentation drawing bytes, native sheet/cell map, measured time series, or benchmark run. |
| **R25 — procurement** | A Pro primary-source follow-up corrected locators and distinguished interim withholding/release from final indirect-rate determination and closeout. | The separate Army compilation's pages 36–117, final-rate instruments, closeout vouchers, and remittance evidence remain unverified. The first-turn Markdown download was not recovered. |

## Retrieval and verification notes

- **R21 package:** the report names `Flight77_Reproducible_Audit_2026-11-12.zip`, 55,468,480 bytes, Library ID `libfile_9afb870a0e8c81919153b878881eb102`, and three member SHA-256 values. Opening its cited Library URL redirected to `chatgpt.com/space`; no package bytes were returned. The report's recorded hashes and prior computations are preserved as that report's claims, not presented here as a fresh independent reproduction.
- **R08 workbooks:** NIST's official project page says experiment spreadsheets are downloadable and lists the five tests plus the instrumentation layout ([NIST project page](https://www.nist.gov/programs-projects/measurement-structural-performance-fire/steel-concrete-composite-floors)). Direct web retrieval rejected the XLSX MIME type; in-app Browser reported `net::ERR_BLOCKED_BY_CLIENT` for the official route; a subsequent shell GET failed DNS resolution. A HEAD response had exposed the ambient workbook target `https://www.nist.gov/system/files/documents/2020/02/14/CB-DA-AMB.xlsx`, but no workbook bytes were acquired. These are access failures, not evidence that NIST's files are absent.
- **R01 ledger:** `Scooby_R01_transaction_ledger_2026-11-13.json` was displayed as a Code file. Its preview returned “Couldn't load this file”; clicking the attachment's download control yielded no completed download. No substitute ledger was fabricated.
- **R13 / R25 first-turn files:** named sandbox artifacts are recorded in the chat capture, but their bytes were not exposed as downloadable attachments in the current view.

## Next research batch

1. **R21 raw-to-export reconciliation**, once the user reattaches or restores access to the named reproducibility ZIP. Verify the ZIP and member hashes first, then recover the exact decoder or reconstruct it from primary format documentation, qualify word keys, validate frame sync and compare selected decoded words to CSV cells. Keep bitstream equivalence separate from historical RAPS execution and physical aircraft installation.
2. **R03 original media**, if the native MP3 and court ZIP bytes become available. Confirm format, provenance and playable originals before listening or making timing/attribution claims.
3. **R08 native NIST data**, if the XLSX downloads become retrievable. Hash each workbook, inventory sheets/headers/units/formulas, reconcile channel locations against the drawing workbook, then decide whether a calibrated held-out benchmark is supportable.
4. **R01 and R25 packet completion** remains secondary: restore the SEC packet/ledger for R01 and the Army compilation for R25 before expanding their conclusions.

**R21 execution status:** I attempted to reopen the listed Library item, but the link resolved to Space. I did not send a new R21 prompt at Pro: the current model menu in that chat displays “Usage limit reached” while GPT‑6 is at High. No Deep Research was started. The specific input needed to resume the raw decoder analysis is the 55.5 MB `Flight77_Reproducible_Audit_2026-11-12.zip` or its three hash-identified members plus the decoder/probe scripts.
