# Hatch source and execution receipts

October 4, 2026. Research only. Main AGENTS, WORKFLOW, START-HERE and CHARTER
pins matched the preceding intake (`3d5a86`, exit 0); WORKFLOW and START-HERE
were reread, and the full charter was reread without truncation at `e880fa`,
exit 0. Branch remains research/sherlock-wtc7-investigation at
ca1c223335c20905d6608eb15c676f88cbfac734 with pre-existing research WIP.

## Acquisition and admission

Official locators are the main archive-lead catalog lines 81/102 and 88/109:
[172163](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000172163.pdf)
and [171497](https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000171497.pdf).
The two permitted tool-reader opens failed internally as inaccessible
(`turn745view0`, `turn745view1`), not demonstrated server refusals. One direct
GET per target then succeeded. No retried source, redirect, neighbor guess,
credentials, private query payload or external case upload was used.

`mktemp -d /private/tmp/wtc7-hatch.XXXXXX` produced
`/private/tmp/wtc7-hatch.7raRXT` (`e58d91`, exit 0). Both commands used this
same explicit pattern, with literal identifiers 172163 and 171497:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 --max-filesize 10485760 --fail --silent --show-error --output /private/tmp/wtc7-hatch.7raRXT/NYC-WTC_000<ID>.pdf --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000<ID>.pdf
```

`-q` disables user curl configuration. No response headers or cookies were
collected. HTTP outcomes were 200, application/pdf, zero redirects: session
57272 ended `65d26b`, exit 0, 49507 bytes; session 87848 ended `1cadc3`, exit
0, 69607 bytes. Original handles were polled rather than restarted.

Python 3.12.14/pypdf admission (`cad963`, exit 0) found each new PDF one page,
unencrypted, with a PDF signature and no AcroForm or OpenAction. This is
limited screening, not a complete active-content or historical-authenticity
audit. No confidentiality marking was observed in the complete page readings.
Business contacts and internal authoring paths are not transcribed into notes.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| NYC-WTC_000172163.pdf | 49507 | 163f7e8a65d719ec14affd8591faea94b425abe1424941ca57309086d2735ee2 |
| NYC-WTC_000171497.pdf | 69607 | 62fb129a8860774a6ffd624915ffd0461340e6dfe4113b7d3227993d1d1ba433 |
| ../followup/NYC-WTC_000172166.pdf | 147759 | 362ad11e3e7b5ac89183be9fa0095f2b0803518e3c854a77ae34f8e626012193 |

The held source pin matched its prior source log at `e58d91`, exit 0. Only its
first physical page was newly selected; the two-page original was not changed
or recopied. Differing new/held PDF hashes are not a substantive-text test.

## Rendering and preservation

Root created `fonts.conf` with apply_patch, using `/System/Library/Fonts`,
`/Library/Fonts`, and `/private/tmp/wtc7-hatch.7raRXT/font-cache`. The private
cache directory was explicitly created before rendering. Configuration hash:
750e12a1eaf4793b05c1fb53e0dcb43b6fec6a99992c8997aece31cec052d446.
Configuration and directory existence do not by themselves prove cache use.

With that file set as FONTCONFIG_FILE, root used the bundled executable:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 1 -png -scale-to 2200 <source.pdf> /private/tmp/wtc7-hatch.7raRXT/<ID>
```

Source IDs in order were 172163, 171497 and held 172166. Poppler reported
26.05.0. A Python subprocess wrapper executed each once, separately captured
stdout and `<ID>.stderr`, and checked actual return codes. Session 25940 ended
`6d1cd3`, exit 0; all three renderer exits were 0 with zero stdout/stderr bytes.
Elapsed times were 1.774, 2.783 and 2.264 seconds. No repeat, crop, rotation,
OCR, enhancement or measurement occurred. No PDF was re-exported.

