# Observer follow-up: held roof-geometry reference

Declared September 20, 2026 UTC after both initial Stage A records froze.
The reviewer has now read root's initial definition record and
`REFERENCE-SCOPE-02.md`; this is shared-context follow-up, not a continuation
of the independent initial freeze. Stage B remains unadmitted.

## Prospective locator and viewing limit

Use only held NCSTAR 1-9:
`/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`, freshly hashed
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

Text-locator ceiling: first 200 physical pages, looking for the exact
Figure 5-1 caption/reference and nearby explicit east/west penthouse and
screenwall roof-layout descriptions. This is a locator, not a full reading
of 200 pages. Determine actual physical page numbers before selecting any
new complete-page visual inspection. Select at most three additional pages,
recording their indices and reasons here before viewing. Root separately owns
physical 306-308, 319-321 and 323; do not duplicate their visual pass.

No new media frame, playback, external retrieval, timing measurement or solver
operation is authorized. Reuse the already viewed complete index-6593 baseline
only. The PDF skill remains in force: full-page views after clean rendering,
preserved diagnostics and separate source versus model/interpretation labels.

## Initial environment check

`command -v pdftotext && command -v pdftoppm ...` returned 1 with no output;
the remaining chained checks did not run. The reviewer then loaded the bundled
dependency paths and independently hashed the held PDF successfully. This was
an environment lookup, not a failed PDF extraction or evidence absence.

## Locator completion and declared three-page selection

The pypdf text locator completed all physical pages 1-200, reporting 797 PDF
pages in total, and returned exit 0. It matched physical 17 (contents), 134,
135 and 143 under the declared expression. No other portion of the PDF was
text-scanned by this reviewer in this pass. This does not exclude unlabeled,
image-only or differently worded geometry references elsewhere.

Before rendering/viewing, select physical **134, 135 and 143**:

- 134 supplies the Figure 5-1 clock/image-pair context and east-penthouse prose.
- 135 contains Figure 5-1's photograph/video-frame comparison.
- 143 explicitly describes both penthouses and parallel screenwalls, with
  roof-photograph captions in its extracted text.

The root was notified of these exact three physical indices before inspection.
Use the existing unit `fonts.conf` and bundled Poppler, saving new complete-page
renders under `observer-geometry-pages/`. Do not use successful process exit
alone as admission if font/render diagnostics appear.

## Execution and complete-page reading

All three pages rendered through bundled `bin/override/pdftoppm`, with
`FONTCONFIG_FILE` set to the already inspected unit `fonts.conf`. The command
created a previously absent output directory, rendered each selected page
with `-singlefile -r 110 -png`, and stopped on any failing render. Session 46687
completed with exit 0 and no stdout/stderr in its initial or terminal output.
The reviewer then viewed all three complete PNGs. Captions, text, photos,
printed page numbers and labels were legible; no missing-glyph or clipped-
layout issue was apparent. No initial warned render was used in this follow-up.

Fresh output hashes:

| Physical / printed page | PNG under `observer-geometry-pages/` | SHA-256 |
|---|---|---|
| 134 / 90 | `ncstar1-9-134.png` | `6e8a6d7ed1ee069cd5b2408a59b693c17c397f27d2b94f7a3bf2b569ba216a49` |
| 135 / 91 | `ncstar1-9-135.png` | `864eb3b0737bdf6d980e52b99430c40eb6949143e52a0613d7bff04467757139` |
| 143 / 99 | `ncstar1-9-143.png` | `85f737a2311eb171b2077acb714d2f9df8fa6265f36770ce2b6296ed5cec76f4` |

The render has not been independently repeated by this reviewer. Hashes pin
the acquired derivatives, not camera authenticity, installed dimensions or
correctness of all source annotations.

## Strongest geometry reference: physical 143, printed 99

The prose distinguishes **two fully enclosed roof structures**, called east
and west penthouses, from **two parallel screenwalls between them** enclosing
an open mechanical-equipment area. Five cooling towers are described north of
that enclosure, extending down to Floor 46 and projecting through the roof.
The building also has a reported 1.3 m (4 ft) parapet. These are different
physical/visual features, not interchangeable names for the upper silhouette.
The parapet dimension is report attribution, not our measurement.

Figure 5-8 is captioned a southwest photograph at 10:22:50 a.m. on September 11.
It labels the east penthouse at the farther/right end of the illustrated
enclosure and west penthouse at the nearer/left end. The large east roof and
smaller west enclosed volume are visibly distinct from the intervening open
equipment zone and from the surrounding building roof edge. The photograph
shows the roof from above, not the low distant Camera 2 perspective.

Figure 5-9 is a cropped northwest photograph, captioned around noon on
September 11. Its east-penthouse arrow points to the larger structure toward
the image's upper left, and its west-penthouse arrow to the smaller enclosure
lower/right. The open equipment area lies between them; additional equipment
is visible outside that enclosure toward the north side. Both images carry
New York City Police Department source/permission credits. They are two source-
attributed photographs in one report, not independently acquired originals
or two newly authenticated historical records in this investigation.

