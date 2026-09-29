# Frozen-record cross-review of the batch-2 report draft

2026-09-16. Bounded review by `/root/fire_batch2_visual`, after both raw observation records froze. No labels were relabeled or reconciled, and no new images were opened. This review checks portrayal of observations and disagreements, not source-attribution accuracy or the separate numeric verification.

Reviewed draft snapshot `report.md`: SHA-256 `bee7e892f63f06dc789352f2262def0d12d91ed67e8487ec6872ecebbe604a4b`. Root was editing the draft during this review; line references and quoted wording refer to that snapshot.

Frozen inputs:

- `main.json`: `63100450901d2358ee14f253a95b154f038091a88e0d3cf1c81e56126a0c2c2b`
- `reviewer.json`: `2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7`

## Findings and corrections

1. **Severity wording should remain explicitly unmeasured (draft lines 16–23).** “They do not support a blanket description of all visible fires as tiny or merely mild” is vulnerable to being read as a positive severity/size judgment, although the next sentences expressly deny thermal measurement. The frozen schema records morphology and visibility, with no calibrated physical extent or severity variable. This is a wording risk, not a contradiction in the raw records. Suggested replacement: “The records contain resolved flame-like morphology as well as ambiguous glow, local nondetection and extensive obscuration. They provide no calibrated classification of physical fire size or severity, so neither ‘all tiny or mild’ nor severe interior heating follows from the imagery alone.” Preserve the existing temperature and structural-capacity limits.

2. **Keep glare provisional in 5-157 (draft line 77).** “Root treats it as glare/highlight” is stronger than root's frozen wording, which says the bright strip “may be glare or another surface” and leaves it unlisted. Suggested wording: “Reviewer records the smooth bright edge as ambiguous glow; root leaves it unlisted and considers glare or another surface plausible.” Neither record settles the emitting surface or mechanism. This row should also expose its smoke-status difference: root uncertain, reviewer visible.

3. **Clarify unequal feature-region scope in 5-126 (draft line 75).** The current summary is broadly faithful, but “both luminous clusters flame-like” can imply an exact same-region morphology disagreement across the entire smooth right portion. Root's second locator `[177,82,294,118]` includes irregular internal contours “especially toward its left”; reviewer splits a flame-like region `[105,82,218,115]` from a smooth ambiguous region `[219,87,296,117]`. Suggested wording: “Root's broader right-hand flame-like locator includes irregular contours especially on its left; reviewer separately marks its smoother right portion as ambiguous glow.” Preserve smoke uncertain versus visible. Neither broad rectangle labels every pixel or establishes uniform burning.

4. **Make the 5-158 localization difference fully explicit (draft line 77).** The current sentence correctly states root's unresolved target and the uncertain luminous target relation. Add that reviewer locates only a limited candidate wall. Both luminous features have `target_relation: uncertain`; the reviewer locator does not establish the true building, opening or depth. Suggested wording: “Root cannot localize the target securely; reviewer localizes a limited candidate wall, while both retain uncertain attachment of the luminous feature.”

## Requested cases that are accurately preserved

- **5-114 / A-ffe3726a0312:** Root's `ambiguous_glow` / `limited_detail` and reviewer's `flame_like` / `partial_detail` are correctly stated. Locators `[212,162,240,248]` and `[213,164,238,248]` support “same approximate edge region.” The caption is not used to settle the disagreement.
- **5-135 / A-69d899e75343:** Both upper edge features are flame-like. Both small lower patches are ambiguous glow, with root assigning candidate-facade relation and reviewer retaining uncertainty. Both cropped bottom strips are flame-like with uncertain target relation. Root has limited detail/no nondetection patch; reviewer has partial detail/one bounded patch. The draft preserves these differences and does not assign the bottom strip to WTC 7.
- **5-61 / A-f1e2fa01e344:** Root has unresolved target/null locator and no nondetection; reviewer has a limited candidate and one bounded dark-grid nondetection. Both have empty luminous lists and visible smoke. The draft accurately treats candidate localization as disputed rather than treating the reviewer locator or source guide as authenticated geometry.
- **5-157 / A-7b61385d1373:** Neither record has flame-like morphology. Reviewer's ambiguous glow remains uncertain in target relation and explicitly allows reflection, glare, clipping and unresolved-source alternatives. Apply finding 2 to avoid turning root's alternative explanation into certainty.
- **5-158 / A-8bc36f05fe38:** Both record flame-like morphology with uncertain target relation and uncertain smoke. Root's null target and reviewer's limited candidate remain materially different even though the luminous-presence field agrees. Apply finding 4 for a complete portrayal.

## Coarse comparison meaning

The six jointly flame-like images are A-9e7b4935c8aa, A-0e60b82a1a4c, A-6902e91e39ee, A-671f312eade8, A-69d899e75343 and A-8bc36f05fe38. Their agreement is at the image-level presence field. It does not require identical boxes, feature counts, target relations or alternatives and does not validate physical identity. The report explicitly states these limits, and its claim ledger assigns grade A only to the fact of the recorded judgments while keeping the physical emitting-flame interpretation at C.

The stated 17 differences concern five coarse fields across 13 images: target evaluability, smoke status, presence of ambiguous glow, presence of flame-like morphology and presence of nondetection regions. The reported category breakdown is consistent with the field values inspected. Root's independent numeric checker owns exact reproduction; this note does not replace it. The report correctly calls these descriptive bookkeeping rather than an accuracy rate, detector calibration, source-event count or physical sample size.

Equal coarse fields can conceal consequential differences. The report correctly identifies the extra small upper-left ambiguous forms in 5-125 and retains the original locators/reasons rather than substituting a consensus record. Apply the localized wording fixes above; no frozen-record amendment is warranted by this cross-review.

## Localized correction disposition — 2026-09-16

Verified the four requested corrections in `report.md`, SHA-256 `737245b4e522ddd9dae0fd39c64e451184ac1070773819bcbf1aa112830b49bc`. This disposition is limited to those passages; the original reviewed snapshot and findings above remain preserved.

1. **Severity wording addressed.** The replacement describes irregular luminous forms consistent with flames and expressly retains the absence of interior-extent, heat-release, temperature and structural-capacity measurement. It no longer rejects a physical size/severity category on the basis of morphology alone.
2. **5-157 provisional glare and smoke disagreement addressed.** Root leaves the bright edge unlisted with glare or another surface plausible. The report now explicitly states root's uncertain smoke versus reviewer's visible smoke.
3. **5-126 unequal region scopes addressed.** The text identifies root's broader second locator, its irregular contours especially toward the left, reviewer's separate smooth-right ambiguous glow, and explicitly says the region scopes are not identical.
4. **5-158 localization disagreement addressed.** The report now distinguishes root's unresolved target from reviewer's limited candidate wall while retaining uncertain luminous target relation in both records.

All four localized findings are addressed. No additional images, source-attribution audit, numerical reanalysis or general report recertification was performed in this follow-up. `main.json` remains `63100450901d2358ee14f253a95b154f038091a88e0d3cf1c81e56126a0c2c2b`; `reviewer.json` remains `2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7`. Neither frozen record was changed.
