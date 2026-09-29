# Independent first shared-node graph verification

Research-only work, September 13, 2026. This reviewer was assigned the first
shared-node input graph, not a complete directional-restraint model. Main's
AGENTS.md, WORKFLOW.md and START-HERE.md were read, together with the complete
unit protocol, SHA-256
b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d.
Evidence-falsification, source-of-truth and development-verification controls
separate source content, deterministic graph extraction and physical inference.

## Implementation independence and source boundary

The new root code and output were not consulted before this reviewer's first
implementation and actual source extraction. The normalized Column 79 label
and the earlier PID 179 result were already known; this is not blind discovery
of a historical column. The new graph selector and streaming extraction were
written independently. Numeric card handling was adapted from this reviewer's
own earlier member-map reader, which was inspected before reuse and is pinned
at de7ee2aa5f4a2aedd4a9446561322aa5e14e688d1c72a57aa96e593df1f148cc.
No earlier root parser or new root function was imported. The prior reader is
a provenance dependency, not an executed extraction dependency.

[verify_restraint.py](verify_restraint.py) first-pass code SHA-256:
5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a.
The actual input streams are only SRC-119, SRC-120 and SRC-121, read from the
three existing compressed originals. Compressed and complete decompressed
byte hashes are checked against the earlier independent pins. The master
thermal include is identified by source alias but not followed. No thermal
assignment, damage-list content, raw macro, held source or external source
is read for this extraction. The source filenames do not select execution.
Comments and arbitrary titles/unknown tokens are not emitted; known engineering
keyword names or hashes are retained. Selected numeric records stay local.

## Declared extraction

Three complete streaming phases are used:

1. Collect compact node/coordinate/source-line arrays and numeric metadata;
   resolve exactly one normalized Column 79 diagnostic, its PSID and its
   supplied part-set members. Verify the include targets and four transform
   metadata cards before applying the supplied part/section/material offset.
2. Parse every physical element in all three geometry streams; select all
   elements in the resolved seed parts and union their physical node IDs.
   Reject duplicate element IDs within a family and duplicate node IDs.
3. Parse all geometry again; retain every element outside the seed parts
   sharing one or more seed node IDs. Require complete element-family coverage
   counts to agree between the two element passes. Attach numeric coordinates
   and retain the source locator of every selected physical node.

Physical connectivity preserves source order and repeated slots. Shells use
the required connectivity/thickness pair. Beam nodes 1 and 2 are endpoints;
node 3 is separately retained as an orientation reference, never used to
create an edge. Discrete ground node 0 is not a physical vertex. Matched seed
IDs are unique and sorted, so repeated connectivity slots do not multiply an
incidence. Coincident coordinates with different IDs never create an edge.
Selected numeric coordinates are parsed binary64 values, required to compare
exactly later, not a tolerance-based geometric proximity match. No dimensional
unit, floor number, physical direction or bracing length is assigned.

Output includes the diagnostic and set locators/cards, all seed and neighbor
element records, matched seed IDs, ordered physical connectivity, separately
retained orientation IDs, selected coordinates and node locators, the seed
coordinate envelope, incident part/section/material references and supplied
definition locators or explicit missing/ambiguous status. Property references
are not physical property values or a constitutive validation.

## Actual synthetic checks before source extraction

Fifteen groups passed in the bundled Python runtime:

- orientation-only beam matching excluded; actual endpoint matching retained;
- repeated ordered vertices retained with unique matched IDs;
- identical coordinates on distinct nodes do not create an edge;
- outside-region original PID 179 becomes effective PID 1179;
- seed-part elements excluded from neighbor results; no-neighbor result empty;
- discrete ground endpoint omitted;
- missing node, duplicate node and incomplete numeric card rejected;
- two-line shell connectivity/thickness pairing and source lines preserved;
- missing shell continuation rejected;
- normalized column label distinguished from a bare numeric identifier;
- existing-output guard rejects an already existing path.

The last control tests the same guard condition on the script's existing path;
it is not yet a separate end-to-end CLI overwrite-refusal execution. Likewise,
the outside-namespace fixture tests the part-ID helper, while the actual run
checks the full supplied transform metadata. These groups do not establish
complete parser branch coverage or source/measurement accuracy.

## Frozen actual extraction

