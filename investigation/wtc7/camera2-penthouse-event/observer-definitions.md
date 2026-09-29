# Independent Stage A source definitions and baseline identity review

September 20, 2026 UTC. Research only. This separately frozen record covers
the four initially declared complete PDF pages and one complete held Camera 2
baseline image. It does not authorize Stage B, measure endpoints, or identify
a collapse cause. The unit protocol and full investigation charter control.

## Independence and actual inspection

The reviewer read the unit protocol and the PDF skill completely before this
task. Earlier local prioritization work had read the causal synthesis, Luna
reevaluation, recent STATUS and four unit reports. The published 9.3 versus
6.9/7.3-second comparison and prior qualitative appearance results were already
known. This is a separately frozen, prior-informed computational review, not
a blinded experiment, human review or independent historical source.

No root definition/identity record was read and no candidate identity or
definition finding was exchanged before saving this file. The reviewer viewed
the complete baseline at index 6593 and no other media frame in this stage.

The reviewer first viewed all four initial PNGs after finding them on disk,
before receiving root's notice that their rendering had reported a Fontconfig
error. That exposure is retained; those initial derivatives were not admitted.
After root reported two completed clean rerender commands, both exit 0 with
no stdout/stderr, the reviewer separately viewed all four complete replacement
PNGs in `source-pages-verified/`. Their four hashes happen to equal the initial
ones. Equality does not retrospectively erase the diagnostic or exposure.
The reviewer did not independently execute the PDF render commands.

## Exact inspected sources and integrity checks

Original PDFs, freshly hashed by this reviewer:

- `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1a.pdf`:
  `03c801bc1338533b54c6a64a66f074165c9429a59df11e2f58a19f5da91aef09`.
- `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf`:
  `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.

Complete admitted page views and fresh PNG hashes:

| PDF / physical page / printed page | `source-pages-verified/` file | SHA-256 |
|---|---|---|
| NCSTAR 1A / 85 / 43 | `ncstar1a-085.png` | `d2b8cb5a7f3e5129e601bc872f028eb5d142d864677d8e86bab5a4926d6ba3d6` |
| NCSTAR 1A / 86 / 44 | `ncstar1a-086.png` | `4903d1f0f9bad3d98f14cd00767c796692c8349532450ac2f57f1ab7591c9965` |
| NCSTAR 1-9A / 147 / 96 | `ncstar1-9a-147.png` | `aa27688a12c3a4d81bf3b5d91812d12a7c6e8ed247b541ac0c8b5c7b7f29439e` |
| NCSTAR 1-9A / 148 / 97 | `ncstar1-9a-148.png` | `76a76f60aabe388ad2e6f15ff17b88d04b2c11bb28f0a7f4d5a4506aa22ec7f8` |

Baseline source:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/multiview-onset-review/refine01/camera2/f006593.png`.
Fresh SHA-256 is
`39bcb70c16ccc468133edf92b3a9dc9ea43edbc5692d82d8adcfc08cc22903a8`,
matching both the selection record and `refine01/receipt.json`, which give
124462 bytes. The selection records index 6593, PTS 659301 at time base
1/2997, exact time 219767/999 seconds, and native dimensions 640 by 480.
It pins the converted source MOV to
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
The reviewer did not freshly hash or decode the MOV in this stage.

The independent lookup of `.frames[6593]` in the held timing inventory agrees
on PTS 659301 and dimensions 640 by 480; it records duration 99 units.
Fresh inventory SHA-256 is
`424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0`,
matching the selection's dependency pin. An initial attempted `jq '.[6593]'`
failed because the JSON is an object; the corrected lookup was made only
after checking its `frames` key. The failed read changed no file or output.

These checks substantiate preserved derivative identity and recorded index/PTS
relationships, not original exposure times or historical authenticity.

## Primary event definitions

NCSTAR 1A physical 85, printed 43, Table 3-1 is explicitly a comparison of
global structural-model predictions and observations for **WTC 7, Case B**.
It separates observation time from analyses with and without debris-impact
damage. Values below are transcribed source claims, not new measurements.

| Event as specified by the source | Observation (s) | With debris impact (s) | Without debris impact (s) |
|---|---:|---:|---:|
| Start of cascading failure of floors surrounding Column 79 | approximately -6, footnote a | -6.6 | -6.6 |
| Buckling of Column 79, quickly followed by Columns 80 and 81 | N/A, footnote b | -1.3 | -1.4 |
| Start of descent of east penthouse | defined as 0 | defined as 0 | defined as 0 |
| Descent of east penthouse below roofline | 2.0 | 2.4, 2.7 | 2.3, 2.6 |
| Buckling of columns across core, starting with Column 76 | N/A, footnote b | 3.5 to 6.1 | 3.2 to 13.5 |
| Initial downward motion of north-face roofline at the eastern section | 6.9 | 6.3 | 9.8 |
| Descent of east end of screenwall below roofline | 8.5 | 7.3, 7.7 | 8.7, 9.2 |
| Descent of west penthouse below roofline | 9.3 | 6.9, 7.3 | 10.6, 10.9 |

