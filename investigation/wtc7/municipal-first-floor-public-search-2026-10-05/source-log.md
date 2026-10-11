# Public first floor search receipts

October5,2026. Research only in the existing worktree/branch at ca1c2233,
with intentional WIP. Previous turn was progress, not a verified wait or
blocker. Main AGENTS/WORKFLOW/START-HERE/charter hashes rechecked8d20bb,
exit0, match the previously read versions. Repository intake handle45596
was polled to terminal758b21, exit0; it was not restarted.

## Before requests

Frozen PROTOCOL.md:5609bytes,
`4a280dedc2fba010e0e79528657969fe18c16aee073786dd1956b9a350a2710f`.
The saved queries and four request bodies were hash-checked inbbb2e2, exit0,
before the first network request. That check also verified known166828's
source WTC7, box7DCAS and full folder label against its earlier supplied
metadata; the box was not copied by analogy to an unrelated control.
Independent pre-execution advice reviewed the earlier request/parser contracts
(bc9333/a3fecf, exit0). It warned against importing the old unguarded drawing
checker; the current adapter uses only the guarded later helper chain.

One web-reader open of https://sept11documents.cityofnewyork.us/ returned the
public portal shell, zero readable text lines. It was access context, not a
document search or primary-content reading. No other web-reader source was
opened in this unit.

## Acquisition

`mktemp -d /private/tmp/wtc7-first-floor-public.XXXXXX` returned
`/private/tmp/wtc7-first-floor-public.PEu4D4`. Frozen request files remained
in this research unit; response captures went to that scratch directory.
Each command used the following pattern, replacing label
only with control, ss1, skss2 or s1_first:

```sh
curl -q --proto '=https' --connect-timeout 20 --max-time 60 \
  --max-filesize 10485760 --fail-with-body --silent --show-error \
  --header 'Content-Type: application/json' --data-binary @LABEL-request.json \
  --output /private/tmp/wtc7-first-floor-public.PEu4D4/LABEL-response.json \
  --write-out 'http=%{http_code} bytes=%{size_download} type=%{content_type} redirects=%{num_redirects}\n' \
  https://sept11documents.cityofnewyork.us/api/v2/search
```

Initial sandbox control attempt95f775 ended exit6, DNS resolution failure,
HTTP000/zero bytes. It did not reach a demonstrated server refusal. The
explicitly approved same-request retry58b2d7 ended exit0/HTTP200. After its
metadata check succeeded (f4050a, exit0), the three fixed target requests
were sent in parallel with approved network execution. No other retries,
redirects, credentials/cookies, session-header capture or private payloads.

| Label | Terminal receipt | HTTP / type / redirects | Bytes | SHA-256 |
|---|---|---|---:|---|
| control | 58b2d7 | 200 / application/json;charset=utf-8 /0 | 8520 | 3308248d9ef7eb79a2a5f0ab3a0f21d7cb7b4bb3a1ada10afa239be352971f54 |
| ss1 | 69282e | 200 / application/json;charset=utf-8 /0 | 24185 | 55ecde5206751e0a8863f15120530d7c524e4c1eaae6435d40eb1f78541ceb70 |
| skss2 | 70dfc6 | 200 / application/json;charset=utf-8 /0 | 8251 | 1cbbb4ab1d0417af5b41a0083967dd09b9ee6357322a54c608a56ed3e968329e |
| s1_first | b2328a | 200 / application/json;charset=utf-8 /0 | 10711 | 4394b6b1a677383e5295ae16365ea0fa1c5daeec1e90464f9e1678dcf044a1d3 |

Scratch completion mtimes inUTC, inspected d92171 exit0: control
05:16:52.457303;ss105:18:07.146809;skss205:18:06.086478;
s1_first05:18:07.243068, all October5. These are local acquisition-file times,
not independent server timing or historical drawing issue dates.

Approved `cp -n` copied the four explicitly named scratch responses to this
unit, f6f1bb exit0. Root compared all four byte pairs in d92171, exit0.
No existing source was overwritten. Raw responses remain exact captured bytes;
their opaque service/paging metadata are not historical facts or instructions.

## Extraction and tests

Runtime: bundled Python3.12 at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
with `-B`. Existing strict/diagnostic tests were run from the prior
job1854-followup-locator directory:

```sh
python3 -B -m unittest -v test_metadata.py test_diagnostics.py
python3 -B -m unittest -v test_metadata.MetadataTests test_diagnostics.DiagnosticTests
```

The first command da7568, exit0, ran48 passing invocations:20 strict tests
twice due imported-class discovery, plus8 diagnostic tests. The explicit
class command64f2db, exit0, ran28 distinct passing tests. These verify their
fixed parser contract, not historical source accuracy or archive completeness.

