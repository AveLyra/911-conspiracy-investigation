# Remaining preservation records acquisition and verification

October 8, 2026 local time; acquisition timestamps below are October 9 UTC.
Worktree `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`. Earlier WIP remains preserved.

## Fixed scope and input checks

The preceding goal turn made substantive progress by locating the full folder
population and reading the first selected item. The intervening acoustic answer
did not complete another investigation workstream. This continuation selected
the remaining complete 14-item population, not a content-selected subset.

Root read the main charter and current feasibility/status/prior result, ran
repository intake, and used source, evidence, PDF and local-writing controls.
No cloud Page or separate authority
was created. This line records no newly run software test suite.

Frozen before acquisition:

| Input | SHA256 |
|---|---|
| PROTOCOL.md | `935f642f7473efad228e625fc641248ebc2e750592bf08669cfb10679e9eec73` |
| roster.json | `8d2f17061c013e9cb4980b14fa95cb63d7d96524424ab19aa24d3b72d02094f2` |
| ../response.json | `328a3a58d22d98c4cbc56ff8683ce618bfd76cbeebb33be8fccbfc3e23432542` |

Root's first jq projection incorrectly assumed object-shaped properties; it
failed without changing inputs. After inspecting the actual array structure,
the corrected projection matched the saved table. Separately, stdout-only Ruby
reconciliation (`bd72d5`, exit0) checked every selected ID, page/byte/end-Bates,
source/box/folder, identity uniqueness, pagination and termination. Totals:
14 documents,70 pages,2,998,001 bytes. A=5/23/1,136,224;
B=4/26/926,159; C=5/21/935,618. All three frozen pins remained unchanged.

## Actual acquisition

One approved shell loop, with `set -e`, exact fixed numeric IDs in roster order,
created new sources/renders directories and refused an existing source path.
For each ID, the actual curl command was:

```sh
curl -q --fail --silent --show-error --max-time 45 --max-filesize 10485760 --proto '=https' --user-agent 'WTC7-research-metadata/1.0' --header 'Accept: application/pdf' --output 'sources/NYC-WTC_000<ID>.pdf' --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects} url=%{url_effective}\n' 'https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000<ID>.pdf'
```

The executed command used absolute output paths under this directory; the
placeholder above expands only to the 14 frozen IDs below. Each call had UTC
start/end timestamps. Initial receipt `ab1b4a`, session32787; final `d72ae1`,
exit0. All14 returned HTTP200, application/pdf, zero redirects, matching
official effective URLs. No retry, query expansion, cookie, credential, upload
or source-route bypass occurred. curl version8.7.1.

| ID suffix | UTC start/end 2026-10-09 | Pages | Bytes | Acquired SHA256 |
|---|---|---:|---:|---|
|153905|00:57:15 / 00:57:16|4|227819|`d93bd5c644fe715f3e00403e79fec629670f8d3d4b9032d8c181b80eb75666b9`|
|153909|00:57:16 / 00:57:17|6|285122|`d0e36a2544636d9f1f44c661187bf647da704b9cf80864daf5f6ef8a64816ce1`|
|153915|00:57:17 / 00:57:17|7|332019|`abd658876aea96345a4375f40144669f19d7760b4388ba98f33eec0b21fa22da`|
|153922|00:57:17 / 00:57:19|4|196812|`3d0c5bf1a8dac8c6c615bea183a34f7b261065cda00818576eb472cd1af47cc6`|
|153926|00:57:19 / 00:57:19|2|94452|`2fda66c2f96b041e259138220ec40b16c987f64ec0cd3d659bca9501ad16e527`|
|153928|00:57:19 / 00:57:20|5|192371|`b210cb96d374e77a3e81990554716626fa81afa584c72889def4165e40186192`|
|153933|00:57:20 / 00:57:20|4|146159|`1ad8b407a793986037f4f8fabde11deb45090715a239d8e276f1b411d574dce2`|
|153937|00:57:20 / 00:57:22|13|460319|`d7090b78cad6f469a0a555bcd939d84c3d7d286039967548956b772b543ec3f2`|
|153950|00:57:22 / 00:57:23|4|127310|`8de4e227d8df8872092bca9085b0893a2970c1ec5fb385f8c4f81f8179acde89`|
|153954|00:57:23 / 00:57:24|5|170214|`434f7bccd3140f9933ccc95843aa7c551b35c8c9c20ac4c4d41f8bfd592ff897`|
|153959|00:57:24 / 00:57:25|5|341431|`caaa89c30b16fafd6d08fcb1bdef2906f725e9ba3bd3eeb0365b8146cfa74323`|
|153964|00:57:25 / 00:57:25|7|271806|`7b0e40f47f823c46450993cf6dc40f0f961e6447397115e87df2648d579da5ba`|
|153971|00:57:25 / 00:57:26|3|95953|`067fe09e2d26274c75f699b94a2a3cd36ba33b6daeee76a12d77ceb58a007d4f`|
|153974|00:57:26 / 00:57:27|1|56214|`cb56ae9d529750542675e76e9e928ef3274faca4705828923f0b6e183eaab3e7`|

