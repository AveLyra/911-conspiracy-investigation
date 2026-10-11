# Dense Clip 3 supervisor review

2026-10-04 UTC. Independent implementation reader `/root/one_pixel_check`.

## Disposition

**Adequate for the declared bounded, operator-serial historical extraction
invocations, subject to the existing source, sampler-control and receipt gates.**
No remaining material implementation blocker was identified for that narrow
use. This is not execution approval for a different command, parallel jobs,
dense scoring without its separate controls, or scientific acceptance.

Reviewed `PLAN.md`, the complete supervisor and tests, preserved failed controls,
and completed `guard-controls03` receipts. The original three defects have
scoped corrections:

- A successful leader exit with a remaining process group is refused and
  cleaned up, not accepted as a completed job.
- Cleanup runs once and preserves the initiating reason. Final inspection
  errors are retained as null measurements plus `snapshot_errors`, not invented
  successful snapshots. The synthetic symlink case produces a failed receipt.
- Keyboard interruption and SIGTERM enter bounded cleanup; the previous SIGTERM
  handler is restored. Child PID is recorded. Permission errors are not treated
  as proof of absence: retries stay within the existing one-second grace,
  polling/reaping the leader precedes the group check, and persistent cleanup
  errors remain explicit failures.

The earlier permission errors have **no established operating-system cause** in
this review. Do not rewrite them as a proven Darwin startup race or harmless
noise. The corrected behavior, not an inferred diagnosis, is the tested result.

## Verification actually inspected

`guard-controls03/summary.json` records **16 tests, zero failures and zero
errors**, with hashes matching the reviewed current code and unchanged tests.
All **12** saved child/refusal receipts match that supervisor hash and have no
`shutdown_error`. The five immediate-stop controls now report returncode **−15**
and retain their proper threshold/interruption reasons. The normal job alone
is completed; expected-refusal jobs remain failed. The timeout and successful-
leader/live-descendant test implementations both assert actual descendant
absence; their passing status is part of the saved test result, not a new
process-death observation by this reviewer.

Controls also cover create-only target/record rejection, missing output,
preflight and mid-run free-space failure, actual monitor dispatch of mocked
job/lane thresholds, the aggregation thresholds, and failed snapshot retention.
The size thresholds are injected controls, not large disk-filling trials.
Earlier `guard-controls01` (**5 failures**) and `guard-controls02` (**3 failures**)
remain preserved, rather than being replaced by the passing record.

Actual review commands: local `cat`, `jq`, `shasum -a 256`, and a stdout-only
assertion script invoked with
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`.
The hash/receipt read exited zero (tool chunk `7012c7`); the independent assertion
check of current pins, all 12 receipts, the five immediate-stop return codes,
and preserved failed runs exited zero (`da9208`). **No tests or subprocess
termination were rerun by this reviewer.** No historical media was opened,
decoded, scored or displayed.

| Reviewed artifact | SHA-256 |
| --- | --- |
| guard.py | `0f20129bd7102935347315599e0e2a30264f5075f1569353339eac439422dbe0` |
| test_guard.py | `d6b24cf12ad0da7fcbc47785c6f428d91f040dc72ff22557a12787c303e45ee4` |
| guard-controls03/summary.json | `0d40bd204977b6fca43ea4e2253750ebe39fe78ec8320cda542545cda2680b94` |

## Continuing limitations and stop conditions

The strongest remaining actual risk is **polling/shutdown overshoot**. A write
burst or slow filesystem inspection can cross a threshold between checks; the
32-MiB reserve is not an operating-system quota. Requested 240-second/256-MiB
bounds and actual elapsed/bytes must remain separate in every extraction
receipt. The whole-lane 1536-MiB budget includes failed attempts, controls and
logs; fresh pre-write checks outside child invocations remain an operator duty.
The continuing free-space floor can also change because of unrelated activity.

Seriality is enforced by the operator, not a lock in this supervisor. Never
start another lane job before the prior invocation has a terminal outcome and
cleanup is resolved. A persistent shutdown error, unknown child status, missing
terminal receipt, failed/unavailable final resource measurement, or limit breach
must stop acceptance and require inspection; none is an automatic retry.

No Python cleanup can guarantee a receipt after supervisor SIGKILL, machine
failure or inability to write the filesystem. Group supervision also is not a
sandbox against a deliberately detaching child; the declared ordinary local
sampler is the reviewed use. Sampler buffered diagnostics lost during forced
termination remain incomplete. A supervisor's `completed` status alone does
not certify clean sampler diagnostics, complete frames, source identity or
historical authenticity. Those independent gates in the plan still apply.

Only this review file was authored. No guard, test, plan, failed receipt,
historical observation or source was edited.
