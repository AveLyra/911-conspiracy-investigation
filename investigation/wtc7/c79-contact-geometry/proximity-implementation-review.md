# Frozen proximity implementation and inference review

September 13, 2026. Research only. This is an independent code, mathematical
method and saved-representation review, not a second geometric implementation,
source rescan, solver run, engineering certification or cause ranking. The
separate numerical arm is responsible for independent distance reproduction.
No results from that arm were used to write the findings below.

## Scope and exact versions

Read the complete [protocol](PROTOCOL.md), [geometric method](GEOMETRIC-METHOD.md),
[implementation addendum](GEOMETRIC-IMPLEMENTATION-ADDENDUM.md), all 399 lines
of [proximity.py](proximity.py), its JSON receipt/schema/group summaries and
all 26 arrays' shapes/dtypes/content hashes. Re-read the preserved
[control-method review](control-method-review.md). Current main controls and
the development-verification/evidence-audit skills govern this review.
No new manual pages, source streams, held documents or solver states were read.

| Reviewed artifact | SHA-256 |
| --- | --- |
| PROTOCOL.md | b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea |
| GEOMETRIC-METHOD.md | 73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e |
| GEOMETRIC-IMPLEMENTATION-ADDENDUM.md | ada9f0cdfcb7d7dd3fd79d3c8cd6daf9f0a3f0937c6e7420f7c23dbd34fba9bd |
| proximity.py | 111f5e99646e05096838997d9aa4cddc0574d9767f784b860cb04dbcf52f0bb2 |
| proximity-root01.json | d2201fcd1f0c36f3240a32813b01ec1c8b90f44d019ac0cbb93ce54a99e5f6cc |
| proximity-root01.npz | b1557b12783c2a7caa7738c2537f941e45c79d3165c9a1385b1de472f29fbcca |
| independent-stage01.json, global-block comparison only | ead0f771054d3bfbe775a215aa7bc295c3c1e741e172b5201ad59816acfccccd |
| control-extraction01.json | dfcca53944ba6772dc65922d5c0083ae5bdec191950f8eb0157d79ffbb6deec8 |

The frozen producer pins stage-root01.json to
`deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963`
and stage-root01.npz to
`2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf`.
Those fixed dependencies, both method documents and the producer itself had
matching before/after hashes in the saved run and in this review's mutation
test. Full source extraction provenance remains in the prior stage; this
review does not replace it. Root02 and the independent proximity computation
are outside this review's arithmetic coverage.

## Implementation matches and mathematical checks

No blocking formula or coverage defect was identified for the fixed reviewed
inputs. This is not a generic approval for arbitrary new geometry.

- Lines 264–312 traverse every selected master record at all three declared
  settings against its complete slave population. There is no nearest-k,
  same-ID/part, orientation, elevation or architectural filter. Master order
  and duplicate records remain separate indices. Same-ID and same-part
  checks annotate rows after admission; they do not exclude them.
- Lines 278–285 require at least one master shell alias, reject multi-part
  alias ambiguity, aggregate the first four supplied thickness fields over
  all aliases, and retain original diagonals. Full alias/source/reference
  records remain traceable through the pinned stage JSON rather than being
  duplicated into every pair row. Lines 267–269 reject nonfinite coordinates,
  negative/nonfinite thickness and one-sided missing-thickness pairs.
- Lines 55–62 implement the declared bilinear parameter extension exactly.
  Lines 301–303 use the original shorter diagonal and unchanged supplied
  low/high thickness scenarios at every extension setting. No claim of an
  actual MAXPAR or effective initialized thickness is embedded in this code.
- The AABB test uses the extended corners and each node's high scenario,
  with the declared epsilon. Reparameterized bilinear weights are
  nonnegative over the selected square, so the patch image is inside that
  box. This proves the intended mathematical broad-phase containment, not
  a bound on all LS-DYNA contact behavior. Unknown thresholds always pass
  admission. All masks and later-outside admitted rows are saved.
- Point-to-triangle code checks projection into the three closed halfplanes
  and all closed edges. The dot with the plane normal makes the halfplane
  tests independent of the point's normal displacement. Reversing winding
  reverses signed distance without altering unsigned distance. Exact zero
  cross-product norm falls back to edges/vertices; no normal is invented.
