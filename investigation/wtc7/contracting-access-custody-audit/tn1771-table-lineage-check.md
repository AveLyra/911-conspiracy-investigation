# TN1771 / later-paper printed-table lineage check

2026-09-28. Separately authored AI source review; working research only, not
licensed engineering review or a formal case finding. No source authority is
changed. Main repository controls and CHARTER WP3 govern. The authorized scope
is [the TN1771 follow-through](tn1771-provenance-followup-2026-09-28.md).

## Frozen result and limits

TN1771 Table 2, complete physical/printed page 27, explicitly identifies
**Test 1**. All **48** time/member/location triples match the previously
checked later-paper Table 5 transcription exactly: **144 of 144 fields,
zero mismatches**, including the missing entries. The comparison retains
9 missing measured temperatures and 11 missing percentages; 37 percentages
are populated. This is identity of printed numeric values and missingness,
not a claim of identical PDF typography, byte-identical native runs,
unchanged inputs, or independent experimental replication.

TN1771 Table 3, complete physical/printed page 31, explicitly identifies
**Test 2** and is a distinct table. For a direct distinguishing example,
Mid Web / A / 30 minutes reads `(337, 284, -8.6)` in Table 3, compared with
`(331, 285, -7.7)` in Table 2. No full Table 3 transcription or arithmetic
audit was performed in this task. The `5.2 Test 2` heading below Table 2 on
page 27 begins the subsequent discussion; it does not relabel Table 2.

These two pages do not resolve the precise duration of furnace exposure,
the earlier 116/120-minute question, channel histories, output-file identity,
or whether a particular number came from a rerun. The 30/60/90/120-minute
table labels are printed comparison times, not independently verified
exposure histories. The page-27 prose's reported times to a steel-temperature
end-point are not automatically termination times. No WTC7 validation or
historical cause conclusion follows from this lineage check.

## Independence, coverage, and source pins

The reviewer had already visually transcribed and checked the later-paper
Table 5, including its arithmetic, and had compared that transcription
against the saved JSON. That prior exposure is disclosed: this review is
not blinded, not a fresh experimental replication, and not independent
event-level evidence. The reviewer read only the TN1771 prospective scope
and acquisition section, not root's or another reader's TN1771 synthesis,
before freezing the source observations and comparison result in chat.
Root did not supply an expected comparison result.

For this task, only the complete native-page render images for TN1771 pages
27 and 31 were viewed. Both printed page numbers were visible. Image views
requested `detail: original`; a tool can still resize the display, so this
does not claim source-pixel metrology. The tables were legible in the full
page views. No PDF text extraction, additional source page, graph tracing,
solver, new acquisition, or reconstruction of missing entries was used.

SHA-256 pins freshly checked in this task:

| Artifact | SHA-256 |
|---|---|
| [TN1771 preserved PDF](nist-tn1771-source01.pdf) | `c94d92defa00689c906f54a7075e4887a1bdd86731688b34d98200ec29fc94e3` |
| `tn1771-render01/tn1771-page-027.png` | `df7c71dd03eae812dd77ff4f0414cd9f4829a5774a94768e9fa8ea2296b4f0e8` |
| `tn1771-render01/tn1771-page-031.png` | `f027a1770f3d1f45563c5d349b654127d40ce52142f268c9218ba004418350cf` |
| [Earlier checked Table 5 derivative](thermal-response-table-check01.json) | `a9c774a54426609fa1fcbd6f8321e2de88d9e235ca737db8e35b0eb8d56438fc` |

The comparison derivative identifies its source as the later-paper PDF
`thermal-response-927871-source01.pdf`, with SHA-256
`953b493d550eda3f8a00f67e4c05817e6112f4baedeb48e542f84a313de5b432`.
That source page 20/Table 5 was inspected in the preceding task, not viewed
again here. A hash checks captured-byte integrity, not historical authenticity.
This reviewer did not rerender the TN1771 pages or independently reproduce
the existing rendering process in this task.

## Full page-27 transcription

Every cell below is `(measured_C, predicted_C, printed_percent)`, with `null`
meaning the source's printed dash. Locations are in printed order A, C, I,
E. The JSON normalization maps Mid Web to `midweb`, Bot Chord to `bottom`,
and Top Chord to `top`. `3.0` and JSON `3` represent the same printed numeric
value; no claim of lexical JSON/PDF identity is made.

