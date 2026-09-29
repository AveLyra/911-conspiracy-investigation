# Exact joint-envelope diagnostic addendum

2026-09-12. Exploratory working research; producer review pending the parent's
independent arithmetic check. This supplements, and leaves unchanged, the
frozen interpretation-review.md and the earlier observations and fits.

All six declared scenarios admit one constant image-coordinate separation
within the envelopes at every included frame. An explicit exact witness is
retained for each scenario. This resolves the narrow open question of
simultaneous feasibility on these included samples. It is not a finding that
the historical separation was constant, the physical accelerations were
equal, the building was rigid, or any collapse mechanism was established.

## Declaration, implementation and execution

Read the complete JOINT-ENVELOPE-ADDENDUM.md before implementation. Its
declaration acknowledges prior-result familiarity and preliminary hand
inspection suggesting possible overlap. No historical blinding or independent
source evidence is claimed. No root joint calculation was consulted.

The evidence/source safeguards preserve these outputs as working derivatives.
The development-verification skill influenced the compact standard-library
implementation, explicit controls, frozen input pins and no-overwrite check.
No browser check applies to this local rational-arithmetic diagnostic.

The script uses fractions.Fraction throughout the feasibility and witness
arithmetic. Coordinate inputs, interval endpoints, constants and witness
positions are serialized as exact rational strings. Frame indices and counts
remain integers. Original observation notes/statuses and all source coordinate
fields are retained in result.json; no input coordinates were changed.

For each included frame it constructs the exact interval
[aL−bU,aU−bL], then intersects those intervals across all included frames.
Combined scenarios first intersect observers' A and B y boxes separately,
and reject an empty observer intersection before testing constant separation.
Unlocalizable pairs are omitted with observer/feature reasons; they receive
no replacement coordinate or witness. A nonempty intersection gets its exact
midpoint c. Each witness A is the midpoint of A_box intersected with c+B_box,
and witness B=A−c. The producer checks witness membership against every
applicable original observer box.

