# Job 1854 follow-up independent derivative check

Final receipt, October 4, 2026 America/New_York / October 5 UTC. Six
independent render processes exited 0. All seven initial full-page PNGs match
root byte-for-byte and in saved dimensions. All 41 declared preserved file
pairs match scratch. Root reported both readers closed seven pages with zero
repeats and zero delayed saves; the seven-raster derivative set is now closed.

## Authority and boundaries

Complete PROTOCOL and PDF skill were read (`e2f9da`, exit 0); complete
repo-orchestration, source-of-truth and evidence-audit skills were read
(`6eb9a9`, exit 0). Previously fully read main AGENTS, WORKFLOW, START-HERE
and investigation CHARTER hashes were verified unchanged. The existing
delegated scope supplies the worktree/job boundaries; broader intake, Git
or content inspection was not added. These skills separate local integrity,
reproducibility, primary observations and historical inference.

Protocol SHA-256: `15290ac185a2a7831dc401d8e34e35ab9221bd6db68e2ccbd37329e5b9c85655`.
Only this note and private checker scratch were written. No source/reader-note
content view, OCR, crop, PDF edit, network, main/legal edit, Git or engine
action occurred. Raw headers were never printed, and no cookie was replayed.
Full raw headers remain local-only, not eligible for publication or push.

```text
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/job1854-followup-review
R=/private/tmp/wtc7-job1854-followup.hchlOL
T=/private/tmp/job1854-followup-derivative.lAme0a
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
Y=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
```

## Admission and source pins

After explicit readiness, bounded `rg --files --hidden --no-ignore` discovered
only the named source/derivative/diagnostic filenames. `mktemp -d
/private/tmp/job1854-followup-derivative.XXXXXX` created T; `P -v` reported
Poppler 26.05.0 (`ef6e7c`, exit 0). No sources were polled before readiness.

A stdout-only `Y -` preflight (`d9a2f1`, exit 0), Python 3.12.14 / pypdf
6.10.0, read each exact PDF as bytes, pinned SHA-256, checked `%PDF-` magic,
exact expected byte length, `len(reader.pages)`, `reader.is_encrypted`, and
root catalog `/AcroForm`, `/OpenAction`, `/AA`. Every check passed; no captured
pypdf warnings. All PDFs are unencrypted with none of those catalog entries.
This is basic admission, not an exhaustive PDF active-content/security audit.

| ID | Bytes | Pages | SHA-256, before and after rendering |
|---|---:|---:|---|
| 171251 | 64028 | 1 | `80680fc00c57f0920f0387ae1f87b71c40c34c254223c8fb44e467dce4818b4d` |
| 172976 | 67745 | 1 | `9528aa1900afa59334f516ff2e3e50a23cba4b92231a62e5cdb7d6df19729618` |
| 172977 | 60316 | 1 | `d6de130d5ebd7376bdfb142819458afd211562cfb024456c29be2f6973eda931` |
| 171520 | 44470 | 1 | `109b1447b5a64ca57f0fd9cacb4d45ec41cc76aa52b71a495e9a39528bcf7d26` |
| 174095 | 55156 | 1 | `732e42d9aff12e7536d9dfeda1d81f95ca7edf0f5c58d6b39bce5003ad894288` |
| 167866 | 114201 | 2 | `2558231620941df315322833fb001d78e6b633901e62acf5a3a0bfd5947107f4` |

All six after-render source hashes (`511320`, exit 0) equal these before pins.
Preserved U PDFs exactly match R as part of the 41-pair check below.

## Font configuration and actual render executions

T/fonts.conf was created with apply_patch and T/font-cache was explicitly
created with `mkdir` before rendering. Both configs use `/System/Library/Fonts`
and `/Library/Fonts`. `diff -u R/fonts.conf T/fonts.conf` (`41a798`, expected
exit 1) showed only the cache path differs: R/fontcache versus T/font-cache.
Config hashes (`d9a2f1`, exit 0):

- Root, also preserved in U (228 bytes): `98c7f9954bb5952d921e76be67f2c1d5846e84510c2152a3b373785c7e976bda`.
- Independent: `0b8cd91197d910863ebfc2b7bda9c98ba27f9fbbee4c69fac7fb51aae8526f04`.

The following command was expanded once per ID in source-table order, with
`<last>` equal to that PDF's page count and the absolute path substitutions
above. A Python subprocess wrapper saved the expanded command, UTC start/end,
monotonic elapsed seconds, renderer return code and wrapper streams in
`T/<ID>-receipt.json`. Original handles were polled to terminal, not restarted.

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l <last> -png -scale-to 2400 \
  "$R/NYC-WTC_000<ID>.pdf" "$T/NYC-WTC_000<ID>" \
  >"$T/<ID>.stdout" 2>"$T/<ID>.stderr"
