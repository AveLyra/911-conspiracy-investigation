# Stage B post-freeze exchange review

September 20, 2026 UTC. Written by the separate Stage B observer after root
explicitly confirmed its own freeze and authorized exchange. This is a
cross-record critical review by one of the two annotators, **not a third
independent visual review**. No new image viewing, extraction or transformation
was performed in this task. Both original observations and scope notes remain
unchanged.

## Verified freeze identities

A fresh `shasum -a 256` read returned the following values, exactly matching
the pre-exchange hashes supplied in the coordination messages:

| Frozen file | SHA-256 |
|---|---|
| root-stage-b.md | c01c9fe3628fae76417d11c166f5981706162c93362984c6114157a6a70e2bbf |
| root-stage-b-scope.md | 3135cf7600ab4b9cef7a60adef238cf653ce38a71fe7af64f54b98b3254124c3 |
| observer-stage-b.md | cea1a9c0db50d0ece47ceb19a877f97977d8348e47c61a84fc630ce5c54a6da5 |
| observer-stage-b-scope.md | 9794d0e106f87bdb0a8783c559992ec62757c9088ba993dd8d5a6da48e13809d |

Both root records were read completely after this check. The observer's own
records and the complete controlling `STAGE-B.md` had already been read/written
before exchange. Hash agreement preserves the stated freeze contents; it does
not itself prove blinding, reviewer competence or source authenticity.

## Agreements and retained differences

| Item | Root frozen annotation | Observer frozen annotation | Review |
|---|---|---|---|
| East last confident visually unchanged | 6701 | 6707 | Different resolvability judgments; not evidence that the physical object was both moving and stationary |
| East first confident lowered profile | 6717 | 6714 | The observer is less conservative about the first clear change |
| East ambiguous run | 6702–6716 | 6708–6713 | Observer's entire bracket is nested in root's bracket |
| Two following persistence frames | 6718, 6719 | 6715, 6716 | Both are the actual following two stored indices; all were viewed natively by both observers |
| West last confident visible associated remnant | 6958 | 6958 | Exact agreement on a conditional component identification |
| West confident below/behind-parapet state | None | None | Both censor the endpoint rather than promote nondetection |
| Finite complete elapsed interval | None | None | Neither record establishes an upper endpoint |

The pre-edge disagreement is 604/2997 s (about 0.202 s); the positive-edge
disagreement is 100/999 s (about 0.100 s). These are observed differences
between two annotations, not estimated population error rates or added
independent clock uncertainties. Their agreement on 6958 is useful
repeatability evidence for this procedure, but both used the same pixels,
source-informed identities and broadly similar AI reasoning. It does not
independently authenticate the roof component or eliminate shared bias.

## Independent arithmetic check against the held selection metadata

Actual read-only calculation command used:

`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -c '…'`

Working directory was the research worktree. The inline program loaded only
`run01/camera2/selection.json`, indexed its `images` entries by
`frame_index_zero_based`, and used Python `fractions.Fraction`. It independently
asserted source PTS, timebase 1/2997, exact stored-time agreement, coverage-set
sizes and membership, following-two-frame indices, nested east brackets, both
elapsed lower bounds and their conservative envelope. No image was opened
or decoded by the calculation. The actual terminal returned **exit 0/PASS**.

| Frame | Source PTS | Exact seconds recomputed as PTS/2997 |
|---:|---:|---|
| 6701 | 670100 | 670100/2997 |
| 6707 | 670704 | 223568/999 |
| 6714 | 671403 | 223801/999 |
| 6715 | 671503 | 671503/2997 |
| 6716 | 671603 | 671603/2997 |
| 6717 | 671703 | 223901/999 |
| 6718 | 671803 | 671803/2997 |
| 6719 | 671903 | 671903/2997 |
| 6958 | 695804 | 695804/2997 |

All exact fractions and displayed decimals in the two observations agree
with these recomputations at their stated precision. The checked consequences:

- Root east bracket width: `1603/2997 = 0.534868201535… s`.
- Observer east bracket width: `233/999 = 0.233233233233… s`.
- Root conditional elapsed lower bound:
  `(695804 - 671703)/2997 = 24101/2997 = 8.041708375042… s`.
