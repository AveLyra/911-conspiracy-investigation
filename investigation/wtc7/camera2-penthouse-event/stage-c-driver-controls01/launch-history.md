# Stage C driver synthetic-control executions

These are implementation controls only. No historical display was rendered or
viewed by the driver agent. Existing source PNGs were read only for integrity
hashes; all rendered controls use deterministic synthetic pixels.

Working directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`.

1. Initial sandbox command:
   `PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 research/sherlock-wtc7-investigation/camera2-penthouse-event/test_stage_c_display.py --out stage-c-driver-controls01/attempt01`.
   Exit 1 before tests or control files: the sandbox denied creation of the
   control directory with `PermissionError: Operation not permitted`. This is
   an execution-permission failure, not a failed test.
2. The identical command ran after reviewed workspace escalation. Exit 0:
   28 tests (5 inherited crop tests plus 23 driver tests), 0 failures/errors,
   3.859 seconds. Protected input/code hashes were unchanged. Its complete
   snapshots, log, synthetic failures and receipt remain in `attempt01/`.
3. Final source-loader review replaced ordinary import loading with execution
   of the exact hash-checked source bytes, avoiding reliance on a cached `.pyc`.
   The same command with `--out stage-c-driver-controls01/attempt02` ran after
   reviewed workspace escalation. Exit 0: the same 28 tests, 0 failures/errors,
   3.751 seconds. All 86 protected input/code fingerprints remained unchanged.
   This is the final implementation test run.

Read-only verification of the final attempt independently rehashed all 2,941
receipt-listed files, checked identical before/after protected-pin documents,
parsed both new Python files, checked whitespace/conflict markers, and confirmed
that neither historical `stage-c-run01/` nor `stage-c-run02/` existed. Exit 0.
`git diff --check` also exited 0; the explicit file checks cover the new,
untracked driver and tests.

Final implementation identities:

- `stage_c_display.py`: `a5f932d13ffd2e8f137e5702a547cb89ab73498b58ace81359751dbb0d91892a`.
- `test_stage_c_display.py`: `ae75b7eebdab55498857814317d88259ccef9b9525d5e490bbe01959f78af015`.
- `attempt02/receipt.json`: `9ea6974084575773c622e5f38d5bffbc9f664d3b6e24512600d62ac9e557af25`.

The independent pixel oracle concatenates source byte rows and repeats each
byte four times horizontally and each resulting row four times vertically.
It does not call the producer crop or resize function. Passing these tests
establishes the tested transformation and rejection behavior, not a historical
roof-component identity or event interpretation. Root review, independent
rerun and explicit release to historical display generation remain separate.
