# CBS candidate source screen — stage1 result

2026-09-28. Research-only. **The fixed samples from Clips1–2 did not establish
a scene/view match to NCSTAR1-9 Figures5-141/142/143.** Both readers reached
that bounded result independently. This is sampled non-recovery, not proof
that either complete clip lacks a matching view. The other six candidates
remain required; no collapse-cause ranking changes.

## What was actually observed

| Candidate | Fixed coverage per reader | Positive scene description | Result and important limit |
|---|---|---|---|
| Vince Demetri Clip1 | 9 of418frames; indices0,53,105,157,209,261,313,365,417 | Distant antenna-topped tower, smoke and broadcast overlay; additional overlapping forms in the last sample | No reference-specific match. Last-sample mixed appearance remains unresolved; no authenticated edit mechanism or whole-file exclusion. |
| Vince Demetri Clip2 | 9 of809frames; indices0,101,202,303,404,505,606,707,808 | Foreground reporting/emergency-vehicle view, followed in the samples by an upper banded building/roof view | No reference-specific match. Lower facade and local detail are cropped/obscured; possible same-building resemblance does not establish the requested view or a common original recording. |

The sought relationships were fixed before these candidate views: local facade
corner/band/grid ordering; distinctive foreground sign/corner/overhang relations;
and the close corner/irregular outlined-area/lower-grid neighborhood. CBS text,
smoke color and generic horizontal bands were not sufficient matching cues.
Neither reader recovered the required pair of distinctive spatial relationships
for any reference. A catalogue folder/operator label is not original-camera
authentication. These samples include broadcast packaging, not automatically
raw operator footage.

The strongest counterargument is coverage:409frames in Clip1 and800 in Clip2
were not visually inspected. A matching shot could occur between samples;
Clip1's mixed final sample further limits any whole-file conclusion. The
source-identification question remains open rather than answered negatively.

## Reader agreement and retained distinctions

Both readers froze three-reference descriptions before candidates, saved
their complete Clip1 notes before viewing Clip2, and froze both candidate
records before exchanging new judgments. Each viewed18candidate images once,
with no extra frames, crops, enhancement, reference rereads or audio. They
share the same acquired media/toolchain and prior familiarity; this is not
independent historical corroboration or a blinded test.

- [Root Clip1](stage1/root-clip1.md) and [separate reader Clip1](stage1/reader-clip1.md)
  both record a different tower composition and the unresolved final mixed
  appearance. The latter explicitly scores the last sample unresolved for
  all three references, rather than silently assigning a negative label.
- [Root Clip2](stage1/root-clip2.md) calls the missing close-up detail unresolved
  as a source of143; the [separate reader](stage1/reader-clip2.md) calls the
  positively visible composition incompatible with the particular reference
  view while also leaving hidden lower detail untested. Preserve both levels:
  the sampled view differs, but obscured/cropped detail is not disproved.
  Root's tentative same-building compatibility is not a jointly verified
  identification and does not bridge the missing scene/source join.

No original observation was rewritten to produce agreement. These differences
do not change the common narrow outcome: no supported association recovered
within the declared sample. Neither finding assesses actual glazing material,
fire size/temperature/duration, lack of fire, event clocks, sound, acceleration,
support loss, intent or the relative probability of collapse mechanisms.

## Reproducibility and preserved failure

The [protocol](PROTOCOL.md), [execution log](execution.md),
[acquisition receipt](stage1/acquisition.json), and
[artifact audit with runnable checker](stage1/artifact-review.md) preserve the
complete source/selection/derivative chain. Both source copies matched their
declared sizes,152,769,456bytes total. A first Clip2 transfer timed out with
partial bytes despite HTTP200; it was preserved and excluded, then the one
permitted full retry completed. No failed evidence was silently discarded.

Fresh parent14tests and adapter25tests passed. A separate selection oracle
checked2,509synthetic sequences/22,581targets. Historical preparation and two
native extraction runs passed unchanged strict diagnostics; all18 selected
frame records and36PNG/RGB hashes reproduced. The independent artifact audit
and root's rerun passed. The code/artifact reviewer disclosed earlier authorship
of the inherited helper: separate selection logic and readback checks are not
a fully independent decoding implementation. Software success is not scene
or historical validation.

Stored rasters are720×480, SAR8:9, bottom-field-first. No display-aspect or
field transform was applied; topology/ordering, not metric shape or motion,
guided this screen. Exact encoded clocks are retained separately for each
clip and are not authenticated camera/exposure times.

## Next discriminating work

Continue the already declared candidate set in stages3–4,5–6,7–8, retaining
the same frozen reference descriptions and sampling/decision rule. Do not
prefer or skip a child on the basis of its number or these first outcomes.
The next stage is Clips3–4, using their exact metadata IDs and the reviewed
adapter after scoped integrity/runtime checks. Any eventual supported scene
match leads to a separately specified exact-frame/field/transform/source test,
not automatic acceptance of report processing or a historical clock.

Stage1's screen and [synthesis review](stage1/synthesis-review.md) are complete;
final documentation checks are recorded in the execution log. The complete eight-item
study and full charter remain incomplete. The actual-human window-state
review is still pending, as are the other separately recorded gates. No
combined matrix save, accepted Sherlock/Faraday finding, legal promotion,
external disclosure, commit or push. The recurring acquisition/schema lesson
was deduplicated locally under SFB-005; feedback delivery remains pending the
archived task's routing decision, not falsely reported as sent.
