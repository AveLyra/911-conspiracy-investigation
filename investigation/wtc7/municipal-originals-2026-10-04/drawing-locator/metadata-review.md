# Independent saved-metadata review

October 4, 2026. Findings frozen before reading root findings. Last input-pin
check: 20:22:05 UTC. This is a read-only review of four saved search pairs and
the two declared held locator files, not a new search or content reading.

## Result

The saved responses contain **29 query-result occurrences but 16 unique
document IDs**. The three drawing-phrase requests alone contain 28 occurrences
and those same 16 IDs; the control adds another occurrence of 167873, not a
new ID. No within-response ID duplicates or conflicting requested properties
for repeated IDs were found. The literal catalog lookup finds only the named
167873 folder, while the backend returns additional records whose displayed
folder labels generally do not contain the drawing tokens. These are locator
candidates, not verified copies of the named sheets.

The strongest next content candidate by metadata is 167874, labeled
`Drawings`, three indexed pages, returned by SKP-4. The one-page 173670,
`Architectural Sketch Log`, is a narrower complementary locator candidate
returned by S-TS-7. Neither is established to contain the sought sheets here.
The eight-page 166828 result has an oil-pipe-route label; its S-TS-7 query hit
does not establish relevance, drawing identity or a causal connection.
Any acquisition/reading requires separate authorization and admission.

## Scope, controls and method

Read the entire protocol. Main AGENTS/WORKFLOW/CHARTER hashes match the
previously read controls. Applied source-of-truth and evidence-audit controls;
the data-quality skill was used only as a scoped companion for schema, grain,
IDs, counts and pagination. No separate analytics product, notebook or broader
source discovery was introduced. Root clarified that the protocol's “prior
unit's folders.json” means the exact catalog path below; no alternative
catalog was searched. Root findings and new PDF contents were not read.

Only this new review note was written. Existing metadata, protocol, main/legal
records and earlier readings remain unchanged. No network, source acquisition,
binary reads, rendering, OCR, image views, Git or engine actions occurred.

Command path abbreviations:

```sh
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/drawing-locator
F=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/folder-document-locator/folders.json
L=/Users/admin/docs/911/research/WTC7_archive_leads_2026-09-16.md
```

Actual terminal checks used `jq-1.8.2`, `rg`, `sed`, `shasum -a 256` and
`wc -c -l`. All local check commands completed with exit 0. Selected raw
metadata fields were parsed, not PDF bodies. The source hashes below were
checked initially and again after analysis without changes.

## Requests, schema and termination

Exact query texts:

```text
ALL extension:pdf source:"WTC 7" "SKP-3"
ALL extension:pdf source:"WTC 7" "SKP-4"
ALL extension:pdf source:"WTC 7" "S-TS-7"
ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE"
```

Every request sets `count: 50`, `content_sample_length: 0`, with identical
eleven-property lists and `formats: ["VALUE"]`: `mes:key`, `title`, `source`,
`agency`, `box_name`, `folder_name`, `page_count`, `pdf_size`,
`production_volume`, `production_end`, `mes:date`. The corresponding
`search_request`, after removing the service-added empty `user_context`,
equals the full saved request. The `user_query` alternative also echoes the
requested query; its `count: 1` is not the document-result count.

Each response is an object with eleven top-level keys. `resultset` contains
`results`, `prev_avail`, `next_avail`, `order_direction`, and
`per_service_dataset`. Each result has exactly the eleven requested property
IDs, one data value per property. Nine values are strings, including
`page_count`; `pdf_size` is numeric; `mes:date` is numeric with
`unit: ms_since_1970`. No content samples/snippets were returned; the only
content-related key found was the echoed `content_sample_length`.

| Query file stem | Estimated count | Actual rows / unique IDs | Sum of page metadata | Previous / next | Service termination |
|---|---:|---:|---:|---|---|
| skp3 | 13 | 13 / 13 | 35 | false / false | NO_MORE_RESULTS |
| skp4 | 12 | 12 / 12 | 34 | false / false | NO_MORE_RESULTS |
| sts7 | 3 | 3 / 3 | 10 | false / false | NO_MORE_RESULTS |
| control | 1 | 1 / 1 | 1 | false / false | NO_MORE_RESULTS |

Every response has one service dataset, identified as
`https://nyc.mindbreeze.com/search/september-11/`, and a paging-state object
with `id`, `digest`, `state_base64`. The presence of that state alone does
not mean a further page exists. Counts are below 50 and agree with rows;
no error/timeout/truncation-named keys were found. These observations support
termination of these saved query listings, not archive-wide completeness.
The reviewer did not independently execute HTTP requests or verify their
transport status/exit codes; JSON service termination is a different fact.

All 29 occurrences are `source: WTC 7`, `box_name: 7DCAS`,
`agency: Citywide Administrative Services, Dept. of`, and
`production_volume: NYC-WTC0007`. Result IDs are consistently
`september11 Connector:September11_MD:<mes:key>:` and titles equal the key
plus `.pdf`. Every page count and byte count is positive; the inclusive
production-end minus key span agrees with the indexed page count. These
are metadata consistency checks, not actual PDF page-count measurements.

