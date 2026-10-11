# Independent NBC saved-metadata review

October 8, 2026 local / October 9 UTC. Scope: saved catalog records and, by a
later bounded instruction, consistency of the parent's report/execution with
the sanitized acquisition disposition. No network calls, downloads, temporary
reference access, media viewing, listening, or historical annotation occurred.

## Finding and review boundary

No material discrepancy found in the checked catalog joins, returned roster,
selection, sizes, or the reviewed report's distinction between two returned
candidates and zero acquired media. This is a separate AI computation and
interpretation of shared saved records, not independent acquisition,
historical corroboration, actual human review, or scientific acceptance.

The evidence-falsification-auditor and source-of-truth-guardian skills informed
the separation of saved metadata, provider assertions, acquired bytes and
source/causal conclusions. Main instructions and investigation charter remain
controlling. No legal, source, accepted-engine, ranking, or human-gate state is
changed by this review.

## Catalog joins and population

The saved chain is mechanically consistent:

| Returned folder | ID | Next saved request |
| --- | --- | --- |
| WTCI-97-I-Multiple | 12az7liDQ8eWu54A09qj-KT8YcNPo0Cyw | ../longer-copy/sources/gms-child-3.request.json |
| Gilsanz Pres-Jan11-12 -WTC7 | 1bxFiHUzf_I2lbWaWc2LHneV0rvI-pDLo | ../longer-copy/sources/presentation-1.request.json |
| Video-NBC | 1TIdDRzUQ1CLRFju9Hcb0vOt99hRo_8I9 | list.request.json |

Each next request URL exactly embeds the returned folder ID; each requests
top_k 1000. The returned folder URL also matches. The frozen parent response
hash matches the protocol. All relevant normalized parent_ids fields are null:
the support is the saved request/response traversal, not independently
populated provider parent-ID fields or original-camera provenance.

The new response contains exactly two distinct files and zero folders. Both
qualify by video/mpeg MIME and extension. Sorting by case-insensitive title,
then ID, gives precisely the actual metadata-request order:

| Order | Title | ID | Reported bytes |
| ---: | --- | --- | ---: |
| 1 | collapse wtc.mpg | 1uBxFfgQNfD4wXTCz_5si4c5mPFvj0i2S | 2703430 |
| 2 | wtc5.mpeg.mpg | 1UEfuJwL-EXTKTf-YQ1l0F88e5eY6scBS | 99297340 |

These are positive decimal-string size fields, totaling 102000770 reported
bytes, not locally measured media sizes. Each get response agrees with its
list entry on id, title, mime_type, size and file_or_folder. Both requests use
the full declared fields selector and exact fileId. The listing's original
returned order is reversed relative to the deterministic selected order; that
is expected, not a changed selection.

Parsing all eight earlier longer-copy listing responses independently produces
27 rows, 27 unique IDs, 18 files and nine folders. Neither new media ID appears
in that set. This establishes a new catalog branch result, not that their
contents differ from earlier files. Neither new title equals
WTC7COLLAPSE.MPG case-insensitively. No explicit pagination or completeness
assurance exists in the saved new response (envelope keys content, isError,
structuredContent; structuredContent contains files only). The two returned
files therefore cannot be generalized to a complete archive population.

## Omissions and inferential ceiling

Both metadata responses omit md5Checksum, sha1Checksum, sha256Checksum,
videoMediaMetadata and capabilities. Their parent_ids fields are explicitly
null, not omitted; normalized title/mime_type/parent_ids are not evidence that
raw Google response fields were preserved verbatim. Listing can_download is
true for each entry, while metadata can_download is absent. Neither establishes
successful acquisition. source_visibility_status remains access_not_verified.

Consequently the secondary locator's 6:22 and 720x480 cannot be compared here.
Missing returned fields are not zero duration, absent streams, mismatching
dimensions, or proof that Google itself has no such metadata. The seven saved
JSONs total 3959 bytes and preserve normalized connector records, not raw Google
HTTP bytes. Recorded 2019 creation/modification timestamps do not establish
historical camera capture dates. Request clocks explicitly describe UTC tool
request bounds, not source dates.

