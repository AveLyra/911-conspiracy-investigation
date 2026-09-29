# Independent render01 integrity review

September 20, 2026. Reviewer: `next_discriminator`. This is a source/derivative
integrity and bounded code review, not a primary-page interpretation or visual
fidelity review. Main controls, the full charter, protocol, evidence/source
preservation skills, development-verification skill and PDF skill were read.
Only this working research note was written; no source, code or frozen product
was changed. No new network request, PDF render, historical-media decode,
page display or content interpretation was performed.

## Result and admission boundary

**Integrity/decodability pass; not a clean-render or glyph-fidelity finding.**
All six pinned inputs match their recorded before/after identities and current
bytes. The exact 74-file inventory is present. All 18 recorded commands match
the declared nine-page/full-page/120-dpi scope and returned 0. All nine PNGs
are complete, decodable, single, nonanimated RGB images, each 1020 by 1320.

All nine image commands also emitted substantial Fontconfig errors. Successful
return codes, valid PNGs and complete pixel arrays do not establish correct
glyph substitution or faithful source-page content. Conversely, the warnings
alone do not demonstrate a wrong glyph or omitted figure.

Products were not inspected before root confirmed terminal session 99363 had
finished with exit 0. The receipt's status is appropriately
`commands_complete_not_visual_review`, not a visual admission certificate.

## Scope, exact paths and pins

Unit root:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/nist-acoustic-detectability`.

Fresh identities, matching `render01/start.json`, both receipt pin sets and
the declared source hash:

| Pinned file | Bytes | SHA-256 |
|---|---:|---|
| Main `authority/nist/wtc7/ncstar-1-9.pdf` | 52,766,002 | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| Unit `PROTOCOL.md` | 4,723 | `ea6bcc9ee92aeef7a1d89799401bc5ddfa82e19956d826853422abd65741fa55` |
| Unit `render.py` | 3,184 | `280086aaea3f05d1f38035aa5e24b60a1eed1bc520e4288608496c34d00ec0f2` |
| `/Users/admin/.pyenv/versions/3.13.7/bin/python3` | 33,816 | `7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e` |
| Poppler native `bin/pdftoppm` | 75,280 | `98ac4fedc4258b7125ad1048034c1448dccc58503614eb105f19d12cdb3a2d0d` |
| Poppler native `bin/pdftotext` | 106,256 | `facaa63884cd1071d5062476443613a9cadc4f0489cfd28da2e4e64c2f8dd4cb` |

The full native Poppler base is
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler`.
`file` independently identifies both pinned Poppler paths as Mach-O arm64
executables, not shell launchers. Their resolved paths are unchanged.
The Python path resolves to the same installation's `bin/python3.13`.
Fresh `-v` invocations of both native Poppler executables returned 0 and
reported version 26.05.0; no PDF was passed. The review's explicit Python
3.13.7 runtime version matched the complete string saved in `start.json`.

These are executable-byte/version checks, **not certification of every shared
library, Python package, font, operating-system dependency or dynamic-loader
decision**. The saved environment contains only the declared `PATH`, `LANG`
and native `DYLD_FALLBACK_LIBRARY_PATH`; it does not pin a Fontconfig file or
font collection. The initial fallback/nonexistent-locator failures reported
by root were not repeated or independently reconstructed by this reviewer.

Receipt SHA-256:
`291effcacdf986c7cffa16ca8c385193c66d63bece169836f9c38005424d3dcd`.
Start-record SHA-256:
`d46a1f0a3873a9058181378a423d45a712f7f56f1b199a59e25f184dd52d92aa`.

## Checks actually executed

