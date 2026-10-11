# Metadata checker method review

October 4, 2026 America/New_York / October 5 UTC. Bounded independent code
review by a prior-informed AI, not a source-content reading or human acceptance.
Main controls, the complete main charter, this unit's protocol, and the
development-verification/evidence-audit skills governed the check. Only this
note was written; root owns the checker and its corrections.

## Initial findings and corrected behavior

The initial checker SHA-256 was
`873a440c9d223cea470756384b102fb914862e827e3af1532569fe6235aa10d7`.
Fifteen synthetic in-memory cases exercised its parsing and calculation route.
Three cases exposed incomplete coverage being understated:

| Synthetic case | Initial behavior | Corrected behavior verified |
|---|---|---|
| `prev_avail=true`, otherwise valid one-record result | Accepted, `incomplete=false` | Accepted, `incomplete=true` |
| Empty `per_service_dataset`, otherwise valid one-record result | Accepted, `incomplete=false` | Accepted, `incomplete=true` |
| `estimated_count=0` with one returned record | Accepted, `incomplete=false` | Stops with `Estimate below returned count requires explicit review` |

Root added these three guards. The corrected checker SHA-256 is
`d561ee20e778bd0111103b3352f251396f618f2be2a23ad172ad96efb7ac6d7a`.
The estimate check requests explicit disposition of a count inconsistency;
it does not establish that an approximate estimate or historical record is false.
The unchanged valid baseline remains accepted with `incomplete=false`.

Initial checks also rejected duplicate JSON keys, duplicate properties and
result IDs, cross-query property conflicts, a wrong source and nonfinite PDF
size. Valid absent empty results remained represented as empty; a next page
and nonterminal service cause each produced `incomplete=true`. These are
bounded controls, not exhaustive schema validation. The final recheck tested
the three changed paths plus the valid baseline, not a new full-source audit.

## Actual check receipts and preserved harness failure

All Python checks used the bundled Python 3.12.14 executable:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

The stdout-only stdin harness imported the checker without invoking its CLI.
It replaced `read` with synthetic catalog/request/response objects and patched
memo reads and PDF filename enumeration to synthetic values. Five conforming
requests shared one synthetic known-control record; only the generator
response was changed for each pagination/count case. No actual response or
source file was needed by these synthetic tests, and no test file was saved.

- Initial 15-case invocation `e49d88`, terminal receipt `4a67f6`: exit 0,
  with the three weaknesses above explicitly printed rather than treated as
  successful validation.
- Corrected-code identity/read check `a6f9ae`: exit 0; hash matched the
  corrected value above and the review-note destination did not yet exist.
- First corrected-code recheck `28fcd4` -> `b1536d`: exit 1. Baseline and
  both incomplete-flag cases passed. The checker correctly rejected the count
  inconsistency, but this reviewer's harness compared a lowercase expected
  substring to the checker's capitalized error text. This was a harness
  expectation error, not a checker regression; the failed receipt is retained.
- Corrected harness `9b5691` -> `ab3f24`: exit 0. Only the error-message
  comparison was made case-insensitive. All four expected outcomes were
  asserted and passed against the unchanged corrected checker hash.

## Frozen real-output scope

Only after root announced its independent freeze, this reviewer inspected
the saved output hash and query-level pagination fields, not peer review notes.
Invocation `35097e` -> `bb5691`, exit 0, verified root-output SHA-256
`ee1f627b30ad1bdf5cc1073f1b52a6c4aae88b6364e2fd5e65b1c948d080b4c6`.
All five real responses have `prev_avail=false`, nonempty termination causes,
and estimates no smaller than the returned counts. Thus none of the three
synthetic counterexamples occurs in the frozen data.

Generator returned 50 of an estimated 144 and punch 50 of 91, both explicitly
incomplete. Sign-off returned 20 with no next page and `NO_MORE_RESULTS`.
The date probe preserved absent results, estimate zero and `NO_MORE_RESULTS`;
the control returned one. The frozen output contains 111 unique metadata IDs
and four IDs with held filename matches. Root separately reported that the
corrected checker's full rerun equals this unchanged frozen output; this
reviewer did not repeat that full saved-response calculation in this recheck.

## Permitted conclusions and remaining limits

The method checks saved request/echo agreement, declared scalar/property and
ID contracts, duplication, cross-query consistency and bounded pagination.
`held_pdf_name_matches` establishes filename correspondence only, not byte
identity, reviewed contents or completed two-reader coverage. Stronger copy
or review claims need their separate source and coverage receipts.

Use normal non-optimized Python: these guards rely on `assert`. Finite tests
do not establish every possible schema behavior, search-token semantics,
OCR recall, transport authenticity, archive completeness, test outcomes or
historical truth. A successful known-record control does not calibrate recall
for the other queries. No positive or negative causal finding follows.

No network, source images/PDF contents, browser/UI work, new acquisition,
Git operations, main/legal/STATUS edits or gate promotion occurred here.
