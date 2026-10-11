# Independent change-order derivative check

October 4, 2026. All ten initial page rasters reproduce exactly.
**Complete declared coverage: ten used rasters, zero larger repeats.**
This verifies local derivation with the same renderer, not historical
authenticity, visual readability or engineering validity.

## Scope and pinned inputs

Read the complete protocol and acquisition-only source log, plus the PDF
skill. Main AGENTS/WORKFLOW/CHARTER hashes match the previously read controls.
Applied evidence/source-preservation boundaries. No page/image content or
root/peer reading notes were viewed; no network, OCR, crop, rotation, source
edits, Git or engine actions. Only this new note and private scratch outputs
were written. Existing source, protocol and frozen files remain untouched.

Protocol SHA-256:
`a30522242bbe2612c2ee451d485faf9eb5225ed3eb2fae33420092a199e192ae`.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/change-order-review
T=/private/tmp/change-order-derivative.lOXvWQ
R=/private/tmp/wtc7-change-order.S8QUPu
P=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm
I=/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo
```

Each source is `U/NYC-WTC_000<ID>.pdf`. `shasum -a 256` and `wc -c`
matched the declared pins/sizes before rendering (`5329af`, exit 0); all
four hashes matched afterward (`055cca`, exit 0). Total bytes: 709482.
Separate `$I <source>` metadata calls each exited 0 with empty stderr,
reporting PDF 1.5, no encryption and the page counts below (`1cfbf7`).
Only page-count/encryption/size/version fields were printed, not content.

| ID | Pages | Bytes | SHA-256, unchanged before/after |
|---|---:|---:|---|
| 168580 | 1 | 41911 | `d6c8b161f3008b5c667fb7a2aa799d6b887a2ec2da9e9159a58f547d79465727` |
| 168581 | 1 | 48367 | `6a5ac540b874575944f6350f808a55ebf70c41e2a9b30f6049e4183298032c71` |
| 171840 | 6 | 374954 | `f5da0371e474998eaf37220836e261c8de2c437fcb1dd911533761391ae17a35` |
| 173920 | 2 | 244250 | `2d06a8d40c8a8b3433e25509211110165c3ddc7d1e78a383e706803684dc3652` |

## Renderer and actual executions

`mktemp -d /private/tmp/change-order-derivative.XXXXXX` created `T`
(`5cd857`, exit 0). Wrote its own `fonts.conf` with `apply_patch` and
explicitly created `T/font-cache` using `mkdir` (`9b2bf5`, exit 0).
Configuration uses `/System/Library/Fonts`, `/Library/Fonts`, `fonts.dtd`
and only the private cache. Checker config SHA-256:
`aff58058a66a3b48eb9f286e9cb480a661fe889def300d56ed7ba09e2243419f`.
Root config SHA-256:
`840f4f2d8250c416cdf06e6556e442b34b0b5d825c800f79297c70fcd0915c50`.
`diff -u "$R/fonts.conf" "$T/fonts.conf"` returned expected exit 1
(`a00ba6`), showing only the cache-path difference. `$P -v` reported 26.05.0.

Each command below ran exactly once, in a separate subprocess with individually
saved diagnostics. The four PDFs rendered concurrently; pages within each
PDF followed physical order. Original live handles were polled to terminal,
not restarted.

```sh
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2400 "$U/NYC-WTC_000168580.pdf" "$T/168580" >"$T/168580.stdout" 2>"$T/168580.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 1 -png -scale-to 2400 "$U/NYC-WTC_000168581.pdf" "$T/168581" >"$T/168581.stdout" 2>"$T/168581.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 6 -png -scale-to 2400 "$U/NYC-WTC_000171840.pdf" "$T/171840" >"$T/171840.stdout" 2>"$T/171840.stderr"
FONTCONFIG_FILE="$T/fonts.conf" "$P" -f 1 -l 2 -png -scale-to 2400 "$U/NYC-WTC_000173920.pdf" "$T/173920" >"$T/173920.stdout" 2>"$T/173920.stderr"
```

Each Python subprocess wrapper saved the expanded command, UTC start/end,
monotonic elapsed time, actual renderer exit and wrapper streams in
`T/<ID>-receipt.json`, then propagated the renderer exit code.

| ID | Start UTC | End UTC | Seconds | Handle / terminal receipt | Renderer exit |
|---|---|---|---:|---|---:|
| 168580 | 22:43:35.349595 | 22:43:39.372690 | 4.022487 | 35171 / 361820 | 0 |
| 168581 | 22:43:35.354179 | 22:43:39.494070 | 4.139825 | 33062 / 515fe4 | 0 |
| 171840 | 22:43:35.353547 | 22:43:51.792991 | 16.438238 | 95154 / 1c5ead | 0 |
| 173920 | 22:43:35.357992 | 22:43:45.610841 | 10.252742 | 40918 / 714ad8 | 0 |

All wrapper streams are empty. All eight separately saved renderer stdout/
stderr files are zero bytes and have the empty-file SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
No warning was emitted. Individual receipt SHA-256 values:

| Receipt basename | SHA-256 |
|---|---|
| 168580-receipt.json | `874678990d8028745a36c6e4e96c0196f6569c6cf04aeab2b63b35b3058e7a5d` |
| 168581-receipt.json | `505ef0067601e5fd0b043510f4e58ef46e35bd57b9f8c9e91267218bfbbe34cd` |
| 171840-receipt.json | `64381ebebab4e5fbd9dcd824c3595bbd676a35356682d74067b453f9e7ba9d5b` |
| 173920-receipt.json | `7c7cdbdc64e5d543dc063f2d73366647d675993179ebefe46e3685151d33d4b7` |

## Complete initial comparison

Root reported all four root renders terminal exit 0 and the ten outputs ready
before comparison. Those root execution facts are attributed, separate from
the independently observed executions above. Every checker handle was also
terminal before comparing.

Actual checks (`055cca`, exit 0): explicit `cmp -s "$T/$name" "$R/$name"`
for all ten basenames below, reporting each return code; `shasum -a 256`
on both copies; `file` on both copies' headers; `wc -c` on fresh images and
diagnostics. `find "$T" -maxdepth 1 -type f -name '*.png' | wc -l` counted
exactly ten images. All comparisons returned 0; matching bytes also establish
equal size. All headers report 8-bit RGB, non-interlaced.

| PNG basename | Dimensions, both copies | Bytes per copy | SHA-256, fresh and root |
|---|---:|---:|---|
| 168580-1.png | 1761 x 2400 | 114523 | `8a1d73e944986808638412e03a2d9ec574f03e3f7c40386841cc2e8892886d4e` |
| 168581-1.png | 1757 x 2400 | 129665 | `eae2c90bc20fbdfd76575a8fb88f5252f88a7ac7bc792f6ec824cae7b58c34d6` |
| 171840-1.png | 1783 x 2400 | 119689 | `56f488e3c84ab8f6899b4c35387acf662d4d209439e118656b2a8edc4f194ee8` |
| 171840-2.png | 1773 x 2400 | 137430 | `bb3e127f500518ea9953a492cc1011791c87320f2d817add96376574f0f5f6c9` |
| 171840-3.png | 1780 x 2400 | 170597 | `5faef93360951a97987f3a4a3a4cd878f3a25bcc68a63a1fb25f9efaa0c0cebc` |
| 171840-4.png | 1773 x 2400 | 137814 | `d3f8ad98bd0e5555314f01abf4265ea201abe23822d79eafa96c93e38972adff` |
| 171840-5.png | 1781 x 2400 | 217240 | `e54bdffe723b1d38172bc98d6e7e2ce654721e92ffba870569a8e14e29cc46d8` |
| 171840-6.png | 1785 x 2400 | 204403 | `4e4a319203cf2a615360a900c8f5975692dbb10139a0b0519bc5008a4f4589f5` |
| 173920-1.png | 1787 x 2400 | 231664 | `deaa8049744354e1b076415e58b9d176f75196c57768d095524efa20fc2ebdc1` |
| 173920-2.png | 1774 x 2400 | 223635 | `8e184a9a1380dd93ed17b562f109e19caca1f47fefdaa2ab31b81e3c480cbbc5` |

Total fresh initial PNG bytes: 1,686,660. No missing page, source-pin change,
renderer failure or byte/dimension mismatch occurred. Scratch files and
receipts are retained; temporary storage is not a durability guarantee.

## Preserved-copy integrity

After root reported the no-overwrite preservation copies complete (`4b1e42`
and `5cc551`, exit 0), the checker compared the nineteen exact files in `U`
with their same-basename root scratch copies in `R` (`8a69e4`, exit 0).
The explicit list comprised the four source PDFs above, `fonts.conf`, the
ten PNG basenames above and `{168580,168581,171840,173920}.stderr`.
Each `cmp -s "$U/$name" "$R/$name"` returned 0: nineteen pairs, zero
failures. All four saved root stderr files measured zero bytes. Fresh hashes
of the preserved PDFs and root font config matched the pinned values above.
The preserved PNGs are therefore also byte-identical to the independently
rendered copies through the ten completed scratch comparisons.

The checker performed no copy or overwrite of those artifacts. Source pins
remain unchanged across its own checks. Root's use of no-overwrite copying
is an attributed execution report; post-copy equality alone cannot prove
the historical copying method or that an earlier destination never existed.
No claim of independently observing root's copy processes is made.

## Final coverage and limits

Root confirmed both readers completed ten initial full-page views each,
with zero larger repeats; the used-raster set is closed. Those viewing facts
are attributed reports, not observations by the checker. All ten declared
rasters have actual successful process and comparison coverage, with no
repeat gap. No larger raster was rendered by the checker, no further render
is authorized in this unit, and no checker process remains live.

The final verified result is four renderer exits 0, eight empty renderer
stream files, unchanged source/config pins at the recorded checks, ten exact
PNG comparisons with matching dimensions, and nineteen exact preserved/root
artifact comparisons. No failed render or comparison was omitted. The
configuration diff exit 1 is the documented expected private-cache difference.

Shared Poppler and fonts can reproduce a common renderer defect. No visual
correctness, legibility, viewer-display geometry, historical authenticity,
engineering adequacy, construction, inspection or human acceptance was tested.
Source and output identity do not establish independent historical evidence.
