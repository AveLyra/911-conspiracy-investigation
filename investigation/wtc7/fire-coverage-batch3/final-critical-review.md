# Final critical review of the batch 3 report

2026-09-24. Read-only report/record review by `/root/fire3_observer`.
Only this review file was written. No observation, source, timeline or report
was relabeled or edited; no new media, acquisition, model run or Chapter 9
claim was added.

## Disposition

The report's substantive result is consistent with the frozen observations,
the source-qualified coverage timeline and the prospective protocol. Three
small but meaningful wording corrections below should be incorporated before
the report is treated as the final summary. They do not require re-annotation,
retiming, new analysis, or a changed conclusion.

Acceptance is limited to an accurate research summary of the completed
25-image observation sub-study and 51-representation coverage join, with the
26th native representation still failing its declared gate. It is not optical
accuracy validation, expert acceptance, model validation, source authenticity,
an accepted case fact, completed WP1, or investigation completion.

## Exact corrections

Line numbers refer to the reviewed `report.md` SHA below.

| Location and wording | Why it needs precision | Exact replacement |
| --- | --- | --- |
| Lines 80-81: "The complete critical review retains all differences." | The critical-review narrative retains every coarse-field difference and selected consequential locator/relation differences. It does not enumerate every wording or rectangle difference. Exhaustive per-asset material remains in the frozen records and full comparison. | "The [critical review](observation-critical-review.md) explains the consequential differences; the [full comparison](comparison-full01.json) and frozen [root](root.json) and [observer](observer.json) records retain every per-asset description and locator." |
| Line 91: "facade-versus-foreground relation differs" for 5-146/156 | Neither disagreement is a positive foreground assignment. The alternate enum is `uncertain`, with foreground/depth among the alternatives. Do not turn uncertainty into a new physical classification. | "Coarse presence agrees but facade-associated versus uncertain relation differs." |
| Lines 163-164: "does not acquire positive support automatically from a failed NIST validation" | In this unit zero complete quantity/location/time model comparisons were performed. A reader could mistake "failed validation" for a performed empirical test that failed, despite the earlier accurate explanation. The intended distinction is lack of validation versus affirmative evidence for another mechanism. | "Deliberate removal also needs its own evidence and physically specified test; it does not acquire positive support merely because this batch has not independently validated NIST's sequence." |

Optional precision in the claim-ledger row at line 158: replace "An unreliable
estimate is not itself intent" with "Timing dependence alone does not establish
an unreliable estimate or intent." The report already explains this correctly
at lines 31-35 and 115-118; this optional change would make the table equally
explicit rather than suggesting unreliability was independently found.

## Requested substantive checks

| Check | Finding |
| --- | --- |
| Nine shared images versus three morphology disagreements | Correct. Shared flame-like-presence figures are 5-122, 123, 134, 136, 138, 140, 142, 143 and 152. Additional observer-only presence is 5-128, 130 and 133. Root has 9, observer 12. These are saved judgments, not resolved emitting-gas identification or independent event counts. |
| Coarse axes versus feature agreement | Correct in substance. Four smoke, three flame-presence and two nondetection-presence differences total 9 of 125 fields; target evaluability and ambiguous-glow presence match. The text preserves corner relation and broad-box disagreements. Correction 1 makes the exhaustive-evidence location accurate, and correction 2 preserves the uncertain enum. |
| Mild visible fire versus structural sufficiency | Correct. The report rejects a uniformly faint-looking description without asserting measured heat, member temperature, connection failure or sufficient conditions for the proposed sequence. It preserves the source's overlong floor-12 and shifted-history issues. |
| Strongest counterexample to dark-image inference | Correct. Figures 5-129/130 are one exposure with different representations. Both readers identify no luminous feature in the small wide image and warm features in the enlargement, with disputed morphology. The report expressly avoids treating this as a calibrated processing experiment or deception. |
| Dependent clocks versus fabrication | Correct. Fire/window comparisons and assumed duration/travel are treated as dependencies rather than independently timed validation; their existence is not called proof of false timing, fabrication or model failure. The optional table change removes residual ambiguity. |
| 25/26 gate failure | Correct. Figure 5-121 remains one unscored tiled representation. Full-page context does not cure the common-scale failure; no tolerance change or no-fire inference is claimed. The result is narrower than the original acceptance condition. |
| 51 representations versus exposures | Correct. The union is 25 prior plus 26 new figures, 50 standalone image assets and one failed tiled representation. Two known same-exposure pairs, shared sequences and ten repeated context assets remain dependencies. No 51-event or 50-independent-exposure claim appears. |
| Zero FA matches versus absence of useful evidence | Correct and explicit at lines 139-142. The report says zero complete matching comparisons were performed here, not zero relevant imagery or no pre-existing discrepancies. The seven inherited FA questions remain distinct from new Chapter 9 verification. Correction 3 keeps the conclusion consistent with this distinction. |
| Causal ordering | No new strict ordering, odds, equality of odds, demolition-first result, innocence/guilt or physical sufficiency claim is made. Correction 3 removes the only phrase that could suggest a completed failed validation test. |

