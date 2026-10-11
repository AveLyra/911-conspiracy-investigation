# Released-file discrepancy index

Research only. Stable IDs live in [discrepancy-index.csv](discrepancy-index.csv). The human grouped list is [index.md](index.md). Investigation/case use is [discrepancy-implications.md](../lsdyna-supplement-content-audit/discrepancy-implications.md).

This is not a fact spine, exhibit list, or pleading. Do not promote a row into `facts/` without a separate verification pass.

## How to look something up

| If you want… | Use |
|---|---|
| One ID | `DISC-###` in the CSV |
| Old D1–D10 labels | CSV `alias` column |
| All missing named files | `kind=named_absent` |
| Version/date/hour mismatches | `kind=version_label` |
| Case A/B/C mixing | `kind=case_mix` |
| Live vs commented cards | `kind=live_vs_commented` |
| FOIA production questions | `case_role` not `none` |
| Conspiracy-track role | `investigation_role` |
| Fresh-agent full sweep | [full-scan-prompt.md](full-scan-prompt.md) |

## Coverage

Scanned 2026-09-11, no solver run. Details: [scan-coverage.md](scan-coverage.md). Gaps: [scan-gaps.md](scan-gaps.md).

- June 2025 extract (`SRC-084`–`SRC-086`): three APDL files; `ANSYS Thermal Data.zip` (25,634 members — every name counted; every ≤2 KiB member text-read except one NUL-blocked file; stratified large-`.int` headers)
- September 2026 LS-DYNA inputs (`SRC-116`–`SRC-121`): keyword comments, includes, controls, set labels; no new include names beyond DISC-001–010
- Phase 2 prose: SRC-115, SRC-030 Draft 2, SRC-086 Finding, SRC-006 August 25 letter

Not scanned as full bodies: large SLAB/member `.int` files beyond 8 KiB headers; PNG pixels. A miss there is an incomplete scan, not proof of absence.

This index is **not** a scan of NCSTAR PDFs, request 000185, or court opinions. The June 5 interim-letter PDF was not re-extracted from the SRC-029 EML attachment; DISC-016 already covers that letter’s LS-DYNA promise.

## Definitely note

**Case (keep; do not overplead):** DISC-016 (June omission, now acknowledged); DISC-001/007/011/012/022/025 (named files still not produced as those names, or dated copies disagree); DISC-006/019/028 (connection-material / “no connection models” boundary); DISC-010/014/026 (2010 identity and Case B count/`SLNo`). SRC-115 still does not explain the other four request categories. Do **not** allege the six September inputs remain undelivered. Do **not** plead collapse cause from these cards.

**Investigation (keep as tests, not as operation evidence):** DISC-004/005/017/018 (handoff is now inspectable text); DISC-001/007/013/026 (thin hour/+10%/`SLNo` cut with no twin control); DISC-015/024 (Fl07 off in Case A/B; Fl11/13 are Core/SLAB-only trees). Do **not** promote DISC-008/009/023/027, penthouse decoupling, `mover`, or +10% into conspiracy support. Nothing in this index is discriminating of a concealed operation.

## ID rule

Assign the next `DISC-###`. Do not reuse. If a row is withdrawn, set `status=withdrawn` and leave the ID.
