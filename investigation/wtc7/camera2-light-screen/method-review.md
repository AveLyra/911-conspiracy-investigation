# Independent method preflight: full-native Camera2 light screen

2026-09-24. Before historical page presentation. This review concerns the
declared workflow, presentation geometry and observation boundaries, not a
historical light finding, detector validation or human acceptance.

## Disposition and scope

The complete frozen `PROTOCOL.md` was read. Its supplied SHA-256 is
`8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25`;
the current source pin is checked below before closing this preflight.
Main CHARTER remains controlling, SHA-256
`54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
The evidence-falsification and source-of-truth disciplines separate source
integrity, presentation verification, qualitative observation and acceptance.

**The workflow is proportionate and methodologically admissible for a
qualitative candidate screen**, conditional on the still-required producer,
synthetic, complete pixel/order and actual display checks. It does not complete
an optical detectability model or supply negative evidence against a mechanism.
The previous eight-still pilot addressed spatial access only; a declared
all-frame temporal screen is a distinct unfinished task, not another repetition
of that pilot or the closed penthouse-outline zoom test.

At this preflight no producer, historical presentation pages or new primary
observation records existed in the scoped listing. No such page or observation
was read here. No external source, source video, image or private record was
opened, and no historical time, intensity or motion arithmetic was performed.
Only this method review is authored by this reader.

## Requests incorporated before execution

The reviewer raised these requirements while the protocol was being written;
the frozen protocol now includes them:

1. A reader other than every primary reader performs the fixed second sample,
   before seeing primary findings. Reader C is assigned all 15 fixed pages.
   This is a fixed reannotation sample, not complete paired coverage or random
   accuracy estimation.
2. A block's first frame and an isolated second-read page's first frame lack
   incoming preceding-frame context. They are U/context-only for that incoming
   transition, with spatial description and in-scope following context retained.
   This U must not be confused with an image/region-assessability failure.
3. Page overlap is context, not independent votes. Preserve the earlier row and
   any later changed judgment. The preceding reader's boundary row is not
   silently replaced by the following reader's context-only U.
4. Six images are presented together. Save all six rows before the next page;
   do not claim each row was saved before seeing the next frame on its page.
5. Original-detail presentation and actual readability are required, not merely
   an assertion that the saved contact sheet has native-sized image rectangles.
   A failed/unreadable display is not screened coverage.
6. One-frame candidates remain eligible; persistence is not a gate. The final
   source frame has no later in-scope neighbor, so a candidate there remains
   right-censored. The first source frame similarly lacks prior context.

No executed historical result motivated these corrections. Source/implementation
coordination may continue, but new substantive first-pass findings must remain
unexchanged until all primary records are frozen. Reader C must also freeze its
record before receiving primary outcomes.

## Independent layout/index check

A source-independent JavaScript calculation, evaluated to stdout only, formed
84 arrays of six integers with `6593 + 5 * page + offset`, offsets 0–5.
It checked the proposed layout indices, not pixels or physical event times.

- The first page is 6593–6598; the last is 7008–7013.
- All 421 integer indices 6593–7013 occur, with no gap or extra index.
- The 84 pages contain 504 image presentations, at most two presentations of
  any one source index. Repeats do not create new exposures.
- Primary blocks 0–27, 28–55 and 56–83 each contain 141 unique source indices;
  their ranges are 6593–6733, 6733–6873 and 6873–7013. The cross-reader
  overlapping indices are 6733 and 6873.
- The fixed repeated pages are
  `0,6,12,18,24,30,36,42,48,54,60,66,72,78,83`, containing 90 unique source
  indices. Their first-frame incoming transitions do not have equivalent
  preceding context to the continuous primary reads. Thus this is not 90
  independently equivalent temporal-transition checks.

These counts are presentation bookkeeping, not historical measurement or
statistical evidence. Two columns of width 640 and three rows of image height
480 plus an external 24-pixel strip imply the declared 1280x1512 canvas. The
actual producer must still prove every image rectangle and label boundary.
Row-major order must remain clear: left then right, followed by the next row.
All adjacent source pairs are included together by the declared stride-five
layout, but that design does not guarantee a reader detects their differences.

The exact index check used the following independent construction:

```javascript
const pages = Array.from({length:84}, (_,p) =>
  Array.from({length:6}, (_,j) => 6593 + 5*p + j));
const counts = new Map();
for (const i of pages.flat()) counts.set(i, (counts.get(i) || 0) + 1);
const repeated = Array.from({length:14}, (_,j) => 6*j).concat([83]);
const missing = Array.from({length:421}, (_,i) => 6593+i)
  .filter(i => !counts.has(i));
```

The reported lengths, endpoints, maxima and sets were printed from these
arrays. No files were generated by that check. Read commands were bounded
`sed`, filename-only `rg --files`, and `shasum`; initial reads of the not-yet-
created unit returned missing-path errors, not scientific failures or evidence
that source images were missing. The complete protocol was read after creation.

## Observation and acceptance cautions

C/N/U are observer dispositions. A C can retain an ordinary or processing
alternative without being erased by that alternative. An N means no additional
conspicuous candidate noticed, not a proved lack of light changes. The phrase
"ordinary scene evolution" must not become a rule excluding a plausible
ambiguous candidate merely because cloud, moving edges, reflection or exposure
could account for it. Conversely, every slow cloud movement need not be called
a physical luminous event. State the visible appearance and uncertainty.

Spatially hidden regions remain unobserved even when a frame's visible portion
gets N. Light/color/radiometric information discarded or altered by the source
chain is not restored by full-resolution display. Encoded PTS locates an access-
copy frame, not original shutter integration or continuous capture. No assumed
flash duration, detector sensitivity, event frequency or causal weight follows.

After freezes, the fixed-sample comparison must preserve different context
availability, salience thresholds, location descriptions and changed judgments.
Agreement is not sensitivity or accuracy. Candidate/context follow-ups selected
because of first-pass outcomes are prior-informed and separately declared, not
additional blinded replications. Any material disagreement left unresolved
must remain explicit; it cannot be repaired by post-result threshold tuning.

The acceptance requirement for all 84 primary and 15 fixed secondary pages
is substantive. A missing page, unreadable native detail or unfinished block
prevents the claimed complete screen. A completed screen still is not human
review, an authenticated physical flash finding or an absence-of-charges test.
Actual human and appropriate synthetic ground-truth prerequisites remain
before consequential automated measurement, not only before later causal use.

## Reader C independence disclosure and current gate

This reused reviewer has read the prior spatial pilot's two frozen records
and synthesis, Camera2 roof-event source/method reports and the present design.
Previous unit work includes source/provenance, representation and mathematical
checks. It has not viewed this unit's historical pages or read new primary
screen results. Complete prior nonexposure across older context cannot be
certified. The later fixed-page reading, if authorized after presentation
clearance, is prior-informed separate reannotation, not numerical/scene
blindness, an independent camera or human/expert review.

Current disposition: **method preflight satisfactory; source/presentation
implementation clearance and all historical page reading still pending**.
