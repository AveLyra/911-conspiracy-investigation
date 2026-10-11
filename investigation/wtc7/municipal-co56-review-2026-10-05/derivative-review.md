# CO56 independent derivative verification

October 5, 2026. Mechanical reproduction only: no primary image was viewed,
no OCR/text extraction or source interpretation performed, and neither reader's
observations were accessed. Matching bytes establish this derivation, not
historical authenticity, readable fine text, installed work or correct interpretation.

## Preflight and fixed population

The complete [protocol](PROTOCOL.md) was read and pinned before this reproduction:
`4f2fc2ad46f4d8b6b65c05c75e8aa61e18f35c49c34c58616aafd15a908e05b2`.
No material method objection was found. Main AGENTS, WORKFLOW, START-HERE and
CHARTER pins matched the previously read controls (`aad280`, exit 0).
Evidence-falsification, source-preservation and PDF skills were reread in full
(`9a337e`, exit 0); both audit reference files were read (`68b782`, exit 0).
No PDF authoring or acquisition was undertaken by this checker.

Both readers subsequently reported their used sets closed: one complete initial
168526-1.png each, zero larger repeats. Root reported its freeze as
`bdb350428abcf8fe4a55b0e4abccbfc0ed697490174dd08fc9dfc6d0ec20b783`
and the independent reader reported
`094df22bdfdd79f014ff97edf5bb4948831f859c55f5fceef6faade40e83f913`.
Only those process notifications were received; no note content was read or
chronology independently certified. Thus the new-raster population is exactly
one 2400-max-dimension PNG; no larger derivative remains outstanding.

## Inputs and environment

| Item | Bytes / dimensions | SHA-256 |
| --- | --- | --- |
| Preserved NYC-WTC_000168526.pdf | 43,286 bytes | `50ee20cad0c90f3baaf07597365e453bd991d89f0ea2d1dd3da0d6b806b8cc57` |
| Preserved and both reproduced 168526-1.png | 113,230 bytes; 1758 x 2400 | `4aa1406ae090a724b5121442883754044ebf4695d8d5ae3164601be8525c992e` |
| Preserved root fonts.conf | 217 bytes | `dbf2a3e2003dcd2c77fb603c62468c73734be4cb66fcbc65899739a83790f2cb` |
| Initial checker fonts.conf | separate configured cache path | `538be97e3bb1ffc2d1a3f2cc92c01f32865557fb07619f99cb02b81400bd1f56` |
| Corrected checker fonts.conf | explicit existing private-cache directory | `47ba69085c8e943d754e886f9d5fb0c4d6396f38d360f45cba4becef5efa39e5` |

The bundled dependency lookup supplied the runtime path. `pdftoppm -v`
reported Poppler 26.05.0 (`9c2faa` / `435d7b`, terminal exit 0).
Launcher `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`
SHA-256 `de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159`;
underlying `dependencies/native/poppler/poppler/bin/pdftoppm` SHA-256
`98ac4fedc4258b7125ad1048034c1448dccc58503614eb105f19d12cdb3a2d0d`.
Both checker configurations use only the same declared font directories,
`/System/Library/Fonts` and `/Library/Fonts`, with a different cache path from
root. No claim is made that the renderer actually needed or used a font cache.

## Actual commands and retained correction

`mktemp -d /private/tmp/wtc7-co56-repro.XXXXXX` created
`/private/tmp/wtc7-co56-repro.qyDr11` (`9bad01`, exit 0).
Its fonts.conf was written with apply_patch, using cachedir
`/private/tmp/wtc7-co56-repro.qyDr11/font-cache`.

The first command was exactly:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-co56-repro.qyDr11/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2400 /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-co56-review-2026-10-05/NYC-WTC_000168526.pdf /private/tmp/wtc7-co56-repro.qyDr11/168526 > /private/tmp/wtc7-co56-repro.qyDr11/render.stdout 2> /private/tmp/wtc7-co56-repro.qyDr11/render.stderr
```

It was started once (`72dbc3`, session 59985), then polled to terminal exit 0
(`6c7ad5`), without restarting after a yield. The subsequent stdout-only byte/
header check (`b5c2d5`) confirmed PNG equality, dimensions, source/control pins
and empty diagnostics, but ended **exit 1** at an extra assertion that the
configured private-cache directory existed. It had not been automatically
created. That failure is retained, not described as a passing overall check.

The first attempt was left untouched. One explicit mechanical correction was
announced to root: `mktemp -d /private/tmp/wtc7-co56-repro-corrected.XXXXXX`
created `/private/tmp/wtc7-co56-repro-corrected.dxmDnl` (`171741`, exit 0), then
`mkdir /private/tmp/wtc7-co56-repro-corrected.dxmDnl/font-cache` succeeded
(`4b86a8`, exit 0). A new apply_patch config named that exact directory.

The corrected command was exactly:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-co56-repro-corrected.dxmDnl/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2400 /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-co56-review-2026-10-05/NYC-WTC_000168526.pdf /private/tmp/wtc7-co56-repro-corrected.dxmDnl/168526 > /private/tmp/wtc7-co56-repro-corrected.dxmDnl/render.stdout 2> /private/tmp/wtc7-co56-repro-corrected.dxmDnl/render.stderr
```

It started once (`1275bd`, session 86019), then reached terminal exit 0
(`29601c`). No source, original derivative, protocol or reader note was changed.
This extra mechanical render was not a reader repeat or a new content view.

## Verification result and limits

The final stdout-only Python check (`e7dd5c`, exit 0) read raw file bytes, used
SHA-256 and PNG signature/IHDR dimensions, and asserted all of the following:

- Root, initial reproduction and corrected reproduction PNG bytes are exactly
  equal, not just visually similar or equal in dimensions; each is 1758 x 2400.
- The source PDF, protocol and preserved root configuration retain the pins above.
- Root and both checker render attempts each have zero-byte stdout and stderr.
  All six empty files have SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- The corrected private-cache directory exists and the configuration names it.
  It contains zero entries; directory existence is not proof of cache use.

The admitted one-page derivative is therefore reproduced across a separately
configured scratch/cache environment, with the first check's setup failure and
corrected attempt explicitly distinguished. Source acquisition, server headers,
PDF page-count/action-flag admission and reader display behavior were not
independently replayed by this checker. The parent provided those admission
receipts; this check directly established file identity and reproduction only.
No source-content, structural, installed-condition or causal conclusion follows.
No main/legal, canonical, engine, Git or disclosure state was changed.