[independent01.json](independent01.json) completed at exit 0, PASS, before
root code/results were accessed. SHA-256:
d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7.
All 15 synthetic groups passed again in the source run. Elapsed time was
118.312266667 seconds; peak resident memory was 370,753,536 bytes. The
receipt records Python 3.12.14 and the NumPy version, exact command, all three
compressed source pins, protocol/prior-reader/code pins and before/after
equality. All nine source-phase streams reached EOF and matched the complete
decompressed hashes. This reviewer read and checked those actual receipts;
there is no failed historical extraction in this run.

| Geometry source | Complete bytes per phase | Physical lines per phase | Parsed element counts in each element pass |
|---|---:|---:|---|
| SRC-119 | 508,372 | 7,905 | 2,461 solids |
| SRC-120 | 232,959,541 | 4,088,491 | 2,042,843 shells |
| SRC-121 | 333,947,423 | 7,196,443 | 964,067 shells; 3,190 beams; 33,364 discrete elements |

The three streams contain 3,593,049 unique input nodes. Their full coordinate
arrays are not exported: only 891 nodes needed by the selected graph are
retained in the result. Diagnostic 179 at SRC-121 keyword line 614 / header
615 / plane cards 616–617 has normalized column label 79 and PSID 179.
SET_PART_LIST 179 at keyword 611 / header 612 / member row 613 selects
effective PID 179. This independently re-establishes the model-label/set
association; it does not authenticate an architectural column extent.

The result retains all 952 seed shells and their 873 unique physical nodes.
Every one of the 20 direct outside-seed neighbors is an SRC-120 shell with
effective PID 1179. They share 18 distinct seed nodes. The graph has two
incident parts including the seed, and no orientation-only beam candidate.
There are no explicit master beam/discrete or mass-solid first neighbors
under this shared-node rule. That negative graph result does not establish
absence of connections encoded through different node IDs and constraint,
contact, tied-interface or other coupling cards.

The seed coordinate envelope by supplied x/y/z axes is respectively
[13.13262, 13.77258], [2.408667, 3.077733], and [-71.1708, -43.6118].
No units, compass directions or floors are assigned to these numbers.
PID 179's supplied reference is SECID 179 / MID 99; the outside original
PID 179 becomes PID/SECID/MID 1179. Both selected parts have a unique supplied
section and material definition locator. “Resolved” here means only that
identifier join, not complete physical properties or verified stiffness.

The independent output and first-pass code hashes were sent to the parent
immediately on completion. The completed root comparison below is a post-freeze
schema comparison, not blind independent discovery. The frozen extraction
was not overwritten or altered for that comparison.

## Inference ceiling

Limits are 512 MiB
decompressed per stream, 65,536 bytes per physical line and 768 MiB observed
peak process memory. Failures are not permission to guess a card's meaning.

This extraction establishes at most a direct shared-node model graph. It does
not independently reproduce constraint/contact/boundary card semantics, tied
interfaces, spring laws, load or damage histories, solver state or the complete
architectural Column 79. A shared node is not automatically a demonstrated
load-bearing restraint; no shared node is not proof of physical disconnection.
Capacity, stability and collapse-cause claims remain outside this unit's first
input test. No root comparison, historical execution or physical validation
is established by successful local parsing alone.

## Exact post-freeze comparison

The parent released its frozen root01/root02 outputs for comparison after the
independent source graph had frozen. An important qualification is retained:
root received this reviewer's summary counts and PID 1179 conclusion before
its own code was saved, but not the independent arrays or code. Root reports
that it did not adapt its selector to those counts. The independence here is
separately implemented extraction with a frozen independent array, not blind
discovery of result counts. Both implementations also had prior knowledge of
the diagnostic/PID 179 model association.

[compare_restraint.py](compare_restraint.py), SHA-256
787db0403077f275300b01b4ec2057f78f09a985a79ac0506989e0db2de789e7,
compares the independently frozen graph with both root outputs. It does not
invoke a new mesh extraction or expand contact cards. It freshly hashes the
three compressed source files for integrity only. Root's 304-line new program
and the relevant helper card/heading/control definitions were inspected before
importing them solely to replay their synthetic tests.

[comparison01.json](comparison01.json), SHA-256
e8170327902408d76cdc136342fc8d3c4017a92704d9027ba7fbfe5ea7e7455e,
completed at exit 0, PASS, with zero failed comparisons. Producer pins are:

- root01.json: f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef;
- root02.json: 179682c5caf5cdfac31c508d88e545a843fb07839bb7150832333790ed9e90e3;
- map_restraint.py: 4d49ed698f9802a859a364d4f71721d54e1d3511b50bd96f7b02f5ac3bc7b520;
- root's prior helper: f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b.

