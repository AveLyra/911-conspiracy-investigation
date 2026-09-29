# Preserved first historical output attempt

After the implementation freeze and root's reconciliation release, the command
`PYTHONDONTWRITEBYTECODE=1 python3 exact_oracle.py --output run01 --reconciliation ../reconciliation.json`
was attempted from `oracle/` under the default filesystem sandbox. Input
validation and in-memory calculations completed, but directory creation failed
at `output.mkdir(exist_ok=False)` with `PermissionError: [Errno 1] Operation not
permitted: 'run01'`. Exit code 1. No result file or directory was created by
this attempt; no numerical result was displayed or inspected.

This is a filesystem write restriction, not a numerical test result. Preserve
this failure record; repeat the unchanged code with appropriate scoped write
permission and retain new result directories exclusively.
