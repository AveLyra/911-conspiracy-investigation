# Job 1854 independent derivative check

Final receipt, October 4, 2026 America/New_York / October 5 UTC.
Derivation passes: five actual renderer processes, 15 full-page PNGs, all
exact-byte matches. All 31 declared preserved files match root scratch
(the initial 30-file set plus the subsequently preserved font configuration).
Root reported both readers closed all 15 initial pages with zero repeats;
the final declared raster set is the 15 independently checked files below.

## Scope and controls

Only this receipt and private scratch were written. No source or image content
was viewed or extracted; no network, OCR, crops, source edits, reader-note
inspection, main/legal edits, or Git/engine actions occurred. Complete main
AGENTS, WORKFLOW, START-HERE, investigation CHARTER, this PROTOCOL, and PDF,
source-of-truth and evidence-falsification skills were read. The skills kept
source integrity, shared-renderer reproducibility and historical truth separate;
the assigned no-content-view boundary controls over generic visual QA.

Protocol SHA-256: `0387668356299df071a0bdc93f53748f387a3a31b1dc48a0973f30de75261618`.
Control hashes were checked in receipt `5aa1d7`, exit 0. Protocol reread:
`5c2136`, exit 0. No frozen note was changed.

Paths used below:

```text
J=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/generator-job1854
R=/private/tmp/wtc7-job1854.wS8WnU
T=/private/tmp/job1854-derivative.jYXKX0
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
```

## Sources and environment

`mktemp -d /private/tmp/job1854-derivative.XXXXXX` created T; `P -v`
reported Poppler 26.05.0. `shasum -a 256` and `wc -c` on the five exact
`R/NYC-WTC_000<ID>.pdf` files matched admission before rendering (`83b33c`,
exit 0) and their hashes remained unchanged afterward (`808eb4`, exit 0).

| ID | Bytes | Physical pages | SHA-256 before and after |
|---|---:|---:|---|
| 171252 | 172757 | 3 | `5185f82a6b8f15b4db8999924abe9897496076bf2936f995fcfa7e83d1ce8473` |
| 172389 | 172163 | 3 | `195af40f88f1dd217caee055b379958abc8a4f0dd06d28e00a775dd325a63b29` |
| 172539 | 171315 | 3 | `e4d75191b064c94ebe6687077cf3b9c7030e3b43a0c34e161c77abf50deffe0b` |
| 172543 | 169718 | 3 | `aa2ec772603711f97829bcbf85e03f1dcf13631ed68e81439d9c79154b6cbde8` |
| 174096 | 169639 | 3 | `4a8e51ca1df5d595c982491e012beb3c305017bf865727915f4e9e03bfabae24` |

Total source bytes: 855592. Bundled Python 3.12.14 / pypdf 6.10.0 preflight
(`7516ba`, exit 0) checked the first five bytes for `%PDF-`, exact sizes,
`len(reader.pages)`, `reader.is_encrypted`, and presence of `/AcroForm`,
`/OpenAction`, `/AA` in the root catalog. All five were three-page PDFs,
unencrypted, with none of those catalog entries; no captured pypdf warnings.
This is a basic admission check, not an exhaustive active-content/security audit.

T/fonts.conf was created via apply_patch; T/font-cache was explicitly created
before rendering. Both configs list `/System/Library/Fonts` and `/Library/Fonts`.
`diff -u R/fonts.conf T/fonts.conf` (`dfdf5f`, expected exit 1) showed only
the cache path changed, from R/fontcache to T/font-cache. Config hashes
(`e132be`, exit 0):

- Root: `2ae7b440eb408d3f6946295f5f21aa0de9b24ca1d7bc10f192d6e14267f56d4a`.
- Independent: `3a8eb8d4d08d9aff22cca0faa99062f57dbc5e57d472b6832ce910af941cf8f4`.

## Actual independent render executions

The following command was expanded once for each ID in the source table, with
the absolute path substitutions above; five processes, not 15. The Python
subprocess wrapper recorded UTC start/end, monotonic elapsed time, exact
expanded command, return code and wrapper streams to `T/<ID>-receipt.json`.
Original process handles were polled to terminal; none was restarted.

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 3 -png -scale-to 2400 \
  "$R/NYC-WTC_000<ID>.pdf" "$T/NYC-WTC_000<ID>" \
  >"$T/<ID>.stdout" 2>"$T/<ID>.stderr"