Strongest contrary interpretation: the WTC7/NBC ancestry and generic
collapse title justify a potentially useful content lead; title mismatch or
WTC5 in the other name does not exclude shared WTC7 footage. Conversely those
labels do not establish WTC7 contents, broadcaster/camera identity, a continuous
third-shot source, original soundtrack, or the origin of a reported bang.
Only admissibly acquired bytes followed by a separately declared source
comparison could begin testing those questions. A picture match alone would
not independently authenticate the soundtrack.

## Additional saved-statement review

I read the complete report.md and execution.md snapshots pinned below, plus
the complete separate acquisition/PROTOCOL.md and sanitized
acquisition/disposition.json. No raw fetch response or temporary reference
value was opened, emitted or reproduced.

The disposition's stable ID, MIME and reported size match selected item 1.
Its returned filename collapse wtc.mpg.mpeg differs from the catalog title;
the report preserves that distinction and does not call it a camera filename.
The record explicitly reports no materialized local-path fields, no inline
base64, local_media_acquired false, and the exact second candidate ID with
request_made false. Its five reference-field entries contain only path/type
descriptors, not reference values. Recorded request parameters and clock bounds
are consistent with the declared sequence.

The report appropriately calls this reference-only/capability-limited, not a
network denial, historical nonmatch or proof of scene silence. However, my
check establishes consistency of saved statements only: I did not independently
reproduce the fetch, confirm the original response shape, inspect the available
tool catalog, or establish that no possible native materialization tool exists.
Those are root execution assertions, not new results of this review. The
sanitized summary cannot authenticate omitted raw response content. The second
candidate's access/content remains untested. No acquired streams or source
match is supplied by the checked records.

The report's externally cited NIST webpage and execution's broader structural,
Polk and WP5 next-work statements were not independently re-investigated.
This review is not blanket clearance of those separate claims. execution.md
is pinned as a pre-review-closeout snapshot; an intentional later appended
closeout requires its own comparison, not a claim that these bytes stayed
unchanged indefinitely.

## Actual checks and receipts

All code was independently authored as read-only Python standard-library
here-documents; it did not import an existing checker or alter the records.

- Initial command: `python3 -B - <<'PY' ... PY`, receipt 8397fa, exit 1.
  Its exact-request assertion mistakenly expected file_id instead of the actual
  saved fileId. A direct read of metadata-1.request.json (a8697c, exit 0)
  identified the reviewer-code mistake. No evidence file or selection changed.
- Corrected complete catalog command, same invocation, receipt 7156a1,
  exit 0, 0.047481333 seconds: 58 explicit assertions passed. It used a
  duplicate-key/nonfinite-rejecting JSON parser; checked fixed protocol and
  parent hashes, successful envelopes, each three-step folder join, unique
  roster IDs, eligibility/sort, full exact request dictionaries, identity/size
  agreement, field presence/null distinctions, prior eight-list counts and
  intersection, exact-title absence, and 18-file before/after SHA256 stability.
- Supplemental command, same invocation, receipt 428185, exit 0,
  0.041269417 seconds: 21 assertions passed. It bound the declared report and
  acquisition-protocol hashes, rechecked all 18 earlier input pins, checked
  clock bounds/IDs, first-request identity/parameters, retained filename
  difference, explicit local-media/second-request dispositions and schema-only
  reference entries, then rehashed the four added records and all 18 prior
  inputs. It did not reproduce acquisition.
- Complete text read of the four supplemental documents: 4cdba5, exit 0.
  Earlier complete catalog/protocol reads and the check commands are retained
  in this task's tool history. Counts of assertions are diagnostic checks, not
  79 independent historical observations or scientific controls.

## Input pins

