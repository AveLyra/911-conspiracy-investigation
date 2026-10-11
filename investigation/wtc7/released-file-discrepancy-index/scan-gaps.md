# Scan gaps

Do not invent a `DISC-***` row from a failed read.

| Target | Blocker | Action |
|---|---|---|
| `ANSYS Thermal Data.zip:CaseB_Temps/INTFILES+10%14SEP07/WTC7-Fl08-1C137-2.int` (328 bytes) | Contains a NUL byte; decoder flagged `binary_nul` | Listed unreadable. No DISC row. Neighboring `WTC7-Fl08-1C*` files in Case A/C are ordinary short `.int` text |
| SRC-029 June 5 interim-letter PDF (`2024-000233-InterimResponse.pdf` inside the EML) | No standalone extract on disk; Phase 2 did not decode the MIME attachment | DISC-016 already records that letter’s LS-DYNA promise vs June extract. Not re-opened here |
| Large SLAB / member `.int` bodies after 8 KiB | Streamed headers only (512 MiB cap unused; files are smaller but numerous) | Sampled headers are BF/BFE temperature cards with no `/input`. Remaining unread = incomplete scan |
| 272 PNG pixels | Filename/count only, per prompt | Folder name is `PNGFILES+10% 14SEP07`. No delete/hour in basenames |

No other Phase 1 member failed to open.
