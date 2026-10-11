# Generator service independent derivative check

Final receipt, October 4, 2026 America/New_York / October 5 UTC. All
three independent renderer processes exited 0, all twelve initial PNGs match
root bytes/dimensions, and all 31 declared preserved pairs match scratch.
Root reported both twelve-page records frozen with zero repeats; coverage is
closed at twelve rasters. Root's delayed final-note save, the initial
transport-check schema error and the producer's failed DNS attempt are retained.

## Scope and controls

Complete PROTOCOL and PDF skill read; current main AGENTS, WORKFLOW,
START-HERE and CHARTER hashes rechecked unchanged (`ed624b`, exit 0).
Complete repo-orchestration, source-of-truth and evidence-audit skills read
(`2175e7`, exit 0). They preserve the separation between source integrity,
local reproducibility and historical inference. Existing delegated scope
controls over broader intake or generic visual QA: no new Git/intake scan,
semantic PDF/image viewing, OCR, crops, network, reader-note inspection,
main/legal edits or engine actions. Only this note and private scratch were
written. No raw headers, cookies or personal contacts were printed.

Protocol SHA-256: `f4382a916a2a8a995c9002f4d62871ff9d42f33275ee712ccfb641c7405df479`.

```text
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/generator-service-review
R=/private/tmp/wtc7-generator-service.kVejEX
T=/private/tmp/generator-service-derivative.rYiNUn
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
Y=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

## Source admission

No source polling occurred before explicit readiness. Bounded filename
discovery used `rg --files --hidden --no-ignore` for the named source,
derivative, transport and config suffixes. `mktemp -d
/private/tmp/generator-service-derivative.XXXXXX` created T; `P -v` reported
Poppler 26.05.0 (`9f0c70`, exit 0).

A stdout-only `Y -` check (`bfbd02`, exit 0), Python 3.12.14 / pypdf 6.10.0,
checked exact byte lengths, SHA-256 against the supplied pins, `%PDF-` magic,
`len(reader.pages)`, `reader.is_encrypted` and root catalog `/AcroForm`,
`/OpenAction`, `/AA`. All three passed with no captured pypdf warnings.
They are unencrypted with none of those catalog entries. This is basic
admission, not an exhaustive active-content/security audit.

| ID | Bytes | Physical pages | SHA-256 before and after render |
|---|---:|---:|---|
| 172371 | 101266 | 2 | `a86f55c98227e46108d0691b0faff79c1cde6eac5ee4e3ce0abea1c51376532b` |
| 172958 | 397072 | 9 | `8b34d8275b5612f758f9ec411124e58295739df17b0b87adbced82b5bb647875` |
| 168654 | 73353 | 1 | `7b9824f021e7f38cc80465c8fb7b7499dde90b278831c6d16976655eba960e05` |

Total source bytes: 571691. After-render `shasum -a 256` checks (`2c0cc4`,
exit 0) match all before pins. U PDFs equal R through the full-copy check.

## Independent render configuration and receipts

T/fonts.conf was created via apply_patch and T/font-cache explicitly created
before rendering. Both root and independent configs list `/System/Library/Fonts`
and `/Library/Fonts`; only the private cache path differs, R/fontcache versus
T/font-cache. Hash plus `diff -u R/fonts.conf T/fonts.conf` receipt `2ad832`
ended with expected diff exit 1, showing that one cache-path difference:

- Root/preserved config, 229 bytes: `51c2c90d7ccb06d7de79963a665646e19f3ebc84568956ab039499bba3bf67bd`.
- Independent config: `f556762b50a6d3f2a09f8ce8df9477dbb5b4bee0aa5d101715250919fc750484`.

The following command was expanded once per ID, using `<last>` = 2, 9, 1
respectively and the absolute substitutions above. Each Python subprocess
wrapper saved its exact command, UTC start/end, monotonic elapsed seconds,
actual renderer return code and wrapper streams in `T/<ID>-receipt.json`.
Original handles were polled to terminal; no renderer was restarted.

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l <last> -png -scale-to 2400 \
  "$R/NYC-WTC_000<ID>.pdf" "$T/NYC-WTC_000<ID>" \
  >"$T/<ID>.stdout" 2>"$T/<ID>.stderr"
```

All three actual renderer/wrapper exits were 0; wrapper streams were empty.
UTC timestamps below are 2026-10-05. Three processes produced twelve pages.