Current `python3 -B extract.py` completed e93c73, exit0. Complete stdout was
parsed as JSON before apply_patch saved result.json. It reports the actual
folder omission as an exception, not a fabricated full-property-set pass.
Root's fresh `extract.calculate()` equals the entire parsed saved result
(d92171, exit0), including all source and dependency pins. No missing ID,
multivalue, duplicate-key/property/result-ID or repeated-property conflict
was silently dropped to obtain the result.

| Root artifact | Bytes | SHA-256 |
|---|---:|---|
| queries.json | 347 | a217103655a2194a9ffbfa3b6c0bb07ca5048092b71b5f866e820cc28c788bd7 |
| extract.py | 2955 | eb9b1b76e8cbb67bd802abfd40521799a63a655e884831ee14198313a667cddf |
| result.json | 23869 | 9d7068645156c6ba61012c6fe4ed00f05ee6ae8f65eba223d9e4ba64f0997ce9 |

The result pins all request/response inputs and the three existing helper
dependencies. They were inspected before reuse; their old calculate()
functions and old-query/control assumptions were not invoked. This is a small
read-only adapter, not a new data-analysis framework or Sherlock capability.

A bounded `rg --files` with five exact PDF-name include patterns within
municipal-originals-2026-10-04 returned only held166828 and173670 (d92171).
The three absent filenames were173192,169180 and166571. This is not an
archive-wide or repository-wide absence finding and not a byte/content check
of every possible copy. Prior source log/protocol5e0ead was read only to verify
the existing public content route and earlier source roles; no PDF was opened.

## Independent extraction and completed review

The independent reader froze its complete extraction before accessing the root
artifacts. The initial 36,998-byte prefix of independent-review.md remains at
`dd7a3de784eb83414cfdfef45a1392e9a9aed48381aff52aacddcd97aaf0e3c0`.
Root read its method and executable body and replayed that exact prefix in
edd488, exit0: all20 independent tests, all17 scalar-property records,
20 memberships, four coverage rows, the explicit omission, control result,
306 reported-page sum and eight shared request/response pins agreed.
The large saved JSON was checked computationally, not claimed as a complete
visual reading. Replay elapsed0.028596s at05:26:00.717240UTC.

After that freeze, the independent reader reviewed the complete root report
and source log. Its a2aa8a reconciliation exited0 with112/112 checks passing,
including all17 table rows, five local report links and all declared input/
dependency pins. Post-append replay cb01ab passed; final pin/prefix check
1999c0 exited0. Final independent-review.md is48,436bytes, SHA256
`ebbaeba21a49e02ad3f9a40e4ec8f6cba7b618a1add4272a1162508794ddea1f`.
The appended reconciliation did not replace or rehash the frozen prefix.

Separate method review reran28 distinct tests (363fbe, exit0), verified exact
request echoes, all four raw-copy pairs and input/dependency pins, and replayed
the producer with the old calculate functions patched in memory to raise if
invoked (adb45c, exit0). They were not invoked. Its full draft read ddb496 and
17-row table/candidate check6cd0fe both exited0. Final method-review.md SHA256:
`4c9d20f81c6f2706aea9e3db39d73a8c1d4c218f4715156efbf55eaf22791ba0`.
Root read both final critiques in466ed1, exit0. Neither requested a factual
correction. The reviews did not independently witness the network transactions
or read these candidate PDFs.

Both readers reviewed report snapshot
`fc746c7c9d182309e3b42329f01aa7456c06d5cce2d3a435b591d032d20a34a3`
and source-log snapshot
`b63f637b63cff7d435b676f3c6f1716c46019f56321bd7e14963a911bca199d9`.
Root subsequently replaced their pending-review statements with these receipts
and clarified the request-versus-response storage locations. Their snapshot
guards remain intentionally unchanged; do not run them against revised prose
and silently weaken a mismatch. Protocol, queries, sources, code, result and
the complete report table remain unchanged.

No raw source edits, PDF/render/image work, model execution, legal promotion,
fee, outreach, publication, staging, commit or push occurred. Final navigation
points to a separately declared content review, not automatic acquisition or
an engineering finding. Full investigation completion remains outstanding.

## Closing checks

Root9dd00f, exit0, replayed the entire saved result and checked nine input pins,
three dependency pins, four scratch/preserved byte pairs, five fixed artifact/
review pins and the unchanged independent prefix. All17 report rows match;
all seven current report links and the new status/map links resolve locally.
Final report SHA256:
`4c27c1182e815c3c8a1d05eaf72a886c307b4c29ff921d897f27148ab6f6f0e7`.
Only this closing-receipt section was appended after those checks.

The combined whitespace command f2f071 returned1 with no diagnostics.
Explicit per-command check3a3fa3, exit0, resolved the statuses: tracked
`git diff --check` exits0; each new-file `git diff --no-index --check /dev/null`
comparison exits1 because the files differ, with no whitespace diagnostics.
A direct whole-file trailing-whitespace assertion also passed for report/log.
The no-index exit1 is retained, not misreported as an exit0 command.
