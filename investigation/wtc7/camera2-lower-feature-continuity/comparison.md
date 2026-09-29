# Complete frozen-observation comparison

2026-09-24. These are categorical comparisons of two prior-informed AI
readings of the same17images, not accuracy scores or independent capture
evidence. Both complete original tables remain unchanged.

- Root68rows SHA256:
  `87b63db5bac9008431c16b102422f7102cb84e1b71759379f7ceaf935cc88128`.
- Observer68rows SHA256:
  `97e9f2f6a01c0e0a35b08ba4fc274710a7b62d81a2dac7ae1db4131eabd7eb8d`.

Each cell gives **root / observer**, concatenating visibility and correspondence.
V/A/U retain the protocol definitions. Second letters: C=appearance-consistent,
Q=uncertain, X=changed, N=not-assessable. No category was recoded to make the
readers agree. All68frame-target pairs appear below, including every failure.

| Frame | NE | EC | WC | NW |
|---|---|---|---|---|
| 6593 | AQ/AQ | AQ/AQ | VC/VC | VC/VC |
| 6654 | AQ/AQ | AQ/AQ | VC/VC | VC/VC |
| 6751 | AQ/AQ | VQ/AQ | VC/VC | VC/VC |
| 6841 | AQ/AQ | VC/VC | VC/VC | VC/VC |
| 6886 | VQ/AQ | VC/VC | VC/VC | VC/VC |
| 6916 | VC/VQ | VC/VC | VC/VC | VC/VC |
| 6931 | VC/VQ | VQ/AQ | VC/VC | VC/VC |
| 6946 | VC/VQ | AQ/AX | VQ/VQ | VC/VC |
| 6961 | AQ/AQ | UN/AX | AQ/AX | VC/VC |
| 6976 | AQ/AQ | UN/AX | UN/AX | VC/VC |
| 6991 | AQ/AQ | UN/AX | UN/AX | VC/VC |
| 7006 | UN/UN | UN/UN | UN/AX | VC/VC |
| 7021 | UN/UN | UN/UN | UN/AX | VC/VC |
| 7036 | UN/UN | UN/UN | UN/AX | VC/VC |
| 7051 | UN/UN | UN/UN | UN/AX | VC/VQ |
| 7081 | UN/UN | UN/UN | UN/UN | UN/UN |
| 7104 | UN/UN | UN/UN | UN/UN | UN/UN |

Visibility matches in56of68pairs; correspondence in53; both fields in50.
The18pairs differing in at least one field are retained above, not resolved
by vote. Root counted the tables programmatically; a separate read-only parser
then reproduced all68 keys, all18 differing pairs, all strict counts and
every common-positive list. Neither parser changed the frozen source tables.

| Target | Root V/A/U counts | Observer V/A/U counts | Both V | Both V and appearance-consistent |
|---|---|---|---|---|
| NE | 4/7/6 | 3/8/6 | 6916,6931,6946 | None |
| EC | 5/3/9 | 3/8/6 | 6841,6886,6916 | 6841,6886,6916 |
| WC | 8/1/8 | 8/7/2 | 6593,6654,6751,6841,6886,6916,6931,6946 | Same list except6946 |
| NW | 15/0/2 | 15/0/2 | All selected through7051 | All selected through7036 |

## Disagreement is not one thing

Three visibility disagreements concern a borderline positive: EC6751, NE6886,
EC6931. The other nine visibility disagreements are U versus A on later
central targets: root regarded the defined junction as unavailable; the
observer recorded the visible surrounding roof region with changed silhouette.
Both exclude a distinct V candidate at those pairs, but that common limited
statement does not erase their original different labels.

The contract leaves some overlap between "visible region, ambiguous junction"
and "no candidate of the defined appearance distinguishable." A later schema
should separate host-region visibility, landmark localization and appearance
change. Do not retroactively normalize these records into artificial agreement.
The correspondence differences also retain substantive caution: the observer
does not accept the short NE positive run as appearance-consistent, and treats
the last NW positive at7051 as uncertain because of overlap. Root's more
permissive judgments do not resolve those limitations.

Common positive judgments are not proof of material-point identity, physical
continuity between samples, precise onset or cause. Common negative judgments
are not proof of destruction or absence of another usable observable.
