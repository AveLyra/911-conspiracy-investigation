# Independent synthetic geometry oracle

September 20, 2026. Reviewer: `next_discriminator`. This initial record was
written before reading root's geometry implementation or numerical output.
Inputs were the complete `MATH-PROTOCOL.md`, applicable main controls/full
charter, and the reviewer's own code. No source image, reading note, historical
measurement or producer implementation was consulted to generate the oracle.

## Method and fixed scope

`independent-math.py` uses standard-library `Fraction` arithmetic throughout.
For each of the six declared inverse fixtures it constructs all four corners
of the residual rectangle, solves each two-by-two system by pivoted
Gauss-Jordan elimination, and takes coordinate minima/maxima over the solved
vertices. A nonsingular linear map sends this rectangle to a parallelogram;
a linear coordinate reaches its extrema at its vertices. No closed-form
interval-radius formula is imported or used.

Zero horizontal displacement is tested by mapping `(0,0)` forward and checking
both residual bounds. Separately, existence of a point with north component
zero is tested against the vertex-derived north interval. When feasible, the
code constructs an exact rational witness by interpolating the minimum- and
maximum-north vertices and checks both original residual inequalities. These
two propositions are not interchangeable.

The pinhole calculation covers exactly the protocol's nine points and two
cameras: 18 projections. It checks right/forward axis normalization and
orthogonality, positive depth, `image_horizontal * depth = signed plane
distance`, and constant horizontal projection/depth over the three prescribed
heights at each of the three horizontal locations. Paired recovered distances
also recover the declared horizontal point. No additional geometry sweep or
historical fitting was performed.

## Frozen results

All quantities below are exact arbitrary synthetic units, not WTC 7 metres
or image pixels. Case ordering is exactly the protocol's ordering.

| Case | East interval | North interval | `(0,0)` feasible | Any north=0 feasible |
|---|---|---|---|---|
| 1 | `[-1/5, 1/5]` | `[8/5, 12/5]` | No | No |
| 2 | `[-1/5, 1/5]` | `[7/5, 13/5]` | No | No |
| 3 | `[-1/5, 1/5]` | `[1, 3]` | No | No |
| 4 | `[-1/5, 1/5]` | `[0, 4]` | No | Yes |
| 5 | `[-1/5, 1/5]` | `[-18, 22]` | Yes | Yes |
| 6 | `[9/5, 11/5]` | `[-161/50, -139/50]` | No | No |

Case 4's exact north-zero witness is `(1/5,0)`; it is not the zero vector.
The 24 vertices, center forward/inverse identities and complete 18 projection
rows are preserved in `independent-math01.json`.

Declared controls passed: singular identical normals reject unique inversion;
a negative error rejects; zero-width errors return the exact point in all
six existing fixtures. All six camera/horizontal-location invariance groups,
six original-edge zero-horizontal projections, 18 plane-distance recoveries,
and nine paired inverse recoveries pass. These are checks on shared synthetic
fixtures, not independent historical observations.

## Actual execution and preserved failure