Executed from the isolated investigation worktree with Python 3.14.0:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/sherlock-wtc7-investigation/camera3-late-reannotation/joint_feasibility.py
```

A syntax check passed first. The first sandboxed execution stopped at the
attempt to create joint01 with a filesystem permission error, before creating
outputs or evaluating controls/case scenarios. The authorized escalated run
then completed with exit 0. Its receipt records identical before/after pins
for the five controlling inputs. Both JSON products match their receipt
byte counts and SHA-256 hashes.

An immediate second invocation returned exit 2 and exactly
`refused_existing_output`; all three joint01 file hashes were unchanged.
No output was deleted, replaced or rerun. Directory-creation denial occurs
before a receipt can be written; this run does not claim a universal durable
failure-receipt guarantee.

## Controls performed before evaluating the observed envelopes

All five control groups passed. Full fixture inputs, exact results and
expectations are retained in controls.json, including rejected cases.

| Group | Declared result checked |
|---|---|
| Feasible | Common constant interval [5,9], with an exact in-box witness. |
| Infeasible | Intersected lower/upper bounds [18,9], explicitly infeasible; no witness. |
| Touching bounds | Singleton common interval [6,6] is feasible; touching is not treated as empty. |
| Common translation | Per-frame shifts +3 and −7 applied to both A/B preserve the constant interval and c; each constructed A/B witness shifts accordingly. |
| Empty observer intersection | Separate fixtures with incompatible A boxes and incompatible B boxes both reject before the constant-separation test, with no witness. |

The controls test exact interval operations and these rejection paths. They
do not validate the physical coverage of the subjective envelopes or the
material identity of any image feature.

## Exact retained scenario results

All intervals below are inclusive and expressed in native vertical pixels.
Negative A−B means A's image y is smaller. Constructed constants/positions
are mathematical witnesses, explicitly not new observations or historical
reconstructions. They are not interpolated image frames.

| Scenario | Declared / included frames | Omitted frames | Feasible c interval | Witness c |
|---|---:|---|---|---|
| root_selected22 | 22 / 21 | 348 | [−31,−30] | −61/2 |
| root_late21 | 21 / 20 | 348 | [−32,−30] | −31 |
| independent_selected22 | 22 / 19 | 342,345,348 | [−32,−30] | −31 |
| independent_late21 | 21 / 18 | 342,345,348 | [−33,−30] | −63/2 |
| combined_selected22 | 22 / 19 | 342,345,348 | [−31,−30] | −61/2 |
| combined_late21 | 21 / 18 | 342,345,348 | [−33,−30] | −63/2 |

selected22 includes frame258 and all declared marks 288..348 in steps of 3;
late21 excludes frame258. Each of the 115 retained witness rows satisfies its
scenario's one c and every applicable original y envelope exactly. Repeated
frames across scenarios are alternative constructions, not new evidence.
No historical scenario had an empty per-frame observer intersection or an
empty common c interval.

The combined scenario uses only frames where both observers localize both
features. It therefore excludes 342/345 even though root alone supplied
labels there. This explains why the combined late interval [−33,−30] is wider
than root's late interval [−32,−30]: their coverage differs. Do not claim that
combining observers necessarily narrows these reported intervals, or that
combined feasibility includes root's two additional late labels.

## Interpretation and remaining limits

The earlier per-window zero inclusion did not demonstrate one jointly
feasible sequence. This new construction now supplies such a sequence on
each scenario's included samples, under the stronger constant-image-separation
constraint. Every A−B fit to a complete window wholly contained in that
particular witness would consequently have zero slope and zero curvature
in exact arithmetic. This is a property of the constructed countermodel;
it does not replace any earlier observed central coordinate or its fit.

Existence within the supplied Cartesian product of y intervals assigns no
likelihood, posterior probability, calibrated confidence or historical truth.
It neither proves that the intervals cover every source/measurement error
nor that all combinations allowed by them are physically realizable. The
witness may use placements differing from both observers' preferred central
labels. Frozen central-coordinate differences remain recorded.

Missing frames still impose no measured constraint and have no witness.
In particular, no scenario supplies a fully observed constant-separation
trajectory through all 21 late marks. There is no continuity, intervening-frame
behavior or physical interpolation assumption in this test.

B remains an Eulerian sample at fixed image column322, not an identified
material point. Constant A_y−B_y alone is not a physical rigid-body condition.
The diagnostic does not solve x movement, horizontal outline resampling,
rotation, depth, perspective, feature deformation or the historical clock.
It estimates no force, moving mass, hidden support timing, gravity match or
mechanism. Earlier R3 visual-preflight disagreement is unchanged and is not
used to alter these coordinate constraints.

The parent's independent check must still verify joins, original inputs,
omissions, intersections, c selection and every witness without importing
this producer. This producer report does not claim that check has passed.
The initial interpretation review remains preserved at SHA-256
`e72884193fa706e56263ef9c701f596d73cd9e19e628f78a41a90af99ed38d03`.

## Artifact pins

| Artifact | SHA-256 |
|---|---|
| JOINT-ENVELOPE-ADDENDUM.md | `d2db97115a3ded371ae5de073607aed0657f8e79c9053c05835b8f2378fd6679` |
| joint_feasibility.py | `14fc35b53ae975333c5d3ecc92e5e95265976c24a6c8cc1d796f586d30e0a070` |
| joint01/controls.json | `6e0a04c10f228f62c991bf06af42d9cb5a8344909f31714bf5e6af57373d8c6a` |
| joint01/result.json | `7e9b4466a1ccbefad226086efd9d66cfaa34d94378100581efb6dd05ad128668` |
| joint01/receipt.json | `ce7d510d44e0c05782aa29d6268c5c3557c89288f74906a8e2bef15c896fe2a2` |

Writes were confined to joint_feasibility.py, the three declared joint01 JSON
products and this addendum. Source records, observations, earlier outputs,
other worktrees and canonical case records were untouched. No external
transmission, publication, accepted finding or cause ranking occurred.
