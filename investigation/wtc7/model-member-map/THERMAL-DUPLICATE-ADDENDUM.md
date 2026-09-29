# Thermal duplicate handling: declared after the first failed full thermal pass

2026-09-12. Supplement to the unchanged [protocol](PROTOCOL.md), before any
successful member/thermal or damage/geometry result from the new root parser.

Root run01 rejected the first repeated thermal-node ID. Root run02 retained
exact-identical repetitions, read the complete thermal stream and rejected
unequal TS values at repeated IDs. These are preserved failures of the
initial scalar-per-node admission rule. No geometry map was produced by
either run, and no cause inference follows from this finding.

The continued analysis will retain physical row counts, unique-node counts,
repeated-row counts and nodes with more than one supplied TS value. TB and
LCID are separately checked, not inferred from TS. For each unique node,
retain the minimum and maximum **supplied coefficients**, without choosing
first/last, summing, averaging, or interpreting the solver's duplicate-card
behavior. Provide parallel threshold summaries of those two endpoints and
separate the unambiguous-node summary. Part and diagnostic-set aggregates
will union node IDs before counting. A bounded numeric example of at most
ten largest coefficient ranges may identify the highest-value follow-up.

These are envelopes of source assignments, not physical temperature
uncertainty, a solved field, or alternative historical collapse runs. Even
identical duplicate coefficients do not establish that the historical solver
treated duplicate cards as redundant. The solver-version-specific handling
and model-author thermal-transfer convention remain explicit dependencies.
The independent reader must check duplicate identity and endpoint summaries
with its own arithmetic before these become report findings.

This adds no source or disclosure route, solver execution, canonical
promotion, legal finding, or numerical cause ranking. All original protocol
privacy, bounded-read, failed-run and source-preservation rules remain.
