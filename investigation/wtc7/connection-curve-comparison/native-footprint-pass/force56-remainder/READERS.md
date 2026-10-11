# Frozen reader contract

Before raw reading, `force56_primary` is primary and `force56_peer` is peer
for both F5-Im3 and F6-Im1. Both are AI readings of the same source, not human
acceptance or independent historical corroboration. Read PROTOCOL.md and the
parent protocol completely. Do not read the counterpart until both freeze.

Per region/role save `reader-F5-primary.py`, `.json`, `-notes.md` (substitute
F6 and peer). A literal source script exposes `build()` returning its original
JSON. It must select no cells by image/code classification. Use apply_patch
for literal source edits and exclusive creation for generated JSON. Freeze
and report hashes before requesting comparison; subsequent corrections must
be additive, not silent replacement.

Use the established approach34 original schema: region_id F5-Im3 or F6-Im1,
pair, source (Im3.jpg or Im1.jpg), reader, target_box, context_box, inputs
(paths relative to this directory, each SHA256/bytes), script_pin, coverage,
routes {solid,dash}, unassigned_bands, human_accepted false, physical_support null.
Inputs must include PROTOCOL.md, READERS.md, both context JSON files, the
corresponding source and all explicitly used helper dependencies. Include the
context's own input map as transitive dependencies, retaining normalized paths.
Check pins before and after producing the original.

Every route has one row per target x, including inspected empty columns:
x, core, fringe, fragment_id, fragment_membership (list of objects with
fragment_id/core/fringe), status, reason, boundary_flags, unassigned_band_refs.
Class sets are sorted unique integers, disjoint and bounded inside target.
Membership pieces are disjoint and their class unions exactly equal the row.
Outer fragment_id is the sole membership ID, otherwise null. An empty row has
no members. Distinguishable dash bodies have distinct local IDs; discontinuous
segments do not acquire continuity merely by sharing a color or route name.

Boundary flags order: target_left,target_right,target_top,target_bottom, only
when selected cells touch that edge. Status vocabulary:
identified_local_fragment, fringe_only, no_attributable_cells, identity_conflict,
boundary_truncated. Empty with conflict refs is identity_conflict, not absence.
Every row has an actual reason. Unassigned bands have the same cell/member
fields plus band_id and candidate_routes (solid/dash/both). Multiple disjoint
bands in a column are allowed. Candidate routes reciprocally reference the
same-column band ID; do not duplicate any band cells in attributed routes.

Standard coverage object: full_context_inspected true, raw_context_cells,
raw_blocks [{columns:[first,last],receipt:string}], actual_views with paths
and actual tool receipt if available, prior_knowledge, uncompleted_context [].
Blocks must exactly cover the context columns once; repeat observations may
be listed separately. State rows covered and exact-white display convention.
A false/truncated/uncompleted observation cannot be attested complete.

Run `read_context.py show --pair F5 --first 308 --last 315` with the bundled
Pillow Python; substitute finite bounds. Omitted rows are exactly white only.
g253 means (253,253,253); inclusive equal-RGB row runs are lossless. Split any
truncated display and reread. Do not smooth, guess or algorithmically pick ink.
