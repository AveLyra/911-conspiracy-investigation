# Discrepancy index (grouped)

IDs are stable in [discrepancy-index.csv](discrepancy-index.csv). This page is for browsing. Research only.

## Named but not delivered as that file

| ID | What | Ask |
|---|---|---|
| [DISC-001](discrepancy-index.csv) | Master wants `…4.1hr.k`; NIST sent `…4.0hr.k` | Where is 4.1hr? |
| [DISC-003](discrepancy-index.csv) | Master comments `WTC7-1.int`; live include is `WTC7_CaseB_400pm.int` | Format crosswalk. June `WTC7-1.int` is a 185-byte ANSYS stub |
| [DISC-007](discrepancy-index.csv) | 4.0hr damage list present; 3.5hr control absent | Produce the 3.5hr pair |
| [DISC-011](discrepancy-index.csv) | Loads APDL includes `…16JUL07` and `…19JUL07_3`; delivered geometry is `…15AUG07` and `…22AUG07` | Same files renamed, or missing dated copies? |
| [DISC-025](discrepancy-index.csv) | Ground-to-7 file is `…22AUG07`; its header says 15 August 07 | Same file, two dates |
| [DISC-012](discrepancy-index.csv) | Loads APDL includes `FL2-LOAD1`…`FL7-LOAD1` | Those six APDL files are not in the extract |
| [DISC-016](discrepancy-index.csv) | June letter promised LS-DYNA inputs; June extract had none | Historical omission; six files arrived 2026-09-11 |
| [DISC-022](discrepancy-index.csv) | `WTC7_CaseB_400pm.int` is not a June thermal-zip member | How does ANSYS Case B map onto this LS-DYNA field? |
| [DISC-029](discrepancy-index.csv) | Case B `WTC7-Fl08-1C137-2.int` is 328 NUL bytes; A/C twins are BF TEMP cards | Readable Case B copy of that member |

## Version / variant labels

| ID | What |
|---|---|
| [DISC-001](discrepancy-index.csv) | 4.1hr vs 4.0hr |
| [DISC-011](discrepancy-index.csv) | July include names vs August delivered APDL; loads file also banners 30JUL07 |
| [DISC-013](discrepancy-index.csv) | Case B thermal folder `INTFILES+10%14SEP07`; A/C have no +10% twin. 400 shared members are not a uniform 1.10 scale of Case A |
| [DISC-014](discrepancy-index.csv) | Case B 8,906 = 8,364 shared ints + 96 `SLNo` + 173 `.nod` + 272 PNG + `mover` vs Fletcher 8,910 |
| [DISC-025](discrepancy-index.csv) | `22AUG07` filename vs 15 August 07 comment |

## Case mixing / unused companions

| ID | What |
|---|---|
| [DISC-002](discrepancy-index.csv) | `G6A_CaseA_El_Delete_List` unused in a Case B package |
| [DISC-015](discrepancy-index.csv) | All 12 `WTC7-N.int` drivers: Case A/B comment out Floor 07; Case C includes it. All pull Floors 11 and 13 |
| [DISC-026](discrepancy-index.csv) | Case B live-includes 96 `SLNo` files; A/C have no such files or `/input` |
| [DISC-027](discrepancy-index.csv) | Case B `mover` script is not named by any thermal or LS-DYNA include |

## Live configuration vs later hooks

| ID | What |
|---|---|
| [DISC-004](discrepancy-index.csv) | Termination 4.50 s; thermal at 6.5 s; damage commented |
| [DISC-005](discrepancy-index.csv) | Deletion list, no residual stress |
| [DISC-017](discrepancy-index.csv) | 2008 slides: apply ANSYS damage instantaneously after temperature |
| [DISC-018](discrepancy-index.csv) | 2008 slides: delete elements, keep mass, drop bending/torsion |
| [DISC-021](discrepancy-index.csv) | Released ANSYS loads file is `0.25LL` gravity, names redacted |

## Category / withholding boundary

| ID | What |
|---|---|
| [DISC-006](discrepancy-index.csv) | `no-conn-matl` still has bolt/seat parts and “Connection …” delete labels |
| [DISC-019](discrepancy-index.csv) | 2009 slides: detailed LS-DYNA connection models vs released bulk MAT 24 |
| [DISC-028](discrepancy-index.csv) | Draft 2 says releasable 16-story ANSYS has no connection models; delivered gravity APDL still has column-element delete/copy steps |

## Prescribed edits (inspectable, not proof of intent)

| ID | What |
|---|---|
| [DISC-009](discrepancy-index.csv) | “Beams to decouple E&W Penthouse” (6 beams) |
| [DISC-020](discrepancy-index.csv) | APDL “Delete column elements below floor” |

## Not a mismatch until mapped

| ID | What |
|---|---|
| [DISC-008](discrepancy-index.csv) | 114,523 nodes above 300 °C; NCSTAR column prose is unlabeled here |
| [DISC-023](discrepancy-index.csv) | Slides say 200–300 °C at C79/connections; field max is 735.6 |
| [DISC-024](discrepancy-index.csv) | Fl07/09/11/13 are Core/SLAB-only (72 files); Fl08/10/12/14 are member-dense (2016). Not a mismatch until mapped |

## Production identity

| ID | What |
|---|---|
| [DISC-010](discrepancy-index.csv) | Six Sept files match Fletcher’s count/category, not his hashes |
| [DISC-014](discrepancy-index.csv) | Case B count/type mix now named: 96 `SLNo` + 173 `.nod` + 272 PNG + `mover` |
| [DISC-016](discrepancy-index.csv) | June non-delivery of LS-DYNA inputs |

## What the extra scan added

New since the first ten LS-DYNA rows: **DISC-011–023**. The same pattern appears in the June APDL/thermal/slides: include names that do not match delivered basenames, a Case B +10% variant with no A/C twin, a Floor-07 on/off split in `WTC7-1.int`, and slides that already described the instantaneous deletion handoff now visible in the Sept deck.

Phase 1 text-read every thermal member ≤2 KiB (23,713 files) plus a stratified header sample of large `.int` files. New rows: **DISC-024–028**. Floor 07 is commented in all 12 Case A/B hour drivers (pin correction to DISC-015). Case B’s extra 96 files are a live `SLNo` class. No new named include appeared beyond DISC-001/011/012.

Second sweep (2026-09-12): hashed all 8,364 shared A/B/C basenames; scanned 1,644 large `.int` bodies for `/input`/delete/hour comments; extracted the SRC-029 June letter PDF from the EML; read PNG text chunks. New row: **DISC-029** (Case B `1C137-2` is NULs). DISC-013/016 pins corrected. Large bodies added no new named include. PNG text chunks: none. A≠B≠C on most shared names is the three-case structure, not a new mismatch.

Remaining unread: PNG pixels; full BF/BFE numeric bodies beyond the include/comment hunt. That is a remaining gap, not a negative finding.

## Priority (what to keep in front)

See [README](README.md#definitely-note). Short version: for the case, keep the June omission, the named missing/unmatched files, the connection-material boundary, and the 2010/Case B count questions. For the investigation, keep the documented handoff, the one-sided 3.5 / 4.0-hour pair, and the June omission; treat +10%/`SLNo`/Fl11-13 only as follow-ups to the hour cut. Do not treat penthouse decoupling, hot unlabeled nodes, `mover`, or “hidden connections” as conspiracy evidence.
