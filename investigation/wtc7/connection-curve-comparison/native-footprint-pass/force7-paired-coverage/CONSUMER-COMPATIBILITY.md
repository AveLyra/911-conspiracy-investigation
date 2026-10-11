# Preserved identity and validation-only compatibility

The new source region is F7-Im2-early. Existing validator
`../force56-remainder/compare.py` unpacks a two-token `pair-source` identifier.
The local consumer first checks the exact new region, source, pair, fixed
integer target/context, role and fields. It creates a deep copy with only
region_id set to F7-Im2 for that validator, in isolated helper instances
configured with the new target/context. It checks the original remains unchanged.
Neither an original nor a saved source identity is relabeled. The old Im2
target is still a distinct preserved reading at a different path.

The existing source-row adapter renames fragment_membership on a copy for
the unchanged conditional calculator. The original status, memberships,
band references and source cells remain intact. Candidate cells retain full
reader paths so old and new regions cannot merge solely by their short names.
Both adapters are synthetic-tested before new historical comparisons.

The protocol's prose “both” means candidate_routes ['solid','dash'], not
a string 'both'. Every band retains its own list and reciprocal references.
All inherited exclusions and local-fragment-neighbor rules remain unchanged.
Results are C_H bookkeeping under three explicit hypotheses, not D or metrics.

Primary/peer are prospectively fixed version-role labels. The current source
readers are not necessarily the agents who authored earlier regions. P/P or
Q/Q across those regions must not be described as a same-person observation.
The four inherited scenarios are a declared sensitivity design, not every
possible combination of disputed cells or all forms of annotation uncertainty.
