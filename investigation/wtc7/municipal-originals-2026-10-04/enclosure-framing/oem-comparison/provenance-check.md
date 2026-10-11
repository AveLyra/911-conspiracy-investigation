# OEM comparison provenance check

2026-10-04. Research only. Fresh integrity checks matched the declared source
PDF, all three original/reproduction PNG pairs, and the exact corresponding
entries in the saved reproduction receipt. No renderer ran in this check.

## Scope and checked artifacts

Read this unit's complete `PROTOCOL.md`, SHA-256
`d90c185f2d39ef527677e2302cf586d57de76b276540dafa37226c177fb9e905`.
Previously read current main instructions remained applicable; the main
`AGENTS.md` and `WORKFLOW.md` hashes were reconfirmed unchanged. Acceptance:
source size/pin, both copies of physical pages 59-61, exact receipt entries,
dimensions/status fields, and byte equality. No page-content inspection,
network, OCR, fresh rendering or source interpretation was performed.

All source reads used this base directory:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup`.

| Artifact | Freshly verified result |
| --- | --- |
| `sources/ncstar-1-1j-attempt02.pdf` | 578804 bytes; SHA-256 `7b1fe2a7a94a67c54fdaabe27e3309b439551512cff97e5026e0b62bb51bf623` |
| `root-reproduction/receipt.json` | SHA-256 `8dad5cf679a7ab1e2b476bf7a9ca6fa51a3ed4db99465365996c21c064802147` |

The source size and hash equal both the assigned pins and the receipt's
`source_bytes` / `source_sha256`. The receipt declares `source_pages: 84`;
this was checked as a receipt field, not a fresh PDF page-count measurement.

## Actual verification and outcomes

`wc -c sources/ncstar-1-1j-attempt02.pdf` returned 578804 (`a64bf8`, exit 0).
The following hash command was run from the source base and returned all
matching pins (`4429b2`, exit 0); it also reconfirmed the earlier checks
(`a64bf8` / `36be45`, both exit 0):

```sh
shasum -a 256 sources/ncstar-1-1j-attempt02.pdf root-reproduction/receipt.json root-derivatives/p59.png root-derivatives/p60.png root-derivatives/p61.png root-reproduction/p59.png root-reproduction/p60.png root-reproduction/p61.png
```

`file` was invoked on those six PNG paths (`36be45`, exit 0). Every file's
header reported 1700 x 2200, 8-bit/color RGB, non-interlaced. No image was
visually opened. An explicit loop over 59, 60 and 61 ran
`cmp -s "root-derivatives/p<page>.png" "root-reproduction/p<page>.png"`,
recording every status (`bfa065`, exit 0): three checked pairs, zero failures.

| Physical page | SHA-256 of both PNG copies and both receipt hash fields | `cmp` exit |
| --- | --- | --- |
| 59 | `880960ccfc33489160eeeda73d9900d77977b3ff58c459042826c1db13b25250` | 0 |
| 60 | `8abc1a82fa2ecf87b58bfa34ff531fb8fd19af1fedfe72e5b78492cf6641c798` | 0 |
| 61 | `c0577e09891e1cc0b6607dbc35093f34142c3208f045f6fdacc09f405892594f` | 0 |

The 402-line receipt was read completely. A `jq -e` assertion check returned
`true`, exit 0 (`d2503c`). It checked the exact source pin/size, receipt
`source_pages == 84`, `all_pass == true`, and an exact selected-page list
`[59,60,61]` (so no missing/duplicate selected entries). For every selected
row it checked both SHA-256 fields against the assigned page pin,
`dimensions == [1700,2200]`, `identical == true`, both
`original_stderr_bytes == 0` and `reproduced_stderr_bytes == 0`, and
`text_identical == true`. The PNG header dimensions independently agree.

Fresh checks were recorded on October 4, 2026, with UTC timestamps 14:47:35
and 14:48:53. There were no comparison failures, retries or discarded results.
Only this new worktree note was written; sources, receipt, images and other
WIP remained read-only and their checked pins did not change.

## What this establishes and does not

The receipt records an earlier reproduction; today's work verifies continued
agreement of its source/page pins and the held original/reproduction bytes.
The receipt's `text_identical`, zero-stderr and `all_pass` values are historical
status assertions. Text files and the receipt's other page rows were not
independently tested today. This receipt does not supply a renderer exit code,
so no historical terminal exit status is inferred merely from zero stderr.
No new renderer execution or renderer-status verification is claimed.

Agreement supports the local provenance chain for these three images. It
does not authenticate the historical records or their underlying drawings,
validate content interpretations, or establish installation or event-day
conditions. No canonical promotion, human acceptance, transmission, staging,
commit or push occurred.
