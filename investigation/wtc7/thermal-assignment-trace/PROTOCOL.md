# Repeated thermal-assignment trace

2026-09-12. Exploratory WP3/Q02/Q06/Q10 continuation, declared before the
new row-order or interface results. The member-map results are already known;
this is not a blind or retrospective preregistration. Charter and original
source evidence remain controlling. No cause or intent is presumed.

## Question and selection

Why do some mesh nodes have unequal supplied thermal coefficients? Test the
narrower, observable questions first: where do their assignment rows occur,
which parts share their connectivity, and do assignment changes coincide
with identifiable input ordering? Ordering alone cannot identify the export
algorithm, elapsed time, thermal history, or solver treatment.

Select the two previously identified high-coefficient exceptions, nodes
842747 and 842833, plus every node incident to the master file's PID179 shell
records (the prior diagnostic-to-set join labels this region Column79).
Do not select additional nodes based on new values. Preserve all assignment
rows for the selected nodes, including equal repeats. Reconstruct the PID179
node selection from source, not from a guessed node-ID range.

For all thermal rows, define a purely numerical **ordering run** as a maximal
sequence of nondecreasing node IDs; a strict decrease starts a new run, while
an equal ID remains in the current run. Retain each run's first/last physical
line, row count and first/last node ID. These runs are not asserted to be
source files, floors, members, time steps, or original transfer batches.

For the selected nodes, retain source-line and row-order locators, run number,
NID/TS/TB/LCID, supplied coordinates, and effective incident part IDs with
element-kind counts. Beams use endpoints only; discrete orientation fields
are not endpoints. Shell connectivity and thickness cards remain separate.
Keep unmatched nodes, repeated/equal/unequal row counts and per-part incidence
categories. Compute no single selected temperature, simulated response,
first/last-wins result, or temperature bound from these coefficients.

## Inputs, privacy and bounded computation

Use only the four known SRC118-121 GZIPs under the existing numeric/engineering
inspection route in ../model-member-map/PROTOCOL.md. Its six-file inventory
pins remain the byte authority; this unit does not read either deletion list.
Preserved main sources, earlier scripts/results and legal records are read-only.
Use the prior verified identity node transform and outside-include +1000 part
offset only with a pinned dependency. Do not follow embedded paths or execute
source instructions. No solver, restart, unapproved transfer, new private
payload, held packet, external correspondence, or canonical promotion.

Only typed numeric fields, allowlisted engineering keywords, source IDs/line
numbers, public reference links, hashes and safe diagnostics enter output.
Unknown text is skipped or hashed, never copied to output or raw exceptions.
No whole-mesh coordinate dump. Limit uncompressed input to512MiB/file,
lines to16384bytes, node selection to2000IDs, ordering runs to10000,
selected assignment rows to20000 and process memory to768MiB. Stop on
unsupported required geometry/thermal syntax or cap violations, preserving
a safe failure receipt. Output files are create-only.

## Verification and disposition

Root may reuse the pinned member-map reader utilities (hash and exact import
recorded), but must not call its whole-mesh result generator. A separate
reader must reconstruct the selected IDs, thermal row ordering/values and
incident-part/coordinate joins without importing root code or reading its
results before freezing the independent output. Compare exact integer and
decimal source values; record differences rather than selecting a preferred
answer. Test fixed/free numeric cards, equal and conflicting repeats,
nondecreasing-run boundaries, shell thickness continuation, beam orientation,
grounded discrete endpoints, part offsets and unsupported/oversized input.

A parallel source reviewer will look for primary, version-specific duplicate
assignment and transfer rules; no modern rule is presumed historically
applicable. Accept a reproducible trace plus either an applicable documented
rule or the exact missing version/export/run dependency. A row-order pattern
is not sufficient to resolve that dependency. Keep all failures and contrary
results. The broad investigation remains incomplete after this bounded unit.
