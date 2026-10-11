# Full Clip 3 extraction stopped before scoring

2026-10-04 UTC. **The first full-frame extraction was refused by the existing
diagnostic parser. No dense correspondence result was produced.** The
[pilot findings](../report.md), original annotations and cause assessment are
unchanged. This is a documented local software limitation, not adverse evidence
about the recording or the collapse.

The [prospective schedule](PLAN.md) covered all 189 indexed Clip 3 frames,
two native extractions and two complete scoring passes, with global selection
only after all 567 comparisons per pass reconciled. The method and supervisor
received separate [method](method-review.md) and
[implementation](supervisor-review.md) reviews. Fresh extractor, pilot and
dense-adapter controls passed after the failures recorded in
[execution.md](execution.md). Passing those controls did not override the
historical run's refusal.

## Observed failure

The saved decoder log's final line, line 394, contains `fps= 83`, with one
ASCII space after the equals sign. The unchanged parser expects a numeric
token immediately after `fps=`. It therefore rejects that line and reports
zero accepted final-summary lines. The field occurs in the decoder's final
processing summary; it is not the source's encoded frame-rate or PTS record.

| Recorded check | Actual outcome |
| --- | --- |
| Source bytes and SHA-256 before and after | Identical to the frozen source |
| Probe process and diagnostics | Exit 0; no stderr bytes |
| Decoder process | Exit 0 |
| Decoder diagnostic admission | Refused; one unmatched line and its resulting missing-summary count |
| Saved show-info entries | 189 frame and 189 color entries |
| Native PNG files written | 189, totaling 130,737,499 bytes |
| Product manifest | Not written: refusal preceded PNG/RGB verification |
| Outer sampler process | Exit 1; refused run receipt |
| Supervisor | Failed because child returned nonzero; no resource-limit breach |
| Recorded elapsed and extraction-directory size | 3.530894 seconds; 131,007,165 bytes |

Root separately reparsed the untouched log with the unchanged parser and
reproduced the refusal. A diagnostic-only, in-memory removal of that one space
made the grammar parse. No log file was altered, no new parser was adopted,
and this counterfactual is **not** admission of the saved extraction. The
untouched show-info entries separately reconcile with the 189 indexed PTS,
geometry, SAR and field-order records. Filenames were counted; root did not
open or display the new PNG pixels. The independent
[artifact review](artifact-review.md) records its own scope and limits.

## What remains untested

There was no second extraction, scoring, aggregation, shortlist or new image
review. The 189 written PNGs are preserved failed-run products, not accepted
measurement inputs. No PNG/RGB identity or repeated-pixel equivalence is claimed
for this dense attempt. The parser failure does not establish media corruption,
historical authenticity, a fire observation, or any physical mechanism.

Clip 3 remains only pilot-scored. The overall source-correspondence population
remains 18 of 1317 frames scored, with 1299 not yet scored under this method.
Clip 7 remains in scope. No numerical probabilities or cause-ranking update
follow from an extraction-format failure.

## Next bounded task

Preserve this schedule, parser, failed run and reviews unchanged. Separately
declare and review a versioned diagnostic-format correction that handles the
specific producer's padded processing-rate field without admitting warnings,
unknown lines, control characters, altered timestamps or unexpected counts.
Use producer-format evidence and positive/negative synthetic fixtures; do not
silently normalize the saved log or retrospectively mark it clean. Record any
new schedule, code/parent pins, diagnostic semantics and create-only output
names before a new historical attempt. Reconcile all required joins and repeats
before scoring; do not skip the gate because the suspected defect is small.

This is the next local implementation task, not a request to relax scientific
standards or a new external-disclosure authorization. The full investigation
goal remains active and incomplete. No legal/main record, accepted Sherlock or
Faraday finding, matrix, commit, push or transmission was changed.