```

Six actual processes, not seven; all six renderer/wrapper exits 0 and all
wrapper stdout/stderr empty. UTC timestamps below are 2026-10-05.

| ID | Handle | Terminal receipt | Start | End | Elapsed seconds |
|---|---:|---|---|---|---:|
| 171251 | 63869 | `5a8bd8` | 02:25:45.941035 | 02:25:55.455036 | 9.513660 |
| 172976 | 8535 | `9a5148` | 02:25:45.880855 | 02:25:55.917727 | 10.036637 |
| 172977 | 2510 | `9e7769` | 02:25:45.879171 | 02:25:56.906142 | 11.026207 |
| 171520 | 48988 | `21e8cb` | 02:25:46.164121 | 02:25:54.171062 | 8.006735 |
| 174095 | 52179 | `8af0f3` | 02:25:46.330877 | 02:25:56.525869 | 10.192165 |
| 167866 | 65630 | `a2c7cd` | 02:25:47.437015 | 02:26:00.071570 | 12.634290 |

Receipt JSON pins, checked after completion:

| ID | T/ID-receipt.json SHA-256 |
|---|---|
| 171251 | `26bcb92f41e63887c85148cb7339bfe7d1e223d0bdf0d4b484a038a0197caf50` |
| 172976 | `2475e8ca69ec36e347513a21704c9650bba1335890541c8fcf25ddf22b1289e1` |
| 172977 | `9db034a21fea1b41c8ca9f1e7cf53ac4dd4da638202d8dff71b193e1815cf220` |
| 171520 | `5f3180b265aa3bfd60c633a37583ac9e8e6f23d678833dece26b4a60e8201f2a` |
| 174095 | `4e8ccd9834248c9b7fe6d6eac63abccea1d2c404fb723f3ebac8f4d119382656` |
| 167866 | `f83ef8733e4ba9b1b805999345a59dc56ee915bbbfa6f46fe8a865369fc4f354` |

`shasum -a 256` and `wc -c` verified all twelve own `<ID>.stdout/.stderr`
files are zero bytes, SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No independent renderer warning was emitted. The twelve preserved root
acquisition/renderer stderr files are also empty and match scratch exactly.

## Seven-raster comparison

For the exact seven names below, `cmp -s T/name.png R/name.png`,
`shasum -a 256 T/name.png`, `wc -c T/name.png` and `file T/name.png R/name.png`
were run (`0d2230`, handle 15915, terminal `511320`, exit 0). Every comparison
status was 0 and both header dimensions agreed. Each directory contained seven
PNGs; all are RGB, 8-bit, non-interlaced. This measures saved-file geometry,
not any reader's displayed image. No image was viewed or decoded for content.

| ID-page (NYC-WTC_000 prefix) | Width x height | Bytes | SHA-256, both files |
|---|---|---:|---|
| 171251-1 | 1785 x 2400 | 118833 | `90ff469d26eadbd665b4ae8792b9223b800e1ce9e4e498b89d17bf77640f6799` |
| 172976-1 | 1786 x 2400 | 138854 | `44c9df736c74424e4cd089fdb807abdb09a620cf7be7cc3f93490447cc0044f8` |
| 172977-1 | 1791 x 2400 | 116875 | `24b4563c69a81f57293cdb82feebaecba48eab1e50fcedde5adcbd90f82fe81f` |
| 171520-1 | 1787 x 2400 | 97579 | `04af133c8e90501cf01d3c6d0c4c2be399c4ccb1113e1c891ce70c84a2e18314` |
| 174095-1 | 1787 x 2400 | 139508 | `da4d57c1f8e9a001e281202d7eba3b69fbe900c41f6fea214d5ffbc049835fa4` |
| 167866-1 | 1794 x 2400 | 77791 | `a35c818f17b25f903ce685d32a9b4fce6c847f96c690dc91608be3262eb44dc5` |
| 167866-2 | 1797 x 2400 | 171440 | `18a7f1670ff855d40eda213bea39f5c92d651e5fbd5513600c78d5437bc4eb0b` |

## All 41 preserved pairs

At 2026-10-05T02:26:05Z, the checker expanded `cmp -s U/name R/name`,
`shasum -a 256 U/name`, `wc -c U/name` for each of six IDs with suffixes
`.pdf`, `.headers`, `.transport.txt`, `.stderr`, `-render.stderr`, `-1.png`,
then `NYC-WTC_000167866-2.png`, `fonts.conf`, `171251-sandbox.headers`,
`171251-sandbox.transport.txt`, `171251-sandbox.stderr`.
Receipt `630346`, handle 70858, terminal `9a4b89`, exit 0: 41 pairs,
every comparison 0, zero failures. Thus all six PDF and seven PNG pins above,
the root config pin, the twelve empty diagnostics, and the following header,
transport and failed-attempt files match their preserved copies exactly.

| ID | Header bytes | Header SHA-256 | Transport bytes | Transport SHA-256 |
|---|---:|---|---:|---|
| 171251 | 512 | `d993fd2145eed6ea2d9a226b362c171a28da1c1c73888e60fd852cdc507a83a5` | 94 | `04d7054ccf215ea554d9f52af159f5680fa6532e4c0fb5065eebec45fa1bac5f` |
| 172976 | 515 | `e34b0b807973a0826c81a8759e5d6f34ba4efce279b2f19cd2d463d7e71decab` | 94 | `19afb0ecffc8f741eb46b9a786afaa12f5459bf94f1c15e13705546b9961ed82` |
| 172977 | 515 | `2eb1f19feec299073cc47fa3828d7409638987a53b53403fbb05ec1458b8b232` | 94 | `ecde36a8a53afd0c59be5d6011ed766f85d1db0539be12301cf61e3465b6fa72` |
| 171520 | 515 | `021f08e2477b1fb1a2c6e1730ad83e4d5c6abacd84503449ee13bf5eead1358a` | 94 | `87c27189cc48d07bce50e50e97abe311523db41dca8ccdf1ed93c78616f74d73` |
| 174095 | 515 | `371499bb598523550ffdcad807a48fcca0235b5dbaefe6897bf670ee3d53c2e4` | 94 | `770d3a60f9f62ea3c88db251251a3e03d7901057d7d17a370c01ea50d125fac0` |
| 167866 | 517 | `acc74c817e5bffe145f2dcfebe5b2936c3a51398040bb59300e086bb1ddf8b81` | 95 | `17a23a0beca5ae1cf229cd5dcc2d7bffb133f3e531136c244aae3f94a7f9beca` |

Allowlisted stdout-only `Y -` transport/header correspondence check (`324348`,
exit 0) read logs and header fields without emitting raw headers. Every
successful log records curl_exit=0, HTTP 200, application/pdf, redirects=0,
and bytes exactly matching its PDF; each header set has exactly one HTTP 200
status, matching Content-Type, no Location header. Successful stderr is empty.
Recorded time_total seconds, in source-table order: 0.407935, 0.546114,
0.856691, 0.379822, 0.653251, 0.897008. These are stored acquisition receipts,
not new network measurements by this checker.

The failed sandbox attempt remains separately preserved and byte-matched:

| File | Bytes | SHA-256 |
|---|---:|---|
| 171251-sandbox.headers | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 171251-sandbox.transport.txt | 75 | `6a132832c5ae73a300bf4bbf1886492a15439c79f428fdf637d136c720a752f6` |
| 171251-sandbox.stderr | 67 | `02a2b254dd32ec6b50259755356a72c28e89ce3fc3d52329aa73c219c559b7e5` |

Its allowlisted log is curl_exit=6, HTTP 000, bytes=0, empty content_type,
redirects=0, time_total=0.042765. The stderr contains the DNS failure marker
`Could not resolve host`; raw stderr/header text was not printed. This is a
failed acquisition, not a successful response or evidence of server refusal.

## Failures, attribution and limits

No checker admission, render or comparison failed in this unit. Config diff
exit 1 was the expected separately declared cache-path difference. The initial
sandbox acquisition failure above remains a failure despite the later success.
Root reported its source-check receipt `063816`, handle 35212 to `ce627a`,
render receipt `040fac`, handle 29736 to `16bd8a`, and preservation receipt
`d5a68a`, handle 48735 to `3578f5`, all exit 0. These are attributed root
receipts; this checker directly observed only its own six renderer exits and
the checks recorded here. Present equality does not prove historical copy
method, no-overwrite execution or independently authenticate acquisition.

After the initial checks, root explicitly reported both readers' frozen
seven-page sets, zero repeats and zero delayed saves. It supplied root-note
pin `c55968144689f3572c99e464c43d09bf7f92bf87080a49f6375dbb29e6668574`
and observer-note pin
`2bab59d316426464f93e580128ea5642cf2d853159467ff51378e94c6d0bc110`.
Those are attributed closure reports, not additional independently checked
pins: this checker neither read nor hash-checked the reader notes. No larger
raster was requested or produced by this checker. Final coverage is six
actual renderer executions, seven rasters and 41 preserved-copy pairs.
Only source admission and local derivation/preservation are assessed. Shared
Poppler/system-font defects can reproduce identically. Hashes and byte matches
do not establish historical authenticity, truth, source-family independence,
equipment performance, installed routing, event-day state, causal conclusions,
display geometry or actual human/expert acceptance. Scratch and failures are
retained; no source, raster, header or diagnostic was deleted or sanitized.
