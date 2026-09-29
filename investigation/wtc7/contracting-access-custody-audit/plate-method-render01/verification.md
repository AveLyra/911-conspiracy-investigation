# Detailed plate-method source and derivative verification

September27,2026. Research only. Scope, results and exact source locators:
[primary-source follow-through](../plate-method-primary-followup-2026-09-27.md).

## Acquisition and identity

The three declared exact official URLs were retrieved to new files with
create-only `test ! -e` guards. Actual command form, with explicit absolute
destinations and the declared URL substituted:

```sh
curl --fail --location --max-time 60 --silent --show-error --output <new-file> --write-out 'HTTP %{http_code} TYPE %{content_type} BYTES %{size_download} FINAL %{url_effective}\n' <declared-url>
```

N5G returned session59787 and101088 returned94787; both were polled to terminal
exit0 before parsing. The861267 download completed directly with exit0.
All returned HTTP200 and unchanged final URLs. N5G type was `application/pdf`;
the papers were `application/pdf;charset=UTF-8`. These are public-acquisition
results, not historical authentication or evidence that the described runs ran.

| Preserved source | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| `../ncstar-1-5g-source01.pdf` |29847167|340|`f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea`|
| `../prasad-101088-source01.pdf` |761491|8|`2bcbf4cb442d180c485e971ea504c4a3a17c21f618fd4c0e8b22aa60872d1019`|
| `../prasad-861267-source01.pdf` |761491|8|`2bcbf4cb442d180c485e971ea504c4a3a17c21f618fd4c0e8b22aa60872d1019`|

All three PDFs are unencrypted. Root's direct `cmp` exited0 for the two papers;
the independent verifier also used `filecmp.cmp(..., shallow=False)` successfully.
N5G matches the prior recorded pin; the paper matches the recorded prior101257
pin. The101257 endpoint was not freshly downloaded or directly compared.

## Page declaration and rendering

Initial N5G locator text: physical1,3,7–12, within the declared1–16 front
matter. Each paper initially physical1 only. Before substantive extraction,
root declared N5G3,7,8,73–98 and one representative paper1,5–8. The former body
range is complete Chapter3, printed29–54; no Chapter4/appendix or original
structural drawing-page review is implied. The byte-identical861267 copy was
not redundantly rendered.

Bundled tools used:

- Python `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,3.12.14, with `-B`.
- pypdf6.10.0; Pillow12.3.0.
- Poppler `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`.
- Existing `../protection-render01/fonts.conf`.

For each of the34 selected pages, the create-only guarded rendering had this
form with explicit absolute paths:

```sh
FONTCONFIG_FILE=<existing-font-config> <bundled-pdftoppm> -f <page> -l <page> -r 160 -singlefile -png <source-pdf> <this-directory>/<prefix>
```

The batch returned session58464 and was polled to terminal exit0 with no
diagnostics before image review. Output names are `n5g-3`, `n5g-7`, `n5g-8`,
`n5g-73` through `n5g-98`, and `paper-1`, `paper-5` through `paper-8`, all PNG.
No output was overwritten. These are full-MediaBox renders, with no CropBox
flag. No rendering replay is claimed.

## Independent artifact verification

The separate verifier ran one read-only stdout-only inline command using the
bundled `python3 -B -`; terminal exit0, no diagnostics. It checked all source
sizes/hashes/page counts/encryption states and direct paper equality. Only
the selected pages' geometry was inspected, not PDF content. All selected
MediaBoxes equal CropBoxes and page rotation is0.

All34 PNGs passed Pillow `verify()` and a fresh-open full `load()`: PNG,RGB,
single frame. Their dimensions agree with the selected MediaBoxes at160dpi:

| Dimensions | Count |
|---|---:|
|1247×1687|1|
|1247×1689|1|
|1247×1712|14|
|1247×1700|13|
|1080×1600|5|

All37 source/derivative artifacts retained size,mtime and SHA-256 before/after
the check. This verifies decoding and dimensional correspondence, not an
independent image-to-PDF content comparison or scientific validation.

## Actual visual review and limits

Root displayed all34 complete pages across the interruption: N5G3,7,8,73–84
before the user-coordinate reply, then85–98 and paper1,5–8 after resumption.
The pages were readable for the reported findings. Several matrix pages are
printed sideways; their axis headings and captions were retained. Dense
trace labels were not exhaustively resolved; no numerical tracing, coordinate
measurement, interpolation or simulation occurred.

The separate source reader inspected full images N5G78–88,93 and paper1,5–8
(17 total), freezing findings before root's new synthesis. It then read the
two preceding audit notes for disconfirming/favorable evidence. This is
prior-informed computational source review, not an independent experiment,
licensed engineering certification or historical authentication.

All download/render handles above are terminal. No process, viewer, model
execution or human acceptance remains claimed live on the strength of a file
or old session record. Private sources, main/canonical/legal records and old
annotations were not changed by this unit.

## Final integration checks

The source reviewer read the first complete draft and corrected a Fig3-8 page
locator and the gap-boundary wording. It verified those corrections and six
local targets; no remaining issue within its17-page coverage. The originating
search/artifact navigator separately checked the account of its own work,
not another independent acquisition: six note/receipt local links resolved,
ten external/fragment targets skipped, bundled `python3 -B -` exit0.

Root ran `awk` across seven touched Markdown files for trailing whitespace
and conflict markers: no issues. `wc -c` and `shasum -a 256` matched all three
source pins above; a fresh `cmp` of the papers exited0. `git diff --check`
passed, and branch/HEAD remained `research/sherlock-wtc7-investigation` /
`2fab1389ba8529494dd206a948014cd41cbf97d2`. Main's tracked dirty-file names
were unchanged; this does not claim a byte-level audit of other agents' files.
No new PDF-content parsing or render replay was performed for these final
checks. One unmatched patch attempt changed nothing before the explicit save.
