# Two-fix retry result

The authorized two harness fixes are implemented in verify_bridge_retry.py;
the original runner and prior failed attempts remain unchanged. Runner SHA-256:
`e94ae5a743fd6fab45431e68c3eecb916e89b03710e4d48b0da4f5b446902b9b`.

Preflight (tool receipt 7b0151, exit 0) verified the exact two-fix source diff,
tee write/flush/isatty behavior, syntax/import without target execution, and
all 13 existing source pins. No product code or native test was modified.

The native invocation used the original env-cleared isolated Python 3.13.7
command, verify_bridge_retry.py, mode native, and fresh run root
`/private/tmp/wtc7-faraday-pilot.eGMyO9/native-retry-20261007`.
Tool receipt 1b2a3a returned terminal runner exit 1. Pytest exited 3 during
configuration: its logging plugin attempted to open `/dev/null`, which the
existing write guard correctly denied as outside the run root. Actual counts:
0 collected, 0 passed, 0 failed, 0 skipped. Both native acceptance checks failed;
zero failed test cases is not a pass. The isatty exception did not recur.

This is another harness/environment incompatibility, not a demonstrated
Faraday export defect. Execution stopped at the declared safety boundary.
Neither custom matrix was run; the enum fix has not been exercised end-to-end.
No evidence export or scientific-rigor pass is established.

The complete run is preserved in captured-retry-20261007, including its exact
invocation, script snapshot, log, receipt and guard controls. Scratch originals
remain. Absolute scratch locators are preserved, not rewritten as portable ones.
Faraday remains clean at 26ab7c96228b3c7ddcec0539f187d104ba49b47b.

Smallest proposed next correction: explicitly direct pytest's log file into
the fresh run root rather than permitting writes to /dev/null or weakening the
guard. That is outside this completed two-fix allowance and was not performed.
No subagent, external message, case import, main-thread goal update, commit or
push was used. This side-conversation result is not an independent review.