## Unique-ID inventory and held-folder comparison

Each ID below has prefix `NYC-WTC_000`; the end column uses the same prefix.
Query membership is exact, not a relevance score. Folder rows are one-based
positions in `F.rows`. Every result's exact `(source, box, folder)` matches
one and only one held catalog row; original spelling, case and `®` marks
were preserved during matching.

| ID suffix | Queries | Indexed pages | Indexed bytes | End suffix | Catalog row | Original folder label |
|---|---|---:|---:|---|---:|---|
| 166828 | sts7 | 8 | 533928 | 166835 | 3653 | Mayor's Office of Emergency Management Alt. Route for Oil Pipes |
| 167170 | skp3 | 2 | 104270 | 167171 | 4142 | Various Change Orders Mayor's Office of Emergency Management 7 World Trade Center New York, New York |
| 167873 | skp3, skp4, sts7, control | 1 | 40327 | 167873 | 4075 | SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE |
| 167874 | skp4 | 3 | 258425 | 167876 | 3136 | Drawings |
| 168580 | skp3, skp4 | 1 | 41911 | 168580 | 2649 | 7 World Trade Center Mayor's Office of Emergency Management - 1st, 7th, & 23rd Floors Chang Order #38 |
| 168581 | skp3, skp4 | 1 | 48367 | 168581 | 2870 | 7th Floor Louvers 7 World Trade Center Change Order #038 Amb. Job #S57-5175 |
| 171286 | skp3, skp4 | 5 | 489175 | 171290 | 2964 | Breakdown of approved Change Orders |
| 171620 | skp3, skp4 | 3 | 326462 | 171622 | 3694 | Mayor's Office of Emergency Management®7 World Trade Center®Breakdown of approved Change Orders |
| 171802 | skp3 | 2 | 113155 | 171803 | 4142 | Various Change Orders Mayor's Office of Emergency Management 7 World Trade Center New York, New York |
| 171840 | skp3, skp4 | 6 | 374954 | 171845 | 2759 | 7 World Trade Center Mayor's Office of Emergency Management 1st, 7th, & 23rd Floors Chang Order #38 |
| 172947 | skp3, skp4 | 3 | 355767 | 172949 | 3329 | MOEM 7 WTC Breakdown of approved Change Orders |
| 172953 | skp3, skp4 | 5 | 345271 | 172957 | 3807 | None |
| 173670 | sts7 | 1 | 67561 | 173670 | 2941 | Architectural Sketch Log |
| 173920 | skp3, skp4 | 2 | 244250 | 173921 | 3053 | Change Order Request Clarification |
| 173949 | skp3, skp4 | 2 | 232649 | 173950 | 2963 | Breakdown of Approved Change Orders |
| 174004 | skp3, skp4 | 2 | 232037 | 174005 | 2963 | Breakdown of Approved Change Orders |

The unique-ID metadata totals are 47 pages and 3,808,509 bytes. They are not
downloaded holdings or 47 unique historical pages. Cross-query duplication
accounts for 13 occurrences beyond the sixteen IDs; repeated IDs' eleven
properties are identical after property-order normalization. Different IDs
are not assumed to represent substantively independent evidence.

Catalog grain is a source/box/folder group, not one document per row.
`F` has ten top-level fields; its `columns` define six positional row fields:
`source_index`, `box`, `folder`, `documents`, `pages`, `first_bates`.
All 4,205 rows have those six types: number, string, string, number, number,
string. Source indexes are 0/1/2 and map through `sources`; index 2 is WTC 7.
All 4,205 `(source_index, box, folder)` triples and all 4,205 first-Bates
values are unique. Document counts sum to the declared 24,437, and pages
sum to 172,544. `labels_withheld` is 0. These describe this saved catalog,
not a fresh inventory of the archive.

The declared case-insensitive patterns `SKP[ -]*[34]` and `S[ -]*TS[ -]*7`
match one catalog row, row 4075, source WTC 7 / 7DCAS, one document / one
page / first Bates 167873. No off-source literal hits occurred. Main held
archive-leads Markdown matches only line 84, with the same original label,
ID and one-document/one-page total. It is a prior locator summary, not a
second original record. The control response matches that exact catalog
folder and known ID; it confirms this route can return the known cover,
not that all three named sheets were indexed or retrieved.

Important group-versus-document distinctions:

- Catalog row 4142 has five documents / thirteen pages, first 167170;
  only two two-page IDs from that group occur in these phrase responses.
- Row 3807's literal folder label is the string `None`, not JSON null. Its
  group has 462 documents / 700 pages, first 166926; result 172953 is one
  five-page document, not the entire group.
- Row 2941 has ten documents / eighteen pages, first 166752; 173670 is one
  one-page result. Do not attribute the group totals to that document.
- Case-distinct rows 2963 (`Approved`, two documents / four pages) and
  2964 (`approved`, one document / five pages) were not merged. Results
  173949 and 174004 jointly match row 2963's totals; 171286 matches 2964.
