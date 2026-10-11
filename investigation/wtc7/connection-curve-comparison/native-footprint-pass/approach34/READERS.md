# Reader assignments and export contract

October 8, 2026. Before E4 raw RGB reading: `approach_e4_primary` is primary
and `approach_e4_peer` is peer. Root remains E3 primary and
`approach_source_peer` remains E3 peer. These are separate computational
readers, not independent instruments, human reviewers or historical witnesses.
The unchanged PROTOCOL.md governs. Readers freeze originals before exchange.

Files per reader: `reader-E3-primary.py`/`.json`/`-notes.md`, and corresponding
E3-peer, E4-primary, E4-peer. Literal expansions may share a pinned mechanical
helper, but must not inspect the counterpart's annotations or algorithmically
select RGB cells. Keep full provenance/coverage in notes and export metadata.

Export top-level keys: `region_id` (`E3-Im10` or `E4-Im10`), `pair`, `source`
(`Im10.jpg`), `reader` (`primary`/`peer`), `target_box`, `context_box`, `inputs`
(relative path to hash/bytes), `script_pin`, `coverage`, `routes` (solid/dash),
`unassigned_bands`, `human_accepted` false, `physical_support` null.

Every route has one entry for every target column: integer `x`, sorted unique
integer `core` and `fringe` row lists (disjoint), `fragment_id` (single local
piece or null), `fragment_membership` (list of `{fragment_id,core,fringe}`),
`status`, `reason`, `boundary_flags`, `unassigned_band_refs`.
Membership unions must equal the cell classes exactly; no overlapping members.
Flags in this order: target_left, target_right, target_top, target_bottom, when
selected cells touch those boundaries. Empty entries have no membership.
Unassigned records additionally have `band_id` and `candidate_routes`
(`solid`, `dash`, or both). Every candidate route must reciprocally reference
the band in the same column. Do not duplicate its cells into an attributed route.
Multiple disjoint pieces of uncertain ink within a column may use separate
membership IDs in one aggregate band; record any aggregate-ownership limitation.

Status names and meanings stay as in parent PROTOCOL. Empty with a nonempty
conflict reference uses identity_conflict, not no_attributable_cells. Selected
route cells plus a conflict reference retain the identified piece and state
the additional uncertainty explicitly. `reason` is mandatory for every entry.
Only selected cells inside targets are exported; context informs boundaries.

Raw display runner is `read_context.py show --pair E3 --first 193 --last 202`
(substitute E4/finite bounds). It omits only exact white and uses lossless
equal-RGB row runs. `g253` means (253,253,253), not a threshold. Every requested
column prints. A truncated output is not inspected coverage: split and reread.
Run synthetic controls before historical saves; record all actual receipts.
No human acceptance, model identity across seams or physical support follows.
