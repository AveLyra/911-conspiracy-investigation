# Sherlock feedback digest coverage addendum

Receipt of the earlier 27-item feedback digest established that all 27 items arrived, not that every original qualification and test survived condensation. This bounded audit identifies 10 specific missing details and 13 partially preserved requirements among 24 selected comparisons. One investigated detail—testing exclusion through actual resampling kernels—was already explicit in the sent digest. This is not an exhaustive omission count or a product defect assessment.

Read [the comparisons](FINDINGS.md), [the 27 digest items](DIGEST-ITEMS.txt), and the [existing detailed technical record](../feedback-technical-record-2026-10-09/README.md). The detailed record remains the published requirements reference; this addendum does not replace it or claim it has the digest's omissions.

## Evidence and limits

The reviewed feedback snapshot has SHA-256 `e1c718bb928ba846deb0d527f69cda7ea00a8d888c2247a864b1d666b4204133`. The complete earlier sent message has SHA-256 `bd3f148bdfb1c5c4c55a33afbba0bedad7e3d3258c224754a12566925d61a740`. The digest file here is only the exact numbered-item excerpt: administrative intake directions and the receipt request are omitted, and its separate hash is recorded in the manifest. It is not represented as the full transmitted message.

The private preservation audit accounted for 272 nonblank source blocks, retaining 225 complete technical bundles and classifying 47 administrative, heading, status or resolved-item blocks for non-retransmission. These are paragraph-bundle counts, not distinct requirement counts. The existing public technical record uses a different, finer unit scheme; its unit counts are not in conflict with this paragraph census. This addendum does not certify a new exhaustive semantic review.

Nineteen local preservation and negative-control checks passed after a Ruby-version compatibility repair. A separate regeneration produced ten byte-identical audit/report files. Those checks establish bounded retention and reproducibility, not semantic completeness, privacy clearance, product implementation or scientific validity. The private original and detailed receipts are not included here. Readers can examine the digest and public technical transcriptions; direct source comparison requires separately authorized access to the pinned original.

A concise recipient log does not prove that the complete received message was lost. Its “already covered” disposition addressed core requirements rather than verifying every detailed test. The audit distinguishes that narrower scope from an actual original-to-digest omission.

## Publication boundary

This addendum includes generic requirements, explicitly synthetic acceptance examples, original source line numbers, public technical-unit references and integrity hashes. It excludes the original feedback log, private source paths, task and message identifiers, receipt records, correspondence, case documents and media. Hashes do not contain plaintext source text but can permit candidate-text comparison; they are not a privacy guarantee.

Repository publication is not a new acknowledgment by the designated Sherlock task, an implementation instruction, an independently verified fix, activation, or a scientific finding. The earlier acknowledgment retains its original scope. The previously published technical record at commit `e62491ba8cbfe7da9ad79a5194776fd4781036fd` is left unchanged.

## Reproduce the integrity checks

Run `ruby verify_addendum.rb` from this directory. It checks exact manifest file hashes, the digest and finding rosters, classification counts, source identity and public-unit JSON line links. In-memory negative controls reject an altered payload and an omitted finding. These are documentation checks, not the proposed product acceptance tests. The manifest pins the existing public record used for the links.
