# Design and sprinkler source receipts

October 4, 2026. Research only. Main AGENTS/WORKFLOW/START-HERE/CHARTER pins
match the fully read prior controls (`f6a704`, exit 0). The intake script
confirmed the same research branch, ca1c2233 HEAD and intentional research WIP.
The selected source PDFs are not canonical litigation facts or accepted
Sherlock findings. Routine business contacts/signatures remain in originals;
no contact details or internal paths are copied to software feedback.

## Selection and catalog correction

Exact public source URLs, read from the main archive-lead catalog:

- https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000167235.pdf
- https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000167873.pdf
- https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000171300.pdf

The initial row-based intake misinterpreted folder totals as expected combined
PDF lengths. The catalog introduction, read at `dca55e`, exit 0, expressly
identifies each URL as the **first document** for a multi-document folder.
The protocol is retained unchanged and the correction was recorded before
root advanced from its first primary page. Actual lengths 2/1/1 are within
the declared caps. Four-page file coverage is not nine-page folder coverage;
no download failure, missing-page anomaly or withholding follows from that
count difference. Other documents in the two multi-document folders remain
unreviewed. This was our selection-metadata error, not a source defect.

## Acquisition and admission

All three permitted tool-reader opens returned internal/inaccessible errors
(`turn746view0` through `turn746view2`), not demonstrated server refusals.
One approved direct GET per exact URL then succeeded. Root scratch was made
by `mktemp -d /private/tmp/wtc7-design-sprinkler.XXXXXX`, resulting in
`/private/tmp/wtc7-design-sprinkler.5CKjlR` (`a99f6e`, exit 0).

Each command used the following pattern, substituting only the three literal
identifiers above, with no retry, redirect or neighboring-ID request:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 --max-filesize 10485760 --fail --silent --show-error --output /private/tmp/wtc7-design-sprinkler.5CKjlR/NYC-WTC_000<ID>.pdf --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000<ID>.pdf
```

User curl configuration was disabled. No headers/cookies/credentials or case
payload were sent or captured. All responses were HTTP 200, application/pdf,
zero redirects. Original handles were polled to terminal completion.

| Source | Terminal receipt | Bytes / actual pages | SHA-256 |
| --- | --- | --- | --- |
| 167235 | 55175 / `6c577d`, exit 0 | 79607 / 2 | e05450bbef04fc1df6005a97233ca8c341f900033f425131686592f2feb9dbd7 |
| 167873 | 22805 / `cb4708`, exit 0 | 40327 / 1 | 21dfad1a9da62a6e88869612309277f386f6600e54dfa34889ef4da8975e8b3d |
| 171300 | 38526 / `7ab1a1`, exit 0 | 84808 / 1 | 8643cab6ed8e8c0caff7cd23c73b1841f6bf6f85a90415786cdf92de530db841 |

Python 3.12.14/pypdf admission (`e64a81`, exit 0) confirmed PDF signatures,
these page counts, no encryption and no AcroForm/OpenAction. This is limited
metadata screening, not an exhaustive security or historical-authenticity
audit. Root observed no confidentiality marking on the four complete pages.

## Root derivation and preservation

A new apply_patch-created fonts.conf names `/System/Library/Fonts`,
`/Library/Fonts`, and a task-specific private font-cache directory explicitly
created before rendering. Root configuration SHA-256:
9140b64fe32bf7d3deb826f09819f6fc0c74d93e6f6ffdf629ba670e01e8cddd.
Directory/configuration existence does not prove the renderer used a cache.

With FONTCONFIG_FILE set to `/private/tmp/wtc7-design-sprinkler.5CKjlR/fonts.conf`,
each source was rendered once using bundled Poppler 26.05.0:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l <actual-page-count> -png -scale-to 2200 /private/tmp/wtc7-design-sprinkler.5CKjlR/NYC-WTC_000<ID>.pdf /private/tmp/wtc7-design-sprinkler.5CKjlR/<ID>
```

Actual page counts were 2, 1 and 1. A Python subprocess wrapper separately
captured stdout, saved `<ID>.stderr`, and checked each process return code.
Session 46748 ended `e0c7fd`, exit 0; all three renderer exits were 0 and each
stdout/stderr stream empty. Elapsed seconds: 3.376, 1.480 and 3.595. No source
was rerendered, re-exported, OCRed, rotated, cropped, enhanced or measured.

