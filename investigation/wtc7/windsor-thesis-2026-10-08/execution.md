# Thesis acquisition and reading execution

October 8, 2026. Research-only continuation of the frozen protocol. The earlier
goal turn made progress by acquiring the original thesis; the intervening
acoustic explanation added no new measurement. This unit resumes existing
work, not the closed IPB article route. No scientific model was executed.

## Original acquisition

The exact [Edinburgh record](https://era.ed.ac.uk/items/2ca19958-abdd-42f6-8c03-6775017f9690)
opened successfully through the web reader, followed by its openly linked
[thesis file](https://era.ed.ac.uk/bitstreams/4f9ade1c-384a-42d6-b863-e1de2cd5657c/download).
The acquisition's exact identifier is also retained in the command and headers.

One ordinary HTTPS preservation GET, with no-overwrite guards, ran:

```sh
test ! -e fletcher-2009-thesis.pdf && test ! -e thesis.headers &&
curl --fail-with-body --location --proto '=https' --connect-timeout 15 \
  --max-time 60 --max-filesize 33554432 --dump-header thesis.headers \
  --output fletcher-2009-thesis.pdf \
  --write-out '\nstatus=%{http_code} bytes=%{size_download} type=%{content_type} url=%{url_effective}\n' \
  'https://era.ed.ac.uk/bitstreams/4f9ade1c-384a-42d6-b863-e1de2cd5657c/download'
```

Work directory was this unit. Tool receipt `61232d` yielded session `18123`;
polling that same handle produced receipt `90c078`, exit 0, HTTP 200,
4,425,293 bytes, `application/pdf;charset=UTF-8`. The server's normal redirect
ended at `https://era.ed.ac.uk/server/api/core/bitstreams/4f9ade1c-384a-42d6-b863-e1de2cd5657c/content`.
This was not another source/client attempt after an origin denial. Original
SHA256 is `4066628f6c6a8b13f7fef63e1602a1b3eae807acbac7f032b67e68c1718a1543`.
Headers and the earlier reader representations remain separate files; their
hashes establish captured-byte identity, not independent historical testimony.

`pdfinfo` reported 207 pages, PDF 1.4, A4, unencrypted and no JavaScript. It also
emitted `Unknown Metadata type '???'`; that metadata diagnostic is retained,
not described as a clean metadata parse. The title page and institutional
metadata identify Ian A. Fletcher, May 2009; source metadata differs between
“subject” and “subjected.” Neither parser metadata nor a hash alone proves
authorship. No additional download, login, fee, contact or mirror search was
performed. Earlier catalogue/article-route failures remain unchanged.

## Frozen coverage and local recovery

[PAGE-SELECTION.md](PAGE-SELECTION.md) froze 61 full pages after contents and
literal locators, before substantive reading. [SCOPE-EXPANSION.md](SCOPE-EXPANSION.md)
then prospectively added 16 complete context pages after root's initial reading.
The final 77-page roster is physical 1, 11–15, 33–34, 81–94, 114–154, 161–162,
166–171, 197–202. No complete-thesis or appendix review is claimed.

The first attempt to create a worktree render directory failed under the
default sandbox. The orchestration erroneously continued into eight rendering
jobs. Every job failed with exit 1, fontconfig/cache diagnostics and inability
to write its image. All eight same handles reached terminal state before any
recovery. [Failed receipts](failed-render-receipts.json) retain the available
initial/terminal tool strings and their truncation metadata; they are not
complete raw stderr files. No successful image or source-content review came
from those jobs. This was a local orchestration/environment failure, not a
source defect or an access denial by the thesis repository.

Recovery created `/private/tmp/windsor-thesis.mXK0Gu` with `mktemp -d` and
authored a fontconfig file using `apply_patch`, retaining the existing system
font directories and using a cache inside that temporary directory. This
avoided writing to main or changing system configuration. The source stayed
read-only. A single title-page preflight completed with exit 0 and empty
combined tool output (session `41646`; receipts `c12dc1`/`f210b8`); its image was
visually inspected before launching more pages. See
[title receipt](render/title-render-receipt.json): separate raw stdout/stderr
streams were not captured for that preflight.

Subsequent range jobs used this command shape:

```sh
FONTCONFIG_FILE=/private/tmp/windsor-thesis.mXK0Gu/fonts.conf \
FONTCONFIG_PATH=/private/tmp/windsor-thesis.mXK0Gu \
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm \
  -f FIRST -l LAST -r 110 -png fletcher-2009-thesis.pdf \
  /private/tmp/windsor-thesis.mXK0Gu/page
```

Exact absolute commands and return statuses are saved in
[initial receipts](render/render-receipts.json) and
[expansion receipts](render/expansion-render-receipts.json). Python's standard
subprocess wrapper imposed 60 seconds per range, captured each stdout/stderr to
separate files, and gated subsequent ranges on exit 0. All nine jobs completed
with exit 0 and zero stdout/stderr bytes. Session `11348` completed via the same
handle (`636419`/`739287`); expansion `9882` likewise (`c2fc84`/`5dba7b`).

Approved worktree writes preserved the initial scratch directory under
`render/` (`edc9c8`), then 21 new expansion images/log/receipt files without
overwriting existing files (`a489d1`). The copied cache is incidental; it is not
evidence or an input-authenticity attestation. The copied fontconfig retains
its original temporary cachedir; future reproduction needs an existing writable
cache, not an assumption that a temporary path is permanent.

Runtime discovery reports bundle 26.1007.11041. Poppler is 26.05.0; bundled
Python and pypdf supplied text/metadata assistance. Full-page images, not text
extraction alone, controlled both readers' source interpretation. The
independent integrity record pins its actual executable and library versions.

## Reading, comparison and limits

Root's 77-page reading was frozen in [root-notes.md](root-notes.md), SHA256
`637d76f1e68a070a6abb9046632c8f604abbd74d8038f76481d828e5eca5caa5`, before
the observer's findings were read. The observer completed the same 77-page
roster and froze [observer-notes.md](observer-notes.md), SHA256
`50c36be05cb713111f14d216057b4b2e6cd9674105fd6d0cb18e79bb004feaac`, before
reading root's findings. Root then read the complete peer note and verified
both freeze hashes (`0a4159`, `e51017`, `ddde06`); an earlier truncated attempt
was not counted as a complete read. [Review](review.md) records their agreement,
the subsequent draft critique and the changes actually adopted.

The separate preservation reviewer did not read either scientific interpretation
before independently rendering all 77 pages. Root read the preserved driver
and independently compared all held/fresh PNG bytes and decoded RGB arrays
(`df235c`, `0e5483`): all 77 pairs matched. The reproduction's driver, configuration,
start/final receipts and 20 log files were copied without overwriting into
`independent-render/` (`be55b3`, exit 0). No duplicate fresh PNG set was added
to the worktree. The [integrity review](integrity-review.md) states the limits
of same-renderer reproduction. Historical scratch paths are not guaranteed
permanent or automatically reusable.

The prior substantive goal turn made **progress** through acquisition,
full-page readings and render reproduction; the intervening acoustic answer
added no historical measurement or repository result. This closeout addresses
critical review, preserves the artifact manifest and updates navigation. Its
observable acceptance criteria are separate outcomes for depth definition and
mesh evidence, a complete 77-page roster and its receipts, unchanged source
and reading freezes, and no unsupported causal or acceptance-state promotion.
Final checks and their limits are recorded in [validation](validation.md).

No new thermal equations, graph values or response percentages were calculated.
Numerical results in the source comparison are attributed to the thesis,
not represented as reproduced native simulations. The original 2007 audit and
2008 access records were read for lineage, not rerun or overwritten. No main,
legal, raw-record, accepted Sherlock/Faraday, human-review or publication state
changed. No commit or push occurred. The bounded source review cannot finish
the broader charter or establish a WTC 7 cause ranking.
