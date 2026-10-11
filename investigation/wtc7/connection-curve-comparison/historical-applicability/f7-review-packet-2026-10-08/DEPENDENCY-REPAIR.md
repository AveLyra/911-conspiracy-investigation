# Dependency closure repair before presentation

October 8, 2026. Candidate packet01/02 at SHA256
`ceadeebf040913d5654c20bce5d55dca5ae2b7e4d6612821818f67af6024fb1c`
are preserved but not released for human review. The original producer and
tests remain unchanged. Their 260 pins omit four transitive code dependencies
of the old independent packet receipt: its independent checker, checker tests,
envelope arithmetic and arithmetic tests. Root's explicit map-difference check
(`eb79ce`) identified these four omissions before a viewer was released.
This narrows the earlier integrity check: every listed pin matched, but listed
pins were not the complete dependency closure. No source data changed.

The repair is a separate `packet_v2.py` consumer. It will pin and execute the
unchanged candidate producer, then include the old independent receipt's full
input map at its explicit graph-root owner. Include this repair declaration,
wrapper and wrapper tests as new method inputs. Save exclusively to
`packet-v2-01.json` and `packet-v2-02.json`; do not overwrite the failed candidate
or change its producer to invalidate its recorded pins.

All fields other than `inputs` and `inputs_after` must exactly equal the
candidate. In particular, all 42 slots, 191 native mappings, source pointers,
version 2 packet ID, scientific assumptions and unaccepted states remain
identical. The full byte hash, not packet ID alone, identifies the new release.
Two exclusive executions and a separate complete reconstruction/closure check
must pass before presentation. Viewer/checker defaults must bind the new
filenames explicitly, with no aliasing or global monkeypatching.

Test synthetic missing-child closure, altered dependency bytes, unchanged
scientific payload and source nonmutation before execution. Preserve failures;
do not relax the declared closure requirement or regenerate different samples.
The original protocol, method review, legal boundaries and human gate continue
unchanged. This is a dependency-only correction, not a new selection rule or
an admitted scientific result.
