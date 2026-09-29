# Conditional slave-to-master geometry diagnostic

September 13, 2026. Prospective for this calculation, after the first-stage
source extractions and exact comparison froze. [PROTOCOL.md](PROTOCOL.md)
and the charter control. This is a geometric candidate-to-part map, not an
LS-DYNA contact initializer, historical run reconstruction or restraint test.
No proximity-selected results were inspected to choose the following rules.

## Inputs and complete coverage

Use the frozen root stage01 or independently extracted stage01 arrays, their
registered schemas and SHA-256 pins. Use all CID1/NSET1 slave nodes against
each of the 710 selected SEG1 master records, and all CID2/SEG2 unique slave
nodes against each of the 32 selected SEG3 master records. Preserve master
record order, duplicate faces, all four ordered vertices, aliases, node IDs,
source lines, part/section/material references and every no-shell node.
Reusing these independently compared extractions is not a new raw-source pass.

No self-node, same-part, orientation, nearest-k, floor or coordinate-range
filter is permitted. Store a packed admission mask for every slave node and
master record at every parameter setting, including zero-candidate records.
Store all admitted rows, including rows later classified outside the gate.
The mask plus complete frozen population identifies every broad-phase exclusion.

## Source-inspired thresholds, not effective solver defaults

The admitted May 2007 Version 971 manual, physical pages 395 and 402–403,
describes a parametric face search and a tied-shell closeness expression.
It does not authenticate the executable or establish our reconstruction of
its projection, pair selection, effective thickness or initial state. The
exact source controls and their applicability remain in the separate review.

For each slave node use the minimum and maximum supplied corner thickness
over its incident shells. For each master use the minimum and maximum of
THIC1–4 over all matching shell aliases, excluding the fifth card field.
Let Dshort be the shorter of the two ORIGINAL ordered master diagonals.
Define two sensitivity thresholds in unchanged model coordinate units:

    delta_low  = max(0.60 * (slave_min + master_min), 0.05 * Dshort)
    delta_high = max(0.60 * (slave_max + master_max), 0.05 * Dshort)

These are chosen supplied-value scenarios, NOT proven lower/upper bounds on
effective LS-DYNA thickness or tie distance. Do not substitute zero for the
four no-shell nodes; retain them for every CID1 master with unknown thresholds
and an unresolved classification. Reject negative/nonfinite supplied
thickness or missing/multiple-master-alias handling not covered above.

## Face domains, distance and geometric bounds

For ordered corners P0,P1,P2,P3 define the bilinear patch

    Q(u,v) = (1-u)(1-v)P0 + u(1-v)P1 + uvP2 + (1-u)vP3.

Evaluate three declared domains: u,v in [-h,1+h], with
h=(e-1)/2 and e in {1.000, 1.006, 1.025}. Values above one are sensitivity
settings motivated by page395, not a finding of the effective MAXPAR for
either interface. No probability or preferred setting is assigned. Evaluate
the patch at each domain's four corners to obtain an extended quad. Keep
the original Dshort and original supplied thickness ranges at all settings;
this is explicitly NOT extrapolated solver thickness.

For each point calculate closest Euclidean distance to both triangle unions:
A=(012,023), B=(013,123) of that extended ordered quad. Point-to-triangle
distance is the minimum of the orthogonal plane projection when inside the
triangle and distances to its three closed edges. Exact zero-area triangles
reduce to edges/vertices. Preserve near-degeneracy flags instead of silently
repairing the face. There is no one-sided normal rejection.

For extended corners R0...R3, let w=norm(R0-R1+R2-R3)/4. The difference
between Q and either triangular parameterization is a scalar times this
mixed corner difference, with scalar magnitude at most 1/4 on the unit
parameter square. Their Hausdorff distance is consequently at most w,
including nonplanar or self-overlapping cases as geometric image sets.
Thus a bilinear-patch distance enclosure is

    L = max(0, dA-w, dB-w)
    U = min(dA+w, dB+w).

This is a mathematical geometric enclosure, not an uncertainty interval for
physical measurement. It can be loose even for a planar non-parallelogram.
Do not represent a self-overlapping or ill-conditioned patch as a physically
valid contact surface just because the image-set bound remains applicable.

The complete broad phase uses distance to the AABB of each extended quad's
corners, admitted when that lower bound <= delta_high + epsilon. A bilinear
patch lies inside this AABB because its reparameterized weights are nonnegative
on its selected domain. Unknown-thickness nodes are always admitted. This
exclusion is conservative only for THIS domain/threshold diagnostic; it
cannot exclude all possible solver ties. It introduces no arbitrary radius.

## Classification and diagnostics

Set epsilon = 1e-10 * max(1, maximum absolute coordinate in the complete
frozen selected-node array), identical for all settings. It is a numerical
boundary buffer, not observed precision, confidence or material tolerance.
It is not a certified floating-point error bound; calculated enclosures and
classifications are numerical diagnostics, not interval-arithmetic certificates.
Compare independent finite distances and bounds at absolute tolerance epsilon
and zero relative tolerance. IDs, masks and classifications must match exactly;
any mismatch, especially near a boundary, remains reported, not tuned away.

Classes: 0 unknown thickness; 1 outside when L > delta_high + epsilon;
3 inside the low-thickness gate when U < delta_low - epsilon; otherwise
2 unresolved/boundary-or-thickness-sensitive. Require L <= U + epsilon;
preserve any small floating inversion and never turn it into an exact bound.

Save dA,dB,L,U,delta_low,delta_high and four signed plane distances plus
four projection-inside flags for every admitted point. Save each master's
four triangle normals/areas, both diagonals, w and extended coordinates.
Flag exact zero edges/areas, and near-zero triangle cross-product norms
<=64*machine_epsilon*max(1, maximum squared edge length of that triangle).
Also retain pairwise normal dot products and center-Jacobian orientation
checks at all four parametric corners. Zero or reversing orientation is a
geometry warning, not automatic repair or exclusion. These flags do not
constitute an exhaustive self-intersection or solver-validity certification.

Join every admitted node to its complete frozen node/part/family incidence
and existing part references. Report per-CID/setting class counts, unique
nodes and parts, unknowns, zero groups, master ambiguity (multiple candidate
records per node), same-ID and same-part overlaps, and extension sensitivity.
Neither incident part numbers nor coordinate coincidence independently
identify a physical seat, floor, structural capacity or surviving load path.

## Verification and disposition

Before historical numeric evaluation, exercise interior, edge and vertex
distances; reversed winding; zero-area/zero-edge faces; warped and planar
non-parallelogram quads; extended-domain containment; a known point admitted
only after extension; thickness-sensitive and unknown gates; broad-phase
conservatism against an unpruned synthetic pass; duplicate masters; and
source-pin/create-only protections. Check the bilinear enclosure against
analytic planar cases and synthetic patch points with known zero distance.

Freeze independent code/results before root proximity-result access. Use
different numerical implementations with the same declared definitions, not
a second call to the root routine. Root runs twice and compares products;
the independent comparison covers all masks, admitted rows, distances,
classes, geometry flags and part joins, documenting normalization and any
unverified fields. Preserve failed code/results. No inference about actual
ties, changing restraint, column instability or cause follows from passing
arithmetic. The next physical discriminator is the mapping to actual
initialization and force/state histories, with precise missing records.
