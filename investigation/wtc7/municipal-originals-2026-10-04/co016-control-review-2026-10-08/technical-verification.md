# Independent technical check of the fixed CO016 population

October 8, 2026 local / October 9 UTC. Research only. This reviewer checked
metadata, copied bytes, basic PDF structure and rendering repeatability. No
document text extraction/OCR, image display, substantive page interpretation,
reading of either observer's notes, network request or source mutation occurred.
The PDF/evidence/source-of-truth skills keep technical integrity separate from
historical authentication, sensitivity clearance and human/expert acceptance.

## Result and coverage

**Technical checks pass for the acquired NYC-WTC_000171905 PDF and both page
derivatives.** All four copied files equal the acquisition scratch originals.
A fresh two-page rerender with a separate temporary font cache equals both
saved PNGs in encoded bytes and decoded RGB pixels.

The declared population remains two documents / three reported pages:

| ID | Reported pages | Reported bytes | Reported last Bates | Checked present state |
| --- | ---: | ---: | --- | --- |
| NYC-WTC_000171905 | 2 | 89091 | NYC-WTC_000171906 | PDF and both complete-page renders acquired; technical checks passed |
| NYC-WTC_000171909 | 1 | 57584 | NYC-WTC_000171909 | No PDF in the worktree or acquisition scratch directory; unacquired and unread |

The latter's absence is a directly checked filesystem state. The two connection
timeouts are root's preserved acquisition results, not requests repeated by
this reviewer: terminal receipts `b90e26` and `3f5678`, curl exit 28,
20.008823 and 20.006215 seconds, HTTP000 / zero bytes. Manifest `http_status:null`
appropriately records that there was no HTTP response. The route is stopped;
the missing page is not a content nonmatch, archival absence or withholding
finding. This check does not silently reduce the original population.

## Selection and control pins

Preflight assertion `17564b` (exit 0) checked both exact IDs, titles, page-count
strings, sizes, last Bates, strict-valid status, empty missing fields, null
strict errors and membership in the single saved `break_glass` query. The
two-row selection totals 3 pages / 146675 reported bytes. That saved query
returned eight rows; selecting these two is not exhaustive query-content or
archive review. A preliminary `jq` lookup (`ce1a37`, exit 5) wrongly addressed
the `documents` object as an array. The corrected object lookup and explicit
assertions succeeded; no evidence or acceptance rule was changed.

These three pins matched before and after preflight and again before and after
the actual rerender (`1a5786`, `b48834`, `a95601`, `721b0e`):

| Control | SHA256 |
| --- | --- |
| PROTOCOL.md | e37fe180397f5e57d8c8fbfc2af5c5fcdd39042c82242abd170b6b264d71942f |
| ../job1854-followup-locator/root-diagnostic.json | c6a80ecc100e77cc3d387e17fa032e8c4032e4e13cb761d20bffd6eaed51e7d8 |
| ../test-chain-review.md | 29df1c8b50b3dac9d91eba18132d36224c5616a09e9fbfaedb13771b1a7c3ad3 |

Only the last file's hash was checked; this technical assignment did not read
its substantive interpretation. The complete current protocol was read.

## Copy, structure and image checks

Original-copy location: `/private/tmp/wtc7-co016-20261008.LWyZwn/`.
Each correspondingly named file in this unit was compared byte-for-byte with
that directory. All four checks passed (`a5e547`, exit 0); none of the checked
leaf paths was a symlink. Pins remained unchanged after rendering (`721b0e`).

| File | Bytes | SHA256 |
| --- | ---: | --- |
| NYC-WTC_000171905.pdf | 89091 | 4e10972135a0d9e24a61da9560cd554a4b5f6e66087aeee109ba041ad4fd2ca6 |
| NYC-WTC_000171905-1.png | 120265 | 3c966e459dac95876a423fc5c23b799fe7574a137ca0927e77588b98d03f2d75 |
| NYC-WTC_000171905-2.png | 98315 | ae767d63f79b21869c981566eae8443c98b36c4063d3672003ae2d9bfb4258e2 |
| fonts.conf | 227 | 4d7cf05f6ca79c9cb870cd5927df09305d0add4fc6e83cdb203f7df7e6b4b023 |

The PDF starts with `%PDF-`, has exactly two pages and is not encrypted.
`pypdf` found no catalog `/AcroForm`, `/OpenAction` or `/AA`, no page `/AA`,
and zero page annotations on both pages. This is the stated limited structural
check, not a comprehensive malicious-content scan or a security certification.
No page text or metadata contact strings were emitted.

Both PNG signatures and IHDR values match successful complete Pillow decodes:

