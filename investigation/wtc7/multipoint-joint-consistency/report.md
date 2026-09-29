# The published motion table is jointly consistent under the two near-30-fps clocks

September20,2026 UTC. Working research; no new video measurement, physical
calibration or collapse-cause finding.

**One complete hidden-precision position history can satisfy all supported
published velocities simultaneously under either previously declared near-30-fps
clock hypothesis.** Exact30fps cannot do so for three of the four roof points.
Two independently implemented exact calculations agree on all12 cases.

This closes a real limitation in the [earlier row-wise calculation](../multipoint-table-reproduction/report.md):
making each row separately compatible did not prove that overlapping rows could
share the same position values. The new test requires precisely that shared
consistency. It strengthens a clock-plus-display-rounding explanation for
these discrepancies, without identifying the authors' actual method.

## Fixed test and results

Inputs are the two previously reconciled page47 transcriptions of the held
Chandler/Walter/Szamboti2023 paper. This unit verified their hashes and all70
rows/11 selected columns; it did not independently reobserve historical motion.
The [prospective protocol](PROTOCOL.md) fixed all assumptions before calculation.

Each printed position and velocity receives its original closed ±0.005 display
interval. One variable per position is reused by every applicable derivative.
The velocity is constrained to `(following position − preceding position)/span`.
Spans correspond to twelve frames at the three previously selected rates; no
clock was fitted or tuned here. Six-frame sampling remains a source-motivated
hypothesis, not an authenticated frame-to-table join.

| Roof point | Position cells / supported velocities | Exact30fps | 30000/1001fps | 2997/100fps |
|---|---:|---|---|---|
| Northeast | 16 / 14 | Feasible | Feasible | Feasible |
| East-center | 43 / 41 | Infeasible | Feasible | Feasible |
| West-center | 40 / 38 | Infeasible | Feasible | Feasible |
| Northwest | 70 / 68 | Infeasible | Feasible | Feasible |

There are169 position variables and161 supported velocity constraints per
clock. The first northwest velocity remains untestable because its preceding
position is not printed. No blank was filled or constraint removed to obtain
agreement. These are twelve mathematical cases on one source table, not
twelve independent recordings or physical experiments.

For feasible cases, the saved outputs provide a complete position witness
checked against every original display/derivative interval. For each infeasible
case, valid input inequalities sum to an explicit contradiction. Root's three
nominal-clock certificates yield `0 ≤ −11/500`, `0 ≤ −23/500` and
`0 ≤ −29/500` in assigned position units for EC/WC/NW respectively. Those are
certificate margins, not measured displacement errors or physical uncertainty.

The separate interval-chain implementation also finds strictly interior
feasibility in all nine feasible cases. Thus their compatibility is not
dependent solely on allowing exact rounding ties. Some particular root
witnesses touch bounds because of their construction; that is not proof that
all solutions must do so. Actual historical rounding/settings remain unknown.

## Verification and independence

Root used exact rational graph inequalities; the independent reviewer used
forward interval reachability and backward witness construction along the
disjoint sample chains, using the separately transcribed table. Both froze two
byte-identical result runs before exchanging findings. Root then reread the
independent code and reproduced every complete case result with that method.
Seven root test methods and18 oracle control groups passed before their
historical calculations, including individually compatible but jointly
inconsistent synthetic rows. A root fixture error and an oracle sandbox-write
failure are retained in [execution](execution.md), not represented as clean
first attempts. No data or clock choice was changed in response to results.

Root outputs: [run01](run01.json), [run02](run02.json), SHA-256
`1ef82cb48b3b688b35acafed4458873657eaf9d237678508b0d9ba7cb23fd86c`.
Independent outputs: [run01](oracle/run01/results.json),
[run02](oracle/run02/results.json), SHA-256
`9774f906fe3fc3f3f6fcd7462bd4b454acdfaee0e05a33c6cf3e0903964492a7`.
Same-method repeats and cross-method agreement are separate checks. All
implementations still share the published evidence and declared assumptions;
this is not independent camera evidence or licensed forensic review.

## What this changes—and does not

The earlier objection—“each row works individually, but perhaps no shared
position history works”—is now answered for these fixed hypotheses. It would
be inaccurate to retain that objection as an unperformed test or to use these
particular residuals as affirmative evidence of fabricated velocities.

The strongest remaining objection is that an internally consistent table can
still inherit tracking, scale, projection, timing or processing errors. Neither
feasibility nor agreement between programs authenticates those inputs. Different
underlying methods may produce the same rounded table. Original project/export
settings and a defensible source-frame relationship are still needed to identify
the historical method. No exact acceleration label, fit mask, all-support-loss
time, force history or initiating mechanism was newly established here.

The [causal-chain assessment](../causal-chain-synthesis/report.md) therefore
does not change its lack of an independently earned strict probability ordering.
This is a completed methodological follow-through to the bounded Luna review,
not clearance of every Luna artifact or completion of the charter. Earlier
nominal-clock failures, fits, transcriptions and all source bytes remain intact.
