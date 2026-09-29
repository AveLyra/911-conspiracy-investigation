# UAF common-observable source reading - standalone freeze

2026-09-20 UTC. Read-only source review under [PROTOCOL.md](PROTOCOL.md).
Prior-informed AI interpretation, not a new historical measurement, engineering
opinion, solver reproduction or blinded observation. Root/NIST notes were not
read, and no substantive findings were exchanged before this record was saved.
This note supplies only the UAF side of the eventual comparison; it does not
authenticate equivalence with a particular NIST camera or native case.

## Source admission and actual coverage

Source: March 2020 final report, Hulsey, Quan and Xiao, *A Structural Reevaluation
of the Collapse of World Trade Center 7*, preserved at
[uaf-final-2020.pdf](../uaf-final-method-audit/source/uaf-final-2020.pdf).
Fresh byte/hash check: 45,196,602 bytes, SHA256
`f3a001ab68dcc6b6e230456aac4729613740336796c1b2515671141589c38bfa`.
It equals the before/after source pins in the existing render receipt and the
start record. Receipt SHA256
`aec3b332d38c90ec682e46eac8684a551ad9e0f7fb72ca57de1b53c4d7d32749`;
start SHA256
`980ecc4fc95a7ca3856ced2257537bb16c906f8d5857f13689649225e916537d`.

The read-only Python admission command used `hashlib`, `json` and Pillow under
`/Users/admin/.pyenv/versions/3.13.7/bin/python3`. It compared source bytes/hash
with all three recorded source pins, each selected PNG's bytes/hash with
`receipt.products`, and its decoded dimensions with `receipt.pages`. All passed,
exit 0. All ten were single-image RGB, 1275 by 1650 pixels; each relevant recorded
warning string was empty. This rechecks preserved bytes/decodability, not the
historical renderer's correctness or source truth. No rerender was performed.

I displayed all ten complete original-size images once, in this order:
physical 105,106,107,108,118,119,120,121,122,123; printed 92,93,94,95,105,106,107,
108,109,110. Files are `../uaf-final-method-audit/render01/pNNN.png`. No failed
displays, repeats, extra pages, crops or enhancements. Main prose, captions,
page numbers and principal plot labels are readable. Embedded screenshot text
is unevenly legible; especially the NIST image's tiny overlay in Figure 4.1(b)
must not provide an exact timing value. No clipping or missing main text was
observed. A paragraph continues beyond selected physical108; I do not silently
complete it from an unviewed page.

## Common case and alignment limits

Printed94, section4.2, says east-penthouse analyses and west-penthouse/north-roofline
analyses were separate sets. It states penthouse beam-column joints were treated
as rigid, affecting the bottom-corner appearance; all collapse analyses include
six southwest exterior column losses attributed to NIST's debris account.
Displayed displacements are expressly exaggerated, not scaled to building
geometry. These are reported assumptions, not freshly checked native settings.

Printed95/105, sections4.2.2/4.6, prescribe simultaneous loss of all core columns
over eight stories, then all exterior columns over eight stories 1.3 seconds
later. Printed95 specifies Floors12-19; printed108 additionally describes
Floors6-13 as a separate alternative. That delay is an input between hidden
support events, not an independently predicted visible penthouse-to-roof interval.

Figure4.16 (printed105) is a **different** hypothetical Columns76-81 case, captioned
dynamic and tipping southeast, highly amplified. Its screenshot labels ACASE2
and time5.4. Figure4.17 (printed106) shows the core/exterior case in two selected
perspectives, also labels ACASE2, and displays time1.7. Distinct screenshot model
labels include Penthouse46 versus Penthouse49. Shared case label ACASE2 does not
identify the same native configuration. No file hash, native clock-zero event,
camera calibration, video-frame ID or mapping of either screenshot clock into
the published observational clock is supplied on these selected pages.

Printed106 says a time-dependent acceleration function accounted for impact
resistance. Its equation, provenance, imposed-versus-derived components and
any parameter calibration are not supplied here. The manuscript calls the
response computed; this does not establish that every compared quantity was
an unfitted prediction. Conversely, absence of the function here does not prove
that the entire trajectory was imposed. Do not transfer a general P-delta or
software-capability statement into an unverified configuration of this case.

## 1. East-penthouse onset

- **Source/event:** printed92, section4.1 item1, reports east-penthouse collapse
  beginning approximately6.9 seconds before descent of the north-face roofline.
  It cites the authors' combined review of video and NIST/FEMA reports, not an
  identified new camera measurement. Visible onset criterion, particular feature,
  frame pair, original clock and error bound are absent here.
- **Model role:** printed94-95, sections4.2.1/4.3, hypothesize failure of Columns79-81
  and vary the removed height band. Section4.3 expressly calls these results
  linear static. This examines conditional deformation after removals, not a
  reproduced elapsed-time prediction for onset from an initiating fire.
- **Alignment/comparability:** a narrative relative offset to north-roof onset
  is present; a native-to-video time transform is not. A structural column-loss
  event, visible first motion and disappearance below a roofline are not aliases.
  No independently predicted6.9-second interval is established by these pages.
- **Falsifier/prerequisite:** identify the exact case, tracked penthouse point,
  camera, onset threshold and independently bounded frame timing. A fixed-case
  predicted onset or associated deformation outside those bounds would challenge
  that case. A static response cannot by itself settle dynamic propagation or
  the historical height of first failure. Printed109's stronger historical/fire
  exclusion is an inference, not an additional observation or timing result.

## 2. West-penthouse passage below a defined roofline