| Image | Bytes | Saved dimensions | Root displayed dimensions | SHA-256 |
| --- | ---: | --- | --- | --- |
| 172163-1.png | 91382 | 1636 x 2200 | 1356 x 1824 | 63cae1c65bae835e2442cc5e3f099cf27682352bb181473f855f545460ca8079 |
| 171497-1.png | 132625 | 1630 x 2200 | 1374 x 1856 | fb8ecc896037b46300c7d7a82c04b05ccf13da77f81f56f7d4a3678b54cb54fb |
| 172166-1.png | 96193 | 1636 x 2200 | 1356 x 1824 | d549de24f49df4b55332212d8e1b1e7d28e54a75b6d3732bcfb8334b4cd5b543 |

`shasum`, `file`, and `wc -c` confirmed root's saved images (`bec253`, exit 0).
Each requested original-detail display explicitly reported resizing. A complete
page was displayed, not native-resolution pixels or a graphical measurement.

One approved `cp -n` preserved exactly nine files in this unit: two new PDFs,
three images, configuration and three empty stderr files (`ca45b9`, exit 0).
An explicit `cmp -s` loop checked all nine against temporary originals with
zero failures (`1f5b3b`, exit 0). The three empty diagnostics each have SHA-256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.

## Independent checks and frozen state

The [independent derivative receipt](derivative-check.md), fully read at
`1f5b3b`, records a separate configuration/cache/output and the same renderer.
All three fresh renders and image comparisons passed; all source-after hashes
matched. No content views occurred in that check. Shared-renderer agreement
is local reproducibility, not historical source independence or authenticity.

Protocol pin, unchanged: 20a72b569b175598d6e957f11974cb07e18c811f049880fd6b553230e13eb58c.
Root observations froze before peer content at `7fe891`, exit 0:
f4a9a8541a309c66059dbca6ec74f583c352bf7c56ef7a7348a0dfc499c2ebd5.
Derivative receipt pin:
063a2974ded45bfdec057dbce993968becc17081520e8d10eca89c1fa78be0db.
The separate reader froze review.md at `c51117`, exit 0, with pin
4a7b3701118d633a86b4f7aa024182458c58c69c0de880f88f6b74730580f62b,
before reading root. Root read the entire peer record at `28d9ec`, exit 0;
the peer read root at `c7ac3e`, exit 0, and checked both frozen hashes at
`dcf142`, exit 0. No material disagreement was found. The peer received no
display-resize notice; that is not confirmation of native-pixel presentation.
Each reader used three first views and no repeat or additional source view.

## Final review and worktree checks

The [text-only synthesis critique](synthesis-review.md) found no material
correction. Root read it completely and confirmed its pin at `9b82de`, exit 0:
553cd42d922fc6c0e1ad6a76a63d6d3731b430aeac300d3b175748726fb2fa58.
The reviewed report remains at
ad9e38c525a4988d5aefca5053b5941cf9ed0b4067c4e518bee978a40c6ad34d.
This receipt-only section is appended after that critique of the earlier
source-log snapshot, without changing its earlier record.

Root ran `shasum -a 256 -c` against fourteen fixed pins: protocol, two frozen
readings, derivative receipt, all three PDF inputs, three images, configuration
and three empty diagnostic files. All fourteen passed. A stdout-only Python
check of all six then-existing unit Markdown files found final newlines,
no trailing whitespace and all nine local link targets present. The same
`set -e` command completed `git diff --check` successfully (`f6ad33`, exit 0).
That Markdown count predates the synthesis critique and this final append;
it is not a repository-wide link or factual verification claim.

Final `git branch --show-current`, `git rev-parse HEAD` and `git status --short`
show the unchanged research branch/HEAD and pre-existing WIP categories
(`fe815b`, exit 0). Existing navigation was updated in research/README.md and
STATUS.md. The duplicate-source/status-role recurrence is covered by existing
SFB-005 fixtures; no new issue, transmission, acknowledgment or fix is claimed.
Main/legal files and frozen earlier evidence remain unchanged. No source
promotion, engine/bridge use, fees, outreach, staging, commit or push occurred.
This finite comparison is complete; the comprehensive goal is not.