| Member | Minutes | A | C | I | E |
|---|---:|---|---|---|---|
| Mid Web | 30 | (331,285,-7.7) | (299,289,-1.7) | (320,285,-5.8) | (332,280,-8.6) |
| Mid Web | 60 | (647,626,-2.2) | (656,633,-2.4) | (618,625,0.7) | (621,617,-0.4) |
| Mid Web | 90 | (792,820,3.5) | (846,826,-1.8) | (770,817,4.5) | (775,811,3.4) |
| Mid Web | 120 | (null,929,null) | (null,934,null) | (899,927,2.4) | (933,923,-0.9) |
| Bot Chord | 30 | (245,237,-1.7) | (180,200,4.5) | (172,198,5.8) | (195,229,7.4) |
| Bot Chord | 60 | (565,578,1.5) | (477,502,3.4) | (417,498,11.7) | (461,561,13.6) |
| Bot Chord | 90 | (752,782,2.9) | (747,709,-3.7) | (628,704,8.5) | (735,765,3.0) |
| Bot Chord | 120 | (929,903,-2.1) | (null,841,null) | (781,838,5.3) | (768,889,11.6) |
| Top Chord | 30 | (92,97,1.3) | (100,101,0.5) | (86,102,4.3) | (132,100,-7.9) |
| Top Chord | 60 | (209,196,-2.7) | (null,203,null) | (169,203,7.5) | (null,151,null) |
| Top Chord | 90 | (382,278,null) | (null,284,null) | (254,284,5.8) | (null,282,null) |
| Top Chord | 120 | (574,348,null) | (null,353,null) | (336,353,2.8) | (null,351,null) |

The existing JSON also contains separately calculated percentages, including
derived extras for Top/A/90 and Top/A/120. Those fields were not compared as
source entries here. The source `printed_percent` remains `null` for both.
This task did not repeat the prior model-percentage arithmetic check.

## Actual checks and outcomes

The following were executed, not merely proposed. All named artifact paths
below are relative to the audit directory containing this note; tool calls
used their full absolute paths.

1. `view_image` opened both `tn1771-render01/tn1771-page-027.png` and
   `tn1771-render01/tn1771-page-031.png` with `detail: original`; both returned
   complete page images, inspected as described above.
2. A manually entered 3-member x 4-time x 4-location array was frozen in the
   tool session after page-image inspection and before reopening the
   comparison JSON. Its 48 triples are reproduced in the table above.
3. `sed -n '1,620p' thermal-response-table-check01.json` returned the complete
   JSON, terminal exit 0. JavaScript `JSON.parse` then parsed that output.
   The comparison selected exactly one JSON row by `(member, time_minutes,
   location)` for each transcribed triple; each of `measured_C`,
   `predicted_C`, and `printed_percent` was compared using strict equality
   (`===`), including `null`. It counted unique keys, source missingness,
   and every mismatch. No tolerance was applied or needed.
4. Actual comparison output:

   ```json
   {"triples_compared":48,"fields_compared":144,"field_matches":144,"source_missing_measured":9,"source_missing_percent":11,"source_populated_percent":37,"comparison_table_row_count":48,"unique_keys":48,"mismatches":[]}
   ```

5. `shasum -a 256` was run together on the preserved TN1771 PDF, both inspected
   PNGs, and `thermal-response-table-check01.json`; terminal exit 0. The
   returned four hashes are recorded above. The PDF hash matches the
   prospectively declared source pin.
6. `git status --short -- research/sherlock-wtc7-investigation/contracting-access-custody-audit/tn1771-table-lineage-check.md`
   in the investigation worktree returned no entry; `test ! -e` on the
   note's absolute path returned exit 0. This note was created with
   `apply_patch`; no existing source or derivative was overwritten.

## Claim ceiling and possible disconfirmation

The directly checked proposition is limited to printed-value identity for
these 48 triples and the explicit Test 1/Test 2 labels. A correctly pinned
page showing a different entry, a transcription mismatch, or a changed
comparison derivative would require revising that result. None appeared in
the declared check. The complete transcription and comparison counts make
that proposition auditable rather than relying on a representative snippet.

The strongest limit on a broader interpretation is that rounded tabular
values can agree even when underlying precision, runs, or inputs differ.
Ordinary reuse of the same reported comparison is consistent with the
observed identity; it is not a second experiment, and the table alone does
not reconstruct the actual document-to-document copying or run lineage.
Those questions require native run/input/output identifiers and their
provenance. No attribution of misconduct or new historical-cause ranking
is established. Preserved PDFs, images, prior JSON, and other notes remain
unchanged by this reviewer.
