# Source, derivation and review receipts

October 4, 2026. Research copy only. The source is the exact catalogued official
[NYC-WTC_000174022 PDF](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000174022.pdf),
located through main `research/WTC7_archive_leads_2026-09-16.md` lines 83/104.
The catalog label is not substituted for the attachment labels observed in
the source. No confidentiality marking was observed on the three pages;
business contacts remain in the preserved source and are not transcribed here.

## Acquisition

The one permitted tool-reader open returned an internal/not-accessible error
(`turn744view0`), not a demonstrated server refusal. One separately declared
direct HTTPS GET then succeeded (`67252f`, exit 0): HTTP 200, application/pdf,
135742 bytes, zero redirects. No retry, neighboring-ID query or archive crawl
occurred. Root's temporary directory was created by `mktemp -d
/private/tmp/wtc7-fsk56.XXXXXX` (`3cd117`, exit 0).

```sh
curl --proto '=https' --connect-timeout 20 --max-time 60 --max-filesize 10485760 --fail --silent --show-error --dump-header /private/tmp/wtc7-fsk56.4NS5KF/response-headers.txt --output /private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000174022.pdf
```

Response headers were kept in temporary local storage, not printed, copied into
the repository or treated as content instructions. Bundled Python 3.12.14 and
pypdf reported three pages, no encryption, no AcroForm or OpenAction, and the
expected PDF signature (`f2dd7f`, exit 0). This is limited metadata screening,
not an exhaustive active-content audit or historical authentication.

## Root rendering and preservation

Bundled Poppler reported version 26.05.0. Both commands used
`FONTCONFIG_FILE=/private/tmp/wtc7-fsk56.4NS5KF/fonts.conf`; the configuration
names system font directories and the private `font-cache` path. Configuration
alone does not prove the cache existed or was used.

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -png -scale-to 2200 /private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf /private/tmp/wtc7-fsk56.4NS5KF/page
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 2 -l 2 -png -scale-to 4400 /private/tmp/wtc7-fsk56.4NS5KF/NYC-WTC_000174022.pdf /private/tmp/wtc7-fsk56.4NS5KF/readability
```

Each was run once, with stderr redirected respectively to `render.stderr`
and `readability.stderr` in the same temporary directory. Initial session
67561 ended at `341d97`, exit 0; the readability session 39789 ended at
`562819`, exit 0. Both stderr files have zero bytes (`69b030`, `19fdfb`).
Root recorded the need for page 2's single repeat before executing it and
before reading page 3. There was no crop, rotation, enhancement, graphical
measurement, OCR or extracted-text substitute. The image tool explicitly
resized the complete readability view to 2744 × 3680; saved-raster size and
displayed size remain distinct.

One scoped approved `cp -n` preserved the PDF, four PNGs, configuration and
two diagnostic files in this unit (`f944e2`, exit 0). A subsequent byte
comparison of all eight source/destination pairs passed (`a8fd64`, exit 0).
The original PDF was not re-exported or modified.

| File | Bytes | Saved image dimensions | SHA-256 |
| --- | ---: | --- | --- |
| NYC-WTC_000174022.pdf | 135742 | Three PDF pages | a2d7dc4ce0e26ac431e98691d387161657f989d1d685a300731aec3b8d79735f |
| page-1.png | 65514 | 1633 × 2200 | a40a3125d96a90e5f03bb19eeb10c270bf24aa3e6852e7b5e5753f63d795fde6 |
| page-2.png | 133902 | 1641 × 2200 | 4a8277c344339c5c3e92e5cc71876df1d3d1b567e22ae0557cad732bf9abc180 |
| page-3.png | 111977 | 1648 × 2200 | 5eebe37c8b9657b497886ab3d1b56687ee76db77b71b74d86949452a951972a3 |
| readability-2.png | 945816 | 3281 × 4400 | 63e3559dbfd6763a2895f45306e80fede115b73a78b55d556d22fc5bfe3d7028 |
| fonts.conf | 233 | Not applicable | 6ba64cd31e9b9080bb4dc654ce045dfa20691fe6bd86077bb7429df78f3d3e9c |
| render.stderr | 0 | Not applicable | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| readability.stderr | 0 | Not applicable | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

