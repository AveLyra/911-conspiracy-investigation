# Folder metadata acquisition and verification

## Sources and actual retrievals

October 4, 2026. Protocol SHA-256 before external reads:
`e4ec67f60955ee307fb0dc21cc43592f00e2ee16585de4a48469254f3f36d9fe`.

The web reader's three GitHub blob opens failed with `Cache miss`
(`turn747view0`, `turn747view1`, `turn747view2`). These are tool retrieval
failures, not evidence that GitHub or the City refused access. One direct
raw GET for each exact file then succeeded. A fourth GET read the CLI named
by the adapter, necessary to inspect the public request interface. No acquired
Python file was executed or imported.

All four upstream URLs share
`https://raw.githubusercontent.com/pranava0x0/sept11documents-mcp/main/`:

| Saved file | Exact suffix | HTTP | Bytes | Type | Redirects | Tool completion |
|---|---|---:|---:|---|---:|---|
| folders.json | docs/data/folders.json | 200 | 421135 | text/plain; charset=utf-8 | 0 | 52b097, exit 0 |
| catalog-summary.json | docs/data/catalog-summary.json | 200 | 1160 | text/plain; charset=utf-8 | 0 | a40905, exit 0 |
| portal.py | sept11/adapters/portal.py | 200 | 20905 | text/plain; charset=utf-8 | 0 | 6261bc, exit 0 |
| portal_api.py | scripts/portal_api.py | 200 | 4177 | text/plain; charset=utf-8 | 0 | 5254dd, exit 0 |

Direct GETs used `curl -q --fail --silent --show-error --max-time 60
--max-filesize 10485760 --output <scratch-file> --write-out <receipt> <url>`.
The first three also allowed at most three HTTPS redirects; actual redirects
were zero. The CLI request did not follow redirects. No credentials or cookies
were supplied. Scratch directory: `/private/tmp/wtc7-folder-locator.RayuZv`.

Two subsequent requests used the exact saved JSON payloads, not downloaded
program execution. Endpoint:
`https://nyc.mindbreeze.com/search/september-11/api/v2/search`.

```sh
curl -q --silent --show-error --max-time 60 --max-filesize 10485760 \
  --proto '=https' --user-agent 'WTC7-research-metadata/1.0' \
  --header 'Content-Type: application/json' --header 'Accept: application/json' \
  --data-binary @<saved-request.json> --output <scratch-response.json> \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects} url=%{url_effective}\n' \
  https://nyc.mindbreeze.com/search/september-11/api/v2/search
```

The angle-bracket values describe the two actual request/response file pairs,
not a verbatim runnable command. Structural request completion `3143b4`:
HTTP 200, 11186 bytes; sprinkler `8ac75b`: HTTP 200, 9587 bytes. Both exit 0,
`application/json;charset=utf-8`, zero redirects. Query spacing exceeded one
second. These were two of eight permitted City metadata requests; neither
returned a next page. No export or content endpoint was called.

Local scratch-file completion mtimes in UTC (not server publication dates):
portal.py 19:36:28.735607; folders.json 19:36:30.996323;
catalog-summary.json 19:36:32.597493; portal_api.py 19:38:18.673332;
structural response 19:39:25.708246; sprinkler response 19:39:46.177642.
The two copy operations completed at `aa2f62` and `abd060`, both exit 0.
The six preserved bodies equal their scratch bytes exactly.

## SHA256 pins

| File | SHA256 |
|---|---|
| folders.json | cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704 |
| catalog-summary.json | e30fd353a280639bc560b2ffcb404e2bac36d475a5660e69e4bdf1099d9cb9cc |
| portal.py | 79dffa99e9c3a74b5fcaecb60e7335b0ff1ac6b7f3fcdca12525cb1d0790c4dc |
| portal_api.py | 0b1c3695d8669f2ddb020dd57c4cf2d9e74f02c553d2d91828f3e043874658dd |
| structural-request.json | b2f568e98237707d63661874262b68ec650d8ee26c32da9085198469af1af7bb |
| sprinkler-request.json | d60767327692fc11c2329f95508c5354431c7ea102cd750c9f5f7bc039ee92f6 |
| structural-response.json | 470c1b10d25218dcf05319199591bea8f906b178e05d92f78711622e70fe247a |
| sprinkler-response.json | 05d526268ba8ae78cb90c6a507d5076b29980ef920a7954c01e080e5470a470f |

