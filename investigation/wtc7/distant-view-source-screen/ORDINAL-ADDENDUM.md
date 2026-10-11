# Ordinal only visual screen after a timestamp failure

October 8, 2026, before native frame extraction or viewing. The original
protocol remains frozen at SHA256
`47cd92e19bc8d2796e66efaf3e828ba9589d3d254da920de3a6802e7727c0daf`.
Its complete matching-timestamp test has not passed and is not being relaxed
into a pass. The source triage can separately use decoded frame ordinals
without asserting exposure times.

The first source probe exited at frame961's missing best-effort timestamp;
the source-preservation step had succeeded. A subsequent read-only metadata
inspection found 962 frames, MPEG4, 704 by480, native YUV420P, many missing
stored PTS fields and no best-effort timestamp at the last frame. No native
image has yet been extracted/viewed in this unit. The first probe retained
its command and zero-warning status but not its raw stdout. Preserve that
limitation and repeat into fresh directories with complete probe JSON and
bounded diagnostic capture; do not rewrite the failed attempt.

The independent code review also found that the reused decoder would allow
absent PTS and label best-effort timestamps as PTS, return fewer than eight
samples for very short clips, and discard diagnostic text. The initial12
synthetic checks did not test those protocol discrepancies. Keep those tests
and the original adapter unchanged; they do not certify the new contract.

## Revised output contract

A new hash-pinned adapter may reuse unchanged decode logic but must replace
the metadata parser. Every frame keeps its ordinal, nullable `stored_pts` and
nullable `best_effort_timestamp` as separate fields. Exact seconds computed
from each available value are separately named. No value fills a missing
field; no rate-derived or interpolated timestamp is admitted. Present pairs
must agree, and each available timestamp series must be strictly increasing.
Missing timestamps leave the original complete-timing test failed.

Require at least eight actual probed frame records, fixed native YUV420P
geometry, a positive time base and agreement of decode count with probe
count. The unchanged eight-ordinal rule selects 0,137,274,411,549,686,823,961
if the repeated count remains962. No source-frame choice is changed because
its PTS is missing. Preserve complete metadata before validation, including
failed validation; preserve stderr text and timeout status through the adapter.
Stop on any warning or error before admitting frames. Do not generate PTS or
change decode order, color format, raster size, rotation or frame rate.

Before historical processing, test nullable timestamps, zero preservation,
PTS disagreement, nonmonotonic known timestamps, short counts, format and
geometry failures, exact selection and safe output names. Verify two fresh
probes and decodes; compare source and decoded-frame identities. The two
separately frozen descriptive passes and original coverage/exclusions remain.
All descriptions use frame ordinals, never inferred seconds or event times.

This is an ordinal visual-source screen, not recovered historical timing,
independent camera authentication, onset measurement, a trajectory or a cause
test. A usable scene can justify a later protocol; missing timestamps cannot
be silently erased in that future work.