## Frozen readings and independent derivation

| Record | SHA-256 |
| --- | --- |
| PROTOCOL.md | 4552522ed7f5f54502ee4b864f94cda0e5ef5da70be3005edf450b511bd93bca |
| root-observations.md | de081ef05651a148a175d30b64ad33eed8505b35e1d3ee670660f62d982b0052 |
| review.md | 6d55ac425d5c424d944448e43fef09deb406c4f6d0b51b0617e3f34747436c1d |
| derivative-check.md | 68d28b63524fc7323d9ec68bb826992e91a5742d4a6e8c956bd1b60d9eb926b4 |

Root's observations were frozen at `6bfff7`, exit 0, before reading the other
reader's notes. The reader's subsequent text-only comparison (`13e1cc`, exit
0) and frozen-hash check (`91eeee`, exit 0) preserved the differing small room
label readings; no extra source view was performed. Root read the complete
independent notes at `a8fd64`, exit 0, and the derivative receipt at `840887`,
exit 0. A shared source, renderer or earlier context is not source independence.

The [independent derivative receipt](derivative-check.md) records separate
temporary output/configuration, actual commands, timing and all four successful
byte comparisons. Its three-page 2200 run ended at `0b89c1`, exit 0; its
page-2-only 4400 run ended at `193cac`, exit 0. Both stdout/stderr streams were
empty. A separate post-initial-run `stat` found the configured private cache
directory absent (combined check exit 1); that diagnostic was retained, not
called a render failure. The directory was explicitly created before the newly
authorized larger render. No initial render was repeated. The checker did not
view page content or validate root's display resampling.

Hash and byte equality establish preservation and reproducibility of these
local derivatives only. They do not establish historical completeness,
authenticity, engineering correctness, approval, installation or event-day state.

## Root completion checks (appended after synthesis critique)

The [text-only synthesis critique](synthesis-review.md) found no material
correction. Its reviewed report pin remains
`29d2d9aa26dd7d2dfb03056cbcce97cadb40d2c92e3bb9305d12619b610c2d4e`;
the critique itself is
`805374cb9c717a003a2a2d7ad39b9352e8d75fea21322eccba4fe362ebebd0be`.
Root confirmed both with `shasum -a 256` (`9aae61`, exit 0). This receipt-only
section was added after the critique of the earlier source-log snapshot; no
earlier acquisition or interpretation text was changed.

The subsequent [preserved-artifact verification](verification.md) independently
checked all eight preserved files against root's temporary originals and all
four images against the checker's renders: twelve byte comparisons, zero
mismatches. It also confirmed page count, dimensions and the four frozen pins.
Root read its complete receipt (`6e2222`, exit 0); the checker reported its
pin as `3de4f45d1435b16296c79b379ef8b80810308aac920cd64aa4ae507a0cceeb0b`.
Neither that check nor this completion entry involved another source view.

Root's stdout-only Python Markdown validation checked final newlines, trailing
whitespace and existence of relative/absolute Markdown link targets in the
seven then-existing unit Markdown files: seven files, six local targets, zero
failures (`775996`, exit 0). This excludes the later verification note and
this append; it is not a whole-repository link audit. `git diff --check`
separately passed (`108495`, exit 0; repeated `5c043a`, exit 0); untracked
unit files were covered by the separate Markdown check rather than Git's diff.

`git branch --show-current`, `git rev-parse HEAD`, and `git status --short`
confirmed the same research branch at
`ca1c223335c20905d6608eb15c676f88cbfac734` and the pre-existing research WIP
categories (`b0f2bc`, exit 0). Navigation and the deduplicated local feedback
entry were updated; these are not canonical promotion or external delivery.
The broad tracked diff also contains prior units and is not all this unit's
work. Nothing was staged, committed or pushed. The finite source-review unit
is complete; the comprehensive investigation and separate review gates are not.