- Observer conditional elapsed lower bound:
  `(695804 - 671403)/2997 = 24401/2997 = 8.141808475142… s`.

The **east union envelope** is root's wider bracket:
`[670100/2997, 223901/999]`, about **223.5903–224.1251 encoded seconds**.
The corresponding conservative elapsed envelope has lower edge
**24101/2997 s, about 8.04 s, and no finite upper edge**. It is conditional on
the shared feature/event association and the access-copy clock. Do not average
the bounds, use their intersection as the combined uncertainty, choose the
later first-positive frame as the onset itself, or assign a finite west bound
at 6967/7013. Exact fractions make arithmetic reproducible; they do not give
the visual measurement twelve-decimal precision.

Native coverage-set arithmetic also passes: root reports 151 unique frames,
observer reports 170, their intersection is 99 and union is **222**, not 321.
Both viewed the 421 selected frames only at overview scale. This review checks
the recorded coverage lists and endpoint/persistence membership, not root's
complete original display history. Root-only context such as 6784 is not newly
visually verified by this reviewer. Repeated source frames, duplicate extraction
runs and shared thumbnails do not add independent historical observations.

## Fit to the prospectively declared definitions

**East:** both identify a left rooftop material-associated contour relative
to adjoining roof/facade context, distinguish it from an upper smoke margin,
and require persistence in the next two stored frames. Both retain every
intervening ambiguous index and expressly deny subpixel physical stillness.
Neither supplies calibrated point tracks or a measured camera-motion transform;
their rejection of whole-camera translation is a differential-geometry
inference. That is appropriate to the limited declared conditional visual
test, but not a replacement for WP2's eventual calibrated motion work.

**West:** both use the contemporaneous moving/deforming local parapet rather
than the baseline's fixed height. Both distinguish the small raised endpoint
from the far-right exterior corner and decline to substitute screenwall loss,
first motion or complete physical roof penetration for the specified event.
Both lack a confident post-state plus two confirmations and correctly refuse
to let three persistent nondetections satisfy that requirement. The censored
result is explicitly permitted by `STAGE-B.md` and is not a failed extractor.

**Remaining interpretive vulnerability:** the positive 6958 annotation still
depends on the remnant actually belonging to the west-penthouse assembly.
The exact penthouse/screenwall/parapet junction was never authenticated at the
pixel level. If the remnant is another structure or a bending parapet, the
conditional lower bound would not constrain the intended west event at all.
Both freezes state this, and a synthesis must keep it attached to the number.

The onset records describe observable first-clear change, not the first
physical motion. For a lower-bound argument, earlier undetected east motion
would lengthen the true elapsed interval, not shorten it, **if** the visible
change belongs to the same east event and 6958 is genuinely pre-disappearance
for the intended west structure. These assumptions are the real limitation;
the exact rational subtraction does not independently establish them.

## Strongest objection and synthesis discipline

The strongest objection to treating agreement as a decisive result is shared
component aliasing: two prior-informed AI reviewers can consistently choose
the same wrong small rooftop remnant. A qualified source/geometry review or
clearer original footage could disconfirm that association. The strongest
objection to censoring is the reverse: both reviewers may be overly conservative
and miss a genuinely traceable crossing in the same native pixels. Agreement
therefore establishes neither a timing discrepancy nor the impossibility of
recovering a timing interval.

The current bounded test yields a conditional lower constraint and a specific
visibility/identity limit. It has not independently reproduced the reported
finite distant-view interval, and it has not refuted it. “Not reproduced” must
not be rewritten as “contradicted.” Conversely, censoring does not erase the
positive observed sequence or make the conditional one-sided result zero
information. Any later comparison with published model times needs an explicit
event/view correspondence and must keep source-clock and identity limitations
visible; this record performs no causal comparison or ranking.

No unannounced visual threshold was changed to harmonize the records. Preserve
both original east brackets and both one-sided results. A further display-aid,
source-quality or qualified-review pass should be separately declared around
the exact disputed contours and report whether it changes identification,
not silently replace either freeze. Human/specialist acceptance and research-
to-legal/engine promotion remain separate gates.

Only this exchange-review file was written in this task. No source, image,
code, receipt, original annotation or scope note was modified; no new viewing,
outside retrieval, solver, publication, commitment, filing or push occurred.
