# Executed audit checks

Local side-conversation audit, October 9, 2026. No product acceptance fixture or scientific experiment was run.

## Actual commands and outcomes

The following invocation paths were used during preparation:

```text
ruby -c /private/tmp/sherlock-feedback-audit.jGhiRB/build_register.rb
  Syntax OK; exit 0.
ruby -c /private/tmp/sherlock-feedback-audit.jGhiRB/build_report.rb
  Syntax OK; exit 0.
ruby -c /private/tmp/sherlock-feedback-audit.jGhiRB/verify_audit.rb
  Syntax OK; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/build_register.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run01
  Success; 272 blocks, 225 retained, 47 classified exclusions; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/build_register.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run02
  Success after adding explicit receipt/acknowledgment input pins; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/build_report.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run02 /private/tmp/sherlock-feedback-audit.jGhiRB/findings.json
  Five artifacts created, 24 detailed comparisons, 225 traceability entries; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/verify_audit.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run02 --save
  First attempt: exit 1, Array#filter_map unavailable in installed Ruby 2.6.10.
  Repaired map/compact compatibility only, preserving the exact predicate.
  Second attempt: 19 checks passed; verification.json written; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/build_register.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run03
  Success; same pinned inputs, empty output directory; exit 0.
ruby /private/tmp/sherlock-feedback-audit.jGhiRB/build_report.rb /private/tmp/sherlock-feedback-audit.jGhiRB/run03 /private/tmp/sherlock-feedback-audit.jGhiRB/findings.json
  Success; exit 0.
```

A separate Ruby SHA-256 comparison of all ten generated run02/run03 preservation/report files (excluding the time-bearing verification receipt) found byte-for-byte identity. Its per-file hashes are preserved in `replay-verification.json`. This does not certify semantic completeness, privacy clearance or any Sherlock feature.

The final methods are retained in `methods/`. Reproduce into a new empty directory, using the retained `findings.json` as the report input. Builders fail rather than overwrite an existing output. They also fail if the pinned original feedback, sent payload, delivery receipt, acknowledgment or recipient log changes. Re-review a new source version deliberately; do not silently replace the pins.

The disclosure screen initially used an overbroad name substring that would also match the benign word “deterministic”; it was corrected before the first generation run to use whole-word names. The verification includes both benign-word and sensitive-marker controls. This textual screen is not a complete privacy review.
