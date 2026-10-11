# Technical record review and verification

## Outcome and limits

The frozen 2,468-line feedback snapshot is represented by 277 source-ordered
units: 254 requirement units and 23 context units. Every source line is
assigned exactly once. All 27 earlier digest topics and all five existing
SFB families are mapped. Requirement units retain technical prose, checkable
acceptance conditions, qualifications and publication transformations.

Three writers read disjoint source partitions. Three separate computational
review passes then compared all assigned units with the actual source,
including context exclusions. They identified four transcription/provenance
issues; all were corrected and received targeted reviewer rechecks. Two
additional checker/documentation issues were also corrected. No remaining
material omitted condition was identified in that bounded review.

This supports calling the packet requirement-complete for the selected
feedback snapshot, not universally complete or mathematically lossless.
The reviewers used the same underlying source and were not independent
human investigators or independent evidentiary sources. The principal
remaining objection is semantic: an unnoticed omission can survive perfect
line coverage and passing tests. The source pins, explicit exclusions,
detailed text and correction procedure keep that claim open to challenge.

## Source and review coverage

| Partition | Source lines | Units | Requirements | Context | Separate comparison |
| --- | --- | --- | --- | --- | --- |
| A | 1–821 | 73 | 67 | 6 | All 73 units |
| B | 822–1648 | 60 | 60 | 0 | All 60 units |
| C | 1649–2468 | 144 | 127 | 17 | All 144 units |

The source is 220,999 bytes, SHA-256
`e1c718bb928ba846deb0d527f69cda7ea00a8d888c2247a864b1d666b4204133`.
The earlier delivered digest has SHA-256
`bd3f148bdfb1c5c4c55a33afbba0bedad7e3d3258c224754a12566925d61a740`.
The digest is a topic index, not the authority for detailed coverage.

[review.json](review.json) contains the full reviewed-unit lists, findings,
resolutions, pre-correction partition hashes and final-record binding. The
authoring partitions are local intermediate artifacts, not separately
published competing requirement authorities. Their complete assembled content
is in [record.json](record.json), apart from the recorded corrections and the
addition of source-span hashes. A structural comparison confirmed that only
the eight declared unit objects changed after the partition reviews; the other
269 unit objects remained unchanged. Supplemental status metadata is
separately identified, not falsely assigned to the older source spans.

## Corrections made before publication

| Finding | Resolution |
| --- | --- |
| TR-L0590 could imply the instrument stopped before heating began. | It now says the instrument's recording stops before heating stops. |
| TR-L1405 used “independently” for separate context pins. | Restored “separately pinned”; no new evidentiary independence is implied. |
| TR-L1544 could imply observed visibility before the excerpt. | It now describes the excerpt beginning with the phenomenon already visible. |
| Five older bridge notes included later export-pilot status outside their cited source spans. | TR-L2351, TR-L2353, TR-L2460, TR-L2462 and TR-L2464 explicitly attribute publication-time context to SUP-01; the README and JSON pin that supplemental source separately. |
| A single requirement could lack mappings while global digest coverage still passed. | Per-requirement SFB and digest mappings are mandatory, with two negative tests. |
| Hash privacy language was too absolute. | Clarified that hashes contain no plaintext but permit candidate-text comparison and are not a privacy guarantee. |

SUP-01 is the separately read and hashed local report
`CONTROL-RETRY-RESULT-2026-10-07.md`, SHA-256
`170e97cdc0ea352254270546655ad7f17443e44fa19ca531a720627c680202ce`.
Its reported synthetic export results were not rerun for this publication.
Neither it nor the original feedback log is included as raw source text.

## Verification performed

The packet uses Python's standard library; the final source-bound check and
unit run used Python 3.14.0. Commands are shown relative to the packet
directory; the source argument denotes the exact separately authorized local
snapshot, not a bundled public source.

```sh
python3 -B verify_record.py --source /authorized/path/SHERLOCK-FEEDBACK.md
python3 -B -m unittest -v test_verify_record.py
```

Results: all 2,468 source lines and per-unit byte hashes matched; 277 review
IDs matched the unit roster and final-record binding; 27 digest topics mapped;
the generated view matched the JSON; all 20 unit tests passed. Tests include
gaps, missing tails, overlaps, reordered units, duplicate JSON keys, missing
individual mappings, empty requirements/acceptance, changed source bytes,
source-span mismatches, missing/duplicate review coverage, changed reviewed
bytes, unlisted packet files and altered manifest-pinned files.

The initial render was blocked by the filesystem sandbox. Authorized rerun in
the existing isolated worktree succeeded. After wording corrections, the
checker rejected the stale generated view; regeneration restored agreement.
Neither event was recorded as a product failure or a successful earlier run.
A test-placement error was found by immediate code readback and corrected
before the final unit run; the changed-file manifest negative case was retained.

The final release procedure additionally checks the completed manifest and
the byte-identical public/private copies, then inspects the exact staged diff
and checks remote branch tips after pushing. A local commit, a push attempt,
and a verified remote commit are distinct states. Actual commit hashes and
push results are reported with delivery; this source document does not claim
a push occurred before it did.

## Publication boundary

Writers and separate reviewers examined publication substitutions. A targeted
scan of unit text found no actual local-user paths, source URLs, email
addresses, case source/exhibit identifiers or task UUIDs. Such a scan is
supporting evidence, not a universal secret detector; prose was reviewed as
well. Synthetic examples and technical field names remain because removing
them would weaken the requirements. The original log and evidence were not
edited. This packet contains no original media, case correspondence,
attachments, litigation strategy or private Sherlock implementation.

The two repository copies must have identical packet manifests and file
bytes. Their directory prefixes differ by the repositories' existing layout.
Only the public repository's navigation gains an additional entry. Unrelated
dirty work, other investigations, original feedback history and private
application changes are outside this publication commit.

Repository publication is not recipient acknowledgment of this expanded
record, implementation, product acceptance, activation or scientific validation.
The old 27-topic acknowledgment remains true at its own scope; it is not
retroactively promoted into a requirement-by-requirement receipt.
