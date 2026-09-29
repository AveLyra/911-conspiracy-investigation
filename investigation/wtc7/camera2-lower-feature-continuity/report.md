# Camera2 lower junctions: a sampled visibility limit

2026-09-24. Research-only result under the main investigation charter.
[Protocol](PROTOCOL.md), [root observations](root-observations.md),
[separate observations](observer.md), [all-pair comparison](comparison.md),
[source/presentation verification](verification.md).

## Result

**The lower central junctions do not automatically provide a longer usable
point record than the previously studied upper rooftop corner.** They are
visible candidates in early selected frames, but their step-like appearance
becomes shallow and merges with the roof outline. The image-right outer corner
remains distinguishable considerably later in this sample. This is a useful
constraint on which observable to measure, not a failure-time or cause finding.

Both readers identify the lower-right junction (source label WC) in the first
eight selected frames through6946, but both already mark its correspondence
uncertain at6946. Neither identifies a distinct WC candidate at any selected
frame from6961 onward. For the lower-left junction EC, both identify a distinct,
appearance-consistent candidate only at6841,6886,6916. Borderline EC positives
at6751 and6931 are disputed. These statements concern the exact sparse sample;
they are not exact first-loss times or evidence that the physical points ceased
to exist.

| Source-labelled appearance | Common positive result | Important limit |
|---|---|---|
| NE, image-left outer corner | Distinct candidate in both readings at6916,6931,6946 | Observer retains uncertain correspondence throughout; earlier/later smoke prevents a continuous identity claim. |
| EC, lower-left step foot | Both V/appearance-consistent at6841,6886,6916 | Earlier/later borderline candidates disagree; neither accepts a distinct candidate from6946 onward. |
| WC, lower-right step foot | Both V through6946 in the fixed sample | Same-feature interpretation uncertain at6946; no distinct candidate in later selected frames. |
| NW, image-right outer corner | Both V through7051 | Observer marks7051 correspondence uncertain; both lose the candidate at7081 and7104. It is not a stationary camera reference. |

Compass names are the prior source's labels, not independently established
member or material identities. Lower WC is not the old upper endpoint T2.
No old T2 coordinate, motion calculation or disappearance was transferred.

## Coverage, disagreements and reproducibility

Each reader viewed all17 complete native640x480 grayscale images and all17
existing unmarked panels. The fixed schedule and exact encoded PTS are in
the protocol and verifier. This is34views per reader of17source frames,
not34independent exposures. Familiar imagery and source labels make the
review retrospective, not an unused holdout. Neither reader is a human or
qualified engineering/forensic reviewer.

Both68-row records were saved before substantive exchange. Root froze at
SHA256 `87b63db5bac9008431c16b102422f7102cb84e1b71759379f7ceaf935cc88128`;
observer at `97e9f2f6a01c0e0a35b08ba4fc274710a7b62d81a2dac7ae1db4131eabd7eb8d`.
No annotations were revised to force agreement. The complete68-pair table
matches both originals in a root programmatic check.
An independent read-only parser separately reproduced all68 keys, all18
different pairs, all strict agreement counts, and every common-positive list;
both frozen hashes remained unchanged before and after that check.

Strict visibility labels agree in56pairs, correspondence labels in53, and both
fields in50. These are counts, not accuracy estimates. Three visibility
disagreements concern borderline positives. Nine are later central-target
U/A differences: root records the defined junction unavailable; the observer
records a visible host roof region with changed silhouette. The schema leaves
some overlap between those descriptions. Both reject a distinct V candidate
in those nine pairs, but the raw disagreement remains. Different correspondence
judgments at NE and late NW are also preserved, not overridden by a majority.

The independent source verifier checked all17 native images, exact frame/PTS
joins, native luma hashes, and every image-region sample in all17 panels:
28,698,975 RGB channel samples matched. Saved synthetic source/panel geometry
also passed. All59 input pins remained unchanged. Root independently checked
the17 crop/resize relationships, then executed the verifier's complete saved
read-only replay successfully. This is numerical/presentation verification,
not physical validation of an observer's feature identity or the original clock.

The preserved source is an explicitly converted, secondary-hosted access copy.
No selected luma duplicates were found; saved map hashes distinguish each
selected frame from its immediate predecessor. Unselected intervals, edits,
near-duplicates, exposure history and original recording authenticity are not
thereby cleared. No video was newly decoded in this unit.

## Claim ledger and strongest contrary reading

| Claim | Layer / support | What could change it |
|---|---|---|
| Distinct lower-step candidates exist in the early sample. | Visual observation, supported within the stated two-reader coverage; not a physical survey. | Better source detail or a documented competing feature identity could revise the selections. |
| The same two lower junctions can be followed throughout the visible descent from these appearances alone. | Not established; the declared features merge/are obscured in later samples. | Source-linked texture, persistent junction geometry, exact saved-point definitions or better footage might establish a longer defensible observable. |
| The right outer appearance remains a distinguishable candidate in later selected frames than the central step-foot appearances. | Supported for this fixed sample; last-frame correspondence remains disputed. | A demonstrated silhouette switch or foreground substitution would weaken the apparent continuation. |
| Published later EC/WC positions are therefore wrong or fabricated. | Unsupported. This study has not inspected what each saved point lands on at its exact corresponding frame. | An exact point-to-image/source-method audit can test that narrower question. |
| The findings establish an interior failure mechanism, free fall, simultaneous support loss or deliberate intervention. | Unsupported by this unit. No coordinates, fitted motion, scale, force model or mechanism discriminator were calculated. | Those require the separate source-calibrated motion and structural workstreams. |

