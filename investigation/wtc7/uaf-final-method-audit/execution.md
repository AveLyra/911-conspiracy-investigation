# UAF final-report audit — execution record

2026-09-20 UTC; research worktree/branch at e8d83d7. Main control hashes
unchanged, prior WIP preserved, repository intake run. Goal active.

## Acquiring the source

- Web open of the exact declared PDF returned a reader error: content length
  45,196,602 exceeds its limit. No PDF text/pages returned, no unsafe rejection
  or server access refusal reported.
- Curl8.7.1 (x86_64-apple-darwin25.0, SecureTransport, LibreSSL3.3.6,
  zlib1.2.12, nghttp2/1.68.1), approved ordinary network request, HTTPS only,
  redirects restricted to HTTPS, file cap52,428,800bytes, max-time60.
  Session63289 ended exit28 at60.008s with27,341,395 bytes of45,196,602.
  HTTP200, application/pdf, unchanged effective URL. No content admitted.
- Preserve source/attempt01.partial SHA256
  e4807cc8a07a9b3205ccbe7501626a4accddcb3e5215a0623149e028fcac5864
  and source/attempt01.headers SHA256
  e71da496c415e96b9b555be261600247cb3ba809b77713c54543e1fbd8dc291c.
- Prospective protocol amendment then allowed one fresh same-URL request to
  /private/tmp/uaf-final-method.nB4sSI/attempt02.pdf and attempt02.headers,
  max-time240, same size/access limits. No range assembly or source repair.
  Session13466 is the actual follow-up handle; its final result is not yet
  recorded at this initial log stage.

The complete command structure is curl --location --max-time TIME
--max-filesize 52428800 --proto '=https' --proto-redir '=https'
--dump-header HEADER --output BODY --write-out HTTP/effective-URL/size/type
against the one URL in PROTOCOL.md. First temporary outputs were report.pdf
and report.headers in the same temporary directory. No authentication or
custom identity supplied. Failed and successful payloads are distinct.

## Runtime and prior-claim checks

Bundled dependency paths located. Its Python does not have pymupdf; explicit
import returned ModuleNotFoundError (not a clean runtime check). Existing
/Users/admin/.pyenv/versions/3.13.7/bin/python3 successfully imports
PyMuPDF1.27.2.2/MuPDF1.27.2. No install or global configuration change.
Known prior Poppler font-configuration failures remain unresolved; the clean
MuPDF reading-derivative route is available and will require page inspection.

Independent prior-claim check confirms Luna asked whether P-delta treatment
was included in the compared results; it did not assert omission. Item3 asks
for exact pages/settings/case status. The claimed lack of an independent
reconstruction is not evidence of missing physics. Source note SHA256
70ee769d60bbd70b7f3c73cfc76cd8de71ecdd7c0c7bbfc27784511906c86815,
technical-review-update.md lines17,32. Independent check did not inspect this
new final report or re-run archive acquisition. The planned crosswalk must
include case identity, gravity initialization, computed/prescribed failures
and actual run linkage, not just keyword presence.

## Completed acquisition and derivatives

Session13466 subsequently completed exit0, HTTP200 with45,196,602 bytes,
same effective URL and application/pdf. The successful output was preserved
without modification as source/uaf-final-2020.pdf; attempt02.headers separately.
No repaired partial or assembled ranges were used. Raw cp -n preservation
kept distinct attempts. SHA256:

- complete PDF f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa
- second headers 8d10e01d3a295ee5117c74ea4bc716f683af15a8732cfd08520d8617fcf099e0

MuPDF opened125pages without encryption, repair or opening warnings, reporting
effective PDF1.4. Independent verification later distinguished the PDF1.3
byte header from the catalog's /Version /1.4; this is not source corruption.
The fixed37-page selection was declared after disclosed text screening and
before visual interpretation. No full-report visual-reading claim.

AST inspection of render.py passed before execution. Actual production command:
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/uaf-final-method-audit/render.py`
from the research worktree. Session20576 completed exit0:37pages, no recorded
page warnings, unchanged five input pins, status complete_not_visual_review.
Output render01 has37PNG,37TXT, start.json and receipt.json. No PDF edited.
The helper's complete status establishes derivatives, not source correctness
or completed human/AI reading. Prior Poppler issues were not repaired.

## Separate readings and review

Root read all37complete selected page images: prior25 then physical112–123.
No failed image display or repeat was needed; extracted-text screening was
disclosed in PAGE-SELECTION. Dense reaction labels were not individually
transcribed. Root froze root-notes.md before exchanging substantive readings:
e168d35bb3c782eebd91fcaa2a65ffc1a008891f03efefdc2bb2da629a0f16b1.
Observer separately read all37full pages, with text assistance for10; its note
preserves the recovered receipt-text truncation, not a failed page display.
Freeze observer-notes.md:
064f3d0df679b829423bcb6e6745f134531cefa3c75a408af668d9b15f7ded59.

After both freezes root read the observer's note. Its useful narrowing is
retained: §4.4 expressly introduces Figs4.8–4.16, so the neighboring exclusion
must not be represented as a separately authenticated configuration for
Figs4.17–4.20. The report now states that scope explicitly. Neither freeze was
rewritten to erase the distinction. No source data or solver was executed.
Independent review/integrity records and final checks are in validation.md.
