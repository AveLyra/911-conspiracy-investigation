# Detailed feedback comparison — selected confirmed gaps

Local, unsent technical review, October 9, 2026. This is not a product-defect or scientific-finding report.

These 24 comparisons distinguish a specific detail absent from the sent digest, partially preserved detail, and a detail explicitly preserved in the digest whose recipient-log pointer remains broad. They are **not an exhaustive count of omitted atomic requirements**. The accompanying annex preserves every retained technical source bundle, including details not individually discussed here, so this selected review is not used as a replacement specification.

“Missing” below means missing or insufficiently explicit in the identified text at the pinned snapshot—not missing from the entire conversation history or current implementation. No product implementation audit was performed. Broad headings do not establish a detailed test was recorded; equally, a concise log does not prove the full received message was lost.

Every test below is a **generic synthetic acceptance example**, not a new test result. Source notes describing earlier local tests remain attributed reports. No such fixture was run against Sherlock in this audit.

## G01 — Protect additions, not only the first baseline

Classification: `partial`.

[original lines 68–78](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:68) → FBR-004. Sent comparison: [item 10](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:36), [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: The digest requires immutable observations, errata and authorized preflights.

Detail requiring explicit treatment: It does not specify comparison against the complete latest reviewed objects plus ordered additions, rejection of undeclared rows or changed prior acceptance flags, or integrity checks bracketing the entire delegated call.

Acceptance: Synthetic: append one authorized row, then independently mutate an older qualification, reorder additions and insert an undeclared row. Each unauthorized change must fail, including changes made during the delegated call.

## G02 — Core/fringe agreement is not a confidence interval

Classification: `partial`.

[original lines 89–100](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:89) → FBR-006. Sent comparison: [item 12](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:42), [item 13](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:45).

Preserved: Item 12 explicitly preserves different core/fringe labels despite equal outer sets.

Detail requiring explicit treatment: The concrete swapped-label fixture, no-gap-filling rule, prohibition on labeling union/intersection as calibrated original-source confidence bounds and unambiguous agreement-count naming are not fully carried forward.

Acceptance: Synthetic: A has core {1}, fringe {3}; B has core {3}, fringe {1}. Retain disagreement; do not insert row 2 or label either set operation a calibrated confidence bound.

## G03 — Freeze outcome-independent human sampling

Classification: `specific_detail_absent`.

[original lines 436–450](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:436) → FBR-036. Sent comparison: [item 10](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:36), [item 11](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:39), [item 24](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:78).

Preserved: The digest requires review coverage and says small samples do not establish universal accuracy.

Detail requiring explicit treatment: It does not require the selection rule and complete target census to be frozen before discrepancy results, or preservation of unavailable targets, ties, coincident footprints and failed original selections.

Acceptance: Synthetic: replay the frozen rule against the full inventory including tied and unavailable targets. Reject convenient replacements chosen after results. Report actual inspected coverage; a passed spot-check is neither whole-source validation nor a calibrated confidence interval.

## G04 — Retain malformed occurrences without fabricated fields

Classification: `specific_detail_absent`.

[original lines 554–562](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:554) → FBR-045. Sent comparison: [item 02](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:12), [item 03](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:15), [item 08](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:30).

Preserved: The digest distinguishes record grains, missing metadata and quarantine generally.

Detail requiring explicit treatment: The missing-descriptive-field fixture and reconciliation of total, strict-valid and quarantined occurrences and unique IDs are absent.

Acceptance: Synthetic: omit a required description but retain the identifier and supplied fields. Do not insert a sentinel or drop the occurrence. Reconcile both counting grains and keep diagnostic success separate from full-contract validity.

## G05 — Tests must compute the claimed outcome

Classification: `specific_detail_absent`.

[original lines 955–971](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:955) → FBR-079. Sent comparison: [item 18](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:60), [item 19](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:63), [item 20](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:66), [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: The digest contains numerical decision and quantity-definition requirements.

Detail requiring explicit treatment: It does not explicitly require a regression control that computes the expected conclusion rather than merely checking a stored constant.

Acceptance: Synthetic: positive and negative input cases must reach the actual claimed computation. A test returning or comparing a prewritten conclusion without that computation must not count as outcome verification.

## G06 — Validate equality-colliding inputs after warming caches

Classification: `specific_detail_absent`.

[original lines 973–983](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:973) → FBR-080. Sent comparison: [item 05](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:21), [item 18](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:60), [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: Item 06 covers a different cache defect: byte-pin caching suppressing dependency traversal.

Detail requiring explicit treatment: The memoized numeric-type validation failure is absent: valid integer keys can allow equal boolean or float inputs to bypass inner validation.

Acceptance: Synthetic: warm the cache with valid integer tuples, then submit equality-colliding boolean and float tuples. Both warm and cold paths must reject invalid types; validate outside the memoized computation.

## G07 — Separate source changes from mistyped expected hashes

Classification: `specific_detail_absent`.

[original lines 1365–1372](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1365) → FBR-108. Sent comparison: [item 05](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:21), [item 06](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:24).

Preserved: The digest protects pins, original failures and original source bytes.

Detail requiring explicit treatment: It does not distinguish a handwritten expected-value transcription error from actual source change or require checking an independent earlier receipt before correcting the checker.

Acceptance: Synthetic: test changed source bytes and a mistyped expected digest separately. Preserve the first failure, consult the independent frozen receipt and prefer importing a pinned manifest value over hand transcription. Never silently rebaseline the source.

## G08 — XML text tails and lexical coverage

Classification: `specific_detail_absent`.

[original lines 1649–1663](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1649) → FBR-127. Sent comparison: [item 03](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:15), [item 05](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:21).

Preserved: The digest covers parser contracts and normalizer omissions generally.

Detail requiring explicit treatment: The XML-specific child-tail, comment/processing-instruction and parsed-versus-lexical coverage tests are absent.

Acceptance: Synthetic: use mixed element text and child tails, comments and processing instructions, structured strings and root/track attributes. Preserve immediate text segments and ownership; distinguish missing, empty, whitespace and nonempty values. Hash inventory alone is not plaintext review.

## G09 — Test candidate-search completeness, not just retained agreement

Classification: `partial`.

[original lines 1738–1752](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1738) → FBR-133. Sent comparison: [item 18](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:60).

Preserved: Item 18 explicitly preserves exact predicates, failed floating runs and feasible witnesses.

Detail requiring explicit treatment: It does not explicitly test completeness of a fast broad-phase candidate search independently of numerical agreement among the candidates it retains.

Acceptance: Synthetic: construct a relevant candidate incorrectly omitted by a fast prefilter. Agreement on every remaining row must not certify the candidate search as complete.

## G10 — Separate keyword ordering, card ordering and layered failures

Classification: `partial`.

[original lines 1754–1772](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1754) → FBR-134. Sent comparison: [item 05](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:21), [item 06](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:24), [item 08](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:30).

Preserved: The digest retains typed namespaces, relation types, blanks and partial failure receipts.

Detail requiring explicit treatment: It omits the specific reordered-keyword versus ordered-numeric-card fixture, and the requirement not to mask the original parse failure with a later resource-limit failure.

Acceptance: Synthetic: reorder keyword options without shifting blank numeric cards or losing the heading. Force a parse error followed by a memory-limit check; retain the original error location and the separate later failure, without inventing missing measurements.

## G11 — Keep event and observable paired

Classification: `specific_detail_absent`.

[original lines 1774–1791](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1774) → FBR-135. Sent comparison: [item 19](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:63), [item 20](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:66), [item 22](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:72), [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: The digest preserves quantity definitions, channels and event/utterance dates generally.

Detail requiring explicit treatment: It does not expressly forbid combining maximum load from one event with independently maximized rotation from another, or treating a missing plot or failed channel as exclusion of the whole specimen.

Acceptance: Synthetic: give two events different load/rotation pairs and retain the rotation at the selected load. Keep null stages and specimen/channel membership. An unsupported normalization or convenient sensor factor is not a documented recipe; a control must exercise the production branch.

## G12 — Check filename exclusions from different working directories

Classification: `specific_detail_absent`.

[original lines 1815–1827](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1815) → FBR-142. Sent comparison: [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: The digest requires correct executable escaping and scoped replay.

Detail requiring explicit treatment: The two-working-directory filename-exclusion regression is absent.

Acceptance: Synthetic: run the provenance search from the target root and another directory. Assert the excluded path components actually stay excluded; exit success alone does not verify the filtering rule.

## G13 — A metadata-output operation may still decode

Classification: `specific_detail_absent`.

[original lines 1905–1919](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1905) → FBR-148. Sent comparison: [item 08](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:30), [item 15](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:51).

Preserved: The digest separates probing, decoding and acceptance and preserves alternate metadata.

Detail requiring explicit treatment: It does not explicitly require verifying internal decoding before promising that a metadata-only output command performs zero decoding.

Acceptance: Synthetic: instrument the declared probe path and record whether stream discovery invokes decoding. Separate returned output type from actual execution scope; retain truncated captures rather than claiming a complete receipt.

## G14 — Preserve conflicting metadata lanes and full payload boundaries

Classification: `partial`.

[original lines 1921–1931](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:1921) → FBR-149. Sent comparison: [item 15](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:51), [item 22](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:72).

Preserved: Item 15 retains alternative metadata lanes, raw bytes and binary tails.

Detail requiring explicit treatment: It does not state the specific rule that disagreement must not suppress both usable values, nor explicitly prohibit reporting equal text prefixes as equal complete payloads.

Acceptance: Synthetic: keep equal NUL-terminated prefixes with differing binary tails and conflicting alternate times. Compare each lane, preserve the conditional ordering conflict and test both declared clock interpretations; neither infer authentication nor erase the conflict merely because editing is possible.

## G15 — Resampling-kernel exclusion is already in the sent item

Classification: `preserved_in_digest_not_detailed_in_recipient_pointer`.

[original lines 2011–2022](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2011) → FBR-157. Sent comparison: [item 16](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:54).

Preserved: Item 16 explicitly says to test exclusions through actual resampling kernels. This is not an original-to-digest omission.

Detail requiring explicit treatment: The recipient's already-covered pointer names broad template/similarity contracts; the inspected saved paragraphs do not enumerate this exact kernel-exclusion acceptance detail.

Acceptance: Synthetic: perturb excluded native pixels separately for each search branch. Verify that the actual interpolation kernel does not introduce them into scored support; a nearest-mask disjointness check is insufficient. Retain this as a detail-level acknowledgment request, not an accusation of message loss.

## G16 — Photometric training/evaluation masks and extrapolation

Classification: `specific_detail_absent`.

[original lines 2024–2034](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2024) → FBR-158. Sent comparison: [item 16](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:54), [item 19](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:63), [item 21](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:69).

Preserved: The digest preserves fit/evaluation roles, exclusion masks and common support broadly.

Detail requiring explicit treatment: It does not enumerate photometric mask intersection after resampling, empty threshold unions, clipping ties, out-of-training-range bright values or the distinction between bright-pixel support and physical fire area.

Acceptance: Synthetic: combine global tone changes with local or displaced bright patches. Assert actual training/evaluation mask separation, preserve the geometry fit and version the photometric mask. Report extrapolation, empty unions and clipping ties without converting encoded brightness to physical area.

## G17 — Reorder images, not only score rows; retain repeated pictures

Classification: `partial`.

[original lines 2102–2115](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2102) → FBR-164; [original lines 2117–2124](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2117) → FBR-165. Sent comparison: [item 15](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:51), [item 16](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:54), [item 21](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:69), [item 23](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:75).

Preserved: Item 16 includes shared stationary scenery with reordered changing details; item 15 says duplicates must not trigger automatic deletion.

Detail requiring explicit treatment: The exact false-control distinction (reversing score rows instead of reference images), duplicate-index versus identical-picture-index distinction and dense-refinement dependence are less explicit in the digest.

Acceptance: Synthetic: actually reorder reference images while preserving stationary scenery. Reject duplicate index entries but retain distinct presented indices with identical pixels. Keep near-best clusters outside a top-two shortlist; dense refinement is not independent corroboration.

## G18 — Common-support denominator and failure states

Classification: `partial`.

[original lines 2126–2139](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2126) → FBR-166. Sent comparison: [item 16](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:54).

Preserved: Item 16 explicitly requires identical valid positions, selected transforms and no refitting; equal cardinality is not equal support.

Detail requiring explicit treatment: The original full-mask coverage denominator and missing-transform/coverage/variance failure handling are not explicit in the condensed item.

Acceptance: Synthetic: two equal-sized but differently positioned valid supports. Evaluate the selected transforms on their intersection, use the original full-mask denominator and retain missing or failed transform/coverage/variance states instead of zero scores.

## G19 — Observation rows, page boundaries and nested candidates

Classification: `partial`.

[original lines 2194–2204](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2194) → FBR-176; [original lines 2206–2215](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2206) → FBR-177. Sent comparison: [item 10](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:36), [item 12](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:42), [item 14](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:48).

Preserved: The digest preserves overlap, delayed saving, candidate identity and observer states generally.

Detail requiring explicit treatment: It does not specify row-scoped parsing when indices recur in prose, page-level save boundaries for images already displayed together, or preservation of a short nested candidate within a longer positive interval.

Acceptance: Synthetic: repeat an index in explanatory prose without adding an observation; retain shared boundary rows without extra votes. Distinguish new candidate, continuation and no additional candidate. Grouping must preserve a separate short candidate and its unresolved initiation.

## G20 — Clock-rate sensitivity and circular calibration

Classification: `partial`.

[original lines 2239–2239](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2239) → FBR-185. Sent comparison: [item 14](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:48), [item 15](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:51), [item 19](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:63), [item 21](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:69).

Preserved: The digest separates calibration, endpoint identity, clocks and conditional reasoning broadly.

Detail requiring explicit treatment: It does not explicitly require the squared effect and correct direction of clock-rate changes on acceleration, distinguish reciprocal scale units, or forbid calibrating with the quantity under test.

Acceptance: Synthetic: for unchanged positions, scale every elapsed time by k and verify acceleration scales by 1/k². Keep pixels-per-length distinct from length-per-pixel. A separate authenticated calibration experiment is permitted; assuming the target acceleration to calibrate its own test is not.

## G21 — Opportunity, severity and consistency review

Classification: `partial`.

[original lines 2289–2303](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2289) → FBR-204. Sent comparison: [item 12](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:42), [item 18](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:60), [item 21](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:69).

Preserved: Item 12 separates opportunity, caution and decisive exclusion.

Detail requiring explicit treatment: It does not spell out membership invariance under ordinary appearance-class changes with identical opportunity, or preserve passing opportunity plus non_evaluable as a contradiction requiring review rather than a negative observation.

Acceptance: Synthetic: vary ordinary appearance classes while holding opportunity constant; membership must not change for that reason alone. Retain contradictory inputs, touching thresholds, zero extent and exclusion precedence. Text-rule comprehension is not visual accuracy calibration.

## G22 — Raw credits, family keys and verified origin are separate

Classification: `partial`.

[original lines 2305–2320](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2305) → FBR-205. Sent comparison: [item 12](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:42), [item 14](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:48), [item 21](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:69), [item 22](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:72).

Preserved: The digest preserves source families, nonexclusive positives and correlated observations.

Detail requiring explicit treatment: It does not explicitly require separate raw-credit, normalized-family and verified-common-origin fields, or prevent importing a precisely timed neighbor's precision into an approximate observation.

Acceptance: Synthetic: link two videos with inconsistent credit strings while retaining the original strings and known relationship. Preserve separate smoke, local flame nondetection and brightness axes, locators and disagreement. Keep the original time precision instead of fabricating a combined answer.

## G23 — Multi-factor model changes and schema-runner boundaries

Classification: `partial`.

[original lines 2349–2351](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2349) → FBR-210. Sent comparison: [item 19](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:63), [item 20](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:66), [item 25](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:81).

Preserved: The digest preserves model configurations and differentiates schema acceptance from authentication.

Detail requiring explicit treatment: The concrete two-factor change that must not be called a one-variable ablation, default date-format non-enforcement, and offline runner separation of unavailable validators, rejections and harness failures are not explicit.

Acceptance: Synthetic: change both geometry and heating and prohibit one-factor attribution. Separately test date-format enforcement under the actual schema validator. An offline schema runner must avoid engine imports and workspace/provider access and distinguish validator absence from schema rejection. Observed schema limits are not defects in an unlocated adapter.

## G24 — A checker must name what it did not check

Classification: `partial`.

[original lines 2437–2445](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md:2437) → FBR-222. Sent comparison: [item 18](/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/feedback-delivery-2026-10-09/outbound.txt:60).

Preserved: Item 18 explicitly rejects producer-selected empty comparison fields and unsafe intermediate arithmetic.

Detail requiring explicit treatment: It does not expressly require a passing field check to list unchecked summary flags and status labels rather than certify the whole report.

Acceptance: Synthetic: change a summary flag outside the declared checked field set. The result must identify that unchecked field, not imply it passed. Keep the already-preserved empty-field and unsafe-intermediate controls intact.
