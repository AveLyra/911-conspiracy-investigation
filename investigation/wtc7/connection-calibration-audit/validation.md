# Verification, source coverage and reproduction

Research-only unit, September12 local / September13 UTC. [Report](report.md)
controls the synthesis; sources control evidence. The evidence-audit and
source-of-truth skills distinguish physical tests, fitted targets and inference.
The PDF skill requires actual full-page inspection; development-verification
governs the narrow arithmetic code. These are workflow checks, not engineering
certification or proof of a historical run.

## Source pins and what was inspected

| Source | SHA-256 | This root turn's full-page visual coverage |
|---|---|---|
| Main's NCSTAR1-9, 797pages | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` | 527,529,531,534–538,541 (9 pages) |
| Main's NCSTAR1-9A, 173pages | `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` | 54–59,64,65,67,73–77 (14 pages) |
| Acquired TN1749,113pages,13,056,103bytes | `5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf` | 1,3,33–35,41–45 (10 pages) |

Main's source paths are `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`
and `ncstar-1-9a.pdf` in that same directory. The latter is November2008 with
January2009 changes. TN1749 is preserved unchanged at
[retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf](retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf).
Its PDF3 says July2012 with February2013 corrections. These reports are separate
source families; descriptions of earlier tests remain secondary to originals.

Root text discovery additionally read NCSTAR1-9 pages528,530 and other selected
method text; it searched PDF501–560 for experimental/citation terms. Complete
NCSTAR1-9A citation text at117 identified the exact2008paper. These are not
additional full-page-image review claims. The independent
[NIST review](nist-validation-review.md), [capacity review](capacity-verification.md),
[retrospective review](retrospective-context.md) and
[final inference review](final-inference-review.md) state their own larger or
different coverage. The same rendered page viewed by two agents is a separate
reading, not a second source acquisition or laboratory experiment.

### Rendering and acquisition limits retained

Root's initial10 NCSTAR1-9 renders in
`/private/tmp/connection-calibration-root.Lvs2CP/n19-p<page>.png`
returned0 but emitted1,512,102stderr bytes each; only counts were retained, not
the diagnostic contents. The absent Fontconfig configuration was noticed;
its exact warning content cannot now be claimed reproduced. Those images
were not overwritten. Root inspected the three table pages536–538 from this
legible initial batch. Separate configured renders of527,529,531,534,535,541,
and subsequently1-9A59, completed with0stdout/0stderr/exit0 and were fully viewed.
The other initial renders were not visually inspected as a separate pass.

Configured renderer:

~~~sh
FONTCONFIG_FILE=/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 59 -l 59 -scale-to 1700 -singlefile -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf /private/tmp/connection-calibration-root.Lvs2CP/configured-n19a-p59
~~~

Use a new output stem on replay; do not overwrite preserved renders. The root
59 PNG is `c24697a3a4f9678e67e84ee50bc03f08bbae36f8123e6d103d90265af2922561`.
Other shared render locations/coverage are in the source reviews. Font warnings
on some retrospective renders are also disclosed there. The exact table
transcriptions and preserved PDFs are the durable numerical inputs; temporary
render paths are not guaranteed permanent artifacts.

Root submitted four targeted queries: `site:nist.gov Sadek 2008 WTC 7 connection
spring model`; `site:nist.gov Sadek 2008 "connection" "experimental"`;
`"Robustness of Composite Floor Systems with Shear Connections" Sadek pdf`;
`site:nist.gov "Robustness of Composite Floor Systems"`. The delegated original-
paper pass used four queries and records11checked routes in
[retrieval-log.json](sources/retrieval-log.json), within the initial12-query cap.
No new query was used for the retrospective follow-up. The exact2008article
was identified but no full PDF acquired; [its manifest](sources/manifest.json)
must not be combined with the acquired later report or a different same-year
moment-connection paper.

Root's TN1749 web fetch failed at the reader's13MB size limit; subsequent reader
find calls were not valid content-absence tests. A direct official-URL curl
request succeeded (exit0), with60second/30MB limits. Bytes/hash and page count
were independently checked before and after preservation. Root's first
confidential/proprietary/distribution-limited lexical scan returned no
candidates; the separate broader scan identified three engineering-sensitivity
pages and inspected them. Neither scan is blanket sensitivity clearance.
No held packet or flagged proprietary command documentation was used.

### Released spreadsheet: inventory-only boundary

The June2025 manifest at
`/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv`
has SHA `30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`.
Its25,643rows group as25,188 `.int`,173 `.nod`,272 `.png`,3 `.apdl`,3 without
extension and one each `.pdf`,`.zip`,`.ppt`,`.pptx`. No Excel extension appears.
This turn inspected the typed inventory, not new archive bodies or embedded
presentation contents. Different encodings, embedded tables or other releases
could hold the needed data. Consequently the spreadsheet/mapping is **not
identified by this check**, not proved nonexistent or categorically withheld.
Earlier [thermal-transfer coverage](../thermal-transfer-crosswalk/report.md)
remains a separate source inspection with its own unresolved semantics.

## Arithmetic: what actually passed