This is substantially stronger than the initial model contour/column-group
pages for **naming and distinguishing the roof structures**. It should be
used with the separately checked Camera 2 position and pre-collapse view,
not replaced by old T1/T2 labels or by inference from which part moves first.

## Figure 5-1 context: physical 134-135, printed 90-91

The caption on physical 135 identifies its paired photograph/video frame as
showing the east penthouse beginning to sink. The upper photograph carries a
Nicolas Cianca credit and an embedded displayed time; the lower frame carries
a CBS News Archives credit. Both show a different composition from our held
distant baseline: lower street/foreground geometry and facade projection
are visibly different. They are not exact Camera 2 baseline counterparts.
The caption supplies a component/phase illustration, not a pixel registration
to index 6593, original camera time or endpoint measurement by this reviewer.

Physical 134's Table 5-1 and surrounding prose separate relative visual time,
television-adjusted NIST time, FEMA reporting and LDEO reporting. NIST describes
using the photograph's timestamp, other tower photographs and comparison to an
untimed video to estimate a relative collapse time. The prose reports that the
full collapse began 6.2 seconds after the selected Figure 5-1 video frame.
That is a published image-pair/absolute-time derivation, **not** the target
east-onset-to-west-below-roofline interval, and the selected frame is not defined
as our exact east-penthouse first-motion zero. The page's statement about
approximately one-second broadcast-time uncertainty must not be silently
assigned to within-video event intervals. No new clock correction is applied.

## What this changes, and what it does not

The initial record's missing **named roof-layout reference** is now partially
resolved: the held report supplies explicitly labeled, unobstructed overhead
photographs and prose separating penthouses, screenwalls, cooling towers and
parapet. This is positive identification evidence, not another absence claim.

I have not yet read or viewed root's seven-page Camera 2 follow-up, so I do not
claim that the view mapping has passed. Combining those source pages with these
photographs may allow the raised portion/step in our baseline to be assigned
more narrowly, but named components and exact measurable boundaries remain
different propositions. Smoke can conceal part of an otherwise identified
east-penthouse region; a screenwall/roofline overlap can limit the west-
penthouse crossing event even when the west penthouse's location is known.

Acceptance should not demand a perfect 3-D camera solution merely to identify
a rooftop region. It should require a documented source/photo/view chain that
excludes the competing penthouse-versus-screenwall/parapet reading at the
chosen event boundary. If that chain succeeds, freeze an operational boundary
and visibility rule before Stage B; if it fails locally, record the particular
remaining overlap rather than treating all roof geometry as unavailable.

No additional local media frames, playback, historical endpoint estimates,
external retrieval, solver/engine state, legal promotion or causal ranking
resulted from this follow-up. The three-page selection is now complete.

An initial append-patch request omitted the `research/sherlock-wtc7-investigation/`
path segment and failed with file-not-found before changing any file. The
correct absolute target was then used; no duplicate output was created.

## Declared shared-source extension

After the three-page geometry pass, root requested an additional five complete
NCSTAR 1-9 pages: physical **306, 308, 319, 320 and 326**, from the clean
`source-pages-verified/` renders. This extension is declared before the
reviewer's viewing. Its purpose is to test whether the roof photographs,
specific Camera 2 source frame/view description and event text now support
coarse east/west-penthouse and parapet regions for a conditional pixel-event
study. No new held media frame or endpoint annotation is included.

Root shared its preliminary Camera 2/3 interpretation in the request; this
additional assessment is explicitly post-exchange critical review, not a new
blind annotation or independent frozen identity discovery. The initial
four-page record remains unchanged. Findings below will distinguish source
identity, coarse component location, exact boundary and historical timing.

## Completed five-page shared-source review

The reviewer viewed all five declared complete pages; source captions, table,
paragraphs and printed numbers were readable. The root supplied the clean
renders; the reviewer freshly hashed them but did not rerun their rendering.

| Physical / printed page | SHA-256 of `source-pages-verified/ncstar1-9-PAGE.png` |
|---|---|
| 306 / 262 | `ec72fddf038142c605799cabcface75478fa7690069659ec759e82c196a4bb11` |
| 308 / 264 | `9cc51f2c899c678f289cc4edf269a591a0d82a9218b6771dad8cba843f1c6a54` |
| 319 / 275 | `36de16f3b8e41259a9d1deee5ebe356cf2e7fdd8ebc12719fd96ef658008530f` |
| 320 / 276 | `fb6518785bcd110fdd58d54dae461ef98b03bb02dda4df95d260b406367f5db1` |
| 326 / 282 | `106250ffe8a32d58b2658adf1963f813772862be0840f6fded38c080a8c9a993` |

### Camera and observation chain

