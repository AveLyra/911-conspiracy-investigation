# Beam-set IDs and discrete-element candidates

2026-09-12. Post-run04 declaration, before root's new cross-family coordinate
joins. The unchanged [protocol](PROTOCOL.md) and [thermal addendum](THERMAL-DUPLICATE-ADDENDUM.md)
still control. Run04 resolves every set2 shell ID, but only six set2 beam IDs
occur in explicit `ELEMENT_BEAM` cards. This is not yet a claim that the
remaining identifiers are absent from the mesh.

The primary manual documents separate beam/discrete set families and null
visualization beams associated with discrete elements; the exact historical
delete-card/null-beam behavior remains unresolved. The [method follow-up](method-followup.md)
records the source pins. Continue by testing the remaining beam-set numeric
IDs against actual `ELEMENT_DISCRETE` records, preserving original card kind,
source line, endpoints, part references and numeric-ID candidate status.
Do not merge such matches into the explicit-beam count or infer that a
particular solver would delete the associated discrete element. No active
deletion card exists in the accepted assembly.

Also retain at most ten high-supplied-TS node examples per named diagnostic
set, with their minimum/maximum coefficients and row counts, to expose the
source of a threshold exception without dumping the node table. These are
the declared existing >300 threshold, not a newly optimized cutoff. A set
envelope concerns only its actual listed parts, not an entire physical
column or a reproduced cross-section-force selection.

Run04 remains intact. The independent reader is already freezing its own
cross-family candidate calculation before seeing root outputs. Source
preservation, exact-value/record-count distinctions, local numeric-only
output limits and all no-solver/no-causal-promotion boundaries continue.
