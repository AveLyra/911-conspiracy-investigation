# Public first-floor lookup: method and preservation review

October 5, 2026. Local research only. **No material defect found in the fixed four-request extraction or response-copy preservation.** One returned record remains an explicit missing-folder exception; this is not an eleven-field-complete population or evidence of archive-wide search recall. This review is separate from the independently implemented semantic extraction assigned to another reader.

## Scope and actual checks

Read the complete [protocol](PROTOCOL.md), [query list](queries.json) and [extractor](extract.py), all four request JSONs, required response structures and the saved [result](result.json). Reviewed the reused diagnostic/adapter contracts in the immediately preceding preflight; their pins remain unchanged. This turn additionally read the complete base `test-acceptance-locator/check_metadata.py` and both inherited synthetic test modules before execution. No primary PDF/image, model input or new network request was opened. Only this new method note was written.

- `4cafa6`, exit 0: complete protocol/extractor/query read and finite unit listing.
- `61f139`, exit 0: complete base helper and both test-module reads; fixed scratch filenames located. No transport-header contents were read.
- `363fbe`, exit 0: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_metadata.MetadataTests test_diagnostics.DiagnosticTests`, from the existing `job1854-followup-locator` directory. **28 unique tests passed in 0.005 s.**
- `adb45c`, exit 0: stdout-only request/response, byte-copy, pin and scoped producer-replay checks described below. Runtime `/opt/homebrew/opt/python@3.14/bin/python3.14`, bytecode disabled.
- `108ccd`, exit 0: helper/test pin receipt; `report.md` did not yet exist. No synthesis verdict is implied by this method note.

Root's earlier module-level unittest command produced **48 invocations of 28 distinct tests** because `test_diagnostics` imports the 20-test `MetadataTests` class, which is discovered again. The explicit class selection above avoids that repeated discovery. Do not describe either run as 48 distinct tests. These are parser/diagnostic tests, not 28 live searches or engineering tests.

## Exact requests and route-control interpretation

Independently checked that `queries.json` has exactly the protocol's four labels in order, and each original query string appears verbatim in the frozen protocol. Each saved request equals the declared structure: count 50, content sample length zero, the same eleven VALUE properties and the exact query. Every response echoes that entire request, allowing only an absent or empty `user_context`; no differing query was silently accepted.

The known-packet control actually returned **NYC-WTC_000166828**, with source `WTC 7`, box `7DCAS` and folder **Mayor's Office of Emergency Management Alt. Route for Oil Pipes**. Those values were checked in the returned control record, not borrowed from the older 167873 control. The extractor tests membership, not an assumed singleton outcome. The same ID appears in `ss1` and `skss2`, but **not** in `s1_first`.

This is a useful positive retrieval/control result and an important query-specific limit. The known packet's appearance under the sheet queries does not establish exact-phrase matching, reliable punctuation/OCR behavior, calibrated recall, or coverage of every applicable revision. Its absence under the paired `"S-1" "first floor"` request cannot establish that a relevant plan is absent. Prior knowledge of the packet's contents is from earlier readings, not a new content inspection here.

## Response-copy preservation and observed coverage

Compared each canonical response's complete bytes directly with its same-name file in `/private/tmp/wtc7-first-floor-public.PEu4D4/`. All four comparisons matched, and the hashes below were independently calculated. This verifies copy preservation from that scratch capture, not transport status, TLS configuration, retrieval time or historical authenticity.

| Query | Bytes | SHA-256 | Returned / estimated | Results key | Next / previous | Service termination |
|---|---:|---|---:|---|---|---|
| control | 8520 | `3308248d9ef7eb79a2a5f0ab3a0f21d7cb7b4bb3a1ada10afa239be352971f54` | 1 / 1 | Present | false / false | NO_MORE_RESULTS |
| ss1 | 24185 | `55ecde5206751e0a8863f15120530d7c524e4c1eaae6435d40eb1f78541ceb70` | 15 / 15 | Present | false / false | NO_MORE_RESULTS |
| skss2 | 8251 | `1cbbb4ab1d0417af5b41a0083967dd09b9ee6357322a54c608a56ed3e968329e` | 1 / 1 | Present | false / false | NO_MORE_RESULTS |
| s1_first | 10711 | `4394b6b1a677383e5295ae16365ea0fa1c5daeec1e90464f9e1678dcf044a1d3` | 3 / 3 | Present | false / false | NO_MORE_RESULTS |

These are four uncapped returned response sets according to the service metadata, not a finding that the index searched every document or that every applicable drawing was returned. There was no pagination, query broadening, source download or fresh HTTP request in this review.

## Reuse, missingness and accounting

The new extractor imports the three pinned helpers and calls `diagnose_query()` for the new four requests. The helper modules have guarded entry points; their old `calculate()` populations are not invoked on import. To check the actual replay path, all three old `calculate()` functions were temporarily patched **in memory** to raise if called. `extract.calculate()` still reproduced the saved result by parsed-object equality. This used the existing producer/validator logic and is **not an independently implemented semantic replication**.

The replay and direct checks confirmed all nine query/request/response pins, all three helper pins and the protocol hash. Raw JSON was also read through a separate duplicate-key rejecting loader for the direct request/copy inspection. Each returned result's property IDs were unique and its retained result ID agreed with its document key. The wrapper preserves ordinal/query/result-ID membership and rejects cross-query diagnostic/property conflicts instead of overwriting them.

The actual exception is **166099, `ss1` ordinal 12**: ten supplied properties, missing `folder_name`. Its key/title/page/byte fields remain usable metadata; its folder remains absent. The result retains the raw exception record, actual supplied values, missing-name list and `strict_valid=false`, with top-level status `explicit_metadata_exceptions`. No literal `None`, empty folder or inferred folder was inserted. All other returned occurrences supplied the requested eleven properties.

Saved producer results are 20 query occurrences, 17 unique document IDs and 306 unique **reported** pages. Thus 19 occurrences/16 IDs are eleven-field-complete; one occurrence/ID is diagnostic-only. Metadata page counts are not newly verified PDF lengths, and distinct IDs need not be independent source families. Positive finite integral counts, scalar/type errors, duplicate IDs/properties, empty responses, missing-folder diagnostics, literal `None`, request mismatch, service/cap uncertainty and cross-query conflicts are covered by the inherited code/tests. No source-level or physical validation is inferred from passing them.

## Reviewed version pins

| Input/code | SHA-256 |
|---|---|
| PROTOCOL.md | `4a280dedc2fba010e0e79528657969fe18c16aee073786dd1956b9a350a2710f` |
| queries.json | `a217103655a2194a9ffbfa3b6c0bb07ca5048092b71b5f866e820cc28c788bd7` |
| extract.py | `eb9b1b76e8cbb67bd802abfd40521799a63a655e884831ee14198313a667cddf` |
| result.json | `9d7068645156c6ba61012c6fe4ed00f05ee6ae8f65eba223d9e4ba64f0997ce9` |
| job1854-followup-locator/diagnose_metadata.py | `98b7a748aa7abe4c8dd1b25c9cbe930a98f6cfc42e59fd373344a82e766540a2` |
| job1854-followup-locator/check_metadata.py | `6f51bfda7c4cf6508ab0095240bbbba3b935d8f23f0bae957bc36f42f8986b72` |
| test-acceptance-locator/check_metadata.py | `d561ee20e778bd0111103b3352f251396f618f2be2a23ad172ad96efb7ac6d7a` |
| job1854-followup-locator/test_metadata.py | `cefeec65be44795043c7ed04eda86730fb4005b993af8eeb9e4d3f7ad91d8479` |
| job1854-followup-locator/test_diagnostics.py | `c159ca2ee7592498f24b20a39120eeff95e0badf5c6edd9cf90e3e2a15fe98c6` |

The helper/test paths in this table are relative to `../municipal-originals-2026-10-04/`; the first four are this unit. Complete exact request/response pins remain in `result.json`. The frozen sources, previous observations and old failed full-contract extraction were not modified or relabeled. Final synthesis and independent semantic reconciliation remain separate before unit closure.

## Subsequent draft synthesis review

The initial method note above was saved at SHA-256 `7af0fc173f915956eb7aa778aa845ffe65d9221e0ac462837d1e504e9ac5caa0` before the report became available. Then read the complete 138-line `report.md` and 112-line `source-log.md`, `ddb496`, exit 0. Reviewed report SHA-256 **`fc746c7c9d182309e3b42329f01aa7456c06d5cce2d3a435b591d032d20a34a3`**; source-log SHA-256 **`b63f637b63cff7d435b676f3c6f1716c46019f56321bd7e14963a911bca199d9`**. No further primary source or network work followed.

No material correction is required in those snapshots. A separate stdout-only saved-result/table check, `6cd0fe`, exit 0, verified all **17** table rows against the saved result: exact supplied folder strings or explicit missingness, page/byte counts, query-membership order and complete ID coverage. It also checked the prioritized candidates' reported **4/25 pages** and the separate **CO56** label on 168526. This checks synthesis transcription, not PDF contents or a second raw semantic extraction.

The report preserves the decisive distinctions: 166828 is retrieved by control/ss1/skss2 but not s1_first; service-reported completion is not archive recall; 166099's omission differs from 171506's literal `None`; 306 is a metadata page total, not acquired/reviewed pages; 173192 and 169180 are conditional content candidates, not proven applicable drawings. It does not treat odd-looking labels as established false positives or tampering, and retains unselected leads including 168526. Different project/revision, duplication or unreadability could defeat the proposed joins. The 48-invocation/28-distinct-test account is accurate.

The source log's acquisition/transport history remains root-attributed: this reviewer checked captured-byte equality and request/response consistency, not a second HTTP transaction or independent network witness. Independent semantic reconciliation and final navigation/closure checks are outside this scoped verdict. No report, source log, frozen input or prior observation was edited by this reviewer.