For the three below-roofline rows, the event text gives the first value's view
as northwest and below, and the second as north at roofline height. These are
view-conditioned analysis numbers; the observation column supplies only one
number per event. This page does **not** give a footage filename, source frame,
Camera 2 identifier, observer uncertainty, or an explicit per-row mapping from
the observation number to one of those two virtual views. It would therefore
be premature to call either modeled value the matched Camera 2 prediction.

Footnote a attributes the approximate -6-second value to NCSTAR 1-9 Appendix C
and Chapter 8; footnote b means not available. The first row must not be
misrepresented as a directly visible floor-failure observation merely because
it appears in the observation column. The table itself supplies the narrower
source qualification.

The proposed measured interval is consequently **start of east-penthouse
descent to descent of west penthouse below the roofline**, not west-penthouse
first motion, general loss of a raised silhouette, screenwall disappearance,
first exterior motion, or the disappearance of all rooftop structures.
The pages do not operationally define a pixel/visibility threshold for either
endpoint. Infinitesimal first motion cannot simply be equated with the first
frame an annotator can distinguish from its baseline.

## Material surrounding qualifications

NCSTAR 1A physical 86, printed 44, section 3.5.2 says the two analyses' west-
penthouse timing predictions straddled the observation, with different
structural mechanisms. Omitting the without-impact 10.6/10.9-second entries
would give an incomplete account of that published comparison. This does not
itself make either case accurate or make the two cases an uncertainty band.

The same page reports a north-face kink visible at 9.3 seconds and qualifies
subsequent simulated movement as beyond the model physics' reliability.
Numerical equality with the west-penthouse table time does not identify those
two events as one physical feature or establish their exact simultaneity.
Section 3.5.3 makes a broader positive accuracy appraisal; that is NIST's
assessment, not independently validated by these page readings.

Section 3.6 specifically identifies **Camera No. 3**, near West Street and
Harrison Street, for a separate roofline timing analysis and points to NCSTAR
1-9 Figure 5-183. That is not affirmative attribution of Table 3-1 to Camera 2,
nor a basis for transferring Camera 3 calibration to the held Camera 2 copy.

NCSTAR 1-9A physical 147, printed 96, describes directional exterior response
and includes Figure 4-41's exterior column-group plan with north/east/south/west
labels. It is not a labeled roof-penthouse plan. The text states that the model
snapshots use northeast and southwest views from above, each with two lateral
displacement contours.

Physical 148, printed 97, contains Figure 4-42's calculated perimeter-column
loads and Figure 4-43's four global-model views at 1.1 (17.1) seconds. Its arrows
identify the collapsing east-penthouse region in the model. Those elevated
northeast/southwest renderings are not the same stated viewpoints as the table's
northwest-below/north-roofline pair and do not independently register the held
Camera 2 baseline. No world-camera projection or roof-component correspondence
is inferred solely from similarly shaped model silhouettes.

## Baseline observation and identity decision

The complete baseline shows a broad dark upper facade with a comparatively
clear right vertical edge. A raised, long, nearly horizontal upper form meets
a small step down near the right side; a lower outline continues to the outer
right corner. Thick, irregular smoke obscures much of the left/top context.
Foreground structures obscure the lower building. These are descriptive image
observations only, not registered building coordinates or endpoint placements.

The visible right outer roof/parapet corner is distinct in appearance from
the raised upper endpoint/step. Neither should automatically stand for the
west penthouse. The long raised form could include screenwall and rooftop
structures in projection; the presently inspected pages do not isolate its
components. The smoke-obscured left region does not furnish an independently
defined east-penthouse tracking polygon in this limited review.

**Stage A identity gate is not met within the declared evidence.** The table's
event zero and endpoint are textually established, but these four pages plus
one baseline do not adequately map east penthouse, west penthouse, screenwall
and reference roofline to this access-copy image. The table-observation-to-
Camera 2 join is also not established. This is a bounded identification limit,
not evidence that the features cannot be identified in other held sources.

## Exact next evidence needed, not performed here

Before an endpoint pass, inspect the underlying NCSTAR 1-9 collapse-video
analysis's **Camera 2 viewpoint/frame illustration and its named roof features**,
plus an applicable labeled roof plan or photograph that separates east
penthouse, screenwall and west penthouse in this projection. Locate the exact
figure/page from the held report before rendering; do not guess a figure number
by adjacency to the separately cited Camera 3 Figure 5-183.

For comparison with the table rather than merely a new within-copy interval,
identify the source observation record/view and the virtual-camera geometry
behind its paired predictions. The table alone does not supply that mapping.
NCSTAR 1A's directly cited NCSTAR 1-9 Figure 5-205 may help distinguish kink/
east-face motion from the west-penthouse endpoint, but it was not inspected
here and must not be assumed to supply the missing Camera 2 roof labeling.

A subsequent approved source-identity follow-up can test these joins without
new media acquisition. Dense frames, clock fitting or more automatic matches
cannot substitute for a failed feature-definition gate. No additional PDF page,
media frame, playback, solver run, causal ranking, outreach, sensitive transfer
or accepted-engine state was introduced by this record.