The branch name `main` in upstream URLs is mutable. These hashes identify
the acquired bytes; no upstream commit identity or original City snapshot
authenticity is asserted. Captured counts are source statements, not new
archive-wide measurements by this investigation.

## Root verification

Python 3.14.0, standard library only, stdout-only checks. The initial shape
probe tried `folders` as a container and printed zero rows. It also printed
the actual top-level keys; the subsequent check used the observed `rows`
field and `columns` array. No empty-catalog finding was made or relied upon.

The final check (`615785`, exit 0) required: the exact six-column catalog
schema; 4205 rows; one match per first Bates; the exact echoed request;
false previous/next flags; every service reporting `NO_MORE_RESULTS`;
one value per property and no duplicate property IDs; exact source/box/folder
joins; valid document-key syntax; agreement among key, title and result ID;
positive integral page/byte counts; document and page sums matching each
folder; first IDs present; five unique IDs overall; and six preserved files
byte-identical to scratch. All passed. The endpoint's `estimated_count`
also reported 3 and 2; coverage does not rest on that estimate alone.

The substantive calculation can be reproduced locally without any network
or downloaded-code execution from this directory:

```python
import json
from pathlib import Path

p = Path('.')
catalog = json.loads((p / 'folders.json').read_text())
assert catalog['columns'] == [
    'source_index', 'box', 'folder', 'documents', 'pages', 'first_bates']
assert len(catalog['rows']) == catalog['rows_total'] == 4205
seen = set()
for label, first in [('structural', 'NYC-WTC_000167235'),
                     ('sprinkler', 'NYC-WTC_000171300')]:
    matches = [r for r in catalog['rows'] if r[5] == first]
    assert len(matches) == 1
    folder = matches[0]
    response = json.loads((p / f'{label}-response.json').read_text())
    request = json.loads((p / f'{label}-request.json').read_text())
    assert response['search_request']['user']['query'] == request['user']['query']
    rs = response['resultset']
    assert rs['prev_avail'] is False and rs['next_avail'] is False
    assert rs['per_service_dataset']
    assert all(s['termination_cause'] == 'NO_MORE_RESULTS'
               for s in rs['per_service_dataset'])
    rows = []
    for result in rs['results']:
        pairs = []
        for prop in result['properties']:
            assert len(prop['data']) == 1
            value = prop['data'][0]['value']
            assert sum(k in value for k in ('str', 'num')) == 1
            pairs.append((prop['id'], value.get('str', value.get('num'))))
        assert len(pairs) == len(dict(pairs))
        row = dict(pairs)
        assert (row['source'], row['box_name'], row['folder_name']) == (
            catalog['sources'][folder[0]], folder[1], folder[2])
        key = row['mes:key']
        assert key not in seen
        seen.add(key)
        assert row['title'] == key + '.pdf'
        assert result['id'] == f'september11 Connector:September11_MD:{key}:'
        rows.append(row)
    assert len(rows) == folder[3]
    assert sum(int(r['page_count']) for r in rows) == folder[4]
    assert first in [r['mes:key'] for r in rows]
    print(label, [(r['mes:key'], r['page_count'], r['pdf_size']) for r in rows])
assert len(seen) == 5
```

This excerpt reproduces the ID/count/join calculation. The earlier execution
additionally performed regex/numeric-type and six-file byte-copy checks as
listed above; the excerpt is not mislabeled as their exact full transcript.

## City hostname confirmation and independent review

