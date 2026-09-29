# Critical review of catalog-join synthesis

2026-09-19. Research-only textual review by Codex agent `/root/ap_catalog_source`.
This is a separate AI review of shared written records, not a new visual pass,
human review, independent historical source, or evidence promotion. The reviewer
previously performed this unit's AP catalog search; its AP assessment is
therefore a consistency check of its own earlier work, not a second independent
AP retrieval. Main repository controls, the charter and unit protocol remain
controlling. Evidence-falsification and source-of-truth skill boundaries apply.

## Assessment

The reviewed report supports a bounded advance: named catalog identities and
acquired byte streams, followed by two separate descriptions supporting a
scene/view family, more strongly for Figure 5-158 than Figure 5-157. The written
records do not support an exact still-to-frame join, uninterrupted sequence,
historical clock, six-second measurement, fire-severity assessment or causal
ranking change. The report generally preserves those distinctions. This
review does not independently confirm the visual correspondence; it checks
that the synthesis faithfully represents the two observers' stated results.

The initial pass identified three wording corrections and a document-state
check. **All three substantive corrections were verified in the revised report,
and validation.md was subsequently created and read completely.** The original
findings below are retained with a dated follow-up disposition at the end.
No remaining substantive objection was found within this assigned textual
review. Final repository/link checks were still to be appended to validation.md
at the follow-up snapshot; this review does not declare them passed. None of
the corrections supplies a reason to discard the recorded positive
orange/flame-like appearance or reverse the provisional scene-family result.

## Concerns and exact corrections

Line references identify the report snapshot pinned below. Root may be editing
the report concurrently; this note records concerns against that version, not
a finding that a later version retains them.

### CR-01 — Locate aspect/interlace metadata correctly

**Text:** report.md lines 81–82: “These PNGs retain the native 720×480 raster,
SAR8:9 and interlace flags”.

**Concern:** This wording makes the PNG files themselves sound as though they
preserve video sample-aspect and field metadata. FRAME-PLAN says native-size
RGB PNGs are produced, while sample aspect ratio and interlace flags are
retained as metadata without resampling. The observer attributes these values
to the plan/JSON. The subsequent method review likewise treats those values
as retained inventory/manifest fields. This review did not inspect PNG chunks
and has no basis to assert that their containers embed those video flags.

**Exact replacement:** “These PNGs retain the native 720×480 raster; the
accompanying metadata retain the source SAR 8:9 and interlace flags. No aspect
correction or deinterlacing was applied, and no geometric metric is inferred
from the displayed raster.”

**Confidence:** High that this correction more accurately states the declared
method. It does not allege that raster dimensions or source flags are wrong.

### CR-02 — Copyright erratum must also retract the insertion-stage claim

**Text:** report.md lines 93–96 correct the frozen root note's attribution of
the copyright label from Figure 5-158 to Figure 5-157. The frozen root note's
last paragraph also calls it “report-added”.

**Concern:** The corrected figure number agrees with observer-reference-freeze
R157-G and observer-samples R157-G. However, those records establish visible
raster text and its absence from the nine candidate samples; R157-G says the
label *may* be a later report overlay. They do not establish the stage at which
it was added. Leaving “report-added” uncorrected could imply an unsupported
report-production history. The existing caveat about camera ownership helps
but does not explicitly resolve that distinct assertion.

**Exact replacement for the erratum:** “Root-note correction: the frozen
note's last paragraph mistakenly attributes a copyright label to Figure
5-158; the observer records the visible Fox label in Figure 5-157. The same
paragraph's description ‘report-added’ is also unestablished: this review
does not determine when the label entered the image. Preserve the frozen note
and this explicit correction. The label is observed raster text, not a
physical landmark or proof of original camera ownership.”

**Confidence:** High for consistency with the written observer record. No
additional image inspection was performed to independently locate the label.

### CR-03 — Keep the positive observation distinct from its fire interpretation

**Text:** report.md lines 110–112: “the newly resolved positive visible-fire
evidence must not be discarded just because it does not establish severity
or mechanism.”

**Concern:** Root's freeze records orange forms; the separate observer records
a positive “visible flame-like appearance”. The report uses that narrower
language elsewhere but here states the interpretation as an unqualified
observation. Fire is a reasonable reading of the recorded appearance; this
is a precision concern, not a finding that the appearance is non-fire or a
request to omit it. The review did not assess alternative optical explanations
through a new visual or temporal test.

