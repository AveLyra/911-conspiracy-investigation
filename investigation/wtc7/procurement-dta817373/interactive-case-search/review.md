# Independent local review of the interactive-search result

2026-10-04. `/root/sibling_byte_audit`. **The bounded result is supported;
the procedural qualification is now documented.** This is review of root's selected
log and one saved screenshot, not an independently repeated search, complete
browser-event audit, raw HTTP preservation or original-document authentication.

## Result and protocol accounting

The saved log records one actual Search Cases click after the field held
`817373`, followed by the observed `/search/?q=817373&site=Tribunal_decisions`
URL. That is evidence of a submitted query, not merely a placeholder or typed
field. The single screenshot directly shows the query, Tribunal Decisions/Orders
filter, “Showing 1 - 2 of 2,” and both entries. It is consistent with the log;
it does not independently prove the complete click history or browser origin.

Recorded budgets: one homepage navigation, one query, two first-page results,
zero of two eligible detail/index opens, no original download/reformulation/
refresh/pagination/category change. This is not an all-category/case-file search.

**Initial correction, now addressed:** the protocol permits one follow-up DOM read only
when a genuine pending/loading state is observed. The initial empty accessibility
state had neither a loading marker nor an explicit no-results message. Later
population demonstrates a state change, but cannot retroactively establish that
the prospective pending-state condition was satisfied before the extra read.
The final accessibility read should therefore be expressly labeled a minor
deviation from that literal condition, rather than exact protocol compliance.
The transparent log preserves what happened; the deviation does not constitute
a second query, invalidate the populated screenshot, or imply manipulation.
An empty first snapshot also cannot establish zero results. No rerun is needed.

## Source identity, implications and remaining limits

Both entries display the case number, decision filename and sales/use-tax
snippets. One displayed path uses `Decisions`, the other `decisions`; exact link
targets come from the saved accessibility log, not the screenshot's abbreviated
breadcrumbs. Neither PDF was opened. URL case variation alone proves neither
byte identity nor distinct versions. Treating them as one apparent case/decision
family, not independent transaction evidence, is justified but not a byte test.

The screenshot confirms September 12, 2014 and October 16, 2003 search labels.
It does not establish issuance dates, a changed decision, or invoice dates.
The earlier held-source date is attributed prior work, not revalidated here.
Neither result is described as an original exhibit or a case-file index.
No new invoice, contract, inventory, 2001 access record or operational bridge
was acquired. Ordinary-maintenance evidence is unchanged, not strengthened by
this non-retrieval. No concealment, intent or collapse-cause conclusion follows.

The strongest alternative is different indexing, another public category or
offline/custodian holdings. Those routes remain untested. A verified original-
file locator would change availability; authenticated contents could alter a
specific date, equipment or transaction-scope claim. Neither a missing online
link nor an additional decision copy supplies that missing evidence.

## Actual review and preservation

Full skills/refs reads: `3629dd`/`44396a`; truncated controls reread in full:
`4541a7`/`f50187`. Full protocol/prior report/review: `e708ab`; pins: `718479`.
Full initial log/report: `a5d9d8`, all exit0. Only the saved UI screenshot was
viewed, once at original detail; its clipped bottom does not omit either entry.

`shasum -a 256` (`2d6ba3`, exit0) matched all four supplied pins below. `file`
(`159e01`) and `stat` (`3c5aa3`), exit0, confirm JPEG 1280×720 and 80,676 bytes.
Root's failed copy/missing-file checks and later temporary-copy match remain
attributed log entries, not newly reproduced here. No local check failed.

| Reviewed input | SHA-256 |
| --- | --- |
| PROTOCOL.md | `eefd015e9c25729f165edb2da8bd804ff0f0af1276b0f8bf997e034e5f7a60ab` |
| source-log.md | `e69b03a065b0df13873dc49d7ccf3a691f6d3ba1a8ddd34bd9732ff2f3bbca3e` |
| report.md, review-pending snapshot | `18ab3f5f8594a73d5b49ec91d9447e804dfe7407e262b5288f0cb75ed03cff52` |
| result.jpg | `f55d57b73116134934e2602c6563f642ca6567114b345e4e19f89320ac0c6c5f` |
| source-log.md, correction | `379118b527f94a4e5e2e3aa4b0360475e45556c02137de17ac1efe4cd47a355b` |
| report.md, correction | `3800a89ab8319f27bd40855e51855f35cc336fced87cad9971bec7db47c6aacf` |

The correction paragraphs were read (`0528d2`, `287e15`, exit0); they address
the finding without rewriting the protocol or claiming a second search.
`51191f` pins their revised files and unchanged protocol/image; old pins remain.
Only this review was added; navigation/review closeout remains root's work.
No external action, original acquisition, main/legal/engine/matrix/source edit,
human acceptance, commit or push was performed.
