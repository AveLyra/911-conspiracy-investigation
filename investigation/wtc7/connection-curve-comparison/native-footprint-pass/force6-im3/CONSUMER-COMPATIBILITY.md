# Explicit compatibility before comparison

October 8, 2026. Recorded after the primary original froze and before any
historical comparison output. No original is rewritten and no pixel, identity,
status, target, exclusion or scientific acceptance criterion is changed.

Primary original SHA256:
`d53723cc3d1b86bdbaf5cbed2dec5690e18ddf67efad2dae323bc7905690a3e9`.
The primary reader clarified these points read-only after freeze; the original
script, JSON and notes retained their reported hashes (receipt `2b0e77`).

1. `coverage.rows: [0,87]` is the inclusive actual inspected-row interval.
   A consumer may recognize this exact key alongside `rows_covered` and
   `rows_inspected`; if multiple are present they must all agree with the
   required context. Preserve original keys. Missing, contradictory, boolean
   or out-of-range coverage must not pass.
2. Primary unassigned bands omit `unassigned_band_refs`. The reader intended
   route-to-band references, not outgoing band-to-band references. Preserve
   that omission rather than insert a fabricated original empty field.
   For this fixed F6 primary, validate the band identity, cells, candidates
   and every reciprocal route reference without requiring that unused field.
   If the field is present, it must be an empty list. This exception does not
   permit missing route references, missing candidate routes, new band links,
   unknown fields or any change to selected cells.
3. Primary actually read and pinned the worktree charter, not the controlling
   main-repository path requested in the job. Its initial note must not be
   interpreted as proof of a canonical-main read. Root compared the two
   complete files byte-for-byte and by SHA256 at `77f45d`; both are currently
   `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
   Root has read the actual main charter. The comparison must pin both paths
   and require continuing exact equality. This bounds the present authority-
   path mistake; it does not make the worktree copy an authority or alter the
   historical record of which file the reader inspected.

Separately preserved F5 primary bands carry two known supplemental fields:
`other_possible_origins` (a list of nonempty strings) and `continuity_claim`
(exactly false). Validate and preserve these; do not drop them to fit a newer
schema. Their presence is not permission to accept unrelated extra fields.

Consumer tests must exercise each permitted representation, conflicting
coverage aliases, missing route references and unauthorized fields. Compatibility
is bookkeeping only, not semantic validation, human acceptance or model support.