Physical 306 Table 5-2 calls Camera 2 a news camera on a high building near
midtown Manhattan, due north of WTC 7, with the entire sequence and higher
magnification than Camera 1. It separately locates Camera 3 near West and
Harrison Streets. The preceding paragraph describes matching events to place
nine clips on a common timeline, estimates a maximum assignment uncertainty
of six frames or 0.2 seconds, and defines zero by east-penthouse descent. This
is NIST's method/uncertainty statement; it does not establish our converted
copy's original clock or justify blindly adding independent 0.2-second errors
to every endpoint. Nor does it replace source caption-specific uncertainties.

Physical 308 Figure 5-185 is explicitly the pre-descent Camera 2 north-face
view with adjusted intensity levels. Its facade, rooftop step, distant right
background buildings, nearer skyline and left-edge vertical strip strongly
match the composition of the one held baseline already viewed. This is a
positive **scene/view-family correspondence**, not proof of the identical
source frame, unchanged crop/photometry, original tape or complete edit history.
Figure 5-186 separately illustrates Camera 3; the two must not be exchanged.

Physical 319 says the screenwall/west-penthouse tops were last seen behind the
north parapet in the Camera 3 view at 8.0 plus or minus 0.1 seconds. It expressly
explains that setback and parapet obstruction mean this does not show the
structures fully sinking through the roof. The same page says the distant
Camera 2 view still showed the screenwall and west penthouse above the roof
and parapet at the later paired image. This is affirmative source explanation
of a **view-dependent endpoint**, not an unexplained contradiction to the 9.3-
second distant-view value.

Physical 320 Figure 5-202 supplies the paired Camera 2/Camera 3 images at
8.1 plus or minus 0.1 seconds, identifying their source clips as Figures 5-185
and 5-186. The prose describes the west-penthouse roofline still visible,
sloping down from its western edge, in a later distant image at 9.0 seconds.
That later Figure 5-203 was not visually inspected by this reviewer; the prose
is the support for this attributed statement here.

Physical 326's prose says the entire west penthouse had disappeared below the
north-wall parapet in the distant view, around 9.3 seconds. Figure 5-208 on the
same page is a **10.0 plus or minus 0.1 second** paired Camera 2/Camera 3 image,
not an illustration captioned 9.3 seconds. The paragraph-plus-explicit-clip
chain connects the approximate 9.3 statement to the distant Camera 2 endpoint,
but does not supply the exact 9.3 frame or our own independent uncertainty.
The 9.3 value must therefore remain an attributed timing claim until new
annotation actually tests it. The geometry of the virtual model views in
Table 3-1 is not authenticated merely by making this historical-view join.

### Updated identity decision: partial pass, not a permanent generic block

The combination of Table 5-2, Figure 5-185, the labeled roof photographs on
physical 143 and the paired-event prose now supports these **coarse regions**
in the held baseline: east-penthouse area toward image-left, the connecting
screenwall span, west-penthouse area toward image-right, and the north facade's
roof/parapet boundary in front of them. This is materially stronger than the
initial four pages alone. No exact polygon, measured material point or unseen
component boundary is invented here. The upper raised region/step on the
right is a plausible west-penthouse-associated endpoint candidate, distinct
from the lower outer north-facade/parapet corner.

It is scientifically reasonable to proceed to a **separately declared
conditional pixel-event test** with this source-informed identity, rather than
requiring a perfect 3-D pose solution before any observation. The next task
should first freeze coarse candidate regions and feature/occlusion rules from
the baseline/source geometry, then preserve uncertainty in whether the actual
event remains visible. This partial pass is not Stage B execution permission
from this observer and does not satisfy actual human/specialist acceptance.

The measurable endpoint should be the last defensibly resolved west-penthouse-
associated upper outline relative to the **contemporaneous local north
parapet/roof edge**. A fixed horizontal line from the initial frame is not a
valid reference while the facade itself descends and deforms. The screenwall's
earlier disappearance, dust, a parapet corner, and the western end of a sloping
roof contour must be separately labeled rather than selected opportunistically
to reproduce 9.3 seconds. The endpoint is loss of visibility in this projection;
it is not direct proof of complete sinking through the roof or internal failure.

The strongest practical objection is unresolved censoring: smoke can hide
the east-penthouse onset, and smoke/overlap/limited resolution may hide the last
west-penthouse edge. Even correct coarse identities cannot manufacture adjacent
pre/post frames that are optically observable. Stage B must allow interval
bounds or non-identifiability, not presume both endpoints can be timed precisely.
Actual file PTS, source processing and observer uncertainty remain separate
from the report's historical relative clock.

This completes eight newly viewed NCSTAR 1-9 pages in the shared follow-up
(three geometry/context pages plus the five-page extension). Together with the
initial stage it is twelve complete PDF-page views, with the initial four
also viewed once as unadmitted warned renders. Only one held media baseline
was viewed throughout these stages. No historical endpoint, causal ranking,
force estimate, accepted-engine state or legal-record change is asserted.
