# What the released model inputs now let us locate

2026-09-12. WP3 / Q02 / Q06 / Q10. Research only. The [charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
controls the investigation; preserved SRC-116–121 control the input evidence.
This is a numeric input-graph reconstruction, not a solver run, expert structural
opinion, authenticated historical temperature field, or legal finding.

**The production supports a real member-level audit, but not yet a reproduction
of the collapse.** The corrected [map](run06/member-map.json) links mesh records,
parts, thermal assignments and supplied deletion-list candidates. It also
exposes repeated unequal thermal assignments and unresolved material references.
Those need explanation before these inputs can be treated as a resolved
historical run. A previous shell-count overstatement was our inventory-method
error, not an agency discrepancy.

## What was actually checked

All six compressed sources passed their existing byte/hash pins before and
after reading and reached EOF under the 512 MiB per-file limit. Only the
three declared active includes were assembled; the two damage lists remained
separate, unused candidate lists. No source filename became an executable or
an extraction destination. Arbitrary headings/comments were omitted or hashed;
output retains numeric joins and bounded engineering classifications only.

The [protocol](PROTOCOL.md), post-failure [thermal rule](THERMAL-DUPLICATE-ADDENDUM.md),
and post-run04 [cross-family rule](CROSS-FAMILY-ADDENDUM.md) preserve when analysis
choices changed. The independently developed [source-method review](method-source-review.md)
and [follow-up](method-followup.md) use LSTC's contemporary
[May 2007 Version 971 manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf).
That edition is not proof of the historical executable/build.

### The mesh count is now a record count

| Supplied mesh component | Typed element records |
|---|---:|
| Master shell elements | 964,067 |
| Outside-region shell include | 2,042,843 |
| Total shells | 3,006,910 |
| Explicit beams | 3,190 |
| Discrete spring/damper elements | 33,364 |
| Mass-component solids | 2,461 |

The assembly has 3,593,049 unique defined nodes, 459 part definitions and
392 parts used by the parsed elements. Every examined element node resolves;
no duplicate node or same-kind element ID was accepted silently. None of the
shell records uses the N3=N4 triangle pattern; this counter does not by itself
prove four distinct vertex IDs. The supplied solids use the
supported single-card form; the reader rejects unsupported two-card forms.

The earlier [content audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/report.md)
counted both shell connectivity and thickness rows. Its outside-include table
correctly called them rows, but its master summary called about 1.93 million
rows shells. The actual master shell count is half that. The old audit and
its output are preserved; this is an additive correction, not a rewritten
source or allegation about NIST.

## Thermal rows do not identify one value per node

The file contains 870,201 assignment rows, **628,127 unique node IDs**, and
242,074 rows beyond one per ID. Of the unique nodes, 235,010 appear more than
once and 170,491 have unequal supplied TS values. Every row has TB=0 and
LCID=2. All unique thermal IDs resolve to mesh nodes and element incidence.

The old histogram is reproducible as a **row** histogram. It must not be
treated as a count of unique physical locations. There are also 50,023 thermal
nodes incident to multiple parts; summing per-part counts yields 683,397
incidences, not that many unique nodes.

| Descriptive input statistic | Minimum supplied TS per node | Maximum supplied TS per node |
|---|---:|---:|
| Unique node count | 628,127 | 628,127 |
| TS >100 | 259,634 | 276,086 |
| TS >200 | 130,896 | 150,041 |
| TS >300 | 70,375 | 88,964 |

These endpoint summaries do **not** choose the first/last assignment or
average/sum duplicates. They are not temperature confidence intervals and
do not bound the unknown solver response. The manual gives the individual
card expression `T(t)=TB+TS*f(t)`, but the inspected section does not specify
the applicable duplicate-card resolution. Even equal repetitions need that
rule before being called redundant. Curve/reference/unit conventions remain
additional dependencies. [Primary-method limits](method-followup.md)

### A specific, bounded column association

There are 83 named cross-section diagnostics and 85 part sets. The verified
documented route is diagnostic label → PSID → part set → part → elements →
nodes. It is not a guess that PID79 means architectural Column79.

For the diagnostic normalized as Column79, master lines614–616 reference
PSID179; the set beginning at611 lists PID179. Its definition at3527 uses
SECID179 and MID99 (`MAT_ELASTIC_VISCOPLASTIC_THERMAL`). It contains 952 shell
elements and 873 incident thermal-node IDs. The model-coordinate envelope is
X13.13262…13.77258, Y2.408667…3.077733, Z−71.1708…−43.6118.

| Model diagnostic / listed part | Incident thermal IDs | IDs with unequal TS | Largest supplied TS |
|---|---:|---:|---:|
| Column79 /179 | 873 | 63 | 116.45 |
| Column80 /180 | 873 | 63 | 91.30 |
| Column81 /181 | 873 | 63 | 135.62 |

The selected source coefficients are low. This is an **input-consistency
observation**, not independent support for the published column temperatures
or initiating mechanism. It does not establish historical temperatures, loss of bracing, column
instability, or propagation to the perimeter. These part sets cover their
actual listed mesh regions, **not necessarily entire physical columns**.
Their names remain model-author attribution without an original-drawing
crosswalk. The cutting-plane force selection itself was not reproduced.

Do not generalize the table into “every column is below300.” The “All Columns”
set has two incident nodes whose maximum supplied TS exceeds300: node842747
in diagnostic176 spans25…574.45, and node842833 in177 spans25…397.93; each
appears in nine thermal rows. Neither has a unique assigned coefficient.
These specific exceptions require source-transfer/duplicate-rule checks,
not silent deletion or a declaration that the published physical claim is
disproved. The largest per-node minimum over that whole set is178.05.

## Candidate deletions now have locations, not an execution history

All 1,543 set2 shell IDs resolve to actual shell elements. Their part counts
are PID11:36, PID27:1,301, PID712:3, PID731:38, PID742:2, PID751:42,
PID761:105, PID772:7 and PID803:9. All45,152 unreferenced CaseA shell IDs
also resolve, across43 parts; their intersection with the set2 shell list
is empty. The CaseA list's purpose remains unestablished by this join.

Of the361 IDs in the set2 beam list:

- Six resolve to explicit `ELEMENT_BEAM` records, all PID98.
- The other355 resolve numerically to `ELEMENT_DISCRETE` records across19
  parts. They are separate **cross-family candidates**, not confirmed
  beam-deletion behavior or IDs missing from the entire mesh.

The six explicit beams form three endpoint pairs at model Z93.0148,
95.5548 and98.0948. Each spans approximately X−2.1336…0, with one member
near Y0 and the other near Y−9.41. Their orientation node is kept separate
from the physical endpoints. This gives a checkable geometry for the earlier
source comment about penthouse decoupling, but neither says when a historical
run used it nor proves that the real structure failed that way.

The contemporary manual separates beam and discrete set families while
describing generated visualization null beams. The inspected text does not
settle deletion of the associated discrete element through that generated
representation. [Exact source and limits](method-followup.md)

No active delete card was found in the accepted assembly. Geometry agreement
with an unused list cannot establish historical deletion, force transfer,
failure timing, intentional support removal, or a valid post-removal replay.

## Missing properties and what changes scientifically

All392 used parts resolve to part definitions and section references, but
23 used parts reference19 material IDs without an active definition in the
parsed assembly:25,33,711,712,713,723,731,733,741,742,743,751,761,762,763,
772,773,802,803. The full part/MID mapping remains in the numeric output.
We did not substitute bulk properties or infer a constitutive law from a
part heading. This strengthens the warning that the package is not yet a
demonstrated runnable reproduction. The prior gravity/thermal schedule is
a configuration finding, not proof even that the stripped deck executes
successfully.

This work makes the audit more specific in both directions. Some core-column
input coefficients are indeed low; all candidate identifiers have meaningful
mesh-record counterparts when their families are kept distinct. Conversely,
unequal repeated thermal assignments, missing material definitions and the
unresolved beam/discrete deletion link are concrete reproduction dependencies.
None establishes that NIST contrived a model, that office fires produced the
observed support loss, or that deliberate demolition did. **No causal ranking
is changed by this input-only unit.**

| Claim | Evidence type / strength | Weakening test or unresolved alternative |
|---|---|---|
| Earlier shell total counted two rows per element | Source-code observation + complete typed count / strong | Different bytes or a different record layout; complete pairing is now checked. |
| Repeated node IDs can carry unequal supplied TS | Direct input observation + calculation / strong | Independent source reconstruction must reproduce the groups; historical solver interpretation remains separate. |
| Named Column79 part has largest supplied TS116.45 | Model-attributed join + calculation / strong for selected cards | Wrong label/set/mesh mapping, other physical-member regions, or duplicate/reference handling can defeat a historical-temperature inference. |
| All candidate IDs map to supplied element records | Typed/numeric join / strong with explicit-family qualification | Discrete matches do not establish executable beam-set deletion. |
| These files validate the global collapse mechanism | Not established | Missing properties, state/run lineage, duplicate handling, contacts/capacities and independently measured response still need tests. |

## Verification and next test

Two root full reads (run04 and run05) had identical common numeric results;
run05 added the declared cross-family candidates and bounded high-TS examples.
Their agreement did not catch a shared-array error in one diagnostic's
geometry bounds. Independent comparison found it; run06 corrects aggregate
ownership and preserves the earlier results as failed verification, not as
source defects. A new synthetic test checks that aggregating bounds cannot
mutate a source part's bounds.
An independently written reader froze its own complete result before viewing
root outputs. Its final comparison and supplemental-source scope are tracked
in [verification-review.md](verification-review.md); [validation.md](validation.md)
records exact commands, pins, failures and final disposition. Passing software
checks is numerical verification, not physical validation or human expert review.

Highest-value next bounded task: trace the repeated thermal assignments and
their source-transfer convention, beginning with nodes842747/842833 and the
Column79-region repetitions. Determine the exact applicable solver/transfer
rule before constructing a scalar thermal field; if it remains unavailable,
record the precise missing implementation/run record. In parallel, the
identified19 material IDs and six explicit penthouse ties give concrete
targets for the existing missing-input/run-state crosswalk. No solver,
outreach, hypothetical property substitution or assumed restart is authorized
by that queue.

The full investigation remains active. Original evidence, prior analyses,
canonical facts, pleadings and correspondence were not changed. No commit,
push, external transfer, Sherlock evidence acceptance or Faraday execution
occurred. Generic typed-record/duplicate/join lessons remain local under the
existing archived-feedback routing boundary.
