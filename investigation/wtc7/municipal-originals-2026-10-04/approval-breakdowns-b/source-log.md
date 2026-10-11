# Remaining schedule sources and verification

October 4, 2026 America/New_York / October 5 UTC. Prior turn completed a
substantive review and corrected agent errors; this unit proceeds to the last
three saved candidates. Active research branch at
`ca1c223335c20905d6608eb15c676f88cbfac734`, intentional unrelated WIP preserved.
Repository intake `c170fd` exited 0. Main control/charter pins match their
fully read versions (`a04b76`); that combined command's final `rg --files`
returned expected exit 1 because no matching acquired PDFs existed yet.

The saved checked metadata is an ID-keyed object, not an array. An initial
array-index inspection failed (`c9b8d0`, jq exit 5); no source was acquired
and the chained scratch creation did not execute. Corrected `to_entries`
inspection (`084eb3`, exit 0) verified all three exact IDs, page counts, byte
counts and literal labels, then created scratch with `mktemp -d`:
`/private/tmp/wtc7-approval-b.dZp5SN`. No source value was altered to pass.

The [protocol](PROTOCOL.md) froze before acquisition at `8eb81e`, exit 0:
`f9a127482c9509df5509f5bee4ba6dce93493c0b665423c4979062e17d42d4a3`.
Peer read all four applicable protocols and checked controls before views
(`c82801`, `66982f`, `5773f1`, `c19d2c`, `d651d7`, exits 0), with no material
method objection. Source labels are not content or installed-state findings.

## Exact acquisition and admission

One web-reader open per exact protocol URL returned tool-inaccessible status,
not a source absence or server refusal. The first sandbox GET for 172953
failed DNS (`a7ee95`, exit 6; HTTP000, zero bytes). Scoped permission then
allowed one direct GET for each source, with no credentials, cookies,
redirects or private payload. Actual command form:

```sh
curl --fail --silent --show-error --max-time 60 --max-filesize 10000000 --proto '=https' --output [exact scratch PDF] --write-out 'HTTP=%{http_code} TYPE=%{content_type} BYTES=%{size_download}\n' [exact protocol URL]
```

| ID | Handle and terminal receipt | Response | SHA256 | Acquired-file mtime UTC |
|---|---|---|---|---|
| 172953 | 71775 / 93c6bb, exit 0 | HTTP200 application/pdf, 345271 bytes | b981e1fde92775b1c59b2d4370488c2d70591efcbb3b98e9a621b2d32e814f00 | 2026-10-05T00:05:20.181826 |
| 173949 | 40280 / 6d8338, exit 0 | HTTP200 application/pdf, 232649 bytes | c480f2a9635763caf4cc17be6a3500c1ec2cb42c878165d863192f6e255e3809 | 2026-10-05T00:05:19.845319 |
| 174004 | 42249 / 43a1ce, exit 0 | HTTP200 application/pdf, 232037 bytes | 89de4a3ae1e611c2c27993ced26f4e921650022b7864713c29cce9095f08c93e | 2026-10-05T00:05:21.410967 |

All original handles were polled to terminal, not restarted on an observation
timeout. Bundled Python3.12.14/pypdf read-only admission verified PDF magic,
expected sizes and 5/2/2 physical pages, no encryption, AcroForm or OpenAction
(`81c11e` output, final `dd5813`, exit 0). These basic checks do not authenticate
historical creation or exhaust document safety. Mtimes describe acquisition.

## Rendering setup

Bundled `pdftoppm -v` confirmed Poppler26.05.0 (`dd5813`, exit 0). Private
font cache created (`b852c3`, exit 0), configuration added with apply_patch;
only the task cache differs from the previous unit's configuration. Every
root render uses `FONTCONFIG_FILE` pointing to this exact scratch config,
the bundled absolute renderer, `-f 1 -l [5 or 2] -png -scale-to 2400`, exact
source and output prefix, and separate retained stderr. Terminal rendering,
reading and preservation receipts will be appended after actual completion.

All root renderer handles are terminal: 172953/67028 returned `eb0cc5`,
173949/40934 returned `9e3573`, 174004/79739 returned `b177f2`, all exit 0.
No restart or warning; three stderr files are zero bytes (`0fea59`, exit 0).
Root config SHA-256:
`b1835e6f03d9d04308f0eb24d7d020b14003301669995b136cacaeea690e764d`.
Nine expected PNG byte/header/hash checks passed (`4b7436`, exit 0); all
maximum dimensions are 2400. Pages 2-3 of 172953 have landscape stored
dimensions; no rotation is performed. Three PDFs and configuration were
preserved using scoped non-overwriting `cp -n` (`75b0e2`, exit 0).

