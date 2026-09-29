# Bounded critical review of the integrated Tilted report

2026-09-19. Separate computational review, not external specialist approval.
No producer, data, image or main-repository file was changed. No calculation,
decode, visual inspection, physical fitting or external action was added.

## Scope and source versions

Read `report.md` completely, then checked its quantitative, coverage and
independence claims against the complete independent scene review, both table
reviews, the complete saved export review, source-semantics review, visual
coverage note and frozen table declaration. The first batched source-semantics
display was truncated; that full review and declaration were reread in a
bounded response before reliance. The scene reviewer has independently
reproduced its own numerical lane; it relies on the completed table reviewer
for that lane rather than treating report repetition as a new computation.

Reviewed document pins:

| Document | SHA-256 at this review |
|---|---|
| `report.md` | `6c38538288169a018de18945305f51193f4c65aa6cbf1d11a58fcb2e21b0f5cd` |
| `scene-independent-review.md` | `021a5bfc32c30fd8da64dba3f4d8d47582ad188ad47f7fb2f126d2a765c2cb74` |
| `project-table-review.md` | `f66f1805d2427c8f72c97d96765971d53c2ff1393da3e2b673e381309d103f67` |
| `table-independent-review.md` | `0892372a2f1a701e8103c61cdc263eba3c16a91e7ae48c5ea53d2d61c5d71d12` |

The known pending `validation.md` link is allowed during integration and is
not a substantive defect. Final delivery should resolve it. The older
project-table note's explicitly versioned pending-independent-review statement
does not defeat the later completed independent receipt; preserve that history
and make its later completion discoverable through the current report.

## Outcome and smallest corrections

No numerical contradiction, source-count error, concealed PM05 failure,
causal ranking or claim of independently validated physical units was found.
The following two bounded wording corrections improve the reviewability of the
report without changing any result or enlarging the declared work.

1. **Partial table coverage in the opening result.** At report lines 13–14,
   “five of 48 tested series pairings reproduce all available published
   position changes within printing limits” can be read as all published
   rows for each passing series. The table has 70 rows, whereas PM06 has only
   16 shared finite comparisons and PM08 has 40. The next paragraph and later
   table disclose this correctly, so this is an ambiguous headline rather
   than hidden data omission. Replace with: “five of 48 tested series
   pairings pass every shared finite position-change comparison within the
   declared printing enclosure.” Keeping the nearby partial-coverage sentence
   prevents a displacement pass from becoming full-table reproduction.

2. **Separate discrete exact agreement from floating tolerance.** At report
   lines 181–184, “agrees on all 668 coordinates, 1,512 absolute residuals,
   1,512 displacement residuals, 3,462 normalized row states and 48 pair
   summaries within the declared 1e−9 bound” applies one numerical qualifier
   to both numbers and categorical states. The independent table review
   establishes exact row-membership/state and decision agreement; only
   numerical values use tolerance. Replace with: “The separate determinant-
   inverse/rational-arithmetic implementation reproduces all 668 coordinate
   values, 1,512 absolute residuals, 1,512 displacement residuals and numerical
   summaries for all 48 pairings within the declared 1e−9 bound. All 3,462
   normalized row states and every enclosure decision agree exactly.” This
   keeps tolerance from appearing to permit a membership or decision error.

An optional scope refinement is useful at lines 208–214. “Before independent
physical fitting, resolve the saved-versus-published input relationship” is a
reasonable chosen next step for reconstructing the publication, but it is not
a universal scientific prerequisite for a separate, newly calibrated motion
study. If the intended dependency is only the former, begin “For further
reconstruction of the published analysis, resolve…” and retain the following
independent-calibration and human/specialist conditions. This does not authorize
new fitting or relax the charter; it avoids treating one unresolved derivative
lineage as a necessary input to every independent observation route.

## Claims that survive adversarial review

- **Scene arithmetic and coverage:** 8 × 701 × 3 × 4 = 67,296 paired metric
  comparisons; 96 complete rankings; 24 full-scene selections; the listed
  source indices, unique interior minima, adjacent runner-ups, minimum gap
  0.0130 and 4.60×10⁻¹³ correlation difference agree with the independent
  review. The eight-query/nine-candidate visual coverage matches the root
  coverage record, including redisplay after a truncated attempt. This
  reviewer did not personally view those images and makes no independent
  visual endorsement. “No single recovered, globally exact frame offset”
  describes what these sampled matches recovered; it should not be expanded
  into proof that no such relation could exist elsewhere in the clip.
