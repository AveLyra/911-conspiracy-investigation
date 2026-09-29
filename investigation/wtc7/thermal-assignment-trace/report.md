# Repeated thermal assignments in the released WTC 7 inputs

Research-only WP3 / Q02 / Q06 / Q10, 2026-09-12. The full [investigation charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
remains controlling. This is an input trace and documentary comparison, not
a structural simulation, expert opinion, historical temperature reconstruction,
or finding about collapse cause or intent.

## Findings

The repeated assignments cannot all be explained simply by nodes shared
between different structural parts. In the model region labeled Column 79,
all 63 nodes with unequal supplied thermal coefficients connect only to
PID 179 in the examined mesh. Each has two assignments. They form seven
groups of nine nodes at regularly spaced model elevations. This is a more
specific transfer/export question than a generic complaint that the model
files are unavailable.

The two previously identified high-coefficient exceptions are different:
they are genuinely shared between parts, but each has nine assignments,
not one per incident part. Their rows do not identify nine historical times.
The effective solver temperature remains unresolved without the repeated-load
rule and input-processing history. The trace does not establish an error,
inflated temperatures, manipulation, or physical cause.

NIST's report identifies the global-analysis code as **mpp971dR4 beta,
revision 41161**, double precision. That is now a specific reported build to
investigate, not an unknown generic version. The executable's identity and
its actual use with the released bytes remain separate, unverified questions.
[NCSTAR 1-9A §3.6.3, printed 66 / PDF 117](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612)

**Verification status:** A separately written reader reproduces the selected
trace exactly. The final comparison passes 19,923 numeric comparisons with
zero difference. The independent checkpoint was frozen before producer
access; later source supplements and comparisons are separately labeled.
See [verification review](verification-review.md). Computational independence
does not create a second historical evidence source or expert validation.

## Selection and source coverage

The [prospective protocol](PROTOCOL.md) selected the two known exceptions,
842747 and 842833, plus every vertex of the master file's PID 179 shells.
The [prior independently checked member map](../model-member-map/report.md)
establishes the diagnostic-label → PSID 179 → PID 179 route. The label does
not authenticate an as-built drawing or mean that this part covers the
entire physical column.

Reconstruction finds 952 regional shells and 873 regional nodes. Including the
two exceptions gives 875 selected nodes and 954 retained thermal rows. Every
selected node has a coordinate, an assignment and mesh incidence. SRC-118–121
were streamed to EOF with pre/post compressed-byte hash checks. Source
lineage and every selected row are in [run01.json](run01.json). Neither
deletion list nor any new June-production payload was inspected in this unit.

The full thermal stream has 870,201 rows and 628,127 unique IDs; 235,010 IDs
repeat, 170,491 with unequal TS. There is one thermal-variable-node keyword
block, not a separately labeled thermal-history block for each repeated row.
All rows use TB = 0 and LCID = 2. These reproduce the earlier input counts, not
independent physical observations.

For a reproducible ordering description, a new **ordering run** starts only
when the next node ID decreases; equal IDs remain in a run. The resulting 677
runs are an analyst-defined numerical segmentation, not identified source
files, floors, export batches or time steps. Its definition was fixed before
the new trace. Blank/comment lines do not create runs. Every run's physical
line endpoints and row count are retained without selecting attractive runs.

## Column 79-region repetitions

| Node category | Nodes | Assignments each | Distinct incident parts |
|---|---:|---:|---:|
| One supplied coefficient, single part |792|1|1|
| One supplied coefficient, shared parts |18|1|2|
| Unequal coefficients, single part |63|2|1|

The 18 shared regional nodes do not repeat in this thermal file; the 63
repeating regional nodes are not shared between parts. Thus a rule attributing
every regional repetition solely to different incident parts is contradicted
by this input topology. Different thermal segments or export selections
within one part remain possible. Neither possibility has been established
as the actual mapping algorithm.

The following grouping by exact Z, ordered TS pair and ordering-run pair
is an explicitly **post-result descriptive summary** of all 63 selected
conflicting nodes, not a newly preregistered physical hypothesis. Values are
supplied coefficients in file order, not effective temperatures. Coordinate
units/floor names are not inferred from regular spacing.

| Model Z | Nodes | Earlier-row TS | Later-row TS | Ordering runs |
|---|---:|---:|---:|---|
|-67.2846|9|50.57|46.97|177,178|
|-63.3984|9|51.94|36.82|178,342|
|-59.5122|9|36.96|25|342,343|
|-55.626|9|25|46.69|343,507|
|-51.7398|9|46.86|97.37|507,508|
|-47.8536|9|97.67|62.24|508,672|
|-43.9674|9|62.56|25|672,673|

Adjacent listed elevations differ by 3.8862 model-coordinate units. The
periodicity is an observed property of this selected mesh/input join. It
suggests checking spatial-segment boundaries in the export routine, but does
not establish floor correspondence, separate source files, interpolation,
intent, or a correct resolution rule.

The later coefficient is lower for 45 nodes and higher for 18. This is useful
disconfirming detail against a description of the repeated rows as uniformly
increasing supplied coefficients. It says nothing about which row, combination
or other value the solver actually used.

For a concrete source locator, node 921518 has TS = 50.57 at SRC-118 line 512465
and TS = 46.97 at line 512527; both rows have TB = 0 / LCID = 2. Its master NODE record is
at line 925814, and its four incident shell elements all belong to PID 179.
The full trace retains the other 62 repeated nodes rather than treating this
example as additional corroboration.

## The two high-coefficient exceptions

| Node | Incident effective parts | Supplied TS values in file order |
|---|---|---|
|842747|73,74,176,1176|25;25;25;25;574.45;493.81;406.24;207.6;65.32|
|842833|74,177,1177|25;25;25;25;397.93;333.86;272.21;144.91;61.12|

Both nodes share master and outside-region shells; parts 73/74 are explicit
beam incidence in this trace. The outside include's +1000 part offset and
unchanged node IDs are inherited from the prior source-checked transform,
with identical source-byte pins. These part IDs are not automatically names
of physical members or proof of distinct thermal domains.

The first four rows for each exception occur in ordering runs 1–4, the next
four in 17–20, and the final row in 171 or 173 respectively. There is no
permission to interpret this sequence as heating followed by cooling. A
first-row choice and a last-row choice would select different coefficients;
neither is an established historical processing rule. The largest supplied
value is likewise not an established effective column temperature.

## What the primary documentation does and does not resolve

NIST describes mapping a Case B four-hour temperature profile to nodal
properties, then ramping it over calculation time 6.5–8.5 seconds. Those seconds
are initialization time, not a reconstruction of four hours of fire. The
inspected transfer paragraph and diagram do not explain repeated-row
generation or resolution. [NCSTAR 1-9A printed 52/56, PDF 103/107](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612)

The May 2007 Version 971 manual gives `T(t)=TB+TS*f(t)` for an individual
VARIABLE_NODE card. Its general discussion of input reordering does not
settle conflicting assignments. The [bounded primary-source review](method-source-review.md)
records nine targeted searches, selected complete manual/report pages,
release-note checks and failed retrievals. No applicable first/last/sum/
average/max rule was located. This is a documented search limit, not proof
that no rule or implementing code exists.

There is positive source correspondence as well: the newly inspected
NCSTAR 1-9A printed 66 lists 3,006,910 shells, 3,190 beams, 2,461 solids and 33,364
discrete elements. These match the corresponding typed counts in the
released assembly. The page also lists rigid entities, which this unit did
not reconstruct. Matching mesh counts supports the package's association
with the reported model size; it does not prove native run identity, complete
properties, effective thermal values or physical validity.

## Claim strength and next discriminating records

| Claim | Evidence layer and limit | What could change it |
|---|---|---|
|The selected 63 regional nodes with unequal coefficients connect to one part; they carry 126 assignment rows.|A within the derived input topology: independently reproduced, not a physical failure finding.|A reproducible parsing/transform error or a materially different historical assembly.|
|Seven regular elevation groups characterize those selected nodes.|A within the descriptive calculation: independently checked; no export algorithm identified.|Different source values/coordinates or a demonstrated grouping error.|
|NIST reports revision 41161 for the global analyses.|A: directly established documentary attribution, not executable authentication.|A corrected report or authenticated run records identifying another build.|
|Those repeated rows inflated historical temperatures.|D: unresolved; no applicable processing rule or matched outputs.|Applicable implementation plus echoed assignments and nodal thermal outputs.|
|The trace changes the preferred collapse explanation.|Not established by this unit.|A demonstrated physical consequence, independently justified input state and discriminating outcome comparison.|

The next high-value join is now precise: the **temperature mapping/export
routine and its node-selection convention**, linked to the supplied profile;
the duplicate-load behavior of **mpp971dR4 beta revision 41161**; and the
corresponding run input echo, warnings and nodal thermal output. These can
test whether the repeated assignments at these elevations arose from
spatial-segment boundaries or another export convention, whether they were
consolidated before processing, and how the solver handled them. No particular answer
is presumed. Missing materials and inactive damage/restart hooks remain the
separate dependencies already recorded in the member-map audit.

## Verification and reproducibility

Root run01 passes eight synthetic control groups and completes in 40.73 s
with 234.25 MiB observed peak memory. It retains all five read-pass receipts
over four distinct source files, numerical selection, ordering runs,
coordinates and incident-part counts. A fresh [run02](run02.json) reproduces
the entire result object exactly; only command, runtime and measured peak
memory differ in the surrounding receipt. Memory is measured after the run,
not an operating-system-enforced allocation ceiling.

The independent reader's 28 control groups pass. Its [frozen reconstruction](independent01.json)
uses exact decimal source values and no producer import; it completed in
70.97 s with 26.72 MiB observed peak memory. After seeing the producer schema,
it separately reread regional shell EID/line locators and global thermal
aggregates in a [supplement](independent-supplement01.json). That post-schema
pass took 21.75 s and is not relabeled as part of the earlier blind checkpoint.

The [independent comparison](independent-comparison01.json) and root rerun
pass for all 875 nodes, 954 assignment rows, 677 ordering runs, 952 regional
shell locators, 2,625 coordinate components and 898 node/part/kind incidence
rows, plus full-file thermal aggregates. There are 15,336 integer and 4,587
exact-decimal comparisons, with maximum difference zero. Repeated checks of
the same values are not additional observations. These readers do not
validate every unselected coordinate, general solver syntax or historical
input processing.

The [interpretation review](interpretation-review.md) caught two draft
wording errors: counting nodes as assignments and naming a possible spatial
boundary explanation as if it were identified. Both were corrected without
changing frozen numerical outputs. The 45-lower/18-higher descriptive count
was checked independently from the table and by root exact-decimal arithmetic.
Root independently viewed all three complete NIST source-page renders
(PDF 103, 107 and 117); it did not perform a fresh render itself.

Run the root calculation from the investigation worktree using the bundled
Python, with a fresh create-only output basename:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/thermal-assignment-trace/trace_assignments.py --output run03.json
```

The recorded root rerun used `--output run02.json`; `run03.json` above is a
fresh reproduction destination, not an execution claimed here. The independent
consumer command and exact code/input hashes are in the verification review.
Source originals, earlier results and canonical records remain unchanged.

No solver, Faraday execution, Sherlock evidence acceptance, canonical fact
promotion, legal amendment, external transmission, commit or push occurred.
The comprehensive investigation remains active and incomplete.