Command, with cwd this unit:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B independent-math.py
```

First invocation: exit 1, `PermissionError: [Errno 1] Operation not permitted`
at `OUTPUT.open('x')` for the authorized result path in the research worktree.
No result file was created. The failure occurred after the calculation reached
its create-only write, but no first-run result artifact is claimed.

Second invocation: same command and **unchanged code**, with scoped write
permission for that one authorized output. Exit 0; six inverse cases, 24
vertices, 18 projections, controls passed. Python 3.13.7; no package installation
or network. The output is create-only, and source/code pins match before and
after the calculation. A subsequent read parsed all saved case/projection rows
and freshly hashed the three listed files. There was no independent human or
licensed-engineer validation of this code.

Frozen pins:

- `MATH-PROTOCOL.md`: 3,807 bytes, SHA-256
  `58d49fe3d792b34ce323882b2f10f97d2e5500cfe62666b9a83005e7645828f2`.
- `independent-math.py`: 9,052 bytes, SHA-256
  `6235e4e34885770666640b95fa8d043b661dbb1dee091846a336cce1d1ad0d97`.
- `independent-math01.json`: 19,251 bytes, SHA-256
  `6df36e503f0c038e3a4f7870eb55be6abd09bdf3193f3f64571af4a2de6c185d`.

## Interpretation ceiling and exchange status

The synthetic cases demonstrate conditioning dependence under **known**
normals and fixed, independently bounded residual errors. Their rectangles
are permitted sets, not stochastic confidence intervals. The pinhole
invariance is checked for the specified ideal axes; it does not supply a
historical camera pose, image registration, depth, lens correction or error
budget. The oracle neither recovers NIST's formula nor validates or refutes
its reported 11 m +/- 3 m. It does not determine real lateral displacement,
feature identity, timing, calibration, support loss or collapse cause.

Strongest objection to promoting this result: exact arithmetic can faithfully
solve an assumed inverse problem whose normals, residual distances or common
point/time joins have not been established for the historical recordings.
No cross-implementation comparison is claimed in this initial frozen record.
Any later comparison belongs in an explicitly post-freeze section, preserving
the oracle code, JSON and this initial account.

## Post-freeze exchange and exact comparison

Exchange was expressly permitted after both numerical outputs were frozen.
The initial 5,479-byte version of this review had SHA-256
`970d87caa250640744b0fe011e70be37124ea25304ffc47f975b0097c26a1960`.
This section is appended; the initial account and frozen oracle code/JSON
remain unchanged.

Root's inspected frozen artifacts:

- `geometry.py`: 5,593 bytes, SHA-256
  `526dd122642561b792e097df56bf3c46955f504820419fbac8d02b86f27c06ed`.
- `math01.json`: 9,233 bytes, SHA-256
  `1ad3d659f3a65fb8fe68787de29a0e27e1d315ce71b592fc2751a564606a8aea`.

**Comparison passes exactly.** A read-only inline command under the same
explicit Python 3.13.7 (`PYTHONDONTWRITEBYTECODE=1 .../python3 -B -`) exited 0
after these checks:

1. Rehash both implementations, both result files, the protocol and initial
   review; match the communicated freezes. Verify root's input pin sets are
   equal and match actual bytes, including its Python executable. Verify the
   oracle's own before/after protocol/code pins similarly.
2. Compare all six common cases by declared order: normals, true displacement,
   error bounds, central residuals, recovered center, both coordinate
   intervals, and both distinct zero-feasibility predicates. Independently
   obtain root's saved radii as half of each four-vertex interval width and
   its centers as the interval midpoints. Check every one of the oracle's
   24 solved vertices against the corresponding saved bounds. All agree.
3. Key projections by camera ID and complete three-coordinate point, not
   row order. Require precisely 18 unique matching keys; compare horizontal
   and vertical image coordinates, depth and signed plane distance. Check
   the independent recovered distance and `horizontal * depth` again.
   All 18 complete projection rows agree exactly. The producer's camera
   constants were also read and match the protocol/oracle.
4. Read both control implementations and compare their common required
   outcomes. Both reject singular inversion and negative error bounds and
   recover zero-width points for all six fixtures. Their chosen negative-error
   control values differ (root `(-1,0)` at zero residual; oracle
   `(-1/5,1/5)` at the first fixture's central residual), but both test the
   same protocol requirement; no identity of those control inputs is claimed.
5. Import each implementation only after exchange; replay `calculate()`
   without calling its writer. Normalize through its own Fraction encoder
   and compare the entire returned result object with its saved result
   fields. Both complete calculations reproduce exactly.
6. Invoke both scripts against their already-existing outputs. Each returns
   exit 1 with the expected `FileExistsError`, before overwriting anything.
   Rehash every frozen artifact above after the comparisons/replays/guards;
   all remain unchanged. These expected refusal controls are distinct from
   the original sandbox permission failure.

No disagreement or substantive numerical defect was found. The methods differ
where intended: root uses inverse-matrix absolute-coefficient radii; the
oracle uses four solved vertices. The producer correctly avoids treating the
coordinate bounding box as if every combination inside it were jointly
feasible. Case 4's east and north intervals separately include zero while
the zero vector is infeasible; its direct residual-space test handles this.

The complete `report.md` was read for its mathematical interpretation ceiling;
SHA-256 at that reading/check:
`644f64a01d37a87181f84c674205551cb4ff7c83fbfc3b5e84060006f6aae67f`.
Its synthetic interval table and distinction between zero north and the zero
vector agree with the independent oracle. Its statement that missing
historical bounds do not automatically admit zero is appropriate. The report
does not turn the synthetic near-parallel cases into claimed real camera
angles or claim reproduction of 11 m +/- 3 m. No material overclaim was found
within this numerical review's remit.

The report's primary-page observations and attributed directional evidence
are **not independently verified by this oracle review**: the reviewer did
not view those pages or any historical frames. The projected-edge principle
and constant-horizontal-coordinate tests retain their stated ideal geometry
and registration assumptions; these executions do not establish real lens,
pose or processing behavior. Shared protocol inputs and two agreeing programs
provide computational cross-checks, not independent historical evidence,
measurement uncertainty, expert approval or a cause determination.