- **Dependence:** The report expressly treats NEAREST/BOX as redundant on
  the retained grid and identifies shared Pillow, inputs and grid. It correctly
  calls the separate scene calculation independent arithmetic rather than
  independent visual authentication. Independent code does not supply a second
  acquisition or independent dimensional calibration.
- **Saved domain and PM05:** 334 rows, eight tracks, selected frames 0,6,…,474,
  80 selected steps and playhead 258 agree with the export/source reviews.
  PM05 has 43 saved rows and eight keys, with all 35 nonkeys preceding the
  first surviving key. “Not interpolation between those surviving keys
  alone” is supported; “not interpolation” without that limitation would not
  be. The report retains 32/43 compatible displacement rows, 11 failing
  nonkeys, their frame indices and maximum 0.230452 residual. It does not
  replace the all-row test with the eight passing keys.
- **Nominal versus strict time:** The zero-pass claim is explicitly limited
  to all 1,512 shared finite publication comparisons, which reuse source rows.
  It preserves the five later PM02 rows whose own nominal times pass outside
  the printed table. It does not claim all 334 rows fail. Current-PTS/U equality
  is conditional on loaded endpoints 0 and 474 and does not authenticate the
  historical Xuggle array. This is consistent with both table reviews.
- **Available, missing and failed pairs:** The five passing displacement
  pairs, their counts/offsets/maxima and separate absolute-position failure
  agree with both table reviews. Three unavailable pairs remain unavailable,
  not successes. The other 40 fail at least one displacement enclosure. The
  common first-row subtraction is declared and its automatic zero residual
  is not counted as independent validation. Assigned units are not promoted
  to validated metres.
- **Strongest alternative and negative claims:** Shared or edited source
  ancestry can produce numerical agreement while preserving common marking,
  projection, scale or clock errors. A different project/version/settings
  can explain retained discrepancies. Neither is uniquely selected. The
  report preserves absolute-position mismatch, strict-time mismatch and PM05
  all-row failure as counterevidence to an exact saved-project/publication
  reconstruction, without calling discrepancy fabrication or rejecting the
  physical movements. It does not infer a collapse mechanism, probability
  ordering, equal odds or intent from these results.

## Verification record and limits

Actual checks were complete Markdown reads (`cat`), numbered-report inspection
(`nl -ba`) and SHA-256 pinning (`shasum -a 256`), followed by textual comparison
against the completed independent reviews. No arithmetic was rerun for this
critical pass, and no unrun check is described as successful. The main
investigation charter, evidence separation and existing review limits remain
controlling. This memo records recommendations against the pinned report
version; it does not claim root has already applied them or completed the
separate final validation document.

## Explicit integration recheck

The end-of-review pin check detected revisions to `report.md` and
`project-table-review.md`; neither changed document was silently substituted
for the reviewed snapshot. Both revised documents were then read completely.

- Revised report SHA-256
  `e1d0900b5d9c7ebec4dfd45322ef346a595ebb1c3cc8cc00f19e68f059ca65ac`
  applies both numbered corrections: the opening says “every shared finite
  position-change comparison,” and categorical states/memberships/rounding
  decisions now agree exactly in a sentence separate from numerical tolerance.
  Both concerns are resolved in this version; the optional next-task scope
  refinement remains a recommendation rather than a failed arithmetic gate.
- Revised project-table review SHA-256
  `5dd1f04ecaa7d29f9bdb1191a3ae940200cb4b0957963ec6cc1057d4aba2ea39`
  records the completed independent comparison, actual rerun and review-version
  history. The two independent review hashes remain unchanged.

This recheck found no new quantitative or inferential issue. It does not claim
to verify edits made after these exact versions or the separate validation
file being prepared by root.

### Optional dependency wording resolved

Root then requested a check of its further final-section revision. Read report
lines 198 through EOF; current report SHA-256 is
`c1851faca025c31edc6ac6d660f5edf2fa97ff569a750f3846b18d783890ce38`.
The next-task paragraph now begins “For further reconstruction of the
published analysis,” and the following paragraph expressly states that new
independent measurements need not await complete reconstruction of the paper's
editing history. Independent endpoint/feature identity, dimensional reference,
aspect/projection, uncertainty and charter human/specialist conditions remain.
The optional dependency concern is resolved in this version. All three review
recommendations are now addressed; no new producer, data or numerical check
was involved in this final-section wording verification.