After the backend response review, root sent the same two saved request bodies
to the adapter's FRONT endpoint,
`https://sept11documents.cityofnewyork.us/api/v2/search`, to verify the route
directly through the City hostname. Same curl parameters, no redirects followed.
Structural completion `918351`: HTTP 200, 11120 bytes, JSON, zero redirects,
exit 0. Sprinkler completion `a7f130`: HTTP 200, 9587 bytes, JSON, zero redirects,
exit 0. These are requests three/four of the eight-request ceiling, with one
backend and one City-hostname result page per folder. No further page was
indicated or fetched. Ten record appearances represent five unique IDs.

| File | SHA256 | Local completion mtime UTC |
|---|---|---|
| structural-front-response.json | 858004f96f45f33ac637a6ae7d84cf7b6e4c8c6750df285b316b37eef77c913a | 2026-10-04 19:45:50.144468 |
| sprinkler-front-response.json | 61f3eb3219955a11c9648fb50b8603e98e7de0ca99d15f230cc1eb4ad2beec13 | 2026-10-04 19:46:21.066442 |

Root's stdout-only JSON comparison (`2e3d28`, exit 0) required equality of
the full echoed request, estimated counts, document IDs and every selected
property's complete data array between each backend/City-host pair; it also
required false previous/next flags, one service and `NO_MORE_RESULTS` for
the City-host response. Both pairs passed. The raw byte hashes differ, so
these are semantically matching selected records, not byte-identical entire
responses. Their service ID is the same documented backend. Copy operation
`fd705e` exited 0; these two source bodies were preserved separately.

The independent initial metadata review froze at
`9eab085e9209707ee16b1640ee9ff2ad3d29ee50f0f284fad3a44ab9ba176f14`.
The independent saved-backend-response review froze at
`1281709e1a93df1c3adc711adcbfb751f7561ca93ad158507a5d32616235239f`.
Root read both full notes. They independently establish the same five IDs
and scoped coverage, not another historical source or source-content review.
Their additional checks and the folder-filter syntax ceiling remain explicit.
Root's saved reproduction excerpt above then ran successfully (`5bd286`,
exit 0), followed by `git diff --check` with exit 0 and no diagnostics.

## Final verification and handoff

The [post-result synthesis review](synthesis-review.md) found no material
correction required. It independently checked the City-hostname pairs and
found matching full selected-property arrays; whole-response differences
were confined to ranking/order fields. Root read the complete review. Its
SHA256 is `0b4847c0935bcc81be1dddfe8f98ffd9a28a80c9a6622c8150de942bff72b33e`.
The reviewed report remains unchanged at
`410a4190ec8951a8aa9da78e22bdf1ef5e75155f2d12e7c999b0c57031d7152d`.
This log's reviewed pre-append version was
`6817f52bbf48cac1f5efb07a9bd71364fd3df2faedd727cf91a0031c460dd71c`;
this closing receipt is additive, not part of that earlier freeze.

Root's final strict four-response check (`23273a`, exit 0) rejected duplicate
JSON keys and property IDs, required exact requested property sets and full
request echoes (only the returned empty `user_context` removed), literal
folder tuples, valid positive integer page/byte fields, unique agreeing IDs,
matching counts/page sums, the expected terminal service, and equality of
records between access routes. All four responses passed.

Final preservation/navigation check (`366692`, exit 0): ten upstream/request/
response pins, protocol and two review pins, eight exact scratch/preserved
copies, and three earlier-unit frozen pins passed. All thirteen then-present
local Markdown links resolved and whitespace checks passed. `git diff --check`
was clean. The later synthesis link is checked separately after this append.
Research README and STATUS were read back after their updates. Branch remains
`research/sherlock-wtc7-investigation`, HEAD
`ca1c223335c20905d6608eb15c676f88cbfac734`, with intentional uncommitted research
WIP. No staging, commit or push occurred.

This unit is complete; the full goal is not. The next action is the declared
three-PDF content comparison described in STATUS, not repeating metadata
arithmetic or treating successful lookup as completed scientific investigation.
Existing SFB-005 already covers the observed catalog/locator-grain need; no
new product-defect claim or feedback transmission was made. The prior verified
archived-destination boundary remains unchanged.
