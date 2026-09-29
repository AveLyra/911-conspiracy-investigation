# Joint-consistency execution and verification

September20,2026 UTC. All work is in this dedicated research worktree,
HEAD e8d83d7. Prior printed-table outputs and source bytes remain unchanged.
No new historical video, source transcription, solver installation or engine
state was used. The [protocol](PROTOCOL.md) preceded joint calculations.

## Root implementation and controls

`calculate.py` constructs exact rational difference constraints, one variable
per present position cell plus a translating anchor. Position bounds and
centered-velocity bounds become directed inequalities. Bellman-Ford either
returns positions satisfying all inequalities or a negative cycle. The separate
certificate checker verifies every edge or sums the contradictory cycle without
rerunning that algorithm. This is numerical consistency checking, not a
structural collapse solver.

Actual pre-historical command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_calculate
```

First run: six test methods passed and the missing-value fixture failed. The
fixture wrongly expected removing a position to invalidate another velocity
when its only affected interior velocity was already blank. The actual two
remaining constraints were correct. The expected count was corrected to two,
and an additional missing neighbor was tested to remove both. Calculation code
and historical data were not changed. Second run: **all seven methods passed**.
The methods include constant/linear histories, translation, exact-boundary and
beyond-bound cases, individually feasible but jointly inconsistent rows,
disconnected/missing constraints, malformed input and corrupted certificates.

Only after the controls passed, root executed these commands separately:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B calculate.py --output run01.json
PYTHONDONTWRITEBYTECODE=1 python3 -B calculate.py --output run02.json
cmp run01.json run02.json
```

Both returned exit0 with12 cases; `cmp` returned exit0. Both output SHA-256:
`1ef82cb48b3b688b35acafed4458873657eaf9d237678508b0d9ba7cb23fd86c`.
Code SHA-256:
`92c729a5c3cde640351551d0ce655545dc9069b8b19d61d1efcd9d59a1ef55a1`.
Protocol SHA-256:
`4ed21c2fae4d36869588130321767134d72539fb618f47168e6c6170026300c0`.
All were communicated as pins/coverage only before independent findings were
exchanged. Inputs and protocol/code identities are also embedded in each run.

Root's separate inline Fraction check mapped the saved witness vertices
directly to the original table rows, not through saved edge bounds. All690
position/velocity interval checks across the nine feasible cases passed.
A subprocess invocation targeting the existing run01 returned the expected
FileExistsError/exit1 before historical calculation; its hash remained unchanged.
The three infeasible cases retain explicit original-edge negative cycles.

## Input and interpretation boundaries

All70 page47 rows and11 selected columns match the separate frozen
transcription after its explicit field-name mapping. Source PDF SHA-256 remains
`cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394`.
This unit rehashes that PDF; it does not repeat its earlier page inspection.
Root/independent transcription pins are checked before and after calculation.

The12 cases contain169 position cells and161 supported velocity constraints
per clock, or1,980 directed inequalities overall. The first northwest velocity
has no preceding printed position and stays unsupported at all three clocks.
Present position cells are shared between overlapping derivative constraints;
blank cells are never zero-filled. No original fit is recalculated or rescaled.

Feasibility uses closed display envelopes, not a specified rounding tie rule.
Some root witnesses touch interval boundaries because of the algorithm's
construction; that alone does not show boundary-only feasibility. Actual
tracking, frame selection, clock and smoothing remain unauthenticated.
Independent implementation/review results are recorded separately once frozen;
root's own checks must not be mislabeled independent source evidence.

## Post-freeze independent checks

The interval-chain implementation froze two198,904-byte result files with
identical SHA-256
`9774f906fe3fc3f3f6fcd7462bd4b454acdfaee0e05a33c6cf3e0903964492a7`
before inspecting root's results. Its18 control groups passed before loading
historical input. Its first control invocation reached a create-only fixture
and was denied permission to create that temporary directory in the worktree;
scoped escalation resolved that environment failure without changing code.
No historical run preceded the successful controls.

The independent reviewer reconstructed all1,980 root inequalities directly
from its separately transcribed inputs, checked all nine root witnesses and
all three negative cycles, and reconciled all12 case outcomes, counts and the
one unsupported row per clock. Its own chains provide six independently checked
contradictions across the three infeasible cases. Different valid certificates
need not select the same inequalities.

Root read the complete309-line interval implementation and124-line controls.
An actual read-only inline command imported that separate implementation,
reconciled its input, called `problem` and `solve` for each saved case, normalized
exact fractions through JSON, and compared every returned result field with
its frozen case. All12 complete case objects reproduced, exit0; no files or
new media were written by this rerun. The exact open-interval calculation finds
all nine feasible cases strictly feasible, not forced to rounding boundaries.

A third computational reader independently rebuilt all1,980 inequalities,
checked1,380 witness edges and20 negative-cycle edges, freshly reran the seven
root test methods, and tested strict feasibility by a separate exact integer
all-pairs closure. It reported no zero-weight cycle in any feasible case,
consistent with the interval result. These are independent implementations/
checks on shared printed data, not independent instruments or human experts.
