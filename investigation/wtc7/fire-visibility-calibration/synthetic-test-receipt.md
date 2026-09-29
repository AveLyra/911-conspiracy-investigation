# Synthetic bookkeeping validation

Research-only, 2026-09-15. The bookkeeping implementer did not open `main.json`,
`reviewer.json`, or any historical annotation set before or during these tests.
Tests read the frozen protocol, preserved geometry, and two original JPEG files
as read-only inputs. All annotation fixtures were synthetic. Temporary synthetic
JSON files and outputs were created in temporary directories, not source paths.

Executed from this directory:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest -v test_summarize.py
```

Final result: **31 tests passed**, including all ten protocol scenario subtests.
An earlier 30-test run also passed; a final metadata test was added after the
root reported that one frozen label file expresses independence as a structured
object. The protocol does not constrain independence metadata to a string.
The parser now preserves either a nonblank string or nonempty object without
coercion and rejects nonfinite nested values. No classification rule changed.

Validated code/input pins:

- `summarize.py`: `bfdf1c875c24d104a9aec2b76306c4445060778676ad43c0c4e60c6bc302b9f8`
- `test_summarize.py`: `4ef40ad0c2c32ed40016ffb9cecc3db2c03e49effae21ed7507b0c58eae07d4a`
- `PROTOCOL.md`: `ea5c641475f47ef7a72fcf25876ec89eca8078b2756303920c323affe2a969a5`

Coverage includes all ten scenario rules; preliminary category invariance;
cautions without automatic veto; preservation of every unresolved reason when
an exclusion controls; exact threshold and eight-pixel boundaries; unknown and
zero in-frame bounds; no unstated multiplication by in-frame fraction; semantic
conflict preservation; independent comparison axes; empty eligible subsets;
independent finite arithmetic; duplicate, missing, unknown, and mismatched IDs;
required fields, enums, strings and reasons; invalid intervals, booleans used as
numbers, NaN, infinities, overflow exponents, and huge integers; duplicate JSON
keys; out-of-frame geometry; source pins and full JPEG dimensions; duplicate
reviewer identity; exclusive output creation including symlink refusal; final
input snapshot hash verification; complete raw-label preservation; and
byte-identical repeated synthetic reports written to different fresh paths.

The geometry checks validate source coordinates, spans, and interval structure,
not polygon topology or architectural identity. Tests establish bookkeeping
behavior, not visual accuracy, qualified forensic review, fire prevalence,
temperature, source-clock authentication, structural effect, or cause. No browser
test was needed for this offline CLI. No new dependencies were installed.

The root agent owns production runs and independent review of their arithmetic.
This receipt contains no production count results.
