# Independent critical review: shared-position consistency

September 20, 2026. Reviewer: `next_discriminator`. Research-only, bounded
arithmetic/code review; no new media, network calls, source transcription,
structural solver, or cause ranking. This is the reviewer's sole new file.

## Finding and scope

**Scoped pass.** The saved feasible witnesses and negative-cycle certificates
are correct for the declared table, three fixed clocks, centered-difference
rule, and display envelopes. Independently reconstructed constraints require
one shared position value wherever a printed position participates in more
than one derivative. They do not accidentally permit a different position for
each velocity row. No material logic error was found in the producer or its
current seven test methods.

This review used the separately frozen transcription as its mathematical input
and reconciled it against the root transcription. It did not import
`calculate.py` for either independent historical check. Running that module's
synthetic tests is a separate, explicitly identified check below. No findings
were sent to the separate interval-chain reviewer before its freeze. The
interval-chain implementation/results were not independently executed here.

## Exact inputs and pins

Paths below are relative to this directory. SHA-256 values were freshly checked;
the producer's saved input pins also matched current bytes.

| Input/artifact | SHA-256 |
|---|---|
| `PROTOCOL.md` | `4ed21c2fae4d36869588130321767134d72539fb618f47168e6c6170026300c0` |
| `calculate.py` | `92c729a5c3cde640351551d0ce655545dc9069b8b19d61d1efcd9d59a1ef55a1` |
| `test_calculate.py` | `7447f3e0a17a20687527e863e612951b8d94ffcc9747a77a787061b495a7a4a0` |
| `run01.json` and `run02.json` | `1ef82cb48b3b688b35acafed4458873657eaf9d237678508b0d9ba7cb23fd86c` |
| `../multipoint-table-reproduction/transcription-root/table47.json` | `a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc` |
| `../multipoint-table-reproduction/transcription-independent/table47.json` | `fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8` |
| `../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf` | `cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394` |

The PDF was rehashed, not newly read or visually transcribed. The accepted
page-47 transcriptions and earlier source inspection remain the evidence join.
All 70 row IDs, their nominal one-fifth-second grid, and 11 selected fields
(770 cells) matched between transcriptions under the documented field mapping.

## Commands actually run and results

In this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_calculate.py
```

Exit 0: **7 test methods passed**. These cover boundary/beyond-bound cases;
constant/linear/translated histories; corrupted certificates; derivative
construction and missing cells; disconnected/empty constraints; individually
feasible but jointly impossible rows; and malformed input. The current
missing-neighbor expectations are logically correct. The earlier failing
fixture/correction history described in `execution.md` is root-reported; this
review did not inspect that superseded test version or rerun its failure.

Two additional commands used `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'` with
inline standard-library-only code. Both exited 0, created no files, and did
not import the producer. The following exact mathematical recipes describe
those checks; the ephemeral inline scripts are not claimed as saved artifacts.

### 1. Independent source-derived certificate verification

1. Load both transcriptions, reconcile the 770 cells, and use the independent
   table to construct every constraint. Parse printed decimal strings as exact
   `Fraction` values. Set `e = 1/200`; obtain the centered span as
   `12 / Fraction(clock)` for each of `30`, `30000/1001`, and `2997/100`.
2. For every present position `y_i`, independently form
   `x_i - x_0 <= y_i + e` and `x_0 - x_i <= -y_i + e`.
   For each printed velocity with both neighboring positions present, form
   `x_next - x_previous <= span*(v_i + e)` and
   `x_previous - x_next <= span*(-v_i + e)`.
   Join neighbors by the nominal sample grid, preserve nulls, and identify
   variables/edges by original row ID rather than trusting saved bounds.
3. Require exactly the 12 declared clock/point cases. Compare all saved edges,
   labels, vertex-to-row mappings and exact bounds with this reconstruction.
   Check feasible positions directly against the original position and velocity
   intervals. For each infeasible certificate, map its labels back to the
   reconstructed inequalities, check adjacency, cancel all variable
   coefficients, and add its exact bounds. Check reported counts and tight
   edges. Require the two output files to be byte-identical and their saved
   source/code/protocol pins to match current bytes.

**Results:** all **1,980** reconstructed directed inequalities match;
**1,380** witness inequalities pass across nine feasible cases; **20** cycle
edges pass across three infeasible cases. There are 483 supported derivative
instances across the three clocks. The first NW velocity remains unsupported
in each clock case. Per clock the position/velocity counts are NE 16/14,
EC 43/41, WC 40/38, NW 70/68.

