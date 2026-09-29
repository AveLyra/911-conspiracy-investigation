# Protection-source reading: derivative verification

2026-09-27. This receipt supports the [source comparison](../protection-assumption-crosswalk-2026-09-27.md),
not historical authenticity, numerical model verification or a new experiment.

## Production actually performed

Root rendered exactly17 pages of the unchanged main-checkout NCSTAR1-9 source:
78-87,125-128,598-600. Selection and later dependency extensions were recorded
before each new content group. From the parent audit directory, each invocation
used the following command with its listed page number substituted for N:

```sh
test ! -e protection-render01/n9-N.png && FONTCONFIG_FILE=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/contracting-access-custody-audit/protection-render01/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f N -l N -singlefile -r 200 -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf protection-render01/n9-N
```

All17 commands reached terminal exit0 with empty stdout/stderr. The first
five used sessions9699(127),36853(128),95721(598),64027(599),39360(600);
126,78,79,125 returned terminally. The final batch used sessions96944(80),
13005(81),90958(82),62974(83),4510(84),71754(85),41964(87), while86 returned
terminally. Every yielded session was polled to completion rather than
restarted. Poppler26.05.0; bundled runtime26.905.11957.

The task-specific fonts.conf is342 bytes; SHA-256
`4c4454f7aaa84378f80b37c5920601c5f8c8baf0a902c98a04e1854b5fddb84e`.
It uses the two system font directories and a cache within this derivative
directory. Executable/library/font closure is not fully pinned by a version
label or that configuration alone.

## Independent read-only checks

A separate verifier used bundled Python3.12.14 with `-B -`, stdlib hashlib/JSON,
Pillow12.3.0 and pypdf6.10.0. It did not import a producer, render, read page
content, view images or modify files. Root and a different source reader own
the visual/source interpretation. Verification checked26 PNGs:17 new and9
reused; all verified and fully decoded as single-frame RGB. The17 exact N9
page objects have MediaBox=CropBox=[0,0,612,792],rotation0, consistent with
1700x2200 at200dpi. Parser logger/direct stderr/warnings were empty.

New images have captured byte/pixel identities, **not** a match against an
earlier independent render. Below are the saved byte identities for replay:

| File | Bytes | SHA-256 |
|---|---:|---|
| n9-78.png | 429534 | `d3070fdfd9e57812664f264f03e0223acf5b1daf10a20b1d54407e8b178ca28a` |
| n9-79.png | 466106 | `31e435f046f71230608c03d69ce854c7e257971bf64673c021922acf32e05b87` |
| n9-80.png | 1164807 | `90a1299d5b15e552db8d5023b6b4f4604d30f3b44058782b23bd08906a2f71b0` |
| n9-81.png | 842858 | `7762df640e800d0a6dabc06ad620812c474c61d7219af4b635db6214f9a79a44` |
| n9-82.png | 1019552 | `9290e590f4cc4754f314b6a57b624ecb8f02440b22a76787c612803c8738d2eb` |
| n9-83.png | 1774770 | `4a18af28433b0501afb24ce819e860a0db413510bba1c5ae237a4afec29bef77` |
| n9-84.png | 2619317 | `918133c0fa817dc2b280ab7ee579949f35445a6fb184c2c15c6367045a7f9635` |
| n9-85.png | 1111477 | `5dc9f35b3310eaa1d1679fd4e49b3f156d1e80af25e072d1ca635ff28b55148e` |
| n9-86.png | 880313 | `a92f8ca1b51784718a0dd1602ed4b3de9d432ab8b790644423bd4a8905c742e0` |
| n9-87.png | 1600955 | `cf17f70058f470e4ad44ecb40d1645150df324aa3470f91f10db30fbf94dadb3` |
| n9-125.png | 438811 | `dbbbbc20a868053b2ada99f385e4e0514f7f37d430c585bad8c048d5fea5de46` |
| n9-126.png | 360744 | `d1158dec308342e88eb8fb3f70498f2ddd982db2d5ae4e124a706aaaaec93cb4` |
| n9-127.png | 548707 | `2c201ca95b4c22b36aecfea089cdc6d6ed60c8a59c98e3d2996e91b90216445f` |
| n9-128.png | 189116 | `302b1e3ade05b16b6fb3588ad934fd0b5bdbad3933e68f16cb62d7134693fc84` |
| n9-598.png | 784246 | `816ac398bffa187503f6326d09ceffd020d773656088e6cb6ee16847fa311ff7` |
| n9-599.png | 422417 | `87dbe02a57af2b00900bcc2f936c4fc4312497cda448d474601f49295f39dd15` |
| n9-600.png | 333409 | `e9259657496e36af08363c94018a9b2ded8f00947266f4451a8970731b88cf6f` |

Nine reused images also passed the available historical pins:

- N9 physical432-434 in the main fuel-audit `nist-source-review/derivatives/`:
  byte counts/hashes match entries37-39 of its `source-manifest.json`, SHA
  `ce748a582152d8c69a16d5bd73b0314ff5bf9f2bf9a6cb5d593df5fe0119dc2b`.
  The separate render receipt verifies selected membership and recorded status,
  but contains no byte hashes; do not conflate those contracts.
- Both errata images in the main fuel-audit `equipment-source-followup/errata-review/derivatives/`:
  hashes/dimensions match its `receipt.json`, SHA
  `df6df5546640d8ae3c3f47872c9c408d794ed1a37c81041bc5ed064cf895ee1b`.
- C physical107,108,110,112 in `../structural-render01/`: byte counts/hashes,
  dimensions/modes and decoded pixel hashes match its receipt, SHA
  `eda0146cc0ac1f7dd7c2af5bbb98ab8effd83240f884cea6f8fa6b383d28a325`.

All reused images are1700x2200 except errata1701x2200. Their cumulative size
with the new images is20,025,198 bytes,291,733,200 decoded RGB bytes.
The three source pins in the parent note match. The initial full check
confirmed33 files unchanged before/after (26 images,3 PDFs,3 receipts,1 font
configuration); the later N9 manifest comparison also preserved that manifest.
These are copy/decoding/selected-page-metadata checks, not a fresh render
replay or independent parser implementation. Root's render statuses remain
root-observed, not independently reproduced by this verifier.

Preserved failure: the verifier's first receipt-schema probe assumed a dict;
the list-valued N9 render receipt caused `AttributeError`, exit1. Corrected
read-only inspection and verification exited0; no file writes resulted.
Root also first tried an obsolete PDF-skill alias path, received file-not-found,
then read the catalog's actual complete instruction file before PDF work.
Neither failed probe is hidden or represented as a successful check.

Root's final stdout-only verification parsed all17 saved new-image table rows,
checked byte counts/hashes, verified and decoded every image, and confirmed
the expected1700x2200 RGB single-frame state. All passed. Four PDF source
pins (including the earlier appendix) and the new font pin matched. Three
working-note whitespace checks and15 local-file links passed; URL/fragment
targets were not validated. `git diff --check` passed for tracked changes.
An initial review-correction patch failed on an extraneous context line without
applying changes; the corrected patch succeeded. Branch/HEAD and main's
preexisting dirty-file listing were rechecked unchanged; no main edits were
made. Intentional WIP remains uncommitted in the investigation worktree.
