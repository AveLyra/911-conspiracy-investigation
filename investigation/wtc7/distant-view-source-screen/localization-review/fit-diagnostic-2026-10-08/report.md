# Synthetic pointer-delivery diagnostic — bounded result

October 8–9, 2026 local. Research-method software, not WTC7 measurement.

## Finding

The new instrumented Fit-view miss is explained by changed delivered input,
with no mapping defect demonstrated in the twelve prescribed cases. The logged
click events carried identical coordinates for two different intended native-pixel rows:

| Case | Intended native cell | Requested CSS position | Delivered CSS position | Reported native cell |
| --- | --- | --- | --- | --- |
| fit-02 | (500,179) | (330.224881,471.797705) | (330,472) | (500,179) |
| fit-03 | (500,180) | (330.224881,472.417139) | (330,472) | (500,179) |

Displayed requests above are rounded for reading; exact numbers, event-time
rectangles and all outcomes are in [browser-cases.json](browser-cases.json).
An independent cell-boundary calculation places that delivered point in row179.
No recorded geometry change explains the difference. The unchanged production
mapper therefore reports the delivered cell correctly in this new case.

This does **not** establish which OS/tool/browser layer changed the request, a
universal rounding rule, or the cause of the earlier uninstrumented miss. It
does not provide a guaranteed one-pixel human error bound. No mapping fix was
made, and the original failure remains preserved.

## Prescribed observations and review

The [protocol](PROTOCOL.md) fixed the twelve targets before implementation or
data collection. The method was prior-informed, not blind. A separate reviewer
authored an interval-boundary oracle without importing the production mapping
or logging code. Its schema alignment finished after initial root observations
had begun but before that reviewer inspected the actual case data. Do not call
the entire checker preregistered or the computational review an independent
browser replication.

| Mode | Intended-cell hits | Delivered-cell mapping agreement | Recorded geometry changes |
| --- | ---: | ---: | ---: |
| Fit | 5/6 | 6/6 | 0 |
| 100% | 3/3 | 3/3 | 0 |
| 200% | 3/3 | 3/3 | 0 |

These are counts for a fixed diagnostic sample, not accuracy estimates for a
population of displays or users. Thirty-six case events reconcile with the
complete 42-event log; the other six events are the two zoom-control triplets.
All were completed, with zero pending at closeout. Four keyboard steps moved
(200,100) right/down and reversed left/up exactly. The six historical entries
stayed uninspected and no synthetic draft was recorded. The repeated 72 empty
rows in twelve snapshots are not 72 independent human reviews.

The [separate review](independent-review.md) and
[peer summary](verification-peer.json) reproduce the root results; root and
peer summary bytes match. The review notes missing pre-request visualViewport
data, inability to exclude unrecorded overlays, and that keyboard observations
contain draft counts rather than full draft snapshots. The final read-only DOM
check after screenshot scrolling still showed control selected, locked(200,100),
no pending box, zero drafts and 42 completed events.

## Verification and retained failures

Root reran ten Python tests, eight logger tests, sixteen independent-oracle
tests and 55 original regression tests: all passed. The original independent
packet verifier rechecked 660 predecessor and17 packet-input pins. A separate
[closeout checker](verify_closeout.mjs), without producer imports, verified all
14 new input pins, seven byte-identical files in each final packet, unchanged
original modules and the single-tag HTML derivation. Its
[live result](closeout-check.json) verifies all seven route bodies/MIME/security
headers and seven refusal/HEAD cases. These checks validate the specified
software contracts, not historical or physical accuracy.

Two preparation failures are retained in [execution.md](execution.md): an
unsupported browser click call delivered no event; and a last server-only
source change invalidated the first two packet pins. Those packets were kept,
an exact pre-change server reconstruction was hash-checked, and two new packets
were built before actual acquisition. Later sandbox denials for loopback HTTP
and screenshot saving were resolved through scoped approved operations, not
misreported as successful initial checks.

The [synthetic screenshot](synthetic-final-view.jpg) shows the final coordinate
readout and disabled human-response controls. It is not historical footage and
was not used to infer event coordinates. The diagnostic server was stopped
after verification; the original viewer was left running. No original source,
annotation, review response, frozen material index or accepted finding changed.

## Decision and next independent task

Keep Fit as overview; use native/doubled view and single-pixel keyboard checking
for precise selection, with explicit abstention where identity is ambiguous.
Six successes at fine scale do not create a general precision guarantee. No
further mapping repair is justified by these results.

Actual DistantView human localization remains pending under the unchanged
[instructions](../HUMAN-REVIEW.md). The next admissible measurement step is a
real reviewer identifying which of the six frames they inspected and giving
their bounds or explicit inability to localize. Full-reasoning review should
then preserve those responses separately and evaluate them under the existing
protocol, without fabricating answers, changing targets or silently retuning
criteria. R1's completed human review is not reopened.

The generic workflow lesson is appended to existing SFB-002/SFB-005 locally;
the archived Sherlock destination remains unresolved. Nothing was sent or
acknowledged. This unit is complete at its declared software scope. The full
investigation remains active/incomplete, with no changed collapse ranking,
legal promotion, Sherlock/Faraday acceptance, commit or push.
