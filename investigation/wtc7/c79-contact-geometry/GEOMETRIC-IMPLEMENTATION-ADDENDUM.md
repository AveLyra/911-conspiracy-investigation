# Pre-evaluation implementation clarification

September 13, 2026, before either proximity implementation's historical
numeric evaluation. The underlying method remains GEOMETRIC-METHOD.md,
SHA-256 `73ec992e3c22d981f5cc367a8799635897903aba1b709941ec1ad2aa20c17d9e`.
Independent mathematical review identified two representation rules requiring
explicit saved treatment, without changing the declared distance or gates:

- If 0 < L-U <= epsilon, preserve both values and assign class2. If L-U >
  epsilon, fail the calculation with a retained receipt. Never clamp the
  enclosure to conceal inversion.
- An exactly zero-area triangle has no unique plane normal or plane
  projection. Store undefined signed plane distances and unit normals as
  NaN with explicit schema meaning, and projection-inside as -1 (unknown),
  not zero/false. Nondegenerate projection flags are 0/1. Edge/vertex
  distances remain defined. Retain separate raw cross products/norms and
  degeneracy flags so a zero cross product is not an asserted unit normal.

These are pre-evaluation clarifications, not corrections chosen from a
historical result. The numerical epsilon is not a certified rounding bound.
