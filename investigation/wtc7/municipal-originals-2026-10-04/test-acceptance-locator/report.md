# Generator test and acceptance record search

October 4, 2026 America/New_York / October 5 UTC. Research only. The bounded
metadata lookup identifies three particularly relevant full-load/result
records for a four-page content review. It does not establish that testing
occurred, passed, covered the installed fuel system or satisfied the July 17,
1999 payment condition. No new PDF content was read in this lookup.

The [prior accounting review](../approval-breakdowns-b/report.md) supplies the
specific lead: payment conditioned on successful emergency-generator testing,
Port Authority sign-off and punch-list completion. That condition is not a
substitute for the test and acceptance records themselves.

## Search coverage

Five exact requests and their raw responses are preserved under the frozen
[protocol](PROTOCOL.md). The [complete extraction](root-metadata.json) retains
every returned ID and property, not only the records selected for reading.

| Exact query focus | Returned | Server estimate | Service disposition |
|---|---:|---:|---|
| generator test | 50 | 144 | COUNT_LIMIT; next page available |
| quoted sign off | 20 | 20 | NO_MORE_RESULTS for this query |
| punch | 50 | 91 | COUNT_LIMIT; next page available |
| quoted 7/17/99 | 0 | 0 | NO_MORE_RESULTS; results key absent |
| Known folder control | 1 | 1 | Expected 167873 returned |

The generator and punch searches are explicitly incomplete; this unit did not
paginate or increase their declared caps. Search syntax/OCR recall remains
unverified. The date-string zero cannot refute the already-read July 17 text.
The control demonstrates retrieval of one known record, not calibrated recall.

The 121 returned occurrences represent 111 unique IDs and 1,772 reported
document pages, including the one-page control. These are metadata counts,
not newly acquired or reviewed pages. Every shared ID has consistent properties;
there are no duplicate IDs within a query. All 111 records join held catalog
folders by exact source, box and label.

The separately searched catalog has 4,205 folder rows. Its 29 matching WTC 7
folders describe 37 documents and 163 pages; these are folder totals, not
the sizes of 29 first-Bates PDFs. No off-source matches were discarded.
For example, folder 172389 contains four three-page records, whereas first
document 172389 alone has three pages. Similar titles do not prove independent
tests or exact copies. The named main lead memo adds no test-result locator.

## Next content selection

These three returned records explicitly name full-load testing or test results.
Within that relevance class they are selected in numeric-ID order, before any
content viewing. Their bytes and pages are expected values from metadata.

| Exact document suffix | Label | Pages | Bytes |
|---:|---|---:|---:|
| 172395 | Emergency Generator Full Load Test, WTC 7 OEM folder | 2 | 103619 |
| 172397 | Emergency Generator Full Load Test | 1 | 35481 |
| 173715 | GENERATOR TEST RESULTS. | 1 | 36410 |

Job 1854 generator-test candidates 171252, 172389, 172539, 172543 and 174096
remain available follow-ups. The Peoria-labeled 168654 may concern a different
testing setting; its relationship to installed-system testing is unknown.
Ten returned punch-list records remain leads, not completion certifications.
The twenty sign-off hits include proposals and accounting records; they are
not twenty demonstrated sign-offs. A generically titled document could contain
a sign-off, so title screening cannot establish absence.

At the lookup freeze, four returned IDs had same-named local municipal PDFs: 167873, 171300,
171557 and 172953. The root join is filename-based; the peer also checked byte
sizes. Neither is a new content/authenticity check. In particular, rediscovering
172953's conditional accounting packet is not independent corroboration that
its conditions were fulfilled.

## Verification and claim limits

Root and the [independent reader](metadata-review.md) froze their metadata
results before exchange. All 111 ID/query/page/byte rows agree; root reproduced
the complete saved extraction and catalog joins. The separate
[preservation check](preservation-check.md) confirms all five response copies
match scratch and all five request objects match the declared contract.

Method review found three weaknesses in hypothetical pagination/count inputs.
The checker was tightened without changing the frozen actual output; see
[source log](source-log.md) and [method review](method-review.md). The peer's
initial missing-results parser failure is preserved, not attributed to an
archive defect. These checks establish bounded local consistency, not source
authenticity, archive exhaustion or historical performance.

**Claim strength:** the saved index directly establishes the returned labels,
IDs and service coverage; the prioritization is an inference from those labels.
Actual test date, outcome, equipment scope, installation and acceptance remain
unknown. Contrary content, wrong-project attribution or later superseding tests
could defeat the proposed connection. No physical-compatibility or overall
collapse-cause ranking changes from this metadata unit. The comprehensive
investigation and its separate scientific, human and permission gates remain open.