| ID | Handle | Terminal receipt | Start | End | Elapsed seconds |
|---|---:|---|---|---|---:|
| 172371 | 11009 | `d6b7a2` | 03:02:36.912447 | 03:02:46.131132 | 9.218436 |
| 172958 | 60577 | `bfc002` | 03:02:36.872657 | 03:02:59.190332 | 22.307487 |
| 168654 | 91737 | `56e229` | 03:02:37.072540 | 03:02:44.053346 | 6.980610 |

| ID | Saved JSON receipt SHA-256 |
|---|---|
| 172371 | `98c6a094127f1b3c3d4ef93e26afeb849a5fbaf1b4cb3160b0a44ac80a8c3700` |
| 172958 | `6927baa4017f0d7b2484d5632c6e4f68367af16d293767221c96273b37e4776b` |
| 168654 | `bb26721636e4915a8577fa777ec1d9dddbc3b0e30d4fe4689b2d8f7eb244eabb` |

All six own `<ID>.stdout/.stderr` files were checked with `wc -c` and
`shasum -a 256`: zero bytes, empty-file SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No renderer warning was emitted. Root's three acquisition and three renderer
stderr files are also empty and exactly match preserved copies.

## Twelve initial PNGs

For every exact full filename represented below, the checker ran
`cmp -s T/name.png R/name.png`, `shasum -a 256 T/name.png`,
`wc -c T/name.png` and `file T/name.png R/name.png`.
Receipt `de0e84`, handle 10698 to terminal `2c0cc4`, exit 0: all twelve
comparisons 0 and both header dimensions equal, twelve PNGs in each set.
All are RGB, 8-bit, non-interlaced. These are saved PNG dimensions, not
certification of displayed image geometry or semantic legibility.

| ID-page (NYC-WTC_000 prefix) | Width x height | Bytes | SHA-256, both files |
|---|---|---:|---|
| 172371-1 | 1786 x 2400 | 168000 | `b016f68563e2dd8eed108472f968a8eafbbc7663be518bfeb89c9b7bf71c0b85` |
| 172371-2 | 1795 x 2400 | 81363 | `f581836e8e872295a6132e3edb7176781910ad4dbfdf595b163b8379c759f5d4` |
| 172958-1 | 1783 x 2400 | 102015 | `2a9768ee0956d311ef8e094529ac1de19df81aa39dce8f3d8fac311de63512b7` |
| 172958-2 | 1784 x 2400 | 143761 | `a66a0c1251ba351fcbf3b815adc2f05b85b46421095fae284cad956b32f42899` |
| 172958-3 | 1783 x 2400 | 174750 | `d1e1dc549648b6c22cadc7de5f6b207fd6991afa5666f5e0d2a9e2e936e01765` |
| 172958-4 | 1782 x 2400 | 148582 | `7833a7188f54a00df09766db90673472ba146ef7051925cd06d198c974ab24ce` |
| 172958-5 | 1784 x 2400 | 182719 | `aae89021cec62f48f6b6c932326a2ae5104eadff23eb23a07b0ec7c225b4f5b4` |
| 172958-6 | 1784 x 2400 | 189846 | `4035b79c8ae10e7b7ce576a3203dd542bcfaeeab58e24be9cb1adfb8b1512da0` |
| 172958-7 | 1781 x 2400 | 64211 | `5f28df20c88979b4f34d949cd2d9a15b680aed0796a2489560dc10323933d01d` |
| 172958-8 | 1783 x 2400 | 107988 | `3350375b3d62e1b19c5301feb247084adbf77263c9f786b60874f5c427b32c38` |
| 172958-9 | 1792 x 2400 | 143305 | `90de60b93bf9ef6f9ccba63c26c96019ecc15e0556c55fb8504db0e14fc1925c` |
| 168654-1 | 1754 x 2400 | 156455 | `93460f6c1aa32b925603bd9a43df50ee3ab4932c2bb5a1ab6e01c307a7fa6d04` |

## Complete preserved-file comparisons

At 2026-10-05T03:02:59Z the checker ran `cmp -s U/name R/name`,
`shasum -a 256 U/name`, `wc -c U/name` for each ID with suffixes `.pdf`,
`.headers`, `.transport.txt`, `.stderr`, `-render.stderr`; the twelve PNGs
above; `fonts.conf`; and all three `172371-sandbox` files below.
Receipt `5d7a8a`, handle 36516 to `512084`, exit 0: 31 pairs, every comparison
0, zero failures. This covers the three source pins, twelve PNG pins, root
config, six empty diagnostics and following transport/failed-attempt pins.