| Page | Dimensions | Mode / PNG IHDR remainder | Decoded RGB SHA256 |
| --- | --- | --- | --- |
| 1 | 1784 x 2400 | RGB; depth 8, color type 2, compression/filter/interlace 0/0/0 | 3e276d001943674ddc9d575cbb6db4bf296ef3192c9a874bbdb1b6b731d0b5f6 |
| 2 | 1782 x 2400 | RGB; depth 8, color type 2, compression/filter/interlace 0/0/0 | 3da0bb7a6c760569212ae5c61a2ab102ca060f29bddd65a9019231812d9b153d |

No claim about visual legibility, Bates reading, correct substantive rendering
or sensitivity clearance is made from these technical pixel comparisons.

## Separate rerender and actual commands

`mktemp -d /private/tmp/wtc7-co016-independent.XXXXXX` created
`/private/tmp/wtc7-co016-independent.H2iga1` (`cc4110`, exit 0).
An additive `apply_patch` created its `fonts.conf`, using the same two font
directories (`/System/Library/Fonts`, `/Library/Fonts`) but a new cache path
`/private/tmp/wtc7-co016-independent.H2iga1/font-cache`. The cache directory was
created with `mkdir` (`ab7f38`, exit 0). No global font configuration changed.
New configuration SHA256:
`323229848724944d97ee10af1614ca73f1964f3d825c8ee3bed816edb9e646f8`.

Exact rerender command, from `/Users/admin/docs/911`, login shell disabled:

```sh
FONTCONFIG_FILE=/private/tmp/wtc7-co016-independent.H2iga1/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 2 -png -scale-to 2400 /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/co016-control-review-2026-10-08/NYC-WTC_000171905.pdf /private/tmp/wtc7-co016-independent.H2iga1/NYC-WTC_000171905
```

Receipt `07c381`: exit 0, 0.614398208 seconds measured tool wall time, empty
captured output (no rendering diagnostic). Both output names were new. Full
pages 1 and 2 were rendered with maximum dimension 2400; no crop, rotation,
enhancement or source reconstruction was applied.

`pdftoppm -v` (`8d3e6f`, exit 0) reported Poppler 26.05.0. The entry point is
a shell wrapper that execs its bundled native binary; the wrapper was read
(`532dfd`) rather than mistaken for the renderer. Fingerprints from `bdb4ed`:

| Runtime artifact | SHA256 |
| --- | --- |
| dependencies/bin/override/pdftoppm | de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159 |
| dependencies/native/poppler/bin/pdftoppm | d9d81b176e8fd38d07f2fbf4f84c17dc991c6bac3730ff3cad3239c4fcbed892 |
| dependencies/python/bin/python3 | 2498a31965647f1507a53e391842b23c29d96f0ef4550475f34a1d2b30c23ddb |

The prefix is `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/`.
Inline structure, manifest and pixel checks used its Python executable with
`-B -`: Python 3.12.14, pypdf 6.10.0 and Pillow 12.3.0. No pycache or new
checker framework was created. `a5e547` performed copy/PDF/IHDR/decode checks;
`721b0e` compared both independently rendered files to the saved PNGs in bytes,
mode, dimensions and decoded RGB bytes, and rechecked all seven control/source
pins. Both exited 0. `shasum -a 256` supplied the explicit pre/post file pins.

**Shared-renderer limit:** this is a separate invocation, temporary output
directory and font cache, but the same Poppler implementation and system font
directories. Equal bytes/pixels demonstrate local repeatability, not agreement
between independent rendering engines, historical authenticity or content truth.

## Source manifest reconciliation

The new `source-manifest.json` was separately checked against the pinned
diagnostic and actual files (`c8a4b9`, exit 0). Its 2697 bytes have SHA256
`4c0be374280e53ecc3df025235ca1e7a85d36b82720daecb8d2311cbdb0de2d0`.
Assertions covered the exact two IDs/order, expected pages/sizes/Bates and URLs,
protocol/metadata hashes, acquired PDF identity, both page-derivative pins,
the missing document's null file/hash and unread state, population totals and
false complete-content/accepted-engine flags. Manifest bytes were unchanged
across that check. Transport outcomes were compared to the saved root log;
they were not independently reacquired. The manifest's content/sensitivity
assertions were not independently evaluated by this technical reviewer.

`source-log.md` was first read while provisional (`86c9bb`); its subsequently
appended retry/render section was read at `bd84ec`. The checked later snapshot
hash was `79ab0074cd4ae1c9481144c6c18f62ac810dbccd6d9d963c8be0bc49b862e740`
(`0d108b`). This is a snapshot of a root-owned execution log, not a requirement
that future append-only interpretation/review entries leave its hash unchanged.
Its initial aggregate diagnostic stopped at the missing second file; that
preserved root failure is not counted as a passing two-file admission check.

No new failure occurred in this technical rerender. Acquisition failures and
the preliminary metadata schema error remain visible. The existing source,
renders, reader notes and all gated DEP records were untouched. Only this
technical note and the explicitly authorized temporary rerender/configuration
were authored. Complete admitted-page readings and interpretive review belong
to their separate records; no human or engineering acceptance follows here.
