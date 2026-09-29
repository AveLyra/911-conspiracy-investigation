# Physical floor-test audit: actual verification

September27,2026. Source reading and complete-page derivatives, not new
experiments, solver execution, curve digitization or historical authentication.
Scope, source observations and retained failures:
[report](physical-floor-test-followup-2026-09-27.md).

## Source acquisition and identity

One final official source acquired:
[NCSTAR1-6B](ncstar-1-6b-source01.pdf),6,657,729bytes,202pages,
SHA-256 `6a641a3ce902a4dad0d52d6218968086460841dd60524e2269366e00323ae5f7`.
The visible title gives September2005. Catalog/embedded production dates are
not substituted for it. The public PDF is encryption-flagged but opens with
an empty password (pypdf result1); no protected/private access occurred.

Actual transport used `curl --fail --location --max-time 90 --no-clobber
--output DEST 'https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101042'`,
where DEST was the absolute linked source path in this worktree. Session34033
reached terminal exit0 before parsing. The draft publication was not acquired.
One official-domain query of the permitted four, two metadata-page opens and
bounded local filename/Markdown lookups were performed, not exhaustive searches.

## Exact rendering and reading coverage

Existing `render_condition_pages.py` was read and reused, not edited. Each
invocation used bundled Python3.12.14 with `-B -`, loaded that module with
`importlib.util`, assigned its `SOURCES` tuple to `('floor',
'ncstar-1-6b-source01.pdf', SHA_ABOVE, 202, PAGES)` and called `render(OUT)`.
The three actual PAGES/OUT arguments and completion receipts are:

| OUT | Physical PAGES | Terminal session/exit | Receipt SHA-256 |
|---|---|---|---|
| floor-test-render01 | 1,3,5,7,8,9,15,31,32,33,34,35,39 | 92711/0 | `2c4ff9cf7a0b248b79ae88504681b1dce18a5d37b24bcfacf7f29f148844b60a` |
| floor-test-render02 | 40,41,42,45,46,58,69,71,78,79,80,81,85,86,99,109,110,119,120,130,131,132,140,141,142 | 59497/0 | `4ae5adc52175460387ca8b9c71ba960b57b44b556e003b4d2e0886696b2ee067` |
| floor-test-render03 | 82,83,84,100 | 40784/0 | `a4b37bfe83421437e7b3f83867354acfbfb4cef2446f55ca8705fdff5ec4fa50` |

Receipts: [batch1](floor-test-render01/receipt.json),
[batch2](floor-test-render02/receipt.json),
[batch3](floor-test-render03/receipt.json). Their command arrays preserve actual
per-page arguments, exit codes and diagnostic paths. The create-only helper
requires source pins and helper SHA
`a5083f34465587ff8ee877b5bd1d7dd5a7ced28ec491ab3ec9bbc1a5aed011ba`.
It invokes bundled Poppler `pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png
SOURCE PREFIX`, uses a per-output font configuration/cache, records complete
decoded PNG/pixel identities, warnings and before/after input pins. No crops,
image enhancement or renderer/source changes. All three invocations reported
zero nonempty rendering stderr, zero parser stderr and zero warnings. Poppler's
separate version command is not counted as an empty rendering diagnostic.

Runtime: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`;
Poppler: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`.
pypdf6.10.0 and Pillow12.3.0; no dependency installs. The source/font/runtime
pins in each receipt describe that invocation, not a hermetic dependency closure.

Root viewed all42 full images. Display resized41 portrait pages from1700×2200
to1376×1780 and one landscape page from2200×1700 to1780×1376; text, tables and
footnotes remained readable. This is source-page reading, not native-pixel
measurement. Initial text locators were physical1–9,15,16; the renderer also
saved text only for its declared pages. No whole-report body or appendix review.

## Separate integrity checks

A separate reviewer ran three read-only stdout-only bundled `python3 -B -`
scripts, one per batch; all exit0 with no errors. Checks covered source bytes,
hash and202-page count; receipt identity; exact selected-page/directory
membership; PNG signatures/IHDR; Pillow verify then fresh full decoding; RGB,
single frame, dimensions and pixel hashes; recorded per-page command mapping;
and actual empty render stdout/stderr. Before/after size,mtime,hash snapshots
were identical for each checked source/receipt/PNG set.

| Batch | PNGs | Checked source/receipt/image artifacts in its interval | Receipt bytes | Empty per-page stdout/stderr files | Other receipt products not rehashed |
|---|---:|---:|---:|---:|---:|
| 1 |13|15|76,428|26|47|
| 2 |25|27|135,586|50|83|
| 3 |4|6|32,130|8|20|

All selected pages have MediaBox=CropBox612×792points and UserUnit1.
Physical132 alone has rotation90 and2200×1700pixels; the other41 have rotation0
and1700×2200pixels, all matching200dpi. Each independent check excluded seven
non-source inputs and the listed other products from fresh rehashing. The
source is repeated across intervals; do not sum interval counts into distinct
experimental observations. These are integrity/geometry/decoding checks, not
an independent rerender, text-accuracy proof, pixel-content correspondence
proof or historical/scientific validation.

