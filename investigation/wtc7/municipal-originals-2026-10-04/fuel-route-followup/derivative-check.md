# Independent single-page render reproduction

October 4, 2026. PASS within the declared one-page derivative scope. This check
was performed after the independent content reading froze; it did not involve
another page-image view or alter either frozen reading.

## Inputs and independence

Source: `NYC-WTC_000171753.pdf` in this directory, 62,089 bytes as admitted by
root; SHA-256 `537331e3169cc995e7729b60c61a806fb65348eae916f93f6f1bbc48bed47310`.
Root reference PNG: `page-1.png`, SHA-256
`eb8b4cb43b9cf48fef81d1b32c8480351614dce9a0ee7e10c5b56c61503e701a`.

The admitted temporary PDF/PNG were hashed before reading (`12be46`, exit 0).
The subsequently preserved PDF/PNG were independently hashed before this
render (`98f8a6`, exit 0) and matched. No source retrieval or editing occurred.
The shared PDF, renderer version, font directories, and reading protocol are
common dependencies. A separate command/output directory is not independent
historical evidence or an independent PDF-rendering implementation.

Runtime discovery used `load_workspace_dependencies`; bundle 26.905.11957.
`pdftoppm -v` reported **26.05.0**, exit 0 (`f0e255`). The override wrapper and
native launcher were inspected (`8fa450`, `97b410`, exit 0): they delegate to
the bundled actual Poppler binary, with the native launcher setting its library
path. Local SHA-256 pins (`fcfa49`, `015b50`, exit 0):

| Component | SHA-256 |
|---|---|
| `dependencies/bin/override/pdftoppm` wrapper | `de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159` |
| `dependencies/native/poppler/bin/pdftoppm` launcher | `d9d81b176e8fd38d07f2fbf4f84c17dc991c6bac3730ff3cad3239c4fcbed892` |
| `dependencies/native/poppler/poppler/bin/pdftoppm` binary | `98ac4fedc4258b7125ad1048034c1448dccc58503614eb105f19d12cdb3a2d0d` |

These are component pins, not a claim to have hashed the entire library/font
dependency closure.

## Fresh configuration and exact execution

`mktemp -d /private/tmp/wtc7-fuel-route-peer.XXXXXX` created
`/private/tmp/wtc7-fuel-route-peer.MMysHO` (`522bfb`, exit 0). A new fonts.conf
was written with apply_patch, using the same font directories but a distinct
private cache, without changing root's configuration or its cache:

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>/System/Library/Fonts</dir>
  <dir>/Library/Fonts</dir>
  <cachedir>/private/tmp/wtc7-fuel-route-peer.MMysHO/font-cache</cachedir>
</fontconfig>
```

Configuration SHA-256:
`686ad59acf527c06c37f74c48697212c0ffc2bd15aebcfbdef4f2ac9e09a988d`.
Exact fresh render command:

```sh
env FONTCONFIG_FILE=/private/tmp/wtc7-fuel-route-peer.MMysHO/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -scale-to 2200 -png /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/fuel-route-followup/NYC-WTC_000171753.pdf /private/tmp/wtc7-fuel-route-peer.MMysHO/page > /private/tmp/wtc7-fuel-route-peer.MMysHO/render.stdout 2> /private/tmp/wtc7-fuel-route-peer.MMysHO/render.stderr
```

Terminal result `fede91`: **exit 0**, no running session remained. One render
attempt; no repair/retry or alternative output selection.

## Actual verification and outcome

- `cmp` of new `/private/tmp/wtc7-fuel-route-peer.MMysHO/page-1.png` against
  this unit's preserved `page-1.png`: **exit 0**, byte-identical (`0c7f72`).
- `file` on both PNGs: **1638 x 2200, RGB 8-bit, non-interlaced**, exit 0
  (`a6fc1d`). No graphical measurement or content comparison was performed.
- `wc -c` on new PNG/stdout/stderr: **127,842 / 0 / 0 bytes**, exit 0
  (`c1e8dc`). There were no captured rendering warnings.
- `shasum -a 256`: new PNG
  `eb8b4cb43b9cf48fef81d1b32c8480351614dce9a0ee7e10c5b56c61503e701a`;
  empty stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
  The source PDF still matched its original pin (`fcfa49`, exit 0).
- Post-render frozen-note hashes also matched (`fcfa49`): independent
  `review.md` = `b270ff8ddea5c7bcfbe5eacf655a74c24a8fd641c534aa25d2c8162dd26bcc60`;
  root = `ce298f97d6930307cba4315be82016619c212a1031d748e14a0ea22053ecec80`.

The new PNG, configuration, empty stdout/stderr, and cache remain in the
fresh temporary directory; none was substituted for a root artifact or source.
This saved report preserves commands, pins and results but does not promise
permanent retention of operating-system temporary files.

## Content cross-review and ceiling

After both reading freezes, the complete root note was read as text
(`b54189`, exit 0); no material disagreement with the independent reading was
identified. Both preserve the June 30 letter date versus July 1/2 fax markings,
the conditional future installation/cost proposal, 8-inch conduit versus
1-1/4-inch lines, unknown segment/revision join, distinct support elements,
and absent installation/approval evidence. No further source view was used.

This is a reproducible local image transformation under shared software, not
authentication of the original letter, fax delivery, asserted feasibility,
performed construction, accepted findings, structural adequacy, or cause.
No changes were made to raw main/legal material, preserved source, older
reports, or the frozen readings. No network, disclosure, engine action,
staging, commit, or push occurred in this check.
