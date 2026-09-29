# Independent joint-consistency oracle

September20,2026 UTC. Research-only exact arithmetic on the two already frozen
page47 transcriptions. Main controls, full charter, new protocol, prior report,
prior PROTOCOL/CLOCK-ADDENDUM and old reconciliation schema were read.
No new PDF/image inspection, acquisition, network, installation, fitting,
clock tuning or physical/structural solver was used.

## Independence, chronology and controls

The oracle consumes the independent transcription
`fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8`.
It reconciles all70 rows/all11 selected columns against the other transcription
and verifies the held PDF hash without rendering it. Source blanks remain
null; no missing position or endpoint is interpolated.

[chain_oracle.py](chain_oracle.py) was independently implemented without reading
root's new calculation or results. For each parity/missing-edge component it
propagates exact Fraction reachable intervals, intersects each with its original
position bounds, and reconstructs a complete witness backwards. Empty reachable
intervals carry chains of original input inequalities whose sum proves
`0 <= negative`. The certificate checker recomputes those inequalities
rather than trusting a reported reachable interval. Every feasible witness
is checked against all original position and difference constraints.

The optional strict version treats **all** bounds/differences as open intervals;
Minkowski addition/intersection remain open. It distinguishes forced
boundary-only feasibility from a particular witness that happens to use a
boundary. This is an exact feasibility distinction, not a recovered rounding
tie policy or physical uncertainty statement.

The first synthetic test invocation reached the final create-only control, then
failed because the sandbox denied its temporary fixture directory inside oracle/.
No historical inputs had been loaded. The scoped escalation reran the same
unchanged code successfully; this was a permission failure, not a mathematical
repair or relaxed acceptance criterion.

All18 control groups passed before each historical run: constant and positive/
negative linear sequences; translation; exact closed endpoint-only feasibility;
beyond-bound failure; individually compatible yet jointly impossible rows;
corrupt certificates and witnesses; disconnected chains; missing-neighbor versus
missing-center distinctions; unsupported first velocity; duplicate/unsorted/
nongrid/malformed rows; duplicate constraints; and create-only refusal.
The two certificate and three witness corruptions are grouped controls, not
five additional independently counted groups.

Actual commands from the investigation worktree, all with
`PYTHONDONTWRITEBYTECODE=1` and Python3.13.7 `-B`:

```sh
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/multipoint-joint-consistency/oracle/test_chain_oracle.py
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/multipoint-joint-consistency/oracle/chain_oracle.py run01
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/multipoint-joint-consistency/oracle/chain_oracle.py run02
```

The test and both create-only runs returned exit0 after narrowly scoped write
approval. Both runs freeze source/protocol/code/runtime pins and unchanged
before/after identities. Their198904-byte results are byte-identical.
Results hash/coverage was sent before reading any root code or outcomes.

| Frozen item | SHA-256 |
|---|---|
| chain_oracle.py | 0cb2814e9811ca384ea49df9c90c1089823fdcb6e534ea58cfea7484b424fedf |
| test_chain_oracle.py | a0989336691a804d0daddef8cdd8a480da95671927d9b6795e6d050eea0c92b9 |
| run01/results.json and run02/results.json | 9774f906fe3fc3f3f6fcd7462bd4b454acdfaee0e05a33c6cf3e0903964492a7 |
| Parent protocol | 4ed21c2fae4d36869588130321767134d72539fb618f47168e6c6170026300c0 |
| Root run01.json and run02.json, checked only after oracle freeze | 1ef82cb48b3b688b35acafed4458873657eaf9d237678508b0d9ba7cb23fd86c |
| Root calculate.py, inspected only after oracle freeze | 92c729a5c3cde640351551d0ce655545dc9069b8b19d61d1efcd9d59a1ef55a1 |

## Post-freeze comparison and results

The exact independently executed comparison is preserved as
[compare_frozen.py](compare_frozen.py), with its output at
[comparison01.json](comparison01.json). It ran first as the identical inline
Python recipe, exit0. It imports only the independent oracle, never root's
calculation or validator.

All12 case decisions agree. Every one of root's1980 input inequalities was
reconstructed from the independently transcribed input, including both
directions of every bound/difference, exact spans, labels and vertex/row joins.
All nine complete root witnesses pass the original constraints. All three
root negative cycles are closed chains with negative sums after independently
validating each constituent inequality. Six separate oracle chain
contradictions also pass the input-based certificate checker; a case may have
contradictions in both parity components.

| Point | Present positions | Supported velocities per clock | At30fps | At30000/1001fps | At2997/100fps |
|---|---:|---:|---|---|---|
| NE |16|14|Feasible|Feasible|Feasible|
| EC |43|41|Infeasible|Feasible|Feasible|
| WC |40|38|Infeasible|Feasible|Feasible|
| NW |70|68|Infeasible|Feasible|Feasible|

Total169 position variables and161 supported velocity constraints per clock.
NW source row1 remains unsupported at all three clocks. The nominal row-wise
failure counts reproduce0/1/5/5 for NE/EC/WC/NW; both alternative spans have
zero row-wise failures. Neither row count nor repeat calculation creates an
independent historical measurement.

Root's checked nominal-clock negative-cycle sums are −11/500,−23/500 and
−29/500 for EC/WC/NW. They need not equal the oracle's differently selected
chain contradictions: both certify the same infeasible input problems.
The oracle's exact open-interval pass finds all nine feasible cases strictly
feasible, so none requires a boundary-only solution. This does not mean
root's particular stored witnesses have no tight inequalities.

The comparison rechecked both oracle receipt inventories, all frozen
input/code/runtime/product identities, root pair identity and all18 captured
paths unchanged after comparison. An initial locator probe incorrectly
expected parent run01/results.json and returned file-not-found; the actual
parent outputs are run01.json/run02.json. No file was changed or missing-data
finding inferred from that locator error. Root's own controls are not claimed
as rerun by this reviewer.

## Interpretation limit

Under each fixed near30 clock hypothesis, display rounding is jointly
sufficient for the entire supported four-point derivative relation, not merely
for separate rows. Nominal30 is inconsistent for three points under the same
assumptions. This strengthens a concrete ordinary explanation for the small
derivative discrepancies; it does not identify the authors' actual hidden
positions, derivative settings, frame spacing or rounding policy.

These are conditional consistency witnesses, **not** recovered tracks,
independent acceleration estimates, calibrated uncertainties, camera
authentication, instantaneous support loss or a collapse-cause test.
The original98 fits and failed nominal row-wise comparisons are untouched.
No data, clock, source or acceptance criterion was tuned to obtain agreement.
No main/legal/accepted-engine state, acquisition, media or frozen root/oracle
result was altered.