## Resumption and reading closure

The intervening user coordinate request repeated an already completed result;
its exact-point/hash confirmation made no new investigation progress. On goal
resumption, root re-read the main charter, incorporated protocols and applicable
skills; main control pins remained unchanged (`8c031f`, exit 0). Branch/HEAD
still match the opening state. No new acquisition or render was needed.

Both readers had viewed 172953 physical page 4 before interruption but saved
its note only afterward, from carried-forward own observations, before the
next source image or substantive peer findings. Both disclosed this deviation.
Root's delayed note was saved with apply_patch on resumption; pages 5–9 then
each received a note before the next image. All nine initial pages were
displayed at explicit original detail at both stages; no resize notice,
repeat, OCR, crop, rotation, enhancement, measurement or older-primary reread.

Root's stdout-only Python structure check (`c8ee68`, exit 0) confirmed nine
ordered source/page sections and nine closing anchors. Frozen root SHA-256:
`fa3ed5e83bbf90c007e4a833d6324a7b84f538eec2d9c57732fabe71614f1bf1`.
Peer closure (`c62153`, exit 0), after its own nine-section check (`5fcf67`):
`5bfaced1c2644a66212fb5f4e921c3608e36e16472c3d78abdc845bb11cf1050`.
Only then did readers exchange substantive notes. Root's initial combined
readback truncated; the missing peer passages were read in bounded follow-ups
(`b793de`, `b28e33`, exits 0). Four disagreements are retained in the report;
none was silently resolved or used to manufacture an accounting anomaly.

## Preservation and independent derivation

Explicit non-overwriting `cp -n` of nine PNGs and three stderr files into this
unit completed under scoped worktree permission (`eb20de`, exit 0). With the
three PDFs and config, sixteen files are preserved. Both readers closed their
repeat sets at zero; no additional derivative was needed.

The independent checker used three separate-cache Poppler executions, all
exit 0, and reproduced all nine image bytes/dimensions (`d7c690`). Its complete
sixteen-file equality check passed (`f52c98`, exit 0), with all hashes retained
and three root stderr files empty. Root read the complete derivative receipt
and final closure (`b793de`, `e23a05`, exits 0). Final receipt SHA-256:
`db4a7e4d70a6831c993a065198eae7e957ce76126ea65317579377f0b0f6b20f`.
This verifies local same-renderer derivation and current preservation, not
historical authenticity, transcription accuracy or engineering validity.

## Root arithmetic after both freezes

Bundled Python 3.12.14 stdout-only execution (`9af884`, exit 0) first asserted
the exact two frozen-note hashes, then compared the following integer-dollar
expressions with source-transcribed values. It reported **19 comparisons,
18 matches, one mismatch**; process success is not a claim all sums matched.
No PDFs/images were reopened and no values were selected by balancing totals.

```python
co8 = [7000,102705,28442,26483,42887,125453,27821,3941]
co13 = co8 + [78288,22721,220262,4874,85000]
checks = [
 (12134322-9500000,2634322),
 (400000+1884322+350000,2634322),
 (sum([1580,4631,701,0,24274,7710,6955,1631,8228,8313,2805,-30681,0,0,7553]),43700),
 (864577-820877,43700),
 (sum(co13),690877),  # 775877, mismatch +85000; retain
 (sum(co13[:-1]),690877),  # diagnostic only, not a repaired source
 (14287986-1668858,12619128),
 (12864619+117684+690877,13673180),
 (12864619+117684+898766,13881069),
 (13673180-1668858,12004322),
 (13881069-1668858,12212211),
 (sum(co8),364732),
 (13727986-1668858,12059128),
 (12864619+117684+364732,13347035),
 (12864619+117684+576854,13559157),
 (13347035-1668858,11678177),
 (13559157-1668858,11890299),
 (12059128-11678177,380951),
 (12059128-11890299,168829),
]
for computed, printed in checks:
    print(computed, printed, computed-printed)
```

The disputed December date is not an arithmetic operand; disputed unrelated
line amounts are excluded. The first-twelve diagnostic shows which listed
amount accounts for the discrepancy, not why the historical worksheet totals
exclude it. No full financial audit or inference of fraud. Independent
arithmetic/critical review and final coverage receipts follow separately.

## Independent arithmetic and queue coverage

Root read the complete separate post-freeze review (`cba465`, exit 0). The
peer's eighteen selected equalities had seventeen matches and one retained
failure (`70814b`, exit 1); two subsequent diagnostic equalities (`2aa335`,
exit 0) identified the same 85,000 difference and first-twelve subtotal.
Root's nineteen-comparison scope includes one of those diagnostics. This
agreement does not supply an independent historical source or resolve any
of the four disputed fields. Both frozen-note pins remain unchanged.

