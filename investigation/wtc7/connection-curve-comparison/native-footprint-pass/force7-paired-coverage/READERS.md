# F7 earlier-Im2 reading contract

Read this protocol and `../force56-remainder/READERS.md` completely. Reuse that
field contract, not its old targets, role aliases or filenames. Here primary
is `envelope_arithmetic`, peer is `energy_admission_review`; serialized reader
is exactly `primary` or `peer`. Keep their originals separate until both freeze.

Save only your own `reader-primary.py`, `reader-primary.json`, and
`reader-primary-notes.md` (or peer). The literal script exposes `build()` and
uses exclusive creation for the JSON. Use apply_patch for code and notes.
No post-freeze changes to an original: preserve an error and version any
correction separately. Report file hashes before any counterpart access.

JSON keys: region_id `F7-Im2-early`, pair `F7`, source `Im2.jpg`, reader,
target_box [220,0,330,88], context_box [218,0,332,88], inputs (relative to this
directory; SHA256/bytes), script_pin, coverage, routes {solid,dash},
unassigned_bands, human_accepted false and physical_support null. Every route
has exactly 110 entries, x220 through329, with the earlier contract's exact
x/core/fringe/fragment_id/list-valued fragment_membership/status/reason/
boundary_flags/unassigned_band_refs fields. Bands add band_id and
candidate_routes; their unassigned_band_refs is an empty list. Multiple
disjoint bands in one column are allowed. Do not pool fragments with distinct
possible ownership into one undifferentiated band.

Coverage: full_context_inspected only when true, raw_context_cells 10032,
raw_blocks [{columns:[first,last],receipt:string}], actual_views,
prior_knowledge, rows [0,87], uncompleted_context []. Account for columns218
through331 exactly once, listing any necessary rereads separately. Raw display
command: `P -B read_context.py show --first 218 --last 225`. P is the bundled
Python executable given in the parent run records. Only exact white omitted;
inclusive equal-RGB runs and gN=N,N,N are lossless. Split truncated output and
actually reread it; do not attest invisible cells.

Pin both context files and their complete declared transitive input maps,
this protocol/contract, the earlier field contract, source and any explicit
helper. Check all before/after pins. Code only expands manually chosen literal
runs; it must not choose cells from RGB. Preserve prior familiarity/coverage
honestly. The context is not extra annotation target, and earlier readings
are not new evidence. No human status may be supplied by an agent.