Root [transcription](capacity-root.json) froze at
`476051df3c2c58689b8dccc20a8a6a6f3ba9d246cca1445ca1d0a40596eebcf4` before reading
the independent transcription/results. The independent transcription and
implementation also froze before root-output access. The post-freeze schema
adapter is explicitly not blind. Source page review used PDF text as an aid,
not as an image substitute. Root engineering labels are normalized aliases;
four11-4 group labels incorrectly add "Beams." The source/independent labels
and report correctly retain core floor girders. No frozen values were changed
to hide that error. Failure-mode labels are independently transcribed only.

- [Root runs01](root-results01.json) and [02](root-results02.json) are byte-
  identical, SHA `02fe6a43dab1f66d4994c855ae69d3620748aeff15fd1e8a8dbff00675246a6b`;
 14synthetic checks pass in each. [calc_capacity.py](calc_capacity.py) is pinned
 at `e4a3cb1a1cbdc4d26b3ae33f58e677cc8c45b0f6b439e484950f07251277ade2`.
- The separate arithmetic has10synthetic control groups. Root read its complete
  implementation and reran it as
  [capacity-independent-root-replay02.json](capacity-independent-root-replay02.json),
  SHA `cb697054f7ffdf2ae12223f3ccd408d4125ea97964959d57b633aa3d5830644b`.
  Its result object equals the initial independent result exactly; receipt
  differences are limited to the command/output name.
- The independent final comparison checks55rows/165displayed numbers,
  9source summaries/18summary calculations,5formulas and explicit metadata,
  precision and label aliases. It passes468exact-rational checks,
  806metadata/value/disposition equalities and468fixed-decimal checks. Root
  read the complete adapter and reran it as
  [capacity-comparison-root01.json](capacity-comparison-root01.json),
  SHA `e99ffd4a997ea0623196b631432c8afcfaf2bee16bf7fb06d955547de4b39eb6`.
  The comparison result matches the independent final receipt exactly.

The fixed16decimal check tolerates5e-17 rounding error; exact rational results
use no floating tolerance. These repeated results do not authenticate hidden
worksheet digits or physical capacities. Formulas deliberately do not assign
the table-load rounding envelope to engineering parameters. No chart was
digitized, no property inferred/substituted and no solver run.

Failures are retained: the independent first receipt write lacked worktree
permission; the first schema adapter rejected21undeclared textual aliases and
misnamed a nondecimal-failure count. Both failed receipts and the exact earlier
adapter remain preserved with explanation in [capacity-verification.md](capacity-verification.md).
Two root report patch attempts failed context validation before the successful
source-context correction; neither changed the frozen initial report. These
are workflow failures, not physical findings.

### Reproduction commands

From `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, select **new**
output names; the following successful names now exist and intentionally refuse
overwrite:

~~~sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/calc_capacity.py --output research/sherlock-wtc7-investigation/connection-calibration-audit/root-results02.json
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/verify_capacity.py --output capacity-independent-root-replay02.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/compare_capacity.py --output capacity-comparison-root01.json
~~~

Runtime: bundled Python3.12.14, standard-library Fraction/Decimal, pypdf6.10.0
for selected PDF extraction, Poppler26.05.0 for rendering. No dependency
installation or interactive browser test applies to this local arithmetic.

## Critical review and closeout boundary

The [initial report](report-before-source-context-review.md), SHA
`ffd69a6903be6726cc66fa87d92a1a3ccfb0aa7b4605060cf6a51e3c7440c243`, remains
preserved. Independent review required the explicit44ksi/seat/custom-model
context on1-9A59 and restriction of a blanket shell-calibration sentence to
the displayed fin models. Root inspected that whole page and corrected both,
also clarifying the table's room-temperature/connection-family scope. The
revised report SHA is
`9b4d9c4b6a3a54b2abb4d1751fbc46d325d7ea981f76c832425c293c03c6e1ff`.
The final review records its actual checked candidate, not assumed acceptance
of any future edit. The original NIST extraction remains unchanged.

All work stays local/uncommitted in the investigation worktree. No main/raw or
canonical legal edits, held-source inspection, paid access/outreach, publication,
commit/push, accepted Sherlock finding or Faraday engine call. Feedback is
deduplicated locally because the designated task remains archived and routing
unresolved. [STATUS](../STATUS.md) is the context-distiller handoff; the next
original-experiment task is not permission to broaden authority. The overall
goal remains active and incomplete.

## Executed closeout checks

[closeout01.json](closeout01.json) records PASS:10Markdown files checked for
trailing whitespace,5Python ASTs parsed,13JSONs parsed and54local links resolved;
29then-existing unit files remain byte-identical through the check. All source/
review pins, root output equality, independent consumer equality, manifest counts
and overwrite refusal pass. Source PDFs and the prior material/run report retain
their pins. The scoped git whitespace check and read-only strict record validator
also pass. These checks were executed, not inferred from the independent review.

The final command for a fresh artifact check is:

~~~sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/connection-calibration-audit/check_closeout.py --output closeout02.json
~~~

Use a new basename when that receipt already exists. This check pins the reviewed
report, preserves old artifacts and exercises refusal without overwriting prior
results; it is not another physical or solver experiment.
