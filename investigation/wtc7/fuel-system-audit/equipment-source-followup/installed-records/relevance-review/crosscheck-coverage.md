> **Redacted historical receipt:** This copy omits one absolute local executable path. Original receipt SHA-256: `3d35fa34940ecbacbb6b3840c78b0aafafd967df13ce3438e3124566fdcd26da`. It reports checks performed on 2026-09-11; they were not independently rerun for this publication. The original receipt and source media remain in retained local storage.

# Eight-page crosscheck coverage and receipt

Completed 2026-09-11 after the separate [prospective selection](crosscheck-selection.md). No optional OEM-page extension was taken.

## Exact identities

All paths here are relative to `fuel-system-audit/equipment-source-followup/installed-records/` unless otherwise stated.

| Artifact | Independently recomputed SHA-256 |
|---|---|
| `sources/testimony-sept8-2006-attempt02.pdf` | `999b33d6256b64ca66596fac4346831180a072aa677ed9623c1dfb48c7c17029` |
| `sources/briefing-nov19-2008-attempt02.pdf` | `b8845c40205a4731d248b6398858dfabedbb927e01f8d6acd1422b40f2fa4850` |
| `run01/receipt.json` | `855d8e5f0831ea510238c35c4230ae62e93c52f3a9a2f0ac87a5c55b0e6dd587` |
| Root `report.md` reviewed snapshot | `9ab966268fcff180c3b6e63cd235ded1c17620ffa117a31fe6e1688e7146aab8` |
| Unchanged initial `relevance-review/report.md` | `a73606443e106890875d5fd5a5a3bd7abc72c12b77938f880fae4de21fb00729` |

The source hashes match root's prospective identities and the receipt. The receipt reports 21 testimony pages and 106 briefing pages; only the eight pages below were read. Original acquisition date/HTTP custody and the rest of each PDF were not reviewed. Hash agreement concerns acquired-byte integrity, not independent historical authenticity.

## Complete page coverage

Each complete page image and its complete text aid were read. Figure/table labels, footnote 52, footnotes a/b, headings and page/slide numbers were retained. Text aid alone does not expose the labels inside briefing slide 15's diagrams; the image supplied those labels.

| Source and physical page | Printed page/slide | PNG SHA-256 | Text-aid SHA-256 |
|---|---|---|---|
| testimony 4 | No printed page visible; final public remarks | `2dae5cae4a09a7fd2632078a2914b8162d2074f7d09ee8bd8b73aa83583bdda5` | `307acd84c1ef1f6b6f87ab5934c944fb5142f06636878115a77a3c2fe2db551e` |
| testimony 8 | NCSTAR 1-1 printed 177 | `ab6c87de542944aeec6cd603adc235639526f5cbb8158b4a34025fcfb7d5bc5b` | `719def95a9e1e694eacf99d6d3525bce70386335b2418747bac83cfbcebb6a4a` |
| testimony 11 | NCSTAR 1-1 printed 180 | `782aee3827dc64b0e2a42ed014ed2450865cbd1219dba8483cf5e8e371ce03ac` | `ec4b710712b55baf16b85306002a4fd607c117f47871a9173ad0ab170dd0fd6a` |
| testimony 12 | NCSTAR 1-1 printed 181 | `90777f829999b8fb8f06ee8d16512a2cb4e559511c390c2d4542773aae3e0ca6` | `1efd1a940c6b02aa6fe38076fcf92e1d8373697cdd11e156e7993b16c09e0284` |
| briefing 15 | slide 15 | `8355d850a054fff4da3a5d9ff444e178e6d6592937618aea90017b4c9bab49fa` | `efa2124f9ae3091839f823975086f72989bd74345c33217374fc88f2da0d6903` |
| briefing 16 | slide 16 | `4810f9d200eccd9190e6c59bbcf4f2129ad66392908d806eb0e4339311f96abd` | `9dc0bffefd729ac5e651ced64346a7e990c0430ea278de230093c71e7486b23f` |
| briefing 49 | slide 49 | `4fa3e251c3c8c1fe8a6654094b9606dc3571a9d49fb0233ac94eacceeb3a0099` | `f88036d090b8e6b3a31dbc168349097aa0eb32621912e3cb97fb0b90c13bb1c1` |
| briefing 50 | slide 50 | `a6d8f1c8a326ead66a931642ea5ca7ea0abb13aecc3dd4dd4b0cc9c0dd94620b` | `8b3a50673c94c3427f02016ecb6aaa65b4743792497ec882e417532800b5912e` |

Files use `run01/testimony-NNN.png/.txt` or `run01/briefing-NNN.png/.txt`. All 16 recomputed derivative hashes agree with their selected receipt rows. Testimony images are 1700x2200; briefing images are 2200x1651. The display reduced them to 1376x1780 and 1824x1368, respectively, with all page bounds visible.

The exact root receipt records this render command shape for the selected pages:

```text
[local executable path redacted] -f N -l N -singlefile -scale-to 2200 -png SOURCE OUTPUT_PREFIX
```

This reviewer verified hashes, metadata and complete visual content; the eight new pages were not independently re-rendered or re-extracted. That limit is distinct from the initial NCSTAR 1-9 review, whose 11 selected images were independently reproduced. Receipt metadata and selected rows were inspected; no raw acquisition logs or unrelated document contents were read.

No source was changed and no additional source was acquired. All new edits are additive working research inside `relevance-review/`; no confidential packet, external transfer, bridge/canonical write, solver run or research-to-case promotion occurred. The full 21/106-page PDFs, OEM physical 10/1J60 comparison, hearing cover material, original Langan report, original interview and installed/model records are outside this review.