**Exact replacement:** “Conversely, the positive orange/flame-like appearance
recorded in these samples is consistent with visible fire and should remain
in the evidence account; it does not establish severity, duration or mechanism.”

**Confidence:** Moderate-to-high that the distinction improves faithfulness
to the stated observation layer. The main report already rejects inferences
about building-wide fire amount and collapse mechanism.

### CR-04 — Do not present a forthcoming validation summary as already reviewed

**Text:** report.md lines 33–36 say validation.md and method-review.md
“distinguish” the various verification/acceptance layers.

**Checkpoint:** An exact filename listing during this review found
method-review.md but no validation.md. The method review had appeared after
the initial file inventory, was then read completely, and supports its own
specific numerical/log-review assertions. The absence finding is limited to
that checkpoint, not a claim that root has failed to produce the document or
that it cannot appear during concurrent integration.

**Required resolution:** Before release, confirm validation.md exists and
accurately reports actual commands, diagnostics and outcomes, including Dub6
exclusion and the unmet human-review gate. If it remains pending, replace
the first sentence with: “The completed method review distinguishes repeatable
computational outputs from decoding fidelity and scientific acceptance; the
consolidated validation summary remains pending.” Keep the next sentence
stating that no scientifically consequential new measurement is accepted.

This critical review makes **no independent assertion that the original decode,
control, negative-test or validation commands passed**. It attributes such
results to the completed method review and does not rerun them.

## Checks with no substantive correction required

- **Catalog identity versus authenticity:** The report/source ledger preserve
  the Organized-category route, decline to borrow the separate Original Video
  from Tapes label, retain the retrospective request-receipt limitation and
  distinguish local hashes from provider checksums. The source reviewer states
  that copies, renaming or edits could satisfy those present-day checks. The
  reviewed synthesis does not promote them to original-camera custody.
- **Sparse scenes versus exact stills:** The two reference scenes are compared
  separately. The report preserves the incomplete R157 foreground comparison,
  unavailable diagonal band, different orange contour/crop/haze and stronger
  R158 correspondence. It does not turn missing anchors into positive matches
  or nondetection into proof of extinguishment. Tight-to-wide sample order is
  expressly distinguished from the order of the report's actual stills and
  uninterrupted recording.
- **Dub6 exclusion and reproducibility:** The completed method review reports
  repeated error concealment and explains why identical output is not decoder
  validation. The report excludes those products from visual findings. The
  phrase “cleanly decoded” for Dub5 should be read narrowly as no diagnostics
  in the inspected logs; it is not historical-source or full-decoder validation.
- **AP:** The result remains a current public keyword-search zero, with legacy
  or permissioned catalog availability unresolved. Root expressly did not
  independently reopen the AP UI. The source ledger's phrase “six exact queries”
  can be polished to “six public queries”: the AP ledger includes one
  catalog-focused metadata query without the number, not six exact-ID queries.
  This small wording issue does not change the bounded search result.
- **Internet Archive:** The report and ledger report metadata-only access and
  no scene-to-AVI or camera-clock join. The independent source review treats
  the 19:35:12 EDT addition as conditional on playback-zero alignment and no
  timing discontinuity, and keeps IA's “original” file field distinct from an
  original camera recording. No IA playback or local AVI corroboration is
  implied. “Stream-only” in the report's short table is less precise than the
  ledger's “stream/loan-only”; using the latter consistently would avoid
  unnecessary compression but does not alter the present access boundary.
- **Fire amount and cause:** The synthesis supplies no fire area, floor count,
  steel temperature, severity, pulse duration, mechanism or intent finding.
  Darker reference rendering is not assigned to deliberate exaggeration or
  accepted photometry. No causal alternative gains a new rank from this unit.
- **Review independence:** Separate AI observations over common supplied
  derivatives are identified as such. Prior root preview/knowledge, named
  candidate knowledge and the unmet human gate are disclosed. This review adds
  no independent camera, scene observation or human expertise.

The strongest remaining challenge is that a copied or edited clip from another
instant at the same camera position could satisfy the stated catalog checks
and broad scene geometry. Missing distinctive R157 detail and unmatched
contours support withholding exact-frame and continuity claims. The strongest
counterweight is the observers' described conjunction of roof-corner, upright,
railing and neighboring-facade relationships; the report preserves that useful
positive result with a narrower ceiling. Both aspects should survive revision.

