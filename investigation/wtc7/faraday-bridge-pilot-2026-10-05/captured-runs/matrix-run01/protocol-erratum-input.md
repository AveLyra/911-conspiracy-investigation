# Faraday bridge protocol hash correction

October 5, 2026. Recorded before any native test or custom matrix execution.
This note corrects one transcription error, not the protocol's scope, scoring,
isolation boundaries or acceptance criteria.

The preserved [original protocol](PROTOCOL.md), SHA-256
`d6b9a077c97dc2b207a587739f7e697f1b94c055bedee1f7a536c022da2569da`,
prints a 62-character schema digest:
`10400ded1ce9cb771197c4e63eb56d8b122798af9f6c6dfb020c24c2b9f662`.
That string is invalid as a SHA-256 digest and must not be used as a source pin.

The harness author identified the discrepancy during read-only preparation.
Root independently ran `shasum -a 256 schemas/sherlock-bridge-link.schema.json`
in the unchanged Faraday checkout. The correct 64-character value is:

`10400ded1ce9cb771197c4e63eb56d8b122798af9f6c6c6dfb020c24c2b9f662`.

It agrees with the separately saved [source review](source-review.md).
Faraday remains clean at commit `26ab7c96228b3c7ddcec0539f187d104ba49b47b`.
The reviewed harness must pin both the unchanged protocol and this erratum,
and use the corrected schema digest. No source/schema change, target test,
failed historical result, or post-result scoring change motivated this correction.
This pre-execution correction does not consume the declared post-execution
harness-only repair allowance.
