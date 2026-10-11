# F6 Im3 reader assignment and exact format

Read this protocol and `../force56-remainder/READERS.md` completely. The latter
supplies the field definitions, not its old targets, filenames, reader identity
alias or source selection. This local protocol controls those substitutions.
Primary is agent `force6_im3_primary`, serialized reader `primary`; peer is
`force6_im3_peer`, serialized reader `peer`. Both act as source readers;
neither supplies actual human acceptance or independent historical corroboration.

Each reader saves only its own `reader-primary.py`, `reader-primary.json`,
`reader-primary-notes.md` (or peer). Use exclusive creation for generated JSON;
use apply_patch for literal code/notes. Report hashes before counterpart access.
No further edit to a frozen original or script; corrections need a preserved
new version and explanation. Keep code-generated expansions distinct from
manual selection; do not make code choose RGB, curves or selected row ranges.

JSON keys: region_id `F6-Im3`, pair `F6`, source `Im3.jpg`, reader, target_box
[145,0,440,88], context_box [143,0,442,88], inputs (file-parent-relative
SHA256/bytes maps), script_pin, coverage, routes {solid,dash}, unassigned_bands,
human_accepted false, physical_support null. Use the previous contract's
exact row/member/band and boundary-flag schema. Select no other pair's ink.

Use the standard coverage form: full_context_inspected true only when true,
raw_context_cells 26312, raw_blocks [{columns:[inclusive_first,inclusive_last],
receipt:string}], actual_views, prior_knowledge, uncompleted_context [].
Blocks must account for each context column 143 through 441 once; record any
recovery rereads separately. Actual rows span 0 through87. Do not invent
coverage receipts or use truncated output as a completed read.

Expected exact-white display command:
`P -B read_context.py show --first 143 --last 148`.
Choose finite block size to keep every display untruncated. Native white
omission is lossless, not a color filter. Complete whole-strip and page views
must also be actually performed and recorded. Work may remain incomplete if
the source or observation channel prevents a faithful annotation; name exactly
what is missing. Empty records require actual inspection, not inferred absence.

Pin both context files, their full declared input maps, this protocol/contract,
the previous field contract and literal script before saving. Preserve all
extra authority/context dependencies actually used; do not treat them as
additional scientific sources. Use no existing F5 annotation to choose F6
cells. The root will compare cross-pair conflicts only after both F6 freezes.
