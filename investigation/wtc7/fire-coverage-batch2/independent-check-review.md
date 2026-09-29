# Independent batch-2 arithmetic and preservation audit

2026-09-16. **PASS for the frozen inputs and producer products below.** Exact
13-asset membership, source/record pins, all five comparison axes and complete
retention of raw descriptions and unforced region lists reproduce. This is not
an assessment of the visual labels' accuracy, temperature, fire extent, cause
or qualified human expert review.

## Independence and sequence

Read current main AGENTS, WORKFLOW and START-HERE and the complete 162-line
unit [PROTOCOL](PROTOCOL.md). Applied evidence-falsification, source-of-truth and
development-verification safeguards. Main, source imagery, prior records,
producer code and all earlier outputs remained read-only.

Before implementing the independent algorithm, inspected only protocol text,
source-key schema/technical image metadata and prior paired membership IDs.
New `main.json`/`reviewer.json` were hashed but their annotation content and
producer products were not opened. Neither `summarize.py` nor its tests were
read, imported or run by this arm.

The initial [checker](independent_check.py) froze at SHA256
`69137496ff17c36bae5120a0f06887adebce66d0a45db5967d1d17522bcf4c21`.
Its [first control receipt](independent-controls01.json), SHA256
`f35841710ded5b2c7770c40630ac4bd3d706e3ff9475248fb5233ab3f8c108a7`,
embeds the complete initial source and records **35/35 PASS** before historical
calculation. The first independent historical result then froze before any
producer comparison was inspected:
[independent-check01.json](independent-check01.json), SHA256
`75deedc4ab184c9eb079a3f011439479517856005fbca0e58a5fbd6142770ade`.

Only then was the producer JSON layout inspected. The first schema query also
included paired annotation content; that occurred after the independent raw
result froze, not during algorithm construction. A separate projection adapter
was added to express the already-derived values in the producer's field names.
No original validation/comparison function was changed: product mode verifies
all 14 original non-main function ASTs against the embedded frozen source.
The main dispatcher and new adapter/control functions changed transparently.

Final checker SHA256:
`cb8725cc75cf2f99ef5900c5541ff01ce334f61ba7b152a3c21a89c0e60c8b44`.
The [second control receipt](independent-controls02.json), SHA256
`6e2ea40c2a9bec77a0078fa3972bb832e2bc15473ee831a3f163d7118425fba0`,
records **43/43 PASS**: the same 35 controls plus eight output-projection tests.
The producer source was subsequently hashed solely to verify its emitted code
pin, not read or executed as an implementation source.

## Source and product pins

| Input/product | SHA256 |
|---|---|
| Unit protocol | `8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff` |
| Reviewed provenance key | `c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3` |
| Prior main image-level record | `d7673cc50ebca454ea30a0d2c45e44041e9d06de9f586e32dd27a65818f535ce` |
| Prior reviewer image-level record | `03c671cfb383e939509e0008101a81e4954141c8c8f680596bbecde573f128f0` |
| Batch-2 main record | `63100450901d2358ee14f253a95b154f038091a88e0d3cf1c81e56126a0c2c2b` |
| Batch-2 reviewer record | `2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7` |
| Both producer comparisons, 177,385 bytes each | `f6934003b585a3d2f43e5ae5c7965b9a5b687247c0c5fa590117e7ddcf8e3cfb` |

The independent raw receipt contains all **19 input pins**, including the 13
individual JPEG byte hashes, and all original annotation records. JPEG byte
counts and hashes were checked directly without image decoding/interpretation.
Record dimensions were compared to the admitted key's native/extracted
dimensions; this is not a fresh image-header or visual measurement. Source
hashes were checked before and after calculation. The producer inventory01 was
not used to reconstruct membership.

The admitted key partitions exactly 28 assets into 25 photographic images and
three geometry graphics. The two pinned prior records each contain the same
12 unique photographic IDs. Their set complement is exactly the protocol's
13 IDs, all present once and in the declared order in both new records. This
reproduces the key's classification and finite extraction membership, not all
historical photographic coverage or 25 independent exposures.

## Exact comparison results

| Axis | Agree | Different |
|---|---:|---:|
| Target evaluability | 7 | 6 |
| Any `flame_like` feature | 12 | 1 |
| Any `ambiguous_glow` feature | 10 | 3 |
| Smoke status | 9 | 4 |
| Any nondetection region | 10 | 3 |

Exactly **3/13** assets agree on all five coarse axes. **0/13** paired full
asset records are exactly equal. These denominators describe AI annotation
comparisons, not sensitivity, accuracy, independent physical trials or fire
frequencies. Presence can agree while location, alternatives, reasons or
visibility assessments differ.

The [product verification receipt](independent-products01.json), SHA256
`0f51feaf254749a4c661c2cb045d765cfe930006008e9deb5e986df22cf8798f`,
records exact agreement with both producer products: each product contains
the expected **65 axis triples, 65 unforced region-list pairs, 39 description
pairs, both entire raw documents, ordered sample membership and all emitted
source/record/image hashes**. Both producer files are byte-identical. No
tolerance or normalization was used to erase string, coordinate or list
differences; the independent raw result also retains recursive field-level
differences and full original records.

Exact JSON-equality counts across 13 pairs are: luminous lists 4; nondetection
lists 3; overlay lists 1; smoke-region lists 0; target rectangles 0. Target
reasons, smoke reasons and visibility-limit lists each have 0 exact equalities.
Exact inequality is not proof that approximate boxes do not overlap or that
every differently worded sentence conflicts. Region matching was deliberately
not forced, and no area/window/fire totals were calculated.

## Controls, commands and limits

Synthetic controls include same-count/different-location regions with unchanged
coarse axes; simultaneous smoke and nondetection; both luminous appearance
types; preservation of changed descriptions; input immutability; changed-byte
hash detection; duplicate keys, malformed JSON and nonfinite values; false
inspection declaration; invalid dimensions, pins, coordinates, bounds/enums;
smoke/target consistency; exact membership/order; and empty/uncertain cases.
The byte-mutation synthetic check tests digest distinction, not a concurrent
live-file attack; actual input pins were separately checked before/after runs.

All invocations used the bundled Python executable
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
with `-B`, working directory this unit. Receipt `argv` records complete commands:

```text
independent_check.py controls --output <unit>/independent-controls01.json
independent_check.py run --output <unit>/independent-check01.json
independent_check.py controls --output <unit>/independent-controls02.json
independent_check.py products --output <unit>/independent-products01.json
```

All four first executions passed. An additional intentional attempt to write
the occupied controls02 path raised `FileExistsError` before processing; its
existing hash remained unchanged. That expected refusal is not a failed
scientific control or an overwritten run.

This is a **frozen-input audit, not general validator equivalence**. The
independent validator permits a nonempty string or string list for luminous
alternatives; the producer and actual frozen records use nonempty string lists.
`math.isfinite` on extraordinarily large Python integers can raise
`OverflowError` rather than the checker's normal `ValueError`; actual native
coordinates are small. No arbitrary hostile-input completeness is claimed.
Reasons and alternatives are checked structurally/nonempty, not certified for
substantive observational adequacy. Top-level extra metadata is preserved,
not silently dropped. Inspection flags are declarations, not a substitute for
actually viewing an image.

No image interpretation, source-attribution adjudication, probability,
temperature, extent, cause or expert certification follows. No source changes,
producer edits, outside-unit writes, web calls, transmissions or canonical
promotion occurred. Initial code, records, controls and products remain
recoverable under their exact pins.