A separate coverage auditor used bundled Python3.12.14/pypdf6.10.0 in
stdout-only read-only checks to compare all sixteen saved metadata IDs with
actual held PDFs. Every ID occurs once, byte and physical-page counts match,
and no PDF read failed. It checked expected per-reader page sections across
fourteen reader files in these seven units:

| Content unit | Candidate ID suffixes and physical page counts | PDFs / pages |
|---|---|---|
| design-sprinkler-followup | 167873 (1) | 1 / 1 |
| drawing-review | 167874 (3), 173670 (1) | 2 / 4 |
| oil-route-packet | 166828 (8) | 1 / 8 |
| change-order-review | 168580 (1), 168581 (1), 171840 (6), 173920 (2) | 4 / 10 |
| various-orders | 167170 (2), 171802 (2) | 2 / 4 |
| approval-breakdowns-a | 171286 (5), 171620 (3), 172947 (3) | 3 / 11 |
| approval-breakdowns-b | 172953 (5), 173949 (2), 174004 (2) | 3 / 9 |

Total: sixteen PDFs/forty-seven physical pages with complete recorded readings
from both readers. This is metadata/section coverage, not a new image review
or independent validation of every transcribed claim. Existing exceptions
remain: both B page-4 delayed saves; various-orders root delayed page-2 save;
change-order peer section10 inserted ahead of4–9; oil-route root display-detail
forwarding deviation; differing drawing-review displays; and batch-A corrections
with separately declared post-exchange views. Section order alone cannot
establish actual observation chronology. No archive-exhaustion claim follows.

Root independently reran preservation/pin/holdings checks (`2671b5`, exit 0)
with bundled Python3.12.14/pypdf: sixteen unit/scratch byte comparisons;
protocol, both frozen notes and derivative-receipt SHA assertions; exactly
one each of thirty-two municipal PDF basenames; 85 actual physical pages;
the sixteen candidate page counts totaling47; and existing report/log local
link targets. No image decoding or historical interpretation in that check.
The independent coverage audit also counted fifteen source-content folders.

Existing SFB-002/SFB-005 interruption/source-version fixtures already cover
the encountered workflow pain points; no duplicate product issue is invented.
The archived feedback destination remains unresolved, with nothing newly
sent, acknowledged or claimed fixed. Main/legal records, source/frozen-note
bytes and all independent scientific/human/permission gates stay protected.

## Critical review and current handoff

The separate reviewer read the complete report and source log (`f96485`,
exit 0), protocol/derivative receipt (`737e77`) and limited batch-A excerpts
for the expressly attributed payment linkage (`2c6ea0`). Its saved critique
found no blocking substantive issue and requested one precision correction:
describe numeric entries under the handwritten heading, not every outstanding
amount as handwritten. Root applied that wording change, without source views
or frozen-note changes. Critical review is AI text/method review, not an
expert or human acceptance. Final review-note pin at `a3fa66`, exit 0:
`73535cd3aa61146bff71fc2236e0eff06611cd84ea450a71beee786110c90dd4`.

Existing STATUS and research README now point to this result and mark the
previously unread queue complete within its scope. The next independent unit
is a bounded lookup for the named generator-test/sign-off/punch-list records,
not a re-run of unchanged arithmetic. Actual source outcomes, model geometry,
field verification and wider charter work remain incomplete. Full-reasoning
source interpretation plus separate metadata/derivation checks remains the
appropriate division of work. No Git write or external transmission occurred.

Final broad navigation check `1ef385` exited 1 on the existing historical
STATUS link `reference-motion/report.md`, outside this turn's edited sections.
That failure is retained; no all-navigation-clean claim is made. The narrow
unit's earlier report/log link check passed at `2671b5`. A follow-up check
below covers all links in the new batch report/log and the newly edited
status/map portions, along with frozen pins and batch Markdown whitespace;
it does not reclassify the older missing link as a pass or delete that history.

The scoped follow-up `b91560` exited 0: five frozen/protocol/review pins,
all new report/log and edited status/map link targets, conflict-marker and
batch Markdown whitespace checks passed. `git diff --check` for the two
edited navigation files also passed (`e2167f`, exit 0). Report final SHA-256:
`82c024ff07ed24ab6fc45f52b62de43e038af7c40af5126295de64a9e389e54f`.
The historical link occurs thousands of lines below the new status entry
(`d1ff46`, exit 0); locate its actual artifact before a later synthesis relies
on that link. It is a separate navigation limitation, not failed PDF derivation.
