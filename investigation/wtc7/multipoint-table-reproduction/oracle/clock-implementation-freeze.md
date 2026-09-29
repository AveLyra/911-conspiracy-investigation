# Independent clock diagnostic freeze

2026-09-19, explicitly post-result follow-up. Original oracle code/results
remain frozen and unchanged. This independent diagnostic was written before
reading the producer's clock code or clock outputs; it imports neither.

- Declared [addendum](../CLOCK-ADDENDUM.md): SHA-256 `198d31a14ca49368bfc00c64ed3d4827d8fea9d7045a4f2a090e75a5ec6a866f`
- `clock_oracle.py`: SHA-256 `bba5b6a71a4685fdb3e6fe45e1bec7b87b714809d1d64e19ffdccc2faf77585b`
- `clock_test_oracle.py`: SHA-256 `618610c1755ba5a9b8abcb2a0f809ff86d92459991f6283097515e0185a2cc06`

Executed `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v clock_test_oracle`
from this directory with Python 3.14.0. Six synthetic-only tests passed in
0.001 seconds. They include the three exact spans, linear histories with known
velocities, positive/negative extremal rounding witnesses at the candidate's
exact bound, explicit beyond-bound failure, translation invariance,
supported/unsupported membership and malformed input failure.

Historical calculation follows this freeze and tests exactly spans `2/5`,
`1001/2500`, and `400/999` seconds. The row-specific hypothesis is a common
centered twelve-frame duration, not recovered historical selection. No
original fit is recalculated or rescaled. Numerical agreement cannot identify
the source timebase or verify the video-to-table join.
