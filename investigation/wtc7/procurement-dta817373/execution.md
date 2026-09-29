# Acquisition, diagnostics and reading log

2026-09-20 UTC. Research-only unit under PROTOCOL.md. Previous goal turn
completed UAF source-method work; this is a new primary-source test, not a
status-only continuation. Main controls/charter hashes unchanged; intake and
dirty worktree inspected. No main writes, commit/push or engine activation.

## Actual source route

One query: `"817373" "Henry"`, restricted to dta.ny.gov. It returned both
the earlier ALJ determination and appellate decision. Opened the official
homepage https://www.dta.ny.gov/ to identify publisher and the selected
https://www.dta.ny.gov/pdf/archive/decisions/817373.dec.pdf . No earlier
determination, later appeal or separate exhibit file opened/acquired.
Web returned37pages and a broad text screen; no visual-reading claim from that.
Root also screened first/last local text pages for identity/date before freezing
all37physical pages for full visual review.

Ordinary HTTPS preservation began after08:33:19UTC on2026-09-20. Curl8.7.1
used --location --max-time60 --max-filesize20971520 --proto '=https'
--proto-redir '=https', with separate decision.pdf/decision.headers in
/private/tmp/dta817373.xy9IZD. Terminal exit0, HTTP200, application/pdf,
294760bytes, no redirects, effective URL unchanged. No retry/session remained.
The exact raw outputs were preserved with cp -n under source/:

-817373.dec.pdf SHA256962c2f2faf8fa7f17ef7a16efa6cbc8d036e4d82b6d8cc86e9237c2ff3234acc
-decision.headers SHA256bf82621e88dc782fd582c5fe06a3a6ced13a24580362b7415ad54c9bdbffc853

**Diagnostic-output error:** curl's `%{json}` write-out exposed a broad transfer-
metadata object and certificate details to the local tool transcript, causing
truncation, instead of the intended minimal status/URL/type/size allowlist.
Do not reproduce that object in reports or feedback. No credentials were
supplied; this is not evidence of remote access failure. Subsequent checks
must print allowlisted fields only. The source and header artifacts remain
unchanged; the transfer is not repeated just to obtain cleaner logging.

MuPDF initial open:37pages, PDF1.4, no repair/encryption/open warning,
zero embedded files. Embedded-file count alone does not prove that no exhibit
images occur among pages. Official April3,2003 appellate decision selected;
earlier ALJ disposition and all later procedural history not independently read.

## Rendering and prospective warning assessment

Refreshed dependency bundle26.905.11957. Existing explicit Python3.13.7,
PyMuPDF1.27.2.2/MuPDF1.27.2 used; no install. Prior bundled-module absence
and Poppler configuration problems are not claimed fixed. Development-
verification safeguards used for narrow adaptation of the prior renderer.
AST parse/import passed. Actual production:
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/procurement-dta817373/render.py`
from the research worktree. Session10293 confirmed terminal exit0,37pages,
unchanged inputs, but **37warning-bearing entries**, not a clean pass.
Every combined render/text entry records a structure-tree format error and
fallback to treating the tree as absent. All original messages remain in the
receipt and tool output. Source PDF not repaired or re-exported.

Before substantive visual admission: a separate integrity reader will isolate
rendering versus extraction diagnostic stages without changing source bytes.
Both full-page readers must assess every page, including footnotes/tables,
for missing/clipped/illegible content and compare decisive text to visible
source. If decisive content is unresolved, do not promote it on the basis of
text extraction alone. Same-engine reproduction is not independent glyph
validation. A visibly complete readable result may be admitted with bounded
diagnostic limitations; never relabel it as a warning-free pipeline.

Independent pre-source lead check confirmed the old README gives identifiers
but no dates/URL/sourcepage or inspected exhibit; the operational plan gives
no additional DTA corroboration. Its universal-proof/ordinary-alternative
boundaries are retained. Root's forthcoming source result must distinguish
findings, testimony, arguments and original documents, not infer authorization
or wrongdoing merely from silence. No substantive notes exchanged yet.

## Completed reading, freeze exchange and checks

The preceding paragraphs record the prospective stage. Subsequently root and
the independent observer each displayed/read every physical page1–37 once,
with no failed/repeated displays or observed illegibility/clipping. This is
37+37 displays of the same source family, not74 independent evidence items.
Root had the earlier web/local-text exposure; observer used selected text
after full visual reading. Both disclose prior-informed status.

Root freeze SHA25695f864b579474705a52b9505007ca28960691ea867c357a0a257b3bc8de54200;
observer freeze SHA256021e4e6a498bd87e8a02886c34516924b27655d45d8972c1e6fc83df4c9a340b.
Substantive notes were compared only after both freezes. No material
disagreement. Observer cautions against treating an inventory including
access-control equipment as a complete access-control maintenance obligation;
the report keeps documented CCTV maintenance distinct from inventory scope.
No original invoice/check/exhibit facsimiles are bundled in the37-page file.

The independent integrity reviewer initially asserted that rendering should
be warning-free; that test exited1. A one-page stage diagnostic and then two
complete37-page operation-order checks corrected that reviewer assumption,
not the source. Session37631 reached terminal exit0. All37 pages warn during
get_pixmap in either order, not during get_text, page loading or PNG encoding.
Both orders reproduce every saved PNG byte stream, full RGB array and text.
Five input pins,75 recorded products,76 directory files and headers stay stable.
See integrity-review.md; neither frozen reading note was changed to retrofit
knowledge acquired later.

Root independently executed an inline read-only verifier with
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B -`
from this worktree. Session32869 reached terminal exit0. It checked exact
directory membership, nonsymlink regular files, all product hashes/lengths,
five before/after/current pins, page order and header hash; then freshly
extracted text before rendering each page. All37 text streams, PNG streams
and decoded RGB arrays match saved products. Expected rendering diagnostics
match exactly on37pages; other measured stages remain warning-free. The
diagnostic buffer was checked explicitly while repetitive console errors were
suppressed, not erased from the saved receipt. All source/product bytes stayed
unchanged. Decimal arithmetic independently confirms3314.84−712.79=2602.05;
no original invoice/payment or all-table arithmetic verification is claimed.

One navigation command guessed a nonexistent unit README and exited2; the
actual index is research/README.md. It did not write files. Oversized status
screens were truncated; targeted follow-up isolated the current handoff and
relevant source/index passages. No truncated screen was treated as a complete
new-source review.

The final independent wording review found no material overclaim and one
page-section precision issue. Findings continue into page29's opening paragraph
before the ALJ-summary heading; the report now says so. An initial multi-file
patch failed its execution-log context check before applying changes. Root
inspected the actual text and reapplied the correction successfully; no frozen
note, source or derivative was altered. The reviewer's earlier report hashes
remain as the actual versions reviewed, not overwritten with a later hash.

All declared source work is now complete within this fixed unit. The stronger
claim that the pipeline is clean remains false; warned visual admission and
same-engine reproducibility are the actual results. Originals, main records,
other WIP and accepted engines remain unchanged. No process from these checks
remains live; no solver, exhibit search, request, transmission, commit or push.