- Row 3136, `Drawings`, has one document / three pages, first 167874,
  matching that result. The other matched single-document groups also
  agree on first Bates and page count; the explicit source table remains the
  reference for IDs rather than an inferred attachment sequence.

## Actual check receipts and reproducible core

Local receipts: protocol read `dc3240`; control pins `b3bf89`; request/full
top-level schemas and initial pins `aa74ff`; query envelopes and resultset
schema `55e68c`; selected properties and catalog schema `d0b104`; per-pair
checks `e23a70`; duplicate/catalog/search checks `30736a`; exact-folder joins
and request/content-field checks `6b039c`; final pins/version `ea87c6`.
All ended exit 0. Two initial skill-text outputs were truncated; missing
instruction sections were read separately before data checks. No data read
or test failed, and no external action was retried.

The executed core checks, with the path abbreviations above, included:

```sh
shasum -a 256 "$U/PROTOCOL.md" "$U"/*-request.json "$U"/*-response.json "$F" "$L"
wc -c "$U"/*-request.json "$U"/*-response.json
wc -c -l "$F" "$L"
rg -n -i -o 'SKP[ -]*[34]|S[ -]*TS[ -]*7' "$L"
sed -n '84p' "$L"
```

For each stem `skp3 skp4 sts7 control`, `jq --slurpfile q
"$U/$stem-request.json"` evaluated the following tests against the matching
response (alongside schemas and counters reported above):

```jq
(.search_request | del(.user_context)) == $q[0]
all(.resultset.results[];
  ([.properties[].id] | sort) == ([$q[0].properties[].name] | sort))
all(.resultset.results[].properties[]; (.data | length) == 1)
```

Cross-query checks used `jq -s` on the four responses in skp3/skp4/sts7/control
order, flattened `properties` by property ID, grouped by result ID, and
compared the flattened property maps within each group. The held-folder
join used `jq -s --slurpfile catalog "$F"` on those same four responses;
each unique result was compared by exact source, box and folder to the
catalog row map. The catalog literal scan selected strings in each row
with `test("SKP[ -]*[34]|S[ -]*TS[ -]*7"; "i")`, retaining row position and
the six original fields only for matching rows. No additional spellings,
files, sources or inferred IDs were searched.

## Input pins

All SHA-256 values below matched the initial and final checks. The eight
request/response files total 67,115 bytes; the exact catalog is 421,135 bytes,
and the main archive-leads file is 17,737 bytes.

| Input | Bytes | SHA-256 |
|---|---:|---|
| PROTOCOL.md | not separately measured | `9369d79f07726b7b46570d734a828158d6d8fe95c0596414c3dd41285f6534cc` |
| control-request.json | 1158 | `05a0df86737b4efeaf9949051c23385e22ed46c16a4ddbca567511e1a45277ef` |
| skp3-request.json | 1087 | `19851b28aad3df3a38bda0f2cbc82f1a743df30a83e9197acf671270c2c23770` |
| skp4-request.json | 1087 | `38b43c87f49cadc3f812f6f9999cc0b4959163af9b1350372528a2b6ee4b2bf0` |
| sts7-request.json | 1088 | `284a857f54451344c2356410cadf2c68e6101fd9f38a72420a0d61d781b11d6a` |
| control-response.json | 8451 | `fdf92a229791be47e9ca997939bc9df8f9543fa4eb7764c3bb3c1770a52ae57b` |
| skp3-response.json | 22502 | `a13e7e290cd0e625db4502ec4197389c1c549b138b48502c2daebc00c62a3a26` |
| skp4-response.json | 21189 | `e4848f93061aaf339bdfb006fce212f95805298ba24fe60e8e1d2fbcb6be9a0b` |
| sts7-response.json | 10553 | `639d3c9f00b00acbdf613525c3ffa27b6f2e3190a1b566269a003d59424b41c7` |
| F (held folders.json) | 421135 | `cf3afa33cc58a0f2a9d48e6fbac57cdd8bb060b046cf5373d261d37bb976b704` |
| L (main archive leads) | 17737 | `01f7419ec36c6686ac154c6f6e05e3309d90704069957119cfc9efb8160bc3ea` |

## Limitations and adverse interpretations

No parser/schema/pin/count inconsistency was observed in this finite sample.
The material interpretive risks are nevertheless substantial: counting 29
hits as 29 records; mistaking folder totals for document page counts;
equating an exact query echo with proven literal/full-text/OCR semantics;
or mistaking a known-cover positive control for proof of attachment retrieval.
Only 167873's displayed folder label contains the sought tokens. The other
returned labels do not establish where or how the backend matched them;
hidden indexed content or search tokenization could explain these hits.
This review did not discriminate those possibilities.

Service ranking/relevance numbers are not confidence estimates. `mes:date`
and catalog capture/generated fields are service/snapshot metadata, not
historical document dates. No date conversion was used to date an event.
The folder catalog is a September 11 snapshot; agreement with these saved
responses does not establish present archive completeness. No missing-sheet,
concealment, installed-state, causation or historical-authenticity conclusion
follows. The next falsifying check is an independently admitted content read
of the specifically identified candidate, which could show different sheets
or only references rather than the requested drawings.