## Admission and rendering

Root's stdout-only Ruby check used JSON, Digest and Open3 to run bundled
pdfinfo on each exact roster source (`a2ef6e`, exit0). All page/byte counts
matched, all PDFs were unencrypted and readable, and pdfinfo returned no error.
This establishes technical admission, not complete content or sensitivity review.

Bundled pdfinfo/pdftoppm both report Poppler26.05.0. One fixed-order loop made a
new per-ID directory with mkdir (refusing an existing directory) then ran:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -r 150 -png sources/<ID>.pdf renders/<ID>/page
```

Initial `e85154`, session62711; final `32f220`, exit0, no renderer diagnostics.
All14 per-document image counts match their expected counts, total70. Page
names are page-1.png etc except the 13-page PDF, which uses page-01.png etc.
Raster existence/counts are not a claim that all pages were visually reviewed.

## Content review and sensitivity gate

Root opened the complete first-page renders of153905,153909,153915. The first
two carry historical attorney-client/work-product markings despite acquisition
from the official public portal. Under the prospective sensitivity condition,
root stopped analysis of those items and instructed all readers to stop any
similarly marked item. No marked substantive finding is reported here.

A user question requests authorization for local-only analysis of officially
published marked copies, with notes confined to this investigation worktree;
it expressly excludes external messages/uploads/publication, pleadings and
canonical promotion. Pending that answer, no silence or preselected option
counts as approval. Ordinary unmarked public records and technical integrity
checks remain in scope. Reader coverage and item dispositions will be recorded
separately; the intended two-reading70-page review is not yet complete.

## Reconciliation and closeout

October 8 local continuation, after the intervening user acoustic question.
The preceding substantive goal unit made progress: it acquired the fixed 14
sources, completed technical checks and produced new partial source readings.
The acoustic answer did not complete another goal workstream. This continuation
finishes the eligible paired readings and their synthesis; it does not declare
the eight stopped items, WP5 or the overall goal complete.

Scope and acceptance for this closeout: retain every fixed population member;
reconcile the six eligible documents' two readings; preserve adverse passages,
duplicates and uncertainty; save only local research synthesis/navigation;
recheck immutable input identity and local links. No new network retrieval,
affected-document content analysis, software implementation, canonical promotion
or external transmission is included. The main AGENTS/workflow/start/charter
pins were rechecked unchanged (`d0599e`, exit 0); repository intake succeeded
(`38be6c`, exit 0). The source/evidence/PDF/writing skills kept source statements
separate from verified historical acts and preserved the sensitivity boundary.

### Actual reading coverage and frozen notes

The [report](report.md#full-population-and-actual-review-coverage) supplies all
14 item dispositions. Initial assigned-reader display counts are A 15/23,
B 14/26, C 17/21: 46 unique displayed pages. This does not mean 46 pages were
cleared or substantively analyzed. Only eligible A (6 pages) and eligible C
(14 pages) have completed paired readings. Gated items total 50 pages; 24 of
them were not displayed by the assigned first readers. Root's views and peer
repeats do not increase the distinct eligible-page denominator.

The B reader confirmed coverage from its actual prior tool history without
reopening the affected records: 153928 pp. 1-5 (marking p. 4); 153933 pp. 1-4
(markings pp. 1-3); 153937 pp. 1-4 (markings pp. 1-4); and 153950 p. 1 as a
sensitivity screen. No primary-B substantive note was produced. A prospective
stop is not permission to omit those items from the inventory.

| Frozen reading or technical record | SHA256 | Actual scope |
| --- | --- | --- |
| [primary A](primary-A.md) | `bd4829ef73402f5a1a77a90ea3a7f6196dae4c52b8e84f436f3ef3c20a2d9f01` | Eligible 153922 and 153926, all 6 pages; partial A coverage disclosed |
| [primary C](primary-C.md) | `675dea8fdfd24bbe5fa7f035f1f7f45f1ebde0352b1b97740259e316e1414c63` | Eligible 153954, 153959, 153971, 153974, all 14 pages; 153964 stop disclosed |
| [rotated peer A](peer-A.md) | `6d09782f61e12693e71f76ad0be000d9f664a32a37ffe2e8e0a45b11d6f7e88a` | The same eligible 6 pages, frozen before reading primary A |
| [rotated peer C](peer-C.md) | `f1c8ad6b4dd5efa60ab78a3f044d330b0c3ee445ca41247d187f6f1ba5dfcdaa` | The same eligible 14 pages, frozen before reading primary C |
| [technical verification](verification.md) | `37eda2fab66a313187355f13ca6fd5bac0b5d49f2ec0d4683185252f00956613` | 14 PDFs, 70 images and 3 fixed rerender repeats; no substantive content finding |

Root read all four frozen reading notes and the technical verification record
fully, then at closeout directly re-viewed the full rendered pages 153971 pp. 1-3
and 153926 p. 2. Actual view calls were labeled
`actual_root_closeout_view` with those paths and used `view_image`, original
detail. These labels are not fabricated opaque tool receipts. They confirmed
the decisive June qualifier, blank form, November dates and incomplete-return
wording. No new root view of an affected document was made in this closeout.

### Reconciliation results and limitations

Reader C compared frozen peer A with primary A only after its peer freeze;
reader B similarly compared peer C with primary C. Neither comparison found a
material substantive disagreement. Root independently read both pairs and
retained these precision points:

- Keep September 2004 letter/routing/due/receipt dates separate. A sixty-day
  commitment is not completed collection. November's next-day request means
  November 18, not an independently established legal deadline.
- Retain the June letter's qualified report of concern and November's stated
  nonreturns. Neither becomes proof of an identified loss or deliberate act.
- Sampling records are not physical samples. A documentary process may still
  lead to records about physical custodians; it is not irrelevant by definition.
- Use apparent near-duplicate envelope representations, without claiming a
  single authenticated physical envelope. Retain the printed BLA abbreviation
  if needed; do not rely on an unsourced expansion in the primary A note.
- Source-copy obstructions remain visible limitations. Legible corresponding
  copies were read on their own merits, not used to reconstruct hidden pixels.

The A reconciliation's full reads/hash checks were `3e0dd4` / `54dc26`.
Its first Ruby diagnostic failed because this runtime lacks `filter_map`;
using `map.compact` yielded ten matching source/render/control pins
(`76c607`, exit 0), without changing data. C reconciliation full-read receipt
`f815de` and unchanged-note check `ab86bb` both succeeded. These are reports
from the separate agents' actual commands, not root reruns.

A further read-only critical pass by the primary A author checked the report
at SHA256 `1e4ff472b5ab8b36cc9872cee8f6a3d86d38a58c1faa709377ee818cbf25969f`
and the municipal navigation paragraphs, finding no required correction. This
review has primary-author overlap and shared sources; it is not external expert
review or independent historical corroboration. No human acceptance is inferred.

### Integrity checks and remaining authority

Root's stdout-only `ruby -` identity check (`0db7b9`, exit 0) parsed the exact
14 PDF and 70 PNG rows of the frozen technical-verification table, matched the
PDF set and counts/bytes to roster.json, and required exact source/image path
sets. It checked SHA256 and byte counts for all 84 files, PDF signatures and
PNG IHDR dimensions. The recomputed compact, sorted PNG registry digest matched
`649b9c95b86248b4610440beb2fba482f31d5c25e43898ae40c85bfd6921be5a`.
Totals remained 2,998,001 PDF bytes and 6,902,494 PNG bytes.

That check also matched 14 explicit frozen control/note/history pins: protocol,
roster, parent response, four readings, technical verification, parent report,
material index and the four main control documents. Total 98 checked files,
zero mismatches. It was an identity/header check, not fresh PDF parsing, image
decoding or historical authentication. The earlier independent technical record
contains the actual parsing, decoding and three repeat-render checks. No older
software test suite is represented as rerun by this documentation closeout.

The original parent report remains at SHA256
`9df34c65c9653a4e8540e2787da0fc83a838ceb8d17311632643e9fff34f1b91`;
the version 3 material index remains at
`e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8`.
Its 272 artifact records were not newly reverified by the 98-file check.
This execution file was intentionally extended; the technical verifier's
earlier 6,354-byte execution-file pin remains an accurate historical version,
not a new pin to silently replace.

The user has not answered the local-only sensitivity permission question.
Seven items bear historical privilege/work-product markings; 153964 instead
triggered an unmarked potentially sensitive-content stop. Narrow permission
for marked copies alone does not automatically authorize that eighth item.
No affected substantive findings enter the report. This is not a ruling about
privilege, a claim of wrongful public release, or evidence of concealment.

The next source step is authorized completion of that exact stopped subset,
preserving these partial freezes in any continuation. Independently available
work remains on versioned F7 annotation/consumer completion as described in
[current status](../../STATUS.md); no F7 code or result changed here. The full
goal remains active, incomplete and not globally blocked. No new software pain
point was demonstrated by this source review, so no duplicate feedback note or
external task message was generated. Existing routing/acceptance gates remain.

Final closeout checks: the same 98-file identity command was repeated after the
report/navigation/methods edits (`9e53f1`, exit 0), with identical results.
`git diff --check` passed (`04a6ed`, exit 0). A read-only Ruby documentation check
verified 24 local link occurrences and their cited heading fragments, no trailing
whitespace in report/execution, and the exact 14-item disposition partition
(six/20 paired; eight/50 gated), receipt `4075a5`, exit 0. The report hash remained
the critically reviewed `1e4ff472b5ab8b36cc9872cee8f6a3d86d38a58c1faa709377ee818cbf25969f`
(`70fdf3`, exit 0). No historical conclusion follows from these mechanical checks.