- The mixed-corner enclosure is mathematically defensible for the declared
  geometric image sets. For the two diagonal triangulations, the difference
  from bilinear interpolation at corresponding parameters is the mixed
  corner vector times, respectively, `uv-min(u,v)` and
  `uv-max(0,u+v-1)`. Their absolute coefficients do not exceed 1/4 on the
  unit square. Combining each distance enclosure with max/min gives the
  stated L/U. It remains potentially loose and does not establish that a
  self-overlapping parameterization is a valid physical contact surface.
- The addendum's degenerate-plane NaN/-1 conventions are implemented.
  Nonfinite distance bounds and infinite/incompletely missing thresholds
  fail classification. Inversions exceeding epsilon fail; smaller known-
  thickness inversions retain original L/U and class2 rather than being
  clamped. Positive/negative orientation diagnostics are saved, not used
  to repair or discard faces. Cross norms preserve twice-area information;
  exact-zero-edge/area flags are recoverable from retained lengths/norms.
- Admitted-node incidence retains all frozen families/parts for those IDs,
  not just the master-associated part. Pair IDs, complete incidence and
  part-reference records permit the join without selecting a winning face.

## Actual saved representation checks

The NPZ was opened with `allow_pickle=False`. All 26 stored arrays match
their declared dtype, shape and C-order content SHA-256. These are integrity
and representation checks, not independent recomputation of the geometry.

The saved pairs have shape 11,292 by 6. Class counts across all settings are
8,520 unknown, 76 outside, 325 unresolved and 2,371 inside the low scenario.
The four no-shell/unknown nodes account for all 8,520 unknown rows:
4 nodes x 710 selected masters x 3 settings. Unknown threshold pairs and
class0 membership match exactly. Every distance bound is finite; no floating
array contains infinity. Degenerate-plane undefined fields agree with the
stored degeneracy state, although there are no exact-degenerate triangles
in this particular output, so real-data agreement is vacuous for that branch.

**All 325 class2 rows are the 325 small L>U numerical inversions.** There are
no non-inverted class2 rows in root01. The maximum inversion is
2.7755575615628914e-17 versus epsilon 9.4869e-9. The code correctly retains
them as unresolved, but they must not be reported as 325 affirmative cases
of thickness-sensitive or boundary geometry. Nor does this check justify
post hoc clamping or promotion to inside. The declared method intentionally
preserves floating uncertainty; it is not interval arithmetic.

For all settings, mask padding is zero and unpacked admitted counts match
the saved per-master coverage. Complete populations are 152,977 CID1 nodes
and 131,740 CID2 nodes. Nodes with no broad admission number 152,851 and
131,460 respectively at each setting. This is absence from this conditional
diagnostic, not absence of all possible contact/restraint. No zero edges,
exact-zero or near-zero triangles, or nonpositive corner-versus-center
Jacobian dots occur in the saved geometry arrays. That limited diagnostic
does not certify absence of every self-intersection or numerical pathology.

## Reporting corrections and nonblocking implementation limits

1. `multiple_candidate_master_nodes` at lines 335–342 counts classes2/3
   only. Unknown-thickness rows are excluded from that summary by design.
   Label it **known-thickness candidate multiplicity** and report unknowns
   separately. It is not multiplicity over all conceivable initialized
   pairs. Unknown rows remain recoverable; no source population is lost.
2. `zero_admission_masters=0` for CID1 follows automatically because each of
   the four unknown nodes is admitted to every master. It is not evidence
   that every master has a known geometrically near node. The output reports
   zero-master groups, but not zero-node groups in its JSON; the masks retain
   those groups and the representation counts above make them explicit.
3. Class2 labels must disclose the actual inversion-only composition above.
   Changes in class3 counts across e do not by themselves demonstrate newly
   available physical connections. Small floating differences can move a
   pair into the preserved inversion category; theoretical domain nesting
   does not require monotonic counts under that conservative classification.
4. The addendum says small inversion implies class2 without explicitly
   qualifying unknown thickness. Code/test lines 143–145 and 221–222 give
   class0 precedence to unknown-thickness inversions. There is no such
   overlap in these frozen arrays, so the wording discrepancy changes no
   current row. Future documentation should state that precedence before
   a new evaluation, preserving both unknownness and inversion information.
5. Integrity-pinned prior extraction supplies several invariants that this
   consumer does not independently re-establish: min<=max thickness order,
   master coordinate/node-array consistency, expected roles/shapes and
   all source aliases. Generalized reuse should validate those explicitly.
   The code also does not globally reject every nonfinite geometric metadata
   field at serialization; observed arrays contain none beyond permitted
   NaNs. This is not a reason to invent an error in the fixed run.