- **Source/event:** printed92, section4.1 item2, reports the screen wall and west
  penthouse **beginning** collapse approximately0.5-1 second before north-roofline
  descent. It combines two components. It does not define entire-penthouse
  passage below a particular parapet, last visibility or final disappearance.
- **Model role:** sections4.2.2/4.6 and Figure4.17 concern the shared core/exterior
  removal case. The1.3-second input delay is not itself a computed west-penthouse
  endpoint. No separately tabulated west-penthouse crossing time appears here.
- **Comparability:** **not numerically comparable** to a roofline-passage time
  without identifying component, parapet, occlusion rule and clock. Do not
  subtract the source's onset interval from another report's disappearance time
  and call the difference model error. The two chosen video perspectives are
  not an authenticated mapping to named NIST cameras in this selection.
- **Falsifier/prerequisite:** a projected same-component crossing from the fixed
  native case and a bounded corresponding video crossing could reject that
  output. No failure to match this unreported endpoint is demonstrated here;
  conversely, no successful endpoint prediction is demonstrated.

## 3. North-facade onset and trajectory

- **Source/event:** printed92 reports approximately2.25-2.5 seconds of free fall,
  approximately105 feet/eight stories, attached sheathing and no visible
  differential movement during that interval. These are attributed observations,
  not this review's measurements. Printed92-93 separately acknowledges window
  breakage12-15 floors beneath the east penthouse; “wholly unaffected exterior”
  is not the paper's consistent account.
- **Case/feature:** printed106-108, Figures4.18-4.20, compare SAP2000 velocity and
  acceleration with Chandler2010. Printed108 identifies the tracked modeled
  feature as the **northwest top corner**, not the whole building's center of
  mass. Figure4.19 shows a tracked image corner; no calibrated three-dimensional
  component or independent raw-coordinate table is supplied here.
- **Quantitative role/alignment:** Figure4.20 overlays red simulation and green
  reported measurement, with a2.5-second annotation and a free-fall trend line.
  It is positive reported agreement, not an independently computed residual.
  Its plotted elapsed clock is not tied here to east-penthouse onset, screenshot
  time1.7, or an explicit common zero. The prescribed removal timing, chosen
  perspectives and resistance function require provenance before this can be
  designated unused-data validation. No new digitization or fitted shift made.
- **Nonuniqueness/falsifier:** printed108 says Floors12-19 and Floors6-13 removals
  yielded identical downward velocity/acceleration for this corner. Thus even
  exact corner agreement does not identify removal height, much less initiation
  mechanism or intent. Test a fixed case against additional independently defined
  features and full time histories with justified uncertainty; a systematic
  incompatible residual could reject that case without rejecting every removal
  scenario. Figure4.21's CBS attribution and Floors17-47 uniform-motion inference
  do not authenticate the camera, its clock, all concealed floors or a rigid COM.

## 4. Lateral deformation

- **Source/features:** printed92-93, Figures4.1(a,b), criticizes differential
  exterior deformation in NIST images. Printed105, Figure4.16, predicts amplified
  southeast tipping after hypothetical loss of Columns76-81. Printed110 contrasts
  that response with the authors' “straight-down” characterization. These are
  several different quantities: local exterior distortion, gross tipping and
  the observed path of an identified corner must remain separate.
- **Role/comparability:** no metric east/north displacement vector, calibrated
  camera projection, corresponding-time lateral trace or uncertainty is supplied
  for the successful core/exterior case on these pages. The general displacement
  exaggeration warning prevents reading a screenshot angle as a world angle.
  “Straight-down” cannot silently mean zero lateral motion of every feature,
  zero internal deformation or all debris within the original footprint.
- **Falsifier/prerequisite:** obtain each native output's physical scale,
  orientation, feature IDs and common event time, then project the same features
  into calibrated video views. Contrary predicted direction or amplitude beyond
  justified uncertainties could reject a specified case. Missing calibration
  does not erase the authors' stated morphological objection; it limits how
  quantitatively or universally it can be asserted.

## 5. North-roof kink appearance

- **Source/event:** printed95, section4.2.2, says a kink appears in video as the
  structure begins collapsing. It discusses an interpretation involving core
  failure and inward buckling/pulling of exterior columns, then expressly states
  the attempted simulation could not reproduce this phenomenon. The proposed
  causal interpretation is not an observed cause.
- **Model role/alignment:** **an admitted unachieved target**, not a successful
  prediction. No kink magnitude, feature coordinate, onset threshold or absolute
  or relative timestamp is provided here. The text attributes difficulty to
  time-dependent buckling/numerical requirements; that is not an independently
  demonstrated impossibility or a verified configuration of every model.
- **Falsifier/prerequisite:** a defined curvature/angle change in an identified
  roof segment, timed and projected consistently, could test an amended fixed
  case. Matching its onset and shape without retuning would add evidence beyond
  the present fit; persisting incompatibility would limit that case's complete-
  collapse match. The manuscript's “almost exactly” language must retain this
  explicit failure, rather than treating the three chosen features as exhaustive.

## Scope disposition and verification boundary

These pages support reported conditional trajectory agreement, declared removal
inputs, explicit nonuniqueness, and a kink target not reproduced. They do not
provide five independently timed predictions, a common camera/time registration,
or an operational cause. No qualitative causal ranking is made. No page expansion
was needed to record these limits; native files and directly relevant missing
definitions remain bounded prerequisites rather than inferred values.

After saving, the read-only Python check exited0: both local links resolved,
no trailing whitespace; source plus all ten PNG pins and receipt/start hashes
were unchanged. Source/render hashes and warnings above were checked freshly;
the earlier full rendering integrity replay was **not rerun** in this unit.
Main/raw sources, old derivatives and all other reviewers' records remain untouched.
