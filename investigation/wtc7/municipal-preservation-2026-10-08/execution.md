# Municipal preservation lookup and reading execution

October 8, 2026 (America/New_York); acquisitions occurred October 9 UTC.
Working research in `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.
HEAD `ca1c223335c20905d6608eb15c676f88cbfac734`. Existing WIP preserved.

## Declaration and authority

Root read main AGENTS, WORKFLOW, START-HERE, full CHARTER and investigation
isolation instructions; repository intake `3afbf8` confirmed the existing
research worktree. Three read-only component reviewers audited WP1/2, WP3/4
and WP5. The WP5 review identified the unread exact preservation folder.
Root verified the actual array-shaped row 643 and the earlier cover reading,
prior lookup scope, saved request and published search implementation. No
downloaded code executed. The write-page skill retained the existing local
research destination; no Page or external publication was created.

Protocol and request were saved before network reads; initial pins `676ebb`:

| File | SHA256 |
|---|---|
| PROTOCOL.md | `8274bfcf654108d1e8c6d0e1b2610232e595c875aeb73c787ca8b56d2a84ec8c` |
| request.json | `c7f4bb6c72167c6829ab330dd306fc7fad1198a3f7cef2d09fce10bdd15a4a6b` |
| Prior folder-document-locator/folders.json | `cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704` |

A separate protocol/body reviewer found no material blocker at these hashes.
It emphasized that first noncover ID means exclusion of the known cover, not
a guarantee that the selected page has useful content. Root did not substitute
another record after reading.

## Actual acquisition

`mktemp -d /private/tmp/wtc7-preservation-20261008.XXXXXX` returned
`/private/tmp/wtc7-preservation-20261008.p204IY` (`e4f012`).

The exact query command (absolute paths preserved for replay context) was:

```sh
curl -q --silent --show-error --max-time 45 --max-filesize 10485760 --proto '=https' --user-agent 'WTC7-research-metadata/1.0' --header 'Content-Type: application/json' --header 'Accept: application/json' --data-binary @/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/request.json --output /private/tmp/wtc7-preservation-20261008.p204IY/response.json --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects} url=%{url_effective}\n' https://sept11documents.cityofnewyork.us/api/v2/search
```

Sandbox execution `73216d` failed DNS resolution, exit 6, HTTP000/zero bytes,
before an HTTP response. The same command was then explicitly submitted for
normal scoped network approval—not an alternate site or bypass of denied
remote access. Approved execution `08df13` exited 0: HTTP200, 26,269 bytes,
`application/json;charset=utf-8`, no redirect, same official effective URL.
There was one completed public search, not two returned result sets.
Response completion mtime: 2026-10-08 20:39:41 -0400 (local acquisition marker,
not source publication or historical date).

Root's stdout-only Ruby check (`9f0111`, exit0) checked query echo, pagination,
single-valued property mapping, exact source/box/folder joins, key/title/result
identity, 16 unique records, 72-page sum and cover inclusion. Its full sorted
table selected 153904, one page/23,291 metadata bytes. A separate Ruby check
(`3b8890`, exit0) additionally checked all 176 property types, positive integral
sizes, end-Bates spans, nonoverlap and uniform agency/volume. The response adds
an empty `user_context`; requested fields echo exactly. All four input pins
remained unchanged. The independently checked table is retained in the report.

Selected content command, after the metadata conditions passed:

```sh
curl -q --silent --show-error --max-time 45 --max-filesize 10485760 --proto '=https' --user-agent 'WTC7-research-metadata/1.0' --header 'Accept: application/pdf' --output /private/tmp/wtc7-preservation-20261008.p204IY/NYC-WTC_000153904.pdf --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects} url=%{url_effective}\n' https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000153904.pdf
```

Scoped approval; `02a09d`, exit0: HTTP200, 23,291 bytes, `application/pdf`,
zero redirects, same official URL. Completion mtime 20:40:57 -0400. No credentials,
cookies, upload, guessed IDs or further content requests.

## Source and derivative checks

`pdfinfo` confirmed one page, unencrypted PDF1.5, rotation0, 618.25×815.05pt;
the byte count matches selected metadata (`b73600`). Root rendered with:

```sh
pdftoppm -f 1 -l 1 -r 150 -singlefile -png /private/tmp/wtc7-preservation-20261008.p204IY/NYC-WTC_000153904.pdf /private/tmp/wtc7-preservation-20261008.p204IY/page-1
```

Exit0, PNG completion mtime20:41:05 -0400. Exact response/PDF/PNG were copied
without overwrite to this unit under ordinary scoped worktree approval
(`364efa`, `53fb01`). Root's three `cmp` commands produced no differences
(`f07292`); the later independent comparisons used `set -e` as well.

| Preserved artifact | Bytes | SHA256 |
|---|---:|---|
| response.json | 26,269 | `328a3a58d22d98c4cbc56ff8683ce618bfd76cbeebb33be8fccbfc3e23432542` |
| NYC-WTC_000153904.pdf | 23,291 | `39d411bde551a5325676aab504303cfecd70dec208e7a868354fab821c057111` |
| page-1.png | 36,248 | `d9b091d51dae83e04802b95c5e053ceb01568f2a2fd0a5c143cf555da6b2ff4d` |

Separate source/derivative checker: `ece0fe` confirmed PDF metadata and
Poppler26.05.0 for both bundled override commands. A new scratch directory
`/private/tmp/wtc7-preservation-independent.4ysvFD` held its rerender:

```sh
pdftoppm -f 1 -l 1 -r 150 -png /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-preservation-2026-10-08/NYC-WTC_000153904.pdf /private/tmp/wtc7-preservation-independent.4ysvFD/page
```

`7cf1a6`, exit0, empty output. `32e889`, exit0: preserved response/PDF/PNG
match initial scratch bytes; fresh PNG matches preserved PNG. Python3.12.14
and Pillow12.3.0 decoded all three PNGs as 1289×1699 RGB, 6,570,033 sample
bytes, identical decoded SHA256
`d5fa7afbc243eb2860bdc60b80e987cfe358fea0da68713a7cd102816b96ae77`.
Hashes stayed unchanged. This repeats a shared renderer; it is not independent
renderer validation or historical authentication. No repository write or new
request occurred during the separate check.

## Content review and preservation

Root inspected the complete page with `view_image` and froze
root-observations.md at SHA256
`2dfdeb462b6d4218b80864f42190a6e3d2295740614921815ca5c0c85ccec03b`
(`6e9152`). The separate reader viewed the complete image once at original
detail without root's notes, OCR or other items, and froze review.md at
`d29e0f9d1a461893f9d59fc87766ca9ba0cb45232b1ba0df0d2f351c5ab38217`
(`323596`). Root then read that entire review (`3d8519`). No material content
disagreement; medium-versus-object qualification retained in the report.
Two AI readings of one access copy are not independent historical evidence.

Root rechecked the unchanged v3 material index using its existing wrapper
(`927310`, exit0): all 272 selected artifact pins and exact prior-content
preservation still pass. This does not yet add the new municipal/F7 records
to that frozen snapshot or constitute a rerun of its 64 software tests.

Audit-only diagnostic failures were not evidence results: a broad directory
listing/combined read was truncated and not counted as complete coverage;
a guessed synthesis README was absent; root's `.sources[0]` query used the
wrong object shape and was corrected with named fields. The WP5 reviewer
likewise corrected an array-versus-object catalog lookup. Relevant authority
and selected source instructions were read completely in smaller calls.

No historical audio/motion processing, physics solver, legal conclusion,
accepted-engine change, external feedback send, commit or push occurred.
The protocol's fixed one-item content scope is complete; 14 documents/70
reported pages remain open. The full charter stays active and incomplete.

## Closeout review and checks

The separate content reader reviewed the complete root reading, result,
execution record and feasibility update (`43b21e`, exit0), finding no material
correction. Its role overlaps one original interpretation; it is not an
independent expert or new historical source. Root read the complete additive
F7 record (`2cff24`) before linking its bounded consequence.

Final `git diff --check` was clean and all eight listed frozen source/reading
pins remained unchanged (`1ec1da`). A separate read-only Ruby check found no
trailing whitespace in nine new/updated unit JSON/Markdown files and resolved
all 29 local file links (`77b418`). This checks file targets, not section-anchor
accuracy or scientific conclusions. No new software test suite was required
or claimed for these source-reading/documentation changes.

The recurring truncated-reading/pinned-partial issue was deduplicated under
existing SFB-004/SFB-005 in SHERLOCK-FEEDBACK, with only a generic synthetic
acceptance requirement. No new product bug/fix, delivery or acknowledgment is
claimed. Current STATUS and research navigation link this result and the full
feasibility update. No new viewer, server, monitor or live wait was started.
