# Scooby priority follow-ups — 13 November 2026

This supplement preserves the six priority research chats created from the 13 November agenda. It is separate from the original 117-chat / 36-file inventory snapshot; those counts and files are unchanged.

## Captured chats

The ChatGPT reader lists six threads and eight completed turns: R13 and R25 have two turns each; R03, R01, R21 and R08 have one each. The visible user/assistant text is preserved as eight turn-level Markdown captures in `chat-captures/`. These are rendered-page captures, not a raw account export, full tool log, or account-side checksum certificate.

| Topic | Thread ID | Turns | Captures |
|---|---|---:|---|
| R13 — Iron Sphere Audit | `6af73dd6-cb60-83ea-ab81-d20a0282c689` | 2 | `chat-captures/6af73dd6-cb60-83ea-ab81-d20a0282c689-turn-01.md`, `...-turn-02.md` |
| R03 — Original Media Audit | `6af73ee1-9c88-83e9-8bae-a8ec5d9a926b` | 1 | `chat-captures/6af73ee1-9c88-83e9-8bae-a8ec5d9a926b-turn-01.md` |
| R01 — SEC trading reconciliation | `6af73f14-5a24-83e9-a414-74e689bffc8c` | 1 | `chat-captures/6af73f14-5a24-83e9-a414-74e689bffc8c-turn-01.md` |
| R21 — Flight 77 Reconciliation | `6af73f2d-baa0-83e9-93d6-19c5bad48a64` | 1 | `chat-captures/6af73f2d-baa0-83e9-93d6-19c5bad48a64-turn-01.md` |
| R08 — Benchmark readiness audit | `6af73f41-63fc-83ea-8480-6483d7e4cb56` | 1 | `chat-captures/6af73f41-63fc-83ea-8480-6483d7e4cb56-turn-01.md` |
| R25 — Procurement Packet Verification | `6af73f56-a568-83e9-b5e3-d6c54fce6e85` | 2 | `chat-captures/6af73f56-a568-83e9-b5e3-d6c54fce6e85-turn-01.md`, `...-turn-02.md` |

A consolidated research-status digest is in the root archive at `project-source-pack/05_Scooby_Priority_Followups_and_Artifact_Access_2026-11-13.md`.

## Retrieved result artifacts

Seven downloadable outputs were retrieved and SHA-256 inventoried:

- R03: original-media gate report.
- R01: bounded SEC audit report.
- R21: raw-candidate reconciliation report.
- R08: NIST source-gate report and instrument-map CSV.
- R25: primary-source verification report and structured claim ledger.

See `manifest.json` for exact paths, sizes and hashes.

## Known retrieval gaps

- **R13:** the result references `Scooby_R13_Record_Recovery_2026-11-13.zip`, but the current chat view exposes no downloadable attachment for it. The visible result text is captured; ZIP bytes are not.
- **R01:** `Scooby_R01_transaction_ledger_2026-11-13.json` appears as a file card, but its preview says “Couldn't load this file”; download attempts timed out. The report and visible response are preserved; the JSON bytes are not.
- **R21:** the report identifies `Flight77_Reproducible_Audit_2026-11-12.zip` (55,468,480 bytes; Library ID `libfile_9afb870a0e8c81919153b878881eb102`). Its cited Library link redirected to ChatGPT Space without opening the file. The report says the three input members hash-matched, but I did not independently repeat that check in this turn. The raw-to-export decoder step remains unrun.
- **R25:** the first-turn response links `Scooby_R25_KBR_packet_gate_and_payment_followup_2026-11-13.md`; that separate artifact's bytes were not retrieved. Its visible response text is in the turn capture and the later source-verification report is preserved.
- **R08:** NIST's project page advertises downloadable experimental spreadsheets and an instrumentation layout, but native workbook bytes were not acquired. The official XLSX routes failed in the available web/browser retrieval paths. No measured time-series rows were extracted.

These gaps are recorded rather than reconstructed from summaries. No local files, chats, or source history were deleted.
