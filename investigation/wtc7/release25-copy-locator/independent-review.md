# Independent local review

2026-09-20 UTC. Text and held-response review only. No new external call,
media retrieval/playback, image viewing, or source change. Only this review
note was written. Main controls/charter remain as previously read and pinned.

## Disposition

No material source/claim contradiction was found in the reviewed report and
ledger. The held-catalog nonmatch is reproducible for the declared scope,
not evidence of absent footage. The report retains the distinction between
the **previously** located eight-file directory and a current copy/content
join, which remains unresolved. It does not turn the reported 429 failures
into empty availability results, claim an exhaustive search, authenticate
camera/DVD origins, or alter the causal ranking.

One minor wording clarification was sent to root: the report says no new
source body was acquired, although two documentation pages returned parsed
text. Prefer “No new raw source body was saved; no media ...” to distinguish
readable documentation from an acquired/preserved target response. This does
not change the locator result. Later report versions need a new version pin.

## Actual independent checks

- Read the entire current protocol, root ledger and report. Reversing the
  protocol's `Source-of-truth,` newline `falsification` typography correction
  to the previous `Source-of-truth,+falsification` bytes reproduces prior
  SHA-256 `2f6a4cd493afe5dae652404c12566e160f93abbe2ea2cd4ed21f31721570f491`.
  Thus the claimed typography-only change was checked, not assumed.
- Loaded all six specified `structuredContent.files` arrays, not merely
  selected titles. Independently recomputed every response's byte count and
  SHA-256 and asserted exact agreement with all six rows of the pinned root
  ledger. Row counts are 9, 239, 6, 2, 24 and 2: **282 rows, 282 unique IDs**.
- Repeated case-insensitive
  `42A0122|G25D33|Video[_ ]?List|\.mdb\b|VTS_01` against
  `json.dumps(item)` for every one of those 282 objects: **zero matches**.
  This searches returned item metadata, not media or unreturned objects.
- Each response's structured content has exactly the `files` key. All 282
  `parent_ids` values are null. These normalized records do not demonstrate
  exhaustive pagination or independently supplied ancestry.
- Read the corresponding six request JSON files. There are 39 returned
  folder records; exactly four IDs intersect the six requested folder IDs,
  leaving **35 returned-but-unlisted folders**. The other MIME counts are
  239 MP4, two WMV and two text records. This is a response-set reconciliation,
  not a current repository inventory or inspection of those recordings.
- Reconciled the ledger totals with my actual lane: root two queries/four
  requests plus agent four/one = **six queries/five requests**; three failures
  are root-reported. Root's three availability calls were one parallel batch,
  not three retries. My successful documentation open was not a failed API
  call. Unused allowances do not imply additional attempts.

The first supplemental folder-count script incorrectly used `mimeType`,
where the normalized response uses `mime_type`. Its folder assertion failed
(exit 1); the six pins, 282-row/unique-ID count and zero-pattern match had
already printed correctly. After inspecting the actual schema, the corrected
full run repeated those checks and passed all assertions (exit 0), including
the 39/4/35 folder count and protocol-delta reconstruction. No failed check
was relabeled a pass or source altered to obtain the result.

## Limits and strongest alternative

Root's transport status, reported HTTP 429 and request settings remain its
execution account: no target response body was available for independent
transport verification, and I did not replay those requests. Absence of such
a response cannot be substituted for `archived_snapshots:{}`. Copies may be
renamed, transcoded, held in the 35 unlisted folders, or absent from indexed
metadata. Generic DVD filenames and source-catalog IDs cannot by themselves
identify matching content. A populated old/current copy crosswalk or a
specifically identified accessible file set could change the failed-join
result without changing any physical conclusion.

## Reviewed versions and reproducibility

| File in this unit | SHA-256 |
| --- | --- |
| PROTOCOL.md | `a8b62c7fbd1be7693c7ea560cc0dd83525fca067ba5244e639254908c75a8659` |
| root-search.md | `9519499d19e9bdbde8ff477c54ae242f42656cbc1b94ae8a860850366dc76d9a` |
| report.md | `159d56964477dbac37b830f4b9abe2bf1abf6a3ea9d286d0066a5f7ffdbad5d1` |
| current-copy-search.md | `ddecf52394d09bcb974a004ac42f2435d73a191a05bb2a12029b95fce8f9b045` |

Source files are the six `*-list.response.json` / matching request pairs
named in the pinned ledger, under
`../late-fire-original-tape-catalog/sources/`. The independently recomputed
six full source hashes and byte counts match that ledger exactly; no new
source copies were made. Reproduction uses Python standard-library
`json.loads`, `json.dumps`, `re.compile(pattern, re.I)`, `hashlib.sha256` on
raw response bytes, and set comparisons of file `id` values. Folder membership
uses `mime_type == 'application/vnd.google-apps.folder'`; requested IDs come
from the saved `/folders/` URLs. This is a metadata/source consistency check,
not human acceptance, scientific validation, or a newly run legal validator.

## Current-version resolution

Re-read the complete corrected report, 3654 bytes, SHA-256
`4560671f052910d3fc4990f68fbe624e61ff7028f7fb7767e36a3d6b7ff637d7`.
It now distinguishes no newly saved raw body from the two parsed documentation
responses that were read. Reversing exactly that paragraph replacement
reproduces the earlier report SHA-256 `159d5696…` pinned above; no other
report delta was assumed. The minor clarification is resolved. No remaining
material inconsistency was found within the local metadata/text scope, with
all transport, historical-authenticity and content-review limits above
unchanged. Initial review text is preserved, not silently rehashed.
