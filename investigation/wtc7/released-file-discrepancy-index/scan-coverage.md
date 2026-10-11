# Phase 1/2 scan coverage

2026-09-11. Research only. Scanner: `phase1_full_scan.py`. No LS-DYNA/ANSYS execution. No writes under `exhibits/raw/`.

## Scanner pins

| Item | Value |
|---|---|
| Scanner | `research/sherlock-wtc7-investigation/released-file-discrepancy-index/phase1_full_scan.py` |
| Scanner SHA-256 | `60ef8597aaa0ccae7dea81a4acd1d611e99da56a6df864961b7384fdb4d9bef8` |
| Thermal zip SHA-256 | `2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181` (matches `SRC-085` / June manifest) |
| Machine outputs | `phase1-coverage.json`, `phase1-hits.json`, `phase1-followup.json`, `phase2-pypdf.json` |

Helpers used for pins only: `phase1_followup.py`, `phase1_followup2.py`, `phase2_prose_scan.py`, `phase2_pypdf.py`. `phase2-pypdf.json` stores category/count excerpts only; recipient address lines were omitted.

## Thermal zip census (complete)

25,634 files + 5 directory entries.

| Case | Files |
|---|---:|
| A | 8,364 (all `.int`; basenames identical to C) |
| B | 8,906 = 8,634 under `INTFILES+10%14SEP07` + 272 PNG under `PNGFILES+10% 14SEP07` |
| C | 8,364 (all `.int`) |

Case B `INTFILES` extras versus A: 96 `WTC7-Fl##-SLNo-N.int` + 173 `.nod` + `mover`.

| Class | Count | What was read |
|---|---:|---|
| `.int` | 25,188 | All ≤2 KiB as text except one NUL-blocked file |
| Hour drivers `WTC7-N.int` | 36 (12 × A/B/C) | All text-read |
| Floor-hour drivers | 288 | All ≤2 KiB text-read; larger even-floor drivers header-sampled |
| `*Core*` | 1,152 | Header-sampled: one large core per `WTC7-Fl##` × case |
| Large `.int` (mostly SLAB / big members) | 384 | 40-file stratified header sample including one SLAB each from A/B/C |
| `.nod` | 173 | All text; node-id / coordinate lists; Case B only |
| PNG | 272 | Filenames and count only |
| Extensionless | 1 | `mover` (148 bytes) fully read |

Floor-prefix counts in A/C: Fl07/09/11/13 = 72 each (12 hour drivers + 12×5 CoreB/Core1/Core2/Core3/SLAB). Fl08/10/12/14 = 2,016 each (those 72 plus member-level `1C`/`2C` files). Case B is +12 per prefix (`SLNo` × 12 hours).

PNG folder name carries `+10% 14SEP07`. Basename examples: `7_000.png`, `7_fl10_ls1_000.png`. No PNG basename contains delete/4.0/4.1/3.5.

## Include / comment graph

Checked against (a) June zip basenames, (b) September six basenames, (c) `facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv`.

Still absent as those names:

- `Damage_Global_ANSYS_CaseB_4.1hr.k` (DISC-001)
- `1 Floor_8-16_16JUL07.apdl` and `2 Floor_GR_TO_7-19JUL07_3.apdl` (DISC-011)
- `FL2-LOAD1.APDL` … `FL7-LOAD1.APDL` (DISC-012)

Present in September only: `WTC7_CaseB_400pm.int` (DISC-022). Commented `WTC7-1.int` exists in June as 184–193 byte ANSYS stubs (DISC-003).

September live includes, re-walked: `elem_thick_to-renum.k`, `discrete_mass.k`, `WTC7_CaseB_400pm.int`. Commented: `$WTC7-1.int`, `$Damage_Global_ANSYS_CaseB_4.1hr.k`. No new filename.

## Phase 2 prose

| Source | File/count named | Bytes agree? |
|---|---|---|
| SRC-115 | “six (6) additional files” released in full | Yes: six `.gz` arrived. Does not name 4.1hr / 3.5hr / FL-LOAD / July APDL |
| SRC-030 Draft 2 8.a.i–ii | Releasable 16-story ANSYS “does not include the connection models”; LS-DYNA “connection material models are removed” | LS-DYNA side already DISC-006. ANSYS side added DISC-028 |
| SRC-086 Finding | Same two withheld categories | No new filename/count row |
| SRC-006 Aug 25 | Withholds 16-story detailed-connection ANSYS and LS-DYNA 47-story inputs/results | Historical; six LS-DYNA inputs later acknowledged (DISC-016) |
| EXH-014 Fletcher | Case B 8,910 released | 8,906 in the zip (DISC-014) |

June 5 interim-letter PDF was not re-extracted from the SRC-029 EML. See [scan-gaps.md](scan-gaps.md).

## Remaining unread

- Full bodies of large SLAB / member `.int` files after the 8 KiB header (BF/BFE temperature cards; no `/input` in sampled headers)
- PNG pixels
- SRC-029 attached June letter PDF (not a standalone extract on disk)

A miss in those classes is an incomplete scan, not proof of absence.