The complete root objects differ only in elapsed_seconds. Their equality
includes repeated metadata but does not independently validate metadata absent
from the independent extraction. Both root results match all 952 seed and 20
neighbor records for source, element source line, EID, family, original and
effective PID, complete ordered physical vertices and orientation field.
Every seed intersection is also checked, including the root's explicitly
retained neighbor intersections. All 891 selected coordinate triples agree
exactly as parsed binary64 values, using float.hex equality without tolerance.
Per-vertex coordinate lookups and seed bounds agree as well. Neither program
uses exact source-decimal strings as its coordinate representation; this is
exact agreement of parsed numbers, not a claim of unrounded physical precision.

The comparator checks the normalized diagnostic/part-set association, 873
seed node IDs, two incident part-reference records, three include edges, four
transform cards, all three geometry streams' five element-family count groups
and the 3,593,049-node total. It checks all six root source-phase EOF/hash
receipts against the independent source pins and line counts. All input/code
hashes remain unchanged across comparison. Exact scalar coverage across both
root comparisons is 61,574 numeric values, 3,940 strings, 37 booleans and 1,962
nulls. The numeric count includes 28,686 coordinate components: selected-node
coordinates, repeated per-element vertex coordinates and six bound values per
root. These repeated checks are not new physical observations.

Explicit schema normalizations are limited to approved source aliases, field
names, root keyword-line locators versus independently retained keyword/header/
card locators, exact integer-valued float metadata, blank fixed-card padding,
and transposition of min/max bounds. Trailing transform padding must be null
before trimming. Vertex order and repeated slots are never discarded or sorted
to force agreement. There is no numerical tolerance, coordinate-nearness join,
unit conversion or physical interpretation in this adapter.

### Compared-field and control ceilings

- Root node coordinates do not contain source/line locators. The 891 node
  locators retained independently are not claimed twice verified.
- Root omits the independent shell thickness/continuation cards, individual
  diagnostic/part-set/transform card-row locators, full PART cards and section/
  material definition-line locators. Only common fields were compared.
- Diagnostic heading hashes use different recipes: root hashes the ID-plus-
  heading card; independent hashes the stripped heading alone. Part-heading
  hashes have no independently retained counterpart. Those hashes were not
  coerced into equality. Normalized column number, ID, PSID and keyword locators
  agree separately.
- Root's CONTACT/NSET inventories, TC/RC fields and nonzero-constraint-node
  total have no independent extraction here. Root-pair determinism is not
  independent source verification of them. No contact expansion was performed.
- Root seed intersections and per-element coordinates were derived from its
  retained node lists/global coordinates for comparison; they are not separate
  stored root fields. Root neighbor intersections are explicitly stored.

Fifteen new comparator controls passed. They detect changed source/line/EID/
family, both part namespaces, vertex ordering, removal of repeated slots,
orientation fields, duplicate intersections and a one-ULP coordinate change;
they also reject boolean-as-ID and nonblank padding, accept exact numeric
representation aliases and check fixture nonmutation. All 15 frozen independent
controls and all 27 root controls were actually replayed and passed. Root's
27 comprise 17 prior helper tests and ten new graph tests, not 27 independent
physical or graph-specific experiments. All actual selected elements are
shells; the agreement does not establish complete beam/ground-discrete-neighbor
coverage, general parser correctness, coupling semantics or physical restraint.

One initial producer-filename probe returned not-found and was corrected from
the actual local inventory. An early schema-summary command printed an overly
large nested numeric inventory and was truncated; later inspection used only
selected fields. Neither event is a successful extraction or an independent
CONTACT/NSET audit, and neither changed source or frozen results. The comparison
itself had no failed numerical run or patched result.

The parent completed the create-only consumer replay in
[comparison-root01.json](comparison-root01.json), SHA-256
10bb00990aa15f9afbbfafa446c510e5c73e97ca1e5e37823152b60a6c23fba3.
This reviewer inspected the actual saved receipt and checked the complete
object against comparison01.json: both are PASS and differ only in command
and elapsed_seconds. All numerical counts, controls, pins, exclusions and
comparison results are identical. This is a separate consumer execution of
the frozen comparison, not another independently implemented mesh extraction.
The bounded direct graph agreement and comparison replay are complete;
source/directional restraint synthesis and any later coupling expansion remain
separate tasks under their own protocols.