## Actual verification and remaining limits

Read completely: `report.md`, `coverage-timeline.md`, `root-source-review.md`;
reviewed the timeline JSON's rows, counts, dependency groups, seven FA entries
and relevant semantics. The already completed critical review read both full
frozen observation files and source attributions, independently recomputed
the coarse comparison, and inspected 14 complete source pages after freeze.
That record is not expanded into a claim that this final pass independently
re-viewed all source pages or all earlier images.

`shasum -a 256` rechecked root/observer, protocol, source attributions and the
earlier critical review; all retained their reviewed pins. The report and
timeline pins below identify the exact reviewed versions. A final `jq -e`
assertion returned `true`, exit 0, for 51 distinct figures, 25 prior/26 new
membership, 50 rows with image records, only 5-121 in the representation-failure
state, two explicit same-underlying-photograph groups, ten context recurrences,
seven FA questions and zero nonempty match lists.

Two preliminary ad hoc `jq -e` expressions returned false because this reviewer
assumed nonexistent/shared enum names (`batch3` instead of `new26`, then one
common standalone-image representation name for both schema generations).
Inspection showed retained old/new representation names for the 25+25 image
rows. The corrected check used actual documented values and image presence;
no data, acceptance criterion or source label was changed to obtain the pass.

| Reviewed artifact | SHA-256 |
| --- | --- |
| `report.md` | `023315add842797c169daa74195290bfae74e807262c72d3c7ec0ae8f3ed4925` |
| `coverage-timeline.md` | `9f387e007e2cf2fc659c7c3074214c44b35b9bb91c45eb409d29bc98720ebce7` |
| `coverage-timeline.json` | `08141aa6d221f80bec33501761b5f19030706bb1e0badfd035375bcb93c73aab` |
| `root.json` | `e8e7b7d23e993c68ecc0ee0df16a39a9204d4b0665f9734e08096e21925044c5` |
| `observer.json` | `6c4021bd658cc7f7b64af061c320809cdec1cbe923803a690a12e13d0015e1ac` |
| `PROTOCOL.md` | `ecdd7be9123231e05217c456ebc5ffbaa71c7828802d1212e0ed26a784e559c6` |
| `observation-critical-review.md` | `ffc942eacbcb14bee47167bf8459ff0b8525237a2294875e97a704bbc99375c8` |

Root is still assembling validation/status files in parallel. This review
does not claim to have checked their finished versions or independently
validate the proposed next connection-calibration branch. That paragraph is
a prospective handoff with explicit prerequisites, not a completed result.
The current source-of-truth and evidence-audit boundaries remain intact.

## Correction recheck - 2026-09-24

I re-read the entire assembled `report.md` after root incorporated the three
required corrections and the optional timing clarification. Final reviewed
report SHA-256:
`0290f01755f6e3116b231c68caebff689c0a7048f02414455ba9e578a7b04407`.

All four corrections are present in context: exhaustive evidence is linked to
the full comparison and frozen records; facade association is contrasted with
uncertainty rather than a claimed foreground assignment; absence of independent
validation is not described as a performed failed test; and timing dependence
does not itself establish unreliable timing or intent. The assembled report
continues to preserve the nine shared/three disputed morphology counts,
coarse-versus-feature distinction, 25-of-26 representation limit, 51 figures
versus independent exposures, zero completed FA matches versus useful image
coverage, and the absence of a newly established causal ordering.

Result: the wording findings in this review are resolved. No additional
report correction was identified within this bounded review. This clears the
report as a faithful research summary within the acceptance scope stated
above; it does not satisfy the failed 26th representation gate, establish
physical or expert validation, or complete WP1/the investigation.

`shasum -a 256` confirmed both frozen observation records retain their prior
hashes: root `e8e7b7d23e993c68ecc0ee0df16a39a9204d4b0665f9734e08096e21925044c5`,
observer `6c4021bd658cc7f7b64af061c320809cdec1cbe923803a690a12e13d0015e1ac`.
No report, timeline, source or frozen label was edited by this recheck; no
imagery was re-annotated and no new media or Chapter 9 claim was introduced.
Root reports a successful independent join-checker replay; that is root's
verification, not an additional execution claimed by this observer.
