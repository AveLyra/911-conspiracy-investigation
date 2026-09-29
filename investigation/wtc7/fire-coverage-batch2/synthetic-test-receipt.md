# Synthetic comparison validation

Research-only, 2026-09-15. The implementation agent did not open this batch's
`main.json` or `reviewer.json`, or prior historical annotation files, before or
during implementation and testing. Observation fixtures were synthetic. Source
reads were limited to the frozen protocol, provenance-key metadata, and the 13
declared JPEGs' bytes and headers. No pixels were decoded, displayed, altered,
generated, or saved by these scripts.

Executed from this directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_summarize.py
```

Result: **27 tests passed** on Python 3.12.14 and Pillow 12.3.0. No dependencies
were installed. No browser was needed for this offline comparison helper.

Validated hashes:

- `summarize.py`: `f24bb98a1b988a8eef20ae2095d5ec7fa6819e3520f0516cbca126c733641464`
- `test_summarize.py`: `e2b971fe187d60ca81c1475dd63afa13d3b137cbbdcfa2680cd557bc6d5995a5`
- `PROTOCOL.md`: `8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff`

Coverage includes the six disclosed protocol scenarios; simultaneous luminous,
smoke and bounded-nondetection descriptions without an exclusive-class conflict;
flame-like versus ambiguous-glow presence; printed marks as overlays; overlapping
and unequal box lists without area sums or physical fire/window counts; retention
of repeated-source limitations; all five comparison axes independently; raw
record preservation; stable asset comparison order; exact 13-asset membership;
duplicate/missing/unknown identifiers and JSON keys; required schema fields,
enums, reasons, alternatives and visibility limits; independence as string or
object without coercion; invalid and nonfinite numeric values including booleans,
overflow exponents and huge integers; positive integer source dimensions;
in-bounds nondegenerate rectangles for every locator field; unresolved target
null consistency; visible, uncertain and not-identified smoke region rules;
source pin/path checks; source-byte and full-native-header checks; and refusal to
overwrite existing, failed-attempt, or symlink destinations.

All 13 actual JPEG hashes, byte lengths, and native dimensions matched their
pinned provenance metadata. The test suite explicitly prohibited image pixel
loading and saving during source verification. Two synthetic paired reports
written to separate fresh paths were byte-identical. An independent expected
one-axis change matched the generated comparison. A synthetic record changed
after initial reading was rejected by the final snapshot hash check.

The helper validates reasons for nonblank presence; substantive adequacy remains
an observational review task. Rectangles remain approximate locators, and exact
JSON inequality is not a physical disagreement measure or box correspondence.
These controls test bookkeeping and schema, not visual detection accuracy,
source-clock authentication, expert qualification, temperatures or causes.

The separate source-review task owns the 28-asset photographic/geometry inventory
and preservation checks for prior records. Root must check that gate before a
historical summary and owns production runs and independent result review. This
receipt contains no production observations or comparison outcomes.