The strongest objection to treating this as a rejection of the published
measurement is that its authors may have used a different visible landmark,
texture, edge intersection or source representation. A straight roof edge can
remain measurable under a specified construction even when a corner vanishes;
it must not silently inherit a material-point interpretation. Conversely,
appearance continuity alone cannot authenticate that interpretation.

The earlier reproduced published-coordinate calculations remain conditional
evidence of gravity-scale curvature in those assigned coordinates. This unit
neither independently confirms that acceleration nor refutes it. It adds a
feature-identity limit and a concrete discriminating next test. No strict
cause ranking, equal odds, intent or legal conclusion follows.

## Next discriminating source test

A read-only metadata follow-up identified a better next test than simply
repeating these17 images: inspect exact saved analysis points on their own
video frames. The held Tilted project has a conditional nominal-grid relation
to the publication, not an authenticated exact publication version.

Root independently checked `../tilted-camera-source-join/project01.json`
SHA256 `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8`:

- `pointmass05`, a conditional EC candidate:43saved rows at150,156,…,402;
  only the final8,360,…,402, are saved keys. The35earlier nonkeys remain
  provenance-uncertain, not confirmed interpolations or independent marks.
- `pointmass08`, a conditional WC candidate:40saved rows at210,216,…,444,
  all saved keys. Key status can describe manual or automated marking.
- The union is50exact row frames,150,156,…,444. The existing eight saved Tilted
  stills,0,67,135,203,271,339,407,475, include none of those row frames.

The [saved-coordinate source review](../tilted-camera-source-join/source-semantics-review.md)
identifies image-space x/y, but direct identity with today's unmodified720x480
decode is still a hypothesis; historical display/aspect handling is unresolved.
No saved filters supports testing that hypothesis, not assuming it. Do not
rotate again, resize to Camera2 width, impose an aspect correction or adjust
coordinates to make a point land on a preferred landmark.

Next: prospectively declare exact native-frame extraction and a **source-guided**
overlay/inspection of all83saved rows on those50frames, with synthetic display
controls and uncertainty about raster mapping. Preserve all nonkeys and failures.
This would examine what the saved analysis represents, not create an independent
motion measurement. Denser unmarked review of the original Camera2 merging
interval is an available separate follow-up if point correspondence remains
unresolved; 701already-held native frames cover6500–7200. A metadata-only
comparison found71common saved rows with identical luma/PTS fields but20
different PNG byte hashes across extraction runs; use each file's own receipt
and verify pixel identity, not container equality.

Human/qualified review, historical timing, physical scale/projection and
automated-measurement controls remain required before consequential historical
kinematics. Neither the stored project nor a coordinate overlay supplies them.
The broader fire, structural, comparator, documentary and Luna coverage work
remains open under the unchanged charter.

## Execution and boundaries

The existing main source files and accepted engines remained read-only. Root's
first default Python invocation lacked Pillow and failed before reading images;
the existing pyenv Python/Pillow12.0.0 then verified the panels. The verifier
used bundled Python3.12.14/NumPy2.3.5/Pillow12.3.0, independently indexed pixels,
and saved a replay; root ran that exact byte-pinned block successfully. Some
combined text outputs were truncated; the remaining observer rows and relied-on
source sections were reread separately, not presumed reviewed.
The separate observer's post-freeze text critique prompted the candidate-
visibility wording above: V does not establish measurement suitability. That
critique did not independently check numerical replay or new project metadata.
The frozen observations remain unchanged. One attempted documentation patch
matched the wrong document text and failed before writing; the scoped patch
was then corrected.

The method reviewer suggested an alternative20-frame/3-target schedule while
root had already frozen17frames/4targets. That alternative was not adopted;
the original fixed contract was completed without silently adding frames.
The method reviewer viewed no images and made no new historical measurements.
Its preparatory commands included a corrected unsupported Ruby method and
absent sparse-worktree lookups, with no source edits. No failed result was
accepted as evidence.

Evidence/source-of-truth skills required the separate localization and identity
judgments, frozen records, failed-state preservation and cautious inference.
The context-distiller skill carries the exact next source test into current
status. The observed label-schema ambiguity is deduplicated under existing
Sherlock feedback IDs, local only while the designated task remains archived.
No new acquisition, private packet access, outreach, fees, filing, transmission,
canonical promotion, commit, push or whole-goal completion occurred.

Final checks actually run: scoped `git diff --check` on research navigation,
status and feedback returned0; a read-only standard-library check verified
all six unit Markdown files for trailing whitespace/newline and local-link
targets, parsed the verifier JSON, rechecked the five frozen input/review
hashes, and matched all68 comparison cells to both source tables. All passed.
Main retains its same seven pre-existing dirty tracked paths and HEAD
`499cefc8a67f4870b62d181493560f0995e0e1ee`; the main control/charter hashes
remain unchanged. This is not a whole-filesystem historical byte comparison.
Research remains on `research/sherlock-wtc7-investigation` at
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`, with intentional uncommitted WIP.