## Separate source review and consequential correction

[Independent observations](floor-test-independent-review.md) initially froze
21 full pages: render01 physical3,5 and render02 physical41,42,58,79,80,81,
85,86,99,109,110,119,120,130,131,132,140,141,142. Initial10,101-byte prefix SHA
`0bb59edb7a60e98fa4af822165310fa72fb06d1111c00596a3f3f86a74e4ee3c`.
Four continuation pages were appended only after render03 terminal success;
original prefix was retained. Full supplemented SHA
`d3917ceaf8a9ec1840871c87342a81ab3697c682550d7bfecfeb52c0a9b4fc7d`.
The25-page reading was frozen before root's synthesis was supplied. It is
prior-informed analytical independence, not blinded physical replication.

The reader then reviewed the entire282-line root report. It found one definite
locator-sentence reversal, corrected to physical=printed+36. Within its25-page
coverage it found no other material interpretation error. Coating/density
means, printed4/9–10 design claims, acquisition and render assertions were
expressly outside that source review; do not claim they were independently
scientifically cleared. Artifact checks above are a separate review role.

A separately declared post-synthesis check then covered render02 physical40,
45,46,69,71,78 in full: cumulative31 reader pages. All reported main/bridging
thickness and density means matched, as did masking/setup and scaling details.
This review recommended retaining the favorable rationale for preserved
sections/coating/slab and adjusted loading; the report now includes it without
claiming full response similarity. This later check is not pre-synthesis or
blinded. The appended review's current SHA is
`c10e170a8d71413c0b39300f5f477a0fd75fd722602407115bf62df2a0d9dc40`;
both earlier prefixes remain identical. No numerical correction was required.

## Failures, scope and limits retained

- Initial local lookups named two absent report paths and an absent worktree
  authority directory; corrected searches used existing paths. No global
  absence inference or missing-record finding followed.
- Initial expected page offset+34 failed: physical35/39 were executive-summary
  xxxiii/Introduction3, not the expected chapter/method openings. Both were
  viewed and the mismatch recorded before body expansion; verified offset+36
  controlled later selection. The later report wording reversal was another
  drafting error, caught and corrected by review, not a source defect.
- Some combined instruction/receipt/navigation outputs were truncated. Required
  instruction tails were separately read, structured artifact fields were
  checked by the reviewer, and pertinent navigation passages retrieved in
  smaller outputs. A truncated preview is not a complete-reading claim.
- Immediate loading and observation continuations were declared before reading.
  Their coverage does not establish original measured load/cooling histories,
  authenticate laboratories or clear unreviewed sensor-validity appendices.
- Four multi-file documentation patches failed exact-line matches, in
  research/README, STATUS and twice in causal-chain validation. Read-only
  searches checked earlier failures; successful exact-old-text patches also
  confirmed the failed attempts had not applied their earlier target changes.
  Corrected patches saved the intended
  changes; failed attempts are not counted as successful edits.

Research worktree only; no raw overwrite, legal promotion, original-drawing
inspection, source execution, solver, graph digitization, accepted Sherlock
finding, Faraday call, human-review substitution, outside engagement, stage,
commit, push or sensitive transmission. The source-of-truth/evidence skills
kept source reports distinct from measurements and causal proof; the PDF skill
required the complete-page checks rather than reliance on abstract/OCR alone.

## Integrated documentation review

The scientific reader rechecked the amended mapping/design rationale and
review coverage, the two dated causal-chain subsections, footnote20 and current
STATUS. No material scientific overclaim was reported. Its chronology correction
was applied:25 pages preceded reading root's synthesis, not necessarily the
creation of a concurrently drafted document. This is review of derivative
claims, not a second experiment or fresh independent artifact check.

The artifact reviewer read the complete143-line verification and288-line report
versions, confirmed accurate attribution of its sizes/pins/geometry/coverage,
snapshot intervals and exclusions, and tested local target existence with a
read-only bundled `python3 -B -` script:10 local links present, zero missing,
two external links skipped, exit0. Its check did not reopen source PDFs,
recheck artifacts, interpret science or verify root's transport history.
Later documentation-only additions do not retroactively enlarge that coverage.

Root's final stdout-only bundled Python document check passed:11 touched
Markdown files for trailing whitespace/conflict markers;44 local targets across
the audit/verification and causal report/scope/verification (two external URLs
skipped; fragments not resolved);20 unique causal footnote definitions with no
unresolved reference; source and three receipt size/hash pins; and the current
independent-review hash plus original10,101-byte prefix hash. No images or
scientific computations were rerun by this final document check. `git diff
--check` exited0. Main's tracked dirty-file listing and the four controlling
instruction/charter hashes remain unchanged. Existing WIP was preserved;
no stage, commit, push, publication, transfer or accepted finding.