All 18 catalog inputs were identical across the catalog before/after check and
both supplemental rechecks. The four supplemental inputs were unchanged
across their own before/after check. Except the explicitly compared frozen
protocol/parent/report/acquisition-protocol identities, these are current
review-time pins and stability checks, not invented acquisition-time hashes.

Paths below resolve relative to this review directory; ../longer-copy/sources
is the sibling prior unit. Sources and all preexisting records remain untouched.

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 4311 | `a907bc6458d2e8d8f090003350cbb7774a93cbcd9f32274f5579b1d7b4125bfb` |
| `list.request.json` | 105 | `8bfcf4590a376d80a738e604ac78f82246953322fe3df2fd6fabe1cd154844f7` |
| `list.response.json` | 1823 | `12cf19aeca36bc0e4ee5ce034e0c908657b3a5da7c0380a305c2ab811033f4f7` |
| `metadata-1.request.json` | 182 | `392415ee5a2f02e3f6e04321f2009721cf565d42577e9a6412944306aa690078` |
| `metadata-1.response.json` | 595 | `d4559be622cdce190f8cac8290363bac8d577fb509862212724d69c023a456b6` |
| `metadata-2.request.json` | 182 | `8985e8537d6a1967e0e47188e24e1078bc8c8d924d1c752165057d3ff7671436` |
| `metadata-2.response.json` | 593 | `49ad151ce9d73371ce3fc3b04734d1a6c8c2676651f876e5fd24742d2e25952c` |
| `request-times.json` | 479 | `57ee64a4ea56e5d2ffc6f456f812200d8b6083b703b2150aa3bb3204bce7745a` |
| `../longer-copy/sources/ramon-list.response.json` | 2654 | `760e70a2ea15dac5b675a73d0fdf2c67f4bdac5d73775a7b38d6940e74b37e0b` |
| `../longer-copy/sources/gms-list.response.json` | 3505 | `c28c74bb62b9bc15c82414555170c75eb5551a3b0f730e7ec4128789dd8e1ccb` |
| `../longer-copy/sources/gms-child-0.response.json` | 1853 | `1d3cecf034d3e735ac4abac6c4fbab5662dea770e24dfe04287bd58f081097ba` |
| `../longer-copy/sources/gms-child-1.response.json` | 5155 | `bda2d744f773255f956c52c0de1d068dd3497860077f78298909935b3f264569` |
| `../longer-copy/sources/gms-child-2.response.json` | 2669 | `b602fcc7b32421970a53ed62bac9d8ad3cb88e57e6a68cd392b6e217de107f96` |
| `../longer-copy/sources/gms-child-3.response.json` | 3526 | `05a994810f9ea004c2b57c1a7de4782880a791749d772397d8d328e38b4c23e5` |
| `../longer-copy/sources/presentation-0.response.json` | 3476 | `a09c00fb4d9168b79c76c49cabd98f5d60d6f7f197c325f1ec535520f3ec24e1` |
| `../longer-copy/sources/presentation-1.response.json` | 984 | `2fd6df4507dbf1c6c045f97f342cdacb9eec5653c2b75a59311dc4c3b0f39830` |
| `../longer-copy/sources/gms-child-3.request.json` | 105 | `4feeab1092deaad3f95cb50960e291c92b52c16e5f2b2e88ad1b3e12b1c61a90` |
| `../longer-copy/sources/presentation-1.request.json` | 105 | `bfbf909014def0ac94dc6a7c0a19c548eced1441539530dd85cc529bd8b045ed` |
| `report.md` | 5133 | `e5714369fd7a3262aab2130cf91b0f994eeba99a686ffc650fdff166727e6165` |
| `execution.md` | 5037 | `435b6abead1018705ddb8a92f84de3ec92102a782f2e225af3516ce752846c7d` |
| `acquisition/PROTOCOL.md` | 2973 | `3076fc825071b5693359f0f6c156d620f15db167ed9284419de5d075f9dd4b95` |
| `acquisition/disposition.json` | 1849 | `29416432e071674a1a89f58a0b02ad344c79e83ea1d7efdc3ae35e4bf32fd0ca` |

