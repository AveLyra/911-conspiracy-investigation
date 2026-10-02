# Phase 1/2/second-sweep scan coverage

2026-09-11 Phase 1/2; 2026-09-12 second sweep. Research only. No LS-DYNA/ANSYS execution. No writes under `exhibits/raw/`.

## Scanner pins

| Item | Value |
|---|---|
| Scanner | `research/sherlock-wtc7-investigation/released-file-discrepancy-index/phase1_full_scan.py` |
| Scanner SHA-256 | `60ef8597aaa0ccae7dea81a4acd1d611e99da56a6df864961b7384fdb4d9bef8` |
| Thermal zip SHA-256 | `2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181` (matches `SRC-085` / June manifest) |
| Machine outputs | `phase1-coverage.json`, `phase1-hits.json`, `phase1-followup.json`, `phase2-pypdf.json`, `phase3-second-sweep.json`, `phase3-followup.json` |
| Second-sweep scanner | `phase3_second_sweep.py` (hash in `phase3-second-sweep.json`) |

Helpers used for pins only: `phase1_followup.py`, `phase1_followup2.py`, `phase2_prose_scan.py`, `phase2_pypdf.py`, `phase3_followup.py`. `phase2-pypdf.json` stores category/count excerpts only; recipient address lines were omitted. The SRC-029 letter PDF was decoded to `/tmp/disc-second-sweep/` only; it was not added under `exhibits/raw/`.

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
| PNG | 272 | Filenames and count; second sweep also read `tEXt`/`iTXt`/`zTXt` (none) |
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

SRC-029 June 5 letter PDF was extracted from the EML (2 pages). It names 16-story gravity ANSYS without connection models; three ANSYS temperature sets; and 47-story LS-DYNA inputs. That confirms DISC-016/021/028 language. It does not name 4.1hr / 3.5hr / FL-LOAD / July APDL.

## Second sweep (2026-09-12)

- Shared A/B/C basenames: 8,364. Byte-identical: A=B 2,298; A=C 2,391. Differing A/C files are members (5,589), cores (276), slabs (96), and the 12 hour drivers (DISC-015). A≠B≠C on most shared names is the three documented fire cases, not a new row.
- Case B `+10%` is not a uniform 1.10 scale of Case A. First 400 shared members with readable `BF TEMP` pairs: 207 near 1.0; 139 in 1.02–1.08; 54 in 1.08–1.12. Recorded on DISC-013; not a separate mismatch.
- 1,644 large `.int` bodies scanned for `/input`, delete/hour comments, and `!`/`$` lines after BF/BFE cards: no extra named include.
- Case B `WTC7-Fl08-1C137-2.int` is 328 NUL bytes; A/C twins are BF TEMP cards (DISC-029).
- 12 Case A vs B hour-driver hash diffs are line-ending only; logical `/input` lists match (Fl07 commented).

## Remaining unread

- Full numeric BF/BFE bodies as temperatures (include/comment hunt on those files is done)
- PNG pixels

A miss in those classes is an incomplete scan, not proof of absence.