| ID | Header bytes | Header SHA-256 | Transport bytes | Transport SHA-256 |
|---|---:|---|---:|---|
| 172371 | 514 | `8e74c01bd247ad47e79bc8d9c4548b40824895e1660f08db5997b0db2a9cb7d6` | 100 | `baa9f807452e5821e61bdd6e07e52c22012c82473d74d31fe3b62adc50fcb43d` |
| 172958 | 517 | `4a7c6a5c5294d16ce964d381b91dcb8263349a924ec147aca21143e4fba711f2` | 100 | `cf5a55819619144abaaaa0904773f63eba337d8efe6af27b54d60a3a486b7810` |
| 168654 | 515 | `c753a40aab54f3ff6515906d91e0c2a37e1c79a3f8e0d7ae98d1e649f32e57bd` | 99 | `d19a095dc5b7bfd5953538f859ac78bd9a0b0e558de34cf8fa169281ef1e7436` |

All full headers remain local-only; no raw header output or sanitizing rewrite.
Allowlisted stdout-only `Y -` transport/header validation, after the retained
schema correction below (`ec4b08`, exit 0), verified exactly six stored log
keys: http_code, bytes, content_type, redirects, time_total, curl_exit. All three
successful logs record HTTP 200, application/pdf, zero redirects, curl exit 0
and exact actual PDF bytes. Each header set has exactly one 200 status,
matching Content-Type and no Location header; successful stderr is empty.
Stored time_total seconds are 0.964136, 1.041148, 0.918410 in source-table order.
These are held producer measurements, not new acquisitions by this checker.

| Failed-attempt file | Bytes | SHA-256 |
|---|---:|---|
| 172371-sandbox.headers | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 172371-sandbox.transport.txt | 80 | `8a9ac53aff542e55fd7e68f3e28651646fd55cf4792d99270ac5e30ef8a8d01a` |
| 172371-sandbox.stderr | 67 | `02a2b254dd32ec6b50259755356a72c28e89ce3fc3d52329aa73c219c559b7e5` |

The failed attempt records http_code=000, curl_exit=6, bytes=0, empty
content_type, redirects=0, time_total=0.004668, with a DNS-failure marker
in stderr and empty headers. This was checked without printing raw stderr
or headers. It remains a failure, not a response or evidence of server refusal.

## Retained checker failure, coverage closure and limits

The first transport validation (`b6a5a6`, exit 3) incorrectly expected this
unit's HTTP field to be named `http`, as in an earlier unit. It reported three
failed transport checks although other emitted header/byte/diagnostic facts
were consistent. Bounded field-name inspection (`dbdd60`, exit 0) established
the actual `http_code` key and numeric values, without raw-header output.
Only that checker mapping was corrected; `ec4b08`, exit 0, reran all three
success-log checks, exact key-set validation and the failed-attempt checks.
No PDF, transport, header, raster or renderer was changed or retried to obtain
the pass. The expected cache diff exit 1 is distinct from this checker failure.

Root reported its renderer terminal receipts `880cd4`, `eb7198`, `9140a0`
all exit 0; these are attributed producer receipts. This checker directly
verified its own three actual renderer exits. Current byte equality does not
prove the producer's historical copy method/no-overwrite execution or
independently authenticate acquisition.

The existing provisional receipt was read completely on resume (`43a277`,
exit 0; then-current SHA-256
`fc74984d24cffc6a3f7d50682b03280295619a71c6e8bceb474693d86d13e5c8`).
Only closure wording was finalized; no renderer, source read or physical
validation was added, and all original results and failure history remain.

Root explicitly reported both twelve-page records frozen with zero repeats,
with root-note pin
`ec4666b3c6cc3ab6d24834fa1a0d11556678f21a18b743b66d42460c8fb8f55c`
and observer-note pin
`d44537b0537aecd5d46cb50458017e2cfbb1c950ab2f46cf6c9a60c37e7dbdbd`.
It also reported that root's final note 12 was saved late from a retained
contemporaneous observation after context interruption and the user's
coordinate turn. The first eleven root notes were saved before the next view;
no new image or peer substantive findings were read in the intervening period.
These are attributed closure/timing reports, not independently checked note
pins or primary observations by this checker. Reader notes were neither read
nor hash-checked here. This receipt does not claim zero root note-save delays.

No larger raster was requested. Final derivative coverage is three actual
renderer executions, twelve 2400-pixel-maximum full-page rasters, and 31
preserved-file comparisons. Shared Poppler/system-font defects can reproduce exactly.
This establishes local derivation and copy integrity, not historical truth,
source-family independence, contractual performance, equipment continuity,
installed/event-day conditions, engineering/causal validity, reader display
geometry or human acceptance. No file was deleted or silently sanitized.