The independent checks were inline Python commands, not a newly saved verifier
program. Product verification used:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B - <<'PY'
# Independent receipt, artifact, PNG and post-read pin checks described below.
PY
```

This block identifies the executed command form, not a claim that its comment
is executable verification code. The reproducible check recipe was:

1. Read the start/receipt JSON; require the exact six expected source paths,
   source hash, pages `[333,334,399,400,401,772,773,774,775]`, DPI 120 and
   declared three-entry environment. Rehash each input using SHA-256 and check
   byte lengths against start/before/after records, not just their equality.
2. Build the expected artifact set independently: for each page, one PNG, one
   text file, and JSON/stdout/stderr for each of render and text extraction;
   plus start and receipt. Require exact set equality, no directories or
   symlink products, and no extra files. Verify every saved product hash and
   length. There are **73 hashed products plus the receipt itself = 74 files**;
   omission of the receipt from its own product hash map is expected.
3. Reconstruct each command's full argument vector from the fixed page list,
   source and native paths. Require `-f` and `-l` to select the same declared
   physical page; image commands additionally require `-singlefile -r 120
   -png`, text commands `-layout`, and exact expected output paths. Require
   `status=returned`, `exit=0`, timeout 60. All 18 stdout files and all nine
   text stderr files are empty; all nine text products are nonempty.
4. Parse each PNG independently: exact signature; complete chunk bounds;
   valid CRC for every chunk; exactly one first IHDR and one terminal IEND;
   no bytes after IEND; no APNG animation chunks. Require 1020 by 1320,
   8-bit RGB, standard compression/filter method, and no interlacing.
   Concatenate IDAT payloads and require complete zlib decoding with no
   unused/trailing compressed input. Check the full 4,040,520 decompressed
   scanline bytes and all row-filter selectors in 0 through 4.
5. Using installed Pillow **12.0.0**, independently reopen each image, require
   PNG/RGB/one frame/nonanimated and expected dimensions; run `verify()`;
   reopen, `load()` fully, and require **4,039,200 RGB pixel bytes**. Hash
   those decoded bytes. This is pixel decoding, not a display or content
   judgment. All nine passed; all contained only IHDR/pHYs/IDAT/IEND chunks.
6. Rehash all 74 artifacts and the six inputs after the read/decode checks.
   Every identity remained unchanged. All checks above completed with exit 0.

Decoded RGB hashes, distinct from the encoded PNG hashes preserved/verified
through the receipt:

| Physical page | Decoded RGB SHA-256 |
|---|---|
| 333 | `593657449320fb5c2bafe8594063e37454f9be11f4ae3076aa5dc2a285352e30` |
| 334 | `9b384d5789be2f09aeedc544bcab17c9840bede449b99793022be3eb952aa4f0` |
| 399 | `93b01134efec4df878b1f139be7141f7f8cae4f6309513ce56f55edce21fea25` |
| 400 | `3b7132c0e13a7d702e694c6ccbcec00cbbcbdb8300b18a255cd43cb7eb907699` |
| 401 | `3ea07382d0e417900632aa14b9040bd64c2fb3bd15e72655e50640df8d8856d3` |
| 772 | `a892ce60f67405431f5f600190514524fae473db2b9347911757bbfea749fe2c` |
| 773 | `190b1c1ea845a63db9d2abd040af253f5157e757aeb945bcd2407f6ad76ec8c6` |
| 774 | `76898c0c27b1a1dad245ee33e0cf96f734b630d4a54024c2d31fb20a38077adb` |
| 775 | `ace869c46e1ba8b611ae91ef78e4821fd71927879c55e7a5727a66c6ea270b19` |

## Diagnostics and controls

Each image stderr file contains **1,471,718 bytes / 32,345 lines**. A complete
line-frequency check found the same five distinct lines in each: one
`Fontconfig error: Cannot load default config file: File not found`, 8,086
`Fontconfig error: No writable cache directories` messages, and their two
cache-path lines plus blank separators repeated 8,086 times. These errors are
not suppressed or relabeled as a diagnostic-free run. No additional distinct
diagnostic message was found in those files.

Before product admission, this reviewer ran four independent in-memory mocked
controls by importing `render.py` without executing its main entry point:
success, nonzero return, `TimeoutExpired`, and existing-directory refusal.
All **4 passed**, exit 0, with no subprocess or file creation. The first three
checked saved status/exit/argv/timeout and exact stdout/stderr bytes; the last
checked refusal before source identity or save calls. **The timeout was
mocked; it was not an experiment that ran a process until timeout.** These
controls used `PYTHONDONTWRITEBYTECODE=1 python3 -` and standard-library mocks.

Root's preserved fixtures under
`/private/tmp/nist-acoustic-render-controls-ds55oi0s` were then read. They
contain the expected actual success exit 0 and nonzero exit 3 command records
and fixture stdout/stderr, plus a separately mocked timeout record with null
exit and partial outputs. This inspection corroborates those saved fixture
bytes, not direct observation of root's earlier execution or a real timeout.
Root's reported existing-directory control has no separate artifact there;
the reviewer's independent refusal check was mocked.

The reviewed code preserves subprocess nonzero/timeout outputs and uses
create-only files/directories. Its `finally` receipt records incomplete status
when the page-command sequence fails. The current run contains no such
command failure. This is not exhaustive coverage of spawn errors, process
termination, filesystem failure, optimized-Python behavior or hostile inputs.
No rerender was needed to establish the limited integrity facts above.

## Recommendation and subsequent distinct visual information

Before root's visual result, this reviewer recommended: **preserve render01
as a warned derivative and resolve font setup before primary-page reliance**.
That conservative recommendation was communicated and is retained here, not
retrospectively replaced by a claim that the initial render was clean.

Root subsequently reported complete viewing of all nine pages without observed
missing glyphs, clipping or incomplete figure labels. Root elected to admit
them for bounded prose/label reading with warnings preserved, not numerical
digitization or a clean-render claim, and reported that a second visual reader
was checking them. Those are **root-reported visual observations and an
admission decision**, not findings independently made by this integrity
reviewer. No visible-content defect has been demonstrated by this review.

The strongest residual objection is that correct bytes and successful pixel
decoding cannot establish the correspondence of rendered glyphs, figures or
page labels to the PDF's intended content. A concrete ambiguity or defect in
that correspondence would require a declared clean-font rerender or another
bounded source check before relying on the affected content. This note neither
supplies a primary-source interpretation nor authorizes a change in causal
weight, legal position or accepted-engine state.
