# Independent typed contact and set-membership review

September 13, 2026. Research-only input inspection; not a solver run or a
finding of historical force transfer, restraint, damage or collapse cause.

## Scope and independence

The independent reader implements CONTACT-TRACE-PROTOCOL.md
(`f367dab9cf29f4958afed5a354a37bfcf1d5cb0f92e8fc39aab3009c2e529c80`)
against SRC-119–121 only. The frozen seed is `independent01.json`
(`d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7`):
873 nodes, 952 shell records, effective PID179. The reader reuses numeric
field parsing, resource gates and pin checking from the author's own frozen
`verify_restraint.py`
(`5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a`),
not root's new contact reader. Existing direct-graph results and prior metadata
counts/variant names were known; this is not blind discovery of those counts.
Root's new contact producer/results have not been inspected at this stage.

The typed joins distinguish node sets, segment sets and part sets even when
their numeric IDs coincide. Node and set IDs remain unchanged across the
previously checked include transform; outside-region part members receive
the recorded +1000 part offset. Segments retain all four ordered node slots,
including repeats, and four attributes separately. Intersections are checked
against the frozen seed, never coincident coordinates or contact distance.

## Primary schema read

The historical May 2007 LSTC Version 971 manual was hash-checked at
`f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
Complete physical pages 364, 366–367, 370–371, 402–403, 1161–1162 and
1171–1174 were visually read before this implementation. These establish
option-name order versus card order, the separate CID/heading card,
typed Card1 selectors, node-list and segment headers/membership, segment
attributes, the repeated N3/N4 triangle convention and contact applicability
limitations. CID heading text is hashed, not exported.

M971 Card1 SSTYP4 denotes a slave node set; the inspected MSTYP alternatives
are different. The reader therefore does not treat a master type4 as a node
set. Zero master ID for automatic single-surface contact is not a missing
master set. All following numeric cards and blank slots are retained, but
optional defaults, selection boxes, exclusions, contact initialization,
distance/projection and penalty values are not evaluated. Input membership
is not proof that a node was tied, transferred force or remained tied.

## First execution and retained failure

The first implementation froze at
`5edd81e375e0e4c437a36a05d55f15714703120d40bf50ce61f71570608c188c`.
All 18 actual synthetic checks passed, including header/member separation,
fixed/free heading parsing, namespace separation, repeated membership,
ordered/unordered distinctions, triangle slots, non-node attributes,
missing-reference reporting, unsupported-variant rejection and an actual
synthetic stream EOF/hash check.

Its first historical-source command terminated with exit1 at the 768 MiB
memory gate and did not create `independent-contacts01.json`. The reader kept
Python counters for every segment row, ordered list and unordered node set;
this is a resource-management defect in the verification implementation,
not evidence of a defective model. The final cap check also masked the inner
failure locator: only the terminal `memory_cap`, source0/line0 message was
returned. The exact peak, interrupted source/line and stream-progress objects
were not retained and must not be reconstructed as observed facts.

The exact first source is preserved as `verify_contacts-before-memory-fix.py`
with that same SHA. `independent-contact-failed01.json`
(`32cd17305341a70d4d30c206b8f8bcf0024bf1b31ff108605581e59f8b8b5901`)
is explicitly a reconstructed command receipt, not a recovered stream receipt.
Its unobserved fields remain null.

## Compact-memory correction

The corrected verifier froze at
`bcc87b26b50de22325a36a3da96343e1306230dd91e3efef240d6cece059b91b`
before the second source pass. Segment rows use compact numeric arrays rather
than Python tuple/frozenset counters for all rows. Duplicate-row comparisons
retain exact binary64 numeric equality with canonical signed zero, and a
separate canonical blank representation. Source nonfinite values are rejected;
node IDs above the exact binary64 integer range are rejected. Ordered node
lists, unordered node sets and full numeric segment rows remain different
statistics. Sorting for aggregate counts does not reorder the retained
seed-intersecting source records.

All 22 actual synthetic checks passed. Four added checks compare compact
counts with independent Python set/Counter answers, preserve blank versus
zero and signed-zero equality, handle an empty set, and reject an inexact
node-ID representation. The correction also keeps a caught source-position
failure in the output receipt rather than masking it with the final memory
gate.

## Successful independent extraction

The corrected pass completed with exit0 and froze `independent-contacts01.json`
at `b30b8ee5435e7cf8ce2ea979245b07fa4b0577606bf97638dbfd76b21043c7c3`
before root's new contact code/results were inspected. It took
18.977921291952953 seconds; peak RSS was 143,949,824 bytes. All 22 controls
passed. Before/after source, code and dependency pins agree. All three full
streams reached EOF with their expected uncompressed hashes:

| Source | Bytes | Physical lines | Typed records found |
| --- | ---: | ---: | --- |
| SRC-119 | 508,372 | 7,905 | None of the scoped set/contact kinds |
| SRC-120 | 232,959,541 | 4,088,491 | None of the scoped set/contact kinds |
| SRC-121 | 333,947,423 | 7,196,443 | 85 part sets, 2 node sets, 6 segment sets, 6 contacts |

The complete stream hashes establish byte coverage, not complete semantic
interpretation of every keyword. This pass parses only the admitted typed
sets/contacts and relies on the frozen direct-graph seed and transform. It
does not rederive the mesh, PART properties, coordinates or include graph.

The two node sets contain 152,977 and 243,047 unique node IDs respectively;
neither intersects the 873-node seed, and neither has repeated member IDs.
Part sets 1, 100 and 179 each explicitly contain PID179 once. All other
part sets have no seed-part intersection under the declared namespace.

| Segment set | All rows | Unique node IDs | Repeated full rows | Seed-intersecting rows | Unique seed nodes | Ordered seed-shell matches | Same unordered seed-node-set matches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 883,899 | 1,286,632 | 18 | 710 | 702 | 420 | 700 |
| 2 | 90,384 | 131,740 | 48 | 0 | 0 | 0 | 0 |
| 3 | 15,216 | 45,636 | 4 | 32 | 96 | 16 | 32 |
| 4 | 888 | 1,992 | 0 | 0 | 0 | 0 | 0 |
| 5 | 7,656 | 11,795 | 0 | 0 | 0 | 0 | 0 |
| 6 | 591,549 | 620,067 | 0 | 0 | 0 | 0 | 0 |

Repeated-row counts count extra occurrences beyond the first, not the number
of distinct repeated rows. Ordered and unordered comparisons are separately
retained; they are not interchangeable with a solver's segment orientation
or contact-pair rules. No segment in these six sets had N3=N4. This last count
does not by itself prove four distinct vertex IDs. All 742 intersecting
segment records retain source-line and membership-row locators, four ordered
nodes, four attributes, exact seed intersections and both kinds of shell
matches. No nonintersecting full node array is exported.

The six CIDs are 1, 2, 3, 4, 5 and 9. All have six retained numeric cards,
including blank fields. The 12 selector records resolve as follows:

| CID | Keyword family | Slave declaration | Master declaration | Declared seed inclusion |
| --- | --- | --- | --- | --- |
| 1 | TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET | Node set1 | Segment set1 | Master set only |
| 2 | TIED_SURFACE_TO_SURFACE_ID_OFFSET | Segment set2 | Segment set3 | Master set only |
| 3 | AUTOMATIC_SINGLE_SURFACE_ID | Part set1 | Not applicable, MSID0 | Part selector includes PID179 |
| 4 | TIED_SURFACE_TO_SURFACE_ID_OFFSET | Segment set4 | Segment set5 | Neither set |
| 5 | TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET | Node set2 | Segment set6 | Neither set |
| 9 | AUTOMATIC_SINGLE_SURFACE_ID | Part set2 | Not applicable, MSID0 | No seed-part intersection |

There are ten resolved typed references and two non-applicable single-surface
master entries, with zero missing typed references. A seed's presence on a
master segment does not establish which external slave nodes were tied to it.
Absence of seed nodes from a slave node set likewise does not establish absent
restraint: the seed may participate through the master surface. Neither
observation determines connection capacity or historical force transfer.

## Post-freeze comparison

After the independent extraction froze, root authorized inspection of its
separately frozen `trace_contacts.py`
(`ba35168bab6391ddd1126433d00047ec18d3f24dde9b4fb4f9250b29241688d8`),
`contacts-root01.json`
(`04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859`)
and `contacts-root02.json`
(`27d22a353b601d1bf2797ea80f846bebe4d42e8467f663778413897437770ed5`).
Root reports that its implementation and first pass were complete before
receiving the independent contact summary counts; prior metadata counts and
the shared protocol/source schemas were already known to both implementations.
The later comparison is explicitly post-schema work, not another blind
source extraction.

The complete root contact reader and relevant root input-stream hash/line
method were read. Root's nine actual synthetic checks were then rerun with
`--controls` and passed; the independent reader's 22 checks were separately
rerun with `--selftest` and passed. Neither command reconstructs the historical
source data. The comparer does not import either producer's contact join
functions.

`compare_contacts.py` froze at
`e3298754cdcda2098ed376b4149384598d941f68e2c6245a84424b2a9c2c21f1`.
Its first AST check and execution passed. The create-only
`contact-comparison01.json` receipt is
`15e6c98727074d577ac1839b93a6525b4d0ae403996403da4ea73dd131b1e2e9`.
Both root records agree with the independently extracted common fields:

- 93 typed sets: 85 part, 2 node and 6 segment; all 88 zero-intersection sets
  remain in the comparison.
- All 742 selected segments, including source line, four ordered/repeated
  node slots, four numeric/null attributes, exact seed intersections and
  ordered/unordered seed-face EID aliases.
- Three selected nonsegment source rows, with within-row membership order
  and duplicates preserved by the adapter.
- Six contacts, all ID/keyword/heading hashes/locators, 36 numeric cards,
  288 card slots and 12 typed selection records.
- All three source EOF receipts per root output, including compressed and
  uncompressed hashes, sizes and physical line totals.

Each root comparison checks 12,491 numeric, 730 null, 123 string and 6 boolean
scalars, with zero mismatches. Numeric comparison has no tolerance: exact
rational values must agree; float/float slots also require identical binary64
representations, including signed zero. Integral JSON float versus integer
representation is allowed only when exactly equal; a boolean is never an ID.
The two full root result/receipt objects are equal after removing only
`elapsed_seconds`. These repeated outputs are not additional independent
source paths.

All 27 negative controls exercise the actual schema adapter and recursive
comparison. They detect dropped zero-intersection sets and selected segments,
changed namespaces/source lines/headers/count meanings, reordered or repeated
vertices, numeric-versus-null attributes, changed seed intersections/face
aliases, wrong PID179/1179 membership, contact IDs/keywords/heading hashes,
card order/null fields, boolean IDs and wrong selector types/IDs/row counts or
single-surface master status. Unknown serialized fields also fail rather
than silently escaping comparison. No browser checks apply to this local
numeric CLI task.

### Explicit schema mappings and exclusions

Root `unique_members` for segments counts unique ordered four-node tuples;
its segment `member_entries` counts rows, and its
`duplicate_member_entries`/`duplicate_ordered_segment_rows` count extra ordered
rows. These correspond to independent ordered-node-list statistics, not
independent node occurrences, full eight-field rows or unordered node sets.
For node/part sets, root's member counts instead mean ID occurrences and
unique IDs. Root part-set `unique_nodes=0` is that schema's unpopulated node
counter, not a statement about incident physical geometry.

Both heading hashes used in the comparison cover the entire CID+heading card
excluding CR/LF. The independent stripped-heading-only hash is deliberately
not compared to it. Source basenames become only the three defined numeric
source aliases, and the root keyword's leading asterisk is removed. No
semantic keyword alias is invented.

Independent face matches preserve source/line/EID records; root supplies
only EID aliases. Before reducing to root's representation, the comparer
checks each independent alias against its frozen seed's exact source line
and ordered/unordered node match. Root has no separate fields against which
to compare the independent membership-row ordinals, nonsegment slot numbers
or original/effective member pair. Nonsegment occurrences are grouped by
physical line for root's representation, retaining order and repetition.

The independent whole-set full-attribute/unordered duplicate totals and
distinct repeated-node counts are not separate root outputs. They therefore
remain independently calculated statistics, not cross-implementation
verified fields. Matching numerical values in the current data do not erase
those semantic differences. The comparer performs fresh compressed-file
hash checks before/after, but no new decompressed geometry scan. All frozen
source-extraction artifacts and the failed first attempt remain unchanged.

## Parent consumer replay and direct-graph presentation check

Parent's consumer replay completed with exit0/PASS and produced
`contact-comparison-root01.json`, SHA
`eb8d0391fb08c59a2125afc46c7d81a1b5a2e9f8a15f4fefee99ef81172a20a0`.
The independent reviewer loaded and recursively compared this actual receipt
against `contact-comparison01.json`. The only differences are `command[1]`
(script path), `command[3]` (output name) and `elapsed_seconds`. Every other
field agrees, including the full source/code pins, both sets of scalar counts,
coverage, all 27 negative controls and the rerun 22/9 producer-control results.
The unittest stderr timing hash could legitimately vary, but did not vary in
this replay; it was not silently excluded from the observed equality check.

A separate read-only derivation from the frozen direct-graph
`independent01.json` (SHA above) deduplicated the matched seed-node IDs across
all 20 neighbor records, then grouped their saved coordinates by exact stored
Z value, without rounding or a tolerance. It confirms 18 distinct shared seed
nodes: 9 at Z=-71.1708 and 9 at Z=-43.6118. These values also equal the saved
seed's minimum and maximum Z. This is a presentation check on the frozen
input-coordinate derivative, not another source extraction or a demonstrated
physical floor/column-end identification. No units, floors or north/south
restraint were inferred from these two coordinate values.

## Scientific disposition

The common-field independent comparison and parent consumer replay are
complete and passed. This is reproducibility of declared source inputs and
joins, not evidence that a contact pair initialized, transferred force,
remained tied after damage or matched a historical run. No directional/floor
mapping, physical capacity, collapse-mechanism probability, wrongdoing or
innocence conclusion follows from this arithmetic/source agreement.

## Report numeric-presentation review

The complete report was read at SHA
`eb39441d52112490feeed9acfd0973e56d7d28186c8b6fa2081adbc7be39a606`,
including the candidate-list section and source footnotes. The numeric/input
presentation passes with no material correction. This disposition does not
certify the separately reviewed NIST support-state prose/diagram, publication
timings, historical interpretation or manual-method interpretation.

The reported diagnostic source lines614–617 and part-set lines611–613 match
the frozen independent line locators. The 952 seed shells, 873 seed nodes,
20 neighbors, 18 shared seed nodes, 891 retained coordinate records, zero
other-family direct neighbors, exact bounds and section/material pairs match
the frozen graph. A separate check of the saved coordinate triples finds
891 distinct tuples as well as 891 unique node IDs, so the table's coordinate
count is not merely assumed from its node count. This establishes uniqueness
of stored input values, not independently measured physical locations or an
architecturally authenticated column extent. The two Z groups each contain
nine shared seed nodes and equal the saved seed's extrema.

The six contact mappings, 93/88 set counts, 742 selected segment records,
36 numeric cards, 12 selectors and all displayed set1/set3 denominators and
ordered/unordered match counts agree. The 18/48/4 extra ordered-row counts
are presented as that statistic, not as full-attribute duplicates or forces.
Neither master membership nor exact-node incidence is promoted to a realized
pair or a quantified restraint.

The candidate section correctly keeps 1,543 shells, six explicit beams and
355 cross-family numeric candidates distinct; the latter two partition one
361-ID beam list. CaseA's 45,152 unique shell IDs and all reported zero
intersections agree with the completed candidate join and parent replay.
The report expressly conditions CaseA shared-node incidence on the frozen
complete graph and notes zero actual positive coordinate comparisons. It
does not equate these zeros with absence of indirect damage or contact effects.

The claim grades remain explicitly attached to reported source statements
and bounded input derivations. The report leaves physical sufficiency,
historical restraint, collapse mechanism and intent unresolved rather than
upgrading a comparison PASS into causal confidence. Source/manual validation
still belongs to the separate review arms.

The existing complete validation text was read at SHA
`f9018c7338ccd43a944ef5f0e0fa7811ec5e9b15a43bcfd30eb30bb82c24f1ea`,
before its candidate-section addition. Its three geometry byte/line totals
match the retained EOF receipts: 508,372/7,905; 232,959,541/4,088,491;
333,947,423/7,196,443. No source-line-count error was found. The direct
comparer's 61,574 numeric scalars and 28,686 coordinate components are
correctly described as totals across both root comparisons; the contact
comparer's 12,491 numeric scalars are correctly per root. The 20 artifact
hashes then in the validation table all match their files.

### Completed final numeric disposition

The updated report SHA is
`6b57c44b9e6b194b019a8a362cb5242ab1f3b69ec679907389382e5593d59fda`.
The reviewer reversed the single replacement of "these selected pairs" with
"candidate pairings under these definitions" in memory and recovered the
exact previously reviewed report hash `eb39441d...`. Thus this final delta
contains no numeric change; it also avoids implying demonstrated contact
pairs. No source or report file was modified by this check.

The complete updated validation was read at SHA
`e5e59c051b1b98ce9216a1db381e1cd09949f137447cb6dacc1ddbecab278f49`.
The candidate section agrees with the frozen results: 1,543/6/355 separate
set2 pools, one 361-ID beam list, 45,152 unique CaseA shell IDs, explicit zeros,
zero real positive coordinate matches, 17 synthetic controls and the stated
consumer metadata differences. In particular, 45,156 is the CaseA physical
source-line total, not its 45,152 membership count. Its 103,872 compressed
and 325,983 uncompressed byte totals and both source hashes are correct.
All 25 artifact hashes now displayed in the validation tables match their
files. The source-reuse versus fresh-list-scan distinction and the conditional
complete-graph/shared-node inference are preserved.

Final bounded disposition: **PASS; no material numeric-presentation correction
required** for these report/validation versions. This ends the requested
numeric review, not the separate source/manual review, physical validation,
historical reconstruction or broader investigation. Subsequent root-only
nonnumeric closeout/navigation additions are not silently included in this
hash-pinned review. No code, frozen extraction, receipt or raw source changed.