6. The routine guard checks creation before the try block. Invalid output
   names/existing outputs stop without a retained failure JSON; calculation
   and pin failures inside the try do retain one. Therefore avoid the
   broader claim that every possible refusal produces a failure receipt.
   Exclusive output creation and input/output hashes are useful controls,
   not protection from every concurrent filesystem race or malicious change.

## Control coverage and actual consumer mutation test

The producer has 15 passing synthetic controls. They cover interior/edge/
vertex and reversed-winding distances, exact degeneracy, planar and warped
patches, extension, unknown/boundary gates, small/large inversions, a planar
unpruned broad-phase comparison, duplicate masks, geometry warnings,
create-only refusal and nonfinite rejection. Important scope distinctions:
the broad-phase fixture is planar, the duplicate fixture checks masks rather
than full duplicate alias/part output, and `sha(__file__) != 64 zeros` is not
a mutation-rejection test. No complete adversarial floating-error proof or
exhaustive self-intersection suite is claimed.

A separate consumer-level mutation test exercised the real unchanged
`main()` and `PINS`, redirecting only BASE to a temporary fixture directory.
Three unmodified pinned dependencies were read-only symlinks. A copied
GEOMETRIC-METHOD.md received one synthetic marker line. `np.load` was replaced
with a no-call sentinel, so an accidental geometry-array load would fail the
test visibly. All 15 controls ran and passed; main then exited1 with
`input_pin_mismatch`, retained its failure receipt and made no array-load
call or success output. All seven watched original code/method/stage/result
hashes were unchanged. This tests before-load mismatch rejection, not an
after-calculation mutation, raw-source change or operating-system race.

Preserved temporary artifacts are in
`/private/tmp/c79-proximity-review.ghL4ds/`:

| Artifact | SHA-256 |
| --- | --- |
| consumer_guard.py | eced58e8689b789a08aeafddf3fdf4582a7aff726fae2fb609d7f5db03a2f309 |
| consumer-guard-result.json | 40dfafb4f75d3d7fbfd437a4537d70dcee4aeb5faea8fdb28885bbcd035f8d15 |
| proximity-root91-failed.json | 620fe53d8f9740a7a73af4b05721ed83a923f5a80583aae6829b4ce247556abc |

The fixture's mutated method hash is
`0a5551acbfd9fda651e662abb6e0c28366a0da5fcbe367140841a0985746b3a4`.
It is not a replacement method or historical input. The guard script ran
with bundled Python3.12.14/NumPy2.3.5, `-B`, exit0; its nested expected
consumer failure was exit1. Temporary paths are not durable repository
storage; the exact setup, result and hashes are recorded here.

## Separately extracted global-control agreement

Compared only the stored CONTROL_CONTACT block in independent-stage01.json
against this reviewer's frozen control-extraction01.json, without another
raw-source pass. They agree exactly on source121, keyword line4, both card
lines5/6, eight positions per row and all 16 numeric values. Both contain
exactly one such block with two numeric cards. This is a second extraction
agreement for those common numeric/locator fields. It does not independently
verify this reader's lexical hashes, field-name mapping, keyword suppression,
EOF coverage or historical effective settings. The earlier method note's
statement that a second comparison had not yet occurred remains an accurate
historical record; this paragraph supplies the later bounded comparison.

## Strongest conclusions and counterevidence

The conditional diagnostic supplies a reproducible candidate-to-incidence
map with complete exclusions and ambiguity, rather than merely repeating
that information is missing. Its non-shared-ID/part candidates illustrate
why absence of a direct shared-node edge cannot alone establish absent tie
restraint. That is the strongest countercheck against an omitted-coupling
claim this work supports. Conversely, near geometry, a positive class3 gate
or an authored penalty-tie card does not establish solver-selected pairs,
directional stiffness, survival, force transfer or actual Column79 restraint.
The most consequential unresolved bridge remains effective thickness/search,
initialized pairing/projection and then the force/state/material history.

Neither a broad exclusion nor an inside classification demonstrates building
support failure or adequacy. No physical floor/member identity, measurement
units, historical solver defaults, NIST fidelity, collapse mechanism or
probability ranking is inferred here. All edits are limited to this review
and temporary synthetic-test artifacts; frozen outputs, original source,
main/legal files and the prior method extraction remain unchanged.
