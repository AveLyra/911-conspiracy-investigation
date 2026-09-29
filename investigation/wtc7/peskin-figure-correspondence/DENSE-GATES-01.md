# Dense execution safeguards, before production

This additive declaration responds to `dense-method-review.md` and preserves
DENSE-01, METHOD-01, the failed synthetic parser control, and their earlier
versions. No dense historical frames have been analyzed yet. The mathematical
registration, full interval and shortlist criteria are unchanged.

Use only four create-only production directories `dense00` through `dense03`,
with corresponding reproduction directories `repro00` through `repro03`.
Unexpected failure requires a separately declared continuation, never overwrite.
Tighten each chunk to at most 275 frames: four chunks cannot exceed the already
declared 1100-frame accepted total. Excess frames fail, rather than truncating
the intended interval. Each primary chunk retains at most 16 native PNGs.
Reproduction writes neither new PNGs nor duplicate score surfaces.

Retain the 450 MiB primary per-chunk limit; reproduction has a 10 MiB limit.
Other unit artifacts must total at most 150 MiB at preflight and closeout.
These eight bounded run slots plus the baseline budget sum to 1990 MiB, below
the 2 GiB unit limit. Check existing slots and aggregate disk usage, budget
surface writes conservatively, and verify actual final sizes. These are local
runner controls, not a claim that unrelated concurrent writers are constrained.

Require exact pins for the frozen method/protocol, passing original controls,
and the independent core comparison. Reproduction requires a completed prior
receipt for the same chunk, source, code, tools and declarations. Hash-check its
complete output manifest before use, compare every score/coverage array and
all frame/result rows, and compare each saved shortlist PNG's decoded RGB with
the fresh stream at its exact selected index. Compressed-file identity alone
does not establish decoded-pixel equality.

Reject nonfinite displayed PTS before its numerical consistency check. Preserve
the absolute ffprobe interval end. Use a 300-second process alarm as well as the
270-second decoder kill timer and final elapsed check. This practical timeout
does not claim a formal bound on uninterruptible operating-system I/O.

The independent rerun of the synthetic checks must target the final script
version before production. Passing controls do not certify exposure identity,
background alignment, historical clocks, temperatures or a collapse mechanism.
