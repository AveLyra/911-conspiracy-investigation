# Scooby priority follow-ups — 13 November 2026

This supplement preserves the six priority research chats created from the 13 November agenda and the subsequent R21, R01 and R08 Pro continuations. It is separate from the original 117-chat / 36-file inventory snapshot; those historical counts and files are unchanged.

## Captured chats

The original priority set has six threads and eight completed turns: R13 and R25 have two turns each; R03, R01, R21 and R08 have one each. Separate R21, R01 and R08 Pro continuations add three chats and three completed turns. The visible user/assistant text is preserved as eleven turn-level Markdown captures in `chat-captures/`. These are rendered-page captures, not a raw account export, full tool log, or account-side checksum certificate.

| Topic | Thread ID | Turns | Captures |
|---|---|---:|---|
| R13 — Iron Sphere Audit | `6af73dd6-cb60-83ea-ab81-d20a0282c689` | 2 | `chat-captures/6af73dd6-cb60-83ea-ab81-d20a0282c689-turn-01.md`, `...-turn-02.md` |
| R03 — Original Media Audit | `6af73ee1-9c88-83e9-8bae-a8ec5d9a926b` | 1 | `chat-captures/6af73ee1-9c88-83e9-8bae-a8ec5d9a926b-turn-01.md` |
| R01 — SEC trading reconciliation | `6af73f14-5a24-83e9-a414-74e689bffc8c` | 1 | `chat-captures/6af73f14-5a24-83e9-a414-74e689bffc8c-turn-01.md` |
| R21 — Flight 77 Reconciliation | `6af73f2d-baa0-83e9-93d6-19c5bad48a64` | 1 | `chat-captures/6af73f2d-baa0-83e9-93d6-19c5bad48a64-turn-01.md` |
| R08 — Benchmark readiness audit | `6af73f41-63fc-83ea-8480-6483d7e4cb56` | 1 | `chat-captures/6af73f41-63fc-83ea-8480-6483d7e4cb56-turn-01.md` |
| R25 — Procurement Packet Verification | `6af73f56-a568-83e9-b5e3-d6c54fce6e85` | 2 | `chat-captures/6af73f56-a568-83e9-b5e3-d6c54fce6e85-turn-01.md`, `...-turn-02.md` |
| R21 — Verify Raw Export Match (Pro continuation) | `6af7d5c1-0fc0-83ea-88a0-9cfe949d3650` | 1 | `chat-captures/6af7d5c1-0fc0-83ea-88a0-9cfe949d3650-turn-01.md` |
| R08 — NIST native workbook recovery (Pro continuation) | `6af86ff2-e864-83ea-b130-fd61999c83c7` | 1 | `chat-captures/6af86ff2-e864-83ea-b130-fd61999c83c7-turn-01.md` |

A consolidated research-status digest is in the root archive at `project-source-pack/05_Scooby_Priority_Followups_and_Artifact_Access_2026-11-13.md`; current R01/R21 status is in `project-source-pack/07_Scooby_Priority_Status_Update_2026-11-14.md`; the R08 native-file recovery is in `project-source-pack/08_Scooby_Priority_Status_Update_2026-11-14.md`.

## Retrieved result artifacts

Sixteen downloadable result outputs are now retrieved and SHA-256 inventoried. The two R21 continuation outputs are in `result-files/R21/raw-word-reconciliation/`. The R01 packet-index outputs are in `result-files/R01/packet-index/`. R08’s complete native recovery bundle is in `result-files/R08/`; its 166 members are extracted for browsing under `result-files/R08/native-recovery/`, and exact ZIP reconstruction parts are in `result-files/R08/package-parts/`. The R21 input package is separately preserved in `result-files/R21/source-inputs/`:

- R03: original-media gate report.
- R01: bounded SEC audit report, complete 704-page coverage report and machine-readable index, and complete audit bundle with the exact official SEC PDF.
- R21: raw-candidate reconciliation report.
- R08: NIST native workbook recovery bundle (six original XLSX files, inventory, source/provenance manifests, corrected map, extracted series and reproducibility scripts), audit HTML and delivery manifest.
- R25: primary-source verification report and structured claim ledger.
- R21 continuation: detailed 8-page report PDF and 34-file reproducibility ZIP. A Ghostscript text extraction is included for indexing; the PDF remains the report artifact.

See `manifest.json` for exact paths, sizes and hashes.

## Known retrieval gaps

- **R13:** the result references `Scooby_R13_Record_Recovery_2026-11-13.zip`, but the current chat view exposes no downloadable attachment for it. The visible result text is captured; ZIP bytes are not.
- **R01 prior ledger:** `Scooby_R01_transaction_ledger_2026-11-13.json` remains unretrieved from the earlier chat. The new 704-page index and complete audit bundle are separate deliverables and do not reconstruct that missing ledger file.
- **R21 source input package:** `Flight77_Reproducible_Audit_2026-11-12.zip` (55,468,480 bytes; Library ID `libfile_9afb870a0e8c81919153b878881eb102`) was downloaded and copied into this supplement. Its SHA-256 is `528cdb88a2010a66af9fd6f30ddfb6b048a49b0b1da15f2c754e079ffa5fc442`; ZIP integrity passed; the three named members independently match the recorded hashes. The archive is a candidate source package, not an agency checksum certificate.
- **R21 continuation ZIP integrity:** the downloaded 397,312-byte ZIP passed `unzip -t`; its reproduction claims and contents are preserved. The original input package is not embedded in it.
- **R25:** the first-turn response links `Scooby_R25_KBR_packet_gate_and_payment_followup_2026-11-13.md`; that separate artifact's bytes were not retrieved. Its visible response text is in the turn capture and the later source-verification report is preserved.
- **R08:** the earlier source-gate report was superseded on 14 November: all six native NIST XLSX files are recovered and checksummed. The source-access gate passes; benchmark readiness remains open for clock alignment, physical sensor-validity windows, thermal inputs and constitutive assumptions. No model ran.

These gaps are recorded rather than reconstructed from summaries. No local files, chats, or source history were deleted.

## Updated priority status

`../project-source-pack/06_Scooby_Priority_Status_Update_2026-11-13.md` supersedes the R21 zero-match status in the earlier snapshot summaries for the bounded computation. `../project-source-pack/07_Scooby_Priority_Status_Update_2026-11-14.md` supersedes the R01 packet-index status in files 04–06. `../project-source-pack/08_Scooby_Priority_Status_Update_2026-11-14.md` supersedes the R08 file-access status in the earlier source gate. The earlier summaries remain unchanged as historical records. R08 was reopened against native NIST files on 14 November. R03, R13 and R25 remain carried forward from the 13 November status and were not independently reopened in this supplement.
