# Detailed digest coverage comparisons

These 24 selected comparisons concern the earlier 27-item digest, **not omissions from the later public technical record**. The technical-unit references link to the separately published detailed requirements; source line numbers are coordinates in the frozen feedback snapshot, not private paths. “Absent” means the specified detail is absent from the digest, not from all conversations or product code. No new product acceptance tests were run.

Each acceptance example below is synthetic. The earlier digest is reproduced in [DIGEST-ITEMS.txt](DIGEST-ITEMS.txt); detailed requirements remain in the [existing technical record](../feedback-technical-record-2026-10-09/README.md). These comparisons do not enumerate every omitted atomic requirement.

## G01 Protect additions, not only the first baseline

Classification: `partial`. Digest items: 10, 23. Public technical units: [TR-L0068](../feedback-technical-record-2026-10-09/record.json#L175).

Preserved in digest: The digest requires immutable observations, errata and authorized preflights.

Detail requiring explicit treatment: It does not specify comparison against the complete latest reviewed objects plus ordered additions, rejection of undeclared rows or changed prior acceptance flags, or integrity checks bracketing the entire delegated call.

Synthetic acceptance example: Synthetic: append one authorized row, then independently mutate an older qualification, reorder additions and insert an undeclared row. Each unauthorized change must fail, including changes made during the delegated call.

## G02 Core/fringe agreement is not a confidence interval

Classification: `partial`. Digest items: 12, 13. Public technical units: [TR-L0089](../feedback-technical-record-2026-10-09/record.json#L226).

Preserved in digest: Item 12 explicitly preserves different core/fringe labels despite equal outer sets.

Detail requiring explicit treatment: The concrete swapped-label fixture, no-gap-filling rule, prohibition on labeling union/intersection as calibrated original-source confidence bounds and unambiguous agreement-count naming are not fully carried forward.

Synthetic acceptance example: Synthetic: A has core {1}, fringe {3}; B has core {3}, fringe {1}. Retain disagreement; do not insert row 2 or label either set operation a calibrated confidence bound.

## G03 Freeze outcome-independent human sampling

Classification: `specific_detail_absent`. Digest items: 10, 11, 24. Public technical units: [TR-L0436](../feedback-technical-record-2026-10-09/record.json#L980).

Preserved in digest: The digest requires review coverage and says small samples do not establish universal accuracy.

Detail requiring explicit treatment: It does not require the selection rule and complete target census to be frozen before discrepancy results, or preservation of unavailable targets, ties, coincident footprints and failed original selections.

Synthetic acceptance example: Synthetic: replay the frozen rule against the full inventory including tied and unavailable targets. Reject convenient replacements chosen after results. Report actual inspected coverage; a passed spot-check is neither whole-source validation nor a calibrated confidence interval.

## G04 Retain malformed occurrences without fabricated fields

Classification: `specific_detail_absent`. Digest items: 02, 03, 08. Public technical units: [TR-L0554](../feedback-technical-record-2026-10-09/record.json#L1237).

Preserved in digest: The digest distinguishes record grains, missing metadata and quarantine generally.

Detail requiring explicit treatment: The missing-descriptive-field fixture and reconciliation of total, strict-valid and quarantined occurrences and unique IDs are absent.

Synthetic acceptance example: Synthetic: omit a required description but retain the identifier and supplied fields. Do not insert a sentinel or drop the occurrence. Reconcile both counting grains and keep diagnostic success separate from full-contract validity.

## G05 Tests must compute the claimed outcome

Classification: `specific_detail_absent`. Digest items: 18, 19, 20, 23. Public technical units: [TR-L0955](../feedback-technical-record-2026-10-09/record.json#L2066).

Preserved in digest: The digest contains numerical decision and quantity-definition requirements.

Detail requiring explicit treatment: It does not explicitly require a regression control that computes the expected conclusion rather than merely checking a stored constant.

Synthetic acceptance example: Synthetic: positive and negative input cases must reach the actual claimed computation. A test returning or comparing a prewritten conclusion without that computation must not count as outcome verification.

## G06 Validate equality-colliding inputs after warming caches

Classification: `specific_detail_absent`. Digest items: 05, 18, 23. Public technical units: [TR-L0973](../feedback-technical-record-2026-10-09/record.json#L2090).

Preserved in digest: Item 06 covers a different cache defect: byte-pin caching suppressing dependency traversal.

Detail requiring explicit treatment: The memoized numeric-type validation failure is absent: valid integer keys can allow equal boolean or float inputs to bypass inner validation.

Synthetic acceptance example: Synthetic: warm the cache with valid integer tuples, then submit equality-colliding boolean and float tuples. Both warm and cold paths must reject invalid types; validate outside the memoized computation.

## G07 Separate source changes from mistyped expected hashes

Classification: `specific_detail_absent`. Digest items: 05, 06. Public technical units: [TR-L1365](../feedback-technical-record-2026-10-09/record.json#L2748).

Preserved in digest: The digest protects pins, original failures and original source bytes.

Detail requiring explicit treatment: It does not distinguish a handwritten expected-value transcription error from actual source change or require checking an independent earlier receipt before correcting the checker.

Synthetic acceptance example: Synthetic: test changed source bytes and a mistyped expected digest separately. Preserve the first failure, consult the independent frozen receipt and prefer importing a pinned manifest value over hand transcription. Never silently rebaseline the source.

## G08 XML text tails and lexical coverage

Classification: `specific_detail_absent`. Digest items: 03, 05. Public technical units: [TR-L1649](../feedback-technical-record-2026-10-09/record.json#L3212).

Preserved in digest: The digest covers parser contracts and normalizer omissions generally.

Detail requiring explicit treatment: The XML-specific child-tail, comment/processing-instruction and parsed-versus-lexical coverage tests are absent.

Synthetic acceptance example: Synthetic: use mixed element text and child tails, comments and processing instructions, structured strings and root/track attributes. Preserve immediate text segments and ownership; distinguish missing, empty, whitespace and nonempty values. Hash inventory alone is not plaintext review.

## G09 Test candidate-search completeness, not just retained agreement

Classification: `partial`. Digest items: 18. Public technical units: [TR-L1738](../feedback-technical-record-2026-10-09/record.json#L3351).

Preserved in digest: Item 18 explicitly preserves exact predicates, failed floating runs and feasible witnesses.

Detail requiring explicit treatment: It does not explicitly test completeness of a fast broad-phase candidate search independently of numerical agreement among the candidates it retains.

Synthetic acceptance example: Synthetic: construct a relevant candidate incorrectly omitted by a fast prefilter. Agreement on every remaining row must not certify the candidate search as complete.

## G10 Separate keyword ordering, card ordering and layered failures

Classification: `partial`. Digest items: 05, 06, 08. Public technical units: [TR-L1754](../feedback-technical-record-2026-10-09/record.json#L3372).

Preserved in digest: The digest retains typed namespaces, relation types, blanks and partial failure receipts.

Detail requiring explicit treatment: It omits the specific reordered-keyword versus ordered-numeric-card fixture, and the requirement not to mask the original parse failure with a later resource-limit failure.

Synthetic acceptance example: Synthetic: reorder keyword options without shifting blank numeric cards or losing the heading. Force a parse error followed by a memory-limit check; retain the original error location and the separate later failure, without inventing missing measurements.

## G11 Keep event and observable paired

Classification: `specific_detail_absent`. Digest items: 19, 20, 22, 23. Public technical units: [TR-L1774](../feedback-technical-record-2026-10-09/record.json#L3395).

Preserved in digest: The digest preserves quantity definitions, channels and event/utterance dates generally.

Detail requiring explicit treatment: It does not expressly forbid combining maximum load from one event with independently maximized rotation from another, or treating a missing plot or failed channel as exclusion of the whole specimen.

Synthetic acceptance example: Synthetic: give two events different load/rotation pairs and retain the rotation at the selected load. Keep null stages and specimen/channel membership. An unsupported normalization or convenient sensor factor is not a documented recipe; a control must exercise the production branch.

## G12 Check filename exclusions from different working directories

Classification: `specific_detail_absent`. Digest items: 23. Public technical units: [TR-L1815](../feedback-technical-record-2026-10-09/record.json#L3556).

Preserved in digest: The digest requires correct executable escaping and scoped replay.

Detail requiring explicit treatment: The two-working-directory filename-exclusion regression is absent.

Synthetic acceptance example: Synthetic: run the provenance search from the target root and another directory. Assert the excluded path components actually stay excluded; exit success alone does not verify the filtering rule.

## G13 A metadata-output operation may still decode

Classification: `specific_detail_absent`. Digest items: 08, 15. Public technical units: [TR-L1905](../feedback-technical-record-2026-10-09/record.json#L3847).

Preserved in digest: The digest separates probing, decoding and acceptance and preserves alternate metadata.

Detail requiring explicit treatment: It does not explicitly require verifying internal decoding before promising that a metadata-only output command performs zero decoding.

Synthetic acceptance example: Synthetic: instrument the declared probe path and record whether stream discovery invokes decoding. Separate returned output type from actual execution scope; retain truncated captures rather than claiming a complete receipt.

## G14 Preserve conflicting metadata lanes and full payload boundaries

Classification: `partial`. Digest items: 15, 22. Public technical units: [TR-L1921](../feedback-technical-record-2026-10-09/record.json#L3871).

Preserved in digest: Item 15 retains alternative metadata lanes, raw bytes and binary tails.

Detail requiring explicit treatment: It does not state the specific rule that disagreement must not suppress both usable values, nor explicitly prohibit reporting equal text prefixes as equal complete payloads.

Synthetic acceptance example: Synthetic: keep equal NUL-terminated prefixes with differing binary tails and conflicting alternate times. Compare each lane, preserve the conditional ordering conflict and test both declared clock interpretations; neither infer authentication nor erase the conflict merely because editing is possible.

## G15 Resampling-kernel exclusion is already in the sent item

Classification: `preserved_in_digest_not_detailed_in_recipient_pointer`. Digest items: 16. Public technical units: [TR-L2011](../feedback-technical-record-2026-10-09/record.json#L4041).

Preserved in digest: Item 16 explicitly says to test exclusions through actual resampling kernels. This is not an original-to-digest omission.

Detail requiring explicit treatment: The recipient's already-covered pointer names broad template/similarity contracts; the inspected saved paragraphs do not enumerate this exact kernel-exclusion acceptance detail.

Synthetic acceptance example: Synthetic: perturb excluded native pixels separately for each search branch. Verify that the actual interpolation kernel does not introduce them into scored support; a nearest-mask disjointness check is insufficient. Retain this as a detail-level acknowledgment request, not an accusation of message loss.

## G16 Photometric training/evaluation masks and extrapolation

Classification: `specific_detail_absent`. Digest items: 16, 19, 21. Public technical units: [TR-L2024](../feedback-technical-record-2026-10-09/record.json#L4061).

Preserved in digest: The digest preserves fit/evaluation roles, exclusion masks and common support broadly.

Detail requiring explicit treatment: It does not enumerate photometric mask intersection after resampling, empty threshold unions, clipping ties, out-of-training-range bright values or the distinction between bright-pixel support and physical fire area.

Synthetic acceptance example: Synthetic: combine global tone changes with local or displaced bright patches. Assert actual training/evaluation mask separation, preserve the geometry fit and version the photometric mask. Report extrapolation, empty unions and clipping ties without converting encoded brightness to physical area.

## G17 Reorder images, not only score rows; retain repeated pictures

Classification: `partial`. Digest items: 15, 16, 21, 23. Public technical units: [TR-L2102](../feedback-technical-record-2026-10-09/record.json#L4196), [TR-L2117](../feedback-technical-record-2026-10-09/record.json#L4218).

Preserved in digest: Item 16 includes shared stationary scenery with reordered changing details; item 15 says duplicates must not trigger automatic deletion.

Detail requiring explicit treatment: The exact false-control distinction (reversing score rows instead of reference images), duplicate-index versus identical-picture-index distinction and dense-refinement dependence are less explicit in the digest.

Synthetic acceptance example: Synthetic: actually reorder reference images while preserving stationary scenery. Reject duplicate index entries but retain distinct presented indices with identical pixels. Keep near-best clusters outside a top-two shortlist; dense refinement is not independent corroboration.

## G18 Common-support denominator and failure states

Classification: `partial`. Digest items: 16. Public technical units: [TR-L2126](../feedback-technical-record-2026-10-09/record.json#L4239).

Preserved in digest: Item 16 explicitly requires identical valid positions, selected transforms and no refitting; equal cardinality is not equal support.

Detail requiring explicit treatment: The original full-mask coverage denominator and missing-transform/coverage/variance failure handling are not explicit in the condensed item.

Synthetic acceptance example: Synthetic: two equal-sized but differently positioned valid supports. Evaluate the selected transforms on their intersection, use the original full-mask denominator and retain missing or failed transform/coverage/variance states instead of zero scores.

## G19 Observation rows, page boundaries and nested candidates

Classification: `partial`. Digest items: 10, 12, 14. Public technical units: [TR-L2194](../feedback-technical-record-2026-10-09/record.json#L4497), [TR-L2206](../feedback-technical-record-2026-10-09/record.json#L4519).

Preserved in digest: The digest preserves overlap, delayed saving, candidate identity and observer states generally.

Detail requiring explicit treatment: It does not specify row-scoped parsing when indices recur in prose, page-level save boundaries for images already displayed together, or preservation of a short nested candidate within a longer positive interval.

Synthetic acceptance example: Synthetic: repeat an index in explanatory prose without adding an observation; retain shared boundary rows without extra votes. Distinguish new candidate, continuation and no additional candidate. Grouping must preserve a separate short candidate and its unresolved initiation.

## G20 Clock-rate sensitivity and circular calibration

Classification: `partial`. Digest items: 14, 15, 19, 21. Public technical units: [TR-L2239](../feedback-technical-record-2026-10-09/record.json#L4697).

Preserved in digest: The digest separates calibration, endpoint identity, clocks and conditional reasoning broadly.

Detail requiring explicit treatment: It does not explicitly require the squared effect and correct direction of clock-rate changes on acceleration, distinguish reciprocal scale units, or forbid calibrating with the quantity under test.

Synthetic acceptance example: Synthetic: for unchanged positions, scale every elapsed time by k and verify acceleration scales by 1/k². Keep pixels-per-length distinct from length-per-pixel. A separate authenticated calibration experiment is permitted; assuming the target acceleration to calibrate its own test is not.

## G21 Opportunity, severity and consistency review

Classification: `partial`. Digest items: 12, 18, 21. Public technical units: [TR-L2289](../feedback-technical-record-2026-10-09/record.json#L5222).

Preserved in digest: Item 12 separates opportunity, caution and decisive exclusion.

Detail requiring explicit treatment: It does not spell out membership invariance under ordinary appearance-class changes with identical opportunity, or preserve passing opportunity plus non_evaluable as a contradiction requiring review rather than a negative observation.

Synthetic acceptance example: Synthetic: vary ordinary appearance classes while holding opportunity constant; membership must not change for that reason alone. Retain contradictory inputs, touching thresholds, zero extent and exclusion precedence. Text-rule comprehension is not visual accuracy calibration.

## G22 Raw credits, family keys and verified origin are separate

Classification: `partial`. Digest items: 12, 14, 21, 22. Public technical units: [TR-L2305](../feedback-technical-record-2026-10-09/record.json#L5243).

Preserved in digest: The digest preserves source families, nonexclusive positives and correlated observations.

Detail requiring explicit treatment: It does not explicitly require separate raw-credit, normalized-family and verified-common-origin fields, or prevent importing a precisely timed neighbor's precision into an approximate observation.

Synthetic acceptance example: Synthetic: link two videos with inconsistent credit strings while retaining the original strings and known relationship. Preserve separate smoke, local flame nondetection and brightness axes, locators and disagreement. Keep the original time precision instead of fabricating a combined answer.

## G23 Multi-factor model changes and schema-runner boundaries

Classification: `partial`. Digest items: 19, 20, 25. Public technical units: [TR-L2349](../feedback-technical-record-2026-10-09/record.json#L5629), [TR-L2350](../feedback-technical-record-2026-10-09/record.json#L5649), [TR-L2351](../feedback-technical-record-2026-10-09/record.json#L5670).

Preserved in digest: The digest preserves model configurations and differentiates schema acceptance from authentication.

Detail requiring explicit treatment: The concrete two-factor change that must not be called a one-variable ablation, default date-format non-enforcement, and offline runner separation of unavailable validators, rejections and harness failures are not explicit.

Synthetic acceptance example: Synthetic: change both geometry and heating and prohibit one-factor attribution. Separately test date-format enforcement under the actual schema validator. An offline schema runner must avoid engine imports and workspace/provider access and distinguish validator absence from schema rejection. Observed schema limits are not defects in an unlocated adapter.

## G24 A checker must name what it did not check

Classification: `partial`. Digest items: 18. Public technical units: [TR-L2437](../feedback-technical-record-2026-10-09/record.json#L6058).

Preserved in digest: Item 18 explicitly rejects producer-selected empty comparison fields and unsafe intermediate arithmetic.

Detail requiring explicit treatment: It does not expressly require a passing field check to list unchecked summary flags and status labels rather than certify the whole report.

Synthetic acceptance example: Synthetic: change a summary flag outside the declared checked field set. The result must identify that unchecked field, not imply it passed. Keep the already-preserved empty-field and unsafe-intermediate controls intact.