| Image | Bytes | Saved size | Root display size | SHA-256 |
| --- | ---: | --- | --- | --- |
| 167235-1.png | 132640 | 1645 x 2200 | 1363 x 1824 | 92a2268c2ec12afbc4231721852ea6a96bf5fcd9ccc57f6fdb6899b028f129de |
| 167235-2.png | 68763 | 1649 x 2200 | 1367 x 1824 | 6802e3137dd2ee20992c542ae7f55470cf1fa6490d2b1251207c9c22d329c5d9 |
| 167873-1.png | 78966 | 1645 x 2200 | 1363 x 1824 | cbc7813ddd99bd8126855b681c5bd852969d1a203f921c449f479e38c62372c8 |
| 171300-1.png | 196764 | 1639 x 2200 | 1359 x 1824 | 8172f42bb17102ead5eb705ea7163cc0ca5e1c03b1854869f31f2b7d98c270b1 |

Root's `shasum`, `file` and `wc -c` checks returned these values at `dca55e`,
exit 0. Four whole-page original-detail views were requested; the tool
explicitly reported the smaller displayed sizes above. No native-size display
or repeat is claimed.

One approved `cp -n` preserved eleven files in this unit: three PDFs, four
PNGs, font configuration and three diagnostic files (`510bdb`, exit 0).
Each diagnostic file is empty, SHA-256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
An explicit eleven-filename `cmp -s` loop matched every preserved file to its
temporary original (`8b1f8d`, exit 0): eleven pairs, zero failures.

## Frozen readings and independent reproduction

Protocol: 57abb5f9c48443dd9defe9972f1cc9779190c23a8cc32733685f1e1149e716d8.
Root complete observations froze at `2e3d7e`, exit 0, before peer content:
a3e92d7c11bfcaa596ee1f9c05978b4e6f22c65bb868bd48d9b7f7a3505e7741.

The [independent derivative receipt](derivative-check.md), fully read at
`0949e7`, exit 0, records separate configuration/cache/output, three successful
renderer processes, all four matching image pairs and unchanged source-after
pins. Its hash is
b37b1250c93707324f23a1a506e0fc5964b74dbdffdae42cec78230cce7e6478.
No source content was viewed by that checker. Shared-renderer agreement is
derivative reproducibility, not historical authenticity, folder completeness,
source-content agreement or performed engineering work.

Independent reading froze at `ec5bb9`, exit 0, with SHA-256
507903af2f5dd36a1e1339718d4755942fc88063ec320d385c29004c70c1633b.
The peer then read root's complete notes at `be026c`, exit 0, and verified
the root freeze at `3b1f5d`, exit 0. Root read the entire independent record
at `f38470`, exit 0. No material disagreement was found. Both readers used
four first full-page views, with no repeat or additional primary source.
The peer did not receive explicit resize notices; absence of that notice is
not confirmation of a native-size display. The catalog-scope correction was
communicated before the peer's views, after root's first page, and is not
independent confirmation of the metadata by that reader.

## Final synthesis and verification

The [text-only critique](synthesis-review.md) found no material correction to
the report. It adds one precision note to the peer's frozen shorthand:
"unaccepted quotation" means acceptance is not shown in the held copy, not
that acceptance never occurred. The original reading is preserved; the report
already states the narrower conclusion. Root read the complete critique and
confirmed its pin at `c2c94c`, exit 0:
3ae3b1c44257cc753efb33275d7ca32e9a6bb9fde59ef3544169fb59aff3e059.
The reviewed report remains
b38eedd5fbfe6f7495dda09a75c353e1f373cc60e88f0e57704cc5e26af2806c.
This receipt-only append follows review of the earlier source-log snapshot;
its prior acquisition and reading record is unchanged.

Root ran `shasum -a 256 -c` against fifteen fixed pins: protocol, two frozen
readings, derivative receipt, three PDFs, four PNGs, configuration and three
empty diagnostic files. All fifteen passed. A stdout-only Python check of
the seven unit Markdown files found final newlines, no trailing whitespace,
and all nine then-present local link targets. `git diff --check` completed in
the same `set -e` command; entire receipt `d7cf5a`, exit 0. This is local
integrity/formatting verification, not a legal or engineering acceptance test;
it predates this receipt-only append.

Branch/HEAD/status check at `c2c94c`, exit 0, confirmed the same branch and
ca1c223335c20905d6608eb15c676f88cbfac734 HEAD with existing research WIP.
Research navigation now distinguishes complete-file from incomplete-folder
coverage and names the next metadata lookup. SFB-005 records the catalog-grain
lesson generically. A fresh two-page archived-thread query found the exact
designated Sherlock chat still archived on its second fifty-entry page; no
send, unarchive or replacement was performed. That classification comes from
the archive list, not the chat's `notLoaded` field. No sensitive source payload
was transmitted. Source preservation, frozen inputs, main/legal boundaries
and separate human-review gates remain intact. No stage, commit or push.
This four-page review is complete; the full investigation remains incomplete.