## Actual scope, verification and version pins

Read report.md, source-ledger.md, FRAME-PLAN.md,
independent-source-review.md, root-samples-freeze.md,
observer-reference-freeze.md and observer-samples.md completely. Read the
subsequently available method-review.md completely. Prior AP review and
repository/skill/protocol reads were retained from this continuing lane.
Used `rg --files`, complete `cat` reads, numbered `nl -ba` reads for exact
locations, and `shasum -a 256` to pin the reviewed text. Aggregate outputs that
were truncated were followed by smaller complete reads. No image, source AVI,
transport header, or raw connector payload was newly inspected for this pass;
no media decoded or downloaded; no external research or send occurred. Only
this note was added. Findings do not silently alter either observation freeze.

| Reviewed text | SHA-256 |
|---|---|
| report.md | `1113b5d5ca0faf2e0a6f899f9888a78c8c12bfcc07582134275fa71abbfe7317` |
| source-ledger.md | `60db3a229ac235febd7a3e016307b3e39fbaf4520b8ff3e2ce613422ed997521` |
| FRAME-PLAN.md | `c5bc934477182bd6d9f85f893f9a57517090c5a3aa1d0492724f625cab9964af` |
| independent-source-review.md | `5e82ca34dca51175ff814ea04fbaad8e0a324257192a6e53b9d8bc62f78ae9fa` |
| root-samples-freeze.md | `6903c2091cfd452353b1c9ad37dbc86fd04fd278f40ea23301f6145d5fc6e843` |
| observer-reference-freeze.md | `826c186a422129ea74e1c37e8b18fd459306a3519af70fd12415cd930a8dfaf3` |
| observer-samples.md | `9771e69ee6e6a8c18f791278c9160da2aac9b3679cd5a72361a62088e075041b` |
| method-review.md | `3ab3592825a5c7324374ec82579020761e98690dd9ed692f3467183a1260221d` |

These pins identify reviewed local versions, not their historical truth or
the state of a subsequent root revision. The report should retain links to
this review and its correction dispositions when integration is complete.

## Focused follow-up: actual correction disposition

Later on 2026-09-19, root reported that it had incorporated the three substantive
wording corrections and created validation.md. This reviewer then read the
entire revised report and entire validation document, rather than relying on
that message alone, and computed their current hashes:

| Follow-up text | SHA-256 |
|---|---|
| report.md | `081948b5e2473416e3d9d38f92e65c58f5116d9a0fe1cca77598929f929af180` |
| validation.md | `3d8a689106bb93fdf8338df563cbd57e5fb8267388ac80379f9c93197158a571` |
| source-ledger.md, unchanged | `60db3a229ac235febd7a3e016307b3e39fbaf4520b8ff3e2ce613422ed997521` |

- **CR-01 resolved:** The revised report explicitly locates SAR and interlace
  flags in accompanying metadata and states no aspect correction/deinterlacing.
- **CR-02 resolved:** The revised erratum corrects the figure number and
  explicitly withdraws “report-added”, leaving insertion stage unknown. This
  is consistent with the observer's reference note; the root freeze remains
  preserved rather than rewritten.
- **CR-03 resolved:** The positive finding now says “orange/flame-like
  appearance”. It retains the observation without asserting severity or
  mechanism. It need not use this review's proposed replacement verbatim.
- **CR-04 resolved as a document-state concern:** validation.md now exists and
  reports actual root invocations, retained diagnostics, repeat/control totals,
  source-specific admission, the helper's limited pass flag, common-source AI
  reviews and the unmet human gate. Those reported totals and Dub6 diagnostic
  limits agree with the method-review text this reviewer read. It does not
  claim that refused products became admitted or that a scientific cause was
  determined. This is documentary reconciliation, not a rerun of its commands.

The follow-up validation snapshot ends by saying final legal-record and link
check results will be appended. Their completion was not observed by this
reviewer. The two low-impact wording suggestions about “six public queries”
and “stream/loan-only” remain optional clarity improvements at this snapshot;
neither changes the stated evidence ceiling or warrants reopening the source
or visual work. Later validation appendices and report/navigation changes are
outside the pinned versions above unless separately reviewed.