```

All timestamps below are 2026-10-05 UTC. All five renderer and wrapper exits
were 0. Wrapper stdout/stderr were empty.

| ID | Handle | Terminal receipt | Start | End | Monotonic seconds |
|---|---:|---|---|---|---:|
| 171252 | 99578 | `1dd6fd` | 01:31:06.960244 | 01:31:34.281704 | 27.350177 |
| 172389 | 2723 | `74bb48` | 01:31:07.110609 | 01:31:35.250882 | 28.169197 |
| 172539 | 42432 | `aadac6` | 01:31:06.801508 | 01:31:32.372713 | 25.599651 |
| 172543 | 60548 | `42c99a` | 01:31:06.761371 | 01:31:32.269544 | 25.514756 |
| 174096 | 28518 | `0912e8` | 01:31:06.966695 | 01:31:33.549021 | 26.610886 |

Saved JSON receipt hashes, checked after completion:

| ID | SHA-256 of T/ID-receipt.json |
|---|---|
| 171252 | `d29cdd5aaacfbf26dee11550952f782ede09d46a1a2776a1121fa8bae3a6b985` |
| 172389 | `c5d6a741608ebfbed4ca1451ea186ed8ca78ef4e625faefb69245b5ebdc6b304` |
| 172539 | `83a0a37c021eb5a4232f70e6cc51c0971e5db580568fa021c51e33100a2d6ad7` |
| 172543 | `97abed659b854e7a16f3ed230df45d1002b70d7677848b8759d4cbf9fbf76f01` |
| 174096 | `5b094acf673b8fc92f1cdb11d76f89a7d26efbbb28b517f844dcf0a12f91af6d` |

`wc -c` and `shasum -a 256` verified all ten independent `<ID>.stdout/.stderr`
files and all five root `NYC-WTC_000<ID>-render.stderr` files: each zero bytes,
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No renderer diagnostic warning was emitted. Root renderer exit-0 status was
provided by root; this checker directly verified its own five actual exits.

## Complete initial-raster comparisons

Actual filenames were first discovered with bounded
`rg --files --hidden --no-ignore -g '*.png' R` (`ba020a`, exit 0).
For each ID and physical page 1, 2, 3, commands were:

```sh
cmp -s "$T/NYC-WTC_000<ID>-<page>.png" "$R/NYC-WTC_000<ID>-<page>.png"
shasum -a 256 "$T/NYC-WTC_000<ID>-<page>.png" "$R/NYC-WTC_000<ID>-<page>.png"
wc -c "$T/NYC-WTC_000<ID>-<page>.png"
file "$T/NYC-WTC_000<ID>-<page>.png" "$R/NYC-WTC_000<ID>-<page>.png"
```

Complete check `808eb4` exited 0: all 15 `cmp` statuses 0, both hashes and
header dimensions equal for every pair; 15 PNGs in each directory, 2004811
PNG bytes per set. Dimensions below are saved PNG header geometry, not a
claim about any reader's displayed image. All are RGB, 8-bit, non-interlaced.

| ID-page | Width × height | Bytes | SHA-256, both full files |
|---|---|---:|---|
| 171252-1 | 1782 × 2400 | 145245 | `d0c8a06cfb23ee0aa586e986318cbc5b273e4694f7fb68bcd1b779dde583512a` |
| 171252-2 | 1787 × 2400 | 142641 | `2a5b106986f44970435c0ce19ba9c6f7bb1c5dfe0217a147a19975efc4df5d9c` |
| 171252-3 | 1793 × 2400 | 116823 | `a830b71a84dfce765849d389a9476da13156bf486e13ae47bfbc3e5c1f9fc1c2` |
| 172389-1 | 1783 × 2400 | 143888 | `4aa7a2d09fa517c2a2bcf79f2874a9eb5c703236b2a14322d80bac6e20ce2c8b` |
| 172389-2 | 1789 × 2400 | 139852 | `9311f500c6fec9f60fb9e6d7bf02a2c660810d0be98c95de94d53db617a18304` |
| 172389-3 | 1776 × 2400 | 114806 | `816d0dfa9af8b3f64490dc039e90ed5ba499fbb21daaa04de6d3895feb29a512` |
| 172539-1 | 1783 × 2400 | 145103 | `243ac5df23cb0e90083b32573b9a0c455c9ace00c7ce3720e05e2ceece690bc0` |
| 172539-2 | 1788 × 2400 | 140358 | `82a0d8ddd156ce78bbd589802c0861a26ae1e30f8b2c5fd0e749474049347cf7` |
| 172539-3 | 1784 × 2400 | 115392 | `02c86755a07256a5a7b7efa3252ede4c12081cb3a974789677a691669cfd830b` |
| 172543-1 | 1782 × 2400 | 143346 | `3565045903234c92045931351a5ecfc700f0c315ea7c18b2f27ec2b07410b89e` |
| 172543-2 | 1789 × 2400 | 140967 | `ef98b9133baddf9dd59630497156799274d8fd4893cea2969798fe860fec3790` |
| 172543-3 | 1787 × 2400 | 116062 | `132f8fb8602f9a2725ffb2acc2969d8d726c4e93e7062b42cf2f1a339db115ce` |
| 174096-1 | 1779 × 2400 | 144215 | `36fc57192a8c3b4252e1232a3b9c5f571daf9dac8fd933d1bc5263bdf286831f` |
| 174096-2 | 1787 × 2400 | 140350 | `0a8d1dcc124478bb97a2d23da02b8f75d496bb851f96f7654d868ecfc7f5355d` |
| 174096-3 | 1784 × 2400 | 115763 | `b2441a83151ddbd1e72a58007f3e9716f93d6ddc65d68276d2756b3b94b3ec80` |

## Preserved-copy checks

After root's copy-ready notification, bounded `rg --files --hidden --no-ignore`
with only `*.pdf`, `*.png`, `*.headers`, `*.stderr` and `fonts.conf` filename
filters found the declared 30 files in J (`4f05b5`, exit 0). Root reported
`cp -n` receipt `d798a0`, exit 0; that execution belongs to root, not this
checker. No J/fonts.conf was present in that initial copyset; its subsequent
preservation and separate check are recorded below. The exact private
cache-path-only difference between root and independent configs remains above.

The independent 30-pair comparison (`da03ca`, exit 0; started
2026-10-05T01:35:33Z) expanded the following commands for IDs 171252, 172389,
172539, 172543, 174096 and suffixes `.pdf`, `.headers`, `-render.stderr`,
`-1.png`, `-2.png`, `-3.png`:

```sh
cmp -s "$J/NYC-WTC_000<ID><suffix>" "$R/NYC-WTC_000<ID><suffix>"
shasum -a 256 "$J/NYC-WTC_000<ID><suffix>" "$R/NYC-WTC_000<ID><suffix>"
wc -c "$J/NYC-WTC_000<ID><suffix>" "$R/NYC-WTC_000<ID><suffix>"
```

All 30 `cmp` statuses were 0, both hashes and sizes matched for each pair,
and the check recorded zero failures. The five preserved PDF pins and fifteen
PNG pins/byte counts equal their tables above. All five preserved diagnostics
are zero bytes with the empty-file hash already recorded. The five headers
were compared only as opaque bytes, not parsed for substantive or historical
authentication claims:

| Header ID | Bytes | SHA-256, both copies |
|---|---:|---|
| 171252 | 514 | `f3dd9f2174e089fd63f1a0a3127a2cd803fd6d10201823f42ddfe3b7115796f3` |
| 172389 | 514 | `2e61968ccdefc7a8962fae20fe01597769b3982b3d766c15c215f295abe2dadb` |
| 172539 | 517 | `50cc12d468dd32675868ed4b085f113883cce41e3bffdb395f1b309d11f203b0` |
| 172543 | 514 | `e0d55785f92ac41c9d8a93686025a74749a7924c0d0edd41c2ff06d96fb84843` |
| 174096 | 514 | `5edbf72eb91ad2757bd2e9d9d6df6361c11dbc335df0f2344eef2ad541d0916d` |

After the initial 30-file check and receipt freeze, root reported preserving
`fonts.conf` with copy receipt `989831`, exit 0. The specifically requested
31st-pair check (`2e9761`, exit 0; 2026-10-05T01:38:14Z) ran:

```sh
cmp -s "$J/fonts.conf" "$R/fonts.conf"
shasum -a 256 "$J/fonts.conf" "$R/fonts.conf"
wc -c "$J/fonts.conf" "$R/fonts.conf"
```

The comparison status was 0; both files were 219 bytes with SHA-256
`2ae7b440eb408d3f6946295f5f21aa0de9b24ca1d7bc10f192d6e14267f56d4a`,
matching the previously recorded root config pin. The current preserved-copy
coverage is therefore 31 pairs: five PDFs, fifteen PNGs, five headers, five
renderer diagnostics and one font configuration. This supplement preserves
the initial 30-file pass and failure history; no renderer or other check was
repeated for the added file.

Current byte equality does not independently prove the historical copy method
or a no-overwrite guarantee. No copy operation was performed by this checker.

## Retained failure and coverage closure

The first comparison loop (`d82248`, exit 1) stopped at assignment to zsh's
read-only variable `status` before it printed any comparison result. That
attempt provides no complete comparison coverage. Only the checker variable
was corrected to `taskCmp`; the entire bounded comparison was then run as
`808eb4`, exit 0, zero recorded failures. No renderer was restarted and no
PDF or raster changed to obtain agreement. The expected config-diff exit 1
above is a reported path difference, not a rendering failure.

Root subsequently reported that both readers froze 15 of 15 initial page
notes and used zero repeats; no further raster was requested. These are
attributed reading-status reports, not this checker's primary content readings.
Root/peer notes were neither read nor independently hash-checked here. The
complete declared derivative coverage is five processes / fifteen 2400-pixel
maximum-dimension full-page rasters, not fifteen renderer processes.

## Limits

Exact agreement supports local reproducibility under the same Poppler version
and system fonts with independent caches. It does not independently establish
historical authenticity, acquisition chain, content truth, equipment performance,
engineering validity, independence of repeated documents, reader display
geometry or human acceptance. A shared renderer defect could reproduce exactly.
Hashes are integrity pins, not historical provenance proof. Basic PDF flag checks
are not a full security audit. Scratch is retained; no files were deleted.