NE is feasible under all three clocks. EC/WC/NW are infeasible at exact 30 fps
and feasible under both declared noninteger clocks. The nominal-clock
certificates, directly verified from the source-derived inequalities, are:

| Case | Edge labels in saved cycle order | Exact sum |
|---|---|---|
| EC | `velocity:55:lower`, `position:54:lower`, `position:60:upper`, `velocity:59:lower`, `velocity:57:lower` | `-11/500` |
| WC | `velocity:64:lower`, `velocity:62:lower`, `velocity:60:lower`, `position:59:lower`, `position:69:upper`, `velocity:68:lower`, `velocity:66:lower` | `-23/500` |
| NW | `velocity:64:lower`, `velocity:62:lower`, `velocity:60:lower`, `velocity:58:lower`, `position:57:lower`, `position:69:upper`, `velocity:68:lower`, `velocity:66:lower` | `-29/500` |

Each cancels to `0 <=` a negative number. These are exact mathematical
contradictions under the stated assumptions, not physical error bars.

### 2. Separate strict-interior check

Reconstruct the inequalities again from the independent transcription. For
each case, multiply all edge bounds by their common denominator `L` to obtain
integer weights. Initialize an all-pairs distance matrix with zero diagonal,
the minimum weight for any parallel edges, and infinity elsewhere; perform
the ordinary Floyd-Warshall recurrence. Check diagonal negativity and, in
each feasible case, whether any original edge `u -> v` of weight `w` has
`w + distance[v][u] == 0`.

All nine feasible cases have **no zero-weight cycle**. This proves strict
interior feasibility, not just an observation about one witness: every simple
cycle has positive integer sum, at least 1, and at most `n` edges. Subtracting
`1/[L*(n+1)]` from every original rational edge bound leaves every simple cycle
positive, so the tightened system remains feasible. All original position and
velocity envelopes can therefore hold strictly. This independently supports
the report's rounding-tie qualification. `witness_tight_edges` counts bounds
hit by a particular returned witness; it does **not** diagnose necessity of
rounding ties. The constructed slack is not a measured physical margin.

## Producer logic and final wording

The producer's direction/sign conventions match the inequalities above.
Initializing all Bellman-Ford distances to zero is equivalent to an implicit
zero-edge supersource; subtracting the anchor value preserves every
difference. An update on the nth relaxation pass, followed by n predecessor
steps, locates a negative cycle. The independent direct verification above
does not rely on that algorithm being correct to establish the saved results.
The producer's source pins, before/after checks and create-only output handling
fit this bounded workflow. This is not a general hostile-input/security audit.

The new `report.md` and `execution.md` were read completely after calculations
and freezes. No material overclaim was found in their characterization of this
review or the arithmetic conclusion. Their hashes at review were respectively
`69cc2d2cac30c25237b93bddada468eefd22f6ad45afe292aa542980cb4721b1`
and `150bcd8ea154ed1f73f2a934868d88c72609c7da2a718491ff2535e03d992044`.
Other reviewers' execution/history statements remain attributed, not newly
certified by this review. The conditional wording about clock-plus-rounding
compatibility is appropriate; it must not become identification of the actual
historical clock or processing method.

**Strongest limitation:** shared-position feasibility can establish internal
consistency while all positions remain affected by the same tracking,
projection, scale, sampling or processing error. The six-frame sampling join,
actual rounding, source clock and physical calibration are not authenticated
by these certificates. Neither this result nor exact-30 infeasibility decides
acceleration, force history, total support loss, authors' intent or collapse
cause. It does not clear all Luna work or complete the investigation charter.

## Separate HBI report textual check

`../comparator-hbi-client-followup/report.md` was read completely; SHA-256
`685e801bef0d63e4e47595ec3b2756ceb137e74ed435876c935adbebb0a9dbad`.
Its account of this reviewer's earlier eight official-document opens, including
two section reopens and the two checksum/signature unsafe-open refusals, is
accurate. It distinguishes the tagged README from the mutable EJS guide and
documents runtime requirements without claiming executed compatibility or
checksum/signature validation. Reading the public key did not validate a
release asset. Root's local runtime and temporary-client search checks remain
root-attributed, not freshly repeated here. The report properly separates a
failed/unexecuted acquisition route from absence of the recording or evidence.
No refusal was retried or routed around during this review.
