# Scan gaps

Do not invent a `DISC-***` row from a failed read.

| Target | Blocker | Action |
|---|---|---|
| `ANSYS Thermal Data.zip:CaseB_Temps/INTFILES+10%14SEP07/WTC7-Fl08-1C137-2.int` (328 bytes) | Entire file is NUL bytes | Now DISC-029. Case A/C twins are ordinary BF TEMP cards |
| SRC-029 June 5 interim-letter PDF (`2024-000233-InterimResponse.pdf` inside the EML) | No standalone extract under `exhibits/raw/` | Second sweep decoded the MIME attachment to `/tmp/disc-second-sweep/` and used it to correct the DISC-016 pin. PDF was not copied into the raw tree |
| Full BF/BFE numeric bodies | Include/comment hunt done; temperatures not mapped to members | Incomplete thermal-physics scan, not a missing-file finding |
| 272 PNG pixels | Filename/count plus empty text-chunk scan | Folder name is `PNGFILES+10% 14SEP07`. No delete/hour in basenames or `tEXt` keys |

No other Phase 1 member failed to open.
